# ENTRADAS: output/07_microplasticos/microplasticos.gpkg e tabelas; campos definidos em FIELDS abaixo.
# SAÍDAS: entrega_final/01_entradas/18_residuos, 19_licenciamento; 02_saidas/06_microplasticos; 03_mapas/14_microplasticos.
# DICIONÁRIOS: 00_documentacao/Microplasticos; nomes curtos SHP, unidade, definição e script produtor.
# CAMINHOS: TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json; saídas existentes do módulo são arquivadas em descontinuado.
from pathlib import Path
import json,shutil,datetime,hashlib
import geopandas as gpd
import pandas as pd
from caminhos_teco import raiz_projeto
R=raiz_projeto();O=R/'output/07_microplasticos';F=R/'entrega_final';STAMP=datetime.datetime.now().strftime('%Y%m%d_%H%M%S');D=F/'00_documentacao/Microplasticos';D.mkdir(parents=True,exist_ok=True)
FIELDS={
'GRID_ID':('GRID_ID','Identificador do centro da grade; usar junto com BACIA para distinguir fragmentos.','código'),
'BACIA':('BACIA','Bacia contribuinte: pampulha, vargem_flores ou ibirite_regap.','código'),
'AREA_KM2':('AREA_KM2','Área do círculo de cálculo de raio 500 m recortado pela bacia; não é a área do hexágono exibido.','km²'),
'POP_DENS':('POP_DENS','População Censo 2022 alocada proporcionalmente à área do setor e dividida pela área do círculo.','habitantes/km²'),
'SEM_REDE':('SEM_REDE','Domicílios estimados sem ligação à rede geral/pluvial ou fossa ligada à rede; não equivale a ausência de tratamento.','%'),
'SEWER_DENS':('SEW_DENS','Domicílios sem ligação geral/pluvial estimados na vizinhança divididos pela área do círculo; herda o tratamento de lacunas do esgotamento anterior.','domicílios/km²'),
'WASTE_DENS':('WAS_DENS','Ponto médio dos limites agregados de domicílios sem coleta por serviço de limpeza dividido pela área do círculo.','domicílios/km²'),
'WASTE_PCT':('WASTE_PCT','Ponto médio do percentual domiciliar sem coleta, ponderado por domicílios e área de interseção.','%'),
'WASTE_LO':('WASTE_LO','Limite inferior do percentual sem coleta compatível com contagens conhecidas e total de domicílios; sigilo não foi convertido em zero.','%'),
'WASTE_HI':('WASTE_HI','Limite superior do percentual sem coleta compatível com contagens conhecidas e total de domicílios.','%'),
'WASTE_COV':('WASTE_COV','Proporção de domicílios da vizinhança com limites de destino do lixo calculáveis; elegibilidade exige pelo menos 99,9%.','%'),
'ROAD_DENS':('ROAD_DENS','Comprimento das vias cadastradas no círculo dividido por sua área; indicador geométrico, sem volume de tráfego ou fator de emissão de pneus.','km/km²'),
'MP_VALID':('MP_VALID','1 se elegível na base anterior, com domicílios, dados finitos e cobertura de resíduos >=99,9%; 0 caso contrário.','0/1'),
'MP_INDEX':('MP_INDEX','Média dos quatro critérios log1p/min-max com pesos iguais; pressão relativa exploratória, não concentração nem probabilidade.','0–100'),
'MP_CLASS':('MP_CLASS','Classe fixa do índice: 1 <=20; 2 >20–40; 3 >40–60; 4 >60–80; 5 >80; 0 insuficiente.','classe'),
'MP_QUINT':('MP_QUINT','Quintil global do índice entre unidades elegíveis das três bacias; fronteiras P20/P40/P60/P80 inclusivas à esquerda.','1–5; 0 insuficiente'),
'MP_K':('MP_K','Perfil k-means do cenário S0, ordenado pela média do índice; perfil não é classe de risco.','perfil'),
'MP_STAB':('MP_STAB','Percentual dos cinco cenários com mesmo perfil de S0, após alinhar rótulos e manter K de S0; inclui S0.','%'),
'MP_LO':('MP_LO','Índice S0 com limite inferior da contagem sem coleta, mantendo as escalas do cenário central e truncamento em 0–1.','0–100'),
'MP_HI':('MP_HI','Índice S0 com limite superior da contagem sem coleta; mede apenas incerteza do sigilo do lixo, não incerteza total.','0–100'),
'MP_MORAN':('MP_MORAN','Moran local do índice em oito vizinhos por bacia: HH/LL/HL/LH após BH 5%; NS não significativo; ND não elegível.','categoria'),
'MP_P':('MP_P','Pseudo-p bilateral do Moran local com 999 permutações condicionais; não é teste da existência de microplásticos.','0–1'),
'MP_Q':('MP_Q','Valor p ajustado por Benjamini-Hochberg dentro de cada bacia e tema.','0–1'),
'ARG_INDEX':('ARG_INDEX','Cópia integral do índice ARG anterior I_S0; não recalculado nem calibrado por microplásticos.','0–100'),
'ARG_K':('ARG_K','Cópia integral do perfil ARG anterior K_S0.','perfil')}
for j,name in enumerate(['População','Domicílios sem rede','Domicílios sem coleta','Densidade viária'],1):FIELDS['MP_N'+str(j)]=('MP_N'+str(j),f'{name}: log1p e min-max conjunto fixo nas três bacias; parâmetros em normalizacao.csv.','0–1')
for sc in range(5):
 FIELDS['MP_S'+str(sc)]=('MP_S'+str(sc),f'Índice do cenário S{sc}; pesos na configuração e tabela de sensibilidade.','0–100')
 FIELDS['MK_S'+str(sc)]=('MK_S'+str(sc),f'Perfil k-means S{sc}, com K de S0 e rótulos alinhados por máxima coincidência.','perfil')
