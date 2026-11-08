"""Suma a filas.csv los rasgos de precio y dueños, y la etiqueta precio_duplica_6.
Uso: python precio.py filas.csv precios.csv directivos.csv
Fechas (para no usar nada que no se sabía):
- Precio de compra = el del mes SIGUIENTE a la presentación del balance (o hasta 2 meses después).
- Compras de directivos = los 12 meses ANTES de la presentación.
- Precio de venta = 72 meses después del de compra (±2).
precio_duplica_6 = (valor de mercado final + dividendos + recompras - emisiones, de los 6 años) / valor de mercado
inicial >= 2. Es lo que gana quien compra la empresa entera: los desdoblamientos de acciones no la afectan.
Quiebra en el medio y sin precio final = 0. Comprada en el medio = sin etiqueta (sesgo: suelen comprarse con prima)."""
import sys, collections
import numpy as np, pandas as pd

df = pd.read_csv(sys.argv[1], low_memory=False)
pr = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[2].split(',')])
pr = pr.sort_values('fuente', ascending=False)          # 'ftd' gana sobre 'directivos'
P = {(i, m): p for i, m, p in zip(pr['id'], pr['mes'], pr['precio'])}
di = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str, 'dueno': str}) for x in sys.argv[3].split(',')])
D = collections.defaultdict(list)
for i, m, du, ti, va in zip(di['id'], di['mes'], di['dueno'], di['tipo'], di['valor']):
    D[i].append((m, du, ti, va))
# Tenencias de los dueños de adentro (4º argumento, opcional): {id: [(mes, dueño, acciones)]}
T = collections.defaultdict(list)
if len(sys.argv) > 4 and sys.argv[4]:
    te = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str, 'dueno': str}) for x in sys.argv[4].split(',')])
    for i, m, du, q in zip(te['id'], te['mes'], te['dueno'], te['acciones']):
        T[i].append((m, du, q))

def suma_mes(m, k):
    y, mm = int(m[:4]), int(m[4:6]) + k
    y += (mm - 1) // 12; mm = (mm - 1) % 12 + 1
    return f'{y:04d}{mm:02d}'
def precio(i, m0, desfases):
    for k in desfases:
        p = P.get((i, suma_mes(m0, k)))
        if p is not None:
            return p
    return None

