# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {p} | p.read_bytes.
# Entrada: E:/teco/entrega_final/00_documentacao/{name} | path.read_text.
# Entrada: {path} | pd.read_csv.
# Entrada: E:/teco/output/05_auditoria_saude/saude_tabnet_auditada.gpkg | gpd.read_file | camada='producao_SIH_georreferenciada'.
# Entrada: E:/teco/teco_base/mg_mun/ide_1103_mg_municipios_pol.shp | gpd.read_file.
# Entrada: E:/teco/entrega_final/00_documentacao/manifesto.json | .read_text.
# Entrada: E:/teco/entrega_final/LEIA_PRIMEIRO.md | p.read_text.
# Entrada: E:/teco/codigo/integrar_cnes_sih_2026_qgis.py | .read_text.
# Entrada: E:/teco/entrega_final/00_documentacao/Field_dictionary_EN.csv | pd.read_csv.
# Entrada: E:/teco/entrega_final/TECO_Consolidado.qgz | zipfile.ZipFile.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Auditoria_CNES_SIH_2026.json | .read_text.
# Entrada: E:/teco/entrega_final/01_entradas/01_bacias/bacias.shp | gpd.read_file.
# Entrada: E:/teco/entrega_final/00_documentacao/manifesto.json | mp.read_text.
# Campos/chaves em data: CNES, Estabelecimento, FORA_PER, INT_15_26, INT_24_26, INT_FONTE, NOME_SIH, Total.
# Campos/chaves em c: CEP, CNES, COMPLEMENTO DO ENDEREÇO, LOGRADOURO, location.
# Campos/chaves em q: COMPLEMENTO DO ENDEREÇO.
# Campos/chaves em sih: CNES, INT_15_26, INT_2024, INT_2025, INT_2026, INT_24_26, INT_FONTE, MES_REC, NOME_SIH, RECENTE, ULT_ATEND.
# Campos/chaves em bacias: geometry, id.
# Campos/chaves em bacias.loc: id.
# Campos/chaves em municipalities: geocodigo, geometry, nome.
# Campos/chaves em audit: atendimentos_2015_2026, atendimentos_anteriores_2015, estabelecimentos, meses_em_colunas, total_oficial.
# Campos/chaves em m: mapas, rasters, vetores.
# Campos/chaves em en: dataset.
# Campos/chaves em en.loc: stored_field.
# Campos/chaves em r: arquivo, layer_id.
# Campos/chaves em raw: COMPETÊNCIA, STATUS DO ESTABELECIMENTO.
# Saída: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/{name} | frame.to_csv.
# Saída: bad.drop(columns=['geometry', 'index_right']) | save.
# Saída: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Relatorio_revisao_CNES_SIH.md | .write_text.
# Saída: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Relatorio_revisao_CNES_SIH.html | .write_text.
# Saída: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/LEIA_PRIMEIRO.md | .write_text.
# Saída: E:/teco/entrega_final/00_documentacao/Inventario_de_camadas.csv | .to_csv.
# Saída: E:/teco/entrega_final/LEIA_PRIMEIRO.md | p.write_text.
# Saída: E:/teco/entrega_final/00_documentacao/Field_dictionary_EN.csv | en.to_csv.
# Saída: E:/teco/entrega_final/00_documentacao/{name} | path.write_text.
# Saída: {x} | save.
# Saída: inside.groupby(['BACIA', 'TIPO_CNES'], as_index=False).size().rename(columns={'size': 'ESTABELECIMENTOS'}) | save.
# Saída: monthly[monthly.CNES.isin(selected.CNES) & monthly.NO_RECORTE].copy() | save.
# Saída: msel.groupby(['CNES', 'NOME_SIH', 'ANO'], as_index=False).INTERNACOES.sum(min_count=1) | save.
# Saída: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/03_consultas_individuais/r.CNES/Internacoes_gerais_mensal_2015_2026.csv | .to_csv.
# Saída: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/03_consultas_individuais/r.CNES/Internacoes_gerais_anual_2015_2026.csv | .to_csv.
# Saída: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/03_consultas_individuais/r.CNES/LEIA_PRIMEIRO.md | .write_text.
# Saída: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Auditoria_CNES_SIH_2026.json | .write_text.
# Saída: E:/teco/entrega_final/00_documentacao/manifesto.json | mp.write_text.
# Campos/chaves gerados em data: CNES, FORA_PER, INT_15_26, INT_24_26, INT_FONTE, MES_REC, NOME_SIH, RECENTE, ULT_ATEND.
# Campos/chaves gerados em monthly: ANO, ANO_MES, INTERNACOES, MES, NO_RECORTE.
# Campos/chaves gerados em c: CNES.
# Campos/chaves gerados em q: COORD_OK, ENDERECO, LAT, LON.
# Campos/chaves gerados em joined: DIST_BAC_M, MUN_GEO, QA_MUN_2026, SELEC_SIH, SIH_HIST.
# Campos/chaves gerados em near: BACIA.
# Campos/chaves gerados em statewide: CNES_EXPORT, MOTIVO.
# Campos/chaves gerados em pending: BACIA_REF, DIST_REF_M.
# Campos/chaves gerados em municipalities: nome.
# Campos/chaves gerados em value: camadas_validas, camadas_vetoriais_com_dicionario, layers.
# Campos/chaves gerados em record: layers.
# Campos/chaves gerados em audit: conferencia_municipal.
# Campos/chaves gerados em m: healthcare_2026_audit, vetores.
# CNES: identificador do estabelecimento de saúde.
# BACIA: identificador da bacia.
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
from datetime import datetime
import ast
import csv
import hashlib
import html
import io
import json
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import geopandas as gpd

