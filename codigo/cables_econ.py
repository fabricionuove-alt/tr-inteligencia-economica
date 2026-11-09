"""Pasos 2 y 4 de la noche WikiLeaks: guarda los cables económicos 2004-2010 (asunto + primeros 4.000 caracteres) y los pedidos de Washington a las embajadas.
Salidas: econ.jsonl, pedidos.jsonl, conteo.csv (etiqueta x mes)."""
import io, re, json, time, collections, urllib.request
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
EC = {'ECON', 'ETRD', 'EINV', 'BEXP', 'EPET', 'ENRG', 'EAIR', 'ECPS', 'EFIN', 'EAGR', 'EIND', 'EMIN', 'ELTN', 'EWWT', 'TSPA', 'TNGD', 'KIPR', 'ELAB', 'EFIS', 'TRGY'}
U = 'https://huggingface.co/datasets/fn5/wikileaks-cables/resolve/main/cables_parsed.jsonl'
t0 = time.time(); r = urllib.request.urlopen(urllib.request.Request(U, headers=UA), timeout=600)
fe, fp = open('econ.jsonl', 'w', encoding='utf-8'), open('pedidos.jsonl', 'w', encoding='utf-8'); cnt = collections.Counter(); ne = np_ = 0
for k, l in enumerate(io.TextIOWrapper(r, encoding='utf-8', errors='ignore')):
    try: x = json.loads(l)
    except Exception: continue
    m = re.match(r'(\d+)/(\d+)/(\d{4})', x.get('datetime') or '')
    if not m or not (2004 <= int(m.group(3)) <= 2010): continue
    b = x.get('body') or ''; t = re.search(r'TAGS:?([^\n]*)', b); tags = set(re.findall(r'[A-Z]{4}', t.group(1).upper())) if t else set()
    ym = f'{m.group(3)}{int(m.group(1)):02d}'
    for g in tags: cnt[(g, ym)] += 1
    i = b.find('SUBJECT'); cu = re.sub(r'\s+', ' ', b[i:] if i >= 0 else b)
    d = {'cable_id': x.get('cable_id'), 'ym': ym, 'origin': x.get('origin'), 'clas': x.get('classification'), 'tags': sorted(tags), 'texto': cu[:4000]}
    if tags & EC: fe.write(json.dumps(d) + '\n'); ne += 1
    if (x.get('origin') or '').startswith('Secretary of State') and (tags & EC) and re.search(r'REQUEST|TASKER|ACTION|INFORMATION ON|PLEASE', cu[:600]): fp.write(json.dumps(d) + '\n'); np_ += 1
    if k % 50000 == 0: print(f'  {k} líneas, económicos {ne}, pedidos {np_} {time.time() - t0:.0f}s', flush=True)
with open('conteo.csv', 'w') as f:
    f.write('tag,ym,n\n')
    for (g, ym), v in cnt.items(): f.write(f'{g},{ym},{v}\n')
print('LISTO económicos', ne, 'pedidos', np_, f'{time.time() - t0:.0f}s', flush=True)
