"""#157: palabras firmes filtran (20% de arriba por industria), Gemma reaprendido elige la mitad de arriba. Reglas en notas/11 (#157)."""
src = open('juntas156.py', encoding='utf-8').read(); exec(src[:src.index("d['pal'] = (")])
k = ['anio_presentado', 'g']; d['fp'] = d.groupby(k)['pw'].rank(pct=True) > .8
d['pal'] = 0.0; f2 = d[d.fp].copy(); f2['q'] = f2.groupby(k)['gem'].rank(pct=True)
d.loc[f2.index, 'pal'] = np.where(f2.q > .5, 2.0, 1.0)            # prueba() elige el 10% de arriba: estas valen 2
d['pal'] += d.groupby(k)['gem'].rank(pct=True) * 1e-3              # desempate dentro de cada nivel
x = d[['id', 'anio_presentado', 'pal']]
oa, pa, _ = prueba(x, range(2019, 2023), 'A157 en fila hundidas'); ob, pb = rinde(x, range(2019, 2023), 'B157 en fila log r4')
npos = sum(rinde(x[x.anio_presentado == y], (y,), f'  B157 {y}')[0] > 0 for y in range(2019, 2023))
print('CRITERIO157', 'PASA' if oa <= -4 and pa < .05 and ob > 0 and pb < .05 and npos >= 3 else 'no pasa', f'(log r4 positivo en {npos} de 4)')
