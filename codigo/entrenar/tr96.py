"""Tr #96: mitad lista de tres secciones (tr87), mitad cohetes (10% de arriba por industria), 10-K 2026, filtro #84. -> datos/tr96_cartera_2026.csv (ticker, peso)"""
import json, hashlib, urllib.request, numpy as np, pandas as pd
from scipy import sparse
D = 'E:/FABRI INFLUENCIA/inteligencia-economica'
P = [(sparse.load_npz(a).tocsr(), np.load(b)) for a, b in (('sal-anon26/sae2a-textos-2026-L12.npz', 'sal-anon26/sae2a-textos-2026-ids.npy'),
     ('sal-lee26/sae2a-textos1A-2026-L12.npz', 'sal-lee26/sae2a-textos1A-2026-ids.npy'), ('sal-lee26/sae2a-textos7-2026-L12.npz', 'sal-lee26/sae2a-textos7-2026-ids.npy'))]
com = sorted(set.intersection(*[set(i) for _, i in P])); pos = [{v: k for k, v in enumerate(i)} for _, i in P]
X = sparse.hstack([x[[p[c] for c in com]] for (x, _), p in zip(P, pos)]).tocsr(); X.data[~np.isfinite(X.data)] = 0
m = np.load('sal-junto3/out/cohete_modelo.npz'); Z = np.log1p(X[:, m['usar']].toarray() / m['med']); Z = (Z - m['mu']) / m['sd']
d = pd.DataFrame({'id': com, 'coh': Z @ m['coef'] + m['b']})
sic = pd.read_csv('sal-sic/sic.csv', dtype={'id': str, 'sic': str}).drop_duplicates('id'); d = d.merge(sic, on='id'); d = d[d['sic'] != '0000'].copy()
d['s3'] = d['sic'].str[:3]; d['s2'] = d['sic'].str[:2]; d['g'] = np.where(d.groupby('s3')['id'].transform('size') >= 10, d['s3'], d['s2'])
d['p'] = d.groupby('g')['coh'].rank(pct=True); A = d[d['p'] > 0.9].copy()
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
tx = json.load(urllib.request.urlopen(urllib.request.Request('https://www.sec.gov/files/company_tickers_exchange.json', headers=UA)))
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]; tk = {}
for cik, nom, t, ex in tx['data']:
    if ex in ('NYSE', 'Nasdaq') and h(cik) not in tk: tk[h(cik)] = t
f84 = pd.read_csv(f'{D}/datos/congelada_84_2026.csv', dtype={'id': str}); fuera = set(f84.loc[f84['venta_directivos'] == 1, 'id'])
A['ticker'] = A['id'].map(tk); A = A[A['ticker'].notna() & ~A['id'].isin(fuera)]
J = pd.read_csv(f'{D}/datos/tr87_cartera_2026.csv', dtype={'id': str})
w = pd.concat([pd.Series(0.5 / len(J), index=J['ticker']), pd.Series(0.5 / len(A), index=A['ticker'])]).groupby(level=0).sum()
out = pd.DataFrame({'ticker': w.index.str.replace('.', '-', regex=False), 'peso': w.values}).sort_values('peso', ascending=False)
out.to_csv(f'{D}/datos/tr96_cartera_2026.csv', index=False)
print('TR96 cohetes', len(A), '| tres secciones', len(J), '| en las dos', len(set(A['ticker']) & set(J['ticker'])), '| total', len(out))
print('TR96 sha256', hashlib.sha256(open(f'{D}/datos/tr96_cartera_2026.csv', 'rb').read()).hexdigest())
