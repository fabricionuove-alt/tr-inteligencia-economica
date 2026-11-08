"""#67 (notas/11): más Gemma (512 tokens, capas 12 y 20, 512 conceptos por empresa). Mismo método y criterio que #65.
Aprende con 2013-2016, confirma 2017-2020; guarda el puntaje sin trampas (2013-2016 dejando el año afuera) y el modelo.
Uso: python sae_analisis2.py CARPETA etiquetas.csv CAPAS(12,20)"""
import sys, json, glob, numpy as np, pandas as pd
from scipy import sparse
from sklearn.linear_model import Ridge
import os
car, CAPAS = sys.argv[1], sys.argv[3].split(','); PRE = os.environ.get('PREFIJO', 'sae2'); SAL = os.environ.get('SALIDA', 'gemma2')
et = pd.read_csv(sys.argv[2], dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['anio_presentado'] = et['anio_presentado'].astype(int); et = et.drop_duplicates(['id', 'anio_presentado'])
bloques, F = {c: [] for c in CAPAS}, []
for a in range(2013, 2021):
    ids = np.load(f'{car}/{PRE}-{a}-ids.npy'); F.append(pd.DataFrame({'id': ids, 'anio_presentado': a}))
    for c in CAPAS:
        bloques[c].append(sparse.load_npz(f'{car}/{PRE}-{a}-L{c}.npz').tocsr())
X = sparse.hstack([sparse.vstack(bloques[c]) for c in CAPAS]).tocsr(); F = pd.concat(F, ignore_index=True)
malo = np.zeros(X.shape[0], bool); r_, _ = X.nonzero(); malo[np.unique(r_[~np.isfinite(X.data)])] = True   # desbordes de media precisión
X.data[~np.isfinite(X.data)] = 0; X.eliminate_zeros()
print(f'SAE2 empresas con valores inválidos (descartadas): {malo.sum()} de {len(malo)}', flush=True)
d = F.reset_index().merge(et, on=['id', 'anio_presentado'], how='left')
d['r4'] = pd.to_numeric(d['_ret4'], errors='coerce'); d['sic3'] = d['sic'].str[:3]
d['ter'] = pd.cut(d['tam'], [0, 1/3, 2/3, 1], include_lowest=True, labels=False)
g = ['anio_presentado', 'sic3', 'ter']
ok = (d['r4'].notna() & d['sic'].notna() & d['tam'].notna()).values & ~malo[d['index'].values]
ok &= (d.groupby(g)['id'].transform('size') >= 5).values
d['lr'] = np.log(d['r4'].clip(lower=0.01)); d['ex'] = np.nan
d.loc[ok, 'ex'] = d.loc[ok, 'lr'] - d[ok].groupby(g)['lr'].transform('median')
exp = ok & d['anio_presentado'].between(2013, 2016).values; con = ok & d['anio_presentado'].between(2017, 2020).values
print(f'SAE2 {X.shape[1]} columnas | filas con resultado {ok.sum()} | por año {d[ok]["anio_presentado"].value_counts().sort_index().to_dict()}', flush=True)
nz = np.asarray((X[np.where(exp)[0]] > 0).mean(0)).ravel(); usar = np.where(nz >= 0.02)[0]
Z = X[:, usar].toarray(); Ze = Z[exp]; med = np.median(Ze[Ze > 0]); Z = np.log1p(Z / med)
mu, sd = Z[exp].mean(0), Z[exp].std(0) + 1e-6; Z = (Z - mu) / sd
y = d['ex'].clip(-3, 3).values
mejor, alfa = -9, None
for al in (1e2, 1e3, 1e4, 1e5):
    cv = []
    for a in range(2013, 2017):
        tr, te = exp & (d['anio_presentado'] != a).values, exp & (d['anio_presentado'] == a).values
        cv.append(np.corrcoef(Ridge(alpha=al).fit(Z[tr], y[tr]).predict(Z[te]), y[te])[0, 1])
    print(f'SAE2 exploración alfa {al:g}: {np.round(cv, 3).tolist()} media {np.mean(cv):.3f}', flush=True)
    if np.mean(cv) > mejor: mejor, alfa = np.mean(cv), al
d['gemma'] = np.nan
for a in range(2013, 2017):
    tr, te = exp & (d['anio_presentado'] != a).values, (d['anio_presentado'] == a).values
    d.loc[te, 'gemma'] = Ridge(alpha=alfa).fit(Z[tr], y[tr]).predict(Z[te])
mod = Ridge(alpha=alfa).fit(Z[exp], y[exp]); fut = (d['anio_presentado'] >= 2017).values; d.loc[fut, 'gemma'] = mod.predict(Z[fut])
x = d[con].copy(); x['p'] = x.groupby(g)['gemma'].rank(pct=True)
ar, ab = x[x['p'] > 0.9], x[x['p'] <= 0.2]
dif = (ar.groupby('anio_presentado')['ex'].mean() - ab.groupby('anio_presentado')['ex'].mean()).round(4)
des = (ar.groupby('anio_presentado')['r4'].apply(lambda s: (s <= 0.5).mean()) - ab.groupby('anio_presentado')['r4'].apply(lambda s: (s <= 0.5).mean())).round(4)
pasa = bool((dif > 0).sum() >= 3 and dif.mean() > 0 and (des < 0).sum() >= 3 and len(dif) == 4)
print(f'CRITERIO {PRE} alfa {alfa:g} | confirmación arriba-abajo a 4 años {dif.to_dict()} media {dif.mean():.4f} | desastres {des.to_dict()} -> {"PASA" if pasa else "no pasa"}', flush=True)
d[['id', 'anio_presentado', 'gemma']].to_csv(f'{os.environ.get("OUT", "/content")}/{SAL}_puntaje.csv', index=False)
np.savez(f'{os.environ.get("OUT", "/content")}/{SAL}_modelo.npz', usar=usar, mu=mu, sd=sd, med=med, coef=mod.coef_, b=mod.intercept_, capas=np.array(CAPAS), ancho=np.array([bloques[c][0].shape[1] for c in CAPAS]))
json.dump({'alfa': alfa, 'dif': dif.to_dict(), 'des': des.to_dict(), 'pasa': pasa}, open(f'{os.environ.get("OUT", "/content")}/{SAL}_resultado.json', 'w'), indent=1, default=str)
