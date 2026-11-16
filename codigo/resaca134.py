"""#134: ¿cuando las jóvenes le ganan a las maduras el primer año, pierden los años 2-4? Reglas en notas/11 (#134)."""
import json, hashlib, numpy as np, pandas as pd
from scipy.stats import spearmanr
rng = np.random.default_rng(0)
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
C = {'O': 'NetCashProvidedByUsedInOperatingActivities', 'I': 'NetCashProvidedByUsedInInvestingActivities', 'F': 'NetCashProvidedByUsedInFinancingActivities'}
R = []
for y in range(2009, 2022):
    v = {}
    for k, c in C.items():
        for o in json.load(open(f'../fuentes/frames/{c}_CY{y}.json'))['data']: v.setdefault(o['cik'], {})[k] = o['val']
    for cik, z in v.items():
        if len(z) < 3: continue
        O, I, F = z['O'] > 0, z['I'] > 0, z['F'] > 0
        e = 'madura' if (O and not I and not F) else ('joven' if ((not O and not I and F) or (not O and I)) else None)
        if e: R.append({'id': hs(cik), 'ap': y + 1, 'etapa': e})
E = pd.DataFrame(R).drop_duplicates(['id', 'ap'])
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['ap'] = et.anio_presentado.astype(int)
for c in ('_ret1', '_ret4'): et[c] = pd.to_numeric(et[c], errors='coerce')
x = et.drop_duplicates(['id', 'ap'])[['id', 'ap', 'sic', 'tam', '_ret1', '_ret4']].dropna()
x['sic3'] = x.sic.str[:3]; x['dec'] = np.minimum((x.tam * 10).astype(int), 9); g = ['ap', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy()
x['l1'] = np.log(np.maximum(x._ret1, .01)); x['l234'] = np.log(np.maximum(x._ret4, .01)) - x['l1']
for c in ('l1', 'l234'): x['e' + c] = (x[c] - x.groupby(g)[c].transform('median')) * 100
x = x.merge(E, on=['id', 'ap'])
co = []
for y, z in x.groupby('ap'):
    j, m = z[z.etapa == 'joven'], z[z.etapa == 'madura']
    if len(j) >= 20 and len(m) >= 20: co.append({'ap': y, 'jovenes': len(j), 'maduras': len(m), 'D1': j.el1.mean() - m.el1.mean(), 'D234': j.el234.mean() - m.el234.mean()})
co = pd.DataFrame(co); print(co.round(1).to_string(index=False), flush=True)
o = spearmanr(co.D1, co.D234)[0]; P = np.array([spearmanr(co.D1, rng.permutation(co.D234.values))[0] for _ in range(10000)]); p = ((P <= o).sum() + 1) / 10001
print(f'RE134 D1 vs D234 rho {o:+.2f} p {p:.4f} (cohortes {len(co)})'); print('CRITERIO134', 'pasa' if o < 0 and p < .05 else 'no pasa')
