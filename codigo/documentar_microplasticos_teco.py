# ENTRADAS: output/07_microplasticos/auditoria/metodo_microplasticos.json e tabelas; figuras PNG do mesmo módulo.
# SAÍDAS: entrega_final/00_documentacao/Microplasticos/Relatorio_ARG_microplasticos.md, .html e .pdf; guia de códigos do módulo.
# CAMINHOS: TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json; executar com reportlab instalado, sem necessidade de QGIS.
from pathlib import Path
import json,csv,html,re,shutil,sys
from caminhos_teco import raiz_projeto
R=raiz_projeto();O=R/'output/07_microplasticos';D=R/'entrega_final/00_documentacao/Microplasticos';D.mkdir(parents=True,exist_ok=True)
meta=json.loads((O/'auditoria/metodo_microplasticos.json').read_text('utf8'))

# Tabelas e estilo
def read(name):
 with (O/'tabelas'/f'{name}.csv').open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def n(x,p=2):return f'{float(x):,.{p}f}'.replace(',','X').replace('.',',').replace('X','.')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)+'\n'
NAMES={'pampulha':'Pampulha','vargem_flores':'Vargem das Flores','ibirite_regap':'Ibirité / REGAP'}
CSS='body{font:16px/1.65 Arial,sans-serif;color:#203e49;margin:0;background:#f0f4f3}main{max-width:1140px;margin:auto;padding:28px}h1{font-size:32px;line-height:1.2}h2{margin-top:35px;color:#185b64}h3{color:#395962}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:9px;border-bottom:1px solid #cedcdb;text-align:left;vertical-align:top}th{background:#e0eeee}img{width:100%;height:auto;background:white}figure{margin:25px 0}figcaption{font-size:14px}a{color:#146d7f}pre{padding:18px;background:#173641;color:#eef5f5;overflow:auto;white-space:pre-wrap}section{background:white;padding:22px;margin:20px 0;border-radius:10px}p{margin:12px 0}nav{display:flex;gap:12px;flex-wrap:wrap}.muted{color:#637a81}'

