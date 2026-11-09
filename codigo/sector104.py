"""#104: los planes de compra que cuentan los cables (procurement_plan) por sector, contra el rendimiento del sector a 4 años. python sector104.py lectura.jsonl [...]"""
import sys, re, json, collections, numpy as np, pandas as pd
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'
SEC = {'defensa': ['defense', 'military', 'security'], 'aviones': ['aircraft', 'aviation', 'aerospace', 'airport', 'space'], 'petróleo': ['oil', 'gas', 'natural_gas', 'pipeline', 'petroleum'],
       'telecom': ['telecom', 'telecommunications', 'ict', 'electronics'], 'trenes': ['rail', 'railway', 'transportation', 'transport'], 'nuclear': ['nuclear'],
       'energía': ['energy', 'power', 'electricity', 'renewable_energy', 'coal'], 'farma': ['pharma', 'health', 'healthcare', 'biotech', 'medical'], 'agro': ['agriculture', 'food', 'food_processing'], 'construcción': ['construction', 'infrastructure', 'road', 'port', 'housing', 'water']}
SIC = {'defensa': ['3812', '348', '376', '3795'], 'aviones': ['372', '4512', '4522', '4581'], 'petróleo': ['13', '29', '4922', '4923'], 'telecom': ['48', '366', '367'],
       'trenes': ['374', '40', '3743'], 'nuclear': ['4911', '4931', '3443', '1094'], 'energía': ['491', '493', '3511', '3612', '3621'], 'farma': ['283', '384', '80'], 'agro': ['01', '02', '07', '20', '0723', '3523'], 'construcción': ['15', '16', '17', '3531', '3241', '3272', '3273', '4941']}
inv = {w: s for s, ws in SEC.items() for w in ws}
import os
excl = {json.loads(l)['cable_id'] for l in open(f'{B}/entrenar/sal-cab102/lectura.jsonl', encoding='utf-8')} if os.environ.get('SIN_BEXP') else set()
cnt = collections.Counter(); tot = collections.Counter()
for l in (l for a in sys.argv[1:] for l in open(a, encoding='utf-8')):
    x = json.loads(l); j = x.get('lectura')
    if not isinstance(j, dict) or x['cable_id'] in excl: continue
    y = int(re.search(r'/(\d{4})', x['datetime']).group(1)); tot[y] += 1
    if j.get('kind') != 'procurement_plan': continue
    for s in {inv.get(str(w).lower()) for w in (j.get('sectors') or [])} - {None}: cnt[(s, y)] += 1
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['sic'])
sic = et.groupby('id')['sic'].agg(lambda s: s.mode().iloc[0]).str.zfill(4)
pr = pd.read_csv(f'{B}/entrenar/sal-cab101/mercado-a/precios-2006.csv', dtype={'id': str, 'mes': str}); pr = pr[pr['mes'].str.match(r'^20[01]\d(0[1-9]|1[0-2])$') & (pr['precio'] > 0)]
pr['m'] = pr['mes'].str[:4].astype(int) * 12 + pr['mes'].str[4:].astype(int) - 1
P = pr.drop_duplicates(['id', 'm']).pivot(index='m', columns='id', values='precio').sort_index(); PF = P.ffill(limit=3)
R = P / P.shift(1); SPL = np.array([1/2, 1/3, 1/4, 1/5, 1/10, 2, 3, 4, 5, 10])
salto = pd.DataFrame(np.any(np.abs(R.values[..., None] / SPL - 1) < 0.03, axis=-1), index=R.index, columns=R.columns)
filas = []
for y in range(2005, 2010):
    a, b = (y + 1) * 12, (y + 5) * 12
    if a not in P.index or b not in P.index: continue
    r = PF.loc[b] / PF.loc[a]; s = salto.loc[a + 1:b].any(axis=0); r = r[np.isfinite(r) & (r > 0) & ~s]; r = r[r.index.isin(sic.index)]
    lr = np.log(r.clip(0.01, 50)); med = lr.median(); ss = sic[lr.index]
    for k, pref in SIC.items():
        g = lr[ss.apply(lambda c: any(c.startswith(p) for p in pref))]
        filas.append({'sector': k, 'anio': y, 'n': len(g), 'ex': g.median() - med, 'cables': cnt[(k, y)], 'parte': cnt[(k, y)] / max(tot[y], 1)})
d = pd.DataFrame(filas); d['parte_rel'] = d['parte'] / d.groupby('sector')['parte'].transform('mean')   # contra el promedio del mismo sector
print(d.pivot(index='sector', columns='anio', values='cables').to_string(), flush=True)
print(d.pivot(index='sector', columns='anio', values='ex').round(3).to_string(), flush=True)
c1 = d[['parte_rel', 'ex']].corr(method='spearman').iloc[0, 1]
alto = d[d['parte_rel'] > 1]['ex'].mean(); bajo = d[d['parte_rel'] <= 1]['ex'].mean()
print(f'SECTOR104 correlación (rangos) parte de cables de compra (contra su promedio) vs exceso del sector a 4 años: {c1:+.3f}; años altos {alto:+.3f} bajos {bajo:+.3f} dif {alto - bajo:+.3f} (n {len(d)})', flush=True)
d.to_csv(f'{B}/entrenar/sal-cab102/sector104_{len(sys.argv) - 1}.csv', index=False)