R=Path(_cp_texto('', 'posix'))
F=R/'entrega_final'
P=F/'01_entradas/17_estabelecimentos_2026'
T=P/'01_tabelas'
D=P/'04_documentacao'
FONTES=[Path(_cp_externo('cnes_mg_csv_510331d')),Path(_cp_externo('sih_cnv_qimg100921200_198_31_2_csv_7af2046'))]
INICIO_RECENTE='2024-01'
FIM='2026-09'
MESES={'Jan':1,'Fev':2,'Mar':3,'Abr':4,'Mai':5,'Jun':6,'Jul':7,'Ago':8,'Set':9,'Out':10,'Nov':11,'Dez':12}
NOMES={'pampulha':'Pampulha','vargem_flores':'Vargem das Flores','ibirite_regap':'Ibirité / REGAP'}
COLS=['CNES','NOME_CNES','NOME_SIH','TIPO_CNES','MUN_COD','MUN_NOME','COMP_CNES','ATIVO_CAD','SUS_CAD','CEP','ENDERECO','LAT','LON','SIH_HIST','INT_FONTE','INT_15_26','INT_24_26','INT_2024','INT_2025','INT_2026','ULT_ATEND','MES_REC','SELEC_SIH','DIST_BAC_M','BACIA']

# Save
def save(frame,name):
    frame.to_csv(T/name,index=False,sep=';',encoding='utf-8-sig')

# Sha
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

# Ler sih
def ler_sih(path):
    rows=list(csv.reader(io.StringIO(path.read_text('latin1')),delimiter=';'))
    start=next(i for i,row in enumerate(rows) if row and row[0]=='Estabelecimento')
    header=rows[start]
    data=pd.DataFrame([r for r in rows[start+1:] if r and re.match(r'^\d{7}\s',r[0])],columns=header)
    data['CNES']=data.Estabelecimento.str[:7]
    data['NOME_SIH']=data.Estabelecimento.str[8:]
    assert data.CNES.is_unique
    monthcols=[x for x in header if re.fullmatch(r'\d{4}/[A-Za-zç]{3}',x)]
    dates={x:f'{x[:4]}-{MESES[x[5:]]:02d}' for x in monthcols}
    values=data[monthcols].replace('-',np.nan).apply(pd.to_numeric)
    inperiod=[c for c in monthcols if '2015-01'<=dates[c]<=FIM]
    recent=[c for c in monthcols if INICIO_RECENTE<=dates[c]<=FIM]
    data['INT_FONTE']=values.sum(axis=1).astype(int)
    data['INT_15_26']=values[inperiod].sum(axis=1).astype(int)
    data['INT_24_26']=values[recent].sum(axis=1).astype(int)
    data['FORA_PER']=data.INT_FONTE-data.INT_15_26
    for year in range(2015,2027):data[f'INT_{year}']=values[[c for c in monthcols if c.startswith(str(year))]].sum(axis=1).astype(int)
    data['ULT_ATEND']=[max((dates[c] for c in monthcols if pd.notna(values.loc[i,c]) and values.loc[i,c]>0),default='') for i in values.index]
    data['MES_REC']=values[recent].gt(0).sum(axis=1).astype(int)
    data['RECENTE']=data.INT_24_26.gt(0)
    rowtotal=pd.to_numeric(data.Total)
    assert np.array_equal(data.INT_FONTE,rowtotal)
    official=next(r for r in rows if r and r[0]=='Total')
    for c in monthcols:
        value=official[header.index(c)]
        assert int(values[c].sum())==(0 if value=='-' else int(value)),c
    assert int(data.INT_FONTE.sum())==int(official[-1])
    monthly=data[['CNES','NOME_SIH',*monthcols]].melt(id_vars=['CNES','NOME_SIH'],var_name='COLUNA_FONTE',value_name='VALOR_FONTE')
    monthly['ANO_MES']=monthly.COLUNA_FONTE.map(dates)
    monthly['ANO']=monthly.ANO_MES.str[:4].astype(int)
    monthly['MES']=monthly.ANO_MES.str[-2:].astype(int)
    monthly['INTERNACOES']=pd.to_numeric(monthly.VALOR_FONTE.replace('-',pd.NA)).astype('Int64')
    monthly['NO_RECORTE']=monthly.ANO_MES.between('2015-01',FIM)
    audit={'titulo':rows[0][0].strip(),'conteudo':rows[1][0],'periodos_processamento_informados':rows[2][0],'eixo_colunas':'Ano/mês atendimento, conforme cabeçalho original','meses_em_colunas':len(monthcols),'primeiro_atendimento':min(dates.values()),'ultimo_atendimento':max(dates.values()),'estabelecimentos':len(data),'total_oficial':int(official[-1]),'atendimentos_2015_2026':int(data.INT_15_26.sum()),'atendimentos_anteriores_2015':int(data.FORA_PER.sum()),'reconciliacao_linhas_colunas_total':'OK','simbolo_traco':'Símbolo original preservado; valor numérico nulo na série longa. A soma usa as contagens publicadas, sem atribuir zero clínico às ausências.'}
    return data,monthly,audit

