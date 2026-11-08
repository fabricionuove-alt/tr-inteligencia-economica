"""Tr a 4 años (#64, notas/11): árboles como Tr, pero aprende a duplicarse / hundirse en 4 años, con y sin los temas de la élite.
Uso: python tr4.py filas.csv personas.csv FALLAS_CSVS TEMA10K_CSVS [salida.json]
Cada camada s aprende sólo con filas ≤ s-4 (su resultado a 4 años ya se conocía al comprar). Cartera Kelly f = 2·P2 - PD, tope 5%.
Con FINAL=1 aprende con todo lo que tiene resultado a 4 años y arma la cartera de la última camada (lista congelada)."""
import sys, os, json, time
import numpy as np, pandas as pd
_aqui = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_aqui, 'kelly.py'), encoding='utf-8').read().split("res = {'camadas': {}}")[0])
from sklearn.metrics import roc_auc_score
salida = sys.argv[5] if len(sys.argv) > 5 else 'tr4.json'
t1 = time.time()
T = pd.concat([pd.read_csv(x, dtype={'id': str}) for x in sys.argv[4].split(',') if x and 'gemma' not in x]).drop_duplicates(['id', 'anio_presentado'])
temas = [c for c in T.columns if c.startswith(('b_', 't_'))]
T = T[T['palabras'] >= 300].copy()
dens = T[temas].div(T['palabras'], axis=0) * 1000; dens['tema_total'] = dens.sum(axis=1)
T = pd.concat([T[['id', 'anio_presentado']], dens], axis=1)
pres = pd.to_numeric(df['_presentado'].astype(str).str[:4], errors='coerce')
j = pd.DataFrame({'i': df.index, 'id': df['id'], 'anio_presentado': pres}).merge(T, on=['id', 'anio_presentado'], how='left')
TEM = []
for c in temas + ['tema_total']:
    R['tem_' + c] = pd.Series(j[c].values, index=j['i'].values).reindex(df.index).groupby(df['anio']).rank(pct=True); TEM.append('tem_' + c)
GEM = []
_gp = [x for x in sys.argv[4].split(',') if 'gemma_puntaje' in x] or [os.environ.get('GEMMA', '')]
if _gp[0] and os.path.exists(_gp[0]):
    G = pd.read_csv(_gp[0], dtype={'id': str}).dropna(subset=['gemma']).drop_duplicates(['id', 'anio_presentado'])
    jg = pd.DataFrame({'i': df.index, 'id': df['id'], 'anio_presentado': pres}).merge(G, on=['id', 'anio_presentado'], how='left')
    R['gemma'] = pd.Series(jg['gemma'].values, index=jg['i'].values).reindex(df.index).groupby(df['anio']).rank(pct=True); GEM = ['gemma']
    print(f'TR4 gemma con dato: {int(R["gemma"].notna().sum())} filas', flush=True)
r4 = num_('_ret4').values.copy()
r4[np.isnan(r4) & df['estado_final'].isin(['quiebra', 'revocada']).values & (ult.values < df['anio'].values + 4)] = 0.0
en4 = ~np.isnan(r4)
dobla4 = (np.nan_to_num(r4, nan=1.0) >= 2).astype(int); des4 = (np.nan_to_num(r4, nan=1.0) <= 0.5).astype(int)
print(f'TR4 filas con resultado a 4 años: {int(en4.sum())}; con temas: {int((en4 & R["tem_tema_total"].notna().values).sum())} '
      f'| temas por año {R["tem_tema_total"].notna().groupby(df["anio"]).sum().to_dict()} ({time.time() - t1:.0f}s)', flush=True)
def arbol(cols, A, y_, k):
    c = [x for x in cols if R.loc[A, x].nunique() >= 3]
    return hgb().fit(R.loc[A, c].values, y_[A]).predict_proba(R.loc[k, c].values)[:, 1]
def cartera(p2, pdes, r):
    w = pesos(p2, pdes); m = (r >= 2) | (r <= 0.5)
    lado = float(roc_auc_score((r[m] >= 2).astype(int), (p2 - pdes)[m])) if m.sum() > 20 else np.nan
    return {'ret': round(float((w * r).sum() + 1 - w.sum()), 4), 'des': round(100 * float(w[r <= 0.5].sum()), 2), 'lado': round(lado, 4), 'empresas': int((w > 0).sum())}

if os.environ.get('FINAL12') == '1':                      # Tr del juego: 12 meses, con Gemma a ciegas
    cuenta = pd.Series(anio).value_counts(); ultima = int(max(a for a, n in cuenta.items() if n >= 1000))   # último año completo
    k = np.where(anio == ultima)[0]; cols = COLS + GEM
    p2, pdes = arbol(cols, en, dobla, k), arbol(cols, en, desastre, k); w = pesos(p2, pdes)
    out = pd.DataFrame({'id': df['id'].values[k], 'anio': ultima, 'p2': p2.round(5), 'pdes': pdes.round(5), 'peso': w.round(6),
                        'gemma': R.loc[k, 'gemma'].round(4).values if GEM else np.nan})
    out = out[out['peso'] > 0].sort_values('peso', ascending=False); out.to_csv('tr_gemma_congelada.csv', index=False)
    print(f'TRG FINAL camada {ultima}: {len(out)} empresas con peso, máximo {out["peso"].max():.4f}, con Gemma {int(R.loc[k, "gemma"].notna().sum()) if GEM else 0} de {len(k)} ({time.time() - t1:.0f}s)', flush=True)
    sys.exit(0)
