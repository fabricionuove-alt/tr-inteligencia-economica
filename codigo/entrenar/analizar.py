"""Prueba de fuga + entrenamiento + comparación con las reglas de los cinco.
Uso: python analizar.py filas.csv [salida.json]

Pasos:
1. Todos los rasgos se pasan a percentil DENTRO de su año (borra la huella de la época).
2. Prueba de fuga: ¿un modelo adivina el año con esos rasgos? Si sí, hay fuga.
3. Por etiqueta: entrena con años viejos, deja un hueco (embargo) y prueba con años nuevos
   que se usan UNA sola vez. Compara: regla tonta (tamaño), reglas de los cinco, modelo.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, joblib
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.inspection import permutation_importance
from reglas_de_los_cinco import REGLAS, REGLAS_PRECIO, REGLAS_TEXTO, REGLAS_FRANQUEZA, REGLAS_DUENOS, REGLAS_IA

t0 = time.time()
df = pd.read_csv(sys.argv[1])
salida = sys.argv[2] if len(sys.argv) > 2 else 'resultados.json'
# Los datos arrancan en 2009: antes de 2012 faltan los rasgos de historia y ese hueco delata el año.
df = df[df['anio'] >= 2012].drop(columns=[c for c in ['anios_hist'] if c in df.columns]).reset_index(drop=True)
ETIQ = ['sobrevive_10', 'sobrevive_10_amplio', 'duplica_6', 'gana_mas_1'] + [e for e in ('precio_duplica_6', 'precio_gana_1') if e in df.columns]
CLASICOS = {'altman_z2': +1, 'ohlson_o': -1, 'piotroski_f': +1}   # signo: hacia dónde es 'mejor'
# Versión amplia: si dejó de presentar balances sin quiebra ni compra registrada ("desconocido"),
# se cuenta como muerte (muchas son quiebras silenciosas de empresas chicas).
ultimo = df.groupby('id')['anio'].transform('max')
df['sobrevive_10_amplio'] = df['sobrevive_10']
mask = (df['estado_final'].isin(['desconocido', 'revocada'])) & (ultimo < df['anio'] + 10) & df['sobrevive_10'].isna()
df.loc[mask, 'sobrevive_10_amplio'] = 0
NO_RASGO = {'id', 'anio', 'estado_final'} | set(ETIQ) | set(CLASICOS)
BINARIOS = {'patrimonio_neg', 'sin_deuda', 'perdida', 'financiera'}
rasgos = [c for c in df.columns if c not in NO_RASGO and not c.startswith('_')]   # '_' = montos crudos ocultos
rasgos = [c for c in rasgos if df[c].notna().sum() > 100]   # una columna vacía no entra (rompía el análisis)
num = [c for c in rasgos if c not in BINARIOS and c != 'sector']

# 1. percentil dentro del año, sin huellas:
#  - los empates (muchas empresas en 0) se desarman al azar; si no, el valor del empate
#    depende de cuántas fueron ese año y delata el año (la primera corrida lo mostró: 42% vs 9%).
#  - los faltantes se rellenan al azar: qué datos existían cambió con los años.
rng0 = np.random.default_rng(42)
R = df[['id', 'anio'] + ETIQ].copy()
Rn = pd.DataFrame(index=df.index)
for c in num:
    ruido = rng0.random(len(df)) * 1e-9
    v = df[c] + ruido * (df[c].abs().max() if df[c].notna().any() else 1)
    p = v.groupby(df['anio']).rank(pct=True, method='first')
    R[c] = p.where(p.notna(), pd.Series(rng0.random(len(df)), index=df.index))
    Rn[c] = p   # con huecos: lo usan las reglas de los cinco (no inventan datos)
for c in sorted(BINARIOS):   # ordenado: el orden de un set cambia en cada corrida
    R[c] = df[c].fillna(pd.Series(rng0.integers(0, 2, len(df)), index=df.index)).astype(float)
R['sector'] = df['sector'].astype(float)
X_cols = num + sorted(BINARIOS) + ['sector']
res = {'filas': len(df), 'empresas': int(df['id'].nunique()),
       'por_anio': df.groupby('anio').size().to_dict()}
print('filas', len(df), 'empresas', df['id'].nunique(), flush=True)

# 2. prueba de fuga: adivinar el año (pares vs impares de empresas para no memorizar la empresa)
def fuga(X, nombre, cols=None):
    cols = cols or X_cols
    sub = df[(df.anio >= 2012) & (df.anio <= 2023)]
    Xs, y = X.loc[sub.index, cols], sub['anio']
    par = sub['id'].apply(lambda s: int(s, 16) % 2 == 0)
    m = HistGradientBoostingClassifier(max_iter=150, random_state=0).fit(Xs[par], y[par])
    acc = accuracy_score(y[~par], m.predict(Xs[~par]))
    azar = y[~par].value_counts(normalize=True).max()
    err = float(np.mean(np.abs(m.predict(Xs[~par]) - y[~par])))
    print(f'FUGA [{nombre}] acierta el año {acc:.3f} (azar {azar:.3f}), error medio {err:.1f} años', flush=True)
    return {'acierto': acc, 'azar': float(azar), 'error_anios': err}

crudo = df.copy(); crudo['sector'] = crudo['sector'].astype(float)
res['fuga_crudo'] = fuga(crudo, 'ratios crudos')
res['fuga_percentil'] = fuga(R, 'percentiles por año')
# ¿De dónde sale lo que queda? Por grupos de rasgos.
res['fuga_solo_percentiles'] = fuga(R, 'sólo percentiles', num)
res['fuga_sin_sector'] = fuga(R, 'percentiles + señales sí/no', num + sorted(BINARIOS))
res['fuga_solo_sino_sector'] = fuga(R, 'sólo sí/no + sector', sorted(BINARIOS) + ['sector'])

# 3. entrenamiento por etiqueta
def puntaje_cinco(X, reglas=None):
    s = np.zeros(len(X)); n = np.zeros(len(X))
    for col, signo, _ in (reglas or REGLAS):
        if col not in X.columns:
            continue
        v = X[col].values
        ok = ~np.isnan(v)
        s[ok] += (v[ok] if signo > 0 else 1 - v[ok]); n[ok] += 1
    return np.where(n > 0, s / np.maximum(n, 1), 0.5)

def auc_ic(y, p, ids, B=300):
    """AUC con intervalo 90% remuestreando EMPRESAS (no filas)."""
    base = roc_auc_score(y, p)
    u = np.unique(ids); idx = {k: np.where(ids == k)[0] for k in u}
    rng = np.random.default_rng(0); vals = []
    for _ in range(B):
        sel = np.concatenate([idx[k] for k in rng.choice(u, len(u))])
        if len(np.unique(y[sel])) == 2:
            vals.append(roc_auc_score(y[sel], p[sel]))
    return base, float(np.percentile(vals, 5)), float(np.percentile(vals, 95))

PARTES = {  # entrenamiento | embargo | prueba (se mira una vez)
    # 10 años con datos desde 2009: las ventanas se pisan (2016-2023). Se informa, no se puede evitar.
    'sobrevive_10': ((2012, 2013), (2014, 2014), (2015, 2015)),
    'sobrevive_10_amplio': ((2012, 2013), (2014, 2014), (2015, 2015)),
    # 6 años: lo que aprende termina en 2019 y la prueba arranca en 2019. Separación limpia.
    'duplica_6':    ((2012, 2013), (2014, 2018), (2019, 2019)),
    # Con precios: ¿la INVERSIÓN se duplicó en 6 años? Misma partición limpia que duplica_6.
    'precio_duplica_6': ((2012, 2013), (2014, 2018), (2019, 2019)),
    # A 12 meses contra la mediana del año. Lo que aprende termina en 2017; prueba 2018-2023.
    'precio_gana_1': ((2012, 2016), (2017, 2017), (2018, 2023)),
    # La pregunta del paper de Chicago Booth: a un año. Lo que aprende termina en 2017; prueba 2018-2023.
    'gana_mas_1':   ((2012, 2016), (2017, 2017), (2018, 2023)),
}
for et, (tr, emb, te) in PARTES.items():
    d = R[R[et].notna()]
    A = d[(d.anio >= tr[0]) & (d.anio <= tr[1])]
    B_ = d[(d.anio >= te[0]) & (d.anio <= te[1])]
    if len(A) < 200 or len(B_) < 200 or A[et].nunique() < 2:
        print(et, 'pocos datos', len(A), len(B_)); continue
    ya, yb = A[et].values.astype(int), B_[et].values.astype(int)
    ids = B_['id'].values
    m = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15,
                                       l2_regularization=1.0, random_state=0).fit(A[X_cols], ya)
    p_mod = m.predict_proba(B_[X_cols])[:, 1]
    os.makedirs('modelos', exist_ok=True)
    joblib.dump({'modelo': m, 'rasgos': X_cols, 'etiqueta': et, 'anios': list(tr)}, f'modelos/{et}_fuera.joblib')
    p_5 = puntaje_cinco(Rn.loc[B_.index])
    hay_precio = all(c in Rn.columns for c, _, _ in REGLAS_PRECIO)
    p_5p = puntaje_cinco(Rn.loc[B_.index], REGLAS + REGLAS_PRECIO) if hay_precio else p_5
    p_tam = B_['log_activos'].fillna(0.5).values
    r = {'entrena': tr, 'embargo': emb, 'prueba': te, 'n_entrena': int(len(A)), 'n_prueba': int(len(B_)),
         'tasa_base_prueba': float(yb.mean())}
    for nombre, p in [('regla_tonta_tamano', p_tam), ('reglas_de_los_cinco', p_5), ('cinco_con_precio', p_5p), ('modelo', p_mod)]:
        a, lo, hi = auc_ic(yb, p, ids)
        r[nombre] = {'auc': a, 'ic90': [lo, hi]}
        # ¿qué pasa con el 20% mejor puntuado vs la tasa base?
        top = p >= np.quantile(p, 0.8); bot = p <= np.quantile(p, 0.2)
        r[nombre]['tasa_quintil_alto'] = float(yb[top].mean()); r[nombre]['tasa_quintil_bajo'] = float(yb[bot].mean())
        print(f'{et:13s} {nombre:20s} AUC {a:.3f} [{lo:.3f}-{hi:.3f}]  quintil alto {yb[top].mean():.3f}  bajo {yb[bot].mean():.3f}  (base {yb.mean():.3f})', flush=True)
    # Contra los modelos publicados, en las MISMAS empresas (los clásicos no se calculan para todas)
    r['clasicos'] = {}
    for cl, sg in CLASICOS.items():
        v = df.loc[B_.index, cl].values.astype(float); ok = ~np.isnan(v)
        if ok.sum() > 200 and len(set(yb[ok])) == 2:
            a_cl = roc_auc_score(yb[ok], sg * v[ok]); a_mo = roc_auc_score(yb[ok], p_mod[ok])
            a_5 = roc_auc_score(yb[ok], p_5[ok])
            r['clasicos'][cl] = {'n': int(ok.sum()), 'clasico': float(a_cl), 'modelo': float(a_mo), 'cinco': float(a_5)}
            print(f'  {et}: {cl:12s} AUC {a_cl:.3f} | modelo en las mismas {a_mo:.3f} | cinco {a_5:.3f}  (n={ok.sum()})', flush=True)
    if et == 'gana_mas_1':   # como lo mide el paper: % de aciertos
        r['acierto_modelo'] = float(((p_mod >= 0.5).astype(int) == yb).mean())
        r['acierto_siempre_sube'] = float(max(yb.mean(), 1 - yb.mean()))
        print(f'  gana_mas_1: ACIERTA {r["acierto_modelo"]:.1%} | decir siempre lo más común {r["acierto_siempre_sube"]:.1%} '
              f'| paper: GPT-4 60.3%, red neuronal 60.1-60.5%, analistas 52.7-56.6%, regresión 52.9%, base 55.5%', flush=True)
    # cada regla sola
    r['reglas_sueltas'] = {}
    for col, signo, quien in REGLAS + REGLAS_PRECIO + REGLAS_TEXTO + REGLAS_FRANQUEZA:
        if col not in Rn.columns:
            continue
        v = Rn.loc[B_.index, col].values; ok = ~np.isnan(v)
        if ok.sum() > 100 and len(np.unique(yb[ok])) == 2:
            r['reglas_sueltas'][col] = {'auc': float(roc_auc_score(yb[ok], v[ok] if signo > 0 else -v[ok])), 'quien': quien}
    pi = permutation_importance(m, B_[X_cols], yb, scoring='roc_auc', n_repeats=3, random_state=0)
    orden = np.argsort(-pi.importances_mean)[:10]
    r['importancia_modelo'] = {X_cols[i]: float(pi.importances_mean[i]) for i in orden}
    # Calibración: si dice 70%, ¿pasa 70%? (deciles de la prueba)
    q = pd.qcut(p_mod, 10, labels=False, duplicates='drop')
    r['calibracion'] = [{'dice': float(p_mod[q == k].mean()), 'pasa': float(yb[q == k].mean()), 'n': int((q == k).sum())}
                        for k in sorted(set(q))]
    # Por sector (división SIC) y sin financieras
    sec = df.loc[B_.index, 'sector'].values; fin = df.loc[B_.index, 'financiera'].values
    r['por_sector'] = {}
    for sv in sorted(set(sec)):
        k = sec == sv
        if k.sum() >= 150 and len(set(yb[k])) == 2:
            r['por_sector'][str(sv)] = {'n': int(k.sum()), 'base': float(yb[k].mean()),
                                        'modelo': float(roc_auc_score(yb[k], p_mod[k])),
                                        'cinco': float(roc_auc_score(yb[k], p_5[k]))}
    k = fin != 1
    r['sin_financieras'] = {'n': int(k.sum()), 'modelo': float(roc_auc_score(yb[k], p_mod[k])),
                            'cinco': float(roc_auc_score(yb[k], p_5[k]))}
    print(f'  {et}: sin financieras modelo {r["sin_financieras"]["modelo"]:.3f}; por sector',
          {s_: round(v['modelo'], 3) for s_, v in r['por_sector'].items()}, flush=True)
    print('  calibración', [(round(c['dice'], 2), round(c['pasa'], 2)) for c in r['calibracion']], flush=True)
    pd.DataFrame({'id': B_['id'].values, 'anio': B_['anio'].values, 'y': yb, 'modelo': p_mod, 'cinco': p_5}
                 ).to_csv(f'pred_prueba_{et}.csv', index=False)
    res[et] = r
    # Modelo final para usar: entrenado con TODOS los años con etiqueta hasta el fin de la prueba
    import joblib
    os.makedirs('modelos', exist_ok=True)
    T = d[d.anio <= te[1]]
    mf = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15,
                                        l2_regularization=1.0, random_state=0).fit(T[X_cols], T[et].astype(int))
    joblib.dump({'modelo': mf, 'rasgos': X_cols, 'etiqueta': et, 'anios': [int(T.anio.min()), int(T.anio.max())]},
                f'modelos/{et}.joblib')

# Las reglas NO se entrenan: se pueden probar limpias en CADA camada (año de compra), no sólo en la prueba.
# ¿Comprar barato funcionó siempre o sólo en una época?
res['por_camada'] = {}
for et in [e for e in ('precio_gana_1', 'precio_duplica_6', 'gana_mas_1', 'sobrevive_10') if e in ETIQ]:
    filas_et = {}
    for a in sorted(df.loc[df[et].notna(), 'anio'].unique()):
        k = (df['anio'] == a) & df[et].notna()
        y = df.loc[k, et].values.astype(int)
        if k.sum() < int(os.environ.get('MIN_CAMADA', 300)) or len(set(y)) < 2:
            continue
        fila = {'n': int(k.sum()), 'base': round(float(y.mean()), 3)}
        for col, sg, _ in REGLAS_IA + REGLAS_DUENOS + REGLAS_FRANQUEZA + REGLAS_TEXTO + REGLAS_PRECIO + [('log_activos', +1, 'tamaño')]:
            if col in Rn.columns:
                v = Rn.loc[k, col].values; ok = ~np.isnan(v)
                if ok.sum() > int(os.environ.get('MIN_CAMADA', 300)) * 2 // 3 and len(set(y[ok])) == 2:
                    fila[col] = round(float(roc_auc_score(y[ok], sg * v[ok])), 3)
        fila['cinco'] = round(float(roc_auc_score(y, puntaje_cinco(Rn.loc[k]))), 3)
        fila['cinco_con_precio'] = round(float(roc_auc_score(y, puntaje_cinco(Rn.loc[k], REGLAS + REGLAS_PRECIO))), 3)
        filas_et[int(a)] = fila
        print(f'CAMADA {et} {a}: ' + '  '.join(f'{c}={v}' for c, v in fila.items()), flush=True)
    res['por_camada'][et] = filas_et

# CRITERIO de las señales #30-33 (notas/11-registro-de-senales.md), escrito antes de mirar:
# precio_gana_1, media ≥ 0,52 y ≥ 6 de 8 años arriba de 0,5 en 2012-2019, y ≥ 0,52 y ≥ 4 de 5 en 2020-2024.
pc_ = res['por_camada'].get('precio_gana_1', {})
res['criterio_duenos'] = {}
for col, _, quien in REGLAS_DUENOS + REGLAS_IA:
    linea = {}
    for nombre_p, (a0, a1, minimo) in {'2012-2019': (2012, 2019, 6), '2020-2024': (2020, 2024, 4)}.items():
        v = [pc_[a][col] for a in pc_ if a0 <= int(a) <= a1 and col in pc_[a]]
        if v:
            linea[nombre_p] = {'media': round(float(np.mean(v)), 3), 'arriba': int(sum(x > 0.5 for x in v)), 'de': len(v),
                               'pasa': bool(np.mean(v) >= 0.52 and sum(x > 0.5 for x in v) >= minimo)}
    res['criterio_duenos'][col] = linea
    print(f'CRITERIO {col}: ' + ' | '.join(f"{k}: media {x['media']} arriba {x['arriba']}/{x['de']} {'PASA' if x['pasa'] else 'no'}" for k, x in linea.items()), flush=True)

# ROBUSTEZ de franq_nosotros (agregado 2-nov después de ver que funciona en las 8 camadas; esto NO es una regla
# nueva sino un control): ¿se sostiene DENTRO de cada tercio de tamaño y DENTRO de cada sector?
# Si sólo funciona entre tamaños o entre sectores, era un disfraz de tamaño o de sector.
res['robustez_nosotros'] = {}
mc = int(os.environ.get('MIN_CAMADA', 300))
for et in [e for e in ('precio_duplica_6', 'precio_gana_1') if e in ETIQ]:
    filas_r = {}
    for a in sorted(df.loc[df[et].notna(), 'anio'].unique()):
        if not 2012 <= a <= 2024 or 'franq_nosotros' not in Rn.columns:   # 2020-2024 = fuera de muestra
            continue
        k = (df['anio'] == a) & df[et].notna() & Rn['franq_nosotros'].notna()
        if k.sum() < mc:
            continue
        sub = pd.DataFrame({'y': df.loc[k, et].astype(int), 'v': Rn.loc[k, 'franq_nosotros'],
                            'tam': pd.qcut(Rn.loc[k, 'log_activos'].rank(method='first'), 3, labels=False),
                            'sec': df.loc[k, 'sector']})
        def dentro(col):
            tot, w = 0.0, 0
            for _, g in sub.groupby(col):
                if len(g) >= (30 if mc >= 300 else 3) and g['y'].nunique() == 2:
                    tot += roc_auc_score(g['y'], g['v']) * len(g); w += len(g)
            return round(tot / w, 3) if w else None
        filas_r[int(a)] = {'todas': round(float(roc_auc_score(sub['y'], sub['v'])), 3),
                           'dentro_tamano': dentro('tam'), 'dentro_sector': dentro('sec')}
        print(f'ROBUSTEZ nosotros {et} {a}: ' + '  '.join(f'{c}={v}' for c, v in filas_r[int(a)].items()), flush=True)
    res['robustez_nosotros'][et] = filas_r

# Puntajes de TODAS las filas con los modelos fuera de muestra (los entrenados sólo con años viejos),
# para cruzar con las carteras reales de los inversores (carteras.py).
P_ = df[['id', 'anio', 'piotroski_f'] + ETIQ].copy()
P_['cinco'] = puntaje_cinco(Rn)
for et in ETIQ:
    pf = f'modelos/{et}_fuera.joblib'
    if os.path.exists(pf):
        mm = joblib.load(pf); P_['p_' + et] = mm['modelo'].predict_proba(R[mm['rasgos']])[:, 1]
P_.to_csv('puntajes_todos.csv', index=False)

# SEÑAL #36 (notas/11): ¿evitar las que el modelo ve frágiles mejora el rendimiento? Dentro del mismo tamaño.
res['fragiles'] = {}
mc36 = int(os.environ.get('MIN_CAMADA', 300))
mA = int(os.environ.get('MIN_ENTRENA', 500))   # filas mínimas para entrenar (sólo se baja en la prueba local)
if 'p_sobrevive_10_amplio' in P_.columns and 'precio_gana_1' in df.columns:
    for a in range(2014, 2025):
        k = (df['anio'] == a) & df['precio_gana_1'].notna() & P_['p_sobrevive_10_amplio'].notna()
        if k.sum() < mc36:
            continue
        y = df.loc[k, 'precio_gana_1'].astype(int).values
        s = P_.loc[k, 'p_sobrevive_10_amplio'].values
        r1 = df.loc[k, '_ret1'].values if '_ret1' in df.columns else None
        tam = pd.qcut(Rn.loc[k, 'log_activos'].rank(method='first'), 5, labels=False).values
        tot = w = 0
        for t_ in range(5):
            g = tam == t_
            if g.sum() >= (30 if mc36 >= 300 else 3) and len(set(y[g])) == 2:
                tot += roc_auc_score(y[g], s[g]) * g.sum(); w += g.sum()
        fragil = s <= np.quantile(s, 0.2)
        fila = {'n': int(k.sum()), 'todas': round(float(roc_auc_score(y, s)), 3),
                'dentro_tamano': round(tot / w, 3) if w else None}
        if r1 is not None:
            fila['ret_mediano_fragiles'] = round(float(np.nanmedian(r1[fragil])), 3)
            fila['ret_mediano_resto'] = round(float(np.nanmedian(r1[~fragil])), 3)
        res['fragiles'][a] = fila
        print(f'FRAGILES {a}: ' + '  '.join(f'{c}={v}' for c, v in fila.items()), flush=True)
    def per(a0, a1, minimo):
        v = [res['fragiles'][a]['dentro_tamano'] for a in res['fragiles'] if a0 <= a <= a1 and res['fragiles'][a]['dentro_tamano'] is not None]
        return (round(float(np.mean(v)), 3), sum(x > 0.5 for x in v), len(v), bool(v and np.mean(v) >= 0.52 and sum(x > 0.5 for x in v) >= minimo)) if v else None
    p1, p2 = per(2014, 2019, 4), per(2020, 2024, 4)
    res['criterio_fragiles'] = {'2014-2019': p1, '2020-2024': p2, 'pasa': bool(p1 and p2 and p1[3] and p2[3])}
    print(f'CRITERIO frágiles (dentro de tamaño): 2014-2019 {p1} | 2020-2024 {p2} -> {"PASA" if res["criterio_fragiles"]["pasa"] else "no pasa"}', flush=True)

# SEÑAL #37 (notas/11): frágiles mejorado. Etiqueta muere_3 + entrenamiento móvil (años 2012..t-4) + señales de mercado.
ult37 = df.groupby('id')['anio'].transform('max')
muere3 = pd.Series(np.nan, index=df.index)
muere3[ult37 >= df['anio'] + 3] = 0.0
muere3[(ult37 < df['anio'] + 3) & df['estado_final'].isin(['quiebra', 'revocada', 'desconocido'])] = 1.0
res['fragiles_v2'] = {}
if 'precio_gana_1' in df.columns:
    for t in range(2016, 2025):
        A = (df['anio'] <= t - 4) & muere3.notna()
        B = (df['anio'] == t) & df['precio_gana_1'].notna()
        if A.sum() < mA or B.sum() < mc36 or muere3[A].nunique() < 2:
            continue
        m37 = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15,
                                             l2_regularization=1.0, random_state=0).fit(R.loc[A, X_cols], muere3[A].astype(int))
        s = -m37.predict_proba(R.loc[B, X_cols])[:, 1]          # más alto = más sano
        y = df.loc[B, 'precio_gana_1'].astype(int).values
        r1 = df.loc[B, '_ret1'].values if '_ret1' in df.columns else None
        tam = pd.qcut(Rn.loc[B, 'log_activos'].rank(method='first'), 5, labels=False).values
        tot = w = 0
        for t_ in range(5):
            g = tam == t_
            if g.sum() >= (30 if mc36 >= 300 else 3) and len(set(y[g])) == 2:
                tot += roc_auc_score(y[g], s[g]) * g.sum(); w += g.sum()
        fragil = s <= np.quantile(s, 0.2)
        fila = {'n': int(B.sum()), 'entrena_hasta': t - 4, 'todas': round(float(roc_auc_score(y, s)), 3),
                'dentro_tamano': round(tot / w, 3) if w else None}
        if r1 is not None:
            fila['ret_mediano_fragiles'] = round(float(np.nanmedian(r1[fragil])), 3)
            fila['ret_mediano_resto'] = round(float(np.nanmedian(r1[~fragil])), 3)
        res['fragiles_v2'][t] = fila
        print(f'FRAGILES_V2 {t}: ' + '  '.join(f'{c}={v}' for c, v in fila.items()), flush=True)
    def per2(a0, a1, minimo):
        v = [res['fragiles_v2'][a]['dentro_tamano'] for a in res['fragiles_v2'] if a0 <= a <= a1 and res['fragiles_v2'][a]['dentro_tamano'] is not None]
        return (round(float(np.mean(v)), 3), int(sum(x > 0.5 for x in v)), len(v), bool(v and np.mean(v) >= 0.52 and sum(x > 0.5 for x in v) >= minimo)) if v else None
    q1, q2 = per2(2016, 2019, 3), per2(2020, 2024, 4)
    res['criterio_fragiles_v2'] = {'2016-2019': q1, '2020-2024': q2, 'pasa': bool(q1 and q2 and q1[3] and q2[3])}
    print(f'CRITERIO frágiles v2 (dentro de tamaño): 2016-2019 {q1} | 2020-2024 {q2} -> {"PASA" if res["criterio_fragiles_v2"]["pasa"] else "no pasa"}', flush=True)

# SEÑAL #38 (notas/11): EL COTO. Sacar el 30% más frágil; dentro, el 30% más "opcional". Medir colas y promedio.
OPC = [('crec_ventas_3', +1), ('id_ventas', +1), ('log_activos', -1), ('volatilidad_12', +1), ('dividendos_fco', -1)]
res['coto'] = {}
if '_ret1' in df.columns:
    r1all = df['_ret1'].copy()
    murio1 = r1all.isna() & df['estado_final'].isin(['quiebra', 'revocada']) & (ult37 < df['anio'] + 1)
    r1all[murio1] = 0.0                                # quiebra en el año = pérdida total
    r6all = df['_ret6'] if '_ret6' in df.columns else pd.Series(np.nan, index=df.index)
    for t in range(2016, 2025):
        A = (df['anio'] <= t - 4) & muere3.notna()
        B = (df['anio'] == t)
        if A.sum() < mA or B.sum() < mc36 or muere3[A].nunique() < 2:
            continue
        m38 = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15,
                                             l2_regularization=1.0, random_state=0).fit(R.loc[A, X_cols], muere3[A].astype(int))
        idx = df.index[B]
        sano = -m38.predict_proba(R.loc[idx, X_cols])[:, 1]
        # corte por POSICIÓN (con empates el corte por valor marcaba a todas como frágiles)
        pos = pd.Series(sano).rank(method='first').values / len(sano)
        fragil = pos <= 0.3
        opc = np.zeros(len(idx)); nn = np.zeros(len(idx))
        for col, sg in OPC:
            if col in Rn.columns:
                v = Rn.loc[idx, col].values; ok = ~np.isnan(v)
                opc[ok] += v[ok] if sg > 0 else 1 - v[ok]; nn[ok] += 1
        opc = np.where(nn > 0, opc / np.maximum(nn, 1), np.nan)
        coto = ~fragil
        rk = lambda v, m: pd.Series(np.where(m, v, np.nan)).rank(method='first', pct=True).values
        opc_coto = coto & (rk(opc, coto) > 0.7)
        loteria = rk(opc, ~np.isnan(opc)) > 0.7
        r1 = r1all.loc[idx].values; r6 = r6all.loc[idx].values
        def met(mask):
            a = r1[mask & ~np.isnan(r1)]; b = r6[mask & ~np.isnan(r6)]
            o = {'n': int(len(a))}
            if len(a) >= 30:
                o.update({'prom_12m': round(float(a.mean()), 3), 'mediana_12m': round(float(np.median(a)), 3),
                          'pct_x2_12m': round(100 * float((a >= 2).mean()), 2), 'pct_desastre_12m': round(100 * float((a <= 0.5).mean()), 2)})
            if len(b) >= 30 and t <= 2019:      # a 6 años sólo camadas que ya los cumplieron
                o.update({'n6': int(len(b)), 'pct_x3_6a': round(100 * float((b >= 3).mean()), 2),
                          'pct_desastre_6a': round(100 * float((b <= 0.25).mean()), 2), 'prom_6a': round(float(b.mean()), 3)})
            return o
        todos = np.ones(len(idx), bool)
        fila = {'universo': met(todos), 'fragiles': met(fragil), 'coto': met(coto), 'coto_opcional': met(opc_coto),
                'loteria_sin_coto': met(loteria)}
        res['coto'][t] = fila
        print(f'COTO {t}: ' + ' | '.join(f"{g}: prom {x.get('prom_12m')} med {x.get('mediana_12m')} x2 {x.get('pct_x2_12m')}% "
                                         f"des {x.get('pct_desastre_12m')}%" + (f" ·6a x3 {x.get('pct_x3_6a')}% des {x.get('pct_desastre_6a')}%" if 'n6' in x else '')
                                         for g, x in fila.items()), flush=True)
    # criterio
    C = res['coto']; ok1 = ok2 = 0; exc = []; ok3 = n3 = 0
    for t, f in C.items():
        u, c = f['universo'], f['coto_opcional']
        if 'prom_12m' in u and 'prom_12m' in c:
            exc.append(c['prom_12m'] - u['prom_12m']); ok1 += c['prom_12m'] > u['prom_12m']
            ok2 += (c['pct_x2_12m'] >= u['pct_x2_12m']) and (c['pct_desastre_12m'] <= u['pct_desastre_12m'])
        if 'n6' in u and 'n6' in c:
            n3 += 1; ok3 += (c['pct_x3_6a'] > u['pct_x3_6a']) and (c['pct_desastre_6a'] < u['pct_desastre_6a'])
    nC = len(exc)
    pasa38 = bool(nC and ok1 >= 6 and np.mean(exc) >= 0.02 and ok2 >= 6 and n3 and ok3 >= 3)
    res['criterio_coto'] = {'camadas': nC, 'gana_promedio': int(ok1), 'exceso_medio': round(float(np.mean(exc)), 4) if exc else None,
                            'colas_mejores_12m': int(ok2), 'colas_mejores_6a': f'{ok3} de {n3}', 'pasa': pasa38}
    print(f'CRITERIO coto: {res["criterio_coto"]} -> {"PASA" if pasa38 else "no pasa"}', flush=True)

# SEÑAL #39 (notas/11): LA CONTRADICCIÓN. Superficie frágil + fondo sano. Dos modelos de fragilidad separados.
SUP = ['margen_neto', 'margen_op', 'margen_op_min5', 'roa', 'roe', 'tendencia_roa', 'perdida', 'rinde_ganancia',
       'rinde_fcf', 'ebit_ev', 'fcf_ventas', 'ret_previo_12', 'volatilidad_12', 'precio_nivel', 'sector']
FON = ['margen_bruto', 'estab_margen', 'crec_ventas_1', 'crec_ventas_3', 'diferido_ventas', 'rpo_ventas', 'id_ventas',
       'capex_fco', 'caja_activos', 'deuda_activos', 'deuda_neta_fco', 'pasivo_activos', 'sin_deuda', 'cobertura_int',
       'fco_activos', 'devengos', 'dilucion_3', 'rotacion', 'patrimonio_neg', 'directivos_compran', 'compra_neta_mcap',
       'dueno_mayor_pct', 'duenos_grandes', 'sector']
SUP = [c for c in SUP if c in X_cols]; FON = [c for c in FON if c in X_cols]
res['contradiccion'] = {'superficie': SUP, 'fondo': FON, 'camadas': {}}
print('CONTRA rasgos superficie', SUP, '| fondo', FON, flush=True)
if '_ret1' in df.columns:
    hgb = lambda: HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15,
                                                 l2_regularization=1.0, random_state=0)
    for t in range(2016, 2025):
        A = (df['anio'] <= t - 4) & muere3.notna()
        B = (df['anio'] == t)
        if A.sum() < mA or B.sum() < mc36 or muere3[A].nunique() < 2:
            continue
        yA = muere3[A].astype(int); idx = df.index[B]
        pos = lambda cols: pd.Series(-hgb().fit(R.loc[A, cols], yA).predict_proba(R.loc[idx, cols])[:, 1]).rank(method='first').values / len(idx)
        ps, pf = pos(SUP), pos(FON)
        sup_fragil = ps <= 0.3
        contra = sup_fragil & (pf > 0.6)
        coherente = sup_fragil & (pf <= 0.4)
        r1 = r1all.loc[idx].values; r6 = r6all.loc[idx].values
        def met39(mask):
            a = r1[mask & ~np.isnan(r1)]; b = r6[mask & ~np.isnan(r6)]
            o = {'n': int(mask.sum()), 'n12': int(len(a)), 'tamano_medio': round(float(np.nanmean(Rn.loc[idx, 'log_activos'].values[mask])), 3)}
            if len(a) >= 30:
                o.update({'prom_12m': round(float(a.mean()), 3), 'mediana_12m': round(float(np.median(a)), 3),
                          'pct_x2_12m': round(100 * float((a >= 2).mean()), 2), 'pct_desastre_12m': round(100 * float((a <= 0.5).mean()), 2)})
            if len(b) >= 30 and t <= 2019:
                o.update({'n6': int(len(b)), 'pct_x3_6a': round(100 * float((b >= 3).mean()), 2),
                          'pct_desastre_6a': round(100 * float((b <= 0.25).mean()), 2), 'prom_6a': round(float(b.mean()), 3)})
            return o
        fila = {'universo': met39(np.ones(len(idx), bool)), 'superficie_fragil': met39(sup_fragil),
                'contradiccion': met39(contra), 'fragil_coherente': met39(coherente)}
        # ¿cuánto se parecen los dos juicios? (si fueran el mismo, no hay contradicción que buscar)
        fila['correlacion_sup_fondo'] = round(float(np.corrcoef(ps, pf)[0, 1]), 3)
        # estela al revés: de las que hicieron x3 en 6 años, ¿qué parte estaba en la contradicción?
        ok6 = ~np.isnan(r6)
        if t <= 2019 and ok6.sum() >= 300:
            g3 = ok6 & (r6 >= 3)
            fila['x3_que_estaban_en_contradiccion_pct'] = round(100 * float(contra[g3].mean()), 2)
            fila['peso_de_la_contradiccion_pct'] = round(100 * float(contra[ok6].mean()), 2)
        res['contradiccion']['camadas'][t] = fila
        print(f'CONTRA {t} (corr {fila["correlacion_sup_fondo"]}): ' + ' | '.join(
            f"{g}: n {x['n']} prom {x.get('prom_12m')} x2 {x.get('pct_x2_12m')}% des {x.get('pct_desastre_12m')}%"
            + (f" ·6a x3 {x.get('pct_x3_6a')}% des {x.get('pct_desastre_6a')}%" if 'n6' in x else '')
            for g, x in fila.items() if isinstance(x, dict))
            + (f" | de las x3: {fila['x3_que_estaban_en_contradiccion_pct']}% en contradicción (pesa {fila['peso_de_la_contradiccion_pct']}%)"
               if 'x3_que_estaban_en_contradiccion_pct' in fila else ''), flush=True)
    C = res['contradiccion']['camadas']
    p2 = n2 = 0; ok1 = ok2 = 0; exc = []; ok3 = n3 = 0
    for t, f in C.items():
        u, c, h = f['universo'], f['contradiccion'], f['fragil_coherente']
        if 'n6' in u and 'n6' in c and 'n6' in h:
            n2 += 1; p2 += (c['pct_x3_6a'] > u['pct_x3_6a']) and (c['pct_desastre_6a'] < h['pct_desastre_6a'])
            n3 += 1; ok3 += (c['pct_x3_6a'] > u['pct_x3_6a']) and (c['pct_desastre_6a'] < u['pct_desastre_6a'])
        if 'prom_12m' in u and 'prom_12m' in c:
            exc.append(c['prom_12m'] - u['prom_12m']); ok1 += c['prom_12m'] > u['prom_12m']
            ok2 += (c['pct_x2_12m'] > u['pct_x2_12m']) and (c['pct_desastre_12m'] <= u['pct_desastre_12m'])
    paso2 = bool(n2 and p2 >= 3)
    paso3 = bool(exc and ok1 >= 6 and np.mean(exc) >= 0.02 and ok2 >= 6 and n3 and ok3 >= 3)
    res['criterio_contradiccion'] = {'paso2_estela': f'{p2} de {n2}', 'paso2_pasa': paso2, 'camadas_12m': len(exc),
                                     'gana_promedio': int(ok1), 'exceso_medio': round(float(np.mean(exc)), 4) if exc else None,
                                     'colas_mejores_12m': int(ok2), 'colas_mejores_6a': f'{ok3} de {n3}', 'paso3_pasa': paso3}
    print(f'CRITERIO contradicción: {res["criterio_contradiccion"]} -> estela {"EXISTE" if paso2 else "no"}, sirve {"SÍ" if paso3 else "no"}', flush=True)

# SEÑAL #40 (notas/11): LA INSISTENCIA. Lo seguro predice el año que viene; lo extraordinario lo desmiente siempre para el mismo lado.
from sklearn.ensemble import HistGradientBoostingRegressor
MET = [m for m in ['margen_op', 'margen_bruto', 'crec_ventas_1', 'roa', 'fco_activos'] if m in Rn.columns]
res['insistencia'] = {'medidas': MET, 'camadas': {}}
if '_ret1' in df.columns and MET:
    t40 = time.time()
    clave = pd.Series(df.index.values, index=pd.MultiIndex.from_arrays([df['id'], df['anio']]))
    clave = clave[~clave.index.duplicated()]
    def fila_de(k):        # índice de la fila de la misma empresa k años antes (o -1)
        v = clave.reindex(pd.MultiIndex.from_arrays([df['id'], df['anio'] - k])).values
        return np.where(np.isnan(v.astype(float)), -1, v).astype(int)
    p1, p2_ = fila_de(1), fila_de(2)
    tiene = p1 >= 0
    Xprev = np.full((len(df), len(X_cols)), np.nan)
    Xprev[tiene] = R[X_cols].values[p1[tiene]]
    anio = df['anio'].values
    desv = np.full((len(df), len(MET)), np.nan)
    for s in range(2015, int(anio.max()) + 1):
        for j, m in enumerate(MET):
            y = Rn[m].values
            A = tiene & (anio >= s - 6) & (anio <= s - 1) & ~np.isnan(y)
            B = tiene & (anio == s) & ~np.isnan(y)
            if A.sum() < mA or B.sum() == 0:
                continue
            mod = HistGradientBoostingRegressor(max_iter=100, learning_rate=0.1, max_leaf_nodes=15, random_state=0).fit(Xprev[A], y[A])
            desv[B, j] = y[B] - mod.predict(Xprev[B])
    print(f'INSIST modelos de lo seguro listos en {time.time() - t40:.0f}s', flush=True)
    def fraccion(D):       # fracción de desvíos positivos en t, t-1, t-2 (5 medidas x 3 años)
        tres = [D, np.where(p1[:, None] >= 0, D[np.maximum(p1, 0)], np.nan), np.where(p2_[:, None] >= 0, D[np.maximum(p2_, 0)], np.nan)]
        st = np.concatenate(tres, axis=1)
        disp = (~np.isnan(st)).sum(1); posi = (st > 0).sum(1)
        return np.where(disp >= 9, posi / np.maximum(disp, 1), np.nan), np.nanmean(np.where(disp[:, None] >= 9, st, np.nan), axis=1)
    frac, media = fraccion(desv)
    rng40 = np.random.default_rng(40)
    mez = desv.copy()                      # azar: desvíos mezclados entre empresas dentro de cada año
    for s in np.unique(anio):
        ii = np.where(anio == s)[0]
        for j in range(len(MET)):
            mez[ii, j] = desv[rng40.permutation(ii), j]
    frac_mez, _ = fraccion(mez)
    nivel = np.nanmean(Rn[MET].values, axis=1)
    for t in range(2017, 2025):
        idx = np.where((anio == t) & ~np.isnan(frac))[0]
        if len(idx) < mc36:
            continue
        sc = frac[idx] + 1e-3 * np.nan_to_num(media[idx])
        rk = pd.Series(sc).rank(method='first', pct=True).values
        ins, rev = rk > 0.9, rk <= 0.1
        foto = pd.Series(nivel[idx]).rank(method='first', pct=True).values > 0.9
        r1 = r1all.values[idx]; r6 = r6all.values[idx]
        def met40(mask):
            a = r1[mask & ~np.isnan(r1)]; b = r6[mask & ~np.isnan(r6)]
            o = {'n': int(mask.sum()), 'tamano_medio': round(float(np.nanmean(Rn['log_activos'].values[idx][mask])), 3)}
            if len(a) >= 30:
                o.update({'prom_12m': round(float(a.mean()), 3), 'mediana_12m': round(float(np.median(a)), 3),
                          'pct_x2_12m': round(100 * float((a >= 2).mean()), 2), 'pct_desastre_12m': round(100 * float((a <= 0.5).mean()), 2)})
            if len(b) >= 30 and t <= 2019:
                o.update({'n6': int(len(b)), 'pct_x3_6a': round(100 * float((b >= 3).mean()), 2),
                          'pct_desastre_6a': round(100 * float((b <= 0.25).mean()), 2), 'prom_6a': round(float(b.mean()), 3)})
            return o
        fila = {'universo': met40(np.ones(len(idx), bool)), 'insistentes': met40(ins), 'al_reves': met40(rev), 'foto_calidad': met40(foto)}
        ok_mez = (anio == t) & ~np.isnan(frac_mez)
        fila['azar'] = {'real_pct_80': round(100 * float((frac[idx] >= 0.8).mean()), 2),
                        'mezclado_pct_80': round(100 * float((frac_mez[ok_mez] >= 0.8).mean()), 2) if ok_mez.sum() else None}
        ok6 = ~np.isnan(r6)
        if t <= 2019 and ok6.sum() >= 300:
            g3 = ok6 & (r6 >= 3)
            fila['estela'] = {'x3_insistentes_pct': round(100 * float(ins[g3].mean()), 2), 'peso_pct': round(100 * float(ins[ok6].mean()), 2)}
        res['insistencia']['camadas'][t] = fila
        print(f'INSIST {t} azar {fila["azar"]} ' + (f'estela {fila["estela"]} ' if 'estela' in fila else '') + '| ' + ' | '.join(
            f"{g}: n {x['n']} tam {x['tamano_medio']} prom {x.get('prom_12m')} x2 {x.get('pct_x2_12m')}% des {x.get('pct_desastre_12m')}%"
            + (f" ·6a x3 {x.get('pct_x3_6a')}% des {x.get('pct_desastre_6a')}%" if 'n6' in x else '')
            for g, x in fila.items() if 'n' in x), flush=True)
    C = res['insistencia']['camadas']
    pa = sum(1 for f in C.values() if f['azar']['mezclado_pct_80'] and f['azar']['real_pct_80'] >= 1.3 * f['azar']['mezclado_pct_80'])
    eb = [f['estela'] for f in C.values() if 'estela' in f]
    pb = sum(1 for e in eb if e['peso_pct'] and e['x3_insistentes_pct'] >= 1.5 * e['peso_pct'])
    ok1 = ok2 = ok3 = n3 = 0; exc = []
    for f in C.values():
        u, c = f['universo'], f['insistentes']
        if 'prom_12m' in u and 'prom_12m' in c:
            exc.append(c['prom_12m'] - u['prom_12m']); ok1 += c['prom_12m'] > u['prom_12m']
            ok2 += (c['pct_x2_12m'] > u['pct_x2_12m']) and (c['pct_desastre_12m'] <= u['pct_desastre_12m'])
        if 'n6' in u and 'n6' in c:
            n3 += 1; ok3 += (c['pct_x3_6a'] > u['pct_x3_6a']) and (c['pct_desastre_6a'] < u['pct_desastre_6a'])
    res['criterio_insistencia'] = {'pasoA_existe': f'{pa} de {len(C)}', 'pasoA_pasa': bool(len(C) and pa >= 6),
                                   'pasoB_estela': f'{pb} de {len(eb)}', 'pasoB_pasa': bool(pb >= 2),
                                   'camadas_12m': len(exc), 'gana_promedio': int(ok1), 'exceso_medio': round(float(np.mean(exc)), 4) if exc else None,
                                   'colas_mejores_12m': int(ok2), 'colas_mejores_6a': f'{ok3} de {n3}',
                                   'pasoC_pasa': bool(exc and ok1 >= 6 and np.mean(exc) >= 0.02 and ok2 >= 6 and ok3 >= 2)}
    print(f'CRITERIO insistencia: {res["criterio_insistencia"]} ({time.time() - t40:.0f}s)', flush=True)

# Referencia para puntuar empresas nuevas: cuantiles de cada rasgo en el último año completo
grandes = df['anio'][df.groupby('anio')['anio'].transform('size') > 3000]
ult = int(grandes.max()) if len(grandes) else int(df['anio'].max())
os.makedirs('modelos', exist_ok=True)
ref = {c: np.nanquantile(df.loc[df.anio == ult, c], np.linspace(0, 1, 201)).tolist() for c in num}
json.dump({'anio_referencia': ult, 'cuantiles': ref}, open('modelos/referencia.json', 'w'))

# PRUEBA CONGELADA: predicciones de hoy para todas las empresas del último año completo.
# Se guarda con su huella (sha256). Dentro de 6 y 10 años se compara contra lo que pase:
# es la única prueba que nadie pudo mirar ni acomodar.
import hashlib, glob as _g
hoy = R[df['anio'] == ult][['id', 'anio']].copy()
for p_ in sorted(_g.glob('modelos/*.joblib')):
    mm = joblib.load(p_)
    hoy[mm['etiqueta']] = mm['modelo'].predict_proba(R.loc[hoy.index, mm['rasgos']])[:, 1]
hoy['cinco'] = puntaje_cinco(Rn.loc[hoy.index])
hoy.to_csv('predicciones_congeladas.csv', index=False)
huella = hashlib.sha256(open('predicciones_congeladas.csv', 'rb').read()).hexdigest()
res['congeladas'] = {'anio': ult, 'empresas': int(len(hoy)), 'sha256': huella}
print('CONGELADAS', len(hoy), 'empresas del año', ult, 'sha256', huella, flush=True)
res['segundos'] = time.time() - t0
json.dump(res, open(salida, 'w'), indent=1, default=float)
print('LISTO', f'{time.time()-t0:.0f}s', flush=True)
