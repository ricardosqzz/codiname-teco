# ENTRADAS: config/encartes_teco.json; output/07_microplasticos/microplasticos.gpkg, camadas microplastic_pressure, waste_census, licensing_screening, waste_management, basins.
# CONTEXTO: vias/malha_viaria.shp (hier_legal); hidrografia_bacias no GPKG territorial; reservatorio/{bacia}.shp.
# CAMPOS: MP_INDEX, MP_CLASS, MP_K, MP_MORAN, MP_STAB, MP_QUINT, WASTE_PCT, ROAD_DENS; BACIA e GRID_ID identificam cada fragmento.
# SAÍDAS: output/07_microplasticos/figuras; PNG 350 dpi, SVG vetorial e galeria.json; três bacias, escala de impressão 1:225000.
# CAMINHOS: TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json; parâmetros da análise em config/microplasticos.json.
from pathlib import Path
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.plot import plotting_extent
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap,Normalize,ListedColormap
from matplotlib.patches import Patch,Rectangle
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
from pyproj import Transformer
from shapely.geometry import box
from caminhos_teco import raiz_projeto
R=raiz_projeto();O=R/'output/07_microplasticos';G=O/'microplasticos.gpkg';F=O/'figuras';F.mkdir(exist_ok=True)
b=gpd.read_file(G,layer='basins').set_index('id').loc[['pampulha','vargem_flores','ibirite_regap']].reset_index()
a=gpd.read_file(G,layer='microplastic_pressure');waste=gpd.read_file(G,layer='waste_census');lic=gpd.read_file(G,layer='licensing_screening');fac=gpd.read_file(G,layer='waste_management')
roads=gpd.read_file(R/'vias/malha_viaria.shp').to_crs(31983);hyd=gpd.read_file(R/'output/02_avaliacao_espacial/teco_avaliacao.gpkg',layer='hidrografia_bacias')
water={key:gpd.read_file(R/'reservatorio'/f'{key}.shp').to_crs(31983) for key in b.id}
views=json.loads((R/'config/encartes_teco.json').read_text('utf8'));T=Transformer.from_crs(31983,4326,always_xy=True)
names={'pampulha':'Pampulha','vargem_flores':'Vargem das Flores','ibirite_regap':'Ibirité / REGAP'}
palette=['#a8d9e6','#68b7a0','#e2d17d','#df995c','#b94854'];CM=LinearSegmentedColormap.from_list('pressure',palette);gallery=[]
plt.rcParams.update({'font.family':'Arial','font.size':9,'svg.fonttype':'none'})
roads['TYPE']=roads.hier_legal.fillna('').str.upper().map(lambda s:0 if 'PRIMARIA' in s or 'EXPRESSA' in s else 1 if 'ARTERIAL' in s or 'COLETORA' in s else 2)

# Encarte triplo
def start(title):
    fig=plt.figure(figsize=(30/2.54,12.7/2.54));fig.suptitle(title,y=.975,fontsize=12.3,fontweight='bold',color='#244853');axes=[]
    for j,r in enumerate(b.itertuples()):
        ax=fig.add_axes([.05+j*.325,.23,.27,8.1/12.7]);axes.append(ax);v=views.get(r.id,{})
        cx=(r.geometry.bounds[0]+r.geometry.bounds[2])/2+v.get('dx',0);cy=(r.geometry.bounds[1]+r.geometry.bounds[3])/2+v.get('dy',0);span=v.get('span',18225)
        assert abs(span/(.27*(30/100))-225000)<1
        ax.set_xlim(cx-span/2,cx+span/2);ax.set_ylim(cy-span/2,cy+span/2);ax.set_aspect('equal');ax.set_facecolor('#f5f6f3');frame=box(cx-span/2,cy-span/2,cx+span/2,cy+span/2)
        for typ,col,lw in [(0,'#827564',.4),(1,'#a49a8c',.25),(2,'#b5b8b1',.15)]:
            rr=roads[(roads.TYPE==typ)&roads.intersects(frame)]
            if len(rr):rr.plot(ax=ax,color=col,linewidth=lw,zorder=3,alpha=.75)
        hh=hyd[hyd.intersects(frame)]
        if len(hh):hh.plot(ax=ax,color='#7eafc2',linewidth=.23,zorder=4)
        ax.set_title(names[r.id],fontsize=10,pad=6,fontweight='bold',color='#244853')
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos,cy=cy:f'{abs(T.transform(x,cy)[0]):.2f}°W'))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y,pos,cx=cx:f'{abs(T.transform(cx,y)[1]):.2f}°S'))
        ax.set_xticks(np.linspace(cx-span*.38,cx+span*.38,3));ax.set_yticks(np.linspace(cy-span*.38,cy+span*.38,3));ax.tick_params(labelsize=7.8,pad=2);ax.tick_params(axis='y',labelrotation=90)
        for sp in ax.spines.values():sp.set_visible(True);sp.set_linewidth(.7);sp.set_zorder(30)
    return fig,axes

