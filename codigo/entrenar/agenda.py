"""Señal #59 (notas/11): la agenda marca la dirección. Temas de Bilderberg (2008-2026) → sector → rendimiento después.
Uso: python agenda.py CARPETA_FOROS [salida.json]
Temas y sectores FIJADOS el 7-nov-2026 antes de bajar precios. Precio = fondo cotizado (ETF) del sector, mensual, Yahoo.
Control = SPY. Ventana: desde el cierre de junio del año de la reunión (las reuniones son mayo-junio)."""
import sys, re, glob, json, html, time, urllib.request
import numpy as np

# tema: (patrón en la agenda, fondo del sector). Lista cerrada: no se agrega ni se saca nada después de ver precios.
TEMAS = {
    'defensa':    (r'defen[cs]e|nato|warfare|weapon|military|deterren|proliferation|nuclear|arctic security', 'ITA'),
    'ciber':      (r'cyber', 'HACK'),
    'tecnologia': (r'artificial intelligence|\bai\b|big data|quantum|technolog|social network|digital|tech competition', 'SOXX'),
    'energia':    (r'energy|oil|commodit|critical minerals', 'XLE'),
    'clima':      (r'climate|kyoto|sustainability|global cooling|energy transition', 'ICLN'),
    'finanzas':   (r'financ|bank|debt|austerity|budget|fiscal', 'XLF'),
    'salud':      (r'medical|health|biology|pandemic', 'XLV'),
    'china':      (r'china|sino', 'FXI'),
    'europa':     (r'europ|\beuro\b|brexit|greece|united kingdom', 'VGK'),
    'india':      (r'india\b|indo-pacific', 'INDA'),
    'emergentes': (r'emerging|africa', 'EEM'),
    'oriente':    (r'middle east|iran|saudi|iraq|near east', 'KSA'),
}
UA = {'User-Agent': 'inteligencia-economica research contacto@inteligencia-economica.local'}

def agenda(carpeta):
    out = {}
    for p in sorted(glob.glob(f'{carpeta}/tema-*.html')):
        y = int(re.search(r'tema-(\d{4})', p).group(1))
        s = open(p, 'rb').read().decode('utf-8', 'ignore')
        t = html.unescape(re.sub(r'<[^>]+>', '\n', re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S))).replace('\xa0', ' ')
        L = [x.strip() for x in t.split('\n') if x.strip()]
        i = next((k for k, x in enumerate(L) if re.search(r'key topics|topics for discussion|deal mainly|topics include', x, re.I)), None)
        if i is None:
            continue
        bloque = []
        for x in L[i:i + 20]:
            if x.startswith('Founded in 1954') or x.startswith('Bilderberg takes its name') or x.startswith('Approximately'):
                break
            bloque.append(x)
        txt = ' | '.join(bloque).lower()
        txt = re.sub(r'(will be held in|meeting will be held).*?(deal mainly with)', ' ', txt)
        out[y] = sorted(k for k, (pat, _) in TEMAS.items() if re.search(pat, txt))
    return out

def mensual(sym):
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1mo&period1=946684800&period2={int(time.time())}'
    for _ in range(3):
        try:
            d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read())['chart']['result'][0]
            ts = d['timestamp']; c = d['indicators']['adjclose'][0]['adjclose']
            return {time.gmtime(a).tm_year * 12 + time.gmtime(a).tm_mon - 1: v for a, v in zip(ts, c) if v}
        except Exception:
            time.sleep(3)
    return {}

if __name__ == '__main__':
    salida = sys.argv[2] if len(sys.argv) > 2 else 'agenda.json'
    A = agenda(sys.argv[1])
    print('AGENDA', {y: v for y, v in A.items()}, flush=True)
    P = {k: mensual(f) for k, (_, f) in TEMAS.items()}; spy = mensual('SPY')
    print('PRECIOS', {k: (min(v) // 12 if v else None) for k, v in P.items()}, flush=True)
    def exceso(k, m0, h):
        p, q = P[k], spy
        if m0 in p and m0 + h in p and m0 in q and m0 + h in q:
            return np.log(p[m0 + h] / p[m0]) - np.log(q[m0 + h] / q[m0])
        return None
    res = {'agenda': A, 'h': {}}
    for h in (12, 36):
        filas = []
        for y in sorted(A):
            m0 = y * 12 + 5                                    # cierre de junio
            previos = set().union(*[set(A.get(y - d, [])) for d in (1, 2)]) if any(y - d in A for d in (1, 2)) else None
            on, nuevo, off = [], [], []
            for k in TEMAS:
                e = exceso(k, m0, h)
                if e is None:
                    continue
                if k in A[y]:
                    on.append(e)
                    if previos is not None and k not in previos:
                        nuevo.append(e)
                else:
                    off.append(e)
            if on and off:
                filas.append({'anio': y, 'on': float(np.mean(on)), 'off': float(np.mean(off)), 'dif': float(np.mean(on) - np.mean(off)),
                              'nuevo': float(np.mean(nuevo) - np.mean(off)) if nuevo else None, 'n_on': len(on), 'n_off': len(off), 'n_nuevo': len(nuevo)})
        g = np.random.default_rng(0)
        r = {'por_anio': filas}
        for clave in ('dif', 'nuevo'):
            v = np.array([f[clave] for f in filas if f[clave] is not None])
            if len(v):
                b = [g.choice(v, len(v)).mean() for _ in range(2000)]
                lo, hi = np.percentile(b, [2.5, 97.5])
                r[clave] = {'media': round(float(v.mean()), 4), 'ic95': [round(float(lo), 4), round(float(hi), 4)],
                            'anios_positivos': f'{int((v > 0).sum())} de {len(v)}', 'frac_pos': float((v > 0).mean())}
                r[clave]['pasa'] = bool(lo > 0 and (v > 0).mean() >= 0.7)
        res['h'][h] = r
        for f in filas:
            print(f'AGENDA h{h} {f["anio"]} | en agenda {f["on"]:+.3f} ({f["n_on"]}) | fuera {f["off"]:+.3f} ({f["n_off"]}) | dif {f["dif"]:+.3f} | '
                  f'nuevos {"" if f["nuevo"] is None else f"{f["nuevo"]:+.3f}"} ({f["n_nuevo"]})', flush=True)
        print(f'CRITERIO h{h}: todos {r.get("dif")} | nuevos {r.get("nuevo")}', flush=True)
    json.dump(res, open(salida, 'w'), indent=1)
