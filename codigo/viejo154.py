"""#154, informativo: Gemma viejo (2013-2016) en 2022 con las mismas medidas, para comparar con el nuevo."""
src = open('gemma154.py', encoding='utf-8').read()
cab = src[:src.index('# 1) Gemma nuevo')]; exec(cab)
from scipy import sparse
m = np.load('sal-junto3/out/gemma_1_1A_7_modelo.npz')
def carga(npz, ids): return sparse.load_npz(npz).tocsr(), np.load(ids, allow_pickle=True)
P = [carga('sal-anon2124/sae2a-textos-2022-L12.npz', 'sal-anon2124/sae2a-textos-2022-ids.npy'), carga('sal-lee2022/sae2a-textos1A-2022-L12.npz', 'sal-lee2022/sae2a-textos1A-2022-ids.npy'), carga('sal-lee2022/sae2a-textos7-2022-L12.npz', 'sal-lee2022/sae2a-textos7-2022-ids.npy')]
com = sorted(set.intersection(*[set(i) for _, i in P])); pos = [{v: k for k, v in enumerate(i)} for _, i in P]
X2 = sparse.hstack([x[[p[c] for c in com]] for (x, _), p in zip(P, pos)]).tocsr(); X2.data[~np.isfinite(X2.data)] = 0
Z2 = (np.log1p(X2[:, m['usar']].toarray() / m['med']) - m['mu']) / m['sd']; dg = pd.DataFrame({'id': [str(c) for c in com], 'anio_presentado': 2022, 'pal': Z2 @ m['coef'] + m['b']})
prueba(dg, (2022,), 'A154v Gemma viejo 2022 hundidas'); rinde(dg, (2022,), 'B154v Gemma viejo 2022 log r4')
