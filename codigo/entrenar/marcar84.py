"""#84 hacia adelante: empresas con pico de público en Wikipedia y venta neta de directivos en los últimos meses. Uso: python marcar84.py wiki_vistas_2026.csv DIRECTIVOS_CSVS -> marcadas84.csv"""
import sys, pandas as pd
W = pd.read_csv(sys.argv[1], dtype={'id': str, 'mes': str}); W['m'] = W['mes'].str[:4].astype(int) * 12 + W['mes'].str[4:6].astype(int) - 1
V = W.pivot_table(index='m', columns='id', values='vistas', aggfunc='sum').sort_index()
base = V.shift(1).rolling(12, min_periods=10).median(); pico = (V >= 2 * base) & (base >= 100)
D = pd.concat([pd.read_csv(x, dtype={'id': str, 'mes': str}) for x in sys.argv[2].split(',') if x]); D['m'] = D['mes'].str[:4].astype(int) * 12 + D['mes'].str[4:6].astype(int) - 1
print('directivos hasta', D['mes'].max(), '| vistas hasta', W['mes'].max(), flush=True)
S = D[D['tipo'] == 'S'].groupby(['id', 'm'])['valor'].sum().to_dict(); P = D[D['tipo'] == 'P'].groupby(['id', 'm'])['valor'].sum().to_dict()
desde = 2026 * 12 + 4                                  # mayo de 2026 en adelante
fil = []
for i in pico.columns:
    for m in pico.index[pico[i].values]:
        if m < desde: continue
        s = sum(S.get((i, k), 0) for k in (m, m + 1)); p = sum(P.get((i, k), 0) for k in (m, m + 1))
        fil.append((i, f'{m // 12}-{m % 12 + 1:02d}', int(s > p and s > 0), round(s), round(p)))
out = pd.DataFrame(fil, columns=['id', 'mes_pico', 'venta_directivos', 'ventas_usd', 'compras_usd']).sort_values(['venta_directivos', 'mes_pico'], ascending=[False, True])
out.to_csv('marcadas84.csv', index=False); print('picos', len(out), '| con venta', int(out['venta_directivos'].sum()), flush=True)
