"""#130: etapa del ciclo de vida (Dickinson 2011) por signo de flujos de caja, hundidas a 4 años contra pares. Reglas en notas/11 (#130)."""
import os, json, time, hashlib, urllib.request, numpy as np, pandas as pd
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; D = f'{B}/fuentes/frames'; rng = np.random.default_rng(0)
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
C = {'O': 'NetCashProvidedByUsedInOperatingActivities', 'I': 'NetCashProvidedByUsedInInvestingActivities', 'F': 'NetCashProvidedByUsedInFinancingActivities'}
filas = []
for y in range(2009, 2022):
    v = {}
    for k, c in C.items():
        f = f'{D}/{c}_CY{y}.json'
        if not os.path.exists(f):
            open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(f'https://data.sec.gov/api/xbrl/frames/us-gaap/{c}/USD/CY{y}.json', headers=UA), timeout=120).read()); time.sleep(.2)
        for o in json.load(open(f))['data']: v.setdefault(o['cik'], {})[k] = o['val']
    for cik, z in v.items():
        if len(z) == 3: filas.append({'id': hs(cik), 'ap': y + 1, **z})
    print('año fiscal', y, sum(len(z) == 3 for z in v.values()), flush=True)
f = pd.DataFrame(filas)
def etapa(r):
    O, I, F = r.O > 0, r.I > 0, r.F > 0
    if not O and not I and F: return 'nacimiento'
    if O and not I and F: return 'crecimiento'
    if O and not I and not F: return 'madurez'
    if not O and I: return 'declive'
    return 'sacudon'
f['etapa'] = f.apply(etapa, axis=1)
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int); et = et.drop_duplicates(['id', 'ap'])[['id', 'ap', 'sic', 'tam', '_ret4']]
x = f.merge(et, on=['id', 'ap']); x['r'] = pd.to_numeric(x['_ret4'], errors='coerce'); x = x.dropna(subset=['sic', 'tam', 'r']).copy()
x['sic3'] = x['sic'].str[:3]; x['dec'] = np.minimum((x['tam'] * 10).astype(int), 9); g = ['ap', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy(); x['h'] = (x['r'] <= .5).astype(float)
print('empresas-año', len(x), x.etapa.value_counts().to_dict(), flush=True)
def tramo(z, nombre, etq, nperm=2000):
    z = z.copy(); z['sen'] = z['etapa'] == nombre
    z['hp'] = z['h'].where(~z['sen']).groupby([z[c] for c in g]).transform('mean'); z = z.dropna(subset=['hp'])
    lab = z['sen'].values; d = (z['h'] - z['hp']).values; gid = z.groupby(g).ngroup().values
    idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
    obs = d[lab].mean() * 100; P = []
    for _ in range(nperm):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        P.append(d[l2].mean() * 100)
    p = ((np.array(P) >= obs).sum() + 1) / (nperm + 1); s = z[lab]
    print(f'VI130 {etq:10s} {nombre:12s} n {lab.sum():6d} hundidas {s.h.mean()*100:5.1f} esperado {s.hp.mean()*100:5.1f} dif {obs:+.1f} p {p:.4f}', flush=True)
    return obs, p
res = {}
for e in ['declive', 'nacimiento', 'sacudon', 'crecimiento', 'madurez']: res[e] = tramo(x, e, '2010-2022', 2000 if e == 'declive' else 500)
d2, _ = tramo(x[x.ap >= 2017], 'declive', '2017-2022')
for y in sorted(x.ap.unique()):
    z = x[(x.ap == y)]; s = z[z.etapa == 'declive']
    print(f'  {y} declive n {len(s):4d} hundidas {s.h.mean()*100:5.1f} | todas {z.h.mean()*100:5.1f}', flush=True)
c, p = res['declive']
print('CRITERIO130', 'PASA' if c >= 3 and p < .05 and d2 > 0 else 'no pasa', f'(declive {c:+.1f} p {p:.4f}; 2017-2022 {d2:+.1f})')
