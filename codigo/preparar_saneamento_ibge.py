# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {p} | p.open.
# Entrada: {path} | pd.read_csv.
# Entrada: E:/teco/saneamento_ibge/resultados/shapefiles/{name}.shp | gpd.read_file.
# Entrada: E:/teco/sub_bacia/shapefiles_v6_20261109_141015/sub_bacias_exclusivas.shp | gpd.read_file.
# Entrada: E:/teco/saneamento_ibge/malha_setores_2022/MG_setores_CD2022.gpkg | gpd.read_file.
# Campos/chaves em a: created_at, intersection_count, sector_count, setor, summary.
# Campos/chaves em out: setor.
# Campos/chaves em check: setor_id.
# Campos/chaves em g: dom_set, setor_id.
# Campos/chaves em bas: bas_id.
# Campos/chaves em geom: setor_id.
# Campos/chaves em raw: V00001, V00309, V00310, V00311, V00313, V00314, _merge, dif_soma, dom_set, nred_set, pct_rede, rede_set, soma8.
# Campos/chaves em geo: V00001, bas_id, dpo_malha, mun_cod, mun_nome, n_ausente, n_sigilo, pct_rdir, pct_rede, pop_malha, qual_dado, setor_id, sig_vars.
# Campos/chaves em clip: V00309, bas_id, dom_a_est, frac_area, nrd_a_est, rec_km2, red_a_est, set_km2, setor_id.
# Campos/chaves em v: bas_id, bas_nome.
# Campos/chaves em c: dom_a_est, dom_set, pct_rdir, pct_rede.
# Campos/chaves em c.loc: dir_a_est, dom_a_est, nrd_a_est, red_a_est.
# Campos/chaves em clip.loc: dom_a_est, nrd_a_est, red_a_est.
# Campos/chaves em geo.loc: setor_id.
# Campos/chaves em x: bas_id, bas_nome, cov_dir, dom_a_est, gap_m2, n_setores, pct_rdir.
# Campos/chaves em audit: qualities, summary.
# Campos/chaves em b: bas_id.
# Campos/chaves em bg: bas_id.
# Saída: path.with_suffix('.qml') | .write_text.
# Saída: E:/teco/saneamento_ibge/resultados/shapefiles/{name}.shp | g.to_file.
# Saída: E:/teco/descontinuado/dt.datetime.now().strftime('%Y%m%d_%H%M%S_saneamento_ibge')/manifesto_arquivamento.json | .write_text.
# Saída: Argumento fornecido pelo chamador | .to_json.
# Saída: E:/teco/saneamento_ibge/resultados/saneamento_teco.gpkg | data.to_file.
# Saída: E:/teco/saneamento_ibge/resultados/saneamento_teco.gpkg | gap_gdf.to_file.
# Saída: E:/teco/saneamento_ibge/resultados/valores_originais_selecionados.csv | original.to_csv.
# Saída: E:/teco/saneamento_ibge/resultados/atributos_setores_bacias.csv | .to_csv.
# Saída: E:/teco/saneamento_ibge/resultados/resumo_bacias.csv | .to_csv.
# Saída: E:/teco/saneamento_ibge/resultados/municipios_interceptados.csv | .to_csv.
# Saída: E:/teco/saneamento_ibge/resultados/dicionario_campos.csv | .to_csv.
# Saída: E:/teco/saneamento_ibge/resultados/auditoria_saneamento.json | .write_text.
# Saída: E:/teco/saneamento_ibge/resultados/Shapefiles_saneamento_TECO.zip | zipfile.ZipFile.
# Saída: E:/teco/saneamento_ibge/resultados/LEIA_PRIMEIRO.md | .write_text.
# Saída: E:/teco/saneamento_ibge/resultados/Previa_saneamento_bacias.png | fig.savefig.
# Campos/chaves gerados em geom: setor_id.
# Campos/chaves gerados em raw: dif_soma, dom_set, n_ausente, n_sigilo, nred_set, pct_fossa, pct_nrede, pct_rdir, pct_rede, pct_vrio, qual_dado, rede_set, sig_vars, soma8.
# Campos/chaves gerados em geo: ano, n_ausente, n_bacias, n_sigilo, set_km2, sig_vars, tot_origem.
# Campos/chaves gerados em clip: dir_a_est, frac_area, n_bacias, rec_km2.
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
import json,datetime as dt,hashlib,shutil,zipfile,html,csv
import numpy as np
import pandas as pd
import geopandas as gpd
import pyogrio
from shapely import make_valid
from shapely.ops import unary_union
from xml.sax.saxutils import escape

