# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {path} | rasterio.open.
# Entrada: E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg | gpd.read_file | camada='hidrografia_bacias'.
# Entrada: E:/teco/output/03_multivariada/teco_multivariada.gpkg | gpd.read_file | camada='unidades_ajuste'.
# Entrada: E:/teco/reservatorio/{k}.shp | gpd.read_file.
# Entrada: E:/teco/output/05_auditoria_saude/RD_MG_todos_estabelecimentos_2016_2025.csv | pd.read_csv.
# Entrada: E:/teco/output/02_avaliacao_espacial/tabelas/sih_bacias_2016_2025.csv | pd.read_csv.
# Entrada: E:/teco/output/04_grade_500m/tabelas/sih_cid10_mensal.csv | pd.read_csv.
# Entrada: E:/teco/output/04_grade_500m/filtro_cid10.csv | pd.read_csv.
# Entrada: E:/teco/vias/malha_viaria.shp | gpd.read_file.
# Campos/chaves em b: geometry, id.
# Campos/chaves em c: DOM_DENS, ESG_EST, SEM_ANALIT, dens_pop, dom_set, geometry, pct_rede, set_km2, setor_id.
# Campos/chaves em aux: ESG_EST, sem_rede.
# Campos/chaves em circles: AIH_LOCAL, AREA_KM2, BACIA, DOM, DOM_EST, DOM_OBS, GRID_ID, I_S0, POP, POP_DENS, SAUDE_N, SEM, SEM_OBS, SEM_REDE, geometry.
# Campos/chaves em health: AIH_ANO, CNES, GRUPO, QA_MUN, geometry.
# Campos/chaves em prod.loc: CNES.
# Campos/chaves em prod: AIH.
# Campos/chaves em filt.loc: CID10.
# Campos/chaves em filt: incluir.
# Campos/chaves em rr: CID10.
# Campos/chaves em source: geometry.
# Campos/chaves em a: cenario, silhouette.
# Campos/chaves em models: S0.
# Campos/chaves em circles.loc: I_S0.
# Campos/chaves em rec: cenario.
# Campos/chaves em local: cluster, q.
# Campos/chaves em meta: centros, unidades_bacia.
# Saída: E:/teco/output/04_grade_500m/tabelas/{n} | .to_csv.
# Saída: E:/teco/output/04_grade_500m/teco_grade_500m.gpkg | f.to_file.
# Saída: E:/teco/output/04_grade_500m/auditoria/metodo_grade.json | .write_text.
# Campos/chaves gerados em circles: AIH_ORIG, AREA_KM2, COB_ESG, ESTABILIDADE, EST_ESG, ORIG_STATUS, POP_DENS, QUINTIL, SEM_OBS_P, SEM_REDE, VALIDO.
# Campos/chaves gerados em c: DOM_DENS, ESG_EST, SEM_ANALIT.
# Campos/chaves gerados em z: AREA, DOM, DOM_EST, DOM_OBS, POP, SEM, SEM_OBS.
# Campos/chaves gerados em health: AIH_ANO.
# Campos/chaves gerados em inter: L.
# Campos/chaves gerados em rec: ARI, k_comum, mesmo_grupo_pct, rho_indice.
# Campos/chaves gerados em hexclip: MORAN.
# Campos/chaves gerados em profiles: n.
# Campos/chaves gerados em meta: CID_selecionados, mapas_entrada, status.
# POP_DENS: habitantes/km².
# SEM_REDE: % de domicílios sem rede de esgoto.
# AIH_LOCAL: média anual de internações no estabelecimento local.
# COB_ESG: % do suporte com saneamento publicado.
# I_S0: índice de pressão com pesos iguais, 0-100.
# CNES: identificador do estabelecimento de saúde.
# CID10: código de diagnóstico.
# GRID_ID: identificador do centro da grade.
# BACIA: identificador da bacia.
# Novas variáveis: config/analise_extensivel.json; definir origem, campo, agregação, transformação e peso.
# CÓDIGO DO PROCESSAMENTO

# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_teco.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_teco.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
        break
