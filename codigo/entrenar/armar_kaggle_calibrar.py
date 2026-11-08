"""Cuaderno de calibración: mi recorte de la sección 7 (2020) contra el corpus.  python armar_kaggle_calibrar.py"""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda n: cel(['%%writefile ' + n + '\n'] + open(n, encoding='utf-8').read().splitlines(keepends=True))
UA = 'inteligencia-economica research contacto@inteligencia-economica.local'
cmd = (f"!cd /kaggle/working && curl -s -A '{UA}' -o /tmp/subs.zip https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip"
       " && timeout 420 python bajar_10k.py 2020 300 /tmp/subs.zip 0.15 0 2>&1 | tee corrida.txt"
       " && python calibrar.py franq-fuera-2020-0.csv '/kaggle/input/**/franq-2019.csv' 2>&1 | tee -a corrida.txt")
celdas = [esc('franqueza.py'), esc('bajar_10k.py'), esc('calibrar.py'), cel([cmd])]
d = '.kaggle-push-ie-calibrar'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': 'fabri9/ie-calibrar', 'title': 'ie-calibrar', 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': ['fabri9/ie-franq-2019']}, open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print('listo')
