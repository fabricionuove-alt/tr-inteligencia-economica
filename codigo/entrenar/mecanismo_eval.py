"""#84: picos de público en Wikipedia, con y sin venta de directivos. Uso: python mecanismo_eval.py filas.csv wiki_vistas.csv DIRECTIVOS_CSVS PRECIOS_CSVS"""
import sys, numpy as np, pandas as pd
df = pd.read_csv(sys.argv[1], usecols=lambda c: c in ('id', 'log_activos', '_presentado'), dtype={'id': str}, low_memory=False)
W = pd.read_csv(sys.argv[2], dtype={'id': str, 'mes': str}); W['m'] = W['mes'].str[:4].astype(int) * 12 + W['mes'].str[4:6].astype(int) - 1
V = W.pivot_table(index='m', columns='id', values='vistas', aggfunc='sum').sort_index()
base = V.shift(1).rolling(12, min_periods=10).median()
pico = (V >= 2 * base) & (base >= 100)
ev = []
for i in pico.columns:
    ms = pico.index[pico[i].values]; ult = -99
    for m in ms:
        if m - ult >= 6: ev.append((i, int(m))); ult = m          # un pico cada 6 meses como máximo
E = pd.DataFrame(ev, columns=['id', 'm']); E = E[E['m'] >= 2016 * 12]
Dd = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[3].split(',') if x])
Dd['m'] = Dd['mes'].str[:4].astype(int) * 12 + Dd['mes'].str[4:6].astype(int) - 1
S = Dd[Dd['tipo'] == 'S'].groupby(['id', 'm'])['valor'].sum().to_dict(); Pc = Dd[Dd['tipo'] == 'P'].groupby(['id', 'm'])['valor'].sum().to_dict()
E['venta'] = [sum(S.get((i, k), 0) for k in (m, m + 1)) > sum(Pc.get((i, k), 0) for k in (m, m + 1)) and sum(S.get((i, k), 0) for k in (m, m + 1)) > 0 for i, m in zip(E['id'], E['m'])]
print(f'MEC picos {len(E)} | con venta de directivos {int(E["venta"].sum())}', flush=True)
pr = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[4].split(',') if x])
if 'fuente' in pr.columns: pr = pr.sort_values('fuente', ascending=False)
pr = pr.drop_duplicates(['id', 'mes']); pr['m'] = pr['mes'].str[:4].astype(int) * 12 + pr['mes'].str[4:6].astype(int) - 1
P = pr[pr['precio'] > 0].pivot_table(index='m', columns='id', values='precio')
ps = df['_presentado'].astype(str); ok = ps.str.len() >= 7; df = df[ok].copy()
df['mp'] = ps[ok].str[:4].astype(int) * 12 + ps[ok].str[5:7].astype(int) - 1; df['la'] = pd.to_numeric(df['log_activos'], errors='coerce'); df = df.dropna(subset=['la']).sort_values('mp')
cache = {}
def ctrl(m0):
    if m0 in cache: return cache[m0]
    if m0 not in P.index or m0 + 12 not in P.index: cache[m0] = None; return None
    r = (P.loc[m0 + 12] / P.loc[m0]).dropna(); t = df[df['mp'] < m0].drop_duplicates('id', keep='last').set_index('id')['la'].reindex(r.index).dropna(); r = r.reindex(t.index)
    dec = np.minimum((t.rank(pct=True, method='first') * 10).astype(int), 9); cache[m0] = (r, dec, np.log(r).groupby(dec).mean()); return cache[m0]
fil = []
for i, m, v in zip(E['id'], E['m'], E['venta']):
    c = ctrl(m + 2)
    if c is None or i not in c[0].index: continue
    r, dec, med = c; fil.append((m // 12, bool(v), float(np.log(r[i]) - med[dec[i]]), int(r[i] <= 0.5)))
X = pd.DataFrame(fil, columns=['anio', 'venta', 'exceso', 'des'])
A, B = X[X['venta']], X[~X['venta']]
g = np.random.default_rng(0); b = [g.choice(A['exceso'].values, len(A)).mean() - g.choice(B['exceso'].values, len(B)).mean() for _ in range(2000)]; lo, hi = np.percentile(b, [2.5, 97.5])
pa = (A.groupby('anio')['exceso'].mean() - B.groupby('anio')['exceso'].mean()).dropna()
print(f'CRITERIO84: con venta n {len(A)} exceso {A["exceso"].mean():+.4f} des {100 * A["des"].mean():.1f}% | sin venta n {len(B)} exceso {B["exceso"].mean():+.4f} des {100 * B["des"].mean():.1f}% | diferencia {A["exceso"].mean() - B["exceso"].mean():+.4f} IC95 [{lo:+.4f},{hi:+.4f}] | años negativos {(pa < 0).sum()} de {len(pa)} {pa.round(3).to_dict()} ->',
      'EL MECANISMO APARECE' if hi < 0 and (pa < 0).mean() >= 0.7 else 'no pasa', flush=True)
print(f'MEC todos los picos contra su tamaño: {X["exceso"].mean():+.4f} (n {len(X)})', flush=True)
