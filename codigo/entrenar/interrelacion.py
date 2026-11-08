"""Señal #43 (notas/11): la interrelación. Un modelo aprende lo extraordinario con todas las huellas juntas
(números + trayectoria + personas) y se compara con cada bloque solo y de a pares.
Uso: python interrelacion.py filas.csv trayectorias.csv personas.csv [salida.json]
Etiqueta: múltiplo a 6 años (_ret6, quiebra = 0) en el 10% más alto de su camada.
Validación cruzada de 5 partes por empresa; AUC dentro del mismo quintil de tamaño."""
import sys, os, json, time
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score

t0 = time.time()
salida = sys.argv[4] if len(sys.argv) > 4 else 'interrelacion.json'
mc = int(os.environ.get('MIN_CAMADA', 300))
df = pd.read_csv(sys.argv[1], low_memory=False)
df = df[df['anio'] >= 2009].drop(columns=[c for c in ['anios_hist'] if c in df.columns]).reset_index(drop=True)

# NÚMEROS: mismos rasgos y mismo pase a percentil que analizar.py
ETIQ = ['sobrevive_10', 'sobrevive_10_amplio', 'duplica_6', 'gana_mas_1', 'precio_duplica_6', 'precio_gana_1']
NO_RASGO = {'id', 'anio', 'estado_final', 'altman_z2', 'ohlson_o', 'piotroski_f'} | set(ETIQ)
BINARIOS = {'patrimonio_neg', 'sin_deuda', 'perdida', 'financiera'}
rasgos = [c for c in df.columns if c not in NO_RASGO and not c.startswith('_') and df[c].notna().sum() > 100]
num = [c for c in rasgos if c not in BINARIOS and c != 'sector']
rng0 = np.random.default_rng(42)
R = pd.DataFrame(index=df.index)
for c in num:
    v = pd.to_numeric(df[c], errors='coerce')
    v = v + rng0.random(len(df)) * 1e-9 * (v.abs().max() if v.notna().any() else 1)
    p = v.groupby(df['anio']).rank(pct=True, method='first')
    R[c] = p.where(p.notna(), pd.Series(rng0.random(len(df)), index=df.index))
for c in sorted(BINARIOS & set(df.columns)):   # ordenado: el orden de un set cambia en cada corrida
    R[c] = df[c].fillna(pd.Series(rng0.integers(0, 2, len(df)), index=df.index)).astype(float)
R['sector'] = df['sector'].astype(float)
NUM = list(R.columns)
tam = pd.to_numeric(df['log_activos'], errors='coerce').groupby(df['anio']).rank(pct=True)

# TRAYECTORIA
tr = pd.read_csv(sys.argv[2], dtype={'id': str})
TRAY = [c for c in tr.columns if c.startswith('tr_')]
R = R.join(df[['id', 'anio']].merge(tr, on=['id', 'anio'], how='left').drop(columns=['id', 'anio']).set_index(df.index))

# PERSONAS: el último trimestre 13F (fecha de compra) anterior o igual al mes de compra de la fila
pe = pd.read_csv(sys.argv[3], dtype={'id': str, 'mes': str})
pe['m'] = pe['mes'].str[:4].astype(int) * 12 + pe['mes'].str[4:6].astype(int) - 1; pe = pe.sort_values('m')   # meses corridos
pe['creyentes_sobre_fondos'] = pe['creyentes'] / pe['fondos_antes'].replace(0, np.nan)
PERS = ['cambio12', 'creyentes', 'fondos_antes', 'compras', 'ventas', 'creyentes_sobre_fondos']
pres = df['_presentado'].astype(str)
ok = pres.str.len() >= 7
m0 = pd.Series(np.nan, index=df.index)
m0[ok] = pres[ok].str[:4].astype(int) * 12 + pres[ok].str[5:7].astype(int) - 1 + 1     # mes siguiente a presentar
q = pd.DataFrame({'i': df.index, 'id': df['id'], 'm': m0}).dropna(subset=['m'])
q['m'] = q['m'].astype(int); q = q.sort_values('m')
j = pd.merge_asof(q, pe[['id', 'm'] + PERS], on='m', by='id', direction='backward', tolerance=6)
for c in PERS:
    R[c] = np.nan
    R.loc[j['i'].values, c] = j[c].values

