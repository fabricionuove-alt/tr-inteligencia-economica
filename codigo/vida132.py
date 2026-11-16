"""#132: qué etapa de vida ve Tr (A) y si el ciclo sale de ahí (B, C). Reglas en notas/11 (#132)."""
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

import json, hashlib
from scipy.stats import spearmanr
rng = np.random.default_rng(0)
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
C = {'O': 'NetCashProvidedByUsedInOperatingActivities', 'I': 'NetCashProvidedByUsedInInvestingActivities', 'F': 'NetCashProvidedByUsedInFinancingActivities'}
def etapa(O, I, F):
    O, I, F = O > 0, I > 0, F > 0
    if not O and not I and F: return 'nacimiento'
    if O and not I and F: return 'crecimiento'
    if O and not I and not F: return 'madurez'
    if not O and I: return 'declive'
    return 'sacudon'
E = []
for y in range(2009, 2022):
    v = {}
    for k, c in C.items():
        for o in json.load(open(f'../fuentes/frames/{c}_CY{y}.json'))['data']: v.setdefault(o['cik'], {})[k] = o['val']
    E += [{'id': hs(cik), 'anio_presentado': y + 1, 'etapa': etapa(z['O'], z['I'], z['F'])} for cik, z in v.items() if len(z) == 3]
E = pd.DataFrame(E).drop_duplicates(['id', 'anio_presentado'])
# A
a = d.merge(E, on=['id', 'anio_presentado'])
print('A: con puntaje y etapa', len(a), flush=True)
filas = []
for y, z in a.groupby('anio_presentado'):
    z = z.copy(); z['g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2']); z['top'] = z.groupby('g')['gemma'].rank(pct=True) > .9
    t, r = z[z.top], z[~z.top]
    f = {'camada': y, 'n_top': len(t)}
    for e in ['madurez', 'crecimiento', 'sacudon', 'nacimiento', 'declive']: f[e] = f'{(t.etapa == e).mean()*100:.0f}/{(r.etapa == e).mean()*100:.0f}'
    f['mad_ok'] = (t.etapa == 'madurez').mean() > (r.etapa == 'madurez').mean()
    f['jov_ok'] = t.etapa.isin(['nacimiento', 'declive']).mean() < r.etapa.isin(['nacimiento', 'declive']).mean()
    filas.append(f)
A = pd.DataFrame(filas); print('A (% arriba / % resto)'); print(A.to_string(index=False), flush=True)
pa = A.mad_ok.all() and A.jov_ok.all()
# B y C
et['r4'] = pd.to_numeric(et['_ret4'], errors='coerce')
e2 = et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'tam', 'r4']].dropna()
x = E.merge(e2, on=['id', 'anio_presentado']); x['sic3'] = x['sic'].str[:3]; x['dec'] = np.minimum((x['tam'] * 10).astype(int), 9); g = ['anio_presentado', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy(); x['lr'] = np.log(np.maximum(x['r4'], .01)); x['ex'] = x['lr'] - x.groupby(g)['lr'].transform('median')
mer4 = et.groupby('anio_presentado')['r4'].median()
sp = pd.read_csv('../fuentes/sp500_shiller.csv'); sp['f'] = sp['Date'].str[:4].astype(int) * 100 + sp['Date'].str[5:7].astype(int); sp = sp.set_index('f')['SP500']
def caida(y):
    k = list(sp.index).index(y * 100 + 3); return sp.iloc[k] / sp.iloc[k - 60:k + 1].max() - 1
co = []
for y, z in x.groupby('anio_presentado'):
    co.append({'ap': y, 'n_mad': (z.etapa == 'madurez').sum(), 'n_jov': z.etapa.isin(['nacimiento', 'declive']).sum(),
               'dif': (z.loc[z.etapa == 'madurez', 'ex'].mean() - z.loc[z.etapa.isin(['nacimiento', 'declive']), 'ex'].mean()) * 100,
               'mercado4': mer4[y], 'caida': caida(y)})
co = pd.DataFrame(co); print(co.round(3).to_string(index=False), flush=True)
def perm(u, v, lado):
    o = spearmanr(u, v)[0]; P = np.array([spearmanr(u, rng.permutation(v))[0] for _ in range(10000)])
    return o, (((P <= o) if lado < 0 else (P >= o)).sum() + 1) / 10001
rb, pb = perm(co.dif.values, co.mercado4.values, -1); rc, pc = perm(co.dif.values, co.caida.values, 1)
print(f'VI132 A maduras arriba en todas: {A.mad_ok.all()} | jovenes abajo en todas: {A.jov_ok.all()}')
print(f'VI132 B maduras-jovenes vs mercado 4 anios rho {rb:+.2f} p {pb:.4f}')
print(f'VI132 C maduras-jovenes vs caida al comprar rho {rc:+.2f} p {pc:.4f}')
print('CRITERIO132 A', 'pasa' if pa else 'no pasa', '| B', 'pasa' if rb < 0 and pb < .05 else 'no pasa', '| C', 'pasa' if rc > 0 and pc < .05 else 'no pasa')
