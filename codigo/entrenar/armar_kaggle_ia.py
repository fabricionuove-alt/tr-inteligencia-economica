"""Cuaderno con placa para llm_franqueza.py.  python armar_kaggle_ia.py AÑO N [DESDE]
Años <= 2020 leen el corpus; 2021+ bajan de la SEC con la lista de ie-candidatos."""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
anio, n = sys.argv[1], sys.argv[2]; desde = sys.argv[3] if len(sys.argv) > 3 else '0'
nombre = f'ie-ia-{anio}-{desde}'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f: cel(['%%writefile ' + f + '\n'] + open(f, encoding='utf-8').read().splitlines(keepends=True))
if int(anio) <= 2020:
    fuente, fuentes, archivos = 'corpus', [], ['llm_franqueza.py']
else:
    fuente, fuentes, archivos = '"$C"', ['fabri9/ie-candidatos'], ['franqueza.py', 'bajar_10k.py', 'llm_franqueza.py']
cmd = ("!cd /kaggle/working && C=$(find /kaggle/input -name candidatos.json | head -1); "
       f"timeout 470 python llm_franqueza.py {anio} {fuente} {n} {desde} 2>&1 | grep -v Warning | tee corrida.txt")
celdas = [esc(f) for f in archivos] + [cel([cmd])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': True, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': fuentes}, open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
