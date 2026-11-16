"""#146: modelo de palabras más regularizado, elegido por estabilidad (sin retornos). Reglas en notas/11 (#146).
python robusto146.py A  -> elige el modelo y prueba 2017-2020 (guarda la elección en sal-cab102/eleccion146.json)
python robusto146.py B  -> con esa elección, prueba 2021-2022 con el texto de edgar-crawler"""
import sys, json
from scipy.stats import spearmanr
exec(open('palabras139.py', encoding='utf-8').read().split('Xa, ya, _, _ = juntar')[0])
modo = sys.argv[1]
hvl = HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm='l2', alternate_sign=False)
Xa, ya, _, _ = juntar(range(2013, 2017)); print('aprender', Xa.shape, flush=True)
dfa = np.asarray((Xa > 0).sum(axis=0)).ravel() / Xa.shape[0]
def armar(dmin):
    cols = np.where(dfa >= dmin)[0]
    return cols, (lambda X: (lambda Y: (Y.data.__setitem__(slice(None), np.log1p(1000 * Y.data)), Y)[1])(X[:, cols].tocsr().astype(float).copy()))
CR = [json.loads(l) for l in open(f'{B}/crawler145/sec1.jsonl', encoding='utf-8')]
def prueba(d, anios, nombre):
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
    por = {y: (s[s.anio_presentado == y].h.mean() - s[s.anio_presentado == y].hp.mean()) * 100 for y in anios}
    print(f'{nombre} n {lab.sum()} hundidas {s.h.mean()*100:.1f} esperado {s.hp.mean()*100:.1f} dif {obs:+.1f} p {p:.4f} | ' + ' '.join(f'{y}:{v:+.1f}' for y, v in por.items()), flush=True)
    return obs, p, por
if modo == 'A':
    Xp, yp, idp, anp = juntar(range(2017, 2021))
    M20, ids20 = palabras(2020); l1 = np.load(f'{B}/edgar-corpus/vec_2020.npz')['l1']; fila = {}
    for i, h in enumerate(ids20):
        if l1[i] >= 300 and h not in fila: fila[h] = i
    par = [(fila[hs(o['cik'])], o['2020']) for o in CR if len((o.get('2020') or '').split()) >= 300 and hs(o['cik']) in fila]
    Ve = M20[[a for a, _ in par]]; Vc = hvl.transform([t for _, t in par]); print('empresas para estabilidad', len(par), flush=True)
    R = []
    for dmin in (.02, .10):
        cols, f = armar(dmin)
        for al in (1, 10, 100, 1000, 10000):
            r = Ridge(alpha=al).fit(f(Xa), ya)
            est = spearmanr(r.predict(f(Ve)), r.predict(f(Vc)))[0]; cg = np.corrcoef(r.predict(f(Xp)), yp)[0, 1]
            R.append((dmin, al, len(cols), est, cg)); print(f'df>={dmin} alfa {al}: columnas {len(cols)} estabilidad {est:+.3f} corr Gemma 2017-2020 {cg:+.3f}', flush=True)
    ok = [x for x in R if x[3] >= .90]; el = max(ok, key=lambda x: x[4]) if ok else max(R, key=lambda x: x[3])
    print('ELEGIDO', el, '' if ok else '(ninguno llega a 0,90: el más estable)', flush=True)
    json.dump({'dmin': el[0], 'alfa': el[1], 'estabilidad': el[3], 'n_estab': len(par)}, open('sal-cab102/eleccion146.json', 'w'))
    cols, f = armar(el[0]); r = Ridge(alpha=el[1]).fit(f(Xa), ya)
    obs, p, por = prueba(pd.DataFrame({'id': idp, 'anio_presentado': anp, 'pal': r.predict(f(Xp))}), range(2017, 2021), 'PA146')
    print('CRITERIO146A', 'PASA' if obs <= -2 and p < .05 else 'no pasa')
else:
    e = json.load(open('sal-cab102/eleccion146.json')); cols, f = armar(e['dmin']); r = Ridge(alpha=e['alfa']).fit(f(Xa), ya); print('eleccion', e, flush=True)
    T = [{'id': hs(o['cik']), 'anio_presentado': int(y), 't': o[y]} for o in CR for y in ('2021', '2022') if len((o.get(y) or '').split()) >= 300]
    T = pd.DataFrame(T).drop_duplicates(['id', 'anio_presentado']); T['pal'] = r.predict(f(hvl.transform(T.t.tolist()))); print('textos 2021-2022', len(T), flush=True)
    obs, p, por = prueba(T.drop(columns='t'), (2021, 2022), 'PB146')
    print('CRITERIO146B', 'PASA' if obs <= -3 and p < .05 and all(v < 0 for v in por.values()) else 'no pasa')