ROOT=Path(_cp_texto('', 'posix'))
INPUT=ROOT/'saneamento_ibge'
OUT=INPUT/'resultados'
SHP=OUT/'shapefiles'
CRS='EPSG:31983'
BASIN=ROOT/'sub_bacia/shapefiles_v6_20261109_141015/sub_bacias_exclusivas.shp'
MESH=INPUT/'malha_setores_2022/MG_setores_CD2022.gpkg'
CODES=[f'V{i:05d}' for i in range(309,317)]
RAW=['V00001']+CODES
DESC={
 'V00001':'Domicílios particulares permanentes ocupados do setor inteiro',
 'V00309':'Domicílios do setor: rede geral ou pluvial',
 'V00310':'Domicílios do setor: fossa séptica ou filtro ligado à rede',
 'V00311':'Domicílios do setor: fossa séptica ou filtro não ligado à rede',
 'V00312':'Domicílios do setor: fossa rudimentar ou buraco',
 'V00313':'Domicílios do setor: vala',
 'V00314':'Domicílios do setor: rio, lago, córrego ou mar',
 'V00315':'Domicílios do setor: outra destinação',
 'V00316':'Domicílios do setor: sem banheiro e sanitário',
 'setor_id':'Código do setor censitário; texto, 15 dígitos',
 'mun_cod':'Código IBGE do município; texto, 7 dígitos',
 'mun_nome':'Município do setor censitário',
 'situacao':'Situação urbana/rural informada na malha IBGE',
 'pop_malha':'Total de pessoas da malha IBGE com atributos; variável básica v0001',
 'dpo_malha':'Domicílios particulares ocupados da malha IBGE; v0007, inclui permanentes e improvisados',
 'tot_origem':'Origem de dom_set: tabela_p1, malha_DPO0 (ausência de domicílios ocupados confirmada) ou sem_valor',
 'ano':'Ano de referência do Censo, 2022; não é a data de publicação do CSV',
 'dom_set':'Total do setor inteiro, igual a V00001',
 'rede_set':'V00309 + V00310 no setor inteiro; nulo se qualquer parcela for indisponível',
 'nred_set':'V00001 - rede_set; complemento agregado, sem preencher categorias X individuais',
 'pct_rede':'100 × rede_set / dom_set; rede geral/pluvial ou fossa ligada; não comprova tratamento',
 'pct_nrede':'100 × nred_set / dom_set; sem conexão às modalidades censitárias acima; não equivale a lançamento sem tratamento',
 'pct_rdir':'100 × V00309 / V00001; somente destinação direta à rede geral/pluvial',
 'pct_fossa':'100 × V00311 / V00001; fossa séptica/filtro não ligado à rede',
 'pct_vrio':'100 × (V00313 + V00314) / V00001; nulo se alguma parcela for X ou ausente',
 'n_sigilo':'Quantidade de variáveis RAW com X; o X não foi convertido em zero',
 'sig_vars':'Códigos das variáveis com X no registro recebido',
 'n_ausente':'Quantidade de RAW ausentes ou com outros símbolos não numéricos',
 'qual_dado':'completo, rede_disp (demais variáveis parciais), parcial, sem_dom, sem_agreg ou revisar',
 'soma8':'Soma das oito categorias de esgotamento, apenas se todas estiverem disponíveis',
 'dif_soma':'soma8 - V00001, apenas quando os dois totais são conhecidos',
 'set_km2':'Área do setor inteiro em SIRGAS 2000 / UTM 23S',
 'n_bacias':'Número de bacias com interseção de área positiva com o setor',
 'bas_id':'Identificador da bacia delimitada no projeto TECO',
 'bas_nome':'Nome da bacia/reservatório',
 'rec_km2':'Área da interseção setor × bacia, km²',
 'frac_area':'rec_km2 / set_km2; não é fração observada dos domicílios',
 'dom_a_est':'Domicílios estimados no recorte por rateio de área, dom_set × frac_area',
 'red_a_est':'Domicílios estimados com destinação à rede por rateio de área, rede_set × frac_area',
 'nrd_a_est':'Domicílios estimados sem conexão às modalidades de rede por rateio de área, nred_set × frac_area',
 'area_km2':'Área da bacia de trabalho fornecida',
 'n_setores':'Número de setores com interseção de área positiva',
 'n_rede_av':'Número de interseções com indicador de rede calculável e dom_set > 0',
 'n_dir_av':'Número de interseções com pct_rdir calculável',
 'n_sem_dom':'Número de interseções com zero domicílios permanentes ocupados',
 'n_parcial':'Número de interseções sem indicador de rede calculável, excluindo zero domicílios',
 'den_a_av':'Denominador estimado somente dos recortes em que pct_rede é calculável',
 'dir_a_est':'Domicílios estimados com destinação direta à rede geral/pluvial, somente nos recortes avaliáveis',
 'den_dir':'Denominador estimado somente dos recortes em que pct_rdir é calculável',
 'cov_dir':'100 × den_dir / dom_a_est; cobertura da modalidade direta sobre domicílios com total conhecido',
 'cov_dom':'100 × den_a_av / dom_a_est; cobertura sobre domicílios com total conhecido, não sobre totais protegidos',
 'cov_geo':'Percentual da área da bacia coberta pela malha censitária',
 'met_rateio':'Método de agregação: area_uniforme, estimativa exploratória; não dasimétrico',
}

