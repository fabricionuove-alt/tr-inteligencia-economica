"""#144: sección 1 de los 10-K 2020 con la extracción de sing116, para comparar con EDGAR-CORPUS. Reglas en notas/11 (#144)."""
import os, sys, json, re, time, hashlib, threading, urllib.request, numpy as np, pandas as pd, scipy.sparse as sp
from concurrent.futures import ThreadPoolExecutor
from sklearn.feature_extraction.text import HashingVectorizer
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; O = f'{B}/fuentes/sec116'; os.makedirs(O, exist_ok=True)
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
    return re.sub(r'\s+', ' ', t)
INI = re.compile(r'item\s*1\s*[\.:\-]?\s*business', re.I); FIN = re.compile(r'item\s*(?:1a\s*[\.:\-]?\s*risk|2\s*[\.:\-]?\s*propert)', re.I)
def seccion1(t):
    fins = [m.start() for m in FIN.finditer(t)]; mejor = ''
    for m in INI.finditer(t):
        f = next((x for x in fins if x > m.end()), None)
        if f and f - m.end() > len(mejor): mejor = t[m.end():f]
    return mejor
if True:
    ciks = sorted(set(json.loads(l)['cik'] for l in open(f'{B}/entrenar/sal-cab102/sim114.jsonl')) & {int(c) for c in np.load(f'{B}/fuentes/edgar-corpus/vec_2020.npz')['ciks']})
    SAL = f'{O}/sec1_2020.jsonl'; hechos = {json.loads(l)['cik'] for l in open(SAL)} if os.path.exists(SAL) else set()
    ciks = [c for c in ciks if c not in hechos]; print('empresas', len(ciks), flush=True)
    def una(cik):
        j = get(f'https://data.sec.gov/submissions/CIK{cik:010d}.json')
        if not j: return {'cik': cik}
        r = json.loads(j)['filings']['recent']; docs = {}
        for f, d, a, p in zip(r['form'], r['filingDate'], r['accessionNumber'], r['primaryDocument']):
            y = int(d[:4])
            if f == '10-K' and y == 2020 and p: docs[y] = (a, p)
        o = {'cik': cik}
        for y, (a, p) in docs.items():
            b = get(f'https://www.sec.gov/Archives/edgar/data/{cik}/{a.replace("-", "")}/{p}')
            if b: s = seccion1(texto(b)); o[str(y)] = s if len(s) > 500 else ''
        return o
    with ThreadPoolExecutor(4) as ex, open(SAL, 'a', encoding='utf-8') as f:
        for i, o in enumerate(ex.map(una, ciks)):
            f.write(json.dumps(o) + chr(10)); f.flush()
            if i % 200 == 0: print('bajadas', i, time.strftime('%H:%M'), flush=True)
    print('LISTO', flush=True); sys.exit()
