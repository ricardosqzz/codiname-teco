# ENTRADAS: entrega_final/01_entradas/18_residuos,19_licenciamento; 02_saidas/06_microplasticos; projeto_teco.qgz e TECO_Consolidado.qgz.
# CAMPOS: MP_INDEX, MP_CLASS, MP_K, MP_MORAN, MP_STAB; BACIA filtra os três reservatórios.
# SAÍDAS: grupo Microplastics e seis layouts triplos em cada QGZ; estilos, nomes curtos, definições de campo e auditoria de validade.
# CAMINHOS: TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json; executar no Python do QGIS.
from pathlib import Path
import os,json,datetime,shutil,sys
os.environ['QT_QPA_PLATFORM']='offscreen'
from qgis.core import *
from qgis.PyQt.QtGui import QColor,QFontDatabase,QFont
from qgis.PyQt.QtCore import Qt
from caminhos_teco import raiz_projeto
R=raiz_projeto();F=R/'entrega_final';P=F/'02_saidas/06_microplasticos/01_consolidado/microplastics.shp'
app=QgsApplication([],False);app.initQgis();STAMP=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
for fontfile in ['arial.ttf','arialbd.ttf','ariali.ttf','arialbi.ttf','calibri.ttf']:
 p=Path('C:/Windows/Fonts')/fontfile
 if p.exists():QFontDatabase.addApplicationFont(str(p))
PAL=['#a8d9e6','#68b7a0','#e2d17d','#df995c','#b94854'];names={'pampulha':'Pampulha','vargem_flores':'Vargem das Flores','ibirite_regap':'Ibirité / REGAP'}
specs=[('MP_INDEX','Microplastic pressure','continuous'),('MP_CLASS','Score classes','classes'),('MP_QUINT','Relative quintiles','quintiles'),('MP_K','Source profiles','profiles'),('MP_MORAN','Local Moran','moran'),('MP_STAB','Weight sensitivity','continuous')]

# Renderizadores e metadados
def vector(project,group,path,name,field=None,kind=None,basin=None):
 layer=QgsVectorLayer(str(path),name,'ogr')
 if not layer.isValid():raise ValueError(str(path))
 if basin:layer.setSubsetString('"BACIA"=\''+basin+'\'')
 if kind=='continuous':
  ranges=[]
  for i,col in enumerate(PAL):
   symbol=QgsFillSymbol.createSimple({'color':col,'outline_color':'#61746b','outline_width':'0.08'});ranges.append(QgsRendererRange(i*20,(i+1)*20,symbol,f'{i*20}–{(i+1)*20}'))
  layer.setRenderer(QgsGraduatedSymbolRenderer(field,ranges))
  renderer=QgsRuleBasedRenderer.convertFromRenderer(layer.renderer());renderer.rootRule().appendChild(QgsRuleBasedRenderer.Rule(QgsFillSymbol.createSimple({'color':'#dbe1dd','outline_color':'#61746b','outline_width':'0.08'}),filterExp='"'+field+'" IS NULL',label='Insufficient inputs'));layer.setRenderer(renderer)
 elif kind in ['classes','profiles','moran','quintiles']:
  if kind=='quintiles':
   vals={0:('Insufficient inputs','#dbe1dd'),**{i+1:(label,PAL[i]) for i,label in enumerate(['≤P20','>P20–P40','>P40–P60','>P60–P80','>P80'])}}
  else:
   vals={'classes':{0:('Insufficient inputs','#dbe1dd'),**{i+1:(v,PAL[i]) for i,v in enumerate(['Very low','Low','Moderate','High','Very high'])}},'profiles':{0:('Insufficient inputs','#dbe1dd'),1:('Profile 1','#72b8bb'),2:('Profile 2','#cd7866')},'moran':{'HH':('High–high','#bf555b'),'LL':('Low–low','#5b91b2'),'HL':('High–low','#e4b278'),'LH':('Low–high','#a5ced3'),'NS':('Not significant','#dfe5de'),'ND':('Insufficient inputs','#c2c8c5')}}[kind]
  cats=[QgsRendererCategory(v,QgsFillSymbol.createSimple({'color':color,'outline_color':'#61746b','outline_width':'0.08'}),label) for v,(label,color) in vals.items()];layer.setRenderer(QgsCategorizedSymbolRenderer(field,cats))
 elif field=='WASTE_PCT':
  ranges=[QgsRendererRange(i*20,(i+1)*20,QgsFillSymbol.createSimple({'color':col,'outline_color':'#61746b','outline_width':'0.07'}),f'{i*20}–{(i+1)*20}%') for i,col in enumerate(PAL)];layer.setRenderer(QgsGraduatedSymbolRenderer(field,ranges))
 elif layer.geometryType()==QgsWkbTypes.PointGeometry:
  if 'licens' in name.lower():
   cats=[QgsRendererCategory(v,QgsMarkerSymbol.createSimple({'name':'diamond' if v else 'circle','color':c,'outline_color':'white','size':'2.4' if v else '1.7'}),label) for v,c,label in [(0,'#b1aeb3','Other activity'),(1,'#b84969','Plastic-related activity: verify')]];layer.setRenderer(QgsCategorizedSymbolRenderer('MP_CAND',cats))
  else:layer.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name':'square','color':'#6c8773','outline_color':'white','size':'2.4'}))
 project.addMapLayer(layer,False);group.addLayer(layer)
 metadata=layer.metadata();metadata.setAbstract('Exploratory source-pressure assessment. Not occurrence, concentration, probability or verified discharge. See Microplastic assessment report and field dictionary.');layer.setMetadata(metadata)
 return layer

