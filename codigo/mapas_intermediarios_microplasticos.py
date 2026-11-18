# ENTRADAS: output/07_microplasticos/microplasticos.gpkg; licensing_screening (REC_ID,ACTIVITY,SOURCE), municipal_waste_plans e waste_census (V00399-00402,WASTE_LO,WASTE_HI).
# CONTEXTO: mapas_microplasticos_teco.py fornece bacias, reservatórios, vias, enquadramentos e escala de impressão.
# SAÍDAS: figuras 14-20; shapefiles 19_licenciamento/02_tipologias e 18_residuos/04_destinos,05_coleta,06_planos,07_lixo_intermediario; tabela, dicionário e auditoria.
# CAMPOS: TP_CODE/TP_NAME agrupam atividades; MP_LINK qualifica vínculo documental, sem peso no índice; DOM_DEST e WASTE_UNC descrevem lixo censitário.
# CAMINHOS: TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json; classificação da atividade principal não comprova emissão ou operação atual.
from pathlib import Path
import json,unicodedata,datetime,shutil
import numpy as np
import pandas as pd
import geopandas as gpd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.colors import Normalize
import mapas_microplasticos_teco as m
R=m.R;O=m.O;F=R/'entrega_final';D=F/'00_documentacao/Microplasticos';stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
TYPES={1:('Plastic processing / recycling','#b74e78','D'),2:('Refining / chemical industry','#d19e45','o'),3:('Metal / vehicle manufacturing','#7e7caf','o'),4:('Waste / wastewater treatment','#589c87','s'),5:('Fuel handling / transport','#8c9b9e','^'),6:('Other activities / infrastructure','#9cbcc8','o')}
LINKS={0:('No specific link in main activity','#bcc7c8'),1:('Plastic material explicitly reported','#b74e78'),2:('Possible process: verify details','#d7aa58'),3:('Waste / effluent management','#589c87')}
DICTIONARY=[]

# Agrupamento documental
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',str(s).lower()) if not unicodedata.combining(c))
def typology(s):
 s=norm(s)
 if any(v in s for v in ['plastic','termoplastic','polimero','borracha','textil','lavander']):return 1
 if any(v in s for v in ['incinera','tratamento de esgoto','tratamento de residuos']):return 4
 if any(v in s for v in ['molas','estamparia','fundidos','metal','fabricacao de pecas','fabricacao de veiculos']):return 3
 if any(v in s for v in ['refino de petroleo','produtos quimicos','substancias quimicas']):return 2
 if any(v in s for v in ['combustive','lubrificant','gas liquefeito','transporte rodoviario']):return 5
 return 6
def archive(p):
 if p.exists():
  dest=R/'descontinuado'/stamp/'intermediarios_microplasticos'/p.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(p),str(dest))
def shp(g,folder,name,fields):
 p=F/folder;archive(p);p.mkdir(parents=True,exist_ok=True);x=g[list(fields)+['geometry']].copy();x.rename(columns={k:v[0] for k,v in fields.items()},inplace=True)
 for c in x.select_dtypes(include=['object','str']).columns:
  if c!='geometry':x[c]=x[c].map(lambda v:v[:250] if isinstance(v,str) else v)
 target=p/(name+'.shp');x.to_file(target,driver='ESRI Shapefile',encoding='UTF-8')
 rows=[{'arquivo':str(target.relative_to(F)).replace('\\','/'),'campo_shp':short,'campo_original':field,'descricao':desc,'unidade':unit,'natureza':'triagem documental / derivado','fonte_camada':'output/07_microplasticos/microplasticos.gpkg','script_python':'05_scripts/python/mapas_intermediarios_microplasticos.py','linha_referencia':'','trecho_referencia':field,'scripts_apoio':'05_scripts/python/mapas_microplasticos_teco.py'} for field,(short,desc,unit) in fields.items()]
 pd.DataFrame(rows).to_csv(p/'campos.csv',sep=';',index=False,encoding='utf-8-sig');DICTIONARY.extend(rows)

