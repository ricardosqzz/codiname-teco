# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/config/encartes_teco.json | .read_text.
# Entrada: E:/teco/output/04_grade_500m/teco_grade_500m.gpkg | gpd.read_file | camada='centros_500m'.
# Entrada: E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg | gpd.read_file | camada='rotas_d8_candidatas'.
# Entrada: E:/teco/reservatorio/{key}.shp | gpd.read_file.
# Entrada: E:/teco/vias/malha_viaria.shp | gpd.read_file.
# Entrada: E:/teco/teco_base/mg_mun/ide_1103_mg_municipios_pol.shp | gpd.read_file.
# Entrada: E:/teco/codigo/figuras_multivariada_teco.py | .read_text.
# Entrada: E:/teco/output/02_avaliacao_espacial/rasters/{r.id}_{suffix}.tif | rasterio.open.
# Entrada: E:/teco/teco_base/uso_terra/uso_terra-reservatorio.tif | rasterio.open.
# Entrada: E:/teco/output/02_avaliacao_espacial/rasters/{r.id}_declividade_embrapa.tif | rasterio.open.
# Entrada: E:/teco/output/04_grade_500m/auditoria/metodo_grade.json | .read_text.
# Entrada: E:/teco/output/04_grade_500m/rasters/{r.id}_{suffix}.tif | rasterio.open.
# Campos/chaves em .loc: ibirite_regap, pampulha, vargem_flores.
# Campos/chaves em kwargs: bar.
# Campos/chaves em census: BACIA.
# Campos/chaves em health: AIH_ANO, BACIA.
# Campos/chaves em meta: cenarios.
# Campos/chaves em circ: BACIA.
# Campos/chaves em route: bacia.
# Saída: E:/teco/output/04_grade_500m/teco_grade_500m.gpkg | roads.to_file.
# Saída: E:/teco/output/04_grade_500m/teco_grade_500m.gpkg | .to_file.
# Saída: E:/teco/output/04_grade_500m/auditoria/galeria_mapas.json | .write_text.
# Campos/chaves gerados em roads: TIPO_VIA.
# Campos/chaves gerados em kwargs: bar, waterdraw.
# Campos/chaves gerados em a: QUINTIL.
# Campos/chaves gerados em av: QUINTIL.
# Campos/chaves gerados em hh: BACIA.
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
import ast,json,math
import numpy as np,pandas as pd,geopandas as gpd,rasterio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize,LinearSegmentedColormap,ListedColormap,BoundaryNorm
from matplotlib.patches import Patch,Rectangle
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
from pyproj import Transformer
from shapely.geometry import box
from rasterio.windows import from_bounds
from rasterio.features import rasterize
from paleta_hipsometria_teco import colormap as hipso_colormap
from idioma_cartografico_teco import en
R=Path(_cp_texto('', 'posix'));O=R/'output/04_grade_500m';B=R/'output/02_avaliacao_espacial';G=O/'teco_grade_500m.gpkg'
MAP_VIEWS=json.loads((R/'config/encartes_teco.json').read_text('utf8')) if (R/'config/encartes_teco.json').exists() else {}
plt.rcParams.update({'font.family':'Arial','font.size':9,'svg.fonttype':'none','axes.titleweight':'bold'})
a=gpd.read_file(G,layer='grade_resultados').rename(columns={'BACIA':'bas_id'});av=a.copy();u=a
b=gpd.read_file(B/'teco_avaliacao.gpkg',layer='bacias_estudo').set_index('id').loc[['pampulha','vargem_flores','ibirite_regap']].reset_index()
water=gpd.GeoDataFrame(pd.concat([gpd.read_file(R/'reservatorio'/f'{key}.shp').to_crs(31983) for key in b.id],ignore_index=True),crs=31983)
hyd=gpd.read_file(B/'teco_avaliacao.gpkg',layer='hidrografia_bacias');roads=gpd.read_file(R/'vias/malha_viaria.shp').to_crs(31983)
hydclip={r.id:gpd.clip(hyd,r.geometry) for r in b.itertuples()}