# Texto metodológico e resultados
def text():
 waste=read('residuos_por_bacia');profiles=read('perfis_kmeans');sens=read('sensibilidade_pesos');moran=[x for x in read('moran_global') if x['theme']=='microplastics']
 wrows=[[NAMES[x['BACIA']],n(x['HH_TOTAL_AL'],0),n(x['WASTE_LO'],3)+'–'+n(x['WASTE_HI'],3)+'%'] for x in waste]
 prows=[[x['MP_K'],x['n'],n(x['POP_DENS'],1),n(x['SEWER_DENS'],1),n(x['WASTE_DENS'],2),n(x['ROAD_DENS'],2),n(x['MP_INDEX'],1)] for x in profiles]
 srows=[[x['scenario'],x['weights'],x['k'],n(x['silhouette'],3),n(x['ARI_base'],3),n(x['rho_score'],3)] for x in sens]
 mrows=[[NAMES[x['basin']],x['n'],n(x['I'],3),n(x['p'],3)] for x in moran]
 return f'''# Pressões potenciais de genes de resistência e microplásticos

Complementação metodológica e resultados exploratórios. Bacias de Pampulha, Vargem das Flores e Ibirité / REGAP. Atualização em 16/11/2026. Responsável cartográfica: Brentano, M. C. B.

## 1. O que esta complementação permite avaliar

A ampliação reúne duas avaliações independentes sobre uma base territorial comum. A primeira preserva a avaliação de pressão antrópica relacionada aos genes de resistência a antimicrobianos (ARG, do inglês antimicrobial resistance genes). A segunda organiza indicadores de fontes potenciais de microplásticos. As duas permitem selecionar áreas para investigação, mas não estimam concentração, carga transportada, risco sanitário ou probabilidade de ocorrência. Uma mancha de alta pressão é uma hipótese espacial a confrontar com as amostras do estudo.

A base comum descreve onde há população e ocupação, como o relevo organiza a drenagem e onde estão o reservatório, os cursos d'água e as vias. Os indicadores específicos descrevem atividades humanas e condições de manejo. Essa separação evita tratar uma variável de transporte, como declividade, como se ela produzisse contaminantes. Também evita atribuir a uma internação uma ocorrência de resistência que não foi medida.

O quadro final não soma os dois índices. Uma região pode ter maior pressão em apenas um tema ou em ambos. A concordância entre mapas será discutida como compartilhamento de condições territoriais, e não como demonstração de associação entre ARG e microplásticos. A avaliação de coocorrência dependerá das medições nos reservatórios e de um desenho amostral compatível.

## 2. Base comum e entradas específicas

{table(['Componente','Uso na avaliação','Decisão desta versão'],[
['População Censo 2022','Indicador de atividade doméstica e urbanização','Densidade no índice MP e na base ARG; sensibilidade retira população do MP.'],
['Destino do esgoto Censo 2022','Conexão domiciliar e possível via de aporte de efluentes','ARG preserva percentual anterior; MP usa densidade de domicílios sem conexão geral/pluvial.'],
['Destino do lixo Censo 2022','Pressão de manejo domiciliar inadequado','MP usa domicílios sem coleta por km²; mapa nativo mostra percentual por setor.'],
['Vias cadastradas','Contexto urbano e superfície potencialmente geradora de partículas','MP usa km de via/km²; não há tráfego, desgaste ou carga de partículas observada.'],
['Uso do solo 2025','Urbanização, cobertura e contexto de escoamento','Permanece como camada comum complementar; não duplica população/vias no índice MP.'],
['Relevo, declividade e hidrografia','Conectividade topográfica candidata','Fora do índice gerador; utilizados na leitura de caminhos D8.'],
['Internações e estabelecimentos','Atividade assistencial local','Somente ARG; internação não é prevalência de resistência nem origem residencial.'],
['Licenciamento e instalações de resíduos','Triagem de atividades e alternativas documentadas de gestão','Camadas específicas MP; sem peso enquanto cobertura municipal e operação não forem verificadas.']])}

A literatura sustenta a investigação de escoamento urbano e efluentes como rotas de microplásticos, incluindo superfícies viárias e atividades domésticas. Lindfors et al. (2025) compararam superfícies urbanas, enquanto Imbulana, Tanaka e Oluwoye (2024) distinguiram escoamento e efluentes em uma bacia urbana. Esses estudos fundamentam a escolha dos mecanismos a investigar. Seus coeficientes e participações não foram transferidos para as bacias mineiras.

## 3. Bases obtidas e como foram tratadas

### 3.1 Destino do lixo no Censo 2022

Foi aproveitado o CSV domiciliar já existente em saneamento_ibge, com o código do setor e as variáveis V00397 a V00402. V00397 representa coleta no domicílio pelo serviço de limpeza e V00398, depósito em caçamba desse serviço. V00399 a V00402 representam queima, enterramento, descarte em terreno/encosta/área pública e outros destinos. O denominador é o total de domicílios particulares permanentes ocupados, preservado da base censitária anterior.

As contagens originais permanecem referidas ao setor inteiro, embora a geometria da camada seja o recorte pela bacia. ORIG_KM2 informa a área original e PART_KM2 informa o recorte. Para estimar a parcela dentro da bacia, a contagem é multiplicada pela razão entre a área recortada e a área original. Trata-se de alocação proporcional, com distribuição homogênea assumida dentro do setor. Não é uma contagem observada das casas localizadas no recorte.

O marcador X significa sigilo. Ele não foi convertido em zero. Quando a soma conhecida das duas formas de coleta permite obter o total combinado sem coleta, utiliza-se o complemento do denominador, sem reconstruir cada categoria sigilosa. Nos demais casos, o limite inferior soma as categorias não coletadas conhecidas e o superior é o total menos as categorias coletadas conhecidas. O ponto médio representa uma hipótese central explícita. Os limites seguem para o teste de sensibilidade. Registros inexistentes, denominadores incompatíveis e setores sem domicílios não recebem um percentual artificial.

{table(['Bacia','Domicílios alocados à bacia (estimativa)','Sem coleta: intervalo agregado'],wrows)}

Os totais acima são agregados uma única vez pelos recortes dos setores. Não foram somados os círculos de 500 m, pois eles se sobrepõem. O percentual global baixo pode coexistir com bolsões locais sem coleta. Também não significa que todo domicílio coletado tenha destinação final ambientalmente adequada, nem que toda ausência de coleta gere microplásticos.

### 3.2 IDE-Sisema, licenças e instalações

A consulta WFS da IDE-Sisema utilizou EPSG:31983 e o envelope das três bacias acrescido de 20 km para contexto regional. Foram obtidas licenças SLA, cadastro histórico estadual 2013–2019, aterros sanitários, transbordo, disposição precária, planos municipais e competência municipal de licenciamento. URLs, arquivos, data e SHA-256 constam no manifesto de downloads. Os registros com CPF e nomes de pessoas permanecem apenas nos originais locais. As camadas derivadas usam identificadores genéricos, processo e atividade.

Há {meta['licencas_bacias']} registros de processos dentro das bacias, não necessariamente {meta['licencas_bacias']} estabelecimentos diferentes. A triagem encontrou {meta['licencas_candidatas']} descrições diretamente relacionadas a plásticos: moldagem de termoplástico e reciclagem a seco, ambas no cadastro histórico. Elas são pistas para leitura do processo. Não confirmam atividade atual, lançamento ou quantidade emitida. O cadastro SLA tem apenas oito registros internos e o histórico, 41; a cobertura não inclui necessariamente os processos municipais ou atividades secundárias.

As instalações de resíduos são apresentadas como contexto de gestão. O recorte regional contém {meta['instalacoes_regionais']} registros de aterro/transbordo, dos quais {meta['instalacoes_bacias']} intersecta as bacias. A ausência de um ponto de lixão na consulta não comprova inexistência de descarte clandestino. Uma instalação regularizada não recebe automaticamente um valor de pressão ou de mitigação: são necessários situação operacional, resíduos aceitos, capacidade e destino real dos resíduos gerados na bacia.

### 3.3 SINIR e informação municipal

Foram baixados os relatórios públicos SINIR de 2024 e 2025. A versão de exercício 2025 informa ano de referência 2024. O recorte técnico inclui diagnóstico, passivos e soluções compartilhadas dos municípios encontrados no recorte territorial; a presença varia entre módulos. Nesta extração foram encontrados registros de {', '.join(meta['municipios_sinir'])}. Um município sem registro na exportação não recebeu valor zero. Os arquivos municipais têm linhas repetidas por meta e composição, portanto não se deve somar a massa por todas as linhas como se cada linha fosse uma coleta independente.

O cadastro estadual de planos de 2024 complementa a leitura municipal. Existência de plano e de coleta seletiva não equivale a cobertura percentual ou desempenho. Esses atributos administrativos não foram replicados como medições independentes em cada célula de 500 m.

## 4. Como funciona a classificação de microplásticos

### 4.1 Suporte espacial e elegibilidade

Os círculos de raio 500 m são as vizinhanças de cálculo já utilizadas no projeto. Cada círculo é recortado pela bacia. Os resultados são exibidos em hexágonos sem sobreposição, que não são a área usada no denominador. A chave é GRID_ID junto com BACIA, porque um centro pode originar dois fragmentos em bacias diferentes.

Das {meta['n_total']} unidades bacia/vizinhança, {meta['n_valid']} foram elegíveis. As seis lacunas da avaliação anterior permanecem. Quatro unidades adicionais não têm domicílios no suporte censitário utilizado, de modo que o percentual de coleta não pode ser calculado. Essas dez unidades permanecem identificadas como informação insuficiente. Não foi criada continuidade artificial por interpolação; a água continua representada como reservatório.

### 4.2 Critérios, normalização e pesos

O cenário S0 usa quatro critérios: densidade populacional; densidade de domicílios sem conexão à rede geral/pluvial; densidade de domicílios sem coleta; densidade de vias cadastradas. As duas densidades domiciliares evitam que uma área quase desabitada se destaque apenas por apresentar um alto percentual de déficit. O esgotamento conserva as hipóteses de lacunas da base anterior. Ausência de conexão não demonstra ausência de tratamento individual.

Aplica-se log1p a cada densidade e, depois, min-max com os extremos do conjunto elegível das três bacias. Os mesmos extremos são usados em todos os cenários. Essa transformação reduz a influência de caudas longas e preserva a ordem, mas não transforma as entradas em taxas de emissão equivalentes. O índice é I = 100 × soma(wj × zj) / soma(wj), com zj entre zero e um. Em S0, todos os pesos valem um.

As classes fixas são muito baixa (0–20), baixa (>20–40), moderada (>40–60), alta (>60–80) e muito alta (>80–100). São faixas exploratórias, não limites legais ou sanitários. O mapa em quintis é mantido como leitura relativa separada: até P20, >P20–P40, >P40–P60, >P60–P80 e >P80. Quintis podem separar regiões pouco diferentes e não demonstram uma ruptura física no transporte.

### 4.3 Cenários e estabilidade

S1 triplica o peso de domicílios sem coleta, S2 triplica vias, S3 triplica domicílios sem rede e S4 retira população. S4 testa parte da redundância entre adensamento e infraestrutura. A matriz de correlação de Spearman acompanha os resultados. Os critérios não são estatisticamente independentes, e a correlação deve ser discutida como limitação do índice composto.

{table(['Cenário','Pesos: pop/rede/lixo/vias','Melhor K','Silhouette','ARI com S0 (K fixo)','Rho do índice'],srows)}

A concordância de perfis no mapa é a proporção dos cinco cenários que preserva o grupo de S0 após alinhar os rótulos. Ela inclui o próprio S0, portanto não pode ser lida como probabilidade e não será menor que 20%. O ARI compara partições como um todo, corrigindo parte da concordância ao acaso. A correlação de Spearman compara a ordenação dos índices, e pode continuar alta mesmo quando algumas fronteiras dos grupos mudam. Os limites inferior e superior do lixo também foram propagados ao índice, com os extremos centrais fixos e truncamento no intervalo normalizado. Esse intervalo representa apenas a incerteza associada ao sigilo do lixo.

### 4.4 K-means: o que os perfis significam

O k-means recebe as quatro entradas normalizadas, e não apenas o índice médio. As colunas são multiplicadas pela raiz quadrada dos pesos normalizados, de modo que a distância euclidiana quadrática reflita os pesos. Foram testados K=2 a K=6, com 20 inicializações por combinação e semente fixa. A implementação usa scipy.cluster.vq.kmeans2 por meio da função fitkm já existente no projeto.

O cenário de pesos iguais selecionou K={meta['k_reference']} pela maior silhouette entre os K testados, com valor {n(meta['silhouette'],3)}. Esse resultado indica separação interna moderada dos perfis neste conjunto. Não é um p-valor e não valida a ocorrência de microplásticos. O K é mantido igual ao de S0 na comparação entre cenários, mesmo quando um cenário tem outro K preferido. Um peso não é considerado correto apenas por produzir silhouette maior.

{table(['Perfil','Unidades','Pop./km²','Sem rede/km²','Sem coleta/km²','Vias km/km²','Índice mediano'],prows)}

Os números acima são medianas das entradas, não cargas físicas. O perfil 1 agrupa, em geral, vizinhanças menos adensadas e com menor densidade viária. O perfil 2 apresenta maior adensamento e infraestrutura viária. Nenhum dos dois deve ser chamado de fonte comprovada ou região contaminada. As classes do índice fornecem intensidade relativa; os perfis do k-means descrevem combinações de variáveis, e por isso as duas saídas não são intercambiáveis.

### 4.5 Moran: associação espacial e não transporte

O Moran global e local foi calculado separadamente em cada bacia. A matriz espacial conecta os oito centros elegíveis mais próximos, é simetrizada e padronizada por linha. O Moran utiliza o índice MP_INDEX; o k-means utiliza a matriz de quatro entradas. Foram feitas 999 permutações, com pseudo-p bilateral. No teste local foi aplicada correção Benjamini-Hochberg a 5% dentro de cada bacia e tema.

{table(['Bacia','Unidades elegíveis','Moran I','Pseudo-p global'],mrows)}

HH significa índice acima da média da bacia cercado por vizinhança também alta; LL representa associação baixa-baixa. HL e LH são contrastes locais. NS indica que o teste não permaneceu significativo após correção, e não ausência de pressão. ND representa falta de entrada. Como os círculos de 500 m se sobrepõem, parte da continuidade pode decorrer do próprio suporte de cálculo. A significância é exploratória e não deve ser apresentada como evidência independente do processo hidrológico. O teste não descobre sozinho o caminho de uma partícula.

## 5. Rotas candidatas até o reservatório

A direção D8 vem dos rasters hidrológicos já existentes. Cada pixel envia o fluxo para um dos oito vizinhos. Nesta etapa, rasteriza-se o índice de cada hexágono sobre a grade de 30 m, soma-se índice × área terrestre contribuinte e divide-se pela área válida acumulada a montante. A água não gera pressão e interrompe a trajetória. Os arquivos contributing_km2 e upstream_pressure são distintos: o primeiro informa área válida conectada; o segundo, a média ponderada do índice nessa área.

O D8 organiza caminhos topográficos candidatos. Não inclui galeria pluvial, rede de esgoto, canalização subterrânea, retenção por vegetação, sorção, ressuspensão, chuva, vazão ou transporte de polímeros. A malha viária é uma fonte potencial e referência urbana; ela não foi queimada no MDE para forçar escoamento. Os caminhos não são probabilidades calibradas. Para decidir quais vias realmente drenam para um curso d'água, o próximo dado mais útil é a localização de bocas de lobo, galerias e lançamentos pluviais.

As três execuções foram verificadas quanto a pixels finitos e ciclos no grafo D8. A ausência de ciclos garante a consistência do processamento topológico, mas não valida a delimitação hidrológica contra observações de campo. Os índices anteriores de ARG foram preservados sem alterações; a conexão topográfica de MP utiliza seu próprio índice.

## 6. O que obter a seguir, sem ampliar excessivamente o modelo

{table(['Prioridade','Informação','Como obter e tratar'],[
['1','Licenças municipais de atividades plásticas, borracha, têxteis e lavanderias','Consultar PBH e o SILO de Contagem; solicitar aos demais municípios planilha de processos com atividade, situação, endereço/coordenada e validade. Geocodificar só quando não houver coordenada e informar precisão. Ler pareceres antes de converter ponto em critério.'],
['1','Descarte irregular e limpeza urbana','Solicitar ao serviço municipal pontos georreferenciados e datas de vistorias, remoção de resíduos, material e recorrência. Não usar denúncia isolada como carga.'],
['1','Drenagem e lançamentos pluviais','Solicitar bocas de lobo, galerias, canais e exutórios; conectar as rotas ao sistema real, mantendo alternativa D8.'],
['2','Destino real dos resíduos e unidades de triagem','Cruzar plano/SINIR com contratos e situação operacional de aterros, cooperativas e triagem. Usar como contexto de gestão, sem descontar automaticamente o índice local.'],
['2','Tráfego das vias principais','Obter contagens oficiais ou hierarquia auditada; substituir a densidade geométrica somente se houver cobertura comparável.'],
['2','Resultados amostrais do estudo','Relacionar ponto, data, método, tamanho detectável e tipo de polímero às hipóteses espaciais. Não calibrar e validar nos mesmos poucos pontos sem teste independente.']])}

Para o licenciamento estadual, abrir a IDE-Sisema e habilitar licenças SLA e histórico. Consultar o processo no acesso visitante do SLA ou no SIAM e conferir atividades secundárias, drenagem, resíduos e destinação. Para BH, o licenciamento ambiental deve ser distinguido do urbanístico. Para Contagem, o SILO oferece consulta de processos e licenças emitidas. Quando não houver exportação aberta, solicitar à secretaria municipal um recorte das oito municipalidades que intersectam as bacias: Belo Horizonte, Betim, Brumadinho, Contagem, Ibirité, Sarzedo, Ribeirão das Neves e Esmeraldas. A busca não deve se limitar aos municípios que dão nome aos reservatórios.

O pacote não adiciona medicamentos vendidos, doenças ou estabelecimentos de saúde ao índice de MP. Também não adiciona todas as categorias de uso do solo como novos critérios. A proposta permanece com quatro critérios e camadas auxiliares, reduzindo redundância e a aparência de precisão de um modelo com muitos pesos ainda não calibrados.

## 7. Arquivos e reprodução

Os originais baixados estão em dados_publicos/residuos_licenciamento/originais; o manifesto está na pasta imediatamente superior. As entradas tratadas ficam em entrega_final/01_entradas/18_residuos e 19_licenciamento. O resultado MP fica em entrega_final/02_saidas/06_microplasticos; cada pasta de camada contém um único shapefile e campos.csv. Os testes S0–S4 têm suas próprias pastas. Rasters, tabelas, dicionários, auditoria e mapas triplos são entregues separadamente. O relatório complementa, sem substituir, o relatório ARG anterior.

Os scripts novos têm configuração inicial de entradas, campos e saídas e aceitam TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json. Config/microplasticos.json define critérios, transformações e pesos. Adicionar uma variável exige também programar sua agregação por círculo e auditar unidade, cobertura e direção de influência. Inserir um arquivo no diretório não basta para incorporá-lo ao índice.

## 8. Referências e fontes para consulta

- IBGE. Censo Demográfico 2022, agregados por setores, características dos domicílios e dicionário disponibilizados na pasta saneamento_ibge. https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html?edicao=41852&t=downloads
- IDE-Sisema. Serviços geográficos e metadados das camadas consultadas em 16/11/2026. https://geoportal.meioambiente.mg.gov.br/webservices
- MMA. Sistema Nacional de Informações sobre a Gestão dos Resíduos Sólidos, SINIR. Catálogo e exportações públicas, exercício 2025, referência 2024. https://dados.mma.gov.br/dataset/sinir
- Lindfors, S. et al. (2025). Microplastics and tyre wear particles in urban runoff from different urban surfaces. Science of the Total Environment, 980, 179527. https://doi.org/10.1016/j.scitotenv.2025.179527
- Imbulana, S.; Tanaka, S.; Oluwoye, I. (2024). Quantifying annual microplastic emissions of an urban catchment: Surface runoff vs wastewater sources. Journal of Environmental Management, 360, 121123. https://doi.org/10.1016/j.jenvman.2024.121123
- Swedish Environmental Protection Agency (2023). Urban Plastics, Report 7104. Rotas e gestão de partículas plásticas urbanas. https://www.naturvardsverket.se/4ace1d/globalassets/media/publikationer-pdf/7100/978-91-620-7104-2.pdf
- OECD/JRC (2008). Handbook on Constructing Composite Indicators. Discussão de normalização, pesos, redundância e sensibilidade. https://doi.org/10.1787/9789264043466-en
- Anselin, L. (1995). Local Indicators of Spatial Association - LISA. Geographical Analysis, 27, 93–115. https://doi.org/10.1111/j.1538-4632.1995.tb00338.x
- Rousseeuw, P. J. (1987). Silhouettes: a graphical aid to the interpretation and validation of cluster analysis. Journal of Computational and Applied Mathematics, 20, 53–65. https://doi.org/10.1016/0377-0427(87)90125-7
- PBH. Licenciamento ambiental. https://prefeitura.pbh.gov.br/meio-ambiente/licenciamento-ambiental
- Contagem. Sistema de Licenciamento Online, SILO. https://alvaras.contagem.mg.gov.br/
'''

