"""#102 confirmación: cables económicos leídos, sin los BEXP ni las empresas-año de la exploración. python cab102_conf.py lectura_a.jsonl lectura_b.jsonl"""
import sys, re, json, hashlib, numpy as np, pandas as pd
sys.path.insert(0, 'E:/FABRI INFLUENCIA/inteligencia-economica/entrenar')
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'
from english_words import get_english_words_set
D = get_english_words_set(['web2'], lower=True) | get_english_words_set(['gcide'], lower=True)
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
def dic(w):
    w = w.lower(); return bool({w, w[:-1], w[:-2], w[:-3] + 'y'} & D)
SUF = {'INC', 'CORP', 'CORPORATION', 'CO', 'COMPANY', 'LTD', 'LIMITED', 'PLC', 'LLC', 'LP', 'L', 'P', 'HOLDINGS', 'HOLDING', 'GROUP', 'THE', 'NV', 'N', 'V', 'SA', 'AG', 'INCORPORATED', 'COS', 'TRUST', 'DE', 'NEW', 'INTERNATIONAL', 'INTL', 'USA', 'US', 'AMERICA', 'AMERICAS', 'GLOBAL', 'OPERATIONS', 'SERVICES', 'SYSTEMS', 'CORP.', 'AND'}
def nucleo(n):
    n = re.sub(r'/[A-Z]{2,3}/?', ' ', str(n).upper()); n = re.sub(r'[^A-Z0-9 ]', ' ', n.replace('&', ' AND ')); w = n.split()
    while w and w[0] == 'THE': w = w[1:]
    while w and w[-1] in SUF: w = w[:-1]
    return ' '.join(w)
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['sic']); ids = set(et['id'])
sic = et.groupby('id')['sic'].agg(lambda s: s.mode().iloc[0]).str[:2]
nom = {}
for l in open(f'{B}/fuentes/exim/cik-lookup-data.txt', encoding='latin1'):
    p = l.rstrip('\n').rsplit(':', 2)
    if len(p) < 3 or not p[1].isdigit(): continue
    i = h(int(p[1]))
    if i in ids:
        c = nucleo(p[0])
        if len(c.replace(' ', '')) >= 4: nom.setdefault(c, set()).add(i)
nom = {c: next(iter(s)) for c, s in nom.items() if len(s) == 1}
ALIAS = {'GE': 'GENERAL ELECTRIC', 'HP': 'HEWLETT PACKARD', 'IBM': 'INTERNATIONAL BUSINESS MACHINES', 'EXXONMOBIL': 'EXXON MOBIL', 'P G': 'PROCTER AND GAMBLE', 'GM': 'GENERAL MOTORS', 'UTC': 'UNITED TECHNOLOGIES', 'ADM': 'ARCHER DANIELS MIDLAND', 'KBR': 'KBR', 'AES': 'AES', 'AIG': 'AMERICAN INTERNATIONAL', 'CAT': 'CATERPILLAR'}
def madre(n):
    c = nucleo(n); c = ALIAS.get(c, c); w = c.split()
    for k in range(len(w), 0, -1):
        q = ' '.join(w[:k])
        if q in nom and (k > 1 or not dic(q) or q == c): return nom[q]
    return None
bexp_ids = {json.loads(l)['cable_id'] for l in open(f'{B}/entrenar/sal-cab102/lectura.jsonl', encoding='utf-8')}
expl = pd.read_csv(f'{B}/entrenar/sal-cab102/cab102_filas.csv', dtype={'id': str}); expl = set(zip(expl['id'], expl['anio']))
filas = []
for l in (l for a in sys.argv[1:] for l in open(a, encoding='utf-8')):
    x = json.loads(l); j = x.get('lectura')
    if x['cable_id'] in bexp_ids: continue
    if not isinstance(j, dict): continue
    y = int(re.search(r'/(\d{4})', x['datetime']).group(1))
    for c in j.get('companies') or []:
        if not isinstance(c, dict): continue
        i = madre(c.get('name', ''))
        if i: filas.append({'id': i, 'anio': y, 'kind': j.get('kind'), 'role': c.get('role'), 'outcome': c.get('outcome'), 'usd': c.get('usd_millions'), 'name': c.get('name')})
f = pd.DataFrame(filas); print('menciones con empresa del dataset', len(f), 'empresas', f['id'].nunique(), flush=True)
print(f.groupby(['kind', 'role']).size().sort_values(ascending=False).head(25).to_dict(), flush=True)
print(f['name'].value_counts().head(30).to_dict(), flush=True)
pr = pd.read_csv(f'{B}/entrenar/sal-cab101/mercado-a/precios-2006.csv', dtype={'id': str, 'mes': str}); pr = pr[pr['mes'].str.match(r'^20[01]\d(0[1-9]|1[0-2])$') & (pr['precio'] > 0)]
pr['m'] = pr['mes'].str[:4].astype(int) * 12 + pr['mes'].str[4:].astype(int) - 1
P = pr.drop_duplicates(['id', 'm']).pivot(index='m', columns='id', values='precio').sort_index(); PF = P.ffill(limit=3)
R = P / P.shift(1); SPL = np.array([1/2, 1/3, 1/4, 1/5, 1/10, 2, 3, 4, 5, 10])
salto = pd.DataFrame(np.any(np.abs(R.values[..., None] / SPL - 1) < 0.03, axis=-1), index=R.index, columns=R.columns)
def ret(y):
    a, b = (y + 1) * 12, (y + 5) * 12
    if a not in P.index or b not in P.index: return pd.Series(dtype=float)
    r = PF.loc[b] / PF.loc[a]; s = salto.loc[a + 1:b].any(axis=0); r = r[np.isfinite(r) & (r > 0) & ~s]; return r[r.index.isin(sic.index)]