# Roadtype
def roadtype(s):
 s=str(s).upper()
 if 'ARTERIAL PRIMARIA' in s or 'EXPRESSA' in s:return 'Principal'
 if 'ARTERIAL' in s or 'COLETORA' in s:return 'Secundária / coletora'
 if 'LOCAL' in s:return 'Local'
 return 'Sem classe cadastrada'
roads['TIPO_VIA']=roads.hier_legal.map(roadtype)
mun=gpd.read_file(R/'teco_base/mg_mun/ide_1103_mg_municipios_pol.shp',bbox=tuple(gpd.GeoSeries([box(*b.total_bounds)],crs=b.crs).to_crs(4326).total_bounds)).to_crs(31983)
mun=mun.iloc[:0]
names={'pampulha':'Pampulha','vargem_flores':'Vargem das Flores','ibirite_regap':'Ibirité / REGAP'};PAL=['#7198ad','#b8c99b','#dfb77b','#bc7d7d','#8c7ba4','#55a28e'];CM=LinearSegmentedColormap.from_list('teco_pressao',['#c8e7ef','#88bcb0','#e4d78d','#de9b66','#b94f58']);trans=Transformer.from_crs(31983,4326,always_xy=True);span=18225.;scale=225000;gallery=[]

base_source=(R/'codigo/figuras_multivariada_teco.py').read_text('utf8').replace('hyd[hyd.intersects(frame)]','hydclip[r.id]')

base_source=base_source.replace(".2f}°O'.replace('.',',')", ".2f}°W'").replace(".2f}°S'.replace('.',',')", ".2f}°S'")
base_source=base_source.replace("f'{v:,.0f}'.replace(',','.') if abs(v)>=100 else f'{v:.1f}'.rstrip('0').rstrip('.').replace('.',',')", "f'{v:,.0f}' if abs(v)>=100 else f'{v:.1f}'.rstrip('0').rstrip('.')")
_savefig=plt.Figure.savefig

# Savefig en
def _savefig_en(fig,*args,**kwargs):
 from matplotlib.text import Text
 for txt in fig.findobj(Text):
  value=en(txt.get_text())
  if value.startswith('Datum: SIRGAS 2000'):
   if 'Brentano' not in value:value+='\nBrentano, M. C. B.'
   txt.set_fontsize(5.1);txt.set_linespacing(1.05)
  txt.set_text(value)
 return _savefig(fig,*args,**kwargs)
plt.Figure.savefig=_savefig_en
tree=ast.parse(base_source);keep={'legend','legend_small','start','finish','continuous','categories'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in keep],type_ignores=[]),'<composicao_cartografica_teco>','exec'))

# Neat
def neat(t):return t.replace('de500m','de 500 m').replace('de500','de 500').replace('500m','500 m')
base_start=start

# Start
def start(title,sectors=True):return base_start(en(neat(title)),sectors)
original_finish=finish
ROAD_CACHE={}

# Drawroads
def drawroads(ax,r,foreground=False):
 if r.id not in ROAD_CACHE:
  x0,x1=ax.get_xlim();y0,y1=ax.get_ylim();frame=box(x0,y0,x1,y1);rr=roads[roads.intersects(frame)].copy();rr.geometry=rr.geometry.intersection(frame).simplify(2,preserve_topology=True);parts=rr.explode(index_parts=False);parts=parts[parts.geom_type=='LineString'];ROAD_CACHE[r.id]={cl:[np.asarray(x.coords) for x in parts.loc[parts.TIPO_VIA==cl].geometry] for cl in parts.TIPO_VIA.unique()}
 for cls,co,lw in [('Sem classe cadastrada','#b5b6b0',.16),('Local','#9caaa9',.21),('Secundária / coletora','#8f8274',.32),('Principal','#7a6b59',.48)]:
  segments=ROAD_CACHE[r.id].get(cls,[])
  if len(segments):ax.add_collection(LineCollection(segments,colors=co,linewidths=lw,zorder=6 if foreground else .8,alpha=.80))

