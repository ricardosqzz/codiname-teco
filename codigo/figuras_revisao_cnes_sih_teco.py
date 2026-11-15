# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/entrega_final/01_entradas/01_bacias/bacias.shp | gpd.read_file.
# Entrada: E:/teco/entrega_final/01_entradas/02_reservatorios/reservatorios.shp | gpd.read_file.
# Entrada: E:/teco/entrega_final/01_entradas/05_hidrografia/hidrografia.shp | gpd.read_file.
# Entrada: E:/teco/entrega_final/01_entradas/06_vias_contexto/vias_contexto.shp | gpd.read_file.
# Entrada: E:/teco/config/encartes_teco.json | .read_text.
# Entrada: E:/teco/codigo/figuras_multivariada_teco.py | .read_text.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/02_camadas/01_cnes_bacias/cnes_2026.shp | gpd.read_file.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/02_camadas/02_selecao_sih/sih_atual.shp | gpd.read_file.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/02_camadas/03_bordas/sih_bordas.shp | gpd.read_file.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/Internacoes_gerais_selecionados_mensal.csv | pd.read_csv.
# Entrada: E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/Internacoes_gerais_selecionados_anual.csv | pd.read_csv.
# Entrada: E:/teco/entrega_final/00_documentacao/manifesto.json | mp.read_text.
# Entrada: E:/teco/entrega_final/index.html | p.read_text.
# Campos/chaves em .loc: ibirite_regap, pampulha, vargem_flores.
# Campos/chaves em allc: BACIA.
# Campos/chaves em sel: BACIA.
# Campos/chaves em near: BACIA.
# Campos/chaves em monthly: CNES.
# Campos/chaves em annual: CNES.
# Campos/chaves em ax.spines: right, top.
# Campos/chaves em r: arquivo, slug, titulo, vetorial.
# Campos/chaves em m: mapas.
# Saída: {fig} | savefig.
# Saída: E:/teco/tmp/figuras_cnes_2026/figuras/{slug}.{ext} | fig.savefig.
# Saída: E:/teco/entrega_final/00_documentacao/manifesto.json | mp.write_text.
# Saída: E:/teco/entrega_final/index.html | p.write_text.
# Campos/chaves gerados em m: mapas.
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
import ast
import json
import shutil
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch,Rectangle
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
from pyproj import Transformer
from shapely.geometry import box
from idioma_cartografico_teco import en

R=Path(_cp_texto('', 'posix'));F=R/'entrega_final';P=F/'01_entradas/17_estabelecimentos_2026'
O=R/'tmp/figuras_cnes_2026';(O/'figuras').mkdir(parents=True,exist_ok=True)
DEST=F/'03_mapas/17_cnes_sih_2026';DEST.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'Arial','font.size':9,'svg.fonttype':'none'})
b=gpd.read_file(F/'01_entradas/01_bacias/bacias.shp').set_index('id').loc[['pampulha','vargem_flores','ibirite_regap']].reset_index()
av=b.rename(columns={'id':'bas_id'});water=gpd.read_file(F/'01_entradas/02_reservatorios/reservatorios.shp')
hyd=gpd.read_file(F/'01_entradas/05_hidrografia/hidrografia.shp');mun=gpd.GeoDataFrame(geometry=[],crs=31983)
roads=gpd.read_file(F/'01_entradas/06_vias_contexto/vias_contexto.shp')
names={'pampulha':'Pampulha','vargem_flores':'Vargem das Flores','ibirite_regap':'Ibirité / REGAP'}
MAP_VIEWS=json.loads((R/'config/encartes_teco.json').read_text('utf8'))
span=18225.;scale=225000;trans=Transformer.from_crs(31983,4326,always_xy=True);gallery=[]
source=(R/'codigo/figuras_multivariada_teco.py').read_text('utf8').replace("color='#a8cedd',edgecolor='#567e8c',lw=.45","color='#45a8cf',edgecolor='#155777',lw=.8")
tree=ast.parse(source);keep={'start','finish','legend','legend_small'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in keep],type_ignores=[]),'<composicao_encartes>','exec'))
savefig=plt.Figure.savefig

