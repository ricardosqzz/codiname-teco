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
