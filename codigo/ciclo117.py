"""#117: ¿la señal de riesgo (cambiadas − quietas) da vuelta con el ciclo? Reglas en notas/11 (#117)."""
import json, numpy as np, pandas as pd
from scipy.stats import spearmanr
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
et = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['ap'] = et['anio_presentado'].astype(int)
for c in ('_ret1', '_ret4'): et[c] = pd.to_numeric(et[c], errors='coerce')
mer4 = et.groupby('ap')['_ret4'].median(); mer1 = et.groupby('ap')['_ret1'].median()
a = pd.read_csv(f'{B}/entrenar/sal-cab102/lazy112_filas.csv', dtype={'id': str})[['id', 'ap', 'sim']]
b = pd.DataFrame([{'id': o['id'], 'ap': y, 'sim': o[f's{y}']} for o in map(json.loads, open(f'{B}/entrenar/sal-cab102/sim114.jsonl')) for y in (2021, 2022) if f's{y}' in o])
s = pd.concat([a, b]).dropna()
e = et.drop_duplicates(['id', 'ap'])[['id', 'ap', 'sic', 'tam', '_ret4']]
x = s.merge(e, on=['id', 'ap']).dropna(subset=['_ret4', 'sic', 'tam']).copy()
x['sic3'] = x['sic'].str[:3]; x['dec'] = np.minimum((x['tam'] * 10).astype(int), 9); g = ['ap', 'sic3', 'dec']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy()
x['lr'] = np.log(np.maximum(x['_ret4'], .01)); x['ex'] = x['lr'] - x.groupby(g)['lr'].transform('median')
x['q'] = x.groupby('ap')['sim'].transform(lambda v: pd.qcut(v.rank(method='first'), 5, labels=False))
filas = []
for y, z in x.groupby('ap'):
    d = z.loc[z.q == 0, 'ex'].mean() - z.loc[z.q == 4, 'ex'].mean()
    filas.append({'ap': y, 'n': len(z), 'dif': d * 100, 'mercado4': mer4[y], 'mercado_antes': mer1.get(y - 1, np.nan)})
t = pd.DataFrame(filas); print(t.round(3).to_string(index=False), flush=True)
def perm(u, v, colas):
    obs = spearmanr(u, v)[0]; P = np.array([spearmanr(u, rng.permutation(v))[0] for _ in range(10000)])
    p = ((P >= obs).sum() + 1) / 10001 if colas == 1 else ((np.abs(P) >= abs(obs)).sum() + 1) / 10001
    return obs, p
rA, pA = perm(t['dif'].values, t['mercado4'].values, 1); rB, pB = perm(t['dif'].values, t['mercado_antes'].values, 2)
print(f'CI117 A: diferencia vs mercado a 4 años  rho {rA:+.2f} p {pA:.4f}', flush=True)
print(f'CI117 B: diferencia vs mercado año antes rho {rB:+.2f} p {pB:.4f}', flush=True)
va = 'pasa' if rA > 0 and pA < .05 else 'no pasa'; vb = 'pasa' if pB < .05 else 'no pasa'
print(f'CRITERIO117 A {va} | B {vb}', flush=True)
t.to_csv(f'{B}/entrenar/sal-cab102/ciclo117_cohortes.csv', index=False)