# Salvar
def salvar(fig,*args,**kwargs):
    from matplotlib.text import Text
    for t in fig.findobj(Text):
        value=en(t.get_text())
        if value.startswith('Datum: SIRGAS 2000'):
            value='Datum: SIRGAS 2000\nUTM 23S · EPSG:31983\nScale 1:225,000\nBrentano, M. C. B.'
            t.set_fontsize(5.1)
        t.set_text(value)
    return savefig(fig,*args,**kwargs)
plt.Figure.savefig=salvar

allc=gpd.read_file(P/'02_camadas/01_cnes_bacias/cnes_2026.shp')
sel=gpd.read_file(P/'02_camadas/02_selecao_sih/sih_atual.shp')
near=gpd.read_file(P/'02_camadas/03_bordas/sih_bordas.shp')
fig,axs=start('Healthcare inventory and recent hospital production',sectors=False)
for ax,r in zip(axs,b.itertuples()):
    frame=box(ax.get_xlim()[0],ax.get_ylim()[0],ax.get_xlim()[1],ax.get_ylim()[1])
    rr=roads[roads.intersects(frame)]
    for category,color,width in [('Sem classe cadastrada','#bdc6c5',.11),('Local','#aebbb9',.15),('Secundária / coletora','#9daca9',.23),('Principal','#879894',.34)]:
        part=rr[rr.TIPO_VIA.eq(category)]
        if len(part):part.plot(ax=ax,color=color,lw=width,zorder=1.8)
    allc[allc.BACIA.eq(r.id)].plot(ax=ax,color='#287b95',markersize=7,alpha=.78,edgecolor='white',linewidth=.12,zorder=9)
    q=sel[sel.BACIA.eq(r.id)]
    if len(q):
        q.plot(ax=ax,color='#bd3658',marker='*',markersize=100,edgecolor='white',linewidth=.6,zorder=18)
        numbering={'2191164':('1',(-14,16)),'2200473':('2',(15,-16)),'6892256':('3',(10,10))}
        for point in q.itertuples():
            code,offset=numbering[point.CNES]
            ax.annotate(code,xy=(point.geometry.x,point.geometry.y),xytext=offset,textcoords='offset points',fontsize=8,fontweight='bold',ha='center',va='center',color='white',bbox={'boxstyle':'circle,pad=.22','fc':'#bd3658','ec':'white','lw':.5},arrowprops={'arrowstyle':'-','color':'#742f48','lw':.6},zorder=21)
    q=near[near.BACIA.eq(r.id)]
    if len(q):q.plot(ax=ax,color='#d49b31',marker='^',markersize=38,edgecolor='#705522',linewidth=.5,zorder=17)
handles=[Line2D([],[],marker='o',ls='',color='#287b95',label='CNES Sep 2026 · all facility types'),Line2D([],[],marker='*',ls='',color='#bd3658',markersize=10,label='SIH production · Jan 2024–Sep 2026'),Line2D([],[],marker='^',ls='',color='#d49b31',label='Outside-boundary review'),Line2D([],[],ls='',label='1  Centro Materno Infantil'),Line2D([],[],ls='',label='2  Hospital Municipal de Contagem'),Line2D([],[],ls='',label='3  Hospital Regional de Ibirité')]
finish(fig,axs,'healthcare_cnes_sih_2026','Healthcare inventory and recent hospital production','Healthcare audit',handles=handles)

