# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/output/01_integracao_territorial/integracao_territorial_teco.gpkg | gpd.read_file | camada='setores_bacias'.
# Entrada: E:/teco/sub_bacia/shapefiles_v6_20261109_141015/sub_bacias_exclusivas.shp | gpd.read_file.
# Entrada: E:/teco/dados_publicos/cnes/estabelecimentos_ativos_municipios.json | f.read_text.
# Entrada: E:/teco/dados_publicos/cnes/tipos.json | .read_text.
# Entrada: E:/teco/teco_base/mg_mun/ide_1103_mg_municipios_pol.shp | gpd.read_file.
# Entrada: E:/teco/sub_bacia/br.id/dem_utm_30m.tif | rasterio.open.
# Entrada: E:/teco/sub_bacia/br.id/direcao_d8.tif | rasterio.open.
# Entrada: E:/teco/reservatorio/{lakefile}.shp | gpd.read_file.
# Entrada: E:/teco/reservatorio/{k}.shp | gpd.read_file.
# Entrada: E:/teco/hidrografia/hidrografia.shp | gpd.read_file.
# Entrada: E:/teco/vias/malha_viaria.shp | gpd.read_file.
# Entrada: E:/teco/teco_base/uso_terra/uso_terra-reservatorio.tif | rasterio.open.
# Entrada: E:/teco/output/02_avaliacao_espacial/tabelas/selecao_kmeans.csv | pd.read_csv.
# Entrada: E:/teco/output/02_avaliacao_espacial/tabelas/sensibilidade_pesos.csv | pd.read_csv.
# Campos/chaves em whole: geometry, pop_2022, setor_id.
# Campos/chaves em clipped: bas_id, dom_a_est, geometry, pct_rede, pop_a_est, red_a_est, setor_id.
# Campos/chaves em x: codigo_tipo_unidade, descricao_tipo_unidade.
# Campos/chaves em d: lat, latitude_estabelecimento_decimo_grau, lon, longitude_estabelecimento_decimo_grau.
# Campos/chaves em d.loc: lat, lon.
# Campos/chaves em b: geometry, id.
# Campos/chaves em g: CNES, codigo_municipio, geometry.
# Campos/chaves em muni: geocodigo, geometry.
# Campos/chaves em c: bas_id, geometry, setor_id.
# Campos/chaves em AUD: analise, cnes.
# Campos/chaves em a.loc: def_rede, dens_pop, pressao, quintil, setor_id.
# Campos/chaves em r: silhouette, slug, titulo.
# Campos/chaves em best: k.
# Campos/chaves em loc: lisa, q_fdr.
# Campos/chaves em a: bas_id, cluster, d8_cob_pct, dist_hid_km, geometry, lisa, pressao, q_fdr, quintil, setor_id.
# Campos/chaves em l: t.
# Campos/chaves em routes: bacia.
# Campos/chaves em mouths: bacia, proxy_nr.
# Campos/chaves em km: k, silhouette.
# Campos/chaves em ss: mantem_P80_pct, peso_pop.
# Campos/chaves em ax.spines: right, top.
# Saída: E:/teco/output/02_avaliacao_espacial/tabelas/{name} | df.to_csv.
# Saída: E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg | g.to_file.
# Saída: E:/teco/output/02_avaliacao_espacial/shapefiles/{name}.shp | g.to_file.
# Saída: E:/teco/output/02_avaliacao_espacial/rasters/{name} | rasterio.open.
# Saída: E:/teco/output/02_avaliacao_espacial/figuras/{slug}.{fmt} | fig.savefig.
# Saída: E:/teco/output/02_avaliacao_espacial/figuras/17_diagnostico_agrupamentos.{fmt} | fig.savefig.
# Saída: E:/teco/output/02_avaliacao_espacial/figuras/18_correlacoes_variaveis.{fmt} | fig.savefig.
# Saída: E:/teco/output/02_avaliacao_espacial/auditoria/galeria.json | .write_text.
# Saída: E:/teco/output/02_avaliacao_espacial/index.html | .write_text.
# Saída: E:/teco/output/02_avaliacao_espacial/auditoria/auditoria.json | .write_text.
# Campos/chaves gerados em AUD: analise, bases, cartografia, cnes, d8.
# Campos/chaves gerados em d: lat, lon.
# Campos/chaves gerados em g: ANO_ATUAL, CNES, COORD_DUP, GRUPO, QA_MUN, TIPO.
# Campos/chaves gerados em qa: QA_MUN.
# Campos/chaves gerados em c: hosp_urg_n, saude_n.
# Campos/chaves gerados em a: cluster, def_rede, lisa, lisa_biv, pressao, prioridade, proxy_nr, q_fdr, quintil.
# Campos/chaves gerados em lookup: ND.
# CNES: identificador do estabelecimento de saúde.
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
import json, math, hashlib, datetime, shutil, warnings
from collections import deque
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize, shapes
from rasterio.windows import from_bounds, Window
from shapely.geometry import LineString, shape
from scipy.spatial import cKDTree, distance
from scipy.cluster.vq import kmeans2
from scipy.stats import rankdata, spearmanr
from scipy.sparse import csr_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MaxNLocator
from pyproj import Transformer

ROOT=Path(_cp_texto('', 'posix')); OUT=ROOT/'output/02_avaliacao_espacial'
GPKG=OUT/'teco_avaliacao.gpkg'; CRS=31983
SOURCE=ROOT/'output/01_integracao_territorial/integracao_territorial_teco.gpkg'
BPATH=ROOT/'sub_bacia/shapefiles_v6_20261109_141015/sub_bacias_exclusivas.shp'
SEED=20261111; PERM=999
AUD={'gerado_em':datetime.datetime.now().astimezone().isoformat(),'semente':SEED,'permutacoes':PERM}
for f in ['shapefiles','rasters','figuras','tabelas','auditoria']:(OUT/f).mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'Arial','font.size':9,'svg.fonttype':'none','axes.titleweight':'bold'})

# Log
def log(*x):print(*x,flush=True)

# Csv
def csv(df,name):df.to_csv(OUT/'tabelas'/name,index=False,encoding='utf-8-sig',sep=';',decimal=',')

# Gp
def gp(g,name,shp=False):
    g.to_file(GPKG,layer=name,driver='GPKG')
    if shp:g.to_file(OUT/'shapefiles'/f'{name}.shp',driver='ESRI Shapefile',encoding='UTF-8')

# Raster
def raster(a,profile,name,nodata=-9999,dtype='float32'):
    p=profile.copy();p.update(driver='GTiff',count=1,dtype=dtype,nodata=nodata,compress='deflate')
    p.pop('photometric',None)
    with rasterio.open(OUT/'rasters'/name,'w',**p) as d:d.write(np.where(np.isfinite(a),a,nodata).astype(dtype),1)

# Hashgeom
def hashgeom(g):return hashlib.sha256(b''.join(g.geometry.to_wkb())).hexdigest()

