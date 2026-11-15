# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg | gpd.read_file | camada='bacias_estudo'.
# Entrada: E:/teco/output/02_avaliacao_espacial/tabelas/sih_bacias_2016_2025.csv | pd.read_csv.
# Campos/chaves em c: geometry, setor_id.
# Campos/chaves em h: CNES, GRUPO, QA_MUN, geometry.
# Campos/chaves em u: geometry, setor_id.
# Campos/chaves em hj: CNES, dias_ano, geometry.
# Campos/chaves em u.loc: setor_id.
# Campos/chaves em r: cenario, k, silhouette.
# Campos/chaves em best: grupos_menores_1pct, k, min_grupo, silhouette.
# Campos/chaves em z: cenario, melhor_k.
# Campos/chaves em models: S0.
# Campos/chaves em scores: S0.
# Campos/chaves em rec: cenario.
# Campos/chaves em a: ESG_EST, EST_BLOCOS, EST_PESOS, MK_S0, MQ_S0, MQ_S4, MQ_S8, bas_id, elegivel, geometry, setor_id.
# Campos/chaves em rr: cluster, q.
# Saída: E:/teco/output/03_multivariada/tabelas/{n} | df.to_csv.
# Saída: E:/teco/output/03_multivariada/teco_multivariada.gpkg | g.to_file.
# Saída: E:/teco/output/03_multivariada/shapefiles/{n}.shp | g.to_file.
# Saída: E:/teco/output/03_multivariada/auditoria/metodo_multivariada.json | .write_text.
# Campos/chaves gerados em vals: urb_pct.
# Campos/chaves gerados em u: ESG_EST, ESG_HI, ESG_LO, ESG_OBS, ESG_ORIG, EST_BLOCOS, EST_PESOS, PC1, PC2, elegivel, saude_dens, saude_n, sem_rede, sih_dens, sih_n, sih_reg.
# Campos/chaves gerados em hj: dias_ano.
# Campos/chaves gerados em meta: tratamento_lacunas.
# CNES: identificador do estabelecimento de saúde.
# Novas variáveis: config/analise_extensivel.json; definir origem, campo, agregação, transformação e peso.
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
import json,math,datetime,hashlib,warnings
import numpy as np
import pandas as pd
import geopandas as gpd
from scipy.spatial import distance,cKDTree
from scipy.optimize import linear_sum_assignment
from scipy.sparse import csr_matrix
from scipy.stats import spearmanr
from analise_espacial_teco import fitkm,silhouette,ari,bh,weights,quint
R=Path(_cp_texto('', 'posix'));BASE=R/'output/02_avaliacao_espacial';O=R/'output/03_multivariada'
for folder in ['figuras','tabelas','shapefiles','auditoria']:(O/folder).mkdir(parents=True,exist_ok=True)
G=O/'teco_multivariada.gpkg';SEED=20261112;PERM=999
FEATURES=['pop_dens','sem_rede','urb_pct','saude_dens','sih_dens']
LABELS=['Adensamento','Sem rede','Urbanização','Serviços de saúde','Atividade SIH registrada']
SCENARIOS={
 'S0':('Base · todos os pesos 1',[1,1,1,1,1]),
 'S1':('Ênfase em esgotamento',[1,2,1,1,1]),
 'S2':('Ênfase assistencial',[1,1,1,2,2]),
 'S3':('Ênfase em ocupação',[2,1,2,1,1]),
 'S4':('Sem atividade SIH registrada',[1,1,1,1,0]),
 'S5':('Sem área urbanizada',[1,1,0,1,1]),
 'S6':('Sem densidade assistencial',[1,1,1,0,1]),
 'S7':('Sem adensamento',[0,1,1,1,1]),
 'S8':('Sem ausência de rede',[1,0,1,1,1]),
 'S9':('Lacunas de esgoto · limite inferior',[1,1,1,1,1]),
 'S10':('Lacunas de esgoto · limite superior',[1,1,1,1,1])}

