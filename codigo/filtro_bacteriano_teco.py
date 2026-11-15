# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/teco/output/04_grade_500m/tabelas/sih_cid10_mensal.csv | pd.read_csv.
# Entrada: E:/teco/dados_publicos/saude_revisao/CID10_oficial_GO.json | .read_text.
# Campos/chaves em a: code, display.
# Campos/chaves em official: concept.
# Campos/chaves em f: CID10, diagnostico.
# Campos/chaves em filt: CID10, diagnostico, grupo_para_revisao, incluir, justificativa, nivel_etiologico.
# Campos/chaves em selected.loc: internacoes.
# Campos/chaves em selected: incluir.
# Saída: E:/teco/output/04_grade_500m/filtro_cid10.csv | .to_csv.
# Saída: E:/teco/output/04_grade_500m/tabelas/classificacao_cid_bacteriana.csv | filt.to_csv.
# Saída: E:/teco/output/04_grade_500m/tabelas/sih_resumo_etiologico.csv | .to_csv.
# Saída: E:/teco/output/04_grade_500m/tabelas/regras_filtro_bacteriano.csv | .to_csv.
# Saída: E:/teco/output/04_grade_500m/auditoria/filtro_bacteriano.json | .write_text.
# Campos/chaves gerados em filt: diagnostico, grupo_para_revisao, incluir, justificativa, nivel_etiologico.
# CID10: código de diagnóstico.
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
import json,re,unicodedata
import pandas as pd
R=Path(_cp_texto('', 'posix'));O=R/'output/04_grade_500m';T=O/'tabelas'
SOURCE='https://fhir.saude.go.gov.br/r4/reds-go/CodeSystem-BRCID10.html'
RULES=[]

# Rule
def rule(tier,label,prefixes,exclude=()):
 RULES.append((tier,label,tuple(prefixes.split()),tuple(exclude)))

# Nums
def nums(letter,a,b):return ' '.join(f'{letter}{i:02d}' for i in range(a,b+1))
rule('A','Infecções intestinais bacterianas',nums('A',0,5))
rule('A','Tuberculose, zoonoses e outras infecções bacterianas',nums('A',15,58))
rule('A','Espiroquetas, clamídias e riquétsias',nums('A',65,79))
rule('A','HIV com infecção bacteriana registrada','B200 B201')
rule('A','Agente bacteriano em doença classificada em outra parte','B95 B96')
rule('A','Sistema nervoso: etiologia bacteriana codificada','G00 G01 G042 G050')
rule('A','Manifestações bacterianas em outros órgãos','I320 I410 J13 J14 J15 J160 J170 J200 J201 J202 J020 J030 M010 M011 M012 M013 M014 M630 M680 N160 N740 N741 N743 N744')
rule('A','Infecção bacteriana neonatal codificada','P231 P232 P233 P234 P235 P236 P36 P370 P372')
rule('B','Gastroenterite/infecção sem agente especificado','A085 A09 B99')
rule('B','Abscessos e infecções neurológicas sem agente definido','G03 G048 G049 G06 G07',('G030',))
rule('B','Infecções oculares compatíveis','H000 H043 H044 H050 H100 H102 H103 H104 H108 H109 H160 H440 H441')
rule('B','Infecções de ouvido/mastoide compatíveis','H600 H601 H602 H603 H608 H609 H65 H66 H67 H70 H750')
rule('B','Endocardite e pericardite infecciosas ou sem etiologia','I301 I33 I38 I39')
rule('B','Infecções respiratórias de etiologia não definida','J01 J02 J03 J04 J051 J06 J168 J178 J18 J208 J209 J22 J32 J350 J36 J390 J391 J440 J85 J86')
rule('B','Infecções odontogênicas e de glândulas salivares','K04 K05 K112 K113 K122')
rule('B','Infecção/abscesso/peritonite abdominal compatível','K350 K351 K570 K572 K574 K578 K61 K630 K65 K670 K671 K672 K673 K674 K678 K750 K810 K830 K800 K801 K803 K804')
rule('B','Pele e tecido subcutâneo','L00 L01 L02 L03 L04 L050 L08 L303')
rule('B','Infecções osteoarticulares e de partes moles','M00 M018 M462 M463 M464 M465 M600 M650 M651 M710 M711 M726 M86 M900 M901 M902')
rule('B','Infecções urinárias/renais compatíveis','N10 N11 N12 N136 N151 N300 N302 N308 N309 N340 N341 N342 N390')
rule('B','Infecções genitais/mamárias compatíveis','A64 N41 N431 N45 N481 N49 N51 N61 N70 N71 N72 N73 N748 N751 N760 N761 N762 N763 N764')
rule('B','Infecção na gestação, parto ou puerpério','O030 O035 O040 O045 O050 O055 O060 O065 O070 O075 O080 O23 O411 O753 O85 O86 O91 O983 O988 O989')
rule('B','Infecções neonatais sem agente definido','P238 P239 P38 P39')
rule('B','Infecção após procedimento, dispositivo ou trauma','T793 T802 T814 T826 T827 T835 T836 T845 T846 T847 T857 T874 T880')
rule('B','Choque séptico ou resposta inflamatória com infecção','R572 R650 R651')

