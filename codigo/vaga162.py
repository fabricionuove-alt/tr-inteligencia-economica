"""#162 (base de #161): entre las elegidas de Tr (palabras #146), las atadas a un cliente grande (#160) contra las otras. Reglas en notas/11 (#161)."""
import sys; sys.argv = ['x', 'A']
src = open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0]
src = src.replace("Xa, ya, _, _ = juntar(range(2013, 2017)); print('aprender', Xa.shape, flush=True)\n", '').replace("dfa = np.asarray((Xa > 0).sum(axis=0)).ravel() / Xa.shape[0]\n", '')
exec(src)
r1 = open('rinde149.py', encoding='utf-8').read(); exec(r1[r1.index('def rinde'):r1.index('Xp, yp, idp, anp = juntar')])
MP = np.load('../repo-tr/modelos/palabras146.npz')
def pal(V):
    V = V[:, MP['cols']].tocsr().astype(float); V.data = np.log1p(1000 * V.data); return V @ MP['coef'] + MP['b']
D = []
for y in range(2010, 2021):
    M, ids = palabras(y); l1 = np.load(f'{B}/edgar-corpus/vec_{y}.npz')['l1']; k = np.where(l1 >= 300)[0]
    D.append(pd.DataFrame({'id': ids[k], 'anio_presentado': y, 'pal': pal(M[k])}))
for y in (2021, 2022):
    T = [(hs(o['cik']), o[str(y)]) for o in CR if len((o.get(str(y)) or '').split()) >= 300]
    D.append(pd.DataFrame({'id': [a for a, _ in T], 'anio_presentado': y, 'pal': pal(hvl.transform([t for _, t in T]))}))
d = pd.concat(D).drop_duplicates(['id', 'anio_presentado'])
C = pd.DataFrame([{'id': hs(int(o['cik'])), 'anio_presentado': y, 'c': o['c']} for y in range(2010, 2023) for o in map(json.loads, open(f'{B}/clientes160/c_{y}.jsonl')) if o['c'] is not None]).drop_duplicates(['id', 'anio_presentado'])
d = d.merge(C, on=['id', 'anio_presentado'], how='left'); d['at'] = d.c.fillna(0) > 0
et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et.anio_presentado.astype(int); et['r4'] = pd.to_numeric(et._ret4, errors='coerce')
x = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'tam', 'r4']], on=['id', 'anio_presentado']).dropna(subset=['sic', 'tam', 'r4'])
x = x[x.sic != '0000'].copy(); x['s3'] = x.sic.str[:3]; x['s2'] = x.sic.str[:2]; x['dec'] = np.minimum((x.tam * 10).astype(int), 9); x['lr'] = np.log(np.maximum(x.r4, .01)); x['h'] = (x.r4 <= .5).astype(float)
x['g'] = ''
for y, z in x.groupby('anio_presentado'): x.loc[z.index, 'g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2'])
x['arr'] = x.groupby(['anio_presentado', 'g'])['pal'].rank(pct=True) > .5
gg = ['anio_presentado', 's3', 'dec']; z = x[x.groupby(gg)['id'].transform('size') >= 5].copy()
z['lrp'] = z['lr'].where(~z['at']).groupby([z[k] for k in gg]).transform('mean'); z = z.dropna(subset=['lrp']); z['dl'] = z.lr - z.lrp
def comparar(anios, arr, nom):
    e = z[(z.arr == arr) & z.anio_presentado.isin(anios)]; a = e['at'].values; v = e.dl.values; obs = v[a].mean() - v[~a].mean(); P = []
    grupos = [np.where(e.anio_presentado.values == y)[0] for y in anios]
    for _ in range(2000):
        a2 = a.copy()
        for ii in grupos: a2[ii] = rng.permutation(a2[ii])
        P.append(v[a2].mean() - v[~a2].mean())
    p = ((np.array(P) <= obs).sum() + 1) / 2001
    por = {y: e[(e.anio_presentado == y) & e['at']].dl.mean() - e[(e.anio_presentado == y) & ~e['at']].dl.mean() for y in anios}
    print(f'{nom}: n {len(e)}, atadas {a.sum()} | atadas menos no atadas, log r4 {obs:+.3f} (x{np.exp(obs):.3f}) p {p:.4f} | ' + ' '.join(f'{y}:{w:+.2f}' for y, w in por.items()), flush=True)
    return obs, p
A = range(2010, 2021); N = (2021, 2022)
ob, pb = comparar(A, False, 'C162 mitad de ABAJO 2010-2020'); oa, pa = comparar(A, True, 'C162 mitad de ARRIBA 2010-2020')
nb, _ = comparar(N, False, 'C162 mitad de ABAJO 2021-2022'); comparar(N, True, 'C162 mitad de ARRIBA 2021-2022')
print('CRITERIO162', 'PASA' if ob < 0 and pb < .05 and ob < oa and nb < 0 else 'no pasa')
