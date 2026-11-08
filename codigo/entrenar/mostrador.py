"""Señales #55-#56 (notas/11): los dos lados del mostrador. Puts y calls de los 13F, sumados a Kelly (#50).
Uso: python mostrador.py filas.csv personas.csv FALLAS_CSVS OP13F_CSVS [salida.json]
La prueba (lado, placebo dentro del tamaño, desastres) es la misma de red.py, tal cual."""
import sys, os, json, time
import numpy as np, pandas as pd
_aqui = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_aqui, 'kelly.py'), encoding='utf-8').read().split("res = {'camadas': {}}")[0])
from sklearn.metrics import roc_auc_score
salida = sys.argv[5] if len(sys.argv) > 5 else 'mostrador.json'
t1 = time.time()

op = pd.concat([pd.read_csv(x, dtype={'id': str, 'fondo': str, 'periodo': str}) for x in sys.argv[4].split(',') if x])
op = op.drop_duplicates(['periodo', 'fondo', 'id', 'tipo'])
op['m'] = op['periodo'].str[:4].astype(int) * 12 + op['periodo'].str[4:6].astype(int) - 1
w = op.pivot_table(index=['id', 'm', 'fondo'], columns='tipo', values='acciones', aggfunc='sum', fill_value=0).reset_index()
for c in ['SH', 'PUT', 'CALL']:
    if c not in w:
        w[c] = 0.0
w = w[(w['PUT'] > 0) | (w['CALL'] > 0)]                         # fondos con alguna opción sobre ESTA empresa
w['put_desc'] = np.where(w['SH'] == 0, w['PUT'], 0.0); w['call_desc'] = np.where(w['SH'] == 0, w['CALL'], 0.0)
w['cubierto'] = ((w['SH'] > 0) & (w['PUT'] > 0)).astype(float); w['con_put'] = (w['PUT'] > 0).astype(float)
e = w.groupby(['id', 'm']).agg(PUT=('PUT', 'sum'), CALL=('CALL', 'sum'), SH=('SH', 'sum'), n=('fondo', 'nunique'),
                                put_desc=('put_desc', 'sum'), call_desc=('call_desc', 'sum'), cub=('cubierto', 'sum'), cp=('con_put', 'sum')).reset_index()
op_t = e['PUT'] + e['CALL']
e['pc'] = e['PUT'] / op_t
e['neto'] = (e['SH'] + e['CALL'] - e['PUT']) / (e['SH'] + op_t)
e = e.sort_values(['id', 'm'])
ant = e.groupby('id')['pc'].shift(1); m_ant = e.groupby('id')['m'].shift(1)
e['d_pc'] = np.where(e['m'] - m_ant == 3, e['pc'] - ant, np.nan)
e['cubiertos'] = e['cub'] / e['cp'].replace(0, np.nan)
e['put_descubierto'] = e['put_desc'] / op_t; e['call_descubierto'] = e['call_desc'] / op_t
e['m'] = e['m'] + 2                                            # el 13F vence 45 días después del cierre del trimestre
print(f'OP13F: {len(op)} filas, {e["id"].nunique()} empresas, trimestres {e["m"].min() // 12}-{e["m"].max() // 12} ({time.time() - t1:.0f}s)', flush=True)

q = pd.DataFrame({'i': df.index, 'id': df['id'], 'm': mp + 1}).dropna(subset=['m'])
q['m'] = q['m'].astype(int); q = q.sort_values('m')
COLB = ['pc', 'neto', 'd_pc', 'PUT', 'n', 'cubiertos', 'put_descubierto', 'call_descubierto']
j = pd.merge_asof(q, e[['id', 'm'] + COLB].sort_values('m'), on='m', by='id', direction='backward', tolerance=6)
X = pd.DataFrame(np.nan, index=df.index, columns=COLB)
X.loc[j['i'].values] = j[COLB].values
X['PUT'] = X['PUT'] / num_('_acciones').where(num_('_acciones') > 0)   # puts sobre acciones en circulación
B = {'neta': X[['pc', 'neto', 'd_pc', 'PUT', 'n']].rename(columns={'PUT': 'put_sobre_acc'}),
     'cobertura': X[['cubiertos', 'put_descubierto', 'call_descubierto']]}
BL = {}
for k, Xk in B.items():
    BL[k] = []
    for c in Xk.columns:
        R[f'{k}_{c}'] = Xk[c].astype(float).replace([np.inf, -np.inf], np.nan).groupby(df['anio']).rank(pct=True); BL[k].append(f'{k}_{c}')
    print(f'BLOQUE {k}: ' + ', '.join(f'{c} {int(R[c].notna().sum())}' for c in BL[k]), flush=True)

_red = open(os.path.join(_aqui, 'red.py'), encoding='utf-8').read()
exec('def modelo(' + _red.split('def modelo(', 1)[1])
