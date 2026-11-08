"""Baja 10-K directo de la SEC, recorta la sección 7 (explicación de la dirección) y mide franqueza
con EXACTAMENTE la misma función de franqueza.py.
Uso: python bajar_10k.py AÑOS N_POR_AÑO SUBS(zip|carpeta) [PAUSA] [CIKS]
  AÑOS: años de presentación, ej. 2021,2022
  N_POR_AÑO: cuántas empresas al azar por año (semilla fija 7)
  CIKS: opcional, archivo con CIKs a forzar (para la calibración contra el corpus)
Salida: franq-fuera-<primer año>.csv (id, anio_presentado, medidas, palabras_sec7)"""
import sys, os, re, io, json, time, html, random, zipfile, hashlib, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from franqueza import medir

UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
TAG = re.compile(r'(?is)<(script|style).*?</\1>|<[^>]+>')
ESP = re.compile(r'[ \t\r\f\v\xa0]+')
# Inicio de la sección 7 y fin (7A u 8). Se toma el tramo MÁS LARGO: el primero suele ser el índice.
INI = re.compile(r'(?i)item\s*7\s*[\.\:\-–—]?\s*management[’\'`s]*\s+discussion')
FIN = re.compile(r'(?i)item\s*(?:7a\s*[\.\:\-–—]?\s*quantitative|8\s*[\.\:\-–—]?\s*financial\s+statements)')

def a_texto(b):
    t = b.decode('utf-8', 'ignore')
    t = TAG.sub(' ', t)
    t = html.unescape(t)
    return ESP.sub(' ', t)

def seccion7(t):
    mejor = ''
    for m in INI.finditer(t):
        f = FIN.search(t, m.end())
        tramo = t[m.end(): f.start() if f else min(len(t), m.end() + 400000)]
        if len(tramo) > len(mejor):
            mejor = tramo
    return mejor

def get(u, pausa):
    for i in range(4):
        try:
            time.sleep(pausa)
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
        except Exception as e:
            if '404' in str(e):
                return None
            time.sleep(3 + 5 * i)
    return None

def candidatos(subs, anios):
    """{año: [(cik, acc, doc)]} primer 10-K de cada empresa operativa en ese año."""
    out = {a: [] for a in anios}
    fuente = zipfile.ZipFile(subs) if not os.path.isdir(subs) else None
    nombres = fuente.namelist() if fuente else [n for n in os.listdir(subs)]
    for n in nombres:
        if not (n.startswith('CIK') and n.endswith('.json') and '-submissions-' not in n):
            continue
        s = json.loads(fuente.read(n) if fuente else open(os.path.join(subs, n), encoding='utf-8').read())
        if s.get('entityType') not in (None, '', 'operating'):
            continue
        r = s.get('filings', {}).get('recent', {})
        visto = set()
        for f, fo, acc, doc in zip(r.get('filingDate', []), r.get('form', []), r.get('accessionNumber', []), r.get('primaryDocument', [])):
            a = int(f[:4])
            if fo == '10-K' and a in out and a not in visto and doc:
                out[a].append((n[3:13], acc, doc)); visto.add(a)
    return out

if __name__ == '__main__':
    ANIOS = [int(a) for a in sys.argv[1].split(',')]
    N = int(sys.argv[2]); SUBS = sys.argv[3]
    PAUSA = float(sys.argv[4]) if len(sys.argv) > 4 else 0.12
    DESDE = int(sys.argv[5]) if len(sys.argv) > 5 else 0      # tramo de la lista al azar (para repartir en cuadernos)
    FORZAR = None
    t0 = time.time()
    if SUBS.endswith('.json'):            # lista ya armada por otro cuaderno
        cand = {int(k): [tuple(x) for x in v] for k, v in json.load(open(SUBS)).items()}
    else:
        cand = candidatos(SUBS, ANIOS)
    print('candidatos por año:', {a: len(cand.get(a, [])) for a in ANIOS}, f'{time.time()-t0:.0f}s', flush=True)
    if N == 0:                             # sólo armar la lista y salir
        json.dump({str(a): v for a, v in cand.items()}, open('candidatos.json', 'w')); print('candidatos.json listo'); sys.exit(0)
    rng = random.Random(7)
    filas = []
    cols = ['franq_numeros', 'franq_cliches', 'franq_euforia', 'franq_admite', 'franq_nosotros', 'franq_niebla', 'franq_largo']
    nombre = f'franq-fuera-{ANIOS[0]}-{DESDE}.csv'
    fh = open(nombre, 'w')                 # se guarda fila por fila: si el reloj corta, lo hecho queda
    fh.write(','.join(['id', 'cik', 'anio_presentado'] + cols) + chr(10)); fh.flush()
    for a in ANIOS:
        lista = [c for c in cand[a] if (FORZAR is None or c[0].lstrip('0') in FORZAR or c[0] in FORZAR)]
        rng.shuffle(lista); lista = lista[DESDE:DESDE + N]
        ok = sin7 = 0
        for k, (cik, acc, doc) in enumerate(lista):
            b = get(f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-", "")}/{doc}', PAUSA)
            if not b:
                continue
            s7 = seccion7(a_texto(b))
            m = medir(s7)
            if not m:
                sin7 += 1; continue
            m.update({'id': h(cik), 'anio_presentado': a, 'cik': cik}); filas.append(m); ok += 1
            fh.write(','.join([m['id'], cik, str(a)] + [str(m[c]) for c in cols]) + chr(10)); fh.flush()
            if k % 200 == 0:
                print(f'  {a}: {k+1}/{len(lista)}  con sección 7: {ok}  sin: {sin7}  {time.time()-t0:.0f}s', flush=True)
        print(f'año {a}: {ok} con sección 7, {sin7} sin recortar', flush=True)
    fh.close()
    print(f'LISTO {len(filas)} filas en {time.time()-t0:.0f}s -> {nombre}', flush=True)
