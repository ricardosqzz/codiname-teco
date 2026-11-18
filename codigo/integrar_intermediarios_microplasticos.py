# ENTRADAS: shapefiles de tipologias licenciadas e resíduos em entrega_final/01_entradas/18_residuos e 19_licenciamento; layouts atuais dos dois projetos QGIS.
# CAMPOS: TP_CODE, MP_LINK, DEST_2024, COLLECT, PLAN, WASTE_UNC e DOM_DEST; BACIA filtra cada encarte.
# SAÍDAS: grupo Intermediate inputs e sete layouts triplos; auditoria em 00_documentacao/Microplasticos.
# CAMINHOS: TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json; usar Python do QGIS. Não altera índices ou agrupamentos.
from pathlib import Path
import os,json,datetime,shutil
os.environ['QT_QPA_PLATFORM']='offscreen'
from qgis.core import *
from qgis.PyQt.QtGui import QColor,QFont,QFontDatabase
from qgis.PyQt.QtCore import Qt
from caminhos_teco import raiz_projeto
R=raiz_projeto();F=R/'entrega_final';NAMES={'pampulha':'Pampulha','vargem_flores':'Vargem das Flores','ibirite_regap':'Ibirité / REGAP'}
SPECS=[
 ('Licensed typologies','19_licenciamento/02_tipologias/lic_typology.shp','TP_CODE',[(1,'Plastic processing / recycling','#b74e78'),(2,'Refining / chemicals','#d19e45'),(3,'Metal / vehicles','#7e7caf'),(4,'Waste / wastewater','#589c87'),(5,'Fuel / transport','#8c9b9e'),(6,'Other / infrastructure','#9cbcc8')]),
 ('Documentary source linkage','19_licenciamento/02_tipologias/lic_typology.shp','MP_LINK',[(0,'No specific link','#bcc7c8'),(1,'Plastic explicitly reported','#b74e78'),(2,'Process: verify details','#d7aa58'),(3,'Waste / effluent management','#589c87')]),
 ('Waste destination','18_residuos/04_destinos/destinations.shp','DEST_2024',[('AS Regularizado','Regulated landfill declaration','#a8c7bc')]),
 ('Selective collection','18_residuos/05_coleta/selective.shp','COLLECT',[(1,'Declared yes','#86b5ac'),(0,'Declared no','#d7b076'),(-1,'No information','#d5dcda')]),
 ('Municipal waste plans','18_residuos/06_planos/waste_plan.shp','PLAN',[(1,'Declared yes','#86b5ac'),(0,'Declared no','#d7b076'),(-1,'No information','#d5dcda')]),
 ('Waste uncertainty','18_residuos/07_lixo_intermediario/waste_detail.shp','WASTE_UNC',[(0,'0–20 pp','#a8d9e6'),(1,'>20–40 pp','#68b7a0'),(2,'>40–60 pp','#e2d17d'),(3,'>60–80 pp','#df995c'),(4,'>80–100 pp','#b94854')]),
 ('Uncollected waste pathways','18_residuos/07_lixo_intermediario/waste_detail.shp','DOM_DEST',[(-1,'Confidential / incomplete','#cdd5d2'),(0,'None reported','#eef0e9'),(1,'Burned','#c98460'),(2,'Buried','#b7a16d'),(3,'Open land / public space','#b15c76'),(4,'Other destination','#7ba5ac')])]

# Renderizadores
def layer(project,group,spec,basin=None):
 title,path,field,values=spec;lyr=QgsVectorLayer(str(F/'01_entradas'/path),title,'ogr');assert lyr.isValid(),path
 if basin:lyr.setSubsetString('"BACIA"=\''+basin+'\'')
 point=lyr.geometryType()==QgsWkbTypes.PointGeometry
 def symbol(c,v):return QgsMarkerSymbol.createSimple({'name':'diamond' if v==1 and field=='MP_LINK' or v==1 and field=='TP_CODE' else 'circle','size':'2.4','color':c,'outline_color':'white'}) if point else QgsFillSymbol.createSimple({'color':c,'outline_color':'#667d7c','outline_width':'0.08'})
 if field=='WASTE_UNC':
  ranges=[QgsRendererRange(v*20,(v+1)*20,symbol(c,v),label) for v,label,c in values];lyr.setRenderer(QgsGraduatedSymbolRenderer(field,ranges))
 else:lyr.setRenderer(QgsCategorizedSymbolRenderer(field,[QgsRendererCategory(v,symbol(c,v),label) for v,label,c in values]))
 project.addMapLayer(lyr,False);group.addLayer(lyr);return lyr

