# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/entrega_final/00_documentacao/tabelas/kmeans_grade.csv | pd.read_csv.
# Entrada: E:/teco/entrega_final/00_documentacao/tabelas/cenarios_grade.csv | pd.read_csv.
# Entrada: E:/teco/entrega_final/00_documentacao/manifesto.json | mfile.read_text.
# Campos/chaves em best: cenario, k, menor_grupo, silhouette.
# Campos/chaves em table: ARI, cenario, descricao, k, menor_grupo, mesmo_grupo_pct, peso_aih_local, peso_populacao, peso_sem_rede, silhouette.
# Campos/chaves em x: ARI, cenario, mesmo_grupo_pct, peso_aih_local, peso_populacao, peso_sem_rede, silhouette.
# Saída: {directory}/Comparacao_kmeans_sensibilidade.json | .write_text.
# Saída: E:/teco/entrega_final/00_documentacao/Comparacao_kmeans_sensibilidade.csv | table.to_csv.
# Saída: E:/teco/entrega_final/00_documentacao/Comparacao_kmeans_sensibilidade.md | .write_text.
# Saída: E:/teco/entrega_final/00_documentacao/manifesto.json | mfile.write_text.
# Campos/chaves gerados em m: comparacao_kmeans_sensibilidade.
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
import json
import pandas as pd
R=Path(_cp_texto('', 'posix'));F=R/'entrega_final';D=F/'00_documentacao';T=D/'tabelas'
fits=pd.read_csv(T/'kmeans_grade.csv',sep=';',decimal=',');scenarios=pd.read_csv(T/'cenarios_grade.csv',sep=';',decimal=',')
best=fits.loc[fits.groupby('cenario').silhouette.idxmax()].copy();assert best.k.eq(2).all()
table=scenarios.merge(best[['cenario','k','silhouette','menor_grupo']],on='cenario',validate='one_to_one')
selected=table.loc[table.silhouette.idxmax()];assert selected.cenario=='S2'
records=table[['cenario','descricao','peso_populacao','peso_sem_rede','peso_aih_local','k','silhouette','ARI','mesmo_grupo_pct','menor_grupo']].to_dict('records')
text='Entre os cenários testados, S2 com dois grupos apresentou a maior silhouette (0,742), mantendo 98,3% das unidades no mesmo perfil de S0 e ARI de 0,932. S2 atribui pesos 1:3:1 a população, ausência de rede e internações locais. O cenário base S0, com pesos iguais, permanece como referência e apresentou silhouette de 0,668. Todos os cinco cenários selecionaram dois grupos entre as soluções com k de 2 a 6.'
limit='As silhouettes descrevem geometrias de distâncias alteradas pelos pesos. O maior valor em S2 indica maior separação sob a ênfase em ausência de rede, não comprova maior acurácia ambiental ou sanitária. A escolha de um peso três vezes maior exige justificativa substantiva; por isso S2 é mantido como sensibilidade e S0 como referência.'
data={'resultado':text,'interpretacao':limit,'numero_unidades_validas':592,'unidades_alteradas_S2':10,'referencia':'S0','maior_separacao':'S2','melhor_k_em_todos_cenarios':2,'comparacao':records}
for directory in [D,R/'output/04_grade_500m/auditoria']:(directory/'Comparacao_kmeans_sensibilidade.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
table.to_csv(D/'Comparacao_kmeans_sensibilidade.csv',sep=';',decimal=',',index=False,encoding='utf-8-sig')
lines=['# K-means e sensibilidade: seleção e interpretação','',text,'',limit,'','| Cenário | Pesos população / sem rede / AIH | k | Silhouette | Mesmo perfil de S0 | ARI |','|---|---|---:|---:|---:|---:|']
for x in records:
 fmt=lambda n,d:f'{n:.{d}f}'.replace('.',',')
 lines.append('| '+x['cenario']+' | '+str(int(x['peso_populacao']))+' / '+str(int(x['peso_sem_rede']))+' / '+str(int(x['peso_aih_local']))+' | 2 | '+fmt(x['silhouette'],3)+' | '+fmt(x['mesmo_grupo_pct'],1)+'% | '+fmt(x['ARI'],3)+' |')
lines+=['','Silhouette não é valor de p. ARI compara duas partições, corrigindo a concordância esperada ao acaso; 1 indica partições iguais. A concordância percentual considera rótulos alinhados. Os grupos não são níveis de risco.']
(D/'Comparacao_kmeans_sensibilidade.md').write_text('\n'.join(lines),encoding='utf8')
mfile=D/'manifesto.json';m=json.loads(mfile.read_text('utf8'));m['comparacao_kmeans_sensibilidade']=data;mfile.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8');print(text,flush=True)
