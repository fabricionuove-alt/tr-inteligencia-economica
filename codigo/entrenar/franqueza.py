"""Franqueza de la dirección, medida con palabras (sin IA), sobre la sección 7 del 10-K (EDGAR-CORPUS).
Uso: python franqueza.py AÑOS [LIMITE] [CARPETA_LOCAL]     (AÑOS de presentación, ej. 2013,2014)
Salida: franq-<primer año>.csv  id, anio_presentado, franq_numeros, franq_cliches, franq_euforia, franq_admite,
        franq_nosotros, franq_niebla, franq_largo
Listas propias, escritas el 2-nov-2026 antes de mirar resultados (ver REGLAS_FRANQUEZA)."""
import sys, os, io, re, json, time, hashlib, urllib.request
from multiprocessing import Pool
try:
    import orjson; cargar = orjson.loads
except ImportError:
    cargar = json.loads

BASE = 'https://huggingface.co/datasets/eloukas/edgar-corpus/resolve/main'
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
C = lambda ws: re.compile(r'\b(?:' + '|'.join(ws) + r')\b', re.I)
CLICHES = C([r'world[- ]class', r'best[- ]in[- ]class', r'industry[- ]leading', r'market[- ]leading', r'synerg\w*',
             r'cutting[- ]edge', r'state[- ]of[- ]the[- ]art', r'paradigm', r'holistic', r'seamless\w*',
             r'value creation', r'core competenc\w*', r'unparalleled', r'transformational', r'game[- ]chang\w*',
             r'going forward', r'well[- ]positioned', r'uniquely positioned', r'robust', r'dynamic'])
# sin 'outstanding' ni 'exceptional': en un balance son 'acciones en circulación' y 'partidas extraordinarias'
EUFORIA = C([r'excellent', r'tremendous\w*', r'extraordinar\w*', r'fantastic',
             r'superb', r'phenomenal', r'incredibl\w*', r'remarkabl\w*', r'unprecedented', r'record[- ]breaking',
             r'spectacular', r'stellar'])
ADMITE = C([r'mistakes?', r'errors?', r'we failed', r'failure to', r'disappoint\w*', r'below (?:our )?expectations',
            r'fell short', r'shortfall', r'underperform\w*', r'we were wrong', r'did not meet', r'lower than (?:we )?expected',
            r'weaker than (?:we )?expected', r'regret\w*'])
NOS = re.compile(r'\b(?:[Ww]e|[Oo]ur|[Oo]urs|us)\b')   # sin ignorar mayusculas: 'US' es el pais
IMPERS = C([r'the company', r'the corporation', r'the registrant', r'management believes', r'it is (?:believed|anticipated|expected)'])
PAL = re.compile(r"[A-Za-z][A-Za-z'-]+")
FRASE = re.compile(r'(?<=[.!?])\s+')
DIG = re.compile(r'\d')
VOC = re.compile(r'[aeiouy]+', re.I)

def silabas(w):
    w = w.lower().rstrip('e')
    return max(1, len(VOC.findall(w)))

def medir(t):
    pal = PAL.findall(t)
    n = len(pal)
    if n < 300:
        return None
    fr = [f for f in FRASE.split(t) if len(f) > 20]
    k = 1000.0 / n
    nos, imp = len(NOS.findall(t)), len(IMPERS.findall(t))
    complejas = sum(1 for w in pal if silabas(w) >= 3)
    return {'franq_numeros': sum(1 for f in fr if DIG.search(f)) / max(1, len(fr)),
            'franq_cliches': len(CLICHES.findall(t)) * k,
            'franq_euforia': len(EUFORIA.findall(t)) * k,
            'franq_admite': len(ADMITE.findall(t)) * k,
            'franq_nosotros': nos / max(1, nos + imp),
            'franq_niebla': 0.4 * (n / max(1, len(fr)) + 100.0 * complejas / n),
            'franq_largo': float(n)}

def lineas(anio, lim, local):
    for parte in ('train', 'validate', 'test'):
        if local:
            p = os.path.join(local, str(anio), f'{parte}.jsonl')
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
            if n >= lim:
                break
            yield l

def un_anio(args):
    anio, lim, local = args
    t0 = time.time(); out = []; vistos = set()
    for l in lineas(anio, lim, local):
        try:
            d = cargar(l)
        except Exception:
            continue
        c = str(d.get('cik', '')).strip()
        if not c or c in vistos:
            continue
        vistos.add(c)
        m = medir(d.get('section_7') or '')
        if m:
            m['id'] = h(c); m['anio_presentado'] = anio
            out.append(m)
    print(f'  año {anio}: {len(out)} empresas con explicación de la dirección, {time.time()-t0:.0f}s', flush=True)
    return out

if __name__ == '__main__':
    ANIOS = [int(a) for a in sys.argv[1].split(',')]
    LIM = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != '-' else 10**9
    LOCAL = sys.argv[3] if len(sys.argv) > 3 else None
    t0 = time.time()
    with Pool(min(4, len(ANIOS))) as pool:
        res = [x for lote in pool.map(un_anio, [(a, LIM, LOCAL) for a in ANIOS]) for x in lote]
    cols = ['id', 'anio_presentado', 'franq_numeros', 'franq_cliches', 'franq_euforia', 'franq_admite',
            'franq_nosotros', 'franq_niebla', 'franq_largo']
    nombre = f'franq-{ANIOS[0]}.csv'
    with open(nombre, 'w') as fh:
        fh.write(','.join(cols) + '\n')
        for r in res:
            fh.write(','.join(str(r[c]) for c in cols) + '\n')
    print(f'LISTO {len(res)} filas en {time.time()-t0:.0f}s -> {nombre}', flush=True)
