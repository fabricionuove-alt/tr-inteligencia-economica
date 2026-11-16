"""#137: puntaje parcial de Gemma por sección (1, 1A, 7), 2017-2020, top 10% por industria vs pares en hundidas a 4 años."""
import numpy as np, pandas as pd
from scipy import sparse
rng = np.random.default_rng(0)
m = np.load('sal-junto3/out/gemma_1_1A_7_modelo.npz'); u = m['usar']; sec = u // 16384
F = []
for y in range(2017, 2021):
    X = sparse.load_npz(f'sal-junto3/sae2aT-{y}-L12.npz').tocsr(); ids = np.load(f'sal-junto3/sae2aT-{y}-ids.npy', allow_pickle=True)
    X.data[~np.isfinite(X.data)] = 0
    Z = np.log1p(X[:, u].toarray() / m['med']); Z = (Z - m['mu']) / m['sd']
    f = pd.DataFrame({'id': ids.astype(str), 'anio_presentado': y, 'total': Z @ m['coef'] + m['b']})
    for k, n in enumerate(['negocio', 'riesgos', 'direccion']): f[n] = Z[:, sec == k] @ m['coef'][sec == k]
    F.append(f)
d = pd.concat(F)
ref = pd.read_csv('sal-junto3/out/gemma_1_1A_7_puntaje.csv', dtype={'id': str})
chk = d.merge(ref, on=['id', 'anio_presentado']); print('control contra el puntaje guardado: corr', round(np.corrcoef(chk.total, chk.gemma)[0, 1], 4), len(chk), flush=True)
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et.anio_presentado.astype(int)
et['r4'] = pd.to_numeric(et._ret4, errors='coerce')
x = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'tam', 'r4']], on=['id', 'anio_presentado']).dropna(subset=['sic', 'tam', 'r4'])
x = x[x.sic != '0000'].copy(); x['s3'] = x.sic.str[:3]; x['s2'] = x.sic.str[:2]; x['dec'] = np.minimum((x.tam * 10).astype(int), 9); x['h'] = (x.r4 <= .5).astype(float)
x['g'] = ''
for y, z in x.groupby('anio_presentado'): x.loc[z.index, 'g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2'])
gg = ['anio_presentado', 's3', 'dec']; x = x[x.groupby(gg)['id'].transform('size') >= 5].copy()
res = {}
for n in ['total', 'negocio', 'riesgos', 'direccion']:
    top = (x.groupby(['anio_presentado', 'g'])[n].rank(pct=True) > .9).values
    z = x.copy(); z['sen'] = top; z['hp'] = z['h'].where(~z.sen).groupby([z[c] for c in gg]).transform('mean'); z = z.dropna(subset=['hp'])
    lab = z.sen.values; dd = (z.h - z.hp).values; gid = z.groupby(gg).ngroup().values
    idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
    obs = dd[lab].mean() * 100; P = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        P.append(dd[l2].mean() * 100)
    p = ((np.array(P) <= obs).sum() + 1) / 2001; s = z[lab]; res[n] = (obs, p)
    anios = ' '.join(f'{y}:{(s[s.anio_presentado==y].h.mean()-s[s.anio_presentado==y].hp.mean())*100:+.1f}' for y in range(2017, 2021))
    print(f'SE137 {n:9s} n {lab.sum():4d} hundidas {s.h.mean()*100:5.1f} esperado {s.hp.mean()*100:5.1f} dif {obs:+.1f} p {p:.4f} | {anios}', flush=True)
lleva = [n for n in ['negocio', 'riesgos', 'direccion'] if res[n][0] <= -3 and res[n][1] < .05]
print('CRITERIO137 llevan la ventaja:', lleva if lleva else 'ninguna sola')
print('correlacion entre parciales:'); print(x[['negocio', 'riesgos', 'direccion']].corr().round(2))
