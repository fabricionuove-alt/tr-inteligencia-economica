"""Guarda el modelo firme de #146 (columnas, pesos) para Rt y comprueba que da lo mismo que el original."""
import sys; sys.argv = ['x', 'A']
exec(open('robusto146.py', encoding='utf-8').read().split("CR = [json.loads")[0])
e = json.load(open('sal-cab102/eleccion146.json')); cols, f = armar(e['dmin']); r = Ridge(alpha=e['alfa']).fit(f(Xa), ya)
np.savez_compressed('../repo-tr/modelos/palabras146.npz', cols=cols.astype(np.int64), coef=r.coef_.astype(np.float64), b=np.float64(r.intercept_))
m = np.load('../repo-tr/modelos/palabras146.npz')
t = [json.loads(l)['2021'] for l in open(f'{B}/crawler145/sec1.jsonl', encoding='utf-8') if len((json.loads(l).get('2021') or '').split()) >= 300][:50]
V = hvl.transform(t)[:, m['cols']].tocsr(); V.data = np.log1p(1000 * V.data)
print('diferencia máxima con el original', np.abs(V @ m['coef'] + m['b'] - r.predict(f(hvl.transform(t)))).max())
