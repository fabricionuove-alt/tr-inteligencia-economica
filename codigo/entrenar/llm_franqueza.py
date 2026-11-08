"""Franqueza de la dirección leída por una IA abierta (señal #34, notas/11-registro-de-senales.md).
Uso: python llm_franqueza.py AÑO FUENTE N [DESDE] [--solo-texto]
  AÑO: año de presentación del 10-K
  FUENTE: 'corpus' (EDGAR-CORPUS test+validate, años <= 2020) o ruta a candidatos.json (bajar de la SEC, 2021+)
          o una carpeta local con AÑO/test.jsonl (prueba)
  N: cuántos textos como máximo; DESDE: tramo de la lista al azar (sólo SEC)
  --solo-texto: arma los recortes y los controles sin usar la IA (para probar sin placa)
Salida: franq-ia-AÑO-DESDE.csv  id, anio_presentado, franq_ia  (se guarda de a lotes)"""
import sys, os, io, json, time, re, random, hashlib, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# El 1.5B falló los controles (franco 5, vago 8: premia el tono optimista). El 3B los pasa (francos 8-10, vagos 1-3).
MODELO = 'Qwen/Qwen2.5-3B-Instruct'
PROMPT = ("You are a skeptical long-term investor. Rate the CANDOR of this management discussion from 1 to 10. "
          "Candid = concrete numbers, admits problems and mistakes, explains causes plainly, speaks as 'we'. "
          "Not candid = vague generalities, jargon, hype, blames outside factors, hides bad news. "
          "Answer with only the number.\n\nTEXT:\n")
CONTROL_FRANCO = ("Our revenue fell 14% to $212 million because we lost our largest customer, Acme, which moved its "
                  "orders to a cheaper competitor. That was our mistake: we had 38% of sales with one client. We cut 90 "
                  "jobs, closed the Ohio plant, and our gross margin dropped from 31% to 24%. We expect 2016 to be weak. ") * 6
CONTROL_VAGO = ("The Company remains uniquely positioned to leverage its world-class, best-in-class platform and robust "
                "synergies going forward. Management believes the transformational strategy will create tremendous value "
                "for stakeholders despite certain macroeconomic headwinds beyond the Company's control. ") * 6
h = lambda cik: hashlib.sha256(('sal-ie-' + str(cik).zfill(10)).encode()).hexdigest()[:12]
recorte = lambda t: ' '.join(t.split()[300:1500])

def textos_corpus(anio, n, local=None):
    base = 'https://huggingface.co/datasets/eloukas/edgar-corpus/resolve/main'
    out, vistos = [], set()
    for parte in ('test', 'validate'):           # particiones al azar del corpus
        if local:
            p = os.path.join(local, str(anio), f'{parte}.jsonl')
            if not os.path.exists(p):
                continue
            fh = open(p, encoding='utf-8')
        else:
            fh = io.TextIOWrapper(urllib.request.urlopen(f'{base}/{anio}/{parte}.jsonl', timeout=300), encoding='utf-8')
        for l in fh:
            d = json.loads(l); c = str(d.get('cik', '')).strip()
            t = d.get('section_7') or ''
            if c and c not in vistos and len(t.split()) > 1500:
                vistos.add(c); out.append((c, recorte(t)))
            if len(out) >= n:
                return out
    return out

def textos_sec(anio, cand_json, n, desde):
    from bajar_10k import get, a_texto, seccion7
    cand = json.load(open(cand_json))[str(anio)]
    rng = random.Random(7); rng.shuffle(cand)
    out = []
    for cik, acc, doc in cand[desde:]:
        b = get(f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-", "")}/{doc}', 0.15)
        t = seccion7(a_texto(b)) if b else ''
        if len(t.split()) > 1500:
            out.append((cik, recorte(t)))
        if len(out) >= n:
            break
    return out

if __name__ == '__main__':
    ANIO, FUENTE, N = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    DESDE = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else 0
    SOLO = '--solo-texto' in sys.argv
    t0 = time.time()
    if FUENTE == 'corpus':
        docs = textos_corpus(ANIO, N)
    elif FUENTE.endswith('.json'):
        docs = textos_sec(ANIO, FUENTE, N, DESDE)
    else:
        docs = textos_corpus(ANIO, N, local=FUENTE)
    print(f'{len(docs)} textos del año {ANIO} en {time.time()-t0:.0f}s', flush=True)
    todos = [('CONTROL_FRANCO', CONTROL_FRANCO), ('CONTROL_VAGO', CONTROL_VAGO)] + docs
    if SOLO:
        print('solo texto: palabras del primer recorte', len(todos[2][1].split()) if len(todos) > 2 else 0); sys.exit(0)
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(MODELO); tok.padding_side = 'left'
    mod = AutoModelForCausalLM.from_pretrained(MODELO, torch_dtype=torch.float16, device_map='cuda')
    print(f'modelo cargado {time.time()-t0:.0f}s', flush=True)
    nombre = f'franq-ia-{ANIO}-{DESDE}.csv'
    fh = open(nombre, 'w'); fh.write('id,anio_presentado,franq_ia' + chr(10)); fh.flush()
    for i in range(0, len(todos), 8):
        lote = todos[i:i + 8]
        msgs = [tok.apply_chat_template([{'role': 'user', 'content': PROMPT + t}], tokenize=False, add_generation_prompt=True) for _, t in lote]
        enc = tok(msgs, return_tensors='pt', padding=True, truncation=True, max_length=2048).to('cuda')
        with torch.no_grad():
            o = mod.generate(**enc, max_new_tokens=3, do_sample=False, pad_token_id=tok.eos_token_id)
        for (c, _), s in zip(lote, tok.batch_decode(o[:, enc['input_ids'].shape[1]:], skip_special_tokens=True)):
            m = re.findall(r'\d+', s); v = int(m[0]) if m and 1 <= int(m[0]) <= 10 else None
            if c.startswith('CONTROL'):
                print(f'{c}: {v}', flush=True)
            else:
                fh.write(f'{h(c)},{ANIO},{"" if v is None else v}' + chr(10))
        fh.flush()
    fh.close()
    print(f'LISTO {len(docs)} textos en {time.time()-t0:.0f}s -> {nombre}', flush=True)
