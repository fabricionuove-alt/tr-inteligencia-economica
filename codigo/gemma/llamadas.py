"""#88: arma llamadas-AÑO.jsonl ({"id","texto"}) con la parte de preguntas de la conferencia de resultados de enero-junio de cada año."""
import json, hashlib, re, urllib.request, pyarrow.parquet as pq, pandas as pd
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
tk = json.load(urllib.request.urlopen(urllib.request.Request('https://www.sec.gov/files/company_tickers.json', headers=UA)))
cik = {v['ticker'].upper().replace('.', '-'): v['cik_str'] for v in tk.values()}
d = pq.read_table('part-0.parquet', columns=['symbol', 'year', 'quarter', 'date', 'content']).to_pandas()
d['f'] = pd.to_datetime(d['date'], errors='coerce'); d = d.dropna(subset=['f'])
d['A'] = d['f'].dt.year; d = d[(d['f'].dt.month <= 6) & d['A'].between(2013, 2020)].sort_values('f')
d = d.drop_duplicates(['symbol', 'A'])
def preguntas(t):
    p = [m.start() for m in re.finditer(r'(?m)^Operator:', t)]
    return t[p[1]:] if len(p) > 1 else t[len(t) // 2:]
n = {}
for A, g in d.groupby('A'):
    with open(f'llamadas-{A}.jsonl', 'w', encoding='utf-8') as f:
        for s, t in zip(g['symbol'], g['content']):
            c = cik.get(str(s).upper().replace('.', '-'))
            if c and isinstance(t, str) and len(t) > 2000:
                f.write(json.dumps({'id': h(c), 'texto': preguntas(t)[:12000]}) + '\n'); n[A] = n.get(A, 0) + 1
print('LLAMADAS por año', n, flush=True)