# Sha
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()

# Polygon
def polygon(g):
    if g is None or g.is_empty:return g
    g=make_valid(g)
    if g.geom_type in ['Polygon','MultiPolygon']:return g
    return unary_union([v for v in g.geoms if v.geom_type in ['Polygon','MultiPolygon']])

# Filtered csv
def filtered_csv(path,columns,ids):
    rows=[];read=0
    for a in pd.read_csv(path,sep=';',dtype='string',usecols=columns,chunksize=20000,keep_default_na=False):
        read+=len(a);selected=a[a['setor'].isin(ids)]
        if len(selected):rows.append(selected)
    assert rows,f'Nenhum setor localizado em {path}'
    out=pd.concat(rows,ignore_index=True)
    assert not out['setor'].duplicated().any(),f'Código duplicado em {path}'
    print(path.name,read,'linhas nacionais;',len(out),'setores selecionados',flush=True)
    return out

# Styles
def styles(path,columns,title):

    colors=['#eef5f4','#c9e3dd','#98c8bf','#5b9e98','#246d70','#d0d2d3','#ffffff']
    rules=[]
    for i in range(5):
        expr=f'"pct_rdir" >= {i*20} AND "pct_rdir" <= {(i+1)*20}' if i==0 else f'"pct_rdir" > {i*20} AND "pct_rdir" <= {(i+1)*20}'
        rules.append(f'<rule symbol="{i}" filter="{escape(expr, {chr(34):"&quot;"})}" label="{i*20}–{(i+1)*20}%"/>')
    if 'dom_set' in columns:
        rules.append('<rule symbol="5" filter="&quot;pct_rdir&quot; IS NULL AND (&quot;dom_set&quot; IS NULL OR &quot;dom_set&quot; &gt; 0)" label="Indicador indisponível"/>')
        rules.append('<rule symbol="6" filter="&quot;dom_set&quot; = 0" label="Sem domicílios ocupados"/>')
    else:rules.append('<rule symbol="5" filter="&quot;pct_rdir&quot; IS NULL" label="Indicador indisponível"/>')
    symbols=[]
    for i,color in enumerate(colors):
        symbols.append(f'<symbol name="{i}" type="fill" alpha="1"><layer class="SimpleFill" enabled="1"><Option type="Map"><Option name="color" value="{color}"/><Option name="outline_color" value="65,77,81,255"/><Option name="outline_width" value="0.12"/><Option name="outline_width_unit" value="MM"/><Option name="style" value="solid"/><Option name="outline_style" value="solid"/><Option name="joinstyle" value="round"/></Option></layer></symbol>')
    aliases=''.join(f'<alias field="{c}" index="{i}" name="{escape(DESC.get(c,c),{chr(34):"&quot;"})}"/>' for i,c in enumerate(columns))
    display='setor_id' if 'setor_id' in columns else 'bas_nome'
    qml=f'<!DOCTYPE qgis PUBLIC "http://mrcc.com/qgis.dtd" "SYSTEM"><qgis version="3.40.0" styleCategories="AllStyleCategories"><layername>{escape(title)}</layername><renderer-v2 type="RuleRenderer" symbollevels="0"><rules>'+''.join(rules)+'</rules><symbols>'+''.join(symbols)+f'</symbols></renderer-v2><aliases>{aliases}</aliases><displayfield>{display}</displayfield></qgis>'
    path.with_suffix('.qml').write_text(qml,encoding='utf8')

# Shapefile
def shapefile(g,name,title):
    cols=[c for c in g.columns if c!='geometry']
    assert all(len(c)<=10 for c in cols),cols
    g=g.copy()
    for c in cols:
        if isinstance(g[c].dtype,pd.StringDtype):g[c]=g[c].astype(object).where(g[c].notna(),None)
    path=SHP/f'{name}.shp';g.to_file(path,driver='ESRI Shapefile',encoding='UTF-8',index=False)
    styles(path,cols,title)
    check=gpd.read_file(path)
    assert len(check)==len(g) and check.crs.to_epsg()==31983
    if 'setor_id' in cols:assert list(check['setor_id'])==list(g['setor_id'])
    for c in ['V00309','pct_nrede','dom_a_est']:
        if c in cols:
            assert np.array_equal(check[c].isna(),g[c].isna()),(name,c,'null altered')
            assert np.allclose(check[c].fillna(0),g[c].fillna(0),rtol=1e-9,atol=1e-7),(name,c,'values changed')
    return path

