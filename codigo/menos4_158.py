"""#158 (base de #156 con y-4): palabras firmes (#146) + Gemma reaprendido cada año (#155), promedio de percentiles por industria, 2019-2022. Reglas en notas/11 (#156)."""
src = open('cadaanio155.py', encoding='utf-8').read(); exec(src[:src.index('D = []')])
MP = np.load('../repo-tr/modelos/palabras146.npz')
def pal(V):
    V = V[:, MP['cols']].tocsr().astype(float); V.data = np.log1p(1000 * V.data); return V @ MP['coef'] + MP['b']
G, W = [], []
for y in range(2019, 2023):
    usar, med, mu, sd, mod = aprender(y - 4); X, ids = rasgos(y); X.data[~np.isfinite(X.data)] = 0
    Z = (np.log1p(X[:, usar].toarray() / med) - mu) / sd; G.append(pd.DataFrame({'id': ids, 'anio_presentado': y, 'gem': Z @ mod.coef_ + mod.intercept_}).drop_duplicates('id'))
    if y <= 2020:
        M, wid = palabras(y); _, prim = np.unique(wid, return_index=True); W.append(pd.DataFrame({'id': wid[prim], 'anio_presentado': y, 'pw': pal(M[prim])}))
    else:
        T = [(hs(o['cik']), o[str(y)]) for o in CR if len((o.get(str(y)) or '').split()) >= 300]
        W.append(pd.DataFrame({'id': [a for a, _ in T], 'anio_presentado': y, 'pw': pal(hvl.transform([t for _, t in T]))}).drop_duplicates('id'))
d = pd.concat(G).merge(pd.concat(W), on=['id', 'anio_presentado'])
s = et[['id', 'anio_presentado', 'sic']].dropna(); d = d.merge(s, on=['id', 'anio_presentado']); d = d[d.sic != '0000'].copy()
d['s3'] = d.sic.str[:3]; d['s2'] = d.sic.str[:2]; d['g'] = ''
for y, z in d.groupby('anio_presentado'): d.loc[z.index, 'g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2'])

k = ['anio_presentado', 'g']; d['fp'] = d.groupby(k)['pw'].rank(pct=True) > .8
d['pal'] = 0.0; f2 = d[d.fp].copy(); f2['q'] = f2.groupby(k)['gem'].rank(pct=True)
d.loc[f2.index, 'pal'] = np.where(f2.q > .5, 2.0, 1.0)
d['pal'] += d.groupby(k)['gem'].rank(pct=True) * 1e-3
x = d[['id', 'anio_presentado', 'pal']]
oa, pa, _ = prueba(x, range(2019, 2023), 'A158 en fila y-4 hundidas'); ob, pb = rinde(x, range(2019, 2023), 'B158 en fila y-4 log r4')
r = {y: rinde(x[x.anio_presentado == y], (y,), f'  B158 {y}')[0] for y in range(2019, 2023)}; npos = sum(v > 0 for v in r.values())
for y in range(2019, 2023): prueba(x[x.anio_presentado == y], (y,), f'  A158 {y}')
g = d[['id', 'anio_presentado', 'gem']].rename(columns={'gem': 'pal'})
prueba(g, range(2019, 2023), 'A158i Gemma y-4 solo hundidas'); rinde(g, range(2019, 2023), 'B158i Gemma y-4 solo log r4')
for y in range(2019, 2023): rinde(g[g.anio_presentado == y], (y,), f'  B158i {y}')
print('CRITERIO158', 'PASA' if oa <= -4 and pa < .05 and ob > 0 and pb < .05 and npos >= 3 and r[2021] > 0 else 'no pasa', f'(log r4 positivo en {npos} de 4; 2021 {r[2021]:+.3f})')