# Ler cnes
def ler_cnes(path):
    c=pd.read_csv(path,dtype='string',keep_default_na=False)
    c['CNES']=c.CNES.str.zfill(7)
    assert c.CNES.is_unique and c.CNES.str.fullmatch(r'\d{7}').all()
    xy=c.location.str.split(',',n=1,expand=True)
    lat=pd.to_numeric(xy[0],errors='coerce');lon=pd.to_numeric(xy[1],errors='coerce')
    valid=lat.between(-24,-13)&lon.between(-52,-38)
    mapping={'NOME FANTASIA':'NOME_CNES','TIPO DO ESTABELECIMENTO':'TIPO_CNES','CÓDIGO DO MUNICÍPIO':'MUN_COD','MUNICÍPIO':'MUN_NOME','COMPETÊNCIA':'COMP_CNES','STATUS DO ESTABELECIMENTO':'ATIVO_CAD','CONVÊNIO SUS':'SUS_CAD'}
    q=c[['CNES','CEP','LOGRADOURO','COMPLEMENTO DO ENDEREÇO',*mapping]].rename(columns=mapping).copy()
    q['ENDERECO']=q.LOGRADOURO+q['COMPLEMENTO DO ENDEREÇO'].map(lambda x:(' · '+x) if x not in ['N/A','-',''] else '')
    q=q.drop(columns=['LOGRADOURO','COMPLEMENTO DO ENDEREÇO'])
    q['LAT']=lat;q['LON']=lon;q['COORD_OK']=valid
    points=gpd.GeoDataFrame(q,geometry=gpd.points_from_xy(lon,lat),crs=4326).to_crs(31983)
    points.loc[~valid,'geometry']=None
    return c,points

# Cruzar
def cruzar(cnes,sih,bacias):
    joined=cnes.merge(sih[['CNES','NOME_SIH','INT_FONTE','INT_15_26','INT_24_26','INT_2024','INT_2025','INT_2026','ULT_ATEND','MES_REC','RECENTE']],on='CNES',how='left',validate='one_to_one')
    joined['SIH_HIST']=joined.INT_FONTE.notna().astype(int)
    joined['SELEC_SIH']=(joined.INT_24_26.gt(0)&joined.ATIVO_CAD.eq('ATIVO')).astype(int)
    joined['DIST_BAC_M']=joined.geometry.distance(bacias.geometry.union_all())
    inside=gpd.sjoin(joined,bacias[['id','geometry']].rename(columns={'id':'BACIA'}),predicate='intersects',how='inner').drop(columns='index_right')
    assert not inside.duplicated(['CNES','BACIA']).any()
    selected=inside[inside.SELEC_SIH.eq(1)].sort_values(['BACIA','CNES']).copy()
    near=joined[joined.SELEC_SIH.eq(1)&joined.DIST_BAC_M.gt(0)&joined.DIST_BAC_M.le(1500)].copy()
    near['BACIA']=[bacias.loc[bacias.distance(g).idxmin(),'id'] for g in near.geometry]
    near=near.sort_values('DIST_BAC_M')
    statewide=sih.merge(cnes.drop(columns='geometry'),on='CNES',how='left',validate='one_to_one',indicator=True)
    statewide['CNES_EXPORT']=statewide._merge.eq('both')
    statewide['MOTIVO']=['Selecionado em MG: produção recente e cadastro ativo' if r.RECENTE and r.CNES_EXPORT and r.ATIVO_CAD=='ATIVO' else 'Sem produção SIH positiva em 2024-2026' if not r.RECENTE else 'Produção recente sem correspondência na exportação CNES ativa' for r in statewide.itertuples()]
    statewide=statewide.drop(columns='_merge')
    pending=statewide[~statewide.CNES_EXPORT].copy()
    oldpath=R/'output/05_auditoria_saude/saude_tabnet_auditada.gpkg'
    old=gpd.read_file(oldpath,layer='producao_SIH_georreferenciada').set_index('CNES')
    pending['DIST_REF_M']=pending.CNES.map(old.DIST_BACIA_M)
    pending['BACIA_REF']=pending.CNES.map(old.BACIA)
    return inside,selected,near,statewide,pending

