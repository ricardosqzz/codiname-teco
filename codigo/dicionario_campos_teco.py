# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entradas: argumentos do chamador e módulos locais relacionados no relatório.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
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
import re

DEFINICOES = {
    'id': ('Identificador da bacia hidrográfica: pampulha, vargem_flores ou ibirite_regap.', 'código'),
    'BACIA': ('Identificador da bacia à qual pertence a feição ou o recorte: pampulha, vargem_flores ou ibirite_regap.', 'código'),
    'bacia': ('Identificador da bacia em que foi traçada a trajetória topográfica D8.', 'código'),
    'reserv': ('Nome do reservatório associado à delimitação da bacia ou ao exutório de referência.', 'texto'),
    'area_km2': ('Área da bacia exclusiva, após retirar sobreposições entre as três bacias, calculada em SIRGAS 2000 / UTM 23S.', 'km²'),
    'orig_km2': ('Área da bacia integrada e suavizada antes do ajuste que elimina sobreposições com as outras bacias.', 'km²'),
    'reduz_km2': ('Área retirada da delimitação original para resolver sobreposições entre bacias; corresponde à diferença entre orig_km2 e area_km2, limitada a valores não negativos.', 'km²'),
    'incl_pct': ('Percentual da área do espelho do reservatório que permanece incluído na bacia exclusiva: 100 × área da interseção entre bacia e reservatório / área do reservatório. Não é percentual da bacia original preservada.', '% do reservatório'),
    'situacao': ('Registro das verificações da delimitação, incluindo integração das áreas contribuintes do lago, possível truncamento do MDE e ajuste de sobreposição entre bacias.', 'texto'),
    'NOME': ('Nome do reservatório representado pelo polígono.', 'texto'),
    'NOME_BACIA': ('Nome do reservatório que identifica a bacia do trecho de rede ou da estação de tratamento.', 'texto'),
    'setor_id': ('Código IBGE de 15 dígitos do setor censitário de origem, armazenado como texto. O mesmo setor pode ter recortes em bacias diferentes.', 'código'),
    'POP_OFIC': ('Total oficial de pessoas do setor censitário inteiro no Censo 2022, equivalente à variável básica V0001. Não se restringe ao recorte do setor dentro da bacia.', 'pessoas'),
    'POP_REC': ('População estimada no recorte do setor dentro da bacia: população do setor inteiro × fração da área do setor interceptada pela bacia.', 'pessoas estimadas'),
    'DENS_POP': ('Densidade populacional do setor inteiro: total oficial de pessoas / área original do setor em km². O valor é mantido nos recortes do mesmo setor.', 'pessoas/km²'),
    'DOM_TOT': ('Domicílios particulares permanentes ocupados do setor inteiro, variável V00001 da tabela Características do Domicílio - Parte 1 do Censo 2022. Ausências e sigilo não são convertidos em zero.', 'domicílios'),
    'DOM_REDE': ('Domicílios particulares permanentes ocupados do setor com destinação à rede geral ou pluvial (V00309) ou a fossa séptica/filtro ligada à rede (V00310). A soma exige disponibilidade das duas parcelas e não comprova tratamento do esgoto.', 'domicílios'),
    'REDE_PCT': ('Percentual observado de domicílios do setor com rede geral/pluvial ou fossa ligada à rede: 100 × (V00309 + V00310) / V00001. Denominador zero, ausência ou sigilo das parcelas permanecem nulos.', '% dos domicílios'),
    'SEM_REDE_OBS': ('Percentual observado de domicílios do setor sem rede geral/pluvial ou fossa ligada à rede: 100 − REDE_PCT. Mantém as lacunas de publicação; não mede diretamente falta de tratamento.', '% dos domicílios'),
    'DESC_RIO': ('Percentual de domicílios do setor com destinação à vala OU a rio, lago, córrego ou mar: 100 × (V00313 + V00314) / V00001. Exige ambas as categorias publicadas; não representa apenas lançamento em rio.', '% dos domicílios'),
    'REDE_DIR': ('Domicílios particulares permanentes ocupados do setor cuja destinação do esgoto é a rede geral ou pluvial, variável V00309 do Censo 2022.', 'domicílios'),
    'FOSS_REDE': ('Domicílios particulares permanentes ocupados do setor cuja destinação do esgoto é fossa séptica ou fossa filtro ligada à rede, variável V00310 do Censo 2022.', 'domicílios'),
    'FOSS_SREDE': ('Domicílios particulares permanentes ocupados do setor cuja destinação do esgoto é fossa séptica ou fossa filtro não ligada à rede, variável V00311 do Censo 2022.', 'domicílios'),
    'FOSSA_RUD': ('Domicílios particulares permanentes ocupados do setor cuja destinação do esgoto é fossa rudimentar ou buraco, variável V00312 do Censo 2022.', 'domicílios'),
    'VALA': ('Domicílios particulares permanentes ocupados do setor cuja destinação do esgoto é vala, variável V00313 do Censo 2022.', 'domicílios'),
    'RIO_LAGO': ('Domicílios particulares permanentes ocupados do setor cuja destinação do esgoto é rio, lago, córrego ou mar, variável V00314 do Censo 2022.', 'domicílios'),
    'OUTRO': ('Domicílios particulares permanentes ocupados do setor com outra forma de destinação do esgoto, variável V00315 do Censo 2022.', 'domicílios'),
    'SEM_BANH': ('Domicílios particulares permanentes ocupados do setor sem banheiro nem sanitário, categoria V00316 do Censo 2022.', 'domicílios'),
    'SIGILO_N': ('Número de células com símbolo X nas nove variáveis censitárias de esgotamento utilizadas: V00001 e V00309 a V00316. Não é quantidade de domicílios nem de dados ausentes por outros motivos.', 'variáveis com sigilo'),
    'v0001': ('Total de pessoas do setor censitário inteiro, variável básica V0001 do Censo 2022. É o total populacional; as variáveis V0002 a V0009 não devem ser somadas a ele.', 'pessoas'),
    'v0002': ('Total de domicílios do setor censitário inteiro, incluindo particulares permanentes ocupados, vagos ou de uso ocasional, particulares improvisados ocupados e coletivos com ou sem morador, variável básica V0002 do Censo 2022.', 'domicílios'),
    'v0003': ('Total de domicílios particulares do setor censitário inteiro, incluindo permanentes ocupados, vagos ou de uso ocasional e improvisados ocupados, variável básica V0003 do Censo 2022.', 'domicílios'),
    'v0004': ('Total de domicílios coletivos com ou sem morador no setor censitário inteiro, variável básica V0004 do Censo 2022.', 'domicílios'),
    'v0005': ('Média de moradores por domicílio particular ocupado, considerando permanentes e improvisados ocupados no setor inteiro, variável básica V0005 do Censo 2022.', 'pessoas/domicílio'),
    'v0006': ('Percentual de domicílios particulares ocupados imputados pelo IBGE entre os domicílios particulares ocupados do setor inteiro, variável básica V0006 do Censo 2022.', '% dos domicílios particulares ocupados'),
    'v0007': ('Total de domicílios particulares ocupados, permanentes e improvisados, no setor inteiro, variável básica V0007 do Censo 2022. Difere do denominador V00001, que considera apenas permanentes ocupados.', 'domicílios'),
    'v0008': ('Total de domicílios particulares de uso ocasional no setor censitário inteiro, variável básica V0008 do Censo 2022.', 'domicílios'),
    'v0009': ('Total de domicílios particulares permanentes vagos no setor censitário inteiro, variável básica V0009 do Censo 2022.', 'domicílios'),
    'COMP_KM': ('Comprimento da geometria linear após o recorte espacial, medido em SIRGAS 2000 / UTM 23S e dividido por 1.000.', 'km'),
    'ogc_fid': ('Identificador original da feição viária no arquivo de origem; pode repetir-se quando uma via é dividida pelo recorte espacial.', 'identificador'),
    'hier_legal': ('Categoria de hierarquia viária informada na malha original. Expressa a classificação cadastral da via, sem estimar tráfego ou escoamento.', 'categoria'),
    'TIPO_VIA': ('Classe cartográfica derivada de hier_legal: Principal para ARTÉRIA PRIMÁRIA/EXPRESSA; Secundária / coletora para as demais arteriais e coletoras; Local para vias locais; Sem classe cadastrada nos outros casos. Não representa tráfego medido.', 'categoria'),
    'CNES': ('Código de sete dígitos do estabelecimento no Cadastro Nacional de Estabelecimentos de Saúde, armazenado como texto para preservar zeros iniciais.', 'código'),
    'GRUPO': ('Grupo assistencial atribuído ao tipo de estabelecimento CNES; na camada local atual, Hospital / hospital-dia identifica as instituições com produção SIH positiva dentro das bacias.', 'categoria'),
    'TIPO': ('Tipo de estabelecimento informado no CNES, como HOSPITAL GERAL ou HOSPITAL ESPECIALIZADO.', 'categoria'),
    'AIH_TODAS': ('Total de autorizações de internação hospitalar normais (IDENT = 1) processadas no estabelecimento em 2016-2025, todas as causas e todas as origens dos pacientes. É produção hospitalar local, não total de residentes da bacia.', 'internações no período'),
    'AIH_FILT': ('Total de AIH normais processadas no estabelecimento em 2016-2025 com diagnóstico principal incluído no filtro A+B: etiologias bacterianas codificadas ou síndromes compatíveis. Considera pacientes de todas as origens; não confirma resistência antimicrobiana.', 'internações A+B no período'),
    'AIH_ANO': ('Média anual da produção hospitalar selecionada A+B: AIH_FILT / 10 anos, para 2016-2025. Não é média somente dos anos em que houve registro.', 'internações A+B/ano'),
    'QA_MUN': ('Verificação espacial do cadastro CNES: 1 quando o código do município cadastrado coincide com o município obtido pela localização do ponto; 0 quando não coincide.', 'indicador 0/1'),
    'NOME_TABNET': ('Nome do estabelecimento na identificação da rede hospitalar consultada no SIH/TabNet.', 'texto'),
    'MUNICIPIO': ('Código do município de localização do estabelecimento obtido no cadastro hospitalar/CNES. Não é município de residência do paciente.', 'código municipal'),
    'SIT_ESPACIAL': ('Situação da localização do hospital: dentro das bacias, fora das bacias ou coordenada pendente com produção confirmada. Não define a residência nem a área atendida pelos pacientes.', 'categoria'),
    'AIH_NRMG': ('Total oficial de internações, consulta NRMG/SIH por residência, de pacientes dos oito municípios interceptados pelas bacias, atendidos no estabelecimento em 2016-2025. Não se limita à população efetivamente residente nas bacias.', 'internações por residência'),
    'RES_RD': ('Total bruto de AIH normais nos arquivos RD, 2016-2025, com residência nos oito municípios interceptados pelas bacias e atendimento no estabelecimento; inclui códigos de diagnóstico sem correspondência no dicionário utilizado.', 'internações por residência'),
    'DIF_RES': ('Diferença entre o total residencial bruto dos RD e a consulta oficial NRMG do estabelecimento: RES_RD − AIH_NRMG. Preserva divergências de tabulação, em vez de ajustar os totais artificialmente.', 'internações'),
    'AIH_A': ('AIH normais de residentes dos oito municípios, atendidos no estabelecimento em 2016-2025, com diagnóstico principal de etiologia bacteriana explicitamente codificada no filtro A. Não comprova resistência antimicrobiana.', 'internações do filtro A'),
    'AIH_B': ('AIH normais de residentes dos oito municípios, atendidos no estabelecimento em 2016-2025, com diagnóstico principal de síndrome compatível com infecção bacteriana no filtro B, sem confirmação do agente.', 'internações do filtro B'),
    'AIH_AB': ('Soma AIH_A + AIH_B para residentes dos oito municípios em 2016-2025. Constitui o filtro amplo selecionado; não é produção hospitalar de todas as origens.', 'internações do filtro A+B'),
    'MEDIA_ANUAL_AB': ('Média anual do filtro A+B entre residentes dos oito municípios atendidos no estabelecimento em 2016-2025: AIH_AB / 10.', 'internações A+B/ano'),
    'RES_AB': ('AIH normais do filtro A+B entre residentes dos quatro municípios da referência anterior (Belo Horizonte, Betim, Contagem e Ibirité), atendidos no estabelecimento em 2016-2025. Campo histórico mantido na camada local; não é o total dos oito municípios.', 'internações A+B no recorte anterior'),
    'DIST_BACIA_M': ('Menor distância plana entre o ponto de localização do hospital e a união das três bacias, em SIRGAS 2000 / UTM 23S. É zero para pontos internos; não representa percurso rodoviário.', 'm'),
    'metodo': ('Procedimento usado para posicionar o exutório: candidato de saída D8 ou referência cartográfica da margem/hidrografia próxima ao vertedouro de Vargem das Flores.', 'categoria'),
    'utm_e': ('Coordenada leste do ponto de exutório de referência, em SIRGAS 2000 / UTM zona 23S (EPSG:31983).', 'm'),
    'utm_n': ('Coordenada norte do ponto de exutório de referência, em SIRGAS 2000 / UTM zona 23S (EPSG:31983).', 'm'),
    'acum_cel': ('Acumulação de células contribuintes D8 no pixel do exutório candidato original. Nula em Vargem das Flores após a mudança para referência cartográfica; a acumulação do ponto anterior não foi transferida.', 'células de MDE'),
    'status': ('Grau de conferência do exutório: candidato D8 sem verificação independente ou referência cartográfica conferida no EIA COPASA 2025 para Vargem das Flores.', 'texto'),
    'prec_m': ('Resolução/precisão cartográfica aproximada de 30 m adotada para os pontos de referência; não é uma estimativa estatística de erro nem levantamento de campo.', 'm aproximados'),
    'COLETA_ID': ('Nome do ponto fornecido na camada de coleta. LP01-LP03, VF01-VF03 e IB01-IB03 são pontos de amostragem; Microcosm1 e Microcosm2 são locais de experimento in situ.', 'código de ponto'),
    'sit_rede': ('Situação do trecho no cadastro de esgoto de Belo Horizonte: S com rede; N sem rede; NI sem informação; C sobreposição espacial de registros S e N, mantida como conflito.', 'categoria S/N/NI/C'),
    'sit_nome': ('Descrição textual da situação sit_rede: com rede cadastrada, sem rede cadastrada, sem informação ou conflito S/N na origem.', 'texto'),
    'comp_m': ('Comprimento do trecho cadastral de esgoto após consolidar geometrias coincidentes e recortar à interseção entre Belo Horizonte e as bacias.', 'm'),
    'ete_id': ('Identificador da estação de tratamento no cadastro IDE-Sisema utilizado no projeto; não é código CNES.', 'identificador cadastral'),
    'mun_nome': ('Nome do município informado no cadastro IDE-Sisema da estação de tratamento.', 'texto'),
    'fase_lic': ('Fase do licenciamento registrada para a estação de tratamento na base IDE-Sisema consultada.', 'categoria cadastral'),
    'situ_lic': ('Situação do licenciamento registrada para a estação de tratamento na base IDE-Sisema consultada; não foi inferida a partir de sua proximidade ao reservatório.', 'texto cadastral'),
    'GRID_ID': ('Identificador do centro da malha de análise. A combinação GRID_ID + BACIA identifica cada recorte de círculo ou hexágono; um centro pode originar recortes em mais de uma bacia.', 'código'),
    'E': ('Coordenada leste do centro gerador da vizinhança de 500 m em SIRGAS 2000 / UTM 23S. Pode ficar fora do polígono recortado na borda da bacia.', 'm'),
    'N': ('Coordenada norte do centro gerador da vizinhança de 500 m em SIRGAS 2000 / UTM 23S. Pode ficar fora do polígono recortado na borda da bacia.', 'm'),
    'RAIO_M': ('Raio nominal de 500 m do círculo de cálculo e raio externo do hexágono de apresentação antes do recorte à bacia.', 'm'),
    'CENTRO_INT': ('Indicador de posição do centro gerador: 1 se a união das três bacias cobre o centro; 0 se o centro está fora, mas a célula ou vizinhança intercepta a área de estudo.', 'indicador 0/1'),
    'AREA_KM2': ('Área do círculo de cálculo com raio nominal de 500 m, após recorte à respectiva bacia. Refere-se ao suporte de cálculo, inclusive quando apresentada em geometria hexagonal.', 'km²'),
    'AREA_CEL': ('Área do hexágono de apresentação após recorte à bacia, calculada em SIRGAS 2000 / UTM 23S. Difere da área do círculo usado nos cálculos.', 'km²'),
    'AREA': ('Soma das áreas de interseção dos setores censitários com o círculo de cálculo recortado à bacia. Mede a área coberta pela malha censitária no cálculo; pode diferir de AREA_KM2.', 'km²'),
    'POP': ('População estimada dentro do círculo recortado: soma da densidade de pessoas de cada setor inteiro × área da interseção setor-círculo. A distribuição dentro do setor é assumida uniforme.', 'pessoas estimadas'),
    'DOM': ('Domicílios particulares permanentes ocupados estimados no círculo recortado: soma da densidade domiciliar V00001 de cada setor × área da interseção setor-círculo.', 'domicílios estimados'),
    'SEM': ('Domicílios estimados sem rede no círculo recortado: soma dos domicílios alocados por área × percentual analítico sem rede do setor / 100. Inclui os preenchimentos analíticos identificados por EST_ESG.', 'domicílios estimados'),
    'DOM_OBS': ('Domicílios alocados ao círculo em interseções de setores com percentual de rede efetivamente observado/publicado. É o denominador usado para avaliar a cobertura dos dados de esgotamento.', 'domicílios estimados'),
    'SEM_OBS': ('Domicílios estimados sem rede apenas nas interseções com percentual observado: soma de domicílios alocados × (1 − percentual observado de rede / 100).', 'domicílios estimados'),
    'DOM_EST': ('Domicílios alocados ao círculo em setores cujo percentual sem rede foi preenchido na matriz analítica. Identifica o peso domiciliar das estimativas, não uma observação censitária.', 'domicílios estimados'),
    'POP_DENS': ('Densidade populacional estimada na vizinhança recortada: POP / AREA_KM2, em habitantes por km². Calculada no círculo de 500 m, mesmo quando exibida no hexágono.', 'pessoas/km²'),
    'SEM_REDE': ('Percentual analítico de domicílios sem rede na vizinhança: 100 × SEM / DOM, com zero quando DOM = 0. Lacunas setoriais são preenchidas pela mediana do município e situação censitária, com alternativas pela mediana municipal e global; EST_ESG informa a parcela estimada. Lacunas sem denominador válido permanecem nulas.', '% dos domicílios'),
    'SEM_OBS_P': ('Percentual sem rede calculado somente com dados observados na vizinhança: 100 × SEM_OBS / DOM_OBS. Denominador nulo ou zero resulta em valor ausente.', '% dos domicílios observados'),
    'COB_ESG': ('Cobertura de observação do esgotamento no círculo: 100 × DOM_OBS / DOM. Mede disponibilidade do dado publicado, não atendimento por rede; exige-se pelo menos 95% no teste local de Moran.', '% do denominador domiciliar'),
    'EST_ESG': ('Parcela dos domicílios alocados ao círculo cuja informação de esgotamento foi preenchida na matriz analítica: 100 × DOM_EST / DOM.', '% do denominador domiciliar'),
    'SAUDE_N': ('Número de estabelecimentos hospitalares com produção SIH positiva e coordenadas aceitas que interceptam o círculo recortado. Não é número de unidades atendendo exclusivamente os moradores da vizinhança.', 'estabelecimentos'),
    'AIH_LOCAL': ('Soma das médias anuais de internações A+B em 2016-2025 dos hospitais localizados no círculo recortado. Usa produção de pacientes de todas as origens; é uma referência de atividade hospitalar local, não internações dos moradores nem carga de genes.', 'internações A+B/ano'),
    'AIH_ORIG': ('Componente previsto para internações por origem residencial dos pacientes. Permanece nulo enquanto não houver geografia de residência validada; não foi substituído por proximidade de hospitais.', 'internações/ano; não preenchido'),
    'ORIG_STATUS': ('Situação da atribuição das internações à residência dos pacientes. Registra a pendência de geografia de CEP/residência validada; distingue esse componente da atividade hospitalar local.', 'texto'),
    'URB_PCT': ('Percentual de pixels válidos de uso do solo classificados como área urbanizada, código 24, dentro do círculo recortado. O denominador exclui pixels NoData.', '% dos pixels válidos'),
    'USO_N': ('Quantidade de pixels válidos do raster de uso do solo incluídos no círculo recortado, usada como suporte de URB_PCT.', 'pixels'),
    'HIPS_M': ('Média das altitudes válidas do MDE Copernicus no círculo recortado; representa o relevo médio da vizinhança.', 'm de altitude'),
    'DECL_PCT': ('Média da declividade percentual dos pixels válidos no círculo recortado. Declividade percentual corresponde a 100 × razão entre desnível e distância horizontal.', '% de declividade'),
    'DIST_KM': ('Média das distâncias topográficas D8 válidas dos pixels do círculo até o reservatório. Soma passos ortogonais e diagonais da grade do MDE; não é distância pela rede de esgoto nem tempo de transporte.', 'km'),
    'TERRA_PCT': ('Percentual da área geométrica do círculo recortado que fica fora dos polígonos dos reservatórios: 100 × área terrestre / área total do círculo recortado.', '% da área'),
    'HIDRO_KM': ('Soma dos comprimentos dos trechos de hidrografia dentro do círculo recortado, em quilômetros. É um descritor físico, sem estimativa de vazão.', 'km'),
    'VIAS_KM': ('Soma dos comprimentos dos trechos de vias dentro do círculo recortado, em quilômetros. Não incorpora volume de tráfego nem simula escoamento sobre as vias.', 'km'),
    'VALIDO': ('Indicador de entrada completa nas três variáveis principais (POP_DENS, SEM_REDE e AIH_LOCAL): 1 quando todas são finitas; 0 quando falta alguma. As seis unidades incompletas não recebem perfil.', 'indicador 0/1'),
    'ESTABILIDADE': ('Percentual dos cinco cenários S0-S4 cujo perfil k-means, com k = 2 e rótulos alinhados, coincide com o perfil S0 da mesma unidade: 100 × concordâncias / 5. Inclui S0 na contagem.', '% dos cinco cenários'),
    'QUINTIL': ('Grupo relativo 1-5 obtido por qcut dos postos médios do escore I_S0 no conjunto das três bacias. Representa aproximadamente 20% das unidades válidas por grupo; 0 indica informação incompleta. Não equivale às faixas fixas F_S0.', 'quintil 1-5; 0 sem classe'),
    'MORAN': ('Resultado local de Moran para I_S0: HH alto com vizinhos altos, LL baixo com vizinhos baixos, HL alto entre baixos, LH baixo entre altos, NS não significativo após FDR de 5%, ISO sem vizinho elegível e ND não elegível. Usa contiguidade Queen e permutações dentro de cada bacia.', 'categoria espacial'),
    'MORAN_Q': ('Valor p local ajustado por Benjamini-Hochberg para controlar falsas descobertas no conjunto elegível de cada bacia. O teste usa 999 permutações; valores até 0,05 sustentam a classe espacial inferencial.', 'valor q, 0-1'),
    'MOR_ELIG': ('Elegibilidade preliminar para o teste de Moran: 1 quando VALIDO é verdadeiro e COB_ESG ≥ 95%; 0 nos demais casos. Uma unidade elegível ainda pode ser ISO se não tiver vizinho elegível.', 'indicador 0/1'),
    'PERFIL_S0': ('Descrição do perfil k-means S0 com k = 2: 1 maior adensamento e maior ligação à rede; 2 menor adensamento e menor ligação à rede; 0 informação incompleta. São perfis multivariados, não classes de risco de resistência.', 'texto'),
    'SCENARIO': ('Código da ponderação do teste. Na ordem população / ausência de rede / atividade hospitalar local, S0 = 1/1/1; S1 = 1/1/3; S2 = 1/3/1; S3 = 3/1/1; S4 = 1/1/0.', 'código de cenário'),
    'W_POP': ('Peso atribuído à densidade populacional normalizada no cenário indicado em SCENARIO; valor 3 em S3 e 1 nos demais cenários.', 'peso relativo'),
    'W_SEWER': ('Peso atribuído ao percentual sem rede normalizado no cenário indicado em SCENARIO; valor 3 em S2 e 1 nos demais cenários.', 'peso relativo'),
    'W_HEALTH': ('Peso atribuído à atividade hospitalar local normalizada: 3 em S1, 0 em S4 e 1 em S0, S2 e S3.', 'peso relativo'),
    'K': ('Número de grupos solicitado no ajuste k-means específico da pasta de teste; foram avaliados k = 2, 3, 4, 5 e 6.', 'grupos'),
    'PROFILE': ('Perfil atribuído pelo k-means do cenário e k desta pasta; 0 indica entrada incompleta. Para k = 2, os rótulos foram alinhados à referência S0; para k > 2, foram ordenados pela média do escore do próprio cenário. Não são classes legais nem níveis universais de risco.', 'perfil 1-k; 0 sem classe'),
    'SCORE': ('Escore relativo do cenário desta pasta: 100 × média ponderada das três entradas normalizadas, com os pesos indicados por SCENARIO. Não é probabilidade de contaminação nem concentração.', 'escore 0-100'),
    'dist_km': ('Comprimento da trajetória candidata amostrada na direção D8 até o reservatório, calculado pela soma dos passos ortogonais/diagonais do MDE. A linha é um caminho topográfico candidato, sem modelagem de vazão ou transporte de genes.', 'km'),
}

