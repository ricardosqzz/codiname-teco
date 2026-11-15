# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/output/04_grade_500m/teco_grade_500m.gpkg | gpd.read_file | camada='grade_resultados'.
# Entrada: E:/teco/sub_bacia/{key}/direcao_d8.tif | rasterio.open.
# Entrada: E:/teco/reservatorio/{key}.shp | gpd.read_file.
# Saída: E:/teco/output/04_grade_500m/rasters/{key}_{suffix}.tif | rasterio.open.
# Saída: E:/teco/output/04_grade_500m/tabelas/conectividade_montante.csv | .to_csv.
# Saída: E:/teco/output/04_grade_500m/auditoria/conectividade.json | .write_text.
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
from collections import deque
import json
import numpy as np,pandas as pd,geopandas as gpd,rasterio
from rasterio.features import rasterize
R=Path(_cp_texto('', 'posix'));O=R/'output/04_grade_500m';G=O/'teco_grade_500m.gpkg'
D8={1:(-1,1),2:(-1,0),3:(-1,-1),4:(0,-1),5:(1,-1),6:(1,0),7:(1,1),8:(0,1)}

# Main
def main():
 (O/'rasters').mkdir(exist_ok=True);a=gpd.read_file(G,layer='grade_resultados');rows=[]
 for key,g in a.groupby('BACIA'):
  with rasterio.open(R/'sub_bacia'/key/'direcao_d8.tif') as d:dr=d.read(1);t=d.transform;profile=d.profile
  h,w=dr.shape;n=h*w;lab=rasterize([(r.geometry,float(r.I_S0)) for r in g.itertuples() if np.isfinite(r.I_S0)],out_shape=(h,w),transform=t,fill=-9999,dtype='float32');valid=lab!=-9999
  lake=gpd.read_file(R/'reservatorio'/f'{key}.shp').to_crs(31983);lm=rasterize([(x,1) for x in lake.geometry],out_shape=(h,w),transform=t,dtype='uint8',all_touched=True).astype(bool)
  domain=valid|lm;dest=np.full(n,-1,dtype=np.int64)
  for code,(dy,dx) in D8.items():
   yy,xx=np.where((dr==code)&domain&~lm);ny=yy+dy;nx=xx+dx;ok=(ny>=0)&(ny<h)&(nx>=0)&(nx<w);src=yy[ok]*w+xx[ok];dst=ny[ok]*w+nx[ok];ok2=domain.ravel()[dst];dest[src[ok2]]=dst[ok2]
  area=np.where(valid&~lm,abs(t.a*t.e)/1e6,0).ravel();weighted=np.where(valid&~lm,lab,0).ravel()*area;indeg=np.bincount(dest[dest>=0],minlength=n);queue=deque(np.flatnonzero(domain.ravel()&(indeg==0)));processed=0
  while queue:
   j=queue.popleft();processed+=1;k=dest[j]
   if k>=0:
    area[k]+=area[j];weighted[k]+=weighted[j];indeg[k]-=1
    if indeg[k]==0:queue.append(k)
  mean=np.divide(weighted,area,out=np.full(n,np.nan),where=area>0).reshape(h,w);mean=np.where(domain,mean,np.nan);area=np.where(domain,area.reshape(h,w),np.nan)
  for suffix,x in [('pressao_montante',mean),('area_montante_km2',area)]:
   p=profile.copy();p.update(driver='GTiff',dtype='float32',count=1,nodata=-9999,compress='deflate')
   with rasterio.open(O/'rasters'/f'{key}_{suffix}.tif','w',**p) as d:d.write(np.where(np.isfinite(x),x,-9999).astype('float32'),1)
  rows.append({'bacia':key,'pixels_dominio':int(domain.sum()),'pixels_processados':processed,'pixels_ciclo':int((domain.ravel()&(indeg>0)).sum()),'max_area_montante_km2':float(np.nanmax(area))})
 pd.DataFrame(rows).to_csv(O/'tabelas/conectividade_montante.csv',index=False,sep=';',encoding='utf-8-sig');(O/'auditoria/conectividade.json').write_text(json.dumps({'metodo':'D8; soma de índice*área / soma de área válida a montante; células de água não geram pressão e encerram a trajetória. Não há atenuação ou vazão. Índice S0 LOCAL exploratório, não emissões.','verificacao':rows},ensure_ascii=False,indent=2),encoding='utf8');print('CONECTIVIDADE',rows,flush=True)
if __name__=='__main__':main()
