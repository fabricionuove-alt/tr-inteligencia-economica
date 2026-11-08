"""Baja las carteras de fin de año (13F, cuarto trimestre) de Pabrai y RV Capital.
Salida: carteras_13f.csv (inversor, anio, nombre, cusip, valor_miles)"""
import json, re, csv, time, urllib.request, os
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
def get(u):
    time.sleep(0.15)
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()

FILERS = {'pabrai': ['0001173334', '0001549575'], 'vinall': ['0001766596']}
out = []
for quien, ciks in FILERS.items():
    for cik in ciks:
        s = json.loads(get(f'https://data.sec.gov/submissions/CIK{cik}.json'))
        r = s['filings']['recent']
        for acc, form, rep in zip(r['accessionNumber'], r['form'], r['reportDate']):
            if form != '13F-HR' or not rep.endswith('-12-31'):
                continue
            base = f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-", "")}'
            idx = json.loads(get(base + '/index.json'))
            xmls = [i['name'] for i in idx['directory']['item'] if i['name'].lower().endswith('.xml') and 'primary' not in i['name'].lower()]
            if not xmls:
                continue
            x = get(f'{base}/{xmls[0]}').decode('utf-8', 'ignore')
            x = re.sub(r'<(/?)[a-zA-Z0-9]+:', r'<\1', x)   # quitar prefijos ns1:
            for b in re.findall(r'<infoTable>(.*?)</infoTable>', x, re.S):
                g = lambda t: (re.search(f'<{t}>(.*?)</{t}>', b, re.S) or [None, ''])[1].strip()
                out.append({'inversor': quien, 'anio': int(rep[:4]), 'nombre': g('nameOfIssuer'),
                            'cusip': g('cusip'), 'valor': g('value'), 'clase': g('titleOfClass')})
            print(quien, cik, rep, len(out), flush=True)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'carteras_13f.csv')
w = csv.DictWriter(open(p, 'w', newline='', encoding='utf-8'), fieldnames=list(out[0]))
w.writeheader(); w.writerows(out)
print('LISTO', len(out), 'posiciones ->', p)
