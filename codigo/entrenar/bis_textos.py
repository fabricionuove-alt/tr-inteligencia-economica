"""#90: bis90/bis.jsonl, un pedazo por discurso (después de la marca «* * *» si está, saltando 300 caracteres). id = AAAAMM|n"""
import zipfile, glob, json, re, pandas as pd
n = 0; c = {}
with open('bis90/bis.jsonl', 'w', encoding='utf-8') as o:
    for f in sorted(glob.glob('../fuentes/bis/s-*.zip')):
        z = zipfile.ZipFile(f); d = pd.read_csv(z.open(z.namelist()[0]))
        for fe, t in zip(d['date'], d['text']):
            if not isinstance(t, str) or len(t) < 2500: continue
            m = re.search(r'\*\s+\*\s+\*', t); t = t[m.end():] if m and m.end() < len(t) // 3 else t
            t = re.sub(r'\s+', ' ', t)[300:1500]; mes = str(fe)[:4] + str(fe)[5:7]
            o.write(json.dumps({'id': f'{mes}|{n}', 'texto': t}) + '\n'); n += 1; c[mes[:4]] = c.get(mes[:4], 0) + 1
print('BIS', n, 'discursos', c)
