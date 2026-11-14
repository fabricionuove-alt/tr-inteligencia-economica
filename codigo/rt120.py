"""#120: Rt con el filtro de #114. Reglas en notas/11 (#120)."""
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

import json
a = pd.read_csv('sal-cab102/lazy112_filas.csv', dtype={'id': str})[['id', 'ap', 'sim']]
b = pd.DataFrame([{'id': o['id'], 'ap': y, 'sim': o[f's{y}']} for o in map(json.loads, open('sal-cab102/sim114.jsonl')) for y in (2021, 2022) if f's{y}' in o])
s = pd.concat([a, b]).dropna(); s['cambiada'] = s.groupby('ap')['sim'].transform(lambda v: pd.qcut(v.rank(method='first'), 5, labels=False)) == 0
et['r4'] = pd.to_numeric(et['_ret4'], errors='coerce')
d = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'r4']], on=['id', 'anio_presentado'], how='left')
d = d.merge(s.rename(columns={'ap': 'anio_presentado'})[['id', 'anio_presentado', 'cambiada']], on=['id', 'anio_presentado'], how='left'); d['cambiada'] = d['cambiada'].fillna(False).astype(bool)
out = []
for y, z in d.groupby('anio_presentado'):
    z = z.copy(); z['g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2']); z['p'] = z.groupby('g')['gemma'].rank(pct=True)
    top = z[z['p'] > .9]; f = top[~top['cambiada']]; r4t, r4f = top.dropna(subset=['r4']), f.dropna(subset=['r4'])
    out.append({'camada': y, 'elegidas': len(top), 'sacadas': int(top['cambiada'].sum()), 'r1_sin': round(top.r1.mean() * 100, 1), 'r1_con': round(f.r1.mean() * 100, 1),
                'hund4_sin': round((r4t.r4 <= .5).mean() * 100, 1), 'hund4_con': round((r4f.r4 <= .5).mean() * 100, 1), 'n_r4': len(r4t),
                'hund4_sacadas': round((top[top.cambiada].dropna(subset=['r4']).r4 <= .5).mean() * 100, 1)})
o = pd.DataFrame(out); print(o.to_string(index=False))
menos = (o.hund4_con < o.hund4_sin).sum(); dr = (o.r1_con - o.r1_sin).mean()
print(f'RT120 hundidas a 4 años más bajas con filtro en {menos} de {len(o)} camadas; rendimiento a 12 meses con - sin {dr:+.1f} pts -> {"PASA: entra a Rt" if menos >= 5 and dr >= -1 else "no pasa"}')
