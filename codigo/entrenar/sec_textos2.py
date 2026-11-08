"""Texto de «el negocio» (Item 1) de los 10-K de un año, sólo de las empresas en QUIERO, con 6 pedidos a la vez (SEC: ≤ 10 por segundo).
Uso: python sec_textos2.py AÑO quiero.txt submissions.zip -> textos-AÑO.jsonl"""
import sys, json, time
from concurrent.futures import ThreadPoolExecutor
from bajar_10k import candidatos, get, a_texto, h
import re
INI = re.compile(r'(?i)item\s*1\s*[\.\:\-–—]?\s*business\b')
FIN = re.compile(r'(?i)item\s*(?:1a\s*[\.\:\-–—]?\s*risk\s+factors|2\s*[\.\:\-–—]?\s*(?:description\s+of\s+)?propert)')
def item1(t):
    mejor = ''
    for m in INI.finditer(t):
        f = FIN.search(t, m.end())
        tramo = t[m.end(): f.start() if f else min(len(t), m.end() + 300000)]
        if len(tramo) > len(mejor):
            mejor = tramo
    return mejor
A, Q, SUBS = int(sys.argv[1]), set(open(sys.argv[2]).read().split()), sys.argv[3]
t0 = time.time(); cand = [c for c in candidatos(SUBS, [A])[A] if h(c[0]) in Q]
print(f'{A}: {len(cand)} 10-K a bajar ({time.time() - t0:.0f}s)', flush=True)
def uno(c):
    cik, acc, doc = c
    b = get(f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-", "")}/{doc}', 0.6)
    if not b: return None
    t = item1(a_texto(b)).strip()
    return json.dumps({'id': h(cik), 'anio_presentado': A, 'texto': t[:4000]}) if len(t) >= 500 else None
ok = 0
with open(f'textos-{A}.jsonl', 'w', encoding='utf-8') as fh, ThreadPoolExecutor(6) as ex:
    for k, r in enumerate(ex.map(uno, cand)):
        if r: fh.write(r + '\n'); ok += 1
        if k % 500 == 0: print(f'  {k}/{len(cand)} con texto {ok} ({time.time() - t0:.0f}s)', flush=True)
print(f'LISTO {A}: {ok} textos ({time.time() - t0:.0f}s)', flush=True)
