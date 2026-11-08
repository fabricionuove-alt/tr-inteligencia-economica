"""Señales #52-#54 (notas/11): red de directores, contagio por la red y control familiar, sumados a Kelly (#50).
Uso: python red.py filas.csv personas.csv FALLAS_CSVS red.csv PRECIOS_CSVS [salida.json]"""
import sys, os, json, time, collections
import numpy as np, pandas as pd
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kelly.py'), encoding='utf-8').read()
exec(_src.split("res = {'camadas': {}}")[0])
import networkx as nx
from sklearn.metrics import roc_auc_score
salida = sys.argv[6] if len(sys.argv) > 6 else 'red.json'
t1 = time.time()

red = pd.read_csv(sys.argv[4], dtype={'id': str, 'dueno': str, 'apellido': str, 'rol': str})
pr = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[5].split(',') if x])
if 'fuente' in pr.columns:
    pr = pr.sort_values('fuente', ascending=False)
pr = pr.drop_duplicates(['id', 'mes'])
pr['m'] = pr['mes'].str[:4].astype(int) * 12 + pr['mes'].str[4:6].astype(int) - 1
P = {(i, m): p for i, m, p in zip(pr['id'], pr['m'], pr['precio']) if p > 0}
mcompra = (mp + 1).values                                     # mes de compra de cada fila (meses corridos)

B = {k: pd.DataFrame(np.nan, index=df.index, columns=c) for k, c in {
    'central': ['grado', 'cercania', 'intermed', 'directores', 'multi'],
    'contagio': ['vec_ret', 'vec_x2', 'vec_des', 'vec_n'],
    'familia': ['personas_10', 'apellido_rep', 'apellidos_n']}.items()}
filas_de = collections.defaultdict(list)
for i, (a, id_) in enumerate(zip(df['anio'].values, df['id'].values)):
    filas_de[(int(a), id_)].append(i)
rg = np.random.default_rng(0)
for a, g in red.groupby('anio'):
    a = int(a)
    dirs = g[g['rol'].str.contains('D')]
    emp_de = dirs.groupby('dueno')['id'].apply(lambda s: sorted(set(s)))
    G = nx.Graph(); G.add_nodes_from(dirs['id'].unique())
    for es in emp_de.values:
        if 1 < len(es) <= 30:                                   # más de 30 = cuentas de fondos, no personas
            for x in range(len(es)):
                for y in range(x + 1, len(es)):
                    G.add_edge(es[x], es[y])
    nodos = list(G.nodes)
    if not nodos:
        continue
    fuentes = rg.choice(nodos, size=min(300, len(nodos)), replace=False)
    harm = collections.Counter()
    for s_ in fuentes:
        for v, d in nx.single_source_shortest_path_length(G, s_).items():
            if d > 0:
                harm[v] += 1.0 / d
    bet = nx.betweenness_centrality(G, k=min(300, len(nodos)), seed=0)
    nb = emp_de.apply(len)
    multi = dirs.assign(n=dirs['dueno'].map(nb)).groupby('id')['n'].apply(lambda s: float((s > 1).mean()))
    ndir = dirs.groupby('id')['dueno'].nunique()
    gt = g[g['rol'].str.contains('T') & (g['persona'] == 1)].groupby('id')['dueno'].nunique()
    gp = g[g['rol'].str.contains('[DO]') & (g['persona'] == 1) & g['apellido'].notna()]
    rep = gp.groupby(['id', 'apellido'])['dueno'].nunique()
    rep = rep[rep >= 2].groupby('id').size()
    for id_ in set(g['id']):
        for i in filas_de.get((a, id_), []):
            if id_ in G:
                B['central'].iloc[i] = [G.degree(id_), harm[id_], bet.get(id_, 0.0), ndir.get(id_, 0), multi.get(id_, 0.0)]
                m_ = mcompra[i]
                if not np.isnan(m_):
                    m_ = int(m_); rs = []
                    for j in G.neighbors(id_):
                        p0, p1_ = P.get((j, m_ - 13)), P.get((j, m_ - 1))
                        if p0 and p1_:
                            rs.append(p1_ / p0)
                    if rs:
                        rs = np.array(rs)
                        B['contagio'].iloc[i] = [float(np.mean(np.log(rs))), float((rs >= 2).mean()), float((rs <= 0.5).mean()), len(rs)]
            B['familia'].iloc[i] = [gt.get(id_, 0), int(rep.get(id_, 0) > 0), rep.get(id_, 0)]
    print(f'RED {a}: {G.number_of_nodes()} empresas, {G.number_of_edges()} uniones, {len(emp_de)} directores ({time.time() - t1:.0f}s)', flush=True)
