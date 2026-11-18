"""#151: ventaja en rendimiento por camada contra la caída del S&P desde su máximo en marzo. Reglas en notas/11 (#151)."""
import pandas as pd, numpy as np
from scipy.stats import spearmanr
v = {2010: .100, 2011: .285, 2012: .151, 2017: .487, 2018: .340, 2019: .217, 2020: .142, 2021: .137, 2022: .026}   # de sal-cab102/rinde149.log y antes150.log
s = pd.read_csv('../fuentes/sp500_shiller.csv', parse_dates=['Date']).set_index('Date').SP500
dd = {y: 1 - s[f'{y}-03-01'] / s[:f'{y}-03-01'].max() for y in v}
r4 = {y: s[f'{y+4}-03-01'] / s[f'{y}-03-01'] for y in v}
for y in v: print(y, f'ventaja {v[y]:+.3f} caída desde el máximo {dd[y]*100:5.1f}% mercado 4 años x{r4[y]:.2f}')
a = spearmanr(list(v.values()), list(dd.values())); b = spearmanr(list(v.values()), list(r4.values()))
print(f'F151 Spearman ventaja vs caída {a[0]:+.2f} p {a[1]:.3f} | (informativo) vs mercado 4 años {b[0]:+.2f} p {b[1]:.3f}')
print('CRITERIO151', 'PASA' if a[0] >= .6 and a[1] < .05 else 'no pasa')
