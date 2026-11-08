"""Señal #47 (notas/11): quién financia el salto. ¿Hacia qué lado rompe una empresa que se va a un extremo?
Uso: python direccion.py filas.csv personas.csv FALLAS_CSVS [salida.json]
Horizonte 12 meses (_ret1, quiebra = 0). Camadas de prueba 2022-2024; cada una aprende sólo con camadas <= s-2."""
import sys, os, json, time
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

t0 = time.time()
salida = sys.argv[4] if len(sys.argv) > 4 else 'direccion.json'
mc = int(os.environ.get('MIN_CAMADA', 300)); mA = int(os.environ.get('MIN_ENTRENA', 500))
df = pd.read_csv(sys.argv[1], low_memory=False)
df = df[df['anio'] >= 2009].drop(columns=[c for c in ['anios_hist'] if c in df.columns]).reset_index(drop=True)
num_ = lambda c: pd.to_numeric(df[c], errors='coerce') if c in df.columns else pd.Series(np.nan, index=df.index)

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
for c in sorted(BINARIOS & set(df.columns)):
    R[c] = df[c].fillna(pd.Series(rng0.integers(0, 2, len(df)), index=df.index)).astype(float)
R['sector'] = df['sector'].astype(float)
NUM = list(R.columns)
tam = num_('log_activos').groupby(df['anio']).rank(pct=True).values

# PERSONAS (igual que interrelacion.py)
pe = pd.read_csv(sys.argv[2], dtype={'id': str, 'mes': str})
pe['m'] = pe['mes'].str[:4].astype(int) * 12 + pe['mes'].str[4:6].astype(int) - 1; pe = pe.sort_values('m')
pe['creyentes_sobre_fondos'] = pe['creyentes'] / pe['fondos_antes'].replace(0, np.nan)
PERS = ['cambio12', 'creyentes', 'fondos_antes', 'compras', 'ventas', 'creyentes_sobre_fondos']
pres = df['_presentado'].astype(str)
ok = pres.str.len() >= 7
mp = pd.Series(np.nan, index=df.index)                       # mes de presentación (meses corridos)
mp[ok] = pres[ok].str[:4].astype(int) * 12 + pres[ok].str[5:7].astype(int) - 1
q = pd.DataFrame({'i': df.index, 'id': df['id'], 'm': mp + 1}).dropna(subset=['m'])
q['m'] = q['m'].astype(int); q = q.sort_values('m')
j = pd.merge_asof(q, pe[['id', 'm'] + PERS], on='m', by='id', direction='backward', tolerance=6)
for c in PERS:
    R[c] = np.nan
    R.loc[j['i'].values, c] = j[c].values

# FINANCIACIÓN (nuevo): todo del balance ya presentado y de los 12 meses antes de presentar
activos = np.exp(num_('log_activos'))
clave = pd.Series(df.index.values, index=pd.MultiIndex.from_arrays([df['id'], df['anio']]))
clave = clave[~clave.index.duplicated()]
p1 = clave.reindex(pd.MultiIndex.from_arrays([df['id'], df['anio'] - 1])).values
tiene1 = ~np.isnan(p1.astype(float)); p1 = np.where(tiene1, p1, 0).astype(int)
prev = lambda s: pd.Series(np.where(tiene1, s.values[p1], np.nan), index=df.index)
acc, emi, rec = num_('_acciones'), num_('_emisiones'), num_('_recompras')
caja, deu, fco, capex = num_('_caja'), num_('_deuda'), num_('_fco'), num_('_capex')
F = pd.DataFrame(index=df.index)
F['emision_neta_activos'] = (emi.fillna(0) - rec.fillna(0)) / activos
F.loc[emi.isna() & rec.isna(), 'emision_neta_activos'] = np.nan
F['dilucion_1'] = acc / prev(acc) - 1
quema = -(fco - capex.fillna(0))
F['anios_de_caja'] = np.where(quema > 0, (caja / quema).clip(upper=50), np.where(fco.notna(), 50.0, np.nan))
F['deuda_nueva_activos'] = (deu - prev(deu)) / activos
# entregas fallidas
fa = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[3].split(',') if x])
fa = fa.groupby(['id', 'mes'], as_index=False)[['fallas', 'dias']].sum()
fa['m'] = fa['mes'].str[:4].astype(int) * 12 + fa['mes'].str[4:6].astype(int) - 1
FS = {(i, m): (f, d) for i, m, f, d in zip(fa['id'], fa['m'], fa['fallas'], fa['dias'])}
hay_ftd = int(fa['m'].min()) if len(fa) else 10**9
f12 = np.full(len(df), np.nan); d12 = np.full(len(df), np.nan); f3 = np.full(len(df), np.nan); d3 = np.full(len(df), np.nan)
for i, (id_, m_, a_) in enumerate(zip(df['id'].values, mp.values, acc.values)):
    if np.isnan(m_) or m_ - 12 < hay_ftd or not (a_ > 0):
        continue
    m_ = int(m_); s12 = s3 = e12 = e3 = 0.0
    for k in range(1, 13):
        x = FS.get((id_, m_ - k))
        if x:
            s12 += x[0]; e12 += x[1]
            if k <= 3:
                s3 += x[0]; e3 += x[1]
    f12[i], d12[i], f3[i], d3[i] = s12 / a_, e12, s3 / a_, e3
