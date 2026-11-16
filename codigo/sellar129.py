"""#129: arma y sella las listas de cambiadas y quietas 2026 (quintiles de similitud 2026 vs 2025)."""
import json, hashlib, datetime as dt, pandas as pd
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'
s = pd.DataFrame([o for o in map(json.loads, open(f'{B}/entrenar/sal-cab102/sim129.jsonl')) if 's2026' in o])
s['q'] = pd.qcut(s['s2026'].rank(method='first'), 5, labels=False)
out = {'prueba': 129, 'sellado': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'n_total': len(s),
       'regla': 'similitud coseno 10-K 2026 vs 2025, texto entero; cambiadas = quintil mas bajo, quietas = quintil mas alto',
       'cambiadas': sorted(int(c) for c in s[s.q == 0].cik), 'quietas': sorted(int(c) for c in s[s.q == 4].cik)}
t = json.dumps(out, indent=1); h = hashlib.sha256(t.encode()).hexdigest()
open(f'{B}/repo-tr/notas/prediccion-129-2026.json', 'w').write(t)
print(len(s), len(out['cambiadas']), len(out['quietas']), 'sha256', h)
