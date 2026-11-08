"""Conceptos internos de Gemma 2 2B (Gemma Scope) sobre «el negocio» de cada 10-K, en varias capas.
Uso: QUIERO=ids.txt python gemma_sae2.py AÑO       (AÑO del EDGAR-CORPUS; QUIERO opcional: sólo esas empresas)
     python gemma_sae2.py textos.jsonl               (líneas {"id":..., "anio_presentado":..., "texto":...}, p.ej. 10-K 2026 bajados de la SEC)
Variables: CAPAS (12,20), N_TOK (512), LOTE (16), TOPK (512).
Salida por capa: sae2-<nombre>-L<capa>.npz y sae2-<nombre>-ids.npy (mismo orden)."""
import sys, os, time, json, glob
import numpy as np, torch
from scipy import sparse
from huggingface_hub import hf_hub_download, list_repo_files, snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM
CAPAS = [int(x) for x in os.environ.get('CAPAS', '12,20').split(',')]
N_TOK, LOTE, TOPK = int(os.environ.get('N_TOK', 512)), int(os.environ.get('LOTE', 16)), int(os.environ.get('TOPK', 512))
t0 = time.time()
ruta = snapshot_download('unsloth/gemma-2-2b', allow_patterns=['*.json', '*.safetensors', '*.model'])
tok = AutoTokenizer.from_pretrained(ruta)
mod = AutoModelForCausalLM.from_pretrained(ruta, dtype=torch.float16, device_map='cuda').eval()
mod.model.layers = mod.model.layers[:max(CAPAS) + 1]; mod.config.num_hidden_layers = max(CAPAS) + 1
archivos = list_repo_files('google/gemma-scope-2b-pt-res')
SAE, guard = {}, {}
for c in CAPAS:
    op = [f for f in archivos if f.startswith(f'layer_{c}/width_16k/average_l0_') and f.endswith('params.npz')]
    f = min(op, key=lambda x: abs(int(x.split('average_l0_')[1].split('/')[0]) - 80))       # el autoencoder de densidad parecida en cada capa
    p = np.load(hf_hub_download('google/gemma-scope-2b-pt-res', f))
    SAE[c] = tuple(torch.tensor(p[k], dtype=torch.float16, device='cuda') for k in ('W_enc', 'b_enc', 'threshold'))
    mod.model.layers[c].register_forward_hook(lambda m, i, o, c=c: guard.__setitem__(c, o[0] if isinstance(o, tuple) else o))
    print(f'capa {c}: {f}', flush=True)
print(f'GEMMA listo ({time.time() - t0:.0f}s)', flush=True)

arg = sys.argv[1]
if arg.endswith('.jsonl'):
    nombre = os.path.basename(arg)[:-6]
    def fuente():
        for l in open(arg, encoding='utf-8'):
            d = json.loads(l); yield d['id'], d['texto']
else:
    from texto import lineas, cargar, h
    nombre = arg; quiero = set(open(os.environ['QUIERO']).read().split()) if os.environ.get('QUIERO') else None
    def fuente():
        vistos = set()
        for l in lineas(int(arg)):
            try:
                d = cargar(l)
            except Exception:
                continue
            c = str(d.get('cik', '')).strip(); t = (d.get('section_1') or '').strip()
            if not c or c in vistos or len(t) < 500:
                continue
            vistos.add(c); i = h(c)
            if quiero is None or i in quiero:
                yield i, t
import re
ANON = os.environ.get('ANON') == '1'
_P = [(re.compile(r'\((?:NYSE|NASDAQ|Nasdaq|NYSE American|AMEX|OTC)[^)]*\)'), ' '),              # (NASDAQ: XXX)
      (re.compile(r'[\w\-\.]+(?:®|™|\(R\)|\(TM\))'), 'PRODUCT'),                              # marcas
      (re.compile(r'\b(?:19|20)\d\d\b'), 'YEAR'), (re.compile(r'\$?\d[\d,\.]*%?'), 'N'),      # años y números
      (re.compile(r'\b[A-Z][\w&\-\.]*(?:\s+(?:of|and|&|de|the)?\s*[A-Z][\w&\-\.]*)+'), 'ENTITY'),  # nombres propios de 2+ palabras
      (re.compile(r'(?<=[a-z,;] )[A-Z][\w&\-]+'), 'ENTITY'),                               # nombre propio suelto en medio de una oración
      (re.compile(r'\b[A-Z]{2,}\b'), 'ENTITY')]                                                # siglas y tickers
def anonimizar(t):
    for p, r in _P:
        t = p.sub(r, t)
    return t
ids, filas, lote_t, lote_i = [], {c: [] for c in CAPAS}, [], []
def procesar():
    e = tok([t[:12000] for t in lote_t], return_tensors='pt', truncation=True, max_length=N_TOK, padding=True).to('cuda')
    with torch.no_grad():
        mod(**e, use_cache=False)
        m = e['attention_mask'].unsqueeze(-1).half()
        for c, (W, b, th) in SAE.items():
            pre = guard[c] @ W + b; f = torch.relu(pre) * (pre > th); f[:, 0] = 0
            media = ((f * m).sum(1) / m.sum(1).clamp(min=1)).float()
            v, i_ = torch.topk(media, TOPK, dim=1)
            filas[c].append(sparse.csr_matrix(torch.zeros_like(media).scatter_(1, i_, v).cpu().numpy()))
    ids.extend(lote_i); lote_t.clear(); lote_i.clear()
for i, t in fuente():
    lote_t.append(anonimizar(t[:12000]) if ANON else t); lote_i.append(i)
    if len(lote_t) == LOTE:
        procesar()
        if len(ids) % 800 == 0:
            print(f'  {len(ids)} empresas ({time.time() - t0:.0f}s)', flush=True)
if lote_t:
    procesar()
for c in CAPAS:
    sparse.save_npz(f'sae2{"a" if ANON else ""}-{nombre}-L{c}.npz', sparse.vstack(filas[c]).tocsr())
np.save(f'sae2{"a" if ANON else ""}-{nombre}-ids.npy', np.array(ids))
print(f'LISTO {nombre}: {len(ids)} empresas, capas {CAPAS} ({time.time() - t0:.0f}s)', flush=True)
