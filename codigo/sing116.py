"""#116: sección 1 de los 10-K 2021-2022 (SEC) y su singularidad contra el rubro. Reglas en notas/11 (#116).
python sing116.py bajar | medir"""
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
if sys.argv[1] == 'bajar':
    ciks = [json.loads(l)['cik'] for l in open(f'{B}/entrenar/sal-cab102/sim114.jsonl')]
    SAL = f'{O}/sec1.jsonl'; hechos = {json.loads(l)['cik'] for l in open(SAL)} if os.path.exists(SAL) else set()
    ciks = [c for c in ciks if c not in hechos]; print('empresas', len(ciks), flush=True)
    def una(cik):
        j = get(f'https://data.sec.gov/submissions/CIK{cik:010d}.json')
        if not j: return {'cik': cik}
        r = json.loads(j)['filings']['recent']; docs = {}
        for f, d, a, p in zip(r['form'], r['filingDate'], r['accessionNumber'], r['primaryDocument']):
            y = int(d[:4])
            if f == '10-K' and y in (2021, 2022) and p: docs[y] = (a, p)
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
# medir
rng = np.random.default_rng(0)
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int); et = et.drop_duplicates(['id', 'ap'])
sic = {(i, a): s for i, a, s in zip(et['id'], et['ap'], et['sic']) if isinstance(s, str)}
R = [json.loads(l) for l in open(f'{O}/sec1.jsonl', encoding='utf-8')]; filas = []
for y in (2021, 2022):
    xs = [(r['cik'], r[str(y)], sic.get((hs(r['cik']), y))) for r in R if r.get(str(y))]
    xs = [(c, t, s[:2]) for c, t, s in xs if s]; print(y, 'con sección 1', len(xs), flush=True)
    df = pd.DataFrame(xs, columns=['cik', 't', 's2'])
    for s2, g in df.groupby('s2'):
        if len(g) < 10: continue
        V = hv.transform(g['t'].tolist()); S = np.asarray(V.sum(axis=0)).ravel(); SS = S @ S; vS = V @ S
        cos = (vS - 1) / np.sqrt(np.maximum(SS - 2 * vS + 1, 1e-12))
        for c, sg in zip(g['cik'], 1 - cos): filas.append({'id': hs(c), 'ap': y, 'sing': sg})
s = pd.DataFrame(filas)
x = s.merge(et[['id', 'ap', 'sic', 'tam', '_ret4']], on=['id', 'ap']); x['r'] = pd.to_numeric(x['_ret4'], errors='coerce'); x = x.dropna(subset=['r', 'sic', 'tam']).copy()
x['q'] = x.groupby('ap')['sing'].transform(lambda v: pd.qcut(v.rank(method='first'), 5, labels=False))
x['sic3'] = x['sic'].str[:3]; x['dec'] = np.minimum((x['tam'] * 10).astype(int), 9); g = ['ap', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy(); x['h'] = (x['r'] <= .5).astype(float)
print('con rendimiento y pares', len(x), flush=True)
def tramo(z, lado, nomb):
    z = z.copy(); z['sen'] = z['q'] == lado
    z['hp'] = z['h'].where(~z['sen']).groupby([z[c] for c in g]).transform('mean')
    z['med'] = z['r'].where(~z['sen']).groupby([z[c] for c in g]).transform('median')
    z = z.dropna(subset=['hp']); z['d'] = z['h'] - z['hp']; z['ex'] = (z['r'] - z['med']) * 100
    lab = z['sen'].values; d = z['d'].values; gid = z.groupby(g).ngroup().values
    idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
    obs = d[lab].mean() * 100; perm = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        perm.append(d[l2].mean() * 100)
    perm = np.array(perm); p = ((perm <= obs).sum() + 1) / 2001 if lado == 4 else ((perm >= obs).sum() + 1) / 2001
    f = z[lab]
    print(f'SG116 {nomb:12s} {"singulares" if lado == 4 else "genéricas "} n {lab.sum():5d} hundidas {f.h.mean()*100:5.1f} esperado {f.hp.mean()*100:5.1f} dif {obs:+.1f} p {p:.4f} | exceso medio {f.ex.mean():+.1f} mediano {f.ex.median():+.1f}', flush=True)
    return obs, p, lab.sum()
c, pc, n = tramo(x, 4, '2021-2022'); tramo(x, 0, '2021-2022')
for y in (2021, 2022): tramo(x[x.ap == y], 4, f'año {y}')
v = 'muestra insuficiente' if n < 300 else ('PASA' if c < 0 and pc < .05 else 'no pasa')
print(f'CRITERIO116 {c:+.1f} pts (p {pc:.4f}, n {n}) -> {v}', flush=True)
