"""#152: modelo firme reaprendido con 2017-2020, probado en 2021-2022. Reglas en notas/11 (#152)."""
import sys; sys.argv = ['x', 'A']
src = open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0]
assert src.count('juntar(range(2013, 2017))') == 1; exec(src.replace('juntar(range(2013, 2017))', 'juntar(range(2017, 2021))'))
r1 = open('rinde149.py', encoding='utf-8').read(); exec(r1[r1.index('def rinde'):r1.index('Xp, yp, idp, anp = juntar')])
cols, f = armar(.02); r = Ridge(alpha=10000).fit(f(Xa), ya); print('aprendido 2017-2020', Xa.shape[0], 'descripciones,', len(cols), 'columnas', flush=True)
T = pd.DataFrame([{'id': hs(o['cik']), 'anio_presentado': int(y), 't': o[y]} for o in CR for y in ('2021', '2022') if len((o.get(y) or '').split()) >= 300]).drop_duplicates(['id', 'anio_presentado'])
T['pal'] = r.predict(f(hvl.transform(T.t.tolist()))); d = T.drop(columns='t')
oa, pa, por = prueba(d, (2021, 2022), 'A152 hundidas')
ob, pb = rinde(d, (2021, 2022), 'B152 log r4')
print('CRITERIO152', 'PASA' if ob > .078 and pb < .05 and oa <= -3 and pa < .05 and all(v < 0 for v in por.values()) else 'no pasa')
