"""Señales #52-#54 (notas/11): quién se sienta en qué directorio, año por año, desde los formularios 3/4/5 de la SEC.
Uso: python red_bajar.py [LIMITE] [FILTRO]
Salida red.csv: anio, id (empresa, hash como siempre), dueno (persona, hash), rol (D director, O directivo,
T dueño de más del 10%, X otro), persona (1 si no parece sociedad), apellido (hash). Sin nombres."""
import sys, io, re, time, zipfile, hashlib, csv, urllib.request

UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
LIM = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6
FILTRO = sys.argv[2] if len(sys.argv) > 2 else ''
def get(u):
    for i in range(4):
        try:
            time.sleep(0.12)
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=180).read()
        except Exception as e:
            print('reintento', u[-40:], type(e).__name__, flush=True); time.sleep(2 + 3 * i)
    return None
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
ho = lambda x: hashlib.sha256(('dueno-' + x).encode()).hexdigest()[:10]
ha = lambda x: hashlib.sha256(('apellido-' + x).encode()).hexdigest()[:10]
SOC = re.compile(r'\b(INC|LLC|L\.?L\.?C|LP|L\.?P|LTD|FUND|FUNDS|CAPITAL|PARTNERS|HOLDINGS?|BANK|GROUP|CORP|CORPORATION|CO|COMPANY|'
                 r'TRUST COMPANY|ADVISORS?|MANAGEMENT|INVESTMENTS?|VENTURES?|SA|AG|NV|PLC|GMBH|LIMITED|ASSOCIATES|FOUNDATION|PARTNERSHIP)\b')
def rol(rel):
    r = rel.upper(); s = ''
    if 'DIRECTOR' in r: s += 'D'
    if 'OFFICER' in r: s += 'O'
    if 'TENPERCENT' in r.replace(' ', '').replace('%', 'PERCENT') or '10' in r: s += 'T'
    return s or 'X'

t0 = time.time()
pag = get('https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets').decode('utf-8', 'ignore')
ins = sorted(x for x in set(re.findall(r'href="([^"]+form345\.zip)"', pag)) if FILTRO in x)[:LIM]
print(len(ins), 'trimestres', flush=True)
vistos = {}
DIN = re.compile(r'\b(ROTHSCHILD|WALLENBERG|AGNELLI|ELKANN|ROCKEFELLER|PRITZKER|WALTON|DU ?PONT|MELLON|BRONFMAN|SAFRA|PICTET|PEUGEOT|ARNAULT|BETTENCOURT|MEYERS|QUANDT|KLATTEN|PORSCHE|PIECH|OETKER|HENKEL|THYSSEN|BOTIN|BOTÍN|MULLIEZ|FRERE|DESMARAIS|WERTHEIMER|LAUDER|MARS|CARGILL|MACMILLAN|BUSCH|COORS|HEARST|COX|NEWHOUSE|ZIFF|HUNT|BASS|KOCH|HABSBURG|HOHENZOLLERN|LIECHTENSTEIN|THURN|GROSVENOR|ORANGE|BOURBON|SAVOY|WINDSOR|GUINNESS|CADBURY|SAINSBURY|WESTON|BRENNINKMEYER|HEINEKEN|BONNIER|PERSSON|KAMPRAD|JACOBS|SCHWARZ|ALBRECHT|REIMANN|LEE|AMBANI|TATA|BIRLA|MAHINDRA)\b')
dinast = []
simb = {}                                                  # (símbolo, año) -> {id: veces}
for k, u in enumerate(ins):
    b = get('https://www.sec.gov' + u)
    if not b:
        print('FALTA', u, flush=True); continue
    z = zipfile.ZipFile(io.BytesIO(b))
    rd = lambda n: z.read(n).decode('latin1').splitlines()
    L = rd('SUBMISSION.tsv'); c = L[0].split('\t')
    iA, iF, iC, iS = c.index('ACCESSION_NUMBER'), c.index('FILING_DATE'), c.index('ISSUERCIK'), c.index('ISSUERTRADINGSYMBOL')
    sub = {}
    for l in L[1:]:
        v = l.split('\t')
        if len(v) > max(iA, iF, iC) and v[iF][-4:].isdigit():
            sub[v[iA]] = (int(v[iF][-4:]), v[iC])
            sy = v[iS].replace('"', '').strip().upper() if len(v) > iS else ''
            if sy:
                d_ = simb.setdefault((sy, int(v[iF][-4:])), {}); d_[h(v[iC])] = d_.get(h(v[iC]), 0) + 1
    L = rd('REPORTINGOWNER.tsv'); c = L[0].split('\t')
    iA2, iO, iN, iR = c.index('ACCESSION_NUMBER'), c.index('RPTOWNERCIK'), c.index('RPTOWNERNAME'), c.index('RPTOWNER_RELATIONSHIP')
    n0 = len(vistos)
    for l in L[1:]:
        v = l.split('\t')
        if len(v) <= max(iA2, iO, iN, iR) or v[iA2] not in sub:
            continue
        anio, cik = sub[v[iA2]]
        _m = DIN.search(v[iN].upper())
        if _m: dinast.append((anio, h(cik), ho(v[iO]), _m.group(1), rol(v[iR])))
        nom = v[iN].upper().strip()
        clave = (anio, h(cik), ho(v[iO]))
        r = rol(v[iR])
        persona = 0 if SOC.search(nom) else 1
        ap = ha(re.split(r'[\s,]+', nom)[0]) if persona and nom else ''
        if clave in vistos:
            viejo = vistos[clave]
            vistos[clave] = (''.join(sorted(set(viejo[0] + r) - ({'X'} if len(set(viejo[0] + r)) > 1 else set()))), persona, ap)
        else:
            vistos[clave] = (r, persona, ap)
    print(f'{k + 1}/{len(ins)} {u[-20:]} +{len(vistos) - n0} ({time.time() - t0:.0f}s)', flush=True)
with open('red.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['anio', 'id', 'dueno', 'rol', 'persona', 'apellido'])
    for (a, i, d), (r, p, ap) in sorted(vistos.items()):
        w.writerow([a, i, d, r, p, ap])
with open('simbolos.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['simbolo', 'anio', 'id'])
    for (sy, a), d_ in sorted(simb.items()):
        w.writerow([sy, a, max(d_, key=d_.get)])
with open('dinastias.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['anio', 'id', 'dueno', 'apellido', 'rol']); w.writerows(sorted(set(dinast)))
print('DINASTIAS', len(set(dinast)), flush=True)
print('LISTO', len(vistos), 'filas', f'({time.time() - t0:.0f}s)', flush=True)
