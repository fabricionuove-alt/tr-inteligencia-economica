"""Suma a filas.csv el parecido de texto (texto-*.csv). Cruce: misma empresa y año en que se PRESENTÓ el 10-K.
Uso: python unir_texto.py filas.csv texto-a.csv,texto-b.csv,..."""
import sys
import pandas as pd
df = pd.read_csv(sys.argv[1], low_memory=False)
tx = pd.concat([pd.read_csv(x) for x in sys.argv[2].split(',') if x]).drop_duplicates(['id', 'anio_presentado'])
df['anio_presentado'] = pd.to_numeric(df['_presentado'].astype(str).str[:4], errors='coerce')
df = df.drop(columns=[c for c in df.columns if c.startswith('texto_igual_')]).merge(tx, on=['id', 'anio_presentado'], how='left')
df = df.drop(columns=['anio_presentado'])
n = int(df['texto_igual_total'].notna().sum())
print('TEXTO filas con dato:', n, 'por año:', df[df.texto_igual_total.notna()].groupby('anio').size().to_dict(), flush=True)
if n == 0:
    print('FALLA: no cruzó ningún texto'); sys.exit(2)
df.to_csv(sys.argv[1], index=False)
