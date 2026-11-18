# ENTRADAS: documentar_microplasticos_teco.text; figuras/galeria.json e mapas 01-20; contagem_tipologias_bacias.csv.
# SAÍDAS: página local do relatório HTML e docs/microplasticos no repositório; prévias públicas SVG com WebP, sem alterar figuras científicas originais.
# TEXTO: começa no item 2; a introdução removida fica somente no relatório de referência. Mapas intermediários acompanham os itens 3.1,3.2,3.3.
# CAMINHOS: TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json; publicação remota é realizada separadamente.
from pathlib import Path
import json,html,datetime,shutil,io,base64
import pandas as pd
from PIL import Image
from caminhos_teco import raiz_projeto
import documentar_microplasticos_teco as doc
R=raiz_projeto();O=R/'output/07_microplasticos';D=R/'entrega_final/00_documentacao/Microplasticos';REPO=R/'github/codiname-teco';SITE=REPO/'docs/microplasticos'
EXPLANATIONS={
'01_waste':'Percentual domiciliar sem coleta por serviço de limpeza, com geometria nativa dos setores. As contagens se referem ao setor inteiro; o recorte não localiza cada domicílio.',
'14_licensed_typologies':'Registros estaduais de licenciamento agrupados pela atividade principal. A família de plásticos inclui os dois registros históricos de moldagem e reciclagem a seco. As demais famílias orientam a leitura dos processos e não têm emissões de microplásticos quantificadas.',
'15_licensed_linkage':'O vínculo é documental: material plástico explícito, processo possível a verificar, manejo de resíduos/efluentes ou ausência de vínculo específico na descrição. As cores não representam níveis medidos de geração ou de risco.',
'16_waste_destinations':'Todos os municípios do recorte declararam destinação a aterro sanitário regularizado na base de 2024. Os símbolos mostram instalações cadastradas visíveis no enquadramento. Não há atribuição automática do resíduo de um município a uma instalação nem traçado de transporte inferido.',
'17_selective_collection':'Existência de coleta seletiva declarada em escala municipal em 2024. A presença do serviço não indica cobertura de todos os bairros nem percentual de recuperação de materiais.',
'18_waste_plans':'Existência declarada de plano municipal de gestão de resíduos em 2024. O mapa não avalia implementação, fiscalização ou eficácia do plano.',
'19_waste_uncertainty':'Diferença, em pontos percentuais, entre os limites superior e inferior do percentual sem coleta. Mostra a amplitude decorrente do sigilo ou da incompletude das categorias; não é um intervalo de confiança.',
'20_waste_pathways':'Destino mais frequente entre as quatro categorias sem coleta quando todas são conhecidas. Registros sigilosos/incompletos ficam separados. O mapa não informa quantidade de plástico e não substitui a conexão hidrológica com o reservatório.'}

# Imagens e texto editorial
def figure(item,public):
 src='mapas/'+item['svg'] if public else '../../03_mapas/14_microplasticos/'+item['png'];link=src if public else '../../03_mapas/14_microplasticos/'+item['svg']
 return '<figure><h3>'+html.escape(item['title'])+'</h3><a href="'+link+'"><img loading="lazy" src="'+src+'" alt="'+html.escape(item['title'])+'"></a><figcaption>'+html.escape(EXPLANATIONS.get(item['id'],''))+'</figcaption></figure>'
def build(public,gallery):
 md=doc.text();body=doc.html_body('# Pressões potenciais de genes de resistência e microplásticos\n\n## 2.'+md.split('## 2.',1)[1]);items={g['id']:g for g in gallery}
 counts=pd.read_csv(O/'tabelas/licencas_por_tipologia.csv',sep=';').groupby(['TP_CODE','TP_NAME']).size().reset_index(name='Registros')
 tab=counts[['TP_NAME','Registros']].to_html(index=False,escape=True)
 groups=[(['01_waste','19_waste_uncertainty','20_waste_pathways'],'<h3>3.2'),(['14_licensed_typologies','15_licensed_linkage','16_waste_destinations'],'<h3>3.3'),(['17_selective_collection','18_waste_plans'],'<h2>4.')]
 for ids,needle in groups:
  extra=''.join(figure(items[k],public) for k in ids)
  if '14_licensed_typologies' in ids:extra='<p>As tipologias abaixo representam atividades principais dos 49 registros de processo, e não necessariamente 49 empresas distintas ou em operação. O cadastro estadual precisa ser complementado por processos municipais. O vínculo potencial não foi transformado em peso ou taxa de emissão.</p>'+tab+extra
  body=body.replace(needle,extra+needle,1)
 used={k for ids,_ in groups for k in ids};body+='<h2>Mapas da classificação e produtos complementares</h2>'+''.join(figure(x,public) for x in gallery if x['id'] not in used)
 nav='<a href="../index.html">Visualizador principal</a>' if public else ''
 nav+='<a href="Relatorio_ARG_microplasticos.md">Texto de referência</a><a href="Guia_codigos_microplasticos.html">Guia dos scripts</a>'
 return '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ARG e microplásticos | Metodologia e mapas</title><style>'+doc.CSS+'</style><main><nav>'+nav+'</nav>'+body+'</main></html>'

# Atualização local e do espelho GitHub
def atualizar():
 gallery=json.loads((O/'figuras/galeria.json').read_text('utf8'));SITE.mkdir(exist_ok=True,parents=True);(SITE/'mapas').mkdir(exist_ok=True)
 for g in gallery:
  if int(g['id'][:2])<14:continue
  with Image.open(O/'figuras'/g['png']) as im:
   im.thumbnail((2400,2400));buf=io.BytesIO();im.save(buf,format='WEBP',quality=93,method=6);encoded=base64.b64encode(buf.getvalue()).decode();w,h=im.size
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><image width="100%" height="100%" xlink:href="data:image/webp;base64,{encoded}"/></svg>';(SITE/'mapas'/g['svg']).write_text(svg,encoding='utf8')
 stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
 for p,public in [(D/'Relatorio_ARG_microplasticos.html',False),(SITE/'index.html',True)]:
  if p.exists():
   archive=R/'descontinuado'/stamp/'visualizador_antes_intermediarios'/('online' if public else 'local')/p.name;archive.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,archive)
  p.write_text(build(public,gallery),encoding='utf8')
 md=doc.text();(D/'Relatorio_ARG_microplasticos.md').write_text(md,encoding='utf8');(SITE/'Relatorio_ARG_microplasticos.md').write_text(md,encoding='utf8')
 for p in [D/'Relatorio_ARG_microplasticos.html',SITE/'index.html']:
  s=p.read_text('utf8');assert '## 1.' not in s and 'O que esta complementação permite avaliar' not in s;assert 'Complementação metodológica e resultados exploratórios.' not in s;assert 'Foi utilizado o mesmo arquivo CSV da pasta saneamento_ibge' in s;assert s.count('<figure>')==20
 print('Visualizadores atualizados: item 2 e vinte mapas',flush=True)
if __name__=='__main__':atualizar()