if os.environ.get('FINAL') == '1':
    ultima = int(anio.max()); k = np.where(anio == ultima)[0]
    p2, pdes = arbol(COLS + TEM, en4, dobla4, k), arbol(COLS + TEM, en4, des4, k)
    w = pesos(p2, pdes)
    out = pd.DataFrame({'id': df['id'].values[k], 'anio': ultima, 'p2': p2.round(5), 'pdes': pdes.round(5), 'peso': w.round(6)})
    out = out[out['peso'] > 0].sort_values('peso', ascending=False); out.to_csv('tr4_congelada.csv', index=False)
    print(f'TR4 FINAL camada {ultima}: {len(out)} empresas con peso, máximo {out["peso"].max():.4f}, con temas {int(R.loc[k, "tem_tema_total"].notna().sum())} de {len(k)} ({time.time() - t1:.0f}s)', flush=True)
    sys.exit(0)

res = {'camadas': {}}
for s in [int(x) for x in os.environ.get('CAMADAS', '2017,2018,2019').split(',')]:
    A = en4 & (anio <= s - 4); k = np.where((anio == s) & en4)[0]
    if A.sum() < mA or len(k) < mc:
        print(f'TR4 {s}: no alcanza ({int(A.sum())}, {len(k)})', flush=True); continue
    r = r4[k]; fila = {'universo': round(float(r.mean()), 4), 'des_universo': round(100 * float((r <= 0.5).mean()), 2),
                       'tr4': cartera(arbol(COLS, A, dobla4, k), arbol(COLS, A, des4, k), r),
                       'tr4+t': cartera(arbol(COLS + TEM, A, dobla4, k), arbol(COLS + TEM, A, des4, k), r)}
    if GEM:
        fila['tr4+g'] = cartera(arbol(COLS + GEM, A, dobla4, k), arbol(COLS + GEM, A, des4, k), r)
        A12 = en & (anio <= s - 2); k12 = np.where((anio == s) & en)[0]; r12 = r1[k12]
        fila['u12'] = round(float(r12.mean()), 4)
        fila['tr12'] = cartera(arbol(COLS, A12, dobla, k12), arbol(COLS, A12, desastre, k12), r12)
        fila['tr12+g'] = cartera(arbol(COLS + GEM, A12, dobla, k12), arbol(COLS + GEM, A12, desastre, k12), r12)
        print(f'TR4G {s} | 4 años: sin ×{fila["tr4"]["ret"]} des {fila["tr4"]["des"]}% | con Gemma ×{fila["tr4+g"]["ret"]} des {fila["tr4+g"]["des"]}% lado {fila["tr4+g"]["lado"]} (sin {fila["tr4"]["lado"]}) || '
              f'12 meses: universo ×{fila["u12"]} | sin ×{fila["tr12"]["ret"]} des {fila["tr12"]["des"]}% | con Gemma ×{fila["tr12+g"]["ret"]} des {fila["tr12+g"]["des"]}% lado {fila["tr12+g"]["lado"]} (sin {fila["tr12"]["lado"]})', flush=True)
    res['camadas'][s] = fila
    print(f'TR4 {s} (aprende ≤ {s - 4}) | universo ×{fila["universo"]} des {fila["des_universo"]}% | sin temas ×{fila["tr4"]["ret"]} des {fila["tr4"]["des"]}% lado {fila["tr4"]["lado"]} | '
          f'con temas ×{fila["tr4+t"]["ret"]} des {fila["tr4+t"]["des"]}% lado {fila["tr4+t"]["lado"]} ({time.time() - t1:.0f}s)', flush=True)
    json.dump(res, open(salida, 'w'), indent=1)
C = res['camadas']; n = len(C)
gt = sum(C[s]['tr4+t']['ret'] > C[s]['tr4']['ret'] for s in C); gu = sum(C[s]['tr4+t']['ret'] > C[s]['universo'] for s in C)
dok = sum(C[s]['tr4+t']['des'] <= C[s]['tr4']['des'] + 1 for s in C)
res['criterio'] = {'temas_suman': f'{gt} de {n}', 'gana_universo': f'{gu} de {n}', 'desastres_ok': f'{dok} de {n}', 'juega': bool(n == 3 and gt >= 2 and gu == 3 and dok >= 2)}
print('CRITERIO TR4:', res['criterio'], flush=True)
if GEM:
    for h, b, u in (('4a', 'tr4', 'universo'), ('12m', 'tr12', 'u12')):
        gg = sum(C[s][b + '+g']['ret'] > C[s][b]['ret'] for s in C); gu = sum(C[s][b + '+g']['ret'] > C[s][u] for s in C); dd = sum(C[s][b + '+g']['des'] <= C[s][b]['des'] + 1 for s in C)
        res['criterio_gemma_' + h] = {'gana_a_tr': f'{gg} de {n}', 'gana_universo': f'{gu} de {n}', 'desastres_ok': f'{dd} de {n}', 'entra': bool(n == 3 and gg >= 2 and gu == 3 and dd >= 2)}
        print(f'CRITERIO GEMMA {h}:', res['criterio_gemma_' + h], flush=True)
json.dump(res, open(salida, 'w'), indent=1)
