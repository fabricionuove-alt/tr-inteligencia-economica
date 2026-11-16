"""Lista los conceptos de Gemma Scope con más peso en el puntaje de Tr/Rt (promesa de #65), con descripción de Neuronpedia."""
import json, time, urllib.request, numpy as np
m = np.load('sal-junto3/out/gemma_1_1A_7_modelo.npz'); u, c = m['usar'], m['coef']
SEC = ['negocio', 'riesgos', 'direccion']; o = np.argsort(c); out = []
def desc(f):
    try:
        j = json.loads(urllib.request.urlopen(f'https://www.neuronpedia.org/api/feature/gemma-2-2b/12-gemmascope-res-16k/{f}', timeout=30).read())
        e = j.get('explanations') or []; return e[0]['description'] if e else ''
    except Exception as ex: return f'(sin descripcion: {ex})'
for lado, ids in (('A FAVOR', o[::-1][:25]), ('EN CONTRA', o[:25])):
    print(lado, flush=True)
    for i in ids:
        f = int(u[i]); s, k = SEC[f // 16384], f % 16384; d = desc(k); time.sleep(.4)
        out.append({'lado': lado, 'seccion': s, 'concepto': k, 'peso': float(c[i]), 'descripcion': d})
        print(f'  {c[i]:+.4f} {s:9s} #{k:5d} {d}', flush=True)
json.dump(out, open('sal-cab102/conceptos136.json', 'w'), ensure_ascii=False, indent=1)
