"""#123 (compras netas de directivos) y #124 (reescritura de toda la economía) vs ciclo de #117. Reglas en notas/11."""
import os, io, json, time, zipfile, urllib.request, numpy as np, pandas as pd
from scipy.stats import spearmanr
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; D = f'{B}/fuentes/insiders'; rng = np.random.default_rng(0)
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
cuenta = {}
for y in range(2009, 2022):
    for q in range(1, 5):
        f = f'{D}/{y}q{q}_form345.zip'
        if not os.path.exists(f):
            for k in range(4):
                try:
                    b = urllib.request.urlopen(urllib.request.Request(f'https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{y}q{q}_form345.zip', headers=UA), timeout=180).read()
                    open(f, 'wb').write(b); break
                except Exception as e: print('reintento', y, q, e, flush=True); time.sleep(10)
            time.sleep(1)
        z = zipfile.ZipFile(f); n = [m for m in z.namelist() if m.upper().endswith('NONDERIV_TRANS.TSV')][0]
        t = pd.read_csv(z.open(n), sep='\t', usecols=['ACCESSION_NUMBER', 'SECURITY_TITLE', 'TRANS_CODE'], dtype=str, on_bad_lines='skip')
        t = t[t.SECURITY_TITLE.str.contains('common', case=False, na=False) & t.TRANS_CODE.isin(['P', 'S'])].drop_duplicates(['ACCESSION_NUMBER', 'TRANS_CODE'])
        c = t.TRANS_CODE.value_counts(); a = cuenta.setdefault(y, [0, 0]); a[0] += int(c.get('P', 0)); a[1] += int(c.get('S', 0))
        print(y, q, int(c.get('P', 0)), int(c.get('S', 0)), flush=True)
npr = {y: (p - s) / (p + s) for y, (p, s) in cuenta.items()}
co = pd.read_csv(f'{B}/entrenar/sal-cab102/ciclo117_cohortes.csv')
a = pd.read_csv(f'{B}/entrenar/sal-cab102/lazy112_filas.csv', usecols=['ap', 'sim'])
b = pd.DataFrame([{'ap': y, 'sim': o[f's{y}']} for o in map(json.loads, open(f'{B}/entrenar/sal-cab102/sim114.jsonl')) for y in (2021, 2022) if f's{y}' in o])
med = pd.concat([a, b]).groupby('ap')['sim'].median()
co['compras_netas_antes'] = co['ap'].map(lambda y: npr[y - 1]); co['similitud_mediana'] = co['ap'].map(med)
print(co.round(3).to_string(index=False), flush=True)
def perm(u, v):
    o = spearmanr(u, v)[0]; P = np.array([spearmanr(u, rng.permutation(v))[0] for _ in range(10000)])
    return o, ((P >= o).sum() + 1) / 10001, ((np.abs(P) >= abs(o)).sum() + 1) / 10001
r, p1, _ = perm(co.compras_netas_antes.values, co.dif.values); r2, _, _ = perm(co.compras_netas_antes.values, co.mercado4.values)
print(f'AD123 compras netas vs diferencia rho {r:+.2f} p {p1:.4f} | vs mercado 4 anios rho {r2:+.2f}')
print('CRITERIO123', 'pasa' if r > 0 and p1 < .05 else 'no pasa')
r, _, p2 = perm(co.similitud_mediana.values, co.dif.values); r2, _, _ = perm(co.similitud_mediana.values, co.mercado4.values)
print(f'AD124 similitud mediana vs diferencia rho {r:+.2f} p {p2:.4f} (dos colas) | vs mercado 4 anios rho {r2:+.2f}')
print('CRITERIO124', 'pasa' if p2 < .05 else 'no pasa')
