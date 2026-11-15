# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/saneamento_ibge/populacao_basico/Agregados_por_setores_basico_BR.csv | pd.read_csv.
# Entrada: E:/teco/teco_base/uso_terra/uso_terra-reservatorio.tif | rasterio.open.
# Entrada: E:/teco/esgoto_bh/REDE_ESGOTO.shp | gpd.read_file.
# Entrada: E:/teco/ete/ide_0603_mg_ete_pto.shp | gpd.read_file.
# Entrada: E:/teco/output/01_integracao_territorial/shapefiles/{name}.shp | gpd.read_file.
# Entrada: E:/teco/sub_bacia/shapefiles_v6_20261109_141015/sub_bacias_exclusivas.shp | gpd.read_file.
# Entrada: E:/teco/saneamento_ibge/resultados/saneamento_teco.gpkg | gpd.read_file | camada='resumo_bacias'.
# Entrada: E:/teco/saneamento_ibge/MG_setores_CD2022.shp | gpd.read_file.
# Campos/chaves em p: setor_id.
# Campos/chaves em unions: N, NI, S.
# Campos/chaves em bas: bas_id, bas_nome, geometry.
# Campos/chaves em net: bas_id, comp_m.
# Campos/chaves em r: DATA, ID_BASE_TR, ID_RDESG, LADO_RDESG, bas_nome, dens_pop, geometry, pct_urb, pop_a_est, sit_rede, uso_cov.
# Campos/chaves em raw: data_apur.
# Campos/chaves em clean: C, NI.
# Campos/chaves em g: area_bh.
# Campos/chaves em row: area_bh.
# Campos/chaves em values: N, S.
# Campos/chaves em e: ete_id, fase_lic, geometry, mun_nome, situ_lic.
# Campos/chaves em old: setor_id.
# Campos/chaves em c.loc: pop_a_est.
# Campos/chaves em summary.at: pop_u_est.
# Campos/chaves em net.loc: comp_m.
# Campos/chaves em audit: summary.
# Campos/chaves em a: summary.
# Saída: E:/teco/descontinuado/dt.datetime.now().strftime('%Y%m%d_%H%M%S_integracao_territorial')/manifesto.json | .write_text.
# Saída: E:/teco/output/01_integracao_territorial/uso_ocupacao_bacias.tif | rasterio.open.
# Saída: {gpkg} | g.to_file.
# Saída: E:/teco/output/01_integracao_territorial/shapefiles/{name}.shp | g.to_file.
# Saída: E:/teco/output/01_integracao_territorial/integracao_territorial_teco.gpkg | rawnet.to_file.
# Saída: E:/teco/output/01_integracao_territorial/uso_ocupacao_por_classe.csv | .to_csv.
# Saída: E:/teco/output/01_integracao_territorial/atributos_integrados_bacias.csv | .to_csv.
# Saída: E:/teco/output/01_integracao_territorial/resumo_bacias.csv | .to_csv.
# Saída: E:/teco/output/01_integracao_territorial/rede_bh_registros_origem.csv | .to_csv.
# Saída: E:/teco/output/01_integracao_territorial/dicionario_campos.csv | .to_csv.
# Saída: E:/teco/output/01_integracao_territorial/auditoria_integracao.json | .write_text.
# Saída: E:/teco/output/01_integracao_territorial/LEIA_PRIMEIRO.md | .write_text.
# Saída: E:/teco/output/01_integracao_territorial/Previa_{field}.png | fig.savefig.
# Campos/chaves gerados em DESC: out_km2, pct_out.
# Campos/chaves gerados em g: area_bh, bh_pct, out_km2, pct_out, rede_qual, uso_ano, uso_cov, uso_dom, uso_km2, uso_npix, uso_valid.
# Campos/chaves gerados em source: sit_rede.
# Campos/chaves gerados em net: comp_m.
# Campos/chaves gerados em raw: comp_m, data_apur.
# Campos/chaves gerados em geo: cens_urb, dens_dom, dens_pop.
# Campos/chaves gerados em clip: frac_area, rec_km2.
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
import sys,json,math,datetime as dt,shutil,zipfile,gc
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.windows import Window,from_bounds
from shapely import intersection,length
from shapely.ops import unary_union

ROOT=Path(_cp_texto('', 'posix'));OUT=ROOT/'output/01_integracao_territorial';SHP=OUT/'shapefiles'
CRS=31983
MESH=ROOT/'saneamento_ibge/MG_setores_CD2022.shp'
BASE=ROOT/'saneamento_ibge/resultados/saneamento_teco.gpkg'
BASIN=ROOT/'sub_bacia/shapefiles_v6_20261109_141015/sub_bacias_exclusivas.shp'
POP=ROOT/'saneamento_ibge/populacao_basico/Agregados_por_setores_basico_BR.csv'
LULC=ROOT/'teco_base/uso_terra/uso_terra-reservatorio.tif'
NETWORK=ROOT/'esgoto_bh/REDE_ESGOTO.shp'
ETE=ROOT/'ete/ide_0603_mg_ete_pto.shp'
sys.path.insert(0,str(ROOT/'codigo'))
from preparar_saneamento_ibge import polygon,sha,DESC as SAN_DESC

