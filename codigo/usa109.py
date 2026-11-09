"""#109: contratistas federales (USAspending) >= 10M por año fiscal, hundimiento a 4 años contra pares del mismo SIC3 x décimo de tamaño.
python usa109.py   (baja a fuentes/usaspending/receptores.csv si no está)"""
import os, json, time, urllib.request, numpy as np, pandas as pd
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local', 'Content-Type': 'application/json'}
F = f'{B}/fuentes/usaspending/receptores.csv'; os.makedirs(os.path.dirname(F), exist_ok=True)
if not os.path.exists(F):
    rows = []
    for fy in range(2009, 2022):
        pg = 1
        while True:
            q = {'filters': {'time_period': [{'start_date': f'{fy - 1}-10-01', 'end_date': f'{fy}-09-30'}], 'award_type_codes': ['A', 'B', 'C', 'D']}, 'limit': 100, 'page': pg}
            for _ in range(5):
                try:
                    d = json.loads(urllib.request.urlopen(urllib.request.Request('https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/', data=json.dumps(q).encode(), headers=UA), timeout=120).read()); break
                except Exception as e: time.sleep(5)
            else: raise SystemExit(f'falló {fy} {pg}')
            res = d['results']; rows += [{'fy': fy, 'name': r['name'], 'usd': r['amount']} for r in res]
            if not res or res[-1]['amount'] < 1e7 or not d['page_metadata']['hasNext']: break
            pg += 1
        print(fy, 'páginas', pg, 'receptores', sum(1 for r in rows if r['fy'] == fy), flush=True)
    pd.DataFrame(rows).to_csv(F, index=False)
src = open(f'{B}/entrenar/cab102_eval.py', encoding='utf-8').read(); exec(src[:src.index('filas = []')])  # madre() igual que #102
a = pd.read_csv(F, keep_default_na=False); a['usd'] = pd.to_numeric(a['usd'], errors='coerce')
un = pd.Series(a['name'].unique()); mp = dict(zip(un, un.map(madre))); a['id'] = a['name'].map(mp)
m = a.dropna(subset=['id']); print('receptores que casan', m['name'].nunique(), 'empresas', m['id'].nunique(), flush=True)
print(m.groupby('name')['usd'].sum().div(1e9).sort_values(ascending=False).head(30).round(1).to_dict(), flush=True)
s = m.groupby(['id', 'fy'])['usd'].sum().reset_index(); s = s[s['usd'] >= 1e7]; s['ap'] = s['fy'] + 1
gan = set(zip(s['id'], s['fy'])); s['primera'] = [all((i, y - k) not in gan for k in (1, 2, 3)) for i, y in zip(s['id'], s['fy'])]
et2 = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et2['ap'] = et2['anio_presentado'].astype(int)
x = et2.drop_duplicates(['id', 'ap']).copy(); x['r'] = pd.to_numeric(x['_ret4'], errors='coerce'); x = x.dropna(subset=['r', 'sic', 'tam'])
x['sic3'] = x['sic'].str[:3]; x['dec'] = np.minimum((x['tam'] * 10).astype(int), 9); g = ['ap', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy(); x['lr'] = np.log(x['r'].clip(lower=0.01))
x = x.merge(s[['id', 'ap', 'usd', 'primera']], on=['id', 'ap'], how='left'); x['gana'] = x['usd'].notna(); x['h'] = (x['r'] <= .5).astype(float)
x['hp'] = x['h'].where(~x['gana']).groupby([x[c] for c in g]).transform('mean')
x['med'] = x['lr'].where(~x['gana']).groupby([x[c] for c in g]).transform('median'); x['ex'] = x['lr'] - x['med']
x = x.dropna(subset=['hp']); x['gid'] = x.groupby(g).ngroup()
def tramo(z, nomb):
    f = z[z['gana']]; obs = f['h'].mean() - f['hp'].mean()
    lab = z['gana'].values; h = z['h'].values; idx = [np.where(z['gid'].values == k)[0] for k in np.unique(z['gid'].values)]
    idx = [ii for ii in idx if lab[ii].any() and not lab[ii].all()]; perm = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        perm.append(h[l2].mean() - f['hp'].mean())
    p = (np.sum(np.array(perm) <= obs) + 1) / 2001
    print(f'USA109 {nomb:24s} n {len(f):5d} hundidas {f["h"].mean():.3f} esperado {f["hp"].mean():.3f} dif {obs:+.3f} p {p:.4f} | exceso medio {f["ex"].mean():+.3f} mediano {f["ex"].median():+.3f}', flush=True)
    return obs, p
e, _ = tramo(x[(x.ap >= 2010) & (x.ap <= 2016)], 'exploración 2010-2016'); c, pc = tramo(x[(x.ap >= 2017) & (x.ap <= 2020)], 'confirmación 2017-2020'); n, _ = tramo(x[x.ap >= 2021], 'nunca usados 2021-2022')
f = x[x['gana']]
for nomb, z in (('>= 1.000M', f[f['usd'] >= 1e9]), ('< 1.000M', f[f['usd'] < 1e9]), ('primera vez', f[f['primera'] == True]), ('ganan seguido', f[f['primera'] == False])):
    print(f'USA109 {nomb:24s} n {len(z):5d} hundidas {z["h"].mean():.3f} esperado {z["hp"].mean():.3f} exceso medio {z["ex"].mean():+.3f}', flush=True)
print(f'CRITERIO109 confirmación {c:+.3f} (p {pc:.4f}) exploración {e:+.3f} nunca usados {n:+.3f} -> {"PASA" if c <= -.02 and pc < .05 and e < 0 and n < 0 else "no pasa"}', flush=True)
f[['id', 'ap', 'usd', 'primera', 'r', 'h', 'hp', 'ex']].to_csv(f'{B}/entrenar/sal-cab102/usa109_filas.csv', index=False)
