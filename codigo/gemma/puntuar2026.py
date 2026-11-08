"""Aplica un modelo congelado de Gemma a los 10-K de 2026. Uso: python puntuar2026.py MODELO.npz PREFIJO(sae2|sae2b) CAPAS SALIDA.csv"""
import sys, glob, numpy as np, pandas as pd
from scipy import sparse
m = np.load(sys.argv[1], allow_pickle=True); pre, capas, sal = sys.argv[2], sys.argv[3].split(','), sys.argv[4]
X = sparse.hstack([sparse.load_npz(f'{pre}-textos-2026-L{c}.npz') for c in capas]).tocsr(); ids = np.load(f'{pre}-textos-2026-ids.npy')
Z = np.log1p(X[:, m['usar']].toarray() / m['med']); Z = (Z - m['mu']) / m['sd']
pd.DataFrame({'id': ids, 'anio_presentado': 2026, 'gemma': Z @ m['coef'] + m['b']}).to_csv(sal, index=False)
print('PUNTAJE 2026', len(ids), sal)