# Finish
def finish(fig,axs,*args,**kwargs):
 for ax,r in zip(axs,b.itertuples()):
  drawroads(ax,r,True)
  ww=water[water.intersects(r.geometry)]
  ww.boundary.plot(ax=ax,color='white',lw=2.0,zorder=10)
  ww.plot(ax=ax,color='#45a8cf',edgecolor='#155777',lw=.85,zorder=11)
 kwargs['waterdraw']=False
 args=list(args)
 if len(args)>1:args[1]=neat(args[1])
 if kwargs.get('bar'):kwargs['bar']=(kwargs['bar'][0],en(neat(kwargs['bar'][1])))
 for h in kwargs.get('handles',[]) or []:h.set_label(en(neat(h.get_label())))
 return original_finish(fig,axs,*args,**kwargs)

# Cat
def cat(field,title,slug,labels,colors,group):
 if ready(slug,title,group):return
 fig,axs=start(title)
 for ax,r in zip(axs,b.itertuples()):
  gg=av[av.bas_id==r.id];gg.plot(ax=ax,color=gg[field].map(colors).fillna('#cbd0d0'),edgecolor='#71888b',lw=.12,zorder=2)
 finish(fig,axs,slug,title,group,handles=[Patch(color=colors[k],label=v) for k,v in labels.items()])

# Ready
def ready(slug,title,group):
 import xml.etree.ElementTree as ET
 try:
  path=O/'figuras'/f'{slug}.png'
  assert path.stat().st_size>1000 and path.stat().st_mtime >= max((O/'auditoria/metodo_grade.json').stat().st_mtime,Path(__file__).stat().st_mtime)
  ET.parse(O/'figuras'/f'{slug}.svg');gallery.append({'slug':slug,'titulo':title,'grupo':group});return True
 except Exception:return False
original_continuous=continuous;original_categories=categories

# Continuous
def continuous(field,title,name,group,*args,**kwargs):
 if not ready(name,title,group):original_continuous(field,title,name,group,*args,**kwargs)

# Categories
def categories(field,title,name,group):
 if not ready(name,title,group):original_categories(field,title,name,group)

# Number health
def number_health(axs,health):

 labels={'2191164':('1',(-14,16)),'2200473':('2',(14,-16)),'6892256':('3',(10,10))}
 for ax,r in zip(axs,b.itertuples()):
  for row in health[health.BACIA==r.id].itertuples():
   number,offset=labels[str(row.CNES)]
   ax.annotate(number,xy=(row.geometry.x,row.geometry.y),xytext=offset,textcoords='offset points',ha='center',va='center',fontsize=8,fontweight='bold',color='white',bbox=dict(boxstyle='circle,pad=.28',fc='#a83e59',ec='white',lw=.6),arrowprops=dict(arrowstyle='-',color='#633644',lw=.65,shrinkA=0,shrinkB=2),zorder=20)

