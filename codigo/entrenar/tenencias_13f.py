"""Tenencias de los fondos concentrados en cada trimestre (señal #42, notas/11).
Uso: python tenencias_13f.py DESDE HASTA CUSIP_CSVS [ZIP_LOCAL]
  DESDE/HASTA: años de PRESENTACIÓN de los 13F. CUSIP_CSVS: cusip-*.csv de mercado.py.
Fondo concentrado = 5 a 300 posiciones en esa presentación. Sin enmiendas, opciones ni no-acciones.
El fondo se guarda con un código anónimo (no su CIK). Si presenta dos veces el mismo período, vale la última.
Salida: t13f-DESDE.csv  periodo (aaaamm del cierre del trimestre), fondo, id, acciones"""
import sys, io, re, time, zipfile, hashlib
import pandas as pd
from mejores_ideas import get, MES

DESDE, HASTA = int(sys.argv[1]), int(sys.argv[2])
CUS = pd.concat([pd.read_csv(x, dtype=str) for x in sys.argv[3].split(',') if x])
LOCAL = sys.argv[4] if len(sys.argv) > 4 else None
mapa = {(c, int(a)): i for c, a, i in zip(CUS['cusip'], CUS['anio'], CUS['id'])}

def periodo(f):                 # '31-MAR-2016' -> '201603'
    d, m, a = f.split('-')
    return f'{int(a):04d}{MES[m.upper()]:02d}'

def un_zip(b):
    z = zipfile.ZipFile(io.BytesIO(b))
    por_nombre = {n.rsplit('/', 1)[-1].upper(): n for n in z.namelist()}
    rd = lambda n, cols: pd.read_csv(z.open(por_nombre[n.upper()]), sep='\t', dtype=str, usecols=cols, quoting=3, on_bad_lines='skip', encoding='latin1')
    sub = rd('SUBMISSION.tsv', ['ACCESSION_NUMBER', 'FILING_DATE', 'SUBMISSIONTYPE', 'CIK', 'PERIODOFREPORT'])
    cov = rd('COVERPAGE.tsv', ['ACCESSION_NUMBER', 'ISAMENDMENT', 'REPORTTYPE'])
    sub = sub[sub['SUBMISSIONTYPE'] == '13F-HR'].merge(cov, on='ACCESSION_NUMBER')
    sub = sub[(sub['ISAMENDMENT'].fillna('N') != 'Y') & sub['REPORTTYPE'].fillna('').str.contains('HOLDINGS')]
    sub = sub.dropna(subset=['PERIODOFREPORT', 'CIK'])
    sub['periodo'] = sub['PERIODOFREPORT'].map(periodo)
    sub['fd'] = pd.to_datetime(sub['FILING_DATE'], format='%d-%b-%Y', errors='coerce')
    sub = sub.sort_values('fd').drop_duplicates(['CIK', 'periodo'], keep='last')     # la última del período
    inf = rd('INFOTABLE.tsv', ['ACCESSION_NUMBER', 'CUSIP', 'SSHPRNAMT', 'SSHPRNAMTTYPE', 'PUTCALL'])
    inf = inf[inf['ACCESSION_NUMBER'].isin(set(sub['ACCESSION_NUMBER'])) & (inf['SSHPRNAMTTYPE'] == 'SH') & inf['PUTCALL'].isna()]
    inf = inf.merge(sub[['ACCESSION_NUMBER', 'CIK', 'periodo']], on='ACCESSION_NUMBER')
    a = inf['periodo'].str[:4].astype(int)
    cu = inf['CUSIP'].str.strip().str.upper()
    inf['id'] = [mapa.get((c, x)) or mapa.get((c, x - 1)) or mapa.get((c, x + 1)) for c, x in zip(cu, a)]
    inf = inf.dropna(subset=['id'])
    inf['acciones'] = pd.to_numeric(inf['SSHPRNAMT'], errors='coerce')
    inf = inf[inf['acciones'] > 0]
    pos = inf.groupby(['CIK', 'periodo', 'id'], as_index=False)['acciones'].sum()
    n = pos.groupby(['CIK', 'periodo'])['id'].transform('count')
    pos = pos[(n >= 5) & (n <= 300)].copy()
    pos['fondo'] = [hashlib.sha256(('sal-ie-fondo-' + c.zfill(10)).encode()).hexdigest()[:10] for c in pos['CIK']]
    return pos[['periodo', 'fondo', 'id', 'acciones']], len(sub)

if __name__ == '__main__':
    t0 = time.time()
    if LOCAL:
        zips = [(LOCAL, open(LOCAL, 'rb').read())]
    else:
        pag = get('https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets').decode('utf-8', 'ignore')
        urls = sorted(set(re.findall(r'href="([^"]+form13f\.zip)"', pag)))
        def anio(u):
            m = re.search(r'(\d{4})q\d_form13f', u) or re.search(r'\d{2}[a-z]{3}(\d{4})-\d{2}[a-z]{3}\d{4}_form13f', u)
            return int(m.group(1)) if m else 0
        urls = [u for u in urls if DESDE <= anio(u) <= HASTA]
        print(len(urls), 'archivos de carteras', flush=True)
        zips = ((u, get('https://www.sec.gov' + u)) for u in urls)
    partes = []
    for u, b in zips:
        if not b:
            continue
        try:
            d, nf = un_zip(b)
        except Exception as e:
            print(f'  {u[-32:]}: SALTEADO {type(e).__name__} {str(e)[:100]}', flush=True); continue
        partes.append(d)
        print(f'  {u[-32:]}: {nf} carteras, {d["fondo"].nunique()} fondos concentrados, {len(d)} posiciones, {time.time()-t0:.0f}s', flush=True)
        pd.concat(partes).drop_duplicates(['periodo', 'fondo', 'id'], keep='last').to_csv(f't13f-{DESDE}.csv', index=False)
    print(f'LISTO {sum(len(p) for p in partes)} posiciones en {time.time()-t0:.0f}s', flush=True)
