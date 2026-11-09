"""#102: un modelo de lenguaje lee cada cable BEXP y saca qué empresas aparecen y en qué papel. Entrada bexp.jsonl; salida lectura.jsonl."""
import json, re, sys, time, subprocess
t0 = time.time()
L = [json.loads(l) for l in open(sys.argv[1], encoding='utf-8')]
if len(sys.argv) > 3: L = L[int(sys.argv[2]):int(sys.argv[3])]   # tramo (para partir en dos placas)
P = """You are reading a U.S. State Department diplomatic cable. Return ONLY a JSON object with these keys:
"kind": one of "advocacy" (U.S. officials pushing a foreign government or buyer to choose a specific company), "dispute" (a company in a commercial or legal dispute with a foreign government or partner), "company_problem" (a company reports trouble, losses, barriers, or plans to leave), "deal_news" (a contract, investment or sale announced or awarded), "procurement_plan" (a country plans large purchases or projects, e.g. power plants, aircraft, rail), "export_control" (end-use or post-shipment checks), "newsletter", "other".
"companies": list of objects, one per company named, with "name" (company name as written), "role" ("helped", "in_dispute", "in_trouble", "won", "lost", "competitor", "mentioned"), "usd_millions" (number or null, the money at stake for that company), "outcome" ("won", "lost", "pending", "none").
"sectors": list of short sector words (e.g. "aircraft", "nuclear", "oil", "telecom", "pharma", "defense", "power", "rail").
"summary": one sentence.

CABLE:
"""
def texto(x):
    b = x['body']; i = b.find('SUBJECT'); b = b[i:] if i >= 0 else b
    return re.sub(r'\s+', ' ', b)[:7000]
import torch
cap = torch.cuda.get_device_capability(0); print('placa', torch.cuda.get_device_name(0), cap, flush=True)
if False:   # vLLM se rompe al instalarse con torch ya cargado (09-11)
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'vllm'], check=False)
    from vllm import LLM, SamplingParams
    llm = LLM(model='Qwen/Qwen2.5-7B-Instruct-AWQ', quantization='awq', dtype='half', max_model_len=4096, gpu_memory_utilization=0.92)
    tok = llm.get_tokenizer(); MOD = 'Qwen2.5-7B-Instruct-AWQ'
    prom = [tok.apply_chat_template([{'role': 'user', 'content': P + texto(x)}], tokenize=False, add_generation_prompt=True) for x in L]
    textos = [o.outputs[0].text for o in llm.generate(prom, SamplingParams(temperature=0, max_tokens=600))]
else:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    MOD = 'Qwen/Qwen2.5-3B-Instruct'; tok = AutoTokenizer.from_pretrained(MOD, padding_side='left')
    mod = AutoModelForCausalLM.from_pretrained(MOD, dtype=torch.float16, device_map='cuda').eval()
    prom = [tok.apply_chat_template([{'role': 'user', 'content': P + texto(x)[:5000]}], tokenize=False, add_generation_prompt=True) for x in L]
    orden = sorted(range(len(prom)), key=lambda i: len(prom[i])); textos = [None] * len(prom)
    for k in range(0, len(orden), 8):
        ii = orden[k:k + 8]; e = tok([prom[i] for i in ii], return_tensors='pt', padding=True).to('cuda')
        with torch.no_grad(): g = mod.generate(**e, max_new_tokens=450, do_sample=False, pad_token_id=tok.eos_token_id)
        for i, row in zip(ii, g): textos[i] = tok.decode(row[e['input_ids'].shape[1]:], skip_special_tokens=True)
        if k % 80 == 0: print(f'  {k}/{len(orden)} {time.time() - t0:.0f}s', flush=True)
print('modelo', MOD, flush=True)
with open('lectura.jsonl', 'w', encoding='utf-8') as f:
    for x, r in zip(L, textos):
        m = re.search(r'\{.*\}', r, re.S)
        try: j = json.loads(m.group(0)) if m else None
        except Exception: j = None
        f.write(json.dumps({'cable_id': x['cable_id'], 'datetime': x['datetime'], 'origin': x['origin'], 'lectura': j, 'crudo': None if j else r[:1500]}) + '\n')
print('LISTO', len(L), f'{time.time() - t0:.0f}s', flush=True)