# Rank01
def rank01(a):
    a=np.asarray(a,float);v=np.isfinite(a);o=np.full(len(a),np.nan)
    if v.sum()>1:o[v]=(rankdata(a[v],method='average')-1)/(v.sum()-1)
    elif v.sum():o[v]=0.5
    return o

# Quint
def quint(a):
    a=np.asarray(a,float);o=np.zeros(len(a),int);v=np.isfinite(a)
    if v.sum():o[v]=np.searchsorted(np.quantile(a[v],[.2,.4,.6,.8]),a[v],side='left')+1
    return o

# Bases
def bases():
    whole=gpd.read_file(SOURCE,layer='setores_inteiros').sort_values('setor_id').reset_index(drop=True)
    clipped=gpd.read_file(SOURCE,layer='setores_bacias').sort_values(['bas_id','setor_id']).reset_index(drop=True)
    b=gpd.read_file(BPATH).sort_values('id').reset_index(drop=True)

    pop=whole[['setor_id','pop_2022','geometry']].rename(columns={'setor_id':'CD_SETOR','pop_2022':'POP_TOT'})
    cols=['setor_id','dom_set','rede_set','pct_rede','V00309','V00310','V00311','V00312','V00313','V00314','V00315','V00316','geometry']
    rename={'setor_id':'CD_SETOR','dom_set':'DOM_TOT','rede_set':'DOM_REDE','pct_rede':'PCT_REDE','V00309':'REDE_DIR','V00310':'FOSS_REDE','V00311':'FOSS_SREDE','V00312':'FOSSA_RUD','V00313':'VALA','V00314':'RIO_LAGO','V00315':'OUTRO','V00316':'SEM_BANH'}
    san=whole[cols].rename(columns=rename)
    gp(pop,'populacao_setores',True);gp(san,'esgotamento_setores',True)
    pc=clipped[['setor_id','bas_id','pop_a_est','geometry']].rename(columns={'setor_id':'CD_SETOR','bas_id':'BACIA','pop_a_est':'POP_EST'})
    sc=clipped[['setor_id','bas_id','dom_a_est','red_a_est','pct_rede','geometry']].rename(columns={'setor_id':'CD_SETOR','bas_id':'BACIA','dom_a_est':'DOM_EST','red_a_est':'REDE_EST','pct_rede':'PCT_REDE'})
    gp(pc,'populacao_recorte_estimado',True);gp(sc,'esgoto_recorte_estimado',True)
    assert hashgeom(pop)==hashgeom(san) and pop.CD_SETOR.equals(san.CD_SETOR)
    assert hashgeom(pc)==hashgeom(sc) and len(pop)==1838 and len(clipped)==1877
    assert whole.setor_id.is_unique and (whole.pop_2022.dropna()>=0).all()
    valid=whole.pct_rede.dropna();assert valid.between(0,100).all()
    AUD['bases']={'setores_inteiros':len(whole),'recortes_setor_bacia':len(clipped),'hash_geometria_igual':hashgeom(pop),'populacao_nulos':int(whole.pop_2022.isna().sum()),'esgoto_percentual_nulos':int(whole.pct_rede.isna().sum()),'crs':'EPSG:31983','fracao_area_max':float(clipped.groupby('setor_id').frac_area.sum().max())}
    csv(pd.DataFrame([{'arquivo':n,'campo':c,'descricao':desc} for n,c,desc in [
        ('populacao_setores','CD_SETOR','Identificador IBGE; texto com 15 dígitos.'),('populacao_setores','POP_TOT','Total oficial de pessoas do setor inteiro (v0001), Censo 2022. Não soma variáveis sobrepostas.'),
        ('esgotamento_setores','DOM_TOT','Domicílios particulares permanentes ocupados, V00001; denominador do tema esgoto.'),('esgotamento_setores','DOM_REDE','V00309 + V00310, somente se ambas publicadas.'),('esgotamento_setores','PCT_REDE','100 × DOM_REDE/DOM_TOT. Nulo quando sigilo, ausência ou denominador zero.'),
        ('esgotamento_setores','REDE_DIR','Rede geral OU pluvial, V00309; não comprova tratamento.'),('esgotamento_setores','FOSS_REDE','Fossa séptica/filtro ligada à rede, V00310.'),('esgotamento_setores','FOSS_SREDE','Fossa séptica/filtro não ligada à rede; não equivale a lançamento sem tratamento.'),('esgotamento_setores','FOSSA_RUD','Fossa rudimentar/buraco.'),('esgotamento_setores','VALA','Vala.'),('esgotamento_setores','RIO_LAGO','Rio, lago, córrego ou mar.'),('esgotamento_setores','OUTRO','Outro destino.'),('esgotamento_setores','SEM_BANH','Sem banheiro/sanitário.'),
        ('populacao_recorte_estimado','POP_EST','POP_TOT × fração de área; estimativa uniforme no recorte, não contagem censitária da bacia.'),('esgoto_recorte_estimado','DOM_EST / REDE_EST','Contagens do setor multiplicadas pela mesma fração de área. Percentual herda o setor inteiro.')]]),'dicionario_bases.csv')
    gp(b,'bacias_estudo');return whole,clipped,b

