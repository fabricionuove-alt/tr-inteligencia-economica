"""#62 (notas/11): empresas alineadas con el consenso de la élite. EXPLORACIÓN en 10-K presentados 2013-2016;
los de 2017-2020 quedan sin mirar hasta que el criterio esté escrito (CONFIRMAR=1 los abre).
Uso: python alineacion.py filas.csv TEMA10K_CSVS consenso_anual.csv [salida.json]
Puntaje de la empresa = Σ_tema (coincidencias del tema por mil palabras de «el negocio») × consenso del tema ese año."""
import sys, os, json
import numpy as np, pandas as pd
CONF = os.environ.get('CONFIRMAR') == '1'
ANIOS = list(range(2017, 2021)) if CONF else list(range(2013, 2017))
salida = sys.argv[4] if len(sys.argv) > 4 else ('alineacion_confirmar.json' if CONF else 'alineacion_explorar.json')
df = pd.read_csv(sys.argv[1], usecols=lambda c: c in ('id', 'anio', 'sector', 'log_activos', '_presentado', '_ret1', '_ret4', '_ret6', 'estado_final'),
                 dtype={'id': str}, low_memory=False)
df['pres'] = pd.to_numeric(df['_presentado'].astype(str).str[:4], errors='coerce')
T = pd.concat([pd.read_csv(x, dtype={'id': str}) for x in sys.argv[2].split(',') if x]).drop_duplicates(['id', 'anio_presentado'])
K = pd.read_csv(sys.argv[3])
temas = [c for c in T.columns if c.startswith(('b_', 't_'))]
d = df.merge(T, left_on=['id', 'pres'], right_on=['id', 'anio_presentado'], how='inner')
d = d[d['anio_presentado'].isin(ANIOS) & (d['palabras'] >= 300)].copy()
ult = df.groupby('id')['anio'].max()
for c in ('_ret1', '_ret4', '_ret6'):
    d[c] = pd.to_numeric(d[c], errors='coerce')
print(f'ALIN filas unidas {len(d)} | años {sorted(d["anio_presentado"].unique())} | {"CONFIRMACIÓN" if CONF else "EXPLORACIÓN"}', flush=True)
peso = {(a, t): c for a, t, c in zip(K['anio'], K['tema'], K['consenso'])}
dens = d[temas].div(d['palabras'], axis=0) * 1000
d['alin'] = sum(dens[t] * d['anio_presentado'].map(lambda a, t=t: peso.get((a, t), 0)) for t in temas)
d['alin_alta'] = sum(dens[t] * d['anio_presentado'].map(lambda a, t=t: float(peso.get((a, t), 0) >= 4)) for t in temas)
d['tema_total'] = dens.sum(axis=1)                              # control: hablar de cualquier tema, sin el consenso
d['tam'] = pd.to_numeric(d['log_activos'], errors='coerce').groupby(d['anio_presentado']).rank(pct=True)
g = d.groupby(['anio_presentado', 'sector'])
for c in ('alin', 'alin_alta', 'tema_total'):
    d[c + '_p'] = g[c].rank(pct=True)                           # dentro del sector y del año
