"""¿Las mejores ideas de los fondos le ganan a la mediana del mercado a 12 meses? (señal #35, criterio en notas/11)
Uso: python evaluar_ideas.py IDEAS PRECIOS ACCIONES FILAS
  IDEAS/PRECIOS/ACCIONES: listas de csv separadas por coma; FILAS: filas.csv (para saber quiénes quebraron)
Valor de mercado = precio del mes × acciones en circulación conocidas en ese momento (portada del último 10-K/10-Q
presentado). Así los desdoblamientos no confunden. Quiebra en el medio y sin precio final = pérdida total."""
import sys, bisect, collections, json
import numpy as np, pandas as pd

leer = lambda arg, **k: pd.concat([pd.read_csv(x, **k) for x in arg.split(',') if x])
ideas = leer(sys.argv[1], dtype={'mes_compra': str, 'id': str}).drop_duplicates(['mes_compra', 'id'])
pr = leer(sys.argv[2], dtype={'id': str, 'mes': str}).sort_values('fuente', ascending=False).drop_duplicates(['id', 'mes'])
P = {(i, m): p for i, m, p in zip(pr['id'], pr['mes'], pr['precio'])}
ac = leer(sys.argv[3], dtype={'id': str})
ac['pres'] = ac['presentado'].str[:4] + ac['presentado'].str[5:7]
S = collections.defaultdict(list)
for i, m, q in sorted(zip(ac['id'], ac['pres'], ac['acciones'])):
    S[i].append((m, q))
fil = pd.read_csv(sys.argv[4], usecols=['id', 'anio', 'estado_final', 'sector'], dtype={'id': str, 'sector': str})
sector = dict(zip(fil['id'], fil['sector']))
muere = {i: g['anio'].max() for i, g in fil[fil['estado_final'].isin(['quiebra', 'revocada'])].groupby('id')}

def suma(m, k):
    y, mm = int(m[:4]), int(m[4:6]) + k
    y += (mm - 1) // 12; mm = (mm - 1) % 12 + 1
    return f'{y:04d}{mm:02d}'
def acciones(i, m):          # último dato presentado ANTES de fin de ese mes
    s = S.get(i)
    if not s:
        return None
    k = bisect.bisect_right(s, (m, float('inf'))) - 1
    return s[k][1] if k >= 0 else None
def mcap(i, m):
    for d in (0, 1, -1):     # tolerancia de un mes en el precio
        p = P.get((i, suma(m, d)))
        if p is not None:
            q = acciones(i, m)
            return p * q if q else None
    return None

ids = sorted({i for i, _ in P})
res = {}
for m in sorted(ideas['mes_compra'].unique()):
    m1 = suma(m, 12)
    ret = {}
    for i in ids:
        a = mcap(i, m)
        if not a:
            continue
        b = mcap(i, m1)
        if b:
            r = b / a
            if 0 < r < 20:
                ret[i] = r
        elif i in muere and muere[i] < int(m1[:4]):
            ret[i] = 0.0
    if len(ret) < 300:
        continue
    med = float(np.median(list(ret.values())))
    elegidas = [i for i in ideas.loc[ideas['mes_compra'] == m, 'id'] if i in ret]
    if not elegidas:
        continue
    # CONTROL (no es el criterio): comparar contra empresas de su mismo tamaño, y de su mismo tamaño y sector.
    # Los fondos compran empresas grandes; si las grandes le ganan a las chicas, eso solo ya "gana".
    tam = {i: mcap(i, m) for i in ret}
    corte = np.quantile([v for v in tam.values() if v], [0.2, 0.4, 0.6, 0.8])
    q = {i: int(np.searchsorted(corte, v)) for i, v in tam.items() if v}
    grupos = collections.defaultdict(list); grupos2 = collections.defaultdict(list)
    for i, r in ret.items():
        if i in q:
            grupos[q[i]].append(r); grupos2[(q[i], sector.get(i))].append(r)
    med_q = {k: np.median(v) for k, v in grupos.items()}
    med_q2 = {k: np.median(v) for k, v in grupos2.items() if len(v) >= 15}
    g_tam = [ret[i] > med_q[q[i]] for i in elegidas if i in q]
    g_sec = [ret[i] > med_q2[(q[i], sector.get(i))] for i in elegidas if i in q and (q[i], sector.get(i)) in med_q2]
    res[m] = {'ideas': len(elegidas), 'universo': len(ret), 'ganan': int(sum(ret[i] > med for i in elegidas)),
              'exceso_mediano': float(np.median([ret[i] - med for i in elegidas])),
              'ganan_tam': int(sum(g_tam)), 'n_tam': len(g_tam), 'ganan_sec': int(sum(g_sec)), 'n_sec': len(g_sec),
              'quintil_medio': float(np.mean([q[i] for i in elegidas if i in q]))}
por_anio = collections.defaultdict(lambda: [0, 0, []])
for m, r in res.items():
    a = int(m[:4]); por_anio[a][0] += r['ganan']; por_anio[a][1] += r['ideas']; por_anio[a][2].append(r['exceso_mediano'])
tabla = {a: {'ideas': v[1], 'ganan_pct': round(100 * v[0] / v[1], 1), 'exceso_mediano': round(float(np.median(v[2])), 3)}
         for a, v in sorted(por_anio.items()) if v[1]}
ctrl = collections.defaultdict(lambda: [0, 0, 0, 0, []])
for m, r in res.items():
    c = ctrl[int(m[:4])]; c[0] += r['ganan_tam']; c[1] += r['n_tam']; c[2] += r['ganan_sec']; c[3] += r['n_sec']; c[4].append(r['quintil_medio'])
for a, v in tabla.items():
    c = ctrl[a]
    v['ganan_pct_mismo_tamano'] = round(100 * c[0] / c[1], 1) if c[1] else None
    v['ganan_pct_mismo_tamano_y_sector'] = round(100 * c[2] / c[3], 1) if c[3] else None
    v['quintil_tamano_medio'] = round(float(np.mean(c[4])), 2)
    print(f'AÑO {a}: {v["ideas"]} ideas, le ganan a la mediana {v["ganan_pct"]}% | mismo tamaño {v["ganan_pct_mismo_tamano"]}% '
          f'| mismo tamaño y sector {v["ganan_pct_mismo_tamano_y_sector"]}% | tamaño medio (0-4) {v["quintil_tamano_medio"]}', flush=True)
def periodo(a0, a1):
    g = sum(por_anio[a][0] for a in por_anio if a0 <= a <= a1); n = sum(por_anio[a][1] for a in por_anio if a0 <= a <= a1)
    return round(100 * g / n, 1) if n else None
p1, p2 = periodo(2013, 2018), periodo(2019, 2024)
arriba = sum(1 for a, v in tabla.items() if 2013 <= a <= 2024 and v['ganan_pct'] > 50)
de = sum(1 for a in tabla if 2013 <= a <= 2024)
pasa = bool(p1 and p2 and p1 >= 52 and p2 >= 52 and arriba >= 9)
print(f'CRITERIO: 2013-2018 {p1}% | 2019-2024 {p2}% | años arriba de 50%: {arriba} de {de} -> {"PASA" if pasa else "no pasa"}', flush=True)
json.dump({'por_mes': res, 'por_anio': tabla, 'p2013_2018': p1, 'p2019_2024': p2, 'anios_arriba': arriba, 'pasa': pasa},
          open('ideas_resultado.json', 'w'), indent=1)
