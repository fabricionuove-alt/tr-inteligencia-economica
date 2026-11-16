"""#147: ¿la señal de #146 es sólo el largo de la descripción? Reglas en notas/11 (#147)."""
import sys; sys.argv = ['x', 'A']
exec(open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0])
e = json.load(open('sal-cab102/eleccion146.json')); cols, f = armar(e['dmin']); r = Ridge(alpha=e['alfa']).fit(f(Xa), ya)
Xp, yp, idp, anp = juntar(range(2017, 2021)); pal = r.predict(f(Xp))
L = np.empty(len(idp))
for y in range(2017, 2021):
    _, ids = palabras(y); l1 = np.load(f'{B}/edgar-corpus/vec_{y}.npz')['l1']; prim = {}
    for i, h in enumerate(ids): prim.setdefault(h, l1[i])
    k = anp == y; L[k] = [prim[h] for h in idp[k]]
ll = np.log1p(L); print('correlacion puntaje vs log(palabras)', round(np.corrcoef(pal, ll)[0, 1], 3), flush=True)
res = pal.copy()
for y in range(2017, 2021):
    k = anp == y; b = np.polyfit(ll[k], pal[k], 1); res[k] = pal[k] - np.polyval(b, ll[k])
obs, p, por = prueba(pd.DataFrame({'id': idp, 'anio_presentado': anp, 'pal': res}), range(2017, 2021), 'PA147 resto sin largo')
obs2, p2, _ = prueba(pd.DataFrame({'id': idp, 'anio_presentado': anp, 'pal': ll}), range(2017, 2021), 'PA147 (informativo) sólo el largo')
print('CRITERIO147', 'PASA: no es sólo el largo' if obs <= -2 and p < .05 else 'no pasa')
