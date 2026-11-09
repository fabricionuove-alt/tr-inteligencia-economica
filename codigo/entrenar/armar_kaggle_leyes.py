"""Cuaderno ie-bis (GPU, #90): Gemma lee a ciegas un pedazo de cada discurso de banquero central 2011-2020."""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__))); nombre = 'ie-leyes'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f, r: cel(['%%writefile ' + f + '\n'] + open(r, encoding='utf-8').read().splitlines(keepends=True))
cmd = "!cd /kaggle/working && cp $(find /kaggle/input -name leyes.jsonl | head -1) . && ANON=1 CAPAS=12 N_TOK=256 TOPK=256 LOTE=16 python gemma_sae2.py leyes.jsonl 2>&1 | grep -v Warning | tee corrida.txt; rm -f leyes.jsonl"
celdas = [esc('gemma_sae2.py', 'colab-sae/gemma_sae2.py'), cel([cmd])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True,
           'enable_gpu': True, 'enable_internet': True, 'dataset_sources': ['fabri9/ie-leyes-textos'], 'competition_sources': [], 'kernel_sources': [], 'model_sources': []},
          open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
