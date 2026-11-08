"""#65 (notas/11): ¿qué conceptos internos de Gemma (Gemma Scope, capa 12, 16.384) marcan el lado a 4 años?
Aprende SÓLO con 10-K presentados 2013-2016 (exploración); confirma 2017-2020 con el puntaje congelado.
Uso: python sae_analisis.py CARPETA_SAE etiquetas.csv [salida.json]"""
import sys, json, glob, numpy as np, pandas as pd
from scipy import sparse
from sklearn.linear_model import Ridge
car, et = sys.argv[1], pd.read_csv(sys.argv[2], dtype={'id': str, 'sic': str})
et = et.dropna(subset=['anio_presentado']); et['anio_presentado'] = et['anio_presentado'].astype(int)
et = et.drop_duplicates(['id', 'anio_presentado'])
M, filas = [], []
for p in sorted(glob.glob(f'{car}/sae-20??.npz')):
    a = int(p[-8:-4]); X = sparse.load_npz(p).tocsr(); ids = np.load(p[:-4] + '-ids.npy')
    M.append(X); filas.append(pd.DataFrame({'id': ids, 'anio_presentado': a}))
X = sparse.vstack(M).tocsr(); F = pd.concat(filas, ignore_index=True)
d = F.reset_index().merge(et, on=['id', 'anio_presentado'], how='inner')
d['r4'] = pd.to_numeric(d['_ret4'], errors='coerce'); d = d.dropna(subset=['r4', 'sic'])
d['sic3'] = d['sic'].str[:3]; d['ter'] = pd.cut(d['tam'], [0, 1/3, 2/3, 1], include_lowest=True, labels=False)
g = ['anio_presentado', 'sic3', 'ter']
d = d[d.groupby(g)['id'].transform('size') >= 5].copy()
d['lr'] = np.log(d['r4'].clip(lower=0.01)); d['ex'] = d['lr'] - d.groupby(g)['lr'].transform('median')     # contra su industria y tamaño
print(f'SAE filas con concepto y resultado: {len(d)} | por año {d["anio_presentado"].value_counts().sort_index().to_dict()}', flush=True)
Xd = X[d['index'].values]
nz = np.asarray((Xd > 0).mean(0)).ravel(); usar = np.where(nz >= 0.02)[0]                       # conceptos presentes en ≥ 2% de las empresas
Z = Xd[:, usar].toarray(); Z = np.log1p(Z / (np.median(Z[Z > 0]) + 1e-9))
exp = d['anio_presentado'].between(2013, 2016).values; con = d['anio_presentado'].between(2017, 2020).values
mu, sd = Z[exp].mean(0), Z[exp].std(0) + 1e-6; Z = (Z - mu) / sd
y = d['ex'].clip(-3, 3).values
mejor, mejor_a = None, None
for alfa in (1e2, 1e3, 1e4, 1e5):                                                                # alfa elegido DENTRO de la exploración
    cv = []
    for a in range(2013, 2017):
        tr, te = exp & (d['anio_presentado'] != a).values, (d['anio_presentado'] == a).values
        p = Ridge(alpha=alfa).fit(Z[tr], y[tr]).predict(Z[te]); cv.append(np.corrcoef(p, y[te])[0, 1])
    print(f'SAE exploración alfa {alfa:g}: correlación por año dejado afuera {np.round(cv, 3).tolist()}', flush=True)
    if mejor is None or np.mean(cv) > mejor: mejor, mejor_a = np.mean(cv), alfa
mod = Ridge(alpha=mejor_a).fit(Z[exp], y[exp]); d['puntaje'] = mod.predict(Z)
coef = pd.Series(mod.coef_, index=usar).sort_values()
res = {'alfa': mejor_a, 'conceptos_usados': int(len(usar)), 'a_favor': coef.tail(25).round(5).to_dict(), 'en_contra': coef.head(25).round(5).to_dict()}
print('SAE conceptos a favor (índice: peso):', {int(k): round(v, 4) for k, v in coef.tail(15).items()}, flush=True)
print('SAE conceptos en contra:', {int(k): round(v, 4) for k, v in coef.head(15).items()}, flush=True)
# CONFIRMACIÓN, criterio de #62 (escrito antes): decil de arriba menos quintil de abajo del puntaje, dentro de industria (SIC 3) y tamaño
x = d[con].copy(); x['p'] = x.groupby(g)['puntaje'].rank(pct=True)
ar, ab = x[x['p'] > 0.9], x[x['p'] <= 0.2]
dif = (ar.groupby('anio_presentado')['ex'].mean() - ab.groupby('anio_presentado')['ex'].mean()).round(4)
des = (ar.groupby('anio_presentado')['r4'].apply(lambda s: (s <= 0.5).mean()) - ab.groupby('anio_presentado')['r4'].apply(lambda s: (s <= 0.5).mean())).round(4)
pasa = bool((dif > 0).sum() >= 3 and dif.mean() > 0 and (des < 0).sum() >= 3 and len(dif) == 4)
res.update({'confirmacion_dif': dif.to_dict(), 'confirmacion_des': des.to_dict(), 'pasa': pasa})
print(f'CRITERIO65 confirmación 2017-2020 | arriba-abajo a 4 años: {dif.to_dict()} media {dif.mean():.4f} | desastres: {des.to_dict()} -> {"PASA" if pasa else "no pasa"}', flush=True)
json.dump(res, open(sys.argv[3] if len(sys.argv) > 3 else 'sae_resultado.json', 'w'), indent=1, default=str)
np.save('sae_modelo.npy', {'usar': usar, 'mu': mu, 'sd': sd, 'coef': mod.coef_, 'b': mod.intercept_, 'med': None}, allow_pickle=True)
