"""Señal #41 (notas/11): confirmar la insistencia de #40 en camadas que nadie miró (2013-2016).
Uso: python insistencia.py filas.csv [desde] [hasta] [salida.json]
Misma receta que #40 (analizar.py) pero usa también los años 2009-2011, sólo para entrenar lo seguro
y para armar las trayectorias. Repite 2017-2019 como control."""
import sys, os, json, time
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

t0 = time.time()
df = pd.read_csv(sys.argv[1], low_memory=False)
D0 = int(sys.argv[2]) if len(sys.argv) > 2 else 2013
D1 = int(sys.argv[3]) if len(sys.argv) > 3 else 2019
salida = sys.argv[4] if len(sys.argv) > 4 else 'insistencia.json'
mc = int(os.environ.get('MIN_CAMADA', 300)); mA = int(os.environ.get('MIN_ENTRENA', 500))
df = df[df['anio'] >= 2009].drop(columns=[c for c in ['anios_hist'] if c in df.columns]).reset_index(drop=True)

# mismos rasgos que analizar.py (nunca etiquetas, clásicos ni montos ocultos)
ETIQ = ['sobrevive_10', 'sobrevive_10_amplio', 'duplica_6', 'gana_mas_1', 'precio_duplica_6', 'precio_gana_1']
NO_RASGO = {'id', 'anio', 'estado_final', 'altman_z2', 'ohlson_o', 'piotroski_f'} | set(ETIQ)
BINARIOS = {'patrimonio_neg', 'sin_deuda', 'perdida', 'financiera'}
rasgos = [c for c in df.columns if c not in NO_RASGO and not c.startswith('_') and df[c].notna().sum() > 100]
num = [c for c in rasgos if c not in BINARIOS and c != 'sector']
rng0 = np.random.default_rng(42)
R = pd.DataFrame(index=df.index); Rn = pd.DataFrame(index=df.index)
for c in num:
    v = pd.to_numeric(df[c], errors='coerce')
    v = v + rng0.random(len(df)) * 1e-9 * (v.abs().max() if v.notna().any() else 1)
    p = v.groupby(df['anio']).rank(pct=True, method='first')
    R[c] = p.where(p.notna(), pd.Series(rng0.random(len(df)), index=df.index)); Rn[c] = p
for c in sorted(BINARIOS & set(df.columns)):   # ordenado: el orden de un set cambia en cada corrida
    R[c] = df[c].fillna(pd.Series(rng0.integers(0, 2, len(df)), index=df.index)).astype(float)
R['sector'] = df['sector'].astype(float)
X_cols = list(R.columns)

ult = df.groupby('id')['anio'].transform('max')
r1all = df['_ret1'].copy()
r1all[r1all.isna() & df['estado_final'].isin(['quiebra', 'revocada']) & (ult < df['anio'] + 1)] = 0.0
r6all = df['_ret6'] if '_ret6' in df.columns else pd.Series(np.nan, index=df.index)

MET = [m for m in ['margen_op', 'margen_bruto', 'crec_ventas_1', 'roa', 'fco_activos'] if m in Rn.columns]
clave = pd.Series(df.index.values, index=pd.MultiIndex.from_arrays([df['id'], df['anio']]))
clave = clave[~clave.index.duplicated()]
def fila_de(k):
    v = clave.reindex(pd.MultiIndex.from_arrays([df['id'], df['anio'] - k])).values
    return np.where(np.isnan(v.astype(float)), -1, v).astype(int)
p1, p2 = fila_de(1), fila_de(2)
tiene = p1 >= 0
Xprev = np.full((len(df), len(X_cols)), np.nan)
Xprev[tiene] = R[X_cols].values[p1[tiene]]
anio = df['anio'].values
desv = np.full((len(df), len(MET)), np.nan)
for s in range(max(2011, D0 - 2), D1 + 1):
    for j, m in enumerate(MET):
        y = Rn[m].values
        A = tiene & (anio >= s - 6) & (anio <= s - 1) & ~np.isnan(y)
        B = tiene & (anio == s) & ~np.isnan(y)
        if A.sum() < mA or B.sum() == 0:
            print(f'INSIST41 sin modelo para {s} {m} (entrena {int(A.sum())})', flush=True)
            continue
        mod = HistGradientBoostingRegressor(max_iter=100, learning_rate=0.1, max_leaf_nodes=15, random_state=0).fit(Xprev[A], y[A])
        desv[B, j] = y[B] - mod.predict(Xprev[B])
print(f'INSIST41 modelos listos en {time.time() - t0:.0f}s', flush=True)

def fraccion(D):
    st = np.concatenate([D, np.where(p1[:, None] >= 0, D[np.maximum(p1, 0)], np.nan),
                         np.where(p2[:, None] >= 0, D[np.maximum(p2, 0)], np.nan)], axis=1)
    disp = (~np.isnan(st)).sum(1); posi = (st > 0).sum(1)
    return np.where(disp >= 9, posi / np.maximum(disp, 1), np.nan), np.nanmean(np.where(disp[:, None] >= 9, st, np.nan), axis=1)
frac, media = fraccion(desv)
rng40 = np.random.default_rng(40)
mez = desv.copy()
for s in np.unique(anio):
    ii = np.where(anio == s)[0]
    for j in range(len(MET)):
        mez[ii, j] = desv[rng40.permutation(ii), j]
