"""#75: dinastías por presencia: cuando un apellido de dinastía entra como director o directivo. Uso: python presencia_eval.py filas.csv dinastias.csv PRECIOS_CSVS"""
import sys, numpy as np, pandas as pd
DIST = {'ROTHSCHILD', 'WALLENBERG', 'AGNELLI', 'ELKANN', 'ROCKEFELLER', 'PRITZKER', 'DU PONT', 'DUPONT', 'MELLON', 'BRONFMAN', 'SAFRA', 'PICTET', 'PEUGEOT', 'ARNAULT',
        'BETTENCOURT', 'QUANDT', 'KLATTEN', 'PORSCHE', 'PIECH', 'OETKER', 'THYSSEN', 'BOTIN', 'BOTÍN', 'MULLIEZ', 'DESMARAIS', 'WERTHEIMER', 'LAUDER', 'HEARST', 'NEWHOUSE',
        'ZIFF', 'HABSBURG', 'HOHENZOLLERN', 'LIECHTENSTEIN', 'THURN', 'GROSVENOR', 'GUINNESS', 'CADBURY', 'SAINSBURY', 'BRENNINKMEYER', 'HEINEKEN', 'BONNIER', 'KAMPRAD',
        'AMBANI', 'BIRLA', 'MAHINDRA', 'REIMANN'}
df = pd.read_csv(sys.argv[1], usecols=lambda c: c in ('id', 'log_activos', '_presentado'), dtype={'id': str}, low_memory=False)
D = pd.read_csv(sys.argv[2], dtype=str); D['anio'] = D['anio'].astype(int)
D = D[D['apellido'].isin(DIST) & D['rol'].str.contains('[DO]')]
pres = set(zip(D['anio'], D['dueno'], D['id']))
E = D[[(a - 1, d, i) not in pres for a, d, i in zip(D['anio'], D['dueno'], D['id'])] & (D['anio'] > 2006)].drop_duplicates(['anio', 'dueno', 'id'])
print(f'PRES eventos {len(E)} | por apellido {E["apellido"].value_counts().to_dict()}', flush=True)
pr = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[3].split(',') if x])
if 'fuente' in pr.columns: pr = pr.sort_values('fuente', ascending=False)
pr = pr.drop_duplicates(['id', 'mes']); pr['m'] = pr['mes'].str[:4].astype(int) * 12 + pr['mes'].str[4:6].astype(int) - 1
P = pr[pr['precio'] > 0].pivot_table(index='m', columns='id', values='precio')
ps = df['_presentado'].astype(str); ok = ps.str.len() >= 7; df = df[ok].copy()
df['mp'] = ps[ok].str[:4].astype(int) * 12 + ps[ok].str[5:7].astype(int) - 1; df['la'] = pd.to_numeric(df['log_activos'], errors='coerce'); df = df.dropna(subset=['la']).sort_values('mp')
fil = []
for a, i, ap in zip(E['anio'], E['id'], E['apellido']):
    m0 = (a + 1) * 12
    if m0 not in P.index or m0 + 12 not in P.index: continue
    r = (P.loc[m0 + 12] / P.loc[m0]).dropna()
    if i not in r.index: continue
    t = df[df['mp'] < m0].drop_duplicates('id', keep='last').set_index('id')['la'].reindex(r.index).dropna(); r = r.reindex(t.index)
    if i not in r.index: continue
    dec = np.minimum((t.rank(pct=True, method='first') * 10).astype(int), 9); med = np.log(r[dec == dec[i]]).mean()
    fil.append((a, ap, float(np.log(r[i]) - med), int(r[i] <= 0.5)))
X = pd.DataFrame(fil, columns=['anio', 'apellido', 'exceso', 'des'])
g = np.random.default_rng(0); b = [g.choice(X['exceso'].values, len(X)).mean() for _ in range(2000)]; lo, hi = np.percentile(b, [2.5, 97.5])
pa = X.groupby('anio')['exceso'].mean()
print(f'CRITERIO75: n {len(X)} | exceso {X["exceso"].mean():+.4f} IC95 [{lo:+.4f},{hi:+.4f}] | años positivos {(pa > 0).sum()} de {len(pa)} {pa.round(3).to_dict()} | desastres {100 * X["des"].mean():.1f}% ->',
      'PASA' if lo > 0 and (pa > 0).mean() >= 0.7 else 'no pasa', flush=True)
print('PRES por apellido:', X.groupby('apellido')['exceso'].agg(['mean', 'size']).round(3).to_dict('index'), flush=True)
