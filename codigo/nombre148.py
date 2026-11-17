"""Lectura (no prueba): palabras con más peso en el modelo firme de #146."""
import sys, collections, re; sys.argv = ['x', 'A']
exec(open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0])
e = json.load(open('sal-cab102/eleccion146.json')); cols, f = armar(e['dmin']); r = Ridge(alpha=e['alfa']).fit(f(Xa), ya)
hv0 = HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm=None, alternate_sign=False)
cnt = collections.Counter()
for o in CR[:800]: cnt.update(re.findall(r'\b[a-z]{2,}\b', (o.get('2020') or '').lower()))
nom = {}
for w, c in cnt.most_common(60000): nom.setdefault(hv0.transform([w]).indices[0], w)
o = np.argsort(r.coef_); w = lambda i: nom.get(cols[i], '?')
print('A FAVOR (esquivan hundidas):', ', '.join(w(i) for i in o[::-1][:50]))
print('EN CONTRA:', ', '.join(w(i) for i in o[:50]))
