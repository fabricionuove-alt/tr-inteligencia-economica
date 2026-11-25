"""#163: parecido a otras empresas (único = bajo) (Hoberg, Phillips y Prabhala 2014): cuánto se mueve el vocabulario del mercado hacia las palabras de la empresa. Reglas en notas/11 (#159)."""
import sys; sys.argv = ['x', 'A']
src = open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0]
src = src.replace("Xa, ya, _, _ = juntar(range(2013, 2017)); print('aprender', Xa.shape, flush=True)\n", '').replace("dfa = np.asarray((Xa > 0).sum(axis=0)).ravel() / Xa.shape[0]\n", '')
exec(src)
r1 = open('rinde149.py', encoding='utf-8').read(); exec(r1[r1.index('def rinde'):r1.index('Xp, yp, idp, anp = juntar')])
def binar(M): M = M.tocsr().copy(); M.data[:] = 1.0; return M
def parecido(M):
    Bm = binar(M); V = np.asarray(Bm.mean(0)).ravel(); u = np.where((V >= .005) & (V <= .25))[0]
    X = Bm[:, u].tocsr(); n = np.sqrt(np.asarray(X.sum(1)).ravel()) + 1e-9; X = sp.diags(1 / n) @ X; X = X.tocsr(); out = np.zeros(X.shape[0])
    for i in range(0, X.shape[0], 1000):
        S = (X[i:i + 1000] @ X.T).toarray()
        for k in range(S.shape[0]): S[k, i + k] = -1
        out[i:i + 1000] = np.sort(S, axis=1)[:, -10:].mean(1)
    return out
def corpus(y):
    M, ids = palabras(y); l1 = np.load(f'{B}/edgar-corpus/vec_{y}.npz')['l1']; k = np.where(l1 >= 300)[0]
    return M[k], ids[k]
F = []
for y in range(2010, 2021):
    M, ids = corpus(y); F.append(pd.DataFrame({'id': ids, 'anio_presentado': y, 'flu': parecido(M)}).drop_duplicates('id')); print(y, flush=True)
for y in (2021, 2022):
    T = [(hs(o['cik']), o[str(y)]) for o in CR if len((o.get(str(y)) or '').split()) >= 300]
    F.append(pd.DataFrame({'id': [a for a, _ in T], 'anio_presentado': y, 'flu': parecido(hvl.transform([t for _, t in T]))}).drop_duplicates('id'))
d = pd.concat(F); print('empresas-año', d.anio_presentado.value_counts().sort_index().to_dict(), flush=True)
baja = d.assign(pal=-d.flu)[['id', 'anio_presentado', 'pal']]; alta = d.assign(pal=d.flu)[['id', 'anio_presentado', 'pal']]
A, N = range(2010, 2021), (2021, 2022)
oa, pa, _ = prueba(baja[baja.anio_presentado <= 2020], A, 'A163 más únicas 2010-2020 hundidas'); ob, pb = rinde(baja[baja.anio_presentado <= 2020], A, 'B163 más únicas 2010-2020 log r4')
na, _, _ = prueba(baja[baja.anio_presentado >= 2021], N, 'A163 más únicas 2021-2022 hundidas'); nb_, _ = rinde(baja[baja.anio_presentado >= 2021], N, 'B163 más únicas 2021-2022 log r4')
prueba(alta[alta.anio_presentado <= 2020], A, 'A163i MÁS parecidas 2010-2020 hundidas (p = de hundirse menos)'); rinde(alta[alta.anio_presentado <= 2020], A, 'B163i MÁS parecidas 2010-2020 log r4')
prueba(alta[alta.anio_presentado >= 2021], N, 'A163i MÁS parecidas 2021-2022 hundidas'); rinde(alta[alta.anio_presentado >= 2021], N, 'B163i MÁS parecidas 2021-2022 log r4')
print('CRITERIO163', 'PASA' if oa <= -3 and pa < .05 and ob > 0 and pb < .05 and na < 0 and nb_ > 0 else 'no pasa')
