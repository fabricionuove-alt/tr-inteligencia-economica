"""#142: el modelo de palabras de #139, igual, aplicado a 2010-2012. Reglas en notas/11 (#142)."""
import hashlib, numpy as np, pandas as pd, scipy.sparse as sp
from sklearn.linear_model import Ridge
from sklearn.feature_extraction.text import HashingVectorizer
rng = np.random.default_rng(0); B = '../fuentes'
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
m = np.load('sal-junto3/out/gemma_1_1A_7_modelo.npz'); u = m['usar']; sec = u // 16384
def parcial(y):
    X = sp.load_npz(f'sal-junto3/sae2aT-{y}-L12.npz').tocsr(); ids = np.load(f'sal-junto3/sae2aT-{y}-ids.npy', allow_pickle=True); X.data[~np.isfinite(X.data)] = 0
    Z = np.log1p(X[:, u].toarray() / m['med']); Z = (Z - m['mu']) / m['sd']
    return pd.Series(Z[:, sec == 0] @ m['coef'][sec == 0], index=ids.astype(str))
def palabras(y):
    M = sp.load_npz(f'{B}/edgar-corpus/m1_{y}.npz').tocsr(); ciks = np.load(f'{B}/edgar-corpus/vec_{y}.npz')['ciks']
    return M, np.array([hs(int(c)) for c in ciks])
def juntar(anios):
    Ms, ys, idv, an = [], [], [], []
    for y in anios:
        M, ids = palabras(y); p = parcial(y); ok = np.array([i in p.index for i in ids])
        _, prim = np.unique(ids, return_index=True); uno = np.zeros(len(ids), bool); uno[prim] = True; ok &= uno
        Ms.append(M[ok]); ys.append(p.loc[ids[ok]].values); idv += list(ids[ok]); an += [y] * ok.sum()
    return sp.vstack(Ms).tocsr(), np.concatenate(ys), np.array(idv), np.array(an)
Xa, ya, _, _ = juntar(range(2013, 2017)); print('aprender', Xa.shape, flush=True)
df = np.asarray((Xa > 0).sum(axis=0)).ravel() / Xa.shape[0]; cols = np.where(df >= .02)[0]; print('columnas', len(cols), flush=True)
f = lambda X: (lambda Y: (Y.data.__setitem__(slice(None), np.log1p(1000 * Y.data)), Y)[1])(X[:, cols].tocsr().astype(float).copy())
r = Ridge(alpha=1.0).fit(f(Xa), ya)
F = []
for y in (2010, 2011, 2012):
    M, ids = palabras(y); F.append(pd.DataFrame({'id': ids, 'anio_presentado': y, 'pal': r.predict(f(M))}))
d = pd.concat(F).drop_duplicates(['id', 'anio_presentado'])
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et.anio_presentado.astype(int); et['r4'] = pd.to_numeric(et._ret4, errors='coerce')
x = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'tam', 'r4']], on=['id', 'anio_presentado']).dropna(subset=['sic', 'tam', 'r4'])
x = x[x.sic != '0000'].copy(); x['s3'] = x.sic.str[:3]; x['s2'] = x.sic.str[:2]; x['dec'] = np.minimum((x.tam * 10).astype(int), 9); x['h'] = (x.r4 <= .5).astype(float)
print('con etiqueta', x.groupby('anio_presentado').size().to_dict(), flush=True)
x['g'] = ''
for y, z in x.groupby('anio_presentado'): x.loc[z.index, 'g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2'])
x['top'] = x.groupby(['anio_presentado', 'g'])['pal'].rank(pct=True) > .9
gg = ['anio_presentado', 's3', 'dec']; z = x[x.groupby(gg)['id'].transform('size') >= 5].copy()
z['hp'] = z['h'].where(~z.top).groupby([z[c] for c in gg]).transform('mean'); z = z.dropna(subset=['hp'])
lab = z.top.values; dd = (z.h - z.hp).values; gid = z.groupby(gg).ngroup().values
idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
obs = dd[lab].mean() * 100; P = []
for _ in range(2000):
    l2 = lab.copy()
    for ii in idx: l2[ii] = rng.permutation(l2[ii])
    P.append(dd[l2].mean() * 100)
p = ((np.array(P) <= obs).sum() + 1) / 2001; s = z[lab]
por = {y: (s[s.anio_presentado == y].h.mean() - s[s.anio_presentado == y].hp.mean()) * 100 for y in (2010, 2011, 2012)}
print(f'PA142 top palabras n {lab.sum()} hundidas {s.h.mean()*100:.1f} esperado {s.hp.mean()*100:.1f} dif {obs:+.1f} p {p:.4f} | ' + ' '.join(f'{y}:{v:+.1f} (n {int((s.anio_presentado==y).sum())})' for y, v in por.items()), flush=True)
print('CRITERIO142', 'PASA' if obs <= -3 and p < .05 and sum(v < 0 for v in por.values()) >= 2 else 'no pasa')
