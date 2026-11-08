"""Cuadernos de la señal #42.
  python armar_kaggle_creyentes.py t13f DESDE HASTA   -> ie-t13f-DESDE (tenencias de fondos concentrados, 13F presentados DESDE..HASTA)
  python armar_kaggle_creyentes.py evaluar GRUPOS      -> ie-creyentes (GRUPOS = años DESDE de los cuadernos t13f, con coma)"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda f: cel(['%%writefile ' + f + '\n'] + open(f, encoding='utf-8').read().splitlines(keepends=True))
F = lambda pat: f"$(find /kaggle/input -name '{pat}' | paste -sd,)"
if sys.argv[1] == 't13f':
    a, b = sys.argv[2], sys.argv[3]
    nombre, fuentes, archivos = f'ie-t13f-{a}', ['fabri9/ie-mercado-a', 'fabri9/ie-mercado-b'], ['mejores_ideas.py', 'tenencias_13f.py']
    cmd = f"!cd /kaggle/working && timeout 900 python tenencias_13f.py {a} {b} \"{F('cusip-*.csv')}\" 2>&1 | tee corrida.txt"
elif sys.argv[1] == 'fam13f':
    a, b = sys.argv[2], sys.argv[3]
    nombre, fuentes, archivos = f'ie-fam13f-{a}', ['fabri9/ie-mercado-a', 'fabri9/ie-mercado-b'], ['mejores_ideas.py', 'familias_13f.py']
    cmd = f"!cd /kaggle/working && timeout 1100 python familias_13f.py {a} {b} \"{F('cusip-*.csv')}\" 2>&1 | tee corrida.txt"
elif sys.argv[1] == 'op13f':
    a, b = sys.argv[2], sys.argv[3]
    nombre, fuentes, archivos = f'ie-op13f-{a}', ['fabri9/ie-mercado-a', 'fabri9/ie-mercado-b'], ['mejores_ideas.py', 'opciones_13f.py']
    cmd = f"!cd /kaggle/working && timeout 1100 python opciones_13f.py {a} {b} \"{F('cusip-*.csv')}\" 2>&1 | tee corrida.txt"
else:
    grupos = sys.argv[2].split(',')
    nombre = 'ie-creyentes'
    fuentes = [f'fabri9/ie-t13f-{g}' for g in grupos] + ['fabri9/ie-mercado-a', 'fabri9/ie-mercado-b', 'fabri9/ie-datos-a', 'fabri9/ie-datos-b']
    archivos = ['creyentes.py']
    juntar = ("python -c \"import json,glob,csv; f=[json.loads(l) for p in glob.glob('/kaggle/input/**/filas-*.jsonl',recursive=True) "
              "for l in open(p) if l.strip()]; w=csv.writer(open('filas.csv','w',newline='')); w.writerow(['id','anio','estado_final']); "
              "[w.writerow([r['id'],r['anio'],r['estado_final']]) for r in f]\"")
    cmd = (f"!cd /kaggle/working && {juntar} && timeout 1100 python creyentes.py \"{F('t13f-*.csv')}\" \"{F('precios-*.csv')}\" "
           f"\"{F('filas-*-acciones.csv')}\" filas.csv \"{F('directivos-*.csv')}\" creyentes.json 2>&1 | tee corrida.txt; rm -f filas.csv")
celdas = [esc(f) for f in archivos] + [cel([cmd])]
d = f'.kaggle-push-{nombre}'; os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{nombre}', 'title': nombre, 'code_file': 'notebook.ipynb', 'language': 'python', 'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True, 'dataset_sources': [], 'competition_sources': [], 'kernel_sources': fuentes}, open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d)
