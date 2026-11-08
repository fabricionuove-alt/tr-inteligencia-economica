"""#71: tenencias de los vehículos de dinastías en los 13F. Uso: python familias_13f.py DESDE HASTA CUSIP_CSVS -> fam13f-DESDE.csv (periodo, familia, id, acciones)"""
import sys, io, re, time, zipfile
import pandas as pd
from mejores_ideas import get, MES
DESDE, HASTA = int(sys.argv[1]), int(sys.argv[2])
CUS = pd.concat([pd.read_csv(x, dtype=str) for x in sys.argv[3].split(',') if x]); mapa = {(c, int(a)): i for c, a, i in zip(CUS['cusip'], CUS['anio'], CUS['id'])}
FAM = {'liechtenstein': r'\bLGT\b', 'rothschild': r'ROTHSCHILD', 'safra': r'SAFRA|SARASIN', 'pictet': r'PICTET', 'lombard_odier': r'LOMBARD ODIER',
       'mirabaud': r'MIRABAUD', 'phipps': r'BESSEMER', 'rockefeller': r'ROCKEFELLER', 'wallenberg': r'WALLENBERG|INVESTOR AB', 'agnelli': r'\bEXOR\b',
       'pritzker': r'PRITZKER', 'mellon': r'MELLON FAMILY|RICHARD KING MELLON|MELLON FOUNDATION', 'cargill': r'CARGILL|MACMILLAN', 'walton': r'WALTON ENTERPRISES|WALTON FAMILY', 'dupont': r'DU ?PONT FAMILY|CHRISTIANA'}
def periodo(f):
    d, m, a = f.split('-'); return f'{int(a):04d}{MES[m.upper()]:02d}'
def un_zip(b):
    z = zipfile.ZipFile(io.BytesIO(b)); pn = {n.rsplit('/', 1)[-1].upper(): n for n in z.namelist()}
    rd = lambda n, cols: pd.read_csv(z.open(pn[n.upper()]), sep='\t', dtype=str, usecols=cols, quoting=3, on_bad_lines='skip', encoding='latin1')
    sub = rd('SUBMISSION.tsv', ['ACCESSION_NUMBER', 'FILING_DATE', 'SUBMISSIONTYPE', 'CIK', 'PERIODOFREPORT'])
    cov = rd('COVERPAGE.tsv', ['ACCESSION_NUMBER', 'ISAMENDMENT', 'FILINGMANAGER_NAME'])
    sub = sub[sub['SUBMISSIONTYPE'] == '13F-HR'].merge(cov, on='ACCESSION_NUMBER'); sub = sub[sub['ISAMENDMENT'].fillna('N') != 'Y'].dropna(subset=['PERIODOFREPORT'])
    nom = sub['FILINGMANAGER_NAME'].fillna('').str.upper(); sub['familia'] = None
    for f, p in FAM.items():
        sub.loc[nom.str.contains(p, regex=True) & sub['familia'].isna(), 'familia'] = f
    sub = sub.dropna(subset=['familia']); sub['periodo'] = sub['PERIODOFREPORT'].map(periodo)
    inf = rd('INFOTABLE.tsv', ['ACCESSION_NUMBER', 'CUSIP', 'SSHPRNAMT', 'SSHPRNAMTTYPE', 'PUTCALL'])
    inf = inf[inf['ACCESSION_NUMBER'].isin(set(sub['ACCESSION_NUMBER'])) & (inf['SSHPRNAMTTYPE'] == 'SH') & inf['PUTCALL'].isna()].merge(sub[['ACCESSION_NUMBER', 'familia', 'periodo', 'FILINGMANAGER_NAME']], on='ACCESSION_NUMBER')
    a = inf['periodo'].str[:4].astype(int); cu = inf['CUSIP'].str.strip().str.upper()
    inf['id'] = [mapa.get((c, x)) or mapa.get((c, x - 1)) or mapa.get((c, x + 1)) for c, x in zip(cu, a)]
    inf = inf.dropna(subset=['id']); inf['acciones'] = pd.to_numeric(inf['SSHPRNAMT'], errors='coerce')
    return inf.groupby(['periodo', 'familia', 'id'], as_index=False)['acciones'].sum(), sorted(set(sub['FILINGMANAGER_NAME']))
t0 = time.time()
pag = get('https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets').decode('utf-8', 'ignore')
urls = sorted(set(re.findall(r'href="([^"]+form13f\.zip)"', pag)))
def anio(u):
    m = re.search(r'(\d{4})q\d_form13f', u) or re.search(r'\d{2}[a-z]{3}(\d{4})-\d{2}[a-z]{3}\d{4}_form13f', u); return int(m.group(1)) if m else 0
urls = [u for u in urls if DESDE <= anio(u) <= HASTA]; partes = []; nombres = set()
for u in urls:
    b = get('https://www.sec.gov' + u)
    if not b: continue
    try:
        d, n = un_zip(b)
    except Exception as e:
        print('SALTEADO', u[-30:], e, flush=True); continue
    partes.append(d); nombres |= set(n)
    print(f'  {u[-30:]}: {len(d)} posiciones de {d["familia"].nunique()} familias ({time.time() - t0:.0f}s)', flush=True)
    pd.concat(partes).to_csv(f'fam13f-{DESDE}.csv', index=False)
open(f'fam13f-nombres-{DESDE}.txt', 'w').write('\n'.join(sorted(nombres)))
print('LISTO', sum(len(p) for p in partes), 'posiciones; declarantes:', len(nombres), flush=True)