frac_mez, _ = fraccion(mez)
nivel = np.nanmean(Rn[MET].values, axis=1)

res = {'medidas': MET, 'camadas': {}}
for t in range(D0, D1 + 1):
    idx = np.where((anio == t) & ~np.isnan(frac))[0]
    if len(idx) < mc:
        print(f'INSIST41 {t}: pocas empresas con trayectoria ({len(idx)})', flush=True)
        continue
    rk = pd.Series(frac[idx] + 1e-3 * np.nan_to_num(media[idx])).rank(method='first', pct=True).values
    ins, rev = rk > 0.9, rk <= 0.1
    foto = pd.Series(nivel[idx]).rank(method='first', pct=True).values > 0.9
    r1 = r1all.values[idx]; r6 = r6all.values[idx]
    def met(mask):
        a = r1[mask & ~np.isnan(r1)]; b = r6[mask & ~np.isnan(r6)]
        o = {'n': int(mask.sum()), 'tamano_medio': round(float(np.nanmean(Rn['log_activos'].values[idx][mask])), 3)}
        if len(a) >= 30:
            o.update({'prom_12m': round(float(a.mean()), 3), 'mediana_12m': round(float(np.median(a)), 3),
                      'pct_x2_12m': round(100 * float((a >= 2).mean()), 2), 'pct_desastre_12m': round(100 * float((a <= 0.5).mean()), 2)})
        if len(b) >= 30 and t <= 2019:
            o.update({'n6': int(len(b)), 'pct_x3_6a': round(100 * float((b >= 3).mean()), 2),
                      'pct_desastre_6a': round(100 * float((b <= 0.25).mean()), 2), 'prom_6a': round(float(b.mean()), 3)})
        return o
    fila = {'universo': met(np.ones(len(idx), bool)), 'insistentes': met(ins), 'al_reves': met(rev), 'foto_calidad': met(foto)}
    ok_mez = (anio == t) & ~np.isnan(frac_mez)
    fila['azar'] = {'real_pct_80': round(100 * float((frac[idx] >= 0.8).mean()), 2),
                    'mezclado_pct_80': round(100 * float((frac_mez[ok_mez] >= 0.8).mean()), 2) if ok_mez.sum() else None}
    ok6 = ~np.isnan(r6)
    if t <= 2019 and ok6.sum() >= 300:
        g3 = ok6 & (r6 >= 3)
        fila['estela'] = {'x3_insistentes_pct': round(100 * float(ins[g3].mean()), 2), 'peso_pct': round(100 * float(ins[ok6].mean()), 2)}
    res['camadas'][t] = fila
    print(f'INSIST41 {t} azar {fila["azar"]} ' + (f'estela {fila["estela"]} ' if 'estela' in fila else '') + '| ' + ' | '.join(
        f"{g}: n {x['n']} tam {x['tamano_medio']} prom {x.get('prom_12m')} x2 {x.get('pct_x2_12m')}% des {x.get('pct_desastre_12m')}%"
        + (f" ·6a x3 {x.get('pct_x3_6a')}% des {x.get('pct_desastre_6a')}%" if 'n6' in x else '')
        for g, x in fila.items() if 'n' in x), flush=True)

# criterio (sólo camadas 2013-2016)
C = {t: f for t, f in res['camadas'].items() if 2013 <= t <= 2016}
c1 = sum(1 for f in C.values() if f['azar']['mezclado_pct_80'] and f['azar']['real_pct_80'] >= 1.3 * f['azar']['mezclado_pct_80'])
c2 = c3 = 0
for f in C.values():
    u, i, fo = f['universo'], f['insistentes'], f['foto_calidad']
    if 'n6' in u and 'n6' in i:
        c2 += (i['pct_x3_6a'] > u['pct_x3_6a']) and (i['pct_desastre_6a'] < u['pct_desastre_6a'])
        if 'n6' in fo:
            c3 += i['pct_x3_6a'] > fo['pct_x3_6a']
res['criterio'] = {'camadas': len(C), 'existe': f'{c1} de {len(C)}', 'seis_anios_vs_universo': f'{c2} de {len(C)}',
                   'seis_anios_vs_foto': f'{c3} de {len(C)}', 'confirma': bool(len(C) == 4 and c1 >= 3 and c2 >= 3 and c3 >= 3)}
print(f'CRITERIO insistencia 2013-2016: {res["criterio"]} -> {"CONFIRMA" if res["criterio"]["confirma"] else "no confirma"} ({time.time() - t0:.0f}s)', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
# trayectorias para #43: los 15 desvíos (medida × año t, t-1, t-2) + fracción positiva + desvío medio
st = np.concatenate([desv, np.where(p1[:, None] >= 0, desv[np.maximum(p1, 0)], np.nan),
                     np.where(p2[:, None] >= 0, desv[np.maximum(p2, 0)], np.nan)], axis=1)
tray = pd.DataFrame(st, columns=[f'tr_{m}_{k}' for k in ('t', 't1', 't2') for m in MET])
tray.insert(0, 'anio', df['anio'].values); tray.insert(0, 'id', df['id'].values)
tray['tr_frac'] = frac; tray['tr_media'] = media
tray.to_csv('trayectorias.csv', index=False)
print('INSIST41 trayectorias.csv', len(tray), flush=True)
