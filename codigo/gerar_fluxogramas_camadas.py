# Caminhos: TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json; executar no Python do QGIS.
# Entradas: 00_documentacao/Guia_objetivo_camadas_TECO.md e 01_entradas da entrega_final.
# Campos representados: POP_DENS, SEM_REDE, AIH_LOCAL, SEWER_DENS, WASTE_DENS, ROAD_DENS, GRID_ID e BACIA.
# Projetos: projeto_teco.qgz e entrega_final/TECO_Consolidado.qgz; preserva camadas e layouts existentes.
# Saídas: 00_documentacao/Fluxogramas; dois SVG, dois PNG, PDF de duas páginas e auditoria JSON.
# Saída QGIS: layout Workflow | Layers; fluxograma documental, sem reexecutar índices ou alterar atributos.
from pathlib import Path
import os,sys,json,html,hashlib,datetime,shutil,math
from caminhos_teco import raiz_projeto

# Caminhos
R=raiz_projeto();F=R/'entrega_final';O=F/'00_documentacao/Fluxogramas'
STAMP=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
COL={'ink':'#17384b','blue':'#23769a','green':'#257b6c','purple':'#78569a','orange':'#b87825','gray':'#62747d','line':'#90a6af'}
S=[]

# Elementos vetoriais
def text(x,y,lines,size=24,color=None,bold=False,gap=33):
    for i,line in enumerate(lines):
        S.append(f'<text x="{x}" y="{y+i*gap}" font-family="Arial" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color or COL["ink"]}">{html.escape(str(line))}</text>')

def rect(x,y,w,h,fill,stroke='none',rx=16):
    S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

def box(x,y,w,h,title,lines,color='blue',size=24):
    c=COL[color];rect(x,y,w,h,'#ffffff','#cbd9df');rect(x,y,8,h,c,rx=3)
    text(x+25,y+43,[title],28,c,True)
    text(x+25,y+83,lines,size,gap=33)

def arrow(points,color='line',dashed=False):
    c=COL.get(color,color);p=' '.join(f'{x},{y}' for x,y in points)
    S.append(f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="3.2" stroke-linejoin="round"'+(' stroke-dasharray="10 8"' if dashed else '')+'/>')
    a,b=points[-2:];dx=b[0]-a[0];dy=b[1]-a[1];n=math.hypot(dx,dy);ux,uy=dx/n,dy/n
    tip=[b,(b[0]-15*ux+6*uy,b[1]-15*uy-6*ux),(b[0]-15*ux-6*uy,b[1]-15*uy+6*ux)]
    S.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in tip)+f'" fill="{c}"/>')

def begin(title,subtitle,page):
    S.clear();S.append('<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 2400 1700"><title>'+html.escape(title)+'</title><desc>'+html.escape(subtitle)+'</desc>')
    rect(0,0,2400,1700,'#f4f7f9',rx=0);text(60,80,[title],47,bold=True)
    text(60,125,[subtitle],25,'#526d7b');text(2225,80,[f'{page} / 2'],30,'#526d7b',True)

def end(name):
    S.append('</svg>');p=O/name;p.write_text('\n'.join(S),encoding='utf8');return p

def archive(path):
    if path.exists():
        dest=R/'descontinuado'/STAMP/'fluxogramas'/path.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)