# Legendas específicas dos novos layouts
def legend(layout,field,title):
 for item in list(layout.items()):
  if isinstance(item,(QgsLayoutItemLabel,QgsLayoutItemLegend)) and item.positionWithUnits().y()>=105:layout.removeLayoutItem(item)
 if field=='MP_K':items=[('Profile 1','#72b8bb'),('Profile 2','#cd7866'),('Insufficient inputs','#dbe1dd')]
 elif field=='MP_MORAN':items=[('High–high','#bf555b'),('Low–low','#5b91b2'),('High–low','#e4b278'),('Low–high','#a5ced3'),('Not significant','#dfe5de'),('Insufficient inputs','#c2c8c5')]
 elif field=='MP_QUINT':items=list(zip(['≤P20','>P20–P40','>P40–P60','>P60–P80','>P80'],PAL))+[('Insufficient inputs','#dbe1dd')]
 else:items=list(zip(['0–20','>20–40','>40–60','>60–80','>80–100'],PAL))+[('Insufficient inputs','#dbe1dd')]
 head=QgsLayoutItemLabel(layout);head.setText(title+(' (agreement, %)' if field=='MP_STAB' else ' (index 0–100)' if field in ['MP_INDEX','MP_CLASS'] else ''));head.setFont(QFont('Arial',7));head.setHAlign(Qt.AlignHCenter);head.attemptMove(QgsLayoutPoint(15,106));head.attemptResize(QgsLayoutSize(276,5));layout.addLayoutItem(head)
 for row in range((len(items)+2)//3):
  parts=items[row*3:row*3+3];start=(300-76*len(parts))/2
  for col,(text,color) in enumerate(parts):
   x=start+76*col;y=113+row*5.5;swatch=QgsLayoutItemLabel(layout);swatch.setText('');swatch.setBackgroundEnabled(True);swatch.setBackgroundColor(QColor(color));swatch.attemptMove(QgsLayoutPoint(x,y+1));swatch.attemptResize(QgsLayoutSize(3,1.8));layout.addLayoutItem(swatch)
   label=QgsLayoutItemLabel(layout);label.setText(text);label.setFont(QFont('Arial',7));label.attemptMove(QgsLayoutPoint(x+4,y));label.attemptResize(QgsLayoutSize(70,4.5));layout.addLayoutItem(label)

# Integração preservando os projetos atuais
def main():
 reports=[]
 for target in [R/'projeto_teco.qgz',F/'TECO_Consolidado.qgz']:
  backup=R/'descontinuado'/STAMP/'qgis_antes_microplasticos'/target.name;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,backup)
  project=QgsProject();assert project.read(str(target));root=project.layerTreeRoot();old=root.findGroup('Microplastics')
  if old:
   ids=[n.layerId() for n in old.findLayers()];root.removeChildNode(old)
   for i in ids:project.removeMapLayer(i)
  grp=root.insertGroup(0,'Microplastics');grp.setExpanded(True);inputs=grp.addGroup('Inputs');allg=grp.addGroup('All basins');per={k:grp.addGroup(v) for k,v in names.items()};terrain=grp.addGroup('Topographic pathways')
  for path,name,field in [(F/'01_entradas/18_residuos/01_destino_lixo/waste_census.shp','Waste collection | census','WASTE_PCT'),(F/'01_entradas/19_licenciamento/01_triagem/licensing.shp','Licensing | process screening',None),(F/'01_entradas/18_residuos/02_instalacoes/waste_fac.shp','Waste facilities | context',None),(F/'01_entradas/18_residuos/03_planos/waste_plans.shp','Municipal waste plans | 2024',None)]:vector(project,inputs,path,name,field)
  outputs={}
  for field,name,kind in specs:
   outputs[field]=vector(project,allg,P,name,field,kind)
   for basin,sub in per.items():outputs[field,basin]=vector(project,sub,P,name,field,kind,basin)
  for basin in names:
   for suffix,title in [('upstream_pressure','Mean upstream pressure'),('contributing_km2','Contributing area km²')]:
    p=F/f'02_saidas/06_microplasticos/04_conectividade/{basin}_{suffix}.tif';rl=QgsRasterLayer(str(p),title+' | '+names[basin]);assert rl.isValid();project.addMapLayer(rl,False);terrain.addLayer(rl)
    shader=QgsColorRampShader();shader.setColorRampType(QgsColorRampShader.Interpolated)
    maximum=100 if suffix=='upstream_pressure' else rl.dataProvider().bandStatistics(1).maximumValue
    shader.setColorRampItemList([QgsColorRampShader.ColorRampItem(i*maximum/4,QColor(c),str(round(i*maximum/4,1))) for i,c in enumerate(PAL)])
    rs=QgsRasterShader();rs.setRasterShaderFunction(shader);rl.setRenderer(QgsSingleBandPseudoColorRenderer(rl.dataProvider(),1,rs))
  dictionary=json.loads((F/'00_documentacao/Microplasticos/Dicionario_QGIS.json').read_text('utf8'))
  for layer in project.mapLayers().values():
   if isinstance(layer,QgsVectorLayer) and 'microplastic' in layer.source().lower():
    for i,f in enumerate(layer.fields()):
     if f.name() in dictionary:layer.setFieldAlias(i,f.name().replace('_',' '));layer.setCustomProperty('fieldDescription/'+f.name(),dictionary[f.name()])
  manager=project.layoutManager();template=manager.layoutByName('Index S0');created=[]
  if template:
   for field,title,kind in specs:
    name='MP | '+title;oldlayout=manager.layoutByName(name)
    if oldlayout:manager.removeLayout(oldlayout)
    layout=manager.duplicateLayout(template,name)
    for item in layout.items():
     if isinstance(item,QgsLayoutItemMap):
      stack=item.layers();new=[];replaced=False
      for lyr in stack:
       source=lyr.source().lower();lname=lyr.name().lower()
       if lname=='s0' or any(v in lname for v in ['index s0','s0 index','multivariate','multivari','index |','base index']) or 'teco_final.shp' in source or 'weighted_index.shp' in source:
        basin=next((k for k in names if k in source or k in lyr.subsetString()),None)
        if not replaced:new.append(outputs.get((field,basin),outputs[field]));replaced=True
       else:new.append(lyr)
      if not replaced:new.append(outputs[field])
      item.setLayers(new);item.setKeepLayerSet(True);item.refresh()
     elif isinstance(item,QgsLayoutItemLegend):
      item.setAutoUpdateModel(False);item.model().rootGroup().clear();item.model().rootGroup().addLayer(outputs[field]);item.setTitle(title);item.adjustBoxSize()
     elif isinstance(item,QgsLayoutItemLabel):
      text=item.text()
      if 'S0' in text or 'Multivariate' in text or 'multivari' in text:item.setText(title)
    legend(layout,field,title);created.append(name)
  for sub in [inputs,allg,terrain,*per.values()]:sub.setExpanded(False)
  project.setFilePathStorage(Qgis.FilePathType.Relative);assert project.write(str(target));reports.append({'project':str(target),'new_layouts':created,'microplastic_layers':len(grp.findLayers()),'invalid_layers':[l.name() for l in project.mapLayers().values() if not l.isValid()]})
  if target==R/'projeto_teco.qgz':
   layout=manager.layoutByName('MP | Microplastic pressure');settings=QgsLayoutExporter.ImageExportSettings();settings.dpi=160;out=R/'temp/microplasticos/qgis_pressure.png';assert QgsLayoutExporter(layout).exportToImage(str(out),settings)==QgsLayoutExporter.Success
 (F/'00_documentacao/Microplasticos/Conferencia_QGIS.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(reports,ensure_ascii=True))
if __name__=='__main__':main()
