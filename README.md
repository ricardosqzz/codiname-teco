# Reservatórios urbanos | Pressão antrópica

[Visualizador online](https://ricardosqzz.github.io/codiname-teco/) · [Códigos e cálculos](https://ricardosqzz.github.io/codiname-teco/codigos/)

## Organização

- `codigo/`: rotinas atuais e dependências locais.
- `config/`: parâmetros de análise, quando aplicáveis.
- `dados/`: derivados mínimos e estatísticas consolidadas.
- `docs/`: visualizador e prévias para navegação.
- `documentacao/codigos/`: documentação por rotina.

As bases brutas, ambientes de programação, arquivos horários volumosos, cópias descontinuadas e documentos temporários não são duplicados. Ajuste `codigo/caminhos_projeto.json` e instale `codigo/requirements-calculo.txt` para usar outra árvore de dados. Rotinas de geração completa exigem as fontes documentadas nos cabeçalhos.

## Reprodução da classificação

Execute `python codigo/reproduzir_analise_configuravel.py`. O cenário base utiliza os derivados publicados. Novas variáveis exigem declarar campo, unidade, agregação, transformação e peso em `config/analise_extensivel.json`. Os resultados são exploratórios e não estimam genes ou risco individual.

## Complementação microplásticos

[Metodologia, mapas e guia dos códigos](https://ricardosqzz.github.io/codiname-teco/microplasticos/). Dois temas separados: ARG preservado e fontes potenciais de microplásticos. Dados derivados e shapefiles em `dados/microplasticos/`. Execute `python codigo/reproduzir_microplasticos.py` para reproduzir MCDA, k-means e Moran a partir dos derivados publicados. As consultas de origem e os caminhos D8 exigem as bases locais indicadas nos cabeçalhos. Licenciamento é catálogo de triagem, sem peso no índice até validar cobertura municipal e operação.
