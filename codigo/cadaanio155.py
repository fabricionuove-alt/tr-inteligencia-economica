"""#155: Gemma reaprendido cada año con las camadas que ya cumplieron 4 años (2013..y-5), probado en y. Reglas en notas/11 (#155)."""
src = open('gemma154.py', encoding='utf-8').read(); exec(src[:src.index('# 1) Gemma nuevo')])
from scipy import sparse
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et['anio_presentado'].astype(int); et = et.drop_duplicates(['id', 'anio_presentado'])
def rasgos(y):
    if y <= 2020:
        X = sparse.load_npz(f'sal-junto3/sae2aT-{y}-L12.npz').tocsr(); ids = np.load(f'sal-junto3/sae2aT-{y}-ids.npy', allow_pickle=True).astype(str)
    else:
        P = [(sparse.load_npz(a).tocsr(), np.load(b, allow_pickle=True)) for a, b in ((f'sal-anon2124/sae2a-textos-{y}-L12.npz', f'sal-anon2124/sae2a-textos-{y}-ids.npy'),
             (f'sal-lee{y}/sae2a-textos1A-{y}-L12.npz', f'sal-lee{y}/sae2a-textos1A-{y}-ids.npy'), (f'sal-lee{y}/sae2a-textos7-{y}-L12.npz', f'sal-lee{y}/sae2a-textos7-{y}-ids.npy'))]
        com = sorted(set.intersection(*[set(i) for _, i in P])); pos = [{v: k for k, v in enumerate(i)} for _, i in P]
        X = sparse.hstack([x[[p[c] for c in com]] for (x, _), p in zip(P, pos)]).tocsr(); ids = np.array([str(c) for c in com])
    return X, ids
def aprender(ult):
    bl, F = [], []
    for a in range(2013, ult + 1):
        X, ids = rasgos(a); bl.append(X); F.append(pd.DataFrame({'id': ids, 'anio_presentado': a}))
    X = sparse.vstack(bl).tocsr(); F = pd.concat(F, ignore_index=True)
    malo = np.zeros(X.shape[0], bool); r_, _ = X.nonzero(); malo[np.unique(r_[~np.isfinite(X.data)])] = True; X.data[~np.isfinite(X.data)] = 0; X.eliminate_zeros()
    d = F.reset_index().merge(et, on=['id', 'anio_presentado'], how='left'); d['r4'] = pd.to_numeric(d['_ret4'], errors='coerce'); d['sic3'] = d['sic'].str[:3]
    d['ter'] = pd.cut(d['tam'], [0, 1/3, 2/3, 1], include_lowest=True, labels=False); g = ['anio_presentado', 'sic3', 'ter']
    ok = (d['r4'].notna() & d['sic'].notna() & d['tam'].notna()).values & ~malo[d['index'].values]; ok &= (d.groupby(g)['id'].transform('size') >= 5).values
    d['lr'] = np.log(d['r4'].clip(lower=0.01)); d['ex'] = np.nan; d.loc[ok, 'ex'] = d.loc[ok, 'lr'] - d[ok].groupby(g)['lr'].transform('median')
    nz = np.asarray((X[np.where(ok)[0]] > 0).mean(0)).ravel(); usar = np.where(nz >= 0.02)[0]
    Z = X[np.where(ok)[0]][:, usar].toarray(); med = np.median(Z[Z > 0]); Z = np.log1p(Z / med); mu, sd = Z.mean(0), Z.std(0) + 1e-6; Z = (Z - mu) / sd
    mod = Ridge(alpha=1000).fit(Z, d['ex'].clip(-3, 3).values[ok]); print(f'  aprendido 2013-{ult}: {ok.sum()} empresas-año, {len(usar)} columnas', flush=True)
    return usar, med, mu, sd, mod
D = []
for y in range(2018, 2023):
    usar, med, mu, sd, mod = aprender(y - 5); X, ids = rasgos(y); X.data[~np.isfinite(X.data)] = 0
    Z = (np.log1p(X[:, usar].toarray() / med) - mu) / sd; D.append(pd.DataFrame({'id': ids, 'anio_presentado': y, 'pal': Z @ mod.coef_ + mod.intercept_}).drop_duplicates('id'))
prueba(D[0], (2018,), 'A155 2018 aparte hundidas'); rinde(D[0], (2018,), 'B155 2018 aparte log r4')
d = pd.concat(D[1:]); oa, pa, _ = prueba(d, range(2019, 2023), 'A155 2019-2022 hundidas'); ob, pb = rinde(d, range(2019, 2023), 'B155 2019-2022 log r4')
