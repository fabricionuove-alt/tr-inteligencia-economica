"""Señal #48 (notas/11): magnitud × desastre × confirmación a los 3 meses.
Uso: python confirmacion.py filas.csv personas.csv FALLAS_CSVS PRECIOS_CSVS DIRECTIVOS_CSVS T13F_CSVS [salida.json]
Las huellas (números + personas + financiación) se arman con el mismo código de direccion.py (#47)."""
import sys, os, json, time, hashlib, collections
import numpy as np, pandas as pd

# huellas: la primera parte de direccion.py, tal cual (usa sys.argv[1..3])
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'direccion.py'), encoding='utf-8').read()
exec(_src.split('# etiqueta a 12 meses')[0])
from sklearn.ensemble import HistGradientBoostingClassifier
salida = sys.argv[7] if len(sys.argv) > 7 else 'confirmacion.json'

# precios, directivos y fondos
pr = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[4].split(',') if x]).sort_values('fuente', ascending=False, kind='stable')
mi = lambda s: s.str[:4].astype(int) * 12 + s.str[4:6].astype(int) - 1
P = {}
for i, m, p in zip(pr['id'], mi(pr['mes']), pr['precio']):
    P.setdefault((i, m), p)                                     # 'ftd' gana sobre 'directivos'
di = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str, 'dueno': str}) for x in sys.argv[5].split(',') if x])
vende = set(zip(di.loc[di['tipo'] == 'S', 'id'], mi(di.loc[di['tipo'] == 'S', 'mes'])))
tf = pd.concat([pd.read_csv(x, dtype={'id': str, 'periodo': str, 'fondo': str}) for x in sys.argv[6].split(',') if x])
tf['m'] = mi(tf['periodo'])
FON = tf.groupby(['id', 'm'])['acciones'].sum().to_dict()
per_fon = collections.defaultdict(list)
for (i, m) in FON:
    per_fon[i].append(m)
for i in per_fon:
    per_fon[i].sort()
del pr, di, tf
print(f'CONF precios {len(P)} | ventas de directivos {len(vende)} | tenencias de fondos {len(FON)} ({time.time() - t0:.0f}s)', flush=True)
def fondos_en(i, hasta):                                        # tenencia del último trimestre cerrado <= hasta
    ms = [m for m in per_fon.get(i, []) if m <= hasta]
    return FON[(i, ms[-1])] if ms else None
def precio(i, m, desf):
    for k in desf:
        p = P.get((i, m + k))
        if p is not None:
            return p
    return None

# resultados: a 12 meses desde el mes 0 (para entrenar) y desde el mes 3 (para medir)
anio = df['anio'].values
ult = df.groupby('id')['anio'].transform('max')
quebro = (df['estado_final'].isin(['quiebra', 'revocada']) & (ult < df['anio'] + 1)).values
r1 = num_('_ret1').values.copy(); r1[np.isnan(r1) & quebro] = 0.0
en = ~np.isnan(r1)
sig = clave.reindex(pd.MultiIndex.from_arrays([df['id'], df['anio'] + 1])).values
tsig = ~np.isnan(sig.astype(float)); sig = np.where(tsig, sig, 0).astype(int)
flujo = (num_('_dividendos').fillna(0) + num_('_recompras').fillna(0) - num_('_emisiones').fillna(0)).values
accv = acc.values
m0 = np.where(np.isnan(mp.values), np.nan, mp.values + 1)
p0 = np.full(len(df), np.nan); p3 = np.full(len(df), np.nan); rt = np.full(len(df), np.nan)
conf = np.zeros(len(df), bool)
for i, id_ in enumerate(df['id'].values):
    if np.isnan(m0[i]) or not (accv[i] > 0):
        continue
    m = int(m0[i])
    a, b = precio(id_, m, [0, 1, 2]), P.get((id_, m + 3))
    if a is None or b is None:
        continue
    p0[i], p3[i] = a, b
    pf = precio(id_, m + 15, [0, 1, -1])
    if pf is not None and tsig[i] and accv[sig[i]] > 0:
        x = (pf * accv[sig[i]] + flujo[sig[i]]) / (b * accv[i])
        if 0 < x < 20:
            rt[i] = x
    elif quebro[i]:
        rt[i] = 0.0
    sin_venta = not any((id_, m + k) in vende for k in range(3))
    fa_, fb_ = fondos_en(id_, m + 1), fondos_en(id_, m - 2)
    fondos_ok = fa_ is None and fb_ is None or (fa_ is not None and (fb_ is None or fa_ >= fb_))
    conf[i] = (b >= a) and sin_venta and fondos_ok
