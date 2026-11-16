"""#135: ¿Tr es sólo calidad? Reglas en notas/11 (#135)."""
import numpy as np, pandas as pd
from scipy import sparse
m = np.load('sal-junto3/out/gemma_1_1A_7_modelo.npz')
def carga(npz, ids): return sparse.load_npz(npz).tocsr(), np.load(ids)
fil = [pd.read_csv('sal-junto3/out/gemma_1_1A_7_puntaje.csv', dtype={'id': str})]
for y in (2021, 2022):
    P = [carga(f'sal-anon2124/sae2a-textos-{y}-L12.npz', f'sal-anon2124/sae2a-textos-{y}-ids.npy'),
         carga(f'sal-lee{y}/sae2a-textos1A-{y}-L12.npz', f'sal-lee{y}/sae2a-textos1A-{y}-ids.npy'),
         carga(f'sal-lee{y}/sae2a-textos7-{y}-L12.npz', f'sal-lee{y}/sae2a-textos7-{y}-ids.npy')]
    com = sorted(set.intersection(*[set(i) for _, i in P])); pos = [{v: k for k, v in enumerate(i)} for _, i in P]
    X = sparse.hstack([x[[p[c] for c in com]] for (x, _), p in zip(P, pos)]).tocsr(); X.data[~np.isfinite(X.data)] = 0
    Z = np.log1p(X[:, m['usar']].toarray() / m['med']); Z = (Z - m['mu']) / m['sd']
    fil.append(pd.DataFrame({'id': com, 'anio_presentado': y, 'gemma': Z @ m['coef'] + m['b']}))
d = pd.concat(fil); d = d[d.anio_presentado >= 2017]
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['anio_presentado'] = et['anio_presentado'].astype(int); et['r1'] = pd.to_numeric(et['_ret1'], errors='coerce')
d = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'r1']], on=['id', 'anio_presentado']).dropna(subset=['r1', 'sic'])
d = d[d['sic'] != '0000']; d['s3'] = d.sic.str[:3]; d['s2'] = d.sic.str[:2]

import os, json, time, hashlib, urllib.request
from scipy.stats import spearmanr
rng = np.random.default_rng(0); D = '../fuentes/frames'
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
def frame(c, per):
    f = f'{D}/{c}_{per}.json'
    if not os.path.exists(f):
        open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(f'https://data.sec.gov/api/xbrl/frames/us-gaap/{c}/USD/{per}.json', headers=UA), timeout=120).read()); time.sleep(.2)
    return {o['cik']: o['val'] for o in json.load(open(f))['data']}
C = {'O': 'NetCashProvidedByUsedInOperatingActivities', 'I': 'NetCashProvidedByUsedInInvestingActivities', 'F': 'NetCashProvidedByUsedInFinancingActivities'}
R = []
for y in range(2016, 2022):
    ni, at = frame('NetIncomeLoss', f'CY{y}'), frame('Assets', f'CY{y}Q4I'); fl = {k: frame(c, f'CY{y}') for k, c in C.items()}
    for cik in set(ni) & set(at):
        if at[cik] <= 0: continue
        e = 'otra'
        if all(cik in fl[k] for k in 'OIF'):
            O, I, F = fl['O'][cik] > 0, fl['I'][cik] > 0, fl['F'][cik] > 0
            e = 'madura' if (O and not I and not F) else ('joven' if ((not O and not I and F) or (not O and I)) else 'otra')
        R.append({'id': hs(cik), 'anio_presentado': y + 1, 'roa': ni[cik] / at[cik], 'etapa': e})
Q = pd.DataFrame(R).drop_duplicates(['id', 'anio_presentado'])
et['r4'] = pd.to_numeric(et['_ret4'], errors='coerce')
x = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'tam', 'r4']], on=['id', 'anio_presentado']).merge(Q, on=['id', 'anio_presentado'])
x = x.dropna(subset=['tam']).copy(); print('con puntaje y rentabilidad', len(x), flush=True)
A = []
for y, z in x.groupby('anio_presentado'):
    z = x.loc[z.index]; x.loc[z.index, 'g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2'])
    A.append((y, spearmanr(z.gemma, z.roa)[0]))
x['top'] = x.groupby(['anio_presentado', 'g'])['gemma'].rank(pct=True) > .9
for y, r in A: print(f'  A {y} rho gemma-rentabilidad {r:+.2f}', flush=True)
pa = all(r > 0 for _, r in A)
x = x.dropna(subset=['r4']).copy(); x['h'] = (x.r4 <= .5).astype(float)
x['qroa'] = x.groupby('anio_presentado')['roa'].transform(lambda v: pd.qcut(v.rank(method='first'), 5, labels=False))
x['ttam'] = np.minimum((x.tam * 3).astype(int), 2); gg = ['anio_presentado', 's2', 'ttam', 'qroa', 'etapa']
x = x[x.groupby(gg)['id'].transform('size') >= 5].copy()
x['hp'] = x['h'].where(~x.top).groupby([x[c] for c in gg]).transform('mean'); x = x.dropna(subset=['hp'])
lab = x.top.values; dd = (x.h - x.hp).values; gid = x.groupby(gg).ngroup().values
idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
obs = dd[lab].mean() * 100; P = []
for _ in range(2000):
    l2 = lab.copy()
    for ii in idx: l2[ii] = rng.permutation(l2[ii])
    P.append(dd[l2].mean() * 100)
p = ((np.array(P) <= obs).sum() + 1) / 2001
t = x[x.top]
print(f'B top Gemma n {lab.sum()} hundidas {t.h.mean()*100:.1f} esperado (misma rentabilidad, etapa, rubro, tamaño) {t.hp.mean()*100:.1f} dif {obs:+.1f} p {p:.4f}')
for y in sorted(x.anio_presentado.unique()):
    z = x[(x.anio_presentado == y) & x.top]; print(f'  B {y} n {len(z)} hundidas {z.h.mean()*100:.1f} esperado {z.hp.mean()*100:.1f}')
print('CRITERIO135 A', 'pasa' if pa else 'no pasa', '| B', 'PASA: ve algo mas que calidad' if obs <= -2 and p < .05 else 'no pasa')
