import subprocess, sys, os, shutil, glob
os.chdir('/content/w')
# configuración de #67 (capas 12 y 20, 512 tokens)
env = dict(os.environ, CAPAS='12,20', N_TOK='512', TOPK='512'); env.pop('QUIERO', None)
subprocess.run([sys.executable, 'gemma_sae2.py', 'textos-2026.jsonl'], env=env, check=False)
# configuración de #65 (capa 12, 256 tokens), con otro prefijo
for f in glob.glob('sae2-textos-2026-*'): shutil.copy(f, f.replace('sae2-', 'sae2grande-'))
env = dict(os.environ, CAPAS='12', N_TOK='256', TOPK='256'); env.pop('QUIERO', None)
subprocess.run([sys.executable, 'gemma_sae2.py', 'textos-2026.jsonl'], env=env, check=False)
for f in glob.glob('sae2-textos-2026-*'): shutil.move(f, f.replace('sae2-', 'sae2chico-'))
for f in glob.glob('sae2grande-textos-2026-*'): shutil.move(f, f.replace('sae2grande-', 'sae2-'))
print('LISTO 2026 leído en las dos configuraciones', flush=True)
