"""id (hash) -> código industrial SIC, desde submissions.zip de la SEC. Uso: python sic_de_sub.py submissions.zip sic.csv"""
import sys, zipfile, json, hashlib, csv
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
z = zipfile.ZipFile(sys.argv[1]); w = csv.writer(open(sys.argv[2], 'w', newline='')); w.writerow(['id', 'sic']); n = 0
for nm in z.namelist():
    if not nm.startswith('CIK') or '-submissions-' in nm:
        continue
    try:
        d = json.loads(z.read(nm))
    except Exception:
        continue
    if d.get('sic'):
        w.writerow([h(d.get('cik', nm[3:13])), d['sic']]); n += 1
print('SIC', n, 'empresas')
