"""Señal #50 (notas/11): cuánto poner en cada empresa (Kelly). f = 2·P2 - PD, tope 5%.
Uso: python kelly.py filas.csv personas.csv FALLAS_CSVS [salida.json]
Las huellas se arman con el mismo código de direccion.py (#47)."""
import sys, os, json, time, hashlib
import numpy as np, pandas as pd

_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'direccion.py'), encoding='utf-8').read()
exec(_src.split('# etiqueta a 12 meses')[0])
from sklearn.ensemble import HistGradientBoostingClassifier
salida = sys.argv[4] if len(sys.argv) > 4 else 'kelly.json'
TOPE = 0.05

anio = df['anio'].values
ult = df.groupby('id')['anio'].transform('max')
quebro = (df['estado_final'].isin(['quiebra', 'revocada']) & (ult < df['anio'] + 1)).values
r1 = num_('_ret1').values.copy(); r1[np.isnan(r1) & quebro] = 0.0
en = ~np.isnan(r1)
dobla = (np.nan_to_num(r1, nan=1.0) >= 2).astype(int)
desastre = (np.nan_to_num(r1, nan=1.0) <= 0.5).astype(int)
COLS = NUM + PERS + FIN
hgb = lambda: HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15, l2_regularization=1.0, random_state=0)
def ajustar(A, y_, k):
    c = [x for x in COLS if R.loc[A, x].nunique() >= 3]
    return hgb().fit(R.loc[A, c].values, y_[A]).predict_proba(R.loc[k, c].values)[:, 1]
def pesos(p2, pdes):
    f = np.clip(2 * p2 - pdes, 0, None)
    if f.sum() <= 0:
        return f
    w = f / f.sum()
    for _ in range(100):                                       # tope 5%: lo que sobra va a las demás, en proporción
        sobre = w > TOPE + 1e-12
        if not sobre.any():
            break
        exceso = (w[sobre] - TOPE).sum(); w[sobre] = TOPE
        libres = (w < TOPE - 1e-12) & (f > 0)
        if not libres.any():
            break
        w[libres] += exceso * w[libres] / w[libres].sum()
    return w
res = {'camadas': {}}
for s in range(2019, 2025):
    A = en & (anio <= s - 2)
    k = np.where((anio == s) & en)[0]
    if A.sum() < mA or len(k) < mc:
        print(f'KELLY {s}: no alcanza (entrena {int(A.sum())}, prueba {len(k)})', flush=True); continue
    p2, pdes = ajustar(A, dobla, k), ajustar(A, desastre, k)
    w = pesos(p2, pdes); r = r1[k]; dentro = w > 0
    caja = 1 - w.sum()
    ret = float((w * r).sum() + caja)
    u = {'prom': round(float(r.mean()), 4), 'des': round(100 * float((r <= 0.5).mean()), 2), 'x2': round(100 * float((r >= 2).mean()), 2)}
    c = {'ret': round(ret, 4), 'des_peso': round(100 * float(w[r <= 0.5].sum()), 2), 'x2_peso': round(100 * float(w[r >= 2].sum()), 2),
         'empresas': int(dentro.sum()), 'en_tope': int((w >= TOPE - 1e-9).sum()), 'caja': round(float(caja), 4),
         'peso_max': round(float(w.max()), 4), 'tam_pond': round(float(np.nansum(w * np.nan_to_num(tam[k], nan=0.5)) / max(w.sum(), 1e-12)), 3)}
    fila = {'universo': u, 'kelly': c, 'gana_universo': bool(ret > u['prom']), 'menos_desastres': bool(c['des_peso'] < u['des'])}
    res['camadas'][s] = fila
    print(f'KELLY {s} (aprende hasta {s - 2}) | cartera ×{c["ret"]} | universo ×{u["prom"]} | des cartera {c["des_peso"]}% vs {u["des"]}% | '
          f'x2 cartera {c["x2_peso"]}% vs {u["x2"]}% | {c["empresas"]} empresas, {c["en_tope"]} en el tope, caja {c["caja"]}, tam {c["tam_pond"]}', flush=True)
    json.dump(res, open(salida, 'w'), indent=1)
C = res['camadas']; n = len(C)
g = sum(f['gana_universo'] for f in C.values()); d = sum(f['menos_desastres'] for f in C.values())
peor_c = min(f['kelly']['ret'] for f in C.values()) if n else None
peor_u = min(f['universo']['prom'] for f in C.values()) if n else None
acum = lambda xs: round(float(np.prod(xs)), 3)
res['criterio'] = {'camadas': n, 'gana_universo': f'{g} de {n}', 'peor_cartera': peor_c, 'peor_universo': peor_u, 'menos_desastres': f'{d} de {n}',
                   'acumulado': {'kelly': acum([f['kelly']['ret'] for f in C.values()]), 'universo': acum([f['universo']['prom'] for f in C.values()])},
                   'sobrevive': bool(n == 6 and g >= 5 and peor_c >= peor_u and d >= 5)}
print(f'CRITERIO Kelly (#50): {res["criterio"]} -> {"SOBREVIVE" if res["criterio"]["sobrevive"] else "se descarta"} ({time.time() - t0:.0f}s)', flush=True)
if res['criterio']['sobrevive'] or os.environ.get('PROBAR_CONGELADA'):   # la variable es sólo para la prueba local
    cuenta = pd.Series(anio).value_counts()
    ultimo = int(max(a_ for a_, n_ in cuenta.items() if n_ > int(os.environ.get('MIN_ULTIMO', 3000))))
    k = np.where(anio == ultimo)[0]
    A = en & (anio <= ultimo - 2)
    p2, pdes = ajustar(A, dobla, k), ajustar(A, desastre, k)
    w = pesos(p2, pdes)
    lista = pd.DataFrame({'id': df['id'].values[k], 'anio': ultimo, 'p_x2': np.round(p2, 6), 'p_desastre': np.round(pdes, 6), 'peso': np.round(w, 8)})
    lista.sort_values(['peso', 'p_x2'], ascending=False).to_csv('congelada_kelly.csv', index=False)
    h = hashlib.sha256(open('congelada_kelly.csv', 'rb').read()).hexdigest()
    res['congelada'] = {'anio': ultimo, 'empresas': int(len(k)), 'con_peso': int((w > 0).sum()), 'sha256': h}
    print(f'CONGELADA Kelly: año {ultimo}, {int((w > 0).sum())} con peso, sha256 {h}', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
