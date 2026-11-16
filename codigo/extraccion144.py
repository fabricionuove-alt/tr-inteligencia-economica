"""#144: puntaje de palabras de #139 con dos extracciones del mismo 10-K 2020. Reglas en notas/11 (#144)."""
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
import json
from scipy.stats import spearmanr
hvl = HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm='l2', alternate_sign=False)
M, ids = palabras(2020); a = pd.DataFrame({'id': ids, 'edgar': r.predict(f(M))}).drop_duplicates('id')
nuevos = []
for l in open(f'{B}/sec116/sec1_2020.jsonl', encoding='utf-8'):
    o = json.loads(l); t = o.get('2020') or ''
    if len(t.split()) >= 300: nuevos.append({'id': hs(o['cik']), 'sec116': float(r.predict(f(hvl.transform([t])))[0]), 'palabras_nuevo': len(t.split())})
b = pd.DataFrame(nuevos); x = a.merge(b, on='id')
rho = spearmanr(x.edgar, x.sec116)[0]
print(f'EX144 empresas con las dos extracciones {len(x)} | Spearman {rho:+.3f} | Pearson {np.corrcoef(x.edgar, x.sec116)[0,1]:+.3f}')
print('CRITERIO144', 'la extraccion no explica 2021-2022' if rho >= .8 else ('la extraccion puede explicarlo' if rho < .5 else 'no decide'))