T = []
for y in range(2004, 2010):
    r = ret(y)
    if r.empty: continue
    t = pd.DataFrame({'id': r.index, 'r': r.values, 'anio': y}); t['sic2'] = t['id'].map(sic); t['lr'] = np.log(t['r'].clip(0.01, 50))
    t['ex'] = t['lr'] - t.groupby('sic2')['lr'].transform('median'); T.append(t)
T = pd.concat(T); print('empresas-año con rendimiento', len(T), T.groupby('anio').size().to_dict(), flush=True)
f = f.merge(T[['id', 'anio', 'ex', 'r']], on=['id', 'anio'], how='inner')
f.to_csv(f'{B}/entrenar/sal-cab102/cab102_conf_filas.csv', index=False)
TODAS = f.copy(); f = f[[(i, a) not in expl for i, a in zip(f['id'], f['anio'])]]; print('sin las de la exploración: menciones', len(f), 'empresas-año', len(set(zip(f['id'], f['anio']))), flush=True)
nombradas = set(zip(f['id'], f['anio']))
base = T[[(i, a) in nombradas for i, a in zip(T['id'], T['anio'])]]
print(f'CAB102 todas las nombradas en cables BEXP (empresa-año únicas {len(base)}): exceso contra su SIC2 {base["ex"].mean():+.3f}, hundidas {(base["r"] <= .5).mean():.3f} (mercado {(T["r"] <= .5).mean():.3f})', flush=True)
def grupo(nomb, msk):
    z = f[msk].drop_duplicates(['id', 'anio'])
    if len(z) == 0: return
    pa = z.groupby('anio')['ex'].mean().round(3).to_dict()
    print(f'CAB102 {nomb:28s} n {len(z):4d} exceso {z["ex"].mean():+.3f} mediana {z["ex"].median():+.3f} hundidas {(z["r"] <= .5).mean():.3f} | por año {pa}', flush=True)
grupo('ayudada (helped)', f['role'] == 'helped')
grupo('ganó (won/outcome won)', (f['role'] == 'won') | (f['outcome'] == 'won'))
grupo('perdió', (f['role'] == 'lost') | (f['outcome'] == 'lost'))
grupo('en disputa', f['role'] == 'in_dispute')
grupo('con problemas', f['role'] == 'in_trouble')
grupo('competidora', f['role'] == 'competitor')
grupo('sólo mencionada', f['role'] == 'mentioned')
grupo('cable de advocacy', f['kind'] == 'advocacy')
grupo('advocacy y ayudada', (f['kind'] == 'advocacy') & (f['role'] == 'helped'))
grupo('monto >= 100M', pd.to_numeric(f['usd'], errors='coerce') >= 100)

# base de fama: todas las nombradas en cualquier cable (por #101), y las muy nombradas
mc = pd.read_csv(f'{B}/entrenar/sal-cab101/menciones_ok.csv', dtype={'id': str}).groupby(['id', 'anio'])['cables'].sum().reset_index()
mc = mc.merge(T[['id', 'anio', 'ex', 'r']], on=['id', 'anio'])
for k in (1, 5, 20):
    z = mc[mc['cables'] >= k]; print(f'BASE nombradas en >= {k:2d} cables en el año: n {len(z)} exceso {z["ex"].mean():+.3f} hundidas {(z["r"] <= .5).mean():.3f}', flush=True)
fam = f.merge(mc[['id', 'anio', 'cables']], on=['id', 'anio'], how='left'); fam['cables'] = fam['cables'].fillna(0)
w = fam[(fam['role'] == 'won') | (fam['outcome'] == 'won')].drop_duplicates(['id', 'anio']); s = fam[fam['role'] == 'mentioned'].drop_duplicates(['id', 'anio'])
print(f'FAMA cables promedio: ganó {w["cables"].mean():.1f} sólo mencionada {s["cables"].mean():.1f}', flush=True)
print(f'CAB102 ganó − sólo mencionada {w["ex"].mean() - s["ex"].mean():+.3f}', flush=True)

ww = f[(f['role'] == 'won') | (f['outcome'] == 'won')].drop_duplicates(['id', 'anio']); ss = f[f['role'] == 'mentioned'].drop_duplicates(['id', 'anio'])
d = ww['ex'].mean() - ss['ex'].mean(); print(f'CRITERIO102 ganó {ww["ex"].mean():+.3f} (n {len(ww)}) sólo mencionada {ss["ex"].mean():+.3f} (n {len(ss)}) diferencia {d:+.3f} -> {"PASA" if d >= .10 and ww["ex"].mean() > 0 else "no pasa"}', flush=True)
for k, z in (('por año ganó', ww), ('por año mencionada', ss)): print(k, z.groupby('anio')['ex'].mean().round(3).to_dict(), flush=True)
w2 = TODAS[(TODAS['role'] == 'won') | (TODAS['outcome'] == 'won')].drop_duplicates(['id', 'anio']); s2 = TODAS[TODAS['role'] == 'mentioned'].drop_duplicates(['id', 'anio'])
print(f'INFORMADO con todas las empresas-año: ganó {w2["ex"].mean():+.3f} (n {len(w2)}) sólo mencionada {s2["ex"].mean():+.3f} (n {len(s2)})', flush=True)
for k in ('company_problem', 'deal_news', 'procurement_plan', 'dispute', 'advocacy', 'export_control', 'newsletter', 'other'): grupo('tipo ' + k, f['kind'] == k)