# Csv
def csv(df,n):df.to_csv(O/'tabelas'/n,index=False,sep=';',decimal=',',encoding='utf-8-sig')

# Gp
def gp(g,n,shp=False):
 g.to_file(G,layer=n,driver='GPKG')
 if shp:g.to_file(O/'shapefiles'/f'{n}.shp',driver='ESRI Shapefile',encoding='UTF-8')

# Log
def log(*x):print(*x,flush=True)

# Assemble
def assemble():
 c=gpd.read_file(BASE/'teco_avaliacao.gpkg',layer='analise_setores')
 h=gpd.read_file(BASE/'teco_avaliacao.gpkg',layer='saude_cnes_ativos')
 b=gpd.read_file(BASE/'teco_avaliacao.gpkg',layer='bacias_estudo')

 u=c[['setor_id','geometry']].dissolve(by='setor_id').reset_index()
 vals=c.groupby('setor_id').agg(pop_dens=('dens_pop','first'),sem_rede=('def_rede','first'),area_km2=('rec_km2','sum'),urb_km2=('urb_km2','sum'),uso_km2=('uso_km2','sum'),dom_set=('dom_set','first'),municipio=('mun_cod','first'),situacao=('situacao','first'),pct_direta=('pct_rdir','first'),dpo_malha=('dpo_malha','first'),pop_total=('pop_2022','first'))
 vals['urb_pct']=100*vals.urb_km2/vals.uso_km2
 u=u.merge(vals,on='setor_id',validate='one_to_one')
 clinical=['Atenção básica','Hospital / hospital-dia','Urgência / pronto atendimento','Outros serviços assistenciais']
 h=h[(h.QA_MUN==1)&h.GRUPO.isin(clinical)]
 joined=gpd.sjoin(h[['CNES','geometry']],u[['setor_id','geometry']],predicate='intersects').sort_values(['CNES','setor_id']).drop_duplicates('CNES')
 counts=joined.groupby('setor_id').size();u['saude_n']=u.setor_id.map(counts).fillna(0).astype(int);u['saude_dens']=u.saude_n/u.area_km2
 hist=pd.read_csv(BASE/'tabelas/sih_bacias_2016_2025.csv',sep=';',dtype={'CNES':str})
 days=hist.groupby('CNES').dias_permanencia.sum(min_count=1)/10
 hj=h[h.CNES.isin(days.index)].copy();hj['dias_ano']=hj.CNES.map(days)
 hs=gpd.sjoin(hj[['CNES','dias_ano','geometry']],u[['setor_id','geometry']],predicate='intersects').sort_values(['CNES','setor_id']).drop_duplicates('CNES')
 reg=hs.groupby('setor_id').dias_ano.sum(min_count=1);u['sih_reg']=u.setor_id.map(reg).fillna(0.)

 u['sih_n']=u.setor_id.map(hs.groupby('setor_id').size()).fillna(0).astype(int);u['sih_dens']=u.sih_reg/u.area_km2
 u['ESG_ORIG']=u.sem_rede;u['ESG_OBS']=u.sem_rede.notna()

 empty=(u.dpo_malha==0)&(u.pop_total==0);u.loc[empty,'sem_rede']=0
 u['ESG_EST']=~u.ESG_OBS&~empty

 med=u.groupby(['municipio','situacao']).ESG_ORIG.transform('median')
 fallback=u.groupby('municipio').ESG_ORIG.transform('median').fillna(u.ESG_ORIG.median())
 u.loc[u.ESG_EST,'sem_rede']=med.fillna(fallback)[u.ESG_EST]

 upper=(100-u.pct_direta).fillna(100).clip(0,100)
 u['ESG_LO']=u.ESG_ORIG.where(u.ESG_OBS,0);u['ESG_HI']=u.ESG_ORIG.where(u.ESG_OBS,upper)
 u.loc[empty,['ESG_LO','ESG_HI']]=0
 u['sem_rede']=np.minimum(u.sem_rede,u.ESG_HI)
 u['elegivel']=np.isfinite(u[FEATURES]).all(axis=1)&(u.uso_km2>0)
 assert u.setor_id.is_unique and len(u)==1838
 csv(pd.DataFrame(u.drop(columns='geometry')),'entradas_por_setor.csv')
 csv(pd.DataFrame(hs.drop(columns='geometry')),'alocacao_sih_setores.csv')
 rules=[('pop_dens','pessoas/km²','População estimada por área / área do recorte; equivale à densidade do setor original.'),('sem_rede','% de domicílios','100 - percentual com rede geral/pluvial ou fossa conectada; não comprova esgoto sem tratamento.'),('urb_pct','% de área mapeada','Área urbanizada / área com uso do solo válido, somadas nos recortes do mesmo setor.'),('saude_dens','estabelecimentos/km²','CNES ativo, município compatível; apenas serviços assistenciais fixos; exclui farmácia, administrativo e móvel.'),('sih_dens','dias de permanência registrados/ano/km²','Soma SIH 2016-2025 dos três estabelecimentos localizados / 10 anos / área; ausência na coorte não significa atividade real nula.')]
 csv(pd.DataFrame(rules,columns=['variavel','unidade','definicao']),'dicionario_multivariada.csv')
 return u,c,b,h

