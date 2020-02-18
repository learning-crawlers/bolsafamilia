# -*- coding: utf-8 -*-
import os
import csv
import json
import hashlib
from urllib.request import urlopen
import requests
from datetime import datetime
from dateutil import relativedelta
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor,as_completed
import zipfile

def get_time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_last_month():
    return datetime.today() - relativedelta.relativedelta(months=1)

def download_file(url):
    file_name = f"{url.split('/')[-1]}_BolsaFamilia_Pagamentos"
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BSAFML_ROOT = os.path.join(BASE_DIR, "bolsafamilia")
    ZIP_FILE = f'{file_name}.zip'
    CSV_FILE = f'{file_name}.csv'

    # download big file if the zip does not exists
    if not os.path.isfile(f'{BSAFML_ROOT}/{ZIP_FILE}'):
        content_length = int(urlopen(url).info().get('Content-Length', -1))
        
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(f'{ZIP_FILE}', 'wb') as f:
                pbar = tqdm(total=content_length)
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        pbar.update(8192)

        # extract if the csv does not exists
        if not os.path.isfile(f'{BSAFML_ROOT}/{CSV_FILE}'):
            
            with zipfile.ZipFile(f'{BSAFML_ROOT}/{ZIP_FILE}', 'r') as fzip: 
                fzip.extractall(BSAFML_ROOT)

    # reading data
    with open(f'{BSAFML_ROOT}/{CSV_FILE}', 
            encoding='utf-8', errors='ignore') as f:

        reader = csv.reader(f, delimiter=';')
        first = True

        for row in reader:
            if not first:
                ms_referncia = row[0]
                ms_competncia = row[1]
                uf = row[2]
                cdigo_municpio_siafi = row[3]
                nome_municpio = row[4]
                nis_favorecido = row[5]
                nome_favorecido = row[6]
                valor_parcela = row[7]

                dict_bf = { 
                    'ms_referncia': ms_referncia, 
                    'ms_competncia': ms_competncia, 
                    'uf': uf, 
                    'cdigo_municpio_siafi': cdigo_municpio_siafi, 
                    'nome_municpio': nome_municpio, 
                    'nis_favorecido': nis_favorecido, 
                    'nome_favorecido': nome_favorecido, 
                    'valor_parcela': valor_parcela 
                }
                
                # hashing json file name
                hash = hashlib.sha224(f'{ms_referncia}\
                    {ms_competncia}{uf}{cdigo_municpio_siafi}{nis_favorecido}\
                    {valor_parcela}'.encode('utf-8')).hexdigest()
                
                file_json = f'{BSAFML_ROOT}/data/{hash.lower()}.json'

                # save file 
                with open(file_json, mode="w") as f:
                    f.write(json.dumps(dict_bf, indent=4))

                print(f'{get_time_now()} [ Ok ] {hash} {nome_favorecido}')

            else:
                first = not first

    return f'{CSV_FILE}'

#===============================================================================
if __name__ == '__main__':
    URL_BOLSA_FAMI_PAGTOS = 'http://transparencia.gov.br/download-de-dados'
    URL_BOLSA_FAMI_PAGTOS = f'{URL_BOLSA_FAMI_PAGTOS}/bolsa-familia-pagamentos'

    quantityOfMonths = 1 # just one
    monthList = [ 
        (get_last_month() - relativedelta.relativedelta(months=x))
                                                    .strftime('%Y%m') 
        for x in range(quantityOfMonths) 
    ]

    # threading in python to run faster (asynchronous)
    with ThreadPoolExecutor(max_workers=3) as executor:
        for thread in as_completed({ 
                executor.submit(
                    download_file, 
                    f'{URL_BOLSA_FAMI_PAGTOS}/{yearMonthReferency}'
                ): yearMonthReferency for yearMonthReferency in monthList 
            }):
            try:
                thread.result()
            except Exception as e:
                print(e)

    exit(0)