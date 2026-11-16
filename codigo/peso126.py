"""#126: mediana de similitud 1997-2009 (#125) vs mercado de peso igual (French, 10 deciles), abril y a marzo y+4."""
import io, json, numpy as np, pandas as pd
from scipy.stats import spearmanr
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'
L = open(f'{B}/fuentes/french/Portfolios_Formed_on_ME.csv').read().splitlines()
i = next(k for k, l in enumerate(L) if 'Average Equal Weighted Returns -- Monthly' in l)
j = next(k for k in range(i + 2, len(L)) if not L[k].strip())
d = pd.read_csv(io.StringIO('\n'.join(L[i + 1:j]))); d.columns = ['f'] + [c.strip() for c in d.columns[1:]]
dec = ['Lo 10'] + [f'{k}-Dec' for k in range(2, 10)] + ['Hi 10']
d['r'] = d[dec].astype(float).mean(axis=1) / 100; d['f'] = d['f'].astype(int)
s = pd.DataFrame([o for o in map(json.loads, open(f'{B}/entrenar/sal-cab102/viejo125.jsonl')) if 'sim' in o]); m = s.groupby('y')['sim'].median().to_frame('mediana')
m['ew4'] = [float(np.prod(1 + d[(d.f >= y * 100 + 4) & (d.f <= (y + 4) * 100 + 3)]['r'])) for y in m.index]
print(m.round(5).to_string(), flush=True)
rng = np.random.default_rng(0); o = spearmanr(m.mediana, m.ew4)[0]
P = np.array([spearmanr(m.mediana, rng.permutation(m.ew4.values))[0] for _ in range(10000)]); p = ((P <= o).sum() + 1) / 10001
print(f'PI126 mediana similitud vs mercado peso igual 4 anios rho {o:+.2f} p {p:.4f}'); print('CRITERIO126', 'pasa' if o < 0 and p < .05 else 'no pasa')