# Elementos comuns e exportação
def finish(fig,axes,key,title,bar=None,handles=None):
    for ax,r in zip(axes,b.itertuples()):
        water[r.id].boundary.plot(ax=ax,color='white',linewidth=2.4,zorder=8);water[r.id].plot(ax=ax,facecolor='#45a8cf',edgecolor='#155777',linewidth=.8,zorder=9)
        gpd.GeoSeries([r.geometry],crs=31983).boundary.plot(ax=ax,color='#35413d',linewidth=.9,zorder=10)
        ax.text(.965,.956,'N',ha='center',va='bottom',transform=ax.transAxes,fontsize=8,zorder=20);ax.annotate('',xy=(.965,.95),xytext=(.965,.865),xycoords='axes fraction',arrowprops={'facecolor':'#244853','width':1.0,'headwidth':4.5,'headlength':6},zorder=20)
        ax.text(.965,.025,'SIRGAS 2000 / UTM 23S\nEPSG:31983 · Scale 1:225000\nBrentano, M. C. B.',transform=ax.transAxes,ha='right',va='bottom',fontsize=5.1,linespacing=1.05,bbox={'facecolor':'white','edgecolor':'#bfc9c7','alpha':.95,'pad':2},zorder=20)
        x0=ax.get_xlim()[0]+18225*.055;y0=ax.get_ylim()[0]+18225*.065
        for j in range(2):ax.add_patch(Rectangle((x0+j*2500,y0),2500,180,facecolor='#263d42' if j==0 else 'white',edgecolor='#263d42',linewidth=.5,zorder=20))
        for j,s in enumerate(['0','2.5','5 km']):ax.text(x0+j*2500,y0+230,s,fontsize=5.5,ha='center',va='bottom',zorder=20)
    if bar:
        cmap,norm,label=bar;cax=fig.add_axes([.29,.105,.46,.025]);cb=fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap=cmap),cax=cax,orientation='horizontal');cb.set_label(label,fontsize=9,labelpad=3);cb.ax.tick_params(labelsize=8,length=3)
    if handles:fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.047),ncol=min(3,len(handles)),fontsize=8,frameon=False,columnspacing=1.5,handletextpad=.55,labelspacing=.7)
    fig.savefig(F/(key+'.png'),dpi=350);fig.savefig(F/(key+'.svg'));plt.close(fig);gallery.append({'id':key,'title':title,'png':key+'.png','svg':key+'.svg'})

# Mapas contínuos
def continuous(field,title,key,vmin=0,vmax=100,source=a):
    fig,axes=start(title);norm=Normalize(vmin,vmax)
    for ax,r in zip(axes,b.itertuples()):
        g=source[source.BACIA==r.id];valid=g[field].notna();g[~valid].plot(ax=ax,facecolor='#dde2df',edgecolor='#b4bbb7',linewidth=.13,zorder=1) if (~valid).any() else None
        g[valid].plot(ax=ax,column=field,cmap=CM,vmin=vmin,vmax=vmax,linewidth=.15,edgecolor='#64726b',zorder=2)
    label='Households/km²' if field in ['WASTE_DENS','SEWER_DENS'] else 'Households (%)' if 'WASTE' in field else 'Agreement with S0 (%)' if field=='MP_STAB' else 'Mapped roads (km/km²)' if field=='ROAD_DENS' else 'Index (0–100)'
    finish(fig,axes,key,title,bar=(CM,norm,label))

# Mapas categóricos
def categories(field,title,key,labels,colors):
    fig,axes=start(title)
    for ax,r in zip(axes,b.itertuples()):
        g=a[a.BACIA==r.id]
        for value,color in colors.items():
            q=g[g[field]==value]
            if len(q):q.plot(ax=ax,facecolor=color,edgecolor='#596a62',linewidth=.16,zorder=2)
    handles=[Patch(facecolor=colors[x],edgecolor='#68776c',linewidth=.4,label=label) for x,label in labels.items()];finish(fig,axes,key,title,handles=handles)

