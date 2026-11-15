# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/00_fontes/sih_cnv_qimg100921200_198_31_2.csv | .read_text.
# Entrada: E:/teco/entrega_final/01_entradas/01_bacias/bacias.shp | gpd.read_file.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/00_fontes/CNES_MG.csv | .open.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/Selecionados_nas_bacias.csv | pd.read_csv.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/CNES_nas_bacias.csv | pd.read_csv.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/Internacoes_gerais_selecionados_mensal.csv | pd.read_csv.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/Internacoes_gerais_selecionados_anual.csv | pd.read_csv.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/02_camadas/01_cnes_bacias/cnes_2026.shp | gpd.read_file.
# Entrada: {src} | src.read_bytes.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/00_fontes/src.name | .read_bytes.
# Entrada: E:/teco/entrega_final/00_documentacao/Integridade_SHA256.csv | .open.
# Entrada: E:/teco/entrega_final/row['arquivo'] | p.read_bytes.
# Campos/chaves em r: Estabelecimento.
# Campos/chaves em row: CNES, STATUS DO ESTABELECIMENTO, arquivo, location, sha256.
# Campos/chaves em sel: CNES, INT_15_26.
# Campos/chaves em monthly: CNES.
# Campos/chaves em annual: CNES.
# Campos/chaves em g: SIH_HIST.
# Saída: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Validacao_independente_CNES_SIH.json | .write_text.
# CNES: identificador do estabelecimento de saúde.
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
import csv
import io
import re
import hashlib
import json
import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import Transformer
from shapely.geometry import Point

R=Path(_cp_texto('', 'posix'));F=R/'entrega_final';P=F/'01_entradas/17_estabelecimentos_2026';T=P/'01_tabelas';D=P/'04_documentacao'
raw=list(csv.reader(io.StringIO((P/'00_fontes/sih_cnv_qimg100921200_198_31_2.csv').read_text('latin1')),delimiter=';'))
header=next(row for row in raw if row and row[0]=='Estabelecimento')
records=[dict(zip(header,row)) for row in raw if row and re.match(r'^\d{7}\s',row[0])]
recent=[x for x in header if re.match(r'^202[456]/',x)]
positive={r['Estabelecimento'][:7] for r in records if sum(int(r[c]) for c in recent if r[c]!='-')>0}
bas=gpd.read_file(F/'01_entradas/01_bacias/bacias.shp').geometry.union_all();trans=Transformer.from_crs(4326,31983,always_xy=True)
expected=set();allinside=set()
with (P/'00_fontes/CNES_MG.csv').open(encoding='utf-8-sig',newline='') as stream:
    for row in csv.DictReader(stream):
        c=row['CNES'].zfill(7);lat,lon=map(float,row['location'].split(','));point=Point(*trans.transform(lon,lat))
        if bas.intersects(point):
            allinside.add(c)
            if c in positive and row['STATUS DO ESTABELECIMENTO']=='ATIVO':expected.add(c)
sel=pd.read_csv(T/'Selecionados_nas_bacias.csv',sep=';',dtype={'CNES':str})
assert set(sel.CNES)==expected and len(expected)==3
assert len(allinside)==742
assert set(pd.read_csv(T/'CNES_nas_bacias.csv',sep=';',dtype={'CNES':str}).CNES)==allinside

monthly=pd.read_csv(T/'Internacoes_gerais_selecionados_mensal.csv',sep=';',dtype={'CNES':str})
annual=pd.read_csv(T/'Internacoes_gerais_selecionados_anual.csv',sep=';',dtype={'CNES':str})
for row in sel.itertuples():
    assert monthly[monthly.CNES.eq(row.CNES)].INTERNACOES.sum()==row.INT_15_26
    assert annual[annual.CNES.eq(row.CNES)].INTERNACOES.sum()==row.INT_15_26
    assert len(monthly[monthly.CNES.eq(row.CNES)])==141
    assert set(annual[annual.CNES.eq(row.CNES)].ANO)==set(range(2015,2027))
g=gpd.read_file(P/'02_camadas/01_cnes_bacias/cnes_2026.shp')
assert g.loc[g.SIH_HIST.eq(0),['INT_FONTE','INT_15_26','INT_24_26']].isna().all().all()
assert g.geometry.intersects(bas).all()
for src in [Path(_cp_externo('cnes_mg_csv_510331d')),Path(_cp_externo('sih_cnv_qimg100921200_198_31_2_csv_7af2046'))]:
    assert hashlib.sha256(src.read_bytes()).hexdigest()==hashlib.sha256((P/'00_fontes'/src.name).read_bytes()).hexdigest()

checks=0
with (F/'00_documentacao/Integridade_SHA256.csv').open(encoding='utf-8-sig',newline='') as stream:
    for row in csv.DictReader(stream,delimiter=';'):
        p=F/row['arquivo']
        if p.suffix.lower() not in ['.shp','.shx','.dbf','.prj','.cpg','.tif','.png','.svg']:continue
        assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],p
        checks+=1
report={'status':'APROVADO','selecao_independente_por_CNES_e_coordenadas':sorted(expected),'cadastros_internos':len(allinside),'internacoes_gerais_2015_2026':int(sel.INT_15_26.sum()),'meses_por_estabelecimento':141,'fontes_copiadas_integralmente':True,'nulos_sem_SIH_preservados':True,'arquivos_geograficos_e_figuras_anteriores_conferidos':checks}
(D/'Validacao_independente_CNES_SIH.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=True),flush=True)
