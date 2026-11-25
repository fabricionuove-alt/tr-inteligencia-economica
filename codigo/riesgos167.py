"""#167: riesgos (1A) parecidos a los de otras empresas (Hoberg, Phillips y Prabhala 2014): cuánto se mueve el vocabulario del mercado hacia las palabras de la empresa. Reglas en notas/11 (#159)."""
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
    M = sp.load_npz(f'{B}/edgar-corpus/m1a_{y}.npz').tocsr(); ciks = np.load(f'{B}/edgar-corpus/vec_{y}.npz')['ciks']; ids = np.array([hs(int(c)) for c in ciks])
    l = np.load(f'{B}/edgar-corpus/vec_{y}.npz')['l1a']; k = np.where(l >= 300 * 6)[0]
    return M[k], ids[k]
F = []
for y in range(2010, 2021):
    M, ids = corpus(y); F.append(pd.DataFrame({'id': ids, 'anio_presentado': y, 'flu': parecido(M)}).drop_duplicates('id')); print(y, flush=True)
d = pd.concat(F); print('empresas-año', d.anio_presentado.value_counts().sort_index().to_dict(), flush=True)
par = d.assign(pal=d.flu)[['id', 'anio_presentado', 'pal']]; uni = d.assign(pal=-d.flu)[['id', 'anio_presentado', 'pal']]
A = range(2010, 2021)
oa, pa, _ = prueba(par, A, 'A167 riesgos MÁS parecidos hundidas (p = de hundirse menos)'); ob, pb = rinde(par, A, 'B167 riesgos MÁS parecidos log r4 (p = de rendir más)')
prueba(uni, A, 'A167i riesgos más únicos hundidas'); rinde(uni, A, 'B167i riesgos más únicos log r4')
print(f'p de hundirse MÁS {1-pa:.4f}; p de rendir MENOS {1-pb:.4f}')
print('CRITERIO167', 'PASA' if oa >= 3 and 1 - pa < .05 and ob < 0 and 1 - pb < .05 else 'no pasa')