NORMALIZADAS = {
    'POP_DENS': ('densidade populacional POP_DENS', 'log1p(x)', 'entra nas três variáveis do índice e do k-means'),
    'SEM_REDE': ('percentual analítico sem rede SEM_REDE', 'x', 'entra nas três variáveis do índice e do k-means'),
    'AIH_LOCAL': ('atividade hospitalar local AIH_LOCAL', 'log1p(x)', 'entra nas três variáveis do índice e do k-means'),
    'URB_PCT': ('percentual urbanizado URB_PCT', 'x', 'é complementar e não entra no índice nem no k-means atuais'),
    'HIPS_M': ('altitude média HIPS_M', 'x', 'é complementar e não entra no índice nem no k-means atuais'),
    'DECL_PCT': ('declividade média DECL_PCT', 'x', 'é complementar e não entra no índice nem no k-means atuais'),
    'DIST_KM': ('distância topográfica média DIST_KM', 'x', 'é complementar e não entra no índice nem no k-means atuais'),
    'VIAS_KM': ('comprimento de vias VIAS_KM', 'x', 'é complementar e não entra no índice nem no k-means atuais'),
    'HIDRO_KM': ('comprimento da hidrografia HIDRO_KM', 'x', 'é complementar e não entra no índice nem no k-means atuais'),
}
PESOS = {'S0': (1,1,1), 'S1': (1,1,3), 'S2': (1,3,1), 'S3': (3,1,1), 'S4': (1,1,0)}
MUNICIPIOS8 = 'Belo Horizonte, Betim, Brumadinho, Contagem, Esmeraldas, Ibirité, Ribeirão das Neves e Sarzedo'

