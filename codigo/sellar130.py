"""#130: lista sellada de empresas en declive y nacimiento con el año fiscal 2025 (10-K presentados en 2026)."""
import json, time, hashlib, datetime as dt, urllib.request
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
C = {'O': 'NetCashProvidedByUsedInOperatingActivities', 'I': 'NetCashProvidedByUsedInInvestingActivities', 'F': 'NetCashProvidedByUsedInFinancingActivities'}
v = {}
for k, c in C.items():
    j = json.loads(urllib.request.urlopen(urllib.request.Request(f'https://data.sec.gov/api/xbrl/frames/us-gaap/{c}/USD/CY2025.json', headers=UA), timeout=120).read()); time.sleep(.2)
    for o in j['data']: v.setdefault(o['cik'], {})[k] = (o['val'], o.get('entityName', ''))
L = {'declive': [], 'nacimiento': []}
for cik, z in v.items():
    if len(z) < 3: continue
    O, I, F = z['O'][0] > 0, z['I'][0] > 0, z['F'][0] > 0
    if not O and I: L['declive'].append(cik)
    elif not O and not I and F: L['nacimiento'].append(cik)
out = {'prueba': 130, 'sellado': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'anio_fiscal': 2025,
       'con_los_tres_flujos': sum(len(z) == 3 for z in v.values()), 'declive': sorted(L['declive']), 'nacimiento': sorted(L['nacimiento'])}
t = json.dumps(out, indent=1); open(f'{B}/repo-tr/notas/prediccion-130-2026.json', 'w').write(t)
print(out['con_los_tres_flujos'], len(out['declive']), len(out['nacimiento']), 'sha256', hashlib.sha256(t.encode()).hexdigest())
