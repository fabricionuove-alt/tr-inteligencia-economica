"""Rt: Tr que no deja de leer. Reglas en notas/15-rt.md.
Cada corrida: (1) busca 10-K nuevos en la SEC, (2) los lee como Tr v5 (#146: descripción del negocio con edgar-crawler + modelo de palabras), (3) decide comprar o vender,
(4) ejecuta lo pendiente al primer cierre posterior a la decisión, (5) anota el valor del día.
Uso: python rt/rt.py            (corrida normal)
     python rt/rt.py control    (lee las 5 empresas de control y compara con el puntaje calculado al armar Tr v5)"""
import os, re, sys, json, time, html, hashlib, datetime as dt, urllib.request
import numpy as np

R = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(R)
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
UA_PRECIOS = {'User-Agent': 'Mozilla/5.0 (Rt inteligencia-economica)'}
CAPITAL, N_POS, COSTO, COSTO_SPY = 10000.0, 365, 0.002, 0.0005
LIMITE_SEG = float(os.environ.get('LIMITE_SEG', 90 * 60))           # tiempo máximo leyendo por corrida
T0 = time.time()
ahora = lambda: dt.datetime.now(dt.timezone.utc)
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]

def get(u, pausa=0.15, cab=UA):
    for i in range(4):
        try:
            time.sleep(pausa); return urllib.request.urlopen(urllib.request.Request(u, headers=cab), timeout=60).read()
        except Exception as e:
            if '404' in str(e): return None
            time.sleep(3 + 5 * i)
    return None

# ---------- texto: igual que bajar_10k.py, sec_textos2.py y sec_textos3.py ----------
# ---------- lectura: como Tr v5 (#146): Item 1 con edgar-crawler + modelo de palabras congelado ----------
EC = os.environ.get('EDGAR_CRAWLER', os.path.join(R, '_edgar-crawler'))   # github lefterisloukas/edgar-crawler, commit 84a8d0c
X_ = {}
def extractor():
    if X_: return X_['ex']
    import tempfile
    sys.path.insert(0, EC); cwd = os.getcwd(); os.chdir(EC)
    try: from extract_items import ExtractItems
    finally: os.chdir(cwd)
    d = tempfile.mkdtemp(); os.makedirs(os.path.join(d, 'raw', '10-K')); os.makedirs(os.path.join(d, 'ext'))
    X_['d'] = d
    X_['ex'] = ExtractItems(remove_tables=True, items_to_extract=['1'], include_signature=False, raw_files_folder=os.path.join(d, 'raw'),
                            extracted_files_folder=os.path.join(d, 'ext'), skip_extracted_filings=False)
    return X_['ex']
def negocio(b, nombre, fecha=''):
    """Item 1 del 10-K, igual que entrenar/crawler145.py."""
    ex = extractor(); fn = f'{nombre}.htm'; ruta = os.path.join(X_['d'], 'raw', '10-K', fn)
    open(ruta, 'w', encoding='utf-8').write('<DOCUMENT>\n<TYPE>10-K\n' + b.decode('utf-8', 'ignore') + '\n</DOCUMENT>')
    meta = {'Type': '10-K', 'filename': fn, 'CIK': nombre, 'Company': '', 'Date': fecha, 'complete_text_file_link': '', 'htm_file_link': '', 'html_index': '',
            'Filing Date': fecha, 'Period of Report': '', 'SIC': '', 'State of Inc': '', 'State location': '', 'Fiscal Year End': '', 'filename_html': ''}
    cwd = os.getcwd(); os.chdir(EC)
    try:
        ex.determine_items_to_extract(meta); js = ex.extract_items(meta)
        return (js or {}).get('item_1', '') or ''
    except Exception: return ''
    finally:
        os.chdir(cwd)
        if os.path.exists(ruta): os.remove(ruta)

MP = np.load(os.path.join(RAIZ, 'modelos', 'palabras146.npz')); HV = []
def puntaje(texto):
    if not HV:
        from sklearn.feature_extraction.text import HashingVectorizer
        HV.append(HashingVectorizer(n_features=2 ** 20, lowercase=True, token_pattern=r'(?u)\b[a-z]{2,}\b', norm='l2', alternate_sign=False))
    v = HV[0].transform([texto])[:, MP['cols']].tocsr(); v.data = np.log1p(1000 * v.data)
    return float((v @ MP['coef'])[0] + MP['b'])