res = {'modo': 'confirmar' if CONF else 'explorar', 'n': int(len(d)), 'por': {}}
for h, c in (('12m', '_ret1'), ('4a', '_ret4'), ('6a', '_ret6')):
    x = d.dropna(subset=[c]).copy()
    x['lr'] = np.log(x[c].clip(lower=0.01))
    x['ex'] = x['lr'] - x.groupby(['anio_presentado', 'sector'])['lr'].transform('median')     # contra su sector ese año
    for var in ('alin_p', 'alin_alta_p', 'tema_total_p'):
        q = pd.cut(x[var], [0, .2, .4, .6, .8, .9, 1.0], include_lowest=True, labels=['0-20', '20-40', '40-60', '60-80', '80-90', '90-100'])
        t = x.groupby(q, observed=True).agg(n=('ex', 'size'), exceso=('ex', 'mean'), x2=(c, lambda s: (s >= 2).mean()), des=(c, lambda s: (s <= 0.5).mean()))
        pa = x.assign(q=q).groupby(['anio_presentado', 'q'], observed=True)['ex'].mean().unstack()
        dif = (pa['90-100'] - pa['0-20']) if '90-100' in pa and '0-20' in pa else pd.Series(dtype=float)
        res['por'][f'{h}_{var}'] = {'tabla': t.round(4).reset_index().astype(str).to_dict('records'), 'arriba_menos_abajo_por_anio': dif.round(4).to_dict()}
        print(f'ALIN {h} {var:13s} | ' + ' | '.join(f'{i}: ex {r.exceso:+.3f} x2 {r.x2:.3f} des {r.des:.3f} (n {r.n})' for i, r in t.iterrows()) +
              f' || 90-100 menos 0-20 por año {dif.round(3).to_dict()}', flush=True)
# criterio de #62 (escrito antes de abrir 2017-2020)
x = d.dropna(subset=['_ret4']).copy(); x['lr'] = np.log(x['_ret4'].clip(lower=0.01))
x['ter'] = pd.cut(x['tam'], [0, 1/3, 2/3, 1], include_lowest=True, labels=False)
crit = {}
GR = [('sector', ['anio_presentado', 'sector']), ('sector_tamano', ['anio_presentado', 'sector', 'ter'])]
if os.environ.get('SIC') and os.path.exists(os.environ['SIC']):
    sic = pd.read_csv(os.environ['SIC'], dtype={'id': str, 'sic': str}).drop_duplicates('id')
    x = x.merge(sic, on='id', how='left'); x['sic3'] = x['sic'].str[:3]; x['sic2'] = x['sic'].str[:2]
    x = x[x.groupby(['anio_presentado', 'sic3'])['id'].transform('size') >= 8]
    print(f'SIC unidos {x["sic3"].notna().sum()} de {len(x)}', flush=True)
    GR += [('sic2', ['anio_presentado', 'sic2']), ('sic3', ['anio_presentado', 'sic3']), ('sic3_tamano', ['anio_presentado', 'sic3', 'ter'])]
for nombre, grupo in GR:
    xx = x.copy(); xx['ex'] = xx['lr'] - xx.groupby(grupo)['lr'].transform('median'); xx['p'] = xx.groupby(grupo)['tema_total'].rank(pct=True)
    ar, ab = xx[xx['p'] > 0.9], xx[xx['p'] <= 0.2]
    dif = ar.groupby('anio_presentado')['ex'].mean() - ab.groupby('anio_presentado')['ex'].mean()
    des = ar.groupby('anio_presentado')['_ret4'].apply(lambda s: (s <= 0.5).mean()) - ab.groupby('anio_presentado')['_ret4'].apply(lambda s: (s <= 0.5).mean())
    crit[nombre] = {'dif_por_anio': dif.round(4).to_dict(), 'media': round(float(dif.mean()), 4), 'positivos': int((dif > 0).sum()), 'des_por_anio': des.round(4).to_dict(), 'menos_des': int((des < 0).sum())}
    print(f'CRITERIO62 {nombre}: dif {crit[nombre]["dif_por_anio"]} media {crit[nombre]["media"]} | desastres arriba-abajo {crit[nombre]["des_por_anio"]}', flush=True)
n = len(crit['sector']['dif_por_anio'])
crit['pasa'] = bool(crit['sector']['positivos'] >= 3 and crit['sector']['media'] > 0 and crit['sector_tamano']['positivos'] >= 3 and crit['sector']['menos_des'] >= 3 and n == 4)
print('CRITERIO62 pasa:', crit['pasa'], flush=True); res['criterio'] = crit
json.dump(res, open(salida, 'w'), indent=1, default=str)
