"""¿El modelo capta el pensamiento real de los inversores? Cruza sus carteras con los puntajes.
Uso: python carteras.py puntajes_todos.csv carteras_13f.csv subs.zip
- Cada posición al 31-dic del año t se compara con el balance del año t-1 (lo que se sabía entonces).
- Puntajes de modelos entrenados sólo con 2012-2013 (o 2012-2016): fuera de muestra para años posteriores.
- Las empresas extranjeras (20-F / 40-F) no tienen estos balances y quedan afuera.
Pregunta A: ¿en qué percentil del universo caen sus elecciones? (50 = como cualquiera)
Pregunta B: ¿a sus elecciones les fue mejor que a la media de esos mismos años?"""
import sys, json, re, zipfile, hashlib, csv, collections
import numpy as np, pandas as pd

P = pd.read_csv(sys.argv[1])
C = pd.read_csv(sys.argv[2])
z = zipfile.ZipFile(sys.argv[3])

STOP = {'INC', 'CORP', 'CORPORATION', 'CO', 'COMPANY', 'LTD', 'LIMITED', 'NV', 'N', 'V', 'PLC', 'HLDGS', 'HOLDINGS',
        'HLDG', 'HOLDING', 'GROUP', 'GRP', 'THE', 'DEL', 'NEW', 'CL', 'A', 'B', 'SA', 'AG', 'LP', 'LLC', 'IN', 'I', 'MICH', 'DE'}
ABREV = {'AMER': 'AMERICA', 'MTRS': 'MOTORS', 'PPTYS': 'PROPERTIES', 'AIRLS': 'AIRLINES', 'INTL': 'INTERNATIONAL',
         'MANAGMT': 'MANAGEMENT', 'MGMT': 'MANAGEMENT', 'ACCEP': 'ACCEPTANCE', 'RESOUR': 'RESOURCES', 'TECH': 'TECHNOLOGIES',
         'SVCS': 'SERVICES', 'FINL': 'FINANCIAL', 'COS': 'COMPANIES', 'INDS': 'INDUSTRIES', 'MET': 'MET'}
STOP |= {'OF', 'AND'}
def norm(s):
    s = re.sub(r'&AMP;|&', ' AND ', str(s).upper())
    w = [ABREV.get(x, x) for x in re.sub(r'[^A-Z0-9 ]', ' ', s).split()]
    w = [x for x in w if x not in STOP]
    return ' '.join(w)

# índice de nombres (actuales y anteriores) -> CIK, sólo empresas que presentaron 10-K
idx = collections.defaultdict(set)
for n in z.namelist():
    if not (n.startswith('CIK') and n.endswith('.json') and '-submissions-' not in n):
        continue
    s = json.loads(z.read(n))
    for nm in [s.get('name')] + [f.get('name') for f in s.get('formerNames', [])]:
        if nm:
            idx[norm(nm)].add(n[3:13])
claves = list(idx)
def buscar(nombre):
    k = norm(nombre)
    if k in idx:
        return idx[k]
    c = [x for x in claves if x.startswith(k) or (len(k) >= 12 and k.startswith(x) and len(x) >= 8)]
    if len(c) == 1:
        return idx[c[0]]
    c = [x for x in claves if x.startswith(k[:max(12, len(k) - 2)])]
    return idx[c[0]] if len(c) == 1 else set()

h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik)).encode()).hexdigest()[:12]
ids_validos = set(P['id'])
mapa, sin = {}, []
for nm in sorted(set(C['nombre'])):
    cands = [h(c) for c in buscar(nm) if h(c) in ids_validos]
    if cands:
        mapa[nm] = cands[0]
    else:
        sin.append(nm)
print('MAPEADAS', len(mapa), 'de', len(set(C['nombre'])), flush=True)
print('  quedan afuera (extranjeras o sin balance):', sin, flush=True)
C['id'] = C['nombre'].map(mapa)
C = C.dropna(subset=['id'])
C['anio_balance'] = C['anio'] - 1          # lo que se sabía el 31-dic
picks = C[['inversor', 'id', 'anio_balance']].drop_duplicates()

# percentil de cada puntaje dentro de su año
cols = [c for c in P.columns if c.startswith('p_')] + ['cinco', 'piotroski_f']
for c in cols:
    P['pct_' + c] = P.groupby('anio')[c].rank(pct=True)
M = picks.merge(P, left_on=['id', 'anio_balance'], right_on=['id', 'anio'], how='inner')
res = {}
desde = {'p_sobrevive_10': 2014, 'p_sobrevive_10_amplio': 2014, 'p_duplica_6': 2014, 'p_gana_mas_1': 2017,
         'cinco': 2012, 'piotroski_f': 2012}
for q in sorted(M['inversor'].unique()):
    x = M[M.inversor == q]
    r = {'posiciones_empresa_anio': int(len(x)), 'empresas': int(x['id'].nunique())}
    print(f'\n== {q}: {len(x)} posiciones empresa-año, {x["id"].nunique()} empresas', flush=True)
    for c in cols:
        y = x[x.anio_balance >= desde.get(c, 2012)]['pct_' + c].dropna()
        if len(y) >= 3:
            r['A_' + c] = {'n': int(len(y)), 'mediana_percentil': float(y.median() * 100), 'mitad_de_arriba': float((y > 0.5).mean())}
            print(f'  A {c:24s} percentil mediano {y.median()*100:4.0f}  en la mitad de arriba {(y>0.5).mean():.0%}  (n={len(y)})', flush=True)
    for et in ['sobrevive_10', 'sobrevive_10_amplio', 'duplica_6', 'gana_mas_1']:
        y = x.dropna(subset=[et])
        if len(y) >= 3:
            base = P[P.anio.isin(y.anio_balance) & P[et].notna()].groupby('anio')[et].mean()
            base_ = float(np.mean([base.get(a, np.nan) for a in y.anio_balance]))
            r['B_' + et] = {'n': int(len(y)), 'tasa_elecciones': float(y[et].mean()), 'tasa_media_mismos_anios': base_}
            print(f'  B {et:24s} a sus elecciones les pasó {y[et].mean():.0%} vs media {base_:.0%}  (n={len(y)})', flush=True)
    res[q] = r
json.dump({'mapeo': mapa, 'afuera': sin, 'resultados': res}, open('carteras_resultados.json', 'w'), indent=1)
print('LISTO')