# etiqueta
r6 = pd.to_numeric(df['_ret6'], errors='coerce')
en = (df['anio'] >= 2013) & (df['anio'] <= 2019) & r6.notna()
corte = r6[en].groupby(df.loc[en, 'anio']).transform(lambda s: s.quantile(0.9))
y = pd.Series(np.nan, index=df.index); y[en] = (r6[en] >= corte).astype(float)
idx = np.where(en)[0]
print(f'INTER filas {len(idx)} | con trayectoria {int(R.loc[idx, "tr_frac"].notna().sum())} | con personas {int(R.loc[idx, "fondos_antes"].notna().sum())} '
      f'| corte del 10% por camada {corte.groupby(df.loc[en, "anio"]).first().round(2).to_dict()} ({time.time() - t0:.0f}s)', flush=True)

MODELOS = {'numeros': NUM, 'trayectoria': TRAY, 'personas': PERS, 'num+tray': NUM + TRAY, 'num+pers': NUM + PERS,
           'tray+pers': TRAY + PERS, 'todo': NUM + TRAY + PERS}
gk = GroupKFold(n_splits=5)
grupos = df['id'].values[idx]; Y = y.values[idx].astype(int)
oof = {}
for nom, cols in MODELOS.items():
    cols = [c for c in cols if R.iloc[idx][c].nunique() >= 3]        # una columna casi constante rompe el algoritmo
    Xm = R.iloc[idx][cols].values
    o = np.zeros(len(idx))
    for a, b in gk.split(Xm, Y, grupos):
        m = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15, l2_regularization=1.0,
                                           random_state=0).fit(Xm[a], Y[a])
        o[b] = m.predict_proba(Xm[b])[:, 1]
    oof[nom] = o
    print(f'INTER modelo {nom} listo ({time.time() - t0:.0f}s)', flush=True)

anio = df['anio'].values[idx]; T = tam.values[idx]; RR = r6.values[idx]
qt = np.full(len(idx), -1)
for a_ in np.unique(anio):
    k = anio == a_
    qt[k] = pd.qcut(pd.Series(T[k]).rank(method='first'), 5, labels=False).values
res = {'camadas': {}}
for a_ in range(2013, 2020):
    k = anio == a_
    if k.sum() < mc:
        continue
    fila = {'n': int(k.sum())}
    u3 = float((RR[k] >= 3).mean()); ud = float((RR[k] <= 0.25).mean())
    fila['universo'] = {'x3': round(100 * u3, 2), 'des': round(100 * ud, 2)}
    for nom, o in oof.items():
        tot = w = 0
        for g in range(5):
            h = k & (qt == g)
            if h.sum() >= 30 and len(set(Y[h])) == 2:
                tot += roc_auc_score(Y[h], o[h]) * h.sum(); w += h.sum()
        s = o[k]; top = s >= np.quantile(s, 0.9)
        fila[nom] = {'auc_tam': round(tot / w, 3) if w else None,
                     'top10_x3': round(100 * float((RR[k][top] >= 3).mean()), 2), 'top10_des': round(100 * float((RR[k][top] <= 0.25).mean()), 2),
                     'top10_tam': round(float(np.nanmean(T[k][top])), 3)}
    res['camadas'][a_] = fila
    print(f'INTER {a_} n {fila["n"]} universo x3 {fila["universo"]["x3"]}% des {fila["universo"]["des"]}% | ' + ' | '.join(
        f"{nom}: auc {v['auc_tam']} top x3 {v['top10_x3']}% des {v['top10_des']}% tam {v['top10_tam']}" for nom, v in fila.items() if nom in MODELOS), flush=True)