CAMPOS_CNES_2026={
 'CNES':('Código CNES de sete dígitos utilizado para cruzar a exportação ElastiCNES com a produção hospitalar SIH estadual; armazenado como texto.','código'),
 'NOME_CNES':('Nome fantasia do estabelecimento na exportação ElastiCNES, competência 2026/09.','texto'),
 'NOME_SIH':('Nome do estabelecimento na tabela estadual SIH por local de internação enviada pelo usuário; pode diferir do nome atual do CNES. Nulo quando o código não aparece nessa tabela.','texto'),
 'TIPO_CNES':('Código e descrição do tipo de estabelecimento na exportação CNES de setembro de 2026, como hospital, consultório ou unidade ambulatorial.','categoria cadastral'),
 'MUN_COD':('Código de seis dígitos do município de localização cadastrado no CNES, sem o dígito verificador IBGE. Não indica residência do paciente.','código municipal'),
 'MUN_NOME':('Nome do município de localização do estabelecimento no cadastro CNES de setembro de 2026.','texto'),
 'COMP_CNES':('Competência da exportação ElastiCNES utilizada no cruzamento: 2026/09. Não é data de abertura do estabelecimento.','ano/mês'),
 'ATIVO_CAD':('Status cadastral informado na exportação ElastiCNES recebida. Todos os 64.706 registros constam como ATIVO; a ausência de produção SIH recente não altera este campo.','status cadastral'),
 'SUS_CAD':('Indicador de convênio SUS informado no cadastro ElastiCNES, preservado separadamente da presença efetiva de internações na consulta SIH.','categoria cadastral'),
 'CEP':('CEP do endereço do estabelecimento informado pelo CNES. Não representa a lista de CEPs dos pacientes atendidos.','código postal'),
 'ENDERECO':('Logradouro e complemento do endereço cadastral do estabelecimento, concatenados quando o complemento está informado.','texto'),
 'LAT':('Latitude em graus decimais extraída da primeira coordenada do campo location do ElastiCNES; usada na criação do ponto antes da reprojeção para EPSG:31983.','graus decimais'),
 'LON':('Longitude em graus decimais extraída da segunda coordenada do campo location do ElastiCNES; usada na criação do ponto antes da reprojeção para EPSG:31983.','graus decimais'),
 'SIH_HIST':('Indicador de correspondência do CNES com a tabela estadual SIH enviada, selecionada por processamento Jan/2015-Set/2026: 1 código encontrado; 0 código ausente. Ausência não comprova inexistência de atendimento ou desativação.','indicador 0/1'),
 'INT_FONTE':('Total do estabelecimento em todas as 151 colunas mensais de atendimento da tabela SIH enviada, incluindo registros de 2014. Confere com a coluna Total da fonte; nulo para CNES ausente da consulta.','internações SUS registradas'),
 'INT_15_26':('Soma das internações do estabelecimento por mês de atendimento de janeiro de 2015 a setembro de 2026, dentro da exportação por processamento Jan/2015-Set/2026. Todas as causas e origens dos pacientes; nulo para CNES ausente da consulta.','internações SUS registradas'),
 'INT_24_26':('Soma das internações por atendimento entre janeiro de 2024 e setembro de 2026; define a janela operacional recente de 33 meses. Todas as causas e origens dos pacientes; nulo para CNES ausente da consulta.','internações SUS registradas'),
 'INT_2024':('Internações SUS do estabelecimento nas colunas de atendimento de janeiro a dezembro de 2024, todas as causas e origens. Nulo se o CNES não consta na tabela estadual.','internações SUS registradas'),
 'INT_2025':('Internações SUS do estabelecimento nas colunas de atendimento de janeiro a dezembro de 2025, todas as causas e origens. Nulo se o CNES não consta na tabela estadual.','internações SUS registradas'),
 'INT_2026':('Internações SUS do estabelecimento nas colunas de atendimento de janeiro a setembro de 2026; período parcial, sujeito a atualização. Nulo se o CNES não consta na tabela estadual.','internações SUS registradas'),
 'ULT_ATEND':('Último mês de atendimento com contagem positiva de internações na tabela SIH enviada, no formato AAAA-MM. Não é data confirmada de encerramento da unidade.','ano-mês'),
 'MES_REC':('Número de meses com internações positivas entre janeiro de 2024 e setembro de 2026, máximo 33. Não conta meses assinalados apenas com traço na exportação.','meses com produção'),
 'SELEC_SIH':('Seleção operacional de atividade: 1 para CNES cadastrado como ATIVO e com INT_24_26 maior que zero; 0 nos demais casos. Na camada interna, aplica-se também a interseção do ponto com a bacia.','indicador 0/1'),
 'DIST_BAC_M':('Menor distância plana do ponto cadastral à união das três bacias, em EPSG:31983. Zero para pontos internos; valor positivo para os hospitais auxiliares de conferência das bordas.','m'),
 'BACIA':('Identificador da bacia intersectada pelo ponto cadastral do estabelecimento, incluindo pontos exatamente sobre o limite.','código'),
}

