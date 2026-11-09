"""#101: qué empresas nombran los cables diplomáticos de EE.UU. (Cablegate), y cuáles en cables de empuje comercial (BEXP).
Salidas: menciones.csv (id, anio, mes, bexp, cables) y nombres.csv (núcleo del nombre, id, cables totales, cables BEXP) para revisar a ojo."""
import re, io, json, time, hashlib, collections, urllib.request, subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'pyahocorasick', 'wordfreq'], check=False)
import ahocorasick
from wordfreq import zipf_frequency
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]   # mismo id que mercado.py
def get(u):
    for i in range(5):
        try:
            time.sleep(0.15); return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120).read()
        except Exception as e:
            print('reintento', u[-50:], type(e).__name__, flush=True); time.sleep(3 + 3 * i)
t0 = time.time()
# 1. nombres de las empresas con 10-K en 2005-2010
nom = {}
for a in range(2005, 2011):
    for q in range(1, 5):
        b = get(f'https://www.sec.gov/Archives/edgar/full-index/{a}/QTR{q}/company.idx')
        if not b: continue
        for l in b.decode('latin1').splitlines()[10:]:
            if l[62:74].strip() in ('10-K', '10-K405', '10-KSB'):
                nom[l[74:86].strip()] = l[:62].strip()
print('empresas con 10-K', len(nom), f'{time.time() - t0:.0f}s', flush=True)
SUF = {'INC', 'CORP', 'CORPORATION', 'CO', 'COMPANY', 'LTD', 'LIMITED', 'PLC', 'LLC', 'LP', 'L', 'P', 'HOLDINGS', 'HOLDING', 'GROUP', 'THE', 'NV', 'N', 'V', 'SA', 'AG', 'INCORPORATED', 'CORPORATIONS', 'COS', 'TRUST', 'DE', 'NEW'}
def nucleo(n):
    n = re.sub(r'/[A-Z]{2,3}/?', ' ', n.upper()); n = re.sub(r'[^A-Z0-9 ]', ' ', n.replace('&', ' AND ')); w = n.split()
    while w and w[0] == 'THE': w = w[1:]
    while w and w[-1] in SUF: w = w[:-1]
    return ' '.join(w)
cuenta = collections.Counter(); por = {}
for cik, n in nom.items():
    c = nucleo(n)
    if len(c.replace(' ', '')) < 5: continue
    if ' ' not in c and zipf_frequency(c.lower(), 'en') >= 4.0: continue
    cuenta[c] += 1; por[c] = cik
nucleos = {c: por[c] for c in cuenta if cuenta[c] == 1}
A = ahocorasick.Automaton()
for c, cik in nucleos.items(): A.add_word(' ' + c + ' ', (c, cik))
A.make_automaton(); print('nombres buscables', len(nucleos), flush=True)
# 2. recorrer los cables (jsonl público de Hugging Face), 2005-01 a 2010-02
U = 'https://huggingface.co/datasets/fn5/wikileaks-cables/resolve/main/cables_parsed.jsonl'
men = collections.Counter(); tot = collections.Counter(); bex = collections.Counter(); n = nb = 0
r = urllib.request.urlopen(urllib.request.Request(U, headers=UA), timeout=600)
for k, l in enumerate(io.TextIOWrapper(r, encoding='utf-8', errors='ignore')):
    try: x = json.loads(l)
    except Exception: continue
    m = re.match(r'(\d+)/(\d+)/(\d{4})', x.get('datetime') or '')
    if not m: continue
    a, me = int(m.group(3)), int(m.group(1))
    if a < 2005 or a > 2010: continue
    b = x.get('body') or ''; t = re.search(r'TAGS:?([^\n]*)', b); tags = set(re.findall(r'[A-Z]{4}', t.group(1).upper())) if t else set()
    eb = int('BEXP' in tags); n += 1; nb += eb
    txt = ' ' + re.sub(r'[^A-Z0-9 ]', ' ', b.upper().replace('&', ' AND ')) + ' '; txt = re.sub(r' +', ' ', txt)
    vis = {v for _, v in A.iter(txt)}
    for c, cik in vis:
        men[(h(cik), a, me, eb)] += 1; tot[c] += 1; bex[c] += eb
    if k % 20000 == 0: print(f'  línea {k}, cables 2005-2010 {n} (BEXP {nb}) {time.time() - t0:.0f}s', flush=True)
print('CABLES 2005-2010', n, 'BEXP', nb, f'{time.time() - t0:.0f}s', flush=True)
with open('menciones.csv', 'w') as f:
    f.write('id,anio,mes,bexp,cables\n')
    for (i, a, me, eb), v in men.items(): f.write(f'{i},{a},{me},{eb},{v}\n')
with open('nombres.csv', 'w') as f:
    f.write('nucleo,id,cables,bexp\n')
    for c, v in tot.most_common(): f.write(f'"{c}",{h(nucleos[c])},{v},{bex[c]}\n')
print('LISTO', len(men), 'filas', len(tot), 'empresas nombradas', flush=True)
for c, v in tot.most_common(40): print('  ', c, v, bex[c])
