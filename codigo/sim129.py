"""#129: baja de la SEC los 10-K 2025-2026 y mide la similitud del texto entero con el año anterior. Reglas en notas/11 (#129).
python sim114.py bajar | medir"""
import os, sys, json, re, time, hashlib, threading, urllib.request, numpy as np, pandas as pd
from concurrent.futures import ThreadPoolExecutor
from sklearn.feature_extraction.text import HashingVectorizer
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; SAL = f'{B}/entrenar/sal-cab102/sim129.jsonl'
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
hv = HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm='l2', alternate_sign=False)
lock = threading.Lock(); ult = [0.0]
def get(u):
    for k in range(5):
        with lock:
            w = 0.12 - (time.time() - ult[0])
            if w > 0: time.sleep(w)
            ult[0] = time.time()
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read()
        except Exception as e:
            if '404' in str(e): return None
            time.sleep(5 * (k + 1))
    return None
def texto(b):
    t = b.decode('utf-8', 'ignore'); t = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', t)
    t = re.sub(r'(?s)<ix:header>.*?</ix:header>', ' ', t); t = re.sub(r'<[^>]+>', ' ', t); t = re.sub(r'&[#\w]+;', ' ', t)
    return t
if sys.argv[1] == 'bajar':
    ciks = sorted({json.loads(l)['cik'] for l in open(f'{B}/entrenar/sal-cab102/sim122.jsonl') if 's2025' in json.loads(l)})
    hechos = {json.loads(l)['cik'] for l in open(SAL)} if os.path.exists(SAL) else set()
    ciks = [c for c in ciks if c not in hechos]; print('empresas por bajar', len(ciks), flush=True)
    def una(cik):
        j = get(f'https://data.sec.gov/submissions/CIK{cik:010d}.json')
        if not j: return {'cik': cik, 'err': 'sub'}
        r = json.loads(j)['filings']['recent']; docs = {}
        for f, d, a, p in zip(r['form'], r['filingDate'], r['accessionNumber'], r['primaryDocument']):
            y = int(d[:4])
            if f == '10-K' and y in (2025, 2026) and p: docs[y] = (a, p)   # recent viene del más nuevo al más viejo: queda el primero del año
        V = {}
        for y, (a, p) in docs.items():
            b = get(f'https://www.sec.gov/Archives/edgar/data/{cik}/{a.replace("-", "")}/{p}')
            if b: t = texto(b); V[y] = (hv.transform([t]), len(t))
        o = {'cik': cik, 'id': hs(cik), 'anios': sorted(V)}
        for y in (2026,):
            if y in V and y - 1 in V and V[y][1] > 5000 and V[y - 1][1] > 5000: o[f's{y}'] = float(V[y][0].multiply(V[y - 1][0]).sum())
        return o
    with ThreadPoolExecutor(4) as ex, open(SAL, 'a') as f:
        for i, o in enumerate(ex.map(una, ciks)):
            f.write(json.dumps(o) + chr(10)); f.flush()
            if i % 100 == 0: print('bajadas', i, time.strftime('%H:%M'), flush=True)
    print('LISTO', flush=True); sys.exit()
