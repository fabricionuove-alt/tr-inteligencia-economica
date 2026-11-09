"""#105: avisos de venta de armas (36(b), Federal Register) por contratista principal, contra el rendimiento a 4 años del 10-K siguiente. python fms105_eval.py"""
import re, json, html, hashlib, numpy as np, pandas as pd
from english_words import get_english_words_set
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
D = get_english_words_set(['web2'], lower=True) | get_english_words_set(['gcide'], lower=True)
def dic(w):
    w = w.lower(); return bool({w, w[:-1] if w.endswith('s') else w, w[:-2] if w.endswith('es') else w, w[:-3] + 'y' if w.endswith('ies') else w} & D)
SUF = {'INC', 'CORP', 'CORPORATION', 'CO', 'COMPANY', 'LTD', 'LIMITED', 'PLC', 'LLC', 'LP', 'L', 'P', 'HOLDINGS', 'HOLDING', 'GROUP', 'THE', 'NV', 'N', 'V', 'SA', 'AG', 'INCORPORATED', 'COS', 'TRUST', 'DE', 'NEW', 'INTERNATIONAL', 'INTL', 'USA', 'US', 'AMERICA', 'AMERICAS', 'GLOBAL', 'OPERATIONS', 'SERVICES', 'SYSTEMS'}
def nucleo(n):
    n = re.sub(r'/[A-Z]{2,3}/?', ' ', str(n).upper()); n = re.sub(r'[^A-Z0-9 ]', ' ', n.replace('&', ' AND ')); w = n.split()
    while w and w[0] == 'THE': w = w[1:]
    while w and w[-1] in SUF: w = w[:-1]
    return ' '.join(w)
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int); ids = set(et['id'])
nom = {}
for l in open(f'{B}/fuentes/exim/cik-lookup-data.txt', encoding='latin1'):
    p = l.rstrip('\n').rsplit(':', 2)
    if len(p) < 3 or not p[1].isdigit(): continue
    i = h(int(p[1]))
    if i in ids:
        c = nucleo(p[0])
        if len(c.replace(' ', '')) >= 4 and (' ' in c or not dic(c)): nom.setdefault(c, set()).add(i)
nom = {c: next(iter(s)) for c, s in nom.items() if len(s) == 1}
ALIAS = {'LOCKHEED': 'LOCKHEED MARTIN', 'RAYTHEON': 'RAYTHEON', 'GENERAL DYNAMICS': 'GENERAL DYNAMICS', 'GE': 'GENERAL ELECTRIC', 'BAE': 'BAE', 'NORTHROP': 'NORTHROP GRUMMAN', 'L 3': 'L 3 COMMUNICATIONS', 'L3': 'L 3 COMMUNICATIONS', 'L3HARRIS': 'L3HARRIS TECHNOLOGIES', 'HONEYWELL': 'HONEYWELL', 'TEXTRON': 'TEXTRON', 'OSHKOSH': 'OSHKOSH'}
def madre(n):
    c = nucleo(n); w = c.split()
    if not w: return None, None
    for a, b in ALIAS.items():
        if c == a or c.startswith(a + ' '): c = b + c[len(a):] if not c.startswith(b) else c; break
    w = c.split()
    for k in range(len(w), 0, -1):
        q = ' '.join(w[:k])
        if q in nom and (k > 1 or not dic(q)): return nom[q], q
    return None, None