# Definicao
def definicao(campo, arquivo=''):
    if '17_estabelecimentos_2026' in arquivo:
        if campo=='BACIA' and '/03_bordas/' in arquivo:
            return ('Identificador da bacia mais próxima do hospital externo, utilizado somente na conferência de estabelecimentos até 1,5 km dos limites. Não indica inclusão na bacia.','código da bacia mais próxima')
        return CAMPOS_CNES_2026[campo]
    if campo == 'id' and '05_hidrografia' in arquivo:
        return ('Identificador do trecho hidrográfico da base de origem, mantido após o recorte às bacias; pode repetir-se quando uma feição é dividida.', 'identificador')
    if campo == 'AREA_KM2' and '02_reservatorios' in arquivo:
        return ('Área do polígono consolidado do espelho do reservatório, calculada em SIRGAS 2000 / UTM 23S; não é a área da bacia.', 'km²')
    if campo == 'NOME' and '08_saude_local' in arquivo:
        return ('Nome do estabelecimento hospitalar informado no cadastro CNES utilizado na camada local.', 'texto')
    if campo == 'AIH_NRMG' and '08_saude_local' in arquivo:
        return ('Total oficial NRMG de internações de residentes de Belo Horizonte, Betim, Contagem e Ibirité atendidos no estabelecimento em 2016-2025. É o recorte histórico de quatro municípios, mantido em RES_NRMG; não é o total dos oito municípios nem a produção completa do hospital.', 'internações no recorte anterior')
    if campo.startswith('N_'):
        base = campo[2:]
        if base not in NORMALIZADAS:
            raise KeyError((arquivo, campo))
        nome, transformacao, uso = NORMALIZADAS[base]
        return (f'Normalização min-max da {nome}, após transformação {transformacao}: (valor transformado − mínimo) / (máximo − mínimo). Limites comuns ao conjunto das três bacias; {uso}. Nulos são mantidos.', 'adimensional 0-1')
    if re.fullmatch('[IFK]_S[0-4]', campo):
        tipo, co = campo.split('_')
        w = PESOS[co]
        pesos = f'{w[0]}/{w[1]}/{w[2]}'
        if tipo == 'I':
            return (f'Escore do cenário {co}: 100 × ({w[0]} × N_POP_DENS + {w[1]} × N_SEM_REDE + {w[2]} × N_AIH_LOCAL) / {sum(w)}. Pesos população/ausência de rede/atividade hospitalar = {pesos}; não é probabilidade de contaminação.', 'escore 0-100')
        if tipo == 'F':
            return (f'Classe de I_{co} em faixas fixas: 1 [0,20), 2 [20,40), 3 [40,60), 4 [60,80), 5 [80,100]; 0 entrada incompleta. Não é classificação por percentis nem risco comprovado.', 'classe 1-5; 0 sem classe')
        return (f'Perfil k-means com k = 2 no cenário {co}, ajustado nas três entradas normalizadas multiplicadas pela raiz quadrada dos pesos {pesos}. Rótulos alinhados a S0 por correspondência ótima: 1 maior adensamento e maior ligação à rede; 2 menor adensamento e menor ligação à rede; 0 entrada incompleta. O número não ordena risco.', 'perfil 1/2; 0 sem classe')
    if campo.startswith('RES8_') or campo.startswith('PROD_'):
        residencial = campo.startswith('RES8_')
        prefixo = 'AIH normais de residentes dos oito municípios (' + MUNICIPIOS8 + ')' if residencial else 'AIH normais produzidas no estabelecimento, de pacientes de todas as origens'
        grupo = campo.split('_',1)[1]
        sufixos = {'A':'diagnóstico principal de etiologia bacteriana codificada, filtro A', 'B':'diagnóstico principal de síndrome compatível, filtro B', 'AB':'filtro amplo A+B, soma das categorias A e B', 'C':'categoria C, condições associadas ou sequelas mantidas separadas do filtro principal A+B', 'SEM_DIC':'código de diagnóstico sem correspondência no dicionário CID utilizado; mantido no total bruto, fora do filtro A+B', 'TOT':'todas as causas, inclusive diagnósticos sem descrição no dicionário'}
        if grupo in sufixos:
            return (f'{prefixo}, processadas em 2016-2025: {sufixos[grupo]}. Não constituem contagem de casos confirmados de resistência antimicrobiana.', 'internações no período')
    if campo not in DEFINICOES:
        raise KeyError(f'Campo sem descrição específica: {arquivo} | {campo}')
    return DEFINICOES[campo]

