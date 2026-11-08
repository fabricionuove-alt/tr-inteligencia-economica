"""Resultados por empresa-año para cruzar con los conceptos de Gemma. Uso: python etiquetas.py filas.csv sic.csv etiquetas.csv"""
import sys, pandas as pd
df = pd.read_csv(sys.argv[1], usecols=lambda c: c in ('id', 'anio', 'sector', 'log_activos', '_presentado', '_ret1', '_ret4', '_ret6', 'estado_final'), dtype={'id': str}, low_memory=False)
df['anio_presentado'] = pd.to_numeric(df['_presentado'].astype(str).str[:4], errors='coerce')
df['tam'] = pd.to_numeric(df['log_activos'], errors='coerce').groupby(df['anio']).rank(pct=True).round(4)
sic = pd.read_csv(sys.argv[2], dtype={'id': str, 'sic': str}).drop_duplicates('id')
df = df.merge(sic, on='id', how='left')
df[['id', 'anio', 'anio_presentado', 'sector', 'sic', 'tam', '_ret1', '_ret4', '_ret6', 'estado_final']].to_csv(sys.argv[3], index=False)
print('ETIQUETAS', len(df))
