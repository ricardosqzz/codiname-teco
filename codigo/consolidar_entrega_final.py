# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/entrega_final/{rel} | gpd.read_file.
# Entrada: E:/teco/entrega_final/{rel} | rasterio.open.
# Entrada: E:/teco/output/04_grade_500m/teco_grade_500m.gpkg | gpd.read_file | camada='influencia_500m'.
# Entrada: E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg | gpd.read_file | camada='rotas_d8_candidatas'.
# Entrada: E:/teco/reservatorio/{key}.shp | gpd.read_file.
# Entrada: E:/teco/config/encartes_teco.json | .read_text.
# Entrada: E:/teco/output/05_auditoria_saude/saude_tabnet_auditada.gpkg | gpd.read_file | camada='rede_internacoes_residentes'.
# Entrada: E:/teco/output/03_multivariada/teco_multivariada.gpkg | gpd.read_file | camada='exutorios_referencia'.
# Entrada: {p} | gpd.read_file.
# Entrada: E:/teco/output/04_grade_500m/auditoria/galeria.json | .read_text.
# Entrada: E:/teco/output/04_grade_500m/auditoria/metodo_grade.json | .read_text.
# Entrada: E:/teco/output/05_auditoria_saude/consolidacao.json | .read_text.
# Campos/chaves em r: arquivo.
# Campos/chaves em record: arquivo.
# Campos/chaves em b: geometry, id.
# Campos/chaves em c: V00309, V00310, V00311, V00312, V00313, V00314, V00315, V00316, bas_id, dens_pop, dom_set, n_sigilo, pct_nrede, pct_rede, pct_vrio, pop_2022, pop_a_est, rede_set, setor_id.
# Campos/chaves em hyd: BACIA, geometry, id.
# Campos/chaves em b.loc: id.
# Campos/chaves em roads: TIPO_VIA, geometry, hier_legal, ogc_fid.
# Campos/chaves em q: Name, geometry.
# Campos/chaves em row: grupo, slug.
# Saída: E:/teco/entrega_final/{rel} | g.to_file.
# Saída: path.parent/dicionario_campos.csv | .to_csv.
# Saída: E:/teco/entrega_final/00_documentacao/Dicionario_dos_campos.csv | .to_csv.
# Saída: E:/teco/entrega_final/00_documentacao/Inventario_de_camadas.csv | .to_csv.
# Saída: E:/teco/entrega_final/00_documentacao/manifesto.json | .write_text.
# Campos/chaves gerados em ww: AREA_KM2.
# Campos/chaves gerados em hyd: COMP_KM.
# Campos/chaves gerados em inner: COMP_KM.
# Campos/chaves gerados em q: BACIA.
# Campos/chaves gerados em a: AREA_CEL.
# Campos/chaves gerados em km: PERFIL_S0.
# Campos/chaves gerados em row: titulo.
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

from dicionario_campos_teco import descrever_campo
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,shutil,re,unicodedata,csv,html,hashlib
import numpy as np,pandas as pd,geopandas as gpd,rasterio
from shapely.geometry import box
R=Path(_cp_texto('', 'posix'));F=R/'entrega_final';B=R/'output/02_avaliacao_espacial';O=R/'output/04_grade_500m';H=R/'output/05_auditoria_saude';G=O/'teco_grade_500m.gpkg';NOW=datetime.now(ZoneInfo('America/Sao_Paulo'))
VECTORS=[];RASTERS=[];FIELDS=[];MAPS=[];SOURCE_MAP={}
ALIAS={'SEM_REDE_OBS':'SEM_REDE','ESTABILIDADE':'ESTAB_PCT','N_AIH_LOCAL':'N_AIH_LOC','ORIG_STATUS':'ORIG_SIT','SIT_ESPACIAL':'SIT_ESP','NOME_TABNET':'NOME','AIH_NRMG':'AIH_RES','MEDIA_ANUAL_AB':'AIH_AB_ANO','DIST_BACIA_M':'DIST_BAC_M','MUNICIPIO':'MUN_CNES'}

# Slug
def slug(text):return re.sub(r'[^a-z0-9]+','_',unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode().lower()).strip('_')

# Desc
def desc(field, arquivo=''):
 return descrever_campo(field, arquivo)

