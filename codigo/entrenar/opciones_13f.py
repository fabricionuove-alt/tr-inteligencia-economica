"""Los dos lados del mostrador (notas/14, tipos B y F): puts y calls declarados en los 13F, y las acciones de esos mismos fondos.
Uso: python opciones_13f.py DESDE HASTA CUSIP_CSVS
Se guardan sólo los fondos que declaran alguna opción en ese período (de ellos, también sus acciones: así se ve si
un mismo fondo está de los dos lados). Fondo con código anónimo. Sin enmiendas; si presenta dos veces, vale la última.
Salida: op13f-DESDE.csv  periodo, fondo, id, tipo (SH acciones / PUT / CALL), acciones (para opciones: acciones de base)"""
import sys, io, re, time, zipfile, hashlib
import pandas as pd
from mejores_ideas import get, MES

DESDE, HASTA = int(sys.argv[1]), int(sys.argv[2])
CUS = pd.concat([pd.read_csv(x, dtype=str) for x in sys.argv[3].split(',') if x])
mapa = {(c, int(a)): i for c, a, i in zip(CUS['cusip'], CUS['anio'], CUS['id'])}
def periodo(f):
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
    sub = sub.sort_values('fd').drop_duplicates(['CIK', 'periodo'], keep='last')
    inf = rd('INFOTABLE.tsv', ['ACCESSION_NUMBER', 'CUSIP', 'SSHPRNAMT', 'SSHPRNAMTTYPE', 'PUTCALL'])
    inf = inf[inf['ACCESSION_NUMBER'].isin(set(sub['ACCESSION_NUMBER'])) & (inf['SSHPRNAMTTYPE'] == 'SH')]
    inf['tipo'] = inf['PUTCALL'].fillna('SH').str.strip().str.upper().replace({'': 'SH'})
    inf = inf[inf['tipo'].isin(['SH', 'PUT', 'CALL'])]
    con_op = set(inf.loc[inf['tipo'] != 'SH', 'ACCESSION_NUMBER'])
    inf = inf[inf['ACCESSION_NUMBER'].isin(con_op)].merge(sub[['ACCESSION_NUMBER', 'CIK', 'periodo']], on='ACCESSION_NUMBER')
    a = inf['periodo'].str[:4].astype(int)
    cu = inf['CUSIP'].str.strip().str.upper()
    inf['id'] = [mapa.get((c, x)) or mapa.get((c, x - 1)) or mapa.get((c, x + 1)) for c, x in zip(cu, a)]
    inf = inf.dropna(subset=['id'])
    inf['acciones'] = pd.to_numeric(inf['SSHPRNAMT'], errors='coerce')
    inf = inf[inf['acciones'] > 0]
    pos = inf.groupby(['CIK', 'periodo', 'id', 'tipo'], as_index=False)['acciones'].sum()
    pos['fondo'] = [hashlib.sha256(('sal-ie-fondo-' + c.zfill(10)).encode()).hexdigest()[:10] for c in pos['CIK']]
    return pos[['periodo', 'fondo', 'id', 'tipo', 'acciones']], len(con_op)

if __name__ == '__main__':
    t0 = time.time()
    pag = get('https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets').decode('utf-8', 'ignore')
    urls = sorted(set(re.findall(r'href="([^"]+form13f\.zip)"', pag)))
    def anio(u):
        m = re.search(r'(\d{4})q\d_form13f', u) or re.search(r'\d{2}[a-z]{3}(\d{4})-\d{2}[a-z]{3}\d{4}_form13f', u)
        return int(m.group(1)) if m else 0
    urls = [u for u in urls if DESDE <= anio(u) <= HASTA]
    print(len(urls), 'archivos de carteras', flush=True)
    partes = []
    for u in urls:
        b = get('https://www.sec.gov' + u)
        if not b:
            continue
        try:
            d, nf = un_zip(b)
        except Exception as e:
            print(f'  {u[-32:]}: SALTEADO {type(e).__name__} {str(e)[:100]}', flush=True); continue
        partes.append(d)
        print(f'  {u[-32:]}: {nf} carteras con opciones, {d["fondo"].nunique()} fondos, '
              f'{(d["tipo"] == "PUT").sum()} puts, {(d["tipo"] == "CALL").sum()} calls, {time.time()-t0:.0f}s', flush=True)
        pd.concat(partes).drop_duplicates(['periodo', 'fondo', 'id', 'tipo'], keep='last').to_csv(f'op13f-{DESDE}.csv', index=False)
    print(f'LISTO {sum(len(p) for p in partes)} filas en {time.time()-t0:.0f}s', flush=True)
