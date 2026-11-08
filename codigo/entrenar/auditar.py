"""Auditoría de etiquetas: sólo para revisar a mano, NUNCA entra al entrenamiento.
Recupera nombre y últimas presentaciones de una muestra de empresas por destino,
y cuenta cómo terminaron las "desconocidas" según su último formulario.
Uso: python auditar.py filas.csv subs.zip"""
import sys, json, zipfile, hashlib, random, collections, csv
import pandas as pd

df = pd.read_csv(sys.argv[1], usecols=['id', 'anio', 'estado_final'])
z = zipfile.ZipFile(sys.argv[2])
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik)).encode()).hexdigest()[:12]
ids = set(df['id'])
mapa = {}
for n in z.namelist():
    if n.startswith('CIK') and n.endswith('.json') and '-submissions-' not in n:
        k = h(n[3:13])
        if k in ids:
            mapa[k] = n
print('empresas mapeadas', len(mapa), 'de', len(ids), flush=True)

por = df.groupby('id').agg(estado=('estado_final', 'first'), ultimo_anio=('anio', 'max')).reset_index()
random.seed(7)
muestra = []
for estado, n in [('quiebra', 25), ('desconocido', 30), ('comprada', 15), ('vive', 10)]:
    ids_e = por[por.estado == estado]['id'].tolist()
    muestra += [(estado, i) for i in random.sample(ids_e, min(n, len(ids_e)))]

final_desc = collections.Counter()
for i in por[por.estado == 'desconocido']['id']:
    if i in mapa:
        s = json.loads(z.read(mapa[i]))
        forms = s['filings']['recent']['form']
        final_desc[forms[0] if forms else '-'] += 1   # el más reciente va primero

with open('auditoria.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['estado', 'id', 'cik', 'nombre', 'ultimo_anio_con_balance', 'ultimas_presentaciones'])
    for estado, i in muestra:
        if i not in mapa:
            continue
        s = json.loads(z.read(mapa[i]))
        r = s['filings']['recent']
        ult = [f"{d} {fo}{(' [' + it + ']') if it else ''}" for d, fo, it in
               list(zip(r['filingDate'], r['form'], r['items']))[:8]]
        w.writerow([estado, i, mapa[i][3:13], s.get('name'), int(por[por.id == i]['ultimo_anio'].iloc[0]), ' | '.join(ult)])

print('CÓMO TERMINARON LAS DESCONOCIDAS (último formulario):', final_desc.most_common(15), flush=True)
print('auditoria.csv listo', flush=True)
