"""Cuaderno de Kaggle que baja los datos de la SEC y arma el dataset anonimizado en 4 núcleos.
    python armar_kaggle_datos.py NOMBRE SEGUNDOS   →   .kaggle-push-NOMBRE/
SEGUNDOS = corte por reloj de todo el trabajo (90 para la prueba, 480 para la de verdad)."""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NOMBRE = sys.argv[1] if len(sys.argv) > 1 else 'ie-datos-prueba'
SEG = sys.argv[2] if len(sys.argv) > 2 else '90'
BASE = int(sys.argv[3]) if len(sys.argv) > 3 else 0   # este cuaderno hace las partes BASE..BASE+3 de 8

UA = 'inteligencia-economica research contacto@inteligencia-economica.local'
guion = f'''set -u
cd /kaggle/working
echo "== empieza $(date +%T)  núcleos: $(nproc)  disco: $(df -h . | tail -1)"
curl -s -A "{UA}" -o /tmp/facts.zip https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip &
curl -s -A "{UA}" -o /tmp/subs.zip https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip &
pip install -q orjson 2>/dev/null; wait; ls -la /tmp/*.zip; echo "== bajado $(date +%T)"
for k in {BASE} {BASE+1} {BASE+2} {BASE+3}; do python construir.py /tmp/facts.zip /tmp/subs.zip filas-$k.jsonl $k 8 > registro-$k.txt 2>&1 & done
wait; echo "== armado $(date +%T)"; for f in registro-*.txt; do tail -n 2 $f; done
python - <<'EOF'
import csv, glob, json
filas = []
for p in sorted(glob.glob('filas-*.jsonl')):
    filas += [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
campos = sorted({{k for r in filas for k in r}})
w = csv.DictWriter(open('filas.csv', 'w', newline='', encoding='utf-8'), fieldnames=campos)
w.writeheader(); w.writerows(filas)
print('TOTAL', len(filas), 'filas', len({{r['id'] for r in filas}}), 'empresas')
EOF
ls -la
'''
cel = lambda src: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': src}
esc = lambda n: cel(['%%writefile ' + n + '\n'] + open(n, encoding='utf-8').read().splitlines(keepends=True))
celdas = [esc('construir.py'),
          cel(['%%writefile corrida.sh\n'] + guion.splitlines(keepends=True)),
          cel([f'!timeout {SEG} bash corrida.sh 2>&1 | tee corrida.txt'])]
d = f'.kaggle-push-{NOMBRE}'
os.makedirs(d, exist_ok=True)
json.dump({'cells': celdas, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}},
           'nbformat': 4, 'nbformat_minor': 5}, open(f'{d}/notebook.ipynb', 'w', encoding='utf-8'))
json.dump({'id': f'fabri9/{NOMBRE}', 'title': NOMBRE, 'code_file': 'notebook.ipynb', 'language': 'python',
           'kernel_type': 'notebook', 'is_private': True, 'enable_gpu': False, 'enable_internet': True,
           'dataset_sources': [], 'competition_sources': [], 'kernel_sources': []},
          open(f'{d}/kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print(d, 'listo, corte', SEG, 's')