CLASS={1:'Floresta (classe agregada)',3:'Formação florestal',4:'Formação savânica',9:'Silvicultura',11:'Campo alagado e área pantanosa',12:'Formação campestre',15:'Pastagem',19:'Lavoura temporária',21:'Mosaico de usos',24:'Área urbanizada',25:'Outras áreas não vegetadas',29:'Afloramento rochoso',30:'Mineração',31:'Aquicultura',33:'Rio, lago e oceano',36:'Lavoura perene'}
GROUPS={
 'urb':([24],'Área urbanizada'),
 'veg':([1,3,4,5,6,7,10,11,12,13,32,49,50,77,84],'Vegetação natural'),
 'agro':([9,14,15,18,19,20,21,35,36,39,40,41,46,47,48,62],'Agropecuária e silvicultura'),
 'min':([30],'Mineração'),
 'agua':([26,31,33],'Corpos de água e aquicultura'),
 'nveg':([22,23,25,29,75,91],'Outras superfícies não vegetadas'),
}
DESC=dict(SAN_DESC,**{
 'pop_2022':'Total de pessoas do setor inteiro, v0001 do Agregado Básico Censo 2022 (revisão 20/05/2026)',
 'dom_ocup':'Domicílios particulares ocupados do setor inteiro, v0007 do Agregado Básico, permanentes e improvisados',
 'dens_pop':'População do setor inteiro / área do setor inteiro, habitantes por km²; não é densidade por pixel',
 'dens_dom':'Domicílios particulares ocupados / área do setor inteiro, domicílios por km²',
 'pop_a_est':'População estimada no recorte: pop_2022 × frac_area; alocação uniforme, não contagem de residentes na bacia',
 'cens_urb':'Situação censitária: 1 urbana, 0 rural, -1 não informada; difere da classe Área Urbanizada do uso do solo',
 'pop_u_est':'População estimada nos recortes de setores de situação urbana do IBGE; não população localizada na mancha urbanizada',
 'pop_r_est':'População estimada nos recortes de setores rurais do IBGE',
 'pct_pop_u':'Percentual da população estimada da bacia em setores de situação urbana do IBGE',
 'uso_ano':'Ano do uso do solo informado no projeto: 2025; não comprovado nos metadados internos do GeoTIFF',
 'uso_cov':'Percentual de centros de pixels com classe válida entre os centros de pixels da geometria; inclui NoData fora da extensão',
 'uso_npix':'Número de centros de pixels do raster dentro da geometria',
 'uso_valid':'Número de centros de pixels com classe válida (código > 0)',
 'uso_km2':'Área aproximada mapeada, pixels válidos × área de pixel, km²',
 'uso_dom':'Grupo de uso do solo com mais pixels na geometria; categorias cartográficas, não risco',
 'area_bh':'Área da geometria situada nos setores do município de BH, km², domínio desta base de rede',
 'bh_pct':'Percentual da área no domínio municipal BH; não representa cobertura pelo serviço',
 'rede_s_km':'Traçados cadastrados S, em km, excluindo sobreposições S/N. Não é medida de tubulação ou ligações. Por setor, não aditivo nas divisas',
 'rede_n_km':'Traçados cadastrados N, em km, excluindo sobreposições S/N. Por setor, não aditivo nas divisas',
 'rede_i_km':'Traçados sem informação, em km, retirando sobreposições com registros S ou N',
 'rede_c_km':'Traçados com sobreposição geométrica de registros S e N, em km; pendentes de conciliação cadastral',
 'rede_t_km':'Comprimento único dos traçados cadastrados na geometria. Valores de setores podem compartilhar trechos na divisa',
 'pct_t_s':'100 × rede_s_km / rede_t_km: proporção do comprimento cadastrado marcado S; não percentual de casas ou pessoas atendidas',
 'cad_comp':'100 × (rede_s_km + rede_n_km) / rede_t_km: completude do indicador sobre o traçado cadastrado',
 'dens_rede':'rede_s_km / area_bh, km de traçado S por km² no domínio BH; não densidade de tubulação comprovada',
 'rede_qual':'fora_BH: base não cobre o local; sem_tr: BH sem traçado neste recorte; cadastro: há registros. Não extrapolar N fora de BH',
 'sit_rede':'Situação consolidada do traçado: S sim; N não; NI sem informação; C conflito geométrico S/N',
 'sit_nome':'Descrição da situação de disponibilidade cadastrada',
 'comp_m':'Comprimento da parte de traçado consolidado, metros',
 'id_trecho':'ID_BASE_TR original da PBH, identifica trecho de referência',
 'id_cad':'ID_RDESG original da PBH, identifica registro cadastral',
 'lado':'LADO_RDESG original: A ambos, E esquerdo, D direito, no sentido de digitalização',
 'data_apur':'DATA original de apuração da informação; não é data de instalação',
 'ete_id':'Identificador original do cadastro de ETE recebido',
 'fase_lic':'Fase declarada no cadastro de licenciamento; não comprova operação atual ou eficiência',
 'situ_lic':'Situação declarada de licenciamento da ETE, conforme base recebida',
 'n_ete':'Quantidade de pontos de ETE no cadastro recebido dentro da bacia; não confirma população atendida',
})
for p,(_,label) in GROUPS.items():
    DESC[f'{p}_km2']=f'Área aproximada de {label.lower()}, pela contagem de pixels, km²'
    DESC[f'pct_{p}']=f'Percentual de {label.lower()} sobre os pixels válidos da geometria; consultar uso_cov'
