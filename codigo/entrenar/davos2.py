"""Señal #61 (notas/11): proyectos de Davos tecnología por tecnología. Uso: python davos2.py tecnologias.csv [salida.json]"""
import sys, re, json, csv, collections
import numpy as np
from agenda import mensual
CAT = {'baterias': (r'batter', 'LIT'), 'nuclear': (r'nuclear', 'NLR'),
       'genomica': (r'genom|gene|crispr|dna|cell atlas|omics|metabolic engineering|phage|living therapeutic', 'ARKG'),
       'farmacos': (r'drug|vaccin|protein|glp-1|nanozym|ageing|aging|therapeut', 'XPH'),
       'diagnostico': (r'biopsy|diagnos|microneedle|biomarker|breath|sensing|organs-on-chips|virtual patient|digital medicine|healthcare|neural electronic|optogenet|transplant', 'IHI'),
       'robotica': (r'robot', 'BOTZ'), 'ia': (r'artificial intelligence|\bai\b|deep learning|neuromorphic|machine|watermark|privacy', 'AIQ'),
       'cuantica': (r'quantum', 'QTUM'), 'chips': (r'sensor|lens|chip|2d material|nanosensor|surfaces|computing', 'SOXX'),
       'espacio': (r'space|satellite|drone|aviation|high altitude|aircraft', 'ITA'), 'solar': (r'solar|sun|perovskite|sunshine', 'TAN'),
       'hidrogeno': (r'hydrogen|fuel cell|ammonia|aviation fuel|catalyst', 'ICLN'), 'autos': (r'vehicle|autonomous vehicle', 'DRIV'),
       'blockchain': (r'blockchain', 'BLOK'), 'manufactura': (r'additive|manufactur|printed', 'PRNT'),
       'agro': (r'farm|crop|fertil|livestock|food|nitrogen', 'MOO'), 'agua': (r'water', 'PHO'),
       'construccion': (r'cement|houses|built world|communities', 'PKB'),
       'materiales': (r'plastic|bioplastic|thermoset|material|elastocal|composite', 'XLB'),
       'comunicaciones': (r'wireless|telepresence|communication|connects the globe|internet of nanothings', 'IYZ'),
       'realidad_virtual': (r'metaverse|immersive|spatial computing|virtual', 'METV'),
       'carbono': (r'carbon|decarboni|osmotic|renewable energy|storage of renewable', 'ICLN')}
def principal():
    A = collections.defaultdict(set); anios = set()
    for f in csv.DictReader(open(sys.argv[1], encoding='utf-8')):
        y = int(f['anio']); anios.add(y)
        for k, (p, _) in CAT.items():
            if re.search(p, f['tecnologia'].lower()):
                A[y].add(k)
    anios = sorted(anios)
    for y in anios: print('LISTA', y, sorted(A[y]), flush=True)
    P = {f: mensual(f) for f in {fd for _, fd in CAT.values()}}; spy = mensual('SPY')
    print('DESDE', {k: (min(P[fd]) // 12 if P[fd] else None) for k, (_, fd) in CAT.items()}, flush=True)
    def exceso(k, m0, h):
        p = P[CAT[k][1]]
        if all(m in p for m in (m0, m0 + h)) and all(m in spy for m in (m0, m0 + h)):
            return float(np.log(p[m0 + h] / p[m0]) - np.log(spy[m0 + h] / spy[m0]))
    res = {'listas': {y: sorted(A[y]) for y in anios}, 'h': {}}
    g = np.random.default_rng(0)
    for h in (12, 36):
        filas, cats = [], collections.defaultdict(lambda: {'on': [], 'off': []})
        for y in anios:
            on, off = [], []
            for k in CAT:
                e = exceso(k, y * 12 + 5, h)
                if e is None: continue
                (on if k in A[y] else off).append(e); cats[k]['on' if k in A[y] else 'off'].append(e)
            if on and off:
                filas.append({'anio': y, 'dif': float(np.mean(on) - np.mean(off)), 'n_on': len(on), 'n_off': len(off)})
                print(f'TEC h{h} {y} | en lista {np.mean(on):+.3f} ({len(on)}) | fuera {np.mean(off):+.3f} ({len(off)}) | dif {np.mean(on) - np.mean(off):+.3f}', flush=True)
        v = np.array([f['dif'] for f in filas])
        lo, hi = np.percentile([g.choice(v, len(v)).mean() for _ in range(2000)], [2.5, 97.5])
        c1 = bool(lo > 0 and (v > 0).mean() >= 0.7)
        dentro = {k: float(np.mean(d['on']) - np.mean(d['off'])) for k, d in cats.items() if d['on'] and d['off']}
        dv = np.array(list(dentro.values()))
        c2 = bool(len(dv) and dv.mean() > 0 and (dv > 0).mean() > 0.5)
        res['h'][h] = {'por_anio': filas, 'entre': {'media': round(float(v.mean()), 4), 'ic95': [round(float(lo), 4), round(float(hi), 4)], 'positivos': f'{int((v > 0).sum())} de {len(v)}', 'cumple': c1},
                       'dentro': {'por_categoria': {k: round(x, 4) for k, x in sorted(dentro.items(), key=lambda t: -t[1])}, 'media': round(float(dv.mean()), 4) if len(dv) else None,
                                  'positivas': f'{int((dv > 0).sum())} de {len(dv)}', 'cumple': c2}, 'pasa': c1 and c2}
        r = res['h'][h]
        print(f'CRITERIO h{h}: entre {r["entre"]} | dentro media {r["dentro"]["media"]} positivas {r["dentro"]["positivas"]} {r["dentro"]["por_categoria"]} -> {"PASA" if r["pasa"] else "no pasa"}', flush=True)
    json.dump(res, open(sys.argv[2] if len(sys.argv) > 2 else 'davos2.json', 'w'), indent=1)

if __name__ == '__main__':
    principal()
