"""Tr v2: red neuronal (perceptrón de dos capas, 5 semillas) con todo lo de Tr + cuánto habla cada empresa de los temas de la élite.
Uso: python trv2.py filas.csv personas.csv FALLAS_CSVS TEMA10K_CSVS [salida.json]
Compara, camada por camada (2019-2024, cada una aprende con ≤ s-2), la cartera Kelly de:
  tr   = Tr actual (árboles, rasgos de #50)       | red  = red neuronal, mismos rasgos
  tr+t = árboles + temas                          | red+t = red neuronal + temas  (candidata a Tr v2)
Criterio (notas/11 #63, escrito antes): Tr v2 reemplaza a Tr si gana a Tr en ≥ 4 de 6, a universo en ≥ 5 de 6,
y su peso en desastres no supera al de Tr en más de 1 punto en ≥ 4 de 6.
Con FINAL=1 entrena con todo y arma la cartera de la última camada (lista congelada)."""
import sys, os, json, time
import numpy as np, pandas as pd
_aqui = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_aqui, 'kelly.py'), encoding='utf-8').read().split("res = {'camadas': {}}")[0])
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_auc_score
salida = sys.argv[5] if len(sys.argv) > 5 else 'trv2.json'
t1 = time.time()
T = pd.concat([pd.read_csv(x, dtype={'id': str}) for x in sys.argv[4].split(',') if x]).drop_duplicates(['id', 'anio_presentado'])
temas = [c for c in T.columns if c.startswith(('b_', 't_'))]
T = T[T['palabras'] >= 300].copy()
dens = T[temas].div(T['palabras'], axis=0) * 1000
dens['tema_total'] = dens.sum(axis=1)
T = pd.concat([T[['id', 'anio_presentado']], dens], axis=1)
pres = pd.to_numeric(df['_presentado'].astype(str).str[:4], errors='coerce')
j = pd.DataFrame({'i': df.index, 'id': df['id'], 'anio_presentado': pres}).merge(T, on=['id', 'anio_presentado'], how='left')
TEM = []
for c in temas + ['tema_total']:
    v = pd.Series(j[c].values, index=j['i'].values).reindex(df.index)
    R['tem_' + c] = v.groupby(df['anio']).rank(pct=True); TEM.append('tem_' + c)
print(f'TRV2 temas con dato: {int(R["tem_tema_total"].notna().sum())} filas; por año {R["tem_tema_total"].notna().groupby(df["anio"]).sum().to_dict()} ({time.time() - t1:.0f}s)', flush=True)

def matriz(cols, idx):
    X = R.loc[idx, cols].values.astype(float)
    falta = np.isnan(X); X = np.where(falta, 0.5, X)
    return np.hstack([X, falta.astype(float)])
def red(cols, A, y_, k, semillas=3):
    c = [x for x in cols if R.loc[A, x].nunique() >= 3]
    XA, Xk = matriz(c, A), matriz(c, k); p = np.zeros(len(k))
    for s in range(semillas):
        m = MLPClassifier(hidden_layer_sizes=(128, 64), alpha=1e-3, learning_rate_init=1e-3, batch_size=256, max_iter=60,
                          early_stopping=True, validation_fraction=0.15, n_iter_no_change=6, random_state=s)
        p += m.fit(XA, y_[A]).predict_proba(Xk)[:, 1]
    return p / semillas
def arbol(cols, A, y_, k):
    c = [x for x in cols if R.loc[A, x].nunique() >= 3]
    return hgb().fit(R.loc[A, c].values, y_[A]).predict_proba(R.loc[k, c].values)[:, 1]
def cartera(p2, pdes, r):
    w = pesos(p2, pdes); m = (r >= 2) | (r <= 0.5)
    lado = float(roc_auc_score((r[m] >= 2).astype(int), (p2 - pdes)[m])) if m.sum() > 20 else np.nan
    return {'ret': round(float((w * r).sum() + 1 - w.sum()), 4), 'des': round(100 * float(w[r <= 0.5].sum()), 2), 'lado': round(lado, 4), 'empresas': int((w > 0).sum())}
VAR = {'tr': (arbol, COLS), 'red': (red, COLS), 'tr+t': (arbol, COLS + TEM), 'red+t': (red, COLS + TEM)}

if os.environ.get('FINAL') == '1':
    ultima = int(anio.max()); A = en.copy(); k = np.where(anio == ultima)[0]
    p2, pdes = red(COLS + TEM, A, dobla, k), red(COLS + TEM, A, desastre, k)
    w = pesos(p2, pdes)
    out = pd.DataFrame({'id': df['id'].values[k], 'anio': ultima, 'p2': p2.round(5), 'pdes': pdes.round(5), 'peso': w.round(6)})
    out = out[out['peso'] > 0].sort_values('peso', ascending=False)
    out.to_csv('trv2_congelada.csv', index=False)
    print(f'TRV2 FINAL camada {ultima}: {len(out)} empresas con peso, peso máximo {out["peso"].max():.4f}, temas con dato '
          f'{int(R.loc[k, "tem_tema_total"].notna().sum())} de {len(k)} ({time.time() - t1:.0f}s)', flush=True)
    sys.exit(0)

res = {'camadas': {}}
CAM = [int(x) for x in os.environ.get('CAMADAS', '2017,2018,2019').split(',')]
for s in CAM:
    A = en & (anio <= s - 2); k = np.where((anio == s) & en)[0]
    if A.sum() < mA or len(k) < mc:
        continue
    r = r1[k]; fila = {'universo': round(float(r.mean()), 4), 'des_universo': round(100 * float((r <= 0.5).mean()), 2)}
    for nombre, (f, cols) in VAR.items():
        fila[nombre] = cartera(f(cols, A, dobla, k), f(cols, A, desastre, k), r)
    res['camadas'][s] = fila
    print(f'TRV2 {s} | universo ×{fila["universo"]} | ' + ' | '.join(f'{n} ×{fila[n]["ret"]} des {fila[n]["des"]}% lado {fila[n]["lado"]}' for n in VAR) + f' ({time.time() - t1:.0f}s)', flush=True)
    json.dump(res, open(salida, 'w'), indent=1)
C = res['camadas']; n = len(C)
g_tr = sum(C[s]['red+t']['ret'] > C[s]['tr']['ret'] for s in C); g_u = sum(C[s]['red+t']['ret'] > C[s]['universo'] for s in C)
d_ok = sum(C[s]['red+t']['des'] <= C[s]['tr']['des'] + 1 for s in C)
res['criterio'] = {'gana_a_tr': f'{g_tr} de {n}', 'gana_universo': f'{g_u} de {n}', 'desastres_ok': f'{d_ok} de {n}', 'reemplaza': bool(n == 3 and g_tr >= 2 and g_u >= 3 and d_ok >= 2)}
for nombre in VAR:
    res['criterio']['acumulado_' + nombre] = round(float(np.prod([C[s][nombre]['ret'] for s in C])), 3)
print('CRITERIO TRV2:', res['criterio'], f'({time.time() - t1:.0f}s)', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
