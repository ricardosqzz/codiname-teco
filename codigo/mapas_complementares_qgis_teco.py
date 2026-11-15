# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/entrega_final/01_entradas/13_relevo/{r.id}_conexao_lago.tif | rasterio.open.
# Entrada: E:/teco/entrega_final/01_entradas/11_pontos_coleta/pontos_coleta.shp | gpd.read_file.
# Entrada: E:/teco/entrega_final/00_documentacao/manifesto.json | .read_text.
# Campos/chaves em points: BACIA, COLETA_ID, MICRO.
# Campos/chaves em x: slug.
# Campos/chaves em m: mapas.
# Campos/chaves em row: grupo, slug.
# Saída: E:/teco/entrega_final/00_documentacao/manifesto.json | .write_text.
# Campos/chaves gerados em points: MICRO.
# Campos/chaves gerados em m: mapas.
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
import json,shutil
import numpy as np,geopandas as gpd,rasterio
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap,BoundaryNorm
from matplotlib.path import Path as MarkerPath
import mapas_grade_teco as cart
R=Path(_cp_texto('', 'posix'));F=R/'entrega_final';D=F/'00_documentacao';O=R/'output/04_grade_500m'
for field,title,slug in [('N_POP_DENS','Normalised population density','normalised_population'),('N_SEM_REDE','Normalised lack of sewer connection','normalised_no_sewer'),('N_AIH_LOCAL','Normalised local hospital activity','normalised_hospital')]:
 cart.continuous(field,title,slug,'Normalised inputs','Normalised value (0–1)',1)
fig,axs=cart.start('Surface connection to the reservoir',sectors=False)
for ax,r in zip(axs,cart.b.itertuples()):
 with rasterio.open(F/f'01_entradas/13_relevo/{r.id}_conexao_lago.tif') as ds:
  ax.imshow(ds.read(1,masked=True),extent=(ds.bounds.left,ds.bounds.right,ds.bounds.bottom,ds.bounds.top),cmap=ListedColormap(['#ddd7c6','#469e9d']),norm=BoundaryNorm([.5,1.5,2.5],2),zorder=2)
cart.finish(fig,axs,'surface_connection','Surface connection to the reservoir','Physical context',handles=[Patch(color='#ddd7c6',label='No surface path traced'),Patch(color='#469e9d',label='Surface path to reservoir')])
points=gpd.read_file(F/'01_entradas/11_pontos_coleta/pontos_coleta.shp');points['MICRO']=points.COLETA_ID.str.contains('microcosm',case=False,na=False)
drop_vertices=np.array([(50,5),(50,5),(14,48),(14,72),(14,94),(30,112),(50,112),(70,112),(86,94),(86,72),(86,48),(50,5),(50,5),(50,5)],float);drop_vertices[:,0]=(drop_vertices[:,0]-50)/55;drop_vertices[:,1]=(60-drop_vertices[:,1])/55;drop=MarkerPath(drop_vertices,[MarkerPath.MOVETO]+[MarkerPath.CURVE4]*12+[MarkerPath.CLOSEPOLY])
fig,axs=cart.start('Sampling sites and in situ microcosms',sectors=False)
for ax,r in zip(axs,cart.b.itertuples()):
 for micro,marker,color,size in [(False,drop,'#263d4c',25),(True,'D','#a04f85',33)]:
  q=points[points.BACIA.eq(r.id)&points.MICRO.eq(micro)]
  if len(q):q.plot(ax=ax,marker=marker,color=color,edgecolor='white',linewidth=.5,markersize=size,zorder=20)
cart.finish(fig,axs,'sampling_sites','Sampling sites and in situ microcosms','Sampling',handles=[Line2D([],[],marker=drop,ls='',color='#263d4c',label='Sampling point'),Line2D([],[],marker='D',ls='',color='#a04f85',label='In situ microcosm')])
m=json.loads((D/'manifesto.json').read_text('utf8'));slugs={x['slug'] for x in cart.gallery};m['mapas']=[x for x in m['mapas'] if x['slug'] not in slugs]
new=[]
for row in cart.gallery:
 folder='14_normalised' if row['grupo']=='Normalised inputs' else ('15_connection' if row['slug']=='surface_connection' else '16_sampling');base='03_mapas/'+folder+'/'+row['slug'];record={**row,'arquivo':base+'.png','vetorial':base+'.svg'}
 for key,ext in [('arquivo','png'),('vetorial','svg')]:
  path=F/record[key];path.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/'figuras'/f"{row['slug']}.{ext}",path)
 new.append(record)
m['mapas']+=new;(D/'manifesto.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8');print('New maps',len(new),'sampling',points.MICRO.value_counts().to_dict(),flush=True)
