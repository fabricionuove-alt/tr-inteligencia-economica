"""Señal #42 (notas/11): los que creen y aguantan. ¿Las caídas en las que alguien que sabe sigue comprando
terminan mejor que las caídas en las que nadie creyó?
Uso: python creyentes.py T13F PRECIOS ACCIONES FILAS DIRECTIVOS [salida.json]
  (listas de csv separadas por coma; FILAS = id, anio, estado_final)
Fecha de compra de cada trimestre = cierre del trimestre + 3 meses (todos los 13F ya presentados: el plazo es 45 días).
Valor de mercado = precio × acciones conocidas en ese momento. Quiebra en el medio = pérdida total."""
import sys, bisect, collections, json, time
import numpy as np, pandas as pd

t0 = time.time()
leer = lambda arg, **k: pd.concat([pd.read_csv(x, **k) for x in arg.split(',') if x])
salida = sys.argv[6] if len(sys.argv) > 6 else 'creyentes.json'
def suma(m, k):
    y, mm = int(m[:4]), int(m[4:6]) + k
    y += (mm - 1) // 12; mm = (mm - 1) % 12 + 1
    return f'{y:04d}{mm:02d}'

# precios y acciones (como evaluar_ideas.py)
pr = leer(sys.argv[2], dtype={'id': str, 'mes': str}).sort_values('fuente', ascending=False).drop_duplicates(['id', 'mes'])
P = {(i, m): p for i, m, p in zip(pr['id'], pr['mes'], pr['precio'])}
ac = leer(sys.argv[3], dtype={'id': str}).dropna(subset=['presentado', 'acciones'])
ac['pres'] = ac['presentado'].str[:4] + ac['presentado'].str[5:7]
S = collections.defaultdict(list)
for i, m, q in sorted(zip(ac['id'], ac['pres'], ac['acciones'])):
    S[i].append((m, q))
def acciones(i, m):
    s = S.get(i)
    if not s:
        return None
    k = bisect.bisect_right(s, (m, float('inf'))) - 1
    return s[k][1] if k >= 0 else None
def mcap(i, m):
    for d in (0, 1, -1):
        p = P.get((i, suma(m, d)))
        if p is not None:
            q = acciones(i, m)
            return p * q if q else None
    return None
fil = pd.read_csv(sys.argv[4], usecols=['id', 'anio', 'estado_final'], dtype={'id': str})
muere = {i: g['anio'].max() for i, g in fil[fil['estado_final'].isin(['quiebra', 'revocada'])].groupby('id')}
di = leer(sys.argv[5], dtype={'id': str, 'mes': str, 'dueno': str})
DI = collections.defaultdict(list)
for i, m, t in sorted(zip(di['id'], di['mes'], di['tipo'])):
    DI[i].append((m, t))
DM = {i: [x[0] for x in v] for i, v in DI.items()}
def tratos(i, desde, hasta):        # tipos de las operaciones de directivos con desde <= mes < hasta
    v = DI.get(i)
    if not v:
        return []
    return [t for _, t in v[bisect.bisect_left(DM[i], desde):bisect.bisect_left(DM[i], hasta)]]
print(f'CREY datos cargados {time.time() - t0:.0f}s', flush=True)

# 13F: fracción de la empresa que tiene cada fondo, trimestre a trimestre
T = leer(sys.argv[1], dtype={'periodo': str, 'fondo': str, 'id': str})
T = T[T['periodo'].str[4:6].isin(['03', '06', '09', '12'])]
T['q'] = T['periodo'].str[:4].astype(int) * 4 + T['periodo'].str[4:6].astype(int) // 3 - 1
qa = {(i, p): acciones(i, p) for i, p in set(zip(T['id'], T['periodo']))}
T['frac'] = T['acciones'] / [qa.get((i, p)) or np.nan for i, p in zip(T['id'], T['periodo'])]
T = T.dropna(subset=['frac'])[['fondo', 'id', 'q', 'frac']]
base = T.copy()
for k in (1, 2, 3, 4):
    L = T.rename(columns={'frac': f'f{k}'}); L['q'] = L['q'] + k
    base = base.merge(L, on=['fondo', 'id', 'q'], how='left')
base['creyente'] = base[['f1', 'f2', 'f3', 'f4']].notna().all(axis=1) & (base['frac'] >= 1.1 * base['f4'])
crey = base.groupby(['id', 'q'])['creyente'].sum()
h4 = T.assign(q=T['q'] + 4).groupby(['id', 'q']).size()        # fondos concentrados que la tenían hace 4 trimestres
print(f'CREY 13F: {len(T)} posiciones, {int(base["creyente"].sum())} casos de creyente, {time.time() - t0:.0f}s', flush=True)

ids = sorted({i for i, _ in P})
qs = sorted(set(T['q']))
filas = []
for q in qs:
    a_, r_ = divmod(q, 4)
    m = suma(f'{a_:04d}{3 * (r_ + 1):02d}', 3)
    if not ('201401' <= m <= '202412'):
        continue
    m12, m72, mm12 = suma(m, 12), suma(m, 72), suma(m, -12)
    for i in ids:
        a = mcap(i, m)
        if not a:
            continue
        antes = mcap(i, mm12)
        b = mcap(i, m12); c = mcap(i, m72) if m <= '201912' else None
        r1 = b / a if b else (0.0 if i in muere and muere[i] < int(m12[:4]) else np.nan)
        r6 = (c / a if c else (0.0 if i in muere and muere[i] < int(m72[:4]) else np.nan)) if m <= '201912' else np.nan
        tr = tratos(i, mm12, m)
        filas.append((m, i, a, (a / antes) if antes else np.nan, r1, r6, int(crey.get((i, q), 0)), int(h4.get((i, q), 0)),
                      tr.count('P'), tr.count('S')))
