"""#156: palabras firmes (#146) + Gemma reaprendido cada año (#155), promedio de percentiles por industria, 2019-2022. Reglas en notas/11 (#156)."""
src = open('cadaanio155.py', encoding='utf-8').read(); exec(src[:src.index('D = []')])
MP = np.load('../repo-tr/modelos/palabras146.npz')
def pal(V):
    V = V[:, MP['cols']].tocsr().astype(float); V.data = np.log1p(1000 * V.data); return V @ MP['coef'] + MP['b']
G, W = [], []
for y in range(2019, 2023):
    usar, med, mu, sd, mod = aprender(y - 5); X, ids = rasgos(y); X.data[~np.isfinite(X.data)] = 0
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
d['pal'] = (d.groupby(['anio_presentado', 'g'])['gem'].rank(pct=True) + d.groupby(['anio_presentado', 'g'])['pw'].rank(pct=True)) / 2
print('empresas-año con las dos señales', len(d), d.anio_presentado.value_counts().sort_index().to_dict(), flush=True)
A = ['anio_presentado']; base = d[['id', 'anio_presentado']]
oa, pa, _ = prueba(d[['id', 'anio_presentado', 'pal']], range(2019, 2023), 'A156 juntas hundidas'); ob, pb = rinde(d[['id', 'anio_presentado', 'pal']], range(2019, 2023), 'B156 juntas log r4')
npos = sum(rinde(d[d.anio_presentado == y][['id', 'anio_presentado', 'pal']], (y,), f'  B156 {y}')[0] > 0 for y in range(2019, 2023))
for c, n in (('gem', 'Gemma reaprendido solo'), ('pw', 'palabras solas')):
    x = d[['id', 'anio_presentado', c]].rename(columns={c: 'pal'}); prueba(x, range(2019, 2023), f'A156i {n} hundidas'); rinde(x, range(2019, 2023), f'B156i {n} log r4')
print('CRITERIO156', 'PASA' if oa <= -4 and pa < .05 and ob > 0 and pb < .05 and npos >= 3 else 'no pasa', f'(log r4 positivo en {npos} de 4)')
