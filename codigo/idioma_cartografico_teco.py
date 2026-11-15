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

import re
WORDS={
'População censitária · setores de origem':'Census population · original census sectors',
'Habitantes no setor completo de origem':'Residents in the complete original sector',
'População no recorte censitário · estimativa por área':'Population within basin boundaries · area allocation',
'Habitantes estimados no recorte da bacia':'Estimated residents within the basin clip',
'Adensamento populacional · setores censitários':'Population density · census sectors',
'Habitantes/km²':'Residents/km²',
'Ligação à rede · dado censitário observado':'Sewer network connection · observed census data',
'Domicílios com rede (%)':'Households connected to the network (%)',
'Ausência de ligação à rede · dado observado':'No sewer network connection · observed data',
'Domicílios sem rede (%)':'Households without a network connection (%)',
'Destinação declarada em vala ou corpo hídrico':'Reported disposal into a ditch or water body',
'Domicílios com destinação em vala ou corpo hídrico (%)':'Households reporting disposal into a ditch or water body (%)',
'Dado não publicado / ausente':'Unpublished / missing data',
'Estabelecimentos com internações confirmadas · localização nas bacias':'Facilities with confirmed admissions · locations within basins',
'Internações por estabelecimento · filtro bacteriano e compatível':'Hospital admissions · bacterial and compatible diagnoses',
'Média anual de AIH selecionadas (2016-2025) · localização do hospital':'Selected admissions per year (2016-2025) · hospital location',
'Malha viária · hierarquia cadastral':'Road network · registered hierarchy',
'Cursos hídricos e reservatórios':'Watercourses and reservoirs',
'Uso e ocupação do solo · 2025 informado':'Land use and land cover · 2025',
'Declividade · classes Embrapa':'Slope · Embrapa classes',
'Potencial relativo exploratório':'Exploratory relative pressure',
'Perfis multivariados':'Multivariate profiles',
'Comparação por quintis · índice relativo local':'Quintile comparison · local relative index',
'Estabilidade entre cenários de ponderação':'Stability across weighting scenarios',
'Cenários com o mesmo perfil (%)':'Scenarios retaining the reference profile (%)',
'Associação espacial exploratória · Moran local':'Exploratory spatial association · local Moran',
'HH · alto próximo de alto':'HH · high surrounded by high',
'LL · baixo próximo de baixo':'LL · low surrounded by low',
'HL · alto próximo de baixo':'HL · high surrounded by low',
'LH · baixo próximo de alto':'LH · low surrounded by high',
'Associação não significativa':'No significant association',
'Informação não elegível':'Ineligible information',
'Sem vizinho elegível':'No eligible neighbour',
'Pressão territorial média a montante · cenário topológico':'Mean upstream territorial pressure · topological scenario',
'Média ponderada por área do índice S0 (0-100)':'Area-weighted upstream mean of S0 (0-100)',
'Área válida contribuinte pelo terreno':'Valid topographic contributing area',
'Área a montante (km²)':'Upstream area (km²)',
'Grade de análise e vizinhanças de 500 m':'Analysis grid and 500 m neighbourhoods',
'Grade de análise e vizinhanças de500m':'Analysis grid and 500 m neighbourhoods',
'Vias, cursos hídricos e trajetórias superficiais candidatas':'Roads, watercourses and candidate surface pathways',
'Plano · 0-3%':'Flat · 0-3%', 'Suave ondulado · 3-8%':'Gently undulating · 3-8%',
'Ondulado · 8-20%':'Undulating · 8-20%', 'Forte ondulado · 20-45%':'Strongly undulating · 20-45%',
'Montanhoso · 45-75%':'Mountainous · 45-75%', 'Escarpado · >75%':'Steep · >75%',
'Área urbanizada':'Built-up area','Vegetação natural':'Natural vegetation',
'Agropecuária / silvicultura':'Agriculture / planted forest','Mineração':'Mining',
'Água / aquicultura':'Water / aquaculture','Outras superfícies':'Other surfaces',
'Muito baixo':'Very low','Muito alto':'Very high','Moderado':'Moderate','Baixo':'Low','Alto':'High',
'Informação incompleta':'Incomplete information','Perfil 1':'Profile 1','Perfil 2':'Profile 2',
'Hipsometria':'Elevation','Elevação (m)':'Elevation (m)','Declividade (%)':'Slope (%)','Declividade':'Slope',
'Distância superficial ao reservatório':'Surface flow-path distance to the reservoir','Distância D8 (km)':'D8 distance (km)',
'Via secundária / coletora':'Secondary / collector road','Via principal':'Primary road','Via local':'Local road',
'Via sem classe cadastrada':'Unclassified road','Sem classe cadastrada':'No registered class',
'Trajetória D8 candidata':'Candidate D8 pathway','Curso hídrico':'Watercourse','Reservatório':'Reservoir',
'Célula de apresentação':'Display cell','Raio de cálculo · 500m':'Calculation radius · 500 m',
'Centro da vizinhança':'Neighbourhood centre','Escala 1:225.000':'Scale 1:225,000',
'Adensamento | setores censitários':'Population density | census sectors',
'Ausência de rede | observado':'No network connection | observed',
'Ligação à rede | observado':'Network connection | observed',
'Limites das bacias':'Basin boundaries',
'População censitária | setor de origem':'Census population | original sector',
'População no recorte | estimativa por área':'Population in basin clip | area allocation',
'Círculos de cálculo | raio500m':'Calculation circles | 500 m radius',
'Centros das vizinhanças':'Neighbourhood centres',
'Vias de fundo | hierarquia cadastral':'Background roads | registered hierarchy',
'Vias recortadas para análise':'Roads clipped for analysis',
'Cursos hídricos':'Watercourses',
'Exutórios de referência':'Reference outlets',
'Trajetórias topográficas candidatas D8':'Candidate D8 topographic pathways',
'Estações de tratamento no cadastro recebido':'Treatment plants in the supplied register',
'Rede cadastrada por trecho - apenas domínio de BH':'Registered network segments - Belo Horizonte coverage only',
'Hospitais com internações confirmadas | dentro das bacias':'Hospitals with confirmed admissions | within basins',
'383 estabelecimentos com internações | residência municipal':'383 admitting facilities | municipal residence query',
'Localização dentro das bacias':'Located within basins','Instituição fora das bacias':'Facility outside the basins',
'Coordenada pendente, produção confirmada':'Coordinates pending, hospital activity confirmed',
'Administrativo / móvel / outros':'Administrative / mobile / other',
'Farmácia (cadastro CNES)':'Pharmacy (CNES register)',
'Outros serviços assistenciais':'Other healthcare services',
'Atenção básica':'Primary care','Urgência / pronto atendimento':'Emergency / urgent care',
'Hospital / hospital-dia':'Hospital / day hospital',
'Perfis k-means: identificadores sem ordem universal de risco':'K-means profiles: identifiers without a universal risk order',
'Perfis sem ordem de risco':'Profiles without a risk order',
'K-means S0 | perfis de atributos':'K-means S0 | attribute profiles',
'K-means S1 | perfis de atributos':'K-means S1 | attribute profiles',
'K-means S2 | perfis de atributos':'K-means S2 | attribute profiles',
'K-means S3 | perfis de atributos':'K-means S3 | attribute profiles',
'K-means S4 | perfis de atributos':'K-means S4 | attribute profiles',
'Moran local | Queen e FDR5%':'Local Moran | Queen and 5% FDR',
'Moran local do cenário S0':'Local Moran for S0',
'Associação espacial | Moran local':'Spatial association | local Moran',
'HH/LL associação; HL/LH contraste':'HH/LL association; HL/LH contrast',
'Escores e faixas dos cinco cenários':'Scores and classes for the five scenarios',
'Comparação dos cenários de ponderação':'Weighting scenario comparison',
'Quintis: comparação distinta das faixas fixas':'Quintiles: comparison distinct from fixed score classes',
'Faixas do escore relativo':'Relative score classes',
'Habitantes no setor completo':'Residents in the complete sector',
'Habitantes estimados no recorte':'Estimated residents in the basin clip',
'Domicílios (%)':'Households (%)','Hipsometria (m)':'Elevation (m)',
'Distância D8 até o lago (km)':'D8 distance to the lake (km)',
'Relevo - classes Embrapa':'Terrain - Embrapa slope classes',
'Relevo e condicionantes':'Terrain and physical context',
'Pressão média a montante':'Mean upstream pressure',
'Área contribuinte km²':'Contributing area km²',
'Figura':'Figure',
}
FIELDS={
'GRID_ID':'Grid identifier','BACIA':'Basin identifier','id':'Identifier','setor_id':'Census sector identifier',
'NOME':'Name','NOME_BACIA':'Basin name','NOME_TABNET':'Name in TabNet','MUNICIPIO':'Municipality',
'POP_OFIC':'Population of the complete original sector','POP_REC':'Area-allocated population in the basin clip',
'DENS_POP':'Population density (residents/km²)','POP_DENS':'Population density (residents/km²)',
'POP':'Area-allocated population in the neighbourhood','DOM':'Area-allocated households in the neighbourhood',
'DOM_TOT':'Households in the complete original sector','DOM_REDE':'Households connected to the network',
'REDE_PCT':'Households connected to the network (%)','SEM_REDE_OBS':'Households without a network connection - observed (%)',
'SEM_REDE':'Households without a network connection - analytical (%)','SEM_OBS_P':'Households without a network connection - observed coverage (%)',
'REDE_DIR':'Households connected to a general or stormwater sewer','FOSS_REDE':'Septic tank connected to the sewer network',
'FOSS_SREDE':'Septic tank not connected to the network','FOSSA_RUD':'Rudimentary pit','VALA':'Disposal into a ditch',
'RIO_LAGO':'Disposal into a river lake stream or sea','DESC_RIO':'Ditch or water-body disposal (%)',
'OUTRO':'Other disposal','SEM_BANH':'No toilet or sanitary facility','SIGILO_N':'Unpublished sanitation fields',
'AIH_LOCAL':'Selected hospital admissions per year at the local facility',
'AIH_ORIG':'Admissions by patient origin - pending spatial allocation',
'AIH_A':'Admissions with explicitly bacterial diagnoses',
'AIH_B':'Admissions with compatible diagnoses',
'AIH_AB':'Admissions selected by the A+B filter',
'AIH_ANO':'Selected hospital admissions per year',
'AIH_FILT':'Selected hospital admissions total',
'AIH_TODAS':'Hospital admissions - all causes',
'AIH_NRMG':'Admissions in the municipal residence query',
'MEDIA_ANUAL_AB':'Selected hospital admissions per year (A+B)',
'N_AIH_LOCAL':'Normal admissions recorded at the facility',
'CNES':'National healthcare facility identifier (CNES)',
'AREA_KM2':'Area (km²)','AREA_CEL':'Display cell area (km²)','RAIO_M':'Calculation radius (m)',
'COB_ESG':'Households with observed sanitation data (%)','EST_ESG':'Households with imputed sanitation data (%)',
'DOM_OBS':'Area-allocated households with observed sanitation','DOM_EST':'Area-allocated households with imputed sanitation',
'SEM':'Area-allocated households without a network connection - analytical',
'SEM_OBS':'Area-allocated households without a network connection - observed',
'SAUDE_N':'Number of admitting facilities in the neighbourhood','VALIDO':'Complete main analytical inputs',
'URB_PCT':'Built-up land (%)','TERRA_PCT':'Land surface (%)','HIPS_M':'Mean elevation (m)',
'DECL_PCT':'Mean slope (%)','DIST_KM':'Mean D8 distance to the reservoir (km)',
'VIAS_KM':'Road length (km)','HIDRO_KM':'Watercourse length (km)','USO_N':'Valid land-cover pixels',
'E':'Easting (m)','N':'Northing (m)','CENTRO_INT':'Centre located inside a basin',
'ESTABILIDADE':'Weighting scenarios retaining the reference profile (%)',
'QUINTIL':'Relative S0 quintile','MORAN':'Local Moran association class','MORAN_Q':'Local Moran FDR-adjusted p-value',
'ORIG_STATUS':'Patient-origin allocation status','TIPO':'Type','TIPO_VIA':'Road class','GRUPO':'Facility type',
'SIT_ESPACIAL':'Spatial verification status','QA_MUN':'Coordinate municipality verification',
'DIST_BACIA_M':'Distance to a basin (m)','COMP_KM':'Length (km)','COLETA_ID':'Sampling point identifier',
'PERFIL_S0':'Reference profile description','reserv':'Reservoir','area_km2':'Area (km²)',
'orig_km2':'Original area (km²)','reduz_km2':'Removed area (km²)','incl_pct':'Reservoir area included (%)',
'situacao':'Verification status','metodo':'Method','bacia':'Basin identifier','dist_km':'Distance (km)',
'utm_e':'Easting (m)','utm_n':'Northing (m)','comp_m':'Length (m)','mun_nome':'Municipality',
'prec_m':'Coordinate precision (m)','sit_nome':'Site name','sit_rede':'Network status',
'fase_lic':'Licensing stage','situ_lic':'Licensing status','ete_id':'Treatment plant identifier',
'acum_cel':'Upstream cell count','hier_legal':'Registered road hierarchy','status':'Status','AREA':'Overlap area (km²)',
}