# Normalized
def normalized(u):
 valid=u.elegivel;raw=u.loc[valid,FEATURES].to_numpy(float);t=raw.copy()
 for i in [0,3,4]:t[:,i]=np.log1p(t[:,i])
 lo=t.min(0);hi=t.max(0);assert (hi>lo).all()
 x=(t-lo)/(hi-lo)
 pars=[{'variavel':f,'transformacao':'log1p' if j in [0,3,4] else 'identidade','min_transformado':lo[j],'max_transformado':hi[j],'peso_base':1,'setores_nao_nulos':int((raw[:,j]>0).sum())} for j,f in enumerate(FEATURES)]
 csv(pd.DataFrame(pars),'parametros_normalizacao.csv')
 csv(pd.DataFrame(x,columns=FEATURES).assign(setor_id=u.loc[valid,'setor_id'].values),'matriz_normalizada.csv')
 return x,valid

# Align
def align(labels,reference):
 k=max(labels.max(),reference.max())+1;tab=np.bincount(reference*k+labels,minlength=k*k).reshape(k,k)
 rr,cc=linear_sum_assignment(-tab);lookup=dict(zip(cc,rr));return np.array([lookup[v] for v in labels])

# Cluster
def cluster(u,x,valid):
 krows=[];scenario_rows=[];profiles=[];models={};predictions={};scores={};counts=[]
 idx=u.index[valid];n=len(idx);minimum=max(5,math.ceil(.01*n))

 for code,(title,ww) in SCENARIOS.items():
  w=np.asarray(ww,float);xx=x.copy()
  if code in ['S9','S10']:
   field='ESG_LO' if code=='S9' else 'ESG_HI';xx[:,1]=u.loc[valid,field].to_numpy()/100
  wx=xx*np.sqrt(w);scores[code]=100*(xx@w)/w.sum();local=[]
  for k in range(2,7):
   loss,cent,l=fitkm(wx,k,SEED+100*int(code[1:]),starts=15)
   sc=silhouette(wx,l);sizes=np.bincount(l,minlength=k)
   row={'cenario':code,'k':k,'silhouette':sc,'min_grupo':int(sizes.min()),'max_grupo':int(sizes.max()),'grupos_menores_1pct':int((sizes<minimum).sum()),'inercia':loss}
   krows.append(row);local.append(row);models[code,k]=(cent,l)
  best=max(local,key=lambda r:r['silhouette']);predictions[code,'best']=models[code,best['k']][1]
  scenario_rows.append({'cenario':code,'nome':title,**dict(zip(FEATURES,ww)),'melhor_k':best['k'],'silhouette_melhor':best['silhouette'],'min_grupo_melhor':best['min_grupo'],'alerta_grupo_pequeno':best['grupos_menores_1pct']>0})
  log('CENARIO',code,best)
 k0=next(z['melhor_k'] for z in scenario_rows if z['cenario']=='S0')
 base=models['S0',k0][1]

 order=sorted(np.unique(base),key=lambda z:scores['S0'][base==z].mean());mp={l:i for i,l in enumerate(order)};base=np.array([mp[z] for z in base])
 base_scores=scores['S0'];stacks=[]
 for rec in scenario_rows:
  co=rec['cenario'];lab=align(models[co,k0][1],base);predictions[co,'fixed']=lab;stacks.append(lab)
  rec.update(k_comum=k0,ARI_base=ari(base,lab),mesmo_perfil_pct=100*np.mean(base==lab),rho_escore=spearmanr(base_scores,scores[co]).statistic,silhouette_k_comum=next(r['silhouette'] for r in krows if r['cenario']==co and r['k']==k0))
  u[f'I_{co}']=np.nan;u.loc[idx,f'I_{co}']=scores[co]
  u[f'K_{co}']=0;u.loc[idx,f'K_{co}']=lab+1
  for cl in np.unique(lab):
   rows=u.loc[idx[lab==cl]];profiles.append({'cenario':co,'cluster':int(cl+1),'n':len(rows),**{f:rows[f].median() for f in FEATURES}})
  counts +=[{'cenario':co,'cluster':int(cl+1),'n':int((lab==cl).sum())} for cl in np.unique(lab)]
 for k in range(2,7):
  raw=models['S0',k][1];order=sorted(np.unique(raw),key=lambda z:base_scores[raw==z].mean());mp={l:i+1 for i,l in enumerate(order)}
  u[f'BASE_K{k}']=0;u.loc[idx,f'BASE_K{k}']=[mp[z] for z in raw]
 u['EST_PESOS']=np.nan;u.loc[idx,'EST_PESOS']=100*np.mean(np.array(stacks)==base,axis=0)

 xy=np.c_[u.loc[idx].geometry.representative_point().x,u.loc[idx].geometry.representative_point().y]
 block=np.floor(xy/2000).astype(int);_,block=np.unique(block,axis=0,return_inverse=True);blocks=np.unique(block);rng=np.random.default_rng(SEED)
 sims=[];boot=[]
 for it in range(30):
  chosen=rng.choice(blocks,size=max(2,int(.8*len(blocks))),replace=False);take=np.isin(block,chosen)
  cent,lab=fitkm(x[take],k0,SEED+500+it,starts=5)[1:]
  pred=distance.cdist(x,cent).argmin(1);pred=align(pred,base);boot.append(pred);sims.append({'replica':it+1,'blocos_mantidos':len(chosen),'setores_treino':int(take.sum()),'ARI':ari(base,pred),'mesmo_perfil_pct':100*np.mean(base==pred)})
 u['EST_BLOCOS']=np.nan;u.loc[idx,'EST_BLOCOS']=100*np.mean(np.array(boot)==base,axis=0)

 xc=x-x.mean(0);U,s,V=np.linalg.svd(xc,full_matrices=False);ev=s*s/(s*s).sum();pc=U[:,:2]*s[:2]
 if np.corrcoef(pc[:,0],base_scores)[0,1]<0:pc[:,0]*=-1;V[0]*=-1
 u['PC1']=np.nan;u['PC2']=np.nan;u.loc[idx,'PC1']=pc[:,0];u.loc[idx,'PC2']=pc[:,1]
 csv(pd.DataFrame({'variavel':FEATURES,'PC1':V[0],'PC2':V[1]}),'pca_cargas.csv')
 csv(pd.DataFrame({'componente':range(1,6),'variancia_explicada':ev}),'pca_variancia.csv')
 csv(pd.DataFrame(krows),'kmeans_todos_k.csv');csv(pd.DataFrame(scenario_rows),'cenarios_sensibilidade.csv');csv(pd.DataFrame(profiles),'perfis_cenarios.csv');csv(pd.DataFrame(sims),'estabilidade_blocos.csv')
 log('K_COMUM',k0);return u,k0,models,base,ev

