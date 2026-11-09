"""#89: puntaje de agenda por empresa y su prueba. python agenda_eval.py CARPETA_AGENDA"""
import sys, json, numpy as np, pandas as pd
from scipy import sparse
B = 'E:/FABRI INFLUENCIA/inteligencia-economica/entrenar'; A = sys.argv[1]
ids = np.load(f'{A}/sae2a-agenda-ids.npy'); X = sparse.load_npz(f'{A}/sae2a-agenda-L12.npz').toarray()
X[~np.isfinite(X)] = 0; X = np.log1p(np.clip(X, 0, None))
k = pd.DataFrame([i.split('|') for i in ids], columns=['fu', 'a', 'k']); k['a'] = k['a'].astype(int)
V = {(f, a): X[g.index].mean(0) for (f, a), g in k.groupby(['fu', 'a'])}
def agenda(f, a):
    if (f, a) not in V: return None
    prev = [V[(f, b)] for b in (a - 1, a - 2) if (f, b) in V]
    return V[(f, a)] - np.mean(prev, 0) if prev else None
et = pd.read_csv(f'{B}/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et['anio_presentado'] = et['anio_presentado'].astype(int); et = et.drop_duplicates(['id', 'anio_presentado'])
FU = sorted({f for f, _ in V}); filas = []
for y in range(2021, 2025):
    i = np.load(f'{B}/sal-anon2124/sae2a-textos-{y}-ids.npy'); Z = sparse.load_npz(f'{B}/sal-anon2124/sae2a-textos-{y}-L12.npz').toarray()
    malo = ~np.isfinite(Z).all(1); Z[~np.isfinite(Z)] = 0; Z = np.log1p(np.clip(Z, 0, None)); Z = Z - Z[~malo].mean(0)
    n = np.linalg.norm(Z, axis=1) + 1e-9
    d = pd.DataFrame({'id': i, 'anio_presentado': y, 'malo': malo})
    for f in FU:
        for nom, ya in (('', y - 1), ('_pl', y - 5)):                       # agenda del año anterior al 10-K; placebo: 4 años antes
            v = agenda(f, ya)
            d[f + nom] = np.nan if v is None else (Z @ v) / n / (np.linalg.norm(v) + 1e-9)
    filas.append(d)
d = pd.concat(filas, ignore_index=True); d = d[~d['malo']].merge(et, on=['id', 'anio_presentado'], how='left')
for f in FU:
    for nom in ('', '_pl'):
        d[f + nom] = d.groupby('anio_presentado')[f + nom].rank(pct=True)
d['agenda'] = d[FU].mean(1); d['agenda_pl'] = d[[f + '_pl' for f in FU]].mean(1)
d['r4'] = pd.to_numeric(d['_ret4'], errors='coerce'); d['r4b'] = pd.to_numeric(d['_ret4'], errors='coerce'); d['sic3'] = d['sic'].str[:3]
d['ter'] = pd.cut(d['tam'], [0, 1/3, 2/3, 1], include_lowest=True, labels=False); g = ['anio_presentado', 'sic3', 'ter']
ok = d['r4'].notna() & d['sic'].notna() & d['tam'].notna(); d = d[ok].copy(); d = d[d.groupby(g)['id'].transform('size') >= 5]
d['lr'] = np.log(d['r4'].clip(lower=0.01)); d['ex'] = d['lr'] - d.groupby(g)['lr'].transform('median')
def prueba(col):
    x = d.dropna(subset=[col]).copy(); x['p'] = x.groupby(g)[col].rank(pct=True)
    ar, ab = x[x['p'] > 0.9], x[x['p'] <= 0.2]
    dif = (ar.groupby('anio_presentado')['ex'].mean() - ab.groupby('anio_presentado')['ex'].mean()).round(3)
    des = (ar.groupby('anio_presentado')['r4'].apply(lambda s: (s <= .5).mean()) - ab.groupby('anio_presentado')['r4'].apply(lambda s: (s <= .5).mean())).round(3)
    return dif, des
R = {}
for col in ['agenda', 'agenda_pl'] + FU + [f + '_pl' for f in FU]:
    dif, des = prueba(col); e, c = dif[dif.index <= 2020], dif[dif.index >= 2021]
    R[col] = {'dif': dif.to_dict(), 'des': des.to_dict(), 'expl': round(e.mean(), 3), 'conf': round(c.mean(), 3), 'conf_pos': int((c > 0).sum())}
    print(f'AG91 {col:22s} exploración {e.mean():+.3f} | confirmación {c.mean():+.3f} ({(c > 0).sum()} de {len(c)} +) | por año {dif.to_dict()} | desastres {des.to_dict()}', flush=True)
a, p = R['agenda'], R['agenda_pl']
neg = sum(v < 0 for k, v in a['dif'].items()); pasa = a['conf'] <= -0.05 and neg >= 3 and a['conf'] < p['conf']
try:
    gp = pd.read_csv(f'{B}/ds-temas/gemma_puntaje.csv', dtype={'id': str}); m = d.merge(gp, on=['id', 'anio_presentado'])
    print('AG91 correlación con Gemma #68:', round(m[['agenda', m.columns[-1]]].corr(method='spearman').iloc[0, 1], 3), flush=True)
except Exception as e: print('AG91 sin correlación', e)
print(f'CRITERIO91 años negativos {neg} de 4 | confirmación {a["conf"]:+.3f} ({a["conf_pos"]} de 4 +), exploración {a["expl"]:+.3f}, placebo {p["conf"]:+.3f} -> {"PASA" if pasa else "no pasa"}', flush=True)
d[['id', 'anio_presentado', 'agenda']].to_csv(f'{A}/agenda91r4_puntaje.csv', index=False); json.dump(R, open(f'{A}/agenda91r4_resultados.json', 'w'), indent=1, default=str)