print(f'CONF con resultado tardío {int((~np.isnan(rt)).sum())} | confirmadas {int(conf[~np.isnan(rt)].sum())} ({time.time() - t0:.0f}s)', flush=True)

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
def candidatas(k, pm, pd_):
    alto = np.argsort(-pm)[:int(round(0.3 * len(k)))]
    return k[alto[pd_[alto] <= np.median(pd_[alto])]]
def met(ii):
    r = rt[ii]
    return {'n': int(len(ii)), 'x2': round(100 * float((r >= 2).mean()), 2) if len(r) else None,
            'des': round(100 * float((r <= 0.5).mean()), 2) if len(r) else None,
            'prom': round(float(r.mean()), 3) if len(r) else None, 'mediana': round(float(np.median(r)), 3) if len(r) else None,
            'tam': round(float(np.nanmean(tam[ii])), 3) if len(r) else None}
res = {'camadas': {}}
for s in range(2019, 2025):
    A = en & (anio <= s - 2)
    k = np.where((anio == s) & ~np.isnan(p0))[0]
    km = k[~np.isnan(rt[k])]
    if A.sum() < mA or len(km) < mc:
        print(f'CONF {s}: no alcanza (entrena {int(A.sum())}, prueba {len(km)})', flush=True); continue
    pm, pd_ = ajustar(A, extremo, k), ajustar(A, desastre, k)
    cand = candidatas(k, pm, pd_)
    cand = cand[~np.isnan(rt[cand])]
    eleg = cand[conf[cand]]
    fila = {'entrena_hasta': s - 2, 'universo': met(km), 'confirmadas_todas': met(km[conf[km]]), 'candidatas': met(cand), 'elegidas': met(eleg)}
    u, e = fila['universo'], fila['elegidas']
    fila['cumple'] = bool(e['n'] >= 30 and e['des'] < u['des'] and e['x2'] >= 1.3 * u['x2'])
    res['camadas'][s] = fila
    print(f'CONF {s} (aprende hasta {s - 2}; {"cumple" if fila["cumple"] else "no cumple"}) | ' + ' | '.join(
        f"{g}: n {v['n']} x2 {v['x2']}% des {v['des']}% prom {v['prom']} med {v['mediana']} tam {v['tam']}"
        for g, v in fila.items() if isinstance(v, dict)), flush=True)
    json.dump(res, open(salida, 'w'), indent=1)
n = len(res['camadas']); c = sum(f['cumple'] for f in res['camadas'].values())
res['criterio'] = {'camadas': n, 'cumple': f'{c} de {n}', 'sobrevive': bool(n == 6 and c >= 5)}
print(f'CRITERIO confirmación (#48): {res["criterio"]} -> {"SOBREVIVE" if res["criterio"]["sobrevive"] else "se descarta"} ({time.time() - t0:.0f}s)', flush=True)
if res['criterio']['sobrevive'] or os.environ.get('PROBAR_CONGELADA'):   # la variable es sólo para la prueba local
    cuenta = pd.Series(anio).value_counts()
    ultimo = int(max(a_ for a_, n_ in cuenta.items() if n_ > int(os.environ.get('MIN_ULTIMO', 3000))))
    k = np.where(anio == ultimo)[0]
    A = en & (anio <= ultimo - 2)
    pm, pd_ = ajustar(A, extremo, k), ajustar(A, desastre, k)
    cand = set(candidatas(k, pm, pd_))
    lista = pd.DataFrame({'id': df['id'].values[k], 'anio': ultimo, 'mes_compra': m0[k], 'puntaje_extremo': np.round(pm, 6),
                          'puntaje_desastre': np.round(pd_, 6), 'candidata': [int(x in cand) for x in k]})
    lista.sort_values(['candidata', 'puntaje_extremo'], ascending=False).to_csv('congelada_confirmacion.csv', index=False)
    h = hashlib.sha256(open('congelada_confirmacion.csv', 'rb').read()).hexdigest()
    res['congelada'] = {'anio': ultimo, 'empresas': int(len(k)), 'candidatas': len(cand), 'sha256': h}
    print(f'CONGELADA confirmación: año {ultimo}, {len(k)} empresas, {len(cand)} candidatas, sha256 {h}', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
