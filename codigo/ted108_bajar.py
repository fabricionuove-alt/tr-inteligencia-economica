"""#108: baja las adjudicaciones de TED (contratos públicos de la UE) 2006-2023 y guarda sólo ganador, país, año, CPV y monto.
Salida: fuentes/ted/adjudicaciones.csv"""
import io, os, csv, sys, zipfile, gzip, urllib.request
csv.field_size_limit(10**8)
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; os.makedirs(f'{B}/fuentes/ted', exist_ok=True)
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
KEEP = ['ID_NOTICE_CAN', 'YEAR', 'CANCELLED', 'ISO_COUNTRY_CODE', 'CPV', 'TYPE_OF_CONTRACT', 'WIN_NAME', 'WIN_COUNTRY_CODE', 'AWARD_VALUE_EURO', 'VALUE_EURO', 'DT_AWARD']
out = open(f'{B}/fuentes/ted/adjudicaciones.csv', 'w', newline='', encoding='utf-8'); w = csv.writer(out); w.writerow(KEEP)
for y in range(2006, 2024):
    u = ('https://data.europa.eu/euodp/repository/ec/dg-grow/mapps/TED%202020/TED%20-%20Contract%20award%20notices%202006.csv.gz' if y == 2006
         else f'https://data.europa.eu/data-management/store/api/legacy/data/ted-contract-award-notices-{y}.zip/')
    raw = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=900).read()
    if y == 2006: fh = io.BytesIO(gzip.decompress(raw))
    else:
        z = zipfile.ZipFile(io.BytesIO(raw)); n = [x for x in z.namelist() if x.lower().endswith('.csv')][0]; fh = z.open(n)
    t = io.TextIOWrapper(fh, encoding='utf-8', errors='replace', newline='')
    r = csv.DictReader(t); k = 0
    for row in r:
        if not row.get('WIN_NAME'): continue
        w.writerow([row.get(c, '') for c in KEEP]); k += 1
    print(y, 'filas con ganador', k, f'{len(raw) / 1e6:.0f} MB', flush=True)
out.close(); print('LISTO', flush=True)