COMMON={'BACIA':('Bacia contribuinte.','código'),'REC_ID':('Identificador genérico do registro; não identifica pessoa física.','código')}
DICT=[]

# Preservação e exportação
def archive(p):
 if p.exists():
  dst=R/'descontinuado'/STAMP/'microplasticos'/p.relative_to(F);dst.parent.mkdir(parents=True,exist_ok=True)
  assert dst.resolve().is_relative_to((R/'descontinuado').resolve());shutil.move(str(p),str(dst))
def export(g,relative,name,defs):
 folder=F/relative;archive(folder);folder.mkdir(parents=True,exist_ok=True);data=g[list(defs)+['geometry']].copy();rename={k:v[0] for k,v in defs.items()};data.rename(columns=rename,inplace=True)
 for c in data.select_dtypes(include=['object','str']).columns:
  if c!='geometry':data[c]=data[c].map(lambda v:v[:250] if isinstance(v,str) else v)
 path=folder/(name+'.shp');data.to_file(path,driver='ESRI Shapefile',encoding='UTF-8')
 rows=[]
 for field,(short,desc,unit) in defs.items():
  row={'arquivo':str(path.relative_to(F)).replace('\\','/'),'campo_shp':short,'campo_original':field,'descricao':desc,'unidade':unit,'natureza':'derivado; ver definição','fonte_camada':str(O/'microplasticos.gpkg'),'script_python':'05_scripts/python/microplasticos_teco.py','linha_referencia':'','trecho_referencia':field,'scripts_apoio':'05_scripts/python/consolidar_microplasticos_teco.py'};rows.append(row);DICT.append(row)
 pd.DataFrame(rows).to_csv(folder/'campos.csv',sep=';',index=False,encoding='utf-8-sig');(folder/'README.md').write_text('\n'.join(f"- **{r['campo_shp']}** ({r['unidade']}): {r['descricao']}" for r in rows),encoding='utf8')
 return path

