"""#160 medir: concentradas contra pares. Reglas en notas/11 (#160)."""
import sys; sys.argv = ['x', 'A']
src = open('robusto146.py', encoding='utf-8').read().split("if modo == 'A':")[0]
src = src.replace("Xa, ya, _, _ = juntar(range(2013, 2017)); print('aprender', Xa.shape, flush=True)\n", '').replace("dfa = np.asarray((Xa > 0).sum(axis=0)).ravel() / Xa.shape[0]\n", '')
exec(src)
r1 = open('rinde149.py', encoding='utf-8').read(); exec(r1[r1.index('def rinde'):r1.index('Xp, yp, idp, anp = juntar')])
R = []
for y in range(2010, 2023):
    for l in open(f'{B}/clientes160/c_{y}.jsonl'):
        o = json.loads(l)
        if o['c'] is not None: R.append({'id': hs(int(o['cik'])), 'anio_presentado': y, 'pal': o['c'] + rng.random() * 1e-6})
d = pd.DataFrame(R).drop_duplicates(['id', 'anio_presentado'])
print('con texto', d.groupby('anio_presentado').size().to_dict()); print('% con concentración > 0', (d.groupby('anio_presentado')['pal'].apply(lambda v: (v > .001).mean() * 100)).round(1).to_dict(), flush=True)
A, N = range(2010, 2021), (2021, 2022); v = d[d.anio_presentado <= 2020]; w = d[d.anio_presentado >= 2021]
oa, pa, _ = prueba(v, A, 'A160 concentradas 2010-2020 hundidas (p = de hundirse MENOS)'); ob, pb = rinde(v, A, 'B160 concentradas 2010-2020 log r4 (p = de rendir MÁS)')
na, _, _ = prueba(w, N, 'A160 concentradas 2021-2022 hundidas'); nb, _ = rinde(w, N, 'B160 concentradas 2021-2022 log r4')
pa_mas, pb_menos = 1 - pa, 1 - pb
print(f'p de hundirse MÁS {pa_mas:.4f}; p de rendir MENOS {pb_menos:.4f}')
print('CRITERIO160', 'PASA' if oa >= 3 and pa_mas < .05 and ob < 0 and pb_menos < .05 and na > 0 and nb < 0 else 'no pasa')
