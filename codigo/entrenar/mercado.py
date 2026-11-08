"""Precios y compras de directivos, todo de la SEC y gratis.
Uso: python mercado.py [LIMITE]   (LIMITE = cuántos archivos de cada tipo, para la prueba corta)
Salidas (todo con id anónimo, igual que las filas):
  precios.csv       id, mes (AAAAMM), precio   ← fails-to-deliver; si falta, precio de compras/ventas de directivos
  directivos.csv    id, mes, dueño (hash), tipo (P compra / S venta), valor
Cómo se sabe de qué empresa es un símbolo: los formularios de directivos traen símbolo + CIK de la empresa
con fecha; se arma símbolo+año -> CIK (los símbolos se reutilizan con los años)."""
import sys, io, re, time, zipfile, hashlib, collections, urllib.request
from multiprocessing import Pool

UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
LIM = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6
FILTRO = sys.argv[2] if len(sys.argv) > 2 else ''   # para probar: sólo archivos cuyo nombre contenga esto (ej. 2015)
DESDE = int(sys.argv[3]) if len(sys.argv) > 3 else 1900   # años que hace este cuaderno (se parte en dos por tiempo)
HASTA = int(sys.argv[4]) if len(sys.argv) > 4 else 2100
def anio_de(u):
    m = re.search(r'(\d{4})q\d_form345', u) or re.search(r'cnsfails(\d{4})', u)
    return int(m.group(1)) if m else 0
def get(u):
    for i in range(4):
        try:
            time.sleep(0.12)
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120).read()
        except Exception as e:
            print('reintento', u[-40:], type(e).__name__, flush=True); time.sleep(2 + 3 * i)
    return None
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
ho = lambda x: hashlib.sha256(('dueno-' + x).encode()).hexdigest()[:10]
MES = {m: f'{i:02d}' for i, m in enumerate(['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'], 1)}
def mes_de(d):  # '30-JUN-2026' -> '202606'
    p = d.split('-')
    return p[2] + MES.get(p[1], '00') if len(p) == 3 else None

t0 = time.time()
pag = get('https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets').decode('utf-8', 'ignore')
ins = sorted(x for x in set(re.findall(r'href="([^"]+form345\.zip)"', pag)) if FILTRO in x)
pag = get('https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data').decode('utf-8', 'ignore')
ftd = sorted(x for x in set(re.findall(r'href="([^"]+cnsfails[^"]+\.zip)"', pag)) if FILTRO in x)
ins = [u for u in ins if DESDE - 1 <= anio_de(u) <= HASTA + 1]   # ±1 año: sólo para el mapa de símbolos
ftd = [u for u in ftd if DESDE <= anio_de(u) <= HASTA]
ins, ftd = ins[:LIM + 2], ftd[:LIM]   # el límite (prueba corta) va DESPUÉS del filtro de años
print(len(ins), 'trimestres de directivos,', len(ftd), 'quincenas de precios', flush=True)

simb = collections.defaultdict(collections.Counter)      # (símbolo, año) -> CIKs
tx = []                                                   # (cik, mes, dueño, tipo, valor, precio)
ten = []                                                  # (cik, mes, dueño, acciones que tiene)
for k, u in enumerate(ins):
    b = get('https://www.sec.gov' + u)
    if not b:
        continue
    z = zipfile.ZipFile(io.BytesIO(b))
    rd = lambda n: z.read(n).decode('latin1').splitlines()
    sub = {}
    fecha = {}
    L = rd('SUBMISSION.tsv'); c = L[0].split('\t')
    iA, iF, iC, iS = c.index('ACCESSION_NUMBER'), c.index('FILING_DATE'), c.index('ISSUERCIK'), c.index('ISSUERTRADINGSYMBOL')
    for l in L[1:]:
        v = l.split('\t')
        if len(v) <= iS:
            continue
        sub[v[iA]] = v[iC]
        fecha[v[iA]] = mes_de(v[iF])
        sy = v[iS].strip().upper()
        if sy and v[iF][-4:].isdigit():
            simb[(sy, v[iF][-4:])][v[iC]] += 1
    duen = {}
    L = rd('REPORTINGOWNER.tsv'); c = L[0].split('\t'); iA2, iO = c.index('ACCESSION_NUMBER'), c.index('RPTOWNERCIK')
    for l in L[1:]:
        v = l.split('\t')
        if len(v) > iO:
            duen.setdefault(v[iA2], v[iO])
    L = rd('NONDERIV_TRANS.tsv'); c = L[0].split('\t')
    iA3, iD, iCo, iSh, iP = (c.index(x) for x in ('ACCESSION_NUMBER', 'TRANS_DATE', 'TRANS_CODE', 'TRANS_SHARES', 'TRANS_PRICEPERSHARE'))
    for l in L[1:]:
        v = l.split('\t')
        if len(v) <= iP or v[iCo] not in ('P', 'S'):
            continue
        try:
            sh, pr = float(v[iSh]), float(v[iP])
        except ValueError:
            continue
        if pr <= 0 or sh <= 0 or v[iA3] not in sub:
            continue
        m = mes_de(v[iD])
        if m and DESDE <= anio_de(u) <= HASTA:   # las transacciones, sólo de los años propios (no duplicar)
            tx.append((sub[v[iA3]], m, ho(duen.get(v[iA3], '?')), v[iCo], sh * pr, pr))
    # TENENCIAS: cuántas acciones le quedan a cada dueño de adentro en cada formulario.
    # Directas (D) e indirectas (I, fideicomisos, sociedades): máximo de cada tipo, sumados.
    if DESDE <= anio_de(u) <= HASTA:
        tiene = collections.defaultdict(lambda: {'D': 0.0, 'I': 0.0})
        for nombre_t in ('NONDERIV_TRANS.tsv', 'NONDERIV_HOLDING.tsv'):
            L = rd(nombre_t); c = L[0].split('\t')
            jA, jS, jD = c.index('ACCESSION_NUMBER'), c.index('SHRS_OWND_FOLWNG_TRANS'), c.index('DIRECT_INDIRECT_OWNERSHIP')
            for l in L[1:]:
                v = l.split('\t')
                if len(v) <= max(jS, jD) or v[jA] not in sub:
                    continue
                try:
                    q = float(v[jS])
                except ValueError:
                    continue
                t_ = 'I' if v[jD].strip().upper() == 'I' else 'D'
                if q > tiene[v[jA]][t_]:
                    tiene[v[jA]][t_] = q
        for acc, dd in tiene.items():
            if fecha.get(acc) and dd['D'] + dd['I'] > 0:
                ten.append((sub[acc], fecha[acc], ho(duen.get(acc, '?')), dd['D'] + dd['I']))
    if k % 10 == 0:
        print(f'directivos {k+1}/{len(ins)}  transacciones {len(tx)}  {time.time()-t0:.0f}s', flush=True)

