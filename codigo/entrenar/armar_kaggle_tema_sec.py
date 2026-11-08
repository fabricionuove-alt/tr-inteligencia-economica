"""Cuadernos ie-tsec-AÑO-DESDE (tema_10k_sec.py). python armar_kaggle_tema_sec.py AÑO N DESDE"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
a, n, d = sys.argv[1:4]; nombre = f'ie-tsec-{a}-{d}'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f: cel(['%%writefile ' + f + '\n'] + open(f, encoding='utf-8').read().splitlines(keepends=True))
ua = 'inteligencia-economica research contacto@inteligencia-economica.local'
cmd = (f"!cd /kaggle/working && curl -s -A '{ua}' -o /tmp/subs.zip https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip && "
       f"timeout 1050 python tema_10k_sec.py {a} {n} {d} /tmp/subs.zip 2>&1 | tee corrida.txt")
celdas = [esc(f) for f in ('franqueza.py', 'bajar_10k.py', 'texto.py', 'agenda.py', 'davos2.py', 'temas_10k.py', 'tema_10k_sec.py')] + [cel([cmd])]
dd = f'.kaggle-push-{nombre}'; os.makedirs(dd, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{dd}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': []}, open(f'{dd}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(dd)