# Conversão de texto e figuras
def inline(s):
 s=html.escape(s);s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s);return re.sub(r'(https?://[^\s<]+)',r'<a href="\1">\1</a>',s)
def html_body(md):
 lines=md.splitlines();out=[];i=0
 while i<len(lines):
  s=lines[i]
  if not s:i+=1;continue
  if s.startswith('| '):
   rows=[]
   while i<len(lines) and lines[i].startswith('|'):
    if not set(lines[i].replace('|','').strip())<=set('-: '):rows.append([v.strip() for v in lines[i].strip('|').split('|')])
    i+=1
   out.append('<table>'+''.join('<tr>'+''.join(f'<{"th" if j==0 else "td"}>{inline(v)}</{"th" if j==0 else "td"}>' for v in row)+'</tr>' for j,row in enumerate(rows))+'</table>');continue
  if s.startswith('#'):
   k=len(s)-len(s.lstrip('#'));out.append(f'<h{k}>{inline(s[k:].strip())}</h{k}>')
  elif s.startswith('- '):out.append('<p>• '+inline(s[2:])+'</p>')
  else:out.append('<p>'+inline(s)+'</p>')
  i+=1
 return '\n'.join(out)

# PDF com pranchas em página horizontal
def pdf(md,gallery):
 from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,Table,TableStyle,PageBreak,NextPageTemplate,Image,KeepTogether
 from reportlab.lib import colors
 from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
 from reportlab.lib.pagesizes import A4,landscape
 from reportlab.lib.units import mm
 from reportlab.pdfbase import pdfmetrics
 from reportlab.pdfbase.ttfonts import TTFont
 for name,file in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
 styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='TextTECO',fontName='Arial',fontSize=10,leading=14,spaceAfter=8,textColor=colors.HexColor('#203e49')));styles.add(ParagraphStyle(name='CellTECO',parent=styles['TextTECO'],fontSize=7.6,leading=10,spaceAfter=0))
 for k in ['Title','Heading1','Heading2','Heading3']:styles[k].fontName='Arial-Bold';styles[k].textColor=colors.HexColor('#205564')
 doc=BaseDocTemplate(str(D/'Relatorio_ARG_microplasticos.pdf'),pagesize=A4,leftMargin=19*mm,rightMargin=19*mm,topMargin=20*mm,bottomMargin=18*mm)
 def foot(c,d):
  w,h=c._pagesize;c.setFont('Arial',8);c.setFillColor(colors.HexColor('#657e84'));c.drawString(19*mm,10*mm,'Reservatórios urbanos | ARG e microplásticos | 16/11/2026');c.drawRightString(w-19*mm,10*mm,str(d.page))
 doc.addPageTemplates([PageTemplate(id='text',frames=Frame(19*mm,18*mm,A4[0]-38*mm,A4[1]-38*mm,id='textframe'),onPage=foot),PageTemplate(id='maps',pagesize=landscape(A4),frames=Frame(13*mm,18*mm,landscape(A4)[0]-26*mm,landscape(A4)[1]-32*mm,id='mapsframe'),onPage=foot)])
 story=[];lines=md.splitlines();i=0
 while i<len(lines):
  s=lines[i]
  if not s:i+=1;continue
  if s.startswith('| '):
   rows=[]
   while i<len(lines) and lines[i].startswith('|'):
    if not set(lines[i].replace('|','').strip())<=set('-: '):rows.append([Paragraph(inline(v.strip()),styles['CellTECO']) for v in lines[i].strip('|').split('|')])
    i+=1
   t=Table(rows,colWidths=[(A4[0]-40*mm)/len(rows[0])]*len(rows[0]),repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dcebea')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.35,colors.HexColor('#c7d8d8')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.extend([t,Spacer(1,10)]);continue
  level=len(s)-len(s.lstrip('#')) if s.startswith('#') else 0
  style='Title' if level==1 else 'Heading'+str(level-1) if level else 'TextTECO'
  story.append(Paragraph(inline(s.lstrip('#').strip() if level else s[2:] if s.startswith('- ') else s),styles[style]));i+=1
 story.extend([NextPageTemplate('maps'),PageBreak()])
 for j,g in enumerate(gallery):
  if j:story.append(PageBreak())
  story.append(Paragraph(g['title'],styles['Heading1']));p=O/'figuras'/g['png'];im=Image(str(p),width=264*mm,height=111.76*mm);story.append(im);story.append(Spacer(1,6));story.append(Paragraph('Encarte original 30 cm × 12,7 cm, 1:225000. Nesta página a imagem foi reduzida; use a barra gráfica ou o SVG/PNG original para aferição de escala. Interpretação no relatório e no visualizador.',styles['TextTECO']))
 doc.build(story)

# Guia dos scripts novos
def codeguide():
 scripts=[('obter_residuos_licenciamento.py','Baixa os sete serviços WFS e as exportações SINIR. Requests aplica tempo limite e tentativas; a consulta usa bbox em EPSG:31983 e paginação. SHA-256 documenta integridade. O RAR exige tar disponível. Originais de licenciamento ficam locais, pois podem conter CPF.','params={'),('microplasticos_teco.py','GeoPandas recorta e agrega geometrias; Pandas lê o CSV censitário em blocos. Os limites UNC_LO/UNC_HI preservam o sigilo. NumPy transforma critérios e calcula o índice. SciPy executa k-means e distâncias; moran_w e BH vêm do módulo estatístico anterior. Rasterio rasteriza o índice e deque percorre o grafo D8 sem ciclos.','score=100'),('mapas_microplasticos_teco.py','Matplotlib compõe três mapas com mesma escala e geometria de impressão. GeoPandas representa setores nativos ou hexágonos conforme o produto. PyProj converte somente rótulos das coordenadas. Rasterio fornece a extensão dos rasters. A legenda mostra unidades físicas nas entradas e índice nos resultados.','fig=plt.figure'),('consolidar_microplasticos_teco.py','Exporta um shapefile por pasta, encurta nomes de campo com mapeamento explícito, copia tabelas, mapas e scripts, atualiza dicionário global e calcula inventário SHA-256. As versões geradas substituídas são movidas a descontinuado. Não altera arquivos brutos.','def export'),('integrar_qgis_microplasticos.py','PyQGIS abre os dois projetos atuais, cria grupo Microplastics e camadas temáticas, aplica estilos e duplica seis layouts triplos sem reconstruir os grupos anteriores. Mantém caminhos relativos e arquiva os projetos antes da atualização.','manager.duplicateLayout'),('documentar_microplasticos_teco.py','Lê auditoria e tabelas, produz texto, tabelas e pranchas em PDF com ReportLab e a página HTML. O guia incorpora trechos do código efetivamente salvo. Não recalcula indicadores nem reclassifica dados.','def pdf')]
 scripts.append(('reproduzir_microplasticos.py','Reproduz a classificação e os testes a partir do GeoJSON derivado publicado, sem baixar novamente as fontes ou processar o MDE. Confere diferença absoluta do índice e interrompe se exceder 1e-8. A reconstrução de censos e caminhos D8 exige a cadeia completa.','engine.classify'))
 md='# Guia dos scripts | Complementação microplásticos\n\nOs caminhos são relativos à raiz do TECO, configurável por TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json. A configuração de critérios e pesos fica em config/microplasticos.json. Os grandes arquivos de base não acompanham o repositório público. A reprodução exige fornecer as entradas descritas no cabeçalho de cada script.\n\n'
 for name,desc,needle in scripts:
  source=(R/'codigo'/name).read_text('utf8');lines=source.splitlines();pos=next((i for i,s in enumerate(lines) if needle in s),0);snippet='\n'.join(lines[max(0,pos-1):pos+4]);md+=f'## {name}\n\n{desc}\n\nTrecho do arquivo, a partir da linha {max(0,pos-1)+1}.\n\n```python\n{snippet}\n```\n\n'
  if name=='microplasticos_teco.py':md+='Os pesos são aplicados à média do índice e, pela raiz quadrada, à distância do k-means. O Moran local não usa os grupos do k-means como entrada: usa o índice e a matriz de vizinhança. O teste local tem 999 permutações condicionais sem reposição por vizinho; os p-valores são corrigidos por BH dentro de cada bacia. O processamento D8 acumula índice × área e área válida; a divisão gera média de pressão a montante, sem simular massa ou decaimento.\n\n'
 md+='## Ordem de execução\n\n1. Configurar a raiz e conferir entradas.\n2. Executar obter_residuos_licenciamento.py para nova consulta, ou preservar a exportação documentada.\n3. Executar microplasticos_teco.py.\n4. Executar mapas_microplasticos_teco.py.\n5. Executar consolidar_microplasticos_teco.py.\n6. Executar integrar_qgis_microplasticos.py no Python do QGIS.\n7. Executar documentar_microplasticos_teco.py com ReportLab.\n\nUma nova variável requer agregação no preparador, definição de transformação/unidade na configuração, pesos em todos os cenários e novos testes de cobertura e redundância. Não reutilizar os pesos como coeficientes de emissão.\n'
 (D/'Guia_codigos_microplasticos.md').write_text(md,encoding='utf8')
 body=[];parts=re.split(r'```python\n(.*?)```',md,flags=re.S)
 for i,p in enumerate(parts):body.append('<pre><code>'+html.escape(p)+'</code></pre>' if i%2 else html_body(p))
 (D/'Guia_codigos_microplasticos.html').write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Guia dos scripts | Microplásticos</title><style>'+CSS+'</style><main>'+''.join(body)+'</main></html>',encoding='utf8')

# Publicação local
def main():
 md=text();(D/'Relatorio_ARG_microplasticos.md').write_text(md,encoding='utf8');gallery=json.loads((O/'figuras/galeria.json').read_text('utf8'))
 figs=''.join('<figure><h3>'+html.escape(g['title'])+'</h3><a href="../../03_mapas/14_microplasticos/'+g['svg']+'"><img loading="lazy" src="../../03_mapas/14_microplasticos/'+g['png']+'" alt="'+html.escape(g['title'])+'"></a></figure>' for g in gallery)
 (D/'Relatorio_ARG_microplasticos.html').write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ARG e microplásticos | Metodologia</title><style>'+CSS+'</style><main><nav><a href="Relatorio_ARG_microplasticos.pdf">Baixar PDF</a><a href="Guia_codigos_microplasticos.html">Guia dos scripts</a></nav>'+html_body(md)+'<h2>Pranchas de resultados</h2>'+figs+'</main></html>',encoding='utf8')
 pdf(md,gallery);codeguide();print('Relatorio e guia',D,flush=True)
if __name__=='__main__':main()
