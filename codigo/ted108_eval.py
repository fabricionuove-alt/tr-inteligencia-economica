"""#108: empresas que ganan contratos públicos en Europa (TED), contra el rendimiento a 4 años del 10-K siguiente. python ted108_eval.py"""
import sys, numpy as np, pandas as pd
B = 'E:/FABRI INFLUENCIA/inteligencia-economica'; rng = np.random.default_rng(0)
src = open(f'{B}/entrenar/cab102_eval.py', encoding='utf-8').read(); exec(src[:src.index('filas = []')])  # madre(), igual que #102
a = pd.read_csv(f'{B}/fuentes/ted/adjudicaciones.csv', dtype=str, keep_default_na=False)
a = a[a['CANCELLED'] != '1']; a['Y'] = pd.to_numeric(a['YEAR'], errors='coerce'); a['eur'] = pd.to_numeric(a['AWARD_VALUE_EURO'], errors='coerce')
print('adjudicaciones con ganador', len(a), a.groupby('Y').size().to_dict(), flush=True)
un = pd.Series(a['WIN_NAME'].unique()); mp = dict(zip(un, un.map(madre))); a['id'] = a['WIN_NAME'].map(mp)
m = a.dropna(subset=['id']); print('con empresa del dataset', len(m), 'empresas', m['id'].nunique(), flush=True)
top = m.groupby('WIN_NAME').size().sort_values(ascending=False).head(40); print(top.to_dict(), flush=True)
s = m.groupby(['id', 'Y']).agg(n=('eur', 'size'), eur=('eur', 'sum')).reset_index(); s['ap'] = s['Y'].astype(int) + 1
gan = set(zip(s['id'], s['Y']))
s['primera'] = [all((i, y - k) not in gan for k in (1, 2, 3)) for i, y in zip(s['id'], s['Y'])]
et2 = pd.read_csv(f'{B}/entrenar/colab-sae/etiquetas.csv', dtype={'id': str, 'sic': str}).dropna(subset=['anio_presentado'])
et2['ap'] = et2['anio_presentado'].astype(int)
x = et2.drop_duplicates(['id', 'ap']).copy(); x['r'] = pd.to_numeric(x['_ret4'], errors='coerce'); x = x.dropna(subset=['r', 'sic', 'tam'])
x['sic3'] = x['sic'].str[:3]; x['ter'] = pd.cut(x['tam'], [0, 1/3, 2/3, 1], include_lowest=True, labels=False); g = ['ap', 'sic3', 'ter']
x = x[x.groupby(g)['id'].transform('size') >= 5].copy(); x['lr'] = np.log(x['r'].clip(lower=0.01))
x = x.merge(s[['id', 'ap', 'n', 'eur', 'primera']], on=['id', 'ap'], how='left'); x['ted'] = x['n'].fillna(0) > 0
x['med_sin'] = x[~x['ted']].groupby(g)['lr'].transform('median'); x['med_sin'] = x.groupby(g)['med_sin'].transform('max'); x['ex2'] = x['lr'] - x['med_sin']
x = x.dropna(subset=['ex2']); x['gid'] = x.groupby(g).ngroup()
def tramo(z, nomb):
    f = z[z['ted']]; obs = f['ex2'].mean()
    lab = z['ted'].values; gid = z['gid'].values; idx = [np.where(gid == k)[0] for k in np.unique(gid)]; ex = z['ex2'].values; perm = []
    for _ in range(2000):
        l2 = lab.copy()
        for ii in idx: l2[ii] = rng.permutation(l2[ii])
        perm.append(ex[l2].mean())
    p = (np.sum(np.array(perm) >= obs) + 1) / 2001
    print(f'TED108 {nomb:28s} n {len(f):5d} exceso {obs:+.3f} mediana {f["ex2"].median():+.3f} p {p:.4f} hundidas {(f["r"] <= .5).mean():.3f} (todas {(z["r"] <= .5).mean():.3f})', flush=True)
    return obs, p
E = x[(x.ap >= 2010) & (x.ap <= 2016)]; C = x[(x.ap >= 2017) & (x.ap <= 2020)]; N = x[x.ap >= 2021]
print('TED108 por año', x[x['ted']].groupby('ap')['ex2'].agg(['size', 'mean']).round(3).to_dict('index'), flush=True)
e, _ = tramo(E, 'exploración 2010-2016'); c, pc = tramo(C, 'confirmación 2017-2020'); n, _ = tramo(N, 'nunca usados 2021-2022')
f = x[x['ted'] & (x.ap >= 2010)]
for nomb, z in (('primera vez', f[f['primera'] == True]), ('ganan seguido', f[f['primera'] == False]), ('>= 10M euros', f[f['eur'] >= 1e7]), ('< 10M euros', f[f['eur'] < 1e7])):
    print(f'TED108 {nomb:28s} n {len(z):5d} exceso {z["ex2"].mean():+.3f}', flush=True)
print(f'TED108 alcance: empresas-año del dataset con TED {x["ted"].sum()} de {len(x)} ({x["ted"].mean():.3%})', flush=True)
print(f'CRITERIO108 confirmación {c:+.3f} (p {pc:.4f}) exploración {e:+.3f} nunca usados {n:+.3f} -> {"PASA" if c >= .05 and pc < .05 and e > 0 and n > 0 else "no pasa"}', flush=True)
x[x['ted']][['id', 'ap', 'n', 'eur', 'primera', 'r', 'ex2']].to_csv(f'{B}/entrenar/sal-cab102/ted108_filas.csv', index=False)