# Entradas e índices
def indices():
    begin('Das camadas de entrada aos índices','Processamento em Python • organização das camadas e apresentação no QGIS',1)
    box(60,175,650,150,'1  Base territorial',['Bacias • reservatórios • exutórios','Pampulha / Vargem das Flores / Ibirité'],size=25)
    box(875,175,650,150,'2  Preparação espacial',['SIRGAS 2000 / UTM 23S • EPSG:31983','Validar geometrias e recortar pela bacia'],size=25)
    box(1690,175,650,150,'3  Suporte da classificação',['Círculos de raio 500 m, recortados','Chave: GRID_ID + BACIA'],size=25)
    arrow([(710,250),(875,250)]);arrow([(1525,250),(1690,250)])
    sources=[('IBGE • População 2022',['Total de pessoas V0001','Rateio por área do recorte','POP_DENS • habitantes/km²']),('IBGE • Esgotamento 2022',['Rede geral/pluvial + fossa ligada','Percentual e densidade sem rede','SEM_REDE / SEWER_DENS']),('CNES + SIH/SUS',['Localizar unidades e conferir atividade','Média anual • 2016–2025','AIH_LOCAL • todas as causas']),('IBGE • Destinação do lixo',['Coleta e demais destinações','Preservar sigilo e hipóteses','WASTE_DENS • domicílios/km²']),('Vias mapeadas',['Recortar e somar comprimentos','Comprimento / área do suporte','ROAD_DENS • km/km²'])]
    for i,(title,lines) in enumerate(sources):
        x=60+465*i;box(x,400,416,205,title,lines,size=22);arrow([(x+208,605),(x+208,665)])
    box(60,665,2280,125,'4  Agregação no mesmo suporte',['Contagens, percentuais e comprimentos nos círculos de 500 m • cobertura e lacunas identificadas • círculos sobrepostos não são somados'],size=24)
    arrow([(2340,250),(2370,250),(2370,727),(2340,727)],'blue')
    box(250,870,840,250,'5A  Pressão associada à resistência',['POP_DENS → ln(1 + x)','SEM_REDE → percentual, sem logaritmo','AIH_LOCAL → ln(1 + x)','Min-max entre unidades elegíveis • S0: pesos 1, 1, 1','Internações são atividade hospitalar, não genes medidos.'],'green',24)
    box(1310,870,840,250,'5B  Pressão potencial de microplásticos',['POP_DENS + SEWER_DENS','WASTE_DENS + ROAD_DENS','Todas passam por ln(1 + x) e min-max','S0: pesos 1, 1, 1, 1','Densidades são indicadores, não massas de microplásticos.'],'blue',24)
    arrow([(670,790),(670,870)],'green');arrow([(1730,790),(1730,870)],'blue')
    text(60,1195,['6  Análises independentes para cada tema'],27,bold=True)
    boxes=[(60,'Índice multicritério',['Média ponderada das entradas','Escore de 0 a 100','Cinco classes fixas e quintis','Índice S0 alimenta o Moran'],'green'),(650,'Moran global e local',['Entrada: escore S0 e vizinhança','ARG: Queen • MP: 8 vizinhos','999 permutações + FDR de 5%','HH / LL / HL / LH / não significativo'],'purple'),(1240,'K-means',['Entrada: matriz normalizada','Pesos aplicados às variáveis','Testar K e comparar silhueta','Saída: perfis multivariados'],'blue'),(1830,'Sensibilidade dos pesos',['Comparar S0 e cenários S1–S4','Recalcular escores e grupos','Concordância / estabilidade','Não representa probabilidade'],'orange')]
    for x,title,lines,color in boxes:box(x,1255,510,225,title,lines,color,22)
    S.append('<polyline points="670,1120 670,1225 1730,1225 1730,1120" fill="none" stroke="#90a6af" stroke-width="3.2"/>')
    S.append('<polyline points="315,1225 2085,1225" fill="none" stroke="#90a6af" stroke-width="3.2"/>')
    for x in [315,1495,2085]:arrow([(x,1225),(x,1255)],'gray')
    arrow([(570,1370),(650,1370)],'purple')
    text(60,1535,['K-means compara perfis de entradas; Moran verifica a associação espacial do índice; D8 pertence ao fluxo da página 2.'],25,'#526d7b')
    rect(60,1580,2280,80,'#17384b');text(85,1616,['QGIS  •  Entradas nas unidades originais + resultados da classificação em hexágonos + tabelas e encartes por bacia'],27,'#ffffff',True)
    text(85,1648,['As transformações servem ao cálculo; população, percentuais e distâncias continuam disponíveis nas unidades de origem.'],23,'#e6eff2')
    for x in [315,905,1495,2085]:arrow([(x,1480),(x,1510)],'gray')
    return end('01_Entradas_indices.svg')

