"""Cuaderno ie-sec-<SECCION> con GPU: Gemma lee a ciegas una sección del 10-K, años 2013-2020 (#87). python armar_kaggle_seccion.py 1A|7"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s = sys.argv[1]; nombre = f'ie-sec-{s.lower()}'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f, ruta: cel(['%%writefile ' + f + '\n'] + open(ruta, encoding='utf-8').read().splitlines(keepends=True))
env = f"QUIERO=/kaggle/working/quiero.txt ANON=1 CAPAS=12 N_TOK=512 TOPK=256 LOTE=8 SECCION=section_{s} SALTO=1500"
cmd = (f"!cd /kaggle/working && pip -q install orjson 2>&1 | tail -1; nvidia-smi --query-gpu=name,memory.total --format=csv; "
       f"for a in 2013 2014 2015 2016 2017 2018 2019 2020; do {env} python gemma_sae2.py $a 2>&1 | grep -v Warning | tee -a corrida.txt; done")
celdas = [esc(f, 'colab-sae/' + f) for f in ('texto.py', 'gemma_sae2.py', 'quiero.txt')] + [cel([cmd])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True,
           'enable_gpu': True, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': [], 'model_sources': []},
          open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