BL = {}
for k, X in B.items():
    BL[k] = []
    for c in X.columns:
        R[f'{k}_{c}'] = X[c].astype(float).groupby(df['anio']).rank(pct=True); BL[k].append(f'{k}_{c}')
    print(f'BLOQUE {k}: ' + ', '.join(f'{c} {int(R[c].notna().sum())}' for c in BL[k]), flush=True)

def modelo(cols, A, y_):
    c = [x for x in cols if R.loc[A, x].nunique() >= 3]
    return hgb().fit(R.loc[A, c].values, y_[A]), c
def kelly_de(p2, pdes, r):
    w = pesos(p2, pdes)
    return float((w * r).sum() + 1 - w.sum()), 100 * float(w[r <= 0.5].sum())
def lado(p2, pdes, r):
    m = (r >= 2) | (r <= 0.5)
    return float(roc_auc_score((r[m] >= 2).astype(int), (p2 - pdes)[m])) if m.sum() > 20 and 0 < (r[m] >= 2).mean() < 1 else np.nan
N = 100
res = {'camadas': {}}
for s in range(2019, 2025):
    A = en & (anio <= s - 2)
    k = np.where((anio == s) & en)[0]
    if A.sum() < mA or len(k) < mc:
        print(f'RED {s}: no alcanza', flush=True); continue
    r = r1[k]; t = tam[k].astype(float)
    dec = np.full(len(k), -1); ok = ~np.isnan(t)
    if ok.sum():
        dec[ok] = np.minimum((np.argsort(np.argsort(t[ok], kind='stable'), kind='stable') * 10) // ok.sum(), 9)
    m2, c2 = modelo(COLS, A, dobla); mD, cD = modelo(COLS, A, desastre)
    b2, bD = m2.predict_proba(R.loc[k, c2].values)[:, 1], mD.predict_proba(R.loc[k, cD].values)[:, 1]
    base = {'lado': lado(b2, bD, r)}; base['ret'], base['des'] = kelly_de(b2, bD, r)
    fila = {'base': {x: round(v, 4) for x, v in base.items()}}
    for nb_, cols in BL.items():
        m2, c2 = modelo(COLS + cols, A, dobla); mD, cD = modelo(COLS + cols, A, desastre)
        X2, XD = R.loc[k, c2].copy(), R.loc[k, cD].copy()
        p2, pd_ = m2.predict_proba(X2.values)[:, 1], mD.predict_proba(XD.values)[:, 1]
        ret, des = kelly_de(p2, pd_, r); ld = lado(p2, pd_, r)
        rets = []
        for sem in range(N):
            g = np.random.default_rng(sem); idx = np.arange(len(k))
            for d in np.unique(dec):
                mm = np.where(dec == d)[0]; idx[mm] = g.permutation(mm)
            Y2, YD = X2.copy(), XD.copy()
            for c in cols:
                if c in Y2: Y2[c] = X2[c].values[idx]
                if c in YD: YD[c] = XD[c].values[idx]
            rets.append(kelly_de(m2.predict_proba(Y2.values)[:, 1], mD.predict_proba(YD.values)[:, 1], r)[0])
        p95 = float(np.percentile(rets, 95))
        fila[nb_] = {'lado': round(ld, 4), 'ret': round(ret, 4), 'des': round(des, 2), 'placebo_p95': round(p95, 4),
                     'placebo_mediana': round(float(np.median(rets)), 4),
                     'c1': bool(ld - base['lado'] >= 0.01), 'c2': bool(ret > p95), 'c3': bool(des <= base['des'] + 0.5)}
        f = fila[nb_]
        print(f'RED {s} {nb_:8s} | lado {f["lado"]} vs {base["lado"]:.4f} | Kelly ×{f["ret"]} vs ×{base["ret"]:.4f} (placebo p95 ×{f["placebo_p95"]}) | '
              f'des {f["des"]}% vs {base["des"]:.2f}% ({time.time() - t1:.0f}s)', flush=True)
    res['camadas'][s] = fila
    json.dump(res, open(salida, 'w'), indent=1)
C = res['camadas']; n = len(C); res['criterio'] = {}
for nb_ in BL:
    c1 = sum(C[s][nb_]['c1'] for s in C); c2 = sum(C[s][nb_]['c2'] for s in C); c3 = sum(C[s][nb_]['c3'] for s in C)
    res['criterio'][nb_] = {'lado': f'{c1} de {n}', 'placebo': f'{c2} de {n}', 'desastres': f'{c3} de {n}',
                            'sobrevive': bool(n == 6 and c1 >= 5 and c2 >= 5 and c3 >= 4)}
    print(f'CRITERIO {nb_}: {res["criterio"][nb_]}', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
