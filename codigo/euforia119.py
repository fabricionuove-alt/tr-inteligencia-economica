"""#119: S-1 por año (índices de EDGAR) contra la diferencia de #117. Reglas en notas/11 (#119)."""
import gzip, time, urllib.request, numpy as np, pandas as pd
from scipy.stats import spearmanr
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
n = {}
for y in range(2009, 2022):
    c = 0
    for q in range(1, 5):
        for k in range(5):
            try: b = urllib.request.urlopen(urllib.request.Request(f'https://www.sec.gov/Archives/edgar/full-index/{y}/QTR{q}/form.gz', headers=UA), timeout=120).read(); break
            except Exception: time.sleep(10)
        for l in gzip.decompress(b).decode('latin1').splitlines():
            if l.startswith('S-1 ') : c += 1
        time.sleep(.3)
    n[y] = c; print(y, 'S-1', c, flush=True)
t = pd.read_csv(f'{B}/entrenar/sal-cab102/ciclo117_cohortes.csv'); t['s1_antes'] = t['ap'].map(lambda a: n.get(a - 1))
print(t[['ap', 'dif', 'mercado4', 's1_antes']].to_string(index=False))
obs = spearmanr(t['s1_antes'], t['dif'])[0]; P = np.array([spearmanr(t['s1_antes'], rng.permutation(t['dif'].values))[0] for _ in range(10000)])
p = ((P <= obs).sum() + 1) / 10001; r2 = spearmanr(t['s1_antes'], t['mercado4'])[0]
print(f'EU119 S-1 año antes vs diferencia rho {obs:+.2f} p {p:.4f} | vs mercado 4 años rho {r2:+.2f}')
print(f'CRITERIO119 {"pasa" if obs < 0 and p < .05 else "no pasa"}')
