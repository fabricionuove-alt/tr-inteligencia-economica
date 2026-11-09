"""#98: exclusiones del fondo de Noruega contra su industria, a 48 y 12 meses. python nbim_eval.py nbim.csv PRECIOS_CSVS sic.csv"""
import sys, numpy as np, pandas as pd
E = pd.read_csv(sys.argv[1], dtype={'id': str, 'mes': str}); M = lambda s: int(s[:4]) * 12 + int(s[4:6]) - 1; E['m'] = E['mes'].map(M)
pr = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[2].split(',') if x])
if 'fuente' in pr.columns: pr = pr.sort_values('fuente', ascending=False)
pr = pr.drop_duplicates(['id', 'mes']); pr['m'] = pr['mes'].map(M); P = pr[pr['precio'] > 0].pivot_table(index='m', columns='id', values='precio').sort_index()
R = P / P.shift(1); SPL = np.array([1/2, 1/3, 1/4, 1/5, 1/10, 2, 3, 4, 5, 10])
salto = pd.DataFrame(np.any(np.abs(R.values[..., None] / SPL - 1) < 0.03, axis=-1), index=R.index, columns=R.columns)
S = pd.read_csv(sys.argv[3], dtype={'id': str, 'sic': str}).drop_duplicates('id').set_index('id')['sic']
print('NBIM eventos', len(E), '| con precios', E['id'].isin(P.columns).sum(), flush=True)
for H in (48, 12):
    ex = []
    for i, m, nom in zip(E['id'], E['m'], E['empresa']):
        if i not in P.columns or m + 1 + H not in P.index or m + 1 not in P.index or i not in S.index: continue
        a, b = P.loc[m + 1], P.loc[m + 1 + H]; r = (b / a).dropna(); r = r[r > 0]; s = salto.loc[m + 2:m + 1 + H, r.index].any(axis=0); r = r[~s.values]
        if i not in r.index: continue
        si = S.reindex(r.index); g = si.str[:3] == S[i][:3]
        if g.sum() < 10: g = si.str[:2] == S[i][:2]
        ex.append((nom, m // 12, np.log(r[i]) - np.log(r[g.values & (r.index != i)]).median()))
    x = np.array([e[2] for e in ex]); rng = np.random.default_rng(0); bs = [rng.choice(x, len(x)).mean() for _ in range(5000)]
    print(f'NBIM {H} meses: n {len(x)} | exceso medio {x.mean():+.3f} IC95 [{np.percentile(bs, 2.5):+.3f},{np.percentile(bs, 97.5):+.3f}] | negativos {(x < 0).mean():.0%} | mediana {np.median(x):+.3f}', flush=True)
    if H == 48:
        pasa = x.mean() <= -0.10 and np.percentile(bs, 97.5) < 0 and (x < 0).mean() >= 0.6
        print('CRITERIO98', 'PASA' if pasa else 'no pasa', flush=True)
        for e in sorted(ex, key=lambda e: e[2]): print(f'  NBIM {e[1]} {e[0][:40]:40s} {e[2]:+.2f}')
