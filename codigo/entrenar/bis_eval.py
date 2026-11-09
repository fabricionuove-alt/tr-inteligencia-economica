"""#90: lo nuevo de cada mes en los discursos de banqueros centrales contra las empresas. python bis_eval.py filas.csv PRECIOS_CSVS DIR_VECTORES_EMPRESAS DIR_BIS etiquetas.csv"""
import sys, glob, numpy as np, pandas as pd
from scipy import sparse
fil, PRS, VE, VB, ET = sys.argv[1:6]
M = lambda s: int(s[:4]) * 12 + int(s[4:6]) - 1
# lo nuevo de cada mes
ib = np.load(glob.glob(f'{VB}/**/sae2a-bis-ids.npy', recursive=True)[0]); XB = sparse.load_npz(glob.glob(f'{VB}/**/sae2a-bis-L12.npz', recursive=True)[0]).toarray()
ok = np.isfinite(XB).all(1); XB = np.log1p(np.clip(np.nan_to_num(XB), 0, None)); mb = np.array([M(i.split('|')[0]) for i in ib])
V = {m: XB[(mb == m) & ok].mean(0) for m in np.unique(mb) if ((mb == m) & ok).sum() >= 10}
def nuevo(m):
    p = [V[k] for k in range(m - 12, m) if k in V]
    return V[m] - np.mean(p, 0) if m in V and len(p) >= 9 else None
print('BIS meses con vector', len(V), 'discursos', ok.sum(), flush=True)
# empresas: vector de su 10-K y mes de presentación
df = pd.read_csv(fil, usecols=lambda c: c in ('id', 'log_activos', '_presentado'), dtype={'id': str}, low_memory=False)
ps = df['_presentado'].astype(str); df = df[ps.str.len() >= 7].copy(); df['mp'] = df['_presentado'].astype(str).str[:4].astype(int) * 12 + df['_presentado'].astype(str).str[5:7].astype(int) - 1
df['ap'] = df['mp'] // 12; df['la'] = pd.to_numeric(df['log_activos'], errors='coerce'); df = df.drop_duplicates(['id', 'ap'])
et = pd.read_csv(ET, dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['ap'] = et['anio_presentado'].astype(int); et = et.drop_duplicates(['id', 'ap'])[['id', 'ap', 'sic']]
Zs, F = [], []
for y in range(2013, 2021):
    i = np.load(glob.glob(f'{VE}/**/sae2a-{y}-ids.npy', recursive=True)[0]); Z = sparse.load_npz(glob.glob(f'{VE}/**/sae2a-{y}-L12.npz', recursive=True)[0]).toarray()
    b = ~np.isfinite(Z).all(1); Z = np.log1p(np.clip(np.nan_to_num(Z), 0, None)); Z = Z - Z[~b].mean(0); Z /= (np.linalg.norm(Z, axis=1, keepdims=True) + 1e-9)
    Zs.append(Z[~b]); F.append(pd.DataFrame({'id': i[~b], 'ap': y}))
Z = np.vstack(Zs); F = pd.concat(F, ignore_index=True).reset_index().merge(df[['id', 'ap', 'mp', 'la']], on=['id', 'ap'], how='inner').merge(et, on=['id', 'ap'], how='left')
print('BIS empresas-año con vector y fecha', len(F), flush=True)
# precios
pr = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in PRS.split(',') if x])
if 'fuente' in pr.columns: pr = pr.sort_values('fuente', ascending=False)
pr = pr.drop_duplicates(['id', 'mes']); pr['m'] = pr['mes'].map(M); P = pr[pr['precio'] > 0].pivot_table(index='m', columns='id', values='precio').sort_index()
R = P / P.shift(1); SPL = np.array([1/2, 1/3, 1/4, 1/5, 1/10, 2, 3, 4, 5, 10])
salto = pd.DataFrame(np.any(np.abs(R.values[..., None] / SPL - 1) < 0.03, axis=-1), index=R.index, columns=R.columns)
def mes(m, nv, ctrl):
    if nv is None or m + 13 not in P.index or m + 1 not in P.index: return None
    a = F[(F['mp'] < m) & (F['mp'] >= m - 15)].sort_values('mp').drop_duplicates('id', keep='last')
    a = a[a['id'].isin(P.columns)].copy()
    r = (P.loc[m + 13, a['id']].values / P.loc[m + 1, a['id']].values); s = salto.loc[m + 2:m + 13, a['id']].any(axis=0).values
    a['r'] = r; a['s'] = (Z[a['index'].values] @ nv) / (np.linalg.norm(nv) + 1e-9); a = a[np.isfinite(a['r']) & (a['r'] > 0) & ~s & a['la'].notna()]
    a['ter'] = pd.qcut(a['la'].rank(method='first'), 3, labels=False); a['sic3'] = a['sic'].astype(str).str[:3]
    a['lr'] = np.log(a['r'].clip(0.01, 20)); g = ['ter'] if ctrl == 'tam' else ['ter', 'sic3']
    if ctrl != 'tam': a = a[a['sic'].notna()]; a = a[a.groupby(g)['id'].transform('size') >= 5]
    a['ex'] = a['lr'] - a.groupby(g)['lr'].transform('median'); a['p'] = a.groupby(g)['s'].rank(pct=True)
    return a.loc[a['p'] > 0.9, 'ex'].mean() - a.loc[a['p'] <= 0.2, 'ex'].mean(), a
def nw(x, L=12):
    x = np.asarray(x) - np.mean(x); n = len(x); v = x @ x / n
    for l in range(1, L + 1): v += 2 * (1 - l / (L + 1)) * (x[l:] @ x[:-l]) / n
    return np.sqrt(v / n)
RES = {}
for nom, des, ctrl in (('principal', 0, 'tam'), ('placebo', 48, 'tam'), ('industria', 0, 'sic'), ('placebo_ind', 48, 'sic')):
    s = {}
    for m in range(2013 * 12 + 6, 2021 * 12):
        o = mes(m, nuevo(m - des), ctrl)
        if o is not None and np.isfinite(o[0]): s[m] = o[0]
    s = pd.Series(s); e, c = s[s.index < 2017 * 12], s[s.index >= 2017 * 12]
    t = c.mean() / nw(c.values); RES[nom] = (e.mean(), c.mean(), t, len(c))
    anual = c.groupby(c.index // 12).mean().round(3).to_dict()
    print(f'BIS {nom:12s} exploración {e.mean():+.4f} ({len(e)} meses) | confirmación {c.mean():+.4f} t_NW {t:+.2f} ({len(c)} meses) | por año {anual}', flush=True)
e, c, t, _ = RES['principal']; pasa = c >= 0.03 and t >= 2 and e > 0 and c > RES['placebo'][1]
print(f'CRITERIO90 confirmación {c:+.4f} t {t:+.2f} exploración {e:+.4f} placebo {RES["placebo"][1]:+.4f} -> {"PASA" if pasa else "no pasa"}', flush=True)