# Native maps
def native_maps(fields=None,health_only=False):
 census=gpd.read_file(G,layer='entradas_censitarias_nativas');health=gpd.read_file(G,layer='saude_todos')
 for field,title,unit,hi in [('POP_OFIC','População censitária · setores de origem','Habitantes no setor completo de origem',None),('POP_REC','População no recorte censitário · estimativa por área','Habitantes estimados no recorte da bacia',None),('DENS_POP','Adensamento populacional · setores censitários','Habitantes/km²',None),('REDE_PCT','Ligação à rede · dado censitário observado','Domicílios com rede (%)',100),('SEM_REDE_OBS','Ausência de ligação à rede · dado observado','Domicílios sem rede (%)',100),('DESC_RIO','Destinação declarada em vala ou corpo hídrico','Domicílios com destinação em vala ou corpo hídrico (%)',100)]:
  if health_only:continue
  if fields and field not in fields:continue
  title=neat(title);fig,axs=start(title,sectors=False);upper=hi if hi else float(census[field].max());norm=Normalize(0,upper)
  for ax,r in zip(axs,b.itertuples()):
   cc=census[census.BACIA==r.id];cc.plot(ax=ax,column=field,cmap=CM,norm=norm,edgecolor='#526f77',lw=.12,zorder=2,missing_kwds={'color':'#cbd0d0','edgecolor':'#647b83','label':'Dado não publicado / ausente'})
  if census[field].isna().any():fig.legend(handles=[Patch(color='#cbd0d0',label='Dado não publicado / ausente')],loc='upper center',bbox_to_anchor=(.515,.19),frameon=False,fontsize=7)
  finish(fig,axs,'nativo_'+field,title,'Entradas na geometria de origem',bar=(plt.cm.ScalarMappable(norm=norm,cmap=CM),unit))
 if fields:return
 title='Estabelecimentos com internações confirmadas · localização nas bacias';fig,axs=start(title,sectors=False)
 types=[('Administrativo / móvel / outros','#7f8589','^',8),('Farmácia (cadastro CNES)','#558b62','s',8),('Outros serviços assistenciais','#9a7967','o',6),('Atenção básica','#765b93','o',11),('Urgência / pronto atendimento','#df9b48','D',15),('Hospital / hospital-dia','#b73857','P',22)]
 for ax,r in zip(axs,b.itertuples()):
  hh=health[health.BACIA==r.id]
  for kind,co,marker,size in types:
   sub=hh[hh.GRUPO==kind]
   if len(sub):sub.plot(ax=ax,color=co,marker=marker,markersize=size,edgecolor='white',lw=.22,zorder=15)
 number_health(axs,health)
 finish(fig,axs,'saude_todos',title,'Saúde e abrangência',handles=[Line2D([],[],marker='o',ls='',color='#a83e59',ms=4,label=label) for label in ['1 · CMI Contagem','2 · Hospital Municipal de Contagem','3 · Regional de Ibirité']])
 title='Internações por estabelecimento · filtro bacteriano e compatível';fig,axs=start(title,sectors=False);hi=float(health.AIH_ANO.max());norm=Normalize(0,hi)
 for ax,r in zip(axs,b.itertuples()):
  hh=health[health.BACIA==r.id];hh.plot(ax=ax,color='#858d91',markersize=3,edgecolor='white',lw=.1,zorder=14);v=hh[hh.AIH_ANO.notna()]
  if len(v):v.plot(ax=ax,column='AIH_ANO',cmap=CM,norm=norm,markersize=65,edgecolor='#253f49',lw=.5,zorder=16)
 number_health(axs,health)
 finish(fig,axs,'saude_internacoes_pontos',title,'Saúde e abrangência',bar=(plt.cm.ScalarMappable(norm=norm,cmap=CM),'Média anual de AIH selecionadas (2016-2025) · localização do hospital'))
 if health_only:return
 for slug,title,kind in [('vias_nativas','Malha viária · hierarquia cadastral','vias'),('hidrografia_nativa','Cursos hídricos e reservatórios','hidro')]:
  fig,axs=start(title,sectors=False)
  if kind=='hidro':
   for ax,r in zip(axs,b.itertuples()):hydclip[r.id].plot(ax=ax,color='#2783a8',lw=.55,zorder=9)
   handles=[Line2D([],[],color='#2783a8',label='Curso hídrico'),Patch(color='#45a8cf',ec='#155777',label='Reservatório')]
  else:handles=[Line2D([],[],color=co,lw=lw,label=la) for la,co,lw in [('Via principal','#7a6b59',1.2),('Via secundária / coletora','#8f8274',.8),('Via local','#9caaa9',.5),('Sem classe cadastrada','#b5b6b0',.4)]]
  finish(fig,axs,slug,title,'Entradas na geometria de origem',handles=handles)

# Relevo maps
def relevo_maps(suffixes=None):
 for suffix,title,label,cmap,lims in [('hipsometria','Hipsometria','Elevação (m)',hipso_colormap(),(780,1450)),('declividade_pct','Declividade','Declividade (%)','YlOrBr',(0,120)),('distancia_hidrologica_km','Distância superficial ao reservatório','Distância D8 (km)','YlGnBu',(0,20))]:
  if suffixes and suffix not in suffixes:continue
  fig,axs=start(title,sectors=False);norm=Normalize(*lims)
  for ax,r in zip(axs,b.itertuples()):
   with rasterio.open(B/'rasters'/f'{r.id}_{suffix}.tif') as d:ax.imshow(d.read(1,masked=True),extent=(d.bounds.left,d.bounds.right,d.bounds.bottom,d.bounds.top),cmap=cmap,norm=norm,zorder=2)
  finish(fig,axs,'relevo_'+suffix,title,'Relevo',bar=(plt.cm.ScalarMappable(norm=norm,cmap=cmap),label))

