"""Tr v5 (#146): modelo de palabras firme (alfa 10.000, columnas >= 2%, aprendido 2013-2016) sobre la descripción del negocio
de los 10-K 2026 sacada con edgar-crawler; 10% de arriba por industria, a partes iguales, filtro #84.
Uso: python tr146.py  -> datos/tr146_cartera_2026.csv"""
import sys, json, hashlib, urllib.request; sys.argv = ['x', 'A']
exec(open('robusto146.py', encoding='utf-8').read().split("CR = [json.loads")[0])
e = json.load(open('sal-cab102/eleccion146.json')); cols, f = armar(e['dmin']); r = Ridge(alpha=e['alfa']).fit(f(Xa), ya)
D = 'E:/FABRI INFLUENCIA/inteligencia-economica'
T = [json.loads(l) for l in open(f'{D}/fuentes/tr146/sec1.jsonl', encoding='utf-8')]
T = [(hs(o['cik']), o['2026'], o['cik']) for o in T if len((o.get('2026') or '').split()) >= 300]
d = pd.DataFrame({'id': [a for a, _, _ in T], 'cik': [k for _, _, k in T], 'anio_presentado': 2026, 'pal': r.predict(f(hvl.transform([t for _, t, _ in T])))}).drop_duplicates('id')
print('TR146 empresas con descripción', len(d), flush=True)
sic = pd.read_csv('sal-sic/sic.csv', dtype={'id': str, 'sic': str}).drop_duplicates('id'); d = d.merge(sic, on='id', how='left')
d = d[d['sic'].notna() & (d['sic'] != '0000')].copy(); d['s3'] = d['sic'].str[:3]; d['s2'] = d['sic'].str[:2]
d['g'] = np.where(d.groupby('s3')['id'].transform('size') >= 10, d['s3'], d['s2'])
d['p'] = d.groupby('g')['pal'].rank(pct=True); c = d[d['p'] > 0.9].copy()
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
tx = json.load(urllib.request.urlopen(urllib.request.Request('https://www.sec.gov/files/company_tickers_exchange.json', headers=UA)))
tk = {}
for cik, nom, t, ex in tx['data']:
    if ex in ('NYSE', 'Nasdaq') and hs(cik) not in tk: tk[hs(cik)] = t
c['ticker'] = c['id'].map(tk)
f84 = pd.read_csv(f'{D}/datos/congelada_84_2026.csv', dtype={'id': str}); fuera = set(f84.loc[f84['venta_directivos'] == 1, 'id'])
print('TR146 cartera', len(c), '| con ticker', c['ticker'].notna().sum(), '| fuera por #84', c['id'].isin(fuera).sum(), flush=True)
c = c[c['ticker'].notna() & ~c['id'].isin(fuera)].sort_values('pal', ascending=False)
c[['id', 'anio_presentado', 'sic', 'pal', 'p', 'ticker']].to_csv(f'{D}/datos/tr146_cartera_2026.csv', index=False)
viejo = set(pd.read_csv(f'{D}/datos/tr87_cartera_2026.csv')['ticker'].dropna())
print('TR146 final', len(c), '| en común con la lista en juego (#87)', len(viejo & set(c['ticker'])), flush=True)
print('TR146 sha256', hashlib.sha256(open(f'{D}/datos/tr146_cartera_2026.csv', 'rb').read()).hexdigest())
# cortes para Rt (mismo armado que los de Gemma: percentil 90 por SIC 3, SIC 2 y todas)
C = {'todas': {'corte': float(d.pal.quantile(.9)), 'n': int(len(d))}}
for k in ('s2', 's3'):
    for g, z in d.groupby(k): C[g] = {'corte': float(z.pal.quantile(.9)), 'n': int(len(z))}
json.dump({'nota': 'Corte del 10% de arriba del puntaje de palabras (#146, Tr v5) por industria (SIC de 2 o 3 cifras) en los 10-K de 2026. Se usa SIC 3 si tiene n>=10, si no SIC 2, si no todas.',
           'fecha': '2026-11-17', 'cortes': dict(sorted(C.items()))}, open(f'{D}/repo-tr/rt/cortes.json', 'w', encoding='utf-8'), indent=0)
q = d.sort_values('pal').iloc[[int(len(d) * x) for x in (.3, .4, .5, .6, .7)]]
q[['cik', 'pal']].to_csv(f'{D}/repo-tr/rt/control.csv', index=False); print('TR146 cortes', len(C), '| control', list(q.cik), flush=True)