CORTES = json.load(open(os.path.join(R, 'cortes.json')))['cortes']
def corte(sic):
    s3, s2 = str(sic)[:3], str(sic)[:2]
    if s3 in CORTES and CORTES[s3]['n'] >= 10: return CORTES[s3]['corte'], s3
    if s2 in CORTES: return CORTES[s2]['corte'], s2
    return CORTES['todas']['corte'], 'todas'

# ---------- la SEC ----------
def empresas_cotizan():
    tx = json.loads(get('https://www.sec.gov/files/company_tickers_exchange.json'))
    out = {}
    for cik, nom, t, ex in tx['data']:
        if ex in ('NYSE', 'Nasdaq') and cik not in out: out[cik] = (t, nom)
    return out
def informes_nuevos(desde_dia, leidos):
    """10-K originales presentados desde 'desde_dia' (índices diarios) y hoy (feed en vivo)."""
    acc = {}
    d = dt.date.fromisoformat(desde_dia); hoy = ahora().date()
    while d < hoy:
        if d.weekday() < 5:
            q = (d.month - 1) // 3 + 1
            b = get(f'https://www.sec.gov/Archives/edgar/daily-index/{d.year}/QTR{q}/form.{d:%Y%m%d}.idx')
            for l in (b or b'').decode('latin1').splitlines():
                if l.startswith('10-K ') and not l.startswith('10-K/'):
                    p = l.split(); a = p[-1].split('/')[-1].replace('.txt', '')
                    acc[a] = (int(p[-3]), d.isoformat())
        d += dt.timedelta(days=1)
    for pag in range(0, 1000, 100):
        b = get(f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=10-K&company=&dateb=&owner=include&start={pag}&count=100&output=atom')
        if not b: break
        ents = re.findall(rb'<entry>(.*?)</entry>', b, re.S)
        for e in ents:
            if re.search(rb'<category[^>]*term="10-K"', e):
                m = re.search(rb'accession-number=([\d\-]+)', e) or re.search(rb'/(\d{10}-\d{2}-\d{6})-index', e)
                c = re.search(rb'/data/(\d+)/', e)
                if m and c: acc[m.group(1).decode()] = (int(c.group(1)), hoy.isoformat())
        if len(ents) < 100: break
    return {a: v for a, v in acc.items() if a not in leidos}
def documento(cik, acc):
    s = json.loads(get(f'https://data.sec.gov/submissions/CIK{cik:010d}.json') or b'{}')
    r = s.get('filings', {}).get('recent', {})
    for a, doc, f in zip(r.get('accessionNumber', []), r.get('primaryDocument', []), r.get('form', [])):
        if a == acc and f == '10-K':
            return f'https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace("-", "")}/{doc}', s.get('sic')
    return None, s.get('sic')

# ---------- precios (Yahoo, ajustados por dividendos) ----------
PRE = {}
def serie(t):
    if t in PRE: return PRE[t]
    j = json.loads(get(f'https://query1.finance.yahoo.com/v8/finance/chart/{t.replace(".", "-")}?range=5y&interval=1d&events=div,splits', 0.3, UA_PRECIOS) or b'{}')
    try:
        x = j['chart']['result'][0]; adj = x['indicators']['adjclose'][0]['adjclose']; cl = x['indicators']['quote'][0]['close']
        off = x['meta']['gmtoffset']
        s = {dt.datetime.fromtimestamp(ts + off, dt.timezone.utc).date().isoformat(): (a, c) for ts, a, c in zip(x['timestamp'], adj, cl) if a and c}
    except Exception: s = {}
    PRE[t] = s; return s
def cierre_despues(t, momento):
    """Primer cierre (16:00 Nueva York ≈ 21:00 UTC) posterior a 'momento'. Devuelve (fecha, ajustado, cierre) o None."""
    for f in sorted(serie(t)):
        if dt.datetime.fromisoformat(f + 'T21:00:00+00:00') > momento: return (f,) + serie(t)[f]
    return None
def ajustado_en(t, f):
    s = serie(t); fs = [x for x in sorted(s) if x <= f]
    return s[fs[-1]][0] if fs else None

# ---------- estado ----------
EF = os.path.join(R, 'estado.json'); OF = os.path.join(R, 'operaciones.jsonl'); VF = os.path.join(R, 'valor.csv'); LF = os.path.join(R, 'lecturas.jsonl')
def cargar():
    if os.path.exists(EF): return json.load(open(EF, encoding='utf-8'))
    return {'inicio': None, 'spy': None, 'pos': {}, 'pendientes': [{'lado': 'arranque', 'decidido': ahora().isoformat()}],
            'leidos': [], 'desde_dia': ahora().date().isoformat(), 'sin_precio': {}}
def anotar(f, d): open(f, 'a', encoding='utf-8').write(json.dumps(d, ensure_ascii=False) + '\n')
def valor_pos(t, p, f):
    a = ajustado_en(t, f); return p['monto'] * a / p['aj_compra'] if a else p['monto']
def valor_total(E, f):
    v = valor_pos('SPY', E['spy'], f) if E['spy'] else 0
    return v + sum(valor_pos(t, p, f) for t, p in E['pos'].items())

def ejecutar(E):
    quedan = []
    for o in E['pendientes']:
        mom = dt.datetime.fromisoformat(o['decidido'])
        if o['lado'] == 'arranque':
            c = cierre_despues('SPY', mom)
            if not c: quedan.append(o); continue
            E['spy'] = {'monto': CAPITAL * (1 - COSTO_SPY), 'aj_compra': c[1], 'fecha': c[0]}; E['inicio'] = c[0]
            anotar(OF, {'fecha': c[0], 'lado': 'compra', 'ticker': 'SPY', 'precio': round(c[2], 4), 'monto': CAPITAL, 'motivo': 'arranque: todo al mercado'}); continue
        t = o['ticker']; c = cierre_despues(t, mom); cs = cierre_despues('SPY', mom)
        if not c or not cs or cs[0] != c[0]: quedan.append(o); continue
        f = c[0]; spy = valor_pos('SPY', E['spy'], f)
        if o['lado'] == 'compra' and t not in E['pos']:
            monto = min(valor_total(E, f) / N_POS, spy)
            if monto < 1: continue
            E['spy']['monto'] *= (spy - monto) / spy                       # vende SPY
            neto = monto * (1 - COSTO_SPY) * (1 - COSTO)
            E['pos'][t] = {'id': o['id'], 'monto': neto, 'aj_compra': c[1], 'fecha': f}
            anotar(OF, {'fecha': f, 'lado': 'compra', 'ticker': t, 'nombre': o.get('nombre'), 'precio': round(c[2], 4), 'monto': round(monto, 2), 'motivo': o['motivo']})
        elif o['lado'] == 'venta' and t in E['pos']:
            v = valor_pos(t, E['pos'][t], f); neto = v * (1 - COSTO) * (1 - COSTO_SPY)
            E['spy']['monto'] *= (spy + neto) / spy if spy > 0 else 1
            anotar(OF, {'fecha': f, 'lado': 'venta', 'ticker': t, 'nombre': o.get('nombre'), 'precio': round(c[2], 4), 'monto': round(v, 2),
                        'resultado': round(v / (E['pos'][t]['monto']) - 1, 4), 'motivo': o['motivo']})
            del E['pos'][t]
    E['pendientes'] = quedan

def deslistadas(E):
    """Rule 7: sin precio 10 días hábiles seguidos -> se vende al último precio conocido."""
    hoy = max(serie('SPY')) if serie('SPY') else None
    if not hoy: return
    for t in list(E['pos']):
        s = serie(t); ult = max(s) if s else None
        dias = sum(1 for f in serie('SPY') if ult is None or f > ult)
        if dias >= 10:
            v = valor_pos(t, E['pos'][t], ult or hoy) * (1 - COSTO); spy = valor_pos('SPY', E['spy'], hoy)
            E['spy']['monto'] *= (spy + v) / spy
            anotar(OF, {'fecha': hoy, 'lado': 'venta', 'ticker': t, 'monto': round(v, 2), 'motivo': f'dejó de cotizar (último precio {ult})'}); del E['pos'][t]

def control():
    import csv
    for r in csv.DictReader(open(os.path.join(R, 'control.csv'))):
        cik = int(r['cik']); s = json.loads(get(f'https://data.sec.gov/submissions/CIK{cik:010d}.json'))['filings']['recent']
        ks = [i for i, (f, d) in enumerate(zip(s['form'], s['filingDate'])) if f == '10-K' and d.startswith('2026')]; k = ks[-1]
        b = get(f'https://www.sec.gov/Archives/edgar/data/{cik}/{s["accessionNumber"][k].replace("-", "")}/{s["primaryDocument"][k]}')
        txt = negocio(b, f'{cik}_2026', s['filingDate'][k]) if b else ''; p = puntaje(txt) if len(txt.split()) >= 300 else None
        l = f'{ahora():%Y-%m-%d %H:%M} CONTROL v5 cik {cik}: al armar Tr v5 {float(r["pal"]):+.4f} | Rt {p if p is None else round(p, 4)}'
        print(l, flush=True); open(os.path.join(R, 'control.log'), 'a', encoding='utf-8').write(l + chr(10))

def correr():
    E = cargar()
    nuevos = informes_nuevos(E['desde_dia'], set(E['leidos']))
    cot = empresas_cotizan() if nuevos else {}
    print(f'{ahora():%Y-%m-%d %H:%M} UTC: 10-K nuevos sin leer {len(nuevos)}', flush=True)
    cortado = False
    for acc, (cik, dia) in sorted(nuevos.items(), key=lambda x: x[1][1]):
        if time.time() - T0 > LIMITE_SEG: cortado = True; print('se acabó el tiempo de esta corrida; sigue en la próxima', flush=True); break
        E['leidos'].append(acc)
        if cik not in cot: continue                                       # no cotiza en NYSE/Nasdaq
        t, nom = cot[cik]; u, sic = documento(cik, acc)
        if not u or not sic or str(sic) == '0000': continue
        b = get(u, 0.2); txt = negocio(b, f'{cik}_{acc}', dia) if b else ''
        if len(txt.split()) < 300: anotar(LF, {'fecha': dia, 'ticker': t, 'acc': acc, 'lectura': 'sin descripción del negocio'}); continue
        p = puntaje(txt); c, grupo = corte(sic); arriba = p > c
        motivo = f'Palabras {p:+.3f} contra el corte {c:+.3f} de su industria (SIC {grupo})'
        anotar(LF, {'fecha': dia, 'ticker': t, 'nombre': nom, 'acc': acc, 'puntaje': round(p, 4), 'corte': c, 'grupo': grupo, 'arriba': arriba})
        print(f'  {t:6s} {motivo} -> {"ARRIBA" if arriba else "abajo"}', flush=True)
        if arriba and t not in E['pos']: E['pendientes'].append({'lado': 'compra', 'ticker': t, 'id': h(cik), 'nombre': nom, 'motivo': motivo, 'decidido': ahora().isoformat()})
        if not arriba and t in E['pos']: E['pendientes'].append({'lado': 'venta', 'ticker': t, 'nombre': nom, 'motivo': 'nuevo 10-K: ' + motivo, 'decidido': ahora().isoformat()})
    if not cortado: E['desde_dia'] = (ahora().date() - dt.timedelta(days=1)).isoformat()   # ayer otra vez: su índice sale a la noche
    E['leidos'] = E['leidos'][-20000:]
    ejecutar(E)
    if E['spy']:
        deslistadas(E)
        f = max(serie('SPY')); v = valor_total(E, f)
        filas = open(VF, encoding='utf-8').read().splitlines() if os.path.exists(VF) else ['fecha,valor,spy_solo,empresas']
        spy_solo = CAPITAL * (1 - COSTO_SPY) * ajustado_en('SPY', f) / ajustado_en('SPY', E['inicio'])
        nueva = f'{f},{v:.2f},{spy_solo:.2f},{len(E["pos"])}'
        filas = [x for x in filas if not x.startswith(f + ',')] + [nueva]
        open(VF, 'w', encoding='utf-8').write('\n'.join(filas) + '\n')
        print(f'VALOR {f}: Rt {v:.2f} | sólo SPY {spy_solo:.2f} | empresas {len(E["pos"])} | pendientes {len(E["pendientes"])}', flush=True)
    json.dump(E, open(EF, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

if __name__ == '__main__':
    control() if sys.argv[1:] == ['control'] else correr()
