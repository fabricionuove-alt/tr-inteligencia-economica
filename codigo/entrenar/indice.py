"""Señales #57-#58 (notas/11): el portero del índice. Altas y bajas por valor del S&P 500, 2011-2024.
Uso: python indice.py filas.csv indice_cambios.csv simbolos.csv PRECIOS_CSVS [salida.json]
Retorno a 12 meses desde el cierre del mes siguiente a la fecha efectiva; control = mismo decil de tamaño, mismos meses."""
import sys, re, json, time
import numpy as np, pandas as pd
t0 = time.time()
salida = sys.argv[5] if len(sys.argv) > 5 else 'indice.json'
df = pd.read_csv(sys.argv[1], usecols=lambda c: c in ('id', 'anio', 'log_activos', '_presentado'), dtype={'id': str}, low_memory=False)
ev = pd.read_csv(sys.argv[2], dtype=str).fillna('')
sim = pd.read_csv(sys.argv[3], dtype={'simbolo': str, 'id': str})
S = {(s, int(a)): i for s, a, i in zip(sim['simbolo'], sim['anio'], sim['id'])}
pr = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[4].split(',') if x])
if 'fuente' in pr.columns:
    pr = pr.sort_values('fuente', ascending=False)
pr = pr.drop_duplicates(['id', 'mes'])
pr['m'] = pr['mes'].str[:4].astype(int) * 12 + pr['mes'].str[4:6].astype(int) - 1
P = pr[pr['precio'] > 0].pivot_table(index='m', columns='id', values='precio')

pres = df['_presentado'].astype(str); ok = pres.str.len() >= 7
df = df[ok].copy(); df['mp'] = pres[ok].str[:4].astype(int) * 12 + pres[ok].str[5:7].astype(int) - 1
df['la'] = pd.to_numeric(df['log_activos'], errors='coerce'); df = df.dropna(subset=['la']).sort_values('mp')

def a_id(sym, y):
    sym = sym.replace('.', '-').strip()
    for s_ in (sym, sym.replace('-', '.'), sym.replace('-', '')):
        for yy in (y, y - 1, y + 1, y - 2):
            if (s_, yy) in S:
                return S[(s_, yy)]
    return None
filas, sin = [], {'alta': 0, 'baja': 0}
for f, alta, baja, mot in zip(ev['fecha'], ev['alta'], ev['baja'], ev['motivo']):
    y, mo = int(f[:4]), int(f[5:7])
    if not 2011 <= y <= 2024:
        continue
    m0 = y * 12 + mo - 1 + 1
    casos = []
    if alta:
        casos.append(('alta', alta))
    if baja and re.search(r'market cap', mot, re.I) and not re.search(r'acqui|merg|spin|split|bought|purchas', mot, re.I):
        casos.append(('baja', baja))
    for tipo, sym in casos:
        i = a_id(sym, y)
        if i is None:
            sin[tipo] += 1; continue
        filas.append((tipo, y, m0, i, sym))
print(f'INDICE eventos unidos: altas {sum(1 for x in filas if x[0] == "alta")} (sin unir {sin["alta"]}), '
      f'bajas por valor {sum(1 for x in filas if x[0] == "baja")} (sin unir {sin["baja"]}) ({time.time() - t0:.0f}s)', flush=True)

cache = {}
def control(m0):
    if m0 in cache:
        return cache[m0]
    if m0 not in P.index or m0 + 12 not in P.index:
        cache[m0] = None; return None
    r = (P.loc[m0 + 12] / P.loc[m0]).dropna()
    t = df[df['mp'] < m0].drop_duplicates('id', keep='last').set_index('id')['la']
    t = t.reindex(r.index).dropna()
    r = r.reindex(t.index)
    dec = np.minimum((t.rank(pct=True, method='first') * 10).astype(int), 9)
    cache[m0] = (r, dec); return cache[m0]
res = {'eventos': [], 'resumen': {}}
for tipo, y, m0, i, sym in filas:
    c = control(m0)
    if c is None or i not in c[0].index:
        continue
    r, dec = c; d = dec[i]
    otros = r[(dec == d) & (r.index != i)]
    if len(otros) < 20:
        continue
    res['eventos'].append({'tipo': tipo, 'anio': y, 'ret': float(r[i]), 'exceso': float(np.log(r[i]) - np.log(otros).mean()),
                           'x2': int(r[i] >= 2), 'des': int(r[i] <= 0.5), 'x2_ctrl': float((otros >= 2).mean()), 'des_ctrl': float((otros <= 0.5).mean())})
E = pd.DataFrame(res['eventos'])
g = np.random.default_rng(0)
for tipo in ('alta', 'baja'):
    e = E[E['tipo'] == tipo] if len(E) else E
    if not len(e):
        print(f'INDICE {tipo}: sin eventos'); continue
    boot = [g.choice(e['exceso'].values, len(e)).mean() for _ in range(2000)]
    lo, hi = np.percentile(boot, [2.5, 97.5])
    por = e.groupby('anio')['exceso'].mean()
    pos = int((por > 0).sum())
    rs = {'n': len(e), 'exceso_medio': round(float(e['exceso'].mean()), 4), 'ic95': [round(float(lo), 4), round(float(hi), 4)],
          'anios_positivos': f'{pos} de {len(por)}', 'por_anio': {int(k): round(float(v), 4) for k, v in por.items()},
          'x2': round(100 * float(e['x2'].mean()), 2), 'x2_ctrl': round(100 * float(e['x2_ctrl'].mean()), 2),
          'des': round(100 * float(e['des'].mean()), 2), 'des_ctrl': round(100 * float(e['des_ctrl'].mean()), 2),
          'pasa': bool(lo > 0 and pos >= 9)}
    res['resumen'][tipo] = rs
    print(f'INDICE {tipo}: {rs["n"]} eventos | exceso medio {rs["exceso_medio"]} (IC95 {rs["ic95"]}) | años positivos {rs["anios_positivos"]} | '
          f'x2 {rs["x2"]}% vs {rs["x2_ctrl"]}% | desastre {rs["des"]}% vs {rs["des_ctrl"]}% | por año {rs["por_anio"]} -> {"PASA" if rs["pasa"] else "no pasa"}', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
