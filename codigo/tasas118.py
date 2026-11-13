"""#118: pendiente 10a−2a (ene-mar del año de presentación) contra la diferencia de #117. Reglas en notas/11 (#118)."""
import numpy as np, pandas as pd
from scipy.stats import spearmanr
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
pend = {}
for y in range(2010, 2023):
    d = pd.read_csv(f'{B}/fuentes/tesoro/t{y}.csv'); d['f'] = pd.to_datetime(d['Date'])
    d = d[d['f'].dt.month <= 3]; pend[y] = (d['10 Yr'] - d['2 Yr']).mean()
t = pd.read_csv(f'{B}/entrenar/sal-cab102/ciclo117_cohortes.csv'); t['pendiente'] = t['ap'].map(pend)
print(t[['ap', 'dif', 'mercado4', 'pendiente']].round(3).to_string(index=False))
def perm(u, v):
    obs = spearmanr(u, v)[0]; P = np.array([spearmanr(u, rng.permutation(v))[0] for _ in range(10000)])
    return obs, ((np.abs(P) >= abs(obs)).sum() + 1) / 10001
r1, p1 = perm(t['pendiente'].values, t['dif'].values); r2, p2 = perm(t['pendiente'].values, t['mercado4'].values)
print(f'TA118 pendiente vs diferencia rho {r1:+.2f} p {p1:.4f}'); print(f'TA118 pendiente vs mercado 4 años rho {r2:+.2f} p {p2:.4f}')
print(f'CRITERIO118 {"pasa" if p1 < .05 else "no pasa"}')
