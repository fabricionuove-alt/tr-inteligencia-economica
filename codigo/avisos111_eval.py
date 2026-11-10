"""#111: evalúa la lectura de Qwen de los avisos 8-K (sal-avisos111/lectura.jsonl). Reglas en notas/11 (#111)."""
import json, hashlib, numpy as np, pandas as pd
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
NO = {'united states', 'usa', 'us', 'u.s.', 'u.s', 'united states of america', 'america', 'puerto rico', 'guam', 'us virgin islands', 'virgin islands', 'american samoa', 'northern mariana islands', 'none', 'null', '', 'unknown', 'n/a'}
R = [json.loads(l) for l in open(f'{B}/entrenar/sal-avisos111/lectura.jsonl', encoding='utf-8')]
print('leídos', len(R), 'sin JSON', sum(r['lectura'] is None for r in R), flush=True)
filas = []
for r in R:
    j = r['lectura'] or {}
    pais = str(j.get('country') or '').strip().lower()
    ok = j.get('foreign_win') is True and pais not in NO
    try: usd = float(j.get('usd_millions'))
    except Exception: usd = np.nan
    filas.append({'cik': r['cik'], 'fecha': r['fecha'], 'ok': ok, 'pais': pais, 'cliente': j.get('customer'), 'usd': usd})
a = pd.DataFrame(filas); print('marcados ganó afuera', a['ok'].sum(), 'empresas', a[a.ok]['cik'].nunique(), flush=True)
print(a[a.ok]['pais'].value_counts().head(15).to_dict(), flush=True)
a = a[a.ok].copy()
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
a['id'] = a['cik'].map(hs); a['Y'] = a['fecha'].str[:4].astype(int)
s = a.groupby(['id', 'Y']).agg(usd=('usd', 'max'), gob=('cliente', lambda c: any(x in ('government', 'state_company') for x in c))).reset_index(); s['ap'] = s['Y'] + 1
gan = set(zip(s['id'], s['Y'])); s['primera'] = [all((i, y - k) not in gan for k in (1, 2, 3)) for i, y in zip(s['id'], s['Y'])]
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int)
x = et.drop_duplicates(['id', 'ap']).copy(); x['r'] = pd.to_numeric(x['_ret4'], errors='coerce'); x = x.dropna(subset=['r', 'sic', 'tam'])
x['sic3'] = x['sic'].str[:3]; x['dec'] = np.minimum((x['tam'] * 10).astype(int), 9); g = ['ap', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy()
x = x.merge(s[['id', 'ap', 'primera', 'usd', 'gob']], on=['id', 'ap'], how='left'); x['gana'] = x['primera'].notna(); x['h'] = (x['r'] <= .5).astype(float)
x['hp'] = x['h'].where(~x['gana']).groupby([x[c] for c in g]).transform('mean')
x['med'] = x['r'].where(~x['gana']).groupby([x[c] for c in g]).transform('median'); x['ex'] = (x['r'] - x['med']) * 100
x = x.dropna(subset=['med']); x['gid'] = x.groupby(g).ngroup()
def tramo(z, nomb):
    f = z[z['gana']]
    if len(f) == 0: print(f'AV111 {nomb:24s} n 0'); return np.nan, 1.0, 0
    obs = f['ex'].mean(); lab = z['gana'].values; ex_all = z['ex'].values
    idx = [np.where(z['gid'].values == k)[0] for k in np.unique(z['gid'].values)]
    idx = [ii for ii in idx if lab[ii].any() and not lab[ii].all()]; perm = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        perm.append(ex_all[l2].mean())
    p = (np.sum(np.array(perm) >= obs) + 1) / 2001
    print(f'AV111 {nomb:24s} n {len(f):5d} exceso medio {obs:+.1f} pts p {p:.4f} mediano {f["ex"].median():+.1f} | hundidas {f["h"].mean():.3f} esperado {f["hp"].mean():.3f}', flush=True)
    return obs, p, len(f)
e, _, _ = tramo(x[(x.ap >= 2010) & (x.ap <= 2016)], 'exploración 2010-2016'); c, pc, nc = tramo(x[(x.ap >= 2017) & (x.ap <= 2020)], 'confirmación 2017-2020'); n, _, _ = tramo(x[x.ap >= 2021], 'nunca usados 2021-2022')
f = x[x['gana']]
for nomb, z in (('>= 100M', f[f['usd'] >= 100]), ('< 100M o sin monto', f[~(f['usd'] >= 100)]), ('gobierno o estatal', f[f['gob'] == True]), ('privado', f[f['gob'] == False]), ('primera vez', f[f['primera'] == True]), ('seguido', f[f['primera'] == False])):
    print(f'AV111 {nomb:24s} n {len(z):5d} exceso medio {z["ex"].mean():+.1f} mediano {z["ex"].median():+.1f} hundidas {z["h"].mean():.3f} esperado {z["hp"].mean():.3f}', flush=True)
v = 'muestra insuficiente' if nc < 30 else ('PASA' if c >= 5 and pc < .05 and e > 0 and n > 0 else 'no pasa')
print(f'CRITERIO111 confirmación {c:+.1f} pts (p {pc:.4f}, n {nc}) exploración {e:+.1f} nunca usados {n:+.1f} -> {v}', flush=True)
f[['id', 'ap', 'primera', 'usd', 'gob', 'r', 'ex', 'h', 'hp']].to_csv(f'{B}/entrenar/sal-cab102/avisos111_filas.csv', index=False)