# Cnes
def cnes(b,c):
    f=ROOT/'dados_publicos/cnes/estabelecimentos_ativos_municipios.json'
    d=pd.DataFrame(json.loads(f.read_text(encoding='utf8')))
    types=json.loads((f.parent/'tipos.json').read_text(encoding='utf8'))['tipos_unidade']
    td={x['codigo_tipo_unidade']:x['descricao_tipo_unidade'] for x in types}
    d['lon']=pd.to_numeric(d.longitude_estabelecimento_decimo_grau,errors='coerce');d['lat']=pd.to_numeric(d.latitude_estabelecimento_decimo_grau,errors='coerce')
    ok=d.lon.between(-50,-35)&d.lat.between(-25,-10)
    csv(d.loc[~ok,['codigo_cnes','nome_fantasia','lat','lon']],'cnes_coordenadas_invalidas.csv')
    g=gpd.GeoDataFrame(d.loc[ok].copy(),geometry=gpd.points_from_xy(d.loc[ok,'lon'],d.loc[ok,'lat']),crs=4326).to_crs(CRS)
    g=gpd.sjoin(g,b[['id','geometry']],predicate='intersects').drop(columns='index_right').rename(columns={'id':'bacia'})
    assert g.codigo_cnes.is_unique
    g['CNES']=g.codigo_cnes.astype(str).str.zfill(7);g['TIPO']=g.codigo_tipo_unidade.map(td)
    def group(t):
        if t in [5,7,15,62]:return 'Hospital / hospital-dia'
        if t in [20,21,73]:return 'Urgência / pronto atendimento'
        if t in [1,2]:return 'Atenção básica'
        if t==43:return 'Farmácia (cadastro CNES)'
        if t in [4,22,36,39,61,69,70,72,78,80,67]:return 'Outros serviços assistenciais'
        return 'Administrativo / móvel / outros'
    g['GRUPO']=g.codigo_tipo_unidade.map(group)
    g['COORD_DUP']=g.groupby(['lon','lat']).CNES.transform('size')
    muni=gpd.read_file(ROOT/'teco_base/mg_mun/ide_1103_mg_municipios_pol.shp',where="geocodigo IN ('3106200','3118601','3106705','3129806','3165537','3109006','3154606','3124104')").to_crs(CRS)
    qa=gpd.sjoin(g[['CNES','codigo_municipio','geometry']],muni[['geocodigo','geometry']],how='left',predicate='intersects').drop_duplicates('CNES')
    qa['QA_MUN']=(qa.codigo_municipio.astype(str).str[:6]==qa.geocodigo.astype(str).str[:6]).astype(int)
    csv(pd.DataFrame(qa.drop(columns='geometry')),'cnes_conferencia_municipio.csv')
    qmap=qa.set_index('CNES').QA_MUN;g['QA_MUN']=g.CNES.map(qmap).fillna(0).astype(int)
    g['ANO_ATUAL']=g.data_atualizacao.str[:4]

    keep=['CNES','nome_fantasia','TIPO','GRUPO','codigo_municipio','bacia','numero_cnpj','data_atualizacao','COORD_DUP','QA_MUN','lon','lat','geometry']
    g=g[keep].rename(columns={'nome_fantasia':'NOME','codigo_municipio':'MUNICIPIO','numero_cnpj':'CNPJ','data_atualizacao':'ATUALIZADO'})
    gp(g,'saude_cnes_ativos');gp(g.rename(columns={'MUNICIPIO':'MUN_IBGE','ATUALIZADO':'DT_ATUAL'}),'saude_cnes_ativos_shape',True)
    csv(pd.DataFrame(g.drop(columns='geometry')),'cnes_ativos_bacias.csv')
    csv(g.groupby(['bacia','GRUPO']).size().rename('quantidade').reset_index(),'cnes_resumo_bacias.csv')

    q=gpd.sjoin(g.loc[g.QA_MUN==1,['CNES','GRUPO','geometry']],c[['setor_id','bas_id','geometry']],predicate='intersects').sort_values(['CNES','setor_id']).drop_duplicates('CNES')
    n=q.groupby(['bas_id','setor_id']).size()
    c=c.copy();c['saude_n']=[n.get((r.bas_id,r.setor_id),0) for r in c.itertuples()]
    hp=g[g.GRUPO.isin(['Hospital / hospital-dia','Urgência / pronto atendimento'])]
    nh=q[q.GRUPO.isin(['Hospital / hospital-dia','Urgência / pronto atendimento'])].groupby(['bas_id','setor_id']).size()
    c['hosp_urg_n']=[nh.get((r.bas_id,r.setor_id),0) for r in c.itertuples()]
    AUD['cnes']={'consultados':len(d),'dentro_bacias':len(g),'coordenadas_invalidas':int((~ok).sum()),'municipio_incompativel':int((g.QA_MUN==0).sum()),'pontos_com_coordenada_compartilhada':int((g.COORD_DUP>1).sum()),'hospitais_urgencia':len(hp),'usados_contagem_setores':len(q),'natureza':'cadastro ativo atual, não série de 2016-2025; coordenadas cadastrais não validadas em campo; divergentes de município não entram nas contagens'}
    log('CNES',AUD['cnes']);return g,c

D8={1:(-1,1),2:(-1,0),3:(-1,-1),4:(0,-1),5:(1,-1),6:(1,0),7:(1,1),8:(0,1)}

