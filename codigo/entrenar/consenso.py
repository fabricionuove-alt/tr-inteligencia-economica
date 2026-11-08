"""EXPLORACIÓN: consenso persistente = menciones del sector en Davos + Bilderberg en los últimos 3 años (t-2..t)."""
import re, csv, collections
import numpy as np
from agenda import agenda, mensual, TEMAS
from davos2 import CAT
amp = {'tecnologia': {'ia', 'chips', 'cuantica', 'robotica', 'blockchain', 'comunicaciones', 'realidad_virtual'}, 'salud': {'genomica', 'farmacos', 'diagnostico'},
       'clima': {'solar', 'hidrogeno', 'carbono', 'baterias'}, 'defensa': {'espacio'}, 'energia': set(), 'finanzas': set(), 'china': set(), 'europa': set(),
       'india': set(), 'emergentes': set(), 'oriente': set(), 'ciber': set()}
D = collections.defaultdict(collections.Counter)
for f in csv.DictReader(open('../fuentes/foros/wef/tecnologias.csv', encoding='utf-8')):
    for k, (p, _) in CAT.items():
        if re.search(p, f['tecnologia'].lower()):
            for a, sub in amp.items():
                if k in sub: D[int(f['anio'])][a] += 1
B = agenda('../fuentes/foros')
spy = mensual('SPY'); Pa = {k: mensual(fd) for k, (_, fd) in TEMAS.items()}
def ex(k, m0, h):
    p = Pa[k]
    return float(np.log(p[m0 + h] / p[m0]) - np.log(spy[m0 + h] / spy[m0])) if all(m in p and m in spy for m in (m0, m0 + h)) else None
for h in (12, 36, 60):
    por = collections.defaultdict(list); filas = []
    for y in range(2010, 2026):
        for k in TEMAS:
            e = ex(k, y * 12 + 5, h)
            if e is None: continue
            s = sum((k in B.get(t, [])) + (D[t][k] > 0) for t in (y - 2, y - 1, y))
            por[min(s, 4)].append(e); filas.append((y, s, e))
    print(f'h{h}: ' + ' | '.join(f'consenso {n}: {np.mean(v):+.3f} (n {len(v)})' for n, v in sorted(por.items())))
    # correlación de rango dentro de cada año (que no sea la época)
    rs = []
    for y in sorted({f[0] for f in filas}):
        f = [(s, e) for yy, s, e in filas if yy == y]
        if len(f) >= 6 and len({s for s, _ in f}) > 1:
            a = np.argsort(np.argsort([s for s, _ in f])); b = np.argsort(np.argsort([e for _, e in f]))
            rs.append(np.corrcoef(a, b)[0, 1])
    rs = np.array(rs); print(f'      rango dentro del año: media {rs.mean():+.3f}, positiva en {(rs > 0).sum()} de {len(rs)}')
print('CASOS consenso >= 4 (a 36 m):')
for y in range(2010, 2026):
    for k in TEMAS:
        s = sum((k in B.get(t, [])) + (D[t][k] > 0) for t in (y - 2, y - 1, y))
        if s >= 4: print(f'   {y} {k:10s} consenso {s} | 36m {ex(k, y*12+5, 36)} | 12m {ex(k, y*12+5, 12)}')
print('TECNOLOGIA por consenso (a 36 m):', {s: round(float(np.mean(v)), 3) for s, v in sorted(collections.defaultdict(list, {}).items())})
t = collections.defaultdict(list)
for y in range(2010, 2024):
    e = ex('tecnologia', y*12+5, 36)
    if e is not None: t[sum(('tecnologia' in B.get(x, [])) + (D[x]['tecnologia'] > 0) for x in (y-2, y-1, y))].append((y, round(e, 3)))
print('   ', dict(t))
