"""Temas de la élite en «el negocio» (Item 1) de los 10-K bajados directo de la SEC (para los años sin EDGAR-CORPUS).
Uso: python tema_10k_sec.py AÑO N DESDE submissions.zip   (al azar con semilla 7; tramo DESDE..DESDE+N para repartir)
Salida: tema10k-AÑO-DESDE.csv, mismas columnas que temas_10k.py."""
import sys, re, random, time
from bajar_10k import candidatos, get, a_texto, h
from temas_10k import PAT
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
if __name__ == '__main__':
    A, N, D, SUBS = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    t0 = time.time(); cand = candidatos(SUBS, [A])[A]
    random.Random(7).shuffle(cand); lista = cand[D:D + N]
    print(f'{A}: {len(cand)} 10-K, tramo {D}-{D + len(lista)} ({time.time() - t0:.0f}s)', flush=True)
    fh = open(f'tema10k-{A}-{D}.csv', 'w'); fh.write(','.join(['id', 'anio_presentado', 'palabras'] + list(PAT)) + '\n')
    ok = 0
    for k, (cik, acc, doc) in enumerate(lista):
        b = get(f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-", "")}/{doc}', 0.11)
        if not b: continue
        t = item1(a_texto(b)).lower()
        if len(t) < 500: continue
        fh.write(','.join([h(cik), str(A), str(len(t.split()))] + [str(len(p.findall(t))) for p in PAT.values()]) + '\n'); fh.flush(); ok += 1
        if k % 200 == 0: print(f'  {k + 1}/{len(lista)} con Item 1: {ok} ({time.time() - t0:.0f}s)', flush=True)
    print(f'LISTO {A}-{D}: {ok} empresas ({time.time() - t0:.0f}s)', flush=True)