DESC['out_km2']='Área aproximada de códigos não abrangidos pelos grupos previstos, km²'
DESC['pct_out']='Percentual de códigos fora dos grupos previstos sobre pixels válidos'

# Archive outputs
def archive_outputs():
    if OUT.exists() and any(OUT.iterdir()):
        dest=ROOT/'descontinuado'/dt.datetime.now().strftime('%Y%m%d_%H%M%S_integracao_territorial')
        assert OUT.resolve().is_relative_to(ROOT) and dest.resolve().is_relative_to(ROOT)
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(OUT),str(dest))
        (dest/'manifesto.json').write_text(json.dumps(dict(source=str(OUT),archived=str(dest),reason='Saída gerada substituída; insumos preservados'),ensure_ascii=False,indent=2),encoding='utf8')
    SHP.mkdir(parents=True,exist_ok=True)

# Pop table
def pop_table(ids):
    rows=[]
    for a in pd.read_csv(POP,sep=';',encoding='latin1',dtype='string',usecols=['CD_SETOR','v0001','v0007'],chunksize=20000,keep_default_na=False):
        a=a[a.CD_SETOR.isin(ids)]
        if len(a):rows.append(a)
    p=pd.concat(rows,ignore_index=True).rename(columns={'CD_SETOR':'setor_id','v0001':'pop_2022','v0007':'dom_ocup'})
    assert p['setor_id'].is_unique
    for c in ['pop_2022','dom_ocup']:p[c]=pd.to_numeric(p[c],errors='coerce').astype(float)
    return p

# Rasterstats
class RasterStats:
    def __init__(self,extent):
        self.ds=rasterio.open(LULC);assert self.ds.crs.to_epsg()==CRS and self.ds.count==1
        w=from_bounds(*extent,transform=self.ds.transform);c=math.floor(w.col_off)-1;r=math.floor(w.row_off)-1
        w=Window(c,r,math.ceil(w.col_off+w.width)-c+1,math.ceil(w.row_off+w.height)-r+1)
        self.window=w;self.transform=self.ds.window_transform(w);self.a=self.ds.read(1,window=w,boundless=True,fill_value=0)
        self.cell_area=abs(self.transform.a*self.transform.e);self.codes=np.unique(self.a);self.codes=self.codes[self.codes>0]
        print('Raster de análise',self.a.shape,'classes',self.codes.tolist(),flush=True)
    def add(self,g,level):
        n=len(g);lab=rasterize([(p,i+1) for i,p in enumerate(g.geometry)],out_shape=self.a.shape,transform=self.transform,fill=0,all_touched=False,dtype='int32')
        total=np.bincount(lab.ravel(),minlength=n+1)[1:]
        hist={int(c):np.bincount(lab[self.a==c],minlength=n+1)[1:] for c in self.codes}
        valid=sum(hist.values());g=g.copy();g['uso_ano']=2025;g['uso_npix']=total;g['uso_valid']=valid
        g['uso_cov']=np.divide(100*valid,total,out=np.full(n,np.nan),where=total>0);g['uso_km2']=valid*self.cell_area/1e6
        assigned=np.zeros(n,dtype=np.int64);stack=[];labels=[]
        for prefix,(codes,label) in GROUPS.items():
            count=sum((hist.get(c,np.zeros(n,dtype=np.int64)) for c in codes));assigned+=count
            g[f'{prefix}_km2']=count*self.cell_area/1e6;g[f'pct_{prefix}']=np.divide(100*count,valid,out=np.full(n,np.nan),where=valid>0)
            stack.append(count);labels.append(label)
        other=valid-assigned;assert (other>=0).all()
        g['out_km2']=other*self.cell_area/1e6;g['pct_out']=np.divide(100*other,valid,out=np.full(n,np.nan),where=valid>0)
        stack.append(other);labels.append('Outros códigos');top=np.argmax(np.stack(stack),axis=0)
        g['uso_dom']=[labels[i] if v>0 else 'Sem dado de uso' for i,v in zip(top,valid)]
        rows=[]
        for i,(_,row) in enumerate(g.iterrows()):
            for code,counts in hist.items():
                if counts[i]>0:rows.append(dict(escala=level,setor_id=row.get('setor_id',''),bas_id=row.get('bas_id',''),codigo=code,classe=CLASS.get(code,f'Classe {code}'),n_pixels=int(counts[i]),area_km2=float(counts[i]*self.cell_area/1e6),pct_valid=float(100*counts[i]/valid[i])))
        assert np.allclose(g[[f'pct_{p}' for p in GROUPS]+['pct_out']].sum(axis=1)[valid>0],100)
        del lab;gc.collect();return g,rows
    def write_clip(self,bas):
        mask=rasterize([(g,1) for g in bas.geometry],out_shape=self.a.shape,transform=self.transform,fill=0,dtype='uint8')
        out=np.where(mask,self.a,0)
        rows,cols=np.where(mask>0);r0,r1=rows.min(),rows.max()+1;c0,c1=cols.min(),cols.max()+1
        profile=self.ds.profile.copy();profile.update(height=r1-r0,width=c1-c0,transform=self.transform*rasterio.Affine.translation(c0,r0),nodata=0,count=1,compress='LZW',driver='GTiff')
        with rasterio.open(OUT/'uso_ocupacao_bacias.tif','w',**profile) as d:
            d.write(out[r0:r1,c0:c1],1);d.update_tags(ANO_INFORMADO_PROJETO='2025',ANO_CONFIRMADO_METADADOS='NAO',RECORTE='Bacias TECO; regra centro de pixel; sem reamostragem',SOURCE=str(LULC))

