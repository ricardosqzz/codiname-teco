# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/output/04_grade_500m/teco_grade_500m.gpkg | gpd.read_file | camada='bacias_estudo'.
# Entrada: E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg | gpd.read_file | camada='saude_hosp_inativos_candidatos'.
# Entrada: E:/teco/output/05_auditoria_saude/RD_MG_todos_estabelecimentos_2016_2025.csv | pd.read_csv.
# Entrada: E:/teco/output/04_grade_500m/tabelas/sih_todas_causas_mensal.csv | pd.read_csv.
# Entrada: E:/teco/output/04_grade_500m/tabelas/sih_total_mensal.csv | pd.read_csv.
# Entrada: E:/teco/output/04_grade_500m/auditoria/metodo_grade.json | .read_text.
# Campos/chaves em c: ANO_DADO, BACIA, ORIG_GEOM, geometry, setor_id.
# Campos/chaves em b: geometry, id.
# Campos/chaves em health: AIH_FILT, AIH_TODAS, CADASTRO, CNES, GRUPO, QA_MUN.
# Campos/chaves em pp.loc: CNES.
# Campos/chaves em pp: AIH.
# Saída: E:/teco/output/04_grade_500m/teco_grade_500m.gpkg | c.to_file.
# Saída: E:/teco/output/04_grade_500m/teco_grade_500m.gpkg | health.to_file.
# Saída: E:/teco/output/04_grade_500m/tabelas/estabelecimentos_todos_bacias.csv | .to_csv.
# Saída: E:/teco/output/04_grade_500m/tabelas/estatisticas_entradas_nativas.csv | .to_csv.
# Saída: E:/teco/output/04_grade_500m/auditoria/camadas_nativas.json | .write_text.
# Saída: E:/teco/output/04_grade_500m/auditoria/metodo_grade.json | .write_text.
# Campos/chaves gerados em c: ANO_DADO, ORIG_GEOM.
# Campos/chaves gerados em health: AIH_ANO, AIH_FILT, AIH_TODAS, CADASTRO, CNES, GRUPO, SIH_STATUS.
# Campos/chaves gerados em old: CADASTRO.
# Campos/chaves gerados em meta: mapas_entrada, status.
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
import json
import numpy as np,pandas as pd,geopandas as gpd
R=Path(_cp_texto('', 'posix'));O=R/'output/04_grade_500m';B=R/'output/02_avaliacao_espacial';G=O/'teco_grade_500m.gpkg'

# Main
def main():
 b=gpd.read_file(G,layer='bacias_estudo')
 c=gpd.read_file(B/'teco_avaliacao.gpkg',layer='analise_setores').rename(columns={'bas_id':'BACIA'})
 mapping={'POP_OFIC':'pop_2022','POP_REC':'pop_a_est','DENS_POP':'dens_pop','REDE_PCT':'pct_rede','SEM_REDE_OBS':'pct_nrede','DESC_RIO':'pct_vrio'}
 for dst,src in mapping.items():c[dst]=c[src]

 c['ORIG_GEOM']='Recorte do setor censitário na bacia';c['ANO_DADO']=2022
 c=c[['setor_id','BACIA',*mapping.keys(),'ORIG_GEOM','ANO_DADO','geometry']].copy()
 c.to_file(G,layer='entradas_censitarias_nativas',driver='GPKG')
 health=gpd.read_file(B/'teco_avaliacao.gpkg',layer='saude_cnes_ativos');health['CADASTRO']='Ativo na extração CNES'
 old=gpd.read_file(B/'teco_avaliacao.gpkg',layer='saude_hosp_inativos_candidatos');old['CADASTRO']='Inativo / referência histórica'
 health=gpd.GeoDataFrame(pd.concat([health,old],ignore_index=True),crs=health.crs);health=health.drop_duplicates('CNES').drop(columns=['bacia'],errors='ignore')
 health=health.drop(columns=['BACIA','id'],errors='ignore');health=gpd.sjoin(health,b[['id','geometry']].rename(columns={'id':'BACIA'}),how='inner',predicate='intersects').drop(columns='index_right')
 health=health.drop_duplicates(['CNES','BACIA']);health['CNES']=health.CNES.astype(str).str.replace(r'\.0$','',regex=True).str.zfill(7)
 production=R/'output/05_auditoria_saude/RD_MG_todos_estabelecimentos_2016_2025.csv'
 if production.exists():
  pp=pd.read_csv(production,sep=';',dtype={'CNES':str});health=health[health.CNES.isin(pp.loc[pp.AIH.gt(0),'CNES'])].copy()
 allf=pd.read_csv(O/'tabelas/sih_todas_causas_mensal.csv',sep=';',dtype={'CNES':str});sel=pd.read_csv(O/'tabelas/sih_total_mensal.csv',sep=';',dtype={'CNES':str})
 alltot=allf.groupby('CNES').internacoes.sum();seltot=sel.groupby('CNES').internacoes.sum()
 health['AIH_TODAS']=health.CNES.map(alltot);health['AIH_FILT']=health.CNES.map(seltot);health['AIH_ANO']=health.AIH_FILT/10
 health['SIH_STATUS']=np.where(health.AIH_TODAS.notna(),'Com AIH normais 2016-2025','Sem AIH localizada; não significa ausência de atendimento')
 health['GRUPO']=health.GRUPO.fillna('Hospital / hospital-dia');health.to_file(G,layer='saude_todos',driver='GPKG')
 health.drop(columns='geometry').to_csv(O/'tabelas/estabelecimentos_todos_bacias.csv',index=False,sep=';',encoding='utf-8-sig')
 stats=[]
 for key,g in c.groupby('BACIA'):
  for col in mapping:
   v=g[col].dropna();stats.append({'bacia':key,'variavel':col,'suporte':'Setor censitário recortado; sem grade de 500 m','n_validos':len(v),'n_ausentes':int(g[col].isna().sum()),'min':v.min(),'mediana':v.median(),'media':v.mean(),'max':v.max(),'desvio_padrao':v.std()})
 pd.DataFrame(stats).to_csv(O/'tabelas/estatisticas_entradas_nativas.csv',sep=';',decimal=',',index=False,encoding='utf-8-sig')
 info={'geometrias':'Setores censitários, pontos CNES, linhas de vias/cursos dágua e rasters nativos; grade somente em classificações/análises.','estabelecimentos':len(health),'CNES_unicos':health.CNES.nunique(),'por_bacia':health.groupby('BACIA').size().to_dict(),'por_grupo':health.groupby('GRUPO').size().to_dict(),'inativos':int(health.CADASTRO.str.startswith('Inativo').sum()),'QA_municipal_divergente':int(health.QA_MUN.eq(0).sum()),'limite':'Somente produção SIH positiva 2016-2025 e localização dentro da bacia. Rede que interna residentes dos quatro municípios: 383 hospitais em tabela separada NRMG, não limitada ao interior da bacia.'}
 (O/'auditoria/camadas_nativas.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf8');print('NATIVAS_PREPARADAS',json.dumps(info,ensure_ascii=True),flush=True)
 meta=json.loads((O/'auditoria/metodo_grade.json').read_text('utf8'));meta['status']='Exploratório local: filtro amplo de etiologias bacterianas codificadas e síndromes compatíveis (A+B). Não atribui internações à residência nem confirma RAM.';meta['mapas_entrada']='Geometrias nativas; grade restrita a classificação, k-means, Moran e análises multivariadas.';(O/'auditoria/metodo_grade.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
