"""Cuaderno de Kaggle: prueba de fuga + entrenamiento + comparación con las reglas de los cinco.
Junta los filas-*.jsonl que dejaron los cuadernos de datos.
    python armar_kaggle_analisis.py NOMBRE FUENTE1,FUENTE2 SEGUNDOS"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NOMBRE = sys.argv[1] if len(sys.argv) > 1 else 'ie-analisis'
FUENTES = (sys.argv[2] if len(sys.argv) > 2 else 'ie-datos-a,ie-datos-b').split(',')
SEG = sys.argv[3] if len(sys.argv) > 3 else '420'
SOLO = sys.argv[4] if len(sys.argv) > 4 else ''   # 'red': sólo arma las filas y corre red.py (#52-#54)

juntar = '''import csv, glob, json
filas = []
for p in sorted(glob.glob('/kaggle/input/**/filas-*.jsonl', recursive=True)):
    filas += [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
campos = sorted({k for r in filas for k in r})
w = csv.DictWriter(open('filas.csv', 'w', newline='', encoding='utf-8'), fieldnames=campos)
w.writeheader(); w.writerows(filas)
print('TOTAL', len(filas), 'filas', len({r['id'] for r in filas}), 'empresas')
'''
guion = '''set -u
SOLO=%s
export PYTHONHASHSEED=0
cd /kaggle/working
pip install -q scikit-learn==1.9.1 2>&1 | tail -1; python -c 'import sklearn; print("sklearn", sklearn.__version__)'
python juntar.py
PR=$(find /kaggle/input -name 'precios-*.csv' | paste -sd,); DI=$(find /kaggle/input -name 'directivos-*.csv' | paste -sd,); echo "precios: $PR"
TE=$(find /kaggle/input -name 'tenencias-*.csv' | paste -sd,)
if [ -n "$PR" ]; then python precio.py filas.csv "$PR" "$DI" "$TE" || { echo "FRENO: sin precios, no sigo"; exit 1; }; fi
TX=$(find /kaggle/input -name 'texto-*.csv' | paste -sd,); echo "texto: $TX"
if [ -n "$TX" ]; then python unir_texto.py filas.csv "$TX" || { echo "FRENO: sin texto, no sigo"; exit 1; }; fi
FQ=$(find /kaggle/input -name 'franq-*.csv' | paste -sd,); echo "franqueza: $FQ"
if [ -n "$FQ" ]; then python unir_franq.py filas.csv "$FQ" || { echo "FRENO: sin franqueza, no sigo"; exit 1; }; fi
PE=$(find /kaggle/input -name 'personas.csv' | head -1); FA=$(find /kaggle/input -name 'fallas-*.csv' | sort | paste -sd,)
RD=$(find /kaggle/input -name 'red.csv' | head -1); echo "red: $RD"
OP=$(find /kaggle/input -name 'op13f-*.csv' | sort | paste -sd,); echo "op13f: $OP"
SI=$(find /kaggle/input -name 'simbolos.csv' | head -1)
TK=$(find /kaggle/input -name 'tema10k-*.csv' | sort | paste -sd,); GP=$(find /kaggle/input -name 'gemma_puntaje.csv' | head -1); [ -n "$GP" ] && TK="$TK,$GP"; echo "tema10k: $TK"
if [ "$SOLO" = "marcar84" ]; then python marcar84.py "$(find /kaggle/input -name 'wiki_vistas_2026.csv' | head -1)" "$DI"; rm -f filas.csv; exit 0; fi
if [ "$SOLO" = "mecanismo" ]; then python mecanismo_eval.py filas.csv "$(find /kaggle/input -name 'wiki_vistas.csv' | head -1)" "$DI" "$PR"; rm -f filas.csv; exit 0; fi
if [ "$SOLO" = "asesores" ]; then python asesores_eval.py filas.csv "$(find /kaggle/input -name 'asesores.csv' | head -1)" "$PR"; rm -f filas.csv; exit 0; fi
if [ "$SOLO" = "presencia" ]; then python presencia_eval.py filas.csv "$(find /kaggle/input -name 'dinastias.csv' | head -1)" "$PR"; rm -f filas.csv; exit 0; fi
if [ "$SOLO" = "familias" ]; then python familias_eval.py filas.csv "$(find /kaggle/input -name 'fam13f-*.csv' | paste -sd,)" "$PR"; rm -f filas.csv; exit 0; fi
if [ "$SOLO" = "etiquetas" ]; then curl -s -A 'inteligencia-economica research contacto@inteligencia-economica.local' -o /tmp/subs.zip https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip; python sic_de_sub.py /tmp/subs.zip sic.csv; python etiquetas.py filas.csv sic.csv etiquetas.csv; rm -f filas.csv sic.csv; exit 0; fi
if [ "${SOLO%%:*}" = "tr4" ]; then export CAMADAS="${SOLO#*:}"; [ "$CAMADAS" = "final" ] && export FINAL=1; [ "$CAMADAS" = "final12" ] && export FINAL12=1; python tr4.py filas.csv "$PE" "$FA" "$TK" tr4.json; rm -f filas.csv; exit 0; fi
if [ "${SOLO%%:*}" = "trv2" ]; then export CAMADAS="${SOLO#*:}"; [ "$CAMADAS" = "final" ] && export FINAL=1; python trv2.py filas.csv "$PE" "$FA" "$TK" trv2.json; rm -f filas.csv; exit 0; fi
if [ "$SOLO" = "confirmar62" ] || [ "$SOLO" = "sic62" ]; then
  if [ "$SOLO" = "sic62" ]; then curl -s -A 'inteligencia-economica research contacto@inteligencia-economica.local' -o /tmp/subs.zip https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip; python sic_de_sub.py /tmp/subs.zip sic.csv; export SIC=sic.csv; python alineacion.py filas.csv "$TK" consenso_anual.csv alin_explorar_sic.json; fi
  CONFIRMAR=1 python alineacion.py filas.csv "$TK" consenso_anual.csv; rm -f filas.csv; exit 0; fi
if [ "$SOLO" = "alineacion" ]; then python alineacion.py filas.csv "$TK" consenso_anual.csv; rm -f filas.csv; exit 0; fi
if [ "$SOLO" = "indice" ]; then python indice.py filas.csv indice_cambios.csv "$SI" "$PR" indice.json; rm -f filas.csv; exit 0; fi
if [ "$SOLO" = "mostrador" ]; then python mostrador.py filas.csv "$PE" "$FA" "$OP" mostrador.json; rm -f filas.csv; exit 0; fi
if [ -n "$RD" ] && [ -n "$PE" ] && [ -n "$FA" ]; then python red.py filas.csv "$PE" "$FA" "$RD" "$PR" red.json; fi
if [ "$SOLO" = "red" ]; then rm -f filas.csv; exit 0; fi
python insistencia.py filas.csv 2013 2019 insistencia.json
PE=$(find /kaggle/input -name 'personas.csv' | head -1); echo "personas: $PE"
if [ -n "$PE" ]; then python interrelacion.py filas.csv trayectorias.csv "$PE" interrelacion.json; fi
FA=$(find /kaggle/input -name 'fallas-*.csv' | sort | paste -sd,); echo "fallas: $FA"
if [ -n "$PE" ] && [ -n "$FA" ]; then python direccion.py filas.csv "$PE" "$FA" direccion.json; fi
TF=$(find /kaggle/input -name 't13f-*.csv' | sort | paste -sd,); echo "t13f: $TF"
if [ -n "$PE" ] && [ -n "$FA" ] && [ -n "$TF" ]; then python confirmacion.py filas.csv "$PE" "$FA" "$PR" "$DI" "$TF" confirmacion.json; fi
if [ -n "$PE" ] && [ -n "$FA" ]; then python cartera.py filas.csv "$PE" "$FA" cartera.json; fi
if [ -n "$PE" ] && [ -n "$FA" ]; then python kelly.py filas.csv "$PE" "$FA" kelly.json; fi
if [ -n "$PE" ] && [ -n "$FA" ]; then python placebo.py filas.csv "$PE" "$FA" placebo.json; fi
python analizar.py filas.csv resultados.json
curl -s -A 'inteligencia-economica research contacto@inteligencia-economica.local' -o /tmp/subs.zip https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip
python auditar.py filas.csv /tmp/subs.zip
python carteras.py puntajes_todos.csv carteras_13f.csv /tmp/subs.zip
rm -f puntajes_todos.csv
rm -f filas.csv
''' % (SOLO or 'todo')
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda n: cel(['%%writefile ' + n + '\n'] + open(n, encoding='utf-8').read().splitlines(keepends=True))
celdas = [esc('reglas_de_los_cinco.py'), esc('analizar.py'), esc('insistencia.py'), esc('interrelacion.py'), esc('direccion.py'), esc('confirmacion.py'), esc('cartera.py'), esc('kelly.py'), esc('placebo.py'), esc('red.py'), esc('mostrador.py'), esc('indice.py'), esc('alineacion.py'), esc('trv2.py'), esc('tr4.py'), esc('etiquetas.py'), esc('familias_eval.py'), esc('presencia_eval.py'), esc('asesores_eval.py'), esc('mecanismo_eval.py'), esc('marcar84.py'), esc('sic_de_sub.py'), esc('consenso_anual.csv'), esc('indice_cambios.csv'), esc('precio.py'), esc('unir_texto.py'), esc('unir_franq.py'), esc('auditar.py'), esc('carteras.py'), esc('carteras_13f.csv'),
          cel(['%%writefile juntar.py\n'] + juntar.splitlines(keepends=True)),
          cel(['%%writefile corrida.sh\n'] + guion.splitlines(keepends=True)),
          cel([f'!timeout {SEG} bash corrida.sh 2>&1 | tee corrida.txt'])]
d = f'.kaggle-push-{NOMBRE}'
os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}},
           'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{NOMBRE}', 'title': NOMBRE, 'code_file': 'notebook.ipynb', 'language': 'python',
           'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True,
           'dataset_sources': (['fabri9/ie-temas'] if SOLO.startswith(('trv2', 'tr4')) else []), 'competition_sources': [], 'kernel_sources': [f'fabri9/{x}' for x in FUENTES]},
          open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d, 'listo, corte', SEG, 's, fuentes', FUENTES)
