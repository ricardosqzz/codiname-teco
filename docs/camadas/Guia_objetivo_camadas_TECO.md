# Guia das camadas dos reservatórios urbanos

Este guia resume o que cada camada representa e como ela participa das avaliações de pressão potencial associadas a genes de resistência a antimicrobianos e a microplásticos. As análises compartilham a base territorial, mas mantêm índices separados. Os resultados orientam a investigação de fontes e rotas possíveis, sem estimar concentração, carga transportada ou probabilidade de contaminação. Conferência de 19/11/2026.

## Base territorial e informações nas unidades originais

| Camada | O que representa | Como é utilizada |
| --- | --- | --- |
| Bacias | Áreas contribuintes de Pampulha, Vargem das Flores e Ibirité / REGAP, delimitadas a partir do relevo e dos exutórios adotados. | Define o recorte e a identidade BACIA. Não corresponde ao limite dos setores do IBGE. |
| Reservatórios e exutórios | Espelhos d'água e pontos de saída da drenagem. | Destino e referência da conectividade topográfica. O exutório tem função diferente do ponto de coleta. |
| Pontos de coleta e microcosmos | Locais de amostragem e de experimentos in situ, representados por gota e losango. | Relaciona os resultados espaciais ao desenho amostral. Não entra como fonte de pressão no índice. |
| População do Censo 2022 | Pessoas por setor. POP_OFIC é o total do setor inteiro; POP_REC é a estimativa no recorte da bacia. | POP_REC usa rateio pela fração de área. POP_DENS representa habitantes/km² no suporte analítico. Não se somam subgrupos do IBGE ao total V0001. |
| Esgotamento do Censo 2022 | REDE_PCT é o percentual ligado à rede geral/pluvial ou a fossa ligada à rede. SEM_REDE é seu complemento. | Indica condições domiciliares de destinação. Ausência de rede não comprova ausência de tratamento, e rede não comprova tratamento efetivo. Lacunas permanecem nulas. |
| Uso e cobertura da terra 2025 | Classes de ocupação nas suas geometrias e unidades originais. | Contextualiza urbanização, vegetação e superfícies. Não recebe um peso adicional no índice atual de microplásticos. |
| Vias | Rede mapeada, distinguindo classes viárias quando disponíveis. | Compõe o fundo cartográfico. ROAD_DENS também entra no índice de microplásticos. A geometria viária não comprova direção do escoamento pluvial. |
| Cursos d'água | Drenagem superficial mapeada. | Contextualiza possíveis conexões com os reservatórios. Não é a rede de esgoto nem informa vazão de efluentes. |
| Hipsometria e declividade | Altitude em metros e inclinação em %, derivadas do Copernicus GLO-30. | Descreve o relevo. A declividade usa classes Embrapa. Não funciona como uma fonte adicional de contaminantes. |
| Distâncias e caminhos D8 | Distância direta ou percurso hidrológico, identificados separadamente. D8 encaminha o fluxo para um de oito pixels vizinhos. | Indica conectividade topográfica potencial. Não simula galerias, vazão, retenção ou transporte real de genes e partículas. |

## Saúde e informações específicas da resistência

| Camada | O que representa | Como é utilizada |
| --- | --- | --- |
| Estabelecimentos CNES e atividade SIH | Localização cadastral cruzada com registros hospitalares, mantendo a identificação de cada unidade. | A seleção de atividade recente evita usar indiscriminadamente cadastros sem produção. Não define a área oficial atendida pelo hospital. |
| Internações por local de internação | Produção hospitalar de 2016-2025, preservando o total e os subconjuntos diagnósticos. | AIH_LOCAL usa a média anual de todas as causas na base atual. O filtro bacteriano é um produto separado, sem comprovar resistência, presença de genes ou residência dos pacientes. |
| Consulta por residência municipal | Internações de residentes dos municípios consultados, com sua origem municipal preservada. | Produto complementar para conferir universo e deslocamentos. Não redistribui automaticamente internações a bairros, CEPs ou círculos de 500 m. |
| Rede cadastral de BH e ETE | Traçados e unidades de saneamento disponíveis nos cadastros utilizados. | Contextualiza infraestrutura e possíveis conexões. Ausência de traçado fora de BH não significa ausência de rede. Não há carga medida atribuída às ETE. |

## Resíduos e informações específicas de microplásticos

| Camada | O que representa | Como é utilizada |
| --- | --- | --- |
| Destinação do lixo do Censo 2022 | Domicílios com coleta e com outras destinações, como queima, enterramento ou descarte em terreno. | WASTE_DENS estima domicílios sem coleta municipal por km². Sigilo não é zero; intervalos e estimativas adotadas permanecem identificados. Não mede massa de plástico descartada. |
| Aterros e outros destinos cadastrados | Instalações de destinação e manejo identificadas nos dados consultados. | Camada de contexto e investigação documental. Localização não comprova emissão de microplásticos nem recebimento dos resíduos de toda a bacia. |
| Coleta seletiva e planos municipais | Declarações e instrumentos municipais disponíveis. | Informa gestão e lacunas. Não representa uma cobertura domiciliar detalhada ou uma rota de caminhões. |
| Licenciamento por tipologia | Registros de processos estaduais intersectados com as bacias, com tipologia e vínculo documental. | Orienta a investigação de atividades potencialmente relevantes. Os 49 registros são processos, não necessariamente 49 empresas ativas. TP_CODE e MP_LINK não recebem peso no índice atual. |

