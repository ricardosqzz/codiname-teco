# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/output/04_grade_500m/teco_grade_500m.gpkg | gpd.read_file | camada='saude_todos'.
# Entrada: E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg | gpd.read_file | camada='analise_setores'.
# Entrada: E:/teco/output/03_multivariada/teco_multivariada.gpkg | gpd.read_file | camada='unidades_ajuste'.
# Entrada: E:/teco/output/04_grade_500m/tabelas/kmeans_grade.csv | pd.read_csv.
# Entrada: E:/teco/saneamento_ibge/populacao_basico/Agregados_por_setores_basico_BR.csv | pd.read_csv.
# Campos/chaves em a: AIH_LOCAL, AREA_KM2, BACIA, GRID_ID, N_AIH_LOCAL, N_POP_DENS, N_SEM_REDE, POP_DENS, SEM_REDE, VALIDO, geometry, is_valid.
# Campos/chaves em c: DOM_DENS, SEM_ANALIT, dens_pop, dom_set, geometry, pct_rede, pop_2022, set_km2, setor_id.
# Campos/chaves em cir: BACIA, GRID_ID, geometry.
# Campos/chaves em hp: AIH_ANO, CNES, geometry.
# Campos/chaves em a.loc: ESTABILIDADE, I_S0, K_S0, QUINTIL.
# Campos/chaves em loc: cluster, q.
# Saída: E:/teco/tmp/consolidacao_final/testes_kmeans.gpkg | out.to_file.
# Saída: E:/teco/tmp/consolidacao_final/Kmeans_all_25_verified.csv | .to_csv.
# Saída: E:/teco/tmp/consolidacao_final/Auditoria_numerica.json | .write_text.
# Campos/chaves gerados em c: DOM_DENS, SEM_ANALIT.
# Campos/chaves gerados em z: AREA, D, OBS, P, S.
# Campos/chaves gerados em out: K, PROFILE, SCENARIO, SCORE.
# POP_DENS: habitantes/km².
# SEM_REDE: % de domicílios sem rede de esgoto.
# AIH_LOCAL: média anual de internações no estabelecimento local.
# I_S0: índice de pressão com pesos iguais, 0-100.
# K_S0: perfil do k-means no cenário de referência.
# CNES: identificador do estabelecimento de saúde.
# GRID_ID: identificador do centro da grade.
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
import json,datetime
import pandas as pd,numpy as np,geopandas as gpd
from scipy.stats import spearmanr
from analise_espacial_teco import fitkm,silhouette,ari
from multivariada_teco import align,queen,moran_w
R=Path(_cp_texto('', 'posix'));O=R/'output/04_grade_500m';B=R/'output/02_avaliacao_espacial';T=R/'tmp/consolidacao_final';T.mkdir(parents=True,exist_ok=True)
G=O/'teco_grade_500m.gpkg';checks=[];models={};errors=[]

# Check
def check(name,condition,detail):
 checks.append({'check':name,'status':'OK' if condition else 'ERROR','detail':detail})
 if not condition:errors.append(name)

