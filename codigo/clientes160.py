"""#160: concentración de clientes en la sección 1. python clientes160.py bajar | medir. Reglas en notas/11 (#160)."""
import os, sys, json, re, time, urllib.request
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; OUT = f'{B}/fuentes/clientes160'; os.makedirs(OUT, exist_ok=True)
ORA = re.compile(r'(?<=[.;])\s+')
PCT = re.compile(r'(\d{1,3}(?:\.\d+)?)\s?(?:%|percent)\s+of\s+(?:[a-z\'’]+\s+){0,4}?(?:revenues?|sales)\b')
CLI = re.compile(r'\b(customers?|clients?|distributors?|accounted for)\b')
def conc(t):
    t = (t or '').lower(); n = len(t.split()); m = 0.0
    if n < 300: return n, None
    for o in ORA.split(t):
        if len(o) > 2000 or not CLI.search(o): continue
        for p in PCT.findall(o):
            v = float(p)
            if 10 <= v <= 100: m = max(m, v)
    return n, m
if sys.argv[1] == 'bajar':
    from concurrent.futures import ThreadPoolExecutor
    def anio(y):
        out = f'{OUT}/c_{y}.jsonl'
        if os.path.exists(out): return
        R = []
        for parte in ('train', 'validate', 'test'):
            u = f'https://huggingface.co/datasets/eloukas/edgar-corpus/resolve/main/{y}/{parte}.jsonl'
            for k in range(5):
                try:
                    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'inteligencia-economica research'}), timeout=120); loc = []
                    for l in r:
                        d = json.loads(l); n, m = conc(d.get('section_1')); loc.append({'cik': d['cik'], 'n': n, 'c': m})
                    R += loc; break
                except Exception as e:
                    print('reintento', y, parte, e, flush=True); time.sleep(20)
        with open(out + '.tmp', 'w') as f:
            for x in R: f.write(json.dumps(x) + '\n')
        os.replace(out + '.tmp', out); print(y, len(R), flush=True)
    with ThreadPoolExecutor(4) as ex: list(ex.map(anio, range(2010, 2021)))
    for y in ('2021', '2022'):
        with open(f'{OUT}/c_{y}.jsonl', 'w') as f:
            for l in open(f'{B}/fuentes/crawler145/sec1.jsonl', encoding='utf-8'):
                o = json.loads(l); n, m = conc(o.get(y)); f.write(json.dumps({'cik': o['cik'], 'n': n, 'c': m}) + '\n')
    print('LISTO', flush=True)
