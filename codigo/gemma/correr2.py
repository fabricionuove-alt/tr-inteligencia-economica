import subprocess, sys, os, zipfile, glob
os.chdir('/content/w'); os.environ['QUIERO'] = '/content/w/quiero.txt'
for a in sys.argv[1].split(','):
    subprocess.run([sys.executable, 'gemma_sae2.py', a], check=False)
    with zipfile.ZipFile(f'/content/sae2-{a}.zip', 'w') as z:
        for f in glob.glob(f'sae2-{a}-*'): z.write(f)
    print('LISTO ZIP', a, flush=True)
