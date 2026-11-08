"""Señal #60 (notas/11): los proyectos de Davos («Top 10 Emerging Technologies») → sector → rendimiento después.
Uso: python davos.py tecnologias.csv [salida.json]. Patrones fijados en notas/11 antes de bajar las listas; medida idéntica a #59."""
import sys, re, json, csv, collections
import numpy as np
from agenda import TEMAS, mensual
PAT = {'salud': r'medic|health|biolog|genom|gene|cell|drug|vaccin|microbio|organ|diagnos|neuro|crispr|protein|enzym',
       'clima': r'solar|batter|hydrogen|carbon|fuel cell|perovskite|grid|renewab|fusion|electric vehicle|green|ammonia|fertil',
       'tecnologia': r'\bai\b|artificial intelligence|machine|quantum|comput|chip|sensor|internet of things|blockchain|5g|6g|robot|autonom|augmented|virtual|metaverse|semiconductor|neural|data|wireless|display|lidar|2d material|graphene',
       'defensa': r'space|satellite|drone|aircraft', 'energia': r'oil|natural gas|shale'}
A = collections.defaultdict(set)
for f in csv.DictReader(open(sys.argv[1], encoding='utf-8')):
    for k, p in PAT.items():
        if re.search(p, f['tecnologia'].lower()):
            A[int(f['anio'])].add(k)
A = {y: sorted(v) for y, v in sorted(A.items())}
print('LISTAS', A, flush=True)
P = {k: mensual(fd) for k, (_, fd) in TEMAS.items()}; spy = mensual('SPY')
def exceso(k, m0, h):
    p = P[k]
    if all(m in p for m in (m0, m0 + h)) and all(m in spy for m in (m0, m0 + h)):
        return np.log(p[m0 + h] / p[m0]) - np.log(spy[m0 + h] / spy[m0])
res = {'listas': A, 'h': {}}
for h in (12, 36):
    filas = []
    for y in A:
        on = [e for k in TEMAS if k in A[y] and (e := exceso(k, y * 12 + 5, h)) is not None]
        off = [e for k in TEMAS if k not in A[y] and (e := exceso(k, y * 12 + 5, h)) is not None]
        if on and off:
            filas.append({'anio': y, 'on': float(np.mean(on)), 'off': float(np.mean(off)), 'dif': float(np.mean(on) - np.mean(off)), 'n_on': len(on), 'n_off': len(off)})
            print(f'DAVOS h{h} {y} | en lista {np.mean(on):+.3f} ({len(on)}) | fuera {np.mean(off):+.3f} ({len(off)}) | dif {np.mean(on) - np.mean(off):+.3f}', flush=True)
    v = np.array([f['dif'] for f in filas]); g = np.random.default_rng(0)
    lo, hi = np.percentile([g.choice(v, len(v)).mean() for _ in range(2000)], [2.5, 97.5])
    r = {'por_anio': filas, 'media': round(float(v.mean()), 4), 'ic95': [round(float(lo), 4), round(float(hi), 4)],
         'anios_positivos': f'{int((v > 0).sum())} de {len(v)}', 'pasa': bool(lo > 0 and (v > 0).mean() >= 0.7)}
    res['h'][h] = r
    print(f'CRITERIO h{h}: media {r["media"]:+.4f} IC95 {r["ic95"]} | positivos {r["anios_positivos"]} -> {"PASA" if r["pasa"] else "no pasa"}', flush=True)
json.dump(res, open(sys.argv[2] if len(sys.argv) > 2 else 'davos.json', 'w'), indent=1)
