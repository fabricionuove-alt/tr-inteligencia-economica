"""Cuadernos ie-txt3-AÑO-K (sec_textos3.py). python armar_kaggle_textos3.py AÑO K"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
a, k = sys.argv[1], sys.argv[2]; nombre = f'ie-txt3-{a}-{k}'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f: cel(['%%writefile ' + f + '\n'] + open(f, encoding='utf-8').read().splitlines(keepends=True))
ua = 'inteligencia-economica research contacto@inteligencia-economica.local'
cmd = (f"!cd /kaggle/working && curl -s -A '{ua}' -o /tmp/subs.zip https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip && "
       f"timeout 3000 python sec_textos3.py {a} quiero26-{k}.txt /tmp/subs.zip {k} 2>&1 | tee corrida.txt")
celdas = [esc(f) for f in ('franqueza.py', 'bajar_10k.py', 'texto.py', 'sec_textos3.py', f'quiero26-{k}.txt')] + [cel([cmd])]
dd = f'.kaggle-push-{nombre}'; os.makedirs(dd, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{dd}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': []}, open(f'{dd}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(dd)
