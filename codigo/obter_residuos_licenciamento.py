# ENTRADAS: bacias_estudo em output/04_grade_500m/teco_grade_500m.gpkg; geometria EPSG:31983.
# FONTES: WFS IDE-Sisema e catálogo CKAN do MMA; lista LAYERS e BUFFER_M editáveis abaixo.
# SAÍDAS: dados_publicos/residuos_licenciamento/originais, manifesto_downloads.json e esquemas.
from pathlib import Path
import sys,json,hashlib,time,datetime,zipfile,subprocess,argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import requests
import geopandas as gpd
from caminhos_teco import raiz_projeto
R=raiz_projeto()
OUT=R/'dados_publicos/residuos_licenciamento';RAW=OUT/'originais';RAW.mkdir(parents=True,exist_ok=True)
WFS='https://geoserver.meioambiente.mg.gov.br/ows'
BUFFER_M=20000
LAYERS={
'licencas_sla':'IDE:ide_2101_mg_empreendimentos_licenciados_pto',
'licencas_historicas':'IDE:ide_2101_mg_historico_empreendi_lic_2013_2019_pto',
'transbordo':'IDE:ide_0601_mg_loc_est_trbd_rsu_pto',
'disposicao_precaria':'IDE:ide_0601_mg_loc_lixao_pto',
'aterros_sanitarios':'IDE:ide_0601_mg_loc_at_sanit_pto',
'plano_residuos_2024':'IDE:ide_240805_mg_idam_pmgirs_2024_pol',
'competencia_municipal':'IDE:ide_2102_mg_licenciamento_ambiental_municipal_pol'}

# Consulta e proveniência
def get(url,params=None):
    error=None
    for attempt in range(3):
        try:
            r=requests.get(url,params=params,timeout=45);r.raise_for_status();return r
        except Exception as e:error=e;time.sleep(1+attempt)
    raise error
def collect(key,name,bounds):
    path=RAW/(key+'.geojson');records=[];offset=0;urls=[];matched=None
    while True:
        params={'service':'WFS','version':'2.0.0','request':'GetFeature','typeNames':name,'srsName':'EPSG:31983','outputFormat':'application/json','bbox':','.join(map(str,bounds))+',EPSG:31983','count':5000,'startIndex':offset}
        r=get(WFS,params);data=r.json();features=data.get('features')
        if features is None:raise ValueError(r.text[:200])
        urls.append(r.url);records.extend(features);matched=data.get('totalFeatures',data.get('numberMatched'))
        if len(features)<5000:break
        offset+=5000
    data['features']=records;data['numberReturned']=len(records);data['totalFeatures']=len(records)
    path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf8')
    return {'chave':key,'camada':name,'arquivo':str(path.relative_to(R)),'consulta_urls':urls,'registros':len(records),'total_servidor':matched,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'campos':list(records[0]['properties']) if records else []}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--cache',action='store_true');args=parser.parse_args()
    b=gpd.read_file(R/'output/04_grade_500m/teco_grade_500m.gpkg',layer='bacias_estudo').to_crs(31983)
    bounds=b.geometry.union_all().buffer(BUFFER_M).bounds;result=[];errors=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs={pool.submit(collect,k,v,bounds):k for k,v in LAYERS.items()}
        for job in as_completed(jobs):
            try:r=job.result();result.append(r);print(json.dumps({'layer':r['chave'],'n':r['registros']},ensure_ascii=True),flush=True)
            except Exception as e:errors.append({'chave':jobs[job],'erro':str(e)});print('ERRO',jobs[job],str(e),flush=True)
    try:
        r=get('https://dados.mma.gov.br/api/3/action/package_show',{'id':'sinir'});(RAW/'sinir_catalogo.json').write_bytes(r.content)
        resources=r.json()['result']['resources'];print('SINIR',json.dumps([{'nome':x['name'],'url':x['url']} for x in resources],ensure_ascii=True),flush=True)
        for resource in resources:
            if resource['url'].lower().endswith('.zip') and '2024' in resource['url']:
                p=RAW/'sinir_estados_municipios_2024.zip'
                if not(args.cache and p.exists()):p.write_bytes(get(resource['url']).content)
                with zipfile.ZipFile(p) as z:
                    files=z.namelist()
                    for n in files:
                        target=(RAW/'sinir_2024'/n).resolve()
                        if not target.is_relative_to((RAW/'sinir_2024').resolve()):raise ValueError('Caminho ZIP inválido')
                    z.extractall(RAW/'sinir_2024')
                result.append({'chave':'sinir_2024','url':resource['url'],'arquivo':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'arquivos':files});print('SINIR_ZIP',len(files),flush=True)
        resource=next(v for v in resources if 'relatorios-2025' in v['url'].lower())
        p=RAW/'sinir_estados_municipios_2025.rar'
        if not(args.cache and p.exists()):p.write_bytes(get(resource['url']).content)
        dest=RAW/'sinir_2025';dest.mkdir(exist_ok=True)
        listing=subprocess.check_output(['tar','-tf',str(p)]).decode('utf8',errors='replace').splitlines()
        for n in listing:
            if Path(n).is_absolute() or '..' in Path(n).parts:raise ValueError('Caminho RAR inválido')
        subprocess.run(['tar','-xf',str(p),'-C',str(dest)],check=True)
        result.append({'chave':'sinir_2025','url':resource['url'],'arquivo':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exercicio':2025,'ano_referencia':2024})
    except Exception as e:errors.append({'chave':'sinir','erro':str(e)})
    (OUT/'manifesto_downloads.json').write_text(json.dumps({'data_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'crs':'EPSG:31983','bbox_m':bounds,'buffer_m':BUFFER_M,'fontes':result,'falhas':errors},ensure_ascii=False,indent=2,default=str),encoding='utf8')
    print('CONCLUIDO',len(result),'fontes;',len(errors),'falhas',flush=True)
if __name__=='__main__':main()
