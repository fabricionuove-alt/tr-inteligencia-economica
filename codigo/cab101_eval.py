"""#101: empresas empujadas por las embajadas (cables BEXP) contra las otras nombradas, a 48 meses. python cab101_eval.py menciones.csv precios.csv etiquetas.csv"""
import sys, numpy as np, pandas as pd
MEN, PR, ET = sys.argv[1:4]
rng = np.random.default_rng(0)
m = pd.read_csv(MEN, dtype={'id': str}); m = m[(m['anio'] >= 2005) & (m['anio'] <= 2009)]
g = m.groupby(['id', 'anio']).agg(bexp=('bexp', 'max'), cables=('cables', 'sum')).reset_index()
et = pd.read_csv(ET, dtype={'id': str, 'sic': str}).dropna(subset=['sic'])
sic = et.groupby('id')['sic'].agg(lambda s: s.mode().iloc[0]).str[:2]
pr = pd.read_csv(PR, dtype={'id': str, 'mes': str}); pr = pr[pr['mes'].str.match(r'^20[01]\d(0[1-9]|1[0-2])$') & (pr['precio'] > 0)]
pr['m'] = pr['mes'].str[:4].astype(int) * 12 + pr['mes'].str[4:].astype(int) - 1
P = pr.drop_duplicates(['id', 'm']).pivot(index='m', columns='id', values='precio').sort_index()
R = P / P.shift(1); SPL = np.array([1/2, 1/3, 1/4, 1/5, 1/10, 2, 3, 4, 5, 10])
salto = pd.DataFrame(np.any(np.abs(R.values[..., None] / SPL - 1) < 0.03, axis=-1), index=R.index, columns=R.columns)
def ret(ids, y):
    a, b = (y + 1) * 12, (y + 5) * 12          # fin de enero Y+1 -> fin de enero Y+5
    ids = [i for i in ids if i in P.columns]
    if a not in P.index or b not in P.index: return pd.Series(dtype=float)
    r = P.loc[b, ids] / P.loc[a, ids]; s = salto.loc[a + 1:b, ids].any(axis=0)
    return r[np.isfinite(r) & (r > 0) & ~s]
filas = []
for y in range(2005, 2010):
    x = g[g['anio'] == y].copy(); x['sic2'] = x['id'].map(sic); x = x.dropna(subset=['sic2'])
    r = ret(x['id'], y); x = x[x['id'].isin(r.index)].copy(); x['r'] = x['id'].map(r)
    todos = pd.DataFrame({'id': sic.index, 'sic2': sic.values}); rt = ret(todos['id'], y); todos = todos[todos['id'].isin(rt.index)].copy(); todos['lr'] = np.log(todos['id'].map(rt).clip(0.01, 50))
    x['lr'] = np.log(x['r'].clip(0.01, 50)); x['anio'] = y
    x['med_ctrl'] = x['sic2'].map(x[x['bexp'] == 0].groupby('sic2')['lr'].median()); x['med_todos'] = x['sic2'].map(todos.groupby('sic2')['lr'].median())
    filas.append(x)
d = pd.concat(filas); d = d.dropna(subset=['med_ctrl']); d = d[d.groupby(['anio', 'sic2'])['bexp'].transform('sum') > 0]
d['ex'] = d['lr'] - d['med_ctrl']; d['ex_t'] = d['lr'] - d['med_todos']
def dif(z): return z[z['bexp'] == 1].groupby('anio')['ex'].mean() - z[z['bexp'] == 0].groupby('anio')['ex'].mean()
por = dif(d); obs = d.loc[d['bexp'] == 1, 'ex'].mean() - d.loc[d['bexp'] == 0, 'ex'].mean()
emp = d[d['bexp'] == 1]; ctl = d[d['bexp'] == 0]
print(f'CAB101 empresas-año: empujadas {len(emp)} / control {len(ctl)}; por año {d.groupby(["anio", "bexp"]).size().unstack().to_dict()}', flush=True)
perm = []
for _ in range(2000):
    z = d.copy(); z['bexp'] = z.groupby(['anio', 'sic2'])['bexp'].transform(lambda s: rng.permutation(s.values)); perm.append(z.loc[z['bexp'] == 1, 'ex'].mean() - z.loc[z['bexp'] == 0, 'ex'].mean())
p = (np.sum(np.array(perm) >= obs) + 1) / (len(perm) + 1)
ex_emp = emp.groupby('anio')['ex'].mean()
print(f'CAB101 exceso de las empujadas contra la mediana del control (mismo SIC2): {ex_emp.round(3).to_dict()} media {emp["ex"].mean():+.3f}', flush=True)
print(f'CAB101 empujadas − control: por año {por.round(3).to_dict()} total {obs:+.3f} permutación p {p:.4f}', flush=True)
print(f'CAB101 contra todas las del SIC2: empujadas {emp["ex_t"].mean():+.3f} control {ctl["ex_t"].mean():+.3f}', flush=True)
print(f'CAB101 hundidas (≤ ×0,5): empujadas {(emp["r"] <= .5).mean():.3f} control {(ctl["r"] <= .5).mean():.3f}', flush=True)
print(f'CAB101 rendimiento mediano ×: empujadas {emp["r"].median():.3f} control {ctl["r"].median():.3f}', flush=True)
pasa = emp['ex'].mean() >= 0.10 and (ex_emp > 0).sum() >= 4 and p < 0.05
print(f'CRITERIO101 exceso {emp["ex"].mean():+.3f}, años positivos {(ex_emp > 0).sum()} de {len(ex_emp)}, p {p:.4f} -> {"PASA" if pasa else "no pasa"}', flush=True)
d.to_csv('cab101_filas.csv', index=False)
