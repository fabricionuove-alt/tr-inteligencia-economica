"""#145 diagnóstico: por qué edgar-crawler no reproduce EDGAR-CORPUS 2020 (coseno de vectores de palabras por empresa)."""
import json, numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
B = 'E:/FABRI INFLUENCIA/inteligencia-economica/fuentes'
hv = HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm='l2', alternate_sign=False)
M = np.load(f'{B}/edgar-corpus/m1_2020.npz', allow_pickle=True); import scipy.sparse as sp
X = sp.csr_matrix((M['data'], M['indices'], M['indptr']), shape=M['shape']) if 'data' in M else None
ck = np.load(f'{B}/edgar-corpus/vec_2020.npz', allow_pickle=True); print(list(M.keys()), list(ck.keys()))
cik = [int(c) for c in ck['ciks']]; fila = {c: i for i, c in enumerate(cik)}; l1 = ck['l1']
R = []
for l in open(f'{B}/crawler145/sec1.jsonl', encoding='utf-8'):
    o = json.loads(l); t = o.get('2020') or ''
    if len(t.split()) < 300 or o['cik'] not in fila: continue
    i = fila[o['cik']]; c = float(X[i].multiply(hv.transform([t])).sum())
    R.append((o['cik'], c, len(t.split()), int(l1[i]) if np.ndim(l1) else -1))
c = np.array([r[1] for r in R]); print('n', len(c), 'coseno: cuantiles', np.round(np.quantile(c, [.05, .1, .25, .5, .75, .9]), 3))
print('>.95', (c > .95).mean().round(3), '<.5', (c < .5).mean().round(3))
for r in sorted(R, key=lambda r: r[1])[:8]: print(r)
exec(open('palabras139.py', encoding='utf-8').read().split('Xp, yp, idp, anp = juntar')[0].replace("B = ", "B_ = "), globals())
from scipy.stats import spearmanr
cos = {r[0]: r[1] for r in R}; T = {}
for l in open(f'{B}/crawler145/sec1.jsonl', encoding='utf-8'):
    o = json.loads(l); t = o.get('2020') or ''
    if o['cik'] in cos and cos[o['cik']] > 0: T[o['cik']] = float(r.predict(f(hv.transform([t])))[0])
Mm = sp.load_npz(f'{B}/edgar-corpus/m1_2020.npz').tocsr()
E = {c: float(r.predict(f(Mm[fila[c]]))[0]) for c in T}
for lo, hi in ((0, .9), (.9, .98), (.98, .999), (.999, 1.01)):
    k = [c for c in T if lo <= cos[c] < hi]
    if len(k) > 5: print(f'coseno {lo}-{hi}: n {len(k)} Spearman {spearmanr([E[c] for c in k], [T[c] for c in k])[0]:+.3f} dif media {np.mean([T[c]-E[c] for c in k]):+.3f} sd {np.std([T[c]-E[c] for c in k]):.3f}')
print('sd de puntajes EDGAR', np.std(list(E.values())))
