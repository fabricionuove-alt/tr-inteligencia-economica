"""EXPLORACIÓN (no es prueba): seguir la pista de #59-#61 desde varios ángulos. Lo que salga se confirma aparte."""
import re, csv, collections, json
import numpy as np
from agenda import agenda, mensual
from davos2 import CAT
D = collections.defaultdict(set)
for f in csv.DictReader(open('../fuentes/foros/wef/tecnologias.csv', encoding='utf-8')):
    for k, (p, _) in CAT.items():
        if re.search(p, f['tecnologia'].lower()): D[int(f['anio'])].add(k)
P = {fd: mensual(fd) for fd in {fd for _, fd in CAT.values()}}; spy = mensual('SPY')
def ex(k, m0, h):
    p = P[CAT[k][1]]
    return float(np.log(p[m0 + h] / p[m0]) - np.log(spy[m0 + h] / spy[m0])) if all(m in p and m in spy for m in (m0, m0 + h)) else None
# 1. cuándo aparece: exceso acumulado mes a mes, en lista menos fuera
print('1. CURVA (meses: diferencia media entre años, años positivos)')
for h in (3, 6, 12, 18, 24, 30, 36, 48, 60):
    v = []
    for y in D:
        on = [e for k in CAT if k in D[y] and (e := ex(k, y * 12 + 5, h)) is not None]
        off = [e for k in CAT if k not in D[y] and (e := ex(k, y * 12 + 5, h)) is not None]
        if on and off: v.append(np.mean(on) - np.mean(off))
    v = np.array(v); print(f'   {h:2d} m: {v.mean():+.3f}  ({(v > 0).sum()} de {len(v)})')
# 2. nueva contra repetida
print('2. NUEVA (no estaba en la lista del año anterior disponible) contra REPETIDA, a 36 m')
anios = sorted(D); nue, rep, off_ = [], [], []
for i, y in enumerate(anios):
    prev = D[anios[i - 1]] if i else set()
    for k in CAT:
        e = ex(k, y * 12 + 5, 36)
        if e is None: continue
        if k in D[y]: (rep if k in prev else nue).append(e)
        else: off_.append(e)
print(f'   nueva {np.mean(nue):+.3f} (n {len(nue)}) | repetida {np.mean(rep):+.3f} (n {len(rep)}) | fuera {np.mean(off_):+.3f} (n {len(off_)})')
# 3. cuántas tecnologías de la lista caen en la categoría (intensidad)
print('3. INTENSIDAD (cuántas de las 10 caen en la categoría), a 36 m')
cnt = collections.defaultdict(collections.Counter)
for f in csv.DictReader(open('../fuentes/foros/wef/tecnologias.csv', encoding='utf-8')):
    for k, (p, _) in CAT.items():
        if re.search(p, f['tecnologia'].lower()): cnt[int(f['anio'])][k] += 1
por = collections.defaultdict(list)
for y in D:
    for k in CAT:
        e = ex(k, y * 12 + 5, 36)
        if e is not None: por[min(cnt[y][k], 2)].append(e)
print('   ' + ' | '.join(f'{n} tecnologías: {np.mean(v):+.3f} (n {len(v)})' for n, v in sorted(por.items())))
# 4. dos foros: Bilderberg (proyectos contra problemas) y coincidencia con Davos
B = agenda('../fuentes/foros')
BT = {}
import glob, html as H
for p in sorted(glob.glob('../fuentes/foros/tema-*.html')):
    y = int(re.search(r'tema-(\d{4})', p).group(1)); s = open(p, 'rb').read().decode('utf-8', 'ignore')
    t = H.unescape(re.sub(r'<[^>]+>', '\n', re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S))).lower()
    BT[y] = t
PROB = r'crisis|threat|terror|war\b|warfare|weapon|risk|challenge|populism|proliferation|disinformation|fragment|inequality|debt'
print('4. BILDERBERG: tema escrito como PROBLEMA contra como PROYECTO (sectores amplios de #59), a 36 m')
from agenda import TEMAS
Pa = {k: mensual(fd) for k, (_, fd) in TEMAS.items()}
def ex2(k, m0, h):
    p = Pa[k]
    return float(np.log(p[m0 + h] / p[m0]) - np.log(spy[m0 + h] / spy[m0])) if all(m in p and m in spy for m in (m0, m0 + h)) else None
prob, proy, fuera = [], [], []
for y, temas in B.items():
    lineas = [l.strip() for l in BT[y].split('\n') if l.strip()]
    for k in TEMAS:
        e = ex2(k, y * 12 + 5, 36)
        if e is None: continue
        if k not in temas: fuera.append(e); continue
        ls = [l for l in lineas if re.search(TEMAS[k][0], l) and len(l) < 200]
        (prob if ls and all(re.search(PROB, l) for l in ls) else proy).append(e)
print(f'   proyecto {np.mean(proy):+.3f} (n {len(proy)}) | problema {np.mean(prob):+.3f} (n {len(prob)}) | fuera {np.mean(fuera):+.3f} (n {len(fuera)})')
print('5. COINCIDENCIA: categoría amplia en Davos y en Bilderberg el mismo año, a 36 m')
amp = {'tecnologia': {'ia', 'chips', 'cuantica', 'robotica', 'blockchain', 'comunicaciones', 'realidad_virtual'}, 'salud': {'genomica', 'farmacos', 'diagnostico'},
       'clima': {'solar', 'hidrogeno', 'carbono', 'baterias'}, 'defensa': {'espacio'}}
dos, uno, nada = [], [], []
for y in D:
    if y not in B: continue
    for k, sub in amp.items():
        e = ex2(k, y * 12 + 5, 36)
        if e is None: continue
        enD, enB = bool(D[y] & sub), k in B[y]
        (dos if enD and enB else uno if enD or enB else nada).append(e)
print(f'   los dos {np.mean(dos):+.3f} (n {len(dos)}) | uno {np.mean(uno):+.3f} (n {len(uno)}) | ninguno {np.mean(nada) if nada else float("nan"):+.3f} (n {len(nada)})')
