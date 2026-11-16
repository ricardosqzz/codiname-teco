# ENTRADA: dados/microplasticos/grade_microplasticos.geojson; MP_VALID, POP_DENS, SEWER_DENS, WASTE_DENS, ROAD_DENS, I_S0, K_S0 e geometry.
# CONFIGURAÇÃO: config/microplasticos.json; mesmos critérios, transformações, pesos, K e semente do produto consolidado.
# SAÍDA: output/repro_microplasticos; classificação, normalização, k-means, sensibilidade e Moran reproduzidos a partir dos derivados públicos.
# LIMITE: este atalho não refaz as fontes censitárias, as consultas públicas ou os caminhos D8; usar microplasticos_teco.py para a cadeia completa.
import json
import numpy as np
import geopandas as gpd
from caminhos_teco import raiz_projeto
import microplasticos_teco as engine
R=raiz_projeto();O=R/'output/repro_microplasticos';(O/'tabelas').mkdir(parents=True,exist_ok=True)

# Reprodução dos derivados publicados
def main():
    g=gpd.read_file(R/'dados/microplasticos/grade_microplasticos.geojson');expected=g.MP_INDEX.copy();engine.O=O
    g,meta=engine.classify(g);g=engine.spatial(g);diff=float(np.nanmax(abs(g.MP_INDEX-expected)))
    assert diff<1e-8,'Índice divergente do produto publicado'
    g.to_file(O/'classificacao_reproduzida.gpkg',layer='microplastic_pressure',driver='GPKG')
    report={**meta,'max_abs_difference':diff,'sources_reprocessed':False};(O/'validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'records':len(g),'eligible':meta['n_valid'],'max_abs_difference':diff},ensure_ascii=True))
if __name__=='__main__':main()