from caminhos_teco import raiz_projeto as _cp_raiz, texto_caminho as _cp_texto, externo as _cp_externo, adaptar_texto as _cp_adaptar
# FIM DOS CAMINHOS PORTÁTEIS

from pathlib import Path
import json,math,datetime
import numpy as np,pandas as pd,geopandas as gpd,rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds,Window
from shapely.geometry import Point,Polygon
from scipy.spatial import distance
from scipy.stats import spearmanr
from analise_espacial_teco import fitkm,silhouette,ari
from multivariada_teco import moran_w,queen,align
R=Path(_cp_texto('', 'posix'));B=R/'output/02_avaliacao_espacial';P=R/'output/03_multivariada';O=R/'output/04_grade_500m';G=O/'teco_grade_500m.gpkg';SEED=20261112
for d in ['figuras','tabelas','auditoria','layouts_qgis']:(O/d).mkdir(parents=True,exist_ok=True)

# Csv
def csv(f,n):pd.DataFrame(f).to_csv(O/'tabelas'/n,index=False,sep=';',decimal=',',encoding='utf-8-sig')

# Gp
def gp(f,n):f.to_file(G,layer=n,driver='GPKG')

# Rasterstats
def rasterstats(path,geom):
 with rasterio.open(path) as d:
  win=from_bounds(*geom.bounds,d.transform).round_offsets().round_lengths().intersection(Window(0,0,d.width,d.height))
  if win.width<1 or win.height<1:return np.array([])
  a=d.read(1,window=win,masked=True);inside=geometry_mask([geom],a.shape,d.window_transform(win),invert=True);v=np.asarray(a)[inside&~np.ma.getmaskarray(a)];return v[np.isfinite(v)]

