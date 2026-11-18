"""#150: ventaja en rendimiento (log r4) del modelo firme en 2010-2012. Reglas en notas/11 (#150)."""
src = open('rinde149.py', encoding='utf-8').read().split('Xp, yp, idp, anp = juntar')[0]; exec(src)
D = []
for y in (2010, 2011, 2012):
    M, ids = palabras(y); _, prim = np.unique(ids, return_index=True)
    D.append(pd.DataFrame({'id': ids[prim], 'anio_presentado': y, 'pal': r.predict(f(M[prim]))}))
o, p = rinde(pd.concat(D), (2010, 2011, 2012), 'R150 2010-2012')
print('CRITERIO150', 'PASA' if o > 0 and p < .05 and o >= .294 else 'no pasa')
