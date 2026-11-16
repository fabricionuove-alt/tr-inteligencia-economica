"""#145: valida edgar-crawler contra EDGAR-CORPUS en 2020 y repite la prueba de #143 en 2021-2022. Reglas en notas/11 (#145)."""
import json
import numpy as np, pandas as pd
from scipy.stats import spearmanr
exec(open('palabras139.py', encoding='utf-8').read().split('Xp, yp, idp, anp = juntar')[0])
hvl = HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm='l2', alternate_sign=False)
T = []
for l in open(f'{B}/crawler145/sec1.jsonl', encoding='utf-8'):
    o = json.loads(l)
    for y in ('2020', '2021', '2022'):
        t = o.get(y) or ''
        if len(t.split()) >= 300: T.append({'id': hs(o['cik']), 'anio_presentado': int(y), 'pal': float(r.predict(f(hvl.transform([t])))[0])})
T = pd.DataFrame(T).drop_duplicates(['id', 'anio_presentado'])
# paso 1: validación 2020
M, ids = palabras(2020); a = pd.DataFrame({'id': ids, 'edgar': r.predict(f(M))}).drop_duplicates('id')
v = a.merge(T[T.anio_presentado == 2020], on='id'); rho = spearmanr(v.edgar, v.pal)[0]
print(f'CR145 validacion 2020: {len(v)} empresas, Spearman con EDGAR-CORPUS {rho:+.3f}', flush=True)
if rho < .85:
    print('CRITERIO145 la herramienta no reproduce EDGAR-CORPUS: no se usa'); raise SystemExit
# paso 2: 2021-2022
d = T[T.anio_presentado >= 2021]
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et.anio_presentado.astype(int); et['r4'] = pd.to_numeric(et._ret4, errors='coerce')
x = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'tam', 'r4']], on=['id', 'anio_presentado']).dropna(subset=['sic', 'tam', 'r4'])
x = x[x.sic != '0000'].copy(); x['s3'] = x.sic.str[:3]; x['s2'] = x.sic.str[:2]; x['dec'] = np.minimum((x.tam * 10).astype(int), 9); x['h'] = (x.r4 <= .5).astype(float)
x['g'] = ''
for y, z in x.groupby('anio_presentado'): x.loc[z.index, 'g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2'])
x['top'] = x.groupby(['anio_presentado', 'g'])['pal'].rank(pct=True) > .9
gg = ['anio_presentado', 's3', 'dec']; z = x[x.groupby(gg)['id'].transform('size') >= 5].copy()
z['hp'] = z['h'].where(~z.top).groupby([z[c] for c in gg]).transform('mean'); z = z.dropna(subset=['hp'])
lab = z.top.values; dd = (z.h - z.hp).values; gid = z.groupby(gg).ngroup().values
idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
obs = dd[lab].mean() * 100; P = []
for _ in range(2000):
    l2 = lab.copy()
    for ii in idx: l2[ii] = rng.permutation(l2[ii])
    P.append(dd[l2].mean() * 100)
p = ((np.array(P) <= obs).sum() + 1) / 2001; s = z[lab]
por = {y: (s[s.anio_presentado == y].h.mean() - s[s.anio_presentado == y].hp.mean()) * 100 for y in (2021, 2022)}
print(f'CR145 top palabras 2021-2022 n {lab.sum()} hundidas {s.h.mean()*100:.1f} esperado {s.hp.mean()*100:.1f} dif {obs:+.1f} p {p:.4f} | ' + ' '.join(f'{y}:{v:+.1f}' for y, v in por.items()))
print('CRITERIO145', 'PASA' if obs <= -3 and p < .05 and all(v < 0 for v in por.values()) else 'no pasa')
