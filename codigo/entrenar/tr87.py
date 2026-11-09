"""Tr v4 (#87): puntaje de Gemma con las tres secciones (negocio + riesgos + dirección) en los 10-K de 2026, cartera #69 y filtro #84.
Uso: python tr87.py  -> datos/tr87_cartera_2026.csv"""
import json, hashlib, urllib.request, numpy as np, pandas as pd
from scipy import sparse
D = 'E:/FABRI INFLUENCIA/inteligencia-economica'
def carga(npz, ids): return sparse.load_npz(npz).tocsr(), np.load(ids)
P = [carga('sal-anon26/sae2a-textos-2026-L12.npz', 'sal-anon26/sae2a-textos-2026-ids.npy'),
     carga('sal-lee26/sae2a-textos1A-2026-L12.npz', 'sal-lee26/sae2a-textos1A-2026-ids.npy'),
     carga('sal-lee26/sae2a-textos7-2026-L12.npz', 'sal-lee26/sae2a-textos7-2026-ids.npy')]
com = sorted(set.intersection(*[set(i) for _, i in P])); pos = [{v: k for k, v in enumerate(i)} for _, i in P]
X = sparse.hstack([x[[p[c] for c in com]] for (x, _), p in zip(P, pos)]).tocsr(); X.data[~np.isfinite(X.data)] = 0
m = np.load('sal-junto3/out/gemma_1_1A_7_modelo.npz')                       # congelado: aprendido sólo con 2013-2016
Z = np.log1p(X[:, m['usar']].toarray() / m['med']); Z = (Z - m['mu']) / m['sd']
d = pd.DataFrame({'id': com, 'anio_presentado': 2026, 'gemma': Z @ m['coef'] + m['b']})
print('TR87 empresas con las tres secciones', len(d), flush=True)
sic = pd.read_csv('sal-sic/sic.csv', dtype={'id': str, 'sic': str}).drop_duplicates('id'); d = d.merge(sic, on='id', how='left')
d = d[d['sic'].notna() & (d['sic'] != '0000')].copy(); d['s3'] = d['sic'].str[:3]; d['s2'] = d['sic'].str[:2]
d['g'] = np.where(d.groupby('s3')['id'].transform('size') >= 10, d['s3'], d['s2'])
d['p'] = d.groupby('g')['gemma'].rank(pct=True); c = d[d['p'] > 0.9].copy()
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
tx = json.load(urllib.request.urlopen(urllib.request.Request('https://www.sec.gov/files/company_tickers_exchange.json', headers=UA)))
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
tk = {}
for cik, nom, t, ex in tx['data']:
    if ex in ('NYSE', 'Nasdaq') and h(cik) not in tk: tk[h(cik)] = t
c['ticker'] = c['id'].map(tk)
f84 = pd.read_csv(f'{D}/datos/congelada_84_2026.csv', dtype={'id': str}); fuera = set(f84.loc[f84['venta_directivos'] == 1, 'id'])
print('TR87 cartera', len(c), '| con ticker', c['ticker'].notna().sum(), '| fuera por #84', c['id'].isin(fuera).sum(), flush=True)
c = c[c['ticker'].notna() & ~c['id'].isin(fuera)].sort_values('gemma', ascending=False)
c[['id', 'anio_presentado', 'sic', 'gemma', 'p', 'ticker']].to_csv(f'{D}/datos/tr87_cartera_2026.csv', index=False)
viejo = set(pd.read_csv(f'{D}/datos/tr_gemma84_cartera_2026.csv')['ticker'].dropna())
print('TR87 final', len(c), '| en común con la lista en juego', len(viejo & set(c['ticker'])), flush=True)
print('TR87 sha256', hashlib.sha256(open(f'{D}/datos/tr87_cartera_2026.csv', 'rb').read()).hexdigest())
