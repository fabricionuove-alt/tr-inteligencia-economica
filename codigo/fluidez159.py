"""#159: fluidez (Hoberg, Phillips y Prabhala 2014): cuánto se mueve el vocabulario del mercado hacia las palabras de la empresa. Reglas en notas/11 (#159)."""
import sys; sys.argv = ['x', 'A']
src = open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0]
src = src.replace("Xa, ya, _, _ = juntar(range(2013, 2017)); print('aprender', Xa.shape, flush=True)\n", '').replace("dfa = np.asarray((Xa > 0).sum(axis=0)).ravel() / Xa.shape[0]\n", '')
exec(src)
r1 = open('rinde149.py', encoding='utf-8').read(); exec(r1[r1.index('def rinde'):r1.index('Xp, yp, idp, anp = juntar')])
def binar(M): M = M.tocsr().copy(); M.data[:] = 1.0; return M
def fluidez(Mt, Mp):
    Bt, Bp = binar(Mt), binar(Mp); Vt = np.asarray(Bt.mean(0)).ravel(); Vp = np.asarray(Bp.mean(0)).ravel()
    usar = (Vt >= .005) & (Vt <= .25); D = np.abs(Vt - Vp) * usar
    Bu = Bt.multiply(usar[None, :]).tocsr(); nb = np.sqrt(np.asarray(Bu.sum(1)).ravel()) + 1e-9
    return (Bu @ D) / nb / (np.linalg.norm(D) + 1e-12)
def corpus(y):
    M, ids = palabras(y); l1 = np.load(f'{B}/edgar-corpus/vec_{y}.npz')['l1']; k = np.where(l1 >= 300)[0]
    return M[k], ids[k]
F = []
prev = corpus(2009)
for y in range(2010, 2021):
    M, ids = corpus(y); f = fluidez(M, prev[0]); prev = (M, ids)
    F.append(pd.DataFrame({'id': ids, 'anio_presentado': y, 'flu': f}).drop_duplicates('id'))
T = {y: [o[str(y)] for o in CR if len((o.get(str(y)) or '').split()) >= 300] for y in (2020, 2021, 2022)}
I = {y: [hs(o['cik']) for o in CR if len((o.get(str(y)) or '').split()) >= 300] for y in (2021, 2022)}
for y in (2021, 2022):
    f = fluidez(hvl.transform(T[y]), hvl.transform(T[y - 1])); F.append(pd.DataFrame({'id': I[y], 'anio_presentado': y, 'flu': f}).drop_duplicates('id'))
d = pd.concat(F); print('empresas-año', d.anio_presentado.value_counts().sort_index().to_dict(), flush=True)
baja = d.assign(pal=-d.flu)[['id', 'anio_presentado', 'pal']]; alta = d.assign(pal=d.flu)[['id', 'anio_presentado', 'pal']]
A, N = range(2010, 2021), (2021, 2022)
oa, pa, _ = prueba(baja[baja.anio_presentado <= 2020], A, 'A159 menor fluidez 2010-2020 hundidas'); ob, pb = rinde(baja[baja.anio_presentado <= 2020], A, 'B159 menor fluidez 2010-2020 log r4')
na, _, _ = prueba(baja[baja.anio_presentado >= 2021], N, 'A159 menor fluidez 2021-2022 hundidas'); nb_, _ = rinde(baja[baja.anio_presentado >= 2021], N, 'B159 menor fluidez 2021-2022 log r4')
prueba(alta[alta.anio_presentado <= 2020], A, 'A159i MAYOR fluidez 2010-2020 hundidas (p = de hundirse menos)'); rinde(alta[alta.anio_presentado <= 2020], A, 'B159i MAYOR fluidez 2010-2020 log r4')
prueba(alta[alta.anio_presentado >= 2021], N, 'A159i MAYOR fluidez 2021-2022 hundidas'); rinde(alta[alta.anio_presentado >= 2021], N, 'B159i MAYOR fluidez 2021-2022 log r4')
print('CRITERIO159', 'PASA' if oa <= -3 and pa < .05 and ob > 0 and pb < .05 and na < 0 and nb_ > 0 else 'no pasa')
