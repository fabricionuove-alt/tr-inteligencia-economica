"""#71: ¿cuando una dinastía entra o sube fuerte en una empresa, a la empresa le va mejor? Uso: python familias_eval.py filas.csv FAM13F_CSVS PRECIOS_CSVS"""
import sys, json, numpy as np, pandas as pd
df = pd.read_csv(sys.argv[1], usecols=lambda c: c in ('id', 'anio', 'log_activos', '_presentado'), dtype={'id': str}, low_memory=False)
F = pd.concat([pd.read_csv(x, dtype={'id': str, 'periodo': str}) for x in sys.argv[2].split(',') if x]).drop_duplicates(['periodo', 'familia', 'id'])
pr = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[3].split(',') if x])
if 'fuente' in pr.columns: pr = pr.sort_values('fuente', ascending=False)
pr = pr.drop_duplicates(['id', 'mes']); pr['m'] = pr['mes'].str[:4].astype(int) * 12 + pr['mes'].str[4:6].astype(int) - 1
P = pr[pr['precio'] > 0].pivot_table(index='m', columns='id', values='precio')
pres = df['_presentado'].astype(str); ok = pres.str.len() >= 7; df = df[ok].copy()
df['mp'] = pres[ok].str[:4].astype(int) * 12 + pres[ok].str[5:7].astype(int) - 1; df['la'] = pd.to_numeric(df['log_activos'], errors='coerce'); df = df.dropna(subset=['la']).sort_values('mp')
F['m'] = F['periodo'].str[:4].astype(int) * 12 + F['periodo'].str[4:6].astype(int) - 1
ev = []
for fam, g in F.groupby('familia'):
    tr = sorted(g['m'].unique()); t = g.pivot_table(index='id', columns='m', values='acciones', aggfunc='sum').fillna(0)
    for a, b in zip(tr, tr[1:]):
        if b - a != 3: continue
        x0, x1 = t[a], t[b]; e = t.index[(x1 > 0) & ((x0 == 0) | (x1 >= 1.5 * x0))]
        ev += [(fam, i, b + 2, int(x0[i] == 0)) for i in e]
E = pd.DataFrame(ev, columns=['familia', 'id', 'm0', 'nueva'])
print(f'FAM eventos: {len(E)} | por familia {E["familia"].value_counts().to_dict()}', flush=True)
cache = {}
def control(m0):
    if m0 in cache: return cache[m0]
    if m0 not in P.index or m0 + 12 not in P.index: cache[m0] = None; return None
    r = (P.loc[m0 + 12] / P.loc[m0]).dropna(); t = df[df['mp'] < m0].drop_duplicates('id', keep='last').set_index('id')['la'].reindex(r.index).dropna()
    r = r.reindex(t.index); dec = np.minimum((t.rank(pct=True, method='first') * 10).astype(int), 9); cache[m0] = (r, dec, np.log(r).groupby(dec).mean()); return cache[m0]
fil = []
for f, i, m0, nueva in E.itertuples(index=False):
    c = control(m0)
    if c is None or i not in c[0].index: continue
    r, dec, med = c
    fil.append((f, m0 // 12, nueva, float(np.log(r[i]) - med[dec[i]]), int(r[i] <= 0.5), float((r[dec == dec[i]] <= 0.5).mean())))
X = pd.DataFrame(fil, columns=['familia', 'anio', 'nueva', 'exceso', 'des', 'des_ctrl'])
DUDOSOS = set()   # la versión sin dudosos se arma aparte (el nombre del declarante no viaja hasta acá)
g = np.random.default_rng(0); res = {}
for nombre, x in (('todas', X), ('sin_cargill_mirabaud', X[~X['familia'].isin(['cargill', 'mirabaud'])])):
    b = [g.choice(x['exceso'].values, len(x)).mean() for _ in range(2000)]; lo, hi = np.percentile(b, [2.5, 97.5])
    pa = x.groupby('anio')['exceso'].mean(); pos = (pa > 0).mean()
    res[nombre] = {'n': len(x), 'exceso': round(float(x['exceso'].mean()), 4), 'ic95': [round(float(lo), 4), round(float(hi), 4)], 'por_anio': pa.round(4).to_dict(),
                   'desastres': round(100 * float(x['des'].mean()), 2), 'des_ctrl': round(100 * float(x['des_ctrl'].mean()), 2), 'pasa': bool(lo > 0 and pos >= 0.7)}
    print(f'CRITERIO71 {nombre}: n {len(x)} | exceso {res[nombre]["exceso"]:+.4f} IC95 {res[nombre]["ic95"]} | años positivos {(pa > 0).sum()} de {len(pa)} {pa.round(3).to_dict()} | desastres {res[nombre]["desastres"]}% vs {res[nombre]["des_ctrl"]}% -> {"PASA" if res[nombre]["pasa"] else "no pasa"}', flush=True)
print('FAM por familia:', X.groupby('familia')['exceso'].agg(['mean', 'size']).round(4).to_dict('index'), flush=True)
print('FAM nueva vs aumento:', X.groupby('nueva')['exceso'].agg(['mean', 'size']).round(4).to_dict('index'), flush=True)
json.dump(res, open('familias.json', 'w'), indent=1, default=str)
