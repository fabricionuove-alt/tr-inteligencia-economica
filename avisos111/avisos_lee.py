"""#111 (CPU, GitHub Actions): Qwen lee cada aviso 8-K y dice si la empresa ganó un contrato de un cliente fuera de EE.UU. Entrada avisos.jsonl; salida lectura.jsonl."""
import json, re, sys, time, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
t0 = time.time()
L = [json.loads(l) for l in open(sys.argv[1], encoding='utf-8')]
k, N = int(sys.argv[2]), int(sys.argv[3]); L = L[k::N]; torch.set_num_threads(4)
P = """You are reading an excerpt of a company's filing (8-K or press release) with the U.S. SEC. The filing company is: {nombre}.
Return ONLY a JSON object with these keys:
"foreign_win": true if the filing company (or its subsidiary) WON or WAS AWARDED a contract or order from a customer OUTSIDE the United States (a foreign government, a foreign state-owned company, or a foreign private company); false otherwise (U.S. customers, U.S. government contracts performed abroad for the U.S. government, losses, bids not yet won, or no contract).
"country": the customer's country as a plain English name, or null.
"customer": one of "government", "state_company", "private", "unknown", or null.
"usd_millions": the contract value in millions of U.S. dollars (number) or null.
"evidence": one short quote from the text.

TEXT:
"""
tok = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-3B-Instruct', padding_side='left')
mod = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-3B-Instruct', dtype=torch.float32).eval()
print('CPU', len(L), 'avisos', flush=True)
prom = [tok.apply_chat_template([{'role': 'user', 'content': P.replace('{nombre}', x['nombre']) + x['texto'][:5000]}], tokenize=False, add_generation_prompt=True) for x in L]
textos = []
for i, pr in enumerate(prom):
    e = tok(pr, return_tensors='pt')
    with torch.no_grad(): g = mod.generate(**e, max_new_tokens=160, do_sample=False, pad_token_id=tok.eos_token_id)
    textos.append(tok.decode(g[0][e['input_ids'].shape[1]:], skip_special_tokens=True))
    if i % 10 == 0: print(f'  {i}/{len(prom)} {time.time() - t0:.0f}s', flush=True)
with open(f'avisos111/sal/lectura_{k:02d}.jsonl', 'w', encoding='utf-8') as f:
    for x, r in zip(L, textos):
        m = re.search(r'\{.*\}', r, re.S)
        try: j = json.loads(m.group(0)) if m else None
        except Exception: j = None
        f.write(json.dumps({'doc': x['doc'], 'cik': x['cik'], 'fecha': x['fecha'], 'lectura': j, 'crudo': None if j else r[:600]}) + '\n')
print('LISTO', len(L), f'{time.time() - t0:.0f}s', flush=True)