# Queen
def queen(g):
 pairs=g.sindex.query(g.geometry,predicate='touches');n=len(g)
 w=csr_matrix((np.ones(pairs.shape[1]),(pairs[0],pairs[1])),shape=(n,n));w=w.maximum(w.T);w.setdiag(0);w.eliminate_zeros();return w

# Moran w
def moran_w(values,w,local=False,seed=SEED):
 good=np.asarray(w.sum(1)).ravel()>0;original=np.flatnonzero(good);w=w[good][:,good].tocsr();v=np.asarray(values)[good];n=len(v)
 if n<4 or v.std()==0:return {'n':n,'isolados':int((~good).sum()),'I':np.nan,'p':np.nan},None,original
 w=w.multiply(1/np.asarray(w.sum(1))).tocsr();z=(v-v.mean())/v.std();lag=w@z;I=float(z@lag/(z@z));expected=-1/(n-1);rng=np.random.default_rng(seed)
 ss=[]
 for _ in range(PERM):zp=rng.permutation(z);ss.append(zp@(w@zp)/(zp@zp))
 pv=(1+(np.abs(np.array(ss)-expected)>=abs(I-expected)).sum())/(PERM+1)
 rec={'n':n,'isolados':int((~good).sum()),'I':I,'p':pv,'permutacoes':PERM}
 if not local:return rec,None,original
 Ii=z*lag;p=np.empty(n)
 for i in range(n):
  start,end=w.indptr[i:i+2];ww=w.data[start:end];m=len(ww);draws=rng.integers(0,n-1,size=(PERM,m))
  for col in range(1,m):
   bad=(draws[:,col,None]==draws[:,:col]).any(1)
   while bad.any():draws[bad,col]=rng.integers(0,n-1,size=bad.sum());bad=(draws[:,col,None]==draws[:,:col]).any(1)
  draws+=draws>=i;sim=z[i]*(z[draws]@ww);ex=-z[i]*z[i]/(n-1);p[i]=(1+(np.abs(sim-ex)>=abs(Ii[i]-ex)).sum())/(PERM+1)
 q=bh(p);cl=np.where((z>=0)&(lag>=0),'HH',np.where((z<0)&(lag<0),'LL',np.where(z>=0,'HL','LH')));cl=np.where(q<=.05,cl,'NS')
 return rec,{'p':p,'q':q,'cluster':cl,'Ii':Ii},original

