"""#82: empresas cuyos documentos de fusión nombran a cada banco, por año (buscador de texto completo de la SEC). -> asesores.csv"""
import json, time, urllib.request, urllib.parse, csv
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
BANCOS = {'Rothschild': '"Rothschild"', 'Lazard': '"Lazard"', 'Goldman': '"Goldman Sachs"', 'MorganStanley': '"Morgan Stanley"', 'JPMorgan': '"J.P. Morgan"'}
w = csv.writer(open('asesores.csv', 'w', newline='')); w.writerow(['banco', 'cik', 'fecha', 'forma'])
for b, q in BANCOS.items():
    for y in range(2005, 2026):
        desde = 0
        while True:
            u = 'https://efts.sec.gov/LATEST/search-index?' + urllib.parse.urlencode({'q': q, 'forms': 'DEFM14A,PREM14A,S-4,SC 14D9', 'dateRange': 'custom', 'startdt': f'{y}-01-01', 'enddt': f'{y}-12-31', 'from': desde})
            j = None
            for i in range(4):
                try: j = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()); break
                except Exception: time.sleep(3 + 3 * i)
            if not j: break
            hs = j['hits']['hits']
            for x in hs:
                s = x['_source']
                for c in s.get('ciks', [])[:1]: w.writerow([b, c, s.get('file_date'), s.get('form')])
            desde += len(hs); time.sleep(0.15)
            if not hs or desde >= min(j['hits']['total']['value'], 1000): break
        print(b, y, desde, flush=True)
print('LISTO')
