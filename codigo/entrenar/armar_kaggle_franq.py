"""Cuaderno de Kaggle para franqueza.py.  python armar_kaggle_franqueza.py NOMBRE SEGUNDOS AÑOS [LIMITE]"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NOMBRE, SEG, ANIOS = sys.argv[1], sys.argv[2], sys.argv[3]
LIM = sys.argv[4] if len(sys.argv) > 4 else '-'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda n: cel(['%%writefile ' + n + '\n'] + open(n, encoding='utf-8').read().splitlines(keepends=True))
celdas = [esc('franqueza.py'), cel([f'!pip install -q orjson; cd /kaggle/working && timeout {SEG} python franqueza.py {ANIOS} {LIM} 2>&1 | tee corrida.txt'])]
d = f'.kaggle-push-{NOMBRE}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}},
           'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{NOMBRE}', 'title': NOMBRE, 'code_file': 'notebook.ipynb', 'language': 'python',
           'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True,
           'dataset_sources': [], 'competition_sources': [], 'kernel_sources': []},
          open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d, 'listo', ANIOS, LIM)
