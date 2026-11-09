"""Cuaderno ie-llamadas con GPU (#88): baja las conferencias, arma los jsonl y Gemma los lee a ciegas."""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__))); nombre = 'ie-llamadas'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f: cel(['%%writefile ' + f + '\n'] + open('colab-sae/' + f, encoding='utf-8').read().splitlines(keepends=True))
url = 'https://huggingface.co/datasets/kurry/sp500_earnings_transcripts/resolve/main/parquet_files/part-0.parquet'
env = "ANON=1 CAPAS=12 N_TOK=512 TOPK=256 LOTE=8"
cmd = (f"!cd /kaggle/working && wget -q -O part-0.parquet {url} && python llamadas.py 2>&1 | tee corrida.txt && rm part-0.parquet && "
       f"for a in 2013 2014 2015 2016 2017 2018 2019 2020; do {env} python gemma_sae2.py llamadas-$a.jsonl 2>&1 | grep -v Warning | tee -a corrida.txt; done")
celdas = [esc(f) for f in ('llamadas.py', 'gemma_sae2.py')] + [cel([cmd])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True,
           'enable_gpu': True, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': [], 'model_sources': []},
          open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
