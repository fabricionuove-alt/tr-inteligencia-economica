"""#87: junta lado a lado los vectores de varias secciones (mismas empresas): python juntar_secciones.py SALIDA PREFIJO_SALIDA dir:prefijo dir:prefijo ..."""
import sys, os, numpy as np
from scipy import sparse
out, po, partes = sys.argv[1], sys.argv[2], [p.split(':') for p in sys.argv[3:]]; os.makedirs(out, exist_ok=True)
for a in range(2013, 2021):
    I = [np.load(f'{d}/{p}-{a}-ids.npy') for d, p in partes]; X = [sparse.load_npz(f'{d}/{p}-{a}-L12.npz').tocsr() for d, p in partes]
    com = sorted(set.intersection(*[set(i) for i in I]))
    pos = [{v: k for k, v in enumerate(i)} for i in I]
    M = sparse.hstack([x[[ps[c] for c in com]] for x, ps in zip(X, pos)]).tocsr()
    sparse.save_npz(f'{out}/{po}-{a}-L12.npz', M); np.save(f'{out}/{po}-{a}-ids.npy', np.array(com)); print(a, len(com), M.shape)
