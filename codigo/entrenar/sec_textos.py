"""Texto de «el negocio» (Item 1) de los 10-K bajados de la SEC, para que Gemma los lea.
Uso: python sec_textos.py AÑO N DESDE submissions.zip  -> textos-AÑO-DESDE.jsonl ({"id", "anio_presentado", "texto"}, 4.000 caracteres)"""
import sys, json, random, time
from bajar_10k import candidatos, get, a_texto, h
from tema_10k_sec import item1
A, N, D, SUBS = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
t0 = time.time(); cand = candidatos(SUBS, [A])[A]; random.Random(7).shuffle(cand); lista = cand[D:D + N]
fh = open(f'textos-{A}-{D}.jsonl', 'w', encoding='utf-8'); ok = 0
for k, (cik, acc, doc) in enumerate(lista):
    b = get(f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-", "")}/{doc}', 0.11)
    if not b: continue
    t = item1(a_texto(b)).strip()
    if len(t) < 500: continue
    fh.write(json.dumps({'id': h(cik), 'anio_presentado': A, 'texto': t[:4000]}) + '\n'); fh.flush(); ok += 1
    if k % 200 == 0: print(f'  {k + 1}/{len(lista)} con texto {ok} ({time.time() - t0:.0f}s)', flush=True)
print(f'LISTO {A}-{D}: {ok} textos ({time.time() - t0:.0f}s)', flush=True)
