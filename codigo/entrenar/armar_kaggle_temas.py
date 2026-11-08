"""Cuadernos ie-tema10k-AÑO (temas_10k.py). python armar_kaggle_temas.py AÑO"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[1]; nombre = f'ie-tema10k-{a}'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f: cel(['%%writefile ' + f + '\n'] + open(f, encoding='utf-8').read().splitlines(keepends=True))
celdas = [esc(f) for f in ('texto.py', 'agenda.py', 'davos2.py', 'temas_10k.py')] + [cel([f'!cd /kaggle/working && pip -q install orjson 2>&1 | tail -1; timeout 1100 python temas_10k.py {a} 2>&1 | tee corrida.txt'])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': []}, open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
