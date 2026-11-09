"""#103: créditos del EXIM Bank por empresa madre, contra el rendimiento a 4 años del 10-K siguiente. python exim103.py"""
import re, hashlib, numpy as np, pandas as pd
from english_words import get_english_words_set
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
D = get_english_words_set(['web2'], lower=True) | get_english_words_set(['gcide'], lower=True)
def dic(w):
    w = w.lower(); c = {w, w[:-1] if w.endswith('s') else w, w[:-2] if w.endswith('es') else w, w[:-3] + 'y' if w.endswith('ies') else w}
    return bool(c & D)
SUF = {'INC', 'CORP', 'CORPORATION', 'CO', 'COMPANY', 'LTD', 'LIMITED', 'PLC', 'LLC', 'LP', 'L', 'P', 'HOLDINGS', 'HOLDING', 'GROUP', 'THE', 'NV', 'N', 'V', 'SA', 'AG', 'INCORPORATED', 'COS', 'TRUST', 'DE', 'NEW', 'INTERNATIONAL', 'INTL', 'USA', 'US', 'AMERICA', 'AMERICAS', 'GLOBAL', 'OPERATIONS', 'SERVICES', 'SYSTEMS'}
def nucleo(n):
    n = re.sub(r'/[A-Z]{2,3}/?', ' ', str(n).upper()); n = re.sub(r'[^A-Z0-9 ]', ' ', n.replace('&', ' AND ')); w = n.split()
    while w and w[0] == 'THE': w = w[1:]
    while w and w[-1] in SUF: w = w[:-1]
    return ' '.join(w)
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int); ids = set(et['id'])
# nombres de las empresas del dataset
nom = {}
for l in open(f'{B}/fuentes/exim/cik-lookup-data.txt', encoding='latin1'):
    p = l.rstrip('\n').rsplit(':', 2)
    if len(p) < 3 or not p[1].isdigit(): continue
    i = h(int(p[1]))
    if i in ids:
        c = nucleo(p[0])
        if len(c.replace(' ', '')) >= 4 and (' ' in c or not dic(c)): nom.setdefault(c, set()).add(i)
nom = {c: next(iter(s)) for c, s in nom.items() if len(s) == 1}
print('núcleos de empresas del dataset', len(nom), flush=True)
# EXIM
d = pd.read_csv(f'{B}/fuentes/exim/autorizaciones.csv', low_memory=False, encoding='utf-8-sig'); d.columns = [re.sub(r'^\W+', '', c.strip()) for c in d.columns]
d = d[(d['Decision'] == 'Approved') & (d['Deal Cancelled'] != 'Yes')].copy(); d['monto'] = pd.to_numeric(d['Approved/Declined Amount'], errors='coerce')
d['F'] = pd.to_numeric(d['Fiscal Year'], errors='coerce')
def madre(n):
    c = nucleo(n); w = c.split()
    for k in range(len(w), 0, -1):            # el núcleo más largo que encabeza el nombre
        q = ' '.join(w[:k])
        if q in nom: return nom[q], q
    return None, None
ex = d[['Primary Exporter']].drop_duplicates(); ex[['id', 'match']] = ex['Primary Exporter'].apply(lambda n: pd.Series(madre(n)))
d = d.merge(ex, on='Primary Exporter', how='left')
m = d.dropna(subset=['id']); print('créditos con empresa del dataset', len(m), 'de', len(d), '; empresas', m['id'].nunique(), flush=True)
print(m.groupby('match')['monto'].sum().div(1e6).sort_values(ascending=False).head(25).round(0).to_dict(), flush=True)
s = m.groupby(['id', 'F'])['monto'].sum().reset_index(); s['ap'] = s['F'].astype(int) + 1
# rendimiento a 4 años del 10-K siguiente
x = et.drop_duplicates(['id', 'ap']).copy(); x['r'] = pd.to_numeric(x['_ret4'], errors='coerce'); x = x.dropna(subset=['r', 'sic', 'tam'])
x['sic3'] = x['sic'].str[:3]; x['ter'] = pd.cut(x['tam'], [0, 1/3, 2/3, 1], include_lowest=True, labels=False); g = ['ap', 'sic3', 'ter']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy(); x['lr'] = np.log(x['r'].clip(lower=0.01))
x = x.merge(s[['id', 'ap', 'monto']], on=['id', 'ap'], how='left'); x['exim'] = x['monto'].fillna(0) > 0
x['med'] = x.groupby(g)['lr'].transform(lambda v: v.median()); x['ex'] = x['lr'] - x.groupby(g)['lr'].transform('median')
x['med_sin'] = x[~x['exim']].groupby(g)['lr'].transform('median'); x['med_sin'] = x.groupby(g)['med_sin'].transform('max'); x['ex2'] = x['lr'] - x['med_sin']
f = x[x['exim']]; print('empresas-año financiadas con rendimiento', len(f), f.groupby('ap').size().to_dict(), flush=True)
por = f.groupby('ap')['ex2'].mean().round(3)
E, C, N = por[por.index <= 2016], por[(por.index >= 2017) & (por.index <= 2020)], por[por.index >= 2021]
print('EXIM103 exceso contra las sin crédito del mismo grupo, por año', por.to_dict(), flush=True)
fe = lambda z: z['ex2'].mean()
print(f'EXIM103 exploración {fe(f[f.ap <= 2016]):+.3f} | confirmación {fe(f[(f.ap >= 2017) & (f.ap <= 2020)]):+.3f} | nunca usados {fe(f[f.ap >= 2021]):+.3f}', flush=True)
for nomb, z in (('>100M', f[f['monto'] > 1e8]), ('<=100M', f[f['monto'] <= 1e8])): print(f'EXIM103 {nomb}: n {len(z)} exceso {fe(z):+.3f}', flush=True)
print(f'EXIM103 hundidas: financiadas {(f["r"] <= .5).mean():.3f} todas {(x["r"] <= .5).mean():.3f}', flush=True)
c, e, n = fe(f[(f.ap >= 2017) & (f.ap <= 2020)]), fe(f[f.ap <= 2016]), fe(f[f.ap >= 2021])
print(f'CRITERIO103 confirmación {c:+.3f} exploración {e:+.3f} nunca usados {n:+.3f} -> {"PASA" if c >= .10 and e > 0 and n > 0 else "no pasa"}', flush=True)
f[['id', 'ap', 'monto', 'r', 'ex2']].to_csv(f'{B}/entrenar/sal-cab101/exim103_filas.csv', index=False)
