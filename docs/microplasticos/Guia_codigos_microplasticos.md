# Guia dos scripts | Complementação microplásticos

Os caminhos são relativos à raiz do TECO, configurável por TECO_PROJECT_ROOT ou codigo/caminhos_projeto.json. A configuração de critérios e pesos fica em config/microplasticos.json. Os grandes arquivos de base não acompanham o repositório público. A reprodução exige fornecer as entradas descritas no cabeçalho de cada script.

## obter_residuos_licenciamento.py

Baixa os sete serviços WFS e as exportações SINIR. Requests aplica tempo limite e tentativas; a consulta usa bbox em EPSG:31983 e paginação. SHA-256 documenta integridade. O RAR exige tar disponível. Originais de licenciamento ficam locais, pois podem conter CPF.

Trecho do arquivo, a partir da linha 33.

```python
    while True:
        params={'service':'WFS','version':'2.0.0','request':'GetFeature','typeNames':name,'srsName':'EPSG:31983','outputFormat':'application/json','bbox':','.join(map(str,bounds))+',EPSG:31983','count':5000,'startIndex':offset}
        r=get(WFS,params);data=r.json();features=data.get('features')
        if features is None:raise ValueError(r.text[:200])
        urls.append(r.url);records.extend(features);matched=data.get('totalFeatures',data.get('numberMatched'))
```

## microplasticos_teco.py

GeoPandas recorta e agrega geometrias; Pandas lê o CSV censitário em blocos. Os limites UNC_LO/UNC_HI preservam o sigilo. NumPy transforma critérios e calcula o índice. SciPy executa k-means e distâncias; moran_w e BH vêm do módulo estatístico anterior. Rasterio rasteriza o índice e deque percorre o grafo D8 sem ciclos.

Trecho do arquivo, a partir da linha 128.

```python
    for code,ww in C['cenarios'].items():
        w=np.asarray(ww);wx=x*np.sqrt(w/w.sum());score=100*(x@w)/w.sum();scores[code]=score;g['MP_'+code]=np.nan;g.loc[idx,'MP_'+code]=score
        for k in C['k_testados']:
            loss,cent,lab=fitkm(wx,k,SEED+100*int(code[1:]),starts=20);sil=silhouette(wx,lab);sizes=np.bincount(lab,minlength=k)
            ks.append({'scenario':code,'k':k,'silhouette':sil,'min_n':int(sizes.min()),'inertia':loss});models[code,k]=(cent,lab)
```

Os pesos são aplicados à média do índice e, pela raiz quadrada, à distância do k-means. O Moran local não usa os grupos do k-means como entrada: usa o índice e a matriz de vizinhança. O teste local tem 999 permutações condicionais sem reposição por vizinho; os p-valores são corrigidos por BH dentro de cada bacia. O processamento D8 acumula índice × área e área válida; a divisão gera média de pressão a montante, sem simular massa ou decaimento.

## mapas_microplasticos_teco.py

Matplotlib compõe três mapas com mesma escala e geometria de impressão. GeoPandas representa setores nativos ou hexágonos conforme o produto. PyProj converte somente rótulos das coordenadas. Rasterio fornece a extensão dos rasters. A legenda mostra unidades físicas nas entradas e índice nos resultados.

Trecho do arquivo, a partir da linha 35.

```python
def start(title):
    fig=plt.figure(figsize=(30/2.54,12.7/2.54));fig.suptitle(title,y=.975,fontsize=12.3,fontweight='bold',color='#244853');axes=[]
    for j,r in enumerate(b.itertuples()):
        ax=fig.add_axes([.05+j*.325,.23,.27,8.1/12.7]);axes.append(ax);v=views.get(r.id,{})
        cx=(r.geometry.bounds[0]+r.geometry.bounds[2])/2+v.get('dx',0);cy=(r.geometry.bounds[1]+r.geometry.bounds[3])/2+v.get('dy',0);span=v.get('span',18225)
```

## consolidar_microplasticos_teco.py

Exporta um shapefile por pasta, encurta nomes de campo com mapeamento explícito, copia tabelas, mapas e scripts, atualiza dicionário global e calcula inventário SHA-256. As versões geradas substituídas são movidas a descontinuado. Não altera arquivos brutos.

Trecho do arquivo, a partir da linha 48.

```python
  assert dst.resolve().is_relative_to((R/'descontinuado').resolve());shutil.move(str(p),str(dst))
def export(g,relative,name,defs):
 folder=F/relative;archive(folder);folder.mkdir(parents=True,exist_ok=True);data=g[list(defs)+['geometry']].copy();rename={k:v[0] for k,v in defs.items()};data.rename(columns=rename,inplace=True)
 for c in data.select_dtypes(include=['object','str']).columns:
  if c!='geometry':data[c]=data[c].map(lambda v:v[:250] if isinstance(v,str) else v)
```

## integrar_qgis_microplasticos.py

