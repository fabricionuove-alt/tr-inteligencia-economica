"""Pone Tr v5 (#146) en juego: actualiza lib/ia.json (privado, en las dos copias) y deja la versión anterior en 'anteriores'."""
import json, hashlib, pandas as pd
D = 'E:/FABRI INFLUENCIA/inteligencia-economica'
c = pd.read_csv(f'{D}/datos/tr146_cartera_2026.csv'); sha = hashlib.sha256(open(f'{D}/datos/tr146_cartera_2026.csv', 'rb').read()).hexdigest()
for p in (f'{D}/simulador/lib/ia.json', 'C:/Users/Fabri/Documents/simulador-c/lib/ia.json'):
    ia = json.load(open(p, encoding='utf-8'))
    if ia['sha256'] == sha: print(p, 'ya estaba'); continue
    ant = [{'version': ia['version'] + ' — retirada el 17-nov-2026: pasa a Tr v5 (#146)', 'sha256': ia['sha256']}] + ia.get('anteriores', [])
    ia = {'version': 'Tr v5 = modelo de palabras firme (#146) sobre la descripción del negocio de cada 10-K 2026 (edgar-crawler), 10% de arriba por industria, a partes iguales, sin venta de directivos en pico de público (#84). 17-nov-2026, tras #146-#148',
          'lista': 'datos/tr146_cartera_2026.csv', 'sha256': sha, 'tickers': list(c.ticker), 'pesos': [1] * len(c), 'filtro84': ia.get('filtro84'), 'anteriores': ant}
    json.dump(ia, open(p, 'w', encoding='utf-8'), ensure_ascii=False); print(p, len(c), 'empresas', sha[:8])
