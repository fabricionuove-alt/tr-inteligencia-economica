"""#106: nombradas en cables económicos confidenciales/secretos contra sólo en abiertos, a 48 meses. python priv106.py"""
import re, json, hashlib, collections, numpy as np, pandas as pd, ahocorasick
from english_words import get_english_words_set
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
D = get_english_words_set(['web2'], lower=True) | get_english_words_set(['gcide'], lower=True)
def dic(w):
    w = w.lower(); return bool({w, w[:-1], w[:-2], w[:-3] + 'y'} & D)
SUF = {'INC', 'CORP', 'CORPORATION', 'CO', 'COMPANY', 'LTD', 'LIMITED', 'PLC', 'LLC', 'LP', 'L', 'P', 'HOLDINGS', 'HOLDING', 'GROUP', 'THE', 'NV', 'N', 'V', 'SA', 'AG', 'INCORPORATED', 'COS', 'TRUST', 'DE', 'NEW', 'INTERNATIONAL', 'INTL', 'USA', 'US', 'AMERICA', 'AMERICAS', 'GLOBAL', 'OPERATIONS', 'SERVICES', 'SYSTEMS'}
def nucleo(n):
    n = re.sub(r'/[A-Z]{2,3}/?', ' ', str(n).upper()); n = re.sub(r'[^A-Z0-9 ]', ' ', n.replace('&', ' AND ')); w = n.split()
    while w and w[0] == 'THE': w = w[1:]
    while w and w[-1] in SUF: w = w[:-1]
    return ' '.join(w)
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['sic']); ids = set(et['id'])
sic = et.groupby('id')['sic'].agg(lambda s: s.mode().iloc[0]).str[:2]
FAMOSAS = {'GENERAL ELECTRIC', 'GENERAL MOTORS', 'GENERAL DYNAMICS', 'CATERPILLAR', 'CHEVRON', 'FORD MOTOR', 'UNITED TECHNOLOGIES', 'AMERICAN EXPRESS', 'EXXON MOBIL', 'COCA COLA', 'MORGAN STANLEY', 'GOLDMAN SACHS', 'OCCIDENTAL PETROLEUM', 'MARATHON OIL', 'APPLE', 'ORACLE', 'INTEL'}
nom = {}
for l in open(f'{B}/fuentes/exim/cik-lookup-data.txt', encoding='latin1'):
    p = l.rstrip('\n').rsplit(':', 2)
    if len(p) < 3 or not p[1].isdigit(): continue
    i = h(int(p[1]))
    if i in ids:
        c = nucleo(p[0])
        if c in FAMOSAS or any(len(w) >= 4 and not w.isdigit() and not dic(w) for w in c.split()): nom.setdefault(c, set()).add(i)
nom = {c: next(iter(s)) for c, s in nom.items() if len(s) == 1}; nom['EXXONMOBIL'] = nom.get('EXXON MOBIL')
nom = {c: i for c, i in nom.items() if i}
A = ahocorasick.Automaton()
for c, i in nom.items(): A.add_word(' ' + c + ' ', (c, i))
A.make_automaton(); print('núcleos', len(nom), flush=True)
men = collections.defaultdict(lambda: {'priv': 0, 'abierto': 0, 'secret': 0}); ej = collections.Counter()
for l in open(f'{B}/entrenar/sal-econ/econ.jsonl', encoding='utf-8'):
    x = json.loads(l); y = int(x['ym'][:4])
    if not 2005 <= y <= 2009: continue
    t = ' ' + re.sub(r'[^A-Z0-9 ]', ' ', x['texto'].upper().replace('&', ' AND ')) + ' '; t = re.sub(r' +', ' ', t)
    cl = x['clas'] or ''; priv = cl.startswith('CONFIDENTIAL') or cl.startswith('SECRET')
    for i in {v[1] for _, v in A.iter(t)}:
        k = men[(i, y)]; k['priv' if priv else 'abierto'] += 1; k['secret'] += cl.startswith('SECRET')
    for _, v in A.iter(t): ej[v[0]] += 1
print('más nombradas', ej.most_common(40), flush=True)
m = pd.DataFrame([{'id': i, 'anio': y, **v} for (i, y), v in men.items()]); m['grupo'] = np.where(m['priv'] > 0, 1, 0)
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
T = pd.concat(T); d = m.merge(T, on=['id', 'anio']); d['cables'] = d['priv'] + d['abierto']
print('empresas-año', len(d), d.groupby(['anio', 'grupo']).size().unstack().to_dict(), flush=True)
dif = lambda z: z.loc[z['grupo'] == 1, 'ex'].mean() - z.loc[z['grupo'] == 0, 'ex'].mean()
obs = dif(d); perm = []
for _ in range(2000):
    z = d.copy(); z['grupo'] = z.groupby(['anio', 'sic2'])['grupo'].transform(lambda s: rng.permutation(s.values)); perm.append(dif(z))
p = (np.sum(np.abs(perm) >= abs(obs)) + 1) / (len(perm) + 1)
d1, d2 = dif(d[d.anio <= 2007]), dif(d[d.anio >= 2008])
for g, z in d.groupby('grupo'): print(f'PRIV106 {"en privado" if g else "sólo abierta"}: n {len(z)} exceso {z["ex"].mean():+.3f} mediana {z["ex"].median():+.3f} hundidas {(z["r"] <= .5).mean():.3f} cables promedio {z["cables"].mean():.1f}', flush=True)
print('PRIV106 diferencia por año', {y: round(dif(z), 3) for y, z in d.groupby('anio')}, flush=True)
sec = d[d['secret'] > 0]; conf = d[(d['grupo'] == 1) & (d['secret'] == 0)]
print(f'PRIV106 informado: secret n {len(sec)} {sec["ex"].mean():+.3f} | sólo confidential n {len(conf)} {conf["ex"].mean():+.3f}', flush=True)
for k in (1, 3, 10):
    z = d[d['cables'] >= k]; print(f'PRIV106 con >= {k} cables: diferencia {dif(z):+.3f} (n {len(z)})', flush=True)
pasa = abs(obs) >= .10 and p < .05 and np.sign(d1) == np.sign(d2)
print(f'CRITERIO106 diferencia {obs:+.3f} p {p:.4f} 2005-07 {d1:+.3f} 2008-09 {d2:+.3f} -> {"PASA" if pasa else "no pasa"}', flush=True)
d.to_csv(f'{B}/entrenar/sal-econ/priv106_filas.csv', index=False)
