"""Cuánto habla cada empresa, en «el negocio» (sección 1 del 10-K), de cada tema de la élite (#62, notas/11).
Fuente: EDGAR-CORPUS (Hugging Face). Uso: python temas_10k.py AÑO [LIMITE]
Salida: tema10k-AÑO.csv  id, anio_presentado, palabras, y una columna por tema (cantidad de coincidencias)."""
import sys, re, json, time, hashlib
from texto import lineas, cargar, h
from agenda import TEMAS
from davos2 import CAT
PAT = {('b_' + k): re.compile(p) for k, (p, _) in TEMAS.items()}
PAT.update({('t_' + k): re.compile(p) for k, (p, _) in CAT.items()})
if __name__ == '__main__':
    anio = int(sys.argv[1]); t0 = time.time(); vistos = set(); n = 0
    with open(f'tema10k-{anio}.csv', 'w') as fh:
        fh.write(','.join(['id', 'anio_presentado', 'palabras'] + list(PAT)) + '\n')
        for l in lineas(anio):
            try:
                d = cargar(l)
            except Exception:
                continue
            c = str(d.get('cik', '')).strip()
            if not c or c in vistos:
                continue
            vistos.add(c)
            t = (d.get('section_1') or '').lower()
            if len(t) < 500:
                continue
            fh.write(','.join([h(c), str(anio), str(len(t.split()))] + [str(len(p.findall(t))) for p in PAT.values()]) + '\n'); n += 1
    print(f'LISTO {anio}: {n} empresas ({time.time() - t0:.0f}s)', flush=True)