# Spatial
def spatial(c,u):
 extra=[x for x in u.columns if x not in c.columns and x!='geometry']

 a=c.merge(u[['setor_id',*extra]],on='setor_id',validate='many_to_one')
 rows=[];qcounts=[]
 for col in ['MQ_S0','MK_S0','MQ_S4','MQ_S8']:a[col]='ND'
 for basin,allg in a[a.elegivel].groupby('bas_id'):
  for var in ['I_S0','I_S1','I_S2','I_S3','I_S4','I_S5','I_S8',*FEATURES]:

   strict=var.startswith('I_') and var!='I_S8' or var=='sem_rede'
   g=allg[allg.ESG_OBS] if strict else allg
   xy=np.c_[g.geometry.representative_point().x,g.geometry.representative_point().y];qw=queen(g)
   for wname,ww in [('queen',qw),('knn8',weights(xy,8))] if var=='I_S0' else [('queen',qw)]:
    loc=(var=='I_S0') or (var in ['I_S4','I_S8'] and wname=='queen');rec,rr,ids=moran_w(g[var].to_numpy(),ww,local=loc);rows.append({'bacia':basin,'variavel':var,'vizinhos':wname,'exclui_esgoto_estimado':strict,**rec})
    if rr is not None:
     field={'I_S4':'MQ_S4','I_S8':'MQ_S8'}.get(var,'MQ_S0' if wname=='queen' else 'MK_S0');a.loc[g.index,field]='ISO';a.loc[g.index[ids],field]=rr['cluster'];a.loc[g.index[ids],field+'_Q']=rr['q']
     qcounts +=[{'bacia':basin,'mapa':field,'classe':cl,'n':int((a.loc[g.index,field]==cl).sum())} for cl in ['HH','LL','HL','LH','NS','ISO']]
  for k in [4,12]:
   g=allg[allg.ESG_OBS];xy=np.c_[g.geometry.representative_point().x,g.geometry.representative_point().y]
   rec,_,_=moran_w(g.I_S0.to_numpy(),weights(xy,k));rows.append({'bacia':basin,'variavel':'I_S0','vizinhos':f'knn{k}',**rec})
 csv(pd.DataFrame(rows),'moran_cenarios.csv');csv(pd.DataFrame(qcounts),'moran_classes.csv')
 gp(a,'setores_multivariada');gp(u,'unidades_ajuste')
 slim=a[['setor_id','bas_id',*[f'I_S{i}' for i in range(11)],*[f'K_S{i}' for i in range(11)],'EST_PESOS','EST_BLOCOS','ESG_EST','MQ_S0','MK_S0','MQ_S4','MQ_S8','geometry']].rename(columns={'setor_id':'CD_SETOR','bas_id':'BACIA'})
 gp(slim,'cenarios_setores',True);csv(pd.DataFrame(a.drop(columns='geometry')),'resultados_cenarios_setores.csv');return a

