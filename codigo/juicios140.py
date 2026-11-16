"""#140: palabras de juicios del Estado y multas ambientales en la sección 1, hundidas a 4 años contra pares. Reglas en notas/11 (#140)."""
import json, re, hashlib, numpy as np, pandas as pd, scipy.sparse as sp
from sklearn.feature_extraction.text import HashingVectorizer
rng = np.random.default_rng(0); B = '../fuentes'
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
L = ['qui', 'whistleblower', 'whistleblowers', 'injunctive', 'abatement', 'pollutant', 'pollutants', 'superfund', 'cercla', 'remediation', 'contamination',
     'contaminated', 'hazardous', 'subpoena', 'subpoenas', 'indictment', 'settlement', 'settlements']
hv = HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm=None, alternate_sign=False)
colsL = sorted({hv.transform([w]).indices[0] for w in L})
R = []
for y in range(2017, 2021):
    M = sp.load_npz(f'{B}/edgar-corpus/m1_{y}.npz').tocsr(); ciks = np.load(f'{B}/edgar-corpus/vec_{y}.npz')['ciks']
    sq = np.asarray(M.multiply(M).sum(axis=1)).ravel(); tasa = np.asarray(M[:, colsL].multiply(M[:, colsL]).sum(axis=1)).ravel()
    # frecuencia normalizada l2: la parte de la «energía» del texto en la lista; sirve para ordenar dentro del año
    R += [{'id': hs(int(c)), 'ap': y, 'tasa': t / s if s > 0 else np.nan} for c, t, s in zip(ciks, tasa, sq)]
pat = re.compile(r'\b(' + '|'.join(L) + r')\b')
for l in open(f'{B}/sec116/sec1.jsonl'):
    o = json.loads(l)
    for y in ('2021', '2022'):
        t = (o.get(y) or '').lower(); n = len(t.split())
        if n >= 300: R.append({'id': hs(o['cik']), 'ap': int(y), 'tasa': len(pat.findall(t)) / n * 1000})
R = pd.DataFrame(R).dropna().drop_duplicates(['id', 'ap'])
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['ap'] = et.anio_presentado.astype(int); et['r4'] = pd.to_numeric(et._ret4, errors='coerce')
x = R.merge(et.drop_duplicates(['id', 'ap'])[['id', 'ap', 'sic', 'tam', 'r4']], on=['id', 'ap']).dropna(subset=['sic', 'tam', 'r4'])
x = x[x.sic != '0000'].copy(); x['s3'] = x.sic.str[:3]; x['dec'] = np.minimum((x.tam * 10).astype(int), 9); x['h'] = (x.r4 <= .5).astype(float)
x['q'] = x.groupby('ap')['tasa'].transform(lambda v: pd.qcut(v.rank(method='first'), 5, labels=False))
gg = ['ap', 's3', 'dec']
def prueba(z, nom):
    z = z[z.groupby(gg)['id'].transform('size') >= 5].copy(); z['sen'] = z.q == 4
    z['hp'] = z['h'].where(~z.sen).groupby([z[c] for c in gg]).transform('mean'); z = z.dropna(subset=['hp'])
    lab = z.sen.values; dd = (z.h - z.hp).values; gid = z.groupby(gg).ngroup().values
    idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
    obs = dd[lab].mean() * 100; P = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        P.append(dd[l2].mean() * 100)
    p = ((np.array(P) >= obs).sum() + 1) / 2001; s = z[lab]
    por = ' '.join(f'{y}:{(s[s.ap==y].h.mean()-s[s.ap==y].hp.mean())*100:+.1f}' for y in sorted(s.ap.unique()))
    print(f'JU140 {nom} n {lab.sum()} hundidas {s.h.mean()*100:.1f} esperado {s.hp.mean()*100:.1f} dif {obs:+.1f} p {p:.4f} | {por}', flush=True); return obs, p
a, pa = prueba(x[x.ap <= 2020], '2017-2020'); b, pb = prueba(x[x.ap >= 2021], '2021-2022')
print('CRITERIO140', 'PASA' if a >= 3 and pa < .05 and b > 0 else 'no pasa')
