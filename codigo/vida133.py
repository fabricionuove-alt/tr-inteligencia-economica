"""#133: maduras - jóvenes (nacimiento + declive), log-exceso a 12 meses contra pares, cohortes 2023-2025. Reglas en notas/11 (#133)."""
import os, json, time, hashlib, urllib.request, numpy as np, pandas as pd
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; D = f'{B}/fuentes/frames'; rng = np.random.default_rng(0)
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
C = {'O': 'NetCashProvidedByUsedInOperatingActivities', 'I': 'NetCashProvidedByUsedInInvestingActivities', 'F': 'NetCashProvidedByUsedInFinancingActivities'}
E = []
for y in (2022, 2023, 2024):
    v = {}
    for k, c in C.items():
        f = f'{D}/{c}_CY{y}.json'
        if not os.path.exists(f):
            open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(f'https://data.sec.gov/api/xbrl/frames/us-gaap/{c}/USD/CY{y}.json', headers=UA), timeout=120).read()); time.sleep(.2)
        for o in json.load(open(f))['data']: v.setdefault(o['cik'], {})[k] = o['val']
    for cik, z in v.items():
        if len(z) < 3: continue
        O, I, F = z['O'] > 0, z['I'] > 0, z['F'] > 0
        e = 'madurez' if (O and not I and not F) else ('joven' if ((not O and not I and F) or (not O and I)) else None)
        if e: E.append({'id': hs(cik), 'ap': y + 1, 'etapa': e})
E = pd.DataFrame(E).drop_duplicates(['id', 'ap'])
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int); et['r1'] = pd.to_numeric(et['_ret1'], errors='coerce')
x = et.drop_duplicates(['id', 'ap'])[['id', 'ap', 'sic', 'tam', 'r1']].dropna()
x = x[x.ap.isin([2023, 2024, 2025])].copy(); x['sic3'] = x['sic'].str[:3]; x['dec'] = np.minimum((x['tam'] * 10).astype(int), 9); g = ['ap', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy(); x['lr'] = np.log(np.maximum(x['r1'], .01)); x['ex'] = (x['lr'] - x.groupby(g)['lr'].transform('median')) * 100
x = x.merge(E, on=['id', 'ap'])
def dif(z): return z.loc[z.etapa == 'madurez', 'ex'].mean() - z.loc[z.etapa == 'joven', 'ex'].mean()
por = {}
for y, z in x.groupby('ap'):
    por[y] = dif(z); print(f'  {y} maduras {int((z.etapa=="madurez").sum())} jovenes {int((z.etapa=="joven").sum())} dif {por[y]:+.1f}', flush=True)
obs = dif(x); lab = (x.etapa == 'madurez').values; ex = x.ex.values; gid = x.groupby(g).ngroup().values
idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
P = []
for _ in range(2000):
    l2 = lab.copy()
    for ii in idx: l2[ii] = rng.permutation(l2[ii])
    P.append(ex[l2].mean() - ex[~l2].mean())
p = ((np.array(P) >= obs).sum() + 1) / 2001
print(f'VI133 total maduras - jovenes {obs:+.1f} p {p:.4f}')
print('CRITERIO133', 'PASA' if all(v > 0 for v in por.values()) and len(por) == 3 and p < .05 else 'no pasa')
