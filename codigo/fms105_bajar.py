"""#105: baja los avisos 36(b) del Federal Register (texto por govinfo.gov; federalregister.gov pide humano) a sal-fms/avisos.jsonl"""
import json, time, urllib.request, urllib.parse, os
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
hechos = set()
if os.path.exists('sal-fms/avisos.jsonl'): hechos = {json.loads(l)['doc'] for l in open('sal-fms/avisos.jsonl', encoding='utf-8')}
out = open('sal-fms/avisos.jsonl', 'a', encoding='utf-8')
for pag in range(1, 30):
    q = urllib.parse.urlencode([('per_page', 100), ('page', pag), ('conditions[term]', '"Arms Sales Notification"'), ('conditions[agencies][]', 'defense-department'), ('conditions[publication_date][gte]', '2008-01-01'),
                                ('fields[]', 'document_number'), ('fields[]', 'publication_date'), ('fields[]', 'title'), ('order', 'oldest')])
    d = json.loads(get('https://www.federalregister.gov/api/v1/documents.json?' + q)); R = d.get('results') or []
    for x in R:
        if x['document_number'] in hechos: continue
        try: t = get(f"https://www.govinfo.gov/content/pkg/FR-{x['publication_date']}/html/{x['document_number']}.htm").decode('utf-8', 'ignore')
        except Exception as e: print('falla', x['document_number'], e, flush=True); continue
        out.write(json.dumps({'doc': x['document_number'], 'fecha': x['publication_date'], 'titulo': x['title'], 'texto': t}) + '\n'); out.flush(); time.sleep(0.3)
    print('página', pag, len(R), 'total', d.get('count'), flush=True)
    if len(R) < 100: break
