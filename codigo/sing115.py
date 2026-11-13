"""#115: singularidad de la sección 1 del 10-K contra su rubro, y su cambio. Reglas en notas/11 (#115)."""
import hashlib, numpy as np, pandas as pd, scipy.sparse as sp
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; D = f'{B}/fuentes/edgar-corpus'; rng = np.random.default_rng(0)
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int); et = et.drop_duplicates(['id', 'ap'])
sic = {(i, a): s for i, a, s in zip(et['id'], et['ap'], et['sic']) if isinstance(s, str)}
filas = []
for y in range(2009, 2021):
    z = np.load(f'{D}/vec_{y}.npz'); M = sp.load_npz(f'{D}/m1_{y}.npz').tocsr(); L = z['l1']
    vistos = {}; 
    for i, c in enumerate(z['ciks']):
        if c in vistos or L[i] <= 500: continue
        s = sic.get((hs(c), y))
        if s: vistos[c] = (i, s[:2])
    df = pd.DataFrame([(c, i, s2) for c, (i, s2) in vistos.items()], columns=['cik', 'i', 's2'])
    for s2, g in df.groupby('s2'):
        if len(g) < 10: continue
        V = M[g['i'].values]; S = np.asarray(V.sum(axis=0)).ravel(); SS = S @ S
        vS = V @ S                                   # v·S
        cos = (vS - 1) / np.sqrt(np.maximum(SS - 2 * vS + 1, 1e-12))
        for c, sg in zip(g['cik'], 1 - cos): filas.append({'id': hs(c), 'ap': y, 'sing': sg})
    print(y, len(df), flush=True)
s = pd.DataFrame(filas).sort_values(['id', 'ap'])
s['prev'] = s.groupby('id')['sing'].shift(); s['prev_ap'] = s.groupby('id')['ap'].shift()
s = s[s['prev_ap'] == s['ap'] - 1].copy(); s['d'] = s['sing'] - s['prev']
x = s.merge(et[['id', 'ap', 'sic', 'tam', '_ret4']], on=['id', 'ap']); x['r'] = pd.to_numeric(x['_ret4'], errors='coerce')
x = x.dropna(subset=['r', 'sic', 'tam']).copy()
x['sic3'] = x['sic'].str[:3]; x['sic2'] = x['sic'].str[:2]; x['dec'] = np.minimum((x['tam'] * 10).astype(int), 9); g = ['ap', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy()
x['ex'] = (x['r'] - x.groupby(g)['r'].transform('median')) * 100; x['h'] = (x['r'] <= .5).astype(float)
print('con rendimiento', len(x), x.groupby('ap').size().to_dict(), flush=True)
def tramo(z, col, nomb):
    z = z.copy(); z['q'] = z.groupby('ap')[col].transform(lambda v: pd.qcut(v.rank(method='first'), 5, labels=False))
    z = z[z['q'].isin([0, 4])].copy(); lab = (z['q'] == 4).values; ex = z['ex'].values
    obs = ex[lab].mean() - ex[~lab].mean(); gid = z.groupby(['ap', 'sic2']).ngroup().values
    grupos = [np.where(gid == k)[0] for k in np.unique(gid)]; perm = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in grupos: l2[ii] = rng.permutation(l2[ii])
        perm.append(ex[l2].mean() - ex[~l2].mean())
    p = ((np.array(perm) >= obs).sum() + 1) / 2001; h = z['h'].values
    print(f'SG115 {nomb:24s} {col:4s} n {lab.sum():5d}/{(~lab).sum():5d} arriba {ex[lab].mean():+.1f} abajo {ex[~lab].mean():+.1f} dif {obs:+.1f} p {p:.4f} | medianas {np.median(ex[lab]):+.1f}/{np.median(ex[~lab]):+.1f} | hundidas {h[lab].mean()*100:.1f}/{h[~lab].mean()*100:.1f}', flush=True)
    return obs, p
T = {'exploración 2010-2016': x[(x.ap >= 2010) & (x.ap <= 2016)], 'confirmación 2017-2020': x[(x.ap >= 2017) & (x.ap <= 2020)]}
res = {k: tramo(v, 'd', k) for k, v in T.items()}
for k, v in T.items(): tramo(v, 'sing', k)
for y in range(2010, 2021): tramo(x[x.ap == y], 'd', f'año {y}')
e = res['exploración 2010-2016'][0]; c, pc = res['confirmación 2017-2020']
print(f'CRITERIO115 confirmación {c:+.1f} pts (p {pc:.4f}) exploración {e:+.1f} -> {"PASA (falta 2021-2022)" if c >= 5 and pc < .05 and e > 0 else "no pasa"}', flush=True)
x[['id', 'ap', 'sing', 'd', 'r', 'ex', 'h']].to_csv(f'{B}/entrenar/sal-cab102/sing115_filas.csv', index=False)
