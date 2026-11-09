"""#100: ley100/leyes.jsonl. Por proyecto de ley (Congreso 112-117, 2011-2022): título + resumen del CRS. id = AAAAMM|presentado|n o AAAAMM|ley|n (mes en que se volvió ley).
Muestra: hasta 150 proyectos presentados por mes (al azar, semilla 0) y todas las leyes."""
import zipfile, glob, re, json, random, html, xml.etree.ElementTree as ET
random.seed(0); pres, leyes = {}, []
for f in sorted(glob.glob('../fuentes/congreso/b-*.zip')):
    z = zipfile.ZipFile(f)
    for n in z.namelist():
        try: b = ET.fromstring(z.read(n)).find('bill')
        except Exception: continue
        fe = (b.findtext('introducedDate') or '')[:7].replace('-', '')
        tit = b.findtext('title') or ''
        su = b.findall('.//summaries/summary') or b.findall('.//summaries/item') or b.findall('.//billSummaries/item')
        txt = ''
        if su:
            txt = su[0].findtext('text') or su[0].findtext('cdata/summary') or ''
        txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', txt))).strip()
        if len(fe) != 6 or len(txt) < 200: continue
        t = (tit + '. ' + txt)[:1500]
        pres.setdefault(fe, []).append(t)
        la = [a.findtext('actionDate') for a in b.findall('.//actions/item') if 'Became Public Law' in (a.findtext('text') or '')]
        if la and la[0]: leyes.append((la[0][:7].replace('-', ''), t))
n = 0
with open('ley100/leyes.jsonl', 'w', encoding='utf-8') as o:
    for m in sorted(pres):
        for k, t in enumerate(random.sample(pres[m], min(150, len(pres[m])))):
            o.write(json.dumps({'id': f'{m}|presentado|{k}', 'texto': t}) + '\n'); n += 1
    for k, (m, t) in enumerate(leyes):
        o.write(json.dumps({'id': f'{m}|ley|{k}', 'texto': t}) + '\n'); n += 1
print('LEYES', n, 'textos |', len(pres), 'meses con proyectos |', len(leyes), 'leyes |', sum(map(len, pres.values())), 'proyectos con resumen')
