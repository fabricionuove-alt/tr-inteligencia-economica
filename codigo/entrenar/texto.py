"""Cuánto cambia el texto del 10-K de un año al otro ("Lazy Prices", Cohen-Malloy-Nguyen 2020).
Fuente: EDGAR-CORPUS (Hugging Face, eloukas/edgar-corpus), 10-K partidos por sección, 1993-2020.
Uso: python texto.py AÑOS [LIMITE] [CARPETA_LOCAL]
  AÑOS: años de presentación a calcular, ej. 2013,2014,2015 (baja también el año anterior a cada uno)
  LIMITE: máx. registros por archivo (prueba corta)
  CARPETA_LOCAL: leer AÑO/*.jsonl de una carpeta en vez de bajar (prueba local)
Salida: texto-<primer año>.csv  id, anio_presentado, texto_igual_total, _riesgos, _juicios, _mdna
El texto se lee de a una línea mientras se baja: no se guarda en disco."""
import sys, os, io, json, time, hashlib, urllib.request
import numpy as np
from scipy import sparse
from multiprocessing import Pool
from sklearn.feature_extraction.text import HashingVectorizer
try:
    import orjson; cargar = orjson.loads          # 3-4 veces más rápido
except ImportError:
    cargar = json.loads
TMP = os.environ.get('TMP_TEXTO', '/tmp')

ANIOS = [int(a) for a in sys.argv[1].split(',')] if len(sys.argv) > 1 and sys.argv[1][:1].isdigit() else []
LIM = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != '-' else 10**9
LOCAL = sys.argv[3] if len(sys.argv) > 3 else None
BASE = 'https://huggingface.co/datasets/eloukas/edgar-corpus/resolve/main'
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
# Secciones: 'total' = todo el texto propio salvo los estados contables (8) y anexos (15), que son números.
PARTES = {
    'total': ['section_1', 'section_1A', 'section_2', 'section_3', 'section_5', 'section_7', 'section_7A',
              'section_9A', 'section_10', 'section_11', 'section_12', 'section_13', 'section_14'],
    'riesgos': ['section_1A'], 'juicios': ['section_3'], 'mdna': ['section_7'],
}
vec = HashingVectorizer(n_features=2 ** 20, alternate_sign=False, norm='l2', stop_words='english',
                        token_pattern=r'(?u)\b[a-zA-Z][a-zA-Z]{2,}\b', dtype=np.float32)

def lineas(anio):
    for parte in ('train', 'validate', 'test'):
        if LOCAL:
            p = os.path.join(LOCAL, str(anio), f'{parte}.jsonl')
            if not os.path.exists(p):
                continue
            fh = open(p, encoding='utf-8')
        else:
            u = f'{BASE}/{anio}/{parte}.jsonl'
            for i in range(4):
                try:
                    fh = io.TextIOWrapper(urllib.request.urlopen(u, timeout=300), encoding='utf-8'); break
                except Exception as e:
                    print('reintento', u, type(e).__name__, flush=True); time.sleep(5 * (i + 1))
            else:
                continue
        for n, l in enumerate(fh):
            if n >= LIM:
                break
            yield l

def vectores(anio):
    """{cik: {parte: vector}} del año (primer 10-K de cada empresa ese año)."""
    t0 = time.time()
    ciks, textos = [], {k: [] for k in PARTES}
    vistos = set()
    for l in lineas(anio):
        try:
            d = cargar(l)
        except Exception:
            continue
        c = str(d.get('cik', '')).strip()
        if not c or c in vistos:
            continue
        vistos.add(c); ciks.append(c)
        for k, secs in PARTES.items():
            textos[k].append(' '.join(d.get(s) or '' for s in secs))
    # se guarda en disco: pasar matrices grandes entre procesos es lento
    for k, v in textos.items():
        sparse.save_npz(os.path.join(TMP, f'v{anio}_{k}.npz'), vec.transform(v))
        np.save(os.path.join(TMP, f'l{anio}_{k}.npy'), np.array([len(x) for x in v]))
    json.dump(ciks, open(os.path.join(TMP, f'c{anio}.json'), 'w'))
    print(f'  año {anio}: {len(ciks)} empresas, {time.time()-t0:.0f}s', flush=True)
    return anio

def cargar_anio(anio):
    ciks = json.load(open(os.path.join(TMP, f'c{anio}.json')))
    M = {k: sparse.load_npz(os.path.join(TMP, f'v{anio}_{k}.npz')).tocsr() for k in PARTES}
    L = {k: np.load(os.path.join(TMP, f'l{anio}_{k}.npy')) for k in PARTES}
    return ciks, M, L

if __name__ == '__main__':
    t0 = time.time()
    necesarios = sorted(set(ANIOS) | {a - 1 for a in ANIOS})
    with Pool(min(4, len(necesarios))) as pool:      # un año por núcleo
        pool.map(vectores, necesarios)
    V = {}
    out = []
    for a in necesarios:
        V[a] = cargar_anio(a)
        if a in ANIOS and (a - 1) in V:
            c1, M1, L1 = V[a]; c0, M0, L0 = V[a - 1]
            pos0 = {c: i for i, c in enumerate(c0)}
            for i, c in enumerate(c1):
                j = pos0.get(c)
                if j is None:
                    continue
                fila = {'id': h(c), 'anio_presentado': a}
                for k in PARTES:
                    # sin texto en alguno de los dos años: no hay dato (no es "cambió todo")
                    if L1[k][i] < 200 or L0[k][j] < 200:
                        fila['texto_igual_' + k] = None
                    else:
                        fila['texto_igual_' + k] = float(M1[k][i].multiply(M0[k][j]).sum())
                out.append(fila)
        for viejo in [x for x in V if x < a - 1]:
            del V[viejo]            # sólo hacen falta dos años en memoria
    nombre = f'texto-{ANIOS[0]}.csv'
    with open(nombre, 'w') as fh:
        cols = ['id', 'anio_presentado'] + ['texto_igual_' + k for k in PARTES]
        fh.write(','.join(cols) + '\n')
        for f in out:
            fh.write(','.join('' if f[c] is None else str(f[c]) for c in cols) + '\n')
    print(f'LISTO {len(out)} pares empresa-año en {time.time()-t0:.0f}s -> {nombre}', flush=True)
