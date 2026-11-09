"""Cuaderno ie-lee26 (GPU, #87 hacia adelante): Gemma lee a ciegas textos1A-2026.jsonl y textos7-2026.jsonl (512 tokens, como el pasado)."""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__))); import sys; A = sys.argv[1]; nombre = f'ie-lee{A}'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f, r: cel(['%%writefile ' + f + '\n'] + open(r, encoding='utf-8').read().splitlines(keepends=True))
cmd = (f"!cd /kaggle/working && for s in 1A 7; do cp $(find /kaggle/input -name textos$s-{A}.jsonl | head -1) . && "
       f"ANON=1 CAPAS=12 N_TOK=512 TOPK=256 LOTE=8 python gemma_sae2.py textos$s-{A}.jsonl 2>&1 | grep -v Warning | tee -a corrida.txt; rm -f textos$s-{A}.jsonl; done")
celdas = [esc('gemma_sae2.py', 'colab-sae/gemma_sae2.py'), cel([cmd])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True,
           'enable_gpu': True, 'enable_internet': True, 'dataset_sources': ['fabri9/ie-textos2122'], 'competition_sources': [], 'kernel_sources': [], 'model_sources': []},
          open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