# Terrain routing
def terrain_routing(b,c):
    rows=[];paths=[];mouths=[];layers={};sector_rows=[]
    for br in b.itertuples():
        key=br.id;folder=ROOT/'sub_bacia'/key
        with rasterio.open(folder/'dem_utm_30m.tif') as ds:dem=ds.read(1).astype(float);p=ds.profile;t=ds.transform;nod=ds.nodata
        if nod is not None:dem[dem==nod]=np.nan
        with rasterio.open(folder/'direcao_d8.tif') as ds:dr=ds.read(1);assert ds.transform==t and ds.shape==dem.shape
        h,w=dem.shape
        mask=rasterize([(br.geometry,1)],out_shape=dem.shape,transform=t,dtype='uint8').astype(bool)
        lakefile={'pampulha':'pampulha','vargem_flores':'vargem_flores','ibirite_regap':'ibirite_regap'}[key]
        lake=gpd.read_file(ROOT/'reservatorio'/f'{lakefile}.shp').to_crs(CRS)
        lm=rasterize([(x,1) for x in lake.geometry],out_shape=dem.shape,transform=t,all_touched=True,dtype='uint8').astype(bool)
        gy,gx=np.gradient(dem,30.,30.);slope=100*np.hypot(gx,gy)
        slclass=np.digitize(slope,[3,8,20,45,75])+1
        raster(np.where(mask,dem,np.nan),p,f'{key}_hipsometria.tif')
        raster(np.where(mask,slope,np.nan),p,f'{key}_declividade_pct.tif')
        raster(np.where(mask,slclass,0),p,f'{key}_declividade_embrapa.tif',nodata=0,dtype='uint8')

        dest=np.full(h*w,-1,np.int64);flatidx=np.arange(h*w).reshape(h,w)
        for code,(dy,dx) in D8.items():
            yy,xx=np.where(dr==code);ny=yy+dy;nx=xx+dx;ok=(ny>=0)&(ny<h)&(nx>=0)&(nx<w)
            dest[yy[ok]*w+xx[ok]]=ny[ok]*w+nx[ok]

        dest[lm.ravel()]=-1
        status=np.zeros(h*w,np.int8);dist=np.full(h*w,np.nan);target=np.full(h*w,-1,np.int64)
        status[lm.ravel()]=1;dist[lm.ravel()]=0;target[lm.ravel()]=np.flatnonzero(lm)
        starts=np.flatnonzero(mask.ravel())
        for start in starts:
            if status[start]:continue
            track=[];seen=set();j=int(start)
            while j>=0 and status[j]==0 and j not in seen:
                seen.add(j);track.append(j);j=int(dest[j])
            if j>=0 and status[j]==1:
                last=j
                for a in reversed(track):
                    ay,ax=divmod(a,w);ly,lx=divmod(last,w)
                    dist[a]=dist[last]+30*math.hypot(ay-ly,ax-lx);status[a]=1;target[a]=target[last];last=a
            else:
                for a in track:status[a]=2
        conn=status.reshape(h,w)==1
        raster(np.where(mask,dist.reshape(h,w)/1000,np.nan),p,f'{key}_distancia_hidrologica_km.tif')
        raster(np.where(mask,conn.astype(int)+1,0),p,f'{key}_conexao_lago.tif',nodata=0,dtype='uint8')
        sub=c[c.bas_id==key].copy()
        lab=rasterize([(geom,i+1) for i,geom in enumerate(sub.geometry)],out_shape=(h,w),transform=t,dtype='int32')

        deficit=sub.dens_pop.to_numpy(float)*(1-sub.pct_rede.to_numpy(float)/100)
        fullpop=sub.dens_pop.to_numpy(float)
        dep=np.r_[0,deficit][lab]*.0009
        total=np.r_[0,fullpop][lab]*.0009
        source_known=np.isfinite(dep)&(lab>0)&mask
        dep=np.where(source_known,dep,0);total=np.where(mask&(lab>0)&np.isfinite(total),total,0)
        raster(np.where(source_known,dep/.0009,np.nan),p,f'{key}_densidade_proxy_sem_rede.tif')
        mouth=target.reshape(h,w)
        hit=mask&conn&source_known&~lm
        sums=np.bincount(mouth[hit],weights=dep[hit],minlength=h*w)
        land_connected=mask&conn&~lm
        sums_total=np.bincount(mouth[land_connected],weights=total[land_connected],minlength=h*w)
        for j in np.flatnonzero(sums_total>0):
            yy,xx=divmod(int(j),w);x,y=rasterio.transform.xy(t,yy,xx)
            from shapely.geometry import Point
            mouths.append({'bacia':key,'proxy_nr':sums[j],'pop_a_est':sums_total[j],'geometry':Point(x,y)})

        chosen=np.flatnonzero((mask&conn&~lm).ravel())
        chosen=chosen[::max(1,len(chosen)//160)]
        for start in chosen:
            track=[];j=int(start)
            while j>=0 and not lm.ravel()[j] and len(track)<10000:
                yy,xx=divmod(j,w);track.append(rasterio.transform.xy(t,yy,xx));j=int(dest[j])
            if j>=0:
                yy,xx=divmod(j,w);track.append(rasterio.transform.xy(t,yy,xx))
            if len(track)>1:paths.append({'bacia':key,'dist_km':dist[start]/1000,'geometry':LineString(track)})
        nlabels=len(sub)+1;cnt=np.bincount(lab[mask],minlength=nlabels)[1:]
        con=np.bincount(lab[mask&conn],minlength=nlabels)[1:]
        for i,r in enumerate(sub.itertuples()):
            z=mask&(lab==i+1);vals=dist.reshape(h,w)[z];sl=slope[z]
            sector_rows.append({'bas_id':key,'setor_id':r.setor_id,'d8_cob_pct':100*con[i]/cnt[i] if cnt[i] else np.nan,'dist_hid_km':np.nanmedian(vals)/1000 if np.isfinite(vals).any() else np.nan,'decliv_med':np.nanmedian(sl) if len(sl) else np.nan})
        rows.append({'bacia':key,'pixels_bacia':int(mask.sum()),'conectados_lago_pct':100*(mask&conn).sum()/mask.sum(),'pixels_sem_d8_lago':int((mask&~conn).sum()),'pixels_esgoto_conhecido_pct':100*source_known.sum()/mask.sum(),'alt_min_m':float(np.nanmin(dem[mask])),'alt_max_m':float(np.nanmax(dem[mask])),'decliv_med_pct':float(np.nanmedian(slope[mask])),'dist_med_km':float(np.nanmedian(dist.reshape(h,w)[mask])/1000)})
        layers[key]={'dem':np.where(mask,dem,np.nan),'slope_class':np.where(mask,slclass,np.nan),'conn':np.where(mask,conn.astype(float),np.nan),'dist':np.where(mask,dist.reshape(h,w)/1000,np.nan),'t':t,'mask':mask}
        log('RELEVO/D8',rows[-1])
    csv(pd.DataFrame(rows),'auditoria_relevo_d8.csv');AUD['d8']=rows
    routes=gpd.GeoDataFrame(paths,crs=CRS);gp(routes,'rotas_d8_candidatas',True)
    mouths=gpd.GeoDataFrame(mouths,crs=CRS);gp(mouths,'entradas_lago_proxy',True)
    c=c.merge(pd.DataFrame(sector_rows),on=['bas_id','setor_id'],how='left',validate='one_to_one')
    return c,layers,routes,mouths

# Ari
def ari(a,b):
    _,a=np.unique(a,return_inverse=True);_,b=np.unique(b,return_inverse=True);n=len(a)
    tab=np.bincount(a*(b.max()+1)+b,minlength=(a.max()+1)*(b.max()+1)).reshape(a.max()+1,b.max()+1)
    comb=lambda x:(x*(x-1)/2).sum()
    x=comb(tab);r=comb(tab.sum(0));s=comb(tab.sum(1));e=r*s/(n*(n-1)/2);den=(r+s)/2-e
    return (x-e)/den if den else 1.

# Fitkm
def fitkm(x,k,seed,starts=12):
    best=None
    for r in range(starts):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore');cent,l=kmeans2(x,k,iter=100,minit='++',rng=np.random.default_rng(seed+r))
        if len(np.unique(l))!=k:continue
        loss=np.sum((x-cent[l])**2)
        if best is None or loss<best[0]:best=(loss,cent,l)
    if best is None:raise RuntimeError('K-means sem todos os grupos')
    return best

# Silhouette
def silhouette(x,l):
    d=distance.cdist(x,x);s=[]
    for i,cl in enumerate(l):
        same=l==cl;n=same.sum()
        if n<=1:s.append(0);continue
        a=d[i,same].sum()/(n-1);b=min(d[i,l==k].mean() for k in np.unique(l) if k!=cl)
        s.append((b-a)/max(a,b) if max(a,b) else 0)
    return float(np.mean(s))

# Weights
def weights(xy,k):
    n=len(xy);idx=cKDTree(xy).query(xy,k=min(k+1,n))[1][:,1:]
    r=np.repeat(np.arange(n),idx.shape[1]);co=idx.ravel()
    w=csr_matrix((np.ones(len(r)),(r,co)),shape=(n,n));w=w.maximum(w.T);w.setdiag(0);w.eliminate_zeros()
    return w.multiply(1/np.asarray(w.sum(1))).tocsr()

# Bh
def bh(p):
    p=np.asarray(p);order=np.argsort(p);q=np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1];o=np.empty(len(p));o[order]=np.minimum(q,1);return o

# Moran
def moran(x,xy,k=8,seed=SEED,local=False,y=None):
    n=len(x);z=(x-x.mean())/x.std(ddof=0);w=weights(xy,k)
    zy=z if y is None else (y-y.mean())/y.std(ddof=0)
    lag=w@zy;obs=float(z@lag/(z@z));rng=np.random.default_rng(seed)
    if y is None:

        sims=[]
        for _ in range(PERM):
            zp=rng.permutation(z);sims.append(zp@(w@zp)/(zp@zp))
        sim=np.asarray(sims)
    else:
        sim=np.array([z@(w@rng.permutation(zy))/(z@z) for _ in range(PERM)])
    expected=-1/(n-1) if y is None else 0.
    pv=(1+np.sum(np.abs(sim-expected)>=abs(obs-expected)))/(PERM+1)
    rec={'n':n,'vizinhos_knn':k,'I':obs,'p_mc_bilateral':pv,'esperado':expected,'permutacoes':PERM}
    if not local:return rec,None
    Ii=z*lag;pvlocal=np.empty(n)

    for i in range(n):
        st,en=w.indptr[i:i+2];nn=w.indices[st:en];ww=w.data[st:en];m=len(nn)
        draws=rng.integers(0,n-1,size=(PERM,m))
        for col in range(1,m):
            bad=(draws[:,col,None]==draws[:,:col]).any(1)
            while bad.any():
                draws[bad,col]=rng.integers(0,n-1,size=bad.sum());bad=(draws[:,col,None]==draws[:,:col]).any(1)
        draws+=draws>=i
        s=z[i]*(zy[draws]@ww);ex=-z[i]**2/(n-1) if y is None else -z[i]*zy[i]/(n-1)
        pvlocal[i]=(1+(np.abs(s-ex)>=abs(Ii[i]-ex)).sum())/(PERM+1)
    q=bh(pvlocal)
    label=np.where((z>=0)&(lag>=0),'HH',np.where((z<0)&(lag<0),'LL',np.where(z>=0,'HL','LH')))
    label=np.where(q<=.05,label,'NS')
    return rec,{'Ii':Ii,'p_local':pvlocal,'q_fdr':q,'lisa':label,'lag':lag}

# Analysis
def analysis(c):
    a=c.copy();a['def_rede']=100-a.pct_rede
    a['pressao']=np.nan;a['quintil']=0;a['cluster']=0;a['lisa']='ND';a['q_fdr']=np.nan
    results=[];kms=[];profiles=[];biv=[];corr=[]

    valid=a.dens_pop.notna()&a.def_rede.notna()&(a.dom_set>0)
    fit=valid & ~a.setor_id.duplicated()
    fitids=a.loc[fit,'setor_id']
    rankp=rank01(np.log1p(a.loc[fit,'dens_pop']));ranks=rank01(a.loc[fit,'def_rede'])
    scores=(rankp+ranks)/2
    scoremap=dict(zip(fitids,scores));qmap=dict(zip(fitids,quint(scores)))
    a.loc[valid,'pressao']=a.loc[valid,'setor_id'].map(scoremap)
    a.loc[valid,'quintil']=a.loc[valid,'setor_id'].map(qmap)
    a['proxy_nr']=a.dens_pop*(1-a.pct_rede/100)
    features=['dens_pop','def_rede']
    x=np.column_stack([np.log1p(a.loc[fit,'dens_pop']),a.loc[fit,'def_rede']]);means=x.mean(0);std=x.std(0);x=(x-means)/std
    for k in range(2,7):
        loss,ce,lab=fitkm(x,k,SEED);sc=silhouette(x,lab)
        stability=[ari(lab,fitkm(x,k,SEED+100+10*s,starts=3)[2]) for s in range(8)]
        kms.append({'k':k,'silhouette':sc,'soma_quadrados':loss,'ARI_med':np.median(stability),'ARI_min':min(stability)})
    best=max(kms,key=lambda r:r['silhouette']);loss,cent,lab=fitkm(x,best['k'],SEED)

    vals=a.loc[fit,'pressao'].to_numpy();order=sorted(np.unique(lab),key=lambda z:vals[lab==z].mean());mapping={l:i+1 for i,l in enumerate(order)}
    cmap=dict(zip(fitids,[mapping[l] for l in lab]));a.loc[valid,'cluster']=a.loc[valid,'setor_id'].map(cmap)
    for cl,g in a.loc[fit].groupby('cluster'):
        profiles.append({'cluster':cl,'setores_unicos':len(g),'dens_pop_med':g.dens_pop.median(),'def_rede_med_pct':g.def_rede.median(),'pressao_med':g.pressao.median()})
    for br,g in a[valid].groupby('bas_id'):
        xy=np.c_[g.geometry.representative_point().x,g.geometry.representative_point().y]
        v=g.pressao.to_numpy(float)
        for k in [4,8,12]:
            r,loc=moran(v,xy,k,local=(k==8));results.append({'bacia':br,'variavel':'indice_exploratorio',**r})
            if loc is not None:
                a.loc[g.index,'lisa']=loc['lisa'];a.loc[g.index,'q_fdr']=loc['q_fdr']
        r,loc=moran(np.log1p(g.dens_pop.to_numpy()),xy,8,y=g.def_rede.to_numpy(),local=True);biv.append({'bacia':br,'X':'log1p_densidade_populacional','W_Y':'deficit_rede_vizinhos',**r})
        a.loc[g.index,'lisa_biv']=loc['lisa'];a.loc[g.index,'qbiv_fdr']=loc['q_fdr']
        for vv,xx in [('log1p_dens_pop',np.log1p(g.dens_pop.to_numpy())),('sem_rede_pct',g.def_rede.to_numpy())]:
            r,_=moran(xx,xy,8);results.append({'bacia':br,'variavel':vv,**r})
        cols=['dens_pop','def_rede','pct_urb','saude_n','decliv_med','dist_hid_km']
        for i,ca in enumerate(cols):
            for cb in cols[i+1:]:
                pair=g[[ca,cb]].dropna();rho=float(spearmanr(pair[ca],pair[cb]).statistic) if len(pair)>3 and pair.nunique().min()>1 else np.nan
                corr.append({'bacia':br,'X':ca,'Y':cb,'n':len(pair),'rho_spearman':rho})

    p=rankp;s=ranks;base=a.loc[fit,'quintil'].to_numpy()
    stability=[]
    for wp in [.25,.4,.5,.6,.75]:
        idx=wp*p+(1-wp)*s;q=quint(idx)
        stability.append({'peso_pop':wp,'peso_deficit':1-wp,'rho_base':spearmanr(idx,a.loc[fit,'pressao']).statistic,'mesmo_quintil_pct':100*np.mean(q==base),'mantem_P80_pct':100*np.mean((q==5)[base==5])})
    a['prioridade']='Informação incompleta'
    a.loc[valid,'prioridade']='Contexto complementar'
    a.loc[valid&(a.quintil>=4),'prioridade']='Pressão relativa elevada'
    a.loc[valid&(a.quintil>=4)&(a.d8_cob_pct>=90),'prioridade']='Investigar conexão superficial'

    a['lisa_biv']=a.lisa_biv.fillna('ND')
    gp(a,'analise_setores');gp(a[['setor_id','bas_id','pressao','quintil','cluster','lisa','q_fdr','d8_cob_pct','dist_hid_km','geometry']].rename(columns={'setor_id':'CD_SETOR','bas_id':'BACIA','pressao':'IND_EXP','quintil':'QUINTIL','cluster':'KMEANS','lisa':'MORAN','q_fdr':'Q_FDR','d8_cob_pct':'D8_COB_PCT','dist_hid_km':'DIST_D8_KM'}),'agrupamentos_setores',True)
    csv(pd.DataFrame(a.drop(columns='geometry')),'analise_setores.csv');csv(pd.DataFrame(results),'moran_global_sensibilidade.csv');csv(pd.DataFrame(biv),'moran_bivariado.csv');csv(pd.DataFrame(kms),'selecao_kmeans.csv');csv(pd.DataFrame(profiles),'perfis_kmeans.csv');csv(pd.DataFrame(corr),'correlacoes_spearman.csv');csv(pd.DataFrame(stability),'sensibilidade_pesos.csv')
    AUD['analise']={'unidades':len(a),'com_indice':int(valid.sum()),'setores_unicos_com_indice':int(fit.sum()),'sem_indice':int((~valid).sum()),'variaveis_indice':features,'ajuste_kmeans_percentis':'Cada setor único entra uma vez no ajuste; rótulos e percentis são transferidos a seus recortes. Moran é calculado nas unidades de cada bacia.','peso':'.5 para percentil de log1p densidade e .5 para percentil déficit de rede','kmeans_escolhido':best,'FDR':'Benjamini-Hochberg dentro de cada bacia; q<=.05; 999 randomizações condicionais; referência kNN8 simetrizado','saude_uso_solo':'contexto e correlações; não incluídos como pesos no cenário base','inferencias':'associações exploratórias; não estima carga, concentração, risco ou probabilidade de ARG'}
    log('ANALISE',AUD['analise']);return a

# Maps
def maps(a,b,health,layers,routes,mouths):
    water=gpd.GeoDataFrame(pd.concat([gpd.read_file(ROOT/'reservatorio'/f'{k}.shp').to_crs(CRS) for k in ['pampulha','vargem_flores','ibirite_regap']],ignore_index=True),crs=CRS)
    hydro=gpd.read_file(ROOT/'hidrografia/hidrografia.shp').to_crs(CRS);hydro=gpd.clip(hydro,b)
    roads=gpd.read_file(ROOT/'vias/malha_viaria.shp').to_crs(CRS);roads=gpd.clip(roads,b)
    gp(hydro,'hidrografia_bacias');gp(roads,'vias_bacias')
    names={'pampulha':'Pampulha','vargem_flores':'Vargem das Flores','ibirite_regap':'Ibirité / REGAP'}
    trans=Transformer.from_crs(CRS,4326,always_xy=True)

    span=max(max(r.geometry.bounds[2]-r.geometry.bounds[0],r.geometry.bounds[3]-r.geometry.bounds[1]) for r in b.itertuples())*1.12
    scale=math.ceil(span/.081/25000)*25000;span=scale*.081
    AUD['cartografia']={'escala_impressao':scale,'largura_eixo_cm':8.1,'lado_quadro_m':span,'figura_cm':[30,14]}
    gallery=[]
    def start(title):
        fig=plt.figure(figsize=(30/2.54,14/2.54));axs=[]
        fig.suptitle(title,x=.5,y=.975,fontsize=13,color='#163d4d',fontweight='bold')
        for j,r in enumerate(b.itertuples()):
            ax=fig.add_axes([.055+j*.321,.235,.27,8.1/14]);axs.append(ax)
            cx,cy=r.geometry.centroid.coords[0];ax.set_xlim(cx-span/2,cx+span/2);ax.set_ylim(cy-span/2,cy+span/2);ax.set_aspect('equal')
            sub=a[a.bas_id==r.id];sub.plot(ax=ax,facecolor='#f2f2ef',edgecolor='#a6afad',linewidth=.12,zorder=1)
            hydro.plot(ax=ax,color='#88b9cc',linewidth=.35,zorder=3)
            ax.set_title(names[r.id],fontsize=10,pad=6)
            ax.xaxis.set_major_locator(MaxNLocator(3));ax.yaxis.set_major_locator(MaxNLocator(3));ax.tick_params(labelsize=8,pad=2)
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos,cy=cy:f'{abs(trans.transform(x,cy)[0]):.2f}°O'.replace('.',',')))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda y,pos,cx=cx:f'{abs(trans.transform(cx,y)[1]):.2f}°S'.replace('.',',')))
            for tick in ax.get_yticklabels():tick.set_rotation(90);tick.set_va('center')
            ax.annotate('',xy=(.944,.944),xytext=(.944,.875),xycoords='axes fraction',arrowprops={'arrowstyle':'-|>','color':'#173e4b','lw':1.1})
            ax.text(.944,.958,'N',transform=ax.transAxes,ha='center',va='bottom',fontsize=9,fontweight='bold')

            length=5000 if span>16000 else 2000;x=cx-span*.43;y=cy-span*.43
            ax.plot([x,x+length/2],[y,y],lw=3,color='#183b45',solid_capstyle='butt',zorder=10);ax.plot([x+length/2,x+length],[y,y],lw=3,color='white',solid_capstyle='butt',zorder=10)
            ax.plot([x,x+length],[y,y],lw=.5,color='#183b45',zorder=11)
            for xx,lab in [(x,'0'),(x+length,f'{length/1000:g} km')]:ax.text(xx,y+span*.016,lab,fontsize=7,ha='center',zorder=12,bbox=dict(facecolor='white',edgecolor='none',pad=.2,alpha=.8))
            ax.text(.975,.027,f'SIRGAS 2000 / UTM 23S\nEscala 1:{scale:,.0f}'.replace(',','.'),transform=ax.transAxes,ha='right',va='bottom',fontsize=6.6,bbox=dict(boxstyle='round,pad=.3',facecolor='white',edgecolor='#b3b9b9',lw=.4,alpha=.92),zorder=15)
            ax.set_xlabel('');ax.set_ylabel('')
        return fig,axs
    def finish(fig,axs,slug,legend=None,colorbar=None):
        for ax,r in zip(axs,b.itertuples()):
            water[water.intersects(r.geometry)].plot(ax=ax,facecolor='#a9d6e5',edgecolor='#326b83',linewidth=.55,zorder=7)
            b[b.id==r.id].boundary.plot(ax=ax,color='#244853',linewidth=.85,zorder=8)
        if legend:fig.legend(handles=legend,loc='lower center',bbox_to_anchor=(.52,.065),ncol=3 if len(legend) in [5,6] else min(len(legend),4),frameon=False,fontsize=8.5,columnspacing=1.4,handletextpad=.45)
        if colorbar:
            sm,label=colorbar;cax=fig.add_axes([.27,.09,.5,.027]);cb=fig.colorbar(sm,cax=cax,orientation='horizontal');cb.set_label(label,fontsize=9,labelpad=3);cb.ax.tick_params(labelsize=8)
        for fmt,dpi in [('png',350),('svg',None)]:fig.savefig(OUT/'figuras'/f'{slug}.{fmt}',dpi=dpi,facecolor='white')
        plt.close(fig);gallery.append({'slug':slug,'titulo':slug.replace('_',' ')})
    for col,title,label,cmap,slug in [
        ('dens_pop','População por setor censitário','Habitantes por km² (setor inteiro)','YlOrRd','01_populacao_densidade'),
        ('pct_rede','Domicílios com rede geral/pluvial ou fossa ligada à rede','Domicílios do setor (%)','YlGnBu','02_esgotamento_rede'),
        ('def_rede','Domicílios sem rede declarada','Domicílios do setor (%)','YlOrRd','03_deficit_rede'),
        ('proxy_nr','Proxy demográfico associado à ausência de rede','Habitantes-equivalentes por km² · alocação uniforme','YlOrRd','15_proxy_demografico_sem_rede'),
        ('pct_urb','Uso e ocupação do solo - área urbanizada','Área urbanizada nos pixels válidos (%)','YlOrBr','04_area_urbanizada')]:
        fig,axs=start(title);vals=a[col].to_numpy();maxv=np.nanpercentile(vals,98) if col=='dens_pop' else 100
        if col=='proxy_nr':maxv=max(1,np.nanpercentile(vals,98))
        norm=matplotlib.colors.Normalize(0,maxv);cm=plt.get_cmap(cmap)
        for ax,r in zip(axs,b.itertuples()):a[a.bas_id==r.id].plot(ax=ax,column=col,cmap=cm,norm=norm,linewidth=.13,edgecolor='#697d7d',missing_kwds={'color':'#d4d4d4','hatch':'///'},zorder=2)
        sm=plt.cm.ScalarMappable(norm=norm,cmap=cm);finish(fig,axs,slug,colorbar=(sm,label+(' · cor limitada ao P98' if col=='dens_pop' else '')))
    fig,axs=start('Estabelecimentos de saúde - cadastro ativo CNES')
    categories=[('Atenção básica','#007b9e','o'),('Hospital / hospital-dia','#b11f38','s'),('Urgência / pronto atendimento','#e17823','^'),('Outros serviços assistenciais','#6d589d','o'),('Farmácia (cadastro CNES)','#278b70','D'),('Administrativo / móvel / outros','#777777','x')]
    for ax,r in zip(axs,b.itertuples()):
        for cat,color,marker in categories:
            g=health[(health.bacia==r.id)&(health.GRUPO==cat)&(health.QA_MUN==1)]
            if len(g):g.plot(ax=ax,color=color,marker=marker,markersize=22 if 'Hospital' in cat else 11,alpha=.8,zorder=6)
        suspect=health[(health.bacia==r.id)&(health.QA_MUN==0)]
        if len(suspect):suspect.plot(ax=ax,color='#252525',marker='+',markersize=16,zorder=7)
    finish(fig,axs,'05_estabelecimentos_saude',legend=[Line2D([],[],marker=m,color='none',markerfacecolor=co,markeredgecolor=co,label=ca,markersize=5) for ca,co,m in categories]+[Line2D([],[],marker='+',color='none',markeredgecolor='#252525',label='Coordenada a revisar',markersize=6)])
    for typ,title,cmap,label,slug in [('dem','Hipsometria','terrain','Elevação (m)','06_hipsometria'),('slope_class','Declividade - classes de relevo Embrapa',None,None,'07_declividade_embrapa'),('dist','Conectividade topográfica com o reservatório','YlGnBu','Distância D8 até a margem (km)','08_distancia_hidrologica')]:
        fig,axs=start(title)
        vals=np.concatenate([l[typ][np.isfinite(l[typ])] for l in layers.values()]);norm=matplotlib.colors.Normalize(np.quantile(vals,.01),np.quantile(vals,.99))
        cm=plt.get_cmap(cmap) if cmap else ListedColormap(['#e8f0c6','#b8d381','#77b36a','#ffca70','#e78650','#b84b43'])
        if typ=='slope_class':norm=BoundaryNorm(np.arange(.5,7.5),6)
        for ax,r in zip(axs,b.itertuples()):
            l=layers[r.id];t=l['t'];h,w=l[typ].shape
            ax.imshow(l[typ],extent=(t.c,t.c+w*t.a,t.f+h*t.e,t.f),cmap=cm,norm=norm,interpolation='nearest',zorder=2)
        if typ=='slope_class':finish(fig,axs,slug,legend=[Patch(color=cm(i),label=s) for i,s in enumerate(['Plano <3%','Suave ondulado 3-8%','Ondulado 8-20%','Forte ondulado 20-45%','Montanhoso 45-75%','Escarpado ≥75%'])])
        else:finish(fig,axs,slug,colorbar=(plt.cm.ScalarMappable(norm=norm,cmap=cm),label))
    for col,title,pal,labels,slug in [
        ('quintil','Pressão antrópica relativa - cenário de pesos iguais',['#cadfe8','#8fc5b1','#e6d276','#e8a96e','#b94445'],['≤P20','P20-P40','P40-P60','P60-P80','>P80'],'09_pressao_quintis'),
        ('cluster','Tipologias multivariadas - k-means',['#7198b1','#b9cda2','#deaf6f','#b36d85','#7b6c9d','#3a8979'],None,'10_kmeans'),
        ('lisa','Associação espacial da pressão relativa - Moran local',['#b93348','#539cae','#efaf7f','#9b7cab','#dfe3df'],['HH','LL','HL','LH','NS'],'11_moran_local'),
        ('lisa_biv','Moran bivariado - população e ausência de rede nos vizinhos',['#b93348','#539cae','#efaf7f','#9b7cab','#dfe3df'],['HH','LL','HL','LH','NS'],'16_moran_bivariado')]:
        fig,axs=start(title);legend=[]
        if col.startswith('lisa'):lookup=dict(zip(labels,pal));lookup['ND']='#bfc4c5';legend=[Patch(color=co,label={'HH':'HH · alto-alto','LL':'LL · baixo-baixo','HL':'HL · alto-baixo','LH':'LH · baixo-alto','NS':'Sem associação significativa','ND':'Informação incompleta'}[v]) for v,co in lookup.items()]
        else:
            cats=sorted(a.loc[a[col]>0,col].unique());lookup={v:pal[int(v)-1] for v in cats};lookup[0]='#bfc4c5';legend=[Patch(color=co,label=(labels[int(v)-1] if labels and v else (f'Perfil {v}' if v else 'Informação incompleta'))) for v,co in lookup.items()]
        for ax,r in zip(axs,b.itertuples()):
            g=a[a.bas_id==r.id];g.plot(ax=ax,color=g[col].map(lookup),edgecolor='#647779',linewidth=.13,zorder=2)
        finish(fig,axs,slug,legend=legend)
    fig,axs=start('Trajetórias superficiais candidatas - direção D8')
    for ax,r in zip(axs,b.itertuples()):
        rr=routes[routes.bacia==r.id];rr.plot(ax=ax,color='#328c94',linewidth=.35,alpha=.7,zorder=4)
        m=mouths[(mouths.bacia==r.id)&(mouths.proxy_nr>0)].nlargest(15,'proxy_nr');ss=5+24*np.sqrt(m.proxy_nr/max(1,m.proxy_nr.max()));m.plot(ax=ax,color='#bd4b45',markersize=ss,edgecolor='white',linewidth=.2,alpha=.85,zorder=8)
    finish(fig,axs,'12_rotas_candidatas',legend=[Line2D([],[],color='#328c94',label='Trajetória topográfica amostrada'),Line2D([],[],marker='o',color='none',markerfacecolor='#bd4b45',markeredgecolor='none',label='15 maiores entradas do proxy sem rede por bacia',markersize=6)])

    fig,axs=start('Rede viária e hidrografia - contexto territorial')
    for ax,r in zip(axs,b.itertuples()):
        ax.collections[0].set_visible(False);roads[roads.intersects(r.geometry)].plot(ax=ax,color='#8d9499',linewidth=.25,zorder=2)
    finish(fig,axs,'13_vias_hidrografia',legend=[Line2D([],[],color='#8d9499',lw=1,label='Vias cadastradas'),Line2D([],[],color='#88b9cc',lw=1,label='Curso hídrico')])

    fig,axs=start('Uso e ocupação do solo - 2025 informado no projeto')
    codes={24:1,1:2,3:2,4:2,5:2,11:2,12:2,9:3,15:3,19:3,21:3,36:3,30:4,31:5,33:5,25:6,29:6}
    colors=['#d57c74','#6b9d78','#d6bd74','#9f88a3','#76b8d0','#c8c2b5']
    with rasterio.open(ROOT/'teco_base/uso_terra/uso_terra-reservatorio.tif') as ds:
        for ax,r in zip(axs,b.itertuples()):
            ax.collections[0].set_visible(False);ww=from_bounds(*r.geometry.bounds,transform=ds.transform).round_offsets().round_lengths();arr=ds.read(1,window=ww);t=ds.window_transform(ww)
            mapped=np.full(arr.shape,np.nan)
            for code,group in codes.items():mapped[arr==code]=group
            m=rasterize([(r.geometry,1)],out_shape=arr.shape,transform=t).astype(bool);mapped[~m]=np.nan
            ax.imshow(mapped,extent=(t.c,t.c+arr.shape[1]*t.a,t.f+arr.shape[0]*t.e,t.f),cmap=ListedColormap(colors),norm=BoundaryNorm(np.arange(.5,7.5),6),interpolation='nearest',zorder=2)
    finish(fig,axs,'14_uso_solo_categorias',legend=[Patch(color=co,label=la) for co,la in zip(colors,['Área urbanizada','Vegetação natural','Agropecuária / silvicultura','Mineração','Água / aquicultura','Outras superfícies'])])

    fig,axs=plt.subplots(1,3,figsize=(12,3.6),layout='constrained')
    g=a[a.cluster>0].drop_duplicates('setor_id');colors=['#7198b1','#deaf6f','#b36d85','#7b6c9d','#3a8979','#537b65']
    for k,gg in g.groupby('cluster'):axs[0].scatter(gg.dens_pop,gg.def_rede,s=9,c=colors[int(k)-1],alpha=.6,label=f'Perfil {k}')
    axs[0].set_xscale('log');axs[0].set_xlabel('Habitantes por km² · escala log');axs[0].set_ylabel('Domicílios sem rede (%)');axs[0].legend(frameon=False);axs[0].set_title('Tipologias dos setores')
    km=pd.read_csv(OUT/'tabelas/selecao_kmeans.csv',sep=';',decimal=',');axs[1].plot(km.k,km.silhouette,'o-',color='#287f88');axs[1].set_xlabel('Número de grupos (k)');axs[1].set_ylabel('Silhouette');axs[1].set_title('Escolha exploratória de k')
    ss=pd.read_csv(OUT/'tabelas/sensibilidade_pesos.csv',sep=';',decimal=',');axs[2].plot(ss.peso_pop,ss.mantem_P80_pct,'o-',color='#b1594e');axs[2].set_ylim(0,105);axs[2].set_xlabel('Peso da densidade populacional');axs[2].set_ylabel('P80 original mantido (%)');axs[2].set_title('Sensibilidade da prioridade relativa')
    for ax in axs:ax.spines[['top','right']].set_visible(False);ax.grid(alpha=.15)
    for fmt in ['png','svg']:fig.savefig(OUT/'figuras'/f'17_diagnostico_agrupamentos.{fmt}',dpi=350)
    plt.close(fig);gallery.append({'slug':'17_diagnostico_agrupamentos','titulo':'Diagnóstico e sensibilidade dos agrupamentos'})
    fig,axs=plt.subplots(1,3,figsize=(12,4),layout='constrained');variables=['dens_pop','def_rede','pct_urb','saude_n','decliv_med','dist_hid_km'];vlabels=['Adensamento','Sem rede','Urbanização','Saúde CNES','Declividade','Distância D8']
    for ax,r in zip(axs,b.itertuples()):
        corr=a[(a.bas_id==r.id)&(a.cluster>0)][variables].corr(method='spearman');im=ax.imshow(corr,vmin=-1,vmax=1,cmap='BrBG');ax.set_xticks(range(6),vlabels,rotation=55,ha='right');ax.set_yticks(range(6),vlabels);ax.set_title(names[r.id])
        for i in range(6):
            for j in range(6):ax.text(j,i,f'{corr.iloc[i,j]:.2f}',ha='center',va='center',fontsize=7,color='white' if abs(corr.iloc[i,j])>.6 else '#18393f')
    fig.colorbar(im,ax=list(axs),shrink=.65,label='Correlação de Spearman (descritiva)')
    for fmt in ['png','svg']:fig.savefig(OUT/'figuras'/f'18_correlacoes_variaveis.{fmt}',dpi=350)
    plt.close(fig);gallery.append({'slug':'18_correlacoes_variaveis','titulo':'Associação descritiva entre variáveis'})
    (OUT/'auditoria/galeria.json').write_text(json.dumps(gallery,ensure_ascii=False,indent=2),encoding='utf8')
    return gallery

