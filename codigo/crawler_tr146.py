"""Tr #146: sección 1 de los 10-K 2026 con edgar-crawler (la herramienta de EDGAR-CORPUS). Reglas en notas/11 (#145).
python crawler145.py prueba   -> una sola empresa (CIK 1750) para ver que extrae
python crawler145.py todo     -> todas"""
import os, sys, json, time, threading, urllib.request
from concurrent.futures import ProcessPoolExecutor, as_completed
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'
sys.path.insert(0, f'{B}/herramientas/edgar-crawler'); os.chdir(f'{B}/herramientas/edgar-crawler')
from extract_items import ExtractItems
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}
O = f'{B}/fuentes/tr146'; os.makedirs(f'{O}/raw/10-K', exist_ok=True); os.makedirs(f'{O}/ext', exist_ok=True)
SAL = f'{O}/sec1.jsonl'
lock = threading.Lock(); ult = [0.0]


def get(u):
    for k in range(5):
        with lock:
            w = 2.5 - (time.time() - ult[0])  # 20 procesos x 1/2,5 s = 8 pedidos/s en total
            if w > 0: time.sleep(w)
            ult[0] = time.time()
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read()
        except Exception as e:
            if '404' in str(e): return None
            time.sleep(5 * (k + 1))
    return None


ex = ExtractItems(remove_tables=True, items_to_extract=['1'], include_signature=False,
                  raw_files_folder=f'{O}/raw', extracted_files_folder=f'{O}/ext', skip_extracted_filings=False)


def una(cik):
    j = get(f'https://data.sec.gov/submissions/CIK{cik:010d}.json')
    if not j: return {'cik': cik}
    r = json.loads(j)['filings']['recent']; docs = {}
    for f, d, a, p in zip(r['form'], r['filingDate'], r['accessionNumber'], r['primaryDocument']):
        y = int(d[:4])
        if f == '10-K' and y == 2026 and p: docs[y] = (a, p, d)
    o = {'cik': cik}
    for y, (a, p, d) in docs.items():
        b = get(f'https://www.sec.gov/Archives/edgar/data/{cik}/{a.replace("-", "")}/{p}')
        if not b: continue
        fn = f'{cik}_{y}.htm'; ruta = f'{O}/raw/10-K/{fn}'
        open(ruta, 'w', encoding='utf-8').write('<DOCUMENT>\n<TYPE>10-K\n' + b.decode('utf-8', 'ignore') + '\n</DOCUMENT>')
        meta = {'Type': '10-K', 'filename': fn, 'CIK': cik, 'Company': '', 'Date': d, 'complete_text_file_link': '', 'htm_file_link': '', 'html_index': '',
                'Filing Date': d, 'Period of Report': '', 'SIC': '', 'State of Inc': '', 'State location': '', 'Fiscal Year End': '', 'filename_html': ''}
        try:
            ex.determine_items_to_extract(meta)
            js = ex.extract_items(meta)
            o[str(y)] = (js or {}).get('item_1', '')
        except Exception as e:
            o[str(y) + '_err'] = repr(e)[:300]
        os.remove(ruta)
    return o


if __name__ == '__main__':
    if sys.argv[1] == 'prueba':
        o = una(1750); print({k: (len(v) if isinstance(v, str) and not k.endswith('_err') else v) for k, v in o.items()}); sys.exit()
    ciks = [int(l) for l in open(f'{O}/ciks.txt')]
    hechos = set()
    if os.path.exists(SAL):
        for l in open(SAL, encoding='utf-8'):
            try: hechos.add(json.loads(l)['cik'])
            except Exception: pass
    ciks = [c for c in ciks if c not in hechos]; print('empresas', len(ciks), flush=True)
    with ProcessPoolExecutor(20) as pool, open(SAL, 'a', encoding='utf-8') as f:
        fs = [pool.submit(una, c) for c in ciks]
        for i, fu in enumerate(as_completed(fs)):
            f.write(json.dumps(fu.result()) + chr(10)); f.flush()
            if i % 100 == 0: print('bajadas', i, time.strftime('%H:%M'), flush=True)
    print('LISTO', flush=True)