# Conferir municipios
def conferir_municipios(statewide):
    sub=statewide[statewide.CNES_EXPORT&statewide.RECENTE].copy()
    points=gpd.GeoDataFrame(sub,geometry=gpd.points_from_xy(sub.LON,sub.LAT),crs=4326)
    municipalities=gpd.read_file(R/'teco_base/mg_mun/ide_1103_mg_municipios_pol.shp').to_crs(4326)
    def nome_municipal(value):
        if not isinstance(value,str) or not any(x in value for x in ['Ã','Â']):return value
        try:return value.encode('latin1').decode('utf8')
        except UnicodeError:return value
    municipalities['nome']=municipalities.nome.map(nome_municipal)
    joined=gpd.sjoin(points,municipalities[['geocodigo','nome','geometry']],how='left',predicate='intersects')
    joined['MUN_GEO']=joined.geocodigo.astype('string').str[:6]
    joined['QA_MUN_2026']=joined.MUN_GEO.eq(joined.MUN_COD)
    bad=joined[~joined.QA_MUN_2026.fillna(False)]
    save(bad.drop(columns=['geometry','index_right']),'Conferencia_coordenadas_municipio.csv')
    return {'estabelecimentos_recentes_conferidos':len(joined),'divergencias_municipais':len(bad),'CNES_divergentes':bad.CNES.tolist(),'divergentes_nos_oito_municipios':int(bad.MUN_COD.isin(['310620','310670','310900','311860','312410','312980','315460','316553']).sum())}

# Camadas
def camadas(frames):
    import consolidar_entrega_final as exp
    exp.F=F;exp.VECTORS=[];exp.FIELDS=[]
    titles={'01_cnes_bacias':('cnes_2026','All CNES facilities inside the basins · Sep 2026'),'02_selecao_sih':('sih_atual','Facilities with recent SIH production inside the basins'),'03_bordas':('sih_bordas','Recent SIH facilities outside but within 1.5 km of a basin')}
    for folder,g in frames.items():
        name,title=titles[folder]
        exp.shapefile(g[COLS+['geometry']].reset_index(drop=True),f'01_entradas/17_estabelecimentos_2026/02_camadas/{folder}/{name}.shp','healthcare_audit',title,'CNES_MG.csv (2026/09) + sih_cnv_qimg100921200_198_31_2.csv (processamento Jan/2015-Set/2026; colunas por atendimento)')
    return exp.VECTORS

