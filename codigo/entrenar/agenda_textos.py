"""#89: arma agenda89/agenda.jsonl con pedazos (~1.200 caracteres) de los textos fechados de los grupos de influencia.
id = fuente|año|k. Fuentes: davos_riesgos (Informe de Riesgos Globales, enero), gates (carta anual, enero-febrero),
bilderberg (temas, junio), davos_tec (10 tecnologías emergentes)."""
import re, html, json, subprocess, os, glob, csv
F = 'E:/FABRI INFLUENCIA/inteligencia-economica/fuentes'; S = 'E:/FABRI INFLUENCIA/inteligencia-economica/entrenar/agenda89'
MAXP = 60
def limpio(t): return re.sub(r'\s+', ' ', t).strip()
def pedazos(t, n=1200):
    p = [t[i:i + n] for i in range(0, len(t) - 300, n)]
    if len(p) > MAXP:                                                # parejos a lo largo del documento
        p = [p[round(k * (len(p) - 1) / (MAXP - 1))] for k in range(MAXP)]
    return p
docs = {}
for f in glob.glob(f'{F}/foros/wef/riesgos-*.pdf'):
    a = int(f[-8:-4]); t = subprocess.run(['pdftotext', '-q', f, '-'], capture_output=True).stdout.decode('utf-8', 'ignore')
    if len(t) > 20000: docs[('davos_riesgos', a)] = limpio(t[len(t) // 20:])      # salteo tapa e índice
for f in glob.glob(f'{F}/fundaciones/cartas/*.html'):
    a = int(re.findall(r'(\d{4})', os.path.basename(f))[0])
    if os.path.basename(f).startswith('informe'): continue
    t = open(f, encoding='utf-8', errors='ignore').read()
    ps = [limpio(html.unescape(re.sub(r'<[^>]+>', '', p))) for p in re.findall(r'(?s)<p[^>]*>(.*?)</p>', t)]
    ps = [p for p in ps if len(p) > 120 and not re.search(r'upload|browser|password|cookie|sign in|comment', p, re.I)]
    if sum(map(len, ps)) > 2500: docs[('gates', a)] = ' '.join(ps)
for f in glob.glob(f'{F}/foros/tema-*.html'):
    a = int(f[-9:-5]); t = open(f, encoding='utf-8', errors='ignore').read()
    t = limpio(html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'(?s)<script.*?</script>|<style.*?</style>', '', t))))
    m = re.search(r'(?i)(?:key )?topics for discussion[^:]*:(.{40,700}?)(?:Founded in 1954|The Bilderberg|$)', t)
    if m: docs[('bilderberg', a)] = 'Topics for discussion this year: ' + m.group(1).strip()
tec = {}
for r in csv.DictReader(open(f'{F}/foros/wef/tecnologias.csv', encoding='utf-8')): tec.setdefault(int(r['anio']), []).append(r['tecnologia'])
for a, l in tec.items(): docs[('davos_tec', a)] = 'Top emerging technologies this year: ' + '; '.join(l) + '.'
n = 0
with open(f'{S}/agenda.jsonl', 'w', encoding='utf-8') as o:
    for (fu, a), t in sorted(docs.items()):
        for k, p in enumerate(pedazos(t) if len(t) > 1500 else [t]):
            o.write(json.dumps({'id': f'{fu}|{a}|{k}', 'texto': p}) + '\n'); n += 1
print('AGENDA', n, 'pedazos'); print({fu: sorted(a for f2, a in docs if f2 == fu) for fu in {f for f, _ in docs}})
