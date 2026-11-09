"""#107: problemas contados a la embajada y callados en el 10-K, a 4 años. python callado107.py lectura1.jsonl [...]"""
import sys, re, json, csv, time, urllib.request, urllib.parse, os, numpy as np, pandas as pd
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
ARGS = sys.argv[1:]
# empresa: misma regla de #102 (la parte de arriba de cab102_eval.py)
src = open(f'{B}/entrenar/cab102_eval.py', encoding='utf-8').read(); src = src[:src.index('filas = []')]
exec(src)  # define nucleo, madre, nom, sic, h, et
id2cik = {}
for l in open(f'{B}/fuentes/exim/cik-lookup-data.txt', encoding='latin1'):
    p = l.rstrip('\n').rsplit(':', 2)
    if len(p) == 3 and p[1].isdigit(): id2cik.setdefault(h(int(p[1])), int(p[1]))
CAP = {r['capital'].upper(): r['country'] for r in csv.DictReader(open(f'{B}/fuentes/paises/capitales.csv', encoding='utf-8'))}
CONS = {'HONG KONG': 'China', 'GUANGZHOU': 'China', 'SHANGHAI': 'China', 'CHENGDU': 'China', 'SHENYANG': 'China', 'LAGOS': 'Nigeria', 'SAO PAULO': 'Brazil', 'RIO DE JANEIRO': 'Brazil', 'RECIFE': 'Brazil',
        'ISTANBUL': 'Turkey', 'ADANA': 'Turkey', 'HO CHI MINH CITY': 'Vietnam', 'CHENNAI': 'India', 'MUMBAI': 'India', 'KOLKATA': 'India', 'HYDERABAD': 'India', 'MONTERREY': 'Mexico', 'CIUDAD JUAREZ': 'Mexico',
        'MERIDA': 'Mexico', 'MATAMOROS': 'Mexico', 'GUADALAJARA': 'Mexico', 'TIJUANA': 'Mexico', 'DUBAI': 'United Arab Emirates', 'JEDDAH': 'Saudi Arabia', 'DHAHRAN': 'Saudi Arabia', 'FRANKFURT': 'Germany',
        'DUSSELDORF': 'Germany', 'MUNICH': 'Germany', 'HAMBURG': 'Germany', 'LEIPZIG': 'Germany', 'HALIFAX': 'Canada', 'TORONTO': 'Canada', 'QUEBEC': 'Canada', 'MONTREAL': 'Canada', 'CALGARY': 'Canada',
        'VANCOUVER': 'Canada', 'CASABLANCA': 'Morocco', 'CHIANG MAI': 'Thailand', 'VLADIVOSTOK': 'Russia', 'YEKATERINBURG': 'Russia', 'ST PETERSBURG': 'Russia', 'SURABAYA': 'Indonesia', 'THESSALONIKI': 'Greece',
        'KARACHI': 'Pakistan', 'LAHORE': 'Pakistan', 'PESHAWAR': 'Pakistan', 'MILAN': 'Italy', 'NAPLES': 'Italy', 'FLORENCE': 'Italy', 'OSAKA KOBE': 'Japan', 'FUKUOKA': 'Japan', 'NAGOYA': 'Japan', 'NAHA': 'Japan',
        'SAPPORO': 'Japan', 'MELBOURNE': 'Australia', 'PERTH': 'Australia', 'SYDNEY': 'Australia', 'DURBAN': 'South Africa', 'JOHANNESBURG': 'South Africa', 'CAPE TOWN': 'South Africa', 'BARCELONA': 'Spain',
        'MARSEILLE': 'France', 'STRASBOURG': 'France', 'KRAKOW': 'Poland', 'ERBIL': 'Iraq', 'BASRAH': 'Iraq', 'KIRKUK': 'Iraq', 'AUCKLAND': 'New Zealand', 'BELFAST': 'United Kingdom', 'EDINBURGH': 'United Kingdom',
        'PRETORIA': 'South Africa', 'TEL AVIV': 'Israel', 'ABU DHABI': 'United Arab Emirates', 'NEW DELHI': 'India', 'BRASILIA': 'Brazil', 'MEXICO': 'Mexico', 'PANAMA': 'Panama', 'KUWAIT': 'Kuwait',
        'GUATEMALA': 'Guatemala', 'SINGAPORE': 'Singapore', 'LUXEMBOURG': 'Luxembourg', 'ALMATY': 'Kazakhstan', 'ASTANA': 'Kazakhstan', 'THE HAGUE': 'Netherlands', 'HAGUE': 'Netherlands', 'CANBERRA': 'Australia',
        'KYIV': 'Ukraine', 'HANOI': 'Vietnam', 'RANGOON': 'Burma', 'COTONOU': 'Benin', 'ABIDJAN': 'Ivory Coast', 'DAR ES SALAAM': 'Tanzania', 'MBABANE': 'Swaziland', 'BRIDGETOWN': 'Barbados', 'PORT OF SPAIN': 'Trinidad and Tobago'}