# Relatorio
def relatorio(audit,raw,inside,selected,near,statewide,pending,summary,archive):
    rows=[]
    for r in selected.itertuples():
        rows.append(f'| {r.CNES} | {r.NOME_CNES} | {NOMES[r.BACIA]} | {int(r.INT_15_26):,} | {int(r.INT_2024):,} | {int(r.INT_2025):,} | {int(r.INT_2026):,} |'.replace(',','.'))
    basinrows=['| '+NOMES[r.BACIA]+' | '+str(r.CNES_TOTAL)+' | '+str(r.SIH_RECENTE)+' |' for r in summary.itertuples()]
    text='''# Revisão dos estabelecimentos e da produção hospitalar em Minas Gerais

## O que esta conferência resolveu

O novo arquivo do ElastiCNES foi cruzado integralmente com a exportação estadual do SIH/SUS pelo código CNES de sete dígitos. A seleção geográfica usa a posição do estabelecimento, por local de internação, e não o município de residência do paciente. Nenhum filtro por diagnóstico foi aplicado à nova produção geral.

O cadastro contém {n_cnes} estabelecimentos distintos, todos com status ATIVO na competência 2026/09. Dentro das três bacias foram encontrados {n_inside} estabelecimentos CNES. Destes, {n_selected} possuem internações na consulta estadual enviada e produção positiva no período recente. Assim, três hospitais não representam todos os serviços de saúde das bacias; representam os estabelecimentos identificados com produção de internações nesta consulta SUS. Consultórios, unidades ambulatoriais e serviços sem internações nesta base continuam no cadastro de contexto.

| Bacia | Todos os estabelecimentos CNES | Selecionados com produção recente SIH |
|---|---:|---:|
{basins}

## Estabelecimentos selecionados

| CNES | Estabelecimento | Bacia | Atendimento 2015-2026 | 2024 | 2025 | 2026 até setembro |
|---|---|---|---:|---:|---:|---:|
{units}

Os valores são internações registradas, não pacientes únicos. Os totais de 2026 são parciais e os últimos seis meses são sujeitos a atualização, conforme a nota da exportação. A presença de internações não demonstra infecção bacteriana, resistência antimicrobiana nem lançamento de efluente contaminado.

O Centro Materno Infantil e o Hospital Municipal de Contagem têm códigos CNES distintos, mas compartilham o endereço cadastral na Avenida João César de Oliveira, 4495. Seus pontos estão muito próximos e se sobrepõem na escala geral do mapa. A contagem considera os dois registros; a nova prancha os identifica separadamente por chamadas numeradas.

Dentro da bacia da Pampulha também consta o Núcleo Oftalmológico, CNES 5924820, classificado como hospital/dia e com convênio SUS no cadastro, mas sem linha de internações na tabela SIH recebida. Ele permanece na lista dos estabelecimentos cadastrados, sem ser declarado desativado. Serviços ambulatoriais e a presença de convênio SUS não asseguram registros de internação nessa consulta.

## Regra de atividade recente e exclusões

Foi adotada produção SIH positiva entre janeiro de 2024 e setembro de 2026, abrangendo os dois últimos anos completos e os nove meses disponíveis de 2026. O critério exclui da seleção operacional as instituições sem registros positivos nesse intervalo, conservando suas séries históricas e o motivo da exclusão. A regra exige também correspondência com cadastro ATIVO na exportação recebida.

A falta de produção nesta consulta não foi transformada em desativação cadastral confirmada. O status do CNES é um dado distinto. A exportação recebida já contém somente registros ATIVO, portanto não permite obter uma lista completa dos estabelecimentos desativados. No conjunto SIH de {n_sih} instituições, {n_recent} têm produção recente e {n_matched_recent} também constam no arquivo CNES ativo. Há {n_pending} códigos SIH sem correspondência nessa exportação, dos quais {n_pending_recent} ainda possuem registro recente. Eles permanecem identificados na tabela de pendências. O único recente sem correspondência, CNES 2146401, possui localização histórica de referência a aproximadamente 315 km das bacias; não foi atribuído às bacias nem declarado desativado.

## Conferência das bordas

A interseção foi realizada entre os pontos location fornecidos pelo CNES e os polígonos das bacias em EPSG:31983. O teste inclui pontos exatamente sobre o limite. Como o arquivo CNES contém pontos, não permite afirmar se a área física de um hospital cujo ponto está fora cruza a bacia. Uma lista auxiliar conserva os hospitais com produção recente localizados até 1,5 km do limite, sem incorporá-los aos totais internos.

{nearby}

O Hospital Alberto Cavalcanti, CNES 0026964, é o caso mais próximo, a cerca de 209 m do limite da Pampulha. Para incluí-lo como instalação que intercepta a bacia, é necessário conferir a localização e o polígono físico da unidade. Um círculo arbitrário ao redor do ponto não foi usado para aumentar a lista de hospitais internos.

Também se comparou o município informado no CNES com o município que contém suas coordenadas. Entre as 502 instituições recentes com correspondência na exportação ativa, 11 apresentam divergência ou ponto fora da malha municipal de Minas Gerais. Nenhuma dessas divergências pertence aos oito municípios interceptados pelas bacias. Os três hospitais selecionados têm localização municipal compatível. A tabela de divergências foi preservada para conferência, sem deslocar pontos automaticamente.

## Período de processamento e período de atendimento

O cabeçalho informa processamento selecionado de Jan/2015 a Set/2026, mas as colunas são Ano/mês atendimento. Por isso a tabela contém {n_months} colunas mensais, inclusive competências de atendimento de 2014. A fonte estadual totaliza {total_source} internações. As linhas de cada hospital, cada coluna mensal e o total estadual foram reconciliados sem diferença. O recorte de atendimento de janeiro de 2015 a setembro de 2026 soma {total_window}; os {before_2015} registros de atendimento anteriores a 2015 foram preservados e separados, sem serem somados aos totais desse recorte.

A série longa conserva o símbolo original “-” e deixa sua medida numérica ausente. As agregações somam somente contagens publicadas. Para um CNES ausente de toda a tabela SIH, as internações permanecem nulas no cadastro de contexto; não foram preenchidas com zero. Esta consulta geral por atendimento não deve ser comparada como se fosse idêntica às tabelas anteriores por processamento ou por residência.

## Onde adicionar as próximas consultas

Utilize a pasta `{individual}`. Foi criada uma subpasta para cada código CNES selecionado, contendo a série geral já extraída. As próximas exportações por causa, ano e mês devem ser salvas na subpasta do respectivo CNES, mantendo o nome original do arquivo. Para diagnósticos, conserve local de internação, o mesmo período de processamento disponível e Ano/mês atendimento nas colunas; exporte os códigos CID-10 com a descrição para que o filtro bacteriano possa ser conferido. Não some subtotais de capítulos CID aos diagnósticos detalhados.

As novas internações gerais documentam a atividade das unidades. O índice espacial vigente continua usando o filtro A+B de 2016-2025, até a integração das consultas específicas e a decisão sobre o período final. O número bruto de internações gerais não substituiu silenciosamente o indicador bacteriano.

## Delimitação das bacias e alcance do recorte

A delimitação das áreas contribuintes dos reservatórios de Vargem das Flores, Lagoa da Pampulha e Ibirité foi realizada em ambiente SIG a partir do Modelo Digital de Elevação Copernicus GLO-30, com resolução de 30 m. O MDE foi reprojetado para SIRGAS 2000 / UTM 23S (EPSG:31983). A direção e a acumulação do fluxo foram obtidas no GRASS GIS, integrado ao QGIS, pelo algoritmo r.watershed com a opção de fluxo único D8 (-s). Os candidatos a exutório foram identificados pela acumulação de fluxo associada aos limites dos reservatórios, e as áreas contribuintes foram delimitadas por r.water.outlet. Em seguida, integraram-se as áreas de drenagem diretamente associadas aos espelhos d’água, retiraram-se sobreposições entre as bacias e suavizaram-se os contornos para representação cartográfica. O código utilizado registra duas iterações e offset de 0,25 na suavização.

A referência cartográfica do exutório de Vargem das Flores foi conferida posteriormente, conforme o relatório anterior, sem refazer a bacia integrada usada nesta seleção. Os polígonos das três bacias não foram alterados nesta revisão. Essa descrição informa o procedimento efetivo e não demonstra, por si só, que toda unidade situada em municípios vizinhos drena para esses reservatórios.

## Arquivos e reprodutibilidade

As duas exportações originais estão em `00_fontes`, com cópias byte a byte dos arquivos enviados. As tabelas estaduais, as listas internas, as pendências e as séries gerais ficam em `01_tabelas`. Cada pasta de `02_camadas` contém um shapefile e seu dicionário. Os códigos de processamento e suas referências ficam em `05_scripts` da entrega. As versões geradas substituídas foram arquivadas em `{archive}`.

Fontes consultadas: [ElastiCNES](https://elasticnes.saude.gov.br/mapa), [notas técnicas de Procedimentos Hospitalares por local de internação](https://tabnet.datasus.gov.br/cgi/sih/Proced_hosp_loc_int_2008.pdf), [Portal CNES e status cadastral](https://wiki.saude.gov.br/cnes/index.php/Portal_CNES). As coordenadas usadas nesta revisão são as da exportação recebida, competência 2026/09; a competência exibida pelo site na consulta pode diferir da do arquivo exportado.
'''.format(n_cnes=len(raw),n_inside=len(inside),n_selected=len(selected),basins='\n'.join(basinrows),units='\n'.join(rows),n_sih=audit['estabelecimentos'],n_recent=int(statewide.RECENTE.sum()),n_matched_recent=int((statewide.RECENTE&statewide.CNES_EXPORT).sum()),n_pending=len(pending),n_pending_recent=int(pending.RECENTE.sum()),nearby='\n'.join(f'- {r.CNES}, {r.NOME_CNES}: {r.DIST_BAC_M:,.0f} m do limite mais próximo ({NOMES[r.BACIA]}).' for r in near.itertuples()),n_months=audit['meses_em_colunas'],total_source=f"{audit['total_oficial']:,}".replace(',','.'),total_window=f"{audit['atendimentos_2015_2026']:,}".replace(',','.'),before_2015=f"{audit['atendimentos_anteriores_2015']:,}".replace(',','.'),individual=str(P/'03_consultas_individuais'),archive=str(archive))
    (D/'Relatorio_revisao_CNES_SIH.md').write_text(text,encoding='utf8')
    def inline(s):
        s=html.escape(s)
        s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
        return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<a href="\2">\1</a>',s)
    content=[];table=False
    for line in text.splitlines():
        if line.startswith('|'):
            if re.fullmatch(r'[| :\-]+',line):continue
            cells=[inline(x.strip()) for x in line.strip('|').split('|')]
            if not table:content.append('<table><tr>'+''.join('<th>'+x+'</th>' for x in cells)+'</tr>');table=True
            else:content.append('<tr>'+''.join('<td>'+x+'</td>' for x in cells)+'</tr>')
            continue
        if table:content.append('</table>');table=False
        if line.startswith('#'):
            level=len(line)-len(line.lstrip('#'));content.append(f'<h{level}>'+inline(line.lstrip('# '))+f'</h{level}>')
        elif line.strip():content.append('<p>'+inline(line)+'</p>')
    if table:content.append('</table>')
    page='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Revisão CNES e SIH</title><style>body{max-width:1150px;margin:32px auto;padding:0 24px;font:16px/1.65 Arial;color:#203d49}h1,h2{color:#21596b;line-height:1.3}h2{margin-top:2em}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:10px;text-align:left;border-bottom:1px solid #d3dfe3}th{background:#e9f1f4}code{overflow-wrap:anywhere}a{color:#166d8d}img{max-width:100%}</style>'+''.join(content)+'</html>'
    (D/'Relatorio_revisao_CNES_SIH.html').write_text(page,encoding='utf8')
    (P/'LEIA_PRIMEIRO.md').write_text('# Cadastro e produção hospitalar revisados\n\nLeia `04_documentacao/Relatorio_revisao_CNES_SIH.html`. A lista principal é `01_tabelas/Selecionados_nas_bacias.csv`.\n\nAdicione as próximas exportações em `03_consultas_individuais`, na subpasta do código CNES. A série geral de cada unidade já foi extraída da tabela estadual recebida. Os dados por diagnóstico ainda dependem das novas exportações.\n\nOs 742 registros CNES internos descrevem todos os tipos de estabelecimento cadastrados; a seleção SIH interna contém três hospitais. A lista de bordas é uma conferência separada, não uma ampliação das bacias.\n',encoding='utf8')

