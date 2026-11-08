"""Cuadernos ie-anon-PARTE con GPU: Gemma lee a ciegas (gemma_sae2.py ANON=1). python armar_kaggle_anon.py NOMBRE AÑOS"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
nombre, anios = sys.argv[1], sys.argv[2]
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f: cel(['%%writefile ' + f + '\n'] + open(f, encoding='utf-8').read().splitlines(keepends=True))
cmd = ("!cd /kaggle/working && cp $(find /kaggle/input -name textos-2026.jsonl | head -1) . && ANON=1 CAPAS=12 N_TOK=256 TOPK=256 python gemma_sae2.py textos-2026.jsonl 2>&1 | grep -v Downloading | tee corrida.txt") if anios == "2026" else ("!cd /kaggle/working && for f in $(find /kaggle/input -name 'textos-202[1-4].jsonl'); do cp $f .; ANON=1 CAPAS=12 N_TOK=256 TOPK=256 python gemma_sae2.py $(basename $f) 2>&1 | grep -v Downloading; done | tee corrida.txt") if anios == "2124" else (f"!cd /kaggle/working && pip -q install orjson 2>&1 | tail -1; nvidia-smi --query-gpu=name --format=csv; "
       f"for a in {anios.replace(',', ' ')}; do QUIERO=quiero.txt ANON=1 CAPAS=12 N_TOK=256 TOPK=256 timeout 1500 python gemma_sae2.py $a 2>&1 | grep -v 'Downloading\|Reconstruct\|Fetching'; done | tee corrida.txt")
celdas = [esc(f) for f in ('texto.py', 'gemma_sae2.py', 'quiero.txt')] + [cel([cmd])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': True, 'enable_internet': True, 'dataset_sources': (['fabri9/ie-temas'] if anios in ('2026', '2124') else []), 'competition_sources': [], 'kernel_sources': []}, open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
