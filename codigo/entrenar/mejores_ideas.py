"""La mejor idea de cada fondo, trimestre por trimestre (señal #35, notas/11).
Uso: python mejores_ideas.py DESDE HASTA CUSIP_CSVS [ZIP_LOCAL]
  DESDE/HASTA: años de PRESENTACIÓN de los 13F (el zip "2016q1" trae lo presentado en ene-mar 2016)
  CUSIP_CSVS: cusip-*.csv separados por coma (de mercado.py)
Mejor idea (Cohen-Polk-Silli 2010) = la acción donde el peso del fondo supera más al peso de esa acción
en el total de todos los fondos. Fondos que cuentan: 5 a 300 posiciones. Sin enmiendas, opciones ni no-acciones.
Compra = mes siguiente a la presentación. Salida: ideas-DESDE.csv  mes_compra, id, fondo"""
import sys, io, re, time, zipfile, urllib.request, collections
import pandas as pd

UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
DESDE, HASTA = int(sys.argv[1]), int(sys.argv[2])
CUS = pd.concat([pd.read_csv(x, dtype=str) for x in sys.argv[3].split(',') if x])
LOCAL = sys.argv[4] if len(sys.argv) > 4 else None
mapa = {(c, int(a)): i for c, a, i in zip(CUS['cusip'], CUS['anio'], CUS['id'])}
MES = {m: i for i, m in enumerate(['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'], 1)}

def get(u):
    for i in range(4):
        try:
            time.sleep(0.15)
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=300).read()
        except Exception as e:
            print('reintento', u[-40:], type(e).__name__, flush=True); time.sleep(5 * (i + 1))
    return None

def mes_compra(fecha):          # '31-MAR-2016' -> '201604'
    d, m, a = fecha.split('-'); m = MES[m] + 1; a = int(a)
    if m == 13:
        m, a = 1, a + 1
    return f'{a:04d}{m:02d}'

def un_zip(b):
    z = zipfile.ZipFile(io.BytesIO(b))
    # en algunos archivos las tablas vienen dentro de una subcarpeta: se buscan por nombre
    por_nombre = {n.rsplit('/', 1)[-1].upper(): n for n in z.namelist()}
    rd = lambda n, cols: pd.read_csv(z.open(por_nombre[n.upper()]), sep='\t', dtype=str, usecols=cols, quoting=3, on_bad_lines='skip', encoding='latin1')
    sub = rd('SUBMISSION.tsv', ['ACCESSION_NUMBER', 'FILING_DATE', 'SUBMISSIONTYPE'])
    cov = rd('COVERPAGE.tsv', ['ACCESSION_NUMBER', 'ISAMENDMENT', 'REPORTTYPE'])
    sub = sub[sub['SUBMISSIONTYPE'] == '13F-HR'].merge(cov, on='ACCESSION_NUMBER')
    sub = sub[(sub['ISAMENDMENT'].fillna('N') != 'Y') & sub['REPORTTYPE'].fillna('').str.contains('HOLDINGS')]
    inf = rd('INFOTABLE.tsv', ['ACCESSION_NUMBER', 'CUSIP', 'VALUE', 'SSHPRNAMTTYPE', 'PUTCALL'])
    inf = inf[inf['ACCESSION_NUMBER'].isin(set(sub['ACCESSION_NUMBER'])) & (inf['SSHPRNAMTTYPE'] == 'SH') & inf['PUTCALL'].isna()]
    inf = inf.merge(sub[['ACCESSION_NUMBER', 'FILING_DATE']], on='ACCESSION_NUMBER')
    inf['anio'] = inf['FILING_DATE'].str[-4:].astype(int)
    cu = inf['CUSIP'].str.strip().str.upper()
    inf['id'] = [mapa.get((c, a)) or mapa.get((c, a - 1)) or mapa.get((c, a + 1)) for c, a in zip(cu, inf['anio'])]
    inf = inf.dropna(subset=['id'])
    inf['VALUE'] = pd.to_numeric(inf['VALUE'], errors='coerce')
    inf = inf[inf['VALUE'] > 0]
    pos = inf.groupby(['ACCESSION_NUMBER', 'FILING_DATE', 'id'], as_index=False)['VALUE'].sum()
    # peso del "mercado" = todos los fondos juntos (las unidades de VALUE son iguales dentro de un mismo zip)
    wm = pos.groupby('id')['VALUE'].sum(); wm = wm / wm.sum()
    tot = pos.groupby('ACCESSION_NUMBER')['VALUE'].transform('sum')
    n = pos.groupby('ACCESSION_NUMBER')['id'].transform('count')
    pos['sobrepeso'] = pos['VALUE'] / tot - pos['id'].map(wm)
    pos = pos[(n >= 5) & (n <= 300)]
    mejor = pos.loc[pos.groupby('ACCESSION_NUMBER')['sobrepeso'].idxmax()]
    return pd.DataFrame({'mes_compra': [mes_compra(f) for f in mejor['FILING_DATE']], 'id': mejor['id'].values,
                         'fondo': mejor['ACCESSION_NUMBER'].values}), len(sub), len(mejor)

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
            d, nf, nm = un_zip(b)
        except Exception as e:          # un archivo raro no frena al resto
            print(f'  {u[-32:]}: SALTEADO {type(e).__name__} {str(e)[:100]}', flush=True); continue
        partes.append(d)
        print(f'  {u[-32:]}: {nf} carteras, {nm} fondos con 5-300 posiciones, {time.time()-t0:.0f}s', flush=True)
        pd.concat(partes).to_csv(f'ideas-{DESDE}.csv', index=False)      # se guarda en cada paso
    print(f'LISTO {sum(len(p) for p in partes)} mejores ideas en {time.time()-t0:.0f}s', flush=True)