filas = []; sinmatch = {}
for l in open(f'{B}/entrenar/sal-fms/avisos.jsonl', encoding='utf-8'):
    x = json.loads(l); t = html.unescape(re.sub(r'<[^>]+>', ' ', x['texto'])); t = re.sub(r'\s+', ' ', t); y = int(x['fecha'][:4])
    for tr in re.split(r'Transmittal No\.', t)[1:]:
        v = re.search(r'Total[ .]*\$\s*([\d.,]+)\s*(billion|million)', tr, re.I)
        monto = float(v.group(1).replace(',', '')) * (1e3 if v.group(2).lower() == 'billion' else 1) if v else np.nan
        m = re.search(r'(?:principal|prime)\s+(?:U\.S\.\s+)?contractors?\s+(?:will be|is|are|for this[^:]*?will be)[:\s]+(.{0,600}?)(?:\.\s+(?:There|The |No |Acceptance|Implementation|Purchaser|This )|$)', tr, re.I)
        if not m or re.match(r'\s*(not|unknown|yet)', m.group(1), re.I): continue
        trozos = [z for z in re.split(r';|\band\b|,\s*(?=[A-Z][a-z]+ [A-Z])|\bin\b|\bof\b', m.group(1)) if z.strip()]
        es = []
        for z in trozos:
            i, q = madre(z.strip())
            if i and i not in es: es.append(i)
            elif not i and len(z.strip()) > 3: sinmatch[z.strip()[:40]] = sinmatch.get(z.strip()[:40], 0) + 1
        for i in es: filas.append({'id': i, 'Y': y, 'monto': monto / len(es), 'doc': x['doc']})
a = pd.DataFrame(filas); print('avisos con empresa del dataset', a['doc'].nunique(), 'menciones', len(a), 'empresas', a['id'].nunique(), flush=True)
print('sin empresa (top)', sorted(sinmatch.items(), key=lambda z: -z[1])[:30], flush=True)
print('por año', a.groupby('Y').size().to_dict(), flush=True)
s = a.groupby(['id', 'Y'])['monto'].sum().reset_index(); s['ap'] = s['Y'] + 1
x = et.drop_duplicates(['id', 'ap']).copy(); x['r'] = pd.to_numeric(x['_ret4'], errors='coerce'); x = x.dropna(subset=['r', 'sic', 'tam'])
x['sic3'] = x['sic'].str[:3]; x['ter'] = pd.cut(x['tam'], [0, 1/3, 2/3, 1], include_lowest=True, labels=False); g = ['ap', 'sic3', 'ter']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy(); x['lr'] = np.log(x['r'].clip(lower=0.01))
x = x.merge(s[['id', 'ap', 'monto']], on=['id', 'ap'], how='left'); x['fms'] = x['monto'].notna()
x['med_sin'] = x[~x['fms']].groupby(g)['lr'].transform('median'); x['med_sin'] = x.groupby(g)['med_sin'].transform('max'); x['ex2'] = x['lr'] - x['med_sin']
f = x[x['fms']].dropna(subset=['ex2']); print('empresas-año con aviso y rendimiento', len(f), f.groupby('ap').size().to_dict(), flush=True)
print('FMS105 por año', f.groupby('ap')['ex2'].mean().round(3).to_dict(), flush=True)
fe = lambda z: z['ex2'].mean()
e, c, n = fe(f[f.ap <= 2016]), fe(f[(f.ap >= 2017) & (f.ap <= 2020)]), fe(f[f.ap >= 2021])
print(f'FMS105 exploración {e:+.3f} | confirmación {c:+.3f} | nunca usados {n:+.3f}', flush=True)
for nomb, z in (('>1000M', f[f['monto'] > 1000]), ('<=1000M', f[f['monto'] <= 1000])): print(f'FMS105 {nomb}: n {len(z)} exceso {fe(z):+.3f}', flush=True)
print(f'FMS105 hundidas: con aviso {(f["r"] <= .5).mean():.3f} todas {(x["r"] <= .5).mean():.3f}', flush=True)
print(f'CRITERIO105 confirmación {c:+.3f} exploración {e:+.3f} nunca usados {n:+.3f} -> {"PASA" if c >= .10 and e > 0 and n > 0 else "no pasa"}', flush=True)
f[['id', 'ap', 'monto', 'r', 'ex2']].to_csv(f'{B}/entrenar/sal-fms/fms105_filas.csv', index=False)
