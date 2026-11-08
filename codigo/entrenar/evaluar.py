"""Puntúa una empresa con los modelos entrenados y las reglas de los cinco.
Uso: python evaluar.py TICKER [carpeta_modelos]
El símbolo sólo sirve para bajar los datos de la SEC; al modelo le llegan ratios en percentil, sin nombre ni fecha."""
import sys, os, json, urllib.request, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import joblib, numpy as np, pandas as pd
import construir as K
from reglas_de_los_cinco import REGLAS

UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
bajar = lambda u: json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())

tk = sys.argv[1].upper()
dm = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modelos')
tabla = bajar('https://www.sec.gov/files/company_tickers.json')
cik = next((str(v['cik_str']).zfill(10) for v in tabla.values() if v['ticker'] == tk), None)
if not cik:
    sys.exit(f'No encuentro {tk} en la SEC (sólo empresas que presentan en EE.UU.)')
facts = bajar(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json')
subs = bajar(f'https://data.sec.gov/submissions/CIK{cik}.json')
f, _ = K.anuales(facts)
t = max(a for a in f if 'activos' in f[a] and 'ventas' in f[a])
r = K.rasgos(f, t)
sic = str(subs.get('sic') or '0')
r['sector'] = float(sic[:1]); r['financiera'] = 1.0 if sic[:2] in [str(x) for x in range(60, 68)] else 0.0

ref = json.load(open(os.path.join(dm, 'referencia.json')))
def pct(c, v):
    q = ref['cuantiles'].get(c)
    if v is None or q is None:
        return None
    return bisect.bisect_left(q, v) / (len(q) - 1)
P = {c: pct(c, r.get(c)) for c in ref['cuantiles']}

print(f'\n{subs.get("name")} ({tk}) · último año fiscal con balance: {t} · comparada contra las empresas de {ref["anio_referencia"]}')
if r['financiera']:
    print('Ojo: es financiera (banco/aseguradora); los balances no se leen igual y el modelo es menos confiable.')
RES = json.load(open(os.path.join(os.path.dirname(dm), 'resultados.json')))
def observado(et, p):
    """En vez del número crudo del modelo: qué pasó en la prueba con empresas de puntaje parecido."""
    cal = RES.get(et, {}).get('calibracion')
    if not cal:
        return None
    c = min(cal, key=lambda c: abs(c['dice'] - p))
    return c['pasa']
print('\nPUNTAJES (en la prueba, de las empresas con un puntaje parecido, a cuántas les pasó)')
for et, txt in [('sobrevive_10', 'el accionista sigue vivo en 10 años (sin quiebra)'),
                ('sobrevive_10_amplio', 'sigue presentando balances en 10 años'),
                ('duplica_6', 'duplica su valor para el dueño en 6 años')]:
    p = os.path.join(dm, f'{et}.joblib')
    if not os.path.exists(p):
        continue
    m = joblib.load(p)
    x = pd.DataFrame([{c: (P.get(c) if c in P else r.get(c)) for c in m['rasgos']}]).astype(float).fillna(0.5)
    p = m['modelo'].predict_proba(x[m['rasgos']])[0, 1]
    o = observado(et, p)
    base = RES.get(et, {}).get('tasa_base_prueba')
    extra = f'   (media de todas: {base:.0%})' if base is not None else ''
    print(f'  {(o if o is not None else p):5.0%}  {txt}{extra}')

faltan = [c for c in ref['cuantiles'] if P.get(c) is None]
if faltan:
    print(f'  (faltan {len(faltan)} datos; el modelo los toma como "del medio": {", ".join(faltan)})')

# Reglas que la prueba mostró mal escritas (AUC por debajo de 0,5): se muestran aparte, no cuentan.
ROTAS = {'devengos': 'dio al revés: las que se mueren tienen pérdidas que hacen negativo el devengo',
         'deuda_neta_fco': 'no predice nada: con caja negativa el cociente no tiene sentido'}
print('\nREGLAS DE LOS CINCO (percentil contra el resto: arriba de 60 cumple, abajo de 40 no)')
for col, signo, quien in REGLAS:
    if col in ROTAS:
        continue
    v = P.get(col)
    if v is None:
        print(f'   ?   {quien}  (sin dato)'); continue
    bueno = v if signo > 0 else 1 - v
    marca = 'SÍ' if bueno >= 0.6 else ('NO' if bueno <= 0.4 else ' ~')
    print(f'  {marca:3s} {bueno*100:3.0f}  {quien}')
print('\nReglas que salieron mal escritas (no cuentan):')
for col, por_que in ROTAS.items():
    print(f'  - {col}: {por_que}')
print('\nLo que esto NO mira: el precio que pagás, los directivos, la cultura, el temperamento.')