# Main
def main():
 b=gpd.read_file(B/'teco_avaliacao.gpkg',layer='bacias_estudo');union=b.geometry.union_all();xmin,ymin,xmax,ymax=union.bounds;r=500.;dx=1.5*r;dy=np.sqrt(3)*r;pts=[];cells=[];rows=[]
 for ix in range(math.floor((xmin-r)/dx),math.ceil((xmax+r)/dx)+1):
  for iy in range(math.floor((ymin-r)/dy)-1,math.ceil((ymax+r)/dy)+1):
   x=ix*dx;y=iy*dy+(ix%2)*dy/2;hex=Polygon([(x+r*np.cos(np.pi*j/3),y+r*np.sin(np.pi*j/3)) for j in range(6)])
   if not hex.intersects(union):continue
   gid=f'G{len(rows)+1:04d}';p=Point(x,y);rows.append({'GRID_ID':gid,'E':x,'N':y,'RAIO_M':500,'CENTRO_INT':int(union.covers(p))});pts.append(p);cells.append(hex)
 centers=gpd.GeoDataFrame(rows,geometry=pts,crs=31983);hexes=gpd.GeoDataFrame(rows,geometry=cells,crs=31983)
 hexclip=gpd.overlay(hexes,b[['id','geometry']],how='intersection').rename(columns={'id':'BACIA'});hexclip=hexclip[hexclip.area>1].reset_index(drop=True)
 circles=centers.copy();circles.geometry=circles.buffer(500,resolution=32);circles=gpd.overlay(circles,b[['id','geometry']],how='intersection').rename(columns={'id':'BACIA'});circles=circles[circles.area>1].reset_index(drop=True);circles['AREA_KM2']=circles.area/1e6

 c=gpd.read_file(B/'teco_avaliacao.gpkg',layer='analise_setores');u=gpd.read_file(P/'teco_multivariada.gpkg',layer='unidades_ajuste');aux=u.set_index('setor_id')
 c['SEM_ANALIT']=c.setor_id.map(aux.sem_rede);c['ESG_EST']=c.setor_id.map(aux.ESG_EST);c['DOM_DENS']=c.dom_set/c.set_km2
 z=gpd.overlay(circles[['GRID_ID','BACIA','geometry']],c[['setor_id','dens_pop','DOM_DENS','pct_rede','SEM_ANALIT','ESG_EST','geometry']],how='intersection');z['AREA']=z.area/1e6;z['POP']=z.dens_pop*z.AREA;z['DOM']=z.DOM_DENS*z.AREA;z['SEM']=z.DOM*z.SEM_ANALIT/100;z['DOM_OBS']=z.DOM.where(z.pct_rede.notna(),0);z['SEM_OBS']=z.DOM*(1-z.pct_rede/100);z['DOM_EST']=z.DOM.where(z.ESG_EST,0)
 sums=z.groupby(['GRID_ID','BACIA'])[['AREA','POP','DOM','SEM','DOM_OBS','SEM_OBS','DOM_EST']].sum(min_count=1)
 circles=circles.merge(sums,on=['GRID_ID','BACIA'],how='left');circles['POP_DENS']=circles.POP/circles.AREA_KM2;circles['SEM_REDE']=100*circles.SEM/circles.DOM.replace(0,np.nan);circles.loc[circles.DOM.eq(0),'SEM_REDE']=0;circles['SEM_OBS_P']=100*circles.SEM_OBS/circles.DOM_OBS.replace(0,np.nan);circles['COB_ESG']=100*circles.DOM_OBS/circles.DOM.replace(0,np.nan);circles['EST_ESG']=100*circles.DOM_EST/circles.DOM.replace(0,np.nan)
 water=gpd.GeoDataFrame(pd.concat([gpd.read_file(R/'reservatorio'/f'{k}.shp').to_crs(31983) for k in b.id],ignore_index=True),crs=31983);wunion=water.geometry.union_all()

 health=gpd.read_file(B/'teco_avaliacao.gpkg',layer='saude_cnes_ativos');health=health[(health.QA_MUN==1)&health.GRUPO.isin(['Atenção básica','Hospital / hospital-dia','Urgência / pronto atendimento','Outros serviços assistenciais'])]
 production=R/'output/05_auditoria_saude/RD_MG_todos_estabelecimentos_2016_2025.csv'
 if production.exists():
  prod=pd.read_csv(production,sep=';',dtype={'CNES':str});health=health[health.CNES.isin(prod.loc[prod.AIH.gt(0),'CNES'])].copy()
 rd=O/'tabelas/sih_cid10_mensal.csv';base=pd.read_csv(B/'tabelas/sih_bacias_2016_2025.csv',sep=';',dtype={'CNES':str});activity=base.groupby('CNES').internacoes.sum()/10
 if rd.exists():
  rr=pd.read_csv(rd,sep=';',dtype={'CNES':str,'CID10':str});fp=O/'filtro_cid10.csv';selected=[]
  if fp.exists():
   filt=pd.read_csv(fp,sep=';',dtype={'CID10':str});selected=filt.loc[filt.incluir.astype(str).str.lower().isin(['true','1','sim']),'CID10'].tolist()
  if fp.exists():rr=rr[rr.CID10.isin(selected)]
  activity=rr.groupby('CNES').internacoes.sum()/10
 health['AIH_ANO']=health.CNES.map(activity).fillna(0)
 hit=gpd.sjoin(health[['CNES','AIH_ANO','geometry']],circles[['GRID_ID','BACIA','geometry']],how='inner',predicate='intersects');hgrp=hit.groupby(['GRID_ID','BACIA']).agg(SAUDE_N=('CNES','nunique'),AIH_LOCAL=('AIH_ANO','sum'))
 circles=circles.merge(hgrp,on=['GRID_ID','BACIA'],how='left');circles[['SAUDE_N','AIH_LOCAL']]=circles[['SAUDE_N','AIH_LOCAL']].fillna(0)

 vals=[]
 for row in circles.itertuples():
  use=rasterstats(R/'teco_base/uso_terra/uso_terra-reservatorio.tif',row.geometry);elev=rasterstats(B/'rasters'/f'{row.BACIA}_hipsometria.tif',row.geometry);slope=rasterstats(B/'rasters'/f'{row.BACIA}_declividade_pct.tif',row.geometry);dist=rasterstats(B/'rasters'/f'{row.BACIA}_distancia_hidrologica_km.tif',row.geometry)
  vals.append({'URB_PCT':100*np.mean(use==24) if len(use) else np.nan,'USO_N':len(use),'HIPS_M':np.mean(elev) if len(elev) else np.nan,'DECL_PCT':np.mean(slope) if len(slope) else np.nan,'DIST_KM':np.mean(dist) if len(dist) else np.nan,'TERRA_PCT':100*row.geometry.difference(wunion).area/row.geometry.area})
 circles=pd.concat([circles,pd.DataFrame(vals)],axis=1)
 hyd=gpd.read_file(B/'teco_avaliacao.gpkg',layer='hidrografia_bacias');roads=gpd.read_file(R/'vias/malha_viaria.shp').to_crs(31983)
 for source,col in [(hyd,'HIDRO_KM'),(roads,'VIAS_KM')]:
  inter=gpd.overlay(source[['geometry']],circles[['GRID_ID','BACIA','geometry']],how='intersection',keep_geom_type=True);inter['L']=inter.length/1000;tot=inter.groupby(['GRID_ID','BACIA']).L.sum();circles[col]=[tot.get((a,b),0) for a,b in zip(circles.GRID_ID,circles.BACIA)]
 circles['AIH_ORIG']=np.nan;circles['ORIG_STATUS']='Pendente: geografia de CEP e causas selecionadas'

 feats=['POP_DENS','SEM_REDE','AIH_LOCAL'];x=np.c_[np.log1p(circles.POP_DENS),circles.SEM_REDE,np.log1p(circles.AIH_LOCAL)];valid=np.isfinite(x).all(1);lo=np.nanmin(x[valid],0);hi=np.nanmax(x[valid],0);norm=(x-lo)/np.where(hi>lo,hi-lo,1)
 circles['VALIDO']=valid
 for j,f in enumerate(feats):circles['N_'+f]=norm[:,j]
 for f in ['URB_PCT','HIPS_M','DECL_PCT','DIST_KM','VIAS_KM','HIDRO_KM']:
  v=circles[f];circles['N_'+f]=(v-v.min())/(v.max()-v.min()) if v.max()>v.min() else 0

 scen={'S0':('Referência local, pesos iguais',[1,1,1]),'S1':('Ênfase em atividade hospitalar local',[1,1,3]),'S2':('Ênfase em ausência de rede',[1,3,1]),'S3':('Ênfase em adensamento',[3,1,1]),'S4':('Sem proxy hospitalar local',[1,1,0])};scrows=[];models={};krows=[]
 for code,(label,weights) in scen.items():
  w=np.array(weights,float);circles['I_'+code]=100*(norm@w)/w.sum();circles['F_'+code]=np.where(valid,np.minimum((circles['I_'+code].fillna(0)/20).astype(int)+1,5),0)
  for k in range(2,7):
   loss,cent,l=fitkm(norm[valid]*np.sqrt(w),k,SEED+100*int(code[1:]),starts=15);sil=silhouette(norm[valid]*np.sqrt(w),l);models[code,k]=(cent,l);krows.append({'cenario':code,'k':k,'silhouette':sil,'inercia':loss,'menor_grupo':int(np.bincount(l).min())})
  scrows.append({'cenario':code,'descricao':label,'peso_populacao':w[0],'peso_sem_rede':w[1],'peso_aih_local':w[2],'melhor_k':max([a for a in krows if a['cenario']==code],key=lambda a:a['silhouette'])['k']})
 k0=scrows[0]['melhor_k'];base_labels=models['S0',k0][1];order=sorted(set(base_labels),key=lambda z:circles.loc[valid,'I_S0'].to_numpy()[base_labels==z].mean());mapping={n:i for i,n in enumerate(order)};base_labels=np.array([mapping[n] for n in base_labels]);labs=[]
 for rec in scrows:
  co=rec['cenario'];lab=align(models[co,k0][1],base_labels);labs.append(lab);circles['K_'+co]=0;circles.loc[valid,'K_'+co]=lab+1;rec['k_comum']=k0;rec['ARI']=ari(base_labels,lab);rec['mesmo_grupo_pct']=100*np.mean(base_labels==lab);rec['rho_indice']=spearmanr(circles.loc[valid,'I_S0'],circles.loc[valid,'I_'+co]).statistic
 circles['ESTABILIDADE']=np.nan;circles.loc[valid,'ESTABILIDADE']=100*np.mean(np.array(labs)==base_labels,axis=0)
 circles['QUINTIL']=0
 goodscore=circles.I_S0.notna()
 circles.loc[goodscore,'QUINTIL']=pd.qcut(circles.loc[goodscore,'I_S0'].rank(method='average'),5,labels=False,duplicates='drop')+1

 hexclip=hexclip.merge(circles.drop(columns=['geometry','E','N','RAIO_M','CENTRO_INT']),on=['GRID_ID','BACIA'],validate='one_to_one');hexclip['MORAN']='ND';mrows=[]
 for key,g in hexclip[hexclip.VALIDO].groupby('BACIA'):
  g=g[g.COB_ESG.ge(95)];w=queen(g);rec,local,ii=moran_w(g.I_S0.to_numpy(),w,local=True);mrows.append({'bacia':key,**rec})
  if local is not None:hexclip.loc[g.index,'MORAN']='ISO';hexclip.loc[g.index[ii],'MORAN']=local['cluster'];hexclip.loc[g.index[ii],'MORAN_Q']=local['q']

 gp(centers,'centros_500m');gp(circles,'influencia_500m');gp(hexclip,'grade_resultados');gp(b,'bacias_estudo');gp(health,'saude_referencia')
 csv(circles.drop(columns='geometry'),'indicadores_grade.csv');csv(scrows,'cenarios_grade.csv');csv(krows,'kmeans_grade.csv');csv(mrows,'moran_grade.csv');csv([{'variavel':f,'transformacao':'log1p' if j!=1 else 'identidade','min':lo[j],'max':hi[j]} for j,f in enumerate(feats)],'normalizacao_grade.csv')
 profiles=circles.groupby('K_S0')[feats+['URB_PCT','DECL_PCT','DIST_KM']].median().reset_index();profiles['n']=circles.groupby('K_S0').size().values;csv(profiles,'perfis_grade.csv')

 stats=[]
 for key,g in circles.groupby('BACIA'):
  for col in [*feats,'POP','DOM','COB_ESG','EST_ESG','SAUDE_N','URB_PCT','HIPS_M','DECL_PCT','DIST_KM','VIAS_KM','HIDRO_KM',*[c for c in circles if c.startswith('N_')]]:
   a=g[col].dropna();stats.append({'bacia':key,'variavel':col,'n_validos':len(a),'n_ausentes':len(g)-len(a),'min':a.min(),'mediana':a.median(),'media':a.mean(),'max':a.max(),'desvio_padrao':a.std()})
 csv(stats,'estatisticas_camadas.csv')
 meta={'data':datetime.datetime.now().astimezone().isoformat(),'raio_m':500,'hexagono_raio_externo_m':500,'distancia_centros_m':float(np.sqrt(3)*500),'centros':len(centers),'unidades_bacia':len(circles),'k_base':int(k0),'fontes_pressao':feats,'cenarios':scen,'normalizacao':'log1p em densidade de população e AIH local; min-max fixo; sem percentil na análise principal.','status':'Exploratório: todas as causas de atividade LOCAL. Não atribui internações aos domicílios; classificação de origem permanece pendente.','sobreposicao':'Círculos são vizinhanças sobrepostas. Contagens não devem ser somadas entre círculos; hexágonos apenas para apresentação sem sobreposição.','Moran':'Queen no suporte hexagonal; apenas COB_ESG>=95%; 999 permutações e FDR5%. Vizinhanças de500m compartilham dados: associação parcialmente induzida pela suavização; não prova focos de genes.','origem_paciente':'AIH_ORIG permanece nulo, sem simular área atendida. CEPs agregados serão usados somente após geocodificação verificável e seleção de causas.'}
 if selected:meta['status']='Exploratório local: causas selecionadas por CID-10. Não atribui internações à residência nem confirma RAM.'
 meta['CID_selecionados']=len(selected);meta['mapas_entrada']='Geometrias nativas; grade apenas para análises.'
 (O/'auditoria/metodo_grade.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8');print('GRADE_CONCLUIDA',meta['centros'],meta['unidades_bacia'],'K',k0,flush=True)
if __name__=='__main__':main()
