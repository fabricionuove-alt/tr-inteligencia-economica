"""#95: Gemma aprende a reconocer a las que hacen x3 o más a 4 años (vectores de tres secciones, a ciegas)."""
import numpy as np, pandas as pd
from scipy import sparse
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
car, PRE = 'sal-junto3', 'sae2aT'
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['anio_presentado'] = et['anio_presentado'].astype(int); et = et.drop_duplicates(['id', 'anio_presentado'])
B, F = [], []
for a in range(2013, 2021):
    F.append(pd.DataFrame({'id': np.load(f'{car}/{PRE}-{a}-ids.npy'), 'anio_presentado': a})); B.append(sparse.load_npz(f'{car}/{PRE}-{a}-L12.npz').tocsr())
X = sparse.vstack(B).tocsr(); X.data[~np.isfinite(X.data)] = 0; F = pd.concat(F, ignore_index=True)
d = F.merge(et, on=['id', 'anio_presentado'], how='left'); d['r4'] = pd.to_numeric(d['_ret4'], errors='coerce')
ok = d['r4'].notna().values; exp = ok & d['anio_presentado'].between(2013, 2016).values
y = (d['r4'] >= 3).astype(int).values
nz = np.asarray((X[np.where(exp)[0]] > 0).mean(0)).ravel(); usar = np.where(nz >= 0.02)[0]
Z = X[:, usar].toarray(); med = np.median(Z[exp][Z[exp] > 0]); Z = np.log1p(Z / med); mu, sd = Z[exp].mean(0), Z[exp].std(0) + 1e-6; Z = (Z - mu) / sd
print('COH columnas', len(usar), '| cohetes en exploración', round(y[exp].mean(), 3), flush=True)
mejor, Cb = -1, None
for C in (1e-4, 1e-3, 1e-2):
    au = []
    for a in range(2013, 2017):
        tr, te = exp & (d['anio_presentado'] != a).values, exp & (d['anio_presentado'] == a).values
        au.append(roc_auc_score(y[te], LogisticRegression(C=C, max_iter=2000).fit(Z[tr], y[tr]).decision_function(Z[te])))
    print(f'COH C {C:g} AUC exploración {np.round(au, 3).tolist()} media {np.mean(au):.3f}', flush=True)
    if np.mean(au) > mejor: mejor, Cb = np.mean(au), C
m = LogisticRegression(C=Cb, max_iter=2000).fit(Z[exp], y[exp]); con = ok & (d['anio_presentado'] >= 2017).values
d['coh'] = m.decision_function(Z)
print('COH AUC confirmación por año', {a: round(roc_auc_score(y[con & (d.anio_presentado == a).values], d.loc[con & (d.anio_presentado == a).values, 'coh']), 3) for a in range(2017, 2021)}, flush=True)
d[['id', 'anio_presentado', 'coh']].to_csv(f'{car}/out/cohete_puntaje.csv', index=False)
np.savez(f'{car}/out/cohete_modelo.npz', usar=usar, mu=mu, sd=sd, med=med, coef=m.coef_[0], b=m.intercept_[0], C=Cb)
# carteras a 4 años
t = pd.read_csv(f'{car}/out/gemma_1_1A_7_puntaje.csv', dtype={'id': str}).rename(columns={'gemma': 't3'})
x = d[con].merge(t, on=['id', 'anio_presentado']); x = x[x['sic'].notna()].copy()
x['s3'] = x['sic'].str[:3]; x['s2'] = x['sic'].str[:2]; x['g'] = np.where(x.groupby(['anio_presentado', 's3'])['id'].transform('size') >= 10, x['s3'], x['s2'])
G = ['anio_presentado', 'g']; x['pt'] = x.groupby(G)['t3'].rank(pct=True); x['pc'] = x.groupby(G)['coh'].rank(pct=True); x['pm'] = x.groupby(G)['pt'].transform(lambda s: s) * 0 + (x['pt'] + x['pc']) / 2; x['pm'] = x.groupby(G)['pm'].rank(pct=True)
def r(m): z = x[m].groupby('anio_presentado')['r4']; return z.mean(), z.apply(lambda s: (s <= .5).mean()), z.median(), z.apply(lambda s: (s >= 3).mean()), z.size()
J = r(x['pt'] > 0.9); M = r(x['pt'] >= 0)
for nom, mm in (('lista en juego (tres secciones)', x['pt'] > 0.9), ('mercado', x['pt'] >= 0), ('A cohete', x['pc'] > 0.9), ('B cohete + tres', x['pm'] > 0.9)):
    R = r(mm); g = int((R[0] > J[0]).sum()); h = int((R[1] <= J[1]).sum()); md = int((R[2] >= J[2]).sum())
    print(f'COH {nom:32s} prom {R[0].round(3).tolist()} | hund {(R[1]*100).round(1).tolist()} | mediana {R[2].round(3).tolist()} | x3+ {(R[3]*100).round(1).tolist()} | n {R[4].tolist()} | vs juego: prom {g}/4 hund {h}/4 med {md}/4 ->', 'PASA' if nom[0] in 'AB' and g >= 3 and h >= 3 and md >= 3 else '-', flush=True)