C = res['camadas']
aucs = [f['todo']['auc_tam'] for f in C.values() if f['todo']['auc_tam'] is not None]
gana = sum(1 for f in C.values() if f['todo']['auc_tam'] is not None and
           f['todo']['auc_tam'] >= max(f[b]['auc_tam'] or 0 for b in ('numeros', 'trayectoria', 'personas')) + 0.01)
colas = sum(1 for f in C.values() if f['todo']['top10_x3'] > f['universo']['x3'] and f['todo']['top10_des'] <= f['universo']['des'])
n = len(C)
res['criterio'] = {'camadas': n, 'auc_tam_todo': round(float(np.mean(aucs)), 3) if aucs else None,
                   'auc_tam_por_modelo': {nom: round(float(np.mean([f[nom]['auc_tam'] for f in C.values() if f[nom]['auc_tam'] is not None])), 3) for nom in MODELOS},
                   'cruce_agrega': f'{gana} de {n}', 'colas_mejores': f'{colas} de {n}',
                   'pasa': bool(n == 7 and aucs and np.mean(aucs) >= 0.60 and gana >= 5 and colas >= 5)}
print(f'CRITERIO interrelación: {res["criterio"]} -> {"PASA" if res["criterio"]["pasa"] else "no pasa"} ({time.time() - t0:.0f}s)', flush=True)
json.dump(res, open(salida, 'w'), indent=1)

# SEÑAL #44 (notas/11): extremo × no hundirse. Modelo D de desastre a 6 años con las mismas huellas y la misma validación.
cols = [c for c in MODELOS['todo'] if R.iloc[idx][c].nunique() >= 3]
Xm = R.iloc[idx][cols].values
Yd = (RR <= 0.25).astype(int)
od = np.zeros(len(idx))
for a, b in gk.split(Xm, Yd, grupos):
    m = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15, l2_regularization=1.0,
                                       random_state=0).fit(Xm[a], Yd[a])
    od[b] = m.predict_proba(Xm[b])[:, 1]
oe = oof['todo']
r1v = pd.to_numeric(df['_ret1'], errors='coerce').values[idx] if '_ret1' in df.columns else np.full(len(idx), np.nan)
res['cruce'] = {}
for a_ in range(2013, 2020):
    k = np.where(anio == a_)[0]
    if len(k) < mc:
        continue
    n10 = max(1, int(round(0.1 * len(k))))
    seguro = k[od[k] <= np.median(od[k])]
    cruce = seguro[np.argsort(-oe[seguro])[:n10]]
    solo_e = k[np.argsort(-oe[k])[:n10]]
    solo_d = k[np.argsort(od[k])[:n10]]
    def met(ii):
        r = RR[ii]; r1 = r1v[ii]; r1 = r1[~np.isnan(r1)]
        return {'n': int(len(ii)), 'x3': round(100 * float((r >= 3).mean()), 2), 'des': round(100 * float((r <= 0.25).mean()), 2),
                'prom6': round(float(r.mean()), 3), 'mediana6': round(float(np.median(r)), 3),
                'prom12m': round(float(r1.mean()), 3) if len(r1) else None, 'tam': round(float(np.nanmean(T[ii])), 3)}
    auc_d = roc_auc_score(Yd[k], od[k]) if len(set(Yd[k])) == 2 else None
    fila = {'auc_desastre': round(auc_d, 3) if auc_d else None, 'universo': met(k), 'cruce': met(cruce), 'solo_extremo': met(solo_e), 'solo_seguro': met(solo_d)}
    res['cruce'][a_] = fila
    print(f'CRUCE {a_} auc D {fila["auc_desastre"]} | ' + ' | '.join(
        f"{g}: x3 {v['x3']}% des {v['des']}% prom6 {v['prom6']} med6 {v['mediana6']} prom12 {v['prom12m']} tam {v['tam']}"
        for g, v in fila.items() if isinstance(v, dict)), flush=True)
