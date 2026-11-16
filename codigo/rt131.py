"""#131: Rt sin las empresas en declive (#130). Reglas en notas/11 (#131)."""
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

import json, hashlib
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
C = {'O': 'NetCashProvidedByUsedInOperatingActivities', 'I': 'NetCashProvidedByUsedInInvestingActivities', 'F': 'NetCashProvidedByUsedInFinancingActivities'}
dec = []
for y in range(2015, 2022):
    v = {}
    for k, c in C.items():
        for o in json.load(open(f'../fuentes/frames/{c}_CY{y}.json'))['data']: v.setdefault(o['cik'], {})[k] = o['val']
    for cik, z in v.items():
        if len(z) == 3 and z['O'] <= 0 and z['I'] > 0: dec.append((hs(cik), y + 1))
dec = set(dec)
et['r4'] = pd.to_numeric(et['_ret4'], errors='coerce')
d = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'r4']], on=['id', 'anio_presentado'], how='left')
d['cambiada'] = [(i, y) in dec for i, y in zip(d['id'], d['anio_presentado'])]
out = []
for y, z in d.groupby('anio_presentado'):
    z = z.copy(); z['g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2']); z['p'] = z.groupby('g')['gemma'].rank(pct=True)
    top = z[z['p'] > .9]; f = top[~top['cambiada']]; r4t, r4f = top.dropna(subset=['r4']), f.dropna(subset=['r4'])
    out.append({'camada': y, 'elegidas': len(top), 'sacadas': int(top['cambiada'].sum()), 'r1_sin': round(top.r1.mean() * 100, 1), 'r1_con': round(f.r1.mean() * 100, 1),
                'hund4_sin': round((r4t.r4 <= .5).mean() * 100, 1), 'hund4_con': round((r4f.r4 <= .5).mean() * 100, 1), 'n_r4': len(r4t),
                'hund4_sacadas': round((top[top.cambiada].dropna(subset=['r4']).r4 <= .5).mean() * 100, 1)})
o = pd.DataFrame(out); print(o.to_string(index=False))
menos = (o.hund4_con < o.hund4_sin).sum(); dr = (o.r1_con - o.r1_sin).mean()
print(f'RT131 hundidas a 4 años más bajas con filtro en {menos} de {len(o)} camadas; rendimiento a 12 meses con - sin {dr:+.1f} pts -> {"muestra insuficiente" if o.sacadas.sum() < 30 else ("PASA: entra a Rt" if menos >= 5 and dr >= -1 else "no pasa")}')
