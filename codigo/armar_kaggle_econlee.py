"""Cuaderno GPU: Qwen lee un tramo de los cables económicos que nombran empresas. python armar_kaggle_econlee.py NOMBRE DESDE HASTA"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__))); nombre, a, b = sys.argv[1:4]
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f, r: cel(['%%writefile ' + f + '\n'] + open(r, encoding='utf-8').read().splitlines(keepends=True))
cmd = f"!cd /kaggle/working && python cables_lee.py $(find /kaggle/input -name econ.jsonl | head -1) {a} {b} 2>&1 | grep -v Warning | tee corrida.txt"
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': [esc('cables_lee.py', 'cables_lee.py'), cel([cmd])], 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True,
           'enable_gpu': True, 'enable_internet': True, 'dataset_sources': ['fabri9/ie-econ-cables'], 'competition_sources': [], 'kernel_sources': [], 'model_sources': []},
          open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