# Camadas finais
def main():
 g=gpd.read_file(O/'microplasticos.gpkg',layer='microplastic_pressure');export(g,'02_saidas/06_microplasticos/01_consolidado','microplastics',FIELDS)
 s=gpd.read_file(O/'microplasticos.gpkg',layer='waste_census')
 defs={'setor_id':('SECTOR_ID','Código do setor censitário Censo 2022; contagens originais referem-se ao setor inteiro.','código'),'BACIA':('BACIA','Bacia do recorte geométrico.','código'),'HH_TOTAL':('HH_TOTAL','Domicílios particulares permanentes ocupados do setor inteiro; denominador do destino do lixo.','domicílios'),'ORIG_KM2':('ORIG_KM2','Área do setor inteiro antes do recorte; usada para alocação proporcional.','km²'),'PART_KM2':('PART_KM2','Área da interseção setor/bacia.','km²'),'UNC_LO':('UNC_LO','Limite inferior de domicílios sem coleta no setor inteiro.','domicílios'),'UNC_HI':('UNC_HI','Limite superior de domicílios sem coleta no setor inteiro.','domicílios'),'WASTE_PCT':FIELDS['WASTE_PCT'],'WASTE_LO':FIELDS['WASTE_LO'],'WASTE_HI':FIELDS['WASTE_HI'],'WASTE_EST':('WASTE_EST','1 se usado ponto médio de intervalo de sigilo; 0 se combinado exato ou inválido, conferir QA.','0/1'),'WASTE_QA':('WASTE_QA','exact_combined: combinado exato; interval_midpoint: hipótese central; no_households: sem domicílios; inconsistent_or_missing: excluir.','categoria')}
 defs['WASTE_PCT']=('WASTE_PCT','Ponto médio do intervalo percentual sem coleta do setor inteiro; não recalculado apenas para a geometria recortada.','%')
 defs['WASTE_LO']=('WASTE_LO','Limite inferior de domicílios sem coleta / HH_TOTAL do setor inteiro × 100.','%')
 defs['WASTE_HI']=('WASTE_HI','Limite superior de domicílios sem coleta / HH_TOTAL do setor inteiro × 100.','%')
 export(s,'01_entradas/18_residuos/01_destino_lixo','waste_census',defs)
 raw=F/'01_entradas/18_residuos/00_tabelas';raw.mkdir(exist_ok=True,parents=True)
 for p in (O/'tabelas').glob('*.csv'):
  if p.stem.startswith(('ibge_','sinir_','planos_','instalacoes_','residuos_por')):shutil.copy2(p,raw/p.name)
 lic=gpd.read_file(O/'microplasticos.gpkg',layer='licensing_screening');ld={k:(k,desc,unit) for k,(desc,unit) in {**COMMON,'SOURCE':('Cadastro SLA ou histórico estadual 2013–2019; registros não equivalem a estabelecimentos únicos.','cadastro'),'PROCESS':('Número público do processo de licenciamento.','identificador'),'ACT_CODE':('Código da atividade principal do cadastro ambiental, não CNAE.','código'),'ACTIVITY':('Descrição da atividade principal; texto completo em licencas_triagem.csv.','texto'),'STATUS':('Situação SLA ou modalidade do processo histórico; não confirma operação atual.','texto'),'VALIDITY':('Validade conforme cadastro; histórico pode informar duração e não data final.','texto'),'ISSUED':('Data de emissão SLA ou ano do processo histórico.','data/ano'),'MP_CAND':('1 se descrição menciona plástico, termoplástico, borracha, têxtil, lavanderia, resina ou polímero; requer leitura do processo.','0/1'),'REVIEW':('Estado de triagem: verificar processo e operação antes de utilizar como fonte quantitativa.','texto'),'URL':('Consulta pública de origem do processo.','URL')}.items()};export(lic,'01_entradas/19_licenciamento/01_triagem','licensing',ld)
 fac=gpd.read_file(O/'microplasticos.gpkg',layer='waste_management');fd={k:(k,d,u) for k,(d,u) in {**COMMON,'TYPE':('Tipo do cadastro: aterro sanitário, transbordo ou disposição precária.','categoria'),'MUNICIPAL':('Município informado no cadastro da instalação.','texto'),'STATUS':('Situação informada pelo cadastro, sem inspeção de campo.','texto'),'SHARED':('Indicação cadastral de uso compartilhado; não comprova capacidade de recebimento.','texto'),'IN_BASIN':('1 se ponto intersecta uma das bacias, 0 se apenas no contexto regional de 20 km.','0/1'),'CHECK':('Pendência de verificar operação, resíduos aceitos e vínculo com o município gerador.','texto')}.items()};export(fac,'01_entradas/18_residuos/02_instalacoes','waste_fac',fd)
 plans=gpd.read_file(O/'microplasticos.gpkg',layer='municipal_waste_plans');pdct={k:(short,d,u) for k,short,d,u in [('nome','MUNICIPAL','Município do polígono; indicador administrativo, não medição em 500 m.','texto'),('geocodigo','MUN_CODE','Código municipal IBGE.','código'),('pmgirs_24','PLAN_2024','Existência informada de plano de gestão integrada em 2024.','cadastro'),('colsel_24','SEL_2024','Existência informada de coleta seletiva em 2024; não é percentual de cobertura.','cadastro'),('tiprsu_24','DEST_2024','Tipologia declarada de destinação final municipal em 2024.','cadastro')]};export(plans,'01_entradas/18_residuos/03_planos','waste_plans',pdct)
 for code in ['S0','S1','S2','S3','S4']:
  keep={k:v for k,v in FIELDS.items() if k in ['GRID_ID','BACIA','MP_VALID','MP_'+code,'MK_'+code,'MP_STAB']};export(g,f'02_saidas/06_microplasticos/02_testes/{code}',code.lower(),keep)
 target=F/'02_saidas/06_microplasticos/03_tabelas';archive(target);shutil.copytree(O/'tabelas',target)
 target=F/'02_saidas/06_microplasticos/04_conectividade';archive(target);shutil.copytree(O/'rasters',target)
 target=F/'03_mapas/14_microplasticos';archive(target);shutil.copytree(O/'figuras',target)
 for n in ['obter_residuos_licenciamento.py','microplasticos_teco.py','mapas_microplasticos_teco.py','consolidar_microplasticos_teco.py','integrar_qgis_microplasticos.py','documentar_microplasticos_teco.py']:
  dest=F/'05_scripts/python'/n;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(R/'codigo'/n,dest)
 cfg=F/'05_scripts/config';cfg.mkdir(exist_ok=True,parents=True);shutil.copy2(R/'config/microplasticos.json',cfg/'microplasticos.json')
 pd.DataFrame(DICT).to_csv(D/'Dicionario_microplasticos.csv',sep=';',index=False,encoding='utf-8-sig')
 (D/'Dicionario_QGIS.json').write_text(json.dumps({r['campo_shp']:r['descricao']+' Unidade: '+r['unidade'] for r in DICT},ensure_ascii=False,indent=2),encoding='utf8')
 p=F/'00_documentacao/Dicionario_dos_campos.csv';old=pd.read_csv(p,sep=';',dtype=str).fillna('');old=old[~old.arquivo.str.contains('18_residuos|19_licenciamento|06_microplasticos',regex=True)];allrows=pd.concat([old,pd.DataFrame(DICT)],ignore_index=True);allrows.to_csv(p,sep=';',index=False,encoding='utf-8-sig')
 (p.with_suffix('.json')).write_text(allrows.to_json(orient='records',force_ascii=False,indent=2),encoding='utf8')
 (p.with_suffix('.html')).write_text('<!doctype html><meta charset="utf-8"><title>Dicionário de campos</title><style>body{font:14px Arial}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #ccd8da;vertical-align:top}</style><h1>Dicionário de campos | ARG e microplásticos</h1>'+allrows.to_html(index=False,escape=True),encoding='utf8')
 shutil.copy2(O/'auditoria/metodo_microplasticos.json',D/'Auditoria_microplasticos.json')
 p=D/'Inventario_arquivos.csv';rows=[]
 for folder in [F/'01_entradas/18_residuos',F/'01_entradas/19_licenciamento',F/'02_saidas/06_microplasticos',F/'03_mapas/14_microplasticos']:
  for f in folder.rglob('*'):
   if f.is_file():rows.append({'arquivo':str(f.relative_to(F)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 pd.DataFrame(rows).to_csv(p,sep=';',index=False,encoding='utf-8-sig');print('Consolidado',len(rows),'arquivos;',len(DICT),'campos',flush=True)
if __name__=='__main__':main()
