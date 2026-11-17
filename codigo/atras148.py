"""#148: el modelo firme de #146 en 2010-2012. Reglas en notas/11 (#148)."""
import sys; sys.argv = ['x', 'A']
exec(open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0])
e = json.load(open('sal-cab102/eleccion146.json')); cols, f = armar(e['dmin']); r = Ridge(alpha=e['alfa']).fit(f(Xa), ya)
D = []
for y in (2010, 2011, 2012):
    M, ids = palabras(y); _, prim = np.unique(ids, return_index=True)
    D.append(pd.DataFrame({'id': ids[prim], 'anio_presentado': y, 'pal': r.predict(f(M[prim]))}))
obs, p, por = prueba(pd.concat(D), (2010, 2011, 2012), 'PA148')
print('CRITERIO148', 'PASA' if obs <= -3 and p < .05 and sum(v < 0 for v in por.values()) >= 2 else 'no pasa')
