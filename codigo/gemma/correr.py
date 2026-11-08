import subprocess, sys, os, shutil
os.chdir('/content/w')
for a in sys.argv[1].split(','):
    subprocess.run([sys.executable, 'gemma_sae.py', a] + sys.argv[2:3], check=False)
    if os.path.exists(f'sae-{a}.npz'):
        shutil.make_archive(f'/content/sae-{a}', 'zip', '.', '.', ) if False else None
        import zipfile
        with zipfile.ZipFile(f'/content/sae-{a}.zip', 'w') as z:
            z.write(f'sae-{a}.npz'); z.write(f'sae-{a}-ids.npy')
        print('LISTO ZIP', a, flush=True)