# Linhagem
def linhagem(campo, arquivo):
    if '17_estabelecimentos_2026' in arquivo:
        script='revisar_cnes_sih_mg_teco.py'
        anchor='def ler_sih' if campo.startswith('INT_') or campo in ['ULT_ATEND','MES_REC','NOME_SIH'] else 'def cruzar' if campo in ['BACIA','SELEC_SIH','SIH_HIST','DIST_BAC_M'] else 'def ler_cnes'
        return ('cruzamento CNES/SIH por código e interseção espacial em Python',script,anchor,'consolidar_entrega_final.py')
    grid = 'grade_500m_teco.py'
    export = 'consolidar_entrega_final.py'
    consolidado = 'consolidar_final_auditado_teco.py'
    if arquivo.startswith('02_saidas/'):
        if campo in ['PROFILE','K','SCORE'] or ('02_kmeans/' in arquivo and campo == 'SCENARIO'):
            return ('calculado em Python', 'auditar_consolidacao_final_teco.py', "out['" + campo + "']", grid + '; analise_espacial_teco.py; multivariada_teco.py; ' + consolidado)
        if campo in ['SCENARIO','W_POP','W_SEWER','W_HEALTH','AREA_CEL','PERFIL_S0','MOR_ELIG']:
            return ('calculado em Python', consolidado, campo, grid)
        if campo in ['bacia','dist_km']:
            return ('calculado em Python', 'analise_espacial_teco.py', 'terrain_routing', '')
        if campo == 'BACIA':
            return ('identificador atribuído por interseção espacial', grid, "rename(columns={'id':'BACIA'})", 'sub_bacia/delimitar_subbacias_teco.py')
        apoios = []
        if campo.startswith('K_S'):
            apoios = ['analise_espacial_teco.py', 'multivariada_teco.py']
        if campo.startswith('MORAN'):
            apoios = ['multivariada_teco.py', 'analise_espacial_teco.py']
        if campo.startswith('N_') or campo.startswith(('I_S','F_S')):
            ancora = "feats=['POP_DENS'" if campo[2:] in ['POP_DENS','SEM_REDE','AIH_LOCAL'] else "for f in ['URB_PCT'"
            if not campo.startswith('N_'):
                ancora = "scen={'S0'"
        else:
            ancora = campo
        if campo.startswith('K_S'):
            ancora = "circles['K_'+co]"
        if campo in ['SEM','DOM_EST','SEM_REDE','EST_ESG']:
            apoios.append('multivariada_teco.py')
        return ('calculado em Python', grid, ancora, '; '.join(apoios))
    if '01_bacias/' in arquivo:
        return ('calculado em PyQGIS', 'delimitar_subbacias_teco.py', "campos_b =", 'analise_espacial_teco.py')
    if '02_reservatorios/' in arquivo:
        return ('calculado em Python' if campo == 'AREA_KM2' else 'identificação do polígono fornecido', export, "water=[]", '')
    if '03_populacao/' in arquivo:
        if campo.startswith('v000'):
            return ('variável oficial IBGE, unida por código do setor', consolidado, "poppath=", 'preparar_ibge_consolidacao_teco.py')
        return ('calculado em Python' if campo in ['POP_REC','DENS_POP'] else 'dado oficial IBGE, identificado no recorte', 'integrar_populacao_uso_rede.py', 'pop_table' if campo != 'POP_REC' else "pop_a_est", 'preparar_saneamento_ibge.py; ' + export)
    if '04_esgotamento/' in arquivo:
        return ('variável oficial IBGE' if campo in ['REDE_DIR','FOSS_REDE','FOSS_SREDE','FOSSA_RUD','VALA','RIO_LAGO','OUTRO','SEM_BANH','DOM_TOT','setor_id'] else 'calculado em Python', 'preparar_saneamento_ibge.py', 'n_sigilo' if campo == 'SIGILO_N' else 'pct_rede', export)
    if '05_hidrografia/' in arquivo:
        return ('calculado em Python' if campo in ['COMP_KM','BACIA'] else 'identificador da hidrografia de origem', export, "hyd=gpd.read_file", 'analise_espacial_teco.py')
    if any(x in arquivo for x in ['06_vias_contexto/','07_vias_bacias/']):
        if campo == 'TIPO_VIA':
            return ('classificação cartográfica em Python', 'mapas_grade_teco.py', 'def roadtype', export)
        return ('calculado em Python' if campo in ['COMP_KM','BACIA'] else 'classificação/identificador da malha viária', export, "roads=gpd.read_file", 'analise_espacial_teco.py; integrar_refino_entrega_teco.py')
    if '08_saude_local/' in arquivo:
        if campo in ['AIH_NRMG','RES_AB']:
            return ('recorte histórico de quatro municípios, unido por CNES', 'integrar_refino_entrega_teco.py', "'RES_NRMG'", 'preparar_refino_sih_teco.py; consolidar_saude_residencia.py')
        if campo in ['AIH_TODAS','AIH_FILT','AIH_ANO']:
            return ('calculado em Python a partir do SIH/RD', 'preparar_camadas_nativas.py', "health['AIH_TODAS']", 'obter_rd_grade.py; filtro_bacteriano_teco.py; refinar_credibilidade_sih_teco.py; avaliar_saude_grade.py')
        if campo == 'QA_MUN':
            return ('verificação espacial em Python', 'analise_espacial_teco.py', "qa['QA_MUN']", 'obter_cnes.py')
        return ('cadastro CNES e localização dentro das bacias', 'analise_espacial_teco.py', 'def cnes', 'obter_cnes.py; preparar_camadas_nativas.py; ' + export)
    if '09_saude_residencia/' in arquivo:
        return ('consulta oficial NRMG' if campo == 'AIH_NRMG' else 'calculado ou integrado por CNES em Python', consolidado, "units=pd.read_csv", 'saude_todos_municipios_teco.py; filtro_bacteriano_teco.py; refinar_credibilidade_sih_teco.py; auditar_tabnet_estabelecimentos.py')
    if '10_exutorios/' in arquivo:
        return ('calculado em Python/PyQGIS', 'auditar_relevo_lancamentos_teco.py', "v=ex.copy()", 'delimitar_subbacias_teco.py')
    if '11_pontos_coleta/' in arquivo:
        return ('atributo do ponto fornecido' if campo == 'COLETA_ID' else 'identificação da bacia de origem', export, "samples=[]", '')
    if '14_rede_cadastral_BH/' in arquivo:
        return ('calculado em Python sobre cadastro PBH', 'integrar_populacao_uso_rede.py', 'def network_layers', 'complementar_entrega_final.py')
    if '15_ETE_cadastro/' in arquivo:
        return ('atributo do cadastro IDE-Sisema' if campo not in ['BACIA','NOME_BACIA'] else 'interseção espacial em Python', 'integrar_populacao_uso_rede.py', 'def etes', 'complementar_entrega_final.py')
    raise KeyError((arquivo, campo))

# Descrever campo
def descrever_campo(campo, arquivo=''):
    return definicao(campo, arquivo)[0]