C = res['cruce']
c1 = sum(1 for f in C.values() if f['cruce']['x3'] > f['universo']['x3'] and f['cruce']['des'] <= f['universo']['des'])
c2 = sum(1 for f in C.values() if f['cruce']['prom6'] > f['universo']['prom6'])
c3 = sum(1 for f in C.values() if f['cruce']['x3'] > f['solo_seguro']['x3'])
res['criterio_cruce'] = {'camadas': len(C), 'colas_mejores': f'{c1} de {len(C)}', 'promedio_mayor': f'{c2} de {len(C)}',
                         'mas_x3_que_solo_seguro': f'{c3} de {len(C)}', 'pasa': bool(len(C) == 7 and c1 >= 5 and c2 >= 5 and c3 >= 5)}
print(f'CRITERIO cruce: {res["criterio_cruce"]} -> {"PASA" if res["criterio_cruce"]["pasa"] else "no pasa"} ({time.time() - t0:.0f}s)', flush=True)
json.dump(res, open(salida, 'w'), indent=1)

# SEÑAL #45 (notas/11): el cruce FUERA DE TIEMPO + lista congelada.
import hashlib
anioA = df['anio'].values; r6A = r6.values; tamA = tam.values
r1A = pd.to_numeric(df['_ret1'], errors='coerce').values if '_ret1' in df.columns else np.full(len(df), np.nan)
enT = (anioA >= 2009) & (anioA <= 2019) & ~np.isnan(r6A)
cortes = {a_: np.quantile(r6A[enT & (anioA == a_)], 0.9) for a_ in np.unique(anioA[enT])}
yE = np.array([r6A[i] >= cortes[anioA[i]] if enT[i] else False for i in range(len(df))]).astype(int)
yD = (np.nan_to_num(r6A, nan=1.0) <= 0.25).astype(int)
colsT = [c for c in MODELOS['todo'] if R.loc[enT, c].nunique() >= 3]
XA = R[colsT].values
hgb = lambda: HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15, l2_regularization=1.0, random_state=0)
def ajustar(A, y_, k):     # sólo columnas con dato en lo que aprende (un bloque que todavía no existía queda afuera)
    c = [j for j in range(XA.shape[1]) if pd.Series(XA[A, j]).nunique() >= 3]
    return hgb().fit(XA[A][:, c], y_[A]).predict_proba(XA[k][:, c])[:, 1], len(c)
def cruzar(k, pe_, pd_):
    n10 = max(1, int(round(0.1 * len(k))))
    seguro = k[pd_ <= np.median(pd_)]
    return seguro[np.argsort(-pe_[np.isin(k, seguro)])[:n10]], k[np.argsort(-pe_)[:n10]], k[np.argsort(pd_)[:n10]]
def met45(ii):
    r = r6A[ii]; r1 = r1A[ii]; r1 = r1[~np.isnan(r1)]
    return {'n': int(len(ii)), 'x3': round(100 * float((r >= 3).mean()), 2), 'des': round(100 * float((r <= 0.25).mean()), 2),
            'prom6': round(float(r.mean()), 3), 'mediana6': round(float(np.median(r)), 3),
            'prom12m': round(float(r1.mean()), 3) if len(r1) else None, 'tam': round(float(np.nanmean(tamA[ii])), 3)}
