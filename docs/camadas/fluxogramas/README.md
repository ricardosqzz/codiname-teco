# Fluxo das camadas no QGIS

O fluxograma acompanha o encadeamento dos arquivos existentes, sem recalcular os indicadores. A primeira página mostra as entradas e a derivação dos dois índices. A segunda mostra relevo, conectividade e camadas complementares.

No QGIS, abra o layout **Workflow | Layers** pelo Gerenciador de Layouts. Ele contém duas páginas A3 e foi incluído em projeto_teco.qgz e entrega_final/TECO_Consolidado.qgz. Os arquivos SVG desta pasta devem acompanhar os projetos, pois o layout os referencia.

| Produto | Uso |
| --- | --- |
| 01_Entradas_indices.svg | Entradas, agregação em 500 m, normalização, índices, k-means, Moran e sensibilidade. |
| 02_Contexto_conectividade.svg | Relevo, caminhos D8, pressão a montante e camadas de interpretação. |
| Fluxo_camadas_QGIS.pdf | Duas páginas vetoriais com texto pesquisável, prontas para leitura ou impressão. |
| Fluxo_camadas_QGIS.png e Fluxo_camadas_QGIS_2.png | Imagens exportadas do layout para uso em apresentações. |
| Auditoria_fluxogramas.json | Verificação das camadas preservadas e identificação dos arquivos. |
| Camadas_representadas.json | Relação das famílias de entrada com arquivos e campos documentados. |

População e esgotamento participam dos dois temas com definições distintas. AIH_LOCAL integra a base atual de resistência e representa a atividade hospitalar de todas as causas; os subconjuntos bacterianos permanecem em produtos separados. Coleta de lixo e densidade de vias integram a avaliação de microplásticos. Uso do solo, licenças, infraestrutura e pontos amostrais contextualizam os resultados, sem um peso adicional automático.

O k-means recebe a matriz de variáveis transformadas e normalizadas, com os pesos de cada cenário. O Moran recebe o índice S0 e uma matriz de vizinhança. O D8 recebe o relevo e fornece conexões topográficas, posteriormente combinadas aos índices para sínteses a montante. Essas três análises respondem a perguntas diferentes.

O fluxograma é documental. As rotinas de cálculo são executadas em Python e nas ferramentas SIG indicadas no guia; esta figura não é um arquivo executável do Modelador Gráfico.