## Suporte da classificação e entradas dos índices

Os mapas de entrada mantêm suas unidades originais. A combinação é feita em vizinhanças com raio aproximado de 500 m, recortadas pelas bacias, e apresentada em hexágonos sem sobreposição. Os círculos podem se sobrepor, portanto seus totais não devem ser somados para obter a população da bacia. O resultado deve ser relacionado pela chave composta GRID_ID e BACIA. Nos dados de esgotamento, os valores observados permanecem separados das estimativas adotadas para preencher lacunas no suporte analítico, com indicadores de cobertura e de estimação.

No índice de resistência, o cenário-base combina POP_DENS, SEM_REDE e AIH_LOCAL com pesos iguais. População e atividade hospitalar passam por log1p; o percentual sem rede mantém sua transformação identidade. As entradas são normalizadas por min-max na base elegível. São indicadores indiretos de pressão antrópica, sem comprovação de resistência microbiológica.

No índice de microplásticos, o cenário-base combina POP_DENS, SEWER_DENS, WASTE_DENS e ROAD_DENS com pesos iguais. SEWER_DENS é a densidade de domicílios sem conexão à rede; difere do percentual SEM_REDE usado no outro índice. As quatro entradas passam por log1p e normalização min-max conjunta nas três bacias. Relevo, licenças, ETE e destinos de resíduos não são parcelas adicionais dessa média.

## Como ler as saídas

| Produto | Pergunta respondida | Interpretação |
| --- | --- | --- |
| Índice multivariado | Onde os indicadores combinados são maiores? | Média ponderada das entradas normalizadas, apresentada de 0 a 100. Os dois temas não são somados. |
| Classes fixas e quintis | Como resumir o índice? | Classes fixas usam cortes 20, 40, 60 e 80. Quintis usam P20, P40, P60 e P80 da distribuição. Uma classe não equivale à outra. |
| Cenários e estabilidade | Quanto a classificação depende dos pesos? | Compara o cenário de pesos iguais com maior peso para variáveis selecionadas ou retirada de uma delas. Concordância não é probabilidade de acerto. |
| K-means | Quais áreas têm combinações semelhantes de atributos? | Usa a matriz de entradas transformadas e normalizadas, e não apenas o índice final. Os grupos são perfis multivariados; seus números não são níveis automáticos de contaminação. |
| Moran global e local | Valores semelhantes estão espacialmente associados? | Alto-alto e baixo-baixo indicam associações locais significativas; alto-baixo e baixo-alto indicam contrastes. Não significativo não significa ausência de pressão. |
| Conectividade a montante | Que pressão potencial existe no terreno contribuinte? | Resume o índice nas áreas conectadas pelo relevo. Não equivale a concentração no reservatório nem a uma pluma transportada. |

Nos produtos de microplásticos, os campos principais são MP_INDEX, MP_CLASS, MP_QUINT, MP_K, MP_STAB e MP_MORAN, para índice, classes fixas, quintis, agrupamento, estabilidade e associação local, respectivamente. As siglas devem ser verificadas no dicionário da camada antes de combinar tabelas de versões diferentes.

## Ferramentas e limites da leitura

Os tratamentos tabulares e espaciais usam Python, com NumPy, pandas, GeoPandas e Shapely. O k-means é executado com SciPy. As rotinas de Moran e de sensibilidade são próprias do projeto e usam os parâmetros registrados em cada produto. O QGIS organiza a visualização, simbologia e encartes. A delimitação hidrológica adotada usa ferramentas GRASS GIS, incluindo r.watershed e r.water.outlet. A direção D8 descreve o relevo e não é calculada pelo k-means ou por Moran.

A principal limitação é a combinação de fontes com períodos, resolução e cobertura distintos. O rateio por área pode representar mal a distribuição real da população dentro de setores extensos. As internações são uma aproximação da atividade hospitalar, e o cadastro de licenciamento ainda precisa de complementação municipal. Essas condições devem acompanhar a leitura das manchas de maior pressão.

Os detalhes estão no Dicionario_dos_campos, nas fichas dos scripts e no relatório metodológico. Referências de implementação incluem o [k-means do SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans2.html), o [r.watershed do GRASS GIS](https://grass.osgeo.org/grass-stable/manuals/r.watershed.html) e o [r.water.outlet](https://grass.osgeo.org/grass-stable/manuals/r.water.outlet.html).
