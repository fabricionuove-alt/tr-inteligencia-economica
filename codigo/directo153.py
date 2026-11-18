"""#153: palabras que aprenden log r4 relativo a pares (camadas 2013-2017), prueba 2022 (2021 aparte). Reglas en notas/11 (#153)."""
import sys; sys.argv = ['x', 'A']
src = open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0]
src = src.replace("Xa, ya, _, _ = juntar(range(2013, 2017)); print('aprender', Xa.shape, flush=True)\n", '').replace("dfa = np.asarray((Xa > 0).sum(axis=0)).ravel() / Xa.shape[0]\n", '')
exec(src)
r1 = open('rinde149.py', encoding='utf-8').read(); exec(r1[r1.index('def rinde'):r1.index('Xp, yp, idp, anp = juntar')])
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et.anio_presentado.astype(int); et['r4'] = pd.to_numeric(et._ret4, errors='coerce')
et = et.drop_duplicates(['id', 'anio_presentado']).dropna(subset=['sic', 'tam', 'r4']); et = et[et.sic != '0000'].copy()
et['s3'] = et.sic.str[:3]; et['dec'] = np.minimum((et.tam * 10).astype(int), 9); et['lr'] = np.log(np.maximum(et.r4, .01))
gg = ['anio_presentado', 's3', 'dec']; et = et[et.groupby(gg)['id'].transform('size') >= 5].copy(); et['y'] = et.lr - et.groupby(gg)['lr'].transform('mean')
Ms, ys = [], []
for y in range(2013, 2018):
    M, ids = palabras(y); _, prim = np.unique(ids, return_index=True)
    e = et[et.anio_presentado == y].set_index('id')['y']; ok = [i for i in prim if ids[i] in e.index]
    Ms.append(M[ok]); ys.append(e.loc[ids[ok]].values)
Xa = sp.vstack(Ms).tocsr(); ya = np.concatenate(ys); dfa = np.asarray((Xa > 0).sum(axis=0)).ravel() / Xa.shape[0]
cols, f = armar(.02); r = Ridge(alpha=10000).fit(f(Xa), ya); print('aprendido', Xa.shape[0], 'empresas-año 2013-2017,', len(cols), 'columnas', flush=True)
T = pd.DataFrame([{'id': hs(o['cik']), 'anio_presentado': int(y), 't': o[y]} for o in CR for y in ('2021', '2022') if len((o.get(y) or '').split()) >= 300]).drop_duplicates(['id', 'anio_presentado'])
T['pal'] = r.predict(f(hvl.transform(T.t.tolist()))); d = T.drop(columns='t')
for y in (2022, 2021):
    z = d[d.anio_presentado == y]
    oa, pa, _ = prueba(z, (y,), f'A153 {y} hundidas'); ob, pb = rinde(z, (y,), f'B153 {y} log r4')
    if y == 2022: ok = ob > 0 and pb < .05 and oa <= -3 and pa < .05
print('CRITERIO153', 'PASA' if ok else 'no pasa')
