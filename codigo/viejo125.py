"""#125: mediana de similitud 10-K vs año anterior, 1997-2009 (muestra 300/año), contra S&P 500 a 4 años. Reglas en notas/11 (#125)."""
import os, re, io, gzip, json, time, threading, urllib.request, numpy as np, pandas as pd
from concurrent.futures import ThreadPoolExecutor
from sklearn.feature_extraction.text import HashingVectorizer
from scipy.stats import spearmanr
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; SAL = f'{B}/entrenar/sal-cab102/viejo125.jsonl'
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
hv = HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm='l2', alternate_sign=False)
lock = threading.Lock(); ult = [0.0]
def espera():
    with lock:
        w = 0.13 - (time.time() - ult[0])
        if w > 0: time.sleep(w)
        ult[0] = time.time()
def get(u, primer_doc=False):
    for k in range(5):
        espera()
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120)
            if not primer_doc: return r.read()
            buf = b''
            while True:
                c = r.read(1 << 16)
                if not c: break
                buf += c; i = buf.find(b'</DOCUMENT>')
                if i >= 0: return buf[:i]
                if len(buf) > 30_000_000: break
            return buf
        except Exception as e:
            if '404' in str(e): return None
            time.sleep(5 * (k + 1))
    return None
pat = re.compile(r'^(10-K405|10-K)\s+.*?\s(\d+)\s+(\d{4}-\d{2}-\d{2})\s+(\S+)\s*$')
idx = {}
for y in range(1996, 2010):
    d = {}
    for q in range(1, 5):
        f = f'{B}/fuentes/edgar-idx/{y}q{q}.gz'
        if not os.path.exists(f):
            os.makedirs(os.path.dirname(f), exist_ok=True); open(f, 'wb').write(get(f'https://www.sec.gov/Archives/edgar/full-index/{y}/QTR{q}/form.gz'))
        for l in gzip.open(f, 'rt', encoding='latin-1'):
            m = pat.match(l)
            if m:
                c, fe, p = int(m.group(2)), m.group(3), m.group(4)
                if c not in d or fe < d[c][0]: d[c] = (fe, p)
    idx[y] = d; print('indice', y, len(d), flush=True)
hechos = {(o['y'], o['cik']) for o in map(json.loads, open(SAL))} if os.path.exists(SAL) else set()
tareas = []
for y in range(1997, 2010):
    comunes = sorted(set(idx[y]) & set(idx[y - 1])); rng = np.random.default_rng(0)
    for c in rng.choice(comunes, 300, replace=False): 
        if (y, int(c)) not in hechos: tareas.append((y, int(c)))
print('tareas', len(tareas), flush=True)
def texto(b):
    t = b.decode('latin-1', 'ignore'); t = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t); return re.sub(r'&[#\w]+;', ' ', t)
def una(yc):
    y, c = yc; V = []
    for yy in (y - 1, y):
        b = get('https://www.sec.gov/Archives/' + idx[yy][c][1], primer_doc=True)
        if not b: return {'y': y, 'cik': c, 'err': 1}
        t = texto(b); V.append((hv.transform([t]), len(t)))
    o = {'y': y, 'cik': c, 'len': [V[0][1], V[1][1]]}
    if min(V[0][1], V[1][1]) > 5000: o['sim'] = float(V[0][0].multiply(V[1][0]).sum())
    return o
with ThreadPoolExecutor(4) as ex, open(SAL, 'a') as f:
    for i, o in enumerate(ex.map(una, tareas)):
        f.write(json.dumps(o) + chr(10)); f.flush()
        if i % 200 == 0: print('bajadas', i, time.strftime('%H:%M'), flush=True)
s = pd.DataFrame([o for o in map(json.loads, open(SAL)) if 'sim' in o]); med = s.groupby('y')['sim'].agg(['median', 'size'])
sp = pd.read_csv(f'{B}/fuentes/sp500_shiller.csv'); sp['f'] = sp['Date'].str[:7]; P = dict(zip(sp.f, sp.SP500))
med['sp4'] = [P[f'{y + 4}-04'] / P[f'{y}-04'] for y in med.index]
print(med.round(5).to_string(), flush=True)
rng = np.random.default_rng(0); o = spearmanr(med['median'], med.sp4)[0]
Pm = np.array([spearmanr(med['median'], rng.permutation(med.sp4.values))[0] for _ in range(10000)])
p = ((Pm <= o).sum() + 1) / 10001
print(f'VI125 mediana similitud vs S&P 4 anios rho {o:+.2f} p {p:.4f}'); print('CRITERIO125', 'pasa' if o < 0 and p < .05 else 'no pasa')
