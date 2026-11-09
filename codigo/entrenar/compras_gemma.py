"""#86: compras de directivos x Gemma. Uso: python compras_gemma.py filas.csv personas.csv FALLAS_CSVS TEMA10K_CSVS"""
import sys, os, numpy as np, pandas as pd
sys.argv = sys.argv[:5] + ['x.json']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tr4.py'), encoding='utf-8').read().split("def arbol(")[0])
d = pd.DataFrame({'anio': anio, 'pres': pres.values, 'compras': R['compras'].values, 'gemma': R['gemma'].values if 'gemma' in R else np.nan, 'r4': r4, 'r1': r1})
d = d[d['pres'].between(2017, 2020) & d['gemma'].notna()]
print(f'CG filas con Gemma 2017-2020: {len(d)} | con compras de directivos: {int((d["compras"] > 0).sum())}', flush=True)
c = d[d['compras'] > 0].copy(); c['alta'] = c.groupby('pres')['gemma'].rank(pct=True) > 0.5
for h, col in (('4 años', 'r4'), ('12 meses', 'r1')):
    x = c.dropna(subset=[col]); u = d.dropna(subset=[col]); gana = des = 0; n = 0
    for a, g in x.groupby('pres'):
        A, B, U = g[g['alta']][col], g[~g['alta']][col], u[u['pres'] == a][col]
        if len(A) < 10 or len(B) < 10: continue
        n += 1; gana += A.mean() > B.mean(); des += (A <= 0.5).mean() < (B <= 0.5).mean()
        print(f'CG {h} {a}: compras+Gemma alta ×{A.mean():.3f} des {100 * (A <= 0.5).mean():.1f}% x3 {100 * (A >= 3).mean():.1f}% (n {len(A)}) | compras+Gemma baja ×{B.mean():.3f} des {100 * (B <= 0.5).mean():.1f}% x3 {100 * (B >= 3).mean():.1f}% (n {len(B)}) | universo ×{U.mean():.3f} des {100 * (U <= 0.5).mean():.1f}%', flush=True)
    print(f'CRITERIO86 {h}: Gemma alta gana {gana} de {n}, menos desastres {des} de {n} ->', ('PASA' if gana >= 3 and des >= 3 else 'no pasa') if h == '4 años' else '(informado)', flush=True)
