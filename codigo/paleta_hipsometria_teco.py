# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:\teco/config/paleta_hipsometria.json | CONFIG.read_text.
# Campos/chaves em s: cor, posicao.
# Campos/chaves em d: paradas.
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
import json
CONFIG=Path(_cp_texto('config/paleta_hipsometria.json', 'posix'))

# Metadata
def metadata():return json.loads(CONFIG.read_text('utf8'))

# Colormap
def colormap():
 from matplotlib.colors import LinearSegmentedColormap
 d=metadata();return LinearSegmentedColormap.from_list('QGIS_GMT_dem1',[(s['posicao'],s['cor']) for s in d['paradas']],N=1024)