# Camadas intermediárias
def prepare():
 lic=m.lic.copy();lic['TP_CODE']=lic.ACTIVITY.map(typology);lic['TP_NAME']=lic.TP_CODE.map(lambda t:TYPES[t][0]);lic['MP_LINK']=lic.TP_CODE.map({1:1,2:2,3:2,4:3,5:0,6:0});lic['MP_ROUTE']=lic.MP_LINK.map(lambda x:LINKS[x][0])
 lic.to_file(m.G,layer='licensing_typology',driver='GPKG')
 fields={'REC_ID':('REC_ID','Identificador genérico do registro, sem identificação pessoal.','código'),'BACIA':('BACIA','Bacia intersectada pelo registro.','código'),'SOURCE':('SOURCE','SLA ou histórico estadual; não confirma operação atual.','cadastro'),'PROCESS':('PROCESS','Número público do processo; pode haver mais de um processo por empreendimento.','identificador'),'ACTIVITY':('ACTIVITY','Descrição da atividade principal; texto completo na tabela CSV.','texto'),'TP_CODE':('TP_CODE','1 plásticos; 2 refino/química; 3 metal/veículos; 4 resíduos/esgoto; 5 combustíveis/transporte; 6 outros/infraestrutura.','categoria'),'TP_NAME':('TP_NAME','Família de atividade principal para a leitura do mapa.','texto'),'MP_LINK':('MP_LINK','1 material plástico explícito; 2 processo possível a verificar; 3 manejo de resíduos/efluentes; 0 vínculo específico não identificado. Não é grau de emissão.','categoria'),'MP_ROUTE':('MP_ROUTE','Significado do vínculo documental, sem intensidade ou probabilidade atribuída.','texto')}
 shp(lic,'01_entradas/19_licenciamento/02_tipologias','lic_typology',fields);lic.drop(columns='geometry').to_csv(O/'tabelas/licencas_por_tipologia.csv',sep=';',index=False,encoding='utf-8-sig')
 rows=[]
 for r in m.b.itertuples():
  for _,q in lic[lic.BACIA.str.contains(r.id,na=False)].iterrows():rows.append({'BACIA':r.id,'TP_CODE':q.TP_CODE,'TP_NAME':q.TP_NAME,'REC_ID':q.REC_ID})
 counts=pd.DataFrame(rows).groupby(['BACIA','TP_CODE','TP_NAME']).size().reset_index(name='RECORDS');counts.to_csv(O/'tabelas/contagem_tipologias_bacias.csv',sep=';',index=False,encoding='utf-8-sig')
 plans=gpd.read_file(m.G,layer='municipal_waste_plans');plans=gpd.overlay(plans,m.b[['id','geometry']],how='intersection',keep_geom_type=True).rename(columns={'id':'BACIA'});plans['COLLECT']=plans.colsel_24.map({'Sim':1,'Não':0}).fillna(-1).astype(int);plans['PLAN']=plans.pmgirs_24.map({'Sim':1,'Não':0}).fillna(-1).astype(int)
 common={'BACIA':('BACIA','Bacia do fragmento municipal; indicador se refere ao município inteiro.','código'),'nome':('MUNICIPAL','Município da declaração administrativa.','texto'),'geocodigo':('MUN_CODE','Código IBGE do município.','código')}
 shp(plans,'01_entradas/18_residuos/04_destinos','destinations',{**common,'tiprsu_24':('DEST_2024','Tipologia municipal de destinação informada em 2024; não é rastreio do resíduo de cada bairro.','cadastro 2024')})
 shp(plans,'01_entradas/18_residuos/05_coleta','selective',{**common,'COLLECT':('COLLECT','1 coleta seletiva declarada; 0 não; -1 sem dado. Não informa percentual de cobertura.','cadastro 2024')})
 shp(plans,'01_entradas/18_residuos/06_planos','waste_plan',{**common,'PLAN':('PLAN','1 plano municipal declarado; 0 não; -1 sem dado. Não avalia implementação.','cadastro 2024')})
 w=m.waste.copy();w['WASTE_UNC']=w.WASTE_HI-w.WASTE_LO;vals=w[[f'V{i:05d}' for i in range(399,403)]].apply(pd.to_numeric,errors='coerce');complete=vals.notna().all(axis=1);w['DOM_DEST']=-1;w.loc[complete,'DOM_DEST']=np.where(vals[complete].sum(axis=1)==0,0,vals[complete].to_numpy().argmax(axis=1)+1)
 w.to_file(m.G,layer='waste_intermediate',driver='GPKG');shp(w,'01_entradas/18_residuos/07_lixo_intermediario','waste_detail',{'setor_id':('SECTOR_ID','Setor censitário Censo 2022.','código'),'BACIA':('BACIA','Bacia do recorte do setor.','código'),'WASTE_UNC':('WASTE_UNC','Diferença entre os limites superior e inferior do percentual sem coleta; não é erro amostral.','pontos percentuais'),'DOM_DEST':('DOM_DEST','Destino mais frequente entre as quatro categorias sem coleta conhecidas: 1 queima; 2 enterra; 3 terreno/encosta/área pública; 4 outro; 0 nenhuma reportada; -1 incompleto/sigiloso. Empate resolvido pela ordem das categorias.','categoria'),'WASTE_QA':('WASTE_QA','Qualidade e condição da estimativa censitária.','categoria')})
 pd.DataFrame(DICTIONARY).to_csv(D/'Dicionario_intermediarios.csv',sep=';',index=False,encoding='utf-8-sig')
 return lic,plans,w,counts

# Mapas das atividades
def licensed(lic,field,title,key,groups):
 fig,axes=m.start(title)
 for ax,r in zip(axes,m.b.itertuples()):
  sub=lic[lic.BACIA.str.contains(r.id,na=False)]
  for value,entry in groups.items():
   label,col,*marker=entry;g=sub[sub[field]==value]
   if len(g):g.plot(ax=ax,color=col,edgecolor='white',linewidth=.45,marker=marker[0] if marker else 'o',markersize=34 if value==1 else 25,zorder=12)
 m.finish(fig,axes,key,title,handles=[Line2D([],[],linestyle='',marker=e[2] if len(e)>2 else 'o',color=e[1],label=e[0]) for e in groups.values()])