res['fuera_de_tiempo'] = {}
for s in range(2015, 2020):
    A = enT & (anioA <= s - 6)
    k = np.where((anioA == s) & ~np.isnan(r6A))[0]
    if A.sum() < 500 or len(k) < mc or len(set(yE[A])) < 2 or len(set(yD[A])) < 2:
        print(f'FUERA {s}: no alcanza (entrena {int(A.sum())})', flush=True); continue
    pe_, nc = ajustar(A, yE, k)
    pd_, _ = ajustar(A, yD, k)
    cr, so_e, so_d = cruzar(k, pe_, pd_)
    fila = {'entrena_hasta': s - 6, 'filas_entrena': int(A.sum()), 'columnas': nc,
            'auc_D': round(float(roc_auc_score(yD[k], pd_)), 3) if len(set(yD[k])) == 2 else None,
            'universo': met45(k), 'cruce': met45(cr), 'solo_extremo': met45(so_e), 'solo_seguro': met45(so_d)}
    res['fuera_de_tiempo'][s] = fila
    print(f'FUERA {s} (aprende con camadas hasta {s - 6}, {fila["filas_entrena"]} filas, {nc} columnas, auc D {fila["auc_D"]}) | ' + ' | '.join(
        f"{g}: x3 {v['x3']}% des {v['des']}% prom6 {v['prom6']} med6 {v['mediana6']} prom12 {v['prom12m']} tam {v['tam']}"
        for g, v in fila.items() if isinstance(v, dict)), flush=True)
C = res['fuera_de_tiempo']
f1 = sum(1 for f in C.values() if f['cruce']['x3'] > f['universo']['x3'] and f['cruce']['des'] <= f['universo']['des'])
f2 = sum(1 for f in C.values() if f['cruce']['prom6'] > f['universo']['prom6'])
f3 = sum(1 for f in C.values() if f['cruce']['x3'] > f['solo_seguro']['x3'])
res['criterio_fuera'] = {'camadas': len(C), 'colas_mejores': f'{f1} de {len(C)}', 'promedio_mayor': f'{f2} de {len(C)}',
                         'mas_x3_que_solo_seguro': f'{f3} de {len(C)}', 'pasa': bool(len(C) == 5 and f1 >= 4 and f2 >= 4 and f3 >= 4)}
print(f'CRITERIO fuera de tiempo: {res["criterio_fuera"]} -> {"PASA" if res["criterio_fuera"]["pasa"] else "no pasa"} ({time.time() - t0:.0f}s)', flush=True)

# lista congelada: aprende con 2009-2019, puntúa el último año completo
cuenta = pd.Series(anioA).value_counts()
ultimo = int(max(a_ for a_, n_ in cuenta.items() if n_ > int(os.environ.get('MIN_ULTIMO', 3000)))) if (cuenta > int(os.environ.get('MIN_ULTIMO', 3000))).any() else int(anioA.max())
k = np.where(anioA == ultimo)[0]
pe_, _ = ajustar(enT, yE, k)
pd_, _ = ajustar(enT, yD, k)
cr, _, _ = cruzar(k, pe_, pd_)
lista = pd.DataFrame({'id': df['id'].values[k], 'anio': ultimo, 'puntaje_extremo': np.round(pe_, 6), 'puntaje_desastre': np.round(pd_, 6)})
lista['elegida'] = np.isin(k, cr).astype(int)
lista = lista.sort_values(['elegida', 'puntaje_extremo'], ascending=False)
lista.to_csv('congelada_cruce.csv', index=False)
h = hashlib.sha256(open('congelada_cruce.csv', 'rb').read()).hexdigest()
res['congelada'] = {'anio': ultimo, 'empresas': int(len(k)), 'elegidas': int(lista['elegida'].sum()), 'sha256': h}
print(f'CONGELADA cruce: año {ultimo}, {len(k)} empresas, {int(lista["elegida"].sum())} elegidas, sha256 {h}', flush=True)
json.dump(res, open(salida, 'w'), indent=1)

# SEÑAL #46 (notas/11): magnitud × dirección, a 4 años, camadas 2020-2021 fuera de tiempo.
r4A = pd.to_numeric(df['_ret4'], errors='coerce').values if '_ret4' in df.columns else np.full(len(df), np.nan)
en4 = ~np.isnan(r4A)
arriba4 = np.zeros(len(df), int); abajo4 = np.zeros(len(df), int)
for a_ in np.unique(anioA[en4]):
    k = en4 & (anioA == a_)
    hi, lo = np.quantile(r4A[k], 0.9), np.quantile(r4A[k], 0.1)
    arriba4[k & (r4A >= hi)] = 1; abajo4[k & (r4A <= lo)] = 1
