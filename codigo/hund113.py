"""#113: ¿las que reescriben mucho su 10-K se hunden más que sus pares de rubro y tamaño? Reglas en notas/11 (#113)."""
import numpy as np, pandas as pd
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
s = pd.read_csv(f'{B}/entrenar/sal-cab102/lazy112_filas.csv', dtype={'id': str}).dropna(subset=['sim', '_ret4'])
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int); et = et.drop_duplicates(['id', 'ap'])[['id', 'ap', 'sic', 'tam']]
x = s.merge(et, on=['id', 'ap']).dropna(subset=['sic', 'tam']).copy()
x['q'] = x.groupby('ap')['sim'].transform(lambda v: pd.qcut(v.rank(method='first'), 5, labels=False))
x['sic3'] = x['sic'].str[:3]; x['dec'] = np.minimum((x['tam'] * 10).astype(int), 9); g = ['ap', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy(); x['h'] = (x['_ret4'] <= .5).astype(float); x['r'] = x['_ret4']
def tramo(z, lado, nomb):
    z = z.copy(); z['sen'] = z['q'] == lado
    z['hp'] = z['h'].where(~z['sen']).groupby([z[c] for c in g]).transform('mean')
    z['med'] = z['r'].where(~z['sen']).groupby([z[c] for c in g]).transform('median')
    z = z.dropna(subset=['hp']); z['d'] = z['h'] - z['hp']; z['ex'] = (z['r'] - z['med']) * 100
    lab = z['sen'].values; d = z['d'].values; gid = z.groupby(g).ngroup().values
    idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
    obs = d[lab].mean() * 100; perm = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        perm.append(d[l2].mean() * 100)
    perm = np.array(perm); p = ((perm >= obs).sum() + 1) / 2001 if lado == 0 else ((perm <= obs).sum() + 1) / 2001
    f = z[lab]
    print(f'HU113 {nomb:24s} {"cambiadas" if lado == 0 else "quietas  "} n {lab.sum():5d} hundidas {f.h.mean()*100:5.1f} esperado {f.hp.mean()*100:5.1f} dif {obs:+.1f} p {p:.4f} | exceso medio {f.ex.mean():+.1f} mediano {f.ex.median():+.1f}', flush=True)
    return obs, p
T = {'exploración 2010-2016': x[(x.ap >= 2010) & (x.ap <= 2016)], 'confirmación 2017-2020': x[(x.ap >= 2017) & (x.ap <= 2020)]}
res = {k: tramo(v, 0, k) for k, v in T.items()}
for k, v in T.items(): tramo(v, 4, k)
e = res['exploración 2010-2016'][0]; c, pc = res['confirmación 2017-2020']
print(f'CRITERIO113 confirmación {c:+.1f} pts (p {pc:.4f}) exploración {e:+.1f} -> {"PASA" if c >= 3 and pc < .05 and e > 0 else "no pasa"}', flush=True)
