"""#149: ¿las elegidas del modelo firme rinden más (log r4) que sus pares? Reglas en notas/11 (#149)."""
import sys; sys.argv = ['x', 'A']
exec(open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0])
e = json.load(open('sal-cab102/eleccion146.json')); cols, f = armar(e['dmin']); r = Ridge(alpha=e['alfa']).fit(f(Xa), ya)
def rinde(d, anios, nombre):
    et = pd.read_csv('colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado']); et['anio_presentado'] = et.anio_presentado.astype(int); et['r4'] = pd.to_numeric(et._ret4, errors='coerce')
    x = d.merge(et.drop_duplicates(['id', 'anio_presentado'])[['id', 'anio_presentado', 'sic', 'tam', 'r4']], on=['id', 'anio_presentado']).dropna(subset=['sic', 'tam', 'r4'])
    x = x[x.sic != '0000'].copy(); x['s3'] = x.sic.str[:3]; x['s2'] = x.sic.str[:2]; x['dec'] = np.minimum((x.tam * 10).astype(int), 9); x['h'] = np.log(np.maximum(x.r4, .01))
    x['g'] = ''
    for y, z in x.groupby('anio_presentado'): x.loc[z.index, 'g'] = np.where(z.groupby('s3')['id'].transform('size') >= 10, z['s3'], z['s2'])
    x['top'] = x.groupby(['anio_presentado', 'g'])['pal'].rank(pct=True) > .9
    gg = ['anio_presentado', 's3', 'dec']; z = x[x.groupby(gg)['id'].transform('size') >= 5].copy()
    z['hp'] = z['h'].where(~z.top).groupby([z[c] for c in gg]).transform('mean'); z['mp'] = z['r4'].where(~z.top).groupby([z[c] for c in gg]).transform('median'); z = z.dropna(subset=['hp'])
    lab = z.top.values; dd = (z.h - z.hp).values; gid = z.groupby(gg).ngroup().values
    idx = [ii for ii in (np.where(gid == k)[0] for k in np.unique(gid)) if lab[ii].any() and not lab[ii].all()]
    obs = dd[lab].mean(); P = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        P.append(dd[l2].mean())
    p = ((np.array(P) >= obs).sum() + 1) / 2001; s = z[lab]
    por = {y: s[s.anio_presentado == y].h.mean() - s[s.anio_presentado == y].hp.mean() for y in anios}
    print(f'{nombre} n {lab.sum()} dif log r4 {obs:+.3f} (x{np.exp(obs):.3f}) p {p:.4f} | mediana r4 elegidas {s.r4.median():.3f} pares {s.mp.median():.3f} | ' + ' '.join(f'{y}:{v:+.3f}' for y, v in por.items()), flush=True)
    return obs, p
Xp, yp, idp, anp = juntar(range(2017, 2021))
o1, p1 = rinde(pd.DataFrame({'id': idp, 'anio_presentado': anp, 'pal': r.predict(f(Xp))}), range(2017, 2021), 'R149 2017-2020')
T = pd.DataFrame([{'id': hs(o['cik']), 'anio_presentado': int(y), 't': o[y]} for o in CR for y in ('2021', '2022') if len((o.get(y) or '').split()) >= 300]).drop_duplicates(['id', 'anio_presentado'])
T['pal'] = r.predict(f(hvl.transform(T.t.tolist())))
o2, p2 = rinde(T.drop(columns='t'), (2021, 2022), 'R149 2021-2022')
print('CRITERIO149', 'PASA' if o1 > 0 and p1 < .05 and o2 > 0 and p2 < .05 else 'no pasa')
