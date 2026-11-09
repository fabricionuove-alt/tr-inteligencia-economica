"""Prueba hacia atrás de Rt (notas/15-rt.md): camadas 2017-2022 con _ret1."""
import numpy as np, pandas as pd
from scipy import sparse
m = np.load('sal-junto3/out/gemma_1_1A_7_modelo.npz')
def carga(npz, ids): return sparse.load_npz(npz).tocsr(), np.load(ids)
fil = [pd.read_csv('sal-junto3/out/gemma_1_1A_7_puntaje.csv', dtype={'id': str})]
for y in (2021, 2022):
    P = [carga(f'sal-anon2124/sae2a-textos-{y}-L12.npz', f'sal-anon2124/sae2a-textos-{y}-ids.npy'),
         carga(f'sal-lee{y}/sae2a-textos1A-{y}-L12.npz', f'sal-lee{y}/sae2a-textos1A-{y}-ids.npy'),
         carga(f'sal-lee{y}/sae2a-textos7-{y}-L12.npz', f'sal-lee{y}/sae2a-textos7-{y}-ids.npy')]
    com = sorted(set.intersection(*[set(i) for _, i in P])); pos = [{v: k for k, v in enumerate(i)} for _, i in P]
    X = sparse.hstack([x[[p[c] for c in com]] for (x, _), p in zip(P, pos)]).tocsr(); X.data[~np.isfinite(X.data)] = 0
    Z = np.log1p(X[:, m['usar']].toarray() / m['med']); Z = (Z - m['mu']) / m['sd']
    fil.append(pd.DataFrame({'id': com, 'anio_presentado': y, 'gemma': Z @ m['coef'] + m['b']}))
d = pd.concat(fil); d = d[d.anio_presentado >= 2017]
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['anio_presentado'] = et['anio_presentado'].astype(int); et['r1'] = pd.to_numeric(et['_ret1'], errors='coerce')
d = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'r1']], on=['id', 'anio_presentado']).dropna(subset=['r1', 'sic'])
d = d[d['sic'] != '0000']; d['s3'] = d.sic.str[:3]; d['s2'] = d.sic.str[:2]
out = []
for y, z in d.groupby('anio_presentado'):
    z = z.copy(); z['g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2']); z['p'] = z.groupby('g')['gemma'].rank(pct=True)
    top = z[z['p'] > .9]; w = min(1, len(top) / 365)
    mer = z['r1'].mean(); elegidas = top['r1'].mean() * (1 - .004)
    rt = w * elegidas + (1 - w) * mer
    out.append({'camada': y, 'empresas': len(z), 'elegidas': len(top), 'parte_en_empresas': round(w, 2), 'Rt': round(rt, 3), 'mercado': round(mer, 3), 'Rt-mercado': round(rt - mer, 3),
                'elegidas_solas': round(elegidas, 3), 'mediana_elegidas': round(top['r1'].median(), 3), 'mediana_mercado': round(z['r1'].median(), 3),
                'hundidas_elegidas': round((top['r1'] <= .5).mean(), 3), 'hundidas_mercado': round((z['r1'] <= .5).mean(), 3)})
o = pd.DataFrame(out); print(o.to_string(index=False))
g = (o['Rt-mercado'] > 0).sum(); prom = o['Rt-mercado'].mean()
print(f'RTATRAS gana {g} de {len(o)} camadas, promedio Rt-mercado {prom:+.3f}; 2021-2022 {o[o.camada >= 2021]["Rt-mercado"].round(3).tolist()} -> {"PASA" if g >= 4 and prom > 0 else "no pasa"}')
