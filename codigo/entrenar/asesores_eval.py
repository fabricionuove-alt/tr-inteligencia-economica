"""#82: empresas asesoradas por bancos de familia (Rothschild, Lazard) contra sólo grandes bancos. Uso: python asesores_eval.py filas.csv asesores.csv PRECIOS_CSVS"""
import sys, hashlib, numpy as np, pandas as pd
h = lambda c: hashlib.sha256(('sal-ie-' + str(int(c)).zfill(10)).encode()).hexdigest()[:12]
df = pd.read_csv(sys.argv[1], usecols=lambda c: c in ('id', 'log_activos', '_presentado'), dtype={'id': str}, low_memory=False)
A = pd.read_csv(sys.argv[2], dtype=str).dropna(subset=['cik', 'fecha']); A['id'] = A['cik'].map(h); A['anio'] = A['fecha'].str[:4].astype(int); A['m'] = A['anio'] * 12 + A['fecha'].str[5:7].astype(int) - 1
fam = A[A['banco'].isin(['Rothschild', 'Lazard'])]; ctl = A[A['banco'].isin(['Goldman', 'MorganStanley', 'JPMorgan'])]
claves_fam = set(zip(fam['id'], fam['anio']))
ctl = ctl[[(i, a) not in claves_fam for i, a in zip(ctl['id'], ctl['anio'])]]
fam = fam.sort_values('m').drop_duplicates(['id', 'anio']); ctl = ctl.sort_values('m').drop_duplicates(['id', 'anio'])
print(f'ASES empresas-año: familia {len(fam)} | control {len(ctl)}', flush=True)
pr = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[3].split(',') if x])
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
def medir(E):
    out = []
    for i, a, m in zip(E['id'], E['anio'], E['m']):
        c = ctrl(m + 1)
        if c is None or i not in c[0].index: continue
        r, dec, med = c; out.append((a, float(np.log(r[i]) - med[dec[i]]), int(r[i] <= 0.5)))
    return pd.DataFrame(out, columns=['anio', 'exceso', 'des'])
F, C = medir(fam), medir(ctl)
g = np.random.default_rng(0); b = [g.choice(F['exceso'].values, len(F)).mean() - g.choice(C['exceso'].values, len(C)).mean() for _ in range(2000)]; lo, hi = np.percentile(b, [2.5, 97.5])
pa = F.groupby('anio')['exceso'].mean() - C.groupby('anio')['exceso'].mean(); pa = pa.dropna()
print(f'CRITERIO82: familia n {len(F)} exceso {F["exceso"].mean():+.4f} des {100 * F["des"].mean():.1f}% | control n {len(C)} exceso {C["exceso"].mean():+.4f} des {100 * C["des"].mean():.1f}% | diferencia {F["exceso"].mean() - C["exceso"].mean():+.4f} IC95 [{lo:+.4f},{hi:+.4f}] | años a favor {(pa > 0).sum()} de {len(pa)} ->',
      'PASA' if lo > 0 and (pa > 0).mean() >= 0.7 else 'no pasa', flush=True)
print('ASES por año (familia - control):', pa.round(3).to_dict(), flush=True)
