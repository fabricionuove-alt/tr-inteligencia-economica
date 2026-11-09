"""#87 hacia adelante: secciones 1A (riesgos) y 7 (dirección) de los 10-K de un año, sólo QUIERO, 6 pedidos a la vez.
Uso: python sec_textos3.py AÑO quiero.txt submissions.zip SUF -> textos1A-AÑO-SUF.jsonl, textos7-AÑO-SUF.jsonl
El texto guardado ya viene sin los primeros 1.500 caracteres (igual que SALTO=1500 en el pasado)."""
import sys, json, time, re
from concurrent.futures import ThreadPoolExecutor
from bajar_10k import candidatos, get, a_texto, h
S = r'\s*[\.\:\-–—]?\s*'
SEC = {'1A': (re.compile(r'(?i)item\s*1a' + S + r'risk\s+factors'), re.compile(r'(?i)item\s*(?:1b' + S + r'unresolved|1c' + S + r'cyber|2' + S + r'(?:description\s+of\s+)?propert)')),
       '7': (re.compile(r'(?i)item\s*7' + S + r'management.{0,3}s\s+discussion'), re.compile(r'(?i)item\s*(?:7a' + S + r'quantitative|8' + S + r'financial\s+statements)'))}
def tramo(t, ini, fin):
    mejor = ''
    for m in ini.finditer(t):
        f = fin.search(t, m.end()); x = t[m.end(): f.start() if f else min(len(t), m.end() + 400000)]
        if len(x) > len(mejor): mejor = x
    return re.sub(r'\s+', ' ', mejor).strip()
A, Q, SUBS, SUF = int(sys.argv[1]), set(open(sys.argv[2]).read().split()), sys.argv[3], sys.argv[4]
t0 = time.time(); cand = [c for c in candidatos(SUBS, [A])[A] if h(c[0]) in Q]
print(f'{A}: {len(cand)} 10-K a bajar ({time.time() - t0:.0f}s)', flush=True)
def uno(c):
    cik, acc, doc = c
    b = get(f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-", "")}/{doc}', 0.6)
    if not b: return {}
    t = a_texto(b); o = {}
    for s, (i, f) in SEC.items():
        x = tramo(t, i, f)
        if len(x) >= 500 + 1500: o[s] = json.dumps({'id': h(cik), 'anio_presentado': A, 'texto': x[1500:13500]})
    return o
n = {'1A': 0, '7': 0}
fh = {s: open(f'textos{s}-{A}-{SUF}.jsonl', 'w', encoding='utf-8') for s in SEC}
with ThreadPoolExecutor(6) as ex:
    for k, o in enumerate(ex.map(uno, cand)):
        for s, r in o.items(): fh[s].write(r + '\n'); n[s] += 1
        if k % 300 == 0: print(f'  {k}/{len(cand)} {n} ({time.time() - t0:.0f}s)', flush=True)
print(f'LISTO {A}-{SUF}: {n} ({time.time() - t0:.0f}s)', flush=True)
