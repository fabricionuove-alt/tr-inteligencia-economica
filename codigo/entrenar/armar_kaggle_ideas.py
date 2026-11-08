"""Cuadernos de la señal #35.
  python armar_kaggle_ideas.py ideas DESDE HASTA     -> ie-ideas-DESDE (mejores ideas de los 13F presentados DESDE..HASTA)
  python armar_kaggle_ideas.py evaluar GRUPOS        -> ie-ideas-eval (GRUPOS = años DESDE de los cuadernos de ideas, con coma)"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f: cel(['%%writefile ' + f + '\n'] + open(f, encoding='utf-8').read().splitlines(keepends=True))
F = lambda pat: f"$(find /kaggle/input -name '{pat}' | paste -sd,)"
if sys.argv[1] == 'ideas':
    a, b = sys.argv[2], sys.argv[3]
    nombre, fuentes, archivos = f'ie-ideas-{a}', ['fabri9/ie-mercado-a', 'fabri9/ie-mercado-b'], ['mejores_ideas.py']
    cmd = f"!cd /kaggle/working && timeout 470 python mejores_ideas.py {a} {b} \"{F('cusip-*.csv')}\" 2>&1 | tee corrida.txt"
else:
    grupos = sys.argv[2].split(',')
    nombre = 'ie-ideas-eval'
    fuentes = [f'fabri9/ie-ideas-{g}' for g in grupos] + ['fabri9/ie-mercado-a', 'fabri9/ie-mercado-b', 'fabri9/ie-datos-a', 'fabri9/ie-datos-b']
    archivos = ['evaluar_ideas.py']
    juntar = ("python -c \"import json,glob,csv; f=[json.loads(l) for p in glob.glob('/kaggle/input/**/filas-*.jsonl',recursive=True) "
              "for l in open(p) if l.strip()]; w=csv.writer(open('filas.csv','w',newline='')); w.writerow(['id','anio','estado_final','sector']); "
              "[w.writerow([r['id'],r['anio'],r['estado_final'],r['sector']]) for r in f]\"")
    cmd = (f"!cd /kaggle/working && {juntar} && timeout 470 python evaluar_ideas.py \"{F('ideas-*.csv')}\" \"{F('precios-*.csv')}\" "
           f"\"{F('filas-*-acciones.csv')}\" filas.csv 2>&1 | tee corrida.txt; rm -f filas.csv")
celdas = [esc(f) for f in archivos] + [cel([cmd])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': fuentes}, open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