# Main
def main():
 native_maps()
 fig,axs=start('Uso e ocupação do solo · 2025 informado',sectors=False);codes={24:1,1:2,3:2,4:2,5:2,11:2,12:2,9:3,15:3,19:3,21:3,36:3,30:4,31:5,33:5,25:6,29:6};colors=['#d57c74','#6b9d78','#d6bd74','#9f88a3','#76b8d0','#c8c2b5']
 with rasterio.open(R/'teco_base/uso_terra/uso_terra-reservatorio.tif') as d:
  for ax,r in zip(axs,b.itertuples()):
   win=from_bounds(*r.geometry.bounds,d.transform).round_offsets().round_lengths();arr=d.read(1,window=win);t=d.window_transform(win);mapped=np.full(arr.shape,np.nan)
   for value,group in codes.items():mapped[arr==value]=group
   mask=rasterize([(r.geometry,1)],out_shape=arr.shape,transform=t).astype(bool);mapped[~mask]=np.nan;ax.imshow(mapped,extent=(t.c,t.c+arr.shape[1]*t.a,t.f+arr.shape[0]*t.e,t.f),cmap=ListedColormap(colors),norm=BoundaryNorm(np.arange(.5,7.5),6),zorder=2)
 finish(fig,axs,'uso_categorias_grade','Uso e ocupação do solo · 2025 informado','Entradas originais',handles=[Patch(color=co,label=la) for co,la in zip(colors,['Área urbanizada','Vegetação natural','Agropecuária / silvicultura','Mineração','Água / aquicultura','Outras superfícies'])])
 fig,axs=start('Declividade · classes Embrapa',sectors=False);colors=['#b7dce6','#a6cba0','#dfd28f','#dda168','#c17866','#946078']
 for ax,r in zip(axs,b.itertuples()):
  with rasterio.open(B/'rasters'/f'{r.id}_declividade_embrapa.tif') as d:ax.imshow(d.read(1,masked=True),extent=(d.bounds.left,d.bounds.right,d.bounds.bottom,d.bounds.top),cmap=ListedColormap(colors),norm=BoundaryNorm(np.arange(.5,7.5),6),zorder=2)
 finish(fig,axs,'declividade_embrapa_grade','Declividade · classes Embrapa','Relevo',handles=[Patch(color=co,label=la) for co,la in zip(colors,['Plano · 0-3%','Suave ondulado · 3-8%','Ondulado · 8-20%','Forte ondulado · 20-45%','Montanhoso · 45-75%','Escarpado · >75%'])])
 meta=json.loads((O/'auditoria/metodo_grade.json').read_text('utf8'))
 tierlabels={1:'Muito baixo',2:'Baixo',3:'Moderado',4:'Alto',5:'Muito alto',0:'Informação incompleta'};tiercolors=dict(zip(range(1,6),['#b7dce6','#8bbca9','#e0ce81','#d99965','#b94d5c']));tiercolors[0]='#cbd0d0'
 for code,(name,_) in meta['cenarios'].items():
  cat('F_'+code,'Potencial relativo exploratório · '+code,'faixas_'+code,tierlabels,tiercolors,'Classificação em cinco faixas')
  categories('K_'+code,'Perfis multivariados · '+code,'kmeans_'+code,'K-means')

 vals=a.I_S0;valid=vals.notna();a['QUINTIL']=0;a.loc[valid,'QUINTIL']=pd.qcut(vals[valid].rank(method='average'),5,labels=False,duplicates='drop')+1;av['QUINTIL']=a.QUINTIL
 cat('QUINTIL','Comparação por quintis · índice relativo local','quintis_grade',tierlabels,tiercolors,'Comparação percentílica')
 continuous('ESTABILIDADE','Estabilidade entre cenários de ponderação','estabilidade_grade','Sensibilidade','Cenários com o mesmo perfil (%)',100,cmap='YlGnBu')
 labels={'HH':'HH · alto próximo de alto','LL':'LL · baixo próximo de baixo','HL':'HL · alto próximo de baixo','LH':'LH · baixo próximo de alto','NS':'Associação não significativa','ND':'Informação não elegível','ISO':'Sem vizinho elegível'};colors={'HH':'#b23a4b','LL':'#5595b0','HL':'#e8ac79','LH':'#9b7daa','NS':'#e2e5df','ND':'#c1c7c6','ISO':'#faf9f3'};cat('MORAN','Associação espacial exploratória · Moran local','moran_grade',labels,colors,'Moran')
 relevo_maps()
 for suffix,title,label,hi in [('pressao_montante','Pressão territorial média a montante · cenário topológico','Média ponderada por área do índice S0 (0-100)',100),('area_montante_km2','Área válida contribuinte pelo terreno','Área a montante (km²)',80)]:
  fig,axs=start(title,sectors=False);norm=Normalize(0,hi)
  for ax,r in zip(axs,b.itertuples()):
   with rasterio.open(O/'rasters'/f'{r.id}_{suffix}.tif') as d:ax.imshow(d.read(1,masked=True),extent=(d.bounds.left,d.bounds.right,d.bounds.bottom,d.bounds.top),cmap=CM,norm=norm,zorder=2)
  finish(fig,axs,'rota_'+suffix,title,'Conectividade exploratória',bar=(plt.cm.ScalarMappable(norm=norm,cmap=CM),label))
 fig,axs=start('Grade de análise e vizinhanças de500m',sectors=False);circ=gpd.read_file(G,layer='influencia_500m');points=gpd.read_file(G,layer='centros_500m')
 for ax,r in zip(axs,b.itertuples()):
  av[av.bas_id==r.id].boundary.plot(ax=ax,color='#577a84',lw=.35,zorder=3);circ[circ.BACIA==r.id].boundary.plot(ax=ax,color='#b47b69',lw=.28,alpha=.5,zorder=4);points[points.intersects(r.geometry.buffer(500))].plot(ax=ax,color='#416d7c',markersize=2,zorder=6)
 finish(fig,axs,'grade_circulos','Grade de análise e vizinhanças de500m','Grade e contexto',handles=[Line2D([],[],color='#577a84',label='Célula de apresentação'),Line2D([],[],color='#b47b69',label='Raio de cálculo · 500m'),Line2D([],[],marker='o',ls='',color='#416d7c',ms=3,label='Centro da vizinhança')])
 fig,axs=start('Vias, cursos hídricos e trajetórias superficiais candidatas',sectors=False);route=gpd.read_file(B/'teco_avaliacao.gpkg',layer='rotas_d8_candidatas')
 for ax,r in zip(axs,b.itertuples()):route[route.bacia==r.id].plot(ax=ax,color='#348594',lw=.6,alpha=.65,zorder=5)
 finish(fig,axs,'vias_rotas_grade','Vias, cursos hídricos e trajetórias superficiais candidatas','Grade e contexto',handles=[Line2D([],[],color='#7a6b59',lw=1,label='Via principal'),Line2D([],[],color='#8f8274',label='Via secundária / coletora'),Line2D([],[],color='#9caaa9',label='Via local'),Line2D([],[],color='#b5b6b0',label='Via sem classe cadastrada'),Line2D([],[],color='#348594',label='Trajetória D8 candidata')])
 roads.to_file(G,layer='vias_contexto',driver='GPKG')
 hparts=[]
 for key,hh in hydclip.items():hh=hh.copy();hh['BACIA']=key;hparts.append(hh)
 gpd.GeoDataFrame(pd.concat(hparts,ignore_index=True),crs=31983).to_file(G,layer='hidro_contexto',driver='GPKG')
 (O/'auditoria/galeria_mapas.json').write_text(json.dumps(gallery,ensure_ascii=False,indent=2),encoding='utf8');print('ATLAS_GRADE',len(gallery),flush=True)
if __name__=='__main__':main()
