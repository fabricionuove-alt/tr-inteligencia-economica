"""#97: la mezcla #96 sobre los 10-K de 2021 y 2022, con los modelos congelados."""
import numpy as np, pandas as pd
from scipy import sparse
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et['anio_presentado'].astype(int)
et = et.drop_duplicates(['id', 'anio_presentado'])
mT, mC = np.load('sal-junto3/out/gemma_1_1A_7_modelo.npz'), np.load('sal-junto3/out/cohete_modelo.npz')
ok1 = ok2 = 0
for A in (2021, 2022):
    P = [(sparse.load_npz(a).tocsr(), np.load(b)) for a, b in ((f'sal-anon2124/sae2a-textos-{A}-L12.npz', f'sal-anon2124/sae2a-textos-{A}-ids.npy'),
         (f'sal-lee{A}/sae2a-textos1A-{A}-L12.npz', f'sal-lee{A}/sae2a-textos1A-{A}-ids.npy'), (f'sal-lee{A}/sae2a-textos7-{A}-L12.npz', f'sal-lee{A}/sae2a-textos7-{A}-ids.npy'))]
    com = sorted(set.intersection(*[set(i) for _, i in P])); pos = [{v: k for k, v in enumerate(i)} for _, i in P]
    X = sparse.hstack([x[[p[c] for c in com]] for (x, _), p in zip(P, pos)]).tocsr(); X.data[~np.isfinite(X.data)] = 0
    def pun(m): Z = np.log1p(X[:, m['usar']].toarray() / m['med']); Z = (Z - m['mu']) / m['sd']; return Z @ m['coef'] + m['b']
    d = pd.DataFrame({'id': com, 'anio_presentado': A, 't3': pun(mT), 'coh': pun(mC)}).merge(et, on=['id', 'anio_presentado'])
    d['r4'] = pd.to_numeric(d['_ret4'], errors='coerce'); d['r1'] = pd.to_numeric(d['_ret1'], errors='coerce'); d = d[d['sic'].notna()].copy()
    d['s3'] = d['sic'].str[:3]; d['s2'] = d['sic'].str[:2]; d['g'] = np.where(d.groupby('s3')['id'].transform('size') >= 10, d['s3'], d['s2'])
    d['pt'] = d.groupby('g')['t3'].rank(pct=True); d['pc'] = d.groupby('g')['coh'].rank(pct=True)
    for r in ('r4', 'r1'):
        z = d[d[r].notna()]; J = z[z.pt > 0.9]; C = z[z.pc > 0.9]
        w = pd.concat([pd.Series(0.5 / len(J), index=J.index), pd.Series(0.5 / len(C), index=C.index)]).groupby(level=0).sum()
        v = z.loc[w.index, r]; pm, hm = (w * v).sum(), (w * (v <= .5)).sum(); mk, hk = z[r].mean(), (z[r] <= .5).mean()
        print(f'TR97 {A} {"4 años" if r == "r4" else "12 meses"}: mezcla ×{pm:.3f} hund {hm:.1%} | tres secciones ×{J[r].mean():.3f} hund {(J[r] <= .5).mean():.1%} | cohetes ×{C[r].mean():.3f} hund {(C[r] <= .5).mean():.1%} | mercado ×{mk:.3f} hund {hk:.1%} | n mercado {len(z)}', flush=True)
        if r == 'r4': ok1 += pm > mk; ok2 += hm < hk
print('CRITERIO97 promedio > mercado', ok1, 'de 2 | menos hundidas', ok2, 'de 2 ->', 'SE CONFIRMA' if ok1 == 2 and ok2 >= 1 else 'no se confirma')