# Legendas e layouts
def add_layout(project,spec,all_layer,per):
 title,path,field,values=spec;manager=project.layoutManager();template=manager.layoutByName('Index S0')
 if not template:return
 name='Inputs | '+title;old=manager.layoutByName(name)
 if old:manager.removeLayout(old)
 layout=manager.duplicateLayout(template,name)
 for item in list(layout.items()):
  if isinstance(item,QgsLayoutItemMap):
   layers=[];found=False
   for lyr in item.layers():
    source=lyr.source();lname=lyr.name().lower()
    if lname=='s0' or 'weighted_index.shp' in source.lower() or 'teco_final.shp' in source.lower():
     basin=next((k for k in NAMES if k in source or k in lyr.subsetString()),None);layers.append(per.get(basin,all_layer));found=True
    else:layers.append(lyr)
   if not found:layers.append(all_layer)
   item.setLayers(layers);item.setKeepLayerSet(True);item.refresh()
  elif isinstance(item,(QgsLayoutItemLabel,QgsLayoutItemLegend)) and item.positionWithUnits().y()>=105:layout.removeLayoutItem(item)
  elif isinstance(item,QgsLayoutItemLabel) and ('S0' in item.text() or 'multivari' in item.text().lower()):item.setText(title)
 for row in range((len(values)+2)//3):
  cells=values[row*3:row*3+3];start=(300-76*len(cells))/2
  for col,(_,label,color) in enumerate(cells):
   x=start+76*col;y=111+row*6;sw=QgsLayoutItemLabel(layout);sw.setBackgroundEnabled(True);sw.setBackgroundColor(QColor(color));sw.attemptMove(QgsLayoutPoint(x,y+1));sw.attemptResize(QgsLayoutSize(3,1.8));layout.addLayoutItem(sw)
   tx=QgsLayoutItemLabel(layout);tx.setText(label);tx.setFont(QFont('Arial',7));tx.attemptMove(QgsLayoutPoint(x+4,y));tx.attemptResize(QgsLayoutSize(70,5));layout.addLayoutItem(tx)

# Integração reutilizável
def add_intermediates(project,parent):
 old=parent.findGroup('Intermediate inputs')
 if old:
  ids=[n.layerId() for n in old.findLayers()];parent.removeChildNode(old)
  for i in ids:project.removeMapLayer(i)
 group=parent.addGroup('Intermediate inputs');allg=group.addGroup('All basins');per={k:group.addGroup(v) for k,v in NAMES.items()}
 for spec in SPECS:
  all_layer=layer(project,allg,spec);basins={key:layer(project,sub,spec,key) for key,sub in per.items()};add_layout(project,spec,all_layer,basins)
 group.setExpanded(False);return len(group.findLayers())

# Execução nos projetos existentes
def main():
 rows=[];held=[];stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
 for target in [R/'projeto_teco.qgz',F/'TECO_Consolidado.qgz']:
  dest=R/'descontinuado'/stamp/'qgis_antes_intermediarios'/target.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,dest)
  print('PROJECT',str(target),flush=True);project=QgsProject();assert project.read(str(target));held.append(project);parent=project.layerTreeRoot().findGroup('Microplastics');assert parent is not None;n=add_intermediates(project,parent);project.setFilePathStorage(Qgis.FilePathType.Relative);assert project.write(str(target));invalid=[l.name() for l in project.mapLayers().values() if not l.isValid()];assert not invalid,invalid;rows.append({'project':str(target),'new_layers':n,'new_layouts':7,'invalid_layers':invalid});print('SAVED',n,flush=True)
 (F/'00_documentacao/Microplasticos/Conferencia_intermediarios_QGIS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(rows,ensure_ascii=True))
if __name__=='__main__':
 app=QgsApplication([],False);app.initQgis()
 for f in ['arial.ttf','arialbd.ttf']:QFontDatabase.addApplicationFont('C:/Windows/Fonts/'+f)
 main()
