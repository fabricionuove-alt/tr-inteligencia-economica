import subprocess, sys, os
os.chdir('/content/w'); os.environ.update({'QUIERO': '/content/w/quiero.txt', 'ANON': '1', 'CAPAS': '12', 'N_TOK': '256', 'TOPK': '256'})
for a in sys.argv[1].split(','):
    subprocess.run([sys.executable, 'gemma_sae2.py', a], check=False)
os.environ.update({'PREFIJO': 'sae2a', 'SALIDA': 'gemma_anon'})
subprocess.run([sys.executable, 'sae_analisis2.py', '/content/w', 'etiquetas.csv', '12'], check=False)
