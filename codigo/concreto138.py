"""#138: concreción (Brysbaert 2014) de la sección 1 vs parcial «negocio» de Gemma y hundidas, 2017-2020. Reglas en notas/11 (#138)."""
import hashlib, numpy as np, pandas as pd, scipy.sparse as sp
from scipy.stats import spearmanr
from sklearn.feature_extraction.text import HashingVectorizer
rng = np.random.default_rng(0); B = '../fuentes'
hs = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
hv = HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm=None, alternate_sign=False)
br = pd.read_csv(f'{B}/brysbaert/concrecion.txt', sep='\t'); br = br[(br.Bigram == 0) & br.Word.astype(str).str.fullmatch(r'[a-z]{2,}')]
col = hv.transform(br.Word.tolist()).tocoo().col if False else np.array([hv.transform([w]).indices[0] for w in br.Word])
s = np.zeros(2 ** 20); n = np.zeros(2 ** 20); np.add.at(s, col, br['Conc.M'].values); np.add.at(n, col, 1)
tiene = n > 0; conc = np.where(tiene, s / np.maximum(n, 1), 0.0); print('palabras con puntaje', len(br), 'columnas', tiene.sum(), flush=True)
C = []
for y in range(2017, 2021):
    M = sp.load_npz(f'{B}/edgar-corpus/m1_{y}.npz').tocsr(); ciks = np.load(f'{B}/edgar-corpus/vec_{y}.npz')['ciks']
    num = M @ conc; den = M @ tiene.astype(float)
    C.append(pd.DataFrame({'id': [hs(int(c)) for c in ciks], 'anio_presentado': y, 'concrecion': np.where(den > 0, num / np.maximum(den, 1e-12), np.nan)}))
C = pd.concat(C).dropna().drop_duplicates(['id', 'anio_presentado'])
m = np.load('sal-junto3/out/gemma_1_1A_7_modelo.npz'); u = m['usar']; sec = u // 16384; F = []
for y in range(2017, 2021):
    X = sp.load_npz(f'sal-junto3/sae2aT-{y}-L12.npz').tocsr(); ids = np.load(f'sal-junto3/sae2aT-{y}-ids.npy', allow_pickle=True); X.data[~np.isfinite(X.data)] = 0
    Z = np.log1p(X[:, u].toarray() / m['med']); Z = (Z - m['mu']) / m['sd']
    F.append(pd.DataFrame({'id': ids.astype(str), 'anio_presentado': y, 'negocio': Z[:, sec == 0] @ m['coef'][sec == 0]}))
d = pd.concat(F).merge(C, on=['id', 'anio_presentado'])
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et.anio_presentado.astype(int); et['r4'] = pd.to_numeric(et._ret4, errors='coerce')
for y, z in d.groupby('anio_presentado'): print(f'  A {y} n {len(z)} rho concrecion-negocio {spearmanr(z.concrecion, z.negocio)[0]:+.2f} | concrecion media {z.concrecion.mean():.3f}', flush=True)
A = [spearmanr(z.concrecion, z.negocio)[0] for _, z in d.groupby('anio_presentado')]
x = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'tam', 'r4']], on=['id', 'anio_presentado']).dropna(subset=['sic', 'tam', 'r4'])
x = x[x.sic != '0000'].copy(); x['s3'] = x.sic.str[:3]; x['s2'] = x.sic.str[:2]; x['dec'] = np.minimum((x.tam * 10).astype(int), 9); x['ttam'] = np.minimum((x.tam * 3).astype(int), 2); x['h'] = (x.r4 <= .5).astype(float)
x['g'] = ''
for y, z in x.groupby('anio_presentado'): x.loc[z.index, 'g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2'])
x['top'] = x.groupby(['anio_presentado', 'g'])['negocio'].rank(pct=True) > .9
x['qc'] = x.groupby('anio_presentado')['concrecion'].transform(lambda v: pd.qcut(v.rank(method='first'), 5, labels=False))
def prueba(sen, gg, lado, nom):
    z = x[x.groupby(gg)['id'].transform('size') >= 5].copy(); z['sen'] = sen.loc[z.index]
    z['hp'] = z['h'].where(~z.sen).groupby([z[c] for c in gg]).transform('mean'); z = z.dropna(subset=['hp'])
    lab = z.sen.values; dd = (z.h - z.hp).values; gid = z.groupby(gg).ngroup().values
    idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
    obs = dd[lab].mean() * 100; P = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        P.append(dd[l2].mean() * 100)
    P = np.array(P); p = (((P >= obs) if lado > 0 else (P <= obs)).sum() + 1) / 2001; s = z[lab]
    print(f'{nom} n {lab.sum()} hundidas {s.h.mean()*100:.1f} esperado {s.hp.mean()*100:.1f} dif {obs:+.1f} p {p:.4f}', flush=True); return obs, p
b, pb = prueba(x.qc == 0, ['anio_presentado', 's3', 'dec'], 1, 'B quintil mas abstracto vs pares')
c0, _ = prueba(x.top, ['anio_presentado', 's2', 'ttam'], -1, 'C0 top negocio vs pares sin igualar concrecion')
c, pc = prueba(x.top, ['anio_presentado', 's2', 'ttam', 'qc'], -1, 'C top negocio vs pares de igual concrecion')
print('CRITERIO138 A', 'pasa' if all(r > 0 for r in A) else 'no pasa', '| B', 'pasa' if b >= 3 and pb < .05 else 'no pasa',
      '| C', 'la concrecion explica buena parte' if c > -1.5 else 'la ventaja sigue con igual concrecion')