# Documentar revisao
def documentar_revisao():
    doc=F/'00_documentacao';m=json.loads((doc/'manifesto.json').read_text('utf8'))
    pd.DataFrame([{k:v for k,v in r.items() if k not in ['campos','observacoes']} for r in m['vetores']]+m['rasters']).to_csv(doc/'Inventario_de_camadas.csv',sep=';',index=False,encoding='utf-8-sig')
    p=F/'LEIA_PRIMEIRO.md';s=p.read_text('utf8')
    s=re.sub(r'- `03_mapas`:[^\n]+',f"- `03_mapas`: {len(m['mapas'])} pares PNG/SVG, incluindo as pranchas anteriores e a revisão CNES/SIH de 2026.",s)
    if '## Revisão CNES/SIH de 2026' not in s:
        s+='\n\n## Revisão CNES/SIH de 2026\n\nAs exportações fornecidas estão em `01_entradas/17_estabelecimentos_2026/00_fontes`. O cruzamento estadual, as séries gerais e os 742 cadastros internos estão em `01_tabelas` desse conjunto. A lista de seleção por internações recentes contém três códigos CNES. Ausência de produção SIH não foi registrada como desativação cadastral confirmada.\n\nSalve as novas consultas por diagnóstico em `01_entradas/17_estabelecimentos_2026/03_consultas_individuais`, na subpasta do código CNES. O relatório complementar está em `04_documentacao/Relatorio_revisao_CNES_SIH.html` do mesmo conjunto. No QGIS, as três novas camadas ficam em `All basins > Observed inputs`; ative-as conforme a consulta desejada. Os resultados A+B de 2016-2025 continuam como referência até integrar as novas consultas por diagnóstico.\n'
    p.write_text(s,encoding='utf8')
    source=ast.parse((R/'codigo/integrar_cnes_sih_2026_qgis.py').read_text('utf8'))
    aliases=next(ast.literal_eval(n.value) for n in source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='aliases' for t in n.targets))
    enpath=doc/'Field_dictionary_EN.csv';en=pd.read_csv(enpath,sep=';',dtype=str,keep_default_na=False)
    mask=en.dataset.str.contains('17_estabelecimentos_2026')
    en.loc[mask,'English_display_alias']=en.loc[mask,'stored_field'].map(aliases).fillna(en.loc[mask,'stored_field'])
    en.to_csv(enpath,sep=';',index=False,encoding='utf-8-sig')
    qgz=F/'TECO_Consolidado.qgz'
    with zipfile.ZipFile(qgz) as z:project=ET.fromstring(z.read(next(n for n in z.namelist() if n.endswith('.qgs'))))
    layernodes=project.findall('./projectlayers/maplayer');count=len(layernodes)
    archive=Path(json.loads((D/'Auditoria_CNES_SIH_2026.json').read_text('utf8'))['archive'])
    for name in ['Conferencia_QGIS_final.json','English_QGIS_display.json','Revisao_QGIS_camadas.json','Validacao_metadados_QGIS.json']:
        path=doc/name
        if not path.exists():continue
        old=archive/'entrega_final/00_documentacao'/name;old.parent.mkdir(parents=True,exist_ok=True)
        if not old.exists():shutil.copy2(path,old)
        value=json.loads(path.read_text('utf8'))
        if name=='Conferencia_QGIS_final.json':value['layers']=count
        elif name=='English_QGIS_display.json':
            for record in value:record['layers']=count
        elif name=='Revisao_QGIS_camadas.json':
            value['layers']=count;catalog=value.get('new_layer_catalog',[]);known={r['layer_id'] for r in catalog}
            for node in layernodes:
                if node.findtext('id') not in known:catalog.append({'name':node.findtext('layername'),'basin':'all','group':'Observed inputs','source':node.findtext('datasource').removeprefix('./'),'layer_id':node.findtext('id')})
        else:
            value['camadas_validas']=count;value['camadas_vetoriais_com_dicionario']=sum('DICIONÁRIO DOS CAMPOS' in (n.findtext('./resourceMetadata/abstract') or '') for n in layernodes)
        path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')

