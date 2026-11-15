"""#121: VIX medio ene-mar del año de presentación vs diferencia cambiadas - quietas (#117). Reglas en notas/11 (#121)."""
import numpy as np, pandas as pd
from scipy.stats import spearmanr
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
v = pd.read_csv(f'{B}/fuentes/vix/VIX_History.csv'); v['f'] = pd.to_datetime(v['DATE'], format='%m/%d/%Y')
v = v[v.f.dt.month <= 3]; vix = v.groupby(v.f.dt.year)['CLOSE'].mean()
t = pd.read_csv(f'{B}/entrenar/sal-cab102/ciclo117_cohortes.csv'); t['vix'] = t['ap'].map(vix)
print(t[['ap', 'n', 'dif', 'mercado4', 'vix']].round(2).to_string(index=False), flush=True)
def perm(a, b):
    o = spearmanr(a, b)[0]; P = np.array([spearmanr(a, rng.permutation(b))[0] for _ in range(10000)])
    return o, ((P >= o).sum() + 1) / 10001
r, p = perm(t['vix'].values, t['dif'].values); r2, p2 = perm(t['vix'].values, t['mercado4'].values)
print(f'VX121 VIX vs diferencia rho {r:+.2f} p {p:.4f}'); print(f'VX121 VIX vs mercado 4 anios rho {r2:+.2f} p {p2:.4f}')
print('CRITERIO121', 'pasa' if r > 0 and p < .05 else 'no pasa')
