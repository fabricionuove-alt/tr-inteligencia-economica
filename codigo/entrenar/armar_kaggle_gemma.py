"""Cuadernos ie-sae-AÑO con GPU (gemma_sae.py). python armar_kaggle_gemma.py AÑO [LIMITE]"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[1]; lim = sys.argv[2] if len(sys.argv) > 2 else '-'; nombre = f'ie-sae-{a}' + ('-prueba' if lim != '-' else '')
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f: cel(['%%writefile ' + f + '\n'] + open(f, encoding='utf-8').read().splitlines(keepends=True))
cmd = f"!cd /kaggle/working && pip -q install orjson 2>&1 | tail -1; nvidia-smi --query-gpu=name,memory.total --format=csv; timeout 1100 python gemma_sae.py {a} {lim} 2>&1 | tee corrida.txt"
celdas = [esc(f) for f in ('texto.py', 'gemma_sae.py')] + [cel([cmd])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True,
           'enable_gpu': True, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': [],
           'model_sources': ['google/gemma-2/transformers/gemma-2-2b/1']}, open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