# Lines
def lines(g):
    if g is None or g.is_empty:return []
    if g.geom_type in ['LineString','LinearRing']:return [g] if g.length>1e-7 else []
    if hasattr(g,'geoms'):return [p for a in g.geoms for p in lines(a)]
    return []

# Network layers
def network_layers(bas,bh_domain):
    source=gpd.read_file(NETWORK).to_crs(CRS);source['sit_rede']=source.IND_RDESG.fillna('NI').replace({'':'NI'})
    assert set(source.sit_rede.unique())<=set(['S','N','NI'])
    target=bas.geometry.union_all().intersection(bh_domain)
    take=source.sindex.query(target,predicate='intersects');r=source.iloc[take].copy();r.geometry=r.geometry.intersection(target);r=r[r.length>1e-7].copy()
    unions={k:unary_union(r.loc[r.sit_rede==k].geometry.tolist()) for k in ['S','N','NI']}
    conflict=unions['S'].intersection(unions['N']);clean={'S':unions['S'].difference(unions['N']),'N':unions['N'].difference(unions['S']),'NI':unions['NI'].difference(unions['S'].union(unions['N'])),'C':conflict}
    parts=[];names={'S':'Com rede cadastrada','N':'Sem rede cadastrada','NI':'Sem informação','C':'Conflito S/N na origem'}
    for key,g in clean.items():
        for p in lines(g):parts.append(dict(sit_rede=key,sit_nome=names[key],geometry=p))
    net=gpd.GeoDataFrame(parts,crs=CRS);net=gpd.overlay(net,bas[['bas_id','bas_nome','geometry']],how='intersection',keep_geom_type=True)
    net=net.explode(index_parts=False,ignore_index=True);net=net[net.length>1e-7].copy();net['comp_m']=net.length
    unique=unary_union(r.geometry.tolist()).length
    assert abs(net['comp_m'].sum()-unique)<max(.01,unique*1e-8),(net.comp_m.sum(),unique)
    raw=gpd.overlay(r[['ID_BASE_TR','ID_RDESG','LADO_RDESG','DATA','sit_rede','geometry']],bas[['bas_id','bas_nome','geometry']],how='intersection',keep_geom_type=True)
    raw=raw.rename(columns={'ID_BASE_TR':'id_trecho','ID_RDESG':'id_cad','LADO_RDESG':'lado','DATA':'data_apur'})
    raw['data_apur']=raw['data_apur'].map(lambda t:None if pd.isna(t) else pd.Timestamp(t).strftime('%Y-%m-%d'));raw['comp_m']=raw.length
    audit=dict(source_features=len(source),source_flags=source.sit_rede.value_counts().to_dict(),source_duplicates_wkb=int(source.geometry.to_wkb().duplicated().sum()),raw_features_in_work_area=len(raw),consolidated_parts=len(net),unique_length_km=unique/1000,conflict_length_km=clean['C'].length/1000,unknown_overlap_known_removed_km=(unions['NI'].length-clean['NI'].length)/1000,rule='Unique geometrical linework; S/N coincident portions flagged C, not assigned automatically; known status overrides NI only on exact overlap',dictionary_url='https://ckan.pbh.gov.br/dataset/cb4df0e5-0849-4d1f-9f19-32a189824a7a/resource/329ad4ec-5912-457d-b13a-134747a2e55a/download/trecho_rede_esgoto.pdf')
    print('Cadastro PBH consolidado',json.dumps(audit,ensure_ascii=True),flush=True)
    return net,raw,audit

# Add network
def add_network(g,net,bh_domain):
    g=g.copy();statuscols={'S':'rede_s_km','N':'rede_n_km','NI':'rede_i_km','C':'rede_c_km'}
    fields=list(statuscols.values())+['rede_t_km','pct_t_s','cad_comp','dens_rede']
    for c in fields:g[c]=np.nan
    g['area_bh']=g.geometry.intersection(bh_domain).area/1e6;g['bh_pct']=100*g['area_bh']/(g.area/1e6);g['rede_qual']='fora_BH'
    for idx,row in g.iterrows():
        if row['area_bh']<=1e-10:continue
        geom=row.geometry.intersection(bh_domain);ids=net.sindex.query(geom,predicate='intersects')
        values={k:0. for k in statuscols}
        if len(ids):
            candidate=net.iloc[ids];lengths=length(intersection(candidate.geometry.to_numpy(),geom))/1000
            for key in values:values[key]=float(np.asarray(lengths)[candidate.sit_rede.to_numpy()==key].sum())
        for key,col in statuscols.items():g.at[idx,col]=values[key]
        total=sum(values.values());g.at[idx,'rede_t_km']=total;g.at[idx,'dens_rede']=values['S']/row['area_bh'];g.at[idx,'rede_qual']='cadastro' if total>0 else 'sem_tr'
        if total>0:g.at[idx,'pct_t_s']=100*values['S']/total;g.at[idx,'cad_comp']=100*(values['S']+values['N'])/total
    return g

