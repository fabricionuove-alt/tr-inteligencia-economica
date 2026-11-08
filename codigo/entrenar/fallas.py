"""Entregas fallidas (fails-to-deliver) por empresa y mes, para la señal #47 (notas/11).
Uso: python fallas.py DESDE HASTA CUSIP_CSVS [LIMITE]
  CUSIP_CSVS: cusip-*.csv de mercado.py (CUSIP + año -> id anónimo).
Cada archivo quincenal de la SEC trae, por día y CUSIP, cuántas acciones no se entregaron a tiempo.
Salida: fallas-DESDE.csv  id, mes (aaaamm), fallas (suma de acciones), dias (días con falla)"""
import sys, io, re, time, zipfile, collections, urllib.request
import pandas as pd

UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
DESDE, HASTA = int(sys.argv[1]), int(sys.argv[2])
CUS = pd.concat([pd.read_csv(x, dtype=str) for x in sys.argv[3].split(',') if x])
LIM = int(sys.argv[4]) if len(sys.argv) > 4 else 10**6
mapa = {(c, int(a)): i for c, a, i in zip(CUS['cusip'], CUS['anio'], CUS['id'])}
def get(u):
    for i in range(4):
        try:
            time.sleep(0.12)
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120).read()
        except Exception as e:
            print('reintento', u[-40:], type(e).__name__, flush=True); time.sleep(2 + 3 * i)
    return None

t0 = time.time()
pag = get('https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data').decode('utf-8', 'ignore')
anio_de = lambda u: int(re.search(r'cnsfails(\d{4})', u).group(1)) if re.search(r'cnsfails(\d{4})', u) else 0
ftd = sorted(u for u in set(re.findall(r'href="([^"]+cnsfails[^"]+\.zip)"', pag)) if DESDE <= anio_de(u) <= HASTA)[:LIM]
print(len(ftd), 'quincenas', flush=True)
suma = collections.Counter(); dias = collections.Counter(); sin = 0
for k, u in enumerate(ftd):
    b = get('https://www.sec.gov' + u)
    if not b:
        continue
    try:
        z = zipfile.ZipFile(io.BytesIO(b))
        for l in z.read(z.namelist()[0]).decode('latin1').splitlines()[1:]:
            v = l.split('|')
            if len(v) < 6 or len(v[0]) != 8:
                continue
            try:
                q = float(v[3])
            except ValueError:
                continue
            cu, a = v[1].strip().upper(), int(v[0][:4])
            i = mapa.get((cu, a)) or mapa.get((cu, a - 1)) or mapa.get((cu, a + 1))
            if i is None:
                sin += 1; continue
            suma[(i, v[0][:6])] += q; dias[(i, v[0][:6])] += 1
    except Exception as e:
        print('archivo roto', u[-30:], type(e).__name__, flush=True)
    if k % 25 == 0:
        print(f'{k + 1}/{len(ftd)}  {len(suma)} empresa-mes  {time.time() - t0:.0f}s', flush=True)
with open(f'fallas-{DESDE}.csv', 'w') as fh:
    fh.write('id,mes,fallas,dias\n')
    for (i, m), q in suma.items():
        fh.write(f'{i},{m},{q:.0f},{dias[(i, m)]}\n')
print('FALLAS', len(suma), 'empresa-mes |', sin, 'filas sin empresa (ETF, extranjeras) |', f'{time.time() - t0:.0f}s', flush=True)
