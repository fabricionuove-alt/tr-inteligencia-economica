"""#141: Gemma + palabras (#139) juntas contra Gemma sola. Reglas en notas/11 (#141)."""
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
Xp, yp, idp, anp = juntar(range(2017, 2021)); sp_ = r.predict(f(Xp))
print('correlacion palabras vs parcial Gemma 2017-2020', round(np.corrcoef(sp_, yp)[0, 1], 3), flush=True)
d = pd.DataFrame({'id': idp, 'anio_presentado': anp, 'pal': sp_})
ref = pd.read_csv('sal-junto3/out/gemma_1_1A_7_puntaje.csv', dtype={'id': str})
d = d.merge(ref[['id', 'anio_presentado', 'gemma']], on=['id', 'anio_presentado'])
d['comb'] = (d.groupby('anio_presentado')['pal'].rank(pct=True) + d.groupby('anio_presentado')['gemma'].rank(pct=True)) / 2
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et.anio_presentado.astype(int); et['r4'] = pd.to_numeric(et._ret4, errors='coerce')
x = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'tam', 'r4']], on=['id', 'anio_presentado']).dropna(subset=['sic', 'tam', 'r4'])
x = x[x.sic != '0000'].copy(); x['s3'] = x.sic.str[:3]; x['s2'] = x.sic.str[:2]; x['dec'] = np.minimum((x.tam * 10).astype(int), 9); x['h'] = (x.r4 <= .5).astype(float)
x['g'] = ''
for y, z in x.groupby('anio_presentado'): x.loc[z.index, 'g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2'])
gg = ['anio_presentado', 's3', 'dec']; x = x[x.groupby(gg)['id'].transform('size') >= 5].copy()
res = {}
for n in ['gemma', 'pal', 'comb']:
    z = x.copy(); z['sen'] = z.groupby(['anio_presentado', 'g'])[n].rank(pct=True) > .9
    z['hp'] = z['h'].where(~z.sen).groupby([z[c] for c in gg]).transform('mean'); z = z.dropna(subset=['hp']); s = z[z.sen]
    tot = (s.h - s.hp).mean() * 100; por = {y: (s[s.anio_presentado == y].h.mean() - s[s.anio_presentado == y].hp.mean()) * 100 for y in range(2017, 2021)}
    res[n] = (tot, por, {y: s[s.anio_presentado == y].h.mean() * 100 for y in range(2017, 2021)})
    print(f'CO141 {n:6s} n {len(s)} hundidas {s.h.mean()*100:.1f} esperado {s.hp.mean()*100:.1f} dif {tot:+.1f} | ' + ' '.join(f'{y}:{v:+.1f}' for y, v in por.items()), flush=True)
mejor = sum(res['comb'][2][y] < res['gemma'][2][y] for y in range(2017, 2021))
print(f'combinada se hunde menos que Gemma sola en {mejor} de 4 años; total {res["comb"][0]:+.1f} contra {res["gemma"][0]:+.1f}')
print('CRITERIO141', 'PASA: candidata para Rt' if mejor >= 3 and res['comb'][0] <= res['gemma'][0] - 1 else 'no pasa')