def municipal(plans,field,title,key,groups,facilities=False):
 fig,axes=m.start(title)
 for ax,r in zip(axes,m.b.itertuples()):
  sub=plans[plans.BACIA==r.id]
  for value,(label,col) in groups.items():
   g=sub[sub[field]==value]
   if len(g):g.plot(ax=ax,facecolor=col,edgecolor='#667d7c',linewidth=.45,zorder=2)
  if facilities:
   frame=m.box(ax.get_xlim()[0],ax.get_ylim()[0],ax.get_xlim()[1],ax.get_ylim()[1]);g=m.fac[m.fac.intersects(frame)]
   for typ,marker,col in [('aterros_sanitarios','s','#8f5072'),('transbordo','^','#c38e42')]:
    if len(g[g.TYPE==typ]):g[g.TYPE==typ].plot(ax=ax,marker=marker,color=col,edgecolor='white',markersize=38,zorder=12)
 handles=[Patch(facecolor=col,edgecolor='#667d7c',label=label) for label,col in groups.values()]
 if facilities:handles +=[Line2D([],[],linestyle='',marker='s',color='#8f5072',label='Landfill: cadastral location'),Line2D([],[],linestyle='',marker='^',color='#c38e42',label='Transfer station: cadastral location')]
 m.finish(fig,axes,key,title,handles=handles)

# Execução e integração
def main():
 lic,plans,w,counts=prepare();m.gallery=[]
 licensed(lic,'TP_CODE','Licensed activity records · source-related typologies','14_licensed_typologies',TYPES)
 licensed(lic,'MP_LINK','Licensed activities · documentary link to microplastics','15_licensed_linkage',LINKS)
 destinations={v:('Regulated landfill: municipal declaration','#a8c7bc') for v in plans.tiprsu_24.dropna().unique()};municipal(plans,'tiprsu_24','Solid-waste destination and registered facilities','16_waste_destinations',destinations,True)
 categories={1:('Declared yes','#86b5ac'),0:('Declared no','#d7b076'),-1:('No information','#d5dcda')}
 municipal(plans,'COLLECT','Selective collection · municipal declaration, 2024','17_selective_collection',categories)
 municipal(plans,'PLAN','Municipal solid-waste management plan · 2024','18_waste_plans',categories)
 fig,axes=m.start('Waste collection deficit · uncertainty from confidential counts')
 for ax,r in zip(axes,m.b.itertuples()):w[w.BACIA==r.id].plot(ax=ax,column='WASTE_UNC',cmap=m.CM,vmin=0,vmax=100,edgecolor='#687c77',linewidth=.12,missing_kwds={'color':'#d5dcda'},zorder=2)
 m.finish(fig,axes,'19_waste_uncertainty','Waste collection deficit · uncertainty from confidential counts',bar=(m.CM,Normalize(0,100),'Upper minus lower bound (percentage points)'))
 fig,axes=m.start('Uncollected household waste · predominant reported destination')
 groups={-1:('Confidential / incomplete','#cdd5d2'),0:('None reported','#eef0e9'),1:('Burned on property','#c98460'),2:('Buried on property','#b7a16d'),3:('Open land / slope / public space','#b15c76'),4:('Other destination','#7ba5ac')}
 for ax,r in zip(axes,m.b.itertuples()):
  sub=w[w.BACIA==r.id]
  for value,(label,col) in groups.items():
   if len(sub[sub.DOM_DEST==value]):sub[sub.DOM_DEST==value].plot(ax=ax,facecolor=col,edgecolor='#718079',linewidth=.12,zorder=2)
 m.finish(fig,axes,'20_waste_pathways','Uncollected household waste · predominant reported destination',handles=[Patch(facecolor=c,edgecolor='#718079',label=l) for l,c in groups.values()])
 gallery=json.loads((m.F/'galeria.json').read_text('utf8'));new={x['id'] for x in m.gallery};gallery=[x for x in gallery if x['id'] not in new]+m.gallery;(m.F/'galeria.json').write_text(json.dumps(gallery,ensure_ascii=False,indent=2),encoding='utf8')
 target=F/'03_mapas/14_microplasticos'
 for item in m.gallery:
  for ext in ['png','svg']:shutil.copy2(m.F/(item['id']+'.'+ext),target/(item['id']+'.'+ext))
 shutil.copy2(m.F/'galeria.json',target/'galeria.json');shutil.copy2(Path(__file__),F/'05_scripts/python'/Path(__file__).name)
 info={'new_maps':len(m.gallery),'licensed_records':len(lic),'explicit_plastic_records':int((lic.MP_LINK==1).sum()),'typology_counts':counts.to_dict('records'),'no_index_recalculation':True,'no_inferred_waste_transport_routes':True};(D/'Intermediarios_licenciamento_residuos.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'maps':len(m.gallery),'records':len(lic)},ensure_ascii=True),flush=True)
if __name__=='__main__':main()