# En
def en(text):
 if not isinstance(text,str):return text
 if text in WORDS:return WORDS[text]
 text=text.replace('reported year 2025','2025')
 out=text
 for a,b in sorted(WORDS.items(),key=lambda kv:len(kv[0]),reverse=True):out=out.replace(a,b)
 out=re.sub(r'(?<=\d) a (?=\d)',' to ',out)
 out=out.replace('°O','°W').replace('2,5','2.5')
 return out

WORDS.update({
'TECO | grade de500m e cenários':'TECO | 500 m grid and scenarios',
'01 Classificação relativa':'01 Relative classification','02 Entradas originais':'02 Original inputs',
'03 Entradas normalizadas':'03 Normalised inputs','04 K-means e Moran':'04 K-means and Moran',
'05 Saúde e grade':'05 Healthcare and grid','06 Contexto':'06 Context',
'07 Suporte aos layouts':'07 Layout support layers','08 Conectividade topológica':'08 Topological connectivity',
'Saúde | rede confirmada por residência NRMG':'Healthcare | confirmed municipal residence query NRMG',
'TECO | avaliação espacial atual':'TECO | current spatial assessment',
'01 Bases temáticas | mesma geometria censitária':'01 Thematic inputs | common census geometry',
'02 Pressão relativa e agrupamentos | exploratório':'02 Relative pressure and exploratory clustering',
'03 Conectividade topográfica | não é rede de esgoto':'03 Topographic connectivity | not a sewer network',
'04 Estabelecimentos | CNES ativo consultado':'04 Facilities | queried active CNES register',
'05 Relevo | Copernicus 30 m':'05 Terrain | Copernicus 30 m',
'Entradas e saídas | arquivos individuais':'Inputs and outputs | individual files',
'CNES | estabelecimentos por tipo assistencial':'CNES | facilities by healthcare type',
'Conferência do ponto anterior e vertedouro | Vargem':'Previous point and spillway verification | Vargem',
'Destinação declarada em rio/lago/mar':'Reported disposal into a ditch or water body',
'ETE / unidade | ANA2020':'WWTP / facility | ANA 2020','ETE | cadastro IDE-Sisema':'WWTP | IDE-Sisema register',
'Entradas no lago | proxy censitário, não carga de ARG':'Lake inflows | census proxy, not an ARG load',
'Esgotamento | somente informações domiciliares':'Sanitation | household information only',
'Esgoto no recorte | estimativas, não totais oficiais':'Sanitation in basin clips | estimates, not official totals',
'K-means base | cinco perfis':'Historical K-means reference | five profiles',
'K-means | tipologias de adensamento e rede':'K-means | population density and network profiles',
'Limites das três bacias':'Boundaries of the three basins',
'Moran bivariado | população × ausência de rede nos vizinhos':'Bivariate Moran | population and neighbouring network deficit',
'Moran local | índice relativo | FDR 5%':'Local Moran | relative index | 5% FDR',
'Oito vizinhos | base':'Eight neighbours | reference',
'Outorgas modo18 regionais | fora das três bacias':'Regional discharge permits mode 18 | outside the three basins',
'População estimada no recorte | rateio por área':'Estimated population in basin clips | area allocation',
'População oficial | apenas ID e total de pessoas':'Official population | identifier and total residents',
'Pressão relativa | quintis | pesos 50/50':'Historical relative pressure | quintiles | 50/50 weights',
'Queen | base':'Queen | reference','Queen | sem esgoto':'Queen | without sanitation',
'Vargem conferido':'Vargem verified','potencial relativo exploratório':'exploratory relative pressure',
'perfis de sensibilidade':'sensitivity profiles',
'SIH 2016-2025 | cobertura e atividade dos estabelecimentos':'SIH 2016-2025 | facility coverage and activity',
'TECO - 3 sub-bacias exclusivas (EPSG:31983)':'TECO - three non-overlapping sub-basins (EPSG:31983)',
'TECO | exutórios de referência corrigidos':'TECO | verified reference outlets',
'Trajetórias D8 amostradas | candidatas a conferência':'Sampled D8 pathways | candidates for verification',
'setores_integrados_bacias':'Integrated census sector and basin clips',
'Índice base | 0-100, sem classificação de risco':'Reference index | 0-100, without a risk classification',
'ARTERIAL PRIMARIA':'PRIMARY ARTERIAL','ARTERIAL SECUNDARIA':'SECONDARY ARTERIAL',
'ARTERIAL':'ARTERIAL','COLETORA':'COLLECTOR','LOCAL':'LOCAL','EXPRESSA':'EXPRESSWAY',
'Fora das bacias':'Outside the basins','Dentro das bacias':'Within the basins',
})
FIELDS.update({'PROD_TOT':'Hospital production - all causes and origins','PROD_A':'Hospital production - bacterial diagnoses',
'PROD_B':'Hospital production - compatible diagnoses','PROD_AB':'Hospital production - selected A+B diagnoses',
'RES_RD':'Patient residence query - raw RD total','DIF_RES':'Difference between raw RD and official residence query',
'RES_NRMG':'Official municipal residence query total','RES_AB':'Municipal residents - selected A+B diagnoses'})

# Field alias
def field_alias(name):
 if name in FIELDS:return FIELDS[name]
 if name.startswith('I_S'):return 'Relative pressure score - '+name[2:]
 if name.startswith('F_S'):return 'Relative pressure class - '+name[2:]
 if name.startswith('K_S'):return 'Multivariate profile - '+name[2:]
 if name.startswith('N_'):return 'Normalised '+field_alias(name[2:]).lower()
 return name
