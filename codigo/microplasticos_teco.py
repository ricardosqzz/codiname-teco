# ENTRADAS: config/microplasticos.json; caminhos relativos à raiz TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json.
# GRADE: grade_resultados e influencia_500m; chaves GRID_ID/BACIA; POP_DENS, SEM_REDE, VIAS_KM, AREA_KM2, VALIDO.
# CENSO: analise_setores; setor_id, dom_set (DPP ocupados), set_km2 (área original), geometria recortada.
# LIXO: CSV IBGE, setor e V00397-00402; X é sigilo, não zero; denominador dom_set.
# CONTEXTO: GeoJSON IDE-Sisema e CSV SINIR; atividade, processo, situação, plano e coleta seletiva; sem CPF/nome pessoal nas saídas.
# SAÍDAS: output/07_microplasticos; microplasticos.gpkg, tabelas, rasters, auditoria; MP_INDEX, MP_CLASS, MP_K, MP_MORAN.
# NOVA ENTRADA: definir a agregação abaixo e acrescentar campo, transformação e pesos em config/microplasticos.json.
from pathlib import Path
from collections import deque
import json,hashlib,datetime,unicodedata,re
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from scipy.spatial import cKDTree,distance
from scipy.sparse import csr_matrix
from scipy.stats import spearmanr
from scipy.optimize import linear_sum_assignment
from caminhos_teco import raiz_projeto
from analise_espacial_teco import fitkm,silhouette,ari
from multivariada_teco import moran_w
R=raiz_projeto();C=json.loads((R/'config/microplasticos.json').read_text('utf8'));O=R/C['saida'];G=O/'microplasticos.gpkg'
for d in ['tabelas','rasters','auditoria','figuras']:(O/d).mkdir(parents=True,exist_ok=True)
SEED=C['semente'];D8={1:(-1,1),2:(-1,0),3:(-1,-1),4:(0,-1),5:(1,-1),6:(1,0),7:(1,1),8:(0,1)}

# Escrita e identificação
def norm(x):return ''.join(c for c in unicodedata.normalize('NFKD',str(x)) if not unicodedata.combining(c)).lower()
def csv(df,name):df.to_csv(O/'tabelas'/f'{name}.csv',sep=';',index=False,encoding='utf-8-sig')
def layer(g,name):
    if len(g):g.to_file(G,layer=name,driver='GPKG')
