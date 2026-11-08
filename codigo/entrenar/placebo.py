"""Señal #51 (notas/11): placebo de Kelly. Baraja (P2, PD) dentro del decil de tamaño; 100 veces por camada.
Uso: python placebo.py filas.csv personas.csv FALLAS_CSVS [salida.json]"""
import sys, os, json
import numpy as np
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kelly.py'), encoding='utf-8').read()
exec(_src.split("res = {'camadas': {}}")[0])
salida = sys.argv[4] if len(sys.argv) > 4 else 'placebo.json'
N = 100
def cartera(w, r):
    return float((w * r).sum() + 1 - w.sum()), float(w[r <= 0.5].sum())
res = {'camadas': {}}
for s in range(2019, 2025):
    A = en & (anio <= s - 2)
    k = np.where((anio == s) & en)[0]
    if A.sum() < mA or len(k) < mc:
        print(f'PLACEBO {s}: no alcanza', flush=True); continue
    p2, pdes = ajustar(A, dobla, k), ajustar(A, desastre, k)
    r = r1[k]; t = tam[k].astype(float)
    dec = np.full(len(k), -1)
    ok = ~np.isnan(t)
    if ok.sum():
        dec[ok] = np.minimum((np.argsort(np.argsort(t[ok], kind='stable'), kind='stable') * 10) // ok.sum(), 9)
    ret_r, des_r = cartera(pesos(p2, pdes), r)
    rets, dess = [], []
    for sem in range(N):
        g = np.random.default_rng(sem); idx = np.arange(len(k))
        for d in np.unique(dec):
            m = np.where(dec == d)[0]; idx[m] = g.permutation(m)
        a, b = cartera(pesos(p2[idx], pdes[idx]), r)
        rets.append(a); dess.append(b)
    rets, dess = np.array(rets), np.array(dess)
    p95 = float(np.percentile(rets, 95))
    fila = {'real': round(ret_r, 4), 'placebo_mediana': round(float(np.median(rets)), 4), 'placebo_p95': round(p95, 4),
            'placebos_que_le_ganan': int((rets >= ret_r).sum()), 'des_real': round(100 * des_r, 2),
            'des_placebo_mediana': round(100 * float(np.median(dess)), 2), 'universo': round(float(r.mean()), 4), 'supera_p95': bool(ret_r > p95)}
    res['camadas'][s] = fila
    print(f'PLACEBO {s} | real ×{fila["real"]} | placebo mediana ×{fila["placebo_mediana"]} p95 ×{fila["placebo_p95"]} | '
          f'{fila["placebos_que_le_ganan"]}/{N} placebos le ganan | des real {fila["des_real"]}% vs placebo {fila["des_placebo_mediana"]}% | universo ×{fila["universo"]}', flush=True)
    json.dump(res, open(salida, 'w'), indent=1)
C = res['camadas']; n = len(C); c = sum(f['supera_p95'] for f in C.values())
res['criterio'] = {'camadas': n, 'supera_p95': f'{c} de {n}', 'sabe_algo': bool(n == 6 and c >= 5)}
print(f'CRITERIO placebo (#51): {res["criterio"]} -> {"LA MÁQUINA SABE ALGO" if res["criterio"]["sabe_algo"] else "es la inclinación a lo chico"} ({time.time() - t0:.0f}s)', flush=True)
json.dump(res, open(salida, 'w'), indent=1)
