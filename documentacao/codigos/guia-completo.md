# Relatório dos códigos — Codiname TECO

Edição de 14 de novembro de 2026. Fontes locais e resultados atuais, sem reexecução dos modelos de dispersão.

## Como usar este relatório

Este documento reúne uma explicação metodológica e fichas dos códigos existentes na pasta de trabalho. Cada ficha informa finalidade, dependências, entradas, campos, produtos e trechos reais do arquivo. O índice HTML ao lado deste PDF permite buscar um nome e abrir a ficha completa, com o código integral numerado. O inventário CSV/JSON registra as assinaturas dos arquivos. Bibliotecas de terceiros distribuídas com Quarto, Node e outros programas não são códigos autorais e ficaram fora desse inventário.

As fichas distinguem cálculo atual, apoio, teste, geração editorial e rotina histórica. A presença de um arquivo na pasta não significa que seja necessário executá-lo para atualizar todos os resultados. As etapas antigas de migração e os geradores dos seminários entregues permanecem para rastreabilidade e não devem ser executados como um lote indiscriminado.

As entradas explicitadas foram levantadas na sintaxe dos programas e conferidas nos módulos principais. Expressões como `{path}`, argumentos do chamador e nomes compostos em tempo de execução são interfaces, não arquivos faltantes. Nos cabeçalhos, “campos/chaves” inclui atributos de camadas, colunas de tabelas e chaves de configuração. O dicionário de campos do TECO mantém a descrição específica por camada. O código integral resolve eventuais ambiguidades de uma expressão dinâmica.

## Caminhos, ambiente e reprodução em outro computador

O arquivo `codigo/caminhos_projeto.json` concentra a raiz, remapeamentos de pastas, exceções de arquivos e dependências externas. Com `raiz_projeto` vazio, a pasta que contém `codigo` é a raiz adotada. Ao copiar toda a árvore do projeto e mantê-la organizada, não é necessário conservar a letra E do disco. Para usar dados fora dessa árvore, preencher `raiz_projeto` ou o item correspondente em `pastas`/`arquivos`. Os programas consultam esse arquivo pelos módulos `caminhos_<projeto>` de cada linguagem.

Exemplo de configuração a adaptar, sem alterar os campos e as equações do processamento:

```json
{"raiz_projeto":"D:/Pesquisa/Meu projeto",
 "pastas":{"output":"D:/Pesquisa/Resultados"},
 "arquivos":{},"externos":{},"ambiente":{}}
```

A raiz pode ser sobrescrita pelas variáveis de ambiente CONGONHAS_PROJECT_ROOT, TECO_PROJECT_ROOT ou COPASA_PROJECT_ROOT. Congonhas também preserva EMI_PROJECT_ROOT. Cada projeto tem seu próprio arquivo de configuração e não consulta o de outro projeto. Os itens em `externos` identificam arquivos fora da árvore, fontes tipográficas, modelos e executáveis. Eles devem ser revistos na máquina de destino. O JSON armazena caminhos, não instala os programas.

As ferramentas administrativas que geram e conferem esta documentação dos três projetos utilizam também a tabela PROJETOS, no início de documentar_portabilidade.py, para localizar cada árvore. Ao transferir essas ferramentas, ajustar essa tabela ou usar --projeto/--raiz no inventariador. Elas não são necessárias para executar a análise configurável entregue à colaboradora. Os cabeçalhos dessas rotinas identificam essa configuração adicional.

O ambiente geográfico usa NumPy, pandas, GeoPandas, Shapely, Rasterio, PyProj/Pyogrio e SciPy. Os recursos PyQGIS/GRASS devem ser executados no Python instalado com o QGIS. Gerar Word/PDF ou pôster pode exigir outro ambiente com python-docx, ReportLab, pypdf, Pillow, lxml, Microsoft Word e as bibliotecas de autoria de apresentações. Os módulos JavaScript que importam `@oai/artifact-tool` dependem desse pacote, fornecido pelo ambiente de autoria utilizado aqui; não basta instalar Node. Essa dependência não é necessária para recalcular os indicadores geográficos.

Os programas anteriores à edição dos caminhos foram arquivados em `descontinuado/20261114_portabilidade_codigo`, preservando sua localização relativa. A edição dos códigos não executou novamente os modelos de dispersão nem substituiu os mapas publicados ou os textos acadêmicos já entregues.

## Conceitos numéricos que atravessam os códigos

Uma normalização coloca variáveis em escalas comparáveis, sem criar informação. Na transformação logarítmica usa-se t=ln(1+x). No min-max, n=(t−mínimo)/(máximo−mínimo). Na padronização z, z=(t−média)/desvio-padrão. Colunas constantes usam denominador 1, para evitar divisão por zero. Lacuna não é automaticamente zero. A máscara de registros completos define quais observações podem entrar em determinado ajuste.

O índice ponderado do TECO é I=100×Σ(wj×nj)/Σwj. Os pesos exprimem hipóteses de importância relativa, não coeficientes obtidos pela medição de genes. No k-means minimiza-se Σi Σj wj×(nij−centrogrupo,j)². Por isso o código multiplica a matriz normalizada por √peso antes do ajuste. Usar o peso diretamente nessa matriz elevaria a influência ao quadrado. A implementação utiliza scipy.cluster.vq.kmeans2, não uma chamada ao k-means do QGIS ou do scikit-learn. Inicializações repetidas e sementes explícitas reduzem a dependência de uma única solução inicial. [Documentação SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans2.html).

A silhouette de cada observação é s=(b−a)/máximo(a,b), em que a mede distância média ao próprio grupo e b à alternativa mais próxima. A média resume separação interna e pode comparar valores de k na mesma matriz. Não é um p-valor, nem porcentagem de acerto, nem comprovação de que o grupo corresponde a uma fonte real. Classes por quintis são cortes ordenados em uma variável. K-means é um agrupamento multivariado por semelhança. A estabilidade compara resultados depois de variar pesos, suporte ou amostras e não se confunde com nenhum dos dois. [Rousseeuw, 1987](https://doi.org/10.1016/0377-0427%2887%2990125-7).

Moran global relaciona os desvios padronizados de cada local aos de seus vizinhos. Com pesos de vizinhança padronizados por linha, o código usa I=(zᵀWz)/(zᵀz). O Moran local usa Ii=zi×(Wz)i. A significância é obtida por permutação, com p=(1+contagem de resultados tão extremos quanto o observado)/(1+número de permutações). O ajuste Benjamini-Hochberg controla a taxa de falsas descobertas da família declarada. HH e LL significam valor alto/baixo cercado de valores semelhantes; HL/LH são contrastes locais. NS indica ausência de evidência com o critério adotado, não ausência de pressão. ISO identifica isolamento topológico quando previsto. Associação espacial não demonstra uma rota hidrológica ou causal.

Uma junção por chave preserva identificadores e exige unicidade. Uma interseção espacial recorta as geometrias. Na média ponderada por área, x̄=Σ(xj×área de interseçãoj)/Σárea válida. Ratear população por área pressupõe distribuição uniforme dentro da parcela original quando não há uma base dasimétrica melhor. Uma reprojeção transforma coordenadas; atribuir um código EPSG sem transformar o dado não corrige uma coordenada errada. [GeoPandas overlay](https://geopandas.org/en/stable/docs/reference/api/geopandas.overlay.html).

## Ampliação controlada das variáveis

TECO e Congonhas receberam `config/analise_extensivel.json` e `codigo/reproduzir_analise_configuravel.py`. O cenário padrão reproduz a matriz publicada a partir dos produtos consolidados, com saída separada. Para acrescentar uma variável, declarar nome, origem, arquivo, camada/campo, unidade, transformação e agregação; depois informar o peso em cada cenário. A origem pode ser uma coluna da base, tabela, camada vetorial ou raster. Os métodos disponíveis são junção por chave, média ponderada pela área, soma de pontos e média dos pixels válidos. Outro tipo de dado requer acrescentar sua regra na função anexar_variavel. O programa interrompe a execução se houver campo ausente, chave duplicada ou agregação desconhecida.

Na expansão, justificar o sinal da variável e evitar contar duas vezes a mesma pressão. Revisar cobertura, ano, universo e lacunas. Transformações e pesos devem ser fixados antes de comparar cenários. No TECO, a agregação espacial usa os círculos de cálculo, enquanto a geometria final de apresentação continua sendo o suporte sem sobreposição. O exemplo de extensão demonstra uma interface técnica; escolher uma nova variável continua sendo uma decisão metodológica. Um peso não informado assume zero, portanto precisa ser conferido antes de interpretar o cenário.
## Fluxo específico do Codiname TECO

O objetivo é identificar pressão antrópica potencial e conectividade preferencial para os reservatórios, sem estimar concentração de genes ou prevalência de resistência. O encadeamento parte da delimitação de bacias, recorta as fontes nativas, constrói vizinhanças de 500 m e só então combina os indicadores. As camadas originais de população, saneamento, relevo, uso da terra e estabelecimentos continuam sendo apresentadas em suas próprias geometrias. A grade é usada na classificação.

O delimitador usa Copernicus GLO-30 reprojetado para SIRGAS 2000/UTM 23S. No código fornecido, `r.watershed` recebe explicitamente `-s=True`, selecionando direção única D8, e `-b=True`; o padrão do GRASS sem -s seria fluxo múltiplo. D8 escolhe uma das oito células vizinhas como direção de saída. O exutório é selecionado com apoio da acumulação e da borda do reservatório, e `r.water.outlet` delimita a contribuição. Conferências de projeção e alinhamento evitam confundir metros com graus. A suavização final é cartográfica e exige atenção para não interpretar a borda como precisão hidrológica subpixel. [Manual GRASS](https://grass.osgeo.org/grass-stable/manuals/r.watershed.html).

As três entradas centrais da matriz atual são POP_DENS (habitantes/km²), SEM_REDE (% de domicílios sem ligação à rede) e AIH_LOCAL (média anual de internações alocadas ao local do estabelecimento, no universo do processamento). POP_DENS e AIH_LOCAL passam por log1p; as três são normalizadas por min-max global. Os mínimos e máximos são fixos ao comparar S0-S4. S0 usa [1,1,1], S1 [1,1,3], S2 [1,3,1], S3 [3,1,1] e S4 [1,1,0]. S4 testa a influência de retirar a informação hospitalar local.

AIH_LOCAL não é número de moradores infectados, consumo de antimicrobianos, resistência confirmada ou carga lançada no reservatório. As bases de internação por residência e de produção no estabelecimento devem continuar separadas. A revisão CNES/SIH de 2026 ampliou o cadastro e auditou os estabelecimentos com produção recente; isso não significa que cada coluna da matriz anterior tenha sido automaticamente recalculada com o novo período. O reprodutor configurável lê o AIH_LOCAL efetivamente armazenado no consolidado. Para alterar a coorte, é necessário atualizar a etapa de saúde, documentar a nova seleção e depois recalcular a matriz.

Há 598 unidades bacia/vizinhança, com 592 registros completos e seis incompletos. Testam-se k=2 a 6, com 15 inicializações por ajuste e semente 20261112 acrescida de 100 por cenário. O k do cenário base é usado como k comum na comparação de rótulos, alinhados por máxima correspondência. O resultado reproduzido selecionou k=2, silhouette 0,667649. Perfis de grupo devem ser interpretados pelas medianas das entradas, não apenas pelo número 1 ou 2. A estabilidade registra a frequência com que a observação permanece no perfil base depois do alinhamento. O índice contínuo, suas cinco faixas fixas e os quintis são produtos distintos do perfil k-means.

O Moran da classificação usa contiguidade Queen no suporte hexagonal, por bacia, com 999 permutações e FDR de 5%. Exigem-se pelo menos 95% de cobertura de saneamento publicado na seleção prevista. O índice de círculos vizinhos compartilha parte dos mesmos dados; essa suavização também pode produzir autocorrelação. HH não comprova genes, lançamento ou infecção, mas aponta agrupamento de pressão para investigação.

Declividade, hidrografia, vias, uso da terra e distância topográfica são contexto físico e possíveis condicionantes de conectividade, sem entrar automaticamente como mais cinco parcelas do índice central. A declividade percentual é 100×√[(∂z/∂x)²+(∂z/∂y)²]. A classificação Embrapa usa os cortes 3, 8, 20, 45 e 75%. A pressão a montante é uma média do índice ponderada pela área válida roteada em D8. Não inclui vazão, tratamento de esgoto, atenuação, sobrevivência bacteriana ou transporte na tubulação. Áreas sem trajetória rastreada são lacuna/limitação do modelo de terreno, não ausência demonstrada de conexão.

Na conferência desta edição, a reprodução manteve todos os rótulos S0-S4 e o Moran do consolidado. A maior diferença absoluta entre índices foi 1,42×10⁻¹⁴, arredondamento numérico. O campo normalizado novo N1/N2/N3 corresponde à ordem declarada no JSON. I_Sx e K_Sx são o índice e o perfil de cada cenário; estabilidade, r_quintil, r_moran e q_fdr identificam os produtos recalculados. As saídas ficam em output/06_analise_configuravel, separadas da entrega validada.

## Catálogo de rotinas

100 arquivos autorais foram documentados. O índice HTML apresenta a ficha integral e o código numerado de cada um. As fichas seguintes preservam os pontos de cálculo, os campos e os trechos citados.

## codigo/analise_espacial_teco.py

Fornece os métodos numéricos de apoio, indicadores censitários, relevo e roteamento topográfico. Seu programa principal guarda a análise setorial anterior; as funções são reutilizadas pela grade de 500 m.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\analise_espacial_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.windows | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| scipy.cluster.vq | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.sparse | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| warnings | Controle de avisos de bibliotecas sem alterar a definição do estimador. |


**Entradas.**

- E:/teco/output/01_integracao_territorial/integracao_territorial_teco.gpkg [camada 'setores_bacias'] — chamada gpd.read_file, linha 140.
- E:/teco/sub_bacia/shapefiles_v6_20261109_141015/sub_bacias_exclusivas.shp — chamada gpd.read_file, linha 141.
- E:/teco/dados_publicos/cnes/estabelecimentos_ativos_municipios.json — chamada f.read_text, linha 166.
- E:/teco/dados_publicos/cnes/tipos.json — chamada .read_text, linha 167.
- E:/teco/teco_base/mg_mun/ide_1103_mg_municipios_pol.shp — chamada gpd.read_file, linha 185.
- E:/teco/sub_bacia/br.id/dem_utm_30m.tif — chamada rasterio.open, linha 214.
- E:/teco/sub_bacia/br.id/direcao_d8.tif — chamada rasterio.open, linha 216.
- E:/teco/reservatorio/{lakefile}.shp — chamada gpd.read_file, linha 220.
- E:/teco/reservatorio/{k}.shp — chamada gpd.read_file, linha 432.
- E:/teco/hidrografia/hidrografia.shp — chamada gpd.read_file, linha 433.
- E:/teco/vias/malha_viaria.shp — chamada gpd.read_file, linha 434.
- E:/teco/teco_base/uso_terra/uso_terra-reservatorio.tif — chamada rasterio.open, linha 531.
- Mais 2 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/teco/output/02_avaliacao_espacial/tabelas/{name} — chamada df.to_csv, linha 108.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada name] — chamada g.to_file, linha 112.
- E:/teco/output/02_avaliacao_espacial/shapefiles/{name}.shp — chamada g.to_file, linha 113.
- E:/teco/output/02_avaliacao_espacial/rasters/{name} — chamada rasterio.open, linha 119.
- E:/teco/output/02_avaliacao_espacial/figuras/{slug}.{fmt} — chamada fig.savefig, linha 473.
- E:/teco/output/02_avaliacao_espacial/figuras/17_diagnostico_agrupamentos.{fmt} — chamada fig.savefig, linha 547.
- E:/teco/output/02_avaliacao_espacial/figuras/18_correlacoes_variaveis.{fmt} — chamada fig.savefig, linha 555.
- E:/teco/output/02_avaliacao_espacial/auditoria/galeria.json — chamada .write_text, linha 557.
- E:/teco/output/02_avaliacao_espacial/index.html — chamada .write_text, linha 564.
- E:/teco/output/02_avaliacao_espacial/auditoria/auditoria.json — chamada .write_text, linha 571.

**Campos e chaves lidos.**

- whole: geometry, pop_2022, setor_id.
- clipped: bas_id, dom_a_est, geometry, pct_rede, pop_a_est, red_a_est, setor_id.
- x: codigo_tipo_unidade, descricao_tipo_unidade.
- d: lat, latitude_estabelecimento_decimo_grau, lon, longitude_estabelecimento_decimo_grau.
- d.loc: lat, lon.
- b: geometry, id.
- g: CNES, codigo_municipio, geometry.
- muni: geocodigo, geometry.
- c: bas_id, geometry, setor_id.
- AUD: analise, cnes.
- a.loc: def_rede, dens_pop, pressao, quintil, setor_id.
- r: silhouette, slug, titulo.
- best: k.
- loc: lisa, q_fdr.
- a: bas_id, cluster, d8_cob_pct, dist_hid_km, geometry, lisa, pressao, q_fdr, quintil, setor_id.
- l: t.
- routes: bacia.
- mouths: bacia, proxy_nr.
- km: k, silhouette.
- ss: mantem_P80_pct, peso_pop.
- ax.spines: right, top.

**Campos e chaves gerados.**

- AUD: analise, bases, cartografia, cnes, d8.
- d: lat, lon.
- g: ANO_ATUAL, CNES, COORD_DUP, GRUPO, QA_MUN, TIPO.
- qa: QA_MUN.
- c: hosp_urg_n, saude_n.
- a: cluster, def_rede, lisa, lisa_biv, pressao, prioridade, proxy_nr, q_fdr, quintil.
- lookup: ND.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| log(*x) | 105-105 | Chamadas efetivas: print |
| csv(df, name) | 108-108 | grava produtos |
| gp(g, name, shp=False) | 111-113 | grava produtos |
| raster(a, profile, name, nodata=-9999, dtype='float32') | 116-119 | Chamadas efetivas: profile.copy, p.update, p.pop, rasterio.open, d.write, .astype, np.where, np.isfinite |
| hashgeom(g) | 122-122 | Chamadas efetivas: .hexdigest, hashlib.sha256, .join, g.geometry.to_wkb Retorno: hashlib.sha256(b''.join(g.geometry.to_wkb())).hexdigest(). |
| rank01(a) | 125-129 | Chamadas efetivas: np.asarray, np.isfinite, np.full, len, v.sum, rankdata Retorno: o. |
| quint(a) | 132-135 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: o. |
| bases() | 138-161 | lê dados Retorno: (whole, clipped, b). |
| cnes(b, c) | 164-205 | lê dados Retorno: (g, c), 'Administrativo / móvel / outros'. |
| terrain_routing(b, c) | 210-293 | lê dados Retorno: (c, layers, routes, mouths). |
| ari(a, b) | 296-301 | Chamadas efetivas: np.unique, len, .reshape, comb, .sum, tab.sum, np.bincount, a.max Retorno: (x - e) / den if den else 1.0. |
| fitkm(x, k, seed, starts=12) | 304-313 | Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida. Retorno: best. |
| silhouette(x, l) | 316-323 | Chamadas efetivas: distance.cdist, enumerate, float, same.sum, min, s.append, np.mean, .sum Retorno: float(np.mean(s)). |
| weights(xy, k) | 326-330 | Chamadas efetivas: len, np.repeat, idx.ravel, csr_matrix, w.maximum, w.setdiag, w.eliminate_zeros, .tocsr Retorno: w.multiply(1 / np.asarray(w.sum(1))).tocsr(). |
| bh(p) | 333-334 | Chamadas efetivas: np.asarray, np.argsort, np.empty, np.minimum, np.minimum.accumulate, len, np.arange Retorno: o. |
| moran(x, xy, k=8, seed=SEED, local=False, y=None) | 337-368 | Chamadas efetivas: len, weights, float, np.random.default_rng, np.empty, range, bh, np.where Retorno: (rec, {'Ii': Ii, 'p_local': pvlocal, 'q_fdr': q, 'lisa': label, 'lag': lag}), (rec, None). |
| analysis(c) | 371-428 | Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.; Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes. Retorno: a. |
| maps(a, b, health, layers, routes, mouths) | 431-558 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: gallery, (fig, axs). |
| index(gallery) | 561-564 | grava produtos |
| main() | 567-572 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/analise_espacial_teco.py, linhas 133-139.

```python
    a=np.asarray(a,float);o=np.zeros(len(a),int);v=np.isfinite(a)
    if v.sum():o[v]=np.searchsorted(np.quantile(a[v],[.2,.4,.6,.8]),a[v],side='left')+1
    return o

# Bases
def bases():
    whole=gpd.read_file(SOURCE,layer='setores_inteiros').sort_values('setor_id').reset_index(drop=True)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

Trecho de codigo/analise_espacial_teco.py, linhas 204-210.

```python
    AUD['cnes']={'consultados':len(d),'dentro_bacias':len(g),'coordenadas_invalidas':int((~ok).sum()),'municipio_incompativel':int((g.QA_MUN==0).sum()),'pontos_com_coordenada_compartilhada':int((g.COORD_DUP>1).sum()),'hospitais_urgencia':len(hp),'usados_contagem_setores':len(q),'natureza':'cadastro ativo atual, não série de 2016-2025; coordenadas cadastrais não validadas em campo; divergentes de município não entram nas contagens'}
    log('CNES',AUD['cnes']);return g,c

D8={1:(-1,1),2:(-1,0),3:(-1,-1),4:(0,-1),5:(1,-1),6:(1,0),7:(1,1),8:(0,1)}

# Terrain routing
def terrain_routing(b,c):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- log: Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.
- gradient: Derivadas nas direções do raster. A declividade depende também do tamanho físico do pixel e da unidade de elevação.
- digitize: Associa valores a intervalos definidos pelos cortes do código, inclusive classes de relevo ou faixas de distância.
- bincount: Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.
- kmeans2: Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida.
- cdist: Matriz de distâncias entre observações. É usada no agrupamento, na silhouette ou na comparação entre centroides.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.
- log1p: Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.
- spearmanr: Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.
- nanpercentile: Percentil que ignora NaN. O número e o período de valores válidos continuam definindo sua representatividade.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/arquivar_revisao_idioma.py

Arquivar revisao idioma. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\arquivar_revisao_idioma.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/teco/tmp/relatorio_detalhado/arquivo_anterior.txt — chamada .write_text, linha 27.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/arquivar_revisao_idioma.py, linhas 11-19.

```python
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_teco.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_teco.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
        break
from caminhos_teco import raiz_projeto as _cp_raiz, texto_caminho as _cp_texto, externo as _cp_externo, adaptar_texto as _cp_adaptar
# FIM DOS CAMINHOS PORTÁTEIS

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atualizar_documentacao_consolidada_teco.py

Atualizar documentacao consolidada teco. Documentação/apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\atualizar_documentacao_consolidada_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/tmp/consolidacao_final/archive_path.txt — chamada .read_text, linha 25.
- E:/teco/output/02_avaliacao_espacial/Relatorio_TECO_academico_base.md — chamada B.read_text, linha 27.
- E:/teco/codigo/guia_entrega_final.py — chamada p.read_text, linha 47.

**Saídas.**

- E:/teco/output/02_avaliacao_espacial/Relatorio_TECO_academico_base.md — chamada B.write_text, linha 45.
- E:/teco/codigo/guia_entrega_final.py — chamada p.write_text, linha 63.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_documentacao_consolidada_teco.py, linhas 24-32.

```python
import shutil,json
R=Path(_cp_texto('', 'posix'));A=Path((R/'tmp/consolidacao_final/archive_path.txt').read_text('utf8').strip());B=R/'output/02_avaliacao_espacial/Relatorio_TECO_academico_base.md'
shutil.copy2(B,A/B.name)
s=B.read_text('utf8')
s=s.replace('Relatório metodológico e interpretação dos resultados do projeto TECO','Relatório metodológico e interpretação dos resultados do projeto TECO\n\nResponsável pela cartografia Brentano, M. C. B.')
s=s.replace('Foram mantidos dois recortes de saúde que respondem a questões distintas.','Foram mantidos dois recortes de saúde que respondem a questões distintas. A consulta inicial de residência abrangeu quatro municípios e foi preservada como referência de comparação. Na consolidação, esse universo foi ampliado para os oito municípios que intersectam as bacias, conforme descrito a seguir.')
new='''### Ampliação para todos os municípios que intersectam as bacias

A conferência entre o domínio censitário e os filtros de residência identificou que as bacias também interceptam Brumadinho, Esmeraldas, Ribeirão das Neves e Sarzedo, além dos quatro municípios inicialmente consultados. A extração foi ampliada para incluir os oito municípios, preservando separadamente a referência anterior. Foram relidos os mesmos 120 arquivos mensais de Minas Gerais, sem alterar a seleção de AIH normais ou o filtro operacional de diagnósticos. A consulta oficial por município, hospital e ano foi repetida no TabNet para conferir o conjunto ampliado.
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atualizar_indice_teco.py

Índice local, catálogo de fontes e interpretação dos cenários TECO.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\atualizar_indice_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/03_multivariada/auditoria/galeria.json — chamada .read_text, linha 31.
- E:/teco/output/02_avaliacao_espacial/auditoria/galeria.json — chamada .read_text, linha 32.
- E:/teco/dados_publicos/lancamentos/{fn} — chamada open, linha 71.

**Saídas.**

- E:/teco/output/02_avaliacao_espacial/index.html — chamada .write_text, linha 57.
- E:/teco/output/03_multivariada/index.html — chamada .write_text, linha 59.
- E:/teco/output/03_multivariada/tabelas/fontes_lancamentos.csv — chamada .open, linha 72.
- E:/teco/output/03_multivariada/tabelas/conexoes_documentais_saneamento.csv — chamada .open, linha 74.
- E:/teco/output/03_multivariada/LEIA_PRIMEIRO.md — chamada .write_text, linha 75.

**Campos e chaves lidos.**

- row: grupo, slug, titulo.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| card(row, prefix) | 36-49 | Chamadas efetivas: slug.startswith, html.escape, .lower, str Retorno: f'<article data-group="{attrs}" data-base="{str(baseflag).lower()}"><h2>{html.escape(title)}</h2><p class="desc">{html.escape(desc)}</p><a href="{path}.svg"><img loading="lazy" src="{path}.png" alt="{. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_indice_teco.py, linhas 36-44.

```python
def card(row,prefix):
 slug=row['slug'];group=row['grupo'];title=row['titulo'];path=prefix+'figuras/'+slug
 desc=''
 if slug.startswith('kmeans') or slug.startswith('base_k'):desc='Perfis de atributos; não são probabilidades de contaminação. As cinco entradas e a leitura dos grupos estão no relatório.'
 if slug.startswith('moran'):desc='HH/LL indicam associação de valores semelhantes; HL/LH indicam contrastes. FDR de 5%; não representa o sentido do escoamento.'
 if slug=='entrada_sem_rede':desc='Variável analítica com estimativa sinalizada nas lacunas. O shapefile censitário original conserva seus valores nulos; S9/S10 testam limites.'
 if slug=='entrada_sih_dens':desc='Atividade registrada dos três estabelecimentos localizados em 2016-2025. Zero não significa ausência real de atividade assistencial.'
 if slug.startswith('estabilidade'):desc='Frequência de manutenção do perfil nos cenários testados. Não é probabilidade de contaminação.'
 if slug=='exutorios':desc='Vargem conferido com planta do vertedouro COPASA 2025 e hidrografia. Precisão cartográfica aproximada de 30 m.'
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atualizar_internacoes_residencia.ps1

Atualizar internacoes residencia. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\atualizar_internacoes_residencia.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_internacoes_residencia.ps1, linhas 10-18.

```text
param([switch]$AtualizarTabnet)
. (Join-Path $PSScriptRoot 'caminhos_teco.ps1')

$ErrorActionPreference = 'Stop'
$tecoRoot = (Get-PortablePath '')
$tecoPython = (Get-PortableExternal 'python_exe_9a6f757')
if ($AtualizarTabnet) { & $tecoPython "$tecoRoot\codigo\obter_sih_residencia_tabnet.py" --atualizar }
else { & $tecoPython "$tecoRoot\codigo\obter_sih_residencia_tabnet.py" }
if ($LASTEXITCODE -ne 0) { throw 'Falha na consulta NRMG.' }
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atualizar_projeto_teco.py

Acrescenta os produtos revisados ao projeto do usuário, preservando sua estrutura.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\atualizar_projeto_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtCore | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.PyQt.QtGui | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- populacao_setores — chamada load, linha 77.
- esgotamento_setores — chamada load, linha 81.
- populacao_recorte_estimado — chamada load, linha 82.
- esgoto_recorte_estimado — chamada load, linha 83.
- analise_setores — chamada load, linha 89.
- rotas_d8_candidatas — chamada load, linha 90.
- entradas_lago_proxy — chamada load, linha 92.
- saude_cnes_ativos — chamada load, linha 94.
- saude_historico_sih — chamada load, linha 96.
- bacias_estudo — chamada load, linha 98.
- E:/teco/projeto_teco.qgz — chamada SOURCE.read_bytes, linha 126.

**Saídas.**

- E:/teco/descontinuado/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_projeto_teco_anterior')/manifesto.json — chamada .write_text, linha 126.
- E:/teco/output/02_avaliacao_espacial/auditoria/previsualizacao_qgis.png — chamada .save, linha 131.
- E:/teco/output/02_avaliacao_espacial/auditoria/conferencia_projeto_qgis.json — chamada .write_text, linha 133.

**Campos e chaves lidos.**

- f: cluster.

**Campos e chaves gerados.**

- os.environ: QT_QPA_PLATFORM.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| load(name, title, group, visible=False, shp=False) | 59-63 | Chamadas efetivas: QgsVectorLayer, l.isValid, p.addMapLayer, .setItemVisibilityChecked, checks.append, str, group.addLayer, l.featureCount Retorno: l. |
| rule(l, field, items, kind='fill') | 65-71 | Chamadas efetivas: QgsFillSymbol.createSimple, QgsRuleBasedRenderer, rr.rootRule, ro.removeChildAt, l.setRenderer, ro.appendChild, QgsRuleBasedRenderer.Rule |
| percent(l, field) | 73-76 | Chamadas efetivas: range, it.append, rule |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_projeto_teco.py, linhas 59-67.

```python
def load(name,title,group,visible=False,shp=False):
    src=str(O/'shapefiles'/f'{name}.shp') if shp else str(G)+'|layername='+name
    l=QgsVectorLayer(src,title,'ogr');assert l.isValid(),src
    p.addMapLayer(l,False);group.addLayer(l).setItemVisibilityChecked(visible)
    checks.append({'layer':title,'valida':True,'feicoes':l.featureCount(),'campos':l.fields().names()});return l
# Rule
def rule(l,field,items,kind='fill'):
    base=QgsFillSymbol.createSimple({'color':'#bfc4c5','outline_color':'#647779','outline_width':'0.08'})
    rr=QgsRuleBasedRenderer(base);ro=rr.rootRule();ro.removeChildAt(0)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atualizar_qgis_multivariada.py

Integra cenários e referências corrigidas ao QGIS, com cópia de segurança.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\atualizar_qgis_multivariada.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- K-means base  /  cinco perfis — chamada load, linha 54.
- Índice base  /  0-100, sem classificação de risco — chamada load, linha 55.
- S{i}  /  perfis de sensibilidade — chamada load, linha 57.
- Base  /  k={k} — chamada load, linha 59.
- {title} — chamada load, linha 67.
- Exutórios de referência  /  Vargem conferido — chamada load, linha 64.
- Conferência do ponto anterior e vertedouro  /  Vargem — chamada load, linha 65.

**Saídas.**

- E:/teco/descontinuado/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_qgis_antes_multivariada')/manifesto.json — chamada .write_text, linha 78.
- E:/teco/output/03_multivariada/auditoria/qgis_multivariada.json — chamada .write_text, linha 85.

**Campos e chaves gerados.**

- os.environ: QT_QPA_PLATFORM.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| load(title, g, layer='setores_multivariada', vis=False) | 42-43 | Chamadas efetivas: QgsVectorLayer, l.isValid, p.addMapLayer, .setItemVisibilityChecked, check.append, g.addLayer, l.featureCount, str Retorno: l. |
| rules(l, entries) | 45-50 | Chamadas efetivas: QgsRuleBasedRenderer, rr.rootRule, rt.removeChildAt, l.setRenderer, QgsFillSymbol.createSimple, rt.appendChild, QgsRuleBasedRenderer.Rule |
| km(l, field, k=5) | 52-52 | Chamadas efetivas: rules, enumerate |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_qgis_multivariada.py, linhas 42-50.

```python
def load(title,g,layer='setores_multivariada',vis=False):
 l=QgsVectorLayer(str(G)+'|layername='+layer,title,'ogr');assert l.isValid(),title;p.addMapLayer(l,False);g.addLayer(l).setItemVisibilityChecked(vis);check.append({'titulo':title,'feicoes':l.featureCount()});return l
# Rules
def rules(l,entries):
 rr=QgsRuleBasedRenderer(QgsFillSymbol.createSimple({'color':'#d5d8d5'}));rt=rr.rootRule();rt.removeChildAt(0)
 for expr,label,color in entries:
  sy=QgsFillSymbol.createSimple({'color':color,'outline_color':'#647b83','outline_width':'0.07'})
  rt.appendChild(QgsRuleBasedRenderer.Rule(sy,0,0,expr,label))
 l.setRenderer(rr)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_consolidacao_final_teco.py

Recalcula indicadores e os 25 ajustes de k-means, compara dados consolidados com fontes censitárias e registra diferenças. É uma conferência numérica, não um novo cenário científico.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\teco\codigo\auditar_consolidacao_final_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| analise_espacial_teco | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| multivariada_teco | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'saude_todos'] — chamada gpd.read_file, linha 59.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'analise_setores'] — chamada gpd.read_file, linha 59.
- E:/teco/output/03_multivariada/teco_multivariada.gpkg [camada 'unidades_ajuste'] — chamada gpd.read_file, linha 65.
- E:/teco/output/04_grade_500m/tabelas/kmeans_grade.csv — chamada pd.read_csv, linha 74.
- E:/teco/saneamento_ibge/populacao_basico/Agregados_por_setores_basico_BR.csv — chamada pd.read_csv, linha 95.

**Saídas.**

- E:/teco/tmp/consolidacao_final/testes_kmeans.gpkg [camada f'{co}_k{k:02d}'] — chamada out.to_file, linha 85.
- E:/teco/tmp/consolidacao_final/Kmeans_all_25_verified.csv — chamada .to_csv, linha 100.
- E:/teco/tmp/consolidacao_final/Auditoria_numerica.json — chamada .write_text, linha 101.

**Campos e chaves lidos.**

- a: AIH_LOCAL, AREA_KM2, BACIA, GRID_ID, N_AIH_LOCAL, N_POP_DENS, N_SEM_REDE, POP_DENS, SEM_REDE, VALIDO, geometry, is_valid.
- c: DOM_DENS, SEM_ANALIT, dens_pop, dom_set, geometry, pct_rede, pop_2022, set_km2, setor_id.
- cir: BACIA, GRID_ID, geometry.
- hp: AIH_ANO, CNES, geometry.
- a.loc: ESTABILIDADE, I_S0, K_S0, QUINTIL.
- loc: cluster, q.

**Campos e chaves gerados.**

- c: DOM_DENS, SEM_ANALIT.
- z: AREA, D, OBS, P, S.
- out: K, PROFILE, SCENARIO, SCORE.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| check(name, condition, detail) | 53-55 | Chamadas efetivas: checks.append, errors.append |
| main() | 58-101 | lê dados; grava produtos; Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_consolidacao_final_teco.py, linhas 70-76.

```python
 joined=gpd.sjoin(hp[['CNES','AIH_ANO','geometry']],cir[['GRID_ID','BACIA','geometry']],predicate='intersects');hh=joined.groupby(['GRID_ID','BACIA']).AIH_ANO.sum();health=np.array([hh.get((r.GRID_ID,r.BACIA),0) for r in a.itertuples()]);check('Hospital activity in calculation neighbourhoods',np.allclose(health,a.AIH_LOCAL),{'facilities':len(hp),'positive_grid_rows':int((health>0).sum())})
 x=np.c_[np.log1p(a.POP_DENS),a.SEM_REDE,np.log1p(a.AIH_LOCAL)];valid=np.isfinite(x).all(1);lo=x[valid].min(0);hi=x[valid].max(0);n=(x-lo)/np.where(hi>lo,hi-lo,1)
 check('Transformation and normalisation',np.allclose(n,a[['N_POP_DENS','N_SEM_REDE','N_AIH_LOCAL']],equal_nan=True,atol=1e-10),{'valid':int(valid.sum()),'incomplete':int((~valid).sum()),'min':lo.tolist(),'max':hi.tolist()})
 weights={'S0':[1,1,1],'S1':[1,1,3],'S2':[1,3,1],'S3':[3,1,1],'S4':[1,1,0]};rows=[]
 saved=pd.read_csv(O/'tabelas/kmeans_grade.csv',sep=';',decimal=',').set_index(['cenario','k'])
 for j,(co,w) in enumerate(weights.items()):
  score=100*(n@w)/sum(w);tiers=np.where(valid,np.minimum(np.nan_to_num(score/20).astype(int)+1,5),0)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- log1p: Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.
- bincount: Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_projetos_qgis_teco.py

Auditar projetos qgis teco. Auditoria/diagnóstico. A organização passa por tree, show.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\teco\codigo\auditar_projetos_qgis_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/teco/tmp/revisao_qgis/path.stem_before.json — chamada .write_text, linha 48.

**Campos e chaves lidos.**

- x: valid.
- node: children, name.
- rec: tree.
- row: actual_max, actual_min, name, renderer_max, renderer_min.

**Campos e chaves gerados.**

- os.environ: QT_QPA_PLATFORM.
- d: actual_max, actual_min, count, fields, renderer, renderer_max, renderer_min, subset, used_attributes, valid_cells.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| tree(node) | 32-33 | Chamadas efetivas: isinstance, node.name, node.layerId, tree, node.children Retorno: {'name': node.name(), 'children': [tree(c) for c in node.children()]} if isinstance(node, QgsLayerTreeGroup) else {'layer': node.layerId(), 'name': node.name()}. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_projetos_qgis_teco.py, linhas 48-54.

```python
 (T/(path.stem+'_before.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2,default=str),encoding='utf8')
 print(path.name,'layers',len(layers),'invalid',sum(not x['valid'] for x in layers),flush=True)
 def show(node,depth=0):
  if 'children' in node:
   print(' '*depth+node['name']+' ['+str(len(node['children']))+']')
   if depth<3:
    for c in node['children']:show(c,depth+1)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_relevo_lancamentos_teco.py

Auditar relevo lancamentos teco. Auditoria/diagnóstico. A organização passa por csv, points.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\teco\codigo\auditar_relevo_lancamentos_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {f} — chamada rasterio.open, linha 44.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'bacias_estudo'] — chamada gpd.read_file, linha 50.
- E:/teco/sub_bacia/shapefiles_v6_20261109_141015/exutorios_finais.shp — chamada gpd.read_file, linha 51.
- E:/teco/reservatorio/vargem_flores.shp — chamada gpd.read_file, linha 52.
- E:/teco/hidrografia/hidrografia.shp — chamada gpd.read_file, linha 56.
- {f} — chamada gpd.read_file, linha 77.
- {f} — chamada open, linha 87.

**Saídas.**

- E:/teco/output/03_multivariada/tabelas/{n} — chamada x.to_csv, linha 41.
- E:/teco/output/03_multivariada/teco_multivariada.gpkg [camada 'exutorios_referencia'] — chamada v.to_file, linha 70.
- E:/teco/output/03_multivariada/teco_multivariada.gpkg [camada 'conferencia_exutorio_vargem'] — chamada comparison.to_file, linha 71.
- E:/teco/output/03_multivariada/auditoria/exutorio_relevo.json — chamada .write_text, linha 73.
- E:/teco/output/03_multivariada/teco_multivariada.gpkg [camada name] — chamada j.to_file, linha 82.
- E:/teco/dados_publicos/lancamentos/manifesto_documentos.json — chamada .write_text, linha 88.

**Campos e chaves lidos.**

- b: geometry, id.

**Campos e chaves gerados.**

- v: prec_m, status.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| csv(x, n) | 41-41 | grava produtos |
| points(g) | 60-64 | Chamadas efetivas: candidates.append, hasattr, points |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_relevo_lancamentos_teco.py, linhas 46-52.

```python
  assert len(v)>0,f
  d.update_tags(1,STATISTICS_MINIMUM=str(float(v.min())),STATISTICS_MAXIMUM=str(float(v.max())),STATISTICS_MEAN=str(float(v.mean())),STATISTICS_STDDEV=str(float(v.std())),STATISTICS_VALID_PERCENT=str(100*len(v)/(d.width*d.height)),STATISTICS_APPROXIMATE='NO')
  stats.append({'arquivo':f.name,'validos':len(v),'min':float(v.min()),'max':float(v.max()),'nodata':d.nodata,'n_nan_validos':int(np.isnan(x).sum())})
csv(pd.DataFrame(stats),'auditoria_rasters.csv')
b=gpd.read_file(B/'teco_avaliacao.gpkg',layer='bacias_estudo')
ex=gpd.read_file(R/'sub_bacia/shapefiles_v6_20261109_141015/exutorios_finais.shp').to_crs(31983)
lake=gpd.read_file(R/'reservatorio/vargem_flores.shp').to_crs(31983).geometry.union_all()
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_tabnet_estabelecimentos.py

Auditar tabnet estabelecimentos. Auditoria/diagnóstico. A organização passa por obtain, cadastro, main.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\teco\codigo\auditar_tabnet_estabelecimentos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| requests | Consultas e downloads HTTP; depende de internet e da disponibilidade do provedor. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |
| urllib.parse | Requisições e manipulação de endereços de serviços públicos. |


**Entradas.**

- E:/teco/dados_publicos/auditoria_sih_20261112/campos_NRMG.json — chamada .read_text, linha 58.
- E:/teco/dados_publicos/auditoria_sih_20261112/cnes/{c}.json — chamada path.read_text, linha 86.
- E:/teco/dados_publicos/saude/campos_tabnet.json — chamada .read_text, linha 63.
- E:/teco/dados_publicos/cnes/{name} — chamada .read_text, linha 102.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'bacias_estudo'] — chamada gpd.read_file, linha 114.

**Saídas.**

- E:/teco/dados_publicos/auditoria_sih_20261112/consulta_estadual.json — chamada .write_text, linha 66.
- E:/teco/dados_publicos/auditoria_sih_20261112/cnes/{c}.json — chamada path.write_text, linha 90.
- E:/teco/output/05_auditoria_saude/tabnet_MG_internacoes_anuais.csv — chamada f.to_csv, linha 97.
- E:/teco/output/05_auditoria_saude/conferencia_todos_estabelecimentos_MG.csv — chamada a.to_csv, linha 118.
- E:/teco/output/05_auditoria_saude/conferencia_estabelecimentos_regiao.csv — chamada regional.to_csv, linha 119.
- E:/teco/output/05_auditoria_saude/estabelecimentos_producao_confirmada_bacias.csv — chamada inside.to_csv, linha 120.
- E:/teco/output/05_auditoria_saude/saude_tabnet_auditada.gpkg [camada 'producao_SIH_georreferenciada'] — chamada g.to_file, linha 121.
- E:/teco/output/05_auditoria_saude/saude_tabnet_auditada.gpkg [camada 'internacoes_dentro_bacias'] — chamada .to_file, linha 121.
- E:/teco/output/05_auditoria_saude/saude_tabnet_auditada.gpkg [camada 'bacias_referencia'] — chamada b.to_file, linha 121.
- E:/teco/output/05_auditoria_saude/auditoria.json — chamada .write_text, linha 124.

**Campos e chaves lidos.**

- item: ano, hospitais_todos.
- fields: Arquivos, Incremento.
- body: Arquivos.
- f.loc: AIH.
- f: ANO.
- j: codigo_cnes.
- a.loc: LAT, LON.
- b.loc: id.
- inside: AIH, BACIA, CNES, NOME_TABNET.

**Campos e chaves gerados.**

- a: BACIA, BORDA_500M, COORD_OK, DIST_BACIA_M, LAT, LON, SIT_ESPACIAL.
- g: BACIA, DIST_BACIA_M, SIT_ESPACIAL.
- meta: fonte_producao.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| obtain() | 55-81 | lê dados; grava produtos Retorno: f, pd.DataFrame(rows).groupby(['CNES', 'NOME_TABNET', 'ANO'], as_index=False).AIH.sum(). |
| cadastro(c) | 84-93 | lê dados; grava produtos Retorno: json.loads(path.read_text('utf8')), j. |
| main() | 96-124 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_tabnet_estabelecimentos.py, linhas 61-67.

```python
   for c,n in item['hospitais_todos'].items():rows.append({'CNES':c,'NOME_TABNET':names.get(c,'Nome não localizado no cadastro de opções NRMG'),'ANO':item['ano'],'AIH':n})
  return pd.DataFrame(rows).groupby(['CNES','NOME_TABNET','ANO'],as_index=False).AIH.sum()
 fields=json.loads((R/'dados_publicos/saude/campos_tabnet.json').read_text('utf8'))
 body={k:'TODAS_AS_CATEGORIAS__' for k in fields if k.startswith('S')}
 body.update(Linha='Estabelecimento',Coluna='Ano_processamento',Incremento=next(v for v,t in fields['Incremento'] if t.startswith('Interna')),Arquivos=[v for v,t in fields['Arquivos'] if 16<=int(v[4:6])<=25],formato='prn',mostre='Mostra');assert len(body['Arquivos'])==120
 (D/'consulta_estadual.json').write_text(json.dumps(body,ensure_ascii=False,indent=2),encoding='utf8');path=D/'tabnet_MG_estabelecimento_2016_2025.html'
 if path.exists():text=path.read_text('utf8')
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/auditar_tabnet_estabelecimentos.py, linhas 79-85.

```python
 f=pd.DataFrame(out);assert not f.duplicated(['CNES','ANO']).any()
 for y,n in total.items():assert f.loc[f.ANO==y,'AIH'].sum()==n,(y,n)
 return f

# Cadastro
def cadastro(c):
 path=D/'cnes'/f'{c}.json';path.parent.mkdir(exist_ok=True)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditoria_final_grade_teco.py

Auditoria final grade teco. Auditoria/diagnóstico. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\teco\codigo\auditoria_final_grade_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sqlite3 | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/output/04_grade_500m/auditoria/metodo_grade.json — chamada .read_text, linha 56.
- E:/teco/output/04_grade_500m/auditoria/coleta_rd.json — chamada .read_text, linha 56.
- E:/teco/output/04_grade_500m/auditoria/qgis_conferencia_final.json — chamada .read_text, linha 56.
- E:/teco/output/04_grade_500m/auditoria/galeria.json — chamada .read_text, linha 56.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'saude_todos'] — chamada gpd.read_file, linha 76.
- E:/teco/output/04_grade_500m/index.html — chamada .read_text, linha 67.
- E:/teco/output/04_grade_500m/tabelas/sih_cid10_mensal.csv — chamada pd.read_csv, linha 69.
- E:/teco/output/04_grade_500m/tabelas/sih_cid10_anual.csv — chamada pd.read_csv, linha 69.
- E:/teco/output/04_grade_500m/tabelas/sih_total_mensal.csv — chamada pd.read_csv, linha 69.
- E:/teco/output/02_avaliacao_espacial/tabelas/sih_bacias_2016_2025.csv — chamada pd.read_csv, linha 69.
- E:/teco/output/04_grade_500m/filtro_cid10.csv — chamada pd.read_csv, linha 71.
- {p} — chamada rasterio.open, linha 81.

**Saídas.**

- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'grade_resultados'] — chamada a.to_file, linha 63.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'influencia_500m'] — chamada cir.to_file, linha 63.
- E:/teco/output/04_grade_500m/auditoria/verificacao_final.json — chamada .write_text, linha 83.

**Campos e chaves lidos.**

- a: K_S0.
- f.loc: I_S0.
- row: slug.
- hour: CID10, internacoes.
- annual: internacoes.
- filt.loc: CID10.
- filt: incluir.
- monthly: internacoes.
- hour.loc: internacoes.
- rd: competencias_obtidas.
- qgis: camadas_invalidas, figuras_complementares_alta_resolucao, layouts.
- health: BACIA, CNES.
- r: slug.

**Campos e chaves gerados.**

- f: QUINTIL.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditoria_final_grade_teco.py, linhas 59-65.

```python
assert not a.duplicated(['GRID_ID','BACIA']).any() and a.geometry.is_valid.all()
assert a.K_S0.gt(0).sum()==592 and a.K_S0.eq(0).sum()==6
for f in [a,cir]:
 f['QUINTIL']=0;v=f.I_S0.notna();f.loc[v,'QUINTIL']=pd.qcut(f.loc[v,'I_S0'].rank(method='average'),5,labels=False,duplicates='drop')+1
f=a;a.to_file(G,layer='grade_resultados',driver='GPKG');cir.to_file(G,layer='influencia_500m',driver='GPKG')
with sqlite3.connect(G) as db:assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for row in gallery:
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/avaliar_saude_grade.py

Avaliar saude grade. Processamento ou módulo de apoio. A organização passa por csv, main, suggestion.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\avaliar_saude_grade.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| calendar | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- sys.argv[sys.argv.index('--planilha') + 1] — chamada zipfile.ZipFile, linha 56.
- E:/teco/output/04_grade_500m/filtro_cid10.csv — chamada pd.read_csv, linha 73.
- sys.argv[sys.argv.index('--planilha') + 1] — chamada path.read_text, linha 79.
- E:/teco/output/04_grade_500m/tabelas/sih_cid10_mensal.csv — chamada pd.read_csv, linha 82.
- E:/teco/output/04_grade_500m/filtro_cid10.csv — chamada pd.read_csv, linha 86.
- E:/teco/output/04_grade_500m/tabelas/cobertura_rd_unidades.csv — chamada pd.read_csv, linha 115.

**Saídas.**

- E:/teco/output/04_grade_500m/tabelas/{n} — chamada f.to_csv, linha 50.
- E:/teco/output/04_grade_500m/filtro_cid10.csv — chamada .to_csv, linha 76.
- E:/teco/output/04_grade_500m/filtro_cid10.csv — chamada filt.to_csv, linha 92.
- E:/teco/output/04_grade_500m/auditoria/filtro_aplicado.json — chamada .write_text, linha 95.
- E:/teco/output/04_grade_500m/figuras/{slug}.{ext} — chamada fig.savefig, linha 105.
- E:/teco/output/04_grade_500m/explorador_internacoes.html — chamada .write_text, linha 118.
- E:/teco/output/04_grade_500m/auditoria/galeria_saude.json — chamada .write_text, linha 119.

**Campos e chaves lidos.**

- vals: A.
- f: CID10, CNES, diagnostico.
- filt.loc: CID10.
- ax3.spines: right, top.

**Campos e chaves gerados.**

- f: diagnostico.
- filt: grupo_para_revisao, incluir, justificativa.
- monthly: dias_mes, internacoes, internacoes_dia, unidade.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| csv(f, n) | 50-50 | grava produtos |
| main() | 53-119 | lê dados; grava produtos Retorno: '  /  '.join((label for lo, hi, label in groups if lo <= c[:3] <= hi)). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/avaliar_saude_grade.py, linhas 82-88.

```python
 f=pd.read_csv(T/'sih_cid10_mensal.csv',sep=';',dtype={'CNES':str,'CID10':str});f['diagnostico']=f.CID10.map(desc).fillna('Descrição não localizada na tabela oficial consultada')
 csv(f,'sih_cid10_mensal.csv');a=f.groupby(['CNES','unidade','ano','CID10','diagnostico'],as_index=False)[['internacoes','dias']].sum();csv(a,'sih_cid10_anual.csv')
 groups=[('A00','A09','Infecções intestinais: selecionar etiologia bacteriana; inclui causas não bacterianas'),('A15','A19','Tuberculose'),('A30','A31','Micobactérias'),('A40','A41','Septicemias bacterianas'),('G00','G00','Meningite bacteriana'),('J13','J15','Pneumonias bacterianas'),('N10','N10','Nefrite tubulointersticial aguda: etiologia a conferir'),('N30','N30','Cistite: etiologia a conferir'),('N39','N39','Trato urinário: selecionar subcódigo; etiologia não garantida'),('L00','L08','Infecções de pele/tecido subcutâneo: etiologia a conferir'),('B95','B96','Agente bacteriano adicional; pode não aparecer no diagnóstico principal'),('U82','U83','Resistência antimicrobiana: código adicional; cobertura do campo principal limitada')]
 def suggestion(c):return ' | '.join(label for lo,hi,label in groups if lo<=c[:3]<=hi)
 filterfile=O/'filtro_cid10.csv';old=pd.read_csv(filterfile,sep=';',dtype={'CID10':str}) if filterfile.exists() else pd.DataFrame()
 filt=f[['CID10','diagnostico']].drop_duplicates().sort_values('CID10');filt['grupo_para_revisao']=filt.CID10.map(suggestion);filt['incluir']=False;filt['justificativa']='Aguardar seleção do pesquisador'
 if len(old):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/avaliar_saude_grade.py, linhas 94-100.

```python
 status='Filtro amplo · bacterianas codificadas e síndromes compatíveis' if selected else 'Seleção vazia · nenhuma causa incluída'
 (O/'auditoria/filtro_aplicado.json').write_text(json.dumps({'CID_selecionados':len(selected),'AIH_selecionadas':int(ff.internacoes.sum()),'criterio':'Seleção explícita da tabela filtro_cid10.csv; vazio não significa todas as causas.'},ensure_ascii=False,indent=2),encoding='utf8')
 totals_all=f.groupby(['CNES','unidade','ano','mes'],as_index=False).internacoes.sum();csv(totals_all,'sih_todas_causas_mensal.csv');csv(totals_all.groupby(['CNES','unidade','ano'],as_index=False).internacoes.sum(),'sih_todas_causas_anual.csv')
 monthly=ff.groupby(['CNES','unidade','ano','mes'],as_index=False).internacoes.sum();idx=pd.MultiIndex.from_product([sorted(f.CNES.unique()),range(2016,2026),range(1,13)],names=['CNES','ano','mes']);monthly=monthly.set_index(['CNES','ano','mes']).reindex(idx).reset_index();monthly['internacoes']=monthly.internacoes.fillna(0);names=f.groupby('CNES').unidade.first();monthly['unidade']=monthly.CNES.map(names);monthly['dias_mes']=[calendar.monthrange(int(y),int(m))[1] for y,m in zip(monthly.ano,monthly.mes)];monthly['internacoes_dia']=monthly.internacoes/monthly.dias_mes
 csv(monthly,'sih_total_mensal.csv');annual=monthly.groupby(['CNES','unidade','ano'],as_index=False).internacoes.sum();csv(annual,'sih_total_anual.csv')
 patterns=monthly.groupby(['CNES','unidade','mes'],as_index=False).agg(media_internacoes=('internacoes','mean'),sd_internacoes=('internacoes','std'),media_por_dia=('internacoes_dia','mean'));csv(patterns,'sih_sazonalidade.csv');summary=[];gallery=[]
 for c,g in monthly.groupby('CNES'):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/caminhos_teco.mjs

Caminhos teco. Configuração compartilhada. A organização passa por settings, raizProjeto, caminho, callback, externo, adaptarTexto, callback, adaptarRuntime.

**Papel.** Configuração compartilhada. **Fonte inspecionada.** E:\teco\codigo\caminhos_teco.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| node:fs | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:path | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:url | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |


**Entradas.**

- process.env[envKey+'_CONFIG'] /  / path.join(code,'caminhos_projeto.json') — chamada fs.readFileSync, linha 14.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/caminhos_teco.mjs, linhas 14-22.

```javascript
const settings=()=>JSON.parse(fs.readFileSync(process.env[envKey+'_CONFIG']||path.join(code,'caminhos_projeto.json'),'utf8').replace(/^\uFEFF/,''));

// Configuração e raiz
export function raizProjeto(style='posix'){
 const c=settings();let r=process.env[envKey]||(project==='congonhas'?process.env.EMI_PROJECT_ROOT:'')||c.raiz_projeto||path.dirname(code);
 r=path.isAbsolute(r)?r:path.resolve(code,r);return style==='posix'?r.replaceAll('\\','/'):r;
}

// Pastas e arquivos
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/caminhos_teco.ps1

Caminhos teco. Configuração compartilhada. A organização passa por Get, Get, Get, Get, Convert.

**Papel.** Configuração compartilhada. **Fonte inspecionada.** E:\teco\codigo\caminhos_teco.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/caminhos_teco.ps1, linhas 12-20.

```text
function Get-PortableSettings { Get-Content -LiteralPath $script:PortableConfig -Raw -Encoding UTF8 | ConvertFrom-Json }
function Get-PortableRoot {
 $c=Get-PortableSettings
 $name="TECO_PROJECT_ROOT"
 $value=[Environment]::GetEnvironmentVariable($name)
 if(-not $value -and "teco" -eq 'congonhas'){$value=$env:EMI_PROJECT_ROOT}
 if(-not $value){$value=$c.raiz_projeto}
 if(-not $value){return (Split-Path $script:PortableCode -Parent)}
 if([System.IO.Path]::IsPathRooted($value)){return $value}
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/caminhos_teco.py

Caminhos teco. Configuração compartilhada. A organização passa por configuracao, raiz_projeto, caminho, texto_caminho, externo, adaptar_texto.

**Papel.** Configuração compartilhada. **Fonte inspecionada.** E:\teco\codigo\caminhos_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- Path(override).expanduser() if override else CONFIG_FILE — chamada path.read_text, linha 24.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- entry: chave, original.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| configuracao() | 21-24 | lê dados Retorno: json.loads(path.read_text('utf-8-sig')) if path.exists() else {}. |
| raiz_projeto() | 26-35 | Chamadas efetivas: configuracao, cfg.get, .strip, .expanduser, p.is_absolute, .resolve, os.environ.get, Path Retorno: BASE_CODIGO.parent, p if p.is_absolute() else (BASE_CODIGO / p).resolve(). |
| caminho(relativo='') | 38-47 | Chamadas efetivas: configuracao, raiz_projeto, .strip, sorted, cfg.get, .replace, rel.startswith, .expanduser Retorno: root / rel if rel else root, base / suffix if suffix else base. |
| texto_caminho(relativo='', estilo='posix') | 49-51 | Chamadas efetivas: caminho, p.as_posix, str Retorno: p.as_posix() if estilo == 'posix' else str(p). |
| externo(chave) | 54-68 | Chamadas efetivas: configuracao, .get, .expanduser, KeyError, isinstance, entry.get, str, ValueError Retorno: p.as_posix() if '/' in text and '\\' not in text else str(p). |
| adaptar_texto(texto) | 71-89 | Chamadas efetivas: configuracao, cfg.get, .values, re.compile, pattern.sub, original.replace, texto_caminho, .join Retorno: pattern.sub(lambda m: pairs[m[0]], str(texto)), texto. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/caminhos_teco.py, linhas 26-34.

```python
def raiz_projeto():
    cfg=configuracao()
    explicit=os.environ.get(ENV_RAIZ,'').strip() or (os.environ.get('EMI_PROJECT_ROOT','').strip() if PROJETO=='congonhas' else '') or cfg.get('raiz_projeto','')
    if explicit:
        p=Path(explicit).expanduser()
        return p if p.is_absolute() else (BASE_CODIGO/p).resolve()
    if cfg.get('modo_entrega'):
        for p in BASE_CODIGO.parents:
            if (p/'01_entradas').is_dir() and (p/'02_saidas').is_dir():return p
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/comparar_kmeans_sensibilidade_teco.py

Comparar kmeans sensibilidade teco. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\comparar_kmeans_sensibilidade_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/00_documentacao/tabelas/kmeans_grade.csv — chamada pd.read_csv, linha 33.
- E:/teco/entrega_final/00_documentacao/tabelas/cenarios_grade.csv — chamada pd.read_csv, linha 33.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada mfile.read_text, linha 49.

**Saídas.**

- {directory}/Comparacao_kmeans_sensibilidade.json — chamada .write_text, linha 41.
- E:/teco/entrega_final/00_documentacao/Comparacao_kmeans_sensibilidade.csv — chamada table.to_csv, linha 42.
- E:/teco/entrega_final/00_documentacao/Comparacao_kmeans_sensibilidade.md — chamada .write_text, linha 48.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada mfile.write_text, linha 49.

**Campos e chaves lidos.**

- best: cenario, k, menor_grupo, silhouette.
- table: ARI, cenario, descricao, k, menor_grupo, mesmo_grupo_pct, peso_aih_local, peso_populacao, peso_sem_rede, silhouette.
- x: ARI, cenario, mesmo_grupo_pct, peso_aih_local, peso_populacao, peso_sem_rede, silhouette.

**Campos e chaves gerados.**

- m: comparacao_kmeans_sensibilidade.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/comparar_kmeans_sensibilidade_teco.py, linhas 32-40.

```python
R=Path(_cp_texto('', 'posix'));F=R/'entrega_final';D=F/'00_documentacao';T=D/'tabelas'
fits=pd.read_csv(T/'kmeans_grade.csv',sep=';',decimal=',');scenarios=pd.read_csv(T/'cenarios_grade.csv',sep=';',decimal=',')
best=fits.loc[fits.groupby('cenario').silhouette.idxmax()].copy();assert best.k.eq(2).all()
table=scenarios.merge(best[['cenario','k','silhouette','menor_grupo']],on='cenario',validate='one_to_one')
selected=table.loc[table.silhouette.idxmax()];assert selected.cenario=='S2'
records=table[['cenario','descricao','peso_populacao','peso_sem_rede','peso_aih_local','k','silhouette','ARI','mesmo_grupo_pct','menor_grupo']].to_dict('records')
text='Entre os cenários testados, S2 com dois grupos apresentou a maior silhouette (0,742), mantendo 98,3% das unidades no mesmo perfil de S0 e ARI de 0,932. S2 atribui pesos 1:3:1 a população, ausência de rede e internações locais. O cenário base S0, com pesos iguais, permanece como referência e apresentou silhouette de 0,668. Todos os cinco cenários selecionaram dois grupos entre as soluções com k de 2 a 6.'
limit='As silhouettes descrevem geometrias de distâncias alteradas pelos pesos. O maior valor em S2 indica maior separação sob a ênfase em ausência de rede, não comprova maior acurácia ambiental ou sanitária. A escolha de um peso três vezes maior exige justificativa substantiva; por isso S2 é mantido como sensibilidade e S0 como referência.'
data={'resultado':text,'interpretacao':limit,'numero_unidades_validas':592,'unidades_alteradas_S2':10,'referencia':'S0','maior_separacao':'S2','melhor_k_em_todos_cenarios':2,'comparacao':records}
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/complementar_entrega_final.py

Complementar entrega final. Consolidação/migração: conferir pré-condições. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Consolidação/migração: conferir pré-condições. **Fonte inspecionada.** E:\teco\codigo\complementar_entrega_final.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| consolidar_entrega_final | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- c.F/00_documentacao/manifesto.json — chamada p.read_text, linha 33.
- c.R/output/01_integracao_territorial/integracao_territorial_teco.gpkg [camada 'ete_cadastro'] — chamada gpd.read_file, linha 38.
- c.F/00_documentacao/Dicionario_dos_campos.csv — chamada pd.read_csv, linha 41.
- c.B/tabelas/linhagem_fontes_tratamento.csv — chamada pd.read_csv, linha 45.

**Saídas.**

- c.F/00_documentacao/Dicionario_dos_campos.csv — chamada dic.to_csv, linha 41.
- c.F/00_documentacao/Linhagem_das_bases.csv — chamada lin.to_csv, linha 47.
- c.F/00_documentacao/Inventario_de_camadas.csv — chamada .to_csv, linha 55.
- c.F/00_documentacao/manifesto.json — chamada p.write_text, linha 56.

**Campos e chaves lidos.**

- r: arquivo, campos.
- m: rasters, vetores.
- lin: produto.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/complementar_entrega_final.py, linhas 32-40.

```python
import consolidar_entrega_final as c
F=c.F;D=F/'00_documentacao';p=D/'manifesto.json';m=json.loads(p.read_text('utf8'));c.VECTORS=[];c.FIELDS=[]
source=c.R/'output/01_integracao_territorial/integracao_territorial_teco.gpkg'
if not any('14_rede_cadastral_BH' in r['arquivo'] for r in m['vetores']):
 a=gpd.read_file(source,layer='rede_bh_consolidada').rename(columns={'bas_id':'BACIA','bas_nome':'NOME_BACIA'})
 c.shapefile(a,'01_entradas/14_rede_cadastral_BH/rede_BH.shp','referencia','Rede cadastrada por trecho - apenas domínio de BH',str(source)+'|rede_bh_consolidada')
 a=gpd.read_file(source,layer='ete_cadastro').rename(columns={'bas_id':'BACIA','bas_nome':'NOME_BACIA'})
 c.shapefile(a,'01_entradas/15_ETE_cadastro/ETE.shp','referencia','Estações de tratamento no cadastro recebido',str(source)+'|ete_cadastro')
 m['vetores']+=c.VECTORS
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/conectividade_grade_teco.py

Roteia pelo terreno D8 a área válida e o índice de pressão a montante. Produz área contribuinte e pressão média topográfica; não calcula vazão, concentração de genes nem transporte na rede de esgoto.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\conectividade_grade_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'grade_resultados'] — chamada gpd.read_file, linha 34.
- E:/teco/sub_bacia/{key}/direcao_d8.tif — chamada rasterio.open, linha 36.
- E:/teco/reservatorio/{key}.shp — chamada gpd.read_file, linha 38.

**Saídas.**

- E:/teco/output/04_grade_500m/rasters/{key}_{suffix}.tif — chamada rasterio.open, linha 51.
- E:/teco/output/04_grade_500m/tabelas/conectividade_montante.csv — chamada .to_csv, linha 53.
- E:/teco/output/04_grade_500m/auditoria/conectividade.json — chamada .write_text, linha 53.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 33-53 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/conectividade_grade_teco.py, linhas 41-47.

```python
   yy,xx=np.where((dr==code)&domain&~lm);ny=yy+dy;nx=xx+dx;ok=(ny>=0)&(ny<h)&(nx>=0)&(nx<w);src=yy[ok]*w+xx[ok];dst=ny[ok]*w+nx[ok];ok2=domain.ravel()[dst];dest[src[ok2]]=dst[ok2]
  area=np.where(valid&~lm,abs(t.a*t.e)/1e6,0).ravel();weighted=np.where(valid&~lm,lab,0).ravel()*area;indeg=np.bincount(dest[dest>=0],minlength=n);queue=deque(np.flatnonzero(domain.ravel()&(indeg==0)));processed=0
  while queue:
   j=queue.popleft();processed+=1;k=dest[j]
   if k>=0:
    area[k]+=area[j];weighted[k]+=weighted[j];indeg[k]-=1
    if indeg[k]==0:queue.append(k)
```

Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.

**Cálculos a observar nesta rotina.**

- bincount: Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/conferir_e_abrir_saneamento_qgis.py

Conferência no QGIS instalado e projeto independente, sem alterar o original.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\teco\codigo\conferir_e_abrir_saneamento_qgis.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/teco/saneamento_ibge/resultados/conferencia_qgis.json — chamada .write_text, linha 62.

**Campos e chaves gerados.**

- os.environ: QT_QPA_PLATFORM.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/conferir_e_abrir_saneamento_qgis.py, linhas 9-17.

```python
"""Conferência no QGIS instalado e projeto independente, sem alterar o original."""
# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_teco.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_teco.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/conferir_qgis_grade_teco.py

Conferir qgis grade teco. Conferência/teste. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\teco\codigo\conferir_qgis_grade_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtGui | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/04_grade_500m/auditoria/galeria_mapas.json — chamada .read_text, linha 51.

**Saídas.**

- E:/teco/output/04_grade_500m/auditoria/qgis_conferencia_final.json — chamada .write_text, linha 58.

**Campos e chaves lidos.**

- rec: max, min.
- r: mapas, valida.
- row: slug, titulo.

**Campos e chaves gerados.**

- os.environ: QT_QPA_FONTDIR, QT_QPA_PLATFORM.
- rec: feicoes, max, min.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/conferir_qgis_grade_teco.py, linhas 50-58.

```python
extra=0
for row in json.loads((O/'auditoria/galeria_mapas.json').read_text('utf8')):
 if row['slug'] in native:continue
 name='TECO500 | Figura | '+row['titulo'];manager=p.layoutManager();old=manager.layoutByName(name)
 if old:manager.removeLayout(old)
 layout=QgsPrintLayout(p);layout.initializeDefaults();layout.setName(name);layout.pageCollection().pages()[0].setPageSize(QgsLayoutSize(300,127));picture=QgsLayoutItemPicture(layout);layout.addLayoutItem(picture);picture.attemptMove(QgsLayoutPoint(0,0));picture.attemptResize(QgsLayoutSize(300,127));picture.setPicturePath(str(O/'figuras'/f"{row['slug']}.png"));manager.addLayout(layout);extra+=1;print('FIGURA_QGIS',row['slug'],flush=True)
groups=group.findGroup('07 Suporte aos layouts') or group.findGroup('07 Layout support layers');groups.setExpanded(False)
assert p.write(str(R/'projeto_teco.qgz'));p.setFileName(str(O/'TECO_grade_500m.qgz'));assert p.write()
(O/'auditoria/qgis_conferencia_final.json').write_text(json.dumps({'camadas':len(records),'camadas_invalidas':len(bad),'layouts':layoutcounts,'figuras_complementares_alta_resolucao':extra,'detalhes':records},ensure_ascii=False,indent=2),encoding='utf8');print('QGIS_CONFERIDO',len(records),'LAYOUTS',len(layoutcounts),'FIGURAS',extra,flush=True)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/consolidar_avaliacao_teco.py

Conferência de entregas, linhagem de dados e figuras complementares TECO.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\consolidar_avaliacao_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| analise_espacial_teco | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada name] — chamada gpd.read_file, linha 56.
- E:/teco/output/02_avaliacao_espacial/shapefiles/{name}.shp — chamada gpd.read_file, linha 56.
- E:/teco/output/02_avaliacao_espacial/tabelas/sih_bacias_2016_2025.csv — chamada pd.read_csv, linha 60.
- E:/teco/output/02_avaliacao_espacial/auditoria/galeria.json — chamada .read_text, linha 72.
- E:/teco/{f} — chamada open, linha 93.
- E:/teco/output/02_avaliacao_espacial/auditoria/auditoria.json — chamada .read_text, linha 99.

**Saídas.**

- E:/teco/output/02_avaliacao_espacial/figuras/19_atividade_hospitalar_2016_2025.{ext} — chamada fig.savefig, linha 70.
- E:/teco/output/02_avaliacao_espacial/auditoria/galeria.json — chamada .write_text, linha 73.
- E:/teco/output/02_avaliacao_espacial/tabelas/linhagem_fontes_tratamento.csv — chamada df.to_csv, linha 94.
- E:/teco/output/02_avaliacao_espacial/tabelas/resumo_analise_bacias.csv — chamada .to_csv, linha 98.
- E:/teco/output/02_avaliacao_espacial/auditoria/auditoria.json — chamada .write_text, linha 101.
- E:/teco/output/02_avaliacao_espacial/Populacao_Esgotamento_Shapefiles.zip — chamada zipfile.ZipFile, linha 102.
- E:/teco/output/02_avaliacao_espacial/LEIA_PRIMEIRO.md — chamada .write_text, linha 106.

**Campos e chaves lidos.**

- whole: CD_SETOR.
- san: CD_SETOR.
- hist: ano_processamento, dias_permanencia, internacoes.
- ax.spines: right, top.
- r: slug.
- df: arquivo_entrada.
- g.loc: rec_km2.
- audit: verificacao_final.

**Campos e chaves gerados.**

- df: sha256_entrada.
- audit: verificacao_final.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/consolidar_avaliacao_teco.py, linhas 61-67.

```python
assert hist.ano_processamento.between(2016,2025).all() and not hist.duplicated(['CNES','ano_processamento']).any()
assert hist.internacoes.sum()==242648
fig,axs=plt.subplots(1,2,figsize=(11.8,3.9),layout='constrained');colors=['#3a7f9b','#b56644','#6d8c67'];labels={'2191164':'Centro Materno Infantil','2200473':'Hospital Municipal de Contagem','6892256':'Hospital Regional de Ibirité'}
for (code,g),co in zip(hist.groupby('CNES'),colors):
    g=g.sort_values('ano_processamento')
    for ax,col in zip(axs,['internacoes','dias_permanencia']):ax.plot(g.ano_processamento,g[col]/1000,'o-',color=co,label=labels.get(code,code),lw=1.7,ms=4)
for ax,la in zip(axs,['Internações SUS (mil)','Dias de permanência (mil)']):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/consolidar_avaliacao_teco.py, linhas 96-102.

```python
for key,g in a.groupby('bas_id'):
    bas.append({'bacia':key,'area_km2':g.rec_km2.sum(),'pop_est':g.pop_a_est.sum(),'recortes':len(g),'com_indice':int((g.quintil>0).sum()),'sem_indice':int((g.quintil==0).sum()),'area_completa_pct':100*g.loc[g.quintil>0,'rec_km2'].sum()/g.rec_km2.sum()})
pd.DataFrame(bas).to_csv(O/'tabelas/resumo_analise_bacias.csv',index=False,encoding='utf-8-sig',sep=';',decimal=',')
audit=json.loads((O/'auditoria/auditoria.json').read_text(encoding='utf8'))
audit['verificacao_final']={'geometrias_pop_esgoto_iguais':True,'shapefiles_reabertos':4,'campos_populacao':[c for c in whole.columns if c!='geometry'],'internacoes_sih_bacias_2016_2025':int(hist.internacoes.sum()),'dias_permanencia_sih_bacias':float(hist.dias_permanencia.sum()),'linhas_sih':len(hist),'figuras':len(gallery),'insumos_originais_preservados':True}
(O/'auditoria/auditoria.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
with zipfile.ZipFile(O/'Populacao_Esgotamento_Shapefiles.zip','w',zipfile.ZIP_DEFLATED) as z:
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/consolidar_entrega_final.py

Consolidar entrega final. Processamento ou módulo de apoio. A organização passa por slug, desc, shapefile, raster, copy, main.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\consolidar_entrega_final.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| dicionario_campos_teco | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unicodedata | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| zoneinfo | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

- E:/teco/entrega_final/{rel} — chamada gpd.read_file, linha 87.
- E:/teco/entrega_final/{rel} — chamada rasterio.open, linha 97.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'influencia_500m'] — chamada gpd.read_file, linha 146.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'rotas_d8_candidatas'] — chamada gpd.read_file, linha 147.
- E:/teco/reservatorio/{key}.shp — chamada gpd.read_file, linha 118.
- E:/teco/config/encartes_teco.json — chamada .read_text, linha 125.
- E:/teco/output/05_auditoria_saude/saude_tabnet_auditada.gpkg [camada 'rede_internacoes_residentes'] — chamada gpd.read_file, linha 129.
- E:/teco/output/03_multivariada/teco_multivariada.gpkg [camada 'exutorios_referencia'] — chamada gpd.read_file, linha 130.
- {p} — chamada gpd.read_file, linha 133.
- E:/teco/output/04_grade_500m/auditoria/galeria.json — chamada .read_text, linha 150.
- E:/teco/output/04_grade_500m/auditoria/metodo_grade.json — chamada .read_text, linha 161.
- E:/teco/output/05_auditoria_saude/consolidacao.json — chamada .read_text, linha 161.

**Saídas.**

- E:/teco/entrega_final/{rel} — chamada g.to_file, linha 86.
- path.parent/dicionario_campos.csv — chamada .to_csv, linha 91.
- E:/teco/entrega_final/00_documentacao/Dicionario_dos_campos.csv — chamada .to_csv, linha 160.
- E:/teco/entrega_final/00_documentacao/Inventario_de_camadas.csv — chamada .to_csv, linha 160.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .write_text, linha 162.

**Campos e chaves lidos.**

- r: arquivo.
- record: arquivo.
- b: geometry, id.
- c: V00309, V00310, V00311, V00312, V00313, V00314, V00315, V00316, bas_id, dens_pop, dom_set, n_sigilo, pct_nrede, pct_rede, pct_vrio, pop_2022, pop_a_est, rede_set, setor_id.
- hyd: BACIA, geometry, id.
- b.loc: id.
- roads: TIPO_VIA, geometry, hier_legal, ogc_fid.
- q: Name, geometry.
- row: grupo, slug.

**Campos e chaves gerados.**

- ww: AREA_KM2.
- hyd: COMP_KM.
- inner: COMP_KM.
- q: BACIA.
- a: AREA_CEL.
- km: PERFIL_S0.
- row: titulo.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| slug(text) | 64-64 | Chamadas efetivas: .strip, re.sub, .lower, .decode, .encode, unicodedata.normalize Retorno: re.sub('[^a-z0-9]+', '_', unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()).strip('_'). |
| desc(field, arquivo='') | 67-68 | Chamadas efetivas: descrever_campo Retorno: descrever_campo(field, arquivo). |
| shapefile(g, rel, role, title, source) | 71-92 | lê dados; grava produtos Retorno: path. |
| raster(src, rel, role, title) | 95-102 | Chamadas efetivas: dst.parent.mkdir, shutil.copy2, str, rasterio.open, d.read, vals.compressed, len, RASTERS.append Retorno: dst. |
| copy(src, rel) | 105-106 | Chamadas efetivas: dst.parent.mkdir, shutil.copy2 Retorno: dst. |
| main() | 109-162 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/consolidar_entrega_final.py, linhas 89-95.

```python
  if c in mapping:assert read[mapping[c]].astype('string').equals(g[mapping[c]].astype('string')),(title,c)
 record={'arquivo':str(Path(rel)).replace('\\','/'),'titulo':title,'papel':role,'feicoes':len(g),'sem_geometria':int(g.geometry.isna().sum()),'crs':'EPSG:31983','fonte':source,'campos':mapping};VECTORS.append(record)
 pd.DataFrame([r for r in FIELDS if r['arquivo']==record['arquivo']]).to_csv(path.parent/'dicionario_campos.csv',sep=';',index=False,encoding='utf-8-sig')
 print('SHP',path.stem,len(g),flush=True);return path

# Raster
def raster(src,rel,role,title):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/consolidar_final_auditado_teco.py

Consolidar final auditado teco. Processamento ou módulo de apoio. A organização passa por copy, safe_remove, main, shp.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\consolidar_final_auditado_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| consolidar_entrega_final | Módulo autoral local; sua ficha está neste relatório. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 81.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada layer] — chamada gpd.read_file, linha 100.
- E:/teco/tmp/consolidacao_final/testes_kmeans.gpkg [camada layer] — chamada gpd.read_file, linha 94.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'rotas_d8_candidatas'] — chamada gpd.read_file, linha 101.
- E:/teco/tmp/consolidacao_final/entrega_final/01_entradas/03_populacao/populacao.shp — chamada gpd.read_file, linha 110.
- next(ib.glob('*basico*study_sectors.csv')) — chamada pd.read_csv, linha 110.
- export.shapefile(g, rel, role, title, source) — chamada p.read_text, linha 116.
- E:/teco/output/05_auditoria_saude/todos_municipios_bacias/Todas_unidades_8_municipios.csv — chamada pd.read_csv, linha 120.
- E:/teco/output/05_auditoria_saude/todos_municipios_bacias/TabNet_NRMG_anual_8_municipios.csv — chamada pd.read_csv, linha 120.
- E:/teco/output/05_auditoria_saude/saude_tabnet_auditada.gpkg [camada 'producao_SIH_georreferenciada'] — chamada gpd.read_file, linha 121.
- E:/teco/tmp/consolidacao_final/Kmeans_all_25_verified.csv — chamada pd.read_csv, linha 124.
- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/Dicionario_dos_campos.csv — chamada pd.read_csv, linha 130.
- Mais 2 referências na ficha HTML e no inventário JSON.

**Saídas.**

- export.shapefile(g, rel, role, title, source) — chamada p.write_text, linha 116.
- E:/teco/tmp/consolidacao_final/entrega_final/04_datasus/01_conjunto_8_municipios/Cadastro_completo_unidades.csv — chamada .to_csv, linha 122.
- E:/teco/tmp/consolidacao_final/entrega_final/04_datasus/01_conjunto_8_municipios/Unidades_fisicamente_nas_bacias.csv — chamada .to_csv, linha 122.
- E:/teco/tmp/consolidacao_final/entrega_final/02_saidas/02_testes/02_kmeans/{r.scenario}/k{r.k}/metrics.csv — chamada .to_csv, linha 126.
- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/Dicionario_dos_campos.csv — chamada dic.to_csv, linha 130.
- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/manifesto.json — chamada .write_text, linha 132.
- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/Inventario_de_camadas.csv — chamada .to_csv, linha 132.
- E:/teco/tmp/consolidacao_final/entrega_final/02_saidas/LEIA_PRIMEIRO.md — chamada .write_text, linha 133.

**Campos e chaves lidos.**

- m: old_to_new_paths, rasters, vetores.
- r: arquivo, fonte.
- a: BACIA, COB_ESG, ESTABILIDADE, EST_ESG, GRID_ID, I_S0, K_S0, MORAN, MORAN_Q, QUINTIL, VALIDO, geometry.
- master: arquivo.
- new: arquivo.
- raw: CD_SETOR.
- units: AIH_NRMG, CNES, RES8_TOTAL.
- geo: BACIA, CNES, DIST_BACIA_M, MUNICIPIO, geometry.
- points: BACIA, RES8_A, RES8_AB, RES8_B.
- olddic: arquivo.
- newdic: arquivo.

**Campos e chaves gerados.**

- m: IBGE_complete_tables, authoritative_result, health_all_municipalities, old_to_new_paths, responsible, test_hierarchy, updated, vetores.
- a: AREA_CEL, PERFIL_S0.
- q: SCENARIO, W_HEALTH, W_POP, W_SEWER.
- mo: MOR_ELIG.
- : 02_saidas/09_rotas_terreno/rotas_terreno.shp.
- r: arquivo.
- units: AIH_NRMG, DIF_RES.
- points: AIH_A, AIH_AB, AIH_B, MEDIA_ANUAL_AB, SIT_ESPACIAL.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| copy(src, dst) | 72-72 | Chamadas efetivas: dst.parent.mkdir, shutil.copy2 |
| safe_remove(p) | 75-77 | Chamadas efetivas: p.exists, .is_relative_to, shutil.rmtree, F.resolve, p.resolve |
| main() | 80-134 | lê dados; grava produtos Retorno: record. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/consolidar_final_auditado_teco.py, linhas 119-125.

```python

 units=pd.read_csv(H/'Todas_unidades_8_municipios.csv',sep=';',dtype={'CNES':str});tab=pd.read_csv(H/'TabNet_NRMG_anual_8_municipios.csv',sep=';',dtype={'CNES':str,'MUN_RES':str});official=tab.groupby('CNES').AIH_TABNET.sum();units['AIH_NRMG']=units.CNES.map(official).fillna(0).astype(int);units['DIF_RES']=units.RES8_TOTAL-units.AIH_NRMG
 geo=gpd.read_file(R/'output/05_auditoria_saude/saude_tabnet_auditada.gpkg',layer='producao_SIH_georreferenciada');geo=geo[['CNES','MUNICIPIO','BACIA','DIST_BACIA_M','geometry']];units=units.merge(geo,on='CNES',how='left',validate='one_to_one');points=gpd.GeoDataFrame(units,geometry='geometry',crs=31983);points['SIT_ESPACIAL']=np.where(points.geometry.isna(),'Coordenada pendente, produção confirmada',np.where(points.BACIA.fillna('').str.strip().ne(''),'Localização dentro das bacias','Instituição fora das bacias'));points['AIH_A']=points.RES8_A;points['AIH_B']=points.RES8_B;points['AIH_AB']=points.RES8_AB;points['MEDIA_ANUAL_AB']=points.RES8_AB/10;points=points.rename(columns={'NOME':'NOME_TABNET','PROD_TOTAL':'PROD_TOT','RES8_TOTAL':'RES_RD'});hp='01_entradas/09_saude_residencia/saude_residencia.shp';m['vetores']=[r for r in m['vetores'] if r['arquivo']!=hp];shp(points,hp,'Admitting facilities for residents of all eight municipalities','input',str(H/'Todas_unidades_8_municipios.csv'))
 points.drop(columns='geometry').to_csv(target/'Cadastro_completo_unidades.csv',sep=';',index=False,encoding='utf-8-sig');local=points[points.BACIA.fillna('').str.strip().ne('')];assert len(local)==3;local.drop(columns='geometry').to_csv(target/'Unidades_fisicamente_nas_bacias.csv',sep=';',index=False,encoding='utf-8-sig')

 km=pd.read_csv(T/'Kmeans_all_25_verified.csv',sep=';')
 for r in km.itertuples():
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/consolidar_final_auditado_teco.py, linhas 133-135.

```python
 (F/'02_saidas/LEIA_PRIMEIRO.md').write_text('# Resultados consolidados\n\nA camada principal é `01_consolidado/TECO_final.shp`. Ela reúne as 598 unidades de apresentação e os resultados de referência. As seis unidades incompletas continuam identificadas, sem converter lacunas em zero.\n\nEm `02_testes`, cada análise contém seus cenários e, no k-means, cada valor de k. Os 25 ajustes foram reproduzidos e conferidos. Os perfis de k>2 foram numerados pela média do escore dentro do teste, sem representar classes legais ou uma ordem universal de risco.\n\nOs círculos de cálculo, centros e rotas ficam em `03_support`. Rasters de conectividade ficam em `04_connectivity`, separados por produto e bacia. As contagens de círculos sobrepostos não devem ser somadas como totais de bacia.\n',encoding='utf8')
 print(json.dumps({'vectors':len(m['vetores']),'rasters':len(m['rasters']),'facilities_all_municipalities':len(points),'missing_coordinates':int(points.geometry.isna().sum()),'physically_inside':len(local),'master':master['arquivo']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/consolidar_saude_residencia.py

Consolidar saude residencia. Processamento ou módulo de apoio. A organização passa por save, main.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\consolidar_saude_residencia.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| filtro_bacteriano_teco | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/05_auditoria_saude/NRMG_internacoes_por_residencia_anuais.csv — chamada pd.read_csv, linha 59.
- E:/teco/output/05_auditoria_saude/RD_MG_residentes_mensal_CID10.csv — chamada pd.read_csv, linha 59.
- E:/teco/dados_publicos/saude_revisao/CID10_oficial_GO.json — chamada .read_text, linha 60.
- E:/teco/output/05_auditoria_saude/conferencia_todos_estabelecimentos_MG.csv — chamada pd.read_csv, linha 67.

**Saídas.**

- E:/teco/output/05_auditoria_saude/{n} — chamada f.to_csv, linha 55.
- rd[~rd.CID10.isin(desc)].copy() — chamada save, linha 61.
- nr.merge(annual, on=['CNES', 'MUN_RES', 'ANO'], how='outer', suffixes=('_NRMG', '_RD')) — chamada save, linha 62.
- pd.DataFrame({'CID10': codes, 'DIAGNOSTICO': [desc.get(c, 'Não localizado no dicionário de compatibilização consultado') for c in codes]}) — chamada save, linha 63.
- compatible.merge(classif[['CID10', 'NIVEL', 'INCLUIR_AB']], on='CID10', validate='many_to_one') — chamada save, linha 64.
- compatible.groupby(['CNES', 'MUN_RES', 'ANO', 'CID10', 'NIVEL'], as_index=False).AIH.sum() — chamada save, linha 64.
- compatible[compatible.INCLUIR_AB] — chamada save, linha 64.
- compatible.groupby(['CNES', 'MUN_RES', 'ANO', 'MES'], as_index=False).AIH.sum() — chamada save, linha 65.
- selected.groupby(['CNES', 'MUN_RES', 'ANO', 'MES'], as_index=False).AIH.sum() — chamada save, linha 65.
- hospitals.merge(geo, on='CNES', how='left', validate='one_to_one') — chamada save, linha 69.
- E:/teco/output/05_auditoria_saude/saude_tabnet_auditada.gpkg [camada 'rede_internacoes_residentes'] — chamada g.to_file, linha 70.
- nr.groupby(['MUN_RES', 'MUNICIPIO_RESIDENCIA'], as_index=False).agg(AIH=('AIH', 'sum'), ESTABELECIMENTOS=('CNES', 'nunique')) — chamada save, linha 71.
- Mais 2 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- x: code, display.
- official: concept.
- rd: AIH, CID10.
- cmp: AIH_NRMG, AIH_RD, DIFERENCA.
- classif: CID10, DIAGNOSTICO, INCLUIR_AB, NIVEL.
- nr: AIH.
- selected.loc: AIH.

**Campos e chaves gerados.**

- cmp: DIFERENCA.
- classif: GRUPO, INCLUIR_AB, NIVEL.
- hospitals: AIH_AB, MEDIA_ANUAL_AB.
- summary: AIH_AB.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| save(f, n) | 55-55 | grava produtos |
| main() | 58-76 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/consolidar_saude_residencia.py, linhas 60-66.

```python
 official=json.loads((R/'dados_publicos/saude_revisao/CID10_oficial_GO.json').read_text('utf8'));desc={x['code'].replace('.',''):x['display'] for x in official['concept']}
 unusual=rd[~rd.CID10.isin(desc)].copy();save(unusual,'RD_registros_codificacao_nao_mapeada.csv');assert unusual.AIH.sum()==18 and set(unusual.CID10)=={'N182','N183','N184','N185'}
 compatible=rd[rd.CID10.isin(desc)].copy();annual=compatible.groupby(['CNES','MUN_RES','ANO'],as_index=False).AIH.sum();cmp=nr.merge(annual,on=['CNES','MUN_RES','ANO'],how='outer',suffixes=('_NRMG','_RD'));cmp[['AIH_NRMG','AIH_RD']]=cmp[['AIH_NRMG','AIH_RD']].fillna(0);cmp['DIFERENCA']=cmp.AIH_RD-cmp.AIH_NRMG;assert cmp.DIFERENCA.eq(0).all();save(cmp,'conferencia_NRMG_RD_reconciliada.csv')
 codes=sorted(rd.CID10.unique());classif=pd.DataFrame({'CID10':codes,'DIAGNOSTICO':[desc.get(c,'Não localizado no dicionário de compatibilização consultado') for c in codes]});z=[classify(c,d) for c,d in zip(classif.CID10,classif.DIAGNOSTICO)];classif['NIVEL']=[a[0] for a in z];classif['GRUPO']=[a[1] for a in z];classif['INCLUIR_AB']=[a[2] for a in z];save(classif,'Filtro_CID10_residencia.csv')
 compatible=compatible.merge(classif[['CID10','NIVEL','INCLUIR_AB']],on='CID10',validate='many_to_one');save(compatible,'NRMG_compativel_mensal_CID10.csv');save(compatible.groupby(['CNES','MUN_RES','ANO','CID10','NIVEL'],as_index=False).AIH.sum(),'NRMG_compativel_anual_CID10.csv');selected=compatible[compatible.INCLUIR_AB];save(selected,'NRMG_filtro_bacteriano_mensal_CID10.csv')
 monthly=compatible.groupby(['CNES','MUN_RES','ANO','MES'],as_index=False).AIH.sum();filtered=selected.groupby(['CNES','MUN_RES','ANO','MES'],as_index=False).AIH.sum();save(monthly,'NRMG_compativel_mensal_estabelecimento.csv');save(filtered,'NRMG_filtro_mensal_estabelecimento.csv')
 hospitals=nr.groupby(['CNES','NOME_TABNET'],as_index=False).AIH.sum().rename(columns={'AIH':'AIH_NRMG'});hospitals=hospitals[hospitals.AIH_NRMG>0].copy();assert len(hospitals)==383
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/dados_relatorio_didatico_teco.py

Dados relatorio didatico teco. Documentação/apoio. A organização passa por raster_values.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\dados_relatorio_didatico_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.mask | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/01_entradas/01_bacias/bacias.shp — chamada gpd.read_file, linha 55.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'analise_setores'] — chamada gpd.read_file, linha 56.
- E:/teco/entrega_final/00_documentacao/Informacoes_gerais_bacias.csv — chamada pd.read_csv, linha 57.
- E:/teco/entrega_final/02_saidas/01_consolidado/TECO_final.shp — chamada gpd.read_file, linha 58.
- E:/teco/entrega_final/01_entradas/12_uso_solo/uso_solo_2025.tif — chamada rasterio.open, linha 62.
- {path} — chamada rasterio.open, linha 73.
- E:/teco/saneamento_ibge/resultados/resumo_bacias.csv — chamada pd.read_csv, linha 77.
- E:/teco/entrega_final/04_datasus/01_conjunto_8_municipios/Unidades_fisicamente_nas_bacias.csv — chamada pd.read_csv, linha 81.
- E:/teco/entrega_final/04_datasus/01_conjunto_8_municipios/Resumo_por_municipio.csv — chamada pd.read_csv, linha 81.
- E:/teco/entrega_final/04_datasus/01_conjunto_8_municipios/TabNet_NRMG_anual_8_municipios.csv — chamada pd.read_csv, linha 81.

**Saídas.**

- E:/teco/tmp/relatorio_didatico/archive_path.txt — chamada .write_text, linha 53.
- E:/teco/tmp/relatorio_didatico/Dados_tabelas_relatorio.json — chamada .write_text, linha 83.
- E:/teco/entrega_final/00_documentacao/tabelas/Uso_solo_por_bacia_2025.csv — chamada .to_csv, linha 83.
- E:/teco/entrega_final/00_documentacao/tabelas/Resumo_bacias_relatorio.csv — chamada .to_csv, linha 83.

**Campos e chaves lidos.**

- c: bas_id.
- q.loc: dom_a_est, red_a_est.
- grid: BACIA.
- p.loc: densidade_hab_km2, populacao_estimada, recortes_setor_bacia.
- row: id, network_pct, observed_coverage_pct.
- reference.loc: cov_dom, pct_rede.
- hm: MUN_RES.

**Campos e chaves gerados.**

- hm: NRMG.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/dados_relatorio_didatico_teco.py, linhas 66-72.

```python
  for k,label in class_names.items():
   n=sum(int(n) for code,n in zip(codes,counts) if classes.get(int(code))==k);lu.append({'bacia':r.id,'classe':label,'area_km2':n*area,'percentual':100*n/len(v)})
  unknown=sum(int(n) for code,n in zip(codes,counts) if int(code) not in classes);assert unknown==0,(r.id,codes)
  q=c[c.bas_id.eq(r.id)];valid=q.pct_rede.notna();den=q.loc[valid,'dom_a_est'].sum();network=q.loc[valid,'red_a_est'].sum();total=q.dom_a_est.sum();g=grid[grid.BACIA.eq(r.id)]
  assert q.setor_id.nunique()==p.loc[r.id,'recortes_setor_bacia']
  elevation=F/f'01_entradas/13_relevo/{r.id}_hipsometria.tif';slope=F/f'01_entradas/13_relevo/{r.id}_declividade_pct.tif'
  def raster_values(path):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/dicionario_campos_teco.py

Centraliza o significado, a unidade, a natureza e a linhagem de cada campo por produto. É a referência para evitar que nomes iguais sejam interpretados como o mesmo universo.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\dicionario_campos_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| definicao(campo, arquivo='') | 190-227 | Chamadas efetivas: campo.startswith, re.fullmatch, campo.split, KeyError, sum Retorno: DEFINICOES[campo], CAMPOS_CNES_2026[campo]. |
| linhagem(campo, arquivo) | 230-297 | Chamadas efetivas: arquivo.startswith, any, KeyError, campo.startswith, apoios.append, .join Retorno: ('cruzamento CNES/SIH por código e interseção espacial em Python', script, anchor, 'consolidar_entrega_final.py'), ('calculado em Python', grid, ancora, '; '.join(apoios)). |
| descrever_campo(campo, arquivo='') | 300-301 | Chamadas efetivas: definicao Retorno: definicao(campo, arquivo)[0]. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/dicionario_campos_teco.py, linhas 213-219.

```python
        if tipo == 'I':
            return (f'Escore do cenário {co}: 100 × ({w[0]} × N_POP_DENS + {w[1]} × N_SEM_REDE + {w[2]} × N_AIH_LOCAL) / {sum(w)}. Pesos população/ausência de rede/atividade hospitalar = {pesos}; não é probabilidade de contaminação.', 'escore 0-100')
        if tipo == 'F':
            return (f'Classe de I_{co} em faixas fixas: 1 [0,20), 2 [20,40), 3 [40,60), 4 [60,80), 5 [80,100]; 0 entrada incompleta. Não é classificação por percentis nem risco comprovado.', 'classe 1-5; 0 sem classe')
        return (f'Perfil k-means com k = 2 no cenário {co}, ajustado nas três entradas normalizadas multiplicadas pela raiz quadrada dos pesos {pesos}. Rótulos alinhados a S0 por correspondência ótima: 1 maior adensamento e maior ligação à rede; 2 menor adensamento e menor ligação à rede; 0 entrada incompleta. O número não ordena risco.', 'perfil 1/2; 0 sem classe')
    if campo.startswith('RES8_') or campo.startswith('PROD_'):
        residencial = campo.startswith('RES8_')
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/documentar_campos_scripts_teco.py

Documentar campos scripts teco. Documentação/apoio. A organização passa por sha, ler_csv, gravar_csv, backup, fonte_script, sem_documentacao, limpar_script, scripts, localizar, dicionarios.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\documentar_campos_scripts_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ast | Inspeção/transformação da sintaxe Python sem executar o processamento científico. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| dicionario_campos_teco | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| importlib.metadata | Importação e identificação de versões das bibliotecas. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| tokenize | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {p} — chamada p.open, linha 116.
- fonte_script(name) — chamada path.read_text, linha 230.
- E:/teco/codigo/consolidar_entrega_final.py — chamada p.read_text, linha 430.
- E:/teco/entrega_final/LEIA_PRIMEIRO.md — chamada zipfile.ZipFile, linha 391.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 426.

**Saídas.**

- {p} — chamada p.open, linha 123.
- fonte_script(name) — chamada path.write_text, linha 233.
- E:/teco/entrega_final/05_scripts/python/{name} — chamada dst.write_text, linha 236.
- E:/teco/entrega_final/05_scripts/exportar_relatorio_word_teco.ps1 — chamada target.write_text, linha 245.
- E:/teco/entrega_final/05_scripts/requirements-geoprocessamento.txt — chamada .write_text, linha 259.
- E:/teco/entrega_final/05_scripts/LEIA_PRIMEIRO.md — chamada .write_text, linha 260.
- E:/teco/entrega_final/00_documentacao/Dicionario_dos_campos.json — chamada .write_text, linha 317.
- E:/teco/entrega_final/00_documentacao/Dicionario_dos_campos.html — chamada .write_text, linha 374.
- E:/teco/codigo/consolidar_entrega_final.py — chamada p.write_text, linha 440.
- p.with_suffix('.metadata.tmp') — chamada zipfile.ZipFile, linha 416.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .write_text, linha 448.
- E:/teco/entrega_final/00_documentacao/Validacao_campos_scripts.json — chamada .write_text, linha 450.

**Campos e chaves lidos.**

- r: arquivo, campo_original, campo_shp, campos, dataset, descricao, descricao_pixel, fonte, linha_referencia, natureza, script_python, scripts_apoio, stored_field, trecho_referencia, unidade.
- manifest: rasters, vetores.
- dataset: arquivo, campos, fonte.
- m: vetores.

**Campos e chaves gerados.**

- target: English_display_alias.
- m: field_documentation.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| sha(p) | 107-112 | Chamadas efetivas: hashlib.sha256, h.hexdigest, p.open, iter, h.update, stream.read Retorno: h.hexdigest(). |
| ler_csv(p) | 115-117 | Chamadas efetivas: p.open, list, csv.DictReader Retorno: list(csv.DictReader(stream, delimiter=';')). |
| gravar_csv(p, rows, fields=None) | 120-126 | Chamadas efetivas: p.parent.mkdir, list, p.open, csv.DictWriter, writer.writeheader, writer.writerows |
| backup(p) | 129-134 | Chamadas efetivas: .is_relative_to, target.parent.mkdir, R.resolve, p.relative_to, target.exists, shutil.copy2, p.resolve |
| fonte_script(name) | 137-138 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: R / 'sub_bacia' / name if name == 'delimitar_subbacias_teco.py' else C / name. |
| sem_documentacao(tree) | 141-151 | grava produtos Retorno: ast.dump(Limpar().visit(tree), include_attributes=False), node. |
| limpar_script(source, name) | 154-208 | Chamadas efetivas: source.startswith, ast.parse, source.splitlines, list, tokenize.generate_tokens, ast.walk, sorted, .join Retorno: result, source. |
| scripts() | 211-275 | lê dados; grava produtos Retorno: records. |
| localizar(script, anchor) | 278-286 | lê dados Retorno: (p.relative_to(F).as_posix(), matches[0] if matches else 1). |
| dicionarios(manifest) | 289-318 | grava produtos Retorno: rows. |
| dicionario_rasters(manifest) | 321-358 | Chamadas efetivas: gravar_csv, localizar, rows.append, len, KeyError Retorno: rows. |
| pagina_campos(rows, rasters) | 361-384 | lê dados; grava produtos |
| metadados_qgis(rows) | 387-420 | Chamadas efetivas: next, ET.fromstring, root.findall, p.with_suffix, tmp.replace, results.append, zipfile.ZipFile, layer.find Retorno: results. |
| main() | 423-451 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/documentar_campos_scripts_teco.py, linhas 312-318.

```python
        gravar_csv((F/path).parent/'dicionario_campos.csv',[r for r in rows if r['arquivo']==path])
    expected=sum(len(r['campos']) for r in manifest['vetores'])
    assert len(rows)==expected and len({(r['arquivo'],r['campo_shp']) for r in rows})==expected
    gravar_csv(D/'Dicionario_dos_campos.csv',rows)
    gravar_csv(D/'Field_dictionary_EN.csv',[en[r['arquivo'],r['campo_shp']] for r in rows])
    (D/'Dicionario_dos_campos.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
    return rows
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/empacotar_relatorio_teco.py

Empacotar relatorio teco. Documentação/apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\empacotar_relatorio_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/entrega_final.zip — chamada zipfile.ZipFile, linha 25.

**Saídas.**

- E:/teco/entrega_final.zip — chamada zipfile.ZipFile, linha 23.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/empacotar_relatorio_teco.py, linhas 24-29.

```python
 for p in files:z.write(p,'entrega_final/'+p.relative_to(F).as_posix())
with zipfile.ZipFile(dst) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(files)
 assert 'entrega_final/00_documentacao/Relatorio_TECO.docx' in z.namelist()
print(json.dumps({'zip':str(dst),'arquivos':len(files),'MB':round(dst.stat().st_size/1e6,2),'crc':'OK'},ensure_ascii=False))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/executar_grade_teco.ps1

Executar grade teco. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\executar_grade_teco.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/executar_grade_teco.ps1, linhas 13-21.

```text
param([string]$PlanilhaFiltro = '')
. (Join-Path $PSScriptRoot 'caminhos_teco.ps1')

$ErrorActionPreference = 'Stop'
$tecoRoot = (Get-PortablePath '')
$tecoPython = (Get-PortableExternal 'python_exe_9a6f757')
$tecoReportPython = (Get-PortableExternal 'python_exe_059becd')
$tecoNode = (Get-PortableExternal 'node_exe_50000f2')
if ($PlanilhaFiltro) { & $tecoPython "$tecoRoot\codigo\avaliar_saude_grade.py" --planilha $PlanilhaFiltro }
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/explorador_residencia_teco.py

Explorador offline de todos os hospitais com AIH de residentes dos 4 municípios.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\explorador_residencia_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/05_auditoria_saude/NRMG_compativel_mensal_CID10.csv — chamada pd.read_csv, linha 39.
- E:/teco/output/05_auditoria_saude/Estabelecimentos_confirmados_residencia.csv — chamada pd.read_csv, linha 39.
- E:/teco/output/05_auditoria_saude/Filtro_CID10_residencia.csv — chamada pd.read_csv, linha 39.
- E:/teco/output/05_auditoria_saude/consolidacao.json — chamada .read_text, linha 39.

**Saídas.**

- {target} — chamada target.write_text, linha 52.
- E:/teco/output/04_grade_500m/figuras/{slug}.{ext} — chamada fig.savefig, linha 56.
- E:/teco/output/04_grade_500m/auditoria/galeria_saude.json — chamada .write_text, linha 58.

**Campos e chaves lidos.**

- hs: CNES.
- f: NIVEL.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 38-58 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/explorador_residencia_teco.py, linhas 54-59.

```python
 for mu,name in zip(MUN,MN):
  q=selected[selected.MUN_RES==mu].groupby(['ANO','MES']).AIH.sum().reindex(pd.MultiIndex.from_product([range(2016,2026),range(1,13)],names=['ANO','MES']),fill_value=0).reset_index();fig,ax=plt.subplots(2,1,figsize=(11.8,6.5),layout='constrained');dt=pd.to_datetime(dict(year=q.ANO,month=q.MES,day=1));ax[0].plot(dt,q.AIH,color='#287991',lw=1.5);ax[0].set_ylabel('AIH selecionadas');ax[0].set_title(name+' · residência municipal · filtro amplo A+B',loc='left',fontweight='bold');ax[0].grid(alpha=.15);pat=q.groupby('MES').AIH.mean();ax[1].bar(range(1,13),pat,color='#659da9');ax[1].set_xticks(range(1,13),['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']);ax[1].set_ylabel('Média mensal no decênio');ax[1].set_title('Mês de processamento · 2016-2025',fontsize=10);ax[1].grid(alpha=.12,axis='y');ax[1].set_ylim(bottom=0);slug='residencia_'+mu
  for ext in ['png','svg']:fig.savefig(P/'figuras'/f'{slug}.{ext}',dpi=330,facecolor='white')
  plt.close(fig);gallery.append({'slug':slug,'titulo':name+' · internações por residência municipal','grupo':'Internações por residência'})
 (P/'auditoria/galeria_saude.json').write_text(json.dumps(gallery,ensure_ascii=False,indent=2),encoding='utf8');print('EXPLORADOR_NRMG',len(data),'registros agregados',len(hospitals),'estabelecimentos',flush=True)
if __name__=='__main__':main()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/exportar_relatorio_word_teco.ps1

Exportar relatorio word teco. Documentação/apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\exportar_relatorio_word_teco.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/exportar_relatorio_word_teco.ps1, linhas 16-24.

```text
. (Join-Path $PSScriptRoot 'caminhos_teco.ps1')


$ErrorActionPreference='Stop'

$reportPath=(Get-PortablePath 'output/02_avaliacao_espacial/Relatorio_TECO.docx')

$pdfPath=(Get-PortablePath 'output/02_avaliacao_espacial/Relatorio_TECO.pdf')

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/figuras_multivariada_teco.py

Figuras multivariada teco. Cartografia/apresentação. A organização passa por legend, legend_small, start, finish, continuous, categories.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\figuras_multivariada_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.font_manager | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| multivariada_teco | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/03_multivariada/teco_multivariada.gpkg [camada 'ete_ana2020_regional'] — chamada gpd.read_file, linha 171.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'rotas_d8_candidatas'] — chamada gpd.read_file, linha 163.
- E:/teco/reservatorio/{key}.shp — chamada gpd.read_file, linha 59.
- E:/teco/teco_base/mg_mun/ide_1103_mg_municipios_pol.shp — chamada gpd.read_file, linha 61.
- E:/teco/output/02_avaliacao_espacial/rasters/{r.id}_{suffix}.tif — chamada rasterio.open, linha 160.
- E:/teco/output/03_multivariada/tabelas/matriz_normalizada.csv — chamada pd.read_csv, linha 176.
- E:/teco/output/03_multivariada/auditoria/metodo_multivariada.json — chamada .read_text, linha 177.
- E:/teco/output/03_multivariada/tabelas/cenarios_sensibilidade.csv — chamada pd.read_csv, linha 187.
- E:/teco/output/03_multivariada/tabelas/kmeans_todos_k.csv — chamada pd.read_csv, linha 187.

**Saídas.**

- E:/teco/output/03_multivariada/figuras/{name}.{ext} — chamada fig.savefig, linha 126.
- E:/teco/output/03_multivariada/figuras/perfis_pca.{ext} — chamada fig.savefig, linha 185.
- E:/teco/output/03_multivariada/figuras/sensibilidade_resumo.{ext} — chamada fig.savefig, linha 194.
- E:/teco/output/03_multivariada/auditoria/galeria.json — chamada .write_text, linha 196.

**Campos e chaves lidos.**

- .loc: ibirite_regap, pampulha, vargem_flores.
- b: id.
- av: bas_id.
- route: bacia.
- ex: id.
- ete: bacia.
- u: elegivel.
- ks: cenario.
- tab: ARI_base, cenario.
- ax.spines: right, top.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| legend(fig, handles, ncol=3, y=0.15) | 70-80 | Chamadas efetivas: fig.canvas.draw, fig.canvas.get_renderer, FontProperties, enumerate, max, sum, legend_small, range Retorno: legend_small(fig, handles, ncol, y, fontsize). |
| legend_small(fig, handles, ncol, y, fs) | 83-84 | Chamadas efetivas: fig.legend |
| start(title, sectors=True) | 87-107 | Chamadas efetivas: plt.figure, fig.suptitle, enumerate, b.itertuples, .get, view.get, fig.add_axes, axs.append Retorno: (fig, axs). |
| finish(fig, axs, name, title, group, handles=None, bar=None, waterdraw=True) | 110-127 | grava produtos |
| continuous(field, title, name, group, label, maxval=None, cmap=CM) | 130-134 | Chamadas efetivas: start, max, Normalize, zip, finish, float, b.itertuples, g.plot |
| categories(field, title, name, group) | 137-141 | Chamadas efetivas: start, sorted, zip, finish, .unique, b.itertuples, g.plot, int |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/figuras_multivariada_teco.py, linhas 75-81.

```python
 widths=[max([renderer.get_text_width_height_descent(h.get_label(),font,False)[0]/fig.bbox.width+2.5*unit for h in handles[c::ncol]] or [0]) for c in range(ncol)]
 gap=1.5*unit;total=sum(widths)+gap*(ncol-1)
 if total>.91:fontsize*=.91/total;return legend_small(fig,handles,ncol,y,fontsize)
 for row,start in enumerate(range(0,len(handles),ncol)):
  items=handles[start:start+ncol];rowwidth=sum(widths[:len(items)])+gap*(len(items)-1);left=.515-rowwidth/2
  for j,h in enumerate(items):fig.legend(handles=[h],bbox_to_anchor=(left+sum(widths[:j])+gap*j,y-row*.052),loc='upper left',frameon=False,borderaxespad=0,fontsize=fontsize,handlelength=1.5,handletextpad=.45)

```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/figuras_revisao_cnes_sih_teco.py

Figuras revisao cnes sih teco. Cartografia/apresentação. A organização passa por salvar.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\figuras_revisao_cnes_sih_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ast | Inspeção/transformação da sintaxe Python sem executar o processamento científico. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| idioma_cartografico_teco | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.dates | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.text | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/01_entradas/01_bacias/bacias.shp — chamada gpd.read_file, linha 69.
- E:/teco/entrega_final/01_entradas/02_reservatorios/reservatorios.shp — chamada gpd.read_file, linha 70.
- E:/teco/entrega_final/01_entradas/05_hidrografia/hidrografia.shp — chamada gpd.read_file, linha 71.
- E:/teco/entrega_final/01_entradas/06_vias_contexto/vias_contexto.shp — chamada gpd.read_file, linha 72.
- E:/teco/config/encartes_teco.json — chamada .read_text, linha 74.
- E:/teco/codigo/figuras_multivariada_teco.py — chamada .read_text, linha 76.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/02_camadas/01_cnes_bacias/cnes_2026.shp — chamada gpd.read_file, linha 93.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/02_camadas/02_selecao_sih/sih_atual.shp — chamada gpd.read_file, linha 94.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/02_camadas/03_bordas/sih_bordas.shp — chamada gpd.read_file, linha 95.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/Internacoes_gerais_selecionados_mensal.csv — chamada pd.read_csv, linha 116.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/Internacoes_gerais_selecionados_anual.csv — chamada pd.read_csv, linha 117.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada mp.read_text, linha 138.
- Mais 1 referências na ficha HTML e no inventário JSON.

**Saídas.**

- {fig} — chamada savefig, linha 90.
- E:/teco/tmp/figuras_cnes_2026/figuras/{slug}.{ext} — chamada fig.savefig, linha 134.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada mp.write_text, linha 144.
- E:/teco/entrega_final/index.html — chamada p.write_text, linha 149.

**Campos e chaves lidos.**

- .loc: ibirite_regap, pampulha, vargem_flores.
- allc: BACIA.
- sel: BACIA.
- near: BACIA.
- monthly: CNES.
- annual: CNES.
- ax.spines: right, top.
- r: arquivo, slug, titulo, vetorial.
- m: mapas.

**Campos e chaves gerados.**

- m: mapas.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| salvar(fig, *args, **kwargs) | 82-90 | grava produtos Retorno: savefig(fig, *args, **kwargs). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/figuras_revisao_cnes_sih_teco.py, linhas 82-90.

```python
def salvar(fig,*args,**kwargs):
    from matplotlib.text import Text
    for t in fig.findobj(Text):
        value=en(t.get_text())
        if value.startswith('Datum: SIRGAS 2000'):
            value='Datum: SIRGAS 2000\nUTM 23S · EPSG:31983\nScale 1:225,000\nBrentano, M. C. B.'
            t.set_fontsize(5.1)
        t.set_text(value)
    return savefig(fig,*args,**kwargs)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/filtro_bacteriano_teco.py

Filtro bacteriano teco. Processamento ou módulo de apoio. A organização passa por rule, nums, classify, main.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\filtro_bacteriano_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unicodedata | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

- E:/teco/output/04_grade_500m/tabelas/sih_cid10_mensal.csv — chamada pd.read_csv, linha 88.
- E:/teco/dados_publicos/saude_revisao/CID10_oficial_GO.json — chamada .read_text, linha 89.

**Saídas.**

- E:/teco/output/04_grade_500m/filtro_cid10.csv — chamada .to_csv, linha 97.
- E:/teco/output/04_grade_500m/tabelas/classificacao_cid_bacteriana.csv — chamada filt.to_csv, linha 98.
- E:/teco/output/04_grade_500m/tabelas/sih_resumo_etiologico.csv — chamada .to_csv, linha 100.
- E:/teco/output/04_grade_500m/tabelas/regras_filtro_bacteriano.csv — chamada .to_csv, linha 101.
- E:/teco/output/04_grade_500m/auditoria/filtro_bacteriano.json — chamada .write_text, linha 103.

**Campos e chaves lidos.**

- a: code, display.
- official: concept.
- f: CID10, diagnostico.
- filt: CID10, diagnostico, grupo_para_revisao, incluir, justificativa, nivel_etiologico.
- selected.loc: internacoes.
- selected: incluir.

**Campos e chaves gerados.**

- filt: diagnostico, grupo_para_revisao, incluir, justificativa, nivel_etiologico.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| rule(tier, label, prefixes, exclude=()) | 41-42 | Chamadas efetivas: RULES.append, tuple, prefixes.split |
| nums(letter, a, b) | 45-45 | Chamadas efetivas: .join, range Retorno: ' '.join((f'{letter}{i:02d}' for i in range(a, b + 1))). |
| classify(code, description='') | 74-84 | Chamadas efetivas: .strip, .lower, re.search, .upper, .decode, code.startswith, .replace, .encode Retorno: ('Fora', 'Sem infecção bacteriana ou síndrome elegível no diagnóstico principal', False), ('Fora', 'Etiologia não bacteriana explicitada', False). |
| main() | 87-103 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/filtro_bacteriano_teco.py, linhas 99-104.

```python
 selected=f.merge(filt[['CID10','nivel_etiologico','incluir']],on='CID10',validate='many_to_one')
 selected.groupby(['CNES','unidade','nivel_etiologico'],as_index=False).internacoes.sum().to_csv(T/'sih_resumo_etiologico.csv',sep=';',index=False,encoding='utf-8-sig')
 pd.DataFrame([{'nivel':t,'grupo':n,'prefixos':' '.join(p),'excecoes':' '.join(e),'fonte':SOURCE} for t,n,p,e in RULES]).to_csv(T/'regras_filtro_bacteriano.csv',sep=';',index=False,encoding='utf-8-sig')
 info={'data':'2026-11-12','fonte_cid':SOURCE,'criterio':'A+B: etiologia bacteriana codificada e síndromes infecciosas compatíveis; C separado, sem incluir comorbidades isoladas.','CID_selecionados':int(filt.incluir.sum()),'CID_por_nivel':filt.nivel_etiologico.value_counts().to_dict(),'AIH_selecionadas':int(selected.loc[selected.incluir,'internacoes'].sum()),'AIH_por_nivel':selected.groupby('nivel_etiologico').internacoes.sum().to_dict(),'limitacao':'Diagnóstico principal; sem confirmação de agente, RAM ou residência atendida. Não inclui SIA/e-SUS.'}
 (O/'auditoria/filtro_bacteriano.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(info,ensure_ascii=True),flush=True)
if __name__=='__main__':main()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/finalizar_estilos_qgis_bacias.py

Finalizar estilos qgis bacias. Cartografia/apresentação. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\finalizar_estilos_qgis_bacias.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| base64 | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/01_entradas/11_pontos_coleta/pontos_coleta.qml — chamada qml.read_text, linha 43.
- E:/teco/entrega_final/00_documentacao/simbolos/sampling_point_drop.svg — chamada svg.read_bytes, linha 43.

**Saídas.**

- E:/teco/entrega_final/01_entradas/11_pontos_coleta/pontos_coleta.qml — chamada qml.write_text, linha 43.

**Campos e chaves gerados.**

- os.environ: QT_QPA_PLATFORM.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/finalizar_estilos_qgis_bacias.py, linhas 42-44.

```python

qml=F/'01_entradas/11_pontos_coleta/pontos_coleta.qml';svg=D/'simbolos/sampling_point_drop.svg';text=qml.read_text('utf8');text=text.replace(svg.as_posix(),'base64:'+base64.b64encode(svg.read_bytes()).decode());qml.write_text(text,encoding='utf8')
print('Default styles and all three projects updated',flush=True)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/finalizar_qgis_entrega.py

Finalizar qgis entrega. Cartografia/apresentação. A organização passa por symbols, walk, visit.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\finalizar_qgis_entrega.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| base64 | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 34.
- E:/teco/entrega_final/01_entradas/11_pontos_coleta/pontos_coleta.qml — chamada qml.read_text, linha 82.
- E:/teco/entrega_final/00_documentacao/simbolos/sampling_point_drop.svg — chamada svg.read_bytes, linha 82.
- E:/teco/entrega_final/00_documentacao/Validacao_QGIS.json — chamada .read_text, linha 84.

**Saídas.**

- E:/teco/entrega_final/01_entradas/11_pontos_coleta/pontos_coleta.qml — chamada qml.write_text, linha 82.
- E:/teco/entrega_final/00_documentacao/Validacao_QGIS.json — chamada .write_text, linha 84.

**Campos e chaves lidos.**

- m: vetores.
- r: arquivo, titulo.
- row: campos.

**Campos e chaves gerados.**

- os.environ: QT_QPA_FONTDIR, QT_QPA_PLATFORM.
- status: camadas, camadas_validas, simbolos_portateis.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| symbols(renderer) | 42-52 | Chamadas efetivas: isinstance, hasattr, rule.symbol, rule.children, visit, renderer.categories, renderer.rootRule, renderer.ranges |
| walk(sym) | 54-60 | Chamadas efetivas: range, sym.symbolLayerCount, sym.symbolLayer, isinstance, sl.subSymbol, sl.path, sl.setPath, walk |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/finalizar_qgis_entrega.py, linhas 42-50.

```python
def symbols(renderer):
 if isinstance(renderer,QgsRuleBasedRenderer):
  def visit(rule):
   if rule.symbol():yield rule.symbol()
   for child in rule.children():yield from visit(child)
  yield from visit(renderer.rootRule())
 elif hasattr(renderer,'categories'):
  for cat in renderer.categories():yield cat.symbol()
 elif hasattr(renderer,'ranges'):
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_relatorio_academico_teco.py

Gerar relatorio academico teco. Documentação/apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\gerar_relatorio_academico_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| runpy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_relatorio_academico_teco.py, linhas 11-19.

```python
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_teco.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_teco.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
        break
from caminhos_teco import raiz_projeto as _cp_raiz, texto_caminho as _cp_texto, externo as _cp_externo, adaptar_texto as _cp_adaptar
# FIM DOS CAMINHOS PORTÁTEIS

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_relatorio_camadas_teco.py

Gerar relatorio camadas teco. Documentação/apoio. A organização passa por num, heading, p, table, figure, dec, borders, hyperlink, build.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\gerar_relatorio_camadas_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.table | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/00_documentacao/tabelas/Dados_tabelas_relatorio.json — chamada data_path.read_text, linha 53.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 53.
- E:/teco/entrega_final/00_documentacao/tabelas/cenarios_grade.csv — chamada .open, linha 167.
- E:/teco/entrega_final/00_documentacao/tabelas/kmeans_grade.csv — chamada .open, linha 167.
- E:/teco/entrega_final/00_documentacao/Referencias_metodologia_TECO.json — chamada .read_text, linha 220.
- E:/teco/entrega_final/f['source'] — chamada Image.open, linha 275.

**Saídas.**

- E:/teco/output/02_avaliacao_espacial/Relatorio_TECO.docx — chamada doc.save, linha 279.
- E:/teco/output/02_avaliacao_espacial/Relatorio_TECO.md — chamada .write_text, linha 279.
- E:/teco/entrega_final/00_documentacao/Relatorio_TECO.md — chamada .write_text, linha 279.
- E:/teco/entrega_final/00_documentacao/Relatorio_figuras_e_tabelas.json — chamada .write_text, linha 279.

**Campos e chaves lidos.**

- data: basins, landuse, local_health, municipal_health.
- x: cenario, effective_dpi, k, slug.
- manifest: mapas.
- record: arquivo, vetorial.
- r: ARI, BACIA, CNES, MUNICIPIO, NRMG, PROD_AB, PROD_TOT, RES8_AB, UNIDADES, area_km2, bacia, cenario, classe, density, elevation_max, elevation_min, grid_n, k_counts, landuse_valid_area_km2, mesmo_grupo_pct, name, network_pct, no_network_pct, observed_coverage_pct, percentual, population, referencia, sectors, sectors_valid_sewer, slope_median, tier_counts, url.
- b: id, name.
- sil: silhouette.
- doc.styles: Normal, Subtitle.
- tab: headers, number, rows, title.
- f: caption, number, slug, source.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| num(v, n=0) | 56-56 | Chamadas efetivas: .replace, float Retorno: f'{float(v):,.{n}f}'.replace(',', '@').replace('.', ',').replace('@', '.'). |
| heading(t, level=1) | 60-60 | Chamadas efetivas: blocks.append |
| p(t) | 63-63 | Chamadas efetivas: blocks.append |
| table(title, heads, rows, widths) | 66-67 | Chamadas efetivas: tables.append, blocks.append, len |
| figure(slug, caption) | 70-71 | Chamadas efetivas: figures.append, blocks.append, len |
| dec(t) | 170-170 | Chamadas efetivas: float, t.replace Retorno: float(t.replace(',', '.')). |
| borders(cell) | 226-233 | Chamadas efetivas: cell._tc.get_or_add_tcPr, OxmlElement, pr.append, e.set, bdr.append, mar.append, qn |
| hyperlink(p, label, url) | 236-237 | Chamadas efetivas: OxmlElement, h.set, fonts.set, pr.append, co.set, r.append, h.append, p._p.append |
| build() | 240-280 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_relatorio_camadas_teco.py, linhas 278-281.

```python
 doc.core_properties.title='Guia das camadas e análises espaciais do projeto TECO';doc.core_properties.author='Projeto TECO';doc.core_properties.subject='Preparação das camadas, síntese por bacia e interpretação dos métodos';doc.core_properties.keywords='TECO, reservatórios, esgotamento, população, k-means, Moran'
 out=B/'Relatorio_TECO.docx';doc.save(out);shutil.copy2(out,D/out.name);text='\n\n'.join(md)+'\n';(B/'Relatorio_TECO.md').write_text(text,encoding='utf8');(D/'Relatorio_TECO.md').write_text(text,encoding='utf8');(D/'Relatorio_figuras_e_tabelas.json').write_text(json.dumps({'figures':figures,'tables':tables,'image_quality':quality,'source_png_retained':True,'date':'2026-11-13','text_words':sum(len(x[1].split()) for x in blocks if x[0]=='text')},ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'words':sum(len(x[1].split()) for x in blocks if x[0]=='text'),'figures':len(figures),'tables':len(tables),'docx_MB':round(out.stat().st_size/1e6,2),'min_effective_dpi':min(x['effective_dpi'] for x in quality)},ensure_ascii=False),flush=True)
if __name__=='__main__':build()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/grade_500m_teco.py

Constrói vizinhanças circulares de 500 m, agrega dados nativos, calcula as três entradas principais, S0-S4, perfis k-means e Moran no suporte hexagonal. Os hexágonos são a apresentação sem sobreposição; os círculos são a unidade de cálculo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\grade_500m_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| analise_espacial_teco | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| multivariada_teco | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.windows | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada rasterio.open, linha 87.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'hidrografia_bacias'] — chamada gpd.read_file, linha 131.
- E:/teco/output/03_multivariada/teco_multivariada.gpkg [camada 'unidades_ajuste'] — chamada gpd.read_file, linha 104.
- E:/teco/reservatorio/{k}.shp — chamada gpd.read_file, linha 109.
- E:/teco/output/05_auditoria_saude/RD_MG_todos_estabelecimentos_2016_2025.csv — chamada pd.read_csv, linha 114.
- E:/teco/output/02_avaliacao_espacial/tabelas/sih_bacias_2016_2025.csv — chamada pd.read_csv, linha 115.
- E:/teco/output/04_grade_500m/tabelas/sih_cid10_mensal.csv — chamada pd.read_csv, linha 117.
- E:/teco/output/04_grade_500m/filtro_cid10.csv — chamada pd.read_csv, linha 119.
- E:/teco/vias/malha_viaria.shp — chamada gpd.read_file, linha 131.

**Saídas.**

- E:/teco/output/04_grade_500m/tabelas/{n} — chamada .to_csv, linha 80.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada n] — chamada f.to_file, linha 83.
- E:/teco/output/04_grade_500m/auditoria/metodo_grade.json — chamada .write_text, linha 173.

**Campos e chaves lidos.**

- b: geometry, id.
- c: DOM_DENS, ESG_EST, SEM_ANALIT, dens_pop, dom_set, geometry, pct_rede, set_km2, setor_id.
- aux: ESG_EST, sem_rede.
- circles: AIH_LOCAL, AREA_KM2, BACIA, DOM, DOM_EST, DOM_OBS, GRID_ID, I_S0, POP, POP_DENS, SAUDE_N, SEM, SEM_OBS, SEM_REDE, geometry.
- health: AIH_ANO, CNES, GRUPO, QA_MUN, geometry.
- prod.loc: CNES.
- prod: AIH.
- filt.loc: CID10.
- filt: incluir.
- rr: CID10.
- source: geometry.
- a: cenario, silhouette.
- models: S0.
- circles.loc: I_S0.
- rec: cenario.
- local: cluster, q.
- meta: centros, unidades_bacia.

**Campos e chaves gerados.**

- circles: AIH_ORIG, AREA_KM2, COB_ESG, ESTABILIDADE, EST_ESG, ORIG_STATUS, POP_DENS, QUINTIL, SEM_OBS_P, SEM_REDE, VALIDO.
- c: DOM_DENS, ESG_EST, SEM_ANALIT.
- z: AREA, DOM, DOM_EST, DOM_OBS, POP, SEM, SEM_OBS.
- health: AIH_ANO.
- inter: L.
- rec: ARI, k_comum, mesmo_grupo_pct, rho_indice.
- hexclip: MORAN.
- profiles: n.
- meta: CID_selecionados, mapas_entrada, status.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| csv(f, n) | 80-80 | grava produtos |
| gp(f, n) | 83-83 | grava produtos |
| rasterstats(path, geom) | 86-90 | Chamadas efetivas: rasterio.open, .intersection, d.read, geometry_mask, Window, np.array, d.window_transform, np.asarray Retorno: v[np.isfinite(v)], np.array([]). |
| main() | 93-173 | lê dados; grava produtos; Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.; Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/grade_500m_teco.py, linhas 93-99.

```python
def main():
 b=gpd.read_file(B/'teco_avaliacao.gpkg',layer='bacias_estudo');union=b.geometry.union_all();xmin,ymin,xmax,ymax=union.bounds;r=500.;dx=1.5*r;dy=np.sqrt(3)*r;pts=[];cells=[];rows=[]
 for ix in range(math.floor((xmin-r)/dx),math.ceil((xmax+r)/dx)+1):
  for iy in range(math.floor((ymin-r)/dy)-1,math.ceil((ymax+r)/dy)+1):
   x=ix*dx;y=iy*dy+(ix%2)*dy/2;hex=Polygon([(x+r*np.cos(np.pi*j/3),y+r*np.sin(np.pi*j/3)) for j in range(6)])
   if not hex.intersects(union):continue
   gid=f'G{len(rows)+1:04d}';p=Point(x,y);rows.append({'GRID_ID':gid,'E':x,'N':y,'RAIO_M':500,'CENTRO_INT':int(union.covers(p))});pts.append(p);cells.append(hex)
```

Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.

Trecho de codigo/grade_500m_teco.py, linhas 135-141.

```python

 feats=['POP_DENS','SEM_REDE','AIH_LOCAL'];x=np.c_[np.log1p(circles.POP_DENS),circles.SEM_REDE,np.log1p(circles.AIH_LOCAL)];valid=np.isfinite(x).all(1);lo=np.nanmin(x[valid],0);hi=np.nanmax(x[valid],0);norm=(x-lo)/np.where(hi>lo,hi-lo,1)
 circles['VALIDO']=valid
 for j,f in enumerate(feats):circles['N_'+f]=norm[:,j]
 for f in ['URB_PCT','HIPS_M','DECL_PCT','DIST_KM','VIAS_KM','HIDRO_KM']:
  v=circles[f];circles['N_'+f]=(v-v.min())/(v.max()-v.min()) if v.max()>v.min() else 0

```

Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.

**Cálculos a observar nesta rotina.**

- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- log1p: Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.
- bincount: Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.
- spearmanr: Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/guia_entrega_final.py

Guia entrega final. Documentação/apoio. A organização passa por pt_number, pdf, table, footer.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\guia_entrega_final.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| reportlab.lib.colors | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.enums | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.pagesizes | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfgen | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 38.
- E:/teco/entrega_final/00_documentacao/Informacoes_gerais_bacias.json — chamada population_path.read_text, linha 40.
- E:/teco/entrega_final/00_documentacao/Comparacao_kmeans_sensibilidade.json — chamada comparison_path.read_text, linha 42.
- E:/teco/entrega_final/04_datasus/03_referencia_4_municipios/Resumo_auditoria_refinada.json — chamada health_path.read_text, linha 44.
- E:/teco/entrega_final/00_documentacao/tabelas/kmeans_grade.csv — chamada k_table.read_text, linha 57.
- E:/teco/entrega_final/00_documentacao/Informacoes_gerais_bacias.md — chamada .read_text, linha 146.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/Como_interpretar_kmeans.md — chamada .write_text, linha 111.
- E:/teco/entrega_final/LEIA_PRIMEIRO.md — chamada .write_text, linha 193.
- E:/teco/entrega_final/index.html — chamada .write_text, linha 195.

**Campos e chaves lidos.**

- comparison_data: comparacao, interpretacao, resultado.
- row: ARI, area_km2, cenario, densidade_hab_km2, grupo, k, menor_grupo, mesmo_grupo_pct, nome, peso_aih_local, peso_populacao, peso_sem_rede, populacao_estimada, silhouette.
- r: arquivo, cenario, feicoes, titulo, vetorial.
- population_data: bacias.
- m: mapas, vetores.
- health_data: dentro_bacias.
- u: CNES, NOME_TABNET.
- styles: title.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| pt_number(value, decimals=0) | 47-47 | Chamadas efetivas: .replace Retorno: f'{value:,.{decimals}f}'.replace(',', '@').replace('.', ',').replace('@', '.'). |
| pdf() | 198-223 | Chamadas efetivas: pdfmetrics.registerFont, enumerate, .build, TTFont, ParagraphStyle, Table, t.setStyle, story.append Retorno: t. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/guia_entrega_final.py, linhas 47-55.

```python
def pt_number(value,decimals=0):return f'{value:,.{decimals}f}'.replace(',','@').replace('.',',').replace('@','.')
population_html=''
kmeans_comparison_html=''
if comparison_data:
 kmeans_comparison_html='<h2>K-means e sensibilidade: qual solução se destacou?</h2><p>'+html.escape(comparison_data['resultado'])+'</p><table><tr><th>Cenário</th><th>Pesos<br>população / sem rede / AIH</th><th>k</th><th>Silhouette</th><th>Mesmo perfil de S0</th><th>ARI</th></tr>'
 for row in comparison_data['comparacao']:
  kmeans_comparison_html+=('<tr class="best">' if row['cenario']=='S2' else '<tr>')+'<td>'+html.escape(row['cenario'])+(' · destaque' if row['cenario']=='S2' else '')+'</td><td>'+str(int(row['peso_populacao']))+' / '+str(int(row['peso_sem_rede']))+' / '+str(int(row['peso_aih_local']))+'</td><td>2</td><td>'+pt_number(row['silhouette'],3)+'</td><td>'+pt_number(row['mesmo_grupo_pct'],1)+'%</td><td>'+pt_number(row['ARI'],3)+'</td></tr>'
 kmeans_comparison_html+='</table><p>'+html.escape(comparison_data['interpretacao'])+' <a href="00_documentacao/Comparacao_kmeans_sensibilidade.csv">Baixar comparação</a>.</p>'
 k_table=D/'tabelas/kmeans_grade.csv'
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/idioma_cartografico_teco.py

Idioma cartografico teco. Cartografia/apresentação. A organização passa por en, field_alias.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\idioma_cartografico_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| en(text) | 176-184 | Chamadas efetivas: text.replace, sorted, re.sub, .replace, isinstance, WORDS.items, out.replace, len Retorno: out, text. |
| field_alias(name) | 236-242 | Chamadas efetivas: name.startswith, .lower, field_alias Retorno: name, FIELDS[name]. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/idioma_cartografico_teco.py, linhas 176-184.

```python
def en(text):
 if not isinstance(text,str):return text
 if text in WORDS:return WORDS[text]
 text=text.replace('reported year 2025','2025')
 out=text
 for a,b in sorted(WORDS.items(),key=lambda kv:len(kv[0]),reverse=True):out=out.replace(a,b)
 out=re.sub(r'(?<=\d) a (?=\d)',' to ',out)
 out=out.replace('°O','°W').replace('2,5','2.5')
 return out
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/indice_grade_teco.py

Visualizador local da grade; histórico por setores fica separado.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\indice_grade_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/04_grade_500m/auditoria/galeria_mapas.json — chamada .read_text, linha 35.
- E:/teco/output/04_grade_500m/auditoria/galeria_saude.json — chamada .read_text, linha 35.
- E:/teco/output/04_grade_500m/auditoria/Informacoes_gerais_bacias.json — chamada population_path.read_text, linha 54.

**Saídas.**

- E:/teco/output/04_grade_500m/index.html — chamada .write_text, linha 60.
- E:/teco/output/02_avaliacao_espacial/index.html — chamada .write_text, linha 63.
- E:/teco/output/04_grade_500m/LEIA_PRIMEIRO.md — chamada .write_text, linha 65.
- E:/teco/output/02_avaliacao_espacial/LEIA_PRIMEIRO.md — chamada .write_text, linha 65.
- E:/teco/output/04_grade_500m/tabelas/fontes_novas.csv — chamada .open, linha 67.
- E:/teco/output/04_grade_500m/auditoria/galeria.json — chamada .write_text, linha 69.

**Campos e chaves lidos.**

- x: grupo.
- c: grupo, slug, titulo.
- data: bacias.
- r: area_km2, densidade_hab_km2, nome, populacao_estimada.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/indice_grade_teco.py, linhas 55-63.

```python
 def fmt(v,n=0):return f'{v:,.{n}f}'.replace(',','@').replace('.',',').replace('@','.')
 summary='<section><h2>Informações gerais das bacias</h2><table style="width:100%;border-collapse:collapse"><tr><th style="text-align:left">Bacia</th><th>População estimada (2022)</th><th>Área (km²)</th><th>Densidade (hab./km²)</th></tr>'
 for r in data['bacias']:summary+='<tr><td>'+html.escape(r['nome'])+'</td>'+''.join('<td style="text-align:center;padding:8px">'+v+'</td>' for v in [fmt(r['populacao_estimada']),fmt(r['area_km2'],2),fmt(r['densidade_hab_km2'],1)])+'</tr>'
 summary+='</table><p>Fonte: IBGE, Censo 2022. População estimada pela fração da área de cada setor dentro da bacia; não é soma das vizinhanças de 500 m.</p></section>'
 page=page.replace('<label>Exibir ',summary+'<label>Exibir ')
(O/'index.html').write_text(page,encoding='utf8')
backup=R/'descontinuado'/'20261112_visualizador_antes_grade500';backup.mkdir(parents=True,exist_ok=True)
if (B/'index.html').exists() and not (backup/'index.html').exists():shutil.copy2(B/'index.html',backup/'index.html')
(B/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../04_grade_500m/index.html"><a href="../04_grade_500m/index.html">Abrir visualizador TECO atualizado</a>',encoding='utf8')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/informacoes_gerais_teco.py

Informacoes gerais teco. Processamento ou módulo de apoio. A organização passa por number.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\informacoes_gerais_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/01_entradas/03_populacao/populacao.shp — chamada gpd.read_file, linha 36.
- E:/teco/entrega_final/01_entradas/01_bacias/bacias.shp — chamada gpd.read_file, linha 36.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada manifest.read_text, linha 54.
- E:/teco/config/paleta_hipsometria.json — chamada .read_text, linha 54.

**Saídas.**

- {directory}/Informacoes_gerais_bacias.json — chamada .write_text, linha 44.
- E:/teco/entrega_final/00_documentacao/Informacoes_gerais_bacias.csv — chamada .to_csv, linha 45.
- E:/teco/output/04_grade_500m/tabelas/Informacoes_gerais_bacias.csv — chamada .to_csv, linha 46.
- E:/teco/entrega_final/00_documentacao/Informacoes_gerais_bacias.md — chamada .write_text, linha 53.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada manifest.write_text, linha 54.

**Campos e chaves lidos.**

- p: BACIA.
- row: area_km2, densidade_hab_km2, nome, populacao_estimada.
- data: fonte, limite, metodo.

**Campos e chaves gerados.**

- m: informacoes_gerais_bacias, paleta_hipsometria.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| number(x, dec=0) | 49-49 | Chamadas efetivas: .replace Retorno: f'{x:,.{dec}f}'.replace(',', '@').replace('.', ',').replace('@', '.'). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/informacoes_gerais_teco.py, linhas 39-45.

```python
for key,name in names.items():
 g=p[p.BACIA==key];assert g.POP_REC.notna().all();population=float(g.POP_REC.sum());area=float(b.loc[key].geometry.area/1e6)
 rows.append({'bacia':key,'nome':name,'ano_base':2022,'populacao_estimada':population,'area_km2':area,'densidade_hab_km2':population/area,'recortes_setor_bacia':len(g)})
data={'fonte':'IBGE, Censo Demográfico 2022, agregado básico v0001','metodo':'Soma de POP_REC: total oficial de cada setor multiplicado pela fração de sua área dentro da bacia.','limite':'Estimativa por rateio uniforme de área, não contagem censitária diretamente medida na bacia; não soma das vizinhanças sobrepostas de 500 m.','bacias':rows}
for directory in [D,O/'auditoria']:
 (directory/'Informacoes_gerais_bacias.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
pd.DataFrame(rows).to_csv(D/'Informacoes_gerais_bacias.csv',sep=';',decimal=',',index=False,encoding='utf-8-sig')
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/iniciar_consolidacao_final_teco.py

Iniciar consolidacao final teco. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\iniciar_consolidacao_final_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/tmp/consolidacao_final/entrega_final/TECO_Consolidado.qgz — chamada zipfile.ZipFile, linha 30.

**Saídas.**

- E:/teco/tmp/consolidacao_final/archive_path.txt — chamada .write_text, linha 29.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/iniciar_consolidacao_final_teco.py, linhas 29-37.

```python
(T/'archive_path.txt').write_text(str(A),encoding='utf8')
with zipfile.ZipFile(S/'TECO_Consolidado.qgz') as z:root=ET.fromstring(z.read(next(n for n in z.namelist() if n.endswith('.qgs'))))
for layout in root.findall('.//Layouts/Layout'):
 for item in layout.findall('.//LayoutItem'):
  if 'SIRGAS' in item.get('labelText',''):
   print(ET.tostring(item,encoding='unicode')[:2200]);break
 else:continue
 break
print('STAGE',S,'ARCHIVE',A)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/inspecao_relatorio_ingles.py

Inspecao relatorio ingles. Documentação/apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\inspecao_relatorio_ingles.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/entrega_final/TECO_Consolidado.qgz — chamada zipfile.ZipFile, linha 28.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'grade_resultados'] — chamada gpd.read_file, linha 40.
- E:/teco/0_ref/referencias_multivariada_crossref.json — chamada .read_text, linha 45.

**Saídas.**

- E:/teco/tmp/relatorio_detalhado/qgis_strings.txt — chamada .write_text, linha 39.
- E:/teco/tmp/relatorio_detalhado/estatisticas_resultados.json — chamada .write_text, linha 44.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/inspecao_relatorio_ingles.py, linhas 42-48.

```python
for key,g in a.groupby('BACIA'):
 stats[key]={'n':len(g),'classes':{c:g[c].value_counts(dropna=False).to_dict() for c in ['F_S0','F_S1','F_S2','F_S3','F_S4','K_S0','K_S2','MORAN','QUINTIL','ESTABILIDADE']},'medias':{c:g[c].mean() for c in ['POP_DENS','SEM_REDE','URB_PCT','I_S0','COB_ESG','EST_ESG','HIPS_M','DECL_PCT','DIST_KM']},'saude_positiva':int(g.AIH_LOCAL.gt(0).sum()),'imputadas':int(g.EST_ESG.gt(0).sum())}
(T/'estatisticas_resultados.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2,default=str),encoding='utf8')
meta=json.loads((R/'0_ref/referencias_multivariada_crossref.json').read_text('utf8'))
if isinstance(meta,dict):meta=list(meta.values())
print('REFERENCIAS',json.dumps([{'titulo':m.get('title'),'doi':m.get('DOI'),'autor':m.get('author',[{}])[0].get('family'),'ano':m.get('published')} for m in meta if isinstance(m,dict)],ensure_ascii=False))
print('STATS',json.dumps(stats,ensure_ascii=False,default=str))
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/integrar_cnes_sih_2026_qgis.py

Integrar cnes sih 2026 qgis. Cartografia/apresentação. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\integrar_cnes_sih_2026_qgis.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Auditoria_CNES_SIH_2026.json — chamada .read_text, linha 30.

**Saídas.**

- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Validacao_QGIS_2026.json — chamada .write_text, linha 52.

**Campos e chaves lidos.**

- audit: archive.

**Campos e chaves gerados.**

- os.environ: QT_QPA_PLATFORM.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/integrar_cnes_sih_2026_qgis.py, linhas 29-37.

```python
R=Path(_cp_texto('', 'posix'));F=R/'entrega_final';P=F/'01_entradas/17_estabelecimentos_2026'
audit=json.loads((P/'04_documentacao/Auditoria_CNES_SIH_2026.json').read_text('utf8'));A=Path(audit['archive'])
projects=[R/'projeto_teco.qgz',F/'TECO_Consolidado.qgz',R/'output/04_grade_500m/TECO_grade_500m.qgz']
layers=[('01_cnes_bacias/cnes_2026.shp','CNES facilities · Sep 2026','#287b95','circle','0.85'),('02_selecao_sih/sih_atual.shp','Recent SIH admissions · 2024–2026','#bd3658','star','2.8'),('03_bordas/sih_bordas.shp','Hospitals near basin boundaries','#d49b31','triangle','2.0')]
aliases={'NOME_CNES':'CNES facility name','NOME_SIH':'SIH facility name','TIPO_CNES':'CNES facility type','MUN_COD':'Municipality code','MUN_NOME':'Municipality','COMP_CNES':'CNES reference month','ATIVO_CAD':'CNES registration status','SUS_CAD':'SUS agreement','ENDERECO':'Facility address','LAT':'Latitude','LON':'Longitude','SIH_HIST':'Matched to SIH query','INT_FONTE':'Admissions · complete source total','INT_15_26':'Admissions · 2015–Sep 2026','INT_24_26':'Admissions · 2024–Sep 2026','INT_2024':'Admissions · 2024','INT_2025':'Admissions · 2025','INT_2026':'Admissions · Jan–Sep 2026','ULT_ATEND':'Latest positive care month','MES_REC':'Recent months with production','SELEC_SIH':'Recent activity selection','DIST_BAC_M':'Distance to basin (m)','BACIA':'Basin / nearest basin for external review'}
app=QgsApplication([],False);app.initQgis();q=QgsProject.instance();results=[]

for path in projects:
    target=A/path.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/integrar_populacao_uso_rede.py

Integrar populacao uso rede. Processamento ou módulo de apoio. A organização passa por archive_outputs, pop_table, lines, network_layers, add_network, etes, export_vector, main, readme, preview.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\integrar_populacao_uso_rede.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| gc | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| preparar_saneamento_ibge | Módulo autoral local; sua ficha está neste relatório. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.windows | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| shapely | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/saneamento_ibge/populacao_basico/Agregados_por_setores_basico_BR.csv — chamada pd.read_csv, linha 152.
- E:/teco/teco_base/uso_terra/uso_terra-reservatorio.tif — chamada rasterio.open, linha 163.
- E:/teco/esgoto_bh/REDE_ESGOTO.shp — chamada gpd.read_file, linha 207.
- E:/teco/ete/ide_0603_mg_ete_pto.shp — chamada gpd.read_file, linha 247.
- E:/teco/output/01_integracao_territorial/shapefiles/{name}.shp — chamada gpd.read_file, linha 266.
- E:/teco/sub_bacia/shapefiles_v6_20261109_141015/sub_bacias_exclusivas.shp — chamada gpd.read_file, linha 277.
- E:/teco/saneamento_ibge/resultados/saneamento_teco.gpkg [camada 'resumo_bacias'] — chamada gpd.read_file, linha 297.
- E:/teco/saneamento_ibge/MG_setores_CD2022.shp — chamada gpd.read_file, linha 279.

**Saídas.**

- E:/teco/descontinuado/dt.datetime.now().strftime('%Y%m%d_%H%M%S_integracao_territorial')/manifesto.json — chamada .write_text, linha 146.
- E:/teco/output/01_integracao_territorial/uso_ocupacao_bacias.tif — chamada rasterio.open, linha 195.
- {gpkg} [camada layer] — chamada g.to_file, linha 264.
- E:/teco/output/01_integracao_territorial/shapefiles/{name}.shp — chamada g.to_file, linha 266.
- E:/teco/output/01_integracao_territorial/integracao_territorial_teco.gpkg [camada 'rede_bh_registros_origem'] — chamada rawnet.to_file, linha 308.
- E:/teco/output/01_integracao_territorial/uso_ocupacao_por_classe.csv — chamada .to_csv, linha 311.
- E:/teco/output/01_integracao_territorial/atributos_integrados_bacias.csv — chamada .to_csv, linha 312.
- E:/teco/output/01_integracao_territorial/resumo_bacias.csv — chamada .to_csv, linha 313.
- E:/teco/output/01_integracao_territorial/rede_bh_registros_origem.csv — chamada .to_csv, linha 314.
- E:/teco/output/01_integracao_territorial/dicionario_campos.csv — chamada .to_csv, linha 316.
- E:/teco/output/01_integracao_territorial/auditoria_integracao.json — chamada .write_text, linha 320.
- E:/teco/output/01_integracao_territorial/LEIA_PRIMEIRO.md — chamada .write_text, linha 359.
- Mais 1 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- p: setor_id.
- unions: N, NI, S.
- bas: bas_id, bas_nome, geometry.
- net: bas_id, comp_m.
- r: DATA, ID_BASE_TR, ID_RDESG, LADO_RDESG, bas_nome, dens_pop, geometry, pct_urb, pop_a_est, sit_rede, uso_cov.
- raw: data_apur.
- clean: C, NI.
- g: area_bh.
- row: area_bh.
- values: N, S.
- e: ete_id, fase_lic, geometry, mun_nome, situ_lic.
- old: setor_id.
- c.loc: pop_a_est.
- summary.at: pop_u_est.
- net.loc: comp_m.
- audit: summary.
- a: summary.

**Campos e chaves gerados.**

- DESC: out_km2, pct_out.
- g: area_bh, bh_pct, out_km2, pct_out, rede_qual, uso_ano, uso_cov, uso_dom, uso_km2, uso_npix, uso_valid.
- source: sit_rede.
- net: comp_m.
- raw: comp_m, data_apur.
- geo: cens_urb, dens_dom, dens_pop.
- clip: frac_area, rec_km2.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| archive_outputs() | 141-147 | grava produtos |
| pop_table(ids) | 150-158 | lê dados Retorno: p. |
| RasterStats() | 161-196 | Chamadas efetivas: rasterio.open, from_bounds, Window, self.ds.window_transform, self.ds.read, abs, np.unique, print Retorno: (g, rows). |
| lines(g) | 199-203 | Chamadas efetivas: hasattr, lines Retorno: [], []. |
| network_layers(bas, bh_domain) | 206-225 | lê dados; grava produtos Retorno: (net, raw, audit). |
| add_network(g, net, bh_domain) | 228-243 | Chamadas efetivas: g.copy, g.iterrows, list, row.geometry.intersection, net.sindex.query, len, statuscols.items, sum Retorno: g. |
| etes(bas) | 246-255 | lê dados Retorno: e, s. |
| export_vector(g, name, gpkg, layer) | 258-273 | lê dados; grava produtos |
| main() | 276-322 | lê dados; grava produtos |
| readme(a) | 325-359 | grava produtos |
| preview(clip, bas) | 362-379 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/integrar_populacao_uso_rede.py, linhas 170-176.

```python
        n=len(g);lab=rasterize([(p,i+1) for i,p in enumerate(g.geometry)],out_shape=self.a.shape,transform=self.transform,fill=0,all_touched=False,dtype='int32')
        total=np.bincount(lab.ravel(),minlength=n+1)[1:]
        hist={int(c):np.bincount(lab[self.a==c],minlength=n+1)[1:] for c in self.codes}
        valid=sum(hist.values());g=g.copy();g['uso_ano']=2025;g['uso_npix']=total;g['uso_valid']=valid
        g['uso_cov']=np.divide(100*valid,total,out=np.full(n,np.nan),where=total>0);g['uso_km2']=valid*self.cell_area/1e6
        assigned=np.zeros(n,dtype=np.int64);stack=[];labels=[]
        for prefix,(codes,label) in GROUPS.items():
```

Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- bincount: Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/integrar_rede_residencia_qgis.py

Rede assistencial confirmada por residência; camada externa não muda encartes.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\integrar_rede_residencia_qgis.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/04_grade_500m/auditoria/qgis_conferencia_final.json — chamada path.read_text, linha 38.

**Saídas.**

- E:/teco/output/04_grade_500m/auditoria/qgis_conferencia_final.json — chamada path.write_text, linha 38.

**Campos e chaves lidos.**

- j: rede_residencia_geometria_pendente.
- r: nome.

**Campos e chaves gerados.**

- os.environ: QT_QPA_FONTDIR, QT_QPA_PLATFORM.
- j: camadas, detalhes, rede_residencia_estabelecimentos, rede_residencia_geometria_pendente.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/integrar_rede_residencia_qgis.py, linhas 37-38.

```python
l.setRenderer(renderer);p.addMapLayer(l,False);group.addLayer(l).setItemVisibilityChecked(False);group.setExpanded(False);assert p.write(str(R/'projeto_teco.qgz'));p.setFileName(str(O/'TECO_grade_500m.qgz'));assert p.write()
path=O/'auditoria/qgis_conferencia_final.json';j=json.loads(path.read_text('utf8'));j['camadas']=len(p.mapLayers());j['rede_residencia_estabelecimentos']=383;j['rede_residencia_geometria_pendente']=sum(f.geometry().isNull() or f.geometry().isEmpty() for f in l.getFeatures());assert j['rede_residencia_geometria_pendente']==2;j['detalhes']=[r for r in j.get('detalhes',[]) if '383 estabelecimentos com internações' not in r['nome']]+[{'nome':l.name(),'valida':True,'fonte':l.source(),'feicoes':383}];path.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf8');print('QGIS_REDE_RESIDENCIA',383,'SEM_PONTO',j['rede_residencia_geometria_pendente'],flush=True)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/integrar_refino_entrega_teco.py

Integrar refino entrega teco. Consolidação/migração: conferir pré-condições. A organização passa por main.

**Papel.** Consolidação/migração: conferir pré-condições. **Fonte inspecionada.** E:\teco\codigo\integrar_refino_entrega_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| runpy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/tmp/entrega_final/arquivo_refino_atual.txt — chamada .read_text, linha 55.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 59.
- E:/teco/output/05_auditoria_saude/refino/Dados_da_conferencia.json — chamada .read_text, linha 59.
- E:/teco/config/paleta_hipsometria.json — chamada .read_text, linha 59.
- E:/teco/config/encartes_teco.json — chamada .read_text, linha 59.
- E:/teco/entrega_final/04_saude_residencia/explorador_residencia.html — chamada explorer.read_text, linha 75.
- E:/teco/entrega_final/{rel} — chamada gpd.read_file, linha 82.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'vias_contexto'] — chamada gpd.read_file, linha 84.
- E:/teco/entrega_final/01_entradas/01_bacias/bacias.shp — chamada gpd.read_file, linha 84.
- E:/teco/entrega_final/00_documentacao/Dicionario_dos_campos.csv — chamada pd.read_csv, linha 88.
- E:/teco/entrega_final/LEIA_PRIMEIRO.md — chamada readme.read_text, linha 92.

**Saídas.**

- E:/teco/entrega_final/04_saude_residencia/Resumo_auditoria_refinada.json — chamada .write_text, linha 64.
- E:/teco/entrega_final/04_saude_residencia/explorador_residencia.html — chamada explorer.write_text, linha 75.
- E:/teco/entrega_final/{rel} — chamada g.to_file, linha 82.
- E:/teco/entrega_final/01_entradas/06_vias_contexto/vias_contexto.shp — chamada context.to_file, linha 87.
- E:/teco/entrega_final/00_documentacao/Dicionario_dos_campos.csv — chamada dic.to_csv, linha 88.
- (F / rel).parent/dicionario_campos.csv — chamada .to_csv, linha 89.
- E:/teco/entrega_final/00_documentacao/Inventario_de_camadas.csv — chamada .to_csv, linha 90.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .write_text, linha 91.
- E:/teco/entrega_final/LEIA_PRIMEIRO.md — chamada readme.write_text, linha 92.

**Campos e chaves lidos.**

- payload: dentro_bacias, metodo, metricas, unidades.
- m: mapas, rasters, vetores.
- row: slug.
- g: CNES.
- v: arquivo.
- record: campos.
- q: CNES.
- roads: TIPO_VIA, geometry, hier_legal, ogc_fid.
- x: arquivo.
- dic: arquivo.

**Campos e chaves gerados.**

- m: auditoria_refinada_saude, encartes, paleta_hipsometria.
- : feicoes.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 58-93 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/integrar_refino_entrega_teco.py, linhas 54-62.

```python
from shapely.geometry import box
R=Path(_cp_texto('', 'posix'));F=R/'entrega_final';D=F/'00_documentacao';H=R/'output/05_auditoria_saude';O=H/'refino';P=R/'output/04_grade_500m';A=Path((R/'tmp/entrega_final/arquivo_refino_atual.txt').read_text('utf8'))

# Main
def main():
 m=json.loads((D/'manifesto.json').read_text('utf8'));payload=json.loads((O/'Dados_da_conferencia.json').read_text('utf8'));u=pd.DataFrame(payload['unidades']).set_index('CNES');m['paleta_hipsometria']=json.loads((R/'config/paleta_hipsometria.json').read_text('utf8'));m['encartes']=json.loads((R/'config/encartes_teco.json').read_text('utf8'));m['auditoria_refinada_saude']=payload['metricas']
 for row in m['mapas']:
  for ext,key in [('png','arquivo'),('svg','vetorial')]:shutil.copy2(P/'figuras'/(row['slug']+'.'+ext),F/row[key])
 files=['Totais_por_unidade_2016_2025.csv','Totais_anuais_por_unidade.csv','Totais_mensais_por_unidade.csv','Unidades_dentro_bacias.csv','Producao_574_unidades_MG.csv','Distribuicao_frequencias_unidades.csv','Conferencia_producao_TabNet_RD.csv','Conferencia_unidades.html']
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/integrar_relatorio_ingles_teco.py

Integrar relatorio ingles teco. Documentação/apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\integrar_relatorio_ingles_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| idioma_cartografico_teco | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| runpy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 31.
- E:/teco/entrega_final/LEIA_PRIMEIRO.md — chamada readme.read_text, linha 44.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/Field_dictionary_EN.csv — chamada .open, linha 38.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .write_text, linha 42.
- E:/teco/entrega_final/LEIA_PRIMEIRO.md — chamada readme.write_text, linha 46.

**Campos e chaves lidos.**

- m: mapas, vetores.
- r: arquivo, slug, titulo.

**Campos e chaves gerados.**

- r: idioma_apresentacao, titulo_ingles.
- m: atualizacao_relatorio, documentos_relatorio, idioma_qgis, idioma_relatorio.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/integrar_relatorio_ingles_teco.py, linhas 30-38.

```python
R=Path(_cp_texto('', 'posix'));F=R/'entrega_final';D=F/'00_documentacao';O=R/'output/04_grade_500m'
m=json.loads((D/'manifesto.json').read_text('utf8'))
for r in m['mapas']:
 if not r['slug'].startswith('residencia_'):
  for ext,key in [('png','arquivo'),('svg','vetorial')]:shutil.copy2(O/'figuras'/(r['slug']+'.'+ext),F/r[key])
  r['idioma_apresentacao']='en';r['titulo_ingles']=en(r['titulo'])
m['atualizacao_relatorio']=datetime.datetime.now().astimezone().isoformat();m['idioma_qgis']='en';m['idioma_relatorio']='pt-BR'
m['documentos_relatorio']=['00_documentacao/Relatorio_TECO.docx','00_documentacao/Relatorio_TECO.pdf','00_documentacao/Relatorio_TECO.md','00_documentacao/Referencias_metodologia_TECO.json']
with (D/'Field_dictionary_EN.csv').open('w',encoding='utf-8-sig',newline='') as s:
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/mapas_complementares_qgis_teco.py

Mapas complementares qgis teco. Cartografia/apresentação. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\mapas_complementares_qgis_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| mapas_grade_teco | Módulo autoral local; sua ficha está neste relatório. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.path | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/01_entradas/13_relevo/{r.id}_conexao_lago.tif — chamada rasterio.open, linha 42.
- E:/teco/entrega_final/01_entradas/11_pontos_coleta/pontos_coleta.shp — chamada gpd.read_file, linha 45.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 53.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .write_text, linha 60.

**Campos e chaves lidos.**

- points: BACIA, COLETA_ID, MICRO.
- x: slug.
- m: mapas.
- row: grupo, slug.

**Campos e chaves gerados.**

- points: MICRO.
- m: mapas.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/mapas_complementares_qgis_teco.py, linhas 41-49.

```python
for ax,r in zip(axs,cart.b.itertuples()):
 with rasterio.open(F/f'01_entradas/13_relevo/{r.id}_conexao_lago.tif') as ds:
  ax.imshow(ds.read(1,masked=True),extent=(ds.bounds.left,ds.bounds.right,ds.bounds.bottom,ds.bounds.top),cmap=ListedColormap(['#ddd7c6','#469e9d']),norm=BoundaryNorm([.5,1.5,2.5],2),zorder=2)
cart.finish(fig,axs,'surface_connection','Surface connection to the reservoir','Physical context',handles=[Patch(color='#ddd7c6',label='No surface path traced'),Patch(color='#469e9d',label='Surface path to reservoir')])
points=gpd.read_file(F/'01_entradas/11_pontos_coleta/pontos_coleta.shp');points['MICRO']=points.COLETA_ID.str.contains('microcosm',case=False,na=False)
drop_vertices=np.array([(50,5),(50,5),(14,48),(14,72),(14,94),(30,112),(50,112),(70,112),(86,94),(86,72),(86,48),(50,5),(50,5),(50,5)],float);drop_vertices[:,0]=(drop_vertices[:,0]-50)/55;drop_vertices[:,1]=(60-drop_vertices[:,1])/55;drop=MarkerPath(drop_vertices,[MarkerPath.MOVETO]+[MarkerPath.CURVE4]*12+[MarkerPath.CLOSEPOLY])
fig,axs=cart.start('Sampling sites and in situ microcosms',sectors=False)
for ax,r in zip(axs,cart.b.itertuples()):
 for micro,marker,color,size in [(False,drop,'#263d4c',25),(True,'D','#a04f85',33)]:
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/mapas_grade_teco.py

Mapas grade teco. Cartografia/apresentação. A organização passa por roadtype, _savefig_en, neat, start, drawroads, finish, cat, ready, continuous, categories.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\mapas_grade_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ast | Inspeção/transformação da sintaxe Python sem executar o processamento científico. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| idioma_cartografico_teco | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.collections | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.text | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| paleta_hipsometria_teco | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.windows | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- E:/teco/config/encartes_teco.json — chamada .read_text, linha 64.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'centros_500m'] — chamada gpd.read_file, linha 245.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'rotas_d8_candidatas'] — chamada gpd.read_file, linha 249.
- E:/teco/reservatorio/{key}.shp — chamada gpd.read_file, linha 68.
- E:/teco/vias/malha_viaria.shp — chamada gpd.read_file, linha 69.
- E:/teco/teco_base/mg_mun/ide_1103_mg_municipios_pol.shp — chamada gpd.read_file, linha 80.
- E:/teco/codigo/figuras_multivariada_teco.py — chamada .read_text, linha 84.
- E:/teco/output/02_avaliacao_espacial/rasters/{r.id}_{suffix}.tif — chamada rasterio.open, linha 212.
- E:/teco/teco_base/uso_terra/uso_terra-reservatorio.tif — chamada rasterio.open, linha 219.
- E:/teco/output/02_avaliacao_espacial/rasters/{r.id}_declividade_embrapa.tif — chamada rasterio.open, linha 227.
- E:/teco/output/04_grade_500m/auditoria/metodo_grade.json — chamada .read_text, linha 229.
- E:/teco/output/04_grade_500m/rasters/{r.id}_{suffix}.tif — chamada rasterio.open, linha 243.

**Saídas.**

- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'vias_contexto'] — chamada roads.to_file, linha 252.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'hidro_contexto'] — chamada .to_file, linha 255.
- E:/teco/output/04_grade_500m/auditoria/galeria_mapas.json — chamada .write_text, linha 256.

**Campos e chaves lidos.**

- .loc: ibirite_regap, pampulha, vargem_flores.
- kwargs: bar.
- census: BACIA.
- health: AIH_ANO, BACIA.
- meta: cenarios.
- circ: BACIA.
- route: bacia.

**Campos e chaves gerados.**

- roads: TIPO_VIA.
- kwargs: bar, waterdraw.
- a: QUINTIL.
- av: QUINTIL.
- hh: BACIA.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| roadtype(s) | 73-78 | Chamadas efetivas: .upper, str Retorno: 'Sem classe cadastrada', 'Principal'. |
| _savefig_en(fig, *args, **kwargs) | 91-99 | Chamadas efetivas: fig.findobj, _savefig, en, value.startswith, txt.set_text, txt.get_text, txt.set_fontsize, txt.set_linespacing Retorno: _savefig(fig, *args, **kwargs). |
| neat(t) | 105-105 | Chamadas efetivas: .replace, t.replace Retorno: t.replace('de500m', 'de 500 m').replace('de500', 'de 500').replace('500m', '500 m'). |
| start(title, sectors=True) | 109-109 | Chamadas efetivas: base_start, en, neat Retorno: base_start(en(neat(title)), sectors). |
| drawroads(ax, r, foreground=False) | 114-119 | Chamadas efetivas: ax.get_xlim, ax.get_ylim, box, .copy, .simplify, rr.explode, .get, len |
| finish(fig, axs, *args, **kwargs) | 122-133 | Chamadas efetivas: zip, list, kwargs.get, original_finish, b.itertuples, drawroads, ww.boundary.plot, ww.plot Retorno: original_finish(fig, axs, *args, **kwargs). |
| cat(field, title, slug, labels, colors, group) | 136-141 | Chamadas efetivas: ready, start, zip, finish, b.itertuples, gg.plot, .fillna, Patch |
| ready(slug, title, group) | 144-150 | Chamadas efetivas: ET.parse, gallery.append, max, path.stat, .stat, Path Retorno: True, False. |
| continuous(field, title, name, group, *args, **kwargs) | 154-155 | Chamadas efetivas: ready, original_continuous |
| categories(field, title, name, group) | 158-159 | Chamadas efetivas: ready, original_categories |
| number_health(axs, health) | 162-168 | Chamadas efetivas: zip, b.itertuples, .itertuples, ax.annotate, str, dict |
| native_maps(fields=None, health_only=False) | 171-204 | lê dados |
| relevo_maps(suffixes=None) | 207-213 | Chamadas efetivas: start, Normalize, zip, finish, hipso_colormap, b.itertuples, rasterio.open, ax.imshow |
| main() | 216-256 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/mapas_grade_teco.py, linhas 73-81.

```python
def roadtype(s):
 s=str(s).upper()
 if 'ARTERIAL PRIMARIA' in s or 'EXPRESSA' in s:return 'Principal'
 if 'ARTERIAL' in s or 'COLETORA' in s:return 'Secundária / coletora'
 if 'LOCAL' in s:return 'Local'
 return 'Sem classe cadastrada'
roads['TIPO_VIA']=roads.hier_legal.map(roadtype)
mun=gpd.read_file(R/'teco_base/mg_mun/ide_1103_mg_municipios_pol.shp',bbox=tuple(gpd.GeoSeries([box(*b.total_bounds)],crs=b.crs).to_crs(4326).total_bounds)).to_crs(31983)
mun=mun.iloc[:0]
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/multivariada_teco.py

Implementa normalização, preenchimento censitário identificado, cenários de pesos, alinhamento de grupos, estabilidade e Moran. O programa principal é a etapa setorial anterior, distinta da grade final.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\multivariada_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| analise_espacial_teco | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| scipy.optimize | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.sparse | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| warnings | Controle de avisos de bibliotecas sem alterar a definição do estimador. |


**Entradas.**

- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'bacias_estudo'] — chamada gpd.read_file, linha 86.
- E:/teco/output/02_avaliacao_espacial/tabelas/sih_bacias_2016_2025.csv — chamada pd.read_csv, linha 96.

**Saídas.**

- E:/teco/output/03_multivariada/tabelas/{n} — chamada df.to_csv, linha 72.
- E:/teco/output/03_multivariada/teco_multivariada.gpkg [camada n] — chamada g.to_file, linha 76.
- E:/teco/output/03_multivariada/shapefiles/{n}.shp — chamada g.to_file, linha 77.
- E:/teco/output/03_multivariada/auditoria/metodo_multivariada.json — chamada .write_text, linha 249.

**Campos e chaves lidos.**

- c: geometry, setor_id.
- h: CNES, GRUPO, QA_MUN, geometry.
- u: geometry, setor_id.
- hj: CNES, dias_ano, geometry.
- u.loc: setor_id.
- r: cenario, k, silhouette.
- best: grupos_menores_1pct, k, min_grupo, silhouette.
- z: cenario, melhor_k.
- models: S0.
- scores: S0.
- rec: cenario.
- a: ESG_EST, EST_BLOCOS, EST_PESOS, MK_S0, MQ_S0, MQ_S4, MQ_S8, bas_id, elegivel, geometry, setor_id.
- rr: cluster, q.

**Campos e chaves gerados.**

- vals: urb_pct.
- u: ESG_EST, ESG_HI, ESG_LO, ESG_OBS, ESG_ORIG, EST_BLOCOS, EST_PESOS, PC1, PC2, elegivel, saude_dens, saude_n, sem_rede, sih_dens, sih_n, sih_reg.
- hj: dias_ano.
- meta: tratamento_lacunas.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| csv(df, n) | 72-72 | grava produtos |
| gp(g, n, shp=False) | 75-77 | grava produtos |
| log(*x) | 80-80 | Chamadas efetivas: print |
| assemble() | 83-122 | lê dados Retorno: (u, c, b, h). |
| normalized(u) | 125-133 | Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original. Retorno: (x, valid). |
| align(labels, reference) | 136-138 | Chamadas efetivas: .reshape, linear_sum_assignment, dict, np.array, max, zip, labels.max, reference.max Retorno: np.array([lookup[v] for v in labels]). |
| cluster(u, x, valid) | 141-191 | Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes. Retorno: (u, k0, models, base, ev). |
| queen(g) | 194-196 | Chamadas efetivas: g.sindex.query, len, csr_matrix, w.maximum, w.setdiag, w.eliminate_zeros, np.ones Retorno: w. |
| moran_w(values, w, local=False, seed=SEED) | 199-216 | Chamadas efetivas: np.flatnonzero, .tocsr, len, float, np.random.default_rng, range, np.empty, bh Retorno: (rec, {'p': p, 'q': q, 'cluster': cl, 'Ii': Ii}, original), ({'n': n, 'isolados': int((~good).sum()), 'I': np.nan, 'p': np.nan}, None, original). |
| spatial(c, u) | 219-242 | Chamadas efetivas: c.merge, .groupby, csv, gp, .rename, pd.DataFrame, queen, moran_w Retorno: a. |
| main() | 245-250 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/multivariada_teco.py, linhas 126-132.

```python
 valid=u.elegivel;raw=u.loc[valid,FEATURES].to_numpy(float);t=raw.copy()
 for i in [0,3,4]:t[:,i]=np.log1p(t[:,i])
 lo=t.min(0);hi=t.max(0);assert (hi>lo).all()
 x=(t-lo)/(hi-lo)
 pars=[{'variavel':f,'transformacao':'log1p' if j in [0,3,4] else 'identidade','min_transformado':lo[j],'max_transformado':hi[j],'peso_base':1,'setores_nao_nulos':int((raw[:,j]>0).sum())} for j,f in enumerate(FEATURES)]
 csv(pd.DataFrame(pars),'parametros_normalizacao.csv')
 csv(pd.DataFrame(x,columns=FEATURES).assign(setor_id=u.loc[valid,'setor_id'].values),'matriz_normalizada.csv')
```

Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/multivariada_teco.py, linhas 136-142.

```python
def align(labels,reference):
 k=max(labels.max(),reference.max())+1;tab=np.bincount(reference*k+labels,minlength=k*k).reshape(k,k)
 rr,cc=linear_sum_assignment(-tab);lookup=dict(zip(cc,rr));return np.array([lookup[v] for v in labels])

# Cluster
def cluster(u,x,valid):
 krows=[];scenario_rows=[];profiles=[];models={};predictions={};scores={};counts=[]
```

Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.

Alinha rótulos de grupos pela maior correspondência; evita contar como mudança apenas a troca do número do grupo.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- log1p: Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.
- bincount: Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.
- linear_sum_assignment: Alinha rótulos de grupos pela maior correspondência; evita contar como mudança apenas a troca do número do grupo.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.
- log: Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- spearmanr: Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.
- cdist: Matriz de distâncias entre observações. É usada no agrupamento, na silhouette ou na comparação entre centroides.
- svd: Decomposição em valores singulares. Na PCA, a matriz centrada é decomposta em U, s e V; a proporção de variância é s²/Σs². É uma descrição da variação, não teste causal.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/obter_cnes.py

Obter cnes. Aquisição/leitura. A organização passa por page, municipality.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\teco\codigo\obter_cnes.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| requests | Consultas e downloads HTTP; depende de internet e da disponibilidade do provedor. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |


**Entradas.**

- E:/teco/dados_publicos/cnes/ativo_{m}_{o}.json — chamada p.read_text, linha 34.

**Saídas.**

- E:/teco/dados_publicos/cnes/ativo_{m}_{o}.json — chamada p.write_text, linha 38.
- E:/teco/dados_publicos/cnes/estabelecimentos_ativos_municipios.json — chamada .write_text, linha 58.
- E:/teco/dados_publicos/cnes/origem.json — chamada .write_text, linha 59.

**Campos e chaves lidos.**

- j: estabelecimentos.
- r: codigo_cnes, codigo_municipio.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| page(m, o) | 32-41 | lê dados; grava produtos Retorno: json.loads(p.read_text(encoding='utf8'))['estabelecimentos'], j['estabelecimentos']. |
| municipality(m) | 44-55 | Chamadas efetivas: all, print, ThreadPoolExecutor, len, list, any, set, pool.map Retorno: rows. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/obter_cnes.py, linhas 56-60.

```python
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=3) as pool: rows=sum(list(pool.map(municipality,MUN)),[])
 (ROOT/'estabelecimentos_ativos_municipios.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
 (ROOT/'origem.json').write_text(json.dumps({'url':URL,'consulta':str(datetime.datetime.now().astimezone()),'filtros':{'municipios':MUN,'status':1,'limit':20,'offset':'página, não deslocamento em linhas'},'registros':len(rows),'aviso':'Cadastro ativo consultado agora; não é série histórica 2016-2025 nem data de referência homogênea dos registros.'},ensure_ascii=False,indent=2),encoding='utf8')
 print('CONCLUIDO',len(rows),flush=True)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/obter_rd_grade.py

Obter rd grade. Aquisição/leitura. A organização passa por month, main, save, val.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\teco\codigo\obter_rd_grade.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| ftplib | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| struct | Decodificação binária com tipos, tamanhos e ordem de bytes definidos. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |


**Entradas.**

- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'saude_historico_sih'] — chamada gpd.read_file, linha 52.
- E:/teco/tmp/rd/RDMG{year % 100}{m}.json — chamada cache.read_text, linha 59.
- E:/teco/tmp/rd/RDMG{year % 100}{m}.dbf — chamada dbf.read_bytes, linha 69.
- E:/teco/dados_publicos/saude_grade/rd/RDMG{year % 100}{m}.dbc — chamada dst.open, linha 85.

**Saídas.**

- dst.with_suffix('.part') — chamada tmp.open, linha 66.
- E:/teco/tmp/rd/RDMG{year % 100}{m}.json — chamada cache.write_text, linha 86.
- E:/teco/output/04_grade_500m/tabelas/{n} — chamada f.to_csv, linha 108.
- pd.DataFrame(allrows).sort_values(['CNES', 'ano', 'mes', 'CID10']) — chamada save, linha 109.
- f.groupby(['CNES', 'unidade', 'ano', 'CID10'], as_index=False)[['internacoes', 'dias']].sum() — chamada save, linha 109.
- pd.DataFrame([[*k, v] for k, v in adm.items()], columns=['CNES', 'ano_mes_internacao', 'CID10', 'internacoes']) — chamada save, linha 110.
- c.drop(columns='internacoes') — chamada save, linha 113.
- pd.DataFrame([[*k, v] for k, v in mun.items()], columns=['CNES', 'municipio_residencia', 'internacoes']) — chamada save, linha 114.
- E:/teco/output/04_grade_500m/filtro_cid10.csv — chamada fl.to_csv, linha 116.
- units.drop(columns='geometry').copy() — chamada save, linha 118.
- E:/teco/output/04_grade_500m/auditoria/coleta_rd.json — chamada .write_text, linha 120.

**Campos e chaves lidos.**

- units: CNES.
- fields: CNES, IDENT.
- z: admissao, ano, ceps, diag, mes, residencia.
- c: internacoes.
- f: CID10.
- meta: aih_normais, competencias_obtidas, unidades_com_aih.

**Campos e chaves gerados.**

- payload: filtro_sha256.
- f: unidade.
- c: internacoes_publicaveis, situacao.
- fl: incluir, justificativa.
- cov: AIH_2016_2025, STATUS.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| month(ym) | 56-90 | lê dados; grava produtos Retorno: cached, payload. |
| main() | 93-120 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/obter_rd_grade.py, linhas 108-114.

```python
 def save(f,n):f.to_csv(O/'tabelas'/n,index=False,sep=';',encoding='utf-8-sig')
 save(f,'sih_cid10_mensal.csv');save(f.groupby(['CNES','unidade','ano','CID10'],as_index=False)[['internacoes','dias']].sum(),'sih_cid10_anual.csv')
 a=pd.DataFrame([[*k,v] for k,v in adm.items()],columns=['CNES','ano_mes_internacao','CID10','internacoes']);save(a,'sih_cid10_mes_internacao.csv')
 c=pd.DataFrame([[*k,v] for k,v in ceps.items()],columns=['CNES','CEP','internacoes']);c['situacao']=c.internacoes.map(lambda n:'Publicação agregada: menos de 5' if n<5 else 'Contagem agregada')

 c['internacoes_publicaveis']=c.internacoes.where(c.internacoes>=5);save(c.drop(columns='internacoes'),'sih_ceps_origem_2016_2025.csv')
 save(pd.DataFrame([[*k,v] for k,v in mun.items()],columns=['CNES','municipio_residencia','internacoes']),'sih_municipios_origem.csv')
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/obter_rd_grade.py, linhas 116-121.

```python
 if not path.exists():fl.to_csv(path,index=False,sep=';',encoding='utf-8-sig')
 cov=units.drop(columns='geometry').copy();cov['AIH_2016_2025']=cov.CNES.map(f.groupby('CNES').internacoes.sum());cov['STATUS']=cov.AIH_2016_2025.notna().map({True:'Produção SIH recuperada',False:'Sem AIH normal recuperada; não é zero atendimento'})
 save(cov,'cobertura_rd_unidades.csv')
 meta={'fonte':'ftp://ftp.datasus.gov.br'+FTP,'consultado':datetime.datetime.now().astimezone().isoformat(),'competencias_esperadas':120,'competencias_obtidas':sum('erro' not in z for z in rows),'unidades_no_cadastro':len(units),'unidades_com_aih':int(f.CNES.nunique()),'aih_normais':int(f.internacoes.sum()),'CID10_distintos':f.CID10.nunique(),'meses':[dict((k,v) for k,v in z.items() if k not in ['diag','ceps','residencia','admissao']) for z in sorted(rows,key=lambda z:(z['ano'],z['mes']))],'metodo':'IDENT=1; diagnóstico principal; competência de processamento. Mantém data de internação em série separada. Não conta pacientes únicos. Arquivos DBF temporários removidos após agregação.','CEP':'Origem observada de pacientes, não território oficial de UBS. Contagens de menos de 5 suprimidas na saída de CEP; não geocodificadas automaticamente.'}
 (O/'auditoria/coleta_rd.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8');print('RD_CONCLUIDO',meta['competencias_obtidas'],meta['unidades_com_aih'],meta['aih_normais'],flush=True)
if __name__=='__main__':main()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/obter_rd_residencia_teco.py

Obter rd residencia teco. Aquisição/leitura. A organização passa por month, main, col, val.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\teco\codigo\obter_rd_residencia_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| struct | Decodificação binária com tipos, tamanhos e ordem de bytes definidos. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/tmp/rd_residencia_v1/RDMG{y % 100}{m}.json — chamada out.read_text, linha 39.
- E:/teco/tmp/rd_residencia_v1/RDMG{y % 100}{m}.dbf — chamada dbf.read_bytes, linha 41.

**Saídas.**

- E:/teco/tmp/rd_residencia_v1/RDMG{y % 100}{m}.json — chamada out.write_text, linha 56.
- E:/teco/output/05_auditoria_saude/RD_MG_residentes_mensal_CID10.csv — chamada f.to_csv, linha 68.
- E:/teco/output/05_auditoria_saude/RD_MG_residentes_anuais.csv — chamada .to_csv, linha 69.
- E:/teco/output/05_auditoria_saude/RD_MG_residentes_estabelecimentos.csv — chamada .to_csv, linha 69.
- E:/teco/output/05_auditoria_saude/RD_MG_todos_estabelecimentos_2016_2025.csv — chamada .to_csv, linha 70.
- E:/teco/output/05_auditoria_saude/RD_residentes_CEP_agregado.csv — chamada cp.to_csv, linha 71.
- E:/teco/output/05_auditoria_saude/RD_residencia_auditoria.json — chamada .write_text, linha 72.

**Campos e chaves lidos.**

- j: ano, ceps, diag, hospitais_todos, mes.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| month(ym) | 36-56 | lê dados; grava produtos Retorno: j, np.char.strip(np.ndarray(n, dtype=f'S{l}', buffer=data, offset=head + a, strides=(rec,))). |
| main() | 59-72 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/obter_rd_residencia_teco.py, linhas 68-73.

```python
 f=pd.DataFrame(rows).sort_values(['CNES','MUN_RES','ANO','MES','CID10']);f.to_csv(O/'RD_MG_residentes_mensal_CID10.csv',sep=';',index=False,encoding='utf-8-sig')
 f.groupby(['CNES','MUN_RES','ANO'],as_index=False).AIH.sum().to_csv(O/'RD_MG_residentes_anuais.csv',sep=';',index=False,encoding='utf-8-sig');f.groupby('CNES',as_index=False).AIH.sum().to_csv(O/'RD_MG_residentes_estabelecimentos.csv',sep=';',index=False,encoding='utf-8-sig')
 pd.DataFrame([{'CNES':c,'AIH':n} for c,n in allh.items()]).to_csv(O/'RD_MG_todos_estabelecimentos_2016_2025.csv',sep=';',index=False,encoding='utf-8-sig')
 cp=pd.DataFrame([[*k,n if n>=5 else None,'Contagem agregada' if n>=5 else 'Menos de 5: suprimido'] for k,n in ceps.items()],columns=['CNES','MUN_RES','CEP','AIH_PUBLICAVEIS','SITUACAO']);cp.to_csv(O/'RD_residentes_CEP_agregado.csv',sep=';',index=False,encoding='utf-8-sig')
 meta={'data':datetime.datetime.now().astimezone().isoformat(),'fonte':'ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/','especificacao':SPEC,'filtro_sha256':FINGER,'competencias':len(results),'AIH_residentes':int(f.AIH.sum()),'hospitais_residentes':f.CNES.nunique(),'hospitais_MG_total':len(allh),'AIH_MG_total':int(sum(allh.values())),'limite':'Arquivos RD da UF de internação MG. A concordância com NRMG será verificada, sem presumir cobertura de atendimentos em outras UFs.'};(O/'RD_residencia_auditoria.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8');print('RD_RES_COMPLETO',json.dumps(meta,ensure_ascii=True),flush=True)
if __name__=='__main__':main()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/obter_sih_grade.py

Obter sih grade. Aquisição/leitura. A organização passa por query, safe.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\teco\codigo\obter_sih_grade.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| bs4 | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| requests | Consultas e downloads HTTP; depende de internet e da disponibilidade do provedor. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |
| urllib.parse | Requisições e manipulação de endereços de serviços públicos. |


**Entradas.**

- E:/teco/dados_publicos/saude_grade/rd_form.txt — chamada .read_bytes, linha 44.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'saude_historico_sih'] — chamada gpd.read_file, linha 47.
- E:/teco/dados_publicos/saude_grade/morb_{cnes}_mensal_2016_2025.html — chamada path.read_text, linha 61.
- E:/teco/output/04_grade_500m/tabelas/sih_cid10_mensal.csv — chamada pd.read_csv, linha 95.

**Saídas.**

- E:/teco/dados_publicos/saude_grade/campos_morbidade.json — chamada .write_text, linha 46.
- E:/teco/dados_publicos/saude_grade/consulta_morb_{cnes}.json — chamada .write_text, linha 60.
- E:/teco/dados_publicos/saude_grade/morb_{cnes}_mensal_2016_2025.html — chamada path.write_text, linha 66.
- E:/teco/output/04_grade_500m/tabelas/conferencia_RD_lista_morbidade.csv — chamada .to_csv, linha 99.
- E:/teco/output/04_grade_500m/tabelas/sih_causas_mensais.csv — chamada f.to_csv, linha 100.
- E:/teco/output/04_grade_500m/tabelas/sih_causas_anuais.csv — chamada .to_csv, linha 101.
- E:/teco/output/04_grade_500m/tabelas/sih_total_mensal.csv — chamada .to_csv, linha 102.
- E:/teco/output/04_grade_500m/tabelas/cobertura_unidades_sih.csv — chamada cov.to_csv, linha 104.
- E:/teco/output/04_grade_500m/auditoria/coleta_sih.json — chamada .write_text, linha 106.

**Campos e chaves lidos.**

- units: CNES.
- fields: Arquivos, Coluna, Incremento, Linha, SEstabelecimento.
- f: CNES.

**Campos e chaves gerados.**

- comparison: diferenca_RD_menos_folhas.
- cov: STATUS_MENSAL.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| query(opt) | 57-84 | lê dados; grava produtos Retorno: rows. |
| safe(opt) | 88-90 | Chamadas efetivas: query, errors.append, str Retorno: query(opt), []. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/obter_sih_grade.py, linhas 90-96.

```python
 except Exception as e:errors.append({'unidade':opt[1],'erro':str(e)});return []
with ThreadPoolExecutor(max_workers=2) as pool:rows=sum(list(pool.map(safe,opts)),[])
f=pd.DataFrame(rows)
if not len(f):raise RuntimeError('Nenhum mês interpretado; conferir retorno original.')
if rdfile.exists():
 expected=pd.read_csv(rdfile,sep=';',dtype={'CNES':str}).groupby('CNES').internacoes.sum()
 actual=f.groupby('CNES').internacoes.sum()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/obter_sih_residencia_tabnet.py

Obter sih residencia tabnet. Aquisição/leitura. A organização passa por query, main.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\teco\codigo\obter_sih_residencia_tabnet.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| requests | Consultas e downloads HTTP; depende de internet e da disponibilidade do provedor. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |
| urllib.parse | Requisições e manipulação de endereços de serviços públicos. |


**Entradas.**

- E:/teco/dados_publicos/auditoria_sih_20261112/campos_NRMG.json — chamada .read_text, linha 39.
- E:/teco/dados_publicos/auditoria_sih_20261112/NRMG_{m}_2016_2025.html — chamada path.read_text, linha 47.

**Saídas.**

- E:/teco/dados_publicos/auditoria_sih_20261112/consulta_NRMG_{m}.json — chamada .write_text, linha 46.
- E:/teco/dados_publicos/auditoria_sih_20261112/NRMG_{m}_2016_2025.html — chamada path.write_text, linha 51.
- E:/teco/output/05_auditoria_saude/NRMG_internacoes_por_residencia_anuais.csv — chamada f.to_csv, linha 70.
- E:/teco/output/05_auditoria_saude/NRMG_estabelecimentos_com_internacoes.csv — chamada u.to_csv, linha 70.
- E:/teco/output/05_auditoria_saude/NRMG_auditoria.json — chamada .write_text, linha 72.

**Campos e chaves lidos.**

- fields: Arquivos, Incremento.
- base: Arquivos.
- f.loc: AIH.
- f: AIH, ANO, CNES.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| query(m) | 42-65 | lê dados; grava produtos Retorno: f. |
| main() | 68-72 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/obter_sih_residencia_tabnet.py, linhas 63-69.

```python
 f=pd.DataFrame(rows);assert len(f)
 for y,total in totals.items():assert f.loc[f.ANO==y,'AIH'].sum()==total,(m,y,total)
 print('NRMG',m,f.CNES.nunique(),int(f.AIH.sum()),flush=True);return f

# Main
def main():
 with ThreadPoolExecutor(2) as pool:f=pd.concat(list(pool.map(query,MUN)),ignore_index=True)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/obter_sih_teco.py

Obter sih teco. Aquisição/leitura. A organização passa por obtain, parse.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\teco\codigo\obter_sih_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| requests | Consultas e downloads HTTP; depende de internet e da disponibilidade do provedor. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |
| urllib.parse | Requisições e manipulação de endereços de serviços públicos. |


**Entradas.**

- E:/teco/dados_publicos/saude/campos_tabnet.json — chamada .read_text, linha 40.
- E:/teco/dados_publicos/saude/sih_municipios_2016_2025_{metric}.html — chamada fn.read_text, linha 54.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'saude_hosp_inativos_candidatos'] — chamada gpd.read_file, linha 81.

**Saídas.**

- E:/teco/dados_publicos/saude/consulta_{metric}.json — chamada .write_text, linha 53.
- E:/teco/dados_publicos/saude/sih_municipios_2016_2025_{metric}.html — chamada fn.write_text, linha 60.
- E:/teco/output/02_avaliacao_espacial/tabelas/sih_municipios_2016_2025.csv — chamada hist.to_csv, linha 86.
- E:/teco/output/02_avaliacao_espacial/tabelas/sih_bacias_2016_2025.csv — chamada inside.to_csv, linha 87.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'saude_historico_sih'] — chamada geo.to_file, linha 90.
- E:/teco/output/02_avaliacao_espacial/tabelas/saude_cobertura_sih.csv — chamada .to_csv, linha 91.
- E:/teco/dados_publicos/saude/origem_sih.json — chamada .write_text, linha 93.

**Campos e chaves lidos.**

- d: Arquivos, Incremento.
- active: CNES, NOME, bacia, geometry.
- inactive: CNES, geometry, id, nome_fantasia.

**Campos e chaves gerados.**

- loc: cadastro.
- ins: cadastro.
- geo: SIT_SIH.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| obtain(metric, value) | 51-63 | lê dados; grava produtos Retorno: fn.read_text(encoding='utf8'), txt. |
| parse(txt, metric) | 66-76 | Chamadas efetivas: html.unescape, pd.DataFrame, zip, re.findall, csv.reader, re.match, io.StringIO, len Retorno: pd.DataFrame(rows). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/obter_sih_teco.py, linhas 87-93.

```python
inside.to_csv(O/'tabelas/sih_bacias_2016_2025.csv',index=False,sep=';',encoding='utf-8-sig')
summary=inside.groupby('CNES')[['internacoes','dias_permanencia']].sum(min_count=1).reset_index()
geo=loc.merge(summary,on='CNES',how='left',validate='one_to_one');geo['SIT_SIH']=geo.internacoes.notna().map({True:'Retornado na consulta 2016-2025',False:'Sem linha retornada; não equivale a ausência de atividade'})
geo.to_file(G,layer='saude_historico_sih',driver='GPKG')
pd.DataFrame(geo.drop(columns='geometry')).to_csv(O/'tabelas/saude_cobertura_sih.csv',index=False,sep=';',encoding='utf-8-sig')
meta={'url':URL,'consulta':datetime.datetime.now().astimezone().isoformat(),'anos_processamento':list(range(2016,2026)),'municipios':mun,'estabelecimentos_com_linhas_municipios':int(hist.CNES.nunique()),'estabelecimentos_localizados_bacias':int(inside.CNES.nunique()),'linhas_bacias':len(inside),'aviso':'Internações SUS e dias de permanência por ano de processamento; não cobre todo atendimento privado nem visitas UBS. Localização pelo cadastro atual e hospitais inativos candidatos. Não representa infecções resistentes ou emissões de genes. Nenhum nulo é convertido em zero, exceto símbolo - definido pelo TabNet como zero.'}
(D/'origem_sih.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(meta,ensure_ascii=True),flush=True)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/paleta_hipsometria_teco.py

Paleta hipsometria teco. Cartografia/apresentação. A organização passa por metadata, colormap.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\paleta_hipsometria_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:\teco/config/paleta_hipsometria.json — chamada CONFIG.read_text, linha 27.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- s: cor, posicao.
- d: paradas.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| metadata() | 27-27 | lê dados Retorno: json.loads(CONFIG.read_text('utf8')). |
| colormap() | 30-32 | Chamadas efetivas: metadata, LinearSegmentedColormap.from_list Retorno: LinearSegmentedColormap.from_list('QGIS_GMT_dem1', [(s['posicao'], s['cor']) for s in d['paradas']], N=1024). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/paleta_hipsometria_teco.py, linhas 27-32.

```python
def metadata():return json.loads(CONFIG.read_text('utf8'))

# Colormap
def colormap():
 from matplotlib.colors import LinearSegmentedColormap
 d=metadata();return LinearSegmentedColormap.from_list('QGIS_GMT_dem1',[(s['posicao'],s['cor']) for s in d['paradas']],N=1024)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/planilha_8municipios_teco.mjs

Planilha 8municipios teco. Processamento ou módulo de apoio. A organização passa por col, sheet, callback, callback, callback, callback, callback, callback, callback, callback.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\planilha_8municipios_teco.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ./caminhos_teco.mjs | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| node:fs/promises | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| @oai/artifact-tool | Biblioteca de autoria do ambiente de apresentações/planilhas; precisa ser disponibilizada na máquina de autoria. |


**Entradas.**

- root+'/workbook_data.json' — chamada fs.readFile, linha 13.

**Saídas.**

- root+'/previews/xlsx_'+sheetName+'.png' — chamada fs.writeFile, linha 26.
- root+'/entrega_final/04_datasus/01_conjunto_8_municipios/Internacoes_8_municipios.xlsx' — chamada x.save, linha 27.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/planilha_8municipios_teco.mjs, linhas 14-22.

```javascript
const col=n=>{let s='';while(n){s=String.fromCharCode(65+(n-1)%26)+s;n=Math.floor((n-1)/26)}return s};
// sheet
function sheet(name,title,headers,rows,widths){
 const s=w.worksheets.add(name),end=rows.length+5,range=`A5:${col(headers.length)}${end}`;s.showGridLines=false;s.getRange(`A1:${col(headers.length)}${end}`).format.font={name:'Arial',size:10};s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:14,bold:true,color:'#234e60'};s.getRange(range).values=[headers,...rows];s.getRange(`A5:${col(headers.length)}5`).format={fill:'#234e60',font:{name:'Arial',size:10,color:'#ffffff',bold:true},wrapText:true,rowHeight:46,verticalAlignment:'center'};s.getRange(`A6:${col(headers.length)}${end}`).format.rowHeight=23;s.getRange(`A6:${col(headers.length)}${end}`).format.verticalAlignment='center';widths.forEach((v,i)=>s.getRange(`${col(i+1)}5:${col(i+1)}${end}`).format.columnWidth=v);s.freezePanes.freezeRows(5);if(rows.length>30)s.tables.add(range,true,name.replaceAll(' ','')+'Data');return s;
}
const units=sheet('Unidades','Internações de residentes dos oito municípios por hospital, 2016-2025',['CNES','Estabelecimento','Bacia física','Total oficial NRMG','Total bruto RD','A','B','A+B','Diferença RD-NRMG','Produção de todas as origens','Produção A+B','Localização'],d.units.map(u=>[u.CNES,u.NOME_TABNET,u.BACIA,u.AIH_NRMG,u.RES_RD,u.RES8_A,u.RES8_B,null,null,u.PROD_TOT,u.PROD_AB,u.SIT_ESPACIAL]),[14,73,22,25,23,17,17,22,26,30,25,49]);let end=d.units.length+5;units.getRange(`A6:A${end}`).setNumberFormat('@');units.getRange(`D6:K${end}`).setNumberFormat('#,##0');units.getRange(`H6:H${end}`).formulas=d.units.map((_,i)=>[`=SUM(F${i+6}:G${i+6})`]);units.getRange(`I6:I${end}`).formulas=d.units.map((_,i)=>[`=E${i+6}-D${i+6}`]);
const summary=sheet('Resumo','TECO  •  Conferência final dos oito municípios',['Recorte','Quantidade'],[['Municípios',8],['Competências mensais, 2016-2025',120],['Hospitais com internações de residentes',387],['Total oficial NRMG',null],['Total bruto RD',null],['Seleção operacional A+B',null],['Diferença preservada RD-NRMG',null],['Hospitais fisicamente dentro das bacias',3],['Coordenadas pendentes, mantidos na tabela',2]],[67,30]);for(const [row,c] of [[9,'D'],[10,'E'],[11,'H'],[12,'I']])summary.getRange('B'+row).formulas=[[`=SUM(Unidades!${c}6:${c}${end})`]];summary.getRange('B6:B14').setNumberFormat('#,##0');
const mun=sheet('Municipios','Residência municipal não identifica residência dentro de uma bacia',['Código IBGE','Município','Hospitais que atenderam residentes','Total NRMG','Total RD','A','B','A+B','RD-NRMG'],d.municipalities.map(u=>[u.MUN_RES,u.MUNICIPIO,u.UNIDADES,u.NRMG,u.RES8_TOTAL,u.RES8_A,u.RES8_B,null,null]),[18,31,32,25,25,22,22,24,25]);mun.getRange('A6:A13').setNumberFormat('@');mun.getRange('C6:I13').setNumberFormat('#,##0');mun.getRange('H6:H13').formulas=d.municipalities.map((_,i)=>[`=SUM(F${i+6}:G${i+6})`]);mun.getRange('I6:I13').formulas=d.municipalities.map((_,i)=>[`=E${i+6}-D${i+6}`]);
const annual=sheet('Anual','Internações por hospital e ano de processamento',['CNES','Estabelecimento','Ano','Total NRMG','Total bruto RD','A','B','A+B'],d.annual.map(u=>[u.CNES,u.NOME_TABNET,u.ANO,u.NRMG,u.RES8_TOTAL,u.RES8_A,u.RES8_B,u.RES8_AB]),[14,73,14,25,25,20,20,24]);annual.getRange(`A6:A${d.annual.length+5}`).setNumberFormat('@');annual.getRange(`C6:C${d.annual.length+5}`).setNumberFormat('0');annual.getRange(`D6:H${d.annual.length+5}`).setNumberFormat('#,##0');
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/planilha_auditoria_residencia.mjs

Planilha auditoria residencia. Processamento ou módulo de apoio. A organização passa por col, sheet, callback, callback, callback, callback, callback.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\planilha_auditoria_residencia.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ./caminhos_teco.mjs | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| node:fs/promises | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| @oai/artifact-tool | Biblioteca de autoria do ambiente de apresentações/planilhas; precisa ser disponibilizada na máquina de autoria. |


**Entradas.**

- out+'/planilha_dados.json' — chamada fs.readFile, linha 13.

**Saídas.**

- out+'/previa_'+name.normalize('NFD').replace(/[\u0300-\u036f]/g,'')+'.png' — chamada fs.writeFile, linha 25.
- out+'/Conferencia_Internacoes_Residencia.xlsx' — chamada x.save, linha 26.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/planilha_auditoria_residencia.mjs, linhas 15-23.

```javascript
function col(n){let s='';for(;n>0;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
// sheet
function sheet(name,title,headers,rows,widths){const s=wb.worksheets.add(name);s.showGridLines=false;s.getRange(`A1:${col(headers.length)}${rows.length+5}`).format.font={name:'Arial',size:10};s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:15,bold:true,color:'#234b5b'};s.getRange(`A5:${col(headers.length)}${rows.length+5}`).values=[headers,...rows];s.getRange(`A5:${col(headers.length)}5`).format={fill:'#31566d',font:{name:'Arial',size:10,bold:true,color:'#ffffff'},rowHeight:34,wrapText:true,verticalAlignment:'center'};s.getRange(`A6:${col(headers.length)}${rows.length+5}`).format.rowHeight=23;widths.forEach((w,i)=>s.getRange(`${col(i+1)}5:${col(i+1)}${rows.length+5}`).format.columnWidth=w);s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(2);return s;}
const r=sheet('Resumo','Internações por residência | conferência da consulta NRMG',['Município de residência','Estabelecimentos com AIH','Internações 2016-2025','AIH filtro amplo A+B'],d.resumo.map(r=>[r.MUNICIPIO_RESIDENCIA,r.ESTABELECIMENTOS,r.AIH,r.AIH_AB]),[30,28,30,30]);r.getRange('B6:D9').setNumberFormat('#,##0');r.getRange('A12').values=[['383 estabelecimentos distintos. Um mesmo hospital pode receber moradores de vários municípios.']];r.getRange('A14').values=[['2.038.486 internações na consulta NRMG. Município de residência não equivale a residência dentro da bacia.']];r.getRange('A16').values=[['O catálogo inclui apenas produção positiva. Ausência de coordenada não exclui um hospital com internações.']];
const h=sheet('Estabelecimentos','Estabelecimentos com internações confirmadas no recorte de residência',['CNES','Nome no TabNet','AIH todas as causas','AIH filtro A+B','AIH etiologia codificada A','AIH compatíveis B','Município do hospital (código)','Localização em relação às bacias','Bacia física','Distância até bacia (m)','Latitude','Longitude'],d.hospitais.map(x=>[x.CNES,x.NOME_TABNET,x.AIH_NRMG,x.AIH_AB,x.AIH_A,x.AIH_B,x.MUNICIPIO==null?null:String(Math.trunc(x.MUNICIPIO)),x.SIT_ESPACIAL,x.BACIA,x.DIST_BACIA_M,x.LAT,x.LON]),[15,74,26,23,26,24,30,50,25,28,18,18]);h.getRange(`A6:A${d.hospitais.length+5}`).setNumberFormat('@');h.getRange(`C6:F${d.hospitais.length+5}`).setNumberFormat('#,##0');h.getRange(`J6:J${d.hospitais.length+5}`).setNumberFormat('#,##0');h.getRange(`K6:L${d.hospitais.length+5}`).setNumberFormat('0.000000');h.tables.add(`A5:L${d.hospitais.length+5}`,true,'HospitaisConfirmados');
const a=sheet('Anual','Consulta oficial | município de residência × hospital × ano',['Município (código)','Município de residência','CNES','Estabelecimento','Ano de processamento','Internações'],d.anual.map(x=>[String(x.MUN_RES),x.MUNICIPIO_RESIDENCIA,x.CNES,x.NOME_TABNET,x.ANO,x.AIH]),[23,30,15,74,26,23]);a.getRange(`A6:A${d.anual.length+5}`).setNumberFormat('@');a.getRange(`C6:C${d.anual.length+5}`).setNumberFormat('@');a.getRange(`E6:F${d.anual.length+5}`).setNumberFormat('#,##0');a.tables.add(`A5:F${d.anual.length+5}`,true,'ProducaoAnual');
const c=sheet('Diagnósticos','Critério aplicado às causas observadas | não confirma resistência',['CID10','Descrição','Nível','Grupo operacional','Incluído em A+B'],d.causas.map(x=>[x.CID10,x.DIAGNOSTICO,x.NIVEL,x.GRUPO,x.INCLUIR_AB?1:0]),[15,85,15,85,24]);c.getRange(`B6:D${d.causas.length+5}`).format.wrapText=true;c.getRange(`A6:E${d.causas.length+5}`).format.rowHeight=32;c.getRange(`E6:E${d.causas.length+5}`).setNumberFormat('0');c.tables.add(`A5:E${d.causas.length+5}`,true,'CausasAuditadas');
const notes=[['Fonte principal','TabNet NRMG: morbidade hospitalar por local de residência. Consultas separadas para BH, Contagem, Betim e Ibirité, 2016-2025.'],['Consulta','Linha Estabelecimento; coluna Ano de processamento; conteúdo Internações; nenhum filtro prévio por CNES, tipo, situação atual ou diagnóstico.'],['Número de unidades','383 estabelecimentos distintos com produção positiva. As contagens municipais se sobrepõem.'],['Localização','3 com coordenadas nas bacias; 378 localizados fora; 2 sem coordenada recuperada. Estes últimos continuam no catálogo, sem ponto inventado.'],['Conferência independente','120 arquivos oficiais RD-MG, enumerando todos os CNES. Foram encontrados 574 hospitais com AIH normal no estado, sem lista prévia de estabelecimentos.'],['Totais','NRMG: 2.038.486. RD integral do recorte: 2.038.504. A diferença de 18 foi localizada em N182/N183/N184/N185 não mapeados no dicionário consultado.'],['Reconciliação','Após separar e preservar esses 18 registros, os totais coincidem para cada combinação hospital × município de residência × ano. Não houve rateio ou ajuste artificial.'],['Filtro','662 códigos observados classificados no critério amplo A+B; 274.254 AIH. A: etiologia bacteriana codificada; B: síndrome compatível sem agente confirmado. C: associações/sequelas fora do índice principal.'],['Meses e doenças','CSV mensais e por CID10 são fornecidos em separado. O explorador permite consultar as séries de todos os 383 estabelecimentos.'],['Residência versus bacia','O filtro municipal não identifica o domicílio dentro da bacia. Os CEPs agregados estão separados para futura geocodificação validada. Não distribuir casos por raio de hospital.'],['Fonte NRMG','https://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/nrmg.def'],['Fonte RD','ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/'],['Auditoria',_cpPath("output/05_auditoria_saude/consolidacao.json")],['Proteção dos agregados','Não há fichas individuais nas saídas. No arquivo por CEP, contagens menores que cinco foram suprimidas.'],['Período','Competência de processamento, não mês de incidência de doença. Não são pacientes únicos nem confirmações de RAM.']];
const n=sheet('Método e fontes','Como interpretar a conferência',['Item','Explicação'],notes,[30,150]);n.getRange(`B6:B${notes.length+5}`).format.wrapText=true;n.getRange(`A6:B${notes.length+5}`).format.rowHeight=44;
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/planilha_grade_teco.mjs

Planilha grade teco. Processamento ou módulo de apoio. A organização passa por callback, column, table, callback, callback, callback, callback, callback, callback, callback.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\planilha_grade_teco.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ./caminhos_teco.mjs | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| node:fs/promises | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| @oai/artifact-tool | Biblioteca de autoria do ambiente de apresentações/planilhas; precisa ser disponibilizada na máquina de autoria. |


**Entradas.**

- out+'/auditoria/planilha_dados.json' — chamada fs.readFile, linha 17.

**Saídas.**

- out+'/auditoria/planilha_'+names.indexOf(name)+'.png' — chamada fs.writeFile, linha 143.
- out+'/Estatisticas_e_Metodologia_TECO.xlsx' — chamada x.save, linha 145.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/planilha_grade_teco.mjs, linhas 23-31.

```javascript
const sheets=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));

// column
function column(n){let s='';for(;n>0;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}

// table
function table(name,title,headers,rows,widths){

 const s=sheets[name];s.showGridLines=false;s.getRange(`A1:${column(headers.length)}${Math.max(12,rows.length+5)}`).format.font={name:'Arial',size:10};
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/planilha_refino_unidades_teco.mjs

Planilha refino unidades teco. Processamento ou módulo de apoio. A organização passa por col, sheet, callback, callback, callback, callback, callback, callback, callback, callback.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\planilha_refino_unidades_teco.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ./caminhos_teco.mjs | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| node:fs/promises | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| @oai/artifact-tool | Biblioteca de autoria do ambiente de apresentações/planilhas; precisa ser disponibilizada na máquina de autoria. |


**Entradas.**

- O+'/Dados_da_conferencia.json' — chamada fs.readFile, linha 19.
- _cpPath("entrega_final/00_documentacao/Comparacao_kmeans_sensibilidade.json") — chamada fs.readFile, linha 21.
- H+'/planilha_dados.json' — chamada fs.readFile, linha 23.

**Saídas.**

- O+'/previa_'+name.normalize('NFD').replace(/[\u0300-\u036f]/g,'')+'.png' — chamada fs.writeFile, linha 75.
- H+'/Conferencia_Internacoes_Residencia.xlsx' — chamada x.save, linha 77.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/planilha_refino_unidades_teco.mjs, linhas 28-36.

```javascript
function col(n){let s='';while(n){s=String.fromCharCode(65+(n-1)%26)+s;n=Math.floor((n-1)/26)}return s;}

// sheet
function sheet(name,title,headers,rows,widths,tableName){

 const s=w.worksheets.add(name),last=rows.length+5;s.showGridLines=false;s.getRange(`A1:${col(headers.length)}${last}`).format.font={name:'Arial',size:10};s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:14,bold:true,color:navy};s.getRange(`A5:${col(headers.length)}${last}`).values=[headers,...rows];s.getRange(`A5:${col(headers.length)}5`).format={fill:navy,font:{name:'Arial',size:10,color:'#ffffff',bold:true},rowHeight:48,wrapText:true,verticalAlignment:'center',horizontalAlignment:'center'};s.getRange(`A6:${col(headers.length)}${last}`).format.rowHeight=24;s.getRange(`A6:${col(headers.length)}${last}`).format.verticalAlignment='center';widths.forEach((v,i)=>s.getRange(`${col(i+1)}5:${col(i+1)}${last}`).format.columnWidth=v);if(rows.length>20){s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(2)}if(tableName)s.tables.add(`A5:${col(headers.length)}${last}`,true,tableName);return s;

}

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_camadas_nativas.py

Preparar camadas nativas. Processamento ou módulo de apoio. A organização passa por main.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\preparar_camadas_nativas.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'bacias_estudo'] — chamada gpd.read_file, linha 48.
- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'saude_hosp_inativos_candidatos'] — chamada gpd.read_file, linha 57.
- E:/teco/output/05_auditoria_saude/RD_MG_todos_estabelecimentos_2016_2025.csv — chamada pd.read_csv, linha 63.
- E:/teco/output/04_grade_500m/tabelas/sih_todas_causas_mensal.csv — chamada pd.read_csv, linha 64.
- E:/teco/output/04_grade_500m/tabelas/sih_total_mensal.csv — chamada pd.read_csv, linha 64.
- E:/teco/output/04_grade_500m/auditoria/metodo_grade.json — chamada .read_text, linha 77.

**Saídas.**

- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'entradas_censitarias_nativas'] — chamada c.to_file, linha 55.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'saude_todos'] — chamada health.to_file, linha 68.
- E:/teco/output/04_grade_500m/tabelas/estabelecimentos_todos_bacias.csv — chamada .to_csv, linha 69.
- E:/teco/output/04_grade_500m/tabelas/estatisticas_entradas_nativas.csv — chamada .to_csv, linha 74.
- E:/teco/output/04_grade_500m/auditoria/camadas_nativas.json — chamada .write_text, linha 76.
- E:/teco/output/04_grade_500m/auditoria/metodo_grade.json — chamada .write_text, linha 77.

**Campos e chaves lidos.**

- c: ANO_DADO, BACIA, ORIG_GEOM, geometry, setor_id.
- b: geometry, id.
- health: AIH_FILT, AIH_TODAS, CADASTRO, CNES, GRUPO, QA_MUN.
- pp.loc: CNES.
- pp: AIH.

**Campos e chaves gerados.**

- c: ANO_DADO, ORIG_GEOM.
- health: AIH_ANO, AIH_FILT, AIH_TODAS, CADASTRO, CNES, GRUPO, SIH_STATUS.
- old: CADASTRO.
- meta: mapas_entrada, status.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 47-77 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_camadas_nativas.py, linhas 64-70.

```python
 allf=pd.read_csv(O/'tabelas/sih_todas_causas_mensal.csv',sep=';',dtype={'CNES':str});sel=pd.read_csv(O/'tabelas/sih_total_mensal.csv',sep=';',dtype={'CNES':str})
 alltot=allf.groupby('CNES').internacoes.sum();seltot=sel.groupby('CNES').internacoes.sum()
 health['AIH_TODAS']=health.CNES.map(alltot);health['AIH_FILT']=health.CNES.map(seltot);health['AIH_ANO']=health.AIH_FILT/10
 health['SIH_STATUS']=np.where(health.AIH_TODAS.notna(),'Com AIH normais 2016-2025','Sem AIH localizada; não significa ausência de atendimento')
 health['GRUPO']=health.GRUPO.fillna('Hospital / hospital-dia');health.to_file(G,layer='saude_todos',driver='GPKG')
 health.drop(columns='geometry').to_csv(O/'tabelas/estabelecimentos_todos_bacias.csv',index=False,sep=';',encoding='utf-8-sig')
 stats=[]
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_ibge_consolidacao_teco.py

Preparar ibge consolidacao teco. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\preparar_ibge_consolidacao_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/02_avaliacao_espacial/teco_avaliacao.gpkg [camada 'analise_setores'] — chamada gpd.read_file, linha 27.
- {p} — chamada pd.read_csv, linha 31.
- {p} — chamada p.open, linha 35.

**Saídas.**

- E:/teco/tmp/consolidacao_final/IBGE/p.stem_study_sectors.csv — chamada f.to_csv, linha 34.
- E:/teco/tmp/consolidacao_final/IBGE/Proveniencia_IBGE.json — chamada .write_text, linha 40.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_ibge_consolidacao_teco.py, linhas 26-34.

```python
R=Path(_cp_texto('', 'posix'));T=R/'tmp/consolidacao_final';T.mkdir(exist_ok=True);O=T/'IBGE';O.mkdir(exist_ok=True)
ids=set(gpd.read_file(R/'output/02_avaliacao_espacial/teco_avaliacao.gpkg',layer='analise_setores',columns=['setor_id']).setor_id);rows=[]
files=[R/'saneamento_ibge/populacao_basico/Agregados_por_setores_basico_BR.csv',*sorted((R/'saneamento_ibge').glob('Agregados*.csv'))]
for p in files:
 encoding='latin1' if p.name.endswith('_basico_BR.csv') else 'utf-8-sig';chunks=[]
 for a in pd.read_csv(p,sep=';',encoding=encoding,dtype='string',keep_default_na=False,chunksize=15000):
  code='CD_SETOR' if 'CD_SETOR' in a else 'setor';q=a[a[code].isin(ids)]
  if len(q):chunks.append(q)
 f=pd.concat(chunks,ignore_index=True);assert not f[code].duplicated().any();dst=O/(p.stem+'_study_sectors.csv');f.to_csv(dst,sep=';',index=False,encoding='utf-8-sig');h=hashlib.sha256()
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_planilha_8municipios.py

Preparar planilha 8municipios. Processamento ou módulo de apoio. A organização passa por csv.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\preparar_planilha_8municipios.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/tmp/consolidacao_final/entrega_final/04_datasus/01_conjunto_8_municipios/{n} — chamada pd.read_csv, linha 27.

**Saídas.**

- E:/teco/tmp/consolidacao_final/workbook_data.json — chamada .write_text, linha 32.

**Campos e chaves lidos.**

- u: CNES, NOME_TABNET.

**Campos e chaves gerados.**

- m: NRMG.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| csv(n) | 27-27 | lê dados Retorno: pd.read_csv(H / n, sep=';', dtype={'CNES': str, 'MUN_RES': str}).fillna(''). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_planilha_8municipios.py, linhas 28-32.

```python
u=csv('Cadastro_completo_unidades.csv');a=csv('Anual_por_unidade.csv');a=a.merge(u[['CNES','NOME_TABNET']],on='CNES',validate='many_to_one')
t=csv('TabNet_NRMG_anual_8_municipios.csv');official=t.groupby(['CNES','ANO']).AIH_TABNET.sum().rename('NRMG').reset_index();a=a.merge(official,how='left',on=['CNES','ANO']).fillna({'NRMG':0})
m=csv('Resumo_por_municipio.csv');mt=t.groupby('MUN_RES').AIH_TABNET.sum();m['NRMG']=m.MUN_RES.map(mt)
d={'units':u.to_dict('records'),'annual':a.to_dict('records'),'municipalities':m.to_dict('records'),'monthly':csv('Conjunto_mensal_por_municipio.csv').to_dict('records')}
(R/'tmp/consolidacao_final/workbook_data.json').write_text(json.dumps(d,ensure_ascii=False,default=int),encoding='utf8')
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_planilha_grade.py

Preparar planilha grade. Processamento ou módulo de apoio. A organização passa por clean, main.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\preparar_planilha_grade.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/04_grade_500m/tabelas/{n} — chamada pd.read_csv, linha 43.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'bacias_estudo'] — chamada gpd.read_file, linha 44.
- E:/teco/output/04_grade_500m/tabelas/sih_total_mensal.csv — chamada pd.read_csv, linha 44.
- E:/teco/output/04_grade_500m/tabelas/sih_total_anual.csv — chamada pd.read_csv, linha 44.
- E:/teco/output/04_grade_500m/filtro_cid10.csv — chamada pd.read_csv, linha 44.
- E:/teco/output/04_grade_500m/tabelas/cobertura_rd_unidades.csv — chamada pd.read_csv, linha 45.
- E:/teco/output/04_grade_500m/auditoria/metodo_grade.json — chamada .read_text, linha 52.
- E:/teco/output/04_grade_500m/tabelas/estabelecimentos_todos_bacias.csv — chamada pd.read_csv, linha 57.

**Saídas.**

- Argumento fornecido pelo chamador — chamada f.to_json, linha 40.
- E:/teco/output/04_grade_500m/auditoria/planilha_dados.json — chamada .write_text, linha 62.

**Campos e chaves lidos.**

- units: AIH_2016_2025, CNES, NOME, STATUS, bacia, cadastro.
- units_native: AIH_ANO, AIH_FILT, AIH_TODAS, BACIA, CADASTRO, CNES, NOME, SIH_STATUS.
- payload: dicionario, fontes, notas.

**Campos e chaves gerados.**

- stats_grade: suporte.
- payload: estatisticas, unidades.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| clean(f) | 40-40 | grava produtos Retorno: json.loads(f.to_json(orient='records', force_ascii=False)). |
| main() | 42-62 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_planilha_grade.py, linhas 46-52.

```python
 for row in b.itertuples():
  q=a[a.BACIA==row.id];summary.append({'bacia':row.id,'area_km2':row.geometry.area/1e6,'vizinhas':len(q),'elegiveis':int(q.K_S0.gt(0).sum()),'sem_classe':int(q.K_S0.eq(0).sum()),'classe1':int(q.F_S0.eq(1).sum()),'classe2':int(q.F_S0.eq(2).sum()),'classe3':int(q.F_S0.eq(3).sum()),'classe4':int(q.F_S0.eq(4).sum()),'classe5':int(q.F_S0.eq(5).sum())})
 columns=['GRID_ID','BACIA','POP_DENS','SEM_REDE','AIH_LOCAL','N_POP_DENS','N_SEM_REDE','N_AIH_LOCAL','I_S0','F_S0','K_S0','EST_ESG','COB_ESG','AREA_KM2','I_S1','I_S2','I_S3','I_S4']
 dictionary=[('POP_DENS','Habitantes/km²','População censitária rateada por interseção de área no círculo, dividida pela área recortada do círculo.','2022','Fonte; normalização log1p e min-max.'),('SEM_REDE','% de domicílios','Média ponderada pelos domicílios, usando ausência de rede. Inclui soluções individuais; não equivale a esgoto sem tratamento.','2022','Fonte; lacunas analíticas sinalizadas em EST_ESG.'),('AIH_LOCAL','Internações/ano','Média 2016-2025 das AIH normais de hospitais dentro da vizinhança. Não representa moradores atendidos.','2016-2025','Proxy LOCAL provisório; todas as causas até seleção.'),('URB_PCT','% de área','Proporção de pixels válidos de classe urbanizada (24) na vizinhança.','2025 informado','Condicionante; não somado ao índice de fontes.'),('HIPS_M','m','Elevação média dos pixels válidos.','Copernicus GLO-30','Condicionante físico.'),('DECL_PCT','%','Declividade média. Classes Embrapa mantidas no raster.','Copernicus GLO-30','Condicionante; maior declividade não significa mais emissão.'),('DIST_KM','km','Distância superficial D8 até alguma margem do reservatório.','Relevo estático','Não inclui caminho dentro do lago.'),('VIAS_KM','km','Comprimento de vias na vizinhança; hierarquia cadastral do insumo.','Cadastro fornecido','Contexto; ruas não foram impostas como canais.'),('HIDRO_KM','km','Comprimento de cursos hídricos na vizinhança.','Cadastro fornecido','Conectividade; conferir canalização/galerias.'),('N_*','0-1','Valor transformado/normalizado, com limites fixos entre cenários.','Derivado','Normalização das entradas não implica inclusão de todas no índice.'),('I_S0...S4','0-100','Média ponderada de N_POP_DENS, N_SEM_REDE e N_AIH_LOCAL.','Derivado','Potencial relativo; não probabilidade, carga ou risco clínico.'),('F_S0...S4','1-5','Faixas fixas de20 pontos do escore, de muito baixo a muito alto.','Derivado','Relativas e exploratórias, não limites sanitários.'),('K_S0...S4','Identificador','Perfis k-means da matriz multivariada normalizada ponderada.','Derivado','Grupo1 não é automaticamente menor risco que grupo2.'),('MORAN','HH/LL/HL/LH/NS/ND/ISO','Moran local do escore S0, Queen, 999 permutações e FDR5%.','Derivado','Compartilhamento de círculos induz parte da suavização espacial.'),('EST_ESG','% de domicílios','Fração do denominador com percentual de rede estimado na matriz analítica.','Derivado','Não altera o dado original do IBGE.'),('COB_ESG','% de domicílios','Fração com dado de rede observado. Moran usa cobertura >=95%.','Derivado','Sem informação não é ausência de saneamento.')]
 sources=[('IBGE Censo2022','https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html','População e esgotamento; sigilos preservados nas camadas originais.'),('SIH-RD oficial','ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/','120 arquivos RDMG1601 a RDMG2512. IDENT1, diagnóstico principal.'),('Tabelas oficiais SIH','ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Auxiliar/TAB_SIH.zip','Descrições CID-10; versões diferentes podem ter códigos sem descrição.'),('TabNet morbidade MG','https://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/niMG.def','Conferência agregada por hospital e mês de processamento.'),('CNES dados abertos','https://apidadosabertos.saude.gov.br/cnes/estabelecimentos','Cadastro atual de localização, não reconstrução de dez anos.'),('PBH abrangência','https://dados.pbh.gov.br/dataset/area-de-abrangencia-saude','Base identificada; download automático bloqueado HTTP403 nesta coleta.'),('Contagem abrangência','https://portal.contagem.mg.gov.br/secretaria-de-saude/','Consulta por logradouro publicada no PowerBI; sem arquivo vetorial recuperado.'),('WHO patógenos prioritários2024','https://www.who.int/publications/i/item/9789240093461/','Orienta revisão microbiológica; CID não confirma resistência.'),('Copernicus GLO-30','https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM','MDE local fornecido; inclui vegetação/construções, não galerias.'),('GRASS D8','https://grass.osgeo.org/grass-stable/manuals/r.watershed.html','Direção topográfica; não modelo de dispersão de genes.')]
 notes=[('Unidade espacial','Círculos de500m em centros triangulares, apresentados por hexágonos de raio externo500m. Círculos se sobrepõem; não somar suas populações como total da bacia.'),('Dado oficial e resolução','A grade não cria população medida em500m. A população e os domicílios são rateados por área dos setores de origem.'),('Cenário de origem dos pacientes','AIH_ORIG está pendente. CEPs observados foram agregados, mas não geocodificados com precisão suficiente. O índice atual usa somente atividade hospitalar LOCAL como hipótese separada.'),('Atualização dos pesos','Alterar os pesos nesta planilha recalcula os escores na aba Grade. K-means, Moran, mapas e relatório só mudam após reprocessamento em Python.'),('Filtro de causas','Marque incluir=1 na aba Filtro CID10. Execute avaliar_saude_grade.py --planilha caminho.xlsx para importar a seleção. Nenhum grupo sugerido é selecionado automaticamente.'),('Meses críticos','Os gráficos principais usam competência de processamento. Não confundir mês de faturamento com mês de adoecimento. O CSV por mês real de internação permite outra leitura, com bordas da janela de processamento.'),('Sensibilidade','S0 pesos1/1/1; S1 1/1/3; S2 1/3/1; S3 3/1/1; S4 1/1/0. Não são cenários de emissão ou prevalência.'),('K-means','Usa as três colunas normalizadas, multiplicadas pela raiz dos pesos; não usa apenas o escore final. Escolhe k2-6 pela silhouette; compara cenários também com k fixo.'),('Moran','Usa o escore por vizinhança e as relações espaciais dos hexágonos. HH não demonstra descarga nem rota. A sobreposição das vizinhanças suaviza valores, exigindo cautela inferencial.'),('Conectividade','Média de índice*área a montante dividida pela área válida, ao longo do D8. Não contém vazão, chuva, diluição, decaimento ou concentração de genes.'),('CEPs e hospitais','Arquivo sih_ceps_origem_2016_2025.csv descreve origens observadas de internações. Contagens menores que5 foram suprimidas; não se deve criar círculo atendido a partir do CEP da unidade.'),('Cobertura SIH','734 cadastros localizados; somente três unidades retornaram AIH normais na janela. Unidades sem SIH podem prestar atendimento ambulatorial. SIA/e-SUS são bases diferentes.')]
 payload={'resumo':summary,'grade':clean(a[columns]),'estatisticas':clean(read('estatisticas_camadas.csv')),'cenarios':clean(s),'unidades':clean(units[['CNES','NOME','bacia','cadastro','AIH_2016_2025','STATUS']]),'mensal':clean(monthly),'anual':clean(annual),'filtro':clean(filt),'dicionario':dictionary,'fontes':sources,'notas':notes,'meta':json.loads((O/'auditoria/metodo_grade.json').read_text('utf8'))}
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_refino_sih_teco.py

Preparar refino sih teco. Processamento ou módulo de apoio. A organização passa por save, jsonready, main, summarize.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\preparar_refino_sih_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/05_auditoria_saude/refino/Producao_hospitalar_mensal_niveis.csv — chamada pd.read_csv, linha 60.
- E:/teco/output/05_auditoria_saude/refino/Residentes4_mensal_niveis.csv — chamada pd.read_csv, linha 60.
- E:/teco/output/05_auditoria_saude/Estabelecimentos_confirmados_residencia.csv — chamada pd.read_csv, linha 60.
- E:/teco/output/05_auditoria_saude/refino/TabNet_producao_MG_anual.csv — chamada pd.read_csv, linha 60.
- E:/teco/output/05_auditoria_saude/refino/Auditoria_releitura.json — chamada .read_text, linha 60.
- E:/teco/output/05_auditoria_saude/NRMG_internacoes_por_residencia_anuais.csv — chamada pd.read_csv, linha 76.
- E:/teco/output/05_auditoria_saude/refino/Conferencia_producao_TabNet_RD.csv — chamada pd.read_csv, linha 85.
- E:/teco/output/04_grade_500m/teco_grade_500m.gpkg [camada 'saude_todos'] — chamada gpd.read_file, linha 90.

**Saídas.**

- E:/teco/output/05_auditoria_saude/refino/{name} — chamada frame.to_csv, linha 53.
- units[unitcols] — chamada save, linha 73.
- inside[unitcols] — chamada save, linha 74.
- summarize(a, ['CNES'], 'PROD').merge(tab[['CNES', 'NOME_TABNET']].drop_duplicates('CNES'), on='CNES', validate='one_to_one') — chamada save, linha 75.
- annual[annual.CNES.isin(units.CNES)].copy() — chamada save, linha 76.
- monthly[monthly.CNES.isin(units.CNES)].copy() — chamada save, linha 77.
- pd.DataFrame(distribution) — chamada save, linha 81.
- E:/teco/output/05_auditoria_saude/refino/Dados_da_conferencia.json — chamada .write_text, linha 88.

**Campos e chaves lidos.**

- p: Sem dicionário.
- years: max, min.
- tab: CNES, NOME_TABNET.
- annual: RES_A, RES_AB, RES_B, RES_C, RES_SEM_DIC, RES_TABNET, RES_TOTAL.
- a: AIH, NIVEL.
- units.loc: AIH_NRMG.
- j: repeticoes_NAIH_no_mes.
- meta: meses, sem_dicionario.
- a.loc: AIH.

**Campos e chaves gerados.**

- units: DIF_RES_RD_NRMG, FREQ_RES, N_ANOS_RES, N_MESES_PROD, N_MESES_RES, PRIMEIRO_ANO_RES, PROD_AB_PCT, RES_AB_PCT, RES_FRAC_PROD, ULTIMO_ANO_RES.
- annual: NOME.
- metrics: AIH_AB_MG, aviso_18.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| save(frame, name) | 53-53 | grava produtos |
| jsonready(value) | 56-56 | grava produtos Retorno: json.loads(json.dumps(value, default=lambda v: int(v) if isinstance(v, np.integer) else float(v) if isinstance(v, np.floating) else str(v), ensure_ascii=False)). |
| main() | 59-90 | lê dados; grava produtos Retorno: result.reset_index(). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_refino_sih_teco.py, linhas 64-70.

```python
   if level not in p:p[level]=0
  result=pd.DataFrame({prefix+'_TOTAL':p.sum(axis=1),prefix+'_A':p.A,prefix+'_B':p.B,prefix+'_AB':p.A+p.B,prefix+'_C':p.C,prefix+'_SEM_DIC':p['Sem dicionário']});return result.reset_index()
 allunit=summarize(a,['CNES'],'PROD');resunit=summarize(b,['CNES'],'RES');units=h.merge(allunit,on='CNES',validate='one_to_one').merge(resunit,on='CNES',validate='one_to_one');units['RES_AB_PCT']=100*units.RES_AB/units.AIH_NRMG;units['PROD_AB_PCT']=100*units.PROD_AB/units.PROD_TOTAL;units['RES_FRAC_PROD']=100*units.AIH_NRMG/units.PROD_TOTAL;units['N_ANOS_RES']=units.CNES.map(b.groupby(['CNES','ANO']).AIH.sum().gt(0).groupby('CNES').sum());units['N_MESES_RES']=units.CNES.map(b.groupby(['CNES','ANO','MES']).AIH.sum().gt(0).groupby('CNES').sum());units['N_MESES_PROD']=units.CNES.map(a.groupby(['CNES','ANO','MES']).AIH.sum().gt(0).groupby('CNES').sum())
 years=b.groupby('CNES').ANO.agg(['min','max']);units['PRIMEIRO_ANO_RES']=units.CNES.map(years['min']);units['ULTIMO_ANO_RES']=units.CNES.map(years['max']);units['FREQ_RES']=pd.cut(units.AIH_NRMG,bins=[0,10,100,1000,np.inf],labels=['1-10 no decênio','11-100 no decênio','101-1.000 no decênio','Mais de 1.000 no decênio']).astype(str)
 units['DIF_RES_RD_NRMG']=units.RES_TOTAL-units.AIH_NRMG
 assert int(units.RES_AB.sum())==274254 and int(units.RES_TOTAL.sum())==2038504 and int(units.AIH_NRMG.sum())==2038486
 assert units.RES_A.equals(units.AIH_A) and units.RES_B.equals(units.AIH_B)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_saneamento_ibge.py

Preparar saneamento ibge. Processamento ou módulo de apoio. A organização passa por sha, polygon, filtered_csv, styles, shapefile, archive_existing, main, write_readme, preview.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\preparar_saneamento_ibge.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyogrio | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shapely | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.sax.saxutils | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {p} — chamada p.open, linha 138.
- {path} — chamada pd.read_csv, linha 152.
- E:/teco/saneamento_ibge/resultados/shapefiles/{name}.shp — chamada gpd.read_file, linha 190.
- E:/teco/sub_bacia/shapefiles_v6_20261109_141015/sub_bacias_exclusivas.shp — chamada gpd.read_file, linha 211.
- E:/teco/saneamento_ibge/malha_setores_2022/MG_setores_CD2022.gpkg — chamada gpd.read_file, linha 217.

**Saídas.**

- path.with_suffix('.qml') — chamada .write_text, linha 179.
- E:/teco/saneamento_ibge/resultados/shapefiles/{name}.shp — chamada g.to_file, linha 188.
- E:/teco/descontinuado/dt.datetime.now().strftime('%Y%m%d_%H%M%S_saneamento_ibge')/manifesto_arquivamento.json — chamada .write_text, linha 206.
- Argumento fornecido pelo chamador — chamada .to_json, linha 242.
- E:/teco/saneamento_ibge/resultados/saneamento_teco.gpkg [camada name] — chamada data.to_file, linha 279.
- E:/teco/saneamento_ibge/resultados/saneamento_teco.gpkg [camada 'lacunas_malha'] — chamada gap_gdf.to_file, linha 281.
- E:/teco/saneamento_ibge/resultados/valores_originais_selecionados.csv — chamada original.to_csv, linha 282.
- E:/teco/saneamento_ibge/resultados/atributos_setores_bacias.csv — chamada .to_csv, linha 283.
- E:/teco/saneamento_ibge/resultados/resumo_bacias.csv — chamada .to_csv, linha 284.
- E:/teco/saneamento_ibge/resultados/municipios_interceptados.csv — chamada .to_csv, linha 285.
- E:/teco/saneamento_ibge/resultados/dicionario_campos.csv — chamada .to_csv, linha 288.
- E:/teco/saneamento_ibge/resultados/auditoria_saneamento.json — chamada .write_text, linha 293.
- Mais 3 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- a: created_at, intersection_count, sector_count, setor, summary.
- out: setor.
- check: setor_id.
- g: dom_set, setor_id.
- bas: bas_id.
- geom: setor_id.
- raw: V00001, V00309, V00310, V00311, V00313, V00314, _merge, dif_soma, dom_set, nred_set, pct_rede, rede_set, soma8.
- geo: V00001, bas_id, dpo_malha, mun_cod, mun_nome, n_ausente, n_sigilo, pct_rdir, pct_rede, pop_malha, qual_dado, setor_id, sig_vars.
- clip: V00309, bas_id, dom_a_est, frac_area, nrd_a_est, rec_km2, red_a_est, set_km2, setor_id.
- v: bas_id, bas_nome.
- c: dom_a_est, dom_set, pct_rdir, pct_rede.
- c.loc: dir_a_est, dom_a_est, nrd_a_est, red_a_est.
- clip.loc: dom_a_est, nrd_a_est, red_a_est.
- geo.loc: setor_id.
- x: bas_id, bas_nome, cov_dir, dom_a_est, gap_m2, n_setores, pct_rdir.
- audit: qualities, summary.
- b: bas_id.
- bg: bas_id.

**Campos e chaves gerados.**

- geom: setor_id.
- raw: dif_soma, dom_set, n_ausente, n_sigilo, nred_set, pct_fossa, pct_nrede, pct_rdir, pct_rede, pct_vrio, qual_dado, rede_set, sig_vars, soma8.
- geo: ano, n_ausente, n_bacias, n_sigilo, set_km2, sig_vars, tot_origem.
- clip: dir_a_est, frac_area, n_bacias, rec_km2.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| sha(p) | 136-140 | Chamadas efetivas: hashlib.sha256, h.hexdigest, p.open, iter, h.update, f.read Retorno: h.hexdigest(). |
| polygon(g) | 143-147 | Chamadas efetivas: make_valid, unary_union Retorno: unary_union([v for v in g.geoms if v.geom_type in ['Polygon', 'MultiPolygon']]), g. |
| filtered_csv(path, columns, ids) | 150-159 | lê dados Retorno: out. |
| styles(path, columns, title) | 162-179 | grava produtos |
| shapefile(g, name, title) | 182-197 | lê dados; grava produtos Retorno: path. |
| archive_existing() | 200-207 | grava produtos |
| main() | 210-299 | lê dados; grava produtos |
| write_readme(a) | 302-334 | grava produtos |
| preview(clip, bas, summary) | 337-365 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_saneamento_ibge.py, linhas 213-219.

```python
    bas.geometry=bas.geometry.map(polygon)
    overlap=float(sum(bas.geometry.iloc[i].intersection(bas.geometry.iloc[j]).area for i in range(3) for j in range(i)))
    assert overlap<=1.01,('Sobreposição de bacias superior a 1m²',overlap)
    union=bas.geometry.union_all();bb=bas.to_crs(4674).total_bounds
    geom=gpd.read_file(MESH,bbox=tuple(bb),columns=['CD_SETOR','CD_MUN','NM_MUN','SITUACAO','v0001','v0007']).to_crs(CRS)
    invalid=int((~geom.is_valid).sum());geom.geometry=geom.geometry.map(polygon)
    geom=geom[geom.intersects(union)].copy();geom=geom[geom.intersection(union).area>0.01].copy()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preservar_resolucao_pdf_teco.py

Preservar resolucao pdf teco. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\preservar_resolucao_pdf_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pypdf | Leitura, montagem e inspeção de PDFs; não substitui a conferência visual das páginas. |
| pypdf.generic | Leitura, montagem e inspeção de PDFs; não substitui a conferência visual das páginas. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zlib | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

- E:/teco/entrega_final/00_documentacao/Relatorio_figuras_e_tabelas.json — chamada .read_text, linha 34.
- E:/teco/entrega_final/f['source'] — chamada Image.open, linha 38.
- E:/teco/entrega_final/f['source'] — chamada Image.open, linha 48.
- E:/teco/entrega_final/catalog['figures'][record['figure'] - 1]['source'] — chamada Image.open, linha 61.

**Saídas.**

- E:/teco/tmp/relatorio_didatico/Relatorio_TECO_full_resolution.pdf — chamada temp.open, linha 57.
- E:/teco/entrega_final/00_documentacao/Qualidade_imagens_relatorio.json — chamada .write_text, linha 65.

**Campos e chaves lidos.**

- catalog: figures.
- f: number, slug, source.
- record: figure, final_pixels.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preservar_resolucao_pdf_teco.py, linhas 43-49.

```python
assert len(observed)==len(originals)==len(catalog['figures'])
cost=np.array([[np.mean((a-b)**2) for b in originals] for _,_,a in observed]);matches=cost.argmin(1);assert len(set(matches))==len(originals),(matches.tolist(),cost.min(1).tolist());assert cost.min(1).max()<120,cost.min(1)
audit=[]
for row,((page_no,img,_),match) in enumerate(zip(observed,matches)):
 f=catalog['figures'][int(match)];p=F/f['source']
 with Image.open(p) as im:
  if im.mode=='RGBA':assert im.getextrema()[3]==(255,255)
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/projeto_integracao_qgis.py

Estilos e projeto QGIS portável para a integração territorial TECO.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\projeto_integracao_qgis.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtGui | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/output/01_integracao_territorial/dicionario_campos.csv — chamada .open, linha 41.
- setores_integrados_bacias — chamada load, linha 95.
- setores_integrados_inteiros — chamada load, linha 91.
- rede_bh_bacias — chamada load, linha 96.
- None — chamada load, linha 98.
- resumo_integrado_bacias — chamada load, linha 101.
- ete_bacias — chamada load, linha 105.

**Saídas.**

- E:/teco/output/01_integracao_territorial/conferencia_qgis.json — chamada .write_text, linha 117.
- E:/teco/output/01_integracao_territorial/Integracao_territorial_TECO.zip — chamada zipfile.ZipFile, linha 119.

**Campos e chaves lidos.**

- r: campo, descricao.

**Campos e chaves gerados.**

- os.environ: QT_QPA_PLATFORM.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| load(name, title, group, visible=False, gpkg_layer=None) | 47-53 | Chamadas efetivas: QgsVectorLayer, layer.isValid, enumerate, layer.setDisplayExpression, p.addMapLayer, group.addLayer, node.setItemVisibilityChecked, str Retorno: layer. |
| fill(color) | 56-56 | Chamadas efetivas: QgsFillSymbol.createSimple Retorno: QgsFillSymbol.createSimple({'color': color, 'outline_color': '#50636c', 'outline_width': '0.10', 'outline_width_unit': 'MM'}). |
| rules(layer, items, kind='fill') | 59-75 | Chamadas efetivas: QgsRuleBasedRenderer, renderer.rootRule, root.removeChildAt, layer.setRenderer, QgsExpressionContext, ctx.appendScopes, layer.getFeatures, CHECK.append |
| bins(field, edges, labels, colors, zero=False) | 78-85 | Chamadas efetivas: enumerate, items.append, zip Retorno: items. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/projeto_integracao_qgis.py, linhas 47-55.

```python
def load(name,title,group,visible=False,gpkg_layer=None):
    source=str(O/'integracao_territorial_teco.gpkg')+'|layername='+gpkg_layer if gpkg_layer else str(S/(name+'.shp'))
    layer=QgsVectorLayer(source,title,'ogr');assert layer.isValid(),source
    for i,f in enumerate(layer.fields()):
        if f.name() in DESC:layer.setFieldAlias(i,DESC[f.name()])
    layer.setDisplayExpression('"setor_id"' if layer.fields().indexFromName('setor_id')>=0 else '"bas_nome"')
    p.addMapLayer(layer,False);node=group.addLayer(layer);node.setItemVisibilityChecked(visible);return layer

# Fill
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/promover_consolidacao_teco.py

Promover consolidacao teco. Consolidação/migração: conferir pré-condições. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Consolidação/migração: conferir pré-condições. **Fonte inspecionada.** E:\teco\codigo\promover_consolidacao_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| idioma_cartografico_teco | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/tmp/consolidacao_final/archive_path.txt — chamada .read_text, linha 31.
- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 35.
- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/Dicionario_dos_campos.csv — chamada pd.read_csv, linha 36.

**Saídas.**

- (F / rel).parent/dicionario_campos.csv — chamada group.to_csv, linha 43.
- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/Dicionario_dos_campos.csv — chamada di.to_csv, linha 44.
- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/Field_dictionary_EN.csv — chamada .to_csv, linha 45.
- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/manifesto.json — chamada .write_text, linha 51.

**Campos e chaves lidos.**

- m: health_all_municipalities, saude.
- di: at.

**Campos e chaves gerados.**

- m: saude, saude_referencia_4_municipios.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/promover_consolidacao_teco.py, linhas 30-38.

```python
from idioma_cartografico_teco import field_alias
R=Path(_cp_texto('', 'posix'));T=R/'tmp/consolidacao_final';F=T/'entrega_final';D=F/'00_documentacao';A=Path((T/'archive_path.txt').read_text('utf8').strip())
assert F.resolve().is_relative_to(R.resolve()) and A.resolve().is_relative_to((R/'descontinuado').resolve())
assert (F/'04_datasus/01_conjunto_8_municipios/Internacoes_8_municipios.xlsx').exists()
assert len(list(F.rglob('*.shp')))==50
m=json.loads((D/'manifesto.json').read_text('utf8'));m['saude_referencia_4_municipios']=m['saude'];m['saude']=m['health_all_municipalities']
di=pd.read_csv(D/'Dicionario_dos_campos.csv',sep=';')
for i,row in di.iterrows():
 if '09_saude_residencia' in row.arquivo:
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/qa_relatorio_teco.py

Qa relatorio teco. Documentação/apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\qa_relatorio_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pypdf | Leitura, montagem e inspeção de PDFs; não substitui a conferência visual das páginas. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada Image.open, linha 37.

**Saídas.**

- E:/teco/tmp/relatorio_detalhado/qa_texto_paginas.json — chamada .write_text, linha 32.
- E:/teco/tmp/relatorio_detalhado/contato_{j // 8 + 1}.png — chamada canvas.save, linha 38.

**Campos e chaves lidos.**

- r: pagina.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/qa_relatorio_teco.py, linhas 36-39.

```python
 for k,path in enumerate(images[j:j+8]):
  im=Image.open(path);im.thumbnail((432,590));x=10+(k%4)*450;y=25+(k//4)*635;canvas.paste(im,(x,y));d.text((x,y-17),path.stem,fill='black')
 canvas.save(T/f'contato_{j//8+1}.png')
print('Páginas',len(p.pages),'imagens',len(images),'tabelas',[r['pagina'] for r in rows if 'Tabela ' in p.pages[r['pagina']-1].extract_text()])
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/qgis_consolidacao_auditada_teco.py

Qgis consolidacao auditada teco. Cartografia/apresentação. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\qgis_consolidacao_auditada_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| idioma_cartografico_teco | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtCore | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.PyQt.QtGui | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 38.

**Saídas.**

- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/manifesto.json — chamada .write_text, linha 111.
- E:/teco/tmp/consolidacao_final/entrega_final/00_documentacao/Conferencia_QGIS_final.json — chamada .write_text, linha 112.

**Campos e chaves lidos.**

- m: mapas, old_to_new_paths, vetores.
- r: arquivo.
- record: arquivo, titulo.
- fields: bacia.

**Campos e chaves gerados.**

- os.environ: QT_QPA_FONTDIR, QT_QPA_PLATFORM.
- record: titulo.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/qgis_consolidacao_auditada_teco.py, linhas 37-45.

```python
QLocale.setDefault(QLocale('en_US'));app.setFont(QFont('Arial',9))
m=json.loads((D/'manifesto.json').read_text('utf8'));mapping=m['old_to_new_paths'];p=QgsProject.instance();assert p.read(str(F/'TECO_Consolidado.qgz'))
records={r['arquivo']:r for r in m['vetores']};changed=[]
for l in list(p.mapLayers().values()):
 src=l.source();base=src.split('|')[0].replace('\\','/');marker='/entrega_final/'
 if marker not in base:raise RuntimeError('Provider outside delivery: '+src)
 rel=base.split(marker,1)[1];new=mapping.get(rel,rel);target=F/new;assert target.is_file(),target
 if isinstance(l,QgsVectorLayer):
  renderer=l.renderer().clone();subset=l.subsetString();l.setDataSource(str(target),l.name(),'ogr');l.setRenderer(renderer)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/qgis_entrega_final.py

Cria cópia portátil do projeto, preservando encartes e identificadores dos layouts.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\qgis_entrega_final.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtGui | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 39.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/Validacao_QGIS.json — chamada .write_text, linha 127.

**Campos e chaves lidos.**

- r: arquivo, fonte.
- m: mapas, rasters, vetores.
- row: arquivo, titulo.
- styles: kmeans, moran, score.

**Campos e chaves gerados.**

- os.environ: QT_QPA_FONTDIR, QT_QPA_PLATFORM.
- styles: kmeans, moran, score.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| vector_path(rel) | 46-46 | Chamadas efetivas: str Retorno: str(F / rel). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/qgis_entrega_final.py, linhas 46-54.

```python
def vector_path(rel):return str(F/rel)
mapping={'grade_resultados':'02_saidas/01_matriz_completa/matriz_resultados.shp','influencia_500m':'02_saidas/08_vizinhancas_500m/vizinhancas.shp','centros_500m':'02_saidas/07_centros_grade/centros.shp','bacias_estudo':'01_entradas/01_bacias/bacias.shp','hidro_contexto':'01_entradas/05_hidrografia/hidrografia.shp','saude_todos':'01_entradas/08_saude_local/saude_local.shp','rede_internacoes_residentes':'01_entradas/09_saude_residencia/saude_residencia.shp'}
rasters={str(Path(r['fonte'])).replace('\\','/').lower():str(F/r['arquivo']) for r in m['rasters']}
done=[]
for layer in list(p.mapLayers().values()):
 old=layer.source().replace('\\','/');lower=old.lower();target=None;subset=layer.subsetString() if isinstance(layer,QgsVectorLayer) else ''
 if layer.id() in keep:
  if '|layername=entradas_censitarias_nativas' in lower:
   target=vector_path('01_entradas/04_esgotamento/esgotamento.shp' if any(w in layer.name() for w in ['rede','Destinação']) else '01_entradas/03_populacao/populacao.shp')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/qgis_grade_teco.py

Camadas e layouts nativos triplos da grade TECO, sem setores IBGE como fundo.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\qgis_grade_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtCore | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.PyQt.QtGui | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| warnings | Controle de avisos de bibliotecas sem alterar a definição do estimador. |


**Entradas.**

- E:/teco/config/encartes_teco.json — chamada .read_text, linha 46.
- {title} [camada layer] — chamada load, linha 72.
- S{i}  /  potencial relativo exploratório — chamada load, linha 78.
- E:/teco/output/04_grade_500m/auditoria/metodo_grade.json — chamada .read_text, linha 80.
- K-means S{i}  /  perfis de atributos — chamada load, linha 82.
- Moran local  /  Queen e FDR5% — chamada load, linha 83.
- Centros das vizinhanças [camada 'centros_500m'] — chamada load, linha 84.
- Círculos de cálculo  /  raio500m [camada 'influencia_500m'] — chamada load, linha 85.
- Hospitais com internações confirmadas  /  dentro das bacias [camada 'saude_todos'] — chamada load, linha 86.
- Reservatório  /  {key} — chamada load, linha 91.
- Limites das bacias [camada 'bacias_estudo'] — chamada load, linha 92.
- Cursos hídricos [camada 'hidro_contexto'] — chamada load, linha 93.
- Mais 1 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/teco/output/04_grade_500m/auditoria/qgis_grade.json — chamada .write_text, linha 143.

**Campos e chaves lidos.**

- meta: k_base.
- f: id.
- groups: 07 Suporte aos layouts.

**Campos e chaves gerados.**

- os.environ: QT_QPA_FONTDIR, QT_QPA_PLATFORM.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| load(title, sub, layer='grade_resultados', source=None, visible=False) | 61-62 | Chamadas efetivas: QgsVectorLayer, l.isValid, p.addMapLayer, .setItemVisibilityChecked, created.append, .addLayer, str Retorno: l. |
| rules(l, entries) | 65-69 | Chamadas efetivas: QgsRuleBasedRenderer, renderer.rootRule, rt.removeChildAt, l.setRenderer, QgsFillSymbol.createSimple, rt.appendChild, QgsRuleBasedRenderer.Rule |
| continuous(title, field, sub, unit, layer='grade_resultados') | 71-76 | lê dados Retorno: l. |
| subset(layer, key, field) | 100-106 | Chamadas efetivas: layer.id, QgsVectorLayer, local.setRenderer, local.isValid, local.source, p.addMapLayer, .setItemVisibilityChecked, layer.source Retorno: support[token]. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/qgis_grade_teco.py, linhas 61-69.

```python
def load(title,sub,layer='grade_resultados',source=None,visible=False):
 l=QgsVectorLayer(source or str(G)+'|layername='+layer,title,'ogr');assert l.isValid(),title;p.addMapLayer(l,False);groups[sub].addLayer(l).setItemVisibilityChecked(visible);created.append(l);return l
COLORS=['#b7dce6','#8bbca9','#e0ce81','#d99965','#b94d5c'];PROFILE=['#7198ad','#b8c99b','#dfb77b','#bc7d7d','#8c7ba4','#55a28e']
# Rules
def rules(l,entries):
 renderer=QgsRuleBasedRenderer(QgsFillSymbol.createSimple({'color':'#dddddd'}));rt=renderer.rootRule();rt.removeChildAt(0)
 for expr,label,col in entries:
  sym=QgsFillSymbol.createSimple({'color':col,'outline_color':'#71888b','outline_width':'0.055'});rt.appendChild(QgsRuleBasedRenderer.Rule(sym,0,0,expr,label))
 l.setRenderer(renderer)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/qgis_hipsometria_teco.py

Qgis hipsometria teco. Cartografia/apresentação. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\qgis_hipsometria_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtGui | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/config/paleta_hipsometria.json — chamada .read_text, linha 28.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/Atualizacao_hipsometria.json — chamada .write_text, linha 43.

**Campos e chaves lidos.**

- config: max_m, min_m, paradas.
- s: cor, posicao.

**Campos e chaves gerados.**

- os.environ: QT_QPA_FONTDIR, QT_QPA_PLATFORM.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/qgis_hipsometria_teco.py, linhas 27-35.

```python
from qgis.PyQt.QtGui import QColor
R=Path(_cp_texto('', 'posix'));F=R/'entrega_final';O=R/'output/04_grade_500m';config=json.loads((R/'config/paleta_hipsometria.json').read_text('utf8'));lo=config['min_m'];hi=config['max_m']
app=QgsApplication([],False);app.initQgis();p=QgsProject.instance()
statuses=[]
for project in [R/'projeto_teco.qgz',F/'TECO_Consolidado.qgz']:
 assert p.read(str(project));changed=0
 for l in p.mapLayers().values():
  if not isinstance(l,QgsRasterLayer) or not l.source().replace('\\','/').endswith('_hipsometria.tif'):continue
  function=QgsColorRampShader(lo,hi);function.setColorRampType(QgsColorRampShader.Interpolated)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/qgis_idioma_ingles_teco.py

Qgis idioma ingles teco. Cartografia/apresentação. A organização passa por translate_tree, rule.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\qgis_idioma_ingles_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| idioma_cartografico_teco | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtCore | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.PyQt.QtGui | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/English_QGIS_display.json — chamada .write_text, linha 95.

**Campos e chaves lidos.**

- old: count, source.

**Campos e chaves gerados.**

- os.environ: QT_QPA_FONTDIR, QT_QPA_PLATFORM.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| translate_tree(root) | 35-38 | Chamadas efetivas: root.children, node.setName, isinstance, en, translate_tree, node.name |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/qgis_idioma_ingles_teco.py, linhas 35-43.

```python
def translate_tree(root):
 for node in root.children():
  node.setName(en(node.name()))
  if isinstance(node,QgsLayerTreeGroup):translate_tree(node)
for path in [R/'projeto_teco.qgz',F/'TECO_Consolidado.qgz']:
 assert p.read(str(path));initial={l.id():{'source':l.source(),'count':l.featureCount() if isinstance(l,QgsVectorLayer) else None} for l in p.mapLayers().values()}
 for layer in p.mapLayers().values():
  layer.setName(en(layer.name()))
  if isinstance(layer,QgsVectorLayer) and not labels_only:
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/qgis_refino_cartografico_teco.py

Qgis refino cartografico teco. Cartografia/apresentação. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\qgis_refino_cartografico_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtGui | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/config/paleta_hipsometria.json — chamada .read_text, linha 31.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/Atualizacao_hipsometria.json — chamada .write_text, linha 56.

**Campos e chaves lidos.**

- cfg: max_m, min_m, paradas.
- f: id.
- s: cor, posicao.

**Campos e chaves gerados.**

- os.environ: QT_QPA_FONTDIR, QT_QPA_PLATFORM.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/qgis_refino_cartografico_teco.py, linhas 30-38.

```python
for font in ['arial.ttf','arialbd.ttf']:QFontDatabase.addApplicationFont(_cp_externo('fonts_4d9cd6a')+font)
cfg=json.loads((R/'config/paleta_hipsometria.json').read_text('utf8'));lo,hi=cfg['min_m'],cfg['max_m'];project=QgsProject.instance();results=[]
for path in [R/'projeto_teco.qgz',F/'TECO_Consolidado.qgz']:
 assert project.read(str(path));ramp_count=0;maps_count=0
 basin_layer=next(l for l in project.mapLayers().values() if isinstance(l,QgsVectorLayer) and l.name() in ['Limites das bacias','Basin boundaries'])
 feature=next(f for f in basin_layer.getFeatures() if f['id']=='vargem_flores');c=feature.geometry().boundingBox().center();cx=c.x()+600;cy=c.y()-600
 for layer in project.mapLayers().values():
  if isinstance(layer,QgsRasterLayer) and layer.source().replace('\\','/').endswith('_hipsometria.tif'):
   ramp=QgsColorRampShader(lo,hi);ramp.setColorRampType(QgsColorRampShader.Interpolated);ramp.setColorRampItemList([QgsColorRampShader.ColorRampItem(lo+s['posicao']*(hi-lo),QColor(s['cor']),f"{lo+s['posicao']*(hi-lo):.1f} m") for s in cfg['paradas']]);shader=QgsRasterShader(lo,hi);shader.setRasterShaderFunction(ramp);renderer=QgsSingleBandPseudoColorRenderer(layer.dataProvider(),1,shader);renderer.setClassificationMin(lo);renderer.setClassificationMax(hi);layer.setRenderer(renderer);layer.saveNamedStyle(str(Path(layer.source()).with_suffix('.qml')));ramp_count+=1
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/refinar_credibilidade_sih_teco.py

Refinar credibilidade sih teco. Processamento ou módulo de apoio. A organização passa por month, official, main, col.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\refinar_credibilidade_sih_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| filtro_bacteriano_teco | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| requests | Consultas e downloads HTTP; depende de internet e da disponibilidade do provedor. |
| struct | Decodificação binária com tipos, tamanhos e ordem de bytes definidos. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |
| urllib.parse | Requisições e manipulação de endereços de serviços públicos. |


**Entradas.**

- E:/teco/dados_publicos/saude_revisao/CID10_oficial_GO.json — chamada .read_text, linha 57.
- E:/teco/codigo/filtro_bacteriano_teco.py — chamada .read_bytes, linha 58.
- E:/teco/tmp/refino_sih/src.stem.json — chamada cache.read_text, linha 64.
- E:/teco/tmp/refino_sih/src.stem.dbf — chamada dbf.read_bytes, linha 66.
- E:/teco/dados_publicos/saude_grade/rd/RDMG{y % 100}{m}.dbc — chamada src.read_bytes, linha 75.
- E:/teco/dados_publicos/saude/campos_tabnet.json — chamada .read_text, linha 80.
- E:/teco/output/05_auditoria_saude/refino/TabNet_producao_MG_2016_2025.html — chamada path.read_text, linha 83.

**Saídas.**

- E:/teco/tmp/refino_sih/src.stem.json — chamada cache.write_text, linha 76.
- E:/teco/output/05_auditoria_saude/refino/consulta_TabNet_producao.json — chamada .write_text, linha 82.
- E:/teco/output/05_auditoria_saude/refino/TabNet_producao_MG_2016_2025.html — chamada path.write_text, linha 87.
- E:/teco/output/05_auditoria_saude/refino/TabNet_producao_MG_anual.csv — chamada f.to_csv, linha 100.
- E:/teco/output/05_auditoria_saude/refino/Producao_hospitalar_mensal_niveis.csv — chamada a.to_csv, linha 114.
- E:/teco/output/05_auditoria_saude/refino/Residentes4_mensal_niveis.csv — chamada b.to_csv, linha 114.
- E:/teco/output/05_auditoria_saude/refino/Diagnosticos_MG_auditados.csv — chamada .to_csv, linha 115.
- E:/teco/output/05_auditoria_saude/refino/Conferencia_producao_TabNet_RD.csv — chamada cmp.to_csv, linha 117.
- E:/teco/output/05_auditoria_saude/refino/Auditoria_releitura.json — chamada .write_text, linha 120.

**Campos e chaves lidos.**

- i: code, display.
- dic: concept.
- a: AIH, CNES, MUN_RES, NIVEL.
- j: aih_normais, ano, cid, mes, res4, todos.
- fields: Arquivos, Incremento.
- body: Arquivos.
- f.loc: AIH_TABNET.
- f: ANO.
- x: ano, mes.
- cmp: AIH_RD, AIH_TABNET.
- a.loc: AIH.

**Campos e chaves gerados.**

- cmp: DIF_RD_TABNET, DIF_RESTANTE.
- audit: combinacoes_divergentes_sem_ajuste, diferenca_final_sem_ajuste.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| month(ym) | 61-76 | lê dados; grava produtos Retorno: j, np.char.strip(np.ndarray(n, dtype=f'S{length}', buffer=buf, offset=head + start, strides=(rec,))). |
| official() | 79-100 | lê dados; grava produtos Retorno: f. |
| main() | 103-120 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/refinar_credibilidade_sih_teco.py, linhas 74-80.

```python
 allcid=a.groupby(['CID10','NIVEL']).size();ids=col('N_AIH')[mask];_,dupcounts=np.unique(ids,return_counts=True)
 j={'ano':y,'mes':m,'finger':finger,'source_bytes':src.stat().st_size,'source_mtime_ns':src.stat().st_mtime_ns,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'registros':n,'aih_normais':int(mask.sum()),'excluidos_ident5':int(((~deleted)&(ident==b'5')).sum()),'excluidos_deletados':int(deleted.sum()),'repeticoes_NAIH_no_mes':int(np.maximum(dupcounts-1,0).sum()),'todos':[[*k,int(v)] for k,v in allc.items()],'res4':[[*k,int(v)] for k,v in r4.items()],'cid':[[*k,int(v)] for k,v in allcid.items()]}
 cache.write_text(json.dumps(j,ensure_ascii=False),encoding='utf8');assert dbf.resolve().is_relative_to(T.resolve());dbf.unlink();print('RD_REFINO',y,m,j['aih_normais'],flush=True);return j

# Official
def official():
 path=O/'TabNet_producao_MG_2016_2025.html';fields=json.loads((R/'dados_publicos/saude/campos_tabnet.json').read_text('utf8'))
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/relatorio_auditoria_residencia.py

Relatório da conferência por residência, com totais e limites verificáveis.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\relatorio_auditoria_residencia.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| reportlab.lib | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.pagesizes | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/05_auditoria_saude/consolidacao.json — chamada .read_text, linha 50.
- E:/teco/output/05_auditoria_saude/Resumo_municipios_residencia.csv — chamada pd.read_csv, linha 50.
- E:/teco/output/05_auditoria_saude/Estabelecimentos_confirmados_residencia.csv — chamada pd.read_csv, linha 50.
- E:/teco/output/05_auditoria_saude/RD_registros_codificacao_nao_mapeada.csv — chamada pd.read_csv, linha 64.

**Saídas.**

- E:/teco/output/05_auditoria_saude/Auditoria_Internacoes_TECO.md — chamada .write_text, linha 88.

**Campos e chaves lidos.**

- styles: Body, Head, Small, TitleTECO.
- r: AIH_NRMG, CNES, NOME_TABNET.
- meta: pendentes_coordenada.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| p(t) | 42-42 | Chamadas efetivas: story.append, md.extend, Paragraph, html.escape |
| h(t) | 44-44 | Chamadas efetivas: story.append, md.extend, Paragraph, html.escape |
| table(head, rows, widths) | 46-47 | Chamadas efetivas: Table, t.setStyle, story.extend, md.extend, TableStyle, Paragraph, Spacer, .join |
| n(x) | 49-49 | Chamadas efetivas: .replace, int Retorno: f'{int(x):,}'.replace(',', '.'). |
| source(label, url) | 83-83 | Chamadas efetivas: story.append, md.extend, Paragraph, Spacer, html.escape |
| footer(canvas, doc) | 86-87 | Chamadas efetivas: canvas.setFont, canvas.setFillColor, canvas.drawString, canvas.drawRightString, colors.HexColor, str |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/relatorio_auditoria_residencia.py, linhas 63-69.

```python
p('Os microdados somaram 2.038.504 registros no recorte, 18 a mais que a consulta NRMG. A diferença ficou integralmente localizada em registros com N182, N183, N184 e N185, não mapeados no dicionário de compatibilização consultado. Ao separar esses 18 registros, a conferência passa a coincidir em cada combinação de hospital, município de residência e ano, e não apenas no total geral. Os registros foram preservados em arquivo próprio. Não houve rateio, arredondamento ou alteração artificial da produção.')
unusual=pd.read_csv(O/'RD_registros_codificacao_nao_mapeada.csv',sep=';',dtype={'CID10':str});table(['Subcódigo registrado','AIH separadas para conferência'],[[c,n(v)] for c,v in unusual.groupby('CID10').AIH.sum().items()],[250,254])
p('A coincidência operacional após essa separação não transforma o dicionário consultado em avaliação clínica dos registros. O arquivo integral continua disponível para revisão de versões de codificação e agrupamento. Para os gráficos que reproduzem o NRMG, utiliza-se a base compatibilizada, com 2.038.486 internações.')
h('4. Filtro das causas bacterianas e compatíveis')
p('No conjunto ampliado foram observados 8.515 códigos de diagnóstico principal. As mesmas regras operacionais foram aplicadas e selecionaram 662 códigos no filtro amplo A+B, totalizando 274.254 internações: 133.203 no grupo A e 141.051 no grupo B. O grupo A reúne etiologia bacteriana codificada; o grupo B reúne síndromes infecciosas que podem ser bacterianas, mas não identificam o agente. Condições associadas ou sequelas ficam no grupo C, para consulta complementar.')
p('Esses números representam produção hospitalar selecionada, sem confirmação microbiológica de bactéria resistente, emissão de genes ou prevalência de resistência antimicrobiana. A classificação por CID é uma seleção operacional do estudo. Os diagnósticos, as regras e os casos não selecionados permanecem disponíveis para revisão. O explorador permite alternar A+B, A, B, C, todas as causas e um diagnóstico específico.')
story.append(PageBreak())
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/relatorio_grade_teco.py

Relatório consolidado da grade500m: método, uso, interpretação e pendências.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\relatorio_grade_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ast | Inspeção/transformação da sintaxe Python sem executar o processamento científico. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| reportlab.lib | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.enums | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.pagesizes | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.utils | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/codigo/relatorio_teco.py — chamada .read_text, linha 48.
- E:/teco/output/04_grade_500m/tabelas/{name} — chamada .open, linha 61.
- E:/teco/output/04_grade_500m/auditoria/metodo_grade.json — chamada .read_text, linha 62.
- E:/teco/output/04_grade_500m/auditoria/coleta_rd.json — chamada .read_text, linha 62.

**Saídas.**

- E:/teco/output/02_avaliacao_espacial/Relatorio_TECO.md — chamada .write_text, linha 157.

**Campos e chaves lidos.**

- s: TitleTECO.
- meta: centros, unidades_bacia.
- rd: CID10_distintos, aih_normais, competencias_obtidas, unidades_no_cadastro.
- r: ARI, CNES, I, K_S0, POP_DENS, SEM_REDE, bacia, cenario, descricao, internacoes_10_anos, media_anual, media_diaria_no_mes, melhor_k, mes_maior_media_diaria, mesmo_grupo_pct, n, p, peso_aih_local, peso_populacao, peso_sem_rede, unidade.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| tidy(text) | 51-54 | Chamadas efetivas: text.replace Retorno: text. |
| p(text) | 56-56 | Chamadas efetivas: oldp, tidy |
| h(text) | 58-58 | Chamadas efetivas: oldh, tidy |
| read(name) | 60-61 | Chamadas efetivas: .open, list, csv.DictReader Retorno: list(csv.DictReader(f, delimiter=';')). |
| footer(canvas, doc) | 151-152 | Chamadas efetivas: canvas.saveState, canvas.setStrokeColor, canvas.line, canvas.setFont, canvas.setFillColor, canvas.drawString, canvas.drawRightString, canvas.restoreState |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/relatorio_grade_teco.py, linhas 51-59.

```python
def tidy(text):
 for old,new in [('externo500m','externo de 500 m'),('EPSG31983','EPSG:31983'),('classe24','classe 24'),('nesses120','nesses 120'),('somaram15','somaram 15'),('sendo6','sendo 6'),('Infantil e9','Infantil e 9'),('de0 a20','de 0 a 20'),('pasta04_grade_500m','pasta 04_grade_500m')]:text=text.replace(old,new)
 for old,new in [('de500m','de 500 m'),('grade500m','grade 500 m'),('raio500m','raio de 500 m'),('de2016','de 2016'),('a2025','a 2025'),('de2025','de 2025'),('em2026','em 2026'),('de2017','de 2017'),('de2022','de 2022'),('Censo2022','Censo 2022'),('ano2025','ano 2025'),('Copernicus GLO30','Copernicus GLO-30'),('de30m','de 30 m'),('de866m','de 866 m'),('aproximadamente866m','aproximadamente 866 m'),('por100','por 100'),('de20','de 20'),('de40','de 40'),('de60','de 60'),('de80','de 80'),('a100','a 100'),('por1','por 1'),('de1 mais','de 1 mais'),('de1:225','de 1:225'),('SIRGAS2000','SIRGAS 2000'),('UTM23S','UTM 23S'),('de0,8','de 0,8'),('intervalo0-1','intervalo 0-1'),('em0-100','em 0-100'),('com999','com 999'),('usadas999','usadas 999'),('FDR5%','FDR 5%'),('pelo menos95%','pelo menos 95%'),('IDENT=1','IDENT=1'),('peso1','peso 1'),('peso3','peso 3'),('WHO2024','WHO 2024'),('em500m','em 500 m'),('de1 indica','de 1 indica')]:text=text.replace(old,new)
 return text
# P
def p(text):oldp(tidy(text))
# H
def h(text):oldh(tidy(text))
# Read
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/relatorio_metodologia_auditoria_teco.py

Relatório integrado: saúde em primeiro plano, procedimentos e alcance de cada módulo.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\relatorio_metodologia_auditoria_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| reportlab.lib.colors | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.pagesizes | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/05_auditoria_saude/refino/Dados_da_conferencia.json — chamada .read_text, linha 36.
- E:/teco/entrega_final/00_documentacao/Comparacao_kmeans_sensibilidade.json — chamada .read_text, linha 36.
- E:/teco/entrega_final/00_documentacao/Informacoes_gerais_bacias.json — chamada .read_text, linha 36.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 36.

**Saídas.**

- E:/teco/output/02_avaliacao_espacial/Relatorio_TECO.md — chamada .write_text, linha 203.

**Campos e chaves lidos.**

- DATA: distribuicao, metricas.
- M: AIH_AB_MG, AIH_MG, AIH_PROD_AB_BACIAS, AIH_PROD_AB_REDE383, AIH_PROD_BACIAS, AIH_PROD_REDE383, AIH_RES_AB, AIH_RES_TABNET.
- r: AIH_RES, ARI, area_km2, cenario, densidade_hab_km2, faixa, mesmo_grupo_pct, nome, populacao_estimada, silhouette, unidades.
- POP: bacias.
- KM: comparacao.
- value: headers, rows.
- styles: title.
- v: headers, highlight, rows, widths.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| n(v, d=0) | 38-38 | Chamadas efetivas: .replace Retorno: f'{v:,.{d}f}'.replace(',', '@').replace('.', ',').replace('@', '.'). |
| section(title, *items) | 41-41 | Chamadas efetivas: S.append, list |
| p(t) | 43-43 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: ('p', t). |
| h(t) | 45-45 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: ('h', t). |
| call(t) | 47-47 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: ('call', t). |
| tab(headers, rows, widths=None, highlight=None) | 49-49 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: ('table', {'headers': headers, 'rows': rows, 'widths': widths, 'highlight': highlight}). |
| markdown() | 167-176 | Chamadas efetivas: .join, lines.append, len, .replace, str Retorno: '\n'.join(lines). |
| pdf() | 179-206 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/relatorio_metodologia_auditoria_teco.py, linhas 38-46.

```python
def n(v,d=0):return f'{v:,.{d}f}'.replace(',','@').replace('.',',').replace('@','.')
S=[]
# Section
def section(title,*items):S.append((title,list(items)))
# P
def p(t):return ('p',t)
# H
def h(t):return ('h',t)
# Call
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/relatorio_teco.py

Relatório explicativo editável (Markdown) e PDF leve da avaliação TECO.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\teco\codigo\relatorio_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| reportlab.lib | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.enums | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.pagesizes | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.utils | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/02_avaliacao_espacial/auditoria/auditoria.json — chamada .read_text, linha 44.
- E:/teco/output/02_avaliacao_espacial/tabelas/{n} — chamada .open, linha 47.
- E:/teco/output/03_multivariada/auditoria/metodo_multivariada.json — chamada .read_text, linha 138.
- E:/teco/output/03_multivariada/auditoria/exutorio_relevo.json — chamada .read_text, linha 139.
- E:/teco/output/03_multivariada/tabelas/{n} — chamada .open, linha 142.

**Saídas.**

- E:/teco/output/02_avaliacao_espacial/tabelas/referencias_teco.csv — chamada .open, linha 269.
- E:/teco/output/02_avaliacao_espacial/Relatorio_TECO.md — chamada .write_text, linha 271.

**Campos e chaves lidos.**

- s: BodyTECO, HeadTECO, SmallTECO, TitleTECO.
- r: ARI_base, CNES, I, NOME, bacia, cenario, cluster, com_indice, conectados_lago_pct, dias_permanencia, dist_med_km, internacoes, melhor_k, mesmo_perfil_pct, n, nome, p, pop_dens, pop_est, recortes, sem_indice, sem_rede, urb_pct, variavel, vizinhos.
- A: d8.
- v: d, n, nome.
- EX: deslocamento_m, referencia.
- M: bibliotecas, semente.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| read(n) | 46-47 | Chamadas efetivas: .open, list, csv.DictReader Retorno: list(csv.DictReader(f, delimiter=';')). |
| num(x, d=0) | 49-49 | Chamadas efetivas: .replace, float, str Retorno: f"{float(str(x).replace(',', '.')):,.{d}f}".replace(',', '_').replace('.', ',').replace('_', '.'). |
| h(t) | 58-58 | Chamadas efetivas: story.append, md.extend, Paragraph, html.escape |
| p(t) | 60-61 | Chamadas efetivas: story.append, md.extend, Paragraph, html.escape |
| link(t, u) | 63-64 | Chamadas efetivas: story.append, md.extend, Paragraph, html.escape |
| table(headers, rows, widths=None) | 66-70 | Chamadas efetivas: Table, t.setStyle, story.extend, md.append, md.extend, TableStyle, str, Paragraph |
| fig(name, caption) | 72-76 | Chamadas efetivas: Path, .getSize, story.append, md.extend, f.is_absolute, KeepTogether, ImageReader, str |
| read3(n) | 141-142 | Chamadas efetivas: .open, list, csv.DictReader Retorno: list(csv.DictReader(f, delimiter=';')). |
| fig3(n, cap) | 144-146 | Chamadas efetivas: f.exists, fig, str |
| page(c, doc) | 273-274 | Chamadas efetivas: c.setStrokeColor, c.line, c.setFont, c.setFillColor, c.drawString, c.drawRightString, colors.HexColor, str |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/relatorio_teco.py, linhas 46-54.

```python
def read(n):
    with (O/'tabelas'/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
# Num
def num(x,d=0):return f'{float(str(x).replace(",",".")):,.{d}f}'.replace(',','_').replace('.',',').replace('_','.')
for n,f in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Arial-Italic','ariali.ttf')]:pdfmetrics.registerFont(TTFont(n,str(Path(_cp_externo('fonts_2a6cc8f'))/f)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial-Italic',boldItalic='Arial-Bold')
s=getSampleStyleSheet();s.add(ParagraphStyle(name='BodyTECO',fontName='Arial',fontSize=10,leading=14.2,alignment=TA_JUSTIFY,spaceAfter=8,allowWidows=0,allowOrphans=0))
s.add(ParagraphStyle(name='HeadTECO',fontName='Arial-Bold',fontSize=13,leading=17,textColor=colors.HexColor('#194956'),spaceBefore=14,spaceAfter=8,keepWithNext=True))
s.add(ParagraphStyle(name='SmallTECO',fontName='Arial',fontSize=8.3,leading=11,spaceAfter=7))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/reorganizar_qgis_bacias.py

Reorganizar qgis bacias. Cartografia/apresentação. A organização passa por add, fill, rules, categorical, interval, raster, paletted, point_style, clear_legend, label.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\reorganizar_qgis_bacias.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| idioma_cartografico_teco | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtCore | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.PyQt.QtGui | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.PyQt.QtXml | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 54.
- E:/teco/config/paleta_hipsometria.json — chamada .read_text, linha 168.
- E:/teco/projeto_teco.qgz — chamada zipfile.ZipFile, linha 233.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/Revisao_QGIS_camadas.json — chamada .write_text, linha 274.

**Campos e chaves lidos.**

- x: arquivo.
- m: vetores.
- s: cor, posicao.
- hip: paradas.
- cache: all, boundaries, connection, index, km, moran, samples, water.
- groups: all.

**Campos e chaves gerados.**

- os.environ: QT_QPA_FONTDIR, QT_QPA_PLATFORM.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| add(source, name, key, group, kind='vector', subset_field=None, visible=False) | 61-68 | Chamadas efetivas: file.exists, l.isValid, isinstance, p.addMapLayer, .setItemVisibilityChecked, newlayers.append, catalog.append, paths.get Retorno: l. |
| fill(color) | 71-71 | Chamadas efetivas: QgsFillSymbol.createSimple Retorno: QgsFillSymbol.createSimple({'color': color, 'outline_color': '#607880', 'outline_width': '.055'}). |
| rules(l, entries, point=False) | 74-77 | Chamadas efetivas: QgsRuleBasedRenderer, ren.rootRule, rt.removeChildAt, l.setRenderer, rt.appendChild, QgsMarkerSymbol.createSimple, fill, QgsRuleBasedRenderer.Rule |
| categorical(l, field, entries) | 80-82 | Chamadas efetivas: rules, .indexFromName, l.name, l.fields, isinstance, str |
| interval(l, field, bounds, colors=COL) | 85-89 | Chamadas efetivas: enumerate, rules, .indexFromName, l.name, entries.append, l.fields, len |
| raster(source, name, key, lo, hi, colors=None) | 92-94 | Chamadas efetivas: add, QgsColorRampShader, ramp.setColorRampType, ramp.setColorRampItemList, QgsRasterShader, s.setRasterShaderFunction, QgsSingleBandPseudoColorRenderer, ren.setClassificationMin Retorno: l. |
| paletted(source, name, key, classes, group=None) | 97-98 | Chamadas efetivas: add, l.setRenderer, QgsPalettedRasterRenderer, l.dataProvider, QgsPalettedRasterRenderer.Class, QColor Retorno: l. |
| point_style(l) | 101-109 | Chamadas efetivas: QgsRuleBasedRenderer, ren.rootRule, rt.removeChildAt, QgsMarkerSymbol, QgsSvgMarkerSymbolLayer, svg.setSize, symbol.changeSymbolLayer, QgsMarkerSymbol.createSimple |
| clear_legend(layout) | 180-182 | Chamadas efetivas: list, layout.items, isinstance, layout.removeLayoutItem, .y, item.positionWithUnits |
| label(layout, text, x, y, width, height, size=6) | 185-186 | Chamadas efetivas: QgsLayoutItemLabel, l.setText, l.setFont, layout.addLayoutItem, l.attemptMove, l.attemptResize, QFont, QgsLayoutPoint Retorno: l. |
| legend(layout, entries, unit) | 189-193 | Chamadas efetivas: clear_legend, label, lab.setHAlign, min, enumerate, len, box.setBackgroundEnabled, box.setBackgroundColor |
| theme_layout(layout, theme, newname, title=None, unit='') | 196-209 | Chamadas efetivas: layout.setName, layout.items, sorted, zip, .renderer, isinstance, len, mp.setLayers |
| count_empty(node) | 263-263 | Chamadas efetivas: sum, isinstance, node.findGroups, c.findLayers Retorno: sum((isinstance(c, QgsLayerTreeGroup) and (not c.findLayers()) for c in node.findGroups())). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/reorganizar_qgis_bacias.py, linhas 262-268.

```python
# Count empty
def count_empty(node):return sum(isinstance(c,QgsLayerTreeGroup) and not c.findLayers() for c in node.findGroups())
assert count_empty(root)==0
for key in keys:
 for g in groups[key]['root'].findGroups():g.setExpanded(False)
groups['all']['root'].setExpanded(True)
for key,g in groups['all'].items():
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/reproduzir_analise_configuravel.py

Reproduz a classificação atual a partir de matrizes já consolidadas e permite testar outra variável com origem, campo, agregação, transformação e pesos declarados. Grava em pasta separada, sem substituir os mapas publicados.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\teco\codigo\reproduzir_analise_configuravel.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| importlib.metadata | Importação e identificação de versões das bibliotecas. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.windows | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| scipy.cluster.hierarchy | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.cluster.vq | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.optimize | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.sparse | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| warnings | Controle de avisos de bibliotecas sem alterar a definição do estimador. |


**Entradas.**

- caminho(spec['arquivo']) — chamada gpd.read_file, linha 68.
- caminho(spec['arquivo']) — chamada pd.read_csv, linha 78.
- caminho(spec['arquivo']) — chamada rasterio.open, linha 82.
- args.config — chamada .read_text, linha 236.

**Saídas.**

- caminho(config['saida'])/analise_configuravel.gpkg [camada 'resultados'] — chamada out.to_file, linha 228.
- caminho(config['saida'])/indicadores.csv — chamada .to_csv, linha 229.
- caminho(config['saida'])/comparacao_k.csv — chamada table.to_csv, linha 230.
- caminho(config['saida'])/normalizacao.csv — chamada params.to_csv, linha 230.
- caminho(config['saida'])/sensibilidade.csv — chamada .to_csv, linha 230.
- caminho(config['saida'])/moran.csv — chamada .to_csv, linha 231.
- caminho(config['saida'])/manifesto.json — chamada .write_text, linha 233.

**Campos e chaves lidos.**

- spec: arquivo, camada, campo, nome.
- support: geometry.
- src: geometry.
- overlap: _a, _av.
- s: _a, _av.
- config: base, campo_bacia, cenarios, chaves, inicializacoes, k_testados, normalizacao, saida, semente, suporte_calculo, variaveis.
- v: nome.
- setting: pesos.
- table: cenario.
- local: cluster, q.

**Campos e chaves gerados.**

- work: _i.
- overlap: _a, _av.
- out: completo, estabilidade, q_fdr, r_moran, r_quintil.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| ler_camada(spec) | 66-68 | lê dados Retorno: gpd.read_file(path, layer=spec['camada']) if spec.get('camada') else gpd.read_file(path). |
| anexar_variavel(base, spec, support) | 71-105 | lê dados Retorno: pd.to_numeric(base[field], errors='coerce').to_numpy(), pd.to_numeric(base[[left]].merge(src[[right, field]], left_on=left, right_on=right, how='left', validate='many_to_one')[field], errors='coerce'). |
| matriz(base, support, config) | 108-124 | Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original. Retorno: (norm, valid, pd.DataFrame({'variavel': fields, 'centro_ou_minimo': center, 'escala_ou_amplitude': scale})). |
| ari(a, b) | 127-132 | Chamadas efetivas: np.unique, len, .reshape, comb, .sum, tab.sum, np.bincount, a.max Retorno: (x - e) / den if den else 1.0. |
| fitkm(x, k, seed, starts=12) | 135-144 | Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida. Retorno: best. |
| silhouette(x, l) | 147-154 | Chamadas efetivas: distance.cdist, enumerate, float, same.sum, min, s.append, np.mean, .sum Retorno: float(np.mean(s)). |
| bh(p) | 157-158 | Chamadas efetivas: np.asarray, np.argsort, np.empty, np.minimum, np.minimum.accumulate, len, np.arange Retorno: o. |
| align(labels, reference) | 161-163 | Chamadas efetivas: .reshape, linear_sum_assignment, dict, np.array, max, zip, labels.max, reference.max Retorno: np.array([lookup[v] for v in labels]). |
| queen(g) | 166-168 | Chamadas efetivas: g.sindex.query, len, csr_matrix, w.maximum, w.setdiag, w.eliminate_zeros, np.ones Retorno: w. |
| moran_w(values, w, local=False, seed=SEED) | 171-188 | Chamadas efetivas: np.flatnonzero, .tocsr, len, float, np.random.default_rng, range, np.empty, bh Retorno: (rec, {'p': p, 'q': q, 'cluster': cl, 'Ii': Ii}, original), ({'n': n, 'isolados': int((~good).sum()), 'I': np.nan, 'p': np.nan}, None, original). |
| executar(config) | 191-233 | grava produtos; Agrupamento hierárquico. Com method=ward, as fusões procuram o menor aumento da dispersão interna.; Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/reproduzir_analise_configuravel.py, linhas 113-119.

```python
            if np.any(values[np.isfinite(values)]<0):raise ValueError('log1p exige valores não negativos nesta análise')
            values=np.log1p(values)
        elif transform!='identidade':raise ValueError('Transformação desconhecida: '+transform)
        columns.append(values);fields.append(spec['nome'])
    x=np.column_stack(columns);valid=np.isfinite(x).all(axis=1)
    if valid.sum()<8:raise ValueError('Menos de oito registros completos; revisar entradas e lacunas')
    if config['normalizacao']=='minmax':
```

Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/reproduzir_analise_configuravel.py, linhas 128-134.

```python
    _,a=np.unique(a,return_inverse=True);_,b=np.unique(b,return_inverse=True);n=len(a)
    tab=np.bincount(a*(b.max()+1)+b,minlength=(a.max()+1)*(b.max()+1)).reshape(a.max()+1,b.max()+1)
    comb=lambda x:(x*(x-1)/2).sum()
    x=comb(tab);r=comb(tab.sum(0));s=comb(tab.sum(1));e=r*s/(n*(n-1)/2);den=(r+s)/2-e
    return (x-e)/den if den else 1.

# Fitkm
```

Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- log1p: Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.
- bincount: Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.
- kmeans2: Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida.
- cdist: Matriz de distâncias entre observações. É usada no agrupamento, na silhouette ou na comparação entre centroides.
- linear_sum_assignment: Alinha rótulos de grupos pela maior correspondência; evita contar como mudança apenas a troca do número do grupo.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.
- linkage: Agrupamento hierárquico. Com method=ward, as fusões procuram o menor aumento da dispersão interna.
- fcluster: Transforma a árvore hierárquica em rótulos de grupos segundo o critério fornecido.
- spearmanr: Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/revisar_cnes_sih_mg_teco.py

Cruza o cadastro CNES-MG e a tabela estadual SIH por local de internação, preserva períodos, valida coordenadas e separa cadastro ativo de estabelecimento com produção hospitalar recente.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\revisar_cnes_sih_mg_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ast | Inspeção/transformação da sintaxe Python sem executar o processamento científico. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| consolidar_entrega_final | Módulo autoral local; sua ficha está neste relatório. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {p} — chamada p.read_bytes, linha 111.
- E:/teco/entrega_final/00_documentacao/{name} — chamada path.read_text, linha 334.
- {path} — chamada pd.read_csv, linha 153.
- E:/teco/output/05_auditoria_saude/saude_tabnet_auditada.gpkg [camada 'producao_SIH_georreferenciada'] — chamada gpd.read_file, linha 186.
- E:/teco/teco_base/mg_mun/ide_1103_mg_municipios_pol.shp — chamada gpd.read_file, linha 195.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 312.
- E:/teco/entrega_final/LEIA_PRIMEIRO.md — chamada p.read_text, linha 314.
- E:/teco/codigo/integrar_cnes_sih_2026_qgis.py — chamada .read_text, linha 319.
- E:/teco/entrega_final/00_documentacao/Field_dictionary_EN.csv — chamada pd.read_csv, linha 321.
- E:/teco/entrega_final/TECO_Consolidado.qgz — chamada zipfile.ZipFile, linha 326.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Auditoria_CNES_SIH_2026.json — chamada .read_text, linha 328.
- E:/teco/entrega_final/01_entradas/01_bacias/bacias.shp — chamada gpd.read_file, linha 356.
- Mais 1 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/{name} — chamada frame.to_csv, linha 107.
- bad.drop(columns=['geometry', 'index_right']) — chamada save, linha 205.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Relatorio_revisao_CNES_SIH.md — chamada .write_text, linha 288.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Relatorio_revisao_CNES_SIH.html — chamada .write_text, linha 307.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/LEIA_PRIMEIRO.md — chamada .write_text, linha 308.
- E:/teco/entrega_final/00_documentacao/Inventario_de_camadas.csv — chamada .to_csv, linha 313.
- E:/teco/entrega_final/LEIA_PRIMEIRO.md — chamada p.write_text, linha 318.
- E:/teco/entrega_final/00_documentacao/Field_dictionary_EN.csv — chamada en.to_csv, linha 324.
- E:/teco/entrega_final/00_documentacao/{name} — chamada path.write_text, linha 344.
- {x} — chamada save, linha 360.
- inside.groupby(['BACIA', 'TIPO_CNES'], as_index=False).size().rename(columns={'size': 'ESTABELECIMENTOS'}) — chamada save, linha 361.
- monthly[monthly.CNES.isin(selected.CNES) & monthly.NO_RECORTE].copy() — chamada save, linha 363.
- Mais 6 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- data: CNES, Estabelecimento, FORA_PER, INT_15_26, INT_24_26, INT_FONTE, NOME_SIH, Total.
- c: CEP, CNES, COMPLEMENTO DO ENDEREÇO, LOGRADOURO, location.
- q: COMPLEMENTO DO ENDEREÇO.
- sih: CNES, INT_15_26, INT_2024, INT_2025, INT_2026, INT_24_26, INT_FONTE, MES_REC, NOME_SIH, RECENTE, ULT_ATEND.
- bacias: geometry, id.
- bacias.loc: id.
- municipalities: geocodigo, geometry, nome.
- audit: atendimentos_2015_2026, atendimentos_anteriores_2015, estabelecimentos, meses_em_colunas, total_oficial.
- m: mapas, rasters, vetores.
- en: dataset.
- en.loc: stored_field.
- r: arquivo, layer_id.
- raw: COMPETÊNCIA, STATUS DO ESTABELECIMENTO.

**Campos e chaves gerados.**

- data: CNES, FORA_PER, INT_15_26, INT_24_26, INT_FONTE, MES_REC, NOME_SIH, RECENTE, ULT_ATEND.
- monthly: ANO, ANO_MES, INTERNACOES, MES, NO_RECORTE.
- c: CNES.
- q: COORD_OK, ENDERECO, LAT, LON.
- joined: DIST_BAC_M, MUN_GEO, QA_MUN_2026, SELEC_SIH, SIH_HIST.
- near: BACIA.
- statewide: CNES_EXPORT, MOTIVO.
- pending: BACIA_REF, DIST_REF_M.
- municipalities: nome.
- value: camadas_validas, camadas_vetoriais_com_dicionario, layers.
- record: layers.
- audit: conferencia_municipal.
- m: healthcare_2026_audit, vetores.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| save(frame, name) | 106-107 | grava produtos |
| sha(p) | 110-111 | lê dados Retorno: hashlib.sha256(p.read_bytes()).hexdigest(). |
| ler_sih(path) | 114-149 | lê dados Retorno: (data, monthly, audit). |
| ler_cnes(path) | 152-166 | lê dados Retorno: (c, points). |
| cruzar(cnes, sih, bacias) | 169-189 | lê dados Retorno: (inside, selected, near, statewide, pending). |
| conferir_municipios(statewide) | 192-206 | lê dados; grava produtos Retorno: {'estabelecimentos_recentes_conferidos': len(joined), 'divergencias_municipais': len(bad), 'CNES_divergentes': bad.CNES.tolist(), 'divergentes_nos_oito_municipios': int(bad.MUN_COD.isin(['310620', '31. |
| camadas(frames) | 209-216 | Chamadas efetivas: frames.items, exp.shapefile, .reset_index Retorno: exp.VECTORS. |
| relatorio(audit, raw, inside, selected, near, statewide, pending, summary, archive) | 219-308 | grava produtos Retorno: re.sub('\\[([^\\]]+)\\]\\((https?://[^)]+)\\)', '<a href="\\2">\\1</a>', s). |
| documentar_revisao() | 311-344 | lê dados; grava produtos |
| main() | 347-377 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/revisar_cnes_sih_mg_teco.py, linhas 126-132.

```python
    recent=[c for c in monthcols if INICIO_RECENTE<=dates[c]<=FIM]
    data['INT_FONTE']=values.sum(axis=1).astype(int)
    data['INT_15_26']=values[inperiod].sum(axis=1).astype(int)
    data['INT_24_26']=values[recent].sum(axis=1).astype(int)
    data['FORA_PER']=data.INT_FONTE-data.INT_15_26
    for year in range(2015,2027):data[f'INT_{year}']=values[[c for c in monthcols if c.startswith(str(year))]].sum(axis=1).astype(int)
    data['ULT_ATEND']=[max((dates[c] for c in monthcols if pd.notna(values.loc[i,c]) and values.loc[i,c]>0),default='') for i in values.index]
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/saude_todos_municipios_teco.py

Saude todos municipios teco. Processamento ou módulo de apoio. A organização passa por month, query, save, main, col, sums.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\saude_todos_municipios_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| filtro_bacteriano_teco | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| requests | Consultas e downloads HTTP; depende de internet e da disponibilidade do provedor. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| struct | Decodificação binária com tipos, tamanhos e ordem de bytes definidos. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| urllib.parse | Requisições e manipulação de endereços de serviços públicos. |


**Entradas.**

- E:/teco/saneamento_ibge/resultados/municipios_interceptados.csv — chamada pd.read_csv, linha 69.
- E:/teco/dados_publicos/saude_revisao/CID10_oficial_GO.json — chamada .read_text, linha 72.
- E:/teco/codigo/filtro_bacteriano_teco.py — chamada .read_bytes, linha 73.
- E:/teco/dados_publicos/auditoria_sih_8_municipios/NRMG_{mu}_2016_2025.html — chamada p.read_text, linha 95.
- E:/teco/tmp/saude8/src.stem.dbf — chamada dbf.read_bytes, linha 81.
- E:/teco/dados_publicos/saude_grade/rd/RDMG{y % 100}{m}.dbc — chamada src.read_bytes, linha 88.
- E:/teco/dados_publicos/auditoria_sih_20261112/campos_NRMG.json — chamada .read_text, linha 92.
- E:/teco/output/05_auditoria_saude/refino/Producao_hospitalar_mensal_niveis.csv — chamada pd.read_csv, linha 124.
- E:/teco/output/05_auditoria_saude/refino/TabNet_producao_MG_anual.csv — chamada pd.read_csv, linha 130.

**Saídas.**

- E:/teco/dados_publicos/auditoria_sih_8_municipios/NRMG_{mu}_2016_2025.html — chamada p.write_text, linha 99.
- E:/teco/dados_publicos/auditoria_sih_8_municipios/consulta_NRMG_{mu}.json — chamada .write_text, linha 93.
- E:/teco/output/05_auditoria_saude/todos_municipios_bacias/buf[pos:pos + 11].split(b'/x00')[0].decode() — chamada f.to_csv, linha 114.
- pd.DataFrame([{'CNES': c, 'MUN_RES': mu, 'CID10': cid, 'ANO': j['ano'], 'MES': j['mes'], 'AIH': n} for j in results for c, mu, cid, n in j['diag']]).sort_values(['CNES', 'MUN_RES', 'ANO', 'MES', 'CID10']) — chamada save, linha 122.
- frame.groupby(['CNES', 'MUN_RES', 'ANO', 'MES', 'NIVEL'], as_index=False).AIH.sum() — chamada save, linha 122.
- sums(frame, ['CNES'], 'RES8').merge(sums(prod, ['CNES'], 'PROD'), on='CNES', how='left', validate='one_to_one') — chamada save, linha 131.
- sums(frame, ['CNES', 'ANO'], 'RES8') — chamada save, linha 131.
- sums(frame, ['CNES', 'ANO', 'MES'], 'RES8') — chamada save, linha 131.
- sums(frame, ['CNES', 'MUN_RES'], 'RES8') — chamada save, linha 131.
- sums(frame, ['MUN_RES', 'ANO', 'MES'], 'RES8').assign(MUNICIPIO=lambda f: f.MUN_RES.map(MUN)) — chamada save, linha 131.
- sums(frame, ['ANO', 'MES'], 'RES8') — chamada save, linha 131.
- sums(frame, ['ANO'], 'RES8') — chamada save, linha 131.
- Mais 4 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- cross: mun_cod, mun_nome.
- x: code, display.
- official: concept.
- j: AIH_residentes8, ano, diag, mes, normal_MG.
- fields: Arquivos, Incremento.
- body: Arquivos.
- f.loc: AIH_TABNET.
- f: AIH_TABNET, ANO, MUN_RES.
- frame: AIH, CID10, CNES, MUN_RES, NIVEL.
- t: A, B, C, Sem dicionário.
- cmp: AIH, AIH_TABNET.
- frame.loc: AIH.
- audit: AIH_AB_RES4_confirmed, AIH_RES4_confirmed.

**Campos e chaves gerados.**

- frame: MUNICIPIO_RESIDENCIA, NIVEL.
- facility: NOME.
- municipal: MUNICIPIO, UNIDADES.
- cmp: DIF_RD_TABNET.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| month(ym) | 76-88 | lê dados; grava produtos Retorno: j, np.char.strip(np.ndarray(n, dtype=f'S{length}', buffer=buf, offset=head + start, strides=(rec,))). |
| query(mu) | 91-111 | lê dados; grava produtos Retorno: f. |
| save(f, name) | 114-114 | grava produtos |
| main() | 117-143 | lê dados; grava produtos Retorno: out. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/saude_todos_municipios_teco.py, linhas 87-93.

```python
 deleted=np.ndarray(n,dtype='S1',buffer=buf,offset=head,strides=(rec,))==b'*';normal=(~deleted)&(col('IDENT')==b'1');res=col('MUNIC_RES');mask=normal&np.isin(res,[k.encode() for k in MUN]);frame=pd.DataFrame({'CNES':np.char.zfill(col('CNES')[mask].astype(str),7),'MUN_RES':res[mask].astype(str),'CID10':col('DIAG_PRINC')[mask].astype(str)})
 values=frame.groupby(['CNES','MUN_RES','CID10']).size();j={'ano':y,'mes':m,'finger':FINGER,'source_bytes':src.stat().st_size,'source_mtime_ns':src.stat().st_mtime_ns,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'normal_MG':int(normal.sum()),'AIH_residentes8':int(mask.sum()),'diag':[[*k,int(v)] for k,v in values.items()]};p.write_text(json.dumps(j,ensure_ascii=False),encoding='utf8');assert dbf.resolve().is_relative_to(T.resolve());dbf.unlink();print('RD8',y,m,j['AIH_residentes8'],flush=True);return j

# Query
def query(mu):
 fields=json.loads((D/'campos_NRMG.json').read_text('utf8'));mk=next(k for k in fields if k.startswith('SMunic'));body={k:'TODAS_AS_CATEGORIAS__' for k in fields if k.startswith('S')};body.update(Linha='Estabelecimento',Coluna='Ano_processamento',Incremento=next(v for v,t in fields['Incremento'] if t.startswith('Interna')),Arquivos=[v for v,t in fields['Arquivos'] if 16<=int(v[4:6])<=25],formato='prn',mostre='Mostra');body[mk]=next(v for v,t in fields[mk] if t.startswith(mu));assert len(body['Arquivos'])==120
 p=D8/f'NRMG_{mu}_2016_2025.html';(D8/f'consulta_NRMG_{mu}.json').write_text(json.dumps(body,ensure_ascii=False,indent=2),encoding='utf8')
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/sondar_dados_grade.py

Sondar dados grade. Processamento ou módulo de apoio. A organização passa por one.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\sondar_dados_grade.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| bs4 | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| requests | Consultas e downloads HTTP; depende de internet e da disponibilidade do provedor. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/teco/dados_publicos/saude_grade/{k}'.dbc' if k == 'rd_piloto' else '.txt' — chamada .write_bytes, linha 35.
- E:/teco/dados_publicos/saude_grade/campos_morbidade.json — chamada .write_text, linha 40.
- E:/teco/dados_publicos/saude_grade/pbh_abrangencia_recursos.json — chamada .write_text, linha 42.

**Campos e chaves lidos.**

- a: name, url.

**Campos e chaves gerados.**

- msg: campos, linha, links, recursos.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| one(k, url) | 33-47 | grava produtos Retorno: msg, {'nome': k, 'erro': str(e)}. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/sondar_dados_grade.py, linhas 33-41.

```python
def one(k,url):
 try:
  t=time.time();r=requests.get(url,timeout=(10,50));r.raise_for_status();(D/(k+('.dbc' if k=='rd_piloto' else '.txt'))).write_bytes(r.content)
  msg={'nome':k,'url':url,'status':r.status_code,'bytes':len(r.content),'seg':round(time.time()-t,1)}
  if k=='rd_form':
   from bs4 import BeautifulSoup
   s=BeautifulSoup(r.content,'html.parser',from_encoding='latin1');fields={a.get('name'):[(o.get('value'),o.get_text()) for o in a.find_all('option')] for a in s.find_all('select')}
   (D/'campos_morbidade.json').write_text(json.dumps(fields,ensure_ascii=False),encoding='utf8');msg['campos']=list(fields);msg['linha']=fields.get('Linha')
  if k=='pbh_abrangencia':
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/testar_conferencia_unidades.mjs

Testar conferencia unidades. Conferência/teste. A organização passa por node, evaluate.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\teco\codigo\testar_conferencia_unidades.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ./caminhos_teco.mjs | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| node:fs/promises | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:vm | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |


**Entradas.**

- _cpPath("entrega_final/04_saude_residencia/Conferencia_unidades.html") — chamada fs.readFile, linha 11.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/testar_conferencia_unidades.mjs, linhas 13-18.

```javascript
function node(id){if(!nodes.has(id))nodes.set(id,{value:id==='area'?'ALL':id==='scope'?'PROD':'',innerHTML:'',textContent:''});return nodes.get(id)}
const ctx={document:{getElementById:node},console};vm.createContext(ctx);vm.runInContext(script,ctx);
const evaluate=source=>vm.runInContext(source,ctx);const sums=evaluate(`rows.reduce((s,r)=>s.map((v,i)=>v+r[i+3]),[0,0,0,0])`);const expected=[12242560,1862329,2038504,274254];if(JSON.stringify(sums)!==JSON.stringify(expected))throw Error('Totais incorretos '+sums);
for(const [area,n] of [['IN',3],['OUT',378],['PENDING',2],['ALL',383]]){node('area').value=area;evaluate('list()');if(!node('count').textContent.startsWith(n+' '))throw Error('Filtro incorreto '+area+' '+node('count').textContent)}
for(const [cnes,total,filtered] of [['2191164','96.232','9.389'],['2200473','97.567','13.651'],['6892256','48.849','7.929']]){evaluate(`choose(units.findIndex(u=>u.CNES==='${cnes}'))`);if(!node('counts').innerHTML.includes(total)||!node('counts').innerHTML.includes(filtered))throw Error('Unidade sem totais '+cnes);if(!node('series').innerHTML.includes('<svg'))throw Error('Série ausente')}
console.log('Explorador validado: 383 unidades, 3 dentro, 378 fora, 2 pendentes; totais e séries coerentes.');
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_entrega_final.py

Validar entrega final. Conferência/teste. A organização passa por ok, __init__, handle_starttag.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\teco\codigo\validar_entrega_final.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html.parser | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| urllib.parse | Requisições e manipulação de endereços de serviços públicos. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 67.
- E:/teco/entrega_final/r['arquivo'] — chamada gpd.read_file, linha 75.
- {d} — chamada pd.read_csv, linha 81.
- E:/teco/entrega_final/00_documentacao/Dicionario_dos_campos.csv — chamada pd.read_csv, linha 84.
- E:/teco/entrega_final/row.script_python — chamada code.read_text, linha 90.
- (F / dataset).parent/dicionario_campos.csv — chamada pd.read_csv, linha 92.
- E:/teco/entrega_final/00_documentacao/Dicionario_rasters.csv — chamada pd.read_csv, linha 93.
- E:/teco/entrega_final/01_entradas/03_populacao/populacao.shp — chamada gpd.read_file, linha 95.
- E:/teco/entrega_final/01_entradas/04_esgotamento/esgotamento.shp — chamada gpd.read_file, linha 95.
- E:/teco/entrega_final/02_saidas/01_consolidado/TECO_final.shp — chamada gpd.read_file, linha 96.
- E:/teco/entrega_final/02_saidas/02_testes/02_kmeans/S{scenario}/k{kval}/profiles.shp — chamada gpd.read_file, linha 100.
- E:/teco/entrega_final/01_entradas/16_IBGE_tabelas/Proveniencia_IBGE.json — chamada .read_text, linha 103.
- Mais 9 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/Validacao_da_entrega.json — chamada .write_text, linha 157.
- E:/teco/entrega_final/00_documentacao/Validacao_da_entrega.md — chamada .write_text, linha 158.
- E:/teco/entrega_final/00_documentacao/Integridade_SHA256.csv — chamada .open, linha 159.

**Campos e chaves lidos.**

- m: mapas, rasters, vetores.
- r: arquivo, feicoes, max, min, sem_geometria.
- g: CNES, setor_id.
- v: PROFILE, campos.
- dic: descricao, unidade.
- a: BACIA, setor_id.
- b: BACIA, setor_id.
- k: K_S0.
- k.loc: SEM_REDE.
- prov: sources.
- src: columns, output, records.
- u: AIH_NRMG, DIF_RES, RES8_AB, RES_RD.
- hm: TabNet_failures, TabNet_municipalities_checked.
- table: RES8_AB, RES8_TOTAL.
- row: slug, vetorial.
- x: detalhe, verificacao.
- report: restricao.

**Campos e chaves gerados.**

- report: apresentacao.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| ok(name, detail) | 70-70 | Chamadas efetivas: checks.append |
| Links() | 145-149 | Chamadas efetivas: .__init__, super, self.paths.append, value.startswith, urlsplit |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_entrega_final.py, linhas 75-81.

```python
 g=gpd.read_file(p);assert len(g)==r['feicoes'],p;assert g.crs.to_epsg()==31983,p
 assert int(g.geometry.isna().sum())==r['sem_geometria'],p
 assert g.loc[g.geometry.notna()].geometry.is_valid.all(),p
 assert all(len(c)<=10 for c in g.columns if c!='geometry'),p
 if 'CNES' in g:assert g.CNES.astype(str).str.fullmatch(r'\d{7}').all(),p
 if 'setor_id' in g:assert g.setor_id.astype(str).str.fullmatch(r'\d{15}').all(),p
for d in [D/'Dicionario_dos_campos.csv']+list(F.rglob('dicionario_campos.csv')):pd.read_csv(d,sep=';')
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/validar_entrega_final.py, linhas 84-90.

```python
dic=pd.read_csv(D/'Dicionario_dos_campos.csv',sep=';',dtype=str,keep_default_na=False)
assert len(dic)==sum(len(v['campos']) for v in m['vetores']) and not dic.duplicated(['arquivo','campo_shp']).any()
assert dic.descricao.str.len().ge(35).all() and dic.unidade.str.len().gt(0).all()
assert not dic.descricao.str.contains('Campo preservado|consultar a tabela original',case=False,regex=True).any()
for row in dic.itertuples():
 code=F/row.script_python;assert code.exists(),code
 lines=code.read_text('utf8').splitlines();assert row.trecho_referencia in lines[int(row.linha_referencia)-1],(row.campo_shp,code)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_multivariada_teco.py

Verificações reproduzíveis das entregas multivariadas TECO.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\teco\codigo\validar_multivariada_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| analise_espacial_teco | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| itertools | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| scipy.sparse | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sqlite3 | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/output/03_multivariada/tabelas/entradas_por_setor.csv — chamada pd.read_csv, linha 44.
- E:/teco/output/03_multivariada/tabelas/matriz_normalizada.csv — chamada pd.read_csv, linha 45.
- E:/teco/output/03_multivariada/teco_multivariada.gpkg [camada 'exutorios_referencia'] — chamada gpd.read_file, linha 59.
- E:/teco/output/03_multivariada/auditoria/galeria.json — chamada .read_text, linha 65.
- E:/teco/output/02_avaliacao_espacial/index.html — chamada .read_text, linha 69.
- E:/teco/projeto_teco.qgz — chamada zipfile.ZipFile, linha 72.
- E:/teco/output/03_multivariada/auditoria/metodo_multivariada.json — chamada .read_text, linha 76.

**Saídas.**

- E:/teco/output/03_multivariada/teco_multivariada.gpkg [camada 'exutorios_referencia'] — chamada v.to_file, linha 61.
- E:/teco/output/03_multivariada/auditoria/metodo_multivariada.json — chamada .write_text, linha 78.
- E:/teco/output/03_multivariada/auditoria/verificacao_final.json — chamada .write_text, linha 80.

**Campos e chaves lidos.**

- u: ESG_EST, ESG_OBS, elegivel, setor_id.
- g.loc: K_S0.
- g: ESG_OBS, elegivel.
- v: id.
- row: slug.

**Campos e chaves gerados.**

- meta: tratamento_lacunas.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_multivariada_teco.py, linhas 46-52.

```python
g=gpd.read_file(O/'teco_multivariada.gpkg',layer='unidades_ajuste')
assert len(u)==1838 and u.setor_id.is_unique and u.elegivel.sum()==1823
assert np.isfinite(x.iloc[:,:5]).all().all() and x.iloc[:,:5].min().min()>=-1e-10 and x.iloc[:,:5].max().max()<=1+1e-10
assert g.loc[g.elegivel,'K_S0'].between(1,5).all() and (g.loc[~g.elegivel,'K_S0']==0).all()
assert g.loc[~g.ESG_OBS,['MQ_S0','MK_S0']].eq('ND').all().all() if 'MQ_S0' in g else True

z=np.array([-2.,-1.,0.,1.,2.]);w=np.zeros((5,5))
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/validar_multivariada_teco.py, linhas 54-60.

```python
perms=np.array([a@(w@a)/(a@a) for a in map(np.array,itertools.permutations(z))])
assert abs(perms.mean()+.25)<1e-12
p=np.array([.001,.035,.2,.01,.9,.046]);assert np.allclose(bh(p),false_discovery_control(p,method='bh'))
assert ari(np.array([1,1,2,2]),np.array([2,2,1,1]))==1

v=gpd.read_file(O/'teco_multivariada.gpkg',layer='exutorios_referencia')
v.loc[v.id=='vargem_flores','acum_cel']=np.nan
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_qgis_reorganizado.py

Validar qgis reorganizado. Conferência/teste. A organização passa por allgroups, matching_rules.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\teco\codigo\validar_qgis_reorganizado.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/Validacao_QGIS_reorganizado.json — chamada .write_text, linha 67.

**Campos e chaves lidos.**

- f: SIT_ESP.
- spatial: Profile stability, Quintiles S0.

**Campos e chaves gerados.**

- os.environ: QT_QPA_PLATFORM.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| allgroups(node) | 30-32 | Chamadas efetivas: node.children, isinstance, allgroups |
| matching_rules(layer) | 35-39 | Chamadas efetivas: collections.Counter, QgsExpressionContext, context.appendScopes, .children, layer.getFeatures, dict, QgsExpressionContextUtils.globalProjectLayerScopes, QgsExpression Retorno: dict(result). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_qgis_reorganizado.py, linhas 30-38.

```python
def allgroups(node):
 for child in node.children():
  if isinstance(child,QgsLayerTreeGroup):yield child;yield from allgroups(child)

# Matching rules
def matching_rules(layer):
 result=collections.Counter();context=QgsExpressionContext();context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer));rules=layer.renderer().rootRule().children();expr=[QgsExpression(r.filterExpression()) for r in rules]
 for f in layer.getFeatures():
  context.setFeature(f);labels=[r.label() for r,e in zip(rules,expr) if bool(e.evaluate(context))];assert len(labels)==1,(layer.name(),f.id(),labels);result[labels[0]]+=1
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_qml_portatil.py

Validar qml portatil. Conferência/teste. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\teco\codigo\validar_qml_portatil.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| base64 | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/00_documentacao/simbolos/sampling_point_drop.svg — chamada svg.read_bytes, linha 28.
- E:/teco/entrega_final/01_entradas/11_pontos_coleta/pontos_coleta.qml — chamada path.read_text, linha 29.

**Saídas.**

- E:/teco/entrega_final/01_entradas/11_pontos_coleta/pontos_coleta.qml — chamada path.write_text, linha 29.

**Campos e chaves gerados.**

- os.environ: QT_QPA_PLATFORM.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_qml_portatil.py, linhas 27-35.

```python

svg=F/'00_documentacao/simbolos/sampling_point_drop.svg';encoded='base64:'+base64.b64encode(svg.read_bytes()).decode('ascii')
path=F/'01_entradas/11_pontos_coleta/pontos_coleta.qml';s=path.read_text('utf8');s=s.replace(svg.as_posix(),encoded);path.write_text(s,encoding='utf8')
test=Path(_cp_texto('tmp/validacao_estilo_portatil', 'posix'));test.mkdir(parents=True,exist_ok=True)
for src in path.parent.glob('pontos_coleta.*'):shutil.copy2(src,test/src.name)
l=QgsVectorLayer(str(test/'pontos_coleta.shp'),'Pontos','ogr');assert l.isValid();sl=l.renderer().symbols(QgsRenderContext())[0].symbolLayer(0);print('tipo',type(sl).__name__,'embutido',sl.path().startswith('base64:'),flush=True)
assert sl.path()==encoded
svgdata=QgsApplication.svgCache().svgContent(encoded,64,app.palette().text().color(),app.palette().text().color(),.2,1)
assert len(svgdata)>0;print('SVG carregado',len(svgdata),'bytes',flush=True)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/verificar_revisao_cnes_sih_teco.py

Verificar revisao cnes sih teco. Conferência/teste. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\teco\codigo\verificar_revisao_cnes_sih_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/00_fontes/sih_cnv_qimg100921200_198_31_2.csv — chamada .read_text, linha 51.
- E:/teco/entrega_final/01_entradas/01_bacias/bacias.shp — chamada gpd.read_file, linha 56.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/00_fontes/CNES_MG.csv — chamada .open, linha 58.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/Selecionados_nas_bacias.csv — chamada pd.read_csv, linha 64.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/CNES_nas_bacias.csv — chamada pd.read_csv, linha 67.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/Internacoes_gerais_selecionados_mensal.csv — chamada pd.read_csv, linha 69.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/01_tabelas/Internacoes_gerais_selecionados_anual.csv — chamada pd.read_csv, linha 70.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/02_camadas/01_cnes_bacias/cnes_2026.shp — chamada gpd.read_file, linha 76.
- {src} — chamada src.read_bytes, linha 80.
- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/00_fontes/src.name — chamada .read_bytes, linha 80.
- E:/teco/entrega_final/00_documentacao/Integridade_SHA256.csv — chamada .open, linha 83.
- E:/teco/entrega_final/row['arquivo'] — chamada p.read_bytes, linha 87.

**Saídas.**

- E:/teco/entrega_final/01_entradas/17_estabelecimentos_2026/04_documentacao/Validacao_independente_CNES_SIH.json — chamada .write_text, linha 90.

**Campos e chaves lidos.**

- r: Estabelecimento.
- row: CNES, STATUS DO ESTABELECIMENTO, arquivo, location, sha256.
- sel: CNES, INT_15_26.
- monthly: CNES.
- annual: CNES.
- g: SIH_HIST.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/verificar_revisao_cnes_sih_teco.py, linhas 54-60.

```python
recent=[x for x in header if re.match(r'^202[456]/',x)]
positive={r['Estabelecimento'][:7] for r in records if sum(int(r[c]) for c in recent if r[c]!='-')>0}
bas=gpd.read_file(F/'01_entradas/01_bacias/bacias.shp').geometry.union_all();trans=Transformer.from_crs(4326,31983,always_xy=True)
expected=set();allinside=set()
with (P/'00_fontes/CNES_MG.csv').open(encoding='utf-8-sig',newline='') as stream:
    for row in csv.DictReader(stream):
        c=row['CNES'].zfill(7);lat,lon=map(float,row['location'].split(','));point=Point(*trans.transform(lon,lat))
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/verificar_revisao_cnes_sih_teco.py, linhas 71-77.

```python
for row in sel.itertuples():
    assert monthly[monthly.CNES.eq(row.CNES)].INTERNACOES.sum()==row.INT_15_26
    assert annual[annual.CNES.eq(row.CNES)].INTERNACOES.sum()==row.INT_15_26
    assert len(monthly[monthly.CNES.eq(row.CNES)])==141
    assert set(annual[annual.CNES.eq(row.CNES)].ANO)==set(range(2015,2027))
g=gpd.read_file(P/'02_camadas/01_cnes_bacias/cnes_2026.shp')
assert g.loc[g.SIH_HIST.eq(0),['INT_FONTE','INT_15_26','INT_24_26']].isna().all().all()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/verificar_traducao_relatorio_teco.py

Verificar traducao relatorio teco. Conferência/teste. A organização passa por __init__, handle_starttag.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\teco\codigo\verificar_traducao_relatorio_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html.parser | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pypdf | Leitura, montagem e inspeção de PDFs; não substitui a conferência visual das páginas. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| urllib.parse | Requisições e manipulação de endereços de serviços públicos. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/teco/tmp/relatorio_detalhado/arquivo_anterior.txt — chamada .read_text, linha 29.
- (T / 'arquivo_anterior.txt').read_text('utf8')/entrega_final.zip — chamada zipfile.ZipFile, linha 31.
- {p} — chamada p.read_bytes, linha 36.
- E:/teco/entrega_final/TECO_Consolidado.qgz — chamada zipfile.ZipFile, linha 38.
- E:/teco/entrega_final/00_documentacao/Relatorio_TECO.docx — chamada zipfile.ZipFile, linha 43.
- E:/teco/entrega_final/index.html — chamada .read_text, linha 54.
- E:/teco/entrega_final/00_documentacao/Referencias_metodologia_TECO.json — chamada .read_text, linha 65.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/Validacao_relatorio_idioma.json — chamada .write_text, linha 66.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| Links() | 58-61 | Chamadas efetivas: .__init__, super |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/verificar_traducao_relatorio_teco.py, linhas 59-66.

```python
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  self.links += [v for k,v in attrs if k in ['href','src'] and v]
parser=Links();parser.feed(html)
for link in parser.links:
 if not link.startswith(('http','#','data:')):assert (F/unquote(link.split('#')[0])).exists(),link
check={'data':__import__('datetime').datetime.now().astimezone().isoformat(),'status':'APROVADO','arquivos_de_dados_identicos_ao_pacote_anterior':count,'camadas_qgis':len(root.findall('.//projectlayers/maplayer')),'layouts_qgis':len(root.findall('.//Layouts/Layout')),'idioma_apresentacao':'English display; stable field codes and original values retained','paginas_relatorio':len(pdf.pages),'links_para_mapas_no_word':local_count,'links_indice':len(parser.links),'tabelas_relatorio':8,'referencias':len(json.loads((D/'Referencias_metodologia_TECO.json').read_text('utf8')))}
(D/'Validacao_relatorio_idioma.json').write_text(json.dumps(check,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(check,ensure_ascii=False))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/visualizar_conferencia_unidades_teco.py

Visualizar conferencia unidades teco. Processamento ou módulo de apoio. A organização passa por main.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\codigo\visualizar_conferencia_unidades_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/teco/output/05_auditoria_saude/refino/Dados_da_conferencia.json — chamada .read_text, linha 30.
- E:/teco/output/05_auditoria_saude/refino/Totais_mensais_por_unidade.csv — chamada pd.read_csv, linha 30.

**Saídas.**

- E:/teco/output/05_auditoria_saude/refino/Conferencia_unidades.html — chamada .write_text, linha 47.

**Campos e chaves lidos.**

- p: unidades.
- u: CNES.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 29-47 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/visualizar_conferencia_unidades_teco.py, linhas 29-37.

```python
def main():
 p=json.loads((O/'Dados_da_conferencia.json').read_text('utf8'));units=p['unidades'];monthly=pd.read_csv(O/'Totais_mensais_por_unidade.csv',sep=';',dtype={'CNES':str});idx={u['CNES']:i for i,u in enumerate(units)}
 rows=[[idx[r.CNES],int(r.ANO)-2016,int(r.MES)-1,int(r.PROD_TOTAL),int(r.PROD_AB),int(r.RES_TOTAL),int(r.RES_AB)] for r in monthly.itertuples()]
 heads=['CNES','Estabelecimento','Produção total','Produção A+B','Residentes: total NRMG','Residentes: A+B','Localização']
 page='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TECO | internações por unidade</title><style>
body{font:16px Arial;margin:0;background:#f3f6f6;color:#213d46}main{max-width:1450px;margin:auto;padding:28px}h1{margin-bottom:8px}p{line-height:1.6}.card{background:white;padding:22px;margin:20px 0;border:1px solid #d6e1e3;border-radius:8px}.stats{display:flex;gap:30px;flex-wrap:wrap}.stats b{font-size:26px;display:block;color:#246277}label{display:block;font-weight:bold}input,select{width:100%;padding:10px;margin:8px 0 15px;box-sizing:border-box;font:15px Arial}.filters{display:grid;grid-template-columns:2fr 1fr;gap:20px}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:10px;border-bottom:1px solid #d6e1e3}th{background:#244d5c;color:white;position:sticky;top:0}td.num{text-align:right;white-space:nowrap}.scroll{max-height:510px;overflow:auto}button{border:0;padding:0;background:none;color:#145d7b;cursor:pointer;text-align:left;font:inherit}.note{background:#fff6df;padding:14px;border-left:4px solid #b98235}.plots{display:grid;grid-template-columns:1fr 1fr;gap:20px}svg{width:100%;height:auto}.small{font-size:13px;color:#536c75}a{color:#18637d}@media(max-width:800px){.plots,.filters{display:block}main{padding:12px}}</style><main>
<h1>Internações por estabelecimento</h1><p>2016-2025 · competência de processamento · SIH/SUS. Produção do hospital e residência dos pacientes são recortes diferentes. Produção total refere-se ao SIH/SUS e não inclui toda a assistência particular ou por planos.</p>
<div class="card stats"><div><b>383</b>unidades que atenderam residentes dos quatro municípios</div><div><b>12.242.560</b>internações dessas unidades, todas as origens</div><div><b>2.038.486</b>internações no recorte residencial do NRMG</div></div>
<p class="note">199 unidades têm até dez internações de residentes de BH, Contagem, Betim e Ibirité no decênio. Somente três dessas 383 unidades têm até dez internações na produção total. As pequenas contagens decorrem principalmente do recorte residencial, não de falta geral de registros.</p>
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## sub_bacia/delimitar_subbacias_teco.py

Executa no QGIS/GRASS a delimitação contribuinte dos reservatórios com MDE reprojetado, direção D8, escolha de exutório e r.water.outlet, com conferência de alinhamento e reaproveitamento condicionado de intermediários.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\teco\sub_bacia\delimitar_subbacias_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| builtins | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_teco | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| osgeo | Interfaces GDAL/OGR para rasters e vetores; usadas também na validação de projeção e grade. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| qgis.PyQt.QtCore | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| qgis.core | API PyQGIS para camadas, simbologia, metadados, árvore do projeto e layouts. Exige o Python do QGIS. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |
| traceback | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

- E:/teco/sub_bacia/{chave}/config_processamento.json — chamada stamp.read_text, linha 1051.

**Saídas.**

- E:/teco/sub_bacia/andamento_processamento.log — chamada ARQ_LOG.open, linha 124.
- E:/teco/sub_bacia/estado_execucao.json — chamada .write_text, linha 924.
- E:/teco/sub_bacia/{chave}/config_processamento.json — chamada stamp.write_text, linha 1059.
- d['pasta']/watershed.ok — chamada .write_text, linha 1109.
- E:/teco/sub_bacia/shapefiles_v6_datetime.now().strftime('%Y%m%d_%H%M%S')/relatorio_bacias_v6.csv — chamada .open, linha 1377.

**Campos e chaves lidos.**

- item: acumulacao, celulas_lago.
- a: acumulacao, bacia_exclusiva, celulas_lago, dist_hidro, elevacao, id, x, y.
- feat: DN.
- r: area_exclusiva_km2, area_removida_km2, bacia, id, reservatorio_geom.
- outro: id, reservatorio_geom.
- x: bacia, id.
- outra: bacia_exclusiva.
- b: bacia_exclusiva, id.
- data: acum, bacia, bruto, dem, direcao.
- resultado: cobertura_pct, path.
- d: acum, alternativas, area_exclusiva_km2, area_km2, area_removida_km2, bacia, bacia_exclusiva, bbox, bruto, candidatos, chave, dem, direcao, exutorio, geom, id, incl_pct, inclusao_exclusiva_pct, nome, pasta, resultado, situacao.
- dados: candidatos, frac_eleito, n_saidas, pixels_aporte_adicional, pixels_lago, pixels_lago_brutos.
- candidato: x, y.
- escolhido: acumulacao, frac_lago, x, y.
- ex: acumulacao, metodo, x, y.

**Campos e chaves gerados.**

- r: area_exclusiva_km2, area_removida_km2, bacia_exclusiva, inclusao_exclusiva_pct.
- c: celulas_lago, frac_lago, metodo.
- candidato: dist_hidro.
- escolhido: celulas_lago, frac_lago, metodo.
- d: alternativas, exutorio, resultado.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _log_somente_arquivo(msg) | 114-117 | Chamadas efetivas: PASTA_RESULTADOS.mkdir, ARQ_LOG.open, fp.write, .format, .strftime, datetime.now |
| log(msg) | 120-125 | Chamadas efetivas: print, PASTA_RESULTADOS.mkdir, ARQ_LOG.open, fp.write, datetime.now |
| arquivo_raster_valido(arquivo) | 128-136 | Chamadas efetivas: gdal.Open, str, arquivo.is_file, arquivo.stat Retorno: valido, False. |
| _srs_dataset(ds, descricao) | 139-146 | Chamadas efetivas: ds.GetProjection, osr.SpatialReference, RuntimeError, srs.ImportFromWkt, str Retorno: srs. |
| _conferir_crs_raster(ds, descricao) | 149-158 | Chamadas efetivas: osr.SpatialReference, destino.SetFromUserInput, _srs_dataset, bool, RuntimeError, origem.IsSame, .format, origem.ExportToProj4 |
| validar_grade_utm(arquivo, referencia=None) | 161-173 | Chamadas efetivas: gdal.Open, _conferir_crs_raster, str, RuntimeError, _conferir_grade |
| obter_algoritmo_grass(nome) | 176-183 | Chamadas efetivas: QgsApplication.processingRegistry, registro.algorithms, RuntimeError, .startswith, alg.id, .split, .lower, .id Retorno: alg.id(). |
| unir_geometrias_utm(caminho, crs_alvo) | 186-206 | Chamadas efetivas: QgsVectorLayer, QgsCoordinateTransform, lyr.getFeatures, QgsGeometry.unaryUnion, str, RuntimeError, lyr.crs, QgsProject.instance Retorno: geom. |
| bbox_para_recorte(geom) | 209-223 | Chamadas efetivas: QgsRectangle, bb.grow, log, geom.boundingBox, math.floor, math.ceil, int, RuntimeError Retorno: (xmin, ymin, xmax, ymax). |
| hidro_local(caminho, area, crs_alvo) | 226-243 | Chamadas efetivas: QgsVectorLayer, QgsCoordinateTransform, QgsRectangle, busca.grow, .setFilterRect, layer.getFeatures, str, RuntimeError Retorno: QgsGeometry.unaryUnion(geoms) if geoms else None. |
| mascara_anel(geom, geotransform, width, height, projecao) | 246-262 | Chamadas efetivas: .Create, ds.SetGeoTransform, ds.SetProjection, .Fill, .CreateDataSource, memoria.CreateLayer, ogr.Feature, ft.SetGeometry Retorno: a. |
| _mascara_lago_gdal(dataset, geom_wkb) | 265-283 | Chamadas efetivas: .Create, mem.SetGeoTransform, mem.SetProjection, .Fill, .CreateDataSource, fonte.CreateLayer, ogr.Feature, feature.SetGeometry Retorno: mask. |
| _conferir_grade(ds, outro) | 286-293 | Chamadas efetivas: _conferir_crs_raster, RuntimeError, np.allclose, ds.GetGeoTransform, outro.GetGeoTransform |
| _destinos_d8(direcao) | 296-310 | Chamadas efetivas: direcao.reshape, np.full, D8_OFFSETS.items, np.flatnonzero, .astype Retorno: downstream. |
| _tarefa_encontrar_saida(task, direcao, acumulacao, geom_wkb) | 313-381 | Chamadas efetivas: gdal.Open, _conferir_grade, _mascara_lago_gdal, .ReadAsArray, _destinos_d8, lake.reshape, np.flatnonzero, enumerate Retorno: {'candidatos': candidatos[:max(NUM_CANDIDATOS, 30)], 'n_saidas': len(candidatos), 'pixel_lago': int(len(lakeidx)), 'frac_eleito': candidatos[0]['frac_lago']}, out. |
| _criar_raster_binario(alvo, origem_ds, array) | 384-398 | Chamadas efetivas: Path, path.exists, .Create, out.SetGeoTransform, out.SetProjection, .WriteArray, .SetNoDataValue, out.FlushCache |
| _poligonizar_mascara_geopackage(task, origem_ds, area_bool, destino) | 401-440 | Chamadas efetivas: Path, destino.exists, origem_ds.GetGeoTransform, origem_ds.GetProjection, .Create, mem.SetGeoTransform, mem.SetProjection, .WriteArray |
| _tarefa_bacia_com_lago(task, raster_bacia, raster_direcao, wkb_res, original_gpkg, corrigido_gpkg, corrigido_tif) | 443-491 | Chamadas efetivas: gdal.Open, _conferir_grade, _mascara_lago_gdal, .ReadAsArray, _destinos_d8, np.full, np.flatnonzero, task.setProgress Retorno: dict(pixels_brutos=int(basin.sum()), pixels_integrados=int(integrado.sum()), pixels_lago=int(lake.sum()), pixels_lago_brutos=int((basin & lake).sum()), pixels_aporte_adicional=int((integrado & ~basin). |
| escolher_candidatos(geom_res, geom_hidro, arquivo_acum, arquivo_dem) | 494-551 | Chamadas efetivas: gdal.Open, ds.GetGeoTransform, dem.GetGeoTransform, .difference, ring.boundingBox, max, min, .astype Retorno: (achados, eleito). |
| ajuste_manual(ponto, raster) | 554-577 | Chamadas efetivas: gdal.Open, ds.GetGeoTransform, max, .astype, .GetNoDataValue, np.where, np.unravel_index, dict Retorno: dict(x=gt[0] + (col + 0.5) * gt[1], y=gt[3] + (row + 0.5) * gt[5], acumulacao=float(val[i, j]), acumulacao_negativa=bool(arr[i, j] < 0), elevacao=None, dist_hidro=None, metodo='manual_snap_60m'). |
| camada_memoria(tipo, nome, campos) | 580-586 | Chamadas efetivas: QgsVectorLayer, .addAttributes, ly.updateFields, ly.isValid, RuntimeError, ly.dataProvider, QgsField Retorno: ly. |
| adicionar_feat(ly, geom, attrs) | 589-595 | Chamadas efetivas: QgsFeature, f.setGeometry, f.setAttributes, .addFeatures, ly.fields, RuntimeError, ly.dataProvider, ly.name |
| gravar_gpkg(ly, arquivo, nome_camada, novo_arquivo=True) | 598-608 | Chamadas efetivas: QgsVectorFileWriter.SaveVectorOptions, QgsVectorFileWriter.writeAsVectorFormatV3, str, .transformContext, RuntimeError, QgsProject.instance |
| toca_borda(poly, dem_raster, margem_m=90) | 611-619 | Chamadas efetivas: gdal.Open, ds.GetGeoTransform, poly.boundingBox, str, bb.xMinimum, bb.xMaximum, bb.yMinimum, bb.yMaximum Retorno: bb.xMinimum() <= xmin + margem_m or bb.xMaximum() >= xmax - margem_m or bb.yMinimum() <= ymin + margem_m or (bb.yMaximum() >= ymax - margem_m). |
| gravar_shapefile(layer, caminho) | 622-634 | Chamadas efetivas: Path, caminho.parent.mkdir, QgsVectorFileWriter.SaveVectorOptions, QgsVectorFileWriter.writeAsVectorFormatV3, str, .transformContext, RuntimeError, .format Retorno: caminho. |
| _adicionar_shp_ao_projeto(caminho, nome, visivel=True, tipo='bacia') | 637-671 | Chamadas efetivas: .lower, QgsProject.instance, list, QgsVectorLayer, projeto.addMapLayer, projeto.layerTreeRoot, raiz.findGroup, grupo.insertLayer |
| _tarefa_warp(task, origem, destino, bbox) | 674-719 | Chamadas efetivas: Path, final.with_name, provis.exists, gdal.WarpOptions, gdal.Warp, _conferir_crs_raster, ds.GetRasterBand, b.ReadAsArray Retorno: {'path': str(final), 'cobertura_pct': pct}, 1. |
| _tarefa_poligonizar(task, origem, saida) | 722-759 | Chamadas efetivas: Path, destino.exists, gdal.Open, ds.GetRasterBand, band.ReadAsArray, .astype, int, .Create Retorno: {'gpkg': str(destino), 'num_pixels_bacia': n}, 1. |
| _somente_poligonos(geom, descricao='geometria') | 762-777 | Chamadas efetivas: geom.isEmpty, geom.isNull, RuntimeError, geom.isGeosValid, geom.makeValid, QgsWkbTypes.geometryType, QgsWkbTypes.isMultiType, geom.convertToMultiType Retorno: geom. |
| _ler_poligonos_intermediarios(caminho, crs_alvo) | 780-800 | Chamadas efetivas: QgsVectorLayer, log, layer.getFeatures, _somente_poligonos, str, RuntimeError, .format, layer.crs Retorno: _somente_poligonos(geom, str(caminho)). |
| _verificar_intersecao_reservatorio(poly, res, caminho) | 803-821 | Chamadas efetivas: log, res.area, RuntimeError, poly.boundingBox, res.boundingBox, .format, bbp.intersects, bbp.xMinimum Retorno: porcentagem. |
| _resolver_sobreposicoes(resultados) | 824-867 | Chamadas efetivas: range, sorted, enumerate, len, _somente_poligonos, poly.area, max, alocadas.append Retorno: resultados. |
| ExecucaoBaciasTECO() | 870-1398 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de sub_bacia/delimitar_subbacias_teco.py, linhas 216-222.

```python
    w, h = int(round((xmax-xmin)/RESOLUCAO_M)), int(round((ymax-ymin)/RESOLUCAO_M))
    log(f"Janela: {w} x {h} celulas; {w*h:,} pixels (buffer {BUFFER_M/1000:.0f} km)")
    if w*h > MAX_CELULAS:
        raise RuntimeError(
            f"Recorte com {w*h:,} pixels acima de MAX_CELULAS={MAX_CELULAS:,}. "
            "Reduza BUFFER_M ou aumente MAX_CELULAS conscientemente."
        )
```

Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

Trecho de sub_bacia/delimitar_subbacias_teco.py, linhas 670-676.

```python
    layer.triggerRepaint()
    log('SHP ADICIONADO AO QGIS: {}'.format(layer.name()))

# Tarefa warp
def _tarefa_warp(task, origem, destino, bbox):

    final = Path(destino)
```

Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

**Cálculos a observar nesta rotina.**

- log: Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 