rule('C','Sequelas bacterianas ou associação sem infecção ativa documentada','B90 B92 I00 I01 I02 K25 K26 K27 K28 D593 Z220 Z221 Z222 Z223')

# Classify
def classify(code,description=''):
 code=str(code).replace('.','').upper().strip()
 text=unicodedata.normalize('NFKD',description).encode('ascii','ignore').decode().lower()

 if re.search(r'viral|virus|micose|fung|candida|ameb|protozo|toxoplas|helmint|esquistossom',text) and not re.search(r'bacter|estreptoc|estafiloc|gonoc|meningoc',text):
  return 'Fora','Etiologia não bacteriana explicitada',False
 for tier,label,pre,exc in RULES:
  if code.startswith(pre) and not code.startswith(exc):return tier,label,tier in ['A','B']
 if re.search(r'bacterian|estreptoc|estafiloc|gonococ|meningococ|pneumococ|escherichia|clostrid|salmonel|shigel|chlamydia|clamidia|sifilis|tuberculos|hanseniase|ricketts|riquets',text):
  return 'A','Etiologia bacteriana identificada na descrição oficial',True
 return 'Fora','Sem infecção bacteriana ou síndrome elegível no diagnóstico principal',False

# Main
def main():
 f=pd.read_csv(T/'sih_cid10_mensal.csv',sep=';',dtype={'CNES':str,'CID10':str})
 official=json.loads((R/'dados_publicos/saude_revisao/CID10_oficial_GO.json').read_text('utf8'))
 desc={a['code'].replace('.',''):a['display'] for a in official['concept']}
 filt=f[['CID10','diagnostico']].drop_duplicates('CID10').sort_values('CID10').copy()
 filt['diagnostico']=[desc.get(c,d) for c,d in zip(filt.CID10,filt.diagnostico)]
 results=[classify(c,d) for c,d in zip(filt.CID10,filt.diagnostico)]
 filt['nivel_etiologico']=[x[0] for x in results];filt['grupo_para_revisao']=[x[1] for x in results];filt['incluir']=[x[2] for x in results]
 explanations={'A':'Doença/agente bacteriano codificado; não equivale a cultura positiva nem resistência confirmada.','B':'Síndrome infecciosa compatível: pode ter causa bacteriana, mas a CID principal não confirma o agente.','C':'Condição associada, sequela ou portador; separada do índice principal de infecções ativas.','Fora':'Excluído do filtro operacional: ausência de síndrome elegível ou etiologia não bacteriana explícita.'}
 filt['justificativa']=filt.nivel_etiologico.map(explanations)
 filt[['CID10','diagnostico','grupo_para_revisao','incluir','justificativa','nivel_etiologico']].to_csv(O/'filtro_cid10.csv',sep=';',index=False,encoding='utf-8-sig')
 filt.to_csv(T/'classificacao_cid_bacteriana.csv',sep=';',index=False,encoding='utf-8-sig')
 selected=f.merge(filt[['CID10','nivel_etiologico','incluir']],on='CID10',validate='many_to_one')
 selected.groupby(['CNES','unidade','nivel_etiologico'],as_index=False).internacoes.sum().to_csv(T/'sih_resumo_etiologico.csv',sep=';',index=False,encoding='utf-8-sig')
 pd.DataFrame([{'nivel':t,'grupo':n,'prefixos':' '.join(p),'excecoes':' '.join(e),'fonte':SOURCE} for t,n,p,e in RULES]).to_csv(T/'regras_filtro_bacteriano.csv',sep=';',index=False,encoding='utf-8-sig')
 info={'data':'2026-11-12','fonte_cid':SOURCE,'criterio':'A+B: etiologia bacteriana codificada e síndromes infecciosas compatíveis; C separado, sem incluir comorbidades isoladas.','CID_selecionados':int(filt.incluir.sum()),'CID_por_nivel':filt.nivel_etiologico.value_counts().to_dict(),'AIH_selecionadas':int(selected.loc[selected.incluir,'internacoes'].sum()),'AIH_por_nivel':selected.groupby('nivel_etiologico').internacoes.sum().to_dict(),'limitacao':'Diagnóstico principal; sem confirmação de agente, RAM ou residência atendida. Não inclui SIA/e-SUS.'}
 (O/'auditoria/filtro_bacteriano.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(info,ensure_ascii=True),flush=True)
if __name__=='__main__':main()
