"""#110: «ganó un contrato afuera» en avisos 8-K (buscador de texto de EDGAR). Reglas en notas/11 (#110).
python fts110.py"""
import os, re, json, time, hashlib, urllib.request, urllib.parse, numpy as np, pandas as pd
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
D = f'{B}/fuentes/fts110'; os.makedirs(f'{D}/docs', exist_ok=True)
def get(u, n=6):
    for k in range(n):
        try:
            time.sleep(0.15); return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
        except Exception as e:
            time.sleep(3 * (k + 1))
    return None
MULTI = ['Cape Verde', 'Costa Rica', 'Dominican Republic', 'El Salvador', 'Equatorial Guinea', 'Ivory Coast', 'New Zealand', 'Papua New Guinea', 'San Marino', 'Saudi Arabia', 'Sierra Leone', 'Solomon Islands', 'South Africa', 'Sri Lanka', 'United Arab Emirates', 'United Kingdom', 'Abu Dhabi', 'Hong Kong', 'Puerto Rico', 'Trinidad and Tobago', 'Antigua and Barbuda', 'Burkina Faso', 'Bosnia and Herzegovina']
SUELTAS = """Afghanistan Albania Algeria Andorra Angola Argentina Armenia Australia Austria Azerbaijan Bahamas Bahrain Bangladesh Barbados Belarus Belgium Belize Benin Bhutan Bolivia Botswana Brazil Brunei Bulgaria Burundi Cambodia Cameroon Canada Chad Chile China Colombia Comoros Congo Croatia Cuba Cyprus Czech Denmark Djibouti Dominica Ecuador Egypt Eritrea Estonia Eswatini Ethiopia Fiji Finland France Gabon Gambia Georgia Germany Ghana Greece Grenada Guatemala Guinea Guyana Haiti Honduras Hungary Iceland India Indonesia Iran Iraq Ireland Israel Italy Jamaica Japan Jordan Kazakhstan Kenya Kiribati Korea Kosovo Kuwait Kyrgyzstan Laos Latvia Lebanon Lesotho Liberia Libya Liechtenstein Lithuania Luxembourg Madagascar Malawi Malaysia Maldives Mali Malta Mauritania Mauritius Mexico Micronesia Moldova Monaco Mongolia Montenegro Morocco Mozambique Myanmar Namibia Nauru Nepal Netherlands Nicaragua Niger Nigeria Norway Oman Pakistan Palau Panama Paraguay Peru Philippines Poland Portugal Qatar Romania Russia Rwanda Samoa Senegal Serbia Seychelles Singapore Slovakia Slovenia Somalia Spain Sudan Suriname Sweden Switzerland Syria Taiwan Tajikistan Tanzania Thailand Timor Togo Tonga Tunisia Turkey Turkmenistan Tuvalu Uganda Ukraine Uruguay Uzbekistan Vanuatu Venezuela Vietnam Yemen Zambia Zimbabwe Kurdistan Dubai""".split()
PAIS = '|'.join(map(re.escape, sorted(set(MULTI + SUELTAS), key=len, reverse=True)))
RX = re.compile(r'(?:government|ministry)\s+of\s+(?:the\s+)?(?:[A-Z][\w\'-]*\s+){0,4}?(?:of\s+(?:the\s+)?)?(' + PAIS + r')\b', re.I)
# 1) buscar
F = f'{D}/hits.csv'
if not os.path.exists(F):
    rows = []
    for q in ('"awarded" "contract" "government of"', '"awarded" "contract" "ministry of"'):
        for y in range(2009, 2022):
            fr = 0
            while True:
                u = 'https://efts.sec.gov/LATEST/search-index?' + urllib.parse.urlencode({'q': q, 'forms': '8-K', 'dateRange': 'custom', 'startdt': f'{y}-01-01', 'enddt': f'{y}-12-31', 'from': fr})
                d = json.loads(get(u)); hh = d['hits']['hits']
                for x in hh:
                    s = x['_source']; rows.append({'q': q, 'y': y, 'cik': s['ciks'][0], 'fecha': s['file_date'], 'doc': x['_id'], 'nombre': s['display_names'][0]})
                fr += len(hh)
                if not hh or fr >= d['hits']['total']['value']: break
            print(q, y, d['hits']['total']['value'], flush=True)
    pd.DataFrame(rows).drop_duplicates(['cik', 'doc']).to_csv(F, index=False)
