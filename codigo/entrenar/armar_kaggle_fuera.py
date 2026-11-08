"""Cuadernos de la prueba fuera de muestra.
  python armar_kaggle_fuera.py candidatos                 -> ie-candidatos (lista de 10-K 2021-2025)
  python armar_kaggle_fuera.py bajar AÑO DESDE N          -> ie-fuera-AÑO-DESDE (baja y mide N balances)"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
UA = 'inteligencia-economica research contacto@inteligencia-economica.local'
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda n: cel(['%%writefile ' + n + '\n'] + open(n, encoding='utf-8').read().splitlines(keepends=True))
if sys.argv[1] == 'candidatos':
    nombre, fuentes = 'ie-candidatos', []
    cmd = (f"!cd /kaggle/working && curl -s -A '{UA}' -o /tmp/subs.zip https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip"
           " && timeout 420 python bajar_10k.py 2021,2022,2023,2024,2025 0 /tmp/subs.zip 2>&1 | tee corrida.txt")
else:
    a, desde, n = sys.argv[2], sys.argv[3], sys.argv[4]
    nombre, fuentes = f'ie-fuera-{a}-{desde}', ['fabri9/ie-candidatos']
    cmd = ("!cd /kaggle/working && C=$(find /kaggle/input -name candidatos.json | head -1) && echo \"lista: $C\""
           f" && timeout 470 python bajar_10k.py {a} {n} \"$C\" 0.15 {desde} 2>&1 | tee corrida.txt")
celdas = [esc('franqueza.py'), esc('bajar_10k.py'), cel([cmd])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': fuentes}, open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