extremo4 = arriba4 | abajo4
def met46(ii):
    r = r4A[ii]
    return {'n': int(len(ii)), 'x2': round(100 * float((r >= 2).mean()), 2), 'des': round(100 * float((r <= 0.25).mean()), 2),
            'prom4': round(float(r.mean()), 3), 'mediana4': round(float(np.median(r)), 3), 'tam': round(float(np.nanmean(tamA[ii])), 3)}
res['magnitud_direccion'] = {}
for s in range(2017, 2022):
    A = en4 & (anioA <= s - 4)
    Ax = A & (extremo4 == 1)
    k = np.where((anioA == s) & en4)[0]
    if A.sum() < 500 or len(k) < mc or len(set(extremo4[A])) < 2 or len(set(arriba4[Ax])) < 2:
        print(f'MAGDIR {s}: no alcanza (entrena {int(A.sum())})', flush=True); continue
    pm, _ = ajustar(A, extremo4, k)
    pr_, _ = ajustar(Ax, arriba4, k)
    n10 = max(1, int(round(0.1 * len(k))))
    alto_m = k[np.argsort(-pm)[:int(round(0.3 * len(k)))]]
    elegidas = alto_m[np.argsort(-pr_[np.isin(k, alto_m)])[:n10]]
    solo_m = k[np.argsort(-pm)[:n10]]; solo_r = k[np.argsort(-pr_)[:n10]]
    ex_k = extremo4[k] == 1
    auc_m = roc_auc_score(extremo4[k], pm) if len(set(extremo4[k])) == 2 else None
    auc_r = roc_auc_score(arriba4[k][ex_k], pr_[ex_k]) if ex_k.sum() and len(set(arriba4[k][ex_k])) == 2 else None
    fila = {'entrena_hasta': s - 4, 'filas_entrena': int(A.sum()), 'extremas_entrena': int(Ax.sum()),
            'auc_M': round(float(auc_m), 3) if auc_m else None, 'auc_R_entre_extremas': round(float(auc_r), 3) if auc_r else None,
            'cuenta': s >= 2020, 'universo': met46(k), 'elegidas': met46(elegidas), 'solo_magnitud': met46(solo_m), 'solo_direccion': met46(solo_r)}
    res['magnitud_direccion'][s] = fila
    print(f'MAGDIR {s} ({"CUENTA" if s >= 2020 else "ya vista, no cuenta"}; aprende hasta {s - 4}, {fila["filas_entrena"]} filas, {fila["extremas_entrena"]} extremas; '
          f'auc M {fila["auc_M"]} auc R {fila["auc_R_entre_extremas"]}) | ' + ' | '.join(
        f"{g}: x2 {v['x2']}% des {v['des']}% prom4 {v['prom4']} med4 {v['mediana4']} tam {v['tam']}" for g, v in fila.items() if isinstance(v, dict)), flush=True)
C = {s: f for s, f in res['magnitud_direccion'].items() if f['cuenta']}
g1 = sum(1 for f in C.values() if f['elegidas']['x2'] > f['universo']['x2'] and f['elegidas']['des'] <= f['universo']['des'])
g2 = sum(1 for f in C.values() if f['elegidas']['prom4'] > f['universo']['prom4'])
res['criterio_magdir'] = {'camadas': len(C), 'colas_mejores': f'{g1} de {len(C)}', 'promedio_mayor': f'{g2} de {len(C)}',
                          'pasa': bool(len(C) == 2 and g1 == 2 and g2 == 2)}
print(f'CRITERIO magnitud×dirección: {res["criterio_magdir"]} -> {"PASA" if res["criterio_magdir"]["pasa"] else "no pasa"} ({time.time() - t0:.0f}s)', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