# Shapefile
def shapefile(g,rel,role,title,source):
 g=g.copy()
 if g.crs is None:raise ValueError('CRS ausente: '+title)
 g=g.to_crs(31983);assert g.loc[g.geometry.notna()].geometry.is_valid.all(),title
 path=F/rel;path.parent.mkdir(parents=True,exist_ok=True);mapping={};seen=set()
 for c in g.columns:
  if c=='geometry':continue
  name=ALIAS.get(c,c)
  name=re.sub('[^A-Za-z0-9_]','_',unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode())[:10] or 'CAMPO'
  base=name;count=1
  while name.upper() in seen:name=base[:8]+str(count);count+=1
  seen.add(name.upper());mapping[c]=name
  if pd.api.types.is_bool_dtype(g[c]):g[c]=g[c].astype('Int32')
  if c in ['CNES','setor_id','CD_SETOR','GRID_ID']:g[c]=g[c].astype('string')
  FIELDS.append({'arquivo':str(Path(rel)).replace('\\','/'),'campo_shp':name,'campo_original':c,'descricao':desc(c,str(Path(rel)).replace('\\','/'))})
 g=g.rename(columns=mapping);g=g[[c for c in g.columns if c!='geometry']+['geometry']];g.to_file(path,index=False,driver='ESRI Shapefile',encoding='UTF-8')
 read=gpd.read_file(path);assert len(read)==len(g) and list(read.columns)==list(g.columns),(title,read.columns,g.columns)
 for c in ['CNES','setor_id','CD_SETOR','GRID_ID']:
  if c in mapping:assert read[mapping[c]].astype('string').equals(g[mapping[c]].astype('string')),(title,c)
 record={'arquivo':str(Path(rel)).replace('\\','/'),'titulo':title,'papel':role,'feicoes':len(g),'sem_geometria':int(g.geometry.isna().sum()),'crs':'EPSG:31983','fonte':source,'campos':mapping};VECTORS.append(record)
 pd.DataFrame([r for r in FIELDS if r['arquivo']==record['arquivo']]).to_csv(path.parent/'dicionario_campos.csv',sep=';',index=False,encoding='utf-8-sig')
 print('SHP',path.stem,len(g),flush=True);return path

# Raster
def raster(src,rel,role,title):
 dst=F/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 with rasterio.open(dst) as d:
  vals=d.read(1,masked=True);v=vals.compressed();v=v[np.isfinite(v)];assert len(v),dst;RASTERS.append({'arquivo':str(Path(rel)).replace('\\','/'),'titulo':title,'papel':role,'crs':str(d.crs),'pixel_x_m':d.res[0],'pixel_y_m':d.res[1],'min':float(v.min()),'max':float(v.max()),'fonte':str(src)})
 for extra in ['.qml']:
  if src.with_suffix(extra).exists():shutil.copy2(src.with_suffix(extra),dst.with_suffix(extra))
 SOURCE_MAP[str(src).replace('\\','/')]=str(dst)
 return dst

# Copy
def copy(src,rel):
 dst=F/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);return dst

