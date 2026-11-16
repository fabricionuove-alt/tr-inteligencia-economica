"""#127: caída del S&P desde su máximo de 60 meses al comprar vs 4 años siguientes (peso igual) y vs diferencia de #117."""
import io, numpy as np, pandas as pd
from scipy.stats import spearmanr
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
sp = pd.read_csv(f'{B}/fuentes/sp500_shiller.csv'); sp['f'] = sp['Date'].str[:4].astype(int) * 100 + sp['Date'].str[5:7].astype(int); sp = sp.set_index('f')['SP500']
def caida(y):
    k = list(sp.index).index(y * 100 + 3); return sp.iloc[k] / sp.iloc[k - 60:k + 1].max() - 1
L = open(f'{B}/fuentes/french/Portfolios_Formed_on_ME.csv').read().splitlines()
i = next(k for k, l in enumerate(L) if 'Average Equal Weighted Returns -- Monthly' in l); j = next(k for k in range(i + 2, len(L)) if not L[k].strip())
d = pd.read_csv(io.StringIO('\n'.join(L[i + 1:j]))); d.columns = ['f'] + [c.strip() for c in d.columns[1:]]
dec = ['Lo 10'] + [f'{k}-Dec' for k in range(2, 10)] + ['Hi 10']; d['r'] = d[dec].astype(float).mean(axis=1) / 100; d['f'] = d['f'].astype(int)
ew4 = lambda y: float(np.prod(1 + d[(d.f >= y * 100 + 4) & (d.f <= (y + 4) * 100 + 3)]['r']))
A = pd.DataFrame({'y': range(1997, 2022)}); A['caida'] = A.y.map(caida); A['ew4'] = A.y.map(ew4)
print(A.round(3).to_string(index=False), flush=True)
def perm(u, v):
    o = spearmanr(u, v)[0]; P = np.array([spearmanr(u, rng.permutation(v))[0] for _ in range(10000)]); return o, ((P <= o).sum() + 1) / 10001
ra, pa = perm(A.caida.values, A.ew4.values)
co = pd.read_csv(f'{B}/entrenar/sal-cab102/ciclo117_cohortes.csv'); co['caida'] = co.ap.map(caida)
print(co[['ap', 'dif', 'mercado4', 'caida']].round(3).to_string(index=False), flush=True)
rb, pb = perm(co.caida.values, co.dif.values)
print(f'CR127 A caida vs 4 anios peso igual (1997-2021) rho {ra:+.2f} p {pa:.4f}')
print(f'CR127 B caida vs diferencia cambiadas-quietas (2010-2022) rho {rb:+.2f} p {pb:.4f}')
print('CRITERIO127 A', 'pasa' if ra < 0 and pa < .05 else 'no pasa', '| B', 'pasa' if rb < 0 and pb < .05 else 'no pasa')