def pais(o):
    c = re.sub(r'^(Embassy|Consulate|Mission|USEU|US Office)\s+', '', o or '').upper().strip()
    return CONS.get(c) or CAP.get(c)
casos = []
for a in ARGS:
    for l in open(a, encoding='utf-8'):
        x = json.loads(l); j = x.get('lectura')
        if not isinstance(j, dict): continue
        y = int(re.search(r'/(\d{4})', x['datetime']).group(1))
        if not 2004 <= y <= 2009: continue
        for c in j.get('companies') or []:
            if not isinstance(c, dict) or c.get('role') not in ('in_trouble', 'in_dispute'): continue
            i = madre(c.get('name', '')); p = pais(x['origin'])
            if i and p and i in id2cik: casos.append({'id': i, 'anio': y, 'pais': p, 'cik': id2cik[i], 'name': c.get('name'), 'cable': x['cable_id']})
k = pd.DataFrame(casos).drop_duplicates(['id', 'anio', 'pais']); print('casos empresa-año-país', len(k), 'empresas', k['id'].nunique(), flush=True)
cache_f = f'{B}/entrenar/sal-cab102/efts_cache.json'; cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
def cuenta(cik, p, y):
    key = f'{cik}|{p}|{y}'
    if key in cache: return cache[key]
    q = urllib.parse.urlencode({'q': f'"{p}"', 'forms': '10-K', 'ciks': str(cik).zfill(10), 'dateRange': 'custom', 'startdt': f'{y}-01-01', 'enddt': f'{y + 1}-12-31'})
    for _ in range(3):
        try: d = json.loads(urllib.request.urlopen(urllib.request.Request('https://efts.sec.gov/LATEST/search-index?' + q, headers=UA), timeout=30).read()); break
        except Exception: time.sleep(3)
    else: return None
    cache[key] = d['hits']['total']['value'] > 0; time.sleep(0.15); return cache[key]
k['contado'] = [cuenta(c, p, y) for c, p, y in zip(k['cik'], k['pais'], k['anio'])]; json.dump(cache, open(cache_f, 'w'))
k = k.dropna(subset=['contado']); k['contado'] = k['contado'].astype(bool)
print('callados', (~k['contado']).sum(), 'contados', k['contado'].sum(), flush=True)
print(k.sort_values('anio')[['anio', 'name', 'pais', 'contado']].to_string(max_rows=80), flush=True)
g = k.groupby(['id', 'anio'])['contado'].agg(lambda s: int(not s.all())).reset_index().rename(columns={'contado': 'callado'})
pr = pd.read_csv(f'{B}/entrenar/sal-cab101/mercado-a/precios-2006.csv', dtype={'id': str, 'mes': str}); pr = pr[pr['mes'].str.match(r'^20[01]\d(0[1-9]|1[0-2])$') & (pr['precio'] > 0)]
pr['m'] = pr['mes'].str[:4].astype(int) * 12 + pr['mes'].str[4:].astype(int) - 1
P = pr.drop_duplicates(['id', 'm']).pivot(index='m', columns='id', values='precio').sort_index(); PF = P.ffill(limit=3)
R = P / P.shift(1); SPL = np.array([1/2, 1/3, 1/4, 1/5, 1/10, 2, 3, 4, 5, 10])
salto = pd.DataFrame(np.any(np.abs(R.values[..., None] / SPL - 1) < 0.03, axis=-1), index=R.index, columns=R.columns)
T = []
for y in range(2005, 2010):
    a, b = (y + 1) * 12, (y + 5) * 12
    r = PF.loc[b] / PF.loc[a]; s = salto.loc[a + 1:b].any(axis=0); r = r[np.isfinite(r) & (r > 0) & ~s]; r = r[r.index.isin(sic.index)]
    t = pd.DataFrame({'id': r.index, 'r': r.values, 'anio': y}); t['sic2'] = t['id'].map(sic); t['lr'] = np.log(t['r'].clip(0.01, 50))
    t['ex'] = t['lr'] - t.groupby('sic2')['lr'].transform('median'); T.append(t)
T = pd.concat(T); d = g.merge(T, on=['id', 'anio'])
dif = lambda z: z.loc[z['callado'] == 1, 'ex'].mean() - z.loc[z['callado'] == 0, 'ex'].mean()
obs = dif(d); perm = [dif(d.assign(callado=rng.permutation(d['callado'].values))) for _ in range(2000)]; p = (np.sum(np.array(perm) <= obs) + 1) / 2001
for c, z in d.groupby('callado'): print(f'CALLADO107 {"callado" if c else "contado"}: n {len(z)} exceso {z["ex"].mean():+.3f} mediana {z["ex"].median():+.3f} hundidas {(z["r"] <= .5).mean():.3f}', flush=True)
print(f'CRITERIO107 callado − contado {obs:+.3f} p {p:.4f} -> {"PASA" if obs <= -.10 and p < .05 else "no pasa"}', flush=True)
k.to_csv(f'{B}/entrenar/sal-cab102/callado107_casos.csv', index=False); d.to_csv(f'{B}/entrenar/sal-cab102/callado107_filas.csv', index=False)
