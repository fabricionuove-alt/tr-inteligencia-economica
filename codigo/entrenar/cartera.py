"""Señal #49 (notas/11): la cartera 80/20. 80% en lo seguro (D bajo) + 20% repartido en las candidatas (M alto, D bajo).
Uso: python cartera.py filas.csv personas.csv FALLAS_CSVS [salida.json]
Las huellas se arman con el mismo código de direccion.py (#47)."""
import sys, os, json, time, hashlib
import numpy as np, pandas as pd

_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'direccion.py'), encoding='utf-8').read()
exec(_src.split('# etiqueta a 12 meses')[0])
from sklearn.ensemble import HistGradientBoostingClassifier
salida = sys.argv[4] if len(sys.argv) > 4 else 'cartera.json'

anio = df['anio'].values
ult = df.groupby('id')['anio'].transform('max')
quebro = (df['estado_final'].isin(['quiebra', 'revocada']) & (ult < df['anio'] + 1)).values
r1 = num_('_ret1').values.copy(); r1[np.isnan(r1) & quebro] = 0.0
en = ~np.isnan(r1)
extremo = np.zeros(len(df), int); desastre = (np.nan_to_num(r1, nan=1.0) <= 0.5).astype(int)
for a_ in np.unique(anio[en]):
    k = en & (anio == a_)
    if k.sum() >= 50:
        hi, lo = np.quantile(r1[k], 0.9), np.quantile(r1[k], 0.1)
        extremo[k & ((r1 >= hi) | (r1 <= lo))] = 1
COLS = NUM + PERS + FIN
hgb = lambda: HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15, l2_regularization=1.0, random_state=0)
def ajustar(A, y_, k):
    c = [x for x in COLS if R.loc[A, x].nunique() >= 3]
    return hgb().fit(R.loc[A, c].values, y_[A]).predict_proba(R.loc[k, c].values)[:, 1]
def partes(k, pm, pd_):
    seguro = k[np.argsort(pd_)[:int(round(0.2 * len(k)))]]
    alto = np.argsort(-pm)[:int(round(0.3 * len(k)))]
    cand = k[alto[pd_[alto] <= np.median(pd_[alto])]]
    return seguro, cand
def met(ii):
    r = r1[ii]
    return {'n': int(len(ii)), 'prom': round(float(r.mean()), 4), 'mediana': round(float(np.median(r)), 3),
            'x2': round(100 * float((r >= 2).mean()), 2), 'des': round(100 * float((r <= 0.5).mean()), 2), 'tam': round(float(np.nanmean(tam[ii])), 3)}
res = {'camadas': {}}
for s in range(2019, 2025):
    A = en & (anio <= s - 2)
    k = np.where((anio == s) & en)[0]
    if A.sum() < mA or len(k) < mc:
        print(f'CARTERA {s}: no alcanza (entrena {int(A.sum())}, prueba {len(k)})', flush=True); continue
    pm, pd_ = ajustar(A, extremo, k), ajustar(A, desastre, k)
    seg, cand = partes(k, pm, pd_)
    u, sg, ca = met(k), met(seg), met(cand)
    cart = round(0.8 * sg['prom'] + 0.2 * ca['prom'], 4)
    fila = {'universo': u, 'seguro': sg, 'candidatas': ca, 'cartera_80_20': cart,
            'gana_universo': bool(cart > u['prom']), 'gana_seguro': bool(cart > sg['prom'])}
    res['camadas'][s] = fila
    print(f'CARTERA {s} (aprende hasta {s - 2}) | cartera ×{cart} | universo ×{u["prom"]} | 100% seguro ×{sg["prom"]} | candidatas ×{ca["prom"]} | '
          + ' | '.join(f"{g}: n {v['n']} x2 {v['x2']}% des {v['des']}% med {v['mediana']} tam {v['tam']}" for g, v in fila.items() if isinstance(v, dict)), flush=True)
    json.dump(res, open(salida, 'w'), indent=1)
C = res['camadas']; n = len(C)
g1 = sum(f['gana_universo'] for f in C.values()); g3 = sum(f['gana_seguro'] for f in C.values())
peor_c = min(f['cartera_80_20'] for f in C.values()) if n else None
peor_u = min(f['universo']['prom'] for f in C.values()) if n else None
acum = lambda xs: round(float(np.prod(xs)), 3)
res['criterio'] = {'camadas': n, 'gana_universo': f'{g1} de {n}', 'peor_cartera': peor_c, 'peor_universo': peor_u,
                   'gana_seguro': f'{g3} de {n}',
                   'acumulado': {'cartera': acum([f['cartera_80_20'] for f in C.values()]), 'universo': acum([f['universo']['prom'] for f in C.values()]),
                                 'seguro': acum([f['seguro']['prom'] for f in C.values()])},
                   'sobrevive': bool(n == 6 and g1 >= 5 and peor_c >= peor_u and g3 >= 4)}
print(f'CRITERIO cartera 80/20 (#49): {res["criterio"]} -> {"SOBREVIVE" if res["criterio"]["sobrevive"] else "se descarta"} ({time.time() - t0:.0f}s)', flush=True)
if res['criterio']['sobrevive'] or os.environ.get('PROBAR_CONGELADA'):   # la variable es sólo para la prueba local
    cuenta = pd.Series(anio).value_counts()
    ultimo = int(max(a_ for a_, n_ in cuenta.items() if n_ > int(os.environ.get('MIN_ULTIMO', 3000))))
    k = np.where(anio == ultimo)[0]
    A = en & (anio <= ultimo - 2)
    pm, pd_ = ajustar(A, extremo, k), ajustar(A, desastre, k)
    seg, cand = partes(k, pm, pd_)
    parte = np.where(np.isin(k, seg), 'seguro', '') ; parte = np.where(np.isin(k, cand), np.char.add(parte, np.where(parte == '', 'candidata', '+candidata')), parte)
    peso = 0.8 * np.isin(k, seg) / max(len(seg), 1) + 0.2 * np.isin(k, cand) / max(len(cand), 1)
    lista = pd.DataFrame({'id': df['id'].values[k], 'anio': ultimo, 'puntaje_extremo': np.round(pm, 6), 'puntaje_desastre': np.round(pd_, 6),
                          'parte': parte, 'peso': np.round(peso, 8)})
    lista.sort_values(['peso', 'puntaje_extremo'], ascending=False).to_csv('congelada_cartera.csv', index=False)
    h = hashlib.sha256(open('congelada_cartera.csv', 'rb').read()).hexdigest()
    res['congelada'] = {'anio': ultimo, 'empresas': int(len(k)), 'seguro': int(len(seg)), 'candidatas': int(len(cand)), 'sha256': h}
    print(f'CONGELADA cartera: año {ultimo}, {len(seg)} en lo seguro, {len(cand)} candidatas, sha256 {h}', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
