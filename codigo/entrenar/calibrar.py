"""Compara la franqueza medida con MI recorte de la sección 7 (bajar_10k.py) contra la del corpus, mismas empresas, 2020."""
import sys, glob
import pandas as pd
mio = pd.read_csv(sys.argv[1])
corpus = pd.concat([pd.read_csv(p) for p in glob.glob(sys.argv[2], recursive=True)])
corpus = corpus[corpus.anio_presentado == 2020]
m = mio.merge(corpus, on=['id', 'anio_presentado'], suffixes=('_mio', '_corpus'))
print('empresas en ambos:', len(m))
for c in ('franq_nosotros', 'franq_numeros', 'franq_largo', 'franq_niebla'):
    print(f'  {c}: correlación {m[c+"_mio"].corr(m[c+"_corpus"]):.3f}  (de rangos {m[c+"_mio"].corr(m[c+"_corpus"], method="spearman"):.3f})')
