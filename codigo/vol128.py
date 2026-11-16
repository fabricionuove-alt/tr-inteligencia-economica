"""#128: caída desde el máximo vs log(riesgosas/quietas) a 4 años, quintiles de volatilidad de French con peso igual, 1964-1996."""
import io, numpy as np, pandas as pd
from scipy.stats import spearmanr
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
sp = pd.read_csv(f'{B}/fuentes/sp500_shiller.csv'); sp['f'] = sp['Date'].str[:4].astype(int) * 100 + sp['Date'].str[5:7].astype(int); sp = sp.set_index('f')['SP500']
def caida(y):
    k = list(sp.index).index(y * 100 + 3); return sp.iloc[k] / sp.iloc[k - 60:k + 1].max() - 1
L = open(f'{B}/fuentes/french/Portfolios_Formed_on_VAR.csv').read().splitlines()
i = next(k for k, l in enumerate(L) if 'Equal Weighted Returns -- Monthly' in l); j = next(k for k in range(i + 2, len(L)) if not L[k].strip())
d = pd.read_csv(io.StringIO('\n'.join(L[i + 1:j]))); d.columns = ['f'] + [c.strip() for c in d.columns[1:]]; d['f'] = d['f'].astype(int)
lo, hi = 'Lo 20', 'Hi 20'
def dif(y):
    z = d[(d.f >= y * 100 + 4) & (d.f <= (y + 4) * 100 + 3)]; assert len(z) == 48
    return float(np.log(np.prod(1 + z[hi].astype(float) / 100)) - np.log(np.prod(1 + z[lo].astype(float) / 100)))
A = pd.DataFrame({'y': range(1964, 1997)}); A['caida'] = A.y.map(caida); A['dif'] = A.y.map(dif)
print(A.round(3).to_string(index=False), flush=True)
o = spearmanr(A.caida, A.dif)[0]; P = np.array([spearmanr(A.caida, rng.permutation(A.dif.values))[0] for _ in range(10000)]); p = ((P <= o).sum() + 1) / 10001
print(f'VO128 caida vs log(riesgosas/quietas) 4 anios, 1964-1996 rho {o:+.2f} p {p:.4f}')
print('CRITERIO128', 'pasa' if o < 0 and p < .05 else 'no pasa')