# Main
def main():
 a=gpd.read_file(G,layer='grade_resultados');cir=gpd.read_file(G,layer='influencia_500m');b=gpd.read_file(G,layer='bacias_estudo');c=gpd.read_file(B/'teco_avaliacao.gpkg',layer='analise_setores');hp=gpd.read_file(G,layer='saude_todos')
 check('Valid geometry and unique keys',bool(a.is_valid.all() and not a.duplicated(['GRID_ID','BACIA']).any()),{'rows':len(a),'centres':a.GRID_ID.nunique()})
 for row in b.itertuples():
  sub=a[a.BACIA==row.id];u=sub.geometry.union_all();gap=row.geometry.difference(u).area;outside=u.difference(row.geometry).area;overlap=sub.area.sum()-u.area
  check('Grid coverage '+row.id,gap<25 and outside<1 and abs(overlap)<1,{'gap_m2':gap,'outside_m2':outside,'overlap_m2':overlap})

 aux=gpd.read_file(R/'output/03_multivariada/teco_multivariada.gpkg',layer='unidades_ajuste').set_index('setor_id');c['SEM_ANALIT']=c.setor_id.map(aux.sem_rede);c['DOM_DENS']=c.dom_set/c.set_km2
 z=gpd.overlay(cir[['GRID_ID','BACIA','geometry']],c[['dens_pop','DOM_DENS','pct_rede','SEM_ANALIT','geometry']],how='intersection');z['AREA']=z.area/1e6;z['P']=z.dens_pop*z.AREA;z['D']=z.DOM_DENS*z.AREA;z['S']=z.D*z.SEM_ANALIT/100;z['OBS']=z.D.where(z.pct_rede.notna(),0)
 s=z.groupby(['GRID_ID','BACIA'])[['P','D','S','OBS']].sum(min_count=1).reindex(pd.MultiIndex.from_frame(a[['GRID_ID','BACIA']]))
 recomputed=np.c_[s.P.to_numpy()/a.AREA_KM2.to_numpy(),100*s.S.to_numpy()/s.D.replace(0,np.nan).to_numpy()];recomputed[s.D.to_numpy()==0,1]=0
 check('Population and sanitation aggregation',np.allclose(recomputed,a[['POP_DENS','SEM_REDE']],equal_nan=True,atol=1e-8),{'max_population_difference':float(np.nanmax(abs(recomputed[:,0]-a.POP_DENS))),'max_sanitation_difference':float(np.nanmax(abs(recomputed[:,1]-a.SEM_REDE)))})
 joined=gpd.sjoin(hp[['CNES','AIH_ANO','geometry']],cir[['GRID_ID','BACIA','geometry']],predicate='intersects');hh=joined.groupby(['GRID_ID','BACIA']).AIH_ANO.sum();health=np.array([hh.get((r.GRID_ID,r.BACIA),0) for r in a.itertuples()]);check('Hospital activity in calculation neighbourhoods',np.allclose(health,a.AIH_LOCAL),{'facilities':len(hp),'positive_grid_rows':int((health>0).sum())})
 x=np.c_[np.log1p(a.POP_DENS),a.SEM_REDE,np.log1p(a.AIH_LOCAL)];valid=np.isfinite(x).all(1);lo=x[valid].min(0);hi=x[valid].max(0);n=(x-lo)/np.where(hi>lo,hi-lo,1)
 check('Transformation and normalisation',np.allclose(n,a[['N_POP_DENS','N_SEM_REDE','N_AIH_LOCAL']],equal_nan=True,atol=1e-10),{'valid':int(valid.sum()),'incomplete':int((~valid).sum()),'min':lo.tolist(),'max':hi.tolist()})
 weights={'S0':[1,1,1],'S1':[1,1,3],'S2':[1,3,1],'S3':[3,1,1],'S4':[1,1,0]};rows=[]
 saved=pd.read_csv(O/'tabelas/kmeans_grade.csv',sep=';',decimal=',').set_index(['cenario','k'])
 for j,(co,w) in enumerate(weights.items()):
  score=100*(n@w)/sum(w);tiers=np.where(valid,np.minimum(np.nan_to_num(score/20).astype(int)+1,5),0)
  check('Score and tiers '+co,np.allclose(score,a['I_'+co],equal_nan=True) and np.array_equal(tiers,a['F_'+co]),{'weights':w})
  for k in range(2,7):
   loss,cent,lab=fitkm(n[valid]*np.sqrt(w),k,20261112+100*j,starts=15);sil=silhouette(n[valid]*np.sqrt(w),lab);reference=saved.loc[co,k];check(f'K-means reproducibility {co} k{k}',abs(loss-reference.inercia)<1e-8 and abs(sil-reference.silhouette)<1e-9,{'inertia':loss,'silhouette':sil,'smallest_group':int(np.bincount(lab).min())});models[co,k]=lab

   if k==2:lab=align(lab,a.loc[valid,'K_S0'].to_numpy()-1)
   else:
    order=sorted(np.unique(lab),key=lambda q:float(np.mean(score[valid][lab==q])));mapping={q:i for i,q in enumerate(order)};lab=np.array([mapping[q] for q in lab])
   out=a[['GRID_ID','BACIA','POP_DENS','SEM_REDE','AIH_LOCAL','N_POP_DENS','N_SEM_REDE','N_AIH_LOCAL','geometry']].copy();out['SCENARIO']=co;out['K']=k;out['PROFILE']=0;out.loc[valid,'PROFILE']=lab+1;out['SCORE']=score
   out.to_file(T/'testes_kmeans.gpkg',layer=f'{co}_k{k:02d}',driver='GPKG')
   rows.append({'scenario':co,'k':k,'inertia':loss,'silhouette':sil,'smallest_group':int(np.bincount(lab).min())})
  check('Published profiles '+co,np.array_equal(align(models[co,2],a.loc[valid,'K_S0'].to_numpy()-1)+1,a.loc[valid,'K_'+co]),{'compared_rows':int(valid.sum())})
 stacks=np.array([align(models[co,2],a.loc[valid,'K_S0'].to_numpy()-1) for co in weights]);stab=100*np.mean(stacks==(a.loc[valid,'K_S0'].to_numpy()-1),axis=0);check('Weight sensitivity stability',np.allclose(stab,a.loc[valid,'ESTABILIDADE']),{})
 q=pd.qcut(a.loc[valid,'I_S0'].rank(method='average'),5,labels=False,duplicates='drop')+1;check('Quintile classification',np.array_equal(q,a.loc[valid,'QUINTIL']),q.value_counts().to_dict())
 for key,grp in a[a.VALIDO].groupby('BACIA'):
  g=grp[grp.COB_ESG.ge(95)];rec,loc,ii=moran_w(g.I_S0.to_numpy(),queen(g),local=True);original=a.loc[g.index[ii]];check('Moran and FDR reproducibility '+key,np.array_equal(loc['cluster'],original.MORAN) and np.allclose(loc['q'],original.MORAN_Q),rec)

 ids=set(c.setor_id);parts=[]
 popsrc=R/'saneamento_ibge/populacao_basico/Agregados_por_setores_basico_BR.csv'
 for chunk in pd.read_csv(popsrc,sep=';',dtype='string',encoding='latin1',chunksize=30000):
  code='CD_SETOR' if 'CD_SETOR' in chunk else 'setor';sub=chunk[chunk[code].isin(ids)]
  if len(sub):parts.append(sub)
 pop=pd.concat(parts,ignore_index=True);code='CD_SETOR' if 'CD_SETOR' in pop else 'setor';pv='v0001' if 'v0001' in pop else 'V0001';ref=pd.to_numeric(pop.set_index(code)[pv],errors='coerce');observed=c.setor_id.map(ref)
 check('Population against complete basic spreadsheet',np.allclose(observed,c.pop_2022,equal_nan=True),{'matched_sectors':len(pop),'unique_sectors':len(ids),'differences':int(~np.isclose(observed,c.pop_2022,equal_nan=True).sum()) if False else int((~np.isclose(observed,c.pop_2022,equal_nan=True)).sum())})
 pd.DataFrame(rows).to_csv(T/'Kmeans_all_25_verified.csv',sep=';',index=False,encoding='utf-8-sig')
 result={'date':datetime.datetime.now().astimezone().isoformat(),'checks':checks,'errors':errors,'status':'OK' if not errors else 'CORRECTION_REQUIRED'};(T/'Auditoria_numerica.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str),encoding='utf8');print(json.dumps(result,ensure_ascii=False,default=str),flush=True)
if __name__=='__main__':main()