# Etes
def etes(bas):
    e=gpd.read_file(ETE).to_crs(CRS);e=e.rename(columns={'id':'ete_id','municipios':'mun_nome'})
    for c in ['mun_nome','fase_lic','situ_lic']:
        def fix(s):
            if not isinstance(s,str):return s
            try:return s.encode('latin1').decode('utf8') if 'Ã' in s or 'Â' in s else s
            except UnicodeError:return s
        e[c]=e[c].map(fix)
    e=gpd.sjoin(e[['ete_id','mun_nome','fase_lic','situ_lic','geometry']],bas[['bas_id','bas_nome','geometry']],how='inner',predicate='within').drop(columns='index_right')
    return e

# Export vector
def export_vector(g,name,gpkg,layer):
    assert g.crs.to_epsg()==CRS and g.is_valid.all() and g.geometry.notna().all()
    cols=[c for c in g.columns if c!='geometry'];assert all(len(c)<=10 for c in cols),[c for c in cols if len(c)>10]
    g=g.copy()
    for c in cols:
        if isinstance(g[c].dtype,pd.StringDtype):g[c]=g[c].astype(object).where(g[c].notna(),None)
    g.to_file(gpkg,layer=layer,driver='GPKG',index=False)
    if name:
        p=SHP/(name+'.shp');g.to_file(p,driver='ESRI Shapefile',encoding='UTF-8',index=False);back=gpd.read_file(p)
        assert len(back)==len(g) and back.crs.to_epsg()==CRS
        for c in ['setor_id','bas_id','sit_rede']:
            if c in g:assert back[c].tolist()==g[c].tolist(),(name,c)
        for c in ['pop_2022','pop_a_est','pct_urb','rede_s_km']:
            if c in g:
                assert np.array_equal(back[c].isna(),g[c].isna()),(name,c,'NULL')
                assert np.allclose(back[c].fillna(0),g[c].fillna(0),atol=1e-7,rtol=1e-9),(name,c)