X = pd.DataFrame(filas, columns=['mes', 'id', 'mcap', 'cambio12', 'r1', 'r6', 'creyentes', 'fondos_antes', 'compras', 'ventas'])
X.loc[~((X['r1'] > 0) & (X['r1'] < 20)) & (X['r1'] != 0), 'r1'] = np.nan
X.loc[~((X['r6'] > 0) & (X['r6'] < 50)) & (X['r6'] != 0), 'r6'] = np.nan
X['tam'] = X.groupby('mes')['mcap'].rank(pct=True)
X[['mes', 'id', 'cambio12', 'creyentes', 'fondos_antes', 'compras', 'ventas']].to_csv('personas.csv', index=False)   # para #43
X['anio'] = X['mes'].str[:4].astype(int)
cae = X['cambio12'] <= 0.8
G = {'universo': np.ones(len(X), bool), 'caidas': cae,
     'creyentes_2': cae & (X['creyentes'] >= 2), 'creyentes_1': cae & (X['creyentes'] >= 1),
     'control_creyentes': cae & (X['fondos_antes'] >= 2) & (X['creyentes'] == 0),
     'adentro_compran': cae & (X['compras'] > 0) & (X['ventas'] == 0), 'control_adentro': cae & (X['ventas'] > 0) & (X['compras'] == 0)}
G = {k: np.asarray(v) for k, v in G.items()}
print(f'CREY tabla {len(X)} filas, {X["mes"].nunique()} fechas, {time.time() - t0:.0f}s', flush=True)

def met(mask):
    a = X['r1'].values[mask]; a = a[~np.isnan(a)]; b = X['r6'].values[mask]; b = b[~np.isnan(b)]
    o = {'n': int(mask.sum()), 'tam': round(float(X['tam'].values[mask].mean()), 3) if mask.sum() else None}
    if len(a) >= 30:
        o.update({'prom_12m': round(float(a.mean()), 3), 'mediana_12m': round(float(np.median(a)), 3),
                  'pct_x2_12m': round(100 * float((a >= 2).mean()), 2), 'pct_desastre_12m': round(100 * float((a <= 0.5).mean()), 2)})
    if len(b) >= 30:
        o.update({'n6': int(len(b)), 'pct_x3_6a': round(100 * float((b >= 3).mean()), 2),
                  'pct_desastre_6a': round(100 * float((b <= 0.25).mean()), 2), 'prom_6a': round(float(b.mean()), 3)})
    return o
res = {'por_anio': {}}
for y in range(2014, 2025):
    en = X['anio'].values == y
    fila = {g: met(en & v) for g, v in G.items()}
    ok6 = en & ~np.isnan(X['r6'].values)
    if ok6.sum() >= 300:
        g3 = ok6 & (X['r6'].values >= 3)
        fila['estela'] = {g: {'x3_en_grupo_pct': round(100 * float(G[g][g3].mean()), 2), 'peso_pct': round(100 * float(G[g][ok6].mean()), 2)}
                          for g in ('creyentes_2', 'creyentes_1', 'adentro_compran')}
    res['por_anio'][y] = fila
    print(f'CREY {y}: ' + ' | '.join(f"{g}: n {x['n']} tam {x['tam']} prom {x.get('prom_12m')} x2 {x.get('pct_x2_12m')}% des {x.get('pct_desastre_12m')}%"
                                    + (f" ·6a x3 {x['pct_x3_6a']}% des {x['pct_desastre_6a']}%" if 'n6' in x else '')
                                    for g, x in fila.items() if g != 'estela')
          + (f" | estela {fila['estela']}" if 'estela' in fila else ''), flush=True)

def criterio(g, ctrl):
    A = res['por_anio']; c1 = c2 = n6 = 0; exc = []
    for y, f in A.items():
        x, c, u = f[g], f[ctrl], f['universo']
        if 'n6' in x and 'n6' in c and 'n6' in u:
            n6 += 1
            c1 += (x['pct_x3_6a'] > c['pct_x3_6a']) and (x['pct_desastre_6a'] <= c['pct_desastre_6a'])
            c2 += x['pct_x3_6a'] > u['pct_x3_6a']
        if 'prom_12m' in x and 'prom_12m' in c:
            exc.append(x['prom_12m'] - c['prom_12m'])
    e = round(float(np.mean(exc)), 4) if exc else None
    return {'anios_6a': n6, 'vs_control_6a': f'{c1} de {n6}', 'vs_universo_6a': f'{c2} de {n6}', 'exceso_12m_vs_control': e,
            'pasa': bool(n6 >= 4 and c1 >= 4 and c2 >= 4 and e is not None and e >= 0)}
res['criterio'] = {'creyentes': criterio('creyentes_2', 'control_creyentes'), 'adentro': criterio('adentro_compran', 'control_adentro'),
                   'creyentes_1_informativo': criterio('creyentes_1', 'control_creyentes')}
for k, v in res['criterio'].items():
    print(f'CRITERIO {k}: {v} -> {"PASA" if v["pasa"] else "no pasa"}', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
print(f'LISTO {time.time() - t0:.0f}s', flush=True)
