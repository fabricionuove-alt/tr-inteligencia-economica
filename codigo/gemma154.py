"""#154: criterio de Gemma reaprendido con 2013-2017 (receta de sae_analisis2.py, alfa 1000), palabras que lo imitan, prueba 2022. Reglas en notas/11 (#154)."""
import sys; sys.argv = ['x', 'A']
from scipy import sparse
src = open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0]
src = src.replace("Xa, ya, _, _ = juntar(range(2013, 2017)); print('aprender', Xa.shape, flush=True)\n", '').replace("dfa = np.asarray((Xa > 0).sum(axis=0)).ravel() / Xa.shape[0]\n", '')
exec(src)
r1 = open('rinde149.py', encoding='utf-8').read(); exec(r1[r1.index('def rinde'):r1.index('Xp, yp, idp, anp = juntar')])
# 1) Gemma nuevo, receta original
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et['anio_presentado'].astype(int); et = et.drop_duplicates(['id', 'anio_presentado'])
bl, F = [], []
for a in range(2013, 2018):
    F.append(pd.DataFrame({'id': np.load(f'sal-junto3/sae2aT-{a}-ids.npy', allow_pickle=True).astype(str), 'anio_presentado': a})); bl.append(sparse.load_npz(f'sal-junto3/sae2aT-{a}-L12.npz').tocsr())
X = sparse.vstack(bl).tocsr(); F = pd.concat(F, ignore_index=True)
malo = np.zeros(X.shape[0], bool); r_, _ = X.nonzero(); malo[np.unique(r_[~np.isfinite(X.data)])] = True; X.data[~np.isfinite(X.data)] = 0; X.eliminate_zeros()
d = F.reset_index().merge(et, on=['id', 'anio_presentado'], how='left'); d['r4'] = pd.to_numeric(d['_ret4'], errors='coerce'); d['sic3'] = d['sic'].str[:3]
d['ter'] = pd.cut(d['tam'], [0, 1/3, 2/3, 1], include_lowest=True, labels=False); g = ['anio_presentado', 'sic3', 'ter']
ok = (d['r4'].notna() & d['sic'].notna() & d['tam'].notna()).values & ~malo[d['index'].values]; ok &= (d.groupby(g)['id'].transform('size') >= 5).values
d['lr'] = np.log(d['r4'].clip(lower=0.01)); d['ex'] = np.nan; d.loc[ok, 'ex'] = d.loc[ok, 'lr'] - d[ok].groupby(g)['lr'].transform('median')
nz = np.asarray((X[np.where(ok)[0]] > 0).mean(0)).ravel(); usar = np.where(nz >= 0.02)[0]
Z = X[:, usar].toarray(); Ze = Z[ok]; med = np.median(Ze[Ze > 0]); Z = np.log1p(Z / med); mu, sd = Z[ok].mean(0), Z[ok].std(0) + 1e-6; Z = (Z - mu) / sd
mod = Ridge(alpha=1000).fit(Z[ok], d['ex'].clip(-3, 3).values[ok]); print('Gemma nuevo: aprendido con', ok.sum(), 'empresas-año 2013-2017,', len(usar), 'columnas', flush=True)
sec = usar // 16384
def parcial_nuevo(y):
    Xy = sparse.load_npz(f'sal-junto3/sae2aT-{y}-L12.npz').tocsr(); ids = np.load(f'sal-junto3/sae2aT-{y}-ids.npy', allow_pickle=True).astype(str); Xy.data[~np.isfinite(Xy.data)] = 0
    Zy = (np.log1p(Xy[:, usar].toarray() / med) - mu) / sd
    return pd.Series(Zy[:, sec == 0] @ mod.coef_[sec == 0], index=ids)
# 2) palabras que imitan el parcial «negocio» del Gemma nuevo (aprende 2013-2016, como #146)
Ms, ys = [], []
for y in range(2013, 2017):
    M, ids = palabras(y); p = parcial_nuevo(y); p = p[~p.index.duplicated()]; _, prim = np.unique(ids, return_index=True)
    k = [i for i in prim if ids[i] in p.index]; Ms.append(M[k]); ys.append(p.loc[ids[k]].values)
Xa = sp.vstack(Ms).tocsr(); ya = np.concatenate(ys); dfa = np.asarray((Xa > 0).sum(axis=0)).ravel() / Xa.shape[0]
cols, f = armar(.02); r = Ridge(alpha=10000).fit(f(Xa), ya); print('palabras nuevas:', Xa.shape[0], 'descripciones,', len(cols), 'columnas', flush=True)
T = pd.DataFrame([{'id': hs(o['cik']), 'anio_presentado': 2022, 't': o['2022']} for o in CR if len((o.get('2022') or '').split()) >= 300]).drop_duplicates('id')
T['pal'] = r.predict(f(hvl.transform(T.t.tolist()))); dpal = T.drop(columns='t')
oa, pa, _ = prueba(dpal, (2022,), 'A154 palabras 2022 hundidas'); ob, pb = rinde(dpal, (2022,), 'B154 palabras 2022 log r4')
# 3) informativo: Gemma nuevo directo en 2022 (rasgos ya calculados)
def carga(npz, ids): return sparse.load_npz(npz).tocsr(), np.load(ids, allow_pickle=True)
P = [carga('sal-anon2124/sae2a-textos-2022-L12.npz', 'sal-anon2124/sae2a-textos-2022-ids.npy'), carga('sal-lee2022/sae2a-textos1A-2022-L12.npz', 'sal-lee2022/sae2a-textos1A-2022-ids.npy'), carga('sal-lee2022/sae2a-textos7-2022-L12.npz', 'sal-lee2022/sae2a-textos7-2022-ids.npy')]
com = sorted(set.intersection(*[set(i) for _, i in P])); pos = [{v: k for k, v in enumerate(i)} for _, i in P]
X2 = sparse.hstack([x[[p[c] for c in com]] for (x, _), p in zip(P, pos)]).tocsr(); X2.data[~np.isfinite(X2.data)] = 0
Z2 = (np.log1p(X2[:, usar].toarray() / med) - mu) / sd; dg = pd.DataFrame({'id': [str(c) for c in com], 'anio_presentado': 2022, 'pal': Z2 @ mod.coef_ + mod.intercept_})
prueba(dg, (2022,), 'A154i Gemma nuevo 2022 hundidas'); rinde(dg, (2022,), 'B154i Gemma nuevo 2022 log r4')
print('CRITERIO154', 'PASA' if ob > 0 and pb < .05 and oa <= -3 and pa < .05 else 'no pasa')