# Main
def main():
    archive=R/'descontinuado'/datetime.now().strftime('%Y%m%d_%H%M%S_revisao_CNES_SIH')
    archive.mkdir(parents=True,exist_ok=False)
    for rel in ['00_documentacao/manifesto.json','00_documentacao/Dicionario_dos_campos.csv','00_documentacao/Field_dictionary_EN.csv','00_documentacao/Inventario_de_camadas.csv','index.html','LEIA_PRIMEIRO.md','TECO_Consolidado.qgz']:
        src=F/rel;dst=archive/'entrega_final'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
    for p in [P/'00_fontes',T,D,P/'03_consultas_individuais']:p.mkdir(parents=True,exist_ok=True)
    provenance=[]
    for p in FONTES:
        dst=P/'00_fontes'/p.name;shutil.copy2(p,dst);assert sha(p)==sha(dst);provenance.append({'arquivo':str(dst.relative_to(F)),'origem_local':str(p),'sha256':sha(dst),'bytes':dst.stat().st_size})
    raw,cnes=ler_cnes(FONTES[0]);sih,monthly,audit=ler_sih(FONTES[1]);bacias=gpd.read_file(F/'01_entradas/01_bacias/bacias.shp')
    basin_hash=sha(F/'01_entradas/01_bacias/bacias.shp')
    inside,selected,near,statewide,pending=cruzar(cnes,sih,bacias)
    summary=pd.DataFrame([{'BACIA':r.id,'NOME':NOMES[r.id],'CNES_TOTAL':int(inside.BACIA.eq(r.id).sum()),'SIH_HIST':int((inside.BACIA.eq(r.id)&inside.SIH_HIST.eq(1)).sum()),'SIH_RECENTE':int(selected.BACIA.eq(r.id).sum())} for r in bacias.itertuples()])
    for x,name in [(statewide,'Cruzamento_SIH_CNES_MG.csv'),(inside[COLS],'CNES_nas_bacias.csv'),(selected[COLS],'Selecionados_nas_bacias.csv'),(near[COLS],'Conferencia_bordas_1500m.csv'),(pending,'SIH_sem_correspondencia_CNES_ativo.csv'),(summary,'Resumo_por_bacia.csv'),(monthly,'SIH_MG_mensal_todas_colunas_fonte.csv')]:save(x,name)
    save(inside.groupby(['BACIA','TIPO_CNES'],as_index=False).size().rename(columns={'size':'ESTABELECIMENTOS'}),'Tipos_CNES_nas_bacias.csv')
    audit['conferencia_municipal']=conferir_municipios(statewide)
    msel=monthly[monthly.CNES.isin(selected.CNES)&monthly.NO_RECORTE].copy();save(msel,'Internacoes_gerais_selecionados_mensal.csv')
    annual=msel.groupby(['CNES','NOME_SIH','ANO'],as_index=False).INTERNACOES.sum(min_count=1);save(annual,'Internacoes_gerais_selecionados_anual.csv')
    for r in selected.itertuples():
        folder=P/'03_consultas_individuais'/r.CNES;folder.mkdir(exist_ok=True)
        msel[msel.CNES.eq(r.CNES)].to_csv(folder/'Internacoes_gerais_mensal_2015_2026.csv',sep=';',index=False,encoding='utf-8-sig')
        annual[annual.CNES.eq(r.CNES)].to_csv(folder/'Internacoes_gerais_anual_2015_2026.csv',sep=';',index=False,encoding='utf-8-sig')
        (folder/'LEIA_PRIMEIRO.md').write_text(f'# {r.CNES} · {r.NOME_CNES}\n\nSalve nesta pasta as exportações por diagnóstico/CID-10 e mês de atendimento. Mantenha os nomes originais e registre o período de processamento selecionado. As duas séries gerais já extraídas estão nesta pasta.\n',encoding='utf8')
    vectors=camadas({'01_cnes_bacias':inside,'02_selecao_sih':selected,'03_bordas':near})
    relatorio(audit,raw,inside,selected,near,statewide,pending,summary,archive)
    assert basin_hash==sha(F/'01_entradas/01_bacias/bacias.shp')
    audit.update({'data':datetime.now().astimezone().isoformat(),'cnes_registros':len(raw),'cnes_unicos':raw.CNES.nunique(),'competencia_cnes':raw['COMPETÊNCIA'].value_counts().to_dict(),'status_cnes':raw['STATUS DO ESTABELECIMENTO'].value_counts().to_dict(),'cnes_nas_bacias':len(inside),'selecao_nas_bacias':len(selected),'limiar_atividade_recente':INICIO_RECENTE+' a '+FIM,'MG_producao_recente':int(sih.RECENTE.sum()),'MG_recente_cnes_ativo':int((statewide.RECENTE&statewide.CNES_EXPORT).sum()),'SIH_sem_CNES':len(pending),'SIH_recente_sem_CNES':int(pending.RECENTE.sum()),'conferencia_bordas_1500m':len(near),'bacias_inalteradas':True,'classificacao_espacial_A_B_2016_2025_inalterada':True,'resumo_bacias':summary.to_dict(orient='records'),'fontes_originais':provenance,'archive':str(archive),'vetores':vectors})
    (D/'Auditoria_CNES_SIH_2026.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
    mp=F/'00_documentacao/manifesto.json';m=json.loads(mp.read_text('utf8'));m['vetores']=[r for r in m['vetores'] if '17_estabelecimentos_2026' not in r['arquivo']]+vectors;m['healthcare_2026_audit']={'auditoria':str((D/'Auditoria_CNES_SIH_2026.json').relative_to(F)),'fontes':provenance,'vetores_adicionais':len(vectors),'selecao_cnes':selected.CNES.tolist(),'destino_novas_consultas':str((P/'03_consultas_individuais').relative_to(F))};mp.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
    documentar_revisao()
    print(json.dumps({k:v for k,v in audit.items() if k not in ['vetores','fontes_originais']},ensure_ascii=True),flush=True)

if __name__=='__main__':main()