# Camadas complementares e drenagem
def contexto():
    begin('Contexto territorial e conectividade','Camadas complementares ajudam a interpretar as manchas; não recebem pesos adicionais nos índices atuais.',2)
    text(60,205,['RELEVO E ROTAS TOPOGRÁFICAS'],28,COL['blue'],True)
    text(1280,205,['CAMADAS DE CONTEXTO E CONFERÊNCIA'],28,COL['gray'],True)
    box(60,245,1060,145,'Copernicus GLO-30',['MDE em SIRGAS 2000 / UTM 23S','Base física de altitude, declividade e direção de fluxo'],size=25)
    box(60,465,505,195,'Hipsometria e declividade',['Altitude em metros','Inclinação em % • classes Embrapa','Mapas de caracterização'],size=24)
    box(615,465,505,195,'Direção e acumulação D8',['Um de oito pixels vizinhos','Área contribuinte e percurso','Conectividade topográfica'],size=24)
    arrow([(590,390),(590,420),(312,420),(312,465)],'blue');arrow([(590,420),(867,420),(867,465)],'blue')
    box(60,745,505,200,'Hidrografia e exutórios',['Cursos d’água mapeados','Reservatório delimita o destino','Exutórios orientam a área drenada'],'gray',24)
    box(615,745,505,200,'Contribuição a montante',['Área contribuinte (km²)','Distância hidrológica (km)','Rotas topográficas candidatas'],'blue',24)
    arrow([(867,660),(867,745)],'blue');arrow([(565,845),(615,845)],'gray')
    box(60,1040,505,205,'Índices espaciais da página 1',['Índice de resistência','Índice de microplásticos','Cada tema é tratado separadamente'],'green',24)
    box(615,1040,505,205,'Pressão média a montante',['Índice ponderado pela área','Agregação pelo caminho D8','Interromper percurso no reservatório'],'blue',24)
    arrow([(867,945),(867,1040)],'blue');arrow([(565,1140),(615,1140)],'green')
    rect(60,1320,1060,180,'#e6eff3','#cbd9df');text(85,1360,['Como interpretar'],28,bold=True)
    text(85,1400,['D8 não representa galerias pluviais, vazão ou transporte calibrado.','O resultado não é uma concentração, carga ou probabilidade.','Distância em linha reta e distância hidrológica são camadas distintas.'],24,gap=34)
    contexts=[(245,'Uso e cobertura da terra • 2025',['Classes nas unidades originais • ocupação e superfícies','Contextualiza urbanização e condições de escoamento.']),(485,'Licenciamento e gestão de resíduos',['Tipologias, processos, aterros, transbordo e destinação','Coleta seletiva e planos são cadastros; sem peso automático.']),(725,'Rede de esgoto de BH e cadastro de ETE',['Infraestrutura disponível e possíveis conexões','Não informa vazão nem comprova lançamento ou carga.']),(965,'Pontos de coleta e microcosmos',['Gota para amostragem • losango para experimento in situ','Referências amostrais, sem função de fonte no índice.']),(1205,'Internações por residência e filtros de causas',['Universo separado da produção hospitalar local','Não constitui área de atendimento por CEP ou bairro.'])]
    for y,title,lines in contexts:box(1280,y,1060,165,title,lines,'gray',25)
    text(1280,1450,['Conferência: CNES, IBGE, SIH, IDE-Sisema e SINIR','mantêm seus períodos, cobertura e limitações.'],25,'#526d7b',gap=35)
    rect(60,1580,2280,80,'#17384b');text(85,1616,['QGIS  •  Camadas nativas + caminhos D8 + índices independentes + reservatórios em destaque nos encartes'],27,'#ffffff',True)
    text(85,1648,['O fluxograma documenta a cadeia existente em Python / SIG. Não é um modelo executável do Modelador Gráfico do QGIS.'],23,'#e6eff2')
    arrow([(867,1245),(867,1290)],'blue');arrow([(1810,1370),(1810,1410)],'gray')
    return end('02_Contexto_conectividade.svg')

# Layout QGIS e exportação
def integrar(paths):
    os.environ['QT_QPA_PLATFORM']='offscreen'
    from qgis.core import QgsApplication,QgsProject,QgsPrintLayout,QgsLayoutItemPage,QgsLayoutItemPicture,QgsLayoutPoint,QgsLayoutSize,QgsLayoutExporter
    from qgis.PyQt.QtGui import QFontDatabase
    app=QgsApplication([],False);app.initQgis()
    for font in ['arial.ttf','arialbd.ttf']:
        p=Path('C:/Windows/Fonts')/font
        if p.exists():QFontDatabase.addApplicationFont(str(p))
    reports=[]
    for target in [R/'projeto_teco.qgz',F/'TECO_Consolidado.qgz']:
        project=QgsProject();assert project.read(str(target)),str(target)
        before={k:(v.name(),v.source(),v.providerType(),v.isValid()) for k,v in project.mapLayers().items()}
        old_names=[x.name() for x in project.layoutManager().layouts() if x.name()!='Workflow | Layers']
        archive(target)
        old=project.layoutManager().layoutByName('Workflow | Layers')
        if old:project.layoutManager().removeLayout(old)
        layout=QgsPrintLayout(project);layout.initializeDefaults();layout.setName('Workflow | Layers')
        layout.pageCollection().pages()[0].setPageSize(QgsLayoutSize(420,297))
        page=QgsLayoutItemPage(layout);page.setPageSize(QgsLayoutSize(420,297));layout.pageCollection().addPage(page)
        for i,p in enumerate(paths):
            picture=QgsLayoutItemPicture(layout);layout.addLayoutItem(picture);picture.attemptMove(QgsLayoutPoint(0,0),True,False,i);picture.attemptResize(QgsLayoutSize(420,297));picture.setPicturePath(str(p))
        project.layoutManager().addLayout(layout)
        after={k:(v.name(),v.source(),v.providerType(),v.isValid()) for k,v in project.mapLayers().items()}
        assert before==after,'Camadas alteradas'
        assert all(project.layoutManager().layoutByName(n) for n in old_names),'Layout anterior ausente'
        assert project.write(str(target))
        if target==F/'TECO_Consolidado.qgz':
            exporter=QgsLayoutExporter(layout);settings=QgsLayoutExporter.PdfExportSettings();settings.dpi=200
            assert exporter.exportToPdf(str(O/'Fluxo_camadas_QGIS.pdf'),settings)==QgsLayoutExporter.Success
            image_settings=QgsLayoutExporter.ImageExportSettings();image_settings.dpi=145
            assert exporter.exportToImage(str(O/'Fluxo_camadas_QGIS.png'),image_settings)==QgsLayoutExporter.Success
            del exporter
        reports.append({'projeto':str(target),'camadas':len(before),'validas':sum(v[3] for v in before.values()),'camadas_preservadas':True,'layouts_anteriores_preservados':True,'layout':'Workflow | Layers','paginas':2})
        print('Layout salvo: '+str(target),flush=True)
        del picture,page,layout
        project.clear()
        del project
    app.exitQgis();return reports

