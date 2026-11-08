"""Prueba de VELOCIDAD (no de resultado): ¿cuánto tarda una IA abierta en leer la franqueza en una placa T4 de Kaggle?
Uso: python llm_prueba.py MODELO N
Lee N explicaciones de la dirección (sección 7) del corpus, recorta ~1.200 palabras de cada una,
le pide a la IA un puntaje de franqueza 1-10 y mide palabras por segundo. Sin claves: el modelo se baja de Hugging Face."""
import sys, io, json, time, re, urllib.request
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODELO = sys.argv[1] if len(sys.argv) > 1 else 'Qwen/Qwen2.5-1.5B-Instruct'
N = int(sys.argv[2]) if len(sys.argv) > 2 else 32
u = 'https://huggingface.co/datasets/eloukas/edgar-corpus/resolve/main/2015/test.jsonl'
textos = []
for l in io.TextIOWrapper(urllib.request.urlopen(u, timeout=300), encoding='utf-8'):
    d = json.loads(l); t = d.get('section_7') or ''
    if len(t.split()) > 1500:
        textos.append(' '.join(t.split()[300:1500]))      # salteo el encabezado legal
    if len(textos) >= N:
        break
PROMPT = ("You are a skeptical long-term investor. Rate the CANDOR of this management discussion from 1 to 10. "
          "Candid = concrete numbers, admits problems and mistakes, explains causes plainly, speaks as 'we'. "
          "Not candid = vague generalities, jargon, hype, blames outside factors, hides bad news. "
          "Answer with only the number.\n\nTEXT:\n")
t0 = time.time()
tok = AutoTokenizer.from_pretrained(MODELO); tok.padding_side = 'left'
mod = AutoModelForCausalLM.from_pretrained(MODELO, torch_dtype=torch.float16, device_map='cuda')
print(f'modelo cargado en {time.time()-t0:.0f}s', flush=True)
msgs = [tok.apply_chat_template([{'role': 'user', 'content': PROMPT + t}], tokenize=False, add_generation_prompt=True) for t in textos]
t1 = time.time(); salidas = []; n_tok = 0
for i in range(0, len(msgs), 8):
    lote = tok(msgs[i:i + 8], return_tensors='pt', padding=True, truncation=True, max_length=2048).to('cuda')
    n_tok += int(lote['attention_mask'].sum())
    with torch.no_grad():
        o = mod.generate(**lote, max_new_tokens=3, do_sample=False, pad_token_id=tok.eos_token_id)
    salidas += tok.batch_decode(o[:, lote['input_ids'].shape[1]:], skip_special_tokens=True)
dt = time.time() - t1
notas = [re.findall(r'\d+', s)[0] if re.findall(r'\d+', s) else '?' for s in salidas]
print(f'{len(msgs)} textos, {n_tok} tokens en {dt:.1f}s = {n_tok/dt:.0f} tokens/s, {dt/len(msgs):.2f} s por texto', flush=True)
print('puntajes:', ' '.join(notas), flush=True)
print(f'ESTIMACIÓN: 36.000 textos ≈ {36000*dt/len(msgs)/60:.0f} minutos de placa', flush=True)
