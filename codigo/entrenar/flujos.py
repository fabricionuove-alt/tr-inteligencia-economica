"""#76: flujos de financiamiento y regulación por tema y año (NIH, NSF, Federal Register). Uso: python flujos.py -> flujos.csv"""
import json, time, urllib.request, urllib.parse, csv, sys
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
TERM = {'baterias': 'battery', 'nuclear': 'nuclear reactor', 'genomica': 'genomics', 'farmacos': 'drug discovery', 'diagnostico': 'diagnostic device',
        'robotica': 'robotics', 'ia': 'artificial intelligence', 'cuantica': 'quantum computing', 'chips': 'semiconductor', 'espacio': 'satellite',
        'solar': 'solar cell', 'hidrogeno': 'hydrogen fuel', 'autos': 'electric vehicle', 'blockchain': 'blockchain', 'manufactura': 'additive manufacturing',
        'agro': 'crop yield', 'agua': 'water purification', 'construccion': 'building construction', 'materiales': 'advanced materials',
        'comunicaciones': 'wireless communication', 'realidad_virtual': 'virtual reality', 'carbono': 'carbon capture'}
def pedir(u, data=None, intentos=4):
    for i in range(intentos):
        try:
            r = urllib.request.Request(u, data=json.dumps(data).encode() if data else None, headers=dict(UA, **({'Content-Type': 'application/json'} if data else {})))
            return json.loads(urllib.request.urlopen(r, timeout=60).read())
        except Exception as e:
            time.sleep(3 + 4 * i)
    return None
def nih(t, y):
    j = pedir('https://api.reporter.nih.gov/v2/projects/search', {'criteria': {'advanced_text_search': {'operator': 'and', 'search_field': 'projecttitle,terms', 'search_text': f'"{t}"'}, 'fiscal_years': [y]}, 'limit': 1})
    return j['meta']['total'] if j else None
def nsf(t, y):
    q = urllib.parse.urlencode({'keyword': f'"{t}"', 'dateStart': f'01/01/{y}', 'dateEnd': f'12/31/{y}', 'printFields': 'id', 'rpp': 1})
    j = pedir('https://api.nsf.gov/services/v1/awards.json?' + q)
    return j['response'].get('metadata', {}).get('totalCount') if j and 'response' in j else None
def fr(t, y):
    q = f'conditions[term]={urllib.parse.quote(chr(34) + t + chr(34))}&conditions[publication_date][year]={y}&per_page=1'
    j = pedir('https://www.federalregister.gov/api/v1/documents.json?' + q)
    return j.get('count') if j else None
w = csv.writer(open('flujos.csv', 'w', newline='')); w.writerow(['tema', 'anio', 'nih', 'nsf', 'fedreg'])
for k, t in TERM.items():
    for y in range(2005, 2026):
        fila = [k, y, nih(t, y), nsf(t, y), fr(t, y)]; w.writerow(fila); time.sleep(0.4)
    print('listo', k, fila, flush=True)
print('LISTO')