PyQGIS abre os dois projetos atuais, cria grupo Microplastics e camadas temáticas, aplica estilos e duplica seis layouts triplos sem reconstruir os grupos anteriores. Mantém caminhos relativos e arquiva os projetos antes da atualização.

Trecho do arquivo, a partir da linha 93.

```python
    if oldlayout:manager.removeLayout(oldlayout)
    layout=manager.duplicateLayout(template,name)
    for item in layout.items():
     if isinstance(item,QgsLayoutItemMap):
      stack=item.layers();new=[];replaced=False
```

## documentar_microplasticos_teco.py

Lê auditoria e tabelas, produz texto, tabelas e pranchas em PDF com ReportLab e a página HTML. O guia incorpora trechos do código efetivamente salvo. Não recalcula indicadores nem reclassifica dados.

Trecho do arquivo, a partir da linha 185.

```python
# PDF com pranchas em página horizontal
def pdf(md,gallery):
 from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,Table,TableStyle,PageBreak,NextPageTemplate,Image,KeepTogether
 from reportlab.lib import colors
 from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
```

## reproduzir_microplasticos.py

Reproduz a classificação e os testes a partir do GeoJSON derivado publicado, sem baixar novamente as fontes ou processar o MDE. Confere diferença absoluta do índice e interrompe se exceder 1e-8. A reconstrução de censos e caminhos D8 exige a cadeia completa.

Trecho do arquivo, a partir da linha 14.

```python
    g=gpd.read_file(R/'dados/microplasticos/grade_microplasticos.geojson');expected=g.MP_INDEX.copy();engine.O=O
    g,meta=engine.classify(g);g=engine.spatial(g);diff=float(np.nanmax(abs(g.MP_INDEX-expected)))
    assert diff<1e-8,'Índice divergente do produto publicado'
    g.to_file(O/'classificacao_reproduzida.gpkg',layer='microplastic_pressure',driver='GPKG')
    report={**meta,'max_abs_difference':diff,'sources_reprocessed':False};(O/'validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'records':len(g),'eligible':meta['n_valid'],'max_abs_difference':diff},ensure_ascii=True))
```

## mapas_intermediarios_microplasticos.py

Agrupa a atividade principal em tipologias documentais, sem atribuir emissão; produz sete mapas, camadas nativas e dicionários de resíduos e licenciamento. As hipóteses de conexão do processo com microplásticos permanecem separadas da classificação do índice.

Trecho do arquivo, a partir da linha 21.

```python
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',str(s).lower()) if not unicodedata.combining(c))
def typology(s):
 s=norm(s)
 if any(v in s for v in ['plastic','termoplastic','polimero','borracha','textil','lavander']):return 1
 if any(v in s for v in ['incinera','tratamento de esgoto','tratamento de residuos']):return 4
```

## integrar_intermediarios_microplasticos.py

Inclui os produtos intermediários nos dois QGIS, com um grupo por bacia e sete layouts triplos. Os mapas mantêm o recorte do encarte, os atributos nativos e a distinção entre declaração municipal e fonte localizada.

Trecho do arquivo, a partir da linha 58.

```python
# Integração reutilizável
def add_intermediates(project,parent):
 old=parent.findGroup('Intermediate inputs')
 if old:
  ids=[n.layerId() for n in old.findLayers()];parent.removeChildNode(old)
```

## atualizar_visualizador_intermediarios.py

Monta o visualizador a partir do item 2, insere os mapas intermediários junto aos itens metodológicos e produz prévias públicas. Não exclui o texto introdutório do relatório de referência e não recalcula indicadores.

Trecho do arquivo, a partir da linha 25.

```python
 return '<figure><h3>'+html.escape(item['title'])+'</h3><a href="'+link+'"><img loading="lazy" src="'+src+'" alt="'+html.escape(item['title'])+'"></a><figcaption>'+html.escape(EXPLANATIONS.get(item['id'],''))+'</figcaption></figure>'
def build(public,gallery):
 md=doc.text();body=doc.html_body('# Pressões potenciais de genes de resistência e microplásticos\n\n## 2.'+md.split('## 2.',1)[1]);items={g['id']:g for g in gallery}
 counts=pd.read_csv(O/'tabelas/licencas_por_tipologia.csv',sep=';').groupby(['TP_CODE','TP_NAME']).size().reset_index(name='Registros')
 tab=counts[['TP_NAME','Registros']].to_html(index=False,escape=True)
```

## Ordem de execução

1. Configurar a raiz e conferir entradas.
2. Executar obter_residuos_licenciamento.py para nova consulta, ou preservar a exportação documentada.
3. Executar microplasticos_teco.py.
4. Executar mapas_microplasticos_teco.py.
5. Executar consolidar_microplasticos_teco.py.
6. Executar integrar_qgis_microplasticos.py no Python do QGIS.
7. Executar documentar_microplasticos_teco.py com ReportLab.

Uma nova variável requer agregação no preparador, definição de transformação/unidade na configuração, pesos em todos os cenários e novos testes de cobertura e redundância. Não reutilizar os pesos como coeficientes de emissão.
