"""Puntaje de Gemma por empresa-año sin trampas: 2013-2016 con un modelo que no vio ese año; 2017-2020 con el modelo congelado."""
import glob, numpy as np, pandas as pd
from scipy import sparse
from sklearn.linear_model import Ridge
et = pd.read_csv('/content/w/etiquetas.csv', dtype={'id': str, 'sic': str}).drop_duplicates(['id', 'anio_presentado'])
M, F = [], []
for p in sorted(glob.glob('/content/w/sae-20??.npz')):
    M.append(sparse.load_npz(p).tocsr()); F.append(pd.DataFrame({'id': np.load(p[:-4] + '-ids.npy'), 'anio_presentado': int(p[-8:-4])}))
X = sparse.vstack(M).tocsr(); F = pd.concat(F, ignore_index=True)
d = F.reset_index().merge(et, on=['id', 'anio_presentado'], how='left')
d['r4'] = pd.to_numeric(d['_ret4'], errors='coerce'); d['sic3'] = d['sic'].str[:3]
d['ter'] = pd.cut(d['tam'], [0, 1/3, 2/3, 1], include_lowest=True, labels=False)
g = ['anio_presentado', 'sic3', 'ter']
ok = d['r4'].notna() & d['sic'].notna() & (d.groupby(g)['id'].transform('size') >= 5)
d['lr'] = np.log(d['r4'].clip(lower=0.01)); d['ex'] = d['lr'] - d[ok].groupby(g)['lr'].transform('median')
exp = (d['anio_presentado'].between(2013, 2016) & ok).values
nz = np.asarray((X[np.where(exp)[0]] > 0).mean(0)).ravel(); usar = np.where(nz >= 0.02)[0]
Z = X[:, usar].toarray(); Ze = Z[exp]; med = np.median(Ze[Ze > 0]); Z = np.log1p(Z / med)
mu, sd = Z[exp].mean(0), Z[exp].std(0) + 1e-6; Z = (Z - mu) / sd
y = d['ex'].clip(-3, 3).values; d['gemma'] = np.nan
for a in range(2013, 2017):
    tr = exp & (d['anio_presentado'] != a).values; te = (d['anio_presentado'] == a).values
    d.loc[te, 'gemma'] = Ridge(alpha=1000).fit(Z[tr], y[tr]).predict(Z[te])
mod = Ridge(alpha=1000).fit(Z[exp], y[exp]); fut = (d['anio_presentado'] >= 2017).values
d.loc[fut, 'gemma'] = mod.predict(Z[fut])
d[['id', 'anio_presentado', 'gemma']].to_csv('/content/gemma_puntaje.csv', index=False)
np.savez('/content/gemma_modelo.npz', usar=usar, mu=mu, sd=sd, med=med, coef=mod.coef_, b=mod.intercept_)
print('PUNTAJE listo', int(d['gemma'].notna().sum()), d.groupby('anio_presentado')['gemma'].count().to_dict(), flush=True)