monthly=pd.read_csv(P/'01_tabelas/Internacoes_gerais_selecionados_mensal.csv',sep=';',dtype={'CNES':str})
annual=pd.read_csv(P/'01_tabelas/Internacoes_gerais_selecionados_anual.csv',sep=';',dtype={'CNES':str})
fig,axs=plt.subplots(3,2,figsize=(12,9),gridspec_kw={'width_ratios':[2.5,1]})
colors=['#297c97','#459681','#9a5984']
for j,r in enumerate(sel.sort_values(['BACIA','CNES']).itertuples()):
    q=monthly[monthly.CNES.eq(r.CNES)].sort_values('ANO_MES');d=pd.to_datetime(q.ANO_MES+'-01');ax=axs[j,0]
    ax.plot(d,q.INTERNACOES,lw=1.25,color=colors[j]);ax.fill_between(d,q.INTERNACOES.to_numpy(float),0,color=colors[j],alpha=.09)
    ax.axvspan(pd.Timestamp('2024-01-01'),pd.Timestamp('2026-10-01'),color='#e5c990',alpha=.18)
    ax.set_title(r.NOME_CNES+' · CNES '+r.CNES,loc='left',fontsize=9.2,pad=8)
    ax.set_xlim(pd.Timestamp('2015-01-01'),pd.Timestamp('2026-10-01'));ax.set_ylim(bottom=0);ax.grid(axis='y',alpha=.15);ax.xaxis.set_major_locator(mdates.YearLocator(2));ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'));ax.set_ylabel('Admissions / month',labelpad=10)
    a=annual[annual.CNES.eq(r.CNES)];ax=axs[j,1];barcolors=[colors[j] if y!=2026 else '#d3a24b' for y in a.ANO]
    ax.bar(a.ANO,a.INTERNACOES,color=barcolors,width=.8);ax.set_ylim(bottom=0);ax.set_title('Annual total · 2026 Jan–Sep',fontsize=9,pad=8);ax.set_xticks([2015,2020,2025]);ax.grid(axis='y',alpha=.15)
for ax in axs.ravel():
    ax.spines[['top','right']].set_visible(False);ax.tick_params(labelsize=8);ax.yaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:,.0f}'))
fig.suptitle('General SUS hospital admissions by care date · all diagnoses',fontsize=14,y=.99,color='#244853',fontweight='bold')
fig.legend(handles=[Patch(color='#e5c990',alpha=.4,label='Operational recent window: Jan 2024–Sep 2026'),Patch(color='#d3a24b',label='Partial year: Jan–Sep 2026')],loc='lower center',ncol=2,frameon=False,fontsize=9)
fig.tight_layout(rect=[0,.045,1,.965],h_pad=2.3,w_pad=2)
slug='healthcare_sih_series_2015_2026'
for ext in ['png','svg']:fig.savefig(O/'figuras'/f'{slug}.{ext}',dpi=350,facecolor='white')
plt.close(fig)
gallery.append({'slug':slug,'titulo':'General SUS hospital admissions by care date · 2015–Sep 2026','grupo':'Healthcare audit','tipo':'chart'})

mp=F/'00_documentacao/manifesto.json';m=json.loads(mp.read_text('utf8'))
slugs={r['slug'] for r in gallery};m['mapas']=[r for r in m['mapas'] if r['slug'] not in slugs]
for r in gallery:
    for ext in ['png','svg']:shutil.copy2(O/'figuras'/f"{r['slug']}.{ext}",DEST/f"{r['slug']}.{ext}")
    r.update(arquivo=(DEST/f"{r['slug']}.png").relative_to(F).as_posix(),vetorial=(DEST/f"{r['slug']}.svg").relative_to(F).as_posix())
    m['mapas'].append(r)
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
p=F/'index.html';s=p.read_text('utf8')
if 'Relatorio_revisao_CNES_SIH.html' not in s:
    cards=''.join('<article><a href="'+r['arquivo']+'"><img loading="lazy" src="'+r['arquivo']+'" alt="'+r['titulo']+'"></a><h3>'+r['titulo']+'</h3><a href="'+r['vetorial']+'">SVG</a></article>' for r in gallery)
    block='<section><h2>Revisão CNES e produção SIH · 2026</h2><p><a href="01_entradas/17_estabelecimentos_2026/04_documentacao/Relatorio_revisao_CNES_SIH.html">Relatório da conferência</a> · <a href="01_entradas/17_estabelecimentos_2026/01_tabelas/Selecionados_nas_bacias.csv">Lista selecionada</a> · <a href="01_entradas/17_estabelecimentos_2026/01_tabelas/CNES_nas_bacias.csv">Todos os CNES internos</a></p><div class="gallery">'+cards+'</div></section>'
    s=s.replace('</main>',block+'</main>');p.write_text(s,encoding='utf8')
print('Figuras CNES/SIH e índice atualizados',flush=True)
