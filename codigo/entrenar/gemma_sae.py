"""#65 (notas/11): los conceptos internos de Gemma 2 2B sobre «el negocio» de cada 10-K.
Gemma lee los primeros N_TOK tokens de la sección 1; en la capa CAPA se toma el estado residual y se pasa por el autoencoder
disperso de Gemma Scope (JumpReLU, 16.384 conceptos). Por empresa se guarda el promedio de cada concepto sobre los tokens.
Uso: python gemma_sae.py AÑO [LIMITE] [CARPETA_LOCAL]   Salida: sae-AÑO.npz (ids, matriz dispersa empresas × conceptos)."""
import sys, os, time, glob
import numpy as np, torch
from scipy import sparse
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer, AutoModelForCausalLM
from texto import lineas, cargar, h
CAPA, N_TOK, LOTE = int(os.environ.get('CAPA', 12)), int(os.environ.get('N_TOK', 256)), int(os.environ.get('LOTE', 16))
anio = int(sys.argv[1]); t0 = time.time()
print('montado:', os.listdir('/kaggle/input') if os.path.isdir('/kaggle/input') else '-', flush=True)
_c = sorted(glob.glob('/kaggle/input/**/config.json', recursive=True), key=len)
if os.environ.get('GEMMA'):
    ruta = os.environ['GEMMA']
elif _c:
    ruta = os.path.dirname(_c[0])
else:
    from huggingface_hub import snapshot_download          # copia pública de los mismos pesos (licencia Gemma aceptada)
    ruta = snapshot_download('unsloth/gemma-2-2b', allow_patterns=['*.json', '*.safetensors', '*.model'])
print('GEMMA en', ruta, flush=True)
tok = AutoTokenizer.from_pretrained(ruta)
mod = AutoModelForCausalLM.from_pretrained(ruta, torch_dtype=torch.float16, device_map='cuda').eval()
p = np.load(hf_hub_download('google/gemma-scope-2b-pt-res', f'layer_{CAPA}/width_16k/average_l0_82/params.npz'))
W, b, th = (torch.tensor(p[k], dtype=torch.float16, device='cuda') for k in ('W_enc', 'b_enc', 'threshold'))
print(f'GEMMA listo, capa {CAPA}, {W.shape[1]} conceptos ({time.time() - t0:.0f}s)', flush=True)
guard = {}
def gancho(m, i, o):
    guard['x'] = o[0] if isinstance(o, tuple) else o
mod.model.layers = mod.model.layers[:CAPA + 1]; mod.config.num_hidden_layers = CAPA + 1   # sólo hasta la capa que se lee
mod.model.layers[CAPA].register_forward_hook(gancho)
ids, filas, lote_t, lote_i, vistos = [], [], [], [], set()
def procesar():
    e = tok(lote_t, return_tensors='pt', truncation=True, max_length=N_TOK, padding=True).to('cuda')
    with torch.no_grad():
        mod(**e, use_cache=False)
        x = guard['x']; pre = x @ W + b; f = torch.relu(pre) * (pre > th)
        m = e['attention_mask'].unsqueeze(-1).half(); f[:, 0] = 0          # el primer token (BOS) se ignora
        media = (f * m).sum(1) / m.sum(1).clamp(min=1)
    v, i_ = torch.topk(media.float(), int(os.environ.get('TOPK', 256)), dim=1)        # los conceptos más fuertes de cada empresa
    d_ = torch.zeros_like(media, dtype=torch.float32).scatter_(1, i_, v)
    filas.append(sparse.csr_matrix(d_.cpu().numpy().astype(np.float32))); ids.extend(lote_i); lote_t.clear(); lote_i.clear()
for l in lineas(anio):
    try:
        d = cargar(l)
    except Exception:
        continue
    c = str(d.get('cik', '')).strip(); t = (d.get('section_1') or '').strip()
    if not c or c in vistos or len(t) < 500:
        continue
    vistos.add(c); lote_t.append(t[:6000]); lote_i.append(h(c))
    if len(lote_t) == LOTE:
        procesar()
        if len(ids) % 400 == 0:
            print(f'  {len(ids)} empresas ({time.time() - t0:.0f}s)', flush=True)
if lote_t:
    procesar()
M = sparse.vstack(filas).tocsr()
sparse.save_npz(f'sae-{anio}.npz', M); np.save(f'sae-{anio}-ids.npy', np.array(ids))
print(f'LISTO {anio}: {M.shape[0]} empresas × {M.shape[1]} conceptos, {M.nnz / max(M.shape[0], 1):.0f} activos por empresa ({time.time() - t0:.0f}s)', flush=True)
