"""¿Qué IA abierta distingue franqueza de verso? Sólo controles escritos a mano (no mira datos reales).
Uso: python llm_controles.py
Pasa un modelo si TODOS los francos sacan más que TODOS los vagos."""
import time, re, torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import llm_franqueza as L

FRANCOS = [L.CONTROL_FRANCO,
           ("Sales declined 9% to $1.1 billion. We misjudged demand in China and were left with $80 million of excess "
            "inventory, which we wrote down. Operating margin fell to 6% from 11%. Our new product launched six months "
            "late because of our own engineering problems, not supply issues. We replaced the head of that division. ") * 6,
           ("Same-store sales fell 4%. Traffic was down 7% and we raised prices 3%, which customers did not accept well. "
            "We closed 42 stores that lost money and took a $35 million charge. Debt rose to $640 million; interest now "
            "takes 19% of our operating income. We will not buy back stock until debt is below $400 million. ") * 6]
VAGOS = [L.CONTROL_VAGO,
         ("Fiscal year was a period of transformation and momentum. The Company continued to execute on its strategic "
          "priorities, leveraging its differentiated capabilities and best-in-class talent to unlock long-term value. "
          "Headwinds in certain markets were offset by robust demand trends and operational excellence initiatives. ") * 6,
         ("Management is excited about the exceptional opportunities ahead. Our world-class portfolio and innovative "
          "culture position the Company for sustainable, profitable growth. While the environment remained dynamic, "
          "the Company delivered solid results and remains confident in its ability to create value going forward. ") * 6]
MODELOS = [('Qwen/Qwen2.5-3B-Instruct', None), ('Qwen/Qwen2.5-7B-Instruct', '4bit')]

for nombre, cuant in MODELOS:
    t0 = time.time()
    try:
        tok = AutoTokenizer.from_pretrained(nombre); tok.padding_side = 'left'
        kw = {'device_map': 'cuda'}
        if cuant == '4bit':
            kw['quantization_config'] = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
        else:
            kw['dtype'] = torch.float16
        mod = AutoModelForCausalLM.from_pretrained(nombre, **kw)
    except Exception as e:
        print(nombre, 'NO CARGA', type(e).__name__, str(e)[:120], flush=True); continue
    def nota(t):
        m = tok.apply_chat_template([{'role': 'user', 'content': L.PROMPT + t}], tokenize=False, add_generation_prompt=True)
        e = tok([m], return_tensors='pt').to('cuda')
        with torch.no_grad():
            o = mod.generate(**e, max_new_tokens=3, do_sample=False, pad_token_id=tok.eos_token_id)
        s = tok.decode(o[0, e['input_ids'].shape[1]:], skip_special_tokens=True)
        n = re.findall(r'\d+', s); return int(n[0]) if n else None
    t1 = time.time()
    f = [nota(t) for t in FRANCOS]; v = [nota(t) for t in VAGOS]
    seg = (time.time() - t1) / 6
    ok = all(x is not None for x in f + v) and min(f) > max(v)
    print(f'{nombre} ({cuant or "fp16"}): francos {f}  vagos {v}  -> {"PASA" if ok else "no pasa"}  '
          f'({seg:.2f} s por texto, carga {t1-t0:.0f}s)', flush=True)
    del mod; torch.cuda.empty_cache()
