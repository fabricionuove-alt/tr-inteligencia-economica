"""#136: promesa contra operación. Reglas en notas/11 (#136)."""
import numpy as np, pandas as pd
from scipy import sparse
m = np.load('sal-junto3/out/gemma_1_1A_7_modelo.npz')
def carga(npz, ids): return sparse.load_npz(npz).tocsr(), np.load(ids)
fil = [pd.read_csv('sal-junto3/out/gemma_1_1A_7_puntaje.csv', dtype={'id': str})]
for y in (2021, 2022):
    P = [carga(f'sal-anon2124/sae2a-textos-{y}-L12.npz', f'sal-anon2124/sae2a-textos-{y}-ids.npy'),
         carga(f'sal-lee{y}/sae2a-textos1A-{y}-L12.npz', f'sal-lee{y}/sae2a-textos1A-{y}-ids.npy'),
         carga(f'sal-lee{y}/sae2a-textos7-{y}-L12.npz', f'sal-lee{y}/sae2a-textos7-{y}-ids.npy')]
    com = sorted(set.intersection(*[set(i) for _, i in P])); pos = [{v: k for k, v in enumerate(i)} for _, i in P]
    X = sparse.hstack([x[[p[c] for c in com]] for (x, _), p in zip(P, pos)]).tocsr(); X.data[~np.isfinite(X.data)] = 0
    Z = np.log1p(X[:, m['usar']].toarray() / m['med']); Z = (Z - m['mu']) / m['sd']
    fil.append(pd.DataFrame({'id': com, 'anio_presentado': y, 'gemma': Z @ m['coef'] + m['b']}))
d = pd.concat(fil); d = d[d.anio_presentado >= 2017]
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['anio_presentado'] = et['anio_presentado'].astype(int); et['r1'] = pd.to_numeric(et['_ret1'], errors='coerce')
d = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'r1']], on=['id', 'anio_presentado']).dropna(subset=['r1', 'sic'])
d = d[d['sic'] != '0000']; d['s3'] = d.sic.str[:3]; d['s2'] = d.sic.str[:2]

import json, re, hashlib
from scipy.stats import spearmanr
rng = np.random.default_rng(0)
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
T = ['preclinical', 'clinical trial', 'clinical trials', 'investigational', 'product candidate', 'product candidates', 'phase 1', 'phase 2', 'phase 3',
     'bitcoin', 'cryptocurrency', 'blockchain', 'digital asset', 'digital assets', 'litigation', 'lawsuit', 'lawsuits', 'plaintiff', 'plaintiffs',
     'going concern', 'not generated any revenue', 'not yet generated revenue']
pat = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, T), key=len, reverse=True)) + r')\b')
P = []
for l in open('../fuentes/sec116/sec1.jsonl'):
    o = json.loads(l)
    for y in ('2021', '2022'):
        t = (o.get(y) or '').lower(); n = len(t.split())
        if n >= 300: P.append({'id': hs(o['cik']), 'anio_presentado': int(y), 'promesa': len(pat.findall(t)) / n * 1e4})
P = pd.DataFrame(P).drop_duplicates(['id', 'anio_presentado'])
et['r4'] = pd.to_numeric(et['_ret4'], errors='coerce')
x = d[d.anio_presentado.isin([2021, 2022])].merge(P, on=['id', 'anio_presentado']).merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'tam', 'r4']], on=['id', 'anio_presentado'])
x = x.dropna(subset=['tam']).copy(); print('empresas-año', len(x), x.groupby('anio_presentado').size().to_dict(), flush=True)
A = {y: spearmanr(z.promesa, z.gemma)[0] for y, z in x.groupby('anio_presentado')}
for y, r in A.items(): print(f'  A {y} rho promesa-gemma {r:+.2f}', flush=True)
x['g'] = ''
for y, z in x.groupby('anio_presentado'): x.loc[z.index, 'g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2'])
x['top'] = x.groupby(['anio_presentado', 'g'])['gemma'].rank(pct=True) > .9
x['qp'] = x.groupby('anio_presentado')['promesa'].transform(lambda v: pd.qcut(v.rank(method='first'), 5, labels=False))
x = x.dropna(subset=['r4']).copy(); x['h'] = (x.r4 <= .5).astype(float)
x['sic3'] = x.sic.str[:3]; x['dec'] = np.minimum((x.tam * 10).astype(int), 9); x['ttam'] = np.minimum((x.tam * 3).astype(int), 2)
def prueba(z, sen, gg, lado, nom):
    z = z[z.groupby(gg)['id'].transform('size') >= 5].copy(); z['sen'] = sen.loc[z.index]
    z['hp'] = z['h'].where(~z.sen).groupby([z[c] for c in gg]).transform('mean'); z = z.dropna(subset=['hp'])
    lab = z.sen.values; dd = (z.h - z.hp).values; gid = z.groupby(gg).ngroup().values
    idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
    obs = dd[lab].mean() * 100; Pm = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        Pm.append(dd[l2].mean() * 100)
    Pm = np.array(Pm); p = (((Pm >= obs) if lado > 0 else (Pm <= obs)).sum() + 1) / 2001; s = z[lab]
    print(f'{nom} n {lab.sum()} hundidas {s.h.mean()*100:.1f} esperado {s.hp.mean()*100:.1f} dif {obs:+.1f} p {p:.4f}', flush=True); return obs, p
b, pb = prueba(x, x.qp == 4, ['anio_presentado', 'sic3', 'dec'], 1, 'B quintil de mas promesa vs pares')
c, pc = prueba(x, x.top, ['anio_presentado', 's2', 'ttam', 'qp'], -1, 'C top Gemma vs pares de igual promesa')
c0, _ = prueba(x, x.top, ['anio_presentado', 's2', 'ttam'], -1, '  (para mirar) top Gemma vs pares sin igualar promesa')
print('CRITERIO136 A', 'pasa' if all(r < 0 for r in A.values()) else 'no pasa', '| B', 'pasa' if b >= 3 and pb < .05 else 'no pasa',
      '| C', 'Gemma ve algo mas que la promesa' if c <= -2 and pc < .05 else 'no: buena parte de lo que ve es la promesa')