# PDF vetorial com texto pesquisável
def pdf_vetorial(paths):
    import xml.etree.ElementTree as ET
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import mm
    fonts=Path(os.environ.get('DOCUMENT_FONT_DIR','C:/Windows/Fonts'))
    pdfmetrics.registerFont(TTFont('FlowArial',str(fonts/'arial.ttf')))
    pdfmetrics.registerFont(TTFont('FlowArialBold',str(fonts/'arialbd.ttf')))
    target=O/'Fluxo_camadas_QGIS.pdf';archive(target)
    c=canvas.Canvas(str(target),pagesize=(420*mm,297*mm),pageCompression=1)
    c.setTitle('Fluxo das camadas no projeto QGIS');c.setAuthor('Projeto dos reservatórios urbanos')
    for path in paths:
        c.saveState();c.translate(0,297*mm);c.scale(420*mm/2400,-297*mm/1700)
        for e in ET.parse(path).getroot():
            tag=e.tag.split('}')[-1];a=e.attrib
            if tag not in ['rect','polyline','polygon','text']:continue
            fill=a.get('fill','none');stroke=a.get('stroke','none')
            if fill!='none':c.setFillColor(HexColor(fill))
            if stroke!='none':c.setStrokeColor(HexColor(stroke))
            c.setLineWidth(float(a.get('stroke-width',1)))
            c.setDash([float(v) for v in a.get('stroke-dasharray','').split()])
            if tag=='rect':
                c.roundRect(float(a['x']),float(a['y']),float(a['width']),float(a['height']),float(a.get('rx',0)),stroke=int(stroke!='none'),fill=int(fill!='none'))
            elif tag in ['polyline','polygon']:
                pts=[tuple(map(float,p.split(','))) for p in a['points'].split()];shape=c.beginPath();shape.moveTo(*pts[0])
                for point in pts[1:]:shape.lineTo(*point)
                if tag=='polygon':shape.close()
                c.drawPath(shape,stroke=int(stroke!='none'),fill=int(fill!='none'))
            else:
                c.saveState();c.translate(float(a['x']),float(a['y']));c.scale(1,-1);c.setFont('FlowArialBold' if int(a.get('font-weight',400))>=600 else 'FlowArial',float(a['font-size']));c.drawString(0,0,e.text or '');c.restoreState()
        c.restoreState();c.showPage()
    c.save()

# Execução e registro
def main():
    O.mkdir(parents=True,exist_ok=True)
    for p in O.glob('*'):
        if p.is_file():archive(p)
    paths=[indices(),contexto()]
    reports=[] if '--somente-svg' in sys.argv else integrar(paths)
    if '--somente-svg' not in sys.argv:pdf_vetorial(paths)
    record={'data':datetime.datetime.now().isoformat(),'tipo':'Fluxograma documental; não altera cálculos, pesos ou resultados','campos':['POP_DENS','SEM_REDE','AIH_LOCAL','SEWER_DENS','WASTE_DENS','ROAD_DENS','GRID_ID','BACIA'],'paginas':[{'arquivo':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],'qgis':reports,'script':'05_scripts/python/gerar_fluxogramas_camadas.py'}
    (O/'Auditoria_fluxogramas.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(record,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