# Archive existing
def archive_existing():
    if OUT.exists() and any(OUT.iterdir()):
        dest=ROOT/'descontinuado'/dt.datetime.now().strftime('%Y%m%d_%H%M%S_saneamento_ibge')
        assert OUT.resolve().is_relative_to(ROOT) and dest.resolve().is_relative_to(ROOT)
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.move(str(OUT),str(dest))
        (dest/'manifesto_arquivamento.json').write_text(json.dumps(dict(original=str(OUT),archived=str(dest),reason='Resultados gerados substituídos; arquivos-base preservados'),ensure_ascii=False,indent=2),encoding='utf8')
    SHP.mkdir(parents=True,exist_ok=True)

# Main
def main():
    bas=gpd.read_file(BASIN).to_crs(CRS)[['id','reserv','geometry']].rename(columns={'id':'bas_id','reserv':'bas_nome'})
    assert len(bas)==3 and bas['bas_id'].is_unique
    bas.geometry=bas.geometry.map(polygon)
    overlap=float(sum(bas.geometry.iloc[i].intersection(bas.geometry.iloc[j]).area for i in range(3) for j in range(i)))
    assert overlap<=1.01,('Sobreposição de bacias superior a 1m²',overlap)
    union=bas.geometry.union_all();bb=bas.to_crs(4674).total_bounds
    geom=gpd.read_file(MESH,bbox=tuple(bb),columns=['CD_SETOR','CD_MUN','NM_MUN','SITUACAO','v0001','v0007']).to_crs(CRS)
    invalid=int((~geom.is_valid).sum());geom.geometry=geom.geometry.map(polygon)
    geom=geom[geom.intersects(union)].copy();geom=geom[geom.intersection(union).area>0.01].copy()
    geom=geom.rename(columns={'CD_SETOR':'setor_id','CD_MUN':'mun_cod','NM_MUN':'mun_nome','SITUACAO':'situacao','v0001':'pop_malha','v0007':'dpo_malha'})
    geom['setor_id']=geom['setor_id'].astype(str);ids=set(geom['setor_id'])
    p1=next(INPUT.glob('*caracteristicas_domicilio1*.csv'));p2=next(INPUT.glob('*caracteristicas_domicilio2*.csv'))
    a=filtered_csv(p1,['setor','V00001'],ids);b=filtered_csv(p2,['setor']+CODES,ids)
    raw=a.merge(b,on='setor',how='outer',validate='one_to_one',indicator=True).rename(columns={'setor':'setor_id'})
    all_joined=bool((raw['_merge']=='both').all())
    raw=raw.drop(columns='_merge');original=raw.copy()
    raw['n_sigilo']=raw[RAW].eq('X').sum(axis=1).astype('int32')
    raw['sig_vars']=raw.apply(lambda r:','.join(c for c in RAW if pd.notna(r[c]) and r[c]=='X'),axis=1)
    raw['n_ausente']=raw[RAW].apply(lambda s:pd.to_numeric(s,errors='coerce').isna() & s.ne('X')).sum(axis=1).astype('int32')
    for c in RAW:raw[c]=pd.to_numeric(raw[c],errors='coerce').astype('float64')
    raw['dom_set']=raw['V00001'];raw['rede_set']=raw[['V00309','V00310']].sum(axis=1,min_count=2)
    raw['nred_set']=raw['dom_set']-raw['rede_set']
    denominator=raw['dom_set'].where(raw['dom_set']>0)
    raw['pct_rede']=100*raw['rede_set']/denominator;raw['pct_nrede']=100*raw['nred_set']/denominator
    raw['pct_rdir']=100*raw['V00309']/denominator;raw['pct_fossa']=100*raw['V00311']/denominator
    raw['pct_vrio']=100*raw[['V00313','V00314']].sum(axis=1,min_count=2)/denominator
    raw['soma8']=raw[CODES].sum(axis=1,min_count=8);raw['dif_soma']=raw['soma8']-raw['dom_set']
    raw['qual_dado']='parcial';raw.loc[raw['pct_rede'].notna(),'qual_dado']='rede_disp'
    raw.loc[raw['dif_soma'].eq(0),'qual_dado']='completo';raw.loc[raw['dom_set'].eq(0),'qual_dado']='sem_dom'
    bad=(raw['dif_soma'].notna() & raw['dif_soma'].abs().gt(0)) | raw['rede_set'].gt(raw['dom_set']) | raw['nred_set'].lt(0)
    raw.loc[bad,'qual_dado']='revisar'
    assert not bad.any(),raw.loc[bad].to_json(orient='records')
    geo=geom.merge(raw,on='setor_id',how='left',validate='one_to_one')
    geo.loc[geo['qual_dado'].isna(),'qual_dado']='sem_agreg';geo['ano']=2022;geo['set_km2']=geo.area/1e6
    geo['tot_origem']=np.where(geo['V00001'].notna(),'tabela_p1','sem_valor')
    verified_zero=geo['qual_dado'].eq('sem_agreg') & geo['dpo_malha'].eq(0) & geo['pop_malha'].eq(0)
    geo.loc[verified_zero,['dom_set','rede_set','nred_set']]=0
    geo.loc[verified_zero,'qual_dado']='sem_dom';geo.loc[verified_zero,'tot_origem']='malha_DPO0'
    geo['n_sigilo']=geo['n_sigilo'].fillna(0).astype('int32');geo['n_ausente']=geo['n_ausente'].fillna(len(RAW)).astype('int32');geo['sig_vars']=geo['sig_vars'].fillna('')
    assert geo['setor_id'].is_unique
    clip=gpd.overlay(geo,bas,how='intersection',keep_geom_type=True)
    clip=clip[clip.area>0.01].copy();clip['rec_km2']=clip.area/1e6;clip['frac_area']=clip['rec_km2']/clip['set_km2']
    assert clip['frac_area'].between(0,1+1e-8).all()
    clip['frac_area']=clip['frac_area'].clip(upper=1)
    for out,source in [('dom_a_est','dom_set'),('red_a_est','rede_set'),('nrd_a_est','nred_set')]:clip[out]=clip[source]*clip['frac_area']
    clip['dir_a_est']=clip['V00309']*clip['frac_area']
    nbas=clip.groupby('setor_id')['bas_id'].nunique();geo['n_bacias']=geo['setor_id'].map(nbas).astype('int32')
    clip['n_bacias']=clip['setor_id'].map(nbas).astype('int32')
    summaries=[];gaps=[]
    for _,v in bas.iterrows():
        c=clip[clip['bas_id']==v['bas_id']];eligible=c['pct_rede'].notna();den=c.loc[eligible,'dom_a_est'].sum(min_count=1)
        dom=c['dom_a_est'].sum(min_count=1);red=c.loc[eligible,'red_a_est'].sum(min_count=1);nred=c.loc[eligible,'nrd_a_est'].sum(min_count=1)
        direct=c['pct_rdir'].notna();den_dir=c.loc[direct,'dom_a_est'].sum(min_count=1);dir_est=c.loc[direct,'dir_a_est'].sum(min_count=1)
        covered=c.geometry.union_all();gap=v.geometry.difference(covered)
        if gap.area>.01:gaps.append(dict(bas_id=v['bas_id'],gap_m2=gap.area,geometry=polygon(gap)))
        summaries.append(dict(bas_id=v['bas_id'],bas_nome=v['bas_nome'],ano=2022,area_km2=v.geometry.area/1e6,n_setores=len(c),n_rede_av=int(eligible.sum()),n_dir_av=int(direct.sum()),n_sem_dom=int(c['dom_set'].eq(0).sum()),n_parcial=int((~eligible & ~c['dom_set'].eq(0)).sum()),dom_a_est=dom,red_a_est=red,nrd_a_est=nred,den_a_av=den,pct_rede=100*red/den if den>0 else None,pct_nrede=100*nred/den if den>0 else None,cov_dom=100*den/dom if dom>0 else None,dir_a_est=dir_est,den_dir=den_dir,pct_rdir=100*dir_est/den_dir if den_dir>0 else None,cov_dir=100*den_dir/dom if dom>0 else None,cov_geo=100*(1-gap.area/v.geometry.area),met_rateio='area_uniforme',geometry=v.geometry))
    summary=gpd.GeoDataFrame(summaries,crs=CRS)

    fractions=clip.groupby('setor_id')['frac_area'].sum()
    assert fractions.le(1+1e-7).all(),fractions[fractions>1+1e-7]
    valid=clip[['red_a_est','nrd_a_est','dom_a_est']].notna().all(axis=1)
    assert np.allclose(clip.loc[valid,'red_a_est']+clip.loc[valid,'nrd_a_est'],clip.loc[valid,'dom_a_est'],atol=1e-7)
    archive_existing()
    outputs=[]
    outputs.append(shapefile(geo,'setores_saneamento_inteiros','Esgotamento 2022 — setores inteiros'))
    outputs.append(shapefile(clip,'setores_saneamento_bacias','Esgotamento 2022 — recorte nas bacias'))
    outputs.append(shapefile(summary,'resumo_saneamento_bacias','Esgotamento 2022 — resumo por bacia, rateio de área'))
    gpkg=OUT/'saneamento_teco.gpkg'
    for data,name in [(geo,'setores_inteiros'),(clip,'setores_recortados'),(summary,'resumo_bacias')]:data.to_file(gpkg,layer=name,driver='GPKG',index=False)
    if gaps:
        gap_gdf=gpd.GeoDataFrame(gaps,crs=CRS);gap_gdf.to_file(gpkg,layer='lacunas_malha',driver='GPKG',index=False)
    original.to_csv(OUT/'valores_originais_selecionados.csv',sep=';',index=False,encoding='utf-8-sig')
    clip.drop(columns='geometry').to_csv(OUT/'atributos_setores_bacias.csv',sep=';',index=False,encoding='utf-8-sig')
    summary.drop(columns='geometry').to_csv(OUT/'resumo_bacias.csv',sep=';',index=False,encoding='utf-8-sig')
    clip.groupby(['bas_id','mun_cod','mun_nome'],as_index=False).agg(rec_km2=('rec_km2','sum'),dom_a_est=('dom_a_est','sum'),n_setores=('setor_id','nunique')).to_csv(OUT/'municipios_interceptados.csv',sep=';',index=False,encoding='utf-8-sig')
    used=list(dict.fromkeys([c for a in [geo,clip,summary] for c in a.columns if c!='geometry']))
    assert all(c in DESC for c in used),[c for c in used if c not in DESC]
    pd.DataFrame([dict(campo=c,descricao=DESC[c]) for c in used]).to_csv(OUT/'dicionario_campos.csv',sep=';',index=False,encoding='utf-8-sig')
    sources=[p1,p2,INPUT/'dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx',MESH,BASIN]
    audit=dict(reference_year=2022,created_at=dt.datetime.now().isoformat(),crs=CRS,basin_file=str(BASIN),basin_overlap_m2=overlap,invalid_mesh_geometries_in_bbox=invalid,sector_count=len(geo),intersection_count=len(clip),joined_tables=all_joined,missing_aggregates=geo.loc[geo['qual_dado']=='sem_agreg','setor_id'].tolist(),absent_topic_records_verified_zero_households=geo.loc[verified_zero,'setor_id'].tolist(),municipalities=geo[['mun_cod','mun_nome']].drop_duplicates().to_dict(orient='records'),qualities=geo['qual_dado'].value_counts().to_dict(),direct_network_indicator_sectors=int(geo['pct_rdir'].notna().sum()),combined_network_indicator_sectors=int(geo['pct_rede'].notna().sum()),suppressed_raw_cells=int(geo['n_sigilo'].sum()),raw_symbols_kept=True,missing_numeric_values_are_null=True,all_complete_category_sums_match=True,allocation_method='Uniform areal weighting of complete sector statistics; exploratory, not a household inventory or dasymetric estimate',landcover_2025_used=False,mesh_gaps_m2={x['bas_id']:x['gap_m2'] for x in gaps},sources=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sources],summary=summary.drop(columns='geometry').replace({np.nan:None}).to_dict(orient='records'),shapefile_paths=[str(p) for p in outputs],checks=['Spatial overlaps <= 1 m2','No duplicated census sector identifier','Tables joined by identical 15-digit sector IDs','All fully available sanitation category sums equal household total','X retained in raw CSV and null in numeric GIS fields','Percentages within 0-100, or null','Areal fractions per sector <= 1','Estimated connected + not-connected households equals eligible denominator','Shapefile readback: feature counts, CRS, IDs, null masks and numeric values'])
    for field in ['pct_rede','pct_nrede','pct_rdir','pct_fossa','pct_vrio']:
        v=geo[field].dropna();assert v.between(-1e-8,100+1e-8).all(),field
    (OUT/'auditoria_saneamento.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
    write_readme(audit)
    preview(clip,bas,summary)
    with zipfile.ZipFile(OUT/'Shapefiles_saneamento_TECO.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in SHP.iterdir():z.write(p,'shapefiles/'+p.name)
        for name in ['LEIA_PRIMEIRO.md','dicionario_campos.csv','resumo_bacias.csv','auditoria_saneamento.json']:z.write(OUT/name,name)
    print(json.dumps(dict(sectors=len(geo),intersections=len(clip),quality=audit['qualities'],summary=audit['summary']),ensure_ascii=True),flush=True)

# Write readme
def write_readme(a):
    s=['# Saneamento censitário nas bacias TECO','',f"Referência: Censo 2022. Processamento: {a['created_at']}. Sistema: SIRGAS 2000 / UTM 23S, EPSG:31983.",'',
    '## Arquivos para abrir no QGIS','',
    '- shapefiles/setores_saneamento_bacias.shp: camada principal; setores recortados nas três bacias, com percentuais e categorias de esgotamento.',
    '- shapefiles/setores_saneamento_inteiros.shp: setores completos que interceptam as áreas de trabalho; mantém a unidade estatística original.',
    '- shapefiles/resumo_saneamento_bacias.shp: três bacias com totais estimados por rateio de área e cobertura do indicador.',
    '- saneamento_teco.gpkg: mesmas camadas, com suporte mais completo a campos nulos. Se houver lacunas geométricas, a camada lacunas_malha as identifica.',
    _cp_adaptar('- Saneamento_TECO.qgz: projeto adicional gerado pela conferência no QGIS, com a camada recortada visível e as duas camadas de apoio disponíveis. O projeto original E:/teco/projeto_teco.qgz permanece intacto.'),
    '- Os arquivos QML junto aos SHP trazem simbologia de pct_rdir (destinação direta à rede geral/pluvial) e nomes explicativos dos campos. A modalidade direta tem maior cobertura de divulgação; pct_rede e pct_nrede continuam disponíveis como indicadores compostos. Copie todos os arquivos de cada shapefile, não apenas o .shp.',
    '- Shapefiles_saneamento_TECO.zip contém os shapefiles completos e a documentação.',
    '', '## O que os campos representam','',
    'V00001 e V00309–V00316 são as contagens oficiais do SETOR INTEIRO. Essas contagens não se tornam contagens observadas da bacia quando a geometria é cortada. dom_set, rede_set e nred_set também se referem ao setor inteiro. NÃO somar esses campos no recorte: um setor pode participar de mais de uma bacia.',
    'rede_set = V00309 + V00310, somente se ambas forem divulgadas. nred_set = V00001 - rede_set. Esse complemento calcula a modalidade agregada sem alterar os X das categorias individuais. pct_rede e pct_nrede utilizam V00001 > 0. V00309 permanece separado em pct_rdir para não confundir destinação direta à rede com fossa ligada.',
    'Os percentuais são os do setor censitário e ficam constantes dentro de cada setor. Não descrevem a situação de cada endereço ou célula de mapa. dom_a_est, red_a_est e nrd_a_est são ESTIMATIVAS proporcionais à fração da área do setor dentro da bacia. Valores fracionários são esperados e não são arredondados antes da soma.',
    'No resumo por bacia, pct_rede e pct_nrede são razões das contagens estimadas, com o MESMO denominador elegível den_a_av. pct_rdir utiliza dir_a_est/den_dir, com denominador próprio para a modalidade direta. Não são médias simples dos percentuais dos setores. cov_dom e cov_dir mostram as respectivas coberturas sobre o total estimado dos setores com total conhecido. Totais X continuam fora desse denominador e não estão implicitamente tratados como zero.',
    '', '## Interpretação para o TECO','',
    'Rede geral ou pluvial é a categoria publicada pelo IBGE. Ela não comprova rede sanitária separadora, ligação contratual ativa, encaminhamento à ETE ou tratamento. Fossa séptica não ligada à rede não equivale automaticamente a destinação inadequada. Os campos são atributos de infraestrutura/destinação declarada, não medidas de carga de microrganismos, antibióticos ou resistência antimicrobiana.',
    'pct_nrede pode apoiar a comparação de infraestrutura sanitária no cenário inicial. A associação com pressão sobre o reservatório exige considerar o encaminhamento do esgoto, os lançamentos, a drenagem e o tratamento. Não foi criado índice de RAM, pesos, k-means ou Moran nesta etapa.',
    '', '## Limitações e verificações','',
    'X e outros símbolos não numéricos permanecem nulos nos campos numéricos do GIS. Os símbolos originais constam em valores_originais_selecionados.csv. n_sigilo, sig_vars, n_ausente e qual_dado permitem rastrear a disponibilidade. Zero domicílios produz percentual nulo, não 0% de atendimento. Nulos da legenda não devem ser interpretados como ausência de rede.',
    'Nos 19 setores sem registro temático, a malha oficial informa zero pessoas (v0001) e zero domicílios particulares ocupados (v0007). Apenas nesses casos, dom_set foi identificado como zero, com tot_origem=malha_DPO0 e qual_dado=sem_dom. Os campos RAW não foram preenchidos. Isso distingue ausência confirmada de domicílios de informação censitária protegida. A malha também intercepta parcelas de municípios além dos cinco iniciais; nenhuma parcela foi descartada apenas por município. municipios_interceptados.csv mostra as áreas e estimativas de cada interseção. Essas parcelas de borda devem ser verificadas com a delimitação hidrológica e os limites municipais de diferentes anos antes de interpretar sua contribuição.',
    'O rateio de área pressupõe distribuição uniforme de domicílios no setor e é apenas exploratório. Pode distorcer os totais em setores parcialmente recortados e de ocupação concentrada. Uma alocação dasimétrica com áreas residenciais e ano compatível deve substituí-lo quando houver base validada. O raster de uso do solo de 2025 foi consultado, mas não usado para localizar residências do Censo 2022.',
    'As bacias são exatamente as delimitadas no projeto, em sub_bacia/shapefiles_v6_20261109_141015/sub_bacias_exclusivas.shp. Não foram refeitas nem modificadas. O script de origem declara exutórios automáticos e delimitação preliminar; a regularização cartográfica não substitui validação hidrológica. Referenciar essa versão ao interpretar os totais.',
    f"Foram selecionados {a['sector_count']} setores únicos e {a['intersection_count']} interseções setor × bacia. As duas tabelas nacionais foram conciliadas pelo código do setor; os totais das oito categorias fecharam em todos os registros com informação completa. A auditoria registra disponibilidade, malha, fontes, hashes e cobertura geométrica.",
    '', '## Fontes e reprodução','',
    _cp_adaptar('Tabelas e dicionário: arquivos fornecidos em E:/teco/saneamento_ibge. Datas dos nomes são revisões/publicações; o ano de referência continua 2022.'),
    'Malha oficial IBGE: https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/malha_com_atributos/setores/gpkg/UF/MG/MG_setores_CD2022.gpkg',
    _cp_adaptar('Script: E:/teco/codigo/preparar_saneamento_ibge.py. Conferência e projeto QGIS adicional: E:/teco/codigo/conferir_e_abrir_saneamento_qgis.py, executado no Python do QGIS após o processamento. Execuções posteriores preservam saídas substituídas em E:/teco/descontinuado. Os insumos e o projeto QGIS original não são alterados.'),
    '', '## Resumo exploratório por bacia','',
    '| Bacia | Setores | Domicílios estimados por área* | Destinação direta à rede geral/pluvial (%) | Cobertura da modalidade direta sobre total conhecido (%) |','|---|---:|---:|---:|---:|']
    for x in a['summary']:s.append(f"| {x['bas_nome']} | {x['n_setores']} | {x['dom_a_est']:.1f} | {x['pct_rdir']:.2f} | {x['cov_dir']:.2f} |")
    s+=['','*Não são contagens observadas dos domicílios dentro da bacia. Consultar as limitações do rateio e os setores com informações protegidas.']
    (OUT/'LEIA_PRIMEIRO.md').write_text('\n'.join(s),encoding='utf8')

# Preview
def preview(clip,bas,summary):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap,BoundaryNorm
    from matplotlib.patches import Patch
    from matplotlib.ticker import FuncFormatter,MaxNLocator
    cmap=ListedColormap(['#eef5f4','#c9e3dd','#98c8bf','#5b9e98','#246d70']);norm=BoundaryNorm([0,20,40,60,80,100.00001],5)
    plt.rcParams.update({'font.family':'Arial','svg.fonttype':'path','pdf.fonttype':42})
    fig,axs=plt.subplots(1,3,figsize=(14,6.6));geo=clip.to_crs(4674);bg=bas.to_crs(4674)
    for ax,(_,b) in zip(axs,bg.iterrows()):
        g=geo[geo['bas_id']==b['bas_id']]
        occupied=g[~g['dom_set'].eq(0)]
        occupied.plot(ax=ax,column='pct_rdir',cmap=cmap,norm=norm,edgecolor='#536064',linewidth=.2,missing_kwds={'color':'#d0d2d3','edgecolor':'#899195','hatch':'///'})
        empty=g[g['dom_set'].eq(0)]
        if len(empty):empty.plot(ax=ax,color='white',edgecolor='#899195',linewidth=.2)
        bg[bg['bas_id']==b['bas_id']].boundary.plot(ax=ax,color='#143b4b',linewidth=1.1)
        x0,y0,x1,y1=b.geometry.bounds;pad=max(x1-x0,y1-y0)*.05
        ax.set_xlim(x0-pad,x1+pad);ax.set_ylim(y0-pad,y1+pad);ax.set_aspect(1/np.cos(np.deg2rad((y0+y1)/2)))
        ax.set_title({'vargem_flores':'Vargem das Flores','pampulha':'Lagoa da Pampulha','ibirite_regap':'Ibirité / REGAP'}[b['bas_id']],fontsize=12,pad=8,fontweight='bold')
        ax.xaxis.set_major_locator(MaxNLocator(3));ax.yaxis.set_major_locator(MaxNLocator(3));ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{abs(v):.2f}°O'));ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{abs(v):.2f}°S'));ax.tick_params(labelsize=8)
        ax.text(.94,.93,'N',transform=ax.transAxes,ha='center',fontsize=9,fontweight='bold');ax.annotate('',xy=(.94,.91),xytext=(.94,.82),xycoords='axes fraction',arrowprops={'arrowstyle':'-|>','color':'#173e4f'})
        ax.set_xlabel('');ax.set_ylabel('')
    handles=[Patch(facecolor=c,edgecolor='#536064',linewidth=.4,label=l) for c,l in zip(cmap.colors,['0–20%','>20–40%','>40–60%','>60–80%','>80–100%'])]+[Patch(facecolor='#d0d2d3',hatch='///',label='Indisponível'),Patch(facecolor='white',edgecolor='#899195',label='Sem domicílios ocupados')]
    fig.suptitle('Domicílios com destinação à rede geral ou pluvial (%)',fontsize=14,fontweight='bold',y=.97)
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.06),ncol=4,frameon=False,fontsize=9,columnspacing=2)
    fig.text(.5,.015,'Censo 2022 · Percentuais do setor inteiro, recortados nas bacias fornecidas · Não comprova tratamento do esgoto · SIRGAS 2000',ha='center',fontsize=8,color='#4b626b')
    fig.subplots_adjust(left=.06,right=.98,bottom=.22,top=.86,wspace=.28)
    fig.savefig(OUT/'Previa_saneamento_bacias.png',dpi=200,facecolor='white');plt.close(fig)

if __name__=='__main__':main()