def digest(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

# Destinação domiciliar e limites de sigilo
def waste(sectors):
    fields=[f'V{i:05d}' for i in range(397,403)];ids=set(sectors.setor_id.astype(str));parts=[]
    for chunk in pd.read_csv(R/C['ibge_lixo'],sep=';',usecols=['setor',*fields],dtype=str,chunksize=30000):
        sub=chunk[chunk.setor.isin(ids)]
        if len(sub):parts.append(sub)
    raw=pd.concat(parts,ignore_index=True).rename(columns={'setor':'setor_id'});assert raw.setor_id.is_unique
    csv(raw,'ibge_lixo_recorte_original')
    s=sectors[['setor_id','bas_id','mun_nome','dom_set','set_km2','geometry']].merge(raw,on='setor_id',how='left',validate='many_to_one')
    vals=s[fields].apply(pd.to_numeric,errors='coerce');total=pd.to_numeric(s.dom_set,errors='coerce')
    known_yes=vals[fields[:2]].sum(axis=1,min_count=1).fillna(0);known_no=vals[fields[2:]].sum(axis=1,min_count=1).fillna(0)
    yes_exact=vals[fields[:2]].notna().all(axis=1);no_exact=vals[fields[2:]].notna().all(axis=1)
    bad=(known_yes+known_no>total+1e-6)|(total<0)|(vals.lt(0).any(axis=1))|total.isna()|~s.setor_id.isin(raw.setor_id)
    lo=known_no.copy();hi=(total-known_yes).clip(lower=0)
    lo=np.where(yes_exact,total-known_yes,lo);hi=np.where(no_exact,known_no,hi)
    bad|=np.asarray(lo)>np.asarray(hi)+1e-6
    s['HH_TOTAL']=total;s['UNC_LO']=np.where(bad,np.nan,lo);s['UNC_HI']=np.where(bad,np.nan,hi)
    s['UNC_MID']=(s.UNC_LO+s.UNC_HI)/2;s['WASTE_LO']=100*s.UNC_LO/total.where(total>0);s['WASTE_HI']=100*s.UNC_HI/total.where(total>0)
    s['WASTE_PCT']=(s.WASTE_LO+s.WASTE_HI)/2;s['WASTE_EST']=((s.UNC_HI-s.UNC_LO)>1e-8).astype(int)
    s['WASTE_QA']=np.where(bad,'inconsistent_or_missing',np.where(total==0,'no_households',np.where(s.WASTE_EST==1,'interval_midpoint','exact_combined')))
    s['ORIG_KM2']=s.set_km2;s['PART_KM2']=s.area/1e6;s['BACIA']=s.bas_id
    for f in ['HH_TOTAL','UNC_LO','UNC_HI','UNC_MID']:s[f+'_AL']=s[f]*s.PART_KM2/s.ORIG_KM2
    sums=s.groupby('BACIA')[['HH_TOTAL_AL','UNC_LO_AL','UNC_HI_AL','UNC_MID_AL']].sum(min_count=1)
    sums['WASTE_LO']=100*sums.UNC_LO_AL/sums.HH_TOTAL_AL;sums['WASTE_HI']=100*sums.UNC_HI_AL/sums.HH_TOTAL_AL
    csv(sums.reset_index(),'residuos_por_bacia');layer(s,'waste_census')
    return s

# Agregação nas vizinhanças de cálculo
def aggregate(g,circles,s):
    pieces=gpd.overlay(circles[['GRID_ID','BACIA','geometry']],s[['setor_id','BACIA','HH_TOTAL','UNC_LO','UNC_HI','ORIG_KM2','geometry']].rename(columns={'BACIA':'SRC_BAS'}),how='intersection',keep_geom_type=True)
    pieces=pieces[pieces.BACIA==pieces.SRC_BAS].copy();pieces['KM2']=pieces.area/1e6
    pieces['HH']=pieces.HH_TOTAL*pieces.KM2/pieces.ORIG_KM2
    for f in ['UNC_LO','UNC_HI']:pieces[f+'_ALLOC']=pieces[f]*pieces.KM2/pieces.ORIG_KM2
    pieces['OBS_HH']=pieces.HH.where(pieces.UNC_LO.notna()&pieces.UNC_HI.notna(),0)
    sums=pieces.groupby(['GRID_ID','BACIA'])[['HH','OBS_HH','UNC_LO_ALLOC','UNC_HI_ALLOC']].sum(min_count=1)
    g=g.merge(sums,on=['GRID_ID','BACIA'],how='left',validate='one_to_one')
    g['WASTE_LO']=100*g.UNC_LO_ALLOC/g.OBS_HH.where(g.OBS_HH>0);g['WASTE_HI']=100*g.UNC_HI_ALLOC/g.OBS_HH.where(g.OBS_HH>0)
    g['WASTE_PCT']=(g.WASTE_LO+g.WASTE_HI)/2;g['WASTE_COV']=100*g.OBS_HH/g.HH.where(g.HH>0)
    g['WASTE_DENS']=(g.UNC_LO_ALLOC+g.UNC_HI_ALLOC)/2/g.AREA_KM2
    g['SEWER_DENS']=g.SEM/g.AREA_KM2
    g['ROAD_DENS']=g.VIAS_KM/g.AREA_KM2
    g['MP_VALID']=(g.VALIDO.astype(bool)&g[C['variaveis'][0]['campo']].notna()&(g.WASTE_COV>=99.9)&g.WASTE_PCT.notna()).astype(int)
    return g

# Catálogos públicos e triagem por atividade
def context(b,sectors):
    raw=R/C['originais'];records=[];region=[];union=b.geometry.union_all()
    for code in ['licencas_sla','licencas_historicas']:
        a=gpd.read_file(raw/(code+'.geojson')).to_crs(31983)
        for i,r in a.iterrows():
            current=code=='licencas_sla';act=str(r.get('des_atvpri' if current else 'atividade',''));process=str(r.get('n_processo' if current else 'processo',''))
            text=norm(act);candidate=bool(re.search(r'plastic|termoplastic|borracha|textil|lavander|resina|polimer',text))
            loc=[str(q.id) for q in b.itertuples() if q.geometry.intersects(r.geometry)]
            rec={'REC_ID':f'{"SLA" if current else "HIS"}{i+1:05d}','SOURCE':code,'PROCESS':process,'ACT_CODE':str(r.get('cod_atvpri' if current else 'cod_dn','')),'ACTIVITY':act,'STATUS':str(r.get('status_pro' if current else 'modalidade','')),'VALIDITY':str(r.get('data_val' if current else 'validade','')),'ISSUED':str(r.get('data_emiss' if current else 'ano','')),'MP_CAND':int(candidate),'BACIA':'|'.join(loc),'REVIEW':'verify_process_and_operation','URL':str(r.get('link','')) if current else 'https://www.siam.mg.gov.br/siam/processo/index.jsp','geometry':r.geometry}
            region.append(rec)
            if loc:records.append(rec)
    lic=gpd.GeoDataFrame(records,crs=31983);layer(lic,'licensing_screening');csv(lic.drop(columns='geometry'),'licencas_triagem')
    csv(pd.DataFrame([{k:v for k,v in r.items() if k!='geometry'} for r in region]),'licencas_contexto_20km')
    facilities=[]
    for code in ['aterros_sanitarios','transbordo','disposicao_precaria']:
        p=raw/(code+'.geojson');data=json.loads(p.read_text('utf8'))
        if not data.get('features'):continue
        a=gpd.read_file(p).to_crs(31983)
        for i,r in a.iterrows():
            loc=[str(q.id) for q in b.itertuples() if q.geometry.intersects(r.geometry)]
            facilities.append({'REC_ID':f'{code[:3]}{i+1:04d}','TYPE':code,'MUNICIPAL':str(r.get('municipio','')),'STATUS':str(r.get('regul_amb',r.get('situacao',''))),'SHARED':str(r.get('compart','')),'BACIA':'|'.join(loc),'IN_BASIN':int(bool(loc)),'CHECK':'acceptance_and_status_unverified','geometry':r.geometry})
    fac=gpd.GeoDataFrame(facilities,crs=31983);layer(fac,'waste_management');csv(fac.drop(columns='geometry'),'instalacoes_residuos_contexto')
    plans=gpd.read_file(raw/'plano_residuos_2024.geojson').to_crs(31983);plans=plans[plans.intersects(union)].copy()
    plans=plans[['nome','geocodigo','pmgirs_24','colsel_24','tiprsu_24','geometry']];layer(plans,'municipal_waste_plans');csv(plans.drop(columns='geometry'),'planos_municipais_2024')
    names={norm(x) for x in sectors.mun_nome.unique()};sinir=[]
    for p in (raw/'sinir_2025').rglob('Municipal*.csv'):
        if not any(x in p.name for x in ['Diagnostico','Passivo','Compartilhadas']):continue
        x=pd.read_csv(p,sep=';',encoding='latin1',dtype=str)
        x.columns=[c.encode('latin1').decode('utf8',errors='replace') if 'Ã' in c or '\x83' in c else c for c in x.columns]
        x['Declarante']=x['Declarante'].map(lambda v:v.encode('latin1').decode('utf8',errors='replace') if isinstance(v,str) and 'Ã' in v else v)
        x=x[(x['UF Declarante']=='MG')&x['Declarante'].map(norm).isin(names)].copy()
        if len(x):
            for f in x:
                x[f]=x[f].map(lambda v:v.encode('latin1').decode('utf8',errors='replace') if isinstance(v,str) and ('Ã' in v or '\x83' in v) else v)
            x['SOURCE_TABLE']=p.stem;csv(x,'sinir_'+('diagnostico' if 'Diagnostico' in p.name else 'passivos' if 'Passivo' in p.name else 'compartilhados'));sinir.append(x)
    return lic,fac,plans,{'licencas_bacias':len(lic),'licencas_candidatas':int(lic.MP_CAND.sum()),'instalacoes_regionais':len(fac),'instalacoes_bacias':int(fac.IN_BASIN.sum()),'municipios_sinir':sorted(set(v for x in sinir for v in x.Declarante.unique()))}

# Multicritério e k-means
def classify(g):
    idx=g.index[g.MP_VALID==1];defs=C['variaveis'];features=[v['campo'] for v in defs];raw=g.loc[idx,features].to_numpy(float);x=raw.copy();params=[]
    for j,v in enumerate(defs):
        if v['transformacao']=='log1p':x[:,j]=np.log1p(x[:,j])
        lo,hi=x[:,j].min(),x[:,j].max();params.append({'campo':features[j],'transformacao':v['transformacao'],'min':lo,'max':hi});x[:,j]=(x[:,j]-lo)/(hi-lo) if hi>lo else 0
        g['MP_N'+str(j+1)]=np.nan;g.loc[idx,'MP_N'+str(j+1)]=x[:,j]
    csv(pd.DataFrame(params),'normalizacao');models={};ks=[];scenarios=[];scores={}
    for code,ww in C['cenarios'].items():
        w=np.asarray(ww);wx=x*np.sqrt(w/w.sum());score=100*(x@w)/w.sum();scores[code]=score;g['MP_'+code]=np.nan;g.loc[idx,'MP_'+code]=score
        for k in C['k_testados']:
            loss,cent,lab=fitkm(wx,k,SEED+100*int(code[1:]),starts=20);sil=silhouette(wx,lab);sizes=np.bincount(lab,minlength=k)
            ks.append({'scenario':code,'k':k,'silhouette':sil,'min_n':int(sizes.min()),'inertia':loss});models[code,k]=(cent,lab)
        best=max([r for r in ks if r['scenario']==code],key=lambda r:r['silhouette']);scenarios.append({**best,'weights':ww})
    k0=next(s['k'] for s in scenarios if s['scenario']=='S0');base=models['S0',k0][1];order=sorted(set(base),key=lambda c:scores['S0'][base==c].mean());lookup={a:i for i,a in enumerate(order)};base=np.array([lookup[a] for a in base]);stability=[]
    for rec in scenarios:
        code=rec['scenario'];lab=models[code,k0][1];cont=np.bincount(base*k0+lab,minlength=k0*k0).reshape(k0,k0);rr,cc=linear_sum_assignment(-cont);lookup=dict(zip(cc,rr));lab=np.array([lookup[v] for v in lab]);stability.append(lab==base)
        rec.update(ARI_base=ari(base,lab),rho_score=spearmanr(scores['S0'],scores[code]).statistic,k_reference=k0)
        g['MK_'+code]=0;g.loc[idx,'MK_'+code]=lab+1
    g['MP_INDEX']=g.MP_S0;g['MP_CLASS']=0;g.loc[idx,'MP_CLASS']=np.clip(np.ceil(g.loc[idx,'MP_INDEX']/20).astype(int),1,5)
    cuts=np.quantile(scores['S0'],[.2,.4,.6,.8]);g['MP_QUINT']=0;g.loc[idx,'MP_QUINT']=np.searchsorted(cuts,scores['S0'],side='left')+1
    g['MP_K']=g.MK_S0;g['MP_STAB']=np.nan;g.loc[idx,'MP_STAB']=100*np.mean(stability,axis=0)
    p=params[2];lower=x.copy();upper=x.copy();lower[:,2]=(np.log1p(g.loc[idx,'UNC_LO_ALLOC']/g.loc[idx,'AREA_KM2'])-p['min'])/(p['max']-p['min']);upper[:,2]=(np.log1p(g.loc[idx,'UNC_HI_ALLOC']/g.loc[idx,'AREA_KM2'])-p['min'])/(p['max']-p['min'])
    lower[:,2]=np.clip(lower[:,2],0,1);upper[:,2]=np.clip(upper[:,2],0,1)
    g['MP_LO']=np.nan;g['MP_HI']=np.nan;g.loc[idx,'MP_LO']=lower.mean(1)*100;g.loc[idx,'MP_HI']=upper.mean(1)*100
    g['ARG_INDEX']=g.I_S0;g['ARG_K']=g.K_S0
    profiles=g[g.MP_VALID==1].groupby('MP_K')[features+['MP_INDEX']].median().reset_index();profiles['n']=g[g.MP_VALID==1].groupby('MP_K').size().values
    csv(profiles,'perfis_kmeans');csv(pd.DataFrame(ks),'kmeans_testes');csv(pd.DataFrame(scenarios),'sensibilidade_pesos');csv(pd.DataFrame(raw,columns=features).corr(method='spearman').reset_index(names='variable'),'correlacao_entradas')
    csv(pd.DataFrame([{'q':i+1,'cut':float(v)} for i,v in enumerate(cuts)]),'cortes_quintis')
    return g,{'n_valid':len(idx),'n_total':len(g),'k_reference':k0,'silhouette':next(r['silhouette'] for r in ks if r['scenario']=='S0' and r['k']==k0),'quintile_cuts':cuts.tolist(),'parameters':params}

# Moran por bacia e tema
def spatial(g):
    rows=[];g['MP_MORAN']='ND';g['MP_P']=np.nan;g['MP_Q']=np.nan
    for basin,sub in g[g.MP_VALID==1].groupby('BACIA'):
        xy=np.c_[sub.geometry.representative_point().x,sub.geometry.representative_point().y];neighbors=cKDTree(xy).query(xy,k=min(C['vizinhos']+1,len(sub)))[1][:,1:]
        w=csr_matrix((np.ones(neighbors.size),(np.repeat(np.arange(len(sub)),neighbors.shape[1]),neighbors.ravel())),shape=(len(sub),len(sub)));w=w.maximum(w.T);w.setdiag(0);w.eliminate_zeros()
        for theme,field in [('microplastics','MP_INDEX'),('ARG_baseline','ARG_INDEX')]:
            rec,local,ids=moran_w(sub[field].to_numpy(float),w,local=True,seed=SEED);rows.append({'basin':basin,'theme':theme,**rec,'neighbors':C['vizinhos'],'FDR':'BH_0.05_within_basin_theme'})
            if theme=='microplastics' and local is not None:
                take=sub.index[ids];g.loc[take,'MP_MORAN']=local['cluster'];g.loc[take,'MP_P']=local['p'];g.loc[take,'MP_Q']=local['q']
    csv(pd.DataFrame(rows),'moran_global');return g

# Conectividade topográfica sem carga ou decaimento
def connectivity(g):
    checks=[]
    for key,sub in g.groupby('BACIA'):
        with rasterio.open(R/'sub_bacia'/key/'direcao_d8.tif') as src:dr=src.read(1);t=src.transform;profile=src.profile
        h,w=dr.shape;n=h*w;lab=rasterize([(r.geometry,float(r.MP_INDEX)) for r in sub.itertuples() if np.isfinite(r.MP_INDEX)],out_shape=(h,w),transform=t,fill=-9999,dtype='float32');valid=lab!=-9999
        lake=gpd.read_file(R/'reservatorio'/f'{key}.shp').to_crs(31983);lm=rasterize([(v,1) for v in lake.geometry],out_shape=(h,w),transform=t,dtype='uint8',all_touched=True).astype(bool)
        domain=valid|lm;dest=np.full(n,-1,dtype='int64')
        for code,(dy,dx) in D8.items():
            yy,xx=np.where((dr==code)&domain&~lm);ny,nx=yy+dy,xx+dx;ok=(ny>=0)&(ny<h)&(nx>=0)&(nx<w);a=yy[ok]*w+xx[ok];b=ny[ok]*w+nx[ok];ok=domain.ravel()[b];dest[a[ok]]=b[ok]
        area=np.where(valid&~lm,abs(t.a*t.e)/1e6,0).ravel();weighted=np.where(valid&~lm,lab,0).ravel()*area
        indeg=np.bincount(dest[dest>=0],minlength=n);queue=deque(np.flatnonzero(domain.ravel()&(indeg==0)));done=0
        while queue:
            j=queue.popleft();done+=1;k=dest[j]
            if k>=0:
                area[k]+=area[j];weighted[k]+=weighted[j];indeg[k]-=1
                if indeg[k]==0:queue.append(k)
        cycles=int((domain.ravel()&(indeg>0)).sum());assert cycles==0,'Ciclo no grafo D8'
        mean=np.divide(weighted,area,out=np.full(n,np.nan),where=area>0).reshape(h,w);mean=np.where(domain,mean,np.nan)
        for name,data in [('upstream_pressure',mean),('contributing_km2',np.where(domain,area.reshape(h,w),np.nan))]:
            pr=profile.copy();pr.update(driver='GTiff',dtype='float32',nodata=-9999,count=1,compress='deflate')
            with rasterio.open(O/'rasters'/f'{key}_{name}.tif','w',**pr) as dst:dst.write(np.where(np.isfinite(data),data,-9999).astype('float32'),1)
        checks.append({'basin':key,'domain_pixels':int(domain.sum()),'processed':done,'cycles':cycles,'finite_mean':int(np.isfinite(mean).sum()),'max_index':float(np.nanmax(mean))})
    csv(pd.DataFrame(checks),'auditoria_d8');return checks

# Execução e auditoria
def main():
    b=gpd.read_file(R/C['base_grade'],layer='bacias_estudo');g=gpd.read_file(R/C['base_grade'],layer='grade_resultados');original=g[['GRID_ID','BACIA','I_S0','K_S0']].copy()
    circles=gpd.read_file(R/C['base_grade'],layer='influencia_500m');s=gpd.read_file(R/C['base_setores'],layer='analise_setores')
    s=waste(s);g=aggregate(g,circles,s);print('Censo e agregacao',len(s),len(g),int(g.MP_VALID.sum()),flush=True)
    lic,fac,plans,ctx=context(b,s.rename(columns={'mun_nome':'mun_nome'}));g,meta=classify(g);g=spatial(g);d8=connectivity(g)
    assert g[['GRID_ID','BACIA']].duplicated().sum()==0
    assert np.allclose(g.ARG_INDEX,original.I_S0,equal_nan=True)
    assert np.allclose(g.ARG_K,original.K_S0,equal_nan=True)
    assert g.loc[g.MP_VALID==1,['MP_INDEX','WASTE_PCT','ROAD_DENS']].notna().all().all()
    assert g.loc[g.MP_VALID==1,'MP_INDEX'].between(0,100).all()
    layer(g,'microplastic_pressure');layer(b,'basins');csv(g.drop(columns='geometry'),'classificacao_microplasticos')
    report={**meta,**ctx,'D8':d8,'ARG_preserved':True,'fields':list(g.columns),'source_hashes':{'ibge_lixo':digest(R/C['ibge_lixo']),'config':digest(R/'config/microplasticos.json')},'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (O/'auditoria/metodo_microplasticos.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k in ['n_valid','n_total','k_reference','silhouette','licencas_candidatas','ARG_preserved']},ensure_ascii=True),flush=True)
if __name__=='__main__':main()