# Main
def main():
    bas=gpd.read_file(BASIN).to_crs(CRS)[['id','reserv','geometry']].rename(columns={'id':'bas_id','reserv':'bas_nome'});bas.geometry=bas.geometry.map(polygon)
    old=gpd.read_file(BASE,layer='setores_inteiros');bb=tuple(bas.to_crs(4674).total_bounds)
    mesh=gpd.read_file(MESH,bbox=bb,columns=['CD_SETOR','geometry']).to_crs(CRS);mesh.geometry=mesh.geometry.map(polygon)
    mesh=mesh[mesh.geometry.intersection(bas.geometry.union_all()).area>.01].copy().rename(columns={'CD_SETOR':'setor_id'})
    assert set(mesh.setor_id)==set(old.setor_id)
    dif=old.set_index('setor_id').geometry.to_frame('old').join(mesh.set_index('setor_id').geometry.to_frame('new'))
    maxdiff=max(a.symmetric_difference(b).area for a,b in zip(dif.old,dif.new));assert maxdiff<1e-5
    geo=mesh.merge(old.drop(columns='geometry'),on='setor_id',validate='one_to_one').merge(pop_table(set(mesh.setor_id)),on='setor_id',how='left',validate='one_to_one')
    assert len(geo)==1838 and geo.pop_2022.notna().all(),('População ausente',geo[geo.pop_2022.isna()].setor_id.tolist())
    assert (geo.pop_2022>=0).all();assert np.allclose(geo.pop_2022,geo.pop_malha)
    geo['dens_pop']=geo.pop_2022/geo.set_km2;geo['dens_dom']=geo.dom_ocup/geo.set_km2
    geo['cens_urb']=np.select([geo.situacao.fillna('').str.lower().eq('urbana'),geo.situacao.fillna('').str.lower().eq('rural')],[1,0],default=-1)
    clip=gpd.overlay(geo,bas,how='intersection',keep_geom_type=True);clip=clip[clip.area>.01].copy();clip['rec_km2']=clip.area/1e6;clip['frac_area']=clip.rec_km2/clip.set_km2
    for out,src in [('pop_a_est','pop_2022'),('dom_a_est','dom_set'),('red_a_est','rede_set'),('nrd_a_est','nred_set'),('dir_a_est','V00309')]:clip[out]=clip[src]*clip.frac_area
    fractions=clip.groupby('setor_id').frac_area.sum();assert fractions.le(1+1e-7).all()
    ras=RasterStats(tuple(geo.total_bounds));geo,cfull=ras.add(geo,'setor_inteiro');clip,cclip=ras.add(clip,'recorte_bacia');bas,cbase=ras.add(bas,'bacia')
    bh=geo.loc[geo.mun_cod=='3106200'].geometry.union_all();net,rawnet,netaudit=network_layers(bas,bh)
    geo=add_network(geo,net,bh);print('Rede nos setores inteiros concluída',flush=True)
    clip=add_network(clip,net,bh);summary=add_network(bas,net,bh)
    e=etes(bas)
    oldsummary=gpd.read_file(BASE,layer='resumo_bacias').drop(columns='geometry')
    summary=summary.merge(oldsummary,on=['bas_id','bas_nome'],how='left',validate='one_to_one')
    for idx,b in summary.iterrows():
        c=clip[clip.bas_id==b.bas_id];p=c.pop_a_est.sum();summary.at[idx,'pop_a_est']=p;summary.at[idx,'dens_pop']=p/b.geometry.area*1e6
        summary.at[idx,'pop_u_est']=c.loc[c.cens_urb==1,'pop_a_est'].sum();summary.at[idx,'pop_r_est']=c.loc[c.cens_urb==0,'pop_a_est'].sum();summary.at[idx,'pct_pop_u']=100*summary.at[idx,'pop_u_est']/p if p>0 else np.nan
        summary.at[idx,'n_ete']=int((e.bas_id==b.bas_id).sum())
        assert abs(c.uso_npix.sum()-b.uso_npix)<=2,(b.bas_id,'contagem de pixels')
        assert abs(c.uso_valid.sum()-b.uso_valid)<=2,(b.bas_id,'pixels válidos')
        if b.area_bh>0:assert np.allclose(sum(net.loc[net.bas_id==b.bas_id,'comp_m'])/1000,b.rede_t_km,rtol=1e-8,atol=1e-6)
    archive_outputs();gpkg=OUT/'integracao_territorial_teco.gpkg'
    for g,n,l in [(geo,'setores_integrados_inteiros','setores_inteiros'),(clip,'setores_integrados_bacias','setores_bacias'),(summary,'resumo_integrado_bacias','resumo_bacias'),(net,'rede_bh_bacias','rede_bh_consolidada')]:export_vector(g,n,gpkg,l)
    rawnet.to_file(gpkg,layer='rede_bh_registros_origem',driver='GPKG',index=False)
    if len(e):export_vector(e,'ete_bacias',gpkg,'ete_cadastro')
    ras.write_clip(bas)
    pd.DataFrame(cfull+cclip+cbase).to_csv(OUT/'uso_ocupacao_por_classe.csv',sep=';',encoding='utf-8-sig',index=False)
    clip.drop(columns='geometry').to_csv(OUT/'atributos_integrados_bacias.csv',sep=';',encoding='utf-8-sig',index=False)
    summary.drop(columns='geometry').to_csv(OUT/'resumo_bacias.csv',sep=';',encoding='utf-8-sig',index=False)
    rawnet.drop(columns='geometry').to_csv(OUT/'rede_bh_registros_origem.csv',sep=';',encoding='utf-8-sig',index=False)
    fields=list(dict.fromkeys(c for a in [geo,clip,summary,net,e] for c in a.columns if c!='geometry'));assert all(c in DESC for c in fields),[c for c in fields if c not in DESC]
    pd.DataFrame([dict(campo=c,descricao=DESC[c]) for c in fields]).to_csv(OUT/'dicionario_campos.csv',sep=';',encoding='utf-8-sig',index=False)
    inputs=[POP,LULC,BASE]
    for p in [MESH,NETWORK,BASIN,ETE]:inputs.extend(p.with_suffix(ext) for ext in ['.shp','.dbf','.shx','.prj','.cpg','.cst'] if p.with_suffix(ext).exists())
    audit=dict(created=dt.datetime.now().isoformat(),crs='EPSG:31983',population_year=2022,population_revision='2026-05-20',landuse_declared_year=2025,landuse_year_internal_metadata_confirmed=False,population_reference_not_updated_to_landuse_year=True,mesh_difference_from_previous_m2=maxdiff,sector_count=len(geo),intersection_count=len(clip),pop_missing=int(geo.pop_2022.isna().sum()),zero_population_sectors=int(geo.pop_2022.eq(0).sum()),landuse_pixel_area_m2=ras.cell_area,landuse_zonal_rule='Native aligned pixels, centre-in-polygon, no resampling; percentages over valid pixels; outside raster remains NoData',population_allocation='Uniform area weighting only for clipped counts. No assignment to urban pixels or buildings.',population_by_landuse_pixels_calculated=False,network=netaudit,network_outside_bh_is_null=True,sector_network_lengths_non_additive_on_shared_boundaries=True,basin_network_lengths_unique=True,ete_count=len(e),ete_operation_or_efficiency_verified=False,summary=summary.drop(columns='geometry').replace({np.nan:None}).to_dict(orient='records'),inputs=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in inputs],checks=['Provided sector geometry matches previous census extraction','All selected sectors have official 2022 population','Area fractions per sector sum to at most one','Land-cover groups partition all valid pixels','Recut sector pixel counts sum to basin pixel counts','Network S/N geometric overlap is isolated as conflict','Unique linework lengths conserved at basin scale','No zero substituted for missing BH coverage outside BH','SHP readback validates IDs, CRS, null masks and numerical fields'])
    (OUT/'auditoria_integracao.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
    readme(audit);preview(clip,bas)
    print(json.dumps(dict(sectors=len(geo),intersections=len(clip),summary=[{k:r[k] for k in ['bas_nome','pop_a_est','dens_pop','pct_urb','uso_cov','area_bh','rede_s_km','rede_c_km','n_ete']} for r in audit['summary']]),ensure_ascii=True),flush=True)

# Readme
def readme(a):
    p=['# TECO: população, uso do solo e cadastro de rede de esgoto','',
    'Sistema SIRGAS 2000 / UTM 23S, EPSG:31983. A população refere-se ao Censo 2022. O uso do solo foi identificado como 2025 no projeto e nos códigos anteriores; os metadados internos do raster não confirmam o ano. A integração não atualiza a população para 2025 nem mede crescimento urbano no tempo.','',
    '## Como abrir','',
    'Abra TECO_integracao_territorial.qgz no QGIS após a etapa de conferência. Os grupos permitem alternar população, área urbanizada, esgotamento, cadastro de rede e ETEs. Integracao_territorial_TECO.zip contém o conjunto portável completo. O projeto original permanece intacto.','',
    '## Camadas principais','',
    '- shapefiles/setores_integrados_bacias.shp: camada principal para análise nas três bacias, com população, densidade, saneamento e uso do solo.','- shapefiles/setores_integrados_inteiros.shp: setores na unidade estatística original.','- shapefiles/resumo_integrado_bacias.shp: resumo das três bacias.','- shapefiles/rede_bh_bacias.shp: disponibilidade cadastrada por traçado, consolidada sem duplicar sobreposições.','- shapefiles/ete_bacias.shp: pontos de ETE no cadastro recebido, se houver dentro das bacias.','- integracao_territorial_teco.gpkg reúne as camadas e mantém também os registros originais de rede recortados.','- uso_ocupacao_bacias.tif: recorte alinhado ao raster original, sem reamostragem.','- dicionario_campos.csv descreve os campos; resumo_bacias.csv e atributos_integrados_bacias.csv permitem conferir os valores.','',
    '## População e adensamento','',
    'pop_2022 é a população oficial do SETOR INTEIRO. dens_pop é pop_2022 / set_km2, em habitantes/km². No recorte, essa densidade continua referenciada ao setor inteiro. pop_a_est é a estimativa proporcional à área do setor dentro da bacia. Não somar pop_2022 no recorte, pois um setor pode participar de mais de uma bacia. Somar somente pop_a_est para o resumo territorial.',
    'No resumo por bacia, dens_pop usa a população estimada e a área da bacia. A alocação uniforme pode distorcer resultados de setores parcialmente recortados, principalmente onde a ocupação se concentra. Não foram atribuídos moradores a cada pixel urbanizado. A classe de área urbanizada inclui usos não residenciais e não comprova a localização dos domicílios.',
    'cens_urb e pct_pop_u descrevem a situação urbana/rural censitária, que difere da mancha urbanizada identificada pelo uso do solo. Não interpretar população de setor urbano como população localizada em pixels urbanos.','',
    '## Uso e ocupação','',
    'Os códigos foram relacionados à legenda fornecida do MapBiomas 10 m, Coleção 4. O código 24 corresponde a área urbanizada. A resolução efetiva do arquivo reprojetado é registrada na auditoria. O cálculo conta centros de pixels contidos em cada geometria, sem interpolação. As áreas são aproximadas pela contagem de pixels e os percentuais usam somente pixels válidos. uso_cov informa a completude da cobertura, inclusive partes de setores que ultrapassam o raster.',
    'urb_km2/pct_urb, veg_km2/pct_veg, agro_km2/pct_agro, min_km2/pct_min, agua_km2/pct_agua e nveg_km2/pct_nveg caracterizam as geometrias. No arquivo de setores inteiros, representam o setor inteiro; no de recortes, representam apenas o recorte. A categoria agro inclui silvicultura; água inclui aquicultura. Os percentuais não indicam intensidade de resistência antimicrobiana. uso_ocupacao_por_classe.csv preserva o detalhamento por código original.','',
    '## Rede de BH: significado e qualidade','',
    'Segundo o dicionário da PBH, IND_RDESG informa existência de rede no trecho ou fragmento: S sim, N não e branco sem informação. LADO_RDESG distingue ambos os lados, esquerdo e direito. DATA é a data de apuração, não de instalação. A camada não é um cadastro de ligações residenciais nem comprova encaminhamento para tratamento. O denominador de pct_t_s é comprimento cadastrado, não domicílios ou habitantes.',
    'Foram preservados os registros de origem no GeoPackage. As geometrias coincidentes de S e N foram isoladas como C (conflito), sem escolher um status automaticamente. Geometrias sem informação que coincidem com registros conhecidos não são somadas novamente. As extensões por bacia são únicas e as quatro classes são geometricamente exclusivas. Não se deve somar extensões entre setores: trechos nas divisas podem tocar mais de um setor.',
    'Fora do domínio municipal de BH, os indicadores de rede ficam NULOS, não zero. area_bh e bh_pct mostram o domínio efetivamente considerado. Em BH sem trecho cadastrado no recorte, rede_qual=sem_tr não significa ausência comprovada de infraestrutura. dens_rede usa somente a área de BH no denominador. Dados de Contagem, Betim, Ibirité, Sarzedo e demais parcelas não foram inventados ou extrapolados.','',
    '## ETEs e limites de interpretação','',
    _cp_adaptar('A camada de ETEs utiliza o arquivo já recebido em E:/teco/ete. A presença de um ponto, sua fase ou situação de licenciamento não demonstra operação atual, vazão atendida, eficiência de tratamento ou conexão de cada setor. Não foi construído índice de RAM, pesos, k-means ou Moran nesta etapa. Os insumos e o projeto E:/teco/projeto_teco.qgz foram preservados. A delimitação das bacias é a fornecida, ainda sujeita à conferência hidrológica indicada em seu script de origem.'),'',
    '## Complementos recomendados, sem ampliar o número de eixos do estudo','',
    '1. CNEFE 2022, filtrado para endereços domiciliares, para melhorar o rateio nos setores cortados e preparar uma alocação dasimétrica. Um endereço ainda não informa número de residentes, ocupação ou ligação à rede. https://www.ibge.gov.br/estatisticas/sociais/populacao/38734-cadastro-nacional-de-enderecos-para-fins-estatisticos.html',
    '2. Cadastro de rede dos demais municípios, interceptores/elevatórias, áreas de atendimento e destino dos lançamentos, com data de referência. Para ETEs, vazões e operação atual são mais úteis que somente a localização.',
    '3. CNES georreferenciado, incluindo hospitais, UBS, urgências, laboratórios e diálise. Pode integrar o eixo de serviços de saúde já previsto, sem criar automaticamente mais variáveis.',
    '4. Confirmar o ano/coleção/banda do raster e, se possível, disponibilizar uso do solo 2022 para uma comparação temporalmente coerente. Manter 2025 como retrato mais recente é possível, desde que a diferença temporal seja explicitada.','',
    '## Resumo exploratório por bacia','',
    '| Bacia | População estimada por área* | Habitantes/km²* | Área urbanizada entre pixels válidos (%) | Cobertura do raster (%) |','|---|---:|---:|---:|---:|']
    for r in a['summary']:p.append(f"| {r['bas_nome']} | {r['pop_a_est']:.1f} | {r['dens_pop']:.1f} | {r['pct_urb']:.2f} | {r['uso_cov']:.2f} |")
    p+=['','*Estimativa exploratória por rateio de área. Não é contagem observada da população dentro de cada bacia.','',
    '## Fontes e reprodução','',
    'População: Agregados por setores, Básico BR, revisão 20/05/2026, IBGE. https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/Agregados_por_Setor_csv/Agregados_por_setores_basico_BR_20260520.zip',
    'Malha: shapefile MG_setores_CD2022 fornecido pelo autor. Seus códigos e geometrias coincidem com o recorte usado na etapa anterior.',
    'Dicionário de rede PBH: https://ckan.pbh.gov.br/dataset/cb4df0e5-0849-4d1f-9f19-32a189824a7a/resource/329ad4ec-5912-457d-b13a-134747a2e55a/download/trecho_rede_esgoto.pdf',
    _cp_adaptar('Scripts em E:/teco/codigo/integrar_populacao_uso_rede.py e E:/teco/codigo/projeto_integracao_qgis.py. Saídas substituídas são preservadas em E:/teco/descontinuado. A auditoria registra fontes e hashes.')]
    (OUT/'LEIA_PRIMEIRO.md').write_text('\n'.join(p),encoding='utf8')

# Preview
def preview(clip,bas):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import BoundaryNorm,ListedColormap
    from matplotlib.patches import Patch
    from matplotlib.ticker import FuncFormatter,MaxNLocator
    colors=['#edf4f8','#c4dce8','#8bbbd2','#438eb4','#145674'];geo=clip.to_crs(4674);bg=bas.to_crs(4674)
    for field,title,bins in [('dens_pop','Densidade populacional dos setores - Censo 2022 (hab./km²)',[0,1000,5000,10000,20000,np.inf]),('pct_urb','Área urbanizada entre pixels válidos (%) - ano informado: 2025',[0,20,40,60,80,100.00001])]:
        fig,axs=plt.subplots(1,3,figsize=(14,6.5));cmap=ListedColormap(colors);norm=BoundaryNorm(bins,5)
        for ax,(_,b) in zip(axs,bg.iterrows()):
            g=geo[geo.bas_id==b.bas_id];g.plot(ax=ax,column=field,cmap=cmap,norm=norm,edgecolor='#4f626b',linewidth=.18,missing_kwds={'color':'#d2d2d2','hatch':'///'});bg[bg.bas_id==b.bas_id].boundary.plot(ax=ax,color='#173b4b',linewidth=1.1)
            ax.set_title({'vargem_flores':'Vargem das Flores','pampulha':'Lagoa da Pampulha','ibirite_regap':'Ibirité / REGAP'}[b.bas_id],fontsize=12,fontweight='bold',pad=8);ax.set_aspect(1/np.cos(np.deg2rad(b.geometry.centroid.y)))
            ax.xaxis.set_major_locator(MaxNLocator(3));ax.yaxis.set_major_locator(MaxNLocator(3));ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{abs(v):.2f}°O'));ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{abs(v):.2f}°S'));ax.tick_params(labelsize=8);ax.set_xlabel('');ax.set_ylabel('')
        labels=['0–1.000','>1.000–5.000','>5.000–10.000','>10.000–20.000','>20.000'] if field=='dens_pop' else ['0–20%','>20–40%','>40–60%','>60–80%','>80–100%']
        fig.legend(handles=[Patch(facecolor=c,edgecolor='#536064',label=l) for c,l in zip(colors,labels)],loc='lower center',bbox_to_anchor=(.5,.08),ncol=5,frameon=False,fontsize=9)
        fig.suptitle(title,fontsize=14,fontweight='bold',y=.96);fig.text(.5,.025,'SIRGAS 2000 · Densidade referenciada ao setor inteiro; uso do solo calculado no recorte · Prévia para conferência',ha='center',fontsize=8,color='#526b76');fig.subplots_adjust(left=.06,right=.98,bottom=.22,top=.86,wspace=.28)
        fig.savefig(OUT/f'Previa_{field}.png',dpi=200,facecolor='white');plt.close(fig)

if __name__=='__main__':main()