h = pd.read_csv(F, dtype={'cik': str})
print('documentos', len(h), 'empresas', h['cik'].nunique(), flush=True)
# 2) bajar y filtrar a otro país
G = f'{D}/afuera.csv'
if not os.path.exists(G):
    out = []
    for i, r in enumerate(h.itertuples()):
        adsh, fn = r.doc.split(':'); p = f'{D}/docs/{adsh}_{fn}'
        if not os.path.exists(p):
            b = get(f'https://www.sec.gov/Archives/edgar/data/{int(r.cik)}/{adsh.replace("-", "")}/{fn}')
            if b is None: print('falló', r.doc, flush=True); continue
            open(p, 'wb').write(b)
        t = re.sub(r'<[^>]+>', ' ', open(p, 'rb').read().decode('latin1')); t = re.sub(r'&nbsp;|&#160;', ' ', t); t = re.sub(r'\s+', ' ', t)
        paises = set()
        for m in re.finditer(r'awarded', t, re.I):
            for mm in RX.finditer(t[max(0, m.start() - 300): m.end() + 300]): paises.add(mm.group(1).title())
        out.append({'cik': r.cik, 'fecha': r.fecha, 'doc': r.doc, 'paises': ';'.join(sorted(paises))})
        if i % 200 == 0: print('bajados', i, flush=True)
    pd.DataFrame(out).to_csv(G, index=False)
a = pd.read_csv(G, dtype={'cik': str}, keep_default_na=False); a = a[a['paises'] != '']
print('avisos con país extranjero', len(a), 'empresas', a['cik'].nunique(), flush=True)
print(a['paises'].str.split(';').explode().value_counts().head(20).to_dict(), flush=True)
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
a['id'] = a['cik'].map(hs); a['Y'] = a['fecha'].str[:4].astype(int); s = a.drop_duplicates(['id', 'Y'])[['id', 'Y']]; s['ap'] = s['Y'] + 1
gan = set(zip(s['id'], s['Y'])); s['primera'] = [all((i, y - k) not in gan for k in (1, 2, 3)) for i, y in zip(s['id'], s['Y'])]
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int)
x = et.drop_duplicates(['id', 'ap']).copy(); x['r'] = pd.to_numeric(x['_ret4'], errors='coerce'); x = x.dropna(subset=['r', 'sic', 'tam'])
x['sic3'] = x['sic'].str[:3]; x['dec'] = np.minimum((x['tam'] * 10).astype(int), 9); g = ['ap', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy()
x = x.merge(s[['id', 'ap', 'primera']], on=['id', 'ap'], how='left'); x['gana'] = x['primera'].notna(); x['h'] = (x['r'] <= .5).astype(float)
x['hp'] = x['h'].where(~x['gana']).groupby([x[c] for c in g]).transform('mean')
x['med'] = x['r'].where(~x['gana']).groupby([x[c] for c in g]).transform('median'); x['ex'] = (x['r'] - x['med']) * 100
x = x.dropna(subset=['med']); x['gid'] = x.groupby(g).ngroup()
def tramo(z, nomb):
    f = z[z['gana']]; obs = f['ex'].mean()
    lab = z['gana'].values; ex_all = (z['r'] - z['med']).values * 100
    idx = [np.where(z['gid'].values == k)[0] for k in np.unique(z['gid'].values)]
    idx = [ii for ii in idx if lab[ii].any() and not lab[ii].all()]; perm = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        perm.append(ex_all[l2].mean())
    p = (np.sum(np.array(perm) >= obs) + 1) / 2001
    print(f'FTS110 {nomb:24s} n {len(f):5d} exceso medio {obs:+.1f} pts p {p:.4f} mediano {f["ex"].median():+.1f} | hundidas {f["h"].mean():.3f} esperado {f["hp"].mean():.3f}', flush=True)
    return obs, p
e, _ = tramo(x[(x.ap >= 2010) & (x.ap <= 2016)], 'exploración 2010-2016'); c, pc = tramo(x[(x.ap >= 2017) & (x.ap <= 2020)], 'confirmación 2017-2020'); n, _ = tramo(x[x.ap >= 2021], 'nunca usados 2021-2022')
f = x[x['gana']]
for nomb, z in (('primera vez', f[f['primera'] == True]), ('seguido', f[f['primera'] == False])):
    print(f'FTS110 {nomb:24s} n {len(z):5d} exceso medio {z["ex"].mean():+.1f} hundidas {z["h"].mean():.3f} esperado {z["hp"].mean():.3f}', flush=True)
print(f'CRITERIO110 confirmación {c:+.1f} pts (p {pc:.4f}) exploración {e:+.1f} nunca usados {n:+.1f} -> {"PASA" if c >= 5 and pc < .05 and e > 0 and n > 0 else "no pasa"}', flush=True)
f[['id', 'ap', 'primera', 'r', 'ex', 'h', 'hp']].to_csv(f'{B}/entrenar/sal-cab102/fts110_filas.csv', index=False)