def mapa_cik(sy, anio):
    c = simb.get((sy, anio)) or simb.get((sy, str(int(anio) - 1))) or simb.get((sy, str(int(anio) + 1)))
    return c.most_common(1)[0][0] if c else None

# bajar fails-to-deliver (secuencial por el límite de la SEC) y leer en paralelo
crudos = []
for k, u in enumerate(ftd):
    b = get('https://www.sec.gov' + u)
    if b:
        crudos.append(b)
    if k % 50 == 0:
        print(f'precios bajados {k+1}/{len(ftd)}  {time.time()-t0:.0f}s', flush=True)

def leer(b):
    out = []
    try:
        z = zipfile.ZipFile(io.BytesIO(b))
        for l in z.read(z.namelist()[0]).decode('latin1').splitlines()[1:]:
            v = l.split('|')
            if len(v) >= 6 and len(v[0]) == 8:
                try:
                    p = float(v[5])
                except ValueError:
                    continue
                if p > 0:
                    out.append((v[0][:6], v[2].strip().upper(), p, v[1].strip().upper()))
    except Exception:
        pass
    return out

import os
if os.name == 'nt':   # Windows (prueba local): en serie
    filas = [x for b in crudos for x in leer(b)]
else:                 # Kaggle (Linux): 4 núcleos
    with Pool(4) as pool:
        filas = [x for lote in pool.map(leer, crudos) for x in lote]
del crudos
print('filas de precio', len(filas), f'{time.time()-t0:.0f}s', flush=True)

px = collections.defaultdict(list)
cus = collections.defaultdict(collections.Counter)      # (CUSIP, año) -> CIKs: para leer las carteras 13F
sin = 0
for mes, sy, p, cu in filas:
    cik = mapa_cik(sy, mes[:4])
    if cik:
        px[(cik, mes)].append(p)
        if len(cu) == 9:
            cus[(cu, mes[:4])][cik] += 1
    else:
        sin += 1
with open(f'cusip-{DESDE}.csv', 'w') as fh:
    fh.write('cusip,anio,id' + chr(10))
    for (cu, a), c in cus.items():
        fh.write(f'{cu},{a},{h(c.most_common(1)[0][0])}' + chr(10))
print('códigos CUSIP con empresa:', len(cus), flush=True)
print('precios sin empresa (ETF, extranjeras, etc.):', sin, flush=True)
# respaldo: precio de las compras/ventas de directivos ese mes
px2 = collections.defaultdict(list)
for cik, mes, _, _, _, pr in tx:
    px2[(cik, mes)].append(pr)
med = lambda a: sorted(a)[len(a) // 2]
with open(f'precios-{DESDE}.csv', 'w') as fh:
    fh.write('id,mes,precio,fuente\n')
    n1 = n2 = 0
    for key in set(px) | set(px2):
        if key in px:
            fh.write(f'{h(key[0])},{key[1]},{med(px[key])},ftd\n'); n1 += 1
        else:
            fh.write(f'{h(key[0])},{key[1]},{med(px2[key])},directivos\n'); n2 += 1
with open(f'directivos-{DESDE}.csv', 'w') as fh:
    fh.write('id,mes,dueno,tipo,valor\n')
    for cik, mes, du, ti, va, _ in tx:
        fh.write(f'{h(cik)},{mes},{du},{ti},{va:.0f}\n')
with open(f'tenencias-{DESDE}.csv', 'w') as fh:
    fh.write('id,mes,dueno,acciones' + chr(10))
    for cik, mes, du, q in ten:
        fh.write(f'{h(cik)},{mes},{du},{q:.0f}' + chr(10))
print(f'LISTO precios empresa-mes: {n1} de fails-to-deliver + {n2} de directivos; transacciones {len(tx)}; tenencias {len(ten)}; {time.time()-t0:.0f}s', flush=True)
