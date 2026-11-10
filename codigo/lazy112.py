"""#112 Lazy Prices: similitud del 10-K con el del año anterior (secciones 1, 1A, 7). Reglas en notas/11 (#112).
python lazy112.py bajar   -> vectores por año en fuentes/edgar-corpus/vec_AAAA.npz (sin guardar el texto)
python lazy112.py medir"""
import os, sys, json, re, time, hashlib, urllib.request, numpy as np, pandas as pd, scipy.sparse as sp
from sklearn.feature_extraction.text import HashingVectorizer
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; D = f'{B}/fuentes/edgar-corpus'; os.makedirs(D, exist_ok=True)
SEC = ['section_1', 'section_1A', 'section_7']
hv = HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm='l2', alternate_sign=False)
if sys.argv[1] == 'bajar':
    for y in range(2009, 2021):
        out = f'{D}/vec_{y}.npz'
        if os.path.exists(out): continue
        ciks, M, largo = [], {s: [] for s in SEC}, {s: [] for s in SEC}
        for parte in ('train', 'validate', 'test'):
            u = f'https://huggingface.co/datasets/eloukas/edgar-corpus/resolve/main/{y}/{parte}.jsonl'
            for k in range(5):
                c0, tanda, cs = len(ciks), {s: [] for s in SEC}, []
                try:
                    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'inteligencia-economica research'}), timeout=120)
                    loc = {s: [] for s in SEC}; lloc = {s: [] for s in SEC}
                    for l in r:
                        d = json.loads(l); cs.append(d['cik'])
                        for s in SEC: t = d.get(s) or ''; tanda[s].append(t); lloc[s].append(len(t))
                        if len(cs) % 500 == 0:
                            for s in SEC: loc[s].append(hv.transform(tanda[s])); tanda[s] = []
                    for s in SEC:
                        if tanda[s]: loc[s].append(hv.transform(tanda[s]))
                    ciks += cs
                    for s in SEC: M[s] += loc[s]; largo[s] += lloc[s]
                    break
                except Exception as e:
                    print('reintento', y, parte, e, flush=True); time.sleep(20)
            else: raise SystemExit(f'falló {y} {parte}')
        M = {s: sp.vstack(v).tocsr() for s, v in M.items()}; largo = {s: np.array(v) for s, v in largo.items()}
        sp.save_npz(f'{D}/m1_{y}.npz', M['section_1']); sp.save_npz(f'{D}/m1a_{y}.npz', M['section_1A']); sp.save_npz(f'{D}/m7_{y}.npz', M['section_7'])
        np.savez(out, ciks=np.array(ciks), l1=largo['section_1'], l1a=largo['section_1A'], l7=largo['section_7'])
        print(y, 'informes', len(ciks), flush=True)
    sys.exit()
# medir
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
filas = []
prev = None
for y in range(2009, 2021):
    z = np.load(f'{D}/vec_{y}.npz'); M = [sp.load_npz(f'{D}/{p}_{y}.npz').tocsr() for p in ('m1', 'm1a', 'm7')]; L = [z['l1'], z['l1a'], z['l7']]
    ciks = z['ciks']; idx = {}
    for i, c in enumerate(ciks): idx.setdefault(c, i)   # primer 10-K del año por empresa
    cur = (idx, M, L)
    if prev:
        pidx, PM, PL = prev
        for c, i in idx.items():
            j = pidx.get(c)
            if j is None: continue
            sims = []
            for s in range(3):
                if L[s][i] > 500 and PL[s][j] > 500: sims.append(float(M[s][i].multiply(PM[s][j]).sum()))
            s1a = float(M[1][i].multiply(PM[1][j]).sum()) if L[1][i] > 500 and PL[1][j] > 500 else np.nan
            if sims: filas.append({'id': hs(c), 'ap': y, 'sim': np.mean(sims), 'sim1a': s1a})
    prev = cur
s = pd.DataFrame(filas); print('pares año contra año', len(s), flush=True)
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int)
x = et.drop_duplicates(['id', 'ap']).merge(s, on=['id', 'ap'])
for c in ('_ret1', '_ret4'): x[c] = pd.to_numeric(x[c], errors='coerce')
x = x.dropna(subset=['_ret1', 'sic']).copy(); x['sic2'] = x['sic'].str[:2]
print('con rendimiento', len(x), x.groupby('ap').size().to_dict(), flush=True)
rng = np.random.default_rng(0)
def tramo(z, col, nomb, simc='sim'):
    z = z.dropna(subset=[simc]).copy()
    z['q'] = z.groupby('ap')[simc].transform(lambda v: pd.qcut(v.rank(method='first'), 5, labels=False))
    z = z[z['q'].isin([0, 4])].dropna(subset=[col]).copy(); z['quieta'] = z['q'] == 4
    r = z[col].values * 100; lab = z['quieta'].values; obs = r[lab].mean() - r[~lab].mean()
    gid = z.groupby(['ap', 'sic2']).ngroup().values; grupos = [np.where(gid == k)[0] for k in np.unique(gid)]
    perm = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in grupos: l2[ii] = rng.permutation(l2[ii])
        perm.append(r[l2].mean() - r[~l2].mean())
    p = (np.sum(np.array(perm) >= obs) + 1) / 2001
    hq = (z.loc[z.quieta, '_ret4'] <= .5).mean(); hc = (z.loc[~z.quieta, '_ret4'] <= .5).mean()
    print(f'LZ112 {nomb:26s} {col} {simc:5s} n {lab.sum():5d}/{(~lab).sum():5d} quietas {r[lab].mean():+.1f} cambiadas {r[~lab].mean():+.1f} dif {obs:+.1f} p {p:.4f} | medianas {np.median(r[lab]):+.1f}/{np.median(r[~lab]):+.1f} | hundidas4 {hq:.3f}/{hc:.3f}', flush=True)
    return obs, p
T = {'exploración 2010-2016': x[(x.ap >= 2010) & (x.ap <= 2016)], 'confirmación 2017-2020': x[(x.ap >= 2017) & (x.ap <= 2020)]}
res = {k: tramo(v, '_ret1', k) for k, v in T.items()}
for k, v in T.items(): tramo(v, '_ret4', k); tramo(v, '_ret1', k, 'sim1a')
for y in range(2010, 2021): tramo(x[x.ap == y], '_ret1', f'año {y}')
e = res['exploración 2010-2016'][0]; c, pc = res['confirmación 2017-2020']
print(f'CRITERIO112 confirmación {c:+.1f} pts (p {pc:.4f}) exploración {e:+.1f} -> {"pasa (falta 2021-2022)" if c >= 3 and pc < .05 and e > 0 else "no pasa"}', flush=True)
x[['id', 'ap', 'sim', 'sim1a', '_ret1', '_ret4']].to_csv(f'{B}/entrenar/sal-cab102/lazy112_filas.csv', index=False)
