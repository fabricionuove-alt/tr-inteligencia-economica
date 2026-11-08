"""Cuaderno de Kaggle de la señal #47: entregas fallidas por empresa y mes.
  python armar_kaggle_fallas.py DESDE HASTA   -> ie-fallas-DESDE"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
a, b = sys.argv[1], sys.argv[2]
nombre = f'ie-fallas-{a}'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f: cel(['%%writefile ' + f + '\n'] + open(f, encoding='utf-8').read().splitlines(keepends=True))
cmd = f"!cd /kaggle/working && timeout 1100 python fallas.py {a} {b} \"$(find /kaggle/input -name 'cusip-*.csv' | paste -sd,)\" 2>&1 | tee corrida.txt"
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': [esc('fallas.py'), cel([cmd])], 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': ['fabri9/ie-mercado-a', 'fabri9/ie-mercado-b']}, open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
