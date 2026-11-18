"""Candidata (no en juego): Tr con Gemma reaprendido con 2013-2021 (#155) sobre los 10-K 2026; mismo armado que tr87/tr146."""
src = open('cadaanio155.py', encoding='utf-8').read(); exec(src[:src.index('D = []')])
import json, hashlib, urllib.request
usar, med, mu, sd, mod = aprender(2021)
P = [(sparse.load_npz(a).tocsr(), np.load(b)) for a, b in (('sal-anon26/sae2a-textos-2026-L12.npz', 'sal-anon26/sae2a-textos-2026-ids.npy'),
     ('sal-lee26/sae2a-textos1A-2026-L12.npz', 'sal-lee26/sae2a-textos1A-2026-ids.npy'), ('sal-lee26/sae2a-textos7-2026-L12.npz', 'sal-lee26/sae2a-textos7-2026-ids.npy'))]
com = sorted(set.intersection(*[set(i) for _, i in P])); pos = [{v: k for k, v in enumerate(i)} for _, i in P]
X = sparse.hstack([x[[p[c] for c in com]] for (x, _), p in zip(P, pos)]).tocsr(); X.data[~np.isfinite(X.data)] = 0
Z = (np.log1p(X[:, usar].toarray() / med) - mu) / sd; d = pd.DataFrame({'id': com, 'anio_presentado': 2026, 'gemma': Z @ mod.coef_ + mod.intercept_})
sic = pd.read_csv('sal-sic/sic.csv', dtype={'id': str, 'sic': str}).drop_duplicates('id'); d = d.merge(sic, on='id', how='left')
d = d[d['sic'].notna() & (d['sic'] != '0000')].copy(); d['s3'] = d['sic'].str[:3]; d['s2'] = d['sic'].str[:2]
d['g'] = np.where(d.groupby('s3')['id'].transform('size') >= 10, d['s3'], d['s2']); d['p'] = d.groupby('g')['gemma'].rank(pct=True); c = d[d['p'] > 0.9].copy()
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
tx = json.load(urllib.request.urlopen(urllib.request.Request('https://www.sec.gov/files/company_tickers_exchange.json', headers=UA))); tk = {}
for cik, nom, t, ex in tx['data']:
    if ex in ('NYSE', 'Nasdaq') and hs(cik) not in tk: tk[hs(cik)] = t
c['ticker'] = c['id'].map(tk); D = 'E:/FABRI INFLUENCIA/inteligencia-economica'
f84 = pd.read_csv(f'{D}/datos/congelada_84_2026.csv', dtype={'id': str}); fuera = set(f84.loc[f84['venta_directivos'] == 1, 'id'])
c = c[c['ticker'].notna() & ~c['id'].isin(fuera)].sort_values('gemma', ascending=False)
c[['id', 'anio_presentado', 'sic', 'gemma', 'p', 'ticker']].to_csv(f'{D}/datos/tr155_candidata_2026.csv', index=False)
v5 = set(pd.read_csv(f'{D}/datos/tr146_cartera_2026.csv')['ticker']); v4 = set(pd.read_csv(f'{D}/datos/tr87_cartera_2026.csv')['ticker'])
print('TR155 candidata', len(c), '| en común con Tr v5 (palabras)', len(v5 & set(c.ticker)), '| con la Gemma vieja (#87)', len(v4 & set(c.ticker)))
print('TR155 sha256', hashlib.sha256(open(f'{D}/datos/tr155_candidata_2026.csv', 'rb').read()).hexdigest())