# Produtos
def main():
    continuous('WASTE_PCT','Household waste collection deficit · Census 2022','01_waste',0,100,waste)
    continuous('ROAD_DENS','Mapped road density · 500 m neighbourhoods','02_roads',0,float(a.ROAD_DENS.max()))
    continuous('ARG_INDEX','ARG-related anthropogenic pressure · preserved baseline','03_arg')
    continuous('MP_INDEX','Exploratory microplastic source pressure · equal weights','04_mp_index')
    categories('MP_CLASS','Microplastic source pressure · fixed score classes','05_mp_classes',{0:'Insufficient inputs',1:'Very low (0–20)',2:'Low (>20–40)',3:'Moderate (>40–60)',4:'High (>60–80)',5:'Very high (>80–100)'},{0:'#dbe1dd',**{i+1:col for i,col in enumerate(palette)}})
    categories('MP_QUINT','Microplastic source pressure · relative quintiles','06_mp_quintiles',{0:'Insufficient inputs',**{i+1:label for i,label in enumerate(['≤P20','>P20–P40','>P40–P60','>P60–P80','>P80'])}},{0:'#dbe1dd',**{i+1:col for i,col in enumerate(palette)}})
    k=int(a.MP_K.max());kc={i+1:c for i,c in enumerate(['#72b8bb','#cd7866','#d9bf65','#8f8dbb','#8eab67','#b76f94'][:k])};categories('MP_K',f'Microplastic source profiles · k-means K={k}','07_mp_kmeans',{0:'Insufficient inputs',**{i:f'Profile {i}' for i in range(1,k+1)}},{0:'#dbe1dd',**kc})
    continuous('MP_STAB','Microplastic profiles · sensitivity to weighting','08_mp_stability')
    categories('MP_MORAN','Microplastic source pressure · local Moran (FDR 5%)','09_mp_moran',{'HH':'High–high','LL':'Low–low','HL':'High–low','LH':'Low–high','NS':'Not significant','ND':'Insufficient inputs'},{'HH':'#bf555b','LL':'#5b91b2','HL':'#e4b278','LH':'#a5ced3','NS':'#dfe5de','ND':'#c2c8c5'})
    fig,axes=start('Documented licensing and solid-waste management · screening')
    for ax,r in zip(axes,b.itertuples()):
        q=lic[lic.BACIA.str.contains(r.id,na=False)];q[q.MP_CAND==0].plot(ax=ax,facecolor='#b1aeb3',edgecolor='white',markersize=14,zorder=11)
        if (q.MP_CAND==1).any():q[q.MP_CAND==1].plot(ax=ax,marker='D',facecolor='#b84969',edgecolor='white',markersize=38,zorder=12)
        f=fac[fac.intersects(box(ax.get_xlim()[0],ax.get_ylim()[0],ax.get_xlim()[1],ax.get_ylim()[1]))]
        if len(f):f.plot(ax=ax,marker='s',facecolor='#6c8773',edgecolor='white',markersize=32,zorder=12)
    finish(fig,axes,'10_licensing','Documented licensing and solid-waste management · screening',handles=[Line2D([],[],linestyle='',marker='o',color='#b1aeb3',label='Other licensed activities'),Line2D([],[],linestyle='',marker='D',color='#b84969',label='Plastic-related activity: verify operation'),Line2D([],[],linestyle='',marker='s',color='#6c8773',label='Management facility: contextual record')])
    fig,axes=start('Microplastic pressure · topographic upstream mean')
    for ax,r in zip(axes,b.itertuples()):
        with rasterio.open(O/'rasters'/f'{r.id}_upstream_pressure.tif') as d:data=d.read(1,masked=True);ax.imshow(data,extent=plotting_extent(d),cmap=CM,vmin=0,vmax=100,zorder=2,interpolation='nearest')
    finish(fig,axes,'11_upstream','Microplastic pressure · topographic upstream mean',bar=(CM,Normalize(0,100),'Mean upstream index (0–100)'))
    continuous('WASTE_DENS','Uncollected household waste · estimated source density','12_waste_density',vmax=float(a.WASTE_DENS.max()))
    continuous('SEWER_DENS','Households without general sewer connection · estimated density','13_sewer_density',vmax=float(a.SEWER_DENS.max()))
    (F/'galeria.json').write_text(json.dumps(gallery,ensure_ascii=False,indent=2),encoding='utf8');print('Mapas',len(gallery),flush=True)
if __name__=='__main__':main()