g = lambda r, k: (r[k] if k in r and pd.notna(r[k]) else None)
por_id = {i: grp.set_index('anio') for i, grp in df.groupby('id')}
nuevas = collections.defaultdict(list)
for idx, r in df.iterrows():
    out = dict.fromkeys(['_ret1', 'rinde_fcf', 'rinde_ganancia', 'libro_precio', 'ebit_ev', 'directivos_compran',
                         'compra_neta_mcap', 'precio_duplica_6', 'dueno_mayor_pct', 'duenos_grandes',
                         'ret_previo_12', 'volatilidad_12', 'precio_nivel', '_ret6', '_ret4'])
    pres = g(r, '_presentado'); acc = g(r, '_acciones')
    if pres and acc and acc > 0:
        mp = pres[:4] + pres[5:7]
        m0 = suma_mes(mp, 1)
        p0 = precio(r['id'], m0, [0, 1, 2])
        # directivos: 12 meses antes de presentar
        desde = suma_mes(mp, -12)
        tr = [x for x in D.get(r['id'], []) if desde <= x[0] < mp]
        out['directivos_compran'] = float(len({x[1] for x in tr if x[2] == 'P'}))
        # Señales de mercado de Campbell-Hilscher-Szilagyi (2008), sólo con precios ANTERIORES a la compra (#37)
        serie = [P.get((r['id'], suma_mes(mp, -k))) for k in range(12, -1, -1)]
        ok = [x for x in serie if x]
        if len(ok) >= 6:
            out['ret_previo_12'] = ok[-1] / ok[0] - 1
            lr = np.diff(np.log(ok))
            out['volatilidad_12'] = float(np.std(lr))
            out['precio_nivel'] = float(np.log(ok[-1]))
        # piel en el juego: última tenencia de cada dueño de adentro en los 24 meses ANTES de presentar
        if T:
            desde24 = suma_mes(mp, -24); ult = {}
            for m_, du, q in T.get(r['id'], []):
                if desde24 <= m_ < mp and (du not in ult or m_ >= ult[du][0]):
                    ult[du] = (m_, q)
            pcts = [min(1.0, q / acc) for _, q in ult.values()]
            out['dueno_mayor_pct'] = max(pcts) if pcts else 0.0
            out['duenos_grandes'] = float(sum(1 for x in pcts if x > 0.05))
        if p0:
            mcap = p0 * acc
            fcf = (g(r, '_fco') or 0) - (g(r, '_capex') or 0) if g(r, '_fco') is not None else None
            out['rinde_fcf'] = fcf / mcap if fcf is not None else None
            out['rinde_ganancia'] = g(r, '_res_neto') / mcap if g(r, '_res_neto') is not None else None
            out['libro_precio'] = g(r, '_patrimonio') / mcap if g(r, '_patrimonio') is not None else None
            ev = mcap + (g(r, '_deuda') or 0) - (g(r, '_caja') or 0)
            out['ebit_ev'] = g(r, '_res_op') / ev if (g(r, '_res_op') is not None and ev > 0) else None
            neto = sum(x[3] for x in tr if x[2] == 'P') - sum(x[3] for x in tr if x[2] == 'S')
            out['compra_neta_mcap'] = neto / mcap
            # etiqueta a 1 año (el paper encontró el efecto en meses): retorno de 12 meses del dueño de toda la empresa
            t1 = r['anio'] + 1
            hist1 = por_id[r['id']]
            p12 = precio(r['id'], m0, [12, 13, 11])
            if p12 is not None and t1 in hist1.index and pd.notna(hist1.loc[t1, '_acciones']):
                x = hist1.loc[t1]
                fl = sum((x[k] if pd.notna(x[k]) else 0) for k in ('_dividendos', '_recompras')) - (x['_emisiones'] if pd.notna(x['_emisiones']) else 0)
                ret1 = (p12 * x['_acciones'] + fl) / mcap
                if 0 < ret1 < 20:
                    out['_ret1'] = ret1
            # etiqueta: 6 años después
            t = r['anio']; hist = por_id[r['id']]
            p6 = precio(r['id'], m0, [72, 73, 74, 71, 70])
            if p6 is not None and (t + 6) in hist.index and pd.notna(hist.loc[t + 6, '_acciones']):
                flujos = 0.0
                for a in range(t + 1, t + 7):
                    if a in hist.index:
                        x = hist.loc[a]
                        flujos += sum((x[k] if pd.notna(x[k]) else 0) for k in ('_dividendos', '_recompras'))
                        flujos -= (x['_emisiones'] if pd.notna(x['_emisiones']) else 0)
                ret = (p6 * hist.loc[t + 6, '_acciones'] + flujos) / mcap
                if 0 < ret < 50:            # más de x50 suele ser un error de unidades en las acciones
                    out['precio_duplica_6'] = 1.0 if ret >= 2 else 0.0
                    out['_ret6'] = ret      # el múltiplo en sí (oculto): para medir colas (#38)
            elif r.get('estado_final') in ('quiebra', 'revocada') and hist.index.max() < t + 6:
                out['precio_duplica_6'] = 0.0
                out['_ret6'] = 0.0
            # lo mismo a 4 años (oculto, #46): para probar en camadas que todavía no cumplieron 6
            p4 = precio(r['id'], m0, [48, 49, 50, 47, 46])
            if p4 is not None and (t + 4) in hist.index and pd.notna(hist.loc[t + 4, '_acciones']):
                fl4 = 0.0
                for a in range(t + 1, t + 5):
                    if a in hist.index:
                        x = hist.loc[a]
                        fl4 += sum((x[k] if pd.notna(x[k]) else 0) for k in ('_dividendos', '_recompras'))
                        fl4 -= (x['_emisiones'] if pd.notna(x['_emisiones']) else 0)
                ret4 = (p4 * hist.loc[t + 4, '_acciones'] + fl4) / mcap
                if 0 < ret4 < 50:
                    out['_ret4'] = ret4
            elif r.get('estado_final') in ('quiebra', 'revocada') and hist.index.max() < t + 4:
                out['_ret4'] = 0.0
    for k, v in out.items():
        nuevas[k].append(v)
for k, v in nuevas.items():
    df[k] = v
# precio_gana_1: el retorno de 12 meses le gana a la MEDIANA de las empresas compradas ese mismo año
# (así no importa si el mercado entero subió o bajó: mide elegir bien, no la época)
med = df.groupby('anio')['_ret1'].transform('median')
df['precio_gana_1'] = (df['_ret1'] > med).astype(float).where(df['_ret1'].notna())
df.to_csv(sys.argv[1], index=False)
c = {k: int(pd.Series(v).notna().sum()) for k, v in nuevas.items()}
if c['rinde_fcf'] == 0:
    print('FALLA: no entró ningún precio (¿faltan _presentado/_acciones en las filas?)', flush=True)
    sys.exit(2)
print('PRECIO filas con dato:', c, '| tasa de duplicar:', round(float(pd.Series(nuevas['precio_duplica_6']).mean()), 3), flush=True)
