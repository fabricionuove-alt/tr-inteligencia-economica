# Tr — inteligencia económica con datos públicos

Tr es el rival del juego [Vos vs Tr](https://vos-contra-la-ia.vercel.app). Este repositorio tiene todo lo necesario para rehacerlo desde cero: el código, el registro de las 100 pruebas (las que funcionaron y las que no), los pesos de los modelos chicos y las huellas de las listas selladas.

Tr no es una sola red neuronal guardada en un archivo. Es una **cadena de pasos**, y cada paso se puede volver a correr:

```
datos públicos ──► rasgos de cada empresa ──► modelos ──► cartera ──► lista sellada (sha256)
 (SEC, precios,      (balances, directivos,     (árboles,    (Gemma +     se revela al
  Wikipedia,          fondos, texto del 10-K     Gemma +      filtro #84)  cumplirse el año
  Gemma Scope)        leído por Gemma)           ridge)
```

## Qué decide Tr hoy (noviembre de 2026)

1. **Gemma lee «el negocio», «los riesgos» y «la explicación de la dirección» de cada 10-K a ciegas** (secciones 1, 1A y 7; #87) (sin nombres, marcas, lugares, años ni números). Gemma 2 2B + el autoencoder disperso de Gemma Scope (capa 12, 16.384 conceptos) + una regresión ridge aprendida sólo con 2013-2016. Señales #65, #68, #69 en `notas/11-registro-de-senales.md`.
2. **Cartera, para 4 años:** el 10% de puntaje más alto dentro de cada industria, a partes iguales. (La mitad «cohetes» de #96 se retiró: no se confirmó en 2021-2022, #97.)
3. **Filtro #84:** afuera las empresas con un pico de visitas en Wikipedia mientras sus directivos venden.

## Qué se probó

`notas/11-registro-de-senales.md` es el registro completo: cada prueba tiene su criterio **escrito antes de correr** y su resultado, incluidas las 70 que no pasaron. `notas/12-cierre.md` es el resumen.

## Cómo reproducirlo

Todo corre gratis. Los pasos pesados van en [Kaggle](https://www.kaggle.com) (CPU) y la lectura de Gemma en una placa gratuita (Kaggle o Google Colab T4). No hace falta ninguna clave de pago.

| Paso | Script | Dónde | Tiempo |
|---|---|---|---|
| 1. Balances de la SEC (companyfacts + submissions) | `codigo/entrenar/construir.py` vía `armar_kaggle_datos.py` | Kaggle CPU | ~20 min × 2 |
| 2. Precios y directivos (Fails-to-Deliver, formularios 3/4/5) | `mercado.py` vía `armar_kaggle_mercado.py` | Kaggle CPU | ~20 min × 2 |
| 3. Rasgos de precio y retornos | `precio.py` | Kaggle CPU | < 5 min |
| 4. Texto del 10-K 2013-2020 (EDGAR-CORPUS) y 2021-2026 (SEC) | `texto.py`, `sec_textos2.py` | Kaggle CPU | ~15 min por año |
| 5. Gemma lee a ciegas | `codigo/gemma/gemma_sae2.py` con `ANON=1 CAPAS=12 N_TOK=256 TOPK=256` | Kaggle GPU o Colab T4 | ~4 min por año |
| 6. Modelo de Gemma (ridge 2013-2016) y confirmación | `codigo/gemma/sae_analisis2.py` | cualquier CPU | segundos |
| 7. Cartera y lista del año | `#69` en el registro; `modelos/gemma_anon_modelo.npz` ya trae los pesos | cualquier CPU | segundos |
| 8. Filtro #84 | `marcar84.py` (visitas de Wikipedia + formularios 4) | Kaggle CPU | ~10 min |

Los `armar_kaggle_*.py` arman cada cuaderno de Kaggle con sus archivos y lo suben con `kaggle kernels push`. La cuenta de Kaggle es la de quien lo corra.

### Versiones fijadas

- Python 3.12; scikit-learn 1.9.1; pandas 3.0; numpy 2.5; scipy 1.18 (ver `requirements.txt`).
- Gemma 2 2B: copia pública `unsloth/gemma-2-2b` en Hugging Face (mismos pesos que `google/gemma-2-2b`; uso sujeto a la licencia de Gemma).
- Gemma Scope: `google/gemma-scope-2b-pt-res`, `layer_12/width_16k/average_l0_82/params.npz`.
- `modelos/gemma_anon_modelo.npz`: los pesos de la regresión que lee los conceptos de Gemma (columnas usadas, media, desvío, coeficientes). Con esto y los dos anteriores, el puntaje de cualquier 10-K se reproduce exacto.

### Lo que puede cambiar con los años

- Las fuentes públicas (SEC, Wikipedia, Yahoo) pueden cambiar de formato o de dirección. Por eso cada paso guarda su salida, y las salidas usadas están fechadas.
- Los modelos de Google están fijados por nombre y archivo; conviene fijar también la revisión exacta del repositorio de Hugging Face al bajarlos.
- Yahoo Finance no garantiza su servicio: el juego lo usa para precios en vivo, no para la investigación (que usa precios de la SEC).

## Listas selladas

Las listas de Tr no se publican mientras se juegan, para que nadie las copie. Sus huellas sha256 sí, para comprobar después que no se cambiaron:

| Lista | sha256 | Se revela |
|---|---|---|
| Tr original (cruce #45, 410 empresas) | `216d486c2abb4b34a7d20cc7fd601ad8e6009c2655a4b341a00722b3fd9e36f7` | nov-2030 (a 4 años) |
| Tr Kelly + Gemma (2.923 empresas) | `fa70b5e519c55662f159a6b120439a5b115c83b81561138596918821ab9a52ab` | nov-2030 (a 4 años) |
| Tr cartera de Gemma (416 empresas) | `ec841cab71a13934f9007d4f16ff0e729e8d666b8f2ce749fadbc2cc692a5f66` | nov-2030 (a 4 años) |
| Tr Gemma (sólo negocio) + filtro #84 (342) | `3f31f1539cfbefe539c1ad306c5266592195387699e127c29767329cbcc381bb` | nov-2030 (a 4 años) |
| Consenso de la élite 2025-2026 | `e73bfd76e79d7145e8cbcfcd8272bef34cfd9b3b5f7ccdc1a90ed80a49a85433` | jul-2028 / jul-2029 |
| Tr mitad tres secciones, mitad cohetes (#96, retirada por #97) | `8cbffce0c594f309e564a74c04a9c575f5fa92661413ae1a123dabc5546dc29c` | nov-2030 (a 4 años) |
| Picos de público con y sin venta de directivos (#84) | `97e0304d1fa13bc9a980d923ede560e91ab6da10ab493a5b30a192247c6a0caa` | nov-2027 |
| **Tr en juego: tres secciones del 10-K + filtro #84 (365)** | `597fe03a5a63ea49121ed18835d9cc40ce2646692caf21ef1f3912ea0ecb3b44` | nov-2030 (a 4 años) |

## El juego

`simulador/` es la web del juego (Vercel, funciones en Node). `simulador/lib/ia.json`, que tiene la lista de Tr, **no está en el repositorio**; `simulador/lib/ia.ejemplo.json` muestra su forma.

## Advertencia

Dinero ficticio. Nada de esto es una recomendación de inversión. Los resultados son pruebas sobre el pasado y una lista sellada hacia adelante.
