"""Suma a filas.csv la franqueza (franq-*.csv). Cruce: misma empresa y año en que se PRESENTÓ el 10-K.
Uso: python unir_texto.py filas.csv texto-a.csv,texto-b.csv,..."""
import sys
import pandas as pd
df = pd.read_csv(sys.argv[1], low_memory=False)
# Cada TIPO de archivo (palabras / IA) se junta por separado: si se mezclan, sacar duplicados borra uno de los dos.
grupos = {}
for x in sys.argv[2].split(','):
    if x:
        t = pd.read_csv(x)
        t = t[['id', 'anio_presentado'] + sorted(c for c in t.columns if c.startswith('franq_'))]   # nunca el CIK
        grupos.setdefault(tuple(t.columns), []).append(t)
tx = None
for cols, ts in grupos.items():
    g = pd.concat(ts).drop_duplicates(['id', 'anio_presentado'])
    tx = g if tx is None else tx.merge(g, on=['id', 'anio_presentado'], how='outer')
df['anio_presentado'] = pd.to_numeric(df['_presentado'].astype(str).str[:4], errors='coerce')
df = df.drop(columns=[c for c in df.columns if c.startswith('franq_')]).merge(tx, on=['id', 'anio_presentado'], how='left')
df = df.drop(columns=['anio_presentado'])
n = int(df['franq_numeros'].notna().sum())
print('FRANQUEZA filas con dato:', n, 'por año:', df[df.franq_numeros.notna()].groupby('anio').size().to_dict(), flush=True)
if n == 0:
    print('FALLA: no cruzó ninguna franqueza'); sys.exit(2)
df.to_csv(sys.argv[1], index=False)