# Main
def main():
 u,c,b,h=assemble();x,valid=normalized(u);u,k0,models,base,ev=cluster(u,x,valid);a=spatial(c,u)
 meta={'gerado':datetime.datetime.now().astimezone().isoformat(),'semente':SEED,'inputs':FEATURES,'cenarios':SCENARIOS,'unidades':len(u),'elegiveis':int(valid.sum()),'k_base':k0,'bibliotecas':{'numpy':np.__version__,'pandas':pd.__version__,'geopandas':gpd.__version__,'scipy':__import__('scipy').__version__},'normalizacao':'log1p nas densidades; min-max fixo nos setores completos; sem percentis na análise principal','distancia_kmeans':'Euclidiana em X * sqrt(peso), peso 1 em cada variável no S0','pca_variancia':ev.tolist(),'moran':'queen e kNN simetrizado; 999 permutações; local condicional; BH/FDR 5% por bacia; ilhas explícitas','sih':'zeros representam ausência de atividade alocada da coorte registrada, não internação real nula; S4 retira essa variável','hidrologia':'relevo, vias e D8 são condicionantes/contexto, não indicadores de fonte somados ao índice'}
 meta['tratamento_lacunas']={'esgoto_publicado':int(u.ESG_OBS.sum()),'esgoto_estimado_matriz':int(u.ESG_EST.sum()),'setores_sem_uso_solo_valido':int((~valid).sum()),'regra':'Mediana do município e situação censitária; fallback municipal; limitada pelo percentual de rede direta publicado. Zero de pressão residencial somente com população e domicílios oficialmente nulos. Shapefiles censitários originais preservados.','sensibilidade':'S9/S10 usam limites inferior e superior; não são intervalos probabilísticos.','moran':'Índices com esgoto e componente sem_rede usam apenas esgoto publicado (ESG_OBS).'}
 (O/'auditoria/metodo_multivariada.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
 log('CONCLUIDO_MULTIVARIADA',O)
if __name__=='__main__':main()