F['fallas_12'], F['dias_falla_12'], F['fallas_3'], F['dias_falla_3'] = f12, d12, f3, d3
for c in F.columns:                                       # percentil dentro del año (sin relleno: el faltante queda faltante)
    R['fin_' + c] = pd.Series(F[c].values, index=df.index).replace([np.inf, -np.inf], np.nan).groupby(df['anio']).rank(pct=True)
FIN = ['fin_' + c for c in F.columns]
print('DIREC huellas de financiación con dato: ' + ', '.join(f'{c} {int(R[c].notna().sum())}' for c in FIN) +
      f' | FTD desde {hay_ftd // 12}-{hay_ftd % 12 + 1:02d} ({time.time() - t0:.0f}s)', flush=True)

# etiqueta a 12 meses
anio = df['anio'].values
ult = df.groupby('id')['anio'].transform('max')
r1 = num_('_ret1').copy()
r1[r1.isna() & df['estado_final'].isin(['quiebra', 'revocada']) & (ult < df['anio'] + 1)] = 0.0
r1 = r1.values; en = ~np.isnan(r1)
arriba = np.zeros(len(df), int); abajo = np.zeros(len(df), int)
for a_ in np.unique(anio[en]):
    k = en & (anio == a_)
    if k.sum() < 50:
        continue
    hi, lo = np.quantile(r1[k], 0.9), np.quantile(r1[k], 0.1)
    arriba[k & (r1 >= hi)] = 1; abajo[k & (r1 <= lo)] = 1
extremo = arriba | abajo

COL_M = NUM + PERS + FIN; COL_R0 = NUM + PERS; COL_R1 = NUM + PERS + FIN
hgb = lambda: HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15, l2_regularization=1.0, random_state=0)
def ajustar(cols, A, y_, k):
    c = [x for x in cols if R.loc[A, x].nunique() >= 3]
    return hgb().fit(R.loc[A, c].values, y_[A]).predict_proba(R.loc[k, c].values)[:, 1]
def met(ii):
    r = r1[ii]
    return {'n': int(len(ii)), 'x2': round(100 * float((r >= 2).mean()), 2), 'des': round(100 * float((r <= 0.5).mean()), 2),
            'prom': round(float(r.mean()), 3), 'mediana': round(float(np.median(r)), 3), 'tam': round(float(np.nanmean(tam[ii])), 3)}
res = {'camadas': {}}
for s in range(2019, int(anio.max()) + 1):
    A = en & (anio <= s - 2); Ax = A & (extremo == 1)
    k = np.where((anio == s) & en)[0]
    if A.sum() < mA or len(k) < mc or len(set(arriba[Ax])) < 2:
        print(f'DIREC {s}: no alcanza (entrena {int(A.sum())}, prueba {len(k)})', flush=True); continue
    pm = ajustar(COL_M, A, extremo, k)
    r0 = ajustar(COL_R0, Ax, arriba, k); r1_ = ajustar(COL_R1, Ax, arriba, k)
    n10 = max(1, int(round(0.1 * len(k))))
    alto = np.argsort(-pm)[:int(round(0.3 * len(k)))]
    eleg = k[alto[np.argsort(-r1_[alto])[:n10]]]
    eleg0 = k[alto[np.argsort(-r0[alto])[:n10]]]
    ex = extremo[k] == 1
    auc = lambda y_, p_: round(float(roc_auc_score(y_, p_)), 3) if len(set(y_)) == 2 else None
    fila = {'cuenta': 2022 <= s <= 2024, 'entrena_hasta': s - 2, 'filas_entrena': int(A.sum()), 'extremas_entrena': int(Ax.sum()),
            'auc_M': auc(extremo[k], pm), 'auc_R0': auc(arriba[k][ex], r0[ex]), 'auc_R1': auc(arriba[k][ex], r1_[ex]),
            'universo': met(k), 'elegidas': met(eleg), 'elegidas_sin_fin': met(eleg0), 'solo_magnitud': met(k[np.argsort(-pm)[:n10]])}
    res['camadas'][s] = fila
    print(f'DIREC {s} ({"CUENTA" if fila["cuenta"] else "ya vista, no cuenta"}; aprende hasta {s - 2}, {fila["filas_entrena"]} filas, '
          f'{fila["extremas_entrena"]} extremas; auc M {fila["auc_M"]} R0 {fila["auc_R0"]} R1 {fila["auc_R1"]}) | ' + ' | '.join(
        f"{g}: x2 {v['x2']}% des {v['des']}% prom {v['prom']} med {v['mediana']} tam {v['tam']}" for g, v in fila.items() if isinstance(v, dict)), flush=True)
    json.dump(res, open(salida, 'w'), indent=1)
C = {s: f for s, f in res['camadas'].items() if f['cuenta']}
c1 = sum(1 for f in C.values() if (f['auc_R1'] or 0) >= 0.70)
c2 = sum(1 for f in C.values() if f['elegidas']['des'] < f['universo']['des'])
c3 = sum(1 for f in C.values() if f['elegidas']['x2'] >= 1.3 * f['universo']['x2'])
n = len(C)
res['criterio'] = {'camadas': n, 'auc_R1_070': f'{c1} de {n}', 'menos_desastres': f'{c2} de {n}', 'x2_13_veces': f'{c3} de {n}',
                   'pasa': bool(n >= 1 and c1 == n and c2 == n and c3 == n)}
print(f'CRITERIO dirección (#47): {res["criterio"]} -> {"PASA" if res["criterio"]["pasa"] else "no pasa"} ({time.time() - t0:.0f}s)', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