# Main
def main():
 if F.exists():
  assert F.resolve().parent==R.resolve() and F.name=='entrega_final'
  target=R/'descontinuado'/NOW.strftime('%Y%m%d_%H%M%S_entrega_final');assert target.resolve().is_relative_to((R/'descontinuado').resolve());F.rename(target)
 F.mkdir();(F/'00_documentacao').mkdir();b=gpd.read_file(G,layer='bacias_estudo');a=gpd.read_file(G,layer='grade_resultados');c=gpd.read_file(B/'teco_avaliacao.gpkg',layer='analise_setores')
 shapefile(b,'01_entradas/01_bacias/bacias.shp','entrada','Delimitações utilizadas',str(G)+'|bacias_estudo')
 water=[]
 names={'pampulha':'Lagoa da Pampulha','vargem_flores':'Reservatório de Vargem das Flores','ibirite_regap':'Reservatório de Ibirité / REGAP'}
 for key in b.id:
  ww=gpd.read_file(R/'reservatorio'/f'{key}.shp').to_crs(31983);water.append({'BACIA':key,'NOME':names[key],'geometry':ww.geometry.union_all()})
 ww=gpd.GeoDataFrame(water,crs=31983);ww['AREA_KM2']=ww.area/1e6;shapefile(ww,'01_entradas/02_reservatorios/reservatorios.shp','entrada','Reservatórios em estudo',_cp_texto('reservatorio', 'posix'))
 pop=gpd.GeoDataFrame({'setor_id':c.setor_id,'BACIA':c.bas_id,'POP_OFIC':c.pop_2022,'POP_REC':c.pop_a_est,'DENS_POP':c.dens_pop,'geometry':c.geometry},crs=c.crs);shapefile(pop,'01_entradas/03_populacao/populacao.shp','entrada','População nos setores recortados',str(B/'teco_avaliacao.gpkg')+'|analise_setores')
 sewer=gpd.GeoDataFrame({'setor_id':c.setor_id,'BACIA':c.bas_id,'DOM_TOT':c.dom_set,'DOM_REDE':c.rede_set,'REDE_PCT':c.pct_rede,'SEM_REDE_OBS':c.pct_nrede,'DESC_RIO':c.pct_vrio,'REDE_DIR':c.V00309,'FOSS_REDE':c.V00310,'FOSS_SREDE':c.V00311,'FOSSA_RUD':c.V00312,'VALA':c.V00313,'RIO_LAGO':c.V00314,'OUTRO':c.V00315,'SEM_BANH':c.V00316,'SIGILO_N':c.n_sigilo,'geometry':c.geometry},crs=c.crs);shapefile(sewer,'01_entradas/04_esgotamento/esgotamento.shp','entrada','Esgotamento observado: contagens e percentuais',str(B/'teco_avaliacao.gpkg')+'|analise_setores')
 hyd=gpd.read_file(G,layer='hidro_contexto');hyd=hyd[['id','BACIA','geometry']].copy();hyd['COMP_KM']=hyd.length/1000;shapefile(hyd,'01_entradas/05_hidrografia/hidrografia.shp','entrada','Hidrografia dentro das bacias',str(G)+'|hidro_contexto')
 roads=gpd.read_file(G,layer='vias_contexto');frames=[]
 for geom in b.geometry:
  x0,y0,x1,y1=geom.bounds;key=b.loc[b.geometry==geom,'id'].iloc[0];view=json.loads((R/'config/encartes_teco.json').read_text('utf8')).get(key,{}) if (R/'config/encartes_teco.json').exists() else {};cx=(x0+x1)/2+view.get('dx',0);cy=(y0+y1)/2+view.get('dy',0);frames.append(box(cx-9112.5,cy-9112.5,cx+9112.5,cy+9112.5))
 context=gpd.clip(roads[['ogc_fid','hier_legal','TIPO_VIA','geometry']],gpd.GeoSeries(frames,crs=31983).union_all());context=context[context.geom_type.isin(['LineString','MultiLineString'])];shapefile(context,'01_entradas/06_vias_contexto/vias_contexto.shp','entrada','Vias de composição dos encartes',str(G)+'|vias_contexto')
 inner=gpd.overlay(roads[['ogc_fid','hier_legal','TIPO_VIA','geometry']],b[['id','geometry']],how='intersection',keep_geom_type=True).rename(columns={'id':'BACIA'});inner['COMP_KM']=inner.length/1000;shapefile(inner,'01_entradas/07_vias_bacias/vias_bacias.shp','entrada','Vias recortadas para análise',str(G)+'|vias_contexto')
 health=gpd.read_file(G,layer='saude_todos');cols=['CNES','NOME','GRUPO','TIPO','BACIA','AIH_TODAS','AIH_FILT','AIH_ANO','QA_MUN','geometry'];shapefile(health[cols],'01_entradas/08_saude_local/saude_local.shp','entrada','Instituições com SIH positivo dentro das bacias',str(G)+'|saude_todos')
 hr=gpd.read_file(H/'saude_tabnet_auditada.gpkg',layer='rede_internacoes_residentes');cols=['CNES','NOME_TABNET','MUNICIPIO','BACIA','SIT_ESPACIAL','AIH_NRMG','AIH_A','AIH_B','AIH_AB','MEDIA_ANUAL_AB','DIST_BACIA_M','geometry'];shapefile(hr[cols],'01_entradas/09_saude_residencia/saude_residencia.shp','entrada','Rede de internações de residentes dos quatro municípios',str(H/'saude_tabnet_auditada.gpkg')+'|rede_internacoes_residentes')
 ex=gpd.read_file(R/'output/03_multivariada/teco_multivariada.gpkg',layer='exutorios_referencia');shapefile(ex,'01_entradas/10_exutorios/exutorios.shp','referencia','Exutórios de referência',str(R/'output/03_multivariada/teco_multivariada.gpkg')+'|exutorios_referencia')
 samples=[]
 for p in (R/'pt_coleta').glob('*.shp'):
  q=gpd.read_file(p).to_crs(31983);q=q[['Name','geometry']].rename(columns={'Name':'COLETA_ID'});q['BACIA']='ibirite_regap' if p.stem=='regap_ibirite' else p.stem;samples.append(q)
 shapefile(gpd.GeoDataFrame(pd.concat(samples,ignore_index=True),crs=31983),'01_entradas/11_pontos_coleta/pontos_coleta.shp','referencia','Pontos de coleta fornecidos pelo pesquisador',_cp_texto('pt_coleta', 'posix'))
 raster(R/'teco_base/uso_terra/uso_terra-reservatorio.tif','01_entradas/12_uso_solo/uso_solo_2025.tif','entrada','Uso do solo: ano 2025 informado no projeto')
 raster(R/'temp/cop30_dem.tif','01_entradas/13_relevo/MDE_base_Copernicus.tif','entrada','MDE integrado Copernicus, suporte do relevo')
 for p in (B/'rasters').glob('*.tif'):
  if any(p.name.endswith('_'+s+'.tif') for s in ['hipsometria','declividade_pct','declividade_embrapa','distancia_hidrologica_km','conexao_lago']):raster(p,'01_entradas/13_relevo/'+p.name,'entrada_tratada','Relevo e condicionantes · '+p.stem)
 a['AREA_CEL']=a.area/1e6;shapefile(a,'02_saidas/01_matriz_completa/matriz_resultados.shp','saida','Matriz completa de resultados na grade de apresentação',str(G)+'|grade_resultados')
 base=['GRID_ID','BACIA','VALIDO','AREA_KM2','AREA_CEL'];score=base+['POP_DENS','SEM_REDE','AIH_LOCAL','N_POP_DENS','N_SEM_REDE','N_AIH_LOCAL']+[f'{k}_S{i}' for i in range(5) for k in ['I','F']];shapefile(a[score+['geometry']],'02_saidas/02_multivariada/multivariada.shp','saida','Escores e faixas dos cinco cenários',str(G)+'|grade_resultados')
 km=a[base+['POP_DENS','SEM_REDE','AIH_LOCAL','URB_PCT']+[f'K_S{i}' for i in range(5)]+['ESTABILIDADE','geometry']].copy();km['PERFIL_S0']=km.K_S0.map({0:'Sem classe: entrada incompleta',1:'Maior adensamento e maior ligacao a rede',2:'Menor adensamento e menor ligacao a rede'});shapefile(km,'02_saidas/03_kmeans/kmeans.shp','saida','Perfis k-means: identificadores sem ordem universal de risco',str(G)+'|grade_resultados')
 shapefile(a[base+['I_S0','MORAN','MORAN_Q','COB_ESG','EST_ESG','geometry']],'02_saidas/04_moran/moran.shp','saida','Moran local do cenário S0',str(G)+'|grade_resultados')
 shapefile(a[base+[f'{k}_S{i}' for i in range(5) for k in ['I','F','K']]+['ESTABILIDADE','geometry']],'02_saidas/05_sensibilidade/sensibilidade.shp','saida','Comparação dos cenários de ponderação',str(G)+'|grade_resultados')
 shapefile(a[base+['I_S0','QUINTIL','geometry']],'02_saidas/06_quintis/quintis.shp','saida','Quintis: comparação distinta das faixas fixas',str(G)+'|grade_resultados')
 shapefile(gpd.read_file(G,layer='centros_500m'),'02_saidas/07_centros_grade/centros.shp','suporte','Centros da grade de análise',str(G)+'|centros_500m')
 circles=gpd.read_file(G,layer='influencia_500m');shapefile(circles,'02_saidas/08_vizinhancas_500m/vizinhancas.shp','suporte','Vizinhanças circulares onde os atributos são calculados',str(G)+'|influencia_500m')
 route=gpd.read_file(B/'teco_avaliacao.gpkg',layer='rotas_d8_candidatas');shapefile(route,'02_saidas/09_rotas_terreno/rotas_terreno.shp','complemento','Trajetórias topográficas candidatas D8',str(B/'teco_avaliacao.gpkg')+'|rotas_d8_candidatas')
 for p in (O/'rasters').glob('*.tif'):raster(p,'02_saidas/10_conectividade/'+p.name,'saida','Leitura topológica a montante · '+p.stem)
 groups={'Entradas na geometria de origem':'01_entradas','Saúde e abrangência':'02_saude','Entradas originais':'03_uso_solo','Relevo':'04_relevo','Classificação em cinco faixas':'05_multivariada','K-means':'06_kmeans','Comparação percentílica':'07_quintis','Sensibilidade':'08_sensibilidade','Moran':'09_moran','Conectividade exploratória':'10_conectividade','Grade e contexto':'11_grade_e_contexto','Internações por residência':'12_series_internacoes'}
 gallery=json.loads((O/'auditoria/galeria.json').read_text('utf8'))
 for row in gallery:
  if row['slug']=='nativo_DESC_RIO':row['titulo']='Destinação declarada em vala ou corpo hídrico'
  sub=groups.get(row['grupo'],slug(row['grupo']));relative='03_mapas/'+sub+'/'+row['slug'];row={**row,'arquivo':relative+'.png','vetorial':relative+'.svg'}
  for ext in ['png','svg']:copy(O/'figuras'/f"{row['slug']}.{ext}",relative+'.'+ext)
  MAPS.append(row)
 for name in ['Conferencia_Internacoes_Residencia.xlsx','Estabelecimentos_confirmados_residencia.csv','NRMG_compativel_mensal_estabelecimento.csv','NRMG_compativel_mensal_CID10.csv','NRMG_compativel_anual_CID10.csv','NRMG_internacoes_por_residencia_anuais.csv','Filtro_CID10_residencia.csv','RD_residentes_CEP_agregado.csv','RD_registros_codificacao_nao_mapeada.csv','conferencia_NRMG_RD_reconciliada.csv','explorador_residencia.html','consolidacao.json','validacao_final.json']:copy(H/name,'04_saude_residencia/'+name)
 for name in ['Relatorio_TECO.pdf','Relatorio_TECO.md']:copy(B/name,'00_documentacao/'+name)
 copy(O/'Estatisticas_e_Metodologia_TECO.xlsx','00_documentacao/Estatisticas_e_Metodologia_TECO.xlsx')
 for name in ['cenarios_grade.csv','kmeans_grade.csv','perfis_grade.csv','moran_grade.csv','normalizacao_grade.csv','indicadores_grade.csv','estatisticas_camadas.csv','regras_filtro_bacteriano.csv']:copy(O/'tabelas'/name,'00_documentacao/tabelas/'+name)
 pd.DataFrame(FIELDS).to_csv(F/'00_documentacao/Dicionario_dos_campos.csv',sep=';',index=False,encoding='utf-8-sig');pd.DataFrame([{k:v for k,v in r.items() if k!='campos'} for r in VECTORS]+RASTERS).to_csv(F/'00_documentacao/Inventario_de_camadas.csv',sep=';',index=False,encoding='utf-8-sig')
 manifest={'data':NOW.isoformat(),'pasta':str(F),'vetores':VECTORS,'rasters':RASTERS,'mapas':MAPS,'metodo_kmeans':json.loads((O/'auditoria/metodo_grade.json').read_text('utf8')),'saude':json.loads((H/'consolidacao.json').read_text('utf8')),'observacoes':['Um SHP por pasta; manter SHP, SHX, DBF, PRJ e CPG juntos.','Rasters nativos preservados, sem vetorização ou redução de resolução.','Grade apenas nas análises, não no desenho dos dados de entrada.','Os grupos atuais usam o cenário institucional local. A rede ampliada NRMG ainda exige geografia da residência para atribuição à grade.','DESC_RIO contém vala+corpo hídrico: rótulo corrigido para corresponder ao cálculo.']}
 (F/'00_documentacao/manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8');print('CONSOLIDADO',len(VECTORS),'SHP',len(RASTERS),'RASTERS',len(MAPS),'FIGURAS',flush=True)
if __name__=='__main__':main()