# Index
def index(gallery):
    cards=''.join(f'<article><h2>{r["titulo"]}</h2><a href="figuras/{r["slug"]}.svg"><img loading="lazy" src="figuras/{r["slug"]}.png"></a><p><a href="figuras/{r["slug"]}.svg">Abrir versão vetorial</a></p></article>' for r in gallery)
    text='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>TECO | avaliação espacial</title><style>body{font:16px Arial;background:#edf2f2;color:#193c48;margin:0}header,main{max-width:1220px;margin:auto;padding:28px}header{background:white}h1{font-size:30px}p{line-height:1.6}article{background:white;border:1px solid #d3dfdf;border-radius:12px;margin:20px 0;padding:18px}img{width:100%;height:auto}h2{font-size:19px}a{color:#176987}</style><header><h1>TECO · fontes potenciais e conectividade</h1><p>Produtos exploratórios das bacias Pampulha, Vargem das Flores e Ibirité/REGAP. As classificações não representam concentração, carga de genes ou probabilidade de contaminação.</p><p><a href="Relatorio_TECO.pdf">Relatório de métodos e avaliação</a> · <a href="tabelas/dicionario_bases.csv">Dicionário das bases</a></p></header><main>'''+cards+'</main></html>'
    (OUT/'index.html').write_text(text,encoding='utf8')

# Main
def main():

    whole,c,b=bases();health,c=cnes(b,c);c,layers,routes,mouths=terrain_routing(b,c);a=analysis(c)
    gallery=maps(a,b,health,layers,routes,mouths);index(gallery)
    (OUT/'auditoria/auditoria.json').write_text(json.dumps(AUD,ensure_ascii=False,indent=2,default=lambda x:x.item() if isinstance(x,np.generic) else str(x)),encoding='utf8')
    log('CONCLUIDO',OUT)
if __name__=='__main__':main()
