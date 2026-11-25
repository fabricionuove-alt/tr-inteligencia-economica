# Registro de señales probadas (para no confundir suerte con hallazgo)

Cada señal se anota ANTES de mirar. Con muchas señales, alguna sale bien por azar: este registro lleva la cuenta.

**Desde el 16-nov-2026, cada resultado lleva además «Qué muestra»:** por qué dio lo que dio, qué tiene de raro (pocos casos, un año que rompe, un empate) y con qué prueba anterior se conecta. El veredicto decide si una regla entra; no explica lo que pasa. Un «no pasa» nunca se cierra como «no hay nada». Si aparece algo, la prueba siguiente se anota y se corre enseguida. Motivo: #131 y #126 se cerraron como «nada» cuando mostraban que Gemma ve la etapa de vida de la empresa y que 2009 era la crisis.

## Ya probadas (2-nov-2026)
| # | Señal | Para el precio | Estado |
|---|---|---|---|
| 1-12 | Ratios de calidad de los cinco (deuda, rentabilidad, márgenes, recompras, dilución…) | 0,51-0,54 estable, chico | calidad sí; precio apenas |
| 13-16 | Barato: flujo de caja, ganancias, libros, EV/EBIT sobre precio | depende de la época | no estable |
| 17-18 | Directivos que compran / compra neta | azar; predicen MÁS muerte | no |
| 19-22 | Texto que no cambia (todo, riesgos, juicios, dirección) | 0,51 | deterioro sí; precio apenas |
| 23-29 | Franqueza por palabras (números, jerga, euforia, admite, nosotros, niebla, largo) | "nosotros" 8 de 8 adentro… | **"nosotros" FALLÓ fuera de muestra** |

Total: 29 señales. Con 29, esperar 1-2 "8 de 8" por azar es normal.

## Nuevas, escritas el 2-nov-2026 antes de mirar
| # | Señal | De quién | Signo |
|---|---|---|---|
| 30 | `diferido_ventas` = ingresos cobrados por adelantado / ventas | Quintana ("ganado el 1 de enero"), Vinall (Wix, capital circulante negativo) | + |
| 31 | `rpo_ventas` = ingresos ya contratados para los próximos años / ventas (desde 2018) | Quintana (contratos, triple net) | + |
| 32 | `dueno_mayor_pct` = % de la empresa del mayor dueño de adentro (formularios de directivos) | Paramés (familias y anclas), Vinall ("obra de su vida") | + |
| 33 | `duenos_grandes` = cuántos de adentro tienen más de 5% | Paramés | + |

**Criterio (para `precio_gana_1`, 12 meses contra la mediana del año), en DOS períodos por separado:**
- 2012-2019: media ≥ 0,52 y arriba de 0,5 en al menos 6 de 8 años.
- 2020-2024: media ≥ 0,52 y arriba de 0,5 en al menos 4 de 5 años.
- Tiene que pasar en los dos. Si pasa sólo en uno, es de una época.
También se informa (sin criterio) supervivencia y ganancias.

## Resultado #30-33 (2-nov-2026) — criterio escrito antes
| # | Señal | 2012-2019 | 2020-2024 | Veredicto | Otras cosas que se vieron |
|---|---|---|---|---|---|
| 30 | Cobrado por adelantado / ventas | 0,517 (5 de 8) | 0,499 (1 de 5) | **no pasa** | ganancias del año siguiente 0,46-0,56, sin patrón |
| 31 | Ya contratado / ventas | sólo 2 años (existe desde 2018) | 0,521 (4 de 5) | **no se puede afirmar** (pasa en un solo período, y en el otro casi no hay datos) | ganancias 0,52-0,59 en 2021-2024: a vigilar |
| 32 | % del mayor dueño de adentro | 0,497 (3 de 8) | 0,465 (1 de 5) | **no pasa** | **al revés en supervivencia (0,42-0,45): con un dueño grande adentro, mueren MÁS** |
| 33 | Dueños de adentro con >5% | 0,498 (3 de 8) | 0,473 (1 de 5) | **no pasa** | igual que #32 |

Total probadas: 33. Ninguna señal pública pasó un criterio fijado antes en los dos períodos.

## #34: franqueza leída por una IA (escrita el 2-nov-2026, ANTES de mirar)
- Modelo: Qwen2.5-1.5B-Instruct (abierto, sin claves), placa T4 de Kaggle.
- Texto: palabras 300 a 1.500 de la explicación de la dirección (sección 7), como en la prueba de velocidad.
- Pregunta fija (la misma de llm_prueba.py): inversor escéptico de largo plazo, franqueza de 1 a 10; franco = números concretos, admite problemas y errores, explica causas, habla como "nosotros"; no franco = generalidades, jerga, euforia, culpa a factores de afuera, esconde malas noticias. Responde sólo el número.
- Muestra: 2013-2020 = archivos test + validate del corpus (son una partición al azar); 2021-2025 = bajados de la SEC al azar (semilla 7).
- Señal `franq_ia`, signo +. Mismo criterio de dos períodos que #30-33 (precio_gana_1: 2012-2019 media ≥ 0,52 y ≥ 6 de 8; 2020-2024 media ≥ 0,52 y ≥ 4 de 5).
- Controles dentro de cada corrida: un texto franco y uno vago escritos a mano; si la IA no los ordena bien, la corrida no vale.
- **Cambio de modelo (antes de mirar cualquier resultado contra precios):** el 1.5B falló los controles en la primera corrida (franco 5, vago 8). Prueba de 6 controles: Qwen2.5-3B francos [10,10,8] vagos [2,3,1] PASA; Qwen2.5-7B 4-bit francos [7,7,4] vagos [2,2,2] PASA. Se usa el **3B** (más separación, misma velocidad). Los puntajes del 1.5B de 2015 se descartan sin compararlos con nada.
Patrón que se repite (#17, #32, #33): lo que los cinco leen como "piel en el juego" (dueños que compran o tienen mucho) en datos masivos aparece en empresas chicas y frágiles. En los cinco funciona porque ELIGEN a qué dueño creerle (Ernie García, Will Lundin, la familia de Reysas); el promedio no distingue al dueño bueno del desesperado.

### Resultado #34 (2-nov-2026)
Controles: las 13 corridas (2013-2025) pusieron franco 10 / vago 2 → todas válidas. Textos leídos: 446-526 por año 2013-2020 (corte de 8 min), 86-246 por año 2021-2025 (hay que bajarlos de la SEC).
- precio_gana_1, 2012-2019: sólo 5 camadas con suficientes empresas con precio (2015-2019): 0,55 · 0,49 · 0,50 · 0,49 · 0,52 → **media 0,509, 2 de 5 → no pasa.**
- 2020-2024: menos de 200 empresas con precio por año → no se puede medir. No hace falta: ya falló en el primer período.
- Ganancias del año siguiente: 0,56 y 0,62 en 2013-2014, después ~0,50. Supervivencia: 0,60 en el único año medible.
**Veredicto: no pasa.** Una IA chica que sí distingue franqueza de verso (controles perfectos) no encuentra que la franqueza escrita prediga el precio.
Total probadas: 34.

## #35: copiar la mejor idea de cada fondo (escrita el 2-nov-2026, ANTES de mirar)
Idea de Pabrai (clonar) con la definición de Cohen, Polk y Silli (2010, "Best Ideas").
- **Datos:** SEC Form 13F Data Sets, 2013 → 2026, todos los fondos con más de 100 M$ en acciones de EE.UU.
- **Fondos que cuentan:** entre 5 y 300 posiciones (deja afuera los que copian al índice y los muy chicos).
- **Mejor idea de un fondo en un trimestre:** la acción donde su peso supera más al peso de esa acción en el total de todos los fondos (sobrepeso máximo).
- **Compra:** el mes siguiente a la fecha en que la SEC publicó esa cartera (≈45 días después del cierre). Nada antes.
- **Resultado a 12 meses:** cambio del valor de mercado (precio × acciones en circulación; así los desdoblamientos no confunden). Quiebra en el medio = pérdida total. Comprada en el medio = sin resultado.
- **Comparación:** contra la mediana de todas las acciones con dato, mismo mes de compra.
- **Medida:** % de las mejores ideas que le ganan a esa mediana (50% = azar), por año de compra. Cada par (acción, mes de compra) cuenta una vez aunque sea la mejor idea de varios fondos (aclarado antes de mirar, al revisar el formato).
- Se excluyen: enmiendas, opciones (PUT/CALL) y posiciones que no son acciones (SSHPRNAMTTYPE ≠ SH).
- **Éxito:** ≥ 52% en 2013-2018 Y ≥ 52% en 2019-2024, y arriba de 50% en al menos 9 de los 12 años.
- **Fracaso:** cualquier otra cosa.

### Resultado #35 (2-nov-2026)
13F 2013-2026: ~222.000 mejores ideas (fondos de 5-300 posiciones), cada par acción-mes una vez.
| Año de compra | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Le ganan a la mediana de todas | 55,9 | 55,7 | 52,5 | 49,8 | 52,1 | 57,7 | 56,9 | 39,5 | 59,0 | 61,6 | 61,3 | 54,2 |
| Contra empresas de su mismo tamaño | 48,9 | 49,0 | 49,0 | 49,2 | 50,9 | 50,0 | 51,8 | 47,3 | 49,6 | 52,1 | 52,8 | 52,8 |
- Criterio escrito antes: 53,8% (2013-18), 55,8% (2019-24), 10 de 12 años → **pasa en lo literal**.
- **Control de tamaño (agregado después, como con "nosotros"): se cae.** Las mejores ideas están casi todas en el quintil más grande (tamaño medio 3,55 de 0-4). Contra empresas de su mismo tamaño: ~49% en 2013-2018, ~50-53% en 2019-2024. Lo que "ganaba" era que los fondos compran empresas grandes, y las grandes le ganaron a la mediana (llena de chicas).
- **Veredicto: no es habilidad para elegir; es tamaño.** Queda a vigilar 2022-2024 (52-53% dentro de tamaño), pero es otra vez una época.
Total probadas: 35.

## #36: evitar las frágiles (escrita el 2-nov-2026, ANTES de mirar)
Une lo que sí funciona (detectar quiebras) con el precio. Base: Campbell, Hilscher y Szilagyi (2008), las acciones en problemas rinden peor.
- Señal: el puntaje de supervivencia del modelo entrenado SÓLO con 2012-2013 (`p_sobrevive_10_amplio`), así que desde 2014 es fuera de muestra.
- Etiqueta: precio_gana_1 (12 meses contra la mediana del año).
- **Medida principal: AUC dentro del mismo tamaño** (quintiles de activos dentro del año), para no repetir el error de #35.
- También: cuánto rinden las del 20% más frágil contra el resto (mediana de retorno).
- **Éxito:** dentro de tamaño, media ≥ 0,52 en 2014-2019 (≥ 4 de 6 años arriba de 0,5) Y media ≥ 0,52 en 2020-2024 (≥ 4 de 5).

### Resultado #36 (2-nov-2026)
| Compra | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AUC dentro de tamaño | 0,574 | 0,496 | 0,551 | 0,541 | 0,565 | 0,421 | 0,495 | 0,550 | 0,520 | 0,518 | 0,475 |
| Retorno mediano 12 m, 20% más frágil | 0,77 | 1,15 | 1,03 | 0,91 | 0,65 | 2,16 | 0,92 | 0,71 | 0,96 | 0,96 | 1,13 |
| Retorno mediano 12 m, el resto | 0,96 | 1,20 | 1,14 | 1,01 | 0,83 | 1,61 | 1,00 | 0,91 | 1,10 | 1,02 | 1,13 |
- Criterio: 2014-2019 0,525 (4 de 6) pasa; 2020-2024 0,512 (3 de 5) **no** → **no pasa, por poco**.
- Lo práctico: el 20% más frágil rindió peor que el resto en 9 de 11 años (entre 6 y 20 puntos menos de mediana). Las excepciones: la camada 2019 (el rebote de las empresas basura en 2020-21) y 2024 (igual).
- Es lo más cerca que llegó cualquier señal. Lo que sirve es para EVITAR, no para elegir.
Total probadas: 36.

## #37: evitar las frágiles, versión mejorada (escrita el 2-nov-2026 ANTES de mirar; OJO: los años de evaluación ya se vieron en #36)
Cambios, todos sacados de la literatura (no de mirar resultados):
1. Señales de mercado de Campbell-Hilscher-Szilagyi (2008): retorno de los 12 meses ANTES de presentar el balance, volatilidad mensual de esos 12 meses, nivel de precio (log). Todo anterior a la fecha de presentación.
2. Etiqueta para entrenar: `muere_3` = deja de presentar en menos de 3 años por quiebra, revocación o baja sin compra (más años con resultado conocido).
3. Entrenamiento móvil: para cada año de compra t, el modelo se entrena con todos los años 2012..t-4 (nunca ve el futuro de t).
Evaluación igual que #36: AUC dentro de quintiles de tamaño sobre precio_gana_1, más retorno mediano del 20% más frágil vs el resto.
**Éxito:** media ≥ 0,52 en 2016-2019 (≥ 3 de 4 arriba de 0,5) Y media ≥ 0,52 en 2020-2024 (≥ 4 de 5).
Como los años ya se miraron, aunque pase, la confirmación real es la prueba congelada hacia adelante.

### Resultado #37 (2-nov-2026)
| Compra | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|
| AUC dentro de tamaño | 0,557 | 0,546 | 0,551 | 0,420 | 0,496 | 0,558 | 0,512 | 0,497 | 0,466 |
| Mediana 20% frágil / resto | 1,02/1,14 | 0,88/1,02 | 0,73/0,83 | 2,05/1,61 | 0,92/1,00 | 0,71/0,91 | 0,96/1,10 | 0,96/1,02 | 1,14/1,13 |
- Criterio: 2016-2019 0,519 (3 de 4), 2020-2024 0,506 (2 de 5) → **no pasa. La "mejora" no mejoró**: dentro de tamaño quedó igual o peor que #36.
- Con las señales de mercado agregadas, #36 subió apenas (0,53 / 0,516), tampoco pasa.
- Lo estable sigue siendo lo mismo: el 20% más frágil rinde peor que el resto en la mayoría de los años (7 de 9), pero dentro de un mismo tamaño la diferencia es chica, y los años de rebote de las empresas basura (camada 2019, 2024) la dan vuelta.
Total probadas: 37.

## #38: el coto (idea de Fabri), escrita el 2-nov-2026 ANTES de mirar
Respaldo previo: `_respaldos/inteligencia-economica-2026-11-02-antes-del-coto/`.
Idea: no predecir la sorpresa; pararse donde una sorpresa grande es posible y un desastre es improbable. Medir COLAS y PROMEDIO (no la mediana, que castiga lo que sorprende). Base: Bessembinder (2018), el 4% de las acciones hace toda la riqueza; trampa conocida: las acciones "lotería" rinden peor en promedio (Bali-Cakici-Whitelaw 2011).
- **Coto:** sacar el 30% más frágil según el modelo móvil de #37 (entrenado con 2012..t-4).
- **Opcionalidad (dentro y fuera del coto):** promedio de percentiles de: crecimiento de ventas 3 años (+), I+D/ventas (+), tamaño (−, más chica), volatilidad 12 meses (+), dividendos/caja (−, reinvierte). "Coto + opcional" = el 30% más opcional DENTRO del coto. "Lotería sin coto" = el 30% más opcional del universo entero.
- **Grupos comparados:** universo, frágiles (el 30% sacado), coto, coto + opcional, lotería sin coto.
- **A 12 meses (camadas 2016-2024):** retorno promedio (cartera igual peso), mediana, % que se duplica (≥ ×2) y % desastre (≤ ×0,5 o quiebra).
- **A 6 años (camadas 2016-2019):** % ≥ ×3 y % ≤ ×0,25.
- **Éxito de "coto + opcional":** (1) promedio a 12 meses mayor que el del universo en ≥ 6 de 9 camadas y exceso medio ≥ +2 puntos; (2) % de duplicadas ≥ universo y % de desastres ≤ universo en ≥ 6 de 9; (3) a 6 años, más ×3 y menos ×0,25 que el universo en ≥ 3 de 4.
- **Pregunta clave aparte:** ¿"coto + opcional" le gana a "lotería sin coto"? (si el coto sirve para algo, tiene que notarse ahí).

### Resultado #38 (2-nov-2026)
Error mío en el cálculo del criterio: contó las camadas 2020-2022 a 6 años, que todavía no cumplieron 6 años (sólo tenían quiebras → "100% desastre"). Lo válido a 6 años es 2016-2019, como estaba escrito.

12 meses (camadas 2016-2024), promedio de la cartera / % que se duplica / % desastre (≤ ×0,5 o quiebra):
| Grupo | prom (media 9 años) | duplica | desastre |
|---|---|---|---|
| Universo | 1,26 | 10,2% | 13,2% |
| Frágiles (30% sacado) | 1,40 | 17,5% | 36,6% |
| Coto (sin frágiles) | 1,24 | 8,8% | 9,2% |
| **Coto + opcional** | **1,40** | **16,2%** | **17,7%** |
| Lotería sin coto | 1,51 | 19,2% | 28,7% |

6 años (camadas 2016-2019), % ×3 / % ≤ ×0,25:
| Grupo | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|
| Universo | 15,5 / 10,7 | 14,5 / 11,7 | 16,0 / 11,9 | 28,5 / 10,4 |
| Coto | 14,5 / 7,4 | 13,8 / 8,2 | 15,6 / 8,6 | 28,3 / 7,1 |
| Coto + opcional | 22,2 / 16,5 | 22,4 / 17,7 | 20,7 / 17,0 | 28,9 / 14,4 |
| Lotería sin coto | 21,6 / 31,4 | 23,3 / 28,7 | 21,3 / 27,4 | 29,2 / 27,1 |

Criterio: (1) promedio mayor que el universo en 8 de 9 y exceso medio +13,5 puntos → **pasa**; (2) más duplicadas Y menos desastres → 1 de 9 → **no**; (3) a 6 años más ×3 Y menos desastres → 0 de 4 → **no**. **Veredicto: no pasa.**

Lo que muestra (descriptivo, no probado como regla):
- El coto solo baja los desastres un tercio (13% → 9%) y deja el promedio igual.
- Dentro del coto, la opcionalidad SÍ trae más sorpresas grandes (duplica 16% vs 10%; ×3 en 6 años 22% vs 15%) y más promedio, pero también más desastres que el universo (18% vs 13%).
- Contra la lotería sin coto, el coto corta los desastres casi a la mitad (29% → 18%; a 6 años 28-31% → 14-18%) y conserva la mayor parte de las sorpresas. Es el efecto que buscaba Fabri, pero no llega a "cruz pierdo poco": pierde menos que la lotería, más que el promedio.
- Cautela: los promedios de acciones chicas y volátiles los inflan pocas ganadoras enormes y precios con errores (se cortó en ×20); las compradas a mitad de camino quedan afuera.
Total probadas: 38.

## #39: la contradicción (superficie frágil, fondo sano), escrita el 2-nov-2026 ANTES de mirar
Idea (de la charla con Fabri): lo extraordinario medido con la vara de lo seguro sale MAL, no invisible. Su estela en los datos sería un desacuerdo: lo que mira todo el mundo dice "frágil" y lo que deja el sacrificio dice "sana". Una empresa común es coherente (fea-fea o linda-linda); la que no cierra es la candidata.
- **Superficie** (lo que mira todo el mundo): margen neto, margen operativo, margen operativo mínimo de 5 años, ROA, ROE, tendencia del ROA, pérdida sí/no, rinde de ganancia, rinde de caja libre, EBIT/valor de empresa, caja libre/ventas, retorno de 12 meses previos, volatilidad 12 meses, nivel de precio.
- **Fondo** (lo que deja el sacrificio): margen bruto, estabilidad del margen, crecimiento de ventas 1 y 3 años, cobros adelantados (diferido/ventas, contratos pendientes/ventas), I+D/ventas, capex/caja operativa, caja/activos, deuda/activos, deuda neta/caja, pasivo/activos, sin deuda, cobertura de intereses, caja operativa/activos, devengos, dilución 3 años, rotación, patrimonio negativo, compras de directivos, compra neta/valor, dueño mayor %, dueños grandes.
- Sector entra en los dos; el tamaño en ninguno (se informa aparte).
- **Dos modelos de fragilidad separados**, misma etiqueta y mismo esquema móvil de #37 (muere en 3 años; entrena con 2012..t-4).
- **Cuadrantes por camada:** superficie frágil = 30% más bajo en "sano según superficie"; fondo sano = 40% más alto en "sano según fondo". **Contradicción** = superficie frágil Y fondo sano. **Frágil coherente** = superficie frágil Y fondo en el 40% más bajo.
- **Paso 2, ¿existe la estela? (camadas 2016-2019, 6 años):** en ≥ 3 de 4 camadas la contradicción tiene más ×3 que el universo Y menos desastres (≤ ×0,25) que el frágil coherente. Si no pasa, la idea muere acá.
- **Paso 3, ¿sirve? (mismo listón que #38):** (1) promedio a 12 meses mayor que el universo en ≥ 6 de 9 camadas (2016-2024) y exceso medio ≥ +2 puntos; (2) más duplicadas Y no más desastres que el universo en ≥ 6 de 9; (3) a 6 años más ×3 Y menos ×0,25 que el universo en ≥ 3 de 4.
- **Control aparte:** la contradicción contra toda la superficie frágil (¿el fondo agrega algo?), y su tamaño medio.
- De paso se corrige el error de #38: a 6 años sólo cuentan las camadas 2016-2019.

### Resultado #39 (2-nov-2026, Kaggle ie-analisis v22)
**Lo central: la contradicción casi no existe en estos datos.** Los dos juicios coinciden mucho (correlación 0,65 a 0,79 según la camada): una empresa que se ve frágil arriba casi siempre está frágil abajo. El cuadrante "superficie frágil + fondo sano" junta sólo 55 a 143 empresas por año (1-3% del universo), de ~4.900.

12 meses (las camadas con ≥ 30 empresas con precio):
| Camada | Universo prom / x2 / desastre | Superficie frágil (toda) | Frágil coherente | **Contradicción** |
|---|---|---|---|---|
| 2016 | 1,21 / 6,1% / 8,7% | 1,08 / 11,0% / 36,7% | 1,11 / 11,7% / 43,0% | 1,03 / 8,3% / 16,7% |
| 2019 | 2,13 / 34,1% / 6,1% | 2,69 / 43,4% / 29,6% | 2,53 / 40,1% / 34,2% | 3,03 / 56,8% / 10,8% |
| 2020 | 1,08 / 6,1% / 15,9% | 1,27 / 17,2% / 32,0% | 1,35 / 19,6% / 36,0% | 1,07 / 9,9% / 14,1% |
| 2021 | 1,00 / 5,0% / 19,1% | 1,16 / 11,5% / 39,1% | 1,10 / 11,2% / 44,9% | 1,22 / 10,1% / 15,9% |
| 2022 | 1,25 / 9,1% / 13,9% | 1,39 / 15,8% / 31,1% | 1,39 / 17,1% / 37,4% | 1,25 / 12,4% / 7,9% |
| 2023 | 1,19 / 8,2% / 14,3% | 1,36 / 16,8% / 29,4% | 1,39 / 18,9% / 32,1% | 1,27 / 8,6% / 22,4% |
(2017, 2018 y 2024: menos de 30 con precio en el cuadrante, sin medir.)

Estela al revés (de las que hicieron ×3 en 6 años, qué parte estaba en la contradicción, contra cuánto pesa el cuadrante): 2016 1,22% vs 1,18%; 2017 0,63% vs 0,74%; 2018 1,74% vs 0,98%; 2019 1,30% vs 1,25%. Juntas: 1,18 veces lo esperable por azar, con muy pocas empresas. **No hay estela clara.**

Criterio: **paso 2 no se pudo medir** (a 6 años ninguna camada llegó a 30 empresas en el cuadrante); por la regla escrita, no pasa. Paso 3: promedio mayor que el universo en 4 de 6, colas mejores en 3 de 6 → **no pasa**.

Lo que sí muestra (descriptivo): dentro de las que se ven frágiles, mirar el fondo separa muy bien a las que se mueren. Desastre a 12 meses del frágil coherente 32-45%; de la contradicción 8-22%, cerca del universo. El fondo no encuentra lo extraordinario, pero rescata a las frágiles que no lo son. Las sorpresas (x2) de la contradicción quedan entre el universo y las frágiles.
Por qué puede haber salido así: los dos modelos aprendieron a predecir la MUERTE, y la muerte es coherente (se ve en todo a la vez). Una vara entrenada para lo que muere no puede ver lo que no cierra. Si se sigue esta idea, el desacuerdo tiene que medirse con algo que no sea la muerte.
Total probadas: 39.

## #40: la insistencia (lo que no vuelve al promedio), escrita el 2-nov-2026 ANTES de mirar
Idea (charla con Fabri): lo seguro es la ley de que todo vuelve al promedio (Fama-French 2000: la rentabilidad revierte ~38% por año; Chan-Karceski-Lakonishok 2003: el crecimiento sostenido no aparece más que por azar). Lo extraordinario no se ve en una foto sino en una trayectoria que desmiente esa ley año tras año, siempre para el mismo lado: la estela de una intención. Se mide en el espacio de los caminos, no de los números.
- **Lo seguro (el 80%):** para cada medida (margen operativo, margen bruto, crecimiento de ventas, ROA, caja operativa/activos), un modelo predice su percentil del año s con TODOS los rasgos del año s-1. Entrena sólo con años s-6..s-1 (nunca ve el año que predice).
- **El desvío:** real - predicho, en percentil. Positivo = le fue mejor de lo que "una empresa como esa" tenía que hacer.
- **Insistencia en el año t:** de los 15 desvíos (5 medidas × años t-2, t-1, t), qué fracción es positiva (al menos 9 con dato). **Insistentes** = el 10% más alto de su camada; **insistentes al revés** = el 10% más bajo (control).
- **Paso A, ¿la insistencia existe más que por azar? (contra CKL 2003):** se mezclan los desvíos entre empresas dentro de cada año (rompe la trayectoria y conserva todo lo demás) y se cuenta cuántas tienen ≥ 80% positivos. Existe si lo real es ≥ 1,3 veces lo mezclado en ≥ 6 de 8 camadas (2017-2024).
- **Paso B, estela:** de las que hicieron ×3 en 6 años (camadas 2017-2019), la parte que era insistente es ≥ 1,5 veces su peso en ≥ 2 de 3.
- **Paso C, ¿sirve? (listón de #38):** a 12 meses (2017-2024), promedio mayor que el universo en ≥ 6 de 8 y exceso medio ≥ +2 puntos; más duplicadas Y no más desastres en ≥ 6 de 8; a 6 años (2017-2019) más ×3 Y menos ×0,25 en ≥ 2 de 3.
- **Pregunta clave aparte:** ¿la trayectoria le gana a la foto? Se compara con el 10% de nivel más alto en esas 5 medidas en el año t ("calidad" de una foto).

### Resultado #40 (3-nov-2026, Kaggle ie-analisis v23)
**Paso A, ¿la insistencia existe? PASA, 8 de 8.** Las empresas con ≥ 80% de desvíos positivos son el 5-7,5% de cada camada, contra 1,4-2,6% si se mezclan los desvíos entre empresas: entre 2,5 y 4,5 veces más que el azar. Es la primera vez en 40 pruebas que la huella existe claramente. (No contradice a CKL 2003: ellos miden crecimiento crudo; acá se mide desmentir lo esperado en cinco medidas a la vez.)

**Paso B, estela: no pasa (1 de 3).** De las que hicieron ×3 en 6 años, la parte insistente contra su peso: 2017 20,7% vs 13,0% (1,59 veces); 2018 16,9% vs 12,4% (1,36); 2019 13,6% vs 11,8% (1,15).

**Paso C: no pasa.** A 12 meses las insistentes NO le ganan al universo (3 de 8, exceso medio −2,7 puntos, menos duplicadas). **A 6 años sí, 3 de 3:**
| Camada | Universo ×3 / desastre | **Insistentes** | Foto de calidad | Al revés |
|---|---|---|---|---|
| 2017 | 14,3% / 11,2% | **22,7% / 5,8%** | 15,8% / 5,4% | 13,3% / 29,5% |
| 2018 | 15,8% / 11,1% | **21,5% / 6,4%** | 18,9% / 5,7% | 14,4% / 33,0% |
| 2019 | 28,9% / 9,3% | **33,3% / 7,0%** | 22,4% / 3,1% | 29,8% / 20,7% |
Desastres a 12 meses: insistentes 2,5-11,5% contra 4,7-20,8% del universo, en las 8 camadas.

**Veredicto por lo escrito: no pasa.** Lo que muestra (descriptivo):
- La trayectoria le gana a la foto en sorpresas: a 6 años, más ×3 que la "calidad" de un año en las 3 camadas, con casi los mismos desastres. La foto da seguridad sin sorpresa; la insistencia da seguridad CON sorpresa.
- El mercado no lo paga en 12 meses y sí en 6: lo que insiste tarda en verse en el precio.
- "Al revés" (siempre peor de lo esperado) junta el triple de desastres: la huella sirve para los dos lados.
- Cautelas: sólo 3 camadas a 6 años y sus ventanas se pisan (2017-23, 2018-24, 2019-25), así que no son 3 pruebas independientes; las insistentes son algo más grandes (0,57-0,61 contra 0,53), aunque la foto es más grande todavía y da menos ×3.
- Para confirmarlo sin acomodar: hacen falta camadas que nadie miró (2013-2016) o la prueba congelada hacia adelante.
Total probadas: 40.

## #41: confirmar la insistencia en años que nadie miró, escrita el 4-nov-2026 ANTES de correr
Lo mismo que #40, sin cambiar nada de la receta (5 medidas, 3 años, 10% más insistente, mezcla para el azar), en las camadas **2013-2016**, que ninguna prueba de insistencia tocó. Para poder armar sus trayectorias se usan también los años 2009-2011 (sólo para entrenar lo seguro y para los desvíos de t-2 y t-1; antes se descartaban porque les faltan rasgos de historia, que se rellenan al azar como siempre). Diferencia inevitable: en los primeros años lo seguro entrena con menos años (desde 2010).
Se corre aparte (entrenar/insistencia.py) y también repite 2017-2019 como control de que da parecido a #40.
- **Confirma si, en 2013-2016:** (1) la insistencia existe más que por azar (real ≥ 1,3 × mezclado) en ≥ 3 de 4; (2) a 6 años las insistentes tienen más ×3 Y menos desastres (≤ ×0,25) que el universo en ≥ 3 de 4; (3) a 6 años más ×3 que la foto de calidad en ≥ 3 de 4.
- Se informa sin criterio: 12 meses y la estela (parte de las ×3 que eran insistentes contra su peso).
- Cautela que queda: las ventanas de 6 años de 2013-2016 se pisan entre sí y con las de 2017-2019; es otra época de entrada, no otro mundo.

### Resultado #41 (4-nov-2026, Kaggle ie-analisis v24)
**No confirma.** (1) Existe: 4 de 4 (real 4,2-5,5% contra 1,0-1,7% mezclado). (2) A 6 años, más ×3 y menos desastres que el universo: 2 de 4. (3) Más ×3 que la foto de calidad: 1 de 4.
| Camada | Universo ×3 / desastre | Insistentes | Foto de calidad | Al revés |
|---|---|---|---|---|
| 2013 | 9,5% / 16,8% | 12,5% / 13,5% | 13,0% / 9,3% | 7,0% / 31,4% |
| 2014 | 18,9% / 12,2% | 21,3% / 10,9% | 20,3% / 6,9% | 21,8% / 34,7% |
| 2015 | 23,7% / 10,4% | 23,5% / 6,4% | 27,1% / 6,0% | 26,7% / 25,9% |
| 2016 | 14,9% / 10,0% | 13,2% / 5,6% | 16,3% / 5,6% | 20,0% / 24,8% |

**El control también se cayó.** Con la misma receta pero entrenando lo seguro con más años (desde 2010), 2017-2019 dan insistentes ×3 15,3% / 17,4% / 28,4% contra un universo de 14,3% / 15,8% / 28,9%. En #40 habían dado 22,7% / 21,5% / 33,3%. **El exceso de sorpresas de #40 dependía de detalles del modelo de lo seguro: no era sólido.**

Lo que queda firme en 12 de 12 camadas:
- La insistencia existe: 3 a 4 veces más que por azar.
- Las insistentes casi nunca se hunden: menos desastres que el universo en las 7 camadas a 6 años. Pero la foto de calidad hace lo mismo o mejor. Insistir, medido así, es otra forma de ver calidad, no sorpresa.
- "Al revés" (siempre peor de lo esperado) es la huella más fuerte de la serie: el doble o el triple de desastres en todas las camadas.
Total probadas: 41.

## #42: los que creen y aguantan (la insistencia en la conducta de las personas), escrita el 4-nov-2026 ANTES de correr
Idea: la contabilidad habla el idioma de lo seguro; la estela de lo cualitativo estaría en lo que hacen quienes conocen la empresa cuando el precio les dice que se equivocaron. Antecedentes: Cheng-Hameed-Subrahmanyam-Titman (JFQA 2017): las caídas rebotan más cuando los institucionales SE VAN (presión de venta, no información); LeHavy-Sloan: más reconocimiento = peor futuro. Por eso el control no es el universo sino las caídas en las que nadie creyó.
- **Caída:** el precio del mes de compra está ≥ 20% abajo del de 12 meses antes.
- **Creyentes (13F):** fondos concentrados (5-300 posiciones en esa presentación, identificados por su CIK). Un fondo es creyente de una acción caída si la tenía hace 4 trimestres, la tuvo en todos los trimestres del medio, y ahora tiene ≥ 10% más de la empresa (acciones del fondo / acciones en circulación, así los desdoblamientos no cuentan como compra). **Grupo: caídas con ≥ 2 creyentes.** Control: caídas que hace 4 trimestres tenían ≥ 2 fondos concentrados y hoy tienen 0 creyentes. Se informa también ≥ 1 creyente.
- **De adentro (formularios 4):** en los 12 meses de la caída, al menos un directivo compró en el mercado (P) y ninguno vendió (S). Control: caídas con ventas de directivos y sin compras. (Ojo: en #34 comprar de adentro venía con MÁS quiebras; acá se mide sólo en caídas.)
- **Compra:** mes siguiente a la presentación del 13F (cuatro fechas por año); quiebra en el medio = pérdida total; valor de mercado = precio × acciones conocidas en ese momento (igual que #35).
- **A 12 meses:** compras 2014-2024. **A 6 años:** compras 2014-2019.
- **Pasa (cada grupo por separado) si:** (1) a 6 años más ×3 que su control Y no más desastres (≤ ×0,25) en ≥ 4 de 6 años; (2) a 6 años más ×3 que el universo en ≥ 4 de 6; (3) a 12 meses el exceso medio sobre su control es ≥ 0 (no se pide que gane rápido, sólo que no pierda).
- Se informa: tamaño medio, n por año, y estela (de las ×3, qué parte estaba en el grupo, contra su peso).

### Resultado #42 (4-nov-2026, Kaggle ie-t13f-* + ie-creyentes)
Datos: 12,9 millones de posiciones de fondos concentrados (13F 2013-2024), 1,86 millones de casos de "creyente", 201 mil compras (44 fechas × empresas). Fecha de compra = cierre del trimestre + 3 meses.

**Creyentes (fondos que suben su parte mientras cae): no pasa.** A 6 años, contra las caídas abandonadas: menos ×3 en 6 de 6 años, aunque también menos desastres. Contra el universo, más ×3 en 4 de 6. A 12 meses rinden 33 puntos menos que el control.
**De adentro (compran y nadie vende en la caída): no pasa.** Contra las caídas en las que venden: más ×3 en 6 de 6 años (18,0/25,2/24,7/17,1/18,7/20,5% contra 11,1/22,8/19,4/16,7/17,3/15,9%) pero MÁS desastres en 6 de 6 (el criterio pedía no más). Contra el universo, más ×3 en 6 de 6. A 12 meses +16 puntos sobre su control. Estela: de las ×3, la parte que estaba en este grupo es 1,16 a 1,41 veces su peso, los 6 años.

**Lo que explica casi todo: el tamaño.**
- Las caídas con creyentes son empresas grandes (percentil de tamaño 0,53-0,61); las abandonadas, chicas (0,18-0,34). Las chicas abandonadas rebotan más, como encontraron Cheng-Hameed-Subrahmanyam-Titman. Los creyentes marcan seguridad, no sorpresa.
- Las caídas en las que compran los de adentro también son chicas (0,23-0,35), y contra otras caídas chicas (las abandonadas por los fondos, 0,18-0,34) dan casi lo mismo: ×3 18,0/25,2/24,7/17,1/18,7/20,5% contra 17,1/31,3/23,5/19,0/19,2/21,2%. La "estela" de los de adentro es, sobre todo, la lotería de las chicas caídas.
- Igual que en #36-#41: lo que se mide en las personas también termina separando seguro de riesgoso, no lo extraordinario de lo común.
Total probadas: 42.

## #43: la interrelación (todas las huellas juntas), escrita el 4-nov-2026 ANTES de correr
Pedido de Fabri: buscar otros ángulos y, sobre todo, su interrelación. Hasta #42 cada huella se probó sola (y casi todas contra el universo). Acá un solo modelo aprende lo extraordinario con todas juntas, para ver si el cruce explica lo que ninguna sola.
- **Etiqueta, en sus propios términos:** extraordinaria = su múltiplo a 6 años (dueño de toda la empresa, quiebra = 0) está en el 10% más alto de su camada. Relativa a la camada, así la época no cuenta.
- **Bloques de huellas:**
  - NÚMEROS: todos los rasgos de siempre (balances, precio, dueños, texto si hay).
  - TRAYECTORIA: los 15 desvíos de #40 (5 medidas × 3 años) + fracción positiva + desvío medio.
  - PERSONAS: en el último trimestre 13F antes de la compra: creyentes, fondos concentrados que la tenían hace un año, compras y ventas de directivos en 12 meses, caída del valor en 12 meses.
- **Modelos:** cada bloque solo, de a pares, y los tres juntos. Mismo algoritmo (árboles, que aprenden los cruces solos).
- **Prueba:** camadas 2013-2019 (personas existen desde 2013, la etiqueta a 6 años hasta 2019). Validación cruzada de 5 partes **por empresa** (una empresa nunca está en entrenamiento y prueba a la vez). Cautela: no es fuera de tiempo; lo será la prueba congelada.
- **Medida:** AUC DENTRO del mismo quintil de tamaño (si no, el tamaño solo "gana"), por camada; y el 10% con puntaje más alto de cada camada: % ×3 y % desastre (≤ ×0,25) contra el universo.
- **Pasa si:** (1) los tres juntos dan AUC dentro de tamaño ≥ 0,60 en promedio; (2) los tres juntos le ganan al mejor bloque solo por ≥ 0,01 en ≥ 5 de 7 camadas (la interrelación agrega); (3) su 10% de arriba tiene más ×3 y no más desastres que el universo en ≥ 5 de 7.

### Resultado #43 (4-nov-2026, Kaggle ie-analisis v25)
14.784 empresas-año (2013-2019), 12.302 con trayectoria, 13.656 con personas.
AUC dentro del mismo tamaño para "estar en el 10% de arriba a 6 años" (promedio de 7 camadas):
| Modelo | AUC |
|---|---|
| números | 0,645 |
| trayectoria | 0,594 |
| personas | 0,570 |
| números + trayectoria | 0,652 |
| números + personas | 0,646 |
| trayectoria + personas | 0,611 |
| **los tres** | **0,650** |
Criterio: (1) AUC ≥ 0,60 → sí (0,650); (2) el cruce agrega ≥ 0,01 sobre el mejor bloque → 2 de 7, no; (3) el 10% de arriba con más ×3 y no más desastres → 0 de 7, no. **No pasa.**

**Lo que muestra:** el modelo SÍ reconoce de antemano a las extraordinarias, dentro de su mismo tamaño: su 10% de arriba se triplica el doble que el universo (25-36% contra 11-28%), los 7 años. Pero junta también el doble o el triple de desastres (26-33% contra 10-19%). **Lo que aprendió es quién va a ir a un extremo, no hacia qué lado.** Cada bloque por separado ve lo mismo y el cruce casi no agrega: las tres huellas cuentan la misma historia, la de una empresa en juego.
Esto es nuevo respecto de #1-#42: antes buscábamos un lado; acá aparece la magnitud. Y para el otro lado ya tenemos el modelo de muerte (AUC 0,81-0,86). La interrelación que falta probar es entre esos dos modelos: extremo alto Y muerte baja.
Total probadas: 43.

## #44: extremo × no hundirse (cruzar los dos modelos), escrita el 4-nov-2026 ANTES de correr
De #43: el modelo de extremos reconoce a las que van a un extremo pero no el lado. El otro lado lo da un modelo de desastre.
- **Modelo E (extremo):** el de #43 con los tres bloques ("todo"), etiqueta 10% de arriba a 6 años.
- **Modelo D (desastre):** mismas huellas, etiqueta = múltiplo a 6 años ≤ ×0,25 (incluye quiebras). Mismo horizonte que E, así hablan del mismo futuro.
- Los dos con la misma validación cruzada por empresa (5 partes), camadas 2013-2019.
- **Cruce:** en cada camada, de la mitad con MENOS riesgo de desastre según D, las de E más alto, hasta juntar el 10% de la camada.
- **Comparados:** universo; solo E (su 10% de arriba); solo D (el 10% más seguro).
- **Pasa si:** el cruce tiene (1) más ×3 que el universo Y no más desastres que el universo en ≥ 5 de 7 camadas; (2) múltiplo promedio a 6 años mayor que el universo en ≥ 5 de 7; (3) más ×3 que "solo D" en ≥ 5 de 7 (que no sea sólo seguridad).
- Se informa: 12 meses, tamaño, y la AUC de D.

### Resultado #44 (4-nov-2026, Kaggle ie-analisis v26): **PASA** (la primera de 44)
Criterio: (1) más ×3 y no más desastres que el universo → 6 de 7; (2) promedio a 6 años mayor → 6 de 7; (3) más ×3 que "solo seguro" → 6 de 7.
| Camada | Universo ×3 / desastre / promedio | **Cruce** | Solo extremo | Solo seguro |
|---|---|---|---|---|
| 2013 | 11,3% / 18,7% / ×1,69 | **15,5% / 7,3% / ×2,28** | 25,2% / 31,6% / ×3,24 | 11,2% / 1,0% / ×1,82 |
| 2014 | 19,8% / 12,8% / ×2,34 | **29,1% / 5,7% / ×2,47** | 33,3% / 28,6% / ×3,98 | 7,6% / 0,5% / ×1,86 |
| 2015 | 24,4% / 10,8% / ×2,62 | **36,6% / 1,5% / ×3,40** | 35,6% / 25,3% / ×3,96 | 18,8% / 0,0% / ×2,12 |
| 2016 | 15,5% / 10,7% / ×2,07 | **26,4% / 0,5% / ×2,49** | 25,9% / 23,1% / ×2,84 | 10,9% / 0,0% / ×1,87 |
| 2017 | 14,5% / 11,7% / ×1,97 | **16,6% / 5,1% / ×2,22** | 23,5% / 25,8% / ×2,69 | 9,7% / 0,0% / ×1,91 |
| 2018 | 16,0% / 11,9% / ×2,06 | **24,2% / 4,7% / ×2,25** | 27,0% / 27,9% / ×2,72 | 12,6% / 0,0% / ×2,08 |
| 2019 | 28,5% / 10,4% / ×3,08 | 25,4% / 5,1% / ×3,07 | 34,6% / 27,7% / ×4,35 | 26,3% / 0,5% / ×2,65 |
AUC del modelo de desastre a 6 años: 0,82-0,85.

Lo que muestra: el cruce se queda con casi todas las sorpresas del modelo de extremos (en 2015 y 2016, todas) y con la seguridad del modelo de desastre: entre 1,1 y 1,7 veces más ×3 que el universo, con entre un cuarto y la mitad de sus desastres. No es tamaño (el cruce mide 0,67-0,70 de tamaño, como el universo de 0,64-0,65). A 12 meses rinde como el universo: lo paga el tiempo, no el año.

**Cautelas antes de creerlo:**
- La validación es por empresa, no fuera de tiempo: el modelo aprendió con otras empresas de los MISMOS años. Comparte la época.
- Las 7 ventanas de 6 años se pisan.
- Es la primera que pasa de 44: con tantas pruebas, una puede pasar por suerte.
- **Siguiente obligatorio:** (a) fuera de tiempo: entrenar sólo con camadas que ya cumplieron sus 6 años antes de cada compra; (b) congelar hoy la lista de las empresas que elige para 2025, con su huella, para mirarla en 2031.
Total probadas: 44.

## #45: el cruce fuera de tiempo + lista congelada 2025, escrita el 4-nov-2026 ANTES de correr
- **Fuera de tiempo:** para comprar en la camada s (2015-2019), los modelos E y D se entrenan SÓLO con camadas c ≤ s-6, cuyos 6 años ya terminaron antes de comprar (2015 aprende con 2009; 2019 con 2009-2013). Mismos bloques que #44; donde un bloque no existía todavía (personas antes de 2013, trayectoria antes de 2012), queda vacío y el modelo aprende sin él. Misma regla de cruce (la mitad más segura según D; de ahí el 10% de la camada con E más alto).
- **Pasa si:** en ≥ 4 de 5 camadas (1) más ×3 y no más desastres que el universo; (2) promedio a 6 años mayor; (3) más ×3 que "solo seguro".
- **Lista congelada:** E y D entrenados con todas las camadas que ya tienen sus 6 años (2009-2019), aplicados a las empresas del último año completo. Se guardan todas con sus dos puntajes y la marca de elegida, con su huella sha256 en este registro. Se mira en 2031 contra el universo de ese año.

### Resultado #45 (4-nov-2026, Kaggle ie-analisis v27)
**Fuera de tiempo: no pasa.** (1) más ×3 y no más desastres que el universo: 2 de 5; (2) promedio a 6 años mayor: 0 de 5; (3) más ×3 que "solo seguro": 5 de 5.
| Camada (aprende hasta) | Universo ×3 / des / prom | Cruce | Solo extremo | Solo seguro |
|---|---|---|---|---|
| 2015 (2009, 855 filas) | 24,4% / 10,8% / ×2,62 | 27,2% / 7,4% / ×2,61 | 27,7% / 28,7% / ×3,07 | 25,3% / 3,5% / ×2,47 |
| 2016 (2010) | 15,5% / 10,7% / ×2,07 | 16,5% / 7,1% / ×1,92 | 23,6% / 15,1% / ×2,85 | 13,2% / 1,4% / ×1,86 |
| 2017 (2011) | 14,5% / 11,7% / ×1,97 | 14,3% / 3,2% / ×1,82 | 18,9% / 26,7% / ×2,16 | 9,7% / 0,5% / ×1,75 |
| 2018 (2012) | 16,0% / 11,9% / ×2,06 | 15,4% / 3,7% / ×1,87 | 20,0% / 16,7% / ×2,16 | 8,4% / 1,9% / ×1,73 |
| 2019 (2013, 8.870 filas) | 28,5% / 10,4% / ×3,08 | 24,4% / 3,7% / ×2,48 | 29,5% / 13,4% / ×3,11 | 19,4% / 0,0% / ×2,21 |

Lo que se sostiene fuera de tiempo:
- **El modelo de extremos sí:** "solo extremo" tiene más ×3 que el universo en 5 de 5 y mejor promedio en 5 de 5 (con más desastres).
- **El de desastre también:** AUC 0,74-0,83, y el cruce corta los desastres a un tercio (3-7% contra 10-12%).
- **Lo que no se sostiene es la combinación:** fuera de tiempo, la mitad segura deja afuera casi todas las sorpresas y el cruce queda en ×3 como el universo, con menos promedio. En #44 los dos modelos se complementaban porque aprendían de la misma época.
- Cautela a favor: aprende con pocos años (855 a 8.870 filas, sin el bloque de personas, que empieza en 2013). Con más años cerrados puede cambiar; eso lo dirá la lista congelada.
- Cautela en contra: las camadas 2015-2019 ya se miraron; cualquier regla de cruce nueva probada sobre ellas no vale como prueba.

**Lista congelada:** `datos/congelada_cruce_2025.csv`, año 2025, 4.101 empresas, 410 elegidas por el cruce, con sus dos puntajes (también sirve para medir "solo extremo" y "solo seguro"). sha256 `b55867cebe73af868f68d81260b246a118381dee420fd20ea8a4862403d39378`. Se mira en 2031.
Total probadas: 45.

## #46: magnitud × dirección, en años que nadie tocó, escrita el 4-nov-2026 ANTES de correr
De #45: el modelo de extremos transfiere fuera de tiempo; el de desastre, entrenado con todas, al filtrar se lleva las sorpresas. Ángulo nuevo: separar dos preguntas.
- **Horizonte 4 años** (múltiplo del dueño de toda la empresa a 48 meses, quiebra = 0), porque es lo que ya cerró para las camadas nuevas.
- **Camadas de prueba: 2020 y 2021**, que ninguna prueba de extremos o cruce usó. Para cada una, todo se entrena sólo con camadas c ≤ s-4 (sus 4 años terminaron antes de comprar).
- **Modelo M (magnitud):** ¿termina en el 10% de arriba o en el 10% de abajo de su camada? (los dos extremos = 1).
- **Modelo R (dirección):** entrenado SÓLO con las que terminaron en un extremo: ¿arriba (1) o abajo (0)?
- **Elección:** el 30% de la camada con M más alto; dentro, el tercio con R más alto (≈ 10% de la camada).
- **Comparados:** universo; solo M (su 10% de arriba); solo R aplicado a todas (su 10% de arriba).
- **Pasa si, en las DOS camadas:** (1) más ×2 a 4 años que el universo Y no más desastres (≤ ×0,25); (2) promedio a 4 años mayor que el universo.
- Se informa sin criterio: 2017-2019 a 4 años (ya vistas a 6 años, no cuentan), tamaño, AUC de M y de R.
- Cautela: son sólo 2 camadas, y 2020 compra en abril de 2021, cerca del pico de la burbuja.

### Error mío encontrado el 4-nov-2026: corridas que no se repetían
Dos corridas iguales daban listas distintas (279 de 410 elegidas en común). Causa: en insistencia.py, interrelacion.py y analizar.py las 4 columnas sí/no se recorrían en el orden de un `set` de Python, que cambia en cada proceso; eso cambia el relleno al azar de los faltantes y el orden de las columnas. Arreglado (orden fijo + PYTHONHASHSEED=0). Verificado: dos corridas seguidas (v29 y v30) dan la misma lista byte por byte.
Con la versión arreglada: #41 igual (no confirma); #43 AUC 0,656 (antes 0,650) y el cruce agrega en 5 de 7 (antes 2 de 7), sigue sin pasar por las colas (0 de 7); #44 sigue pasando (6 de 7 / 6-7 de 7 / 7 de 7: queda una diferencia mínima entre corridas en el promedio de 2019, que está pegado al del universo); #45 igual (no pasa); la lista congelada se rehizo.
**Lista congelada vigente:** `datos/congelada_cruce_2025.csv`, sha256 `216d486c2abb4b34a7d20cc7fd601ad8e6009c2655a4b341a00722b3fd9e36f7`. La anterior (b55867…) quedó como `congelada_cruce_2025_v1_no_reproducible.csv`; no cuenta. Ninguna de las dos se miró contra resultados (no existen todavía).

### Resultado #46 (4-nov-2026, versión arreglada, v29 = v30)
**No pasa.** (1) más ×2 a 4 años y no más desastres que el universo: 0 de 2; (2) promedio mayor: 1 de 2.
| Camada | Universo ×2 / des / prom4 | Elegidas | Solo magnitud | Solo dirección |
|---|---|---|---|---|
| 2020 | 16,5% / 16,7% / ×1,47 | 26,0% / 29,7% / ×2,08 | 25,6% / 38,5% / ×2,39 | 16,5% / 9,2% / ×1,46 |
| 2021 | 20,3% / 15,8% / ×1,71 | 19,4% / 39,1% / ×1,54 | 21,5% / 46,8% / ×2,50 | 17,6% / 8,8% / ×1,44 |
- La magnitud se reconoce muy bien, fuera de tiempo y en años nuevos: AUC 0,75-0,77.
- **La dirección es lo difícil:** entre las extremas, separar las que suben de las que se hunden da AUC 0,60-0,63. Algo hay, pero no alcanza: las elegidas siguen juntando el doble de desastres.
- Estado del mapa: magnitud, sí; desastre, sí; dirección dentro de lo extremo, débil. Ahí está lo que falta.
Total probadas: 46.

## #47: quién financia el salto, escrita el 4-nov-2026 ANTES de correr
De #46: la magnitud se reconoce; la dirección dentro de lo extremo, no (AUC 0,60-0,63). Ángulo nuevo: la dirección depende de **quién pone la plata**. Referentes: las que emiten acciones rinden menos después (Loughran y Ritter 1995, "The New Issues Puzzle"; Pontiff y Woodgate 2008, "Share Issuance and Cross-sectional Returns"); en las caídas, el rebote depende de quién queda adentro (Cheng, Hameed, Subrahmanyam y Titman 2017).
- **Horizonte 12 meses** (retorno del dueño de toda la empresa, quiebra = 0). **Camadas de prueba: 2022, 2023 y 2024** (las que tengan ≥ 300 empresas con resultado). Las pruebas #43-#46 no las miraron. (Aviso: las primeras pruebas, #1-#37, sí usaron retornos a 12 meses de todos los años; esta regla es nueva y no se ajustó sobre ellas.)
- Cada camada s se entrena sólo con camadas ≤ s-2 (sus 12 meses ya cerraron antes de comprar).
- **Extremo** = 10% de arriba o 10% de abajo de su camada a 12 meses.
- **Huellas nuevas de financiación** (todas con datos anteriores a la compra): emisión neta sobre activos ((emisiones - recompras) / activos), dilución de un año (acciones / acciones del año anterior), años de caja (caja / quema de caja libre; sin quema = 50), deuda nueva sobre activos, y **entregas fallidas** (FTD de la SEC) de los 12 meses antes de presentar: suma sobre acciones y días con falla, y lo mismo en los últimos 3 meses.
- Más las de siempre: números (percentiles) y personas (fondos concentrados que suben su parte, compras y ventas de los de adentro).
- **Modelo M** (¿extremo?) con todo. **Modelo R** (¿arriba o abajo?, entrenado sólo con extremas) en dos versiones: R0 sin las huellas de financiación nuevas, R1 con ellas.
- **Elegidas:** el 30% con M más alto; dentro, el tercio con R1 más alto (≈ 10% de la camada).
- **Pasa si, en TODAS las camadas que cuentan:** (1) AUC de R1 entre las que terminaron extremas ≥ 0,70; (2) las elegidas tienen menos desastres (≤ ×0,5 a 12 meses) que el universo; (3) las elegidas se duplican (≥ ×2) al menos 1,3 veces más que el universo.
- Se informa sin criterio: R0 contra R1 (¿agrega la financiación?), 2019-2021 (ya vistas, no cuentan), tamaño.

### Resultado #47 (4-nov-2026, Kaggle ie-analisis v31)
**No pasa.** (1) AUC de R1 ≥ 0,70: 0 de 3; (2) menos desastres que el universo: 0 de 3; (3) ×2 al menos 1,3 veces el universo: 3 de 3.
| Camada (12 meses) | Universo ×2 / des / prom | Elegidas | Elegidas sin financiación | Solo magnitud | AUC M / R0 / R1 |
|---|---|---|---|---|---|
| 2022 | 9,1% / 13,9% / ×1,25 | 23,5% / 27,4% / ×1,65 | 19,9% / 25,4% / ×1,60 | 21,0% / 46,7% / ×1,63 | 0,82 / 0,675 / 0,687 |
| 2023 | 8,2% / 14,3% / ×1,19 | 25,0% / 22,4% / ×1,79 | 23,8% / 22,4% / ×1,78 | 23,3% / 34,6% / ×1,72 | 0,82 / 0,626 / 0,641 |
| 2024 | 14,3% / 8,8% / ×1,47 | 30,5% / 12,9% / ×2,09 | 34,0% / 14,2% / ×2,27 | 34,3% / 28,3% / ×2,37 | 0,81 / 0,567 / 0,537 |
- La financiación casi no mueve la dirección: R1 le gana a R0 por 0,01-0,02 en 2022-2023 y pierde en 2024.
- Lo que sí aparece, sin criterio: las elegidas se duplican 2-3 veces más que el universo y tienen un promedio a 12 meses más alto en las 3 camadas (×1,65 contra ×1,25; ×1,79 contra ×1,19; ×2,09 contra ×1,47), pero con 1,5-2 veces más desastres. Es una cartera de apuestas, no de sorpresas seguras.
- 2019-2021 (ya vistas): R1 0,63-0,73, mismo patrón.
- Las listas congeladas no cambiaron (216d486c…).
Total probadas: 47.

## #48: magnitud × desastre × confirmación, escrita el 4-nov-2026 ANTES de correr
De #47: la dirección no se adivina el día de la compra. Ángulo nuevo: **esperar a que la empresa la muestre**, como los cinco (entran de a poco y suben cuando la tesis se confirma).
- **Modelos** (huellas de #47: números + personas + financiación; cada camada s aprende con camadas ≤ s-2): M = ¿termina en un extremo a 12 meses?; D = ¿desastre a 12 meses (≤ ×0,5)?
- **Candidatas:** el 30% con M más alto y, dentro, la mitad con D más bajo.
- **Confirmación a los 3 meses** (todo sabido antes de la compra tardía): (a) precio del mes 3 ≥ precio del mes 0; (b) ningún directivo vendió en los meses 0-2; (c) la tenencia de los fondos concentrados en el último trimestre cerrado hasta el mes 1 (su 13F ya presentado) no es menor que en el trimestre anterior al mes 0 (si no hay fondos, cuenta como "no vendieron").
- **Resultado:** 12 meses desde la compra tardía (mes 3 → mes 15): (precio15 × acciones del balance siguiente + dividendos + recompras - emisiones) / (precio3 × acciones); quiebra = 0. Todos los grupos se miden igual.
- **Comparados:** universo (todas con ese resultado), candidatas sin confirmar, elegidas (candidatas confirmadas).
- **Camadas 2019-2024, todas ya vistas: sólo pueden descartarla.** Se descarta si NO se cumple en al menos 5 de 6: elegidas con menos desastres que el universo Y ×2 al menos 1,3 veces el universo.
- Si sobrevive: lista congelada de 2025 (candidatas; la confirmación se aplica cuando haya precios del mes 3) y se espera el resultado real.

### Resultado #48 (4-nov-2026, Kaggle ie-analisis v32)
**Se descarta:** cumple en 1 de 6 (sólo 2019). No se congela lista.
| Camada (12 meses desde el mes 3) | Universo ×2 / des / prom | Candidatas | Elegidas (confirmadas) |
|---|---|---|---|
| 2019 | 25,4% / 4,3% / ×1,85 | 44,6% / 7,6% / ×2,38 | 47,9% / 3,1% / ×2,56 (n 96) |
| 2020 | 5,2% / 17,4% / ×1,01 | 17,5% / 28,5% / ×1,41 | 12,2% / 34,7% / ×1,19 (n 49) |
| 2021 | 8,8% / 11,5% / ×1,28 | 21,7% / 20,9% / ×1,70 | 4,2% / 27,1% / ×0,89 (n 48) |
| 2022 | 8,7% / 14,3% / ×1,25 | 23,2% / 31,3% / ×1,65 | 19,4% / 40,8% / ×1,33 (n 98) |
| 2023 | 10,6% / 11,6% / ×1,35 | 26,5% / 20,1% / ×1,89 | 27,3% / 19,7% / ×2,24 (n 66) |
| 2024 | 15,4% / 9,4% / ×1,53 | 33,4% / 16,7% / ×2,22 | 29,7% / 18,2% / ×2,46 (n 148) |
- La confirmación no protege: en 4 de 6 años las confirmadas tienen MÁS desastres que las candidatas sin confirmar, y en 4 de 6 menos ×2. Lo que sube en los primeros 3 meses entre las volátiles tiende a devolverlo (coherente con la reversión de corto plazo en acciones chicas).
- Lo que se repite en #46-#48: las candidatas (mucha magnitud, poco desastre) tienen 2-3 veces más ×2 y promedio más alto que el universo en 6 de 6, siempre con más desastres. La magnitud se reconoce; el lado, no.
Total probadas: 48.

## #49: la cartera 80/20, escrita el 4-nov-2026 ANTES de correr
De #46-#48: el lado no se adivina, pero las candidatas (M alto, D bajo) tienen promedio mayor que el universo en 6 de 6, con más desastres. Ángulo nuevo: no elegir empresa por empresa sino **armar la cartera** para que el error cueste poco y el acierto pague (Pabrai, "heads I win, tails I don't lose much"; la "barbell" de Taleb).
- **Modelos:** los mismos de #48 (M y D a 12 meses, huellas de #47; cada camada s aprende con ≤ s-2).
- **80% seguro:** el 20% de la camada con D más bajo, a partes iguales.
- **20% extraordinario:** las candidatas (30% con M más alto y, dentro, la mitad con D más bajo), a partes iguales.
- **Retorno de la cartera** en cada camada = 0,8 × promedio del seguro + 0,2 × promedio de las candidatas (12 meses desde el mes 0, quiebra = 0). Se compara con el universo a partes iguales y con el 100% seguro.
- **Camadas 2019-2024, ya vistas: sólo pueden descartarla.** Sobrevive si: (1) le gana al universo en ≥ 5 de 6; (2) su peor camada no es peor que la peor del universo; (3) le gana al 100% seguro en ≥ 4 de 6.
- Si sobrevive: se congela la cartera de 2025 (qué empresas van en cada parte) y se espera el resultado real.

### Resultado #49 (4-nov-2026, Kaggle ie-analisis v33)
**Se descarta:** (1) le gana al universo en 1 de 6; (2) peor camada ×0,997 contra ×1,001 del universo (no cumple por poco); (3) le gana al 100% seguro en 6 de 6.
| Camada (12 meses) | Cartera 80/20 | Universo | 100% seguro (des) | Candidatas (des) |
|---|---|---|---|---|
| 2019 | ×1,81 | ×2,13 | ×1,52 (0,3%) | ×2,97 (5,4%) |
| 2020 | ×1,12 | ×1,08 | ×1,09 (1,6%) | ×1,24 (29,6%) |
| 2021 | ×1,00 | ×1,00 | ×0,96 (2,6%) | ×1,14 (32,5%) |
| 2022 | ×1,21 | ×1,25 | ×1,16 (1,5%) | ×1,41 (26,3%) |
| 2023 | ×1,18 | ×1,19 | ×1,09 (0,9%) | ×1,53 (24,2%) |
| 2024 | ×1,27 | ×1,47 | ×1,11 (0,9%) | ×1,89 (13,2%) |
Acumulado de las 6: cartera ×3,6; universo ×5,0; 100% seguro ×2,2 (las camadas se superponen en el tiempo: es una suma ilustrativa, no una cartera real).
- Las dos partes hacen su trabajo: lo seguro baja los desastres de 6-19% a 0,3-2,6%, y el 20% extraordinario le suma a lo seguro en 6 de 6.
- Lo que no alcanza: el universo a partes iguales está lleno de acciones chicas cuyo promedio lo tiran para arriba unas pocas que se multiplican. Con un 80% en empresas grandes y seguras, la cartera no llega a ese promedio.
- Las candidatas solas le ganan al universo en promedio en 6 de 6 (ya se sabía desde #46-#48, y en años ya vistos).
Total probadas: 49.

## #50: cuánto poner (Kelly), escrita el 4-nov-2026 ANTES de correr
De #49: lo seguro y lo extraordinario funcionan por separado, pero un 80% fijo en empresas grandes no alcanza al universo. Ángulo nuevo: no **qué** elegir sino **cuánto** poner en cada una (Pabrai usa Kelly: apuesta fuerte sólo cuando las chances están muy a favor).
- **Modelos:** P2 = probabilidad de ×2 a 12 meses y PD = probabilidad de desastre (≤ ×0,5), mismas huellas de #47, mismo HistGradientBoosting; cada camada s aprende con ≤ s-2.
- **Peso Kelly** de cada empresa (apuesta que gana +100% con P2 o pierde 50% con PD): f = 2·P2 - PD; si f ≤ 0 no entra. Pesos = f / suma de f, con tope 5% por empresa (lo que sobra se reparte entre las demás). Si ninguna tiene f > 0, la cartera queda en caja (×1).
- Pueden entrar todas las empresas, chicas incluidas.
- **Retorno** = suma de peso × resultado a 12 meses desde el mes 0 (quiebra = 0). **Desastres** = peso de la cartera puesto en empresas que terminan ≤ ×0,5, contra el % de desastres del universo a partes iguales.
- **Camadas 2019-2024, ya vistas: sólo pueden descartarla.** Sobrevive si: (1) le gana al universo en ≥ 5 de 6; (2) su peor camada no es peor que la peor del universo; (3) menos desastres que el universo en ≥ 5 de 6.
- Si sobrevive: se congela la cartera de 2025 con sus pesos y se espera el resultado real.

### Resultado #50 (4-nov-2026, Kaggle ie-analisis v35)
**Se descarta:** (1) le gana al universo en 6 de 6; (2) peor camada ×1,35 contra ×1,00 del universo (cumple); (3) menos desastres en 0 de 6 (no cumple).
| Camada (12 meses) | Cartera Kelly | Universo | Peso en desastres (universo) | Peso en ×2 (universo) | Empresas con peso |
|---|---|---|---|---|---|
| 2019 | ×3,28 | ×2,13 | 6,3% (6,1%) | 55,5% (34,1%) | 1720 |
| 2020 | ×1,67 | ×1,08 | 22,9% (15,9%) | 20,9% (6,1%) | 1642 |
| 2021 | ×1,35 | ×1,00 | 28,5% (19,1%) | 14,3% (5,0%) | 2786 |
| 2022 | ×1,65 | ×1,25 | 23,6% (13,9%) | 20,5% (9,1%) | 2211 |
| 2023 | ×1,91 | ×1,19 | 25,6% (14,3%) | 21,8% (8,2%) | 1650 |
| 2024 | ×1,50 | ×1,47 | 9,0% (8,8%) | 17,1% (14,3%) | 2566 |
Acumulado ilustrativo: Kelly ×35, universo ×5,0.
- Ninguna empresa llegó al tope del 5%: los pesos quedaron repartidos entre 1600-2800 empresas, cargados hacia las chicas (tamaño medio 0,41-0,54).
- Es la primera regla que le gana al universo en los 6 años y con mejor peor año. Lo que la descarta es el criterio de desastres: pone más peso en empresas que caen a la mitad, a cambio de mucho más peso en las que se duplican.
- Años ya vistos: no confirma nada. No se congela lista (lo dice el criterio escrito antes).
Total probadas: 50.

## #51: el placebo de Kelly, escrita el 4-nov-2026 ANTES de correr
Pregunta: ¿el ×35 de #50 sale de lo que el modelo sabe de cada empresa o sólo de inclinarse a las chicas?
- **Real:** la cartera Kelly de #50, tal cual (mismos modelos, f = 2·P2 - PD, tope 5%).
- **Placebo:** en cada camada, los pares (P2, PD) se barajan al azar entre empresas del mismo decil de tamaño (las sin tamaño, entre sí). Misma fórmula, mismo tope. Conserva la inclinación a lo chico y la forma de los pesos; borra lo que el modelo sabe de cada empresa. 100 barajadas por camada (semillas 0-99).
- **La máquina sabe algo si:** la cartera real supera al percentil 95 de los placebos en ≥ 5 de 6 camadas (2019-2024).
- Se informa también el peso en desastres real contra el de los placebos.

### Resultado #51 (5-nov-2026, Kaggle ie-analisis v36)
**La máquina sabe algo:** la cartera real supera al percentil 95 de los placebos en 5 de 6 camadas.
| Camada | Real | Placebo mediana | Placebo p95 | Placebos que le ganan | Desastres real / placebo |
|---|---|---|---|---|---|
| 2019 | ×3,32 | ×2,27 | ×2,44 | 0/100 | 6,2% / 8,5% |
| 2020 | ×1,63 | ×1,07 | ×1,15 | 0/100 | 23,1% / 23,7% |
| 2021 | ×1,36 | ×1,04 | ×1,10 | 0/100 | 28,3% / 26,6% |
| 2022 | ×1,67 | ×1,26 | ×1,34 | 0/100 | 24,6% / 18,3% |
| 2023 | ×1,91 | ×1,23 | ×1,40 | 0/100 | 25,7% / 19,1% |
| 2024 | ×1,51 | ×1,49 | ×1,55 | 31/100 | 9,0% / 8,8% |
- La inclinación a lo chico sola da lo mismo que el universo (placebo ≈ universo). Lo que suma está en las empresas que el modelo elige dentro de cada tamaño.
- Los desastres extra de Kelly (2022-2023) también vienen del modelo: elige lo que se mueve mucho, para los dos lados.
- 2024 es la única camada sin ventaja.
- La corrida de #50 dentro de v36 dio casi igual que v35 (×35,5 contra ×35,0; 1463-2837 empresas contra 1650-2786): hay una pequeña variación entre corridas que no está resuelta. No cambia ninguna conclusión.
- Años ya vistos: muestra que la ventaja no es la inclinación a lo chico, no que vaya a repetirse.
Total probadas: 51.

## #52-#54: redes de directores (plan en notas/13), escritas el 7-nov-2026 ANTES de correr
Datos: formularios 3/4/5 de la SEC 2006-2026 (REPORTINGOWNER: quién reporta, con la marca de director, directivo o dueño de más del 10%). Una persona = su CIK de la SEC (hasheado). Para la camada `anio` se usan sólo formularios presentados en el año calendario `anio`, todos anteriores a la compra (mes siguiente al 10-K, en `anio`+1).
- **#52 Directorio central (H1).** Red de empresas unidas si comparten al menos un director ese año. Rasgos: grado, cercanía armónica, intermediación (aproximada, 300 fuentes), cantidad de directores y fracción de ellos que se sienta en otro directorio.
- **#53 Contagio por la red (H2).** De las empresas vecinas (comparten director): retorno medio en los 12 meses antes de la compra y fracción que se duplicó o cayó a la mitad en esos 12 meses (precios mensuales ya usados, nada posterior a la compra).
- **#54 Control familiar (H5).** Dueños de más del 10% que son personas (no sociedades: sin INC, LLC, LP, FUND, CAPITAL, PARTNERS, HOLDINGS, BANK, GROUP, CORP, TRUST COMPANY); y si dos o más directores o directivos de la empresa comparten apellido.
Cada bloque se prueba por separado, sumado a los rasgos de #50 (NUM + PERS + FIN), mismos modelos P2 y PD a 12 meses, cada camada s aprende con ≤ s-2, camadas 2019-2024 (ya vistas: sólo pueden descartar).
**Sobrevive (cada bloque) si cumple las tres:**
1. **Lado:** AUC de (P2 - PD) para separar las que se duplican de las que caen a la mitad (sólo esas dos), con el bloque menos sin el bloque ≥ +0,01 en ≥ 5 de 6 camadas.
2. **Placebo:** la cartera Kelly con el bloque real supera al percentil 95 de 100 carteras Kelly con el bloque barajado entre empresas del mismo decil de tamaño (mismo modelo, sólo se baraja el bloque en las de prueba) en ≥ 5 de 6 camadas.
3. **Desastres:** peso de la cartera en desastres con el bloque ≤ sin el bloque + 0,5 puntos en ≥ 4 de 6 camadas.
Lo que sobreviva no se cree: se congela su lista de 2025 y se repite tal cual en China.

### Resultado #52-#54 (7-nov-2026, Kaggle ie-red v1 + ie-analisis v37)
Datos: 83 trimestres de formularios 3/4/5 (2006-2026), 1,66 millones de filas empresa-persona-año. Red por año: 5.200-8.300 empresas, 10-16 mil uniones, ~31-40 mil directores. Rasgos con dato: central 63.722 filas, contagio 48.148, familia 65.142.
**Las tres se descartan.**
| Bloque | Lado (≥ +0,01) | Placebo (> p95) | Desastres (≤ +0,5) | Veredicto |
|---|---|---|---|---|
| #52 directorio central | 0 de 6 | 3 de 6 | 5 de 6 | se descarta |
| #53 contagio por la red | 3 de 6 | 0 de 6 | 4 de 6 | se descarta |
| #54 control familiar | 2 de 6 | 2 de 6 | 5 de 6 | se descarta |
Lado (AUC ×2 contra desastre), con bloque / sin bloque: central 0,82/0,82 · 0,58/0,58 · 0,59/0,66 · 0,62/0,62 · 0,54/0,55 · 0,60/0,59; contagio 0,80 · 0,59 · 0,62 · 0,64 · 0,55 · 0,60; familia 0,81 · 0,56 · 0,65 · 0,66 · 0,55 · 0,62.
- Las subas de la cartera con algún bloque (familia 2021 ×1,74 contra ×1,36; contagio 2024 ×1,82 contra ×1,51) aparecen igual con el bloque barajado dentro del tamaño: es el ruido de reentrenar con más columnas, no lo que dicen los directores.
- Lo único que se repite: con familia, el peso en desastres baja en 2020-2023 (22,0/22,2/9,9/16,5% contra 23,1/28,3/24,6/25,7%). No estaba en el criterio y no se convierte en hallazgo mirando después; queda como pregunta para una prueba nueva, con su propio criterio.
- Lo que dice la literatura (Larcker-So-Wang) no aparece acá, sumado a lo que el modelo ya sabe: lo que la red aporta ya está en el tamaño, los balances y las personas.
Total probadas: 54.

## #55-#56: los dos lados del mostrador (notas/14, tipos B y F), escritas el 7-nov-2026 ANTES de correr
Antecedente: Aragon y Martin (JFE 2012): las opciones que los fondos declaran en el 13F predicen la volatilidad y el retorno de la acción (1,55% anormal en el trimestre, 1999-2006).
Datos: 13F 2013-2026 con puts y calls (op13f), sólo fondos que declaran alguna opción en ese trimestre, con sus acciones. Para cada empresa se toma el último trimestre cuyo 13F ya venció (cierre del trimestre + 45 días) antes del mes de compra, como en #42.
- **#55 Apuesta neta (B).** Acciones de base en PUT, en CALL y acciones (SH) de esos fondos. Rasgos: puts / (puts + calls); neto = (SH + CALL - PUT) / (SH + CALL + PUT); el cambio de puts / (puts + calls) contra el trimestre anterior; puts sobre acciones en circulación; cantidad de fondos con opciones.
- **#56 Cobertura (F).** Por empresa: parte de los fondos que tienen acciones y puts a la vez (cubiertos); parte de las acciones de base en puts de fondos SIN acciones de esa empresa (put descubierto, apuesta en contra pura); ídem calls sin acciones (call descubierto, apuesta a favor pura).
Mismo criterio que #52-#54 (sumado a los rasgos de #50, cada camada aprende con ≤ s-2, camadas 2019-2024, ya vistas: sólo descartan). Sobrevive (cada bloque) si: (1) lado ≥ +0,01 en ≥ 5 de 6; (2) Kelly real > p95 de 100 con el bloque barajado dentro del decil de tamaño en ≥ 5 de 6; (3) desastres ≤ sin bloque + 0,5 puntos en ≥ 4 de 6.

### Resultado #55-#56 (7-nov-2026, Kaggle ie-op13f-2013/2020/2023 + ie-analisis v39)
Datos: 12,3 millones de filas de 13F 2013-2026 de fondos que declaran opciones (~650-1.250 fondos por trimestre, ~20-26 mil puts y otros tantos calls), 7.101 empresas. Con dato en las filas: 32.103 (las empresas con opciones son las más grandes y líquidas).
(Una primera corrida, v38, usó opciones sólo hasta 2020q2 por un corte de tiempo en la descarga; no cuenta.)
**Las dos se descartan.**
| Bloque | Lado (≥ +0,01) | Placebo (> p95) | Desastres (≤ +0,5) | Veredicto |
|---|---|---|---|---|
| #55 apuesta neta | 1 de 6 | 0 de 6 | 5 de 6 | se descarta |
| #56 cobertura | 1 de 6 | 0 de 6 | 5 de 6 | se descarta |
- La cartera con el bloque real queda por debajo del percentil 95 del placebo los 6 años: lo que suma o resta es ruido de reentrenar.
- Aragon y Martin medían 1999-2006 y retorno en el mismo trimestre; acá, sumado a lo que el modelo ya sabe y a 12 meses, no aparece.
Total probadas: 56.

## #57-#58: el portero del índice (notas/14, capa 2, tipo D/E), escritas el 7-nov-2026 ANTES de correr
El comité de S&P Dow Jones decide a discreción quién entra y quién sale del S&P 500, y con esa decisión mueve la plata de los fondos indexados (que son los mismos tres gigantes de la capa supracorporativa).
Antecedentes: altas con salto al anuncio que después se diluye; el efecto se achicó con los años (Greenwood y Sammon, 2022); las bajas rebotan después (Chen, Noronha y Singal, 2004).
Datos: tabla de cambios del S&P 500 con fecha efectiva y motivo (Wikipedia, «Historical components of the S&P 500», con su referencia a S&P en cada fila). Símbolo → empresa con los formularios 3/4/5 (símbolo y CIK del emisor, por año). Precios mensuales ya usados.
- **#57 Altas** con fecha efectiva 2011-2024.
- **#58 Bajas por valor de mercado** («market capitalization»), sin las bajas por compra, fusión o escisión, 2011-2024.
- **Retorno:** 12 meses desde el cierre del primer mes después de la fecha efectiva (sin el salto del anuncio). **Control:** todas las demás empresas con precio en esos mismos meses y del mismo decil de tamaño (activos del último balance). **Exceso** = log(1 + retorno) - promedio de log(1 + retorno) del control.
- **Pasa (cada una) si:** (1) el exceso medio de todos los eventos es > 0 con el intervalo 95% por remuestreo (2.000 veces) sin tocar el 0; (2) exceso medio > 0 en ≥ 9 de los 14 años.
- Se informa también: la tasa de ×2 y de desastre de cada grupo contra su control, y cuántos eventos se pudieron unir a una empresa.

### Resultado #57-#58 (7-nov-2026, Kaggle ie-red v2 + ie-analisis v40)
Unidos a empresa: 283 altas (9 sin unir) y 99 bajas por valor (1 sin unir); con precio y control: 225 altas y 96 bajas.
**Las dos se descartan.**
| | Eventos | Exceso medio a 12 meses (IC95) | Años positivos | ×2 contra control | Desastre contra control |
|---|---|---|---|---|---|
| #57 altas | 225 | -0,018 (-0,072 a +0,035) | 7 de 14 | 1,3% / 3,3% | 4,0% / 4,7% |
| #58 bajas por valor | 96 | -0,013 (-0,105 a +0,078) | 6 de 14 | 10,4% / 3,4% | 6,3% / 4,6% |
- Después de entrar, nada: el índice ya no regala (como Greenwood y Sammon).
- Las que echan tienen **tres veces más ×2** que su control y también más desastres: la decisión del portero marca magnitud, para los dos lados. Es lo mismo que vienen mostrando #46-#56: lo que se ve desde afuera dice cuánto, no hacia dónde.
Total probadas: 58.

## #59: la agenda marca la dirección (notas/14, de arriba hacia abajo), escrita el 7-nov-2026 ANTES de bajar precios
Idea de Fabri: si los que deciden juegan de los dos lados con cada empresa, la dirección no está en la empresa sino en el mundo que se ponen a construir, y eso se anuncia antes.
- **Agenda:** temas publicados por Bilderberg 2008-2019 y 2022-2026 (sitio oficial y su archivo en Internet Archive; 2020-2021 no hubo reunión).
- **Temas y sectores fijados antes de ver precios** (entrenar/agenda.py, lista cerrada de 12): defensa→ITA, ciber→HACK, tecnología/IA→SOXX, energía→XLE, clima→ICLN, finanzas→XLF, salud→XLV, China→FXI, Europa→VGK, India→INDA, emergentes/África→EEM, Medio Oriente→KSA. Un tema cuenta si su patrón de palabras aparece en la agenda de ese año.
- **Exceso** = log del fondo del sector menos log de SPY, desde el cierre de junio del año de la reunión, a 12 y a 36 meses.
- **Comparación por año:** promedio de los temas EN la agenda menos promedio de los temas FUERA (entre los 12 con precio). Variante **nuevos:** temas en la agenda que no estaban en las dos anteriores.
- **Pasa si (a 36 meses, la principal):** el promedio de las diferencias por año > 0 con IC 95% por remuestreo de años sin tocar el 0, y diferencia > 0 en ≥ 70% de los años. Se informa igual a 12 meses y la variante nuevos.
- Cautelas escritas antes: pocos años (≈ 14 a 36 meses), fondos que no existían al principio (HACK 2014, INDA 2012, KSA 2015), y la agenda de un solo foro.
- Corrección antes de ver precios: el patrón de clima tomaba «sustainable» de «¿es sostenible la recuperación?» (2014); queda «sustainability».

### Resultado #59 (7-nov-2026, local, datos/agenda_resultados.json)
**No pasa** (criterio principal, 36 meses): diferencia media +2,6 puntos (IC95 -8,0 a +11,4), positiva en 8 de 14 años. Nuevos: -13,1 puntos, 4 de 7.
**A 12 meses (informado, no es el criterio):** +3,3 puntos (IC95 -0,9 a +7,5), positiva en 11 de 16 años (69%). Es lo más cerca que estuvo una señal de dirección en todo el registro, pero no alcanza.
- El peor año es 2009: el tema era la crisis financiera y los bancos siguieron cayendo (-52 puntos a 36 meses). En la agenda conviven **problemas** (crisis, amenazas) y **proyectos** (lo que se ponen a construir); el criterio los mezcló. Separarlos ahora sería mirar después: si se prueba, va con criterio nuevo y sobre otro foro (Davos, BIS) que no se miró.
Total probadas: 59.

## #60: los proyectos de Davos (otro foro, nunca mirado), escrita el 7-nov-2026 ANTES de bajar las listas
Viene de #59: la agenda mezcla problemas y proyectos. Davos los publica separados: «Top 10 Emerging Technologies» (proyectos, desde 2012, junio) y «Global Risks Report» (problemas, enero). Acá sólo proyectos.
- **Listas:** las 10 tecnologías de cada año 2012-2025, del sitio del Foro o su copia en Internet Archive (el sitio bloquea la descarga automática).
- **Tecnología → sector**, mismos 12 fondos de #59, con estos patrones fijados ahora: salud (XLV): medic|health|biolog|genom|gene|cell|drug|vaccin|microbio|organ|diagnos|neuro|crispr|protein|enzym; clima (ICLN): solar|batter|hydrogen|carbon|fuel cell|perovskite|grid|renewab|fusion|electric vehicle|green|ammonia|fertil; tecnología (SOXX): \bai\b|artificial intelligence|machine|quantum|comput|chip|sensor|internet of things|blockchain|5g|6g|robot|autonom|augmented|virtual|metaverse|semiconductor|neural|data|wireless|display|lidar|2d material|graphene; defensa (ITA): space|satellite|drone|aircraft; energía (XLE): oil|natural gas|shale. Una tecnología puede caer en más de un sector.
- **Medida y criterio:** idénticos a #59 (exceso contra SPY desde el cierre de junio del año de la lista; en la lista contra fuera; pasa a 36 meses con IC95 sin tocar el 0 y ≥ 70% de años positivos; se informa 12 meses).
- Cautela escrita antes: casi todo cae en tecnología, salud y clima, así que «fuera» es casi siempre lo mismo (finanzas, Europa, China, emergentes, energía): la prueba compara proyectos contra el resto de la economía, no un proyecto contra otro.

### Resultado #60 (7-nov-2026, local, datos/davos_resultados.json)
Listas conseguidas: 2015, 2016, 2017, 2019, 2020, 2021, 2023, 2024, 2025 (PDF del Foro en www3.weforum.org y copia de 2016 en Internet Archive). Faltan 2012-2014, 2018 y 2022 (el servidor no las entrega).
**Pasa, tal como estaba escrito** (36 meses): diferencia media +20,8 puntos (IC95 +10,1 a +31,8), positiva en 7 de 7 años. A 12 meses: +7,6 (IC95 -3,8 a +20,5), 4 de 9.
| Año | En la lista | Fuera | Diferencia a 36 meses |
|---|---|---|---|
| 2015 | -3,3 | -18,7 | +15,3 |
| 2016 | +6,0 | -4,9 | +10,9 |
| 2017 | +17,2 | -27,8 | +45,1 |
| 2019 | +22,8 | -19,5 | +42,4 |
| 2020 | +5,8 | -9,0 | +14,8 |
| 2021 | -18,6 | -19,9 | +1,3 |
| 2023 | +1,9 | -13,9 | +15,8 |
**Por qué todavía no se cree (escrito como cautela antes de correr):** la lista cae casi siempre en los mismos tres sectores (tecnología, salud, clima; defensa sólo en 2015 y 2021). Entonces lo que pasa es «tecnología, salud y clima le ganaron a finanzas, Europa, China, emergentes y petróleo entre 2015 y 2026»: una apuesta casi fija, no algo que la lista de cada año agregue. Faltan además 5 de los 14 años.
**Lo que lo separaría:** bajar al nivel de cada tecnología, con fondos específicos que existan (baterías, nuclear, genómica, robótica, cuántica, espacio, hidrógeno, IA), y comparar lo que entra a la lista ese año contra lo mismo cuando no está. Si la lista sabe algo, tiene que notarse cuando cambia. Va con criterio nuevo, escrito antes.
Total probadas: 60.

## #61: los proyectos de Davos, tecnología por tecnología, escrita el 7-nov-2026 ANTES de bajar precios
Para separar #60 de una apuesta fija a tecnología, salud y clima: ahora cada categoría tiene su fondo específico, y entra o no entra a la lista según el año.
**Categorías (patrón → fondo), lista cerrada:**
baterías (batter → LIT) · nuclear (nuclear → NLR) · genómica (genom|gene|crispr|dna|cell atlas|omics|metabolic engineering|phage|living therapeutic → ARKG) · fármacos (drug|vaccin|protein|glp-1|nanozym|ageing|aging|therapeut → XPH) · diagnóstico y dispositivos médicos (biopsy|diagnos|microneedle|biomarker|breath|sensing|organs-on-chips|virtual patient|digital medicine|healthcare|neural electronic|optogenet|transplant → IHI) · robótica (robot → BOTZ) · IA y software (artificial intelligence|\bai\b|deep learning|neuromorphic|machine|watermark|privacy → AIQ) · cuántica (quantum → QTUM) · chips y sensores (sensor|lens|chip|2d material|nanosensor|surfaces|computing → SOXX) · espacio y aeronaves (space|satellite|drone|aviation|high altitude|aircraft → ITA) · solar (solar|sun|perovskite|sunshine → TAN) · hidrógeno y combustibles (hydrogen|fuel cell|ammonia|aviation fuel|catalyst → ICLN) · autos (vehicle|autonomous vehicle → DRIV) · blockchain (blockchain → BLOK) · impresión 3D y manufactura (additive|manufactur|printed → PRNT) · agro y alimentos (farm|crop|fertil|livestock|food|nitrogen → MOO) · agua (water → PHO) · construcción (cement|houses|built world|communities → PKB) · materiales (plastic|bioplastic|thermoset|material|elastocal|composite → XLB) · comunicaciones (wireless|telepresence|communication|connects the globe|internet of nanothings → IYZ) · realidad virtual (metaverse|immersive|spatial computing|virtual → METV) · captura de carbono (carbon|decarboni|osmotic|renewable energy|storage of renewable → ICLN).
**Medida:** exceso contra SPY desde el cierre de junio del año de la lista, a 36 meses (principal) y 12 meses. Años de lista: 2015-2017, 2019-2021, 2023-2025.
**Pasa si las dos:**
1. **Entre categorías, cada año:** promedio de las categorías en la lista menos el de las que no están (sólo categorías con precio ese año): media de los años > 0 con IC95 sin tocar el 0, y > 0 en ≥ 70% de los años.
2. **Dentro de cada categoría, en el tiempo:** para las categorías que estuvieron y no estuvieron en distintos años, el exceso de sus años «en la lista» menos el de sus años «fuera»: promedio entre categorías > 0 y positivo en más de la mitad de ellas.

### Resultado #61 (7-nov-2026, local, datos/davos2_resultados.json)
**No pasa** (36 meses): entre categorías, +6,8 puntos (IC95 -3,4 a +15,2), positiva en 6 de 7 años → el intervalo toca el 0 (falla la condición 1). Dentro de cada categoría: +6,3 puntos, positiva en 11 de 20 (cumple la 2). A 12 meses: +2,0 (IC95 -3,0 a +7,2), 6 de 9.
- **Lo que esto dice de #60:** el +20,8 de #60 era casi todo la apuesta fija a tecnología, salud y clima. Al nivel de cada tecnología queda un tercio (+6,8), con la misma inclinación a favor (6 de 7 años) pero sin fuerza para descartar el azar.
- Donde la lista acertó al momento: genómica (+154 puntos los años que entró contra los que no), solar (+69), realidad virtual (+45), IA (+38). Donde no: manufactura (-58), hidrógeno (-41), diagnóstico (-35), baterías (-33). Leído después: no cuenta.
- Con 7 años y 22 categorías la prueba es chica. Lo que la confirmaría o la mata sin mirar atrás: las listas de 2012-2014, 2018 y 2022 (faltan) y las que vengan (2026 en adelante), con este mismo criterio sin tocar.
Total probadas: 61.

## Congelada hacia adelante: consenso de la élite 2025-2026 (7-nov-2026)
De la exploración de #59-#61 (consenso = menciones del sector en Bilderberg y Davos en los últimos 3 años): a 36 meses, sólo los sectores con consenso ≥ 4 le ganaron a SPY (+19,5 puntos contra -11 a -21 del resto; casi todo tecnología, con clima como excepción fuerte en contra). Es exploración: no se cree hasta que se cumpla hacia adelante.
Predicción congelada en datos/congelada_consenso_2025_2026.csv (sha256 e73bfd76e79d7145e8cbcfcd8272bef34cfd9b3b5f7ccdc1a90ed80a49a85433):
- **2025** (de junio 2025 a junio 2028): defensa (ITA, 5), tecnología (SOXX, 6), clima (ICLN, 5), salud (XLV, 4) le ganan a SPY.
- **2026** (de junio 2026 a junio 2029): defensa (ITA, 4), tecnología (SOXX, 5) le ganan a SPY.
Se mide en julio de 2028 y de 2029 contra SPY, sin cambiar nada.

## #62: las empresas que hablan el idioma de la élite (exploración 2013-2016, criterio escrito ANTES de abrir 2017-2020)
Datos: sección 1 («el negocio») del 10-K, EDGAR-CORPUS; coincidencias por mil palabras con los patrones de los 12 temas de Bilderberg (#59) y las 22 categorías de Davos (#61). 17.910 empresas-año presentadas en 2013-2016 (exploración, ya mirada).
**Lo que mostró la exploración** (exceso del log del múltiplo contra la mediana de su sector y año; 90-100 menos 0-20 del percentil dentro del sector):
- `tema_total` (cuánto habla de cualquiera de los temas): a 4 años +17/+17/+35/+41 puntos (2013-2016), a 6 años +13/+41/+51/+35; desastres a 6 años 14,3% contra 22,1%.
- `alin` (lo mismo ponderado por el consenso de cada año): a 4 años +8/+6/+26/+23. **Ponderar por el consenso no agrega** sobre hablar de los temas.
**Criterio para 2017-2020 (sin tocar después):** variable `tema_total`, percentil dentro de sector y año; horizonte principal 4 años (`_ret4`, quiebra = 0).
1. Exceso del decil de arriba (90-100) menos el quintil de abajo (0-20), dentro de sector y año: > 0 en ≥ 3 de 4 años y promedio > 0.
2. Lo mismo dentro del tercio de tamaño (activos) además del sector: > 0 en ≥ 3 de 4 años (que no sea tamaño).
3. Desastres (≤ ×0,5 a 4 años): menos en el decil de arriba que en el quintil de abajo en ≥ 3 de 4 años.
Se informa además: 12 meses, 6 años donde exista, y `alin` (si el consenso agrega fuera de muestra).

### Resultado #62, confirmación 2017-2020 (7-nov-2026, Kaggle ie-tema10k-2017..2020 + ie-analisis): **PASA**
17.106 empresas-año nunca miradas. Decil de arriba menos quintil de abajo de `tema_total`, a 4 años:
| | 2017 | 2018 | 2019 | 2020 | Criterio |
|---|---|---|---|---|---|
| dentro de sector | +23,3 | +26,5 | +17,3 | -4,1 | 3 de 4, media +15,8 ✅ |
| dentro de sector y tercio de tamaño | +16,9 | +15,8 | +14,3 | -10,7 | 3 de 4 ✅ |
| desastres arriba - abajo | -5,9 | -8,0 | -4,3 | -2,2 | 4 de 4 ✅ |
| a 6 años (informado) | +41,8 | +38,1 | +30,6 | +22,3 | 4 de 4 |
`alin` (ponderado por consenso) a 4 años: +25,7/+24,8/+4,1/-15,0: otra vez **no agrega** sobre `tema_total`.
**Cautela antes de creerlo:** el sector es de un dígito (muy grueso). Si las palabras sólo separan a las tecnológicas dentro de cada sector, la señal es la apuesta a tecnología de 2013-2024. Siguiente obligatorio: control con el código industrial de 3 dígitos de la SEC, y contra la tendencia de cada industria.
Total probadas: 62.

## #63: Tr v2, red neuronal con los temas de la élite, escrita el 7-nov-2026 ANTES de correr
Pedido de Fabri: que lo encontrado entre a Tr, entrenando una red neuronal.
- **Rasgos:** los de Tr (#50: balances, personas, financiación) + densidad de cada tema de la élite en «el negocio» del 10-K (34 temas y su total, percentil por año). Temas: EDGAR-CORPUS (10-K 2013-2020) y bajados de la SEC (2021-2026).
- **Modelo:** perceptrón de dos capas (128 y 64), 3 semillas promediadas, faltantes en 0,5 con su marca. Mismas etiquetas (×2 y desastre a 12 meses) y misma cartera Kelly (f = 2·P2 - PD, tope 5%).
- **Se comparan cuatro:** Tr actual (árboles), red sin temas, árboles con temas, red con temas (candidata).
- **Tr v2 reemplaza a Tr en el juego si:** gana a Tr en ≥ 4 de 6 camadas (2019-2024), gana al universo en ≥ 5 de 6, y su peso en desastres no supera al de Tr en más de 1 punto en ≥ 4 de 6. Si reemplaza: se entrena con todo, se congela su cartera de 2025 con su sha256 y la lista vieja queda en el registro.

### #62, control por industria fina (7-nov-2026, ie-analisis v44, SIC de submissions.zip, grupos de ≥ 8 empresas)
| Decil de arriba menos quintil de abajo, a 4 años | 2013 | 2014 | 2015 | 2016 | **2017** | **2018** | **2019** | **2020** |
|---|---|---|---|---|---|---|---|---|
| SIC de 2 dígitos | -12,6 | +7,3 | +21,9 | +17,3 | +10,5 | +38,8 | +17,6 | -5,0 |
| SIC de 3 dígitos | -13,1 | +2,7 | +14,2 | +3,1 | +15,5 | +34,5 | +16,6 | -5,0 |
| SIC de 3 dígitos y tercio de tamaño | 0,0 | +7,9 | +4,7 | -5,4 | +17,4 | +23,0 | +22,6 | +5,5 |
- En la confirmación (2017-2020, en negrita) sobrevive al control fino: 3 de 4 dentro de la industria de 3 dígitos y 4 de 4 dentro de industria y tamaño, con menos desastres en casi todos.
- En la exploración (2013-2016) la señal dentro de la industria fina era débil (+1,7 de promedio). No es «ganaron las tecnológicas», pero tampoco es pareja en el tiempo.
- **Cambio antes de correr (7-nov, sin ningún resultado de #63 visto):** para no esperar la bajada de 30.000 10-K de 2021-2025, la comparación se hace en las camadas **2017, 2018 y 2019** (las que tienen temas del corpus; cada una aprende con ≤ s-2). Reemplaza si: gana a Tr en ≥ 2 de 3, gana al universo en 3 de 3, y desastres ≤ Tr + 1 punto en ≥ 2 de 3.

### Resultado #63 (7-nov-2026, Kaggle ie-trv2-2017/2018/2019): **no reemplaza**
| Camada | Universo | Tr (árboles) | Red | Árboles + temas | Red + temas |
|---|---|---|---|---|---|
| 2017 | ×1,10 | ×1,89 (lado 0,711) | ×1,16 (0,635) | ×1,73 (**0,724**) | ×1,16 (0,625) |
| 2018 | ×0,96 | ×1,81 (0,625) | ×1,12 (0,537) | ×1,64 (**0,669**) | ×1,27 (0,622) |
| 2019 | ×2,13 | ×3,28 (0,809) | ×2,47 (0,774) | ×3,31 (0,799) | ×2,50 (0,790) |
- La red neuronal pierde contra los árboles en las 3 camadas, con o sin temas (×1,16 contra ×1,89 en 2017). Coincide con lo conocido para datos de tabla: los árboles suelen ganarle a las redes (Grinsztajn, Oyallon y Varoquaux, NeurIPS 2022).
- **Los temas mejoran el lado** en los árboles en 2 de 3 camadas (+0,013 y +0,044 de AUC), la primera mejora de dirección en todo el registro; pero la cartera a 12 meses no sube (×1,73 y ×1,64 contra ×1,89 y ×1,81; 2019 casi igual). La señal de los temas trabaja a 4-6 años (#62), y la cartera mira 12 meses.
Total probadas: 63.

## #64: Tr a 4 años, escrita el 8-nov-2026 ANTES de correr
De #62-#63: los temas de la élite marcan dirección a 4-6 años, no a 12 meses. Pedido de Fabri: que Tr juegue con eso.
- **Modelo:** árboles como Tr (HistGradientBoosting), etiquetas a 4 años: ×2 (`_ret4` ≥ 2) y desastre (≤ ×0,5, quiebra = 0). Cartera Kelly f = 2·P2 - PD, tope 5%.
- **Sin mirar el futuro:** la camada s aprende sólo con filas ≤ s-4 (su resultado a 4 años ya se sabía al comprar).
- **Se comparan:** Tr a 4 años sin temas y con temas (candidato). Camadas 2017, 2018 y 2019 (las que tienen temas del corpus y resultado a 4 años).
- **Juega en el juego si:** con temas le gana a sin temas en ≥ 2 de 3, al universo en 3 de 3, y su peso en desastres no supera al de sin temas en más de 1 punto en ≥ 2 de 3.

### Resultado #64 (8-nov-2026, Kaggle ie-tr4): **no juega**
| Camada (aprende ≤ s-4) | Universo a 4 años (desastres) | Tr 4 años sin temas | Tr 4 años con temas |
|---|---|---|---|
| 2017 | ×1,73 (20,1%) | ×1,756 (8,5%), lado 0,791 | ×1,756 (8,0%), lado **0,808** |
| 2018 | ×1,55 (21,5%) | ×1,583 (10,0%), lado 0,763 | ×1,596 (10,0%), lado **0,769** |
| 2019 | ×2,37 (18,5%) | ×2,120 (9,7%), lado 0,763 | ×2,088 (10,0%), lado 0,753 |
Criterio: temas suman 1 de 3, gana al universo 2 de 3, desastres 3 de 3 → no juega.
- Lo que sí hace Tr a 4 años: **corta los desastres a la mitad** (8-10% contra 18-21% del universo) rindiendo como el universo.
- Los temas vuelven a mejorar el lado en 2 de 3, pero en la cartera Kelly (repartida en miles de empresas) la diferencia de #62, que es entre el 10% de arriba y el 20% de abajo, se diluye.
Total probadas: 64.

## #65: el espacio latente de Gemma (Gemma Scope), escrita el 8-nov-2026 ANTES de correr
Pedido de Fabri: buscar la respuesta en el espacio latente de un modelo, no en palabras elegidas a mano.
- **Lectura:** Gemma 2 2B (pesos públicos, licencia Gemma aceptada por Fabri) lee los primeros 256 tokens de «el negocio» de cada 10-K (EDGAR-CORPUS, 2013-2020). En la capa 12, el autoencoder disperso de Gemma Scope (16.384 conceptos, JumpReLU) da cuánto se enciende cada concepto; por empresa, el promedio sobre los tokens (se guardan los 256 más fuertes). Corre en Colab T4.
- **Aprendizaje (sólo 2013-2016):** ridge sobre los conceptos presentes en ≥ 2% de las empresas, contra el exceso a 4 años dentro de su industria (SIC 3) y tercio de tamaño; el alfa se elige dejando un año afuera dentro de la exploración.
- **Confirmación 2017-2020, puntaje congelado, mismo criterio que #62:** decil de arriba menos quintil de abajo (dentro de SIC 3 y tamaño) > 0 en ≥ 3 de 4 años y promedio > 0, y menos desastres arriba en ≥ 3 de 4.
- Se informa: los conceptos con más peso a favor y en contra (con su descripción en Neuronpedia).

### Resultado #65 (8-nov-2026, Colab T4): **PASA, fuerte**
50.302 empresas-año leídas por Gemma (2013-2020). Con resultado a 4 años y grupo de ≥ 5 pares (SIC 3 × tamaño): 10.548 (unas 1.300 por año).
Exploración, correlación con el exceso a 4 años dejando un año afuera (alfa 1.000): 0,34 / 0,50 / 0,50 / 0,37.
| Confirmación (puntaje congelado) | 2017 | 2018 | 2019 | 2020 |
|---|---|---|---|---|
| decil de arriba menos quintil de abajo, a 4 años, dentro de SIC 3 y tamaño | **+91,0** | **+45,6** | **+32,1** | **+19,1** |
| desastres arriba - abajo | -16,9 | -11,9 | -11,5 | -5,3 |
Cautela: la muestra es más chica (sólo empresas con precio a 4 años y pares suficientes) y la correlación es alta para retornos: puede estar reconociendo «qué clase de empresa se hunde», algo que Tr ya sabe por los balances. Por eso la prueba que decide es #66.

## #66: Tr + Gemma, escrita el 8-nov-2026 ANTES de correr
- Puntaje de Gemma sin trampas: 2013-2016 con un modelo que no vio ese año; 2017-2020 con el modelo congelado (aprendido sólo con 2013-2016). datos: gemma_puntaje.csv.
- Se suma como un rasgo más (percentil por año) a Tr a 12 meses (#50, aprende ≤ s-2) y a Tr a 4 años (#64, aprende ≤ s-4). Camadas 2017, 2018, 2019.
- **Gemma entra a Tr si, en la versión a 4 años o en la de 12 meses:** con Gemma le gana a sin Gemma en ≥ 2 de 3, al universo en 3 de 3, y desastres ≤ sin Gemma + 1 punto en ≥ 2 de 3.

### Resultado #66 (8-nov-2026, Kaggle ie-tr4 v3): **no entra por el criterio, pero Gemma mejora a Tr en todo lo que mide el lado**
| Camada | Tr 4 años sin / con Gemma | lado sin / con | Tr 12 meses sin / con Gemma | lado sin / con | Universo 4 a / 12 m |
|---|---|---|---|---|---|
| 2017 | ×1,739 / **×1,823** (des 8,6 / 8,2%) | 0,795 / **0,800** | ×1,893 / ×1,890 (des 11,9 / 11,3%) | 0,711 / **0,728** | ×1,73 / ×1,10 |
| 2018 | ×1,586 / **×1,636** (9,8 / 9,8%) | 0,769 / **0,773** | ×1,872 / ×1,860 (21,0 / 20,6%) | 0,623 / **0,641** | ×1,55 / ×0,96 |
| 2019 | ×2,105 / **×2,205** (9,8 / 9,4%) | 0,759 / **0,766** | ×3,280 / ×3,276 (6,4 / 5,5%) | 0,809 / **0,822** | ×2,37 / ×2,13 |
- 4 años: con Gemma gana a sin Gemma 3 de 3 y baja desastres 3 de 3, pero en 2019 el universo (×2,37) le gana → no cumple «universo 3 de 3».
- 12 meses: misma plata (diferencias de 0,1-0,4%), menos desastres 3 de 3.
- **Lo que se repite en las 6 comparaciones:** con Gemma, el lado (×2 contra desastre) mejora siempre (+0,004 a +0,018 de AUC) y el peso en desastres baja o queda igual. Es la mejora de dirección más pareja del registro, chica en tamaño.
Total probadas: 66.

## #67: más Gemma, escrita el 8-nov-2026 ANTES de correr
Pedido de Fabri: más Gemma, y usar lo descubierto de un modo que sirva.
- Gemma 2 2B lee 512 tokens de «el negocio» (antes 256), capas 12 y 20 de Gemma Scope (16.384 conceptos cada una), 512 conceptos más fuertes por empresa y capa. Sólo las empresas con resultado a 4 años e industria (3.659 empresas, 18.403 empresa-años 2013-2020).
- Mismo método y criterio de confirmación que #65 (ridge aprendido en 2013-2016, alfa elegido dejando un año afuera; confirmación 2017-2020 con decil de arriba menos quintil de abajo dentro de SIC 3 y tamaño, > 0 en ≥ 3 de 4 y media > 0, desastres menos en ≥ 3 de 4).
- **Uso decidido antes (pedido de Fabri):** como Gemma en #66 bajó desastres y mejoró el lado en 6 de 6 sin cambiar la plata, Tr pasa a elegir con Gemma (la versión que mejor mida entre #65 y #67). La lista vieja de Tr queda en el registro con su sha256; la nueva se congela con la suya.

## #68: ¿Gemma predice o recuerda? Prueba a ciegas, escrita el 8-nov-2026 ANTES de correr
Pregunta de Fabri: ¿puede estar adivinando porque ya vio esto? Riesgo real: Gemma 2 se entrenó con internet hasta 2024 y puede «saber» qué les pasó a las empresas en 2017-2024 (look-ahead bias de los modelos de lenguaje, Glasserman y Lin 2023).
- **Prueba:** mismos informes, misma capa (12), mismos 256 tokens que #65, pero **anonimizados antes de que Gemma los lea**: se borran nombres propios (de dos o más palabras y sueltos en medio de oración), siglas y tickers, marcas, años y todos los números. Queda sólo la descripción del negocio.
- Mismo aprendizaje (2013-2016) y mismo criterio de confirmación (2017-2020) que #65.
- **Lectura:** si a ciegas pasa y conserva al menos la mitad del efecto de #65 (media de la confirmación ≥ +23 puntos), Gemma predice por el negocio y no por la identidad. Si se cae, #65 era memoria y Gemma no entra a Tr.
- Aparte, la prueba sin pasado posible queda congelada: informes de 2026, resultados 2027-2030.

### Resultado #68 (8-nov-2026, Kaggle ie-anon-a/b con GPU + análisis local): **PASA a ciegas**
23.185 empresas-año leídas sin nombres, marcas, lugares, años ni números; 11.229 con resultado y pares. Exploración (alfa 1.000): 0,30 / 0,44 / 0,46 / 0,28.
| Confirmación 2017-2020, a 4 años, dentro de SIC 3 y tamaño | 2017 | 2018 | 2019 | 2020 | media |
|---|---|---|---|---|---|
| con nombres (#65) | +91,0 | +45,6 | +32,1 | +19,1 | +47,0 |
| **a ciegas (#68)** | **+71,0** | **+28,1** | **+29,7** | **+25,4** | **+38,5** |
| desastres a ciegas, arriba - abajo | -10,3 | -3,3 | -8,3 | -5,8 | |
Conserva 82% del efecto (el umbral escrito era 50%). **Gemma predice por la descripción del negocio, no por reconocer a la empresa.** Queda un riesgo que no se puede borrar del todo (un negocio muy único se reconoce aunque no tenga nombre); la prueba limpia es la congelada 2026 → 2027-2030.
Decisión (escrita en #67): Tr pasa a elegir con Gemma, usando la versión a ciegas.
Total probadas: 68.

## Tr con Gemma, en el juego (8-nov-2026)
- Modelo: árboles de Tr (12 meses, Kelly, tope 5%) + puntaje de Gemma a ciegas (#68) como rasgo. Aprende con toda la historia; camada 2025 (balances presentados en 2026, 3.145 de 4.101 con texto leído por Gemma).
- Comparación previa con Gemma a ciegas (ie-tr4 v4): a 4 años, con Gemma gana a sin Gemma 3 de 3 (×1,797/1,610/2,170 contra ×1,756/1,583/2,120) y baja desastres 3 de 3; a 12 meses ×1,849/1,793/3,357 contra ×1,913/1,812/3,287, desastres 12,2/18,6/6,2% contra 12,6/20,8/6,0%.
- Lista congelada: datos/tr_gemma_congelada_2025.csv, 2.923 empresas con peso, sha256 **fa70b5e519c55662f159a6b120439a5b115c83b81561138596918821ab9a52ab**. En el juego: las 364 de más peso con ticker NYSE/Nasdaq (48% del peso), con sus pesos (simulador/lib/ia.json, api/ia.js). La lista anterior (216d486c…) queda en lib/ia.json → anterior.
- Lo que se vio antes de subir: del 1-oct al 7-nov-2026 la mediana de la lista nueva cayó 24% (SPY -4%, IWM -2%, lista vieja -1%). Es una cartera de empresas muy chicas y volátiles: mucho riesgo para los dos lados.

### Resultado #67 (8-nov-2026, Colab): más Gemma no mejora
Capas 12 y 20, 512 tokens, 512 conceptos (3 empresas descartadas por desborde de media precisión): confirmación a 4 años +94,6 / +54,0 / **-3,9** / +8,7 (media +38,3), desastres menos 4 de 4 → pasa el criterio, pero es menos pareja que la versión chica (#65: +91/+46/+32/+19) y que la ciega (#68: +71/+28/+30/+25). Se queda la versión ciega de la capa 12 para Tr. (La prueba ciega repetida en Colab dio casi igual: +71/+24/+25/+25.)
Total probadas: 68.

## #69: la cartera de Gemma contra el mercado, escrita el 8-nov-2026 ANTES de correr
- Puntaje: Gemma a ciegas (#68), 2017-2020 con el modelo congelado (aprendido sólo con 2013-2016).
- **Cartera:** cada año, el 10% de puntaje más alto dentro de su industria (SIC de 3 dígitos; si la industria tiene menos de 10 empresas con puntaje, SIC de 2), a partes iguales. **Mercado:** todas las empresas con puntaje y resultado ese año, a partes iguales.
- Retorno = promedio del múltiplo (quiebra = 0), a 12 meses (`_ret1`) y a 4 años (`_ret4`), desde el mes siguiente al 10-K.
- **Sirve para el juego (1 año) si:** a 12 meses le gana al mercado en ≥ 3 de 4 años (2017-2020) y no tiene más desastres (≤ ×0,5) en ≥ 3 de 4. **Sirve a largo plazo si:** lo mismo a 4 años.

### Resultado #69 (8-nov-2026, local): **SIRVE, a 1 año y a 4 años**
| | 2017 | 2018 | 2019 | 2020 |
|---|---|---|---|---|
| 12 meses: cartera Gemma / mercado | ×1,309 / ×1,238 | ×1,242 / ×1,144 | ×1,052 / ×0,953 | ×2,226 / ×2,156 |
| desastres | 2,3 / 4,6% | 3,7 / 6,3% | 15,8 / 18,5% | 1,6 / 2,2% |
| 4 años: cartera Gemma / mercado | ×2,657 / ×2,225 | ×1,906 / ×1,813 | ×1,661 / ×1,667 | ×2,547 / ×2,478 |
| desastres | 7,3 / 10,8% | 9,7 / 13,0% | 8,9 / 14,2% | 8,4 / 11,8% |
12 meses: gana 4 de 4, desastres 4 de 4. 4 años: gana 3 de 4 (2019 empate), desastres 4 de 4. Unas 300 empresas por año. «Mercado» = las empresas con texto y resultado ese año, a partes iguales.
**Uso:** Tr pasa a jugar esta cartera (el 10% de arriba de Gemma a ciegas dentro de cada industria, a partes iguales), con los 10-K de 2026.
Total probadas: 69.
- **En el juego desde el 8-nov-2026:** Tr = cartera de Gemma (#69) con los 10-K de 2026: 416 empresas, 347 con ticker NYSE/Nasdaq, a partes iguales. datos/tr_gemma_cartera_2026.csv, sha256 **ec841cab71a13934f9007d4f16ff0e729e8d666b8f2ce749fadbc2cc692a5f66**. Las versiones anteriores (fa70b5e5…, 216d486c…) quedan en simulador/lib/ia.json → anteriores.

## #70: la cartera de Gemma en 2021-2024 (años nunca usados con Gemma), escrita el 8-nov-2026 ANTES de correr
- 10-K presentados en 2021-2024, bajados de la SEC (Item 1), sólo empresas con resultado a 12 meses e industria; leídos a ciegas por Gemma con el modelo congelado de #68 (aprendido sólo con 2013-2016, sin tocar).
- Misma cartera y misma medida que #69 (10% de arriba por industria, a partes iguales, contra todas las empresas con puntaje).
- **Se confirma si:** a 12 meses le gana al mercado en ≥ 3 de 4 años (2021-2024) y no tiene más desastres en ≥ 3 de 4. A 4 años sólo se informa (2021-2022 tienen resultado).

### #61 completada (8-nov-2026): listas de Davos 2012, 2013, 2014, 2018 (y 2026)
Fuentes: 2012 Computing Community Consortium (cccblog.org, lista numerada; el n.º 1 confirmado por la nota del Foro); 2013 InCompliance y Krasnano (el 10.º, «Enhanced nutrition», sólo en la segunda); 2014 Pulse (8 de 10) + Business Insider (los dos que faltaban, por título); 2018 blog de Irving Wladawsky-Berger (10 de 10); 2026 PDF del Foro bajado por Fabri. 2022: no hubo edición (el Foro pasó de 2021 a 2023). Se vuelve a correr #61 con el mismo criterio, sin tocar nada.
Resultado con 13 años (2012-2021, 2023-2025): **no pasa**, y se debilita: 36 meses +2,1 puntos (IC95 -5,0 a +9,7), 7 de 11 años; 12 meses +1,3, 8 de 13. Las listas de Davos por sí solas no marcan dirección; lo que funcionó es Gemma leyendo a cada empresa (#65-#69).

## #71: la acción de las familias nobles y dinastías, por sus vehículos en el 13F, escrita el 8-nov-2026 ANTES de correr
Pedido de Fabri: las familias no figuran como dueñas; su acción se ve por los bancos y fondos propios que declaran carteras en EE.UU.
- **Lista cerrada de vehículos (por nombre del declarante en el 13F):** LGT (casa de Liechtenstein), Rothschild (Rothschild & Co, Edmond de Rothschild, Rothschild Investment), Safra / J. Safra Sarasin, Pictet, Lombard Odier, Mirabaud, Bessemer (Phipps), Rockefeller, Wallenberg / Investor AB, Exor (Agnelli), Pritzker, Mellon (familia, no el banco BNY), Cargill / Macmillan, Walton, Du Pont (familia).
- **Evento:** el vehículo abre una posición nueva o sube ≥ 50% sus acciones de una empresa en un trimestre. **Fecha:** cierre del trimestre + 45 días (cuando se hace público).
- **Medida:** retorno de la empresa a 12 meses desde el mes siguiente, menos el promedio de las empresas del mismo decil de tamaño en esos meses (log). 2013-2025.
- **Pasa si:** exceso medio > 0 con IC95 (remuestreo por evento) sin tocar el 0, y positivo en ≥ 70% de los años. Se informa por familia y los desastres.

## #72-#73: repensar Davos (Fabri: «por ahí hay algo que no entendés»), escritas el 8-nov-2026 ANTES de correr
Tres errores posibles en #60-#61: (a) unidad equivocada (fondos de sector, no las empresas que la tecnología mueve); (b) la lista llega tarde (elige lo que ya subió, como clima en 2021: señal al revés, «los dos lados del mostrador»); (c) los fondos temáticos nacen con la moda.
- **#72 ¿La lista llega después de la suba?** Para cada categoría y año: retorno del fondo contra SPY en los 12 meses ANTES de junio del año de la lista. Pasa (la lista sigue a la moda) si las categorías en la lista subieron antes más que las de afuera en ≥ 70% de los años con IC95 sin tocar el 0. Se informa además la interacción: categorías en la lista que NO habían subido antes contra las que sí, a 36 meses después.
- **#73 Davos empresa por empresa.** Con los 10-K 2013-2020 (sección 1, conteo de las 22 categorías de #61): puntaje = cuánto habla la empresa de las categorías que están en la lista de Davos de ese año (por mil palabras), percentil dentro de SIC 3 y tamaño. Exploración 2013-2016 sólo se mira; **confirma** 2017-2020 con el criterio de #62: decil de arriba menos quintil de abajo a 4 años > 0 en ≥ 3 de 4 y media > 0, desastres menos en ≥ 3 de 4.

### Resultado #72-#73 (8-nov-2026, local)
- **#72 no se confirma:** las categorías de la lista subieron apenas más en los 12 meses previos (+1,6 puntos, IC95 -2,2 a +4,9, 11 de 14). Las que ya venían subiendo rindieron mejor después que las que no (-5,7 contra -13,6 a 36 meses): impulso, no señal al revés. La lista no llega tarde.
- **#73 empresa por empresa:** hablar de las tecnologías de la lista DE ESE AÑO no pasa (confirmación +16,0/-4,8/-9,5/+11,7). Hablar de **todas las tecnologías que sigue Davos** (las 22 categorías, sin importar el año) **pasa**: +18,8/+17,8/+3,6/+3,2 (media +10,8), desastres menos en 3 de 4.
- **Lo que no se entendía:** la información de Davos no está en el calendario (qué entra cada año) sino en el contenido (el conjunto de lo que sigue), y se ve en las empresas, no en los fondos de sector. Coincide con #62 y con Gemma: el idioma de lo nuevo, leído en cada empresa, marca a las que les va mejor que a sus pares.
Total probadas: 73.

### Resultado #71 (8-nov-2026, Kaggle ie-fam13f-* + ie-familias): **no pasa, da al revés**
55 declarantes de 11 dinastías (Pictet, Lombard Odier, Rothschild/Edmond de Rothschild, Safra Sarasin, LGT, Bessemer, Rockefeller, Exor, Investor AB, Mirabaud, Cargill). 78.898 eventos (posición nueva o +50%), 52.533 con precio y control.
Exceso a 12 meses contra el mismo decil de tamaño: **-1,9 puntos (IC95 -2,3 a -1,5)**, positivo en 6 de 13 años; desastres 7,3% contra 7,2%. Por familia: todas entre -4,8 y -0,3, salvo Agnelli/Exor +3,9 (26 eventos) y Mirabaud +2,4 (77).
Lectura: lo que declaran los bancos privados de las familias es sobre todo plata de clientes, manejada casi como un índice; no es la apuesta propia de la familia. Las apuestas propias (Exor, Investor AB) son pocas para medir. Dudoso: «Rothschild Investment Corp /IL» (Chicago) puede no ser de la familia; no cambia el resultado (todas las familias dan parecido).
Total probadas: 73 (+#71).

### Resultado #70 (8-nov-2026): **no se confirma en 2021-2024**
Gemma a ciegas, modelo congelado de 2013-2016, 14.150 10-K de 2021-2024.
| 12 meses | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|
| cartera Gemma / mercado | ×1,008 / ×1,039 | **×1,090 / ×1,051** | ×1,235 / ×1,302 | ×1,173 / ×1,203 |
| desastres | **10,7 / 14,7%** | **11,9 / 16,4%** | **10,1 / 10,4%** | **11,6 / 11,8%** |
Gana al mercado 1 de 4 (sólo 2022, el año de la caída); **menos desastres 4 de 4**. A 4 años (sólo 2021-2022 tienen resultado): pierde 2021 (×1,21 contra ×1,39), gana 2022 (×2,09 contra ×1,80).
Lectura: en años recientes Gemma sigue protegiendo (menos empresas hundidas, mejor en la caída de 2022) pero no le gana al mercado en plata. El modelo se aprendió con 2013-2016 y se aplica 5 a 8 años después; lo que marca «lo nuevo» cambia con el tiempo. Siguiente: re-aprender con los años más recientes ya cerrados (sin mirar el futuro) y volver a medir.
Total probadas: 73.

## #74: Gemma re-aprendido con los años recientes, escrita el 8-nov-2026 ANTES de correr
Mismos conceptos de Gemma a ciegas (capa 12). Para elegir en el año a, la regresión (ridge, alfa 1.000 como antes) aprende sólo con informes cuyo resultado ya se conocía:
- **A: objetivo 12 meses**, aprende con informes presentados ≤ a-2.
- **B: objetivo 4 años**, aprende con informes presentados ≤ a-5.
Mismo exceso (dentro de SIC 3 y tamaño) y misma cartera y criterio que #70 en 2021-2024: le gana al mercado a 12 meses en ≥ 3 de 4 y desastres ≤ en ≥ 3 de 4. Si A o B pasa, Tr juega Gemma re-aprendido cada año.

### Resultado #74 (8-nov-2026, local): **no pasa**
- A (12 meses, aprende ≤ a-2): gana 1 de 4 (×1,038/1,015/1,259/1,215 contra ×1,039/1,051/1,302/1,203); desastres 2 de 4.
- B (4 años, aprende ≤ a-5): gana 1 de 4 (×1,020/1,072/1,208/1,195); **desastres menos 4 de 4** (10,3/13,2/9,7/11,3% contra 14,7/16,4/10,4/11,8%).
**Conclusión sobre Gemma:** protege siempre (menos empresas hundidas en los 8 años medidos) y ganó en plata en 2017-2020 y en la caída de 2022, pero desde 2021 no le gana al mercado a un año, ni re-aprendiendo. Sirve como freno de desastres, no como motor de ganancia.
Total probadas: 74.

## #76: los flujos de la élite hacia cada tema, fuera de las empresas, escrita el 8-nov-2026 ANTES de bajar datos
Fabri: «no busques tanto en las empresas»: la influencia se ve antes, en adónde va la plata y la atención.
- **Temas:** las 22 categorías de #61 con su fondo de sector, y estos términos de búsqueda fijados ahora: baterías «battery»; nuclear «nuclear reactor»; genómica «genomics»; fármacos «drug discovery»; diagnóstico «diagnostic device»; robótica «robotics»; IA «artificial intelligence»; cuántica «quantum computing»; chips «semiconductor»; espacio «satellite»; solar «solar cell»; hidrógeno «hydrogen fuel»; autos «electric vehicle»; blockchain «blockchain»; manufactura «additive manufacturing»; agro «crop yield»; agua «water purification»; construcción «building construction»; materiales «advanced materials»; comunicaciones «wireless communication»; realidad virtual «virtual reality»; carbono «carbon capture».
- **Flujos por tema y año:** proyectos financiados por NIH (RePORTER) y por NSF, documentos del Federal Register. Medida: crecimiento del log del conteo contra el año anterior, en percentil entre temas ese año, promedio de las tres fuentes.
- **Prueba:** cada año (2008-2023, según exista el fondo), los temas con flujo en el tercio de arriba contra el tercio de abajo, exceso del fondo contra SPY desde junio del año siguiente, a 36 meses (principal) y 12 meses.
- **Pasa si:** media de las diferencias > 0 con IC95 sin tocar el 0 y ≥ 70% de años positivos.

## #77: la plata de la Fundación Gates por tema, escrita el 8-nov-2026 ANTES de correr
- 41.847 donaciones comprometidas 1994-2026 (archivo público de la fundación), con propósito, división, tema y monto.
- Cada donación se asigna a las 22 categorías de #61 con los mismos patrones de #61 aplicados al texto de «propósito» + «tema».
- Flujo por categoría y año: crecimiento del log del monto comprometido contra el año anterior, percentil entre categorías ese año.
- Misma prueba y criterio que #76 (tercio de arriba contra tercio de abajo, fondo contra SPY desde junio del año siguiente, 36 meses principal; pasa con IC95 sin tocar el 0 y ≥ 70% de años positivos).

## #75: familias por PRESENCIA (no por propiedad), escrita el 8-nov-2026 ANTES de correr
Fabri: la influencia de las familias no está en la propiedad visible.
- Formularios 3/4/5 2006-2026: personas que reportan como director o directivo (rol D u O) con apellido de dinastía. **Sólo apellidos distintivos** (se excluyen comunes como Lee, Hunt, Bass, Cox, Koch, Mars, Orange, Busch, Coors, Jacobs, Weston, Schwarz, Walton, Persson, Meyers, Henkel, Tata, Albrecht): Rothschild, Wallenberg, Agnelli, Elkann, Rockefeller, Pritzker, du Pont, Mellon, Bronfman, Safra, Pictet, Peugeot, Arnault, Bettencourt, Quandt, Klatten, Porsche, Piëch, Oetker, Thyssen, Botín, Mulliez, Desmarais, Wertheimer, Lauder, Hearst, Newhouse, Ziff, Habsburg, Hohenzollern, Liechtenstein, Thurn, Grosvenor, Guinness, Cadbury, Sainsbury, Brenninkmeyer, Heineken, Bonnier, Kamprad, Ambani, Birla, Mahindra, Reimann.
- **Evento:** la persona aparece por primera vez como director o directivo de esa empresa (no estaba el año anterior). Compra: enero del año siguiente; retorno a 12 meses contra el mismo decil de tamaño.
- **Pasa si:** exceso medio > 0 con IC95 sin tocar el 0 y positivo en ≥ 70% de los años con eventos. Se informa por apellido y la cantidad de eventos (pueden ser pocos).

### Resultados #75-#77 (8-nov-2026)
- **#75 familias por presencia: no se puede afirmar.** 15.456 apariciones de apellidos de dinastía en formularios 3/4/5; con apellidos distintivos y rol de director o directivo, sólo 136 entradas nuevas en 20 años y 50 con precio. Exceso a 12 meses +0,0 (IC95 -9,2 a +8,7), 7 de 14 años. En las empresas que cotizan en EE.UU. casi no se las ve (lo que anticipó Fabri).
- **#76 financiamiento científico + regulación (NIH, NSF, Federal Register) por tema: no pasa.** Tercio de más aceleración contra tercio de menos: 12 meses -1,5 puntos (11 de 18 años), 36 meses +0,2 (9 de 16).
- **#77 plata de la Fundación Gates por tema: no pasa.** 12 meses -3,5 (8 de 18), 36 meses -2,7 (8 de 16).
Lectura: con 22 temas medidos por fondos de sector, ni la plata pública ni la filantrópica anticipan qué sector rinde. Queda la duda de la unidad (fondos de sector, pocos temas por año): la plata entra a ciencia que tarda más de 3 años en llegar a la bolsa, o llega a empresas que no están en esos fondos.
Total probadas: 77.
- **#76b/#77b (escrito antes de correr, 8-nov):** mismas pruebas a 60, 84 y 120 meses (la plata en ciencia puede tardar más en llegar a la bolsa). Mismo criterio (IC95 sin tocar el 0 y ≥ 70% de años positivos). Además, flujo acumulado de 3 años (promedio de los percentiles t-2..t) a 60 meses.
  Resultado #76b/#77b: **no pasa a ningún plazo.** Ciencia + reglas: 5 años +0,9 (9 de 15), 7 años -6,9 (5 de 13), 10 años -13,6 (5 de 10); acumulado 3 años a 5 años -2,6 (6 de 13). Gates: 5 años -5,6 (6 de 16), 7 años -3,9 (6 de 14), 10 años -12,5 (4 de 11). Si algo, a 10 años los temas que más plata recibieron rinden algo menos (sin fuerza estadística).

## #78-#79: llegar antes que la plata, y lo que arrastra cada tema (preguntas de Fabri), escritas el 8-nov-2026 ANTES de correr
- **#78a ¿El precio se mueve cuando llega la plata?** Por año: temas en el tercio de más aceleración de financiamiento (NIH+NSF+regulación, #76) contra el tercio de menos, exceso del fondo contra SPY **en ese mismo año calendario**. Si pasa (IC95 sin tocar el 0, ≥ 70% de años), anticipar la plata sirve.
- **#78b ¿Se puede anticipar la plata?** Correlación de rango, por año, entre lo que dijo la élite en t (consenso de #59/#61: menciones en Bilderberg y Davos en t-2..t, y estar en la lista de Davos en t) y la aceleración del financiamiento en t+1 y t+2. Pasa si es positiva en ≥ 70% de los años con IC95 sin tocar el 0.
- **#79 lo que arrastra cada tema:** insumos fijados ahora: baterías y autos → litio (LIT) y cobre (COPX); solar → plata (SLV) y cobre; IA, chips y comunicaciones → cobre, uranio (URA) y eléctricas (XLU); nuclear → uranio; hidrógeno → platino (PPLT) y paladio (PALL); agro → agrícolas (DBA); construcción → mineras (PICK). Señal de cada insumo = promedio del flujo de los temas que lo usan. Por año, insumos en la mitad de arriba contra la mitad de abajo, exceso contra SPY a 12 y 36 meses desde junio del año siguiente. Mismo criterio.

### Resultados #78-#79 (8-nov-2026, local)
- **#78a: el precio y la plata NO llegan juntos; van al revés.** El año en que más acelera el financiamiento de un tema, su fondo rinde **-4,8 puntos** contra los temas que menos aceleran (IC95 -8,9 a -0,7, no toca el 0), positivo sólo 9 de 19. La plata pública entra cuando el sector va mal en la bolsa (o el sector cae mientras entra la plata). No era la hipótesis escrita (que buscaba a favor); se anota como hallazgo a probar hacia adelante.
- **#78b: lo que dice la élite no anticipa adónde va la plata pública.** Correlación de rango de Davos (t-2..t) con la aceleración en t+1: -0,01 (4 de 13); en t+2: -0,07 (4 de 12).
- **#79: las materias primas que arrastra cada tema no se anticipan por el flujo.** 12 meses -2,1 (6 de 15); 36 meses +1,8 (5 de 13).
Total probadas: 79.

## #80: confirmar #78a con otra plata pública (contratos y subsidios federales), escrita el 8-nov-2026 ANTES de correr
Hipótesis ahora con dirección (la que apareció en #78a): el año en que más acelera la plata pública hacia un tema, su sector rinde PEOR.
- Fuente independiente: USAspending (contratos + subsidios federales), monto obligado por año fiscal para cada uno de los 22 términos de #76 (búsqueda por palabra clave), 2008-2025.
- Medida: crecimiento del log del monto contra el año anterior, percentil entre temas ese año. Tercio de más aceleración contra tercio de menos, exceso del fondo contra SPY en el mismo año calendario.
- **Se confirma si:** diferencia media < 0 con IC95 sin tocar el 0 y negativa en ≥ 60% de los años.

### Resultado #80 (8-nov-2026): **no se confirma**
Contratos y subsidios federales (USAspending) por tema, mismo año: +1,5 puntos (IC95 -2,8 a +6,8), negativo en 11 de 17. La pista de #78a (el sector rinde peor cuando llega la plata pública) no se sostiene con otra fuente: se descarta.

## #81: la plata PROPIA de las dinastías suecas (registro de operaciones de la Finansinspektionen), escrita el 8-nov-2026 ANTES de correr
Fabri: la acción de las familias no está en la propiedad visible de EE.UU.; está en sus vehículos propios, sobre todo en Europa.
- Registro sueco de operaciones de personas con cargo y sus vinculados (desde 2016): compras («Förvärv») hechas por vehículos o miembros de Wallenberg (Investor AB, FAM, fundaciones), Stenbeck (Kinnevik), Persson (Stefan y Karl-Johan Persson, Ramsbury), Lundberg (Fredrik Lundberg, L E Lundbergföretagen), Douglas (Latour, Bergsäker), Bonnier, Schörling (Melker Schörling AB). Se excluyen las de otras personas con esos apellidos.
- Evento: primera compra de ese vehículo en esa empresa en un mes. Retorno de la acción a 12 meses desde el mes siguiente, contra el índice amplio de Estocolmo (^OMXSPI).
- **Pasa si:** exceso medio > 0 con IC95 sin tocar el 0 y positivo en ≥ 70% de los años. Se informa por familia.

### Resultado #81 (8-nov-2026, local): **no pasa**
299 compras de vehículos propios de 7 dinastías suecas (2016-2025), 219 con cotización e índice. Exceso a 12 meses contra ^OMXSPI: **-0,05 puntos (IC95 -4,4 a +4,0)**, positivo en 5 de 10 años; desastres 2,3%. Por familia: Wallenberg +5,8 (26), Lundberg +4,9 (80), Bonnier +5,5 (24), Persson -3,3 (68, sobre todo H&M), Stenbeck -19,3 (7), Schörling -18,8 (5), Douglas -25,9 (9).
Lectura: cuando las dinastías compran con su plata en sus propias empresas, la acción rinde como el índice. Compran para sostener el control a décadas, no para acertar el año. Su peso en la economía es enorme (el grupo Wallenberg es una parte grande de la bolsa de Estocolmo), pero estar de su lado da el rendimiento del mercado, no más.
Total probadas: 81.

## #82: los bancos de familia como asesores (no como dueños), escrita el 8-nov-2026 ANTES de correr
Fabri: las familias influyen sin ser dueñas. Canal: sus bancos deciden por dónde va la plata de otros (fusiones, ventas, reestructuraciones).
- Buscador de texto completo de la SEC (2005-2025), documentos de fusiones y ofertas (DEFM14A, PREM14A, S-4, SC 14D9): empresas cuyos documentos nombran a **Rothschild** o **Lazard** (bancos de origen familiar), contra las que nombran sólo a Goldman Sachs, Morgan Stanley o J.P. Morgan (control).
- Evento: primera mención de la empresa en un año. Retorno a 12 meses desde el mes siguiente contra el mismo decil de tamaño (las que siguen cotizando).
- **Pasa si:** las de banco de familia superan a las de control en exceso medio con IC95 de la diferencia sin tocar el 0, y en ≥ 70% de los años.
- Cambio antes de ver resultados (8-nov): la bajada se cortó por un error del buscador; el control queda Goldman Sachs (2005-2025) + Morgan Stanley (2005-2017), sin J.P. Morgan. Familia: Rothschild 913 menciones, Lazard 2.087.

### Resultado #82 (8-nov-2026, Kaggle ie-asesores): **no pasa**
Empresas-año: asesoradas por Rothschild o Lazard 1.210 (202 con precio y control de tamaño); sólo por grandes bancos 5.662 (925). Exceso a 12 meses: familia -6,2 (desastres 13,9%), control -6,6 (11,8%); diferencia +0,5 puntos (IC95 -12,1 a +13,1), a favor en 7 de 16 años.
Lectura: que el asesor sea un banco de familia no cambia lo que le pasa a la empresa después. Pocos casos con precio (muchas son compradas y dejan de cotizar).
Total probadas: 82.

## #83: la élite entra antes que la multitud y le vende cuando llega (mecanismo propio), escrita el 8-nov-2026 ANTES de correr
Lo que se repite en #46-#82: lo que hacen los que saben marca magnitud, no lado. Mecanismo: la dirección depende de la etapa de la multitud. Élite sin multitud = la élite entrando (sube después); élite con multitud = la élite saliendo (baja después). Antecedente visto sin buscarlo: clima con todo el consenso en 2021, se desplomó.
- **Élite:** apariciones de la categoría en las listas de Davos en t-2..t (0 a 3).
- **Multitud:** crecimiento de las visitas anuales en Wikipedia (inglés, usuarios) al artículo del tema en t contra t-1 (artículos fijados ahora: Lithium-ion battery, Nuclear power, Genomics, Drug discovery, Medical diagnosis, Robotics, Artificial intelligence, Quantum computing, Semiconductor, Satellite, Solar cell, Hydrogen economy, Electric vehicle, Blockchain, 3D printing, Precision agriculture, Water purification, Construction, Graphene, 5G, Virtual reality, Carbon capture and storage). Datos desde 2015 → t = 2016-2025.
- **Grupos, por año:** «temprano» = élite ≥ 1 y multitud en la mitad de abajo; «tarde» = élite ≥ 1 y multitud en la mitad de arriba.
- **Pasa si:** temprano rinde más que tarde (fondo contra SPY desde junio del año siguiente) a 12 meses en ≥ 70% de los años con IC95 sin tocar el 0. Se informa 36 meses.

### Resultado #83 (8-nov-2026, local): **no pasa, y va al revés**
Temprano (élite sin multitud) menos tarde (élite con multitud): 12 meses -3,4 puntos (IC95 -8,4 a +1,3), positivo 2 de 8 años; 36 meses -2,8 (3 de 6). Lo que se ve es lo contrario del mecanismo: los temas a los que llega la multitud rinden algo más el año siguiente (impulso), sin fuerza estadística. Con 22 temas por año la prueba es chica.
Total probadas: 83.

## #84: el mecanismo de #83, empresa por empresa (directivos que venden cuando llega el público), escrita el 8-nov-2026 ANTES de correr
- **Llega el público:** mes en que las visitas al artículo de Wikipedia (inglés) de la empresa son ≥ 2 veces la mediana de sus 12 meses previos (artículo unido por el CIK de la SEC en Wikidata, P5531). 2016-2025.
- **La élite vende:** en ese mes o el siguiente, los directivos de la empresa venden en el mercado más de lo que compran (formularios 4, ventas «S» > compras «P»).
- **Comparación:** picos de público CON venta de directivos contra picos SIN venta. Retorno a 12 meses desde el mes +2 contra el mismo decil de tamaño.
- **Pasa (el mecanismo existe) si:** con venta rinde menos que sin venta, diferencia < 0 con IC95 sin tocar el 0 y negativa en ≥ 70% de los años.
- Datos (8-nov, antes de ver resultados): visitas de Wikipedia de 2.077 de 3.211 empresas (el resto no respondió o no existe el artículo).

### Resultado #84 (8-nov-2026, Kaggle ie-mecanismo): **el mecanismo aparece en conjunto, pero no alcanza el criterio de constancia**
2.595 picos de público en Wikipedia (2016-2025), 613 con venta neta de directivos; con precio y control de tamaño: 487 con venta y 528 sin.
- Con venta de directivos: **-4,6 puntos** a 12 meses contra su tamaño (desastres 10,1%). Sin venta: **+4,4** (8,7%).
- **Diferencia -9,0 puntos, IC95 -17,0 a -1,3: no toca el 0** (cumple la primera condición).
- Negativa en 6 de 10 años (el criterio pedía 7): no cumple la constancia. Por año: 2016 +15,9 / 2017 +2,4 / 2018 0,0 / 2019 -11,2 / 2020 -30,5 / 2021 -12,2 / 2022 +7,6 / 2023 -4,9 / 2024 -1,5 / 2025 -18,3.
- Todos los picos juntos: +0,1 contra su tamaño (el pico solo no dice nada; lo que separa es si los de adentro venden).
Lectura: es la primera señal del lado (dirección) que sale de cruzar a la élite con la multitud: cuando el público llega a una empresa y sus directivos venden, a la empresa le va 9 puntos peor que cuando el público llega y no venden. Por el criterio escrito, no se da por buena todavía; se congela hacia adelante.
Total probadas: 84.
- **Hacia adelante (8-nov-2026):** datos/congelada_84_2026.csv, sha256 **97e0304d1fa13bc9a980d923ede560e91ab6da10ab493a5b30a192247c6a0caa**: 279 picos de público (mayo-octubre 2026), 51 con venta de directivos. Se mide en noviembre de 2027: con venta contra sin venta, contra su tamaño.
- **En Tr:** se sacan de la cartera de Gemma las 5 marcadas (MRNA, AFRM, AON, SLB, OSCR): 342 empresas, datos/tr_gemma84_cartera_2026.csv, sha256 **3f31f1539cfbefe539c1ad306c5266592195387699e127c29767329cbcc381bb**.
- 8-nov-2026: repositorio público https://github.com/fabricionuove-alt/tr-inteligencia-economica (código, registro, pesos de Gemma, huellas; sin listas selladas ni claves). Enlazado en «Cómo piensa Tr». Carpeta local: inteligencia-economica/repo-tr.

## #85: profundizar #84, escrita el 8-nov-2026 ANTES de correr
Mismos picos de público (Wikipedia ≥ 2 veces su mediana de 12 meses, base ≥ 100), ahora con todas las empresas que respondan (antes 2.077).
- **Espejo:** picos con compra neta de directivos (P > S, P > 0) contra picos sin operaciones. Predicción: con compra rinde MÁS.
- **Dosis:** entre los picos con venta, tercio de ventas más grandes (en dólares, contra el tamaño de la empresa: ventas / activos) contra tercio más chico. Predicción: más venta → peor.
- **Repetición de #84** con la muestra completa.
- **Pasa (el mecanismo es real) si:** (1) se repite #84 con IC95 < 0; (2) el espejo da > 0 con IC95 sin tocar el 0 o al menos en ≥ 60% de los años; (3) la dosis va en la dirección predicha (tercio grande peor que tercio chico).

## #86: compras de directivos + Gemma, escrita el 8-nov-2026 ANTES de correr
De #42: donde los directivos compran hay más ×3 (6 de 6) pero también más desastres. Gemma (#68) baja los desastres. ¿Juntas?
- Filas 2017-2020 (10-K con puntaje de Gemma a ciegas sin trampas) donde los directivos compraron en el mercado en los 12 meses previos (formularios 4, compras > 0).
- Dentro de ellas: mitad de Gemma alta contra mitad baja (dentro del año). Resultados a 4 años (`_ret4`, quiebra = 0) y 12 meses.
- **Pasa si:** a 4 años, Gemma alta tiene menos desastres (≤ ×0,5) en ≥ 3 de 4 años Y múltiplo promedio mayor en ≥ 3 de 4. Se informa contra el universo y contra las compras sin Gemma.

### Resultado #86 (8-nov-2026)
11.389 filas con Gemma 2017-2020; 5.068 con compras de directivos.
- **4 años:** Gemma alta tiene menos desastres en 4 de 4 años (6,9/12,8/13,1/10,0% contra 16,7/17,4/18,7/15,7%), pero la reducción llega a ×0,5 sólo en 2017. El múltiplo promedio es mayor sólo en 2 de 4 años (2017 ×2,49 contra ×1,84; 2019 ×1,72 contra ×1,59; 2018 y 2020 empatan o pierde). **No pasa.**
- **12 meses (informado, no es el criterio):** Gemma alta gana en 4 de 4 años y tiene menos desastres en 4 de 4 (por ejemplo 2019: 16,2% contra 26,8%).
- **Lectura:** dentro de las compras de directivos, Gemma repite lo que hace en todo el universo: protege y no suma rendimiento a 4 años. Juntarlas no da algo nuevo. No entra en Tr.

## #87: Gemma lee los riesgos (sección 1A) y la explicación de la dirección (sección 7), escrita el 8-nov-2026 ANTES de correr
#68 leyó sólo «el negocio» (sección 1). Lo que la empresa teme y cómo la dirección explica sus números puede decir otra cosa.
- Mismo método que #68: a ciegas (mismo anonimizador), capa 12 de Gemma Scope, mismas empresas (quiero.txt), ridge aprendido sólo con 2013-2016 (alfa elegido en la exploración), confirmación 2017-2020, rendimiento a 4 años dentro de SIC 3 y tercio de tamaño.
- Cambios por la forma de estas secciones: se saltean los primeros 1.500 caracteres (fórmulas legales del comienzo: «invertir en nuestras acciones implica riesgos», «la siguiente discusión debe leerse junto con…») y se leen 512 tokens en vez de 256.
- **Pasa cada sección si:** la confirmación da media ≥ +20 puntos (diferencia de exceso entre el décimo de arriba y el de abajo, como #65/#68) con ≥ 3 de 4 años positivos.
- **Suma a Tr si:** juntando 1 + 1A + 7 en un solo ridge (aprendido igual, 2013-2016), la confirmación mejora la media de #68 (+38,5) en ≥ 5 puntos sin bajar en más de un año. Si no suma, la sección queda informada y Tr no cambia.

## #88: Gemma lee las conferencias de resultados (preguntas de analistas y respuestas sin guion), escrita el 8-nov-2026 ANTES de correr
El 10-K lo escriben abogados; en la conferencia la dirección contesta en vivo. Fuente: `kurry/sp500_earnings_transcripts` (Hugging Face, MIT, 2005-2025).
- **Sesgo de la fuente, dicho antes:** son las empresas del S&P 500 de 2025, o sea sobrevivientes. Casi no hay quiebras; la comparación es arriba contra abajo DENTRO de ellas, no contra el mercado. Por eso los desastres se informan pero no deciden.
- Para cada empresa y año A (2013-2020): la primera conferencia entre enero y junio de A (la del cierre del año, cerca del 10-K). Se lee desde el segundo turno del operador (donde empiezan las preguntas), a ciegas con el mismo anonimizador, capa 12, 512 tokens.
- Ticker → CIK con `company_tickers.json` de la SEC; resultados a 4 años de las mismas etiquetas que #68.
- Ridge aprendido sólo con 2013-2016, confirmación 2017-2020, pares dentro de SIC de 2 dígitos (la muestra es chica para SIC 3 × tamaño).
- **Pasa si:** la confirmación da media ≥ +20 puntos con ≥ 3 de 4 años positivos. Se informa la correlación con el puntaje de #68 en las mismas empresas (si es alta, la conferencia no agrega nada nuevo).

### Resultado #85 (8-nov-2026, Kaggle ie-mecanismo2, muestra completa: 3.964 picos, 915 con venta)
| Prueba | diferencia a 12 meses | IC95 | años en la dirección predicha | criterio |
|---|---|---|---|---|
| (1) #84 repetida: venta contra sin venta | -9,8 | [-15,9; -3,3] | 5 de 10 | IC < 0: **sí** |
| (2) espejo: compra contra sin operaciones (predicho +) | +0,8 | [-9,6; +11,0] | 4 de 10 | **no** |
| (3) dosis: venta grande contra chica (predicho -) | -10,2 | [-21,3; +0,5] | 6 de 10 | dirección: **sí** |
**No pasa** (pedía las tres). Con la muestra completa, vender durante un pico de público sigue yendo peor en promedio y más venta va peor, pero el efecto se concentra en pocos años (2019, 2020, 2025) y comprar no anticipa nada. Lectura: no es «los directivos saben y la multitud llega tarde»; es una señal de venta asimétrica y poco estable.
**Tr:** el filtro #84 queda como está en la lista sellada (ya jugada y con su sha), pero no se refuerza ni se extiende; la prueba que decide es la congelada 97e0304d… (nov-2027).

## #89: lo que los grupos de influencia ponen en agenda cada año, contra las empresas que se le parecen, escrita el 8-nov-2026 ANTES de correr
Fabri: la influencia no está en la propiedad; está en lo que estos grupos instalan. Cada texto tiene fecha: se compara lo que dijeron en el año Y con los 10-K presentados en Y+1 (después de que lo dijeron) y su rendimiento a 4 años.
- **Textos (públicos, fechados):** Informe de Riesgos Globales de Davos (2011-2020, enero), carta anual de la Fundación Gates (2010-2020), temas de Bilderberg (2013-2019, junio), 10 tecnologías emergentes de Davos (2012-2020). Hasta 60 pedazos de ~1.200 caracteres por documento, parejos a lo largo del texto.
- **Lectura:** Gemma 2 2B + Gemma Scope capa 12, a ciegas (mismo anonimizador que #68), 256 tokens por pedazo; el vector de cada fuente-año es el promedio de sus pedazos. Las empresas son los mismos vectores de #68 (10-K, sección 1). Los textos se leen en CPU (float32); las empresas se leyeron en placa (float16): diferencia numérica chica, dicha antes.
- **Lo nuevo del año:** agenda_Y = vector_Y − promedio de los dos años anteriores de la misma fuente (si falta uno, el que haya). Así no cuenta lo que dicen siempre, sólo lo que traen ese año.
- **Puntaje de cada empresa:** coseno entre su vector (log1p) y agenda_Y de cada fuente; se pasa a percentil dentro del año y se promedian las fuentes que haya ese año. **Sin nada aprendido:** cero parámetros ajustados a rendimientos.
- **Medida:** décimo de arriba contra el 20% de abajo dentro de SIC 3 × tercio de tamaño, exceso a 4 años (como #68). Exploración: agendas 2012-2015 → 10-K 2013-2016. Confirmación: agendas 2016-2019 → 10-K 2017-2020.
- **Placebo de tiempo:** lo mismo con la agenda de 4 años antes (Y−4 en vez de Y). Si da igual, lo que mide es el tema de siempre y no el momento.
- **Pasa si:** en la confirmación media ≥ +15 puntos con ≥ 3 de 4 años positivos, la exploración también da media > 0, y la confirmación supera al placebo de tiempo. Se informa cada fuente por separado y la correlación con el puntaje de #68.
- **Si pasa:** entra a Tr como segundo puntaje (promedio de percentiles con Gemma #68) solamente si esa suma mejora la confirmación de #68; si no, queda como señal propia informada.
- *(agregado antes de correr, 8-nov 20:00)*: los vectores de las empresas se centran restando el promedio de las empresas de ese año antes del coseno, para que no gane la que «se parece a todo».

## #90: lo nuevo que dicen los banqueros centrales cada mes, contra las empresas que se le parecen, escrita el 8-nov-2026 ANTES de correr
Lo aprendido: las pruebas de influencia anuales tienen 8 datos y casi nada se puede confirmar con 8. Los discursos de los banqueros centrales (lista del BIS, 1996-2026, con fecha exacta) permiten medir MES a MES: ~100 meses en vez de 8 años. Es la élite supranacional más concreta.
- **Lectura:** cada discurso de 2011-2020, un pedazo de ~1.200 caracteres saltando los primeros 300 (título y saludos), a ciegas, Gemma capa 12, 256 tokens (como #68 y #89). Vector del mes = promedio de sus discursos.
- **Lo nuevo del mes:** vector del mes − promedio de los 12 meses anteriores.
- **Empresas:** su último 10-K presentado antes de ese mes (vectores de #68, centrados por año). Puntaje = coseno con lo nuevo del mes. Nada aprendido de rendimientos.
- **Resultado:** precio de fin del mes siguiente a fin de 12 meses después (precios mensuales del proyecto). Se descartan las empresas-mes con un salto de precio de desdoblamiento (cociente mensual 1/2, 1/3, 1/4, 1/5, 1/10 o sus inversos, ±3%). Exceso = log del rendimiento menos la mediana de su grupo.
- **Medida principal:** décimo de arriba contra 20% de abajo dentro del tercio de tamaño del mes (SIN control de industria: la dirección que empujan los bancos centrales suele ser por sector, y eso es lo que se busca). Secundaria: dentro de SIC 3.
- **Exploración:** meses 2013-07 a 2016-12. **Confirmación:** 2017-01 a 2020-12. **Placebo de tiempo:** lo nuevo de 48 meses antes.
- **Pasa si:** en la confirmación la diferencia media es ≥ +3 puntos a 12 meses con t de Newey-West (12 rezagos, porque los meses se pisan) ≥ 2; la exploración da media > 0; y supera al placebo. Se informa la secundaria dentro de industria y la correlación con #89.

### Resultado #87, primera parte: sección 1A (riesgos), 8-nov-2026 (Kaggle ie-sec-1a + análisis local)
22.638 empresas-año leídas a ciegas; 11.190 con resultado. Exploración alfa 1.000: 0,24 / 0,39 / 0,34 / 0,28.
| Confirmación 2017-2020, a 4 años, dentro de SIC 3 y tamaño | 2017 | 2018 | 2019 | 2020 | media |
|---|---|---|---|---|---|
| negocio (#68) | +71,0 | +28,1 | +29,7 | +25,4 | +38,5 |
| **riesgos (1A) sola** | **+66,0** | **+46,1** | **+13,8** | **+5,0** | **+32,7** |
| desastres riesgos, arriba - abajo | -10,9 | -11,1 | -6,8 | -1,1 | |
| negocio + riesgos juntos (informado; la prueba escrita es 1 + 1A + 7) | +106,9 | +52,1 | +26,1 | +2,6 | +46,9 |
**La sección de riesgos PASA sola** (≥ +20 con 4 de 4 años positivos). Juntada con el negocio sube la media (+8,4) y la exploración (0,31 → 0,43), pero baja en 2019 y 2020: no cumpliría «sin bajar en más de un año». Lo que decide es la prueba escrita (1 + 1A + 7), cuando termine la sección 7.

### Resultado #87 completo: secciones 1A y 7, y las tres juntas (8-nov-2026)
| Confirmación 2017-2020, a 4 años | 2017 | 2018 | 2019 | 2020 | media | exploración (corr.) |
|---|---|---|---|---|---|---|
| negocio (#68) | +71,0 | +28,1 | +29,7 | +25,4 | +38,5 | 0,37 |
| riesgos (1A) | +66,0 | +46,1 | +13,8 | +5,0 | +32,7 | 0,31 |
| **dirección (7)** | **+64,6** | **+56,3** | **+35,6** | **+17,1** | **+43,4** | 0,29 |
| **las tres juntas (prueba escrita)** | **+112,9** | **+52,7** | **+31,4** | **-0,8** | **+49,1** | **0,45** |
Desastres, arriba - abajo: dirección -11,0/-14,5/-7,2/-6,3; las tres juntas -20,3/-12,4/-10,8/-2,8.
- Las dos secciones **pasan solas** (≥ +20, 4 de 4 años positivos).
- **Las tres juntas suman a Tr según el criterio escrito:** +49,1 contra +38,5 (≥ +5) y bajan contra #68 en un solo año (2020). Entran a Tr.
- Lo que no me gusta y queda dicho: el junto se apoya mucho en 2017 y en 2020 da cero; la sección 7 sola es la más pareja. Juntar tres veces más conceptos (49.152) con el mismo ridge puede ajustar de más. La prueba limpia es la congelada.

### Resultado #88: conferencias de resultados (8-nov-2026, Kaggle ie-llamadas)
387-513 empresas del S&P 500 por año; 2.436 con resultado. Exploración 0,06 / 0,32 / 0,13 / 0,07.
Confirmación (pares dentro de SIC 2): +14,4 / +10,4 / +8,5 / -17,0, media **+4,1**. **No pasa** (pedía ≥ +20). Las preguntas de los analistas, leídas a ciegas, dicen mucho menos que lo que la empresa escribe de sí misma. Muestra chica y sólo sobrevivientes, dicho antes.

### Resultado #90 (8-nov-2026, Kaggle ie-bis + ie-bis90): **no pasa, cero limpio**
9.217 discursos, 120 meses con vector, 20.811 empresas-año con vector y fecha.
| | exploración (42 meses) | confirmación (48 meses) | t Newey-West | por año 2017/18/19/20 |
|---|---|---|---|---|
| principal (dentro de tamaño) | -0,3 | -0,3 | -0,29 | +1,1 / +2,6 / -0,2 / -4,8 |
| placebo (48 meses antes) | +1,3 | +1,7 | +0,76 | |
| dentro de industria | -0,1 | -0,3 | -0,50 | |
Con 90 meses no hay excusa de muestra chica: parecerse a lo nuevo que dicen los banqueros centrales no anticipa nada a 12 meses, ni entre sectores ni dentro de ellos. Límite de la prueba, dicho: el parecido es entre la descripción del negocio y un discurso macro; puede que el canal de los bancos centrales sea la tasa y el crédito (macro), no el tipo de empresa.

### Resultado #89 (8-nov-2026, Kaggle ie-agenda89g v2, a ciegas): **no pasa; da al revés**
(La v1 se corrió sin anonimizar por un error mío en el comando: no se midió.)
| Diferencia a 4 años, décimo más parecido a lo nuevo de la agenda contra el 20% menos parecido | exploración | confirmación | años + |
|---|---|---|---|
| **todas las fuentes juntas** | -3,9 | **-11,6** | 1 de 4 |
| placebo (agenda de 4 años antes) | +5,8 | -4,4 | 1 de 4 |
| Riesgos Globales de Davos | +0,9 | -12,2 | 1 de 4 |
| 10 tecnologías de Davos | -12,4 | -6,1 | 1 de 4 |
| Bilderberg | -9,0 | +4,8 | 3 de 4 |
| carta de Gates | -0,6 | +0,6 | 2 de 4 |
Correlación con Gemma #68: -0,01 (mide otra cosa). Lectura: las empresas que más se parecen a lo que Davos instala como nuevo rinden PEOR después, no mejor. Encaja con #61 y #83 (cuando la élite pone un tema, el precio ya lo tiene). **Es una hipótesis, no un resultado:** el criterio buscaba lo contrario. Si se prueba, va con criterio nuevo escrito antes y sobre años no usados (2021-2024 con resultado a 12 meses, o la congelada).

## #91: ¿parecerse a lo nuevo de la agenda de la élite anticipa rendir MENOS? Escrita el 8-nov-2026 ANTES de correr, después de ver #89
Hipótesis salida de #89 (no estaba en su criterio). Se prueba sólo sobre años NO usados en #89.
- Mismo método exacto que #89 (a ciegas, capa 12, 256 tokens, lo nuevo = año − promedio de los dos anteriores, coseno con empresas centradas, percentil por fuente y promedio de fuentes). Mismos textos y fuentes, sumando los años 2021-2023 que falten (Riesgos Globales 2021-2023, carta de Gates 2021-2023, Bilderberg 2022-2023, tecnologías 2021 y 2023).
- Empresas: 10-K de 2021-2024 leídos a ciegas (vectores de #70). Agenda del año anterior al 10-K.
- Resultado a **12 meses** (`_ret1`, el único cerrado para los cuatro años); a 4 años sólo se informa 2021-2022.
- **Pasa (la agenda anticipa rendir menos) si:** décimo de arriba menos 20% de abajo, dentro de SIC 3 × tamaño, a 12 meses, ≤ -5 puntos de media con ≥ 3 de 4 años negativos, y más negativo que el placebo (agenda de 4 años antes).
- Si pasa: entra a Tr como filtro (sacar de la cartera el décimo más parecido a la agenda del año) y se congela hacia adelante con los 10-K de 2026 y la agenda de 2025.

### Resultado #91 (8-nov-2026, ie-agenda89g v3): **no pasa; la dirección se mantiene pero chica**
10-K 2021-2024, 12 meses: +4,3 / -3,4 / -4,7 / -5,2, media **-2,2** (3 de 4 negativos; pedía ≤ -5). Placebo +1,8. Lo de #89 no era casualidad del todo (la dirección «parecerse a la agenda va peor» se repite 3 de 4 años y le gana al placebo), pero es demasiado chico para usarlo. Tr no cambia.

Lo de #91 se informa a 4 años en 2021-2022 (9-nov-2026, local, agenda91r4_eval.py; ya estaba anunciado en #91, no es prueba nueva)
10-K 2021: **+11,3**; 10-K 2022: **-11,8**; media **-0,2**. Placebo (agenda de 4 años antes): +10,0 / -28,2. La señal de #89 dada vuelta (que parecerse a la agenda de la élite rinda menos a 4 años) no se repite en los años nuevos: un año da a favor, otro en contra, y el placebo se mueve igual. Tr no cambia.

### #87 como cartera (8-nov-2026, local, misma medida que #69) — decisión: Tr NO cambia la lista en juego
| | 2017 | 2018 | 2019 | 2020 |
|---|---|---|---|---|
| 12 meses: tres secciones / mercado | ×1,352 / ×1,244 | ×1,244 / ×1,133 | ×0,969 / ×0,939 | ×2,106 / ×2,167 |
| 12 meses: lista en juego (#69) / mercado | ×1,309 / ×1,238 | ×1,242 / ×1,144 | ×1,052 / ×0,953 | ×2,226 / ×2,156 |
| hundidas a 12 meses: tres secciones / mercado | 2,5 / 4,7% | 3,5 / 6,2% | 15,0 / 18,7% | 1,7 / 2,0% |
| 4 años: tres secciones / mercado | ×2,763 / ×2,209 | ×1,793 / ×1,806 | ×1,561 / ×1,677 | ×2,466 / ×2,487 |
| hundidas a 4 años: tres secciones / mercado | 6,0 / 10,5% | 7,5 / 13,0% | 8,0 / 14,1% | 7,6 / 11,4% |
El criterio de #87 medía la separación entre el décimo de arriba y el 20% de abajo, y ahí mejora (+49 contra +38,5). Pero el juego compra el décimo de arriba contra el mercado, y ahí la de tres secciones es **peor** que la lista en juego: a 12 meses gana 3 de 4 (la actual 4 de 4) con promedio ×1,418 contra ×1,457; a 4 años gana 1 de 4 (la actual 3 de 4). Protege más (menos hundidas 4 de 4 en los dos plazos), rinde menos. La mejora de la separación vino de identificar mejor a las peores, no a las mejores.
**Decisión:** la lista en juego sigue siendo 3f31f153…. La de tres secciones queda sellada como lista paralela para comparar al cumplirse el año: datos/tr87_cartera_2026.csv (365 empresas), sha256 **597fe03a5a63ea49121ed18835d9cc40ce2646692caf21ef1f3912ea0ecb3b44**. Uso que sí tiene: las de abajo de las tres secciones son las que conviene evitar (filtro de desastres), a probar con criterio propio.

## #92: la lista en juego, sin las que las tres secciones marcan como peores, escrita el 8-nov-2026 ANTES de correr
- Cartera #69 (10% de arriba de Gemma #68 por industria), sacando las que en el puntaje de tres secciones (#87) quedan en el 20% de abajo de su industria. Misma medida que #69, 2017-2020.
- **Entra a Tr si:** contra la cartera #69 sin filtro, rinde igual o más a 12 meses en ≥ 3 de 4 años y tiene menos hundidas en ≥ 3 de 4.

### Resultado #92: **no pasa, no cambia nada**
El filtro saca sólo 4 a 7 empresas por año de la cartera (las dos lecturas casi coinciden arriba): a 12 meses igual o más 2 de 4, menos hundidas 2 de 4. Diferencias de ×0,001-0,007. Tr sigue igual.
Total probadas: 92.

## #93: Gemma aprendida para el plazo del juego (12 meses), escrita el 8-nov-2026 ANTES de correr
Hasta ahora el ridge de Gemma aprendió el rendimiento a 4 años; el juego dura 1.
- Mismo método que #68 y #87 (a ciegas, 2013-2016 para aprender, alfa por exploración), pero el objetivo es `_ret1` (12 meses) contra SIC 3 × tamaño. Tres variantes: negocio (1), dirección (7), y las tres secciones.
- Medida de juego: la cartera #69 (10% de arriba por industria, a partes iguales) contra el mercado y contra la lista en juego, 2017-2020, a 12 meses.
- **Reemplaza a la lista en juego si:** a 12 meses le gana a la cartera #69 actual en ≥ 3 de 4 años con promedio mayor, y no tiene más hundidas en ≥ 3 de 4. Si más de una variante pasa, se elige la de mayor promedio.

### Resultado #93 (8-nov-2026, local): **no pasa ninguna; la lista en juego sigue siendo la mejor**
Separación a 12 meses (aprendida para 12 meses), 2017-2020: negocio +0,2/+17,3/-1,4/+5,1; dirección +5,2/+17,6/+14,6/+8,6; tres secciones +15,0/+17,6/+13,8/+3,5.
| Cartera a 12 meses | 2017 | 2018 | 2019 | 2020 | promedio |
|---|---|---|---|---|---|
| lista en juego (#69, aprendida a 4 años) | ×1,296 | ×1,230 | ×1,048 | ×2,202 | ×1,444 |
| negocio aprendida a 12 meses | ×1,207 | ×1,192 | ×0,894 | ×2,204 | ×1,374 |
| dirección aprendida a 12 meses | ×1,251 | ×1,150 | ×0,952 | ×2,236 | ×1,397 |
| tres secciones aprendidas a 12 meses | ×1,322 | ×1,237 | ×0,954 | ×2,228 | ×1,435 |
Aprender a 12 meses es aprender ruido: el precio de un año mezcla demasiado. Lo que Gemma aprendió mirando 4 años elige mejor también para 1 año. Tr no cambia.
Total probadas: 93.

## #94: usar el puntaje de tres secciones por donde predice mejor (las de abajo), escrita el 8-nov-2026 ANTES de correr
Fabri: «¿cómo algo que pronostica mejor no va a sumar?». La mejora de #87 está en reconocer a las peores; la cartera #69 sólo compra el 10% de arriba y nunca la usa. Variantes de cartera (a partes iguales, mismas reglas de industria que #69), 2017-2020:
- (a) 20% de arriba de tres secciones; (b) 30% de arriba; (c) todo menos el 20% de abajo de tres secciones; (d) todo menos el 40% de abajo; (e) 10% de arriba del promedio de percentiles de #68 y tres secciones; (f) 20% de arriba de ese promedio.
- **Reemplaza a la lista en juego si:** a 12 meses le gana a la cartera #69 en ≥ 3 de 4 años con promedio mayor, no tiene más hundidas en ≥ 3 de 4, y a 4 años no es peor que #69 en más de 2 de 4. Son 6 variantes: se dice, y la elegida queda además congelada.

### #87 corregido (8-nov-2026): **entra a Tr**, como decía su criterio
Error mío: después de que #87 pasó su criterio escrito, agregué una medida (promedio de la cartera) que no estaba escrita y la frené. Mirando por qué: el promedio lo mueven unas 5 empresas que se disparan.
| 12 meses, 2017-2020 | mediana | sin las 5 mejores de cada año | hundidas |
|---|---|---|---|
| lista anterior (#69) | ×1,177 / 1,062 / 0,842 / 1,604 | ×1,198 / 1,083 / 0,849 / 2,022 | 2,4 / 4,3 / 15,7 / 1,3% |
| **tres secciones** | **×1,186 / 1,094 / 0,852 / 1,605** | **×1,247 / 1,122 / 0,872** / 1,971 | **2,2 / 3,5 / 15,0** / 1,7% |
La de tres secciones es mejor para la empresa típica los 4 años, y sin las 5 de suerte gana 3 de 4. Juega desde el 8-nov-2026: datos/tr87_cartera_2026.csv, 365 empresas, sha256 **597fe03a5a63ea49121ed18835d9cc40ce2646692caf21ef1f3912ea0ecb3b44**. La anterior (3f31f153…) queda en anteriores. #94: ninguna variante más amplia le gana.

### Plazo del juego: 4 años (8-nov-2026, pedido de Fabri)
El año era un estimado. Tr juega a 4 años, que es el plazo con el que aprendió Gemma: las listas de Tr se revelan en noviembre de 2030. A 4 años, 2017-2020, la lista de tres secciones: mediana ×1,774 / 1,411 / 1,334 / 1,628 contra mercado ×1,465 / 1,335 / 1,244 / 1,663 (3 de 4), hundidas 6,0 / 7,5 / 8,0 / 7,6% contra 10,5 / 13,0 / 14,1 / 11,4% (4 de 4); promedio ×2,76 / 1,79 / 1,56 / 2,47 contra ×2,21 / 1,81 / 1,68 / 2,49 (1 de 4: el promedio lo mueven las pocas que se multiplican).

## #95: Gemma aprende a reconocer a las que se multiplican (×3 o más a 4 años), escrita el 8-nov-2026 ANTES de correr
Lo que vimos en #87/#94: Tr esquiva a las que se hunden pero no agarra más «cohetes» que el mercado (x3 o más: 19,7/13,3/7,2/21,7% contra 15,6/10,5/9,0/21,4%), y el promedio lo mueven ellos.
- Mismos vectores de tres secciones (#87), a ciegas. Objetivo: 1 si `_ret4` ≥ 3, si no 0. Regresión logística con penalización L2 (C elegido en la exploración 2013-2016 dejando un año afuera, por AUC), aprendida sólo con 2013-2016.
- Cartera A: 10% de arriba por industria del puntaje de cohete. Cartera B: 10% de arriba del promedio de percentiles (cohete + tres secciones). Reglas de industria como #69.
- **Reemplaza a la lista en juego si:** a 4 años, 2017-2020, contra la lista en juego (tres secciones): promedio del múltiplo mayor en ≥ 3 de 4 años, hundidas no más en ≥ 3 de 4, y mediana no menor en ≥ 3 de 4. Dos variantes: se dice.

### Resultado #95 (8-nov-2026, local): **no pasa**, pero el detector de cohetes funciona
AUC (×3 o más a 4 años): exploración 0,76; confirmación 0,71 / 0,63 / 0,57 / 0,45.
| A 4 años, 2017-2020 | promedio | hundidas | mediana | ×3 o más |
|---|---|---|---|---|
| lista en juego (tres secciones) | ×2,81 / 1,78 / 1,59 / 2,54 | 5,1 / 8,6 / 7,2 / 8,2% | ×1,71 / 1,42 / 1,36 / 1,67 | 19,8 / 12,1 / 6,8 / 22,6% |
| mercado | ×2,21 / 1,81 / 1,68 / 2,49 | 10,5 / 13,0 / 14,1 / 11,4% | ×1,47 / 1,34 / 1,24 / 1,66 | 15,6 / 10,5 / 9,0 / 21,4% |
| A: 10% de arriba en cohete | **×3,31 / 1,93 / 1,77 / 2,79** | 12,6 / 15,6 / 15,5 / 16,7% | ×1,88 / 1,38 / 1,27 / 1,57 | 30,8 / 14,8 / 10,4 / 21,4% |
| B: cohete + tres secciones | ×2,93 / 1,95 / 1,65 / 2,74 | 6,0 / 9,2 / 9,7 / 12,7% | ×1,85 / 1,49 / 1,31 / 1,64 | 21,8 / 15,2 / 8,4 / 22,0% |
A le gana en promedio a la lista en juego y al mercado los 4 años, pero se hunde más que el mercado. B gana en promedio 4 de 4 pero se hunde más que la lista en juego 4 de 4. Ninguna cumple las tres condiciones.

## #96: mitad lista en juego, mitad cohetes (A), escrita el 8-nov-2026 ANTES de correr, después de ver #95
- Cartera: 50% de la plata en la lista de tres secciones (a partes iguales dentro) y 50% en la A de cohetes; si una empresa está en las dos, recibe las dos mitades.
- **Entra a Tr si:** a 4 años, 2017-2020: promedio mayor que la lista en juego en ≥ 3 de 4, promedio mayor que el mercado en ≥ 3 de 4, y hundidas (peso en empresas que terminan ≤ ×0,5) menores que el mercado en ≥ 3 de 4. Se informa también en 2021-2022 (10-K con resultado a 4 años, nunca usados).

### Resultado #96 (8-nov-2026, local): **PASA, entra a Tr**
| A 4 años | 2017 | 2018 | 2019 | 2020 |
|---|---|---|---|---|
| mezcla mitad y mitad | **×3,061** | **×1,857** | **×1,680** | **×2,665** |
| lista de tres secciones | ×2,809 | ×1,781 | ×1,586 | ×2,544 |
| mercado | ×2,209 | ×1,806 | ×1,677 | ×2,487 |
| hundidas: mezcla / mercado | 8,9 / 10,5% | 12,1 / 13,0% | 11,4 / 14,1% | 12,5 / 11,4% |
Le gana a la lista en juego 4 de 4 y al mercado 4 de 4, con menos hundidas que el mercado 3 de 4. 2021-2022 no se pudo informar (faltan las secciones 1A y 7 de esos años leídas por Gemma).
**Juega desde el 8-nov-2026:** datos/tr96_cartera_2026.csv, 639 empresas (365 de tres secciones + 347 cohetes, 73 en las dos), con pesos. sha256 **8cbffce0c594f309e564a74c04a9c575f5fa92661413ae1a123dabc5546dc29c**, se revela en noviembre de 2030. La anterior (597fe03a…) queda en anteriores.
Total probadas: 96.

## #97: la mezcla #96 en años nunca usados (10-K 2021 y 2022, resultado a 4 años), escrita el 8-nov-2026 ANTES de correr
- Modelos congelados tal cual (tres secciones #87 y cohetes #95, aprendidos sólo con 2013-2016). Gemma lee a ciegas las secciones 1A y 7 de los 10-K de 2021 y 2022 bajados de la SEC (igual que 2026); la sección 1 ya está leída (#70).
- Misma cartera que #96 (mitad tres secciones, mitad cohetes, 10% de arriba por industria), contra el mercado (todas las empresas con las tres secciones y resultado).
- **Se confirma si:** en 2021 y en 2022 el promedio a 4 años de la mezcla supera al del mercado, y en al menos uno de los dos tiene menos hundidas que el mercado. Si falla, Tr vuelve a la lista de tres secciones sola (597fe03a…) y se dice.

## #98: cuando el fondo soberano de Noruega excluye a una empresa, ¿después rinde menos? Escrita el 8-nov-2026 ANTES de correr
El fondo más grande del mundo (NBIM, ~1,5% de las acciones del planeta) publica a quién excluye y cuándo; otros fondos lo siguen. Es plata de largo plazo con decisión fechada: influencia que no está en la propiedad de una familia sino en una lista.
- **Datos:** lista vigente de exclusiones y observaciones de nbim.no (201 decisiones 2006-2026); se cruzan con la SEC por nombre exacto (52 empresas). Sesgo dicho antes: es la lista VIGENTE, faltan las exclusiones revocadas.
- **Evento:** el mes de la decisión. Rendimiento desde fin del mes siguiente a 48 meses (principal, el plazo de Tr) y a 12 meses (informado), contra la mediana de las empresas de su misma industria (SIC 3; SIC 2 si hay menos de 10) en la misma ventana. Saltos de desdoblamiento descartados como en #90.
- **Pasa (la exclusión anticipa rendir menos) si:** a 48 meses el exceso medio (log) es ≤ -10 puntos, con IC95 por remuestreo que no toca el 0, y ≥ 60% de los eventos negativos.
- Si pasa: Tr saca de su lista a las empresas excluidas u observadas por el fondo (hoy).

### Resultado #98 (8-nov-2026, Kaggle ie-nbim): **no pasa; da al revés**
52 empresas cruzadas, 40 con precios, 28 con ventana de 48 meses. Exceso contra su industria a 48 meses: **+6,5 puntos** (IC95 -14,9 a +25,7), negativos sólo 29%, mediana +7,9. A 12 meses +8,3 (n 34). Las excluidas por el fondo de Noruega (carbón, armas, tabaco) rinden IGUAL O MÁS que su industria después, no menos: es la «prima de las acciones del pecado» que documentaron Hong y Kacperczyk (2009). Las únicas caídas grandes son Fluor (2018) y el cannabis (2022). Muestra chica y sólo con la lista vigente. Tr no cambia.
Total probadas: 98.

## #99: llegar antes que el precio — ¿lo que dice la élite en privado anticipa lo que Davos instala después? Escrita el 8-nov-2026 ANTES de correr
Lo aprendido (#89, #91, #98): la élite mueve el precio cuando habla en público; después ya no se gana. Para aprovecharlo hay que llegar ANTES. Bilderberg se reúne en junio y es cerrada; los banqueros centrales hablan todos los meses; Davos publica en enero.
- **(a) ¿Se anticipa?** Coseno entre lo nuevo de Bilderberg (junio del año Y-1) y lo nuevo de los Riesgos Globales de Davos (enero del año Y), contra el mismo coseno con años cambiados (placebo: todas las otras parejas de años). Igual con lo nuevo de los discursos del BIS de julio a diciembre de Y-1 contra Davos Y.
- **(b) ¿Se gana?** Empresas más parecidas a lo nuevo de Bilderberg Y-1 (vectores de su último 10-K, como #89): rendimiento de fin de junio de Y-1 a fin de junio de Y+3 (4 años, el plazo de Tr), décimo de arriba contra 20% de abajo dentro de industria y tamaño. Años 2013-2019 y 2022.
- **Pasa (a) si** el coseno de los años correctos supera al 90% de los placebos para Bilderberg o para el BIS. **Pasa (b) si** la diferencia media es ≥ +10 puntos con ≥ 5 de 8 años positivos. Sólo si pasan las dos entra a Tr.

### Resultado #99 (a) (8-nov-2026, local): **no pasa**; (b) no se corre (pedía las dos)
Bilderberg (junio Y-1) → Davos (enero Y), 8 parejas: coseno medio +0,022 contra placebo -0,001; el correcto supera sólo al 55% de los placebos (pedía 90%). BIS (julio-diciembre Y-1) → Davos Y, 9 parejas: +0,054 contra +0,009, supera al 68%. Hay un poco de anticipo (los dos van en la dirección esperada), pero no alcanza: lo nuevo que dice Davos en enero no se lee claro en lo que dijeron Bilderberg o los bancos centrales seis meses antes.
Total probadas: 99.

### Resultado #97 (8-nov-2026, Kaggle ie-lee2021/2022 + local): **no se confirma; Tr vuelve a la lista de tres secciones**
| 10-K | A 4 años | mezcla #96 | tres secciones | cohetes | mercado |
|---|---|---|---|---|---|
| 2021 | promedio | ×1,295 | ×1,280 | ×1,309 | ×1,415 |
| 2021 | hundidas | 31,4% | **22,9%** | 39,9% | 26,4% |
| 2022 | promedio | ×1,652 | ×1,707 | ×1,597 | ×1,724 |
| 2022 | hundidas | 26,8% | **22,1%** | 31,6% | 24,3% |
La mezcla no le gana al mercado en ninguno de los dos años y se hunde más (0 de 2 y 0 de 2). La mitad «cohetes» es la que falla: en 2021-2022 lo que se parecía a los que se multiplicaron en 2013-2020 terminó hundido el 32-40% de las veces (los años de las SPAC y del dinero barato que se cortó). La de tres secciones sola tampoco le gana al mercado, pero se hunde menos los dos años: repite lo de #70 (protege, no gana).
Como estaba escrito: Tr vuelve a la lista de tres secciones (597fe03a…), y la #96 (8cbffce0…) pasa a anteriores.
Total probadas: 99.

## #100: lo nuevo que entra al Congreso de EE.UU. cada mes (la idea antes de la ley), contra las empresas que se le parecen, a 4 años. Escrita el 8-nov-2026 ANTES de correr
Camino de la influencia: la idea pasa de fundaciones y grupos a un proyecto de ley mucho antes de que llegue la plata pública. Los proyectos son públicos, fechados y miles (no 8 por año).
- **Textos:** GovInfo BILLSTATUS, Congresos 112-117 (2011-2022): título + resumen oficial del CRS. Proyectos presentados: hasta 150 por mes al azar (semilla 0). Leyes: todas (1.387), por el mes en que se firmaron.
- **Lectura:** igual que #90 (a ciegas, capa 12, 256 tokens). Lo nuevo del mes = vector del mes − promedio de los 12 anteriores (proyectos); para leyes, trimestre contra los 4 trimestres anteriores.
- **Empresas y medida:** como #90 (último 10-K antes del mes, centrado, coseno), pero a **48 meses** (el plazo de Tr) desde fin del mes siguiente; décimo de arriba contra 20% de abajo dentro del tercio de tamaño (principal) y dentro de industria (informada). Exploración: meses 2013-07 a 2016-12; confirmación: 2017-01 a 2021-12 (incluye años nunca usados). t de Newey-West con 48 rezagos. Placebo: lo nuevo de 48 meses antes.
- **Pasa si:** en la confirmación la diferencia media es ≥ +10 puntos a 4 años con t ≥ 2, la exploración da > 0 y supera al placebo; para proyectos o para leyes. Si pasa, entra a Tr como segundo puntaje y se prueba antes en 2021-2022 (regla nueva: nada entra al juego sin pasar años nunca usados).

### Resultado #100 (8-nov-2026, Kaggle ie-leyes + ie-leyes100): **no pasa**
21.844 textos (141 meses de proyectos, 116 trimestres móviles de leyes), 20.811 empresas-año. A 48 meses:
| | exploración | confirmación (2017-2021) | t NW | placebo |
|---|---|---|---|---|
| proyectos, dentro de tamaño (principal) | +7,2 | +1,9 | 0,51 | -1,9 |
| **proyectos, dentro de industria** | +4,1 | **+3,0** | **2,14** | -3,5 |
| leyes, dentro de tamaño (principal) | +5,0 | +0,2 | 0,25 | +5,0 |
| leyes, dentro de industria | -0,8 | +4,3 | 2,11 | -0,2 |
Lo principal no pasa (pedía +10 con t ≥ 2). Queda una señal chica y consistente dentro de industria con los proyectos (+3 puntos a 4 años, t 2,1, exploración y placebo del lado correcto): de dos empresas del mismo rubro, la que se parece más a lo nuevo que entra al Congreso rinde un poco más. Es demasiado chica para mover a Tr; queda anotada.
Total probadas: 100.


## #101: las empresas que las embajadas de EE.UU. empujaban en secreto (cables de WikiLeaks), a 4 años. Escrita el 9-nov-2026 ANTES de correr
Lo que la élite dice en público (#89-#100) no sirvió con mi método. Esto mira lo que hacía en privado: los cables diplomáticos filtrados (Cablegate, 251.287 cables, copia pública fn5/wikileaks-cables en Hugging Face). Eran secretos hasta nov-2010/sep-2011: nadie podía comprar sabiéndolos.
- **Cables:** fechados 2005-01 a 2010-02. Empuje = cable con la etiqueta **BEXP** (promoción de negocios y exportaciones) en su línea TAGS.
- **Empresas:** nombres de las que presentaron 10-K en EDGAR 2005-2010 (full-index), sin sufijos (INC, CORP, CO…). Se busca el nombre como palabra entera. Afuera: nombres de menos de 5 letras, nombres de una palabra común en inglés (wordfreq ≥ 4,0) y nombres que corresponden a más de una empresa. Rubro: SIC de etiquetas.csv (cualquier año; se pierde la que murió antes de 2010).
- **Grupos, por año Y (2005-2009):** empujadas = nombradas en ≥ 1 cable BEXP de Y. Control = nombradas en cables de Y pero en ninguno BEXP (igual de conocidas para los diplomáticos).
- **Resultado:** rendimiento de fin de enero de Y+1 a fin de enero de Y+5 (48 meses, el plazo de Tr), con precios mensuales de la SEC (desde 2006), sin saltos por split. Exceso = log rendimiento − mediana del control del mismo SIC 2 y año.
- **Pasa si:** el exceso medio de las empujadas es ≥ +10 puntos, positivo en ≥ 4 de 5 años, y la permutación (mezclar quién es empujada dentro de año × SIC 2, 2.000 veces) da p < 0,05.
- Informado aparte: contra todas las empresas del SIC 2 (no sólo las nombradas), y la parte de empujadas que se hunde (≤ ×0,5).
- **Uso en Tr:** los cables terminan en 2010, así que no entran directo. Si pasa, la siguiente prueba busca lo mismo en una fuente actual y pública del empuje del gobierno (créditos del EXIM Bank, casos del Advocacy Center de Comercio) y tiene que pasar 2021-2022 antes de entrar.
- **Cambio del filtro de nombres (9-nov, ANTES de mirar ningún rendimiento):** el filtro por frecuencia dejaba pasar frases comunes (NATIONAL SECURITY, EDUCATE, AMBASSADORS, que son nombres de empresas). Regla nueva: el nombre tiene que tener al menos una palabra de ≥ 4 letras que no esté en el diccionario inglés (web2 + gcide, también en singular). De 1.797 empresas nombradas quedan 707, y 145 con algún cable BEXP. Se pierden empresas reales de nombre común (General Electric, Chevron, Caterpillar) y quedan algunos lugares (HAGUE, NEWARK): ese ruido cae en los dos grupos y achica la diferencia, no la inventa.

### Resultado #101 (9-nov-2026, Kaggle ie-cables101 + local cab101_eval.py): **no pasa con esta medida; muestra muy chica**
112.446 cables de 2005-2010, 1.227 con BEXP. Con precio, rubro y control en el mismo SIC 2 quedan **60 empresas-año empujadas** contra 168 nombradas sin empuje (2009 tiene la mitad).
| | 2005 | 2006 | 2007 | 2008 | 2009 | total |
|---|---|---|---|---|---|---|
| exceso de las empujadas sobre el control, a 4 años | -23,8 | +12,3 | -14,6 | -14,1 | -5,3 | **-6,5** |
Permutación p 0,71. Contra todo su rubro: empujadas +4,0, nombradas sin empuje +8,0. Mediana ×1,34 contra ×1,47; hundidas 6,7% contra 5,4%.
Lo que se puede decir: entre las empresas que nombran los cables, a las que la embajada empujaba no les fue mejor en los 4 años siguientes, **medido así**. Límites de la medida: muy pocas empresas (60, porque los cables de 2005-2008 son pocos y los precios salen de los fails-to-deliver de la SEC); el filtro de nombres pierde empresas grandes de nombre común (General Electric, Chevron, Caterpillar); sólo mira la etiqueta BEXP y no lo que dice el cable; compara contra empresas que los diplomáticos también nombran, que pueden haber recibido otro tipo de ayuda. Tr no cambia.
Total probadas: 101.

## #103: las empresas que el gobierno de EE.UU. financia para exportar (créditos del EXIM Bank), a 4 años. Escrita el 9-nov-2026 ANTES de cruzar ningún rendimiento
Disparada por los cables (#101/#102): el empuje del gobierno a empresas concretas aparece en los cables junto al EXIM («EXIM and EB/CBA advocate for Boeing»). El EXIM publica cada crédito aprobado (data.gov, FY2007-FY2026: exportador, monto, fecha), así que es la versión pública y actual del mismo empuje, y sirve para Tr.
- **Empresa:** el exportador (o filial) se lleva a la empresa madre por nombre: núcleo del nombre (sin INC, CORP, LLC…) igual al de una empresa del dataset (nombres de cik-lookup-data de la SEC), o que empiece con ese núcleo seguido de palabras (filiales: «GENERAL ELECTRIC ENERGY PARTS» → GENERAL ELECTRIC); gana el núcleo más largo. Núcleo de una sola palabra sólo si no está en el diccionario inglés (regla de #101).
- **Señal del año fiscal F:** monto aprobado total del EXIM para esa empresa en F. Se cruza con el 10-K presentado en el año calendario F+1 (el año fiscal del EXIM termina en septiembre) y su rendimiento a 4 años (`_ret4`).
- **Medida:** exceso de log rendimiento contra la mediana de su SIC 3 × tercio de tamaño (como #69). Empresas con crédito contra las del mismo grupo sin crédito.
- **Años:** exploración 10-K 2012-2016, confirmación 2017-2020, años nunca usados 2021-2022.
- **Pasa si:** el exceso medio de las financiadas es ≥ +10 puntos en la confirmación y positivo en la exploración, y en 2021-2022 es > 0. Recién ahí entra a Tr (como suma al puntaje o como filtro), y se congela con el EXIM FY2025-2026.
- Informado: por tamaño del crédito (más de 100 millones de dólares contra menos), y la parte que se hunde (≤ ×0,5).

### Resultado #103 (9-nov-2026, local exim103.py): **no pasa**
52.203 créditos aprobados (FY2007-2026); 2.842 de 325 empresas del dataset (Boeing se lleva 84.000 millones de dólares, después GE, Anadarko, Exxon). Con rendimiento a 4 años y grupo: 204 empresas-año.
| | exploración 2012-2016 | confirmación 2017-2020 | nunca usados 2021-2022 |
|---|---|---|---|
| exceso contra las sin crédito del mismo SIC 3 × tamaño | -6,9 | **+18,1** | **-43,9** |
Por año: 2012 +23, 2013 -17, 2014 -26, 2016 -36, 2017 +13, 2018 +42, 2020 +32, 2021 +8, 2022 -101 (en 2022 son 10 empresas chicas con créditos de capital de trabajo de 0,1 a 9 millones; 4 se hundieron, una a cero).
Informado: créditos de más de 100 millones (los grandes, el empuje tipo Boeing): 17 casos, +21,9. Hundidas: 9,8% de las financiadas contra 17,3% de todas (no es contra el mismo grupo: las financiadas son más grandes).
Lo que se puede decir, medido así: tener un crédito del EXIM no marca a las empresas que rinden más; cambia mucho de año en año y en los años nuevos va en contra. Queda anotado, sin probar, que los créditos grandes (17 casos) dan a favor.
Total probadas: 103.

## #102: lo que dicen los cables de cada empresa (leídos por un modelo), a 4 años. Exploración en los cables BEXP; confirmación escrita el 9-nov-2026 ANTES de leer los cables económicos
**Cómo se leyó:** Qwen2.5-3B (Kaggle, T4) leyó cada cable y devolvió en JSON el tipo de cable (pedido de compra del país, noticia de negocio, control de exportaciones, boletín, problema de empresa, gestión/advocacy, disputa) y cada empresa nombrada con su papel (ayudada, ganó, perdió, en disputa, con problemas, competidora, sólo mencionada). Las empresas se llevan a la madre por nombre (regla de #103, con alias: GE, IBM, HP, ExxonMobil…). Rendimiento: fin de enero Y+1 a fin de enero Y+5, exceso de log contra la mediana del SIC 2 (como #101).

### Exploración (cables BEXP, 1.350 de 1.387 leídos; 373 menciones de 129 empresas del dataset; 133 empresas-año con precio). Ya mirada: NO es prueba
| grupo | n | exceso a 4 años |
|---|---|---|
| todas las nombradas | 133 | +11,8 (hundidas 4,5% contra 17,1% del mercado) |
| ganó (contrato, venta) | 66 | **+13,3** |
| ayudada | 63 | +4,8 |
| con problemas | 16 | +21,9 |
| sólo mencionada | 34 | **-12,8** |
| base: nombradas en cualquier cable / en ≥ 20 cables | 738 / 87 | +4,2 / +7,4 |
Ganó − sólo mencionada: **+26 puntos**, y no es fama: las sólo mencionadas salen en más cables (29 por año contra 15). La pista: lo que el cable cuenta (que la empresa ganó algo) separa, la mera mención no.

### Confirmación (escrita antes de leerlos): los 9.095 cables económicos 2004-2010 que nombran empresas, sin los cables BEXP ya leídos
- **Empresas-año:** sólo las que NO aparecieron en la exploración (para que sea independiente). Años de cable 2005-2009.
- **Pasa si:** ganó − sólo mencionada ≥ +10 puntos, y el exceso de las que ganaron es > 0.
- Informado: con problemas, en disputa, ayudada, por tipo de cable; y con todas las empresas-año (aunque estén en la exploración).
- **Uso en Tr:** los cables terminan en 2010; si pasa, la siguiente prueba busca la misma señal («ganó un contrato afuera», contada por un tercero) en una fuente pública actual y tiene que pasar 2021-2022.

## #104: los planes de compra de los países que cuentan los cables, por sector, a 4 años. Exploración en los BEXP; confirmación escrita el 9-nov-2026 ANTES de leer los cables económicos
Disparada por la lectura de #102: el tipo de cable más común entre los BEXP es «el país X planea comprar» (359 de 1.350: defensa, aviones, petróleo, telecom, trenes, nuclear). Pregunta: cuando un sector aparece más que lo normal en esos planes, ¿al sector le va mejor después?
- **Medida:** por sector (10, con sus SIC) y año de cable 2005-2009: parte de los cables de ese año que son plan de compra del sector, dividida por el promedio del mismo sector (así no gana el sector que siempre sale). Rendimiento del sector: mediana del log de sus empresas (fin de enero Y+1 a Y+5) menos la mediana del mercado.
- **Exploración (BEXP, ya mirada):** correlación de rangos **−0,33**; años en que el sector sale más que lo normal **−5,6** contra +8,3 los otros (**−13,8**). Va en la misma dirección que #89 (donde la élite se mete, el sector después rinde menos). Ej.: nuclear sube de 5 cables en 2007 a 17 en 2008 y rinde −15.
- **Confirmación:** los cables económicos (sin los BEXP). Pasa si la correlación es ≤ −0,20 y la diferencia altos − bajos ≤ −10 puntos.
- **Límite que ya se sabe:** los rendimientos son los mismos 50 sector-año; la confirmación sólo prueba que otros cables cuentan lo mismo, no es independiente en los precios. Para Tr hace falta una fuente actual de planes de compra públicos (licitaciones) y pasar 2021-2022.

## #105: ventas de armas al exterior aprobadas por el gobierno de EE.UU., por contratista, a 4 años. Escrita el 9-nov-2026 ANTES de bajar los avisos
Disparada por #102/#104: en los cables el empuje más común es «el país X planea comprar» y el sector que más sale es defensa; y lo que separaba era que la empresa *ganara* algo. La versión pública y actual: cada venta de armas a otro gobierno (Foreign Military Sales) se avisa al Congreso y se publica en el Federal Register («36(b) Notification», 2.037 avisos desde 1996), con el monto estimado y el «principal contractor».
- **Empresa:** cada contratista principal nombrado se lleva a la empresa madre con la regla de #103 (núcleo del nombre, filiales por el comienzo del nombre, alias como #102: Lockheed, Raytheon, Boeing…).
- **Señal del año Y:** monto estimado total de los avisos publicados en Y que la nombran (si nombra varias, el monto se reparte por igual). Se cruza con el 10-K presentado en Y+1 y su `_ret4`.
- **Medida:** exceso de log rendimiento contra la mediana de las empresas del mismo SIC 3 × tercio de tamaño sin avisos (como #103).
- **Años:** exploración 10-K 2012-2016, confirmación 2017-2020, nunca usados 2021-2022.
- **Pasa si:** exceso medio ≥ +10 puntos en la confirmación, positivo en la exploración, y > 0 en 2021-2022. Si pasa entra a Tr y se congela con los avisos de 2025-2026.
- Informado: avisos de más de 1.000 millones de dólares; y a qué parte de las empresas de defensa del dataset alcanza.

## #106: empresas nombradas en cables económicos secretos o confidenciales (lo que se habla en privado) contra las nombradas sólo en cables abiertos, a 4 años. Escrita el 9-nov-2026 ANTES de medir
Disparada por la pregunta de Fabri (qué hace la élite en privado, no lo que dice): los 39.674 cables económicos 2004-2010 traen su clasificación (13.065 confidenciales o secretos, 26.141 abiertos o de uso oficial).
- **Empresas:** nombres de las empresas del dataset (cik-lookup de la SEC, regla de nombres de #103 + alias de #102) buscados en el texto guardado de cada cable (asunto + primeros 4.000 caracteres).
- **Grupos por empresa-año (cable 2005-2009):** «en privado» = nombrada en al menos un cable CONFIDENTIAL o SECRET ese año; «sólo abierta» = nombrada ese año sólo en cables UNCLASSIFIED.
- **Medida:** exceso de log rendimiento contra la mediana del SIC 2 (fin de enero Y+1 a Y+5, como #101). Diferencia privado − abierto, y permutación dentro de año × SIC 2 (2.000).
- **Dirección:** no sé cuál esperar (en #102 las «con problemas», casi siempre confidenciales, dieron +22 con 16 casos), así que se escribe para los dos lados.
- **Pasa si:** |diferencia| ≥ 10 puntos, permutación de dos colas p < 0,05, y el mismo signo en 2005-2007 y en 2008-2009.
- Informado: secret contra confidential; la cantidad de cables (fama) en cada grupo.

### Resultado #106 (9-nov-2026, local priv106.py): **no pasa con esta medida**
339 empresas-año con precio (196 nombradas en privado, 143 sólo en abierto).
| | exceso a 4 años | hundidas | cables por año |
|---|---|---|---|
| nombradas en cables confidenciales o secretos | +3,5 | 10,7% | 12,7 |
| sólo en cables abiertos | +10,4 | 7,7% | 2,2 |
Diferencia **−6,9**, permutación p 0,46; 2005-07 −4,5, 2008-09 −8,2. Secret +3,9 (46), sólo confidential +3,4.
Lo que se puede decir, medido así: que a una empresa la nombren en privado no separa su rendimiento a 4 años. Límites: pocas empresas con precio; la búsqueda de nombres trae también lugares y palabras (IRELAND, STAFFING, EVOLVING, GEORGETOWN, que son empresas del dataset con nombre de cosa) y ese ruido cae en los dos grupos; sólo mira el texto guardado (primeros 4.000 caracteres); y la mención no dice qué se dijo — eso lo mide #102 con la lectura.
Total probadas: 106.

### Resultado #105 (9-nov-2026, local fms105_bajar.py + fms105_eval.py): **no pasa; muestra muy chica**
1.508 avisos 2008-2026 (federalregister.gov pide humano para el texto; se bajó de govinfo.gov). Hasta 2010 los avisos son imágenes sin texto; desde 2011 traen el contratista. 656 avisos nombran a 34 empresas del dataset; con rendimiento y grupo de comparación quedan **41 empresas-año** (los grandes de defensa casi no tienen 5 pares en su SIC 3 × tamaño).
| | exploración 2012-2016 | confirmación 2017-2020 | nunca usados 2021-2022 |
|---|---|---|---|
| exceso contra las sin aviso del mismo grupo | +18,1 | **−11,0** | −57,2 (2 casos) |
Avisos de más de 1.000 millones: −1,1 (20); menos: +12,6 (21). Hundidas: 0 de 41.
Lo que se puede decir, medido así: con tan pocos casos no se ve que el aviso de una venta de armas marque a la empresa. Límites: 41 casos; la regla de nombres no reconoce «RTX Corporation» (73 avisos) ni «BAE Systems»; el Federal Register publica con meses de atraso (2021: 12 avisos, 2022: 4).
### Resultado #102 confirmación (9-nov-2026, cab102_conf.py con los 9.095 cables económicos leídos por Qwen en Kaggle): **PASA**
Sin ningún cable ni empresa-año de la exploración: 642 menciones, 278 empresas-año con precio.
| papel en el cable | n | exceso a 4 años contra su SIC2 | hundidas |
|---|---|---|---|
| **ganó** (contrato, licitación) | 134 | **+7,1** | 9,0% |
| ayudada por la embajada | 123 | +1,3 | 10,6% |
| con problemas | 72 | −13,1 | 6,9% |
| en disputa | 27 | +15,8 | 3,7% |
| competidora | 21 | +23,1 | 4,8% |
| **sólo mencionada** | 94 | **−13,5** | 18,1% |
**Ganó − sólo mencionada = +20,7** (criterio ≥ +10 y ganó > 0: pasa). Exploración BEXP: +26. Con todas las empresas-año: +5,6 contra −9,4 (+15,0).
La fama no lo explica: las sólo mencionadas salen en más cables (15,8 por año) que las que ganaron (13,5). Base de todas las nombradas: +4,2.
Por año ganó: 2005 +35,9, 2006 +2,0, 2007 +9,0, 2008 −0,6, 2009 +12,4 (2004 un solo caso). Sólo mencionada: −29,2, −29,3, +0,5, −0,6, −15,7. La diferencia sale casi toda de 2005, 2006 y 2009; en 2007-2008 no separa.
Cambio contra la exploración: «con problemas» dio +21,9 en los BEXP (16 casos) y −13,1 acá (72): ese lado no se sostiene.
Lo que se puede decir: dos lecturas separadas de cables distintos dan que las empresas que la embajada cuenta como ganadoras rinden después más que las que sólo aparecen nombradas. **No entra a Tr todavía**: los cables terminan en 2010; falta la misma señal en una fuente pública actual y pasar 2021-2022.

### Resultado #104 confirmación (9-nov-2026, SIN_BEXP=1 sector104.py con los cables económicos): **no pasa**
Correlación de rangos **−0,125** (criterio ≤ −0,20); sector-años que salen más que lo normal +0,4 contra +5,3 los otros, **−4,9** (criterio ≤ −10). Misma dirección que la exploración, la mitad de fuerte.
Lo que se puede decir, medido así: con los cables económicos la relación entre planes de compra de un sector y su rendimiento es más floja que en los BEXP y no alcanza el umbral. Límite: son los mismos 50 sector-año de precios.


## #107: problemas que la empresa le cuenta a la embajada y calla en su 10-K, a 4 años. Escrita el 9-nov-2026 ANTES de cruzar los 10-K y los rendimientos
Disparada por la lectura de los cables: ExxonMobil le dice a la embajada en Túnez (2006) que no gana plata y piensa irse, y ningún 10-K de Exxon nombra Túnez; Chevron se va de Ruanda (2008) y su 10-K nunca nombra Ruanda. En cambio Halliburton (Nigeria) y Motorola (Telsim, Turquía) sí lo cuentan.
- **Casos:** todas las lecturas (cables BEXP y económicos 2004-2009) donde una empresa del dataset tiene papel «con problemas» o «en disputa». País = el del origen del cable (embajada; consulados por su país).
- **¿Lo cuenta?:** búsqueda de texto completo de EDGAR (efts.sec.gov): algún 10-K de esa empresa presentado en el año del cable o el siguiente nombra el país.
- **Medida:** exceso de log rendimiento contra la mediana del SIC 2 a 48 meses (como #101), por empresa-año (si tiene varios casos, «callado» si calla al menos uno).
- **Hipótesis (escrita antes):** a las que callan les va peor que a las que cuentan.
- **Pasa si:** callado − contado ≤ −10 puntos y permutación (una cola) p < 0,05. Con tan pocos casos esperables, si no pasa se dice «con esta medida no apareció».

### Resultado #107 (9-nov-2026, callado107.py con BEXP + cables económicos y la búsqueda de texto de EDGAR): **no pasa con esta medida**
343 casos empresa-año-país «con problemas» o «en disputa» (132 empresas); en 132 el 10-K de ese año o el siguiente no nombra el país, en 211 sí. Con precio: 140 empresas-año.
| | n | exceso a 4 años contra su SIC2 | hundidas |
|---|---|---|---|
| calló el país en el 10-K | 51 | −2,6 | 2,0% |
| lo contó | 89 | +3,7 | 6,7% |
Diferencia **−6,3**, p 0,29 (criterio ≤ −10 y p < 0,05). Dirección la esperada, chica y sin fuerza.
Los que más callan: Microsoft (8 casos), ExxonMobil (6), Boeing (5), General Motors (4+2), ConocoPhillips, Chrysler, GE.
Lo que se puede decir, medido así: callar en el 10-K un problema que se le contó a la embajada no separa el rendimiento a 4 años. Límites: la regla de nombres casa también bancos centrales y países con empresas del dataset («China», «National Bank of Ukraine», «Bank of Jamaica»: ruido en los dos grupos); una empresa grande puede no nombrar un país chico por materialidad, no por esconder; la búsqueda de EDGAR sólo cubre 10-K desde 2001 con texto completo.

## #108: empresas que ganan contratos públicos en Europa (TED), a 4 años. Escrita el 9-nov-2026 ANTES de cruzar ganadores con rendimientos
Disparada por #102, que pasó: en los cables, las empresas que la embajada cuenta como «ganó» rinden después +20,7 más que las sólo mencionadas. Los cables terminan en 2010; hace falta la misma señal («ganó un contrato afuera, lo cuenta un tercero») en una fuente pública que siga hoy. El Banco Mundial no sirve (casi no hay empresas cotizadas de EE.UU. entre sus adjudicatarios). TED publica cada adjudicación de contrato público de la UE con el nombre del ganador (data.europa.eu, 2006-2023).
- **Empresa:** el nombre del ganador (WIN_NAME) se lleva a la empresa madre con la misma regla de #102 (`madre()` de cab102_eval.py, sin cambios): núcleo más largo que encabeza el nombre, filiales locales incluidas («Hewlett-Packard Italiana» → HP).
- **Señal del año Y:** la empresa tiene al menos una adjudicación con año de aviso Y. Se cruza con el 10-K presentado en Y+1 y su `_ret4`.
- **Medida:** exceso de log rendimiento contra la mediana de las empresas del mismo SIC 3 × tercio de tamaño sin adjudicación ese año (como #103). Permutación de la etiqueta dentro de año × SIC 3 × tercio (2.000), una cola.
- **Años (10-K):** exploración 2010-2016, confirmación 2017-2020, nunca usados 2021-2022.
- **Pasa si:** exceso medio ≥ +5 puntos en la confirmación con p < 0,05, positivo en la exploración y > 0 en 2021-2022. Si pasa entra a Tr como señal congelada con las adjudicaciones de 2024-2026 (TED sigue publicando).
- Informado: empresas que ganan por primera vez (sin adjudicación en los 3 años anteriores) contra las que ganan siempre; monto adjudicado ≥ 10 millones de euros; a qué parte del dataset alcanza; y los nombres que más casan, para ver errores de la regla.
- **Límite que ya se sabe:** las grandes (IBM, HP, Microsoft) ganan algo todos los años; ahí la señal casi no cambia. Por eso se informa «primera vez» aparte, pero el criterio es el de arriba.

### Resultado #108 (9-nov-2026, ted108_bajar.py + ted108_eval.py): **no pasa como estaba escrita; aparece otra cosa, la registro como pista**
9,6 millones de adjudicaciones 2006-2023; 274.573 casan con 1.600 empresas del dataset (casi todo filiales europeas de salud: Johnson & Johnson, Stryker, Covidien, Boston Scientific, Pfizer, Abbott; también ruido de la regla: «Alliance Healthcare», «Bionovo Aneta Ludwig»). Alcanza al 11,9% de las empresas-año.
| | exploración 2010-2016 | confirmación 2017-2020 | nunca usados 2021-2022 |
|---|---|---|---|
| n | 988 | 724 | 394 |
| exceso medio (criterio) | +0,6 | **−4,3** | −2,3 |
| exceso mediano | +5,2 | +5,1 | +11,5 |
| permutación una cola (contra sus pares, mismas reglas) | p 0,001 | p 0,03 | p 0,01 |
| hundidas (≤ la mitad) ganadoras / todas | **5,9% / 15,5%** | **7,5% / 12,6%** | **22,6% / 28,8%** |
Criterio (media ≥ +5 en confirmación): **no pasa**. Primera vez que ganan: −24,6 (304); ganan seguido: +2,3.
**Lo que apareció de costado, en los tres tramos:** las que ganan contratos públicos en Europa se hunden mucho menos que sus pares del mismo rubro y tamaño, y su mediana va por arriba; la media no sube porque les faltan también los saltos grandes para arriba. La permutación (que compara contra la media de los pares, que también es negativa) da que les va mejor en los tres tramos. Es la misma forma que en #102 (las que «ganaron» en los cables se hundían 9,0% contra 17,1% del mercado).
Lo que se puede decir: con la media como estaba escrita, ganar contratos en la UE no da más rendimiento a 4 años; lo que sí se repite es menos hundimiento. **Eso ya está visto en los tres tramos, así que no se puede confirmar con estos años**: Control hecho después (mismo SIC 3 × tercio de tamaño): hundidas ganadoras contra lo esperado por sus pares **5,9% / 11,1%**, **7,5% / 10,3%**, **22,0% / 27,7%**: la diferencia se achica pero sigue en los tres tramos. Tres de cada cuatro ganadoras están en el tercio grande; ser de las más grandes dentro del tercio puede explicar parte. La pista #109 tiene que controlar tamaño fino (activos) además del tercio. queda como pista #109 para confirmar con 10-K que todavía no tienen rendimiento (adjudicaciones 2023-2026 → hundidas a 4 años), y sirve como defensa (no como ganancia) en Tr.
Total probadas: 108 (#102 pasa la confirmación con cables; #104, #107 y #108 no; pista: las que ganan contratos públicos se hunden menos).

## #109: las que ganan contratos públicos se hunden menos — confirmación con otra fuente (contratos federales de EE.UU., USAspending). Escrita el 9-nov-2026 ANTES de bajar los datos
Disparada por lo que apareció de costado en #108 (y en #102): las ganadoras de contratos en la UE se hundían menos que sus pares en los tres tramos. Esos años ya están vistos con TED; para confirmar hace falta otra fuente que nunca miré: los contratos federales de EE.UU. (api.usaspending.gov, por empresa madre y año fiscal, desde 2008).
- **Empresa:** nombre del receptor (padre) con la misma regla `madre()` de #102.
- **Señal del año Y:** contratos federales por ≥ 10 millones de dólares en el año fiscal Y. Se cruza con el 10-K presentado en Y+1 y su `_ret4`.
- **Medida:** hundida = `_ret4` ≤ 0,5. Comparación contra lo esperado por sus pares sin contratos del mismo año × SIC 3 × **décimo** de tamaño (más fino que en #108, para que no lo explique el tamaño). Permutación de la etiqueta dentro de esos grupos (2.000), una cola.
- **Años (10-K):** exploración 2010-2016, confirmación 2017-2020, nunca usados 2021-2022.
- **Pasa si:** en la confirmación las ganadoras se hunden al menos 2 puntos menos que lo esperado con p < 0,05, y también menos (cualquier diferencia) en la exploración y en 2021-2022. Si pasa entra a Tr como defensa (bajar la nota de hundimiento) y se congela con los contratos de 2024-2026.
- Informado: exceso medio y mediano (como #108); montos ≥ 1.000 millones; primera vez contra ganan seguido.

### Resultado #109 (9-nov-2026, entrenar/usa109.py): **no pasa**
USAspending, años fiscales 2009-2021, ~4.900 receptores por año (los de ≥ 10 millones); casan con la regla `madre()` 825 nombres = 523 empresas (las más grandes: Lockheed, Boeing, Raytheon, Northrop, McKesson, Leidos, Booz Allen, General Dynamics).
| tramo | n | hundidas ganadoras | esperado por pares (año × SIC 3 × décimo de tamaño) | dif | p | exceso medio / mediano |
|---|---|---|---|---|---|---|
| exploración 2010-2016 | 311 | 6,1% | 9,0% | −2,9 | 0,24 | +0,031 / −0,006 |
| confirmación 2017-2020 | 255 | 6,3% | 6,4% | −0,1 | 0,73 | −0,058 / −0,003 |
| nunca usados 2021-2022 | 149 | 17,4% | 17,5% | −0,1 | 0,54 | −0,036 / +0,037 |
Aparte: ≥ 1.000 millones n 58, ninguna hundida (esperado 5,7%); < 1.000 millones 9,3% / 10,2%; primera vez 12,5% / 13,0%; ganan seguido 8,0% / 9,4%.
Criterio (confirmación ≤ −2 puntos con p < 0,05 y negativo en los otros dos): **no pasa** (−0,1, p 0,73).
Lo que se puede decir: con contratos federales de EE.UU. y pares del mismo décimo de tamaño, ganar contratos no se hunde menos en la confirmación. Con este método no apareció; lo de #108 puede ser tamaño fino o propio de la UE. No entra a Tr. Las 58 con ≥ 1.000 millones sin ninguna hundida se anota como dato, no como señal (no estaba escrito como criterio).
Total probadas: 109 (#102 pasa; #104, #107, #108 y #109 no).

## #110: «ganó un contrato afuera», versión pública de hoy (avisos 8-K a la SEC). Escrita el 9-nov-2026 ANTES de bajar los datos
Lo que funcionó en #102 no era el cable en sí sino el dato «esta empresa ganó un contrato en otro país». Ese dato hoy lo publica la propia empresa en sus avisos a la SEC (8-K y sus anexos, comunicados de prensa). Si es público el día que sale puede estar ya en el precio; por eso se prueba, no se supone.
- **Fuente:** buscador de texto completo de EDGAR (efts.sec.gov), formularios 8-K, años 2009-2021, dos búsquedas fijas: `"awarded" "contract" "government of"` y `"awarded" "contract" "ministry of"`.
- **Filtro a otro país:** se baja cada documento encontrado y cuenta sólo si a ≤ 300 caracteres de «awarded» aparece «Government of» o «Ministry of» seguido del nombre de un país que no sea EE.UU. (lista fija de países de la ONU). Sin modelo de lenguaje.
- **Señal del año Y:** la empresa (CIK) tiene al menos un aviso así presentado en el año calendario Y. Se cruza con su 10-K presentado en Y+1 y su `_ret4`.
- **Medida:** exceso = `_ret4` − mediana de `_ret4` de sus pares sin aviso del mismo año × SIC 3 × décimo de tamaño (grupos ≥ 5), en puntos. Permutación de la etiqueta dentro de los grupos (2.000), una cola.
- **Años (10-K):** exploración 2010-2016, confirmación 2017-2020, nunca usados 2021-2022.
- **Pasa si:** en la confirmación el exceso medio es ≥ +5 puntos con p < 0,05, y también positivo en la exploración y en 2021-2022. Si pasa, entra a Rt (no a Tr, que está sellada) como regla escrita aparte.
- Informado: hundidas contra lo esperado, mediana del exceso, primera vez contra seguido.

### Resultado #110 (9-nov-2026, entrenar/fts110.py): **no pasa — muestra insuficiente**
El buscador encontró 3.810 avisos 8-K de 1.730 empresas con las dos búsquedas. Con el filtro escrito (a ≤ 300 caracteres de «awarded», «Government of» o «Ministry of» + nombre de un país) quedan **56 avisos de 33 empresas** (Turquía 6, Honduras 5, India 4…; Puerto Rico entró por error en la lista, no es otro país). Al cruzar con el 10-K del año siguiente y pares del mismo año × SIC 3 × décimo de tamaño quedan **7 casos**: 4 en exploración (exceso medio +417 puntos, por una sola empresa; mediana −7), 1 en confirmación (+16, p 0,43), 2 en 2021-2022 (−50).
Criterio (confirmación ≥ +5 con p < 0,05 y positivo en los otros dos): **no pasa**. Con 1 caso en confirmación no hay nada que medir: con este método la señal no se pudo encontrar en los avisos, que nombran al cliente de otras formas («the Saudi Ministry of Health», «a Middle East customer», el nombre de la empresa estatal). No se cambia el filtro mirando el resultado; una versión que lea los avisos con un modelo de lenguaje (como en #102) sería otra prueba, escrita aparte.
Total probadas: 110 (#102 pasa; #104, #107, #108, #109 y #110 no).

## #111: «ganó un contrato afuera» leído por un modelo en los avisos 8-K (la versión de #102 con fuente actual). Escrita el 9-nov-2026 ANTES de leer
#110 no pudo medir: el filtro de palabras dejó 7 casos porque los avisos nombran al cliente de otras formas. Esta prueba lee los mismos 3.810 avisos (ya bajados, sin mirar resultados nuevos) con el mismo tipo de lector que marcó los cables en #102.
- **Lector:** Qwen2.5-3B-Instruct en Kaggle (GPU), temperatura 0. Texto: hasta 5.000 caracteres alrededor de la primera aparición de «awarded». Pregunta fija: si la empresa que presenta el aviso **ganó** un contrato o pedido de un cliente **fuera de EE.UU.** (gobierno extranjero, empresa estatal o privada extranjera), el país y el monto en millones.
- **Señal del año Y:** la empresa tiene al menos un aviso presentado en Y que el lector marca `foreign_win = true` con un país distinto de EE.UU. (y no Puerto Rico ni otro territorio de EE.UU.).
- **Medida, años y criterio:** idénticos a #110 (exceso de `_ret4` contra la mediana de pares sin señal del mismo año × SIC 3 × décimo de tamaño; permutación 2.000; pasa si confirmación 2017-2020 ≥ +5 puntos con p < 0,05 y positivo en exploración 2010-2016 y en 2021-2022).
- **Si hay menos de 30 casos en la confirmación**, se informa «muestra insuficiente» y no se saca conclusión.
- Informado: hundidas contra lo esperado, mediana, por monto (≥ 100 millones), gobierno contra privado.
- **Cambio de máquina (antes de leer):** Kaggle no tenía placas libres; el mismo lector y la misma pregunta corren en CPU en GitHub Actions (precisión completa en vez de media; ver el control de Rt: diferencias chicas). Los avisos se leen de a uno en vez de en tandas de 8.

### Resultado #111 (10-nov-2026, entrenar/avisos111_eval.py; lectura en GitHub Actions, 60 tramos en CPU): **muestra insuficiente**
Qwen leyó los 3.810 avisos (12 sin respuesta legible). Marcó «ganó un contrato de un cliente fuera de EE.UU.» en **304 avisos de 141 empresas** (China 35, Reino Unido 32, Vietnam 16, Brasil 14…). Revisando a mano unos pocos, hay errores claros (un premio de responsabilidad social en Perú contado como contrato); no se corrige porque la regla estaba escrita.
Al cruzar con el 10-K del año siguiente, `_ret4` y pares del mismo año × SIC 3 × décimo de tamaño (grupos ≥ 5) quedan **32 casos**: la mayoría de esas empresas son chicas o no están en el dataset de rendimientos.
| tramo | n | exceso medio | p | mediano | hundidas / esperado |
|---|---|---|---|---|---|
| exploración 2010-2016 | 18 | −7,1 | 0,69 | +1,5 | 5,6% / 23,3% |
| confirmación 2017-2020 | 8 | −17,2 | 0,86 | +5,9 | 12,5% / 14,8% |
| nunca usados 2021-2022 | 6 | −40,9 | 0,93 | −57,3 | 33,3% / 27,3% |
Aparte: gobierno o empresa estatal n 14, exceso +11,0 (mediana +7,1), hundidas 7,1% contra 26,6%; privado n 18, −36,9.
Criterio: con 8 casos en la confirmación (< 30) es **muestra insuficiente**; no se saca conclusión. Lo que se ve, sin valor de prueba: el exceso medio es negativo en los tres tramos; el único lado que se parece a #102 (clientes gobierno o estatales: más rendimiento y menos hundidas) tiene 14 casos.
Lo que se puede decir: con los avisos 8-K que nombran a un gobierno o ministerio, la versión actual de «ganó un contrato afuera» casi no toca a las empresas grandes que tengo medidas. Con este método no se pudo probar.
Total probadas: 111 (#102 pasa; #104, #107, #108, #109 y #110 no; #111 sin muestra).

## #112: «Lazy Prices» — las que casi no cambian su 10-K rinden más que las que lo reescriben. Escrita el 10-nov-2026 ANTES de bajar los textos
Fabri: «no va a buscar más nada». Lo que nunca probé es la idea publicada más conocida sobre el texto del 10-K y que apunta a la **dirección**, no a la magnitud: Cohen, Malloy y Nguyen, «Lazy Prices», *Journal of Finance* 75(3), 2020. Las empresas que cambian poco el informe de un año a otro rinden más después; las que lo cambian mucho, menos (sobre todo por la sección de riesgos). El trabajo salió en 2018 (SSRN): después de eso puede haberse gastado.
- **Fuente:** EDGAR-CORPUS (Loukas y otros, 2021; huggingface.co/datasets/eloukas/edgar-corpus), 10-K separados por sección, años 2009-2020. Para 2021-2022 (nunca usados) se bajan de la SEC con el mismo corte por sección si hace falta; si no se consiguen, se informa sin ese tramo y el criterio se evalúa con los otros dos.
- **Medida (fija):** para cada empresa (CIK) y año, similitud coseno de frecuencias de palabras (minúsculas, sólo letras, `HashingVectorizer` 2^20, norma L2) entre su 10-K y el del año anterior, en las secciones 1, 1A y 7; similitud = promedio de las secciones que existan en los dos años (al menos una). Sin 10-K el año anterior, no entra.
- **Grupos:** cada año de presentación, quintiles de similitud entre todas las empresas con rendimiento medido. «Quietas» = quintil más alto; «cambiadas» = quintil más bajo.
- **Resultado:** `_ret1` (12 meses desde el informe, quiebra = 0), como en el trabajo. Diferencia = media de `_ret1` de quietas − media de cambiadas, en puntos. Permutación de la etiqueta quieta/cambiada dentro de año × SIC 2 (2.000), una cola.
- **Años (10-K):** exploración 2010-2016, confirmación 2017-2020, nunca usados 2021-2022.
- **Pasa si:** confirmación ≥ +3 puntos con p < 0,05, y positiva en exploración y (si se consigue) en 2021-2022. Si pasa, entra a Rt como regla escrita aparte (Tr está sellada).
- Informado: lo mismo a 4 años (`_ret4`), hundidas, mediana, y la sección 1A sola.

### Resultado #112 (10-nov-2026, entrenar/lazy112.py): **no pasa**
EDGAR-CORPUS 2009-2020: 95.000 10-K, 70.796 pares empresa-año contra su año anterior; con rendimiento medido 24.317 (2010 tiene pocos: 394). Rendimientos como multiplicador × 100 (123,7 = ×1,237); la diferencia es en puntos.
| tramo | quietas / cambiadas (n) | `_ret1` medio quietas / cambiadas | dif | p | medianas | hundidas a 4 años |
|---|---|---|---|---|---|---|
| exploración 2010-2016 | 2.798 / 2.798 | 123,7 / 129,8 | −6,1 | 0,99 | 113,1 / 109,7 | 7,9% / 14,5% |
| confirmación 2017-2020 | 2.068 / 2.070 | 133,7 / 145,0 | −11,2 | 0,97 | 109,9 / 106,8 | 7,4% / 11,9% |
A 4 años: −1,4 y −25,9. Sólo la sección 1A: −5,0 y −1,1. Por año, las quietas le ganan a las cambiadas en 3 de 11 (2010, 2011, 2015), nunca con p < 0,05.
Criterio (confirmación ≥ +3 con p < 0,05 y positiva en exploración): **no pasa**; no hace falta bajar 2021-2022.
Lo que se puede decir: con esta medida y estos años, el efecto publicado no aparece en el promedio; va al revés. Se repite lo de todo el registro: las que cambian poco el informe **se hunden menos** (en los dos tramos, casi la mitad) y la mediana es algo más alta; el promedio de las que cambian mucho lo tiran para arriba unas pocas que se disparan. Magnitud, no dirección. Límites: el trabajo original mide con rendimiento mensual de carteras y el corte de secciones de EDGAR-CORPUS no es el mismo; el trabajo salió en 2018, a mitad de estos años.
Total probadas: 112 (#102 pasa; #104, #107, #108, #109, #110 y #112 no; #111 sin muestra).

## #113: las que reescriben mucho su 10-K se hunden más de lo que dicen su rubro y su tamaño. Escrita el 10-nov-2026 ANTES de medir contra pares
**Por qué:** en #112 las «cambiadas» (quintil más bajo de similitud con el 10-K anterior) se hundieron casi el doble que las «quietas» a 4 años (15,2% contra 8,6% en confirmación). Eso ya se vio, en crudo. Lo que NO se midió: si es algo más que tamaño y rubro (las chicas y las de ciertos rubros cambian más el texto y también se hunden más).
**Datos:** los mismos de #112 (lazy112_filas.csv: similitud y _ret4) cruzados con etiquetas.csv (sic, tam).
**Señal:** cambiada = quintil más bajo de `sim` en su año.
**Pares:** mismo año × SIC de 3 dígitos × decil de tamaño, grupos ≥5. Esperado = tasa de hundidas de las no señaladas del grupo. Hundida = `_ret4` ≤ 0,5.
**Medida:** hundidas de las cambiadas − esperado (puntos). Permutación dentro de grupos, 2000 veces, una cola.
**Criterio:** confirmación 2017-2020 ≥ +3 pts con p < 0,05, y exploración 2010-2016 > 0. Si no, no pasa.
**Aparte (no decide):** lo mismo con exceso de rendimiento a 4 años contra la mediana de pares, y del lado de las quietas.
**Resultado #113 (10-nov-2026): no pasa por poco.** Cambiadas: se hunden 13,7% contra 11,3% esperado por sus pares en confirmación (+2,4 pts, p 0,035; el umbral era +3) y 17,7% contra 12,9% en exploración (+4,8, p 0,002). La diferencia existe y es significativa en los dos tramos, pero en confirmación es más chica que lo fijado. Quietas: −3,2 (p 0,006) y −0,8 (p 0,37). El exceso medio es positivo (+40 / +44) y el mediano ≈ 0: más dispersión, no menos rendimiento. Nota: el preregistro se escribió antes de medir, pero se subió a GitHub junto con el resultado (el primer envío fue rechazado). Script: entrenar/hund113.py; salida: sal-cab102/hund113.log.
Total probadas: 113 (#102 pasa; #104, #107-#110, #112 y #113 no; #111 sin muestra).

## #114: lo de #113 en años nunca usados (10-K presentados en 2021 y 2022). Escrita el 10-nov-2026 ANTES de bajar los informes
**Por qué:** #113 dio +2,4 pts (p 0,035) en 2017-2020, debajo de su umbral (+3): queda como «no pasa». Esta es otra prueba, con años que ninguna prueba de texto tocó, para ver si el efecto sigue apareciendo.
**Datos:** de la SEC (data.sec.gov/submissions + Archives), el primer 10-K de cada año 2020, 2021 y 2022 de las empresas que tienen 10-K en EDGAR-CORPUS 2020. Se baja el documento principal, se le sacan etiquetas y números.
**Medida de similitud:** coseno del texto ENTERO (no por secciones; otra extracción que #112/#113) con HashingVectorizer igual que #112, contra el 10-K del año anterior.
**Señal, pares y medida:** idénticos a #113 (quintil más bajo de similitud en su año; pares año × SIC3 × decil de tamaño, grupos ≥5; hundida = _ret4 ≤ 0,5; permutación dentro de grupos, 2000, una cola).
**Criterio:** 2021-2022 juntos: hundidas de las cambiadas − esperado > 0 con p < 0,05. Si no, no pasa. Con menos de 300 cambiadas: muestra insuficiente.
**Resultado #114 (10-nov-2026): PASA.** 2.858 empresas bajadas de la SEC, 5.295 pares de 10-K (2.539 en 2021, 2.756 en 2022). Cambiadas (n 376 en grupos de pares): se hundieron 36,7% contra 28,0% esperado por sus pares de rubro y tamaño, +8,7 pts, p 0,004. Quietas: 20,2% contra 26,6%, −6,4, p 0,002. Por año: 2021 +13,9 (p 0,0005), 2022 +4,4 (p 0,14). El exceso medio sigue positivo (+38) y el mediano negativo (−8): más dispersión, la mitad de abajo cae más. Lo que pasa es la parte de riesgo: reescribir mucho el 10-K anticipa hundirse más que los pares; no dice que vayan a rendir menos en promedio. Script: entrenar/sim114.py; salida: sal-cab102/sim114.log.
Total probadas: 114 (#102 y #114 pasan; #104, #107-#110, #112 y #113 no; #111 sin muestra).

## #115: singularidad — las que se vuelven más distintas de su rubro rinden más que las que se van pareciendo. Escrita el 13-nov-2026 ANTES de medir
**Por qué (idea propia, no de un paper):** #112-#114 mostraron que cuánto cambia el texto anticipa riesgo, no dirección. Cambiar no dice hacia dónde. Acá importa la dirección del cambio en el espacio del rubro: alejarse del discurso común (algo propio) contra acercarse (volverse genérica).
**Datos:** vectores de la sección 1 (negocio) de EDGAR-CORPUS 2009-2020 ya calculados para #112 (HashingVectorizer, l2), sic y tam de etiquetas.csv.
**Medida:** singularidad = 1 − coseno con el centroide de las demás empresas de su SIC de 2 dígitos ese año (sin contarse a sí misma; grupos ≥10, sección con >500 caracteres). Δ = singularidad este año − el año anterior.
**Señal:** quintil más alto de Δ en su año = «se singulariza»; quintil más bajo = «converge».
**Medida de resultado:** exceso a 4 años = _ret4 − mediana de su grupo año × SIC3 × decil de tamaño (grupos ≥5), en puntos. Diferencia de medias se singulariza − converge; permutación dentro de año × SIC2, 2000, una cola.
**Criterio:** confirmación 2017-2020 ≥ +5 pts con p < 0,05 y exploración 2010-2016 > 0. Si pasa, falta 2021-2022 antes de cualquier uso en Tr. Aparte (no decide): hundidas de cada lado y el nivel de singularidad (no el cambio).
**Resultado #115 (13-nov-2026): no pasa.** 6.278 empresa-años con cambio de singularidad y rendimiento. Se singularizan − convergen, exceso a 4 años: exploración −15,6 pts (p 0,76), confirmación +20,0 (p 0,11; casi todo de 2017, +97). Medianas iguales (0). Aparte, no decide: el NIVEL de singularidad (no el cambio) separa hundidas: las más singulares de su rubro se hundieron 12,0% contra 17,8% de las más genéricas en exploración y 9,4% contra 19,2% en confirmación, sin rendir más en promedio (−37,2 y −1,4 pts). Otra vez magnitud y no dirección. Pista para una prueba aparte con 2021-2022 (habría que volver a bajar los textos por sección). Script: entrenar/sing115.py; salida: sal-cab102/sing115.log.
Total probadas: 115 (#102 y #114 pasan; #104, #107-#110, #112, #113 y #115 no; #111 sin muestra).

## #116: las más singulares de su rubro se hunden menos que sus pares, en años nunca usados (10-K de 2021 y 2022). Escrita el 13-nov-2026 ANTES de bajar
**Por qué:** en #115, aparte del criterio, las más singulares se hundieron 9,4% contra 19,2% de las más genéricas (2017-2020), en crudo. Falta saber si es algo más que tamaño y rubro, y si sigue en años nuevos.
**Datos:** los mismos 10-K de 2021 y 2022 que #114 (SEC), de las mismas empresas. Sección 1 = el tramo más largo entre un título «Item 1. Business» y el siguiente «Item 1A» o «Item 2»; si no se encuentra o tiene ≤500 caracteres, la empresa queda afuera.
**Medida:** singularidad igual que #115 (1 − coseno con el centroide del resto de su SIC2 ese año, grupos ≥10).
**Señal:** quintil más alto de singularidad en su año. Pares, hundida y permutación: idénticos a #113/#114 (año × SIC3 × decil de tamaño, grupos ≥5; _ret4 ≤ 0,5; 2000, una cola hacia abajo).
**Criterio:** 2021-2022 juntos: hundidas de las singulares − esperado < 0 con p < 0,05. Con menos de 300 singulares en grupos de pares: muestra insuficiente.

**Resultado #116 (13-nov-2026): no pasa.** Sección 1 encontrada en 2.557 informes de 2021 y 2.536 de 2022; 2.084 con rendimiento y pares. Singulares: se hundieron 20,9% contra 20,8% esperado por sus pares de rubro y tamaño (+0,1, p 0,56). Lo que en #115 separaba en crudo (9,4% contra 19,2%) con pares no apareció: con este método, parece venir del rubro y el tamaño. Aparte, no decide: exceso mediano a 4 años +7,3 en las singulares contra −11,7 en las genéricas (que se hundieron 31,4% contra 27,2% esperado, p 0,13). Script: entrenar/sing116.py; salida: sal-cab102/sing116.log.

## #117: el ciclo — el lado riesgoso gana cuando el mercado sube, y eso se puede saber antes. Escrita el 13-nov-2026 ANTES de medir
**Por qué (pedido de Fabri: «un ciclo que no estás viendo»):** varias señales dan vuelta el signo según los años (#115: −15,6 en 2010-2016 y +20,0 en 2017-2020; Gemma gana en 2017-2020 y no en 2021-2024; los «cohetes» fallan en 2021-2022). En vez de leerlo como azar, la hipótesis es que la dirección depende de la fase del ciclo.
**Señal de riesgo:** «cambiadas» = quintil más bajo de similitud con el 10-K anterior (la de #112-#114, la que más anticipa hundirse); «quietas» = quintil más alto. 2010-2020 de lazy112_filas.csv (secciones, EDGAR-CORPUS) y 2021-2022 de sim114.jsonl (texto entero, SEC).
**Diferencia por cohorte (año de presentación):** media de exceso logarítmico a 4 años de las cambiadas − de las quietas. Exceso log = log(max(_ret4, 0,01)) − mediana de log de su grupo año × SIC3 × decil de tamaño (grupos ≥5).
**A (explica):** correlación de Spearman entre esa diferencia y la mediana de _ret4 de todo el mercado en la misma cohorte (13 cohortes 2010-2022). Hipótesis ρ > 0.
**B (decide si sirve para elegir):** correlación de Spearman entre la diferencia y lo que el mercado rindió el año ANTERIOR (mediana de _ret1 de la cohorte previa, que ya se sabe al comprar). Hipótesis: ρ ≠ 0 (cualquier signo, dos colas).
**Criterio:** A: ρ > 0 con p < 0,05 (permutación de cohortes, 10.000, una cola). B: |ρ| con p < 0,05 (dos colas). Si A pasa y B no: «el ciclo existe pero no se ve antes con esta medida». Con 13 cohortes la prueba es de poca potencia: un no pasa no descarta el ciclo.
**Resultado #117 (13-nov-2026): A pasa, B no pasa.** 13 cohortes 2010-2022 (40 a 1.142 empresas cada una). A: la diferencia cambiadas − quietas sigue al mercado: ρ +0,61, p 0,018. Cuando la cohorte del mercado rinde mucho a 4 años, el lado riesgoso pierde menos o gana (2010 +45,7, 2011 +12,7); cuando rinde poco, pierde más (2021 −35,8, con el mercado en ×1,00). B: lo que el mercado rindió el año anterior no lo anticipa (ρ +0,01, p 0,99): el ciclo existe en esta señal, pero con esta medida no se ve antes. Aparte, no decide: en exceso logarítmico (que castiga a las que se hunden) las cambiadas quedaron debajo de las quietas en 11 de 13 cohortes. Script: entrenar/ciclo117.py; salida: sal-cab102/ciclo117.log y ciclo117_cohortes.csv.

## #118: ¿la curva de tasas anticipa hacia qué lado va el ciclo de #117? Escrita el 13-nov-2026 ANTES de bajar las tasas
**Por qué:** #117 mostró que la diferencia cambiadas − quietas sigue al mercado (ρ +0,61), pero el rendimiento del año anterior no lo anticipa. La pendiente de la curva de tasas (10 años − 2 años) es el indicador de ciclo más usado y se conoce al comprar.
**Datos:** tasas diarias del Tesoro de EE.UU. (home.treasury.gov, daily_treasury_yield_curve), 2010-2022.
**Medida:** pendiente media de 10 años − 2 años entre enero y marzo del año de presentación (cuando salen la mayoría de los 10-K).
**Prueba:** Spearman entre esa pendiente y la diferencia por cohorte de #117 (ciclo117_cohortes.csv, 13 cohortes, sin tocar), y aparte contra la mediana del mercado a 4 años. Permutación de cohortes 10.000, dos colas.
**Criterio:** pasa si la pendiente con la diferencia da p < 0,05. Con 13 cohortes, un no pasa no descarta nada.
**Resultado #118 (13-nov-2026): no pasa.** Pendiente 10a−2a de ene-mar contra la diferencia cambiadas − quietas: ρ +0,03 (p 0,92). Contra el mercado a 4 años: ρ +0,37 (p 0,20). Con esta medida y 13 cohortes la curva no anticipó la fase del ciclo que mueve la señal. Script: entrenar/tasas118.py; salida: sal-cab102/tasas118.log.
Total probadas: 118 (#102 y #114 pasan; #117 pasa la parte A (el ciclo existe) y no la B (verlo antes); #104, #107-#110, #112, #113, #115, #116 y #118 no; #111 sin muestra).

## #119: la euforia anticipa el ciclo — después de años con muchas salidas a la bolsa, el lado riesgoso rinde peor. Escrita el 13-nov-2026 ANTES de contar
**Por qué:** #117 mostró el ciclo y #118 que la curva de tasas no lo anticipa. Baker y Wurgler (2006, Journal of Finance, «Investor sentiment and the cross-section of stock returns») encuentran que después de épocas de sentimiento alto las acciones especulativas rinden peor; uno de sus componentes es la cantidad de salidas a la bolsa.
**Datos:** índices trimestrales de EDGAR (full-index/AAAA/QTRn/form.gz), 2009-2021.
**Medida:** cantidad de formularios S-1 (originales, sin enmiendas S-1/A) presentados en el año calendario anterior al de presentación de la cohorte (se conoce al comprar).
**Prueba:** Spearman entre esa cantidad y la diferencia cambiadas − quietas por cohorte de #117 (ciclo117_cohortes.csv, 13 cohortes 2010-2022, sin tocar). Permutación de cohortes 10.000.
**Criterio:** ρ < 0 con p < 0,05 (una cola, la dirección de Baker y Wurgler). Con 13 cohortes, un no pasa no descarta nada.
**Resultado #119 (13-nov-2026): no pasa.** S-1 por año en EDGAR: de 701 (2019) a 2.236 (2021). Contra la diferencia cambiadas − quietas de la cohorte siguiente: ρ −0,16 (p 0,29), en la dirección de Baker y Wurgler pero sin fuerza; contra el mercado a 4 años, ρ −0,25. La cohorte 2022, la del año con más salidas a la bolsa (2021), sí quedó abajo (−18,9), pero con 13 cohortes no alcanza. Script: entrenar/euforia119.py; salida: sal-cab102/euforia119.log.
Total probadas: 119 (#102 y #114 pasan; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118 y #119 no; #111 sin muestra).

## #120: Rt con el filtro de #114 — no comprar las que más reescribieron su 10-K. Escrita el 14-nov-2026 ANTES de cruzar con las elegidas de Rt
**Por qué:** #114 pasó en años nunca usados (las cambiadas se hunden +8,7 pts más que sus pares). La regla de #112 dice que lo que pasa entra a Rt como regla escrita aparte (Tr está sellada). Antes de tocar el Rt que corre, se mide en su prueba hacia atrás.
**Datos:** las elegidas de Rt por camada 2017-2022 (rt_atras.py: el 10% de arriba de Gemma en su industria) y la similitud con el 10-K anterior (2017-2020 de lazy112_filas.csv; 2021-2022 de sim114.jsonl). Cambiada = quintil más bajo de similitud entre todas las empresas de su año. Ojo: esas similitudes ya se usaron en #112-#114; lo nuevo es el cruce con las elegidas de Rt.
**Comparación por camada:** elegidas sin filtro contra elegidas sin las cambiadas (las que no tienen similitud se quedan).
**Criterio para que entre a Rt:** hundidas a 4 años (_ret4 ≤ 0,5) más bajas con filtro en al menos 5 de las 6 camadas, Y rendimiento medio a 12 meses (_ret1) con filtro no más de 1 punto por debajo del de sin filtro en promedio de las 6. Si pasa, se programa en rt.py como regla aparte con fecha; si no, Rt sigue igual.
**Resultado #120 (14-nov-2026): no pasa, Rt sigue igual.** El filtro saca entre 39 y 59 de las ~280-340 elegidas por camada. Hundidas a 4 años sin → con filtro: 2017 4,9 → 5,1; 2018 8,2 → 8,3; 2019 7,7 → 6,3; 2020 7,3 → 5,3; 2021 23,8 → 20,9; 2022 21,5 → 20,2. Bajan en 4 de 6 (el criterio pedía 5). El rendimiento a 12 meses con filtro quedó +2,2 pts arriba en promedio (subió en las 6). Las sacadas se hundieron 37,8% en 2021 y 29,3% en 2022, contra 23,8% y 21,5% de todas las elegidas. Script: entrenar/rt120.py; salida: sal-cab102/rt120.log.
Total probadas: 120 (#102 y #114 pasan; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#120 no; #111 sin muestra).

## #121: el miedo del mercado al comprar anticipa la fase del ciclo de #117. Escrita el 14-nov-2026 ANTES de bajar el VIX
**Por qué:** #117 mostró que la diferencia cambiadas − quietas sigue al mercado a 4 años, y #117B, #118 y #119 no lograron verlo antes. Asness («The Siren Song of Factor Timing», 2016) dice que adivinar la fase es muy difícil; el trabajo «Timing the Factor Zoo» (AEA 2024) encuentra que las señales de volatilidad sí mejoran algo. Un VIX alto suele venir antes de años buenos de mercado (prima por varianza, Bekaert y Hoerova 2014), y en años buenos el lado riesgoso pierde menos (#117A).
**Datos:** historia diaria del VIX publicada por Cboe (cdn.cboe.com, VIX_History.csv), 2010-2022.
**Medida:** VIX medio al cierre entre enero y marzo del año de presentación (cuando salen la mayoría de los 10-K; se conoce al comprar).
**Prueba:** Spearman entre ese VIX y la diferencia por cohorte de #117 (ciclo117_cohortes.csv, 13 cohortes 2010-2022, sin tocar). Permutación de cohortes 10.000.
**Criterio:** ρ > 0 con p < 0,05 (una cola). Aparte, sólo para mirar: VIX contra el mercado a 4 años. Con 13 cohortes, un no pasa no descarta nada.
**Resultado #121 (14-nov-2026): no pasa.** VIX medio de enero a marzo: de 11,7 (2017) a 31,2 (2020). Contra la diferencia cambiadas − quietas: ρ +0,04 (p 0,45). Contra el mercado a 4 años: ρ −0,15. 2020 tuvo el miedo más alto y la diferencia quedó en −9,8; 2010 y 2016 tuvieron el mismo VIX (≈20) y diferencias de +45,7 y −22,4. Con esta medida y 13 cohortes el miedo al comprar no anticipó la fase. Script: entrenar/vix121.py; salida: sal-cab102/vix121.log.
Total probadas: 121 (#102 y #114 pasan; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#121 no; #111 sin muestra).

## #122: el filtro de #114 como seguro, en años que nunca tocó (2023-2025). Escrita el 14-nov-2026 ANTES de bajar los 10-K
**Por qué:** #117-#121 muestran que la fase del mercado no se adivina antes con ninguno de cuatro termómetros. Entonces una señal de riesgo no se juzga por «gana en 5 de 6 años» sino como un seguro: que no falle en ningún año y que en el total esquive hundimientos. #120 se juzgó con la regla vieja y no se re-juzga con datos ya vistos; esta prueba usa camadas nuevas.
**Datos:** 10-K de 2022, 2023, 2024 y 2025 bajados de la SEC (API submissions + Archives) para las empresas con etiqueta 2023-2025 y rendimiento a 12 meses (_ret1). Ninguna similitud de estos años se calculó antes. No hay _ret4 todavía para estos años, así que el horizonte es 12 meses.
**Medida:** igual que #114: similitud coseno del texto entero contra el 10-K del año anterior; cambiadas = quintil más bajo de su año. Hundida a 12 meses = _ret1 ≤ 0,5. Pares = año × SIC de 3 dígitos × decil de tamaño, grupos ≥ 5; esperado = tasa de hundimiento de los pares no cambiados; permutación dentro de grupos, 2000, una cola.
**Criterio (seguro):** pasa si (1) en el total 2023-2025 las cambiadas se hunden más que lo esperado con p < 0,05, Y (2) en cada uno de los 3 años la diferencia es ≥ 0 (no falla ningún año). Con menos de 300 cambiadas: muestra insuficiente. Si pasa, entra a Rt como regla aparte con fecha.
**Resultado #122 (15-nov-2026): no pasa.** 9.377 pares de 10-K (2023: 3.157, 2024: 3.191, 2025: 3.029); 785 cambiadas con pares. Hundidas a 12 meses: 13,4% contra 12,8% esperado, +0,6 pts (p 0,34). Por año: 2023 +2,3, 2024 −0,0, 2025 −0,9: falla en dos años. A 12 meses y en 2023-2025 el filtro no funcionó como seguro. Fuera del criterio, sólo para anotar: las quietas (quintil más alto de similitud) se hundieron menos que sus pares (6,4% contra 8,3%, −1,8 pts, p 0,03); no se usa para nada sin una prueba propia. Script: entrenar/sim122.py; salida: sal-cab102/sim122.log.
Total probadas: 122 (#102 y #114 pasan; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#122 no; #111 sin muestra).

## #123: los de adentro saben la fase — compras netas de directivos en el año anterior. Escrita el 16-nov-2026 ANTES de bajar los datos
**Por qué:** #117B-#122 buscaron la fase con termómetros de afuera (precios, tasas, salidas a la bolsa, VIX). Seyhun (1988) y Lakonishok y Lee (2001, Review of Financial Studies, «Are insider trades informative?») encuentran que las compras y ventas de directivos sumadas en todo el mercado anticipan el rendimiento del mercado. Los de adentro ven la fase antes.
**Datos:** SEC, Insider Transactions Data Sets (formularios 3/4/5 estructurados), trimestres 2009T1-2021T4 (sec.gov/files/structureddata/data/insider-transactions-data-sets/AAAAqN_form345.zip), tabla NONDERIV_TRANS.
**Medida:** proporción neta de compras del año calendario anterior a la presentación (se conoce al comprar): (compras P − ventas S) / (P + S), contando transacciones de acciones comunes con código P o S, sin duplicados por número de acceso.
**Prueba:** Spearman entre esa proporción y la diferencia cambiadas − quietas por cohorte de #117 (ciclo117_cohortes.csv, 13 cohortes 2010-2022, sin tocar). Permutación 10.000.
**Criterio:** ρ > 0 con p < 0,05 (una cola: más compras de adentro → mejor mercado → el lado riesgoso pierde menos). Aparte, sólo para mirar, contra el mercado a 4 años. Con 13 cohortes, un no pasa no descarta nada.

## #124: los informes mismos dicen la fase — cuánto reescribe toda la economía. Escrita el 16-nov-2026 ANTES de calcular
**Por qué:** la idea propia: si en un año casi todas las empresas reescriben su 10-K, algo cambió para todas (un golpe, un cambio de época). Es un termómetro de adentro que nadie mira así.
**Datos:** similitudes ya calculadas (lazy112_filas.csv 2010-2020, sim114.jsonl 2021-2022), todas las empresas, no sólo las cambiadas.
**Medida:** mediana de la similitud con el 10-K anterior de todas las empresas de la cohorte (se conoce al comprar).
**Prueba:** Spearman entre esa mediana y la diferencia de #117, 13 cohortes, permutación 10.000.
**Criterio:** p < 0,05 a dos colas (no sé el signo de antemano). Ojo: la similitud ya se usó para armar cambiadas y quietas; lo nuevo es usar su nivel de toda la economía como termómetro.
**Resultado #123 (16-nov-2026): no pasa.** Compras netas de directivos del año anterior, de −0,55 (2021) a −0,13 (2009; en el primer trimestre de 2009, con el mercado en el piso, compraron 9.755 veces contra 5.602 ventas). Contra la diferencia cambiadas − quietas: ρ +0,26 (p 0,19). Contra el mercado a 4 años: ρ +0,38. Va en la dirección de Lakonishok y Lee, pero sin fuerza con 13 cohortes. Script: entrenar/adentro123.py; salida: sal-cab102/adentro123.log.
**Resultado #124 (16-nov-2026): PASA.** Mediana de la similitud de toda la economía contra la diferencia: ρ −0,57 (p 0,045, dos colas). Contra el mercado a 4 años: ρ −0,76. Cuando casi todas las empresas reescriben (2010 después de la crisis, 2020), los 4 años siguientes son buenos para el mercado y el lado riesgoso pierde menos. Cuando casi todas copian el informe del año anterior (2017, 2021, 2022), vienen años flojos. **Advertencias, sin cambiar el veredicto:** (1) 2010-2020 vienen de lazy112 (secciones 1, 1A y 7) y 2021-2022 de sim114 (texto entero), y las dos más altas y peores son justo las del método nuevo. Mirado aparte, sólo 2010-2020 con el mismo método: ρ −0,55 con la diferencia (p 0,08) y −0,62 con el mercado (p 0,04); la dirección se mantiene. (2) Las medianas son todas muy parecidas (0,9927 a 0,9986). (3) Con 124 pruebas, p 0,045 está en el borde. Por eso no entra a Rt todavía: se sella una predicción.
**Predicción sellada #124 (16-nov-2026, se resuelve 2027-2029):** con el texto entero (mismo método que 2021-2022), la mediana de similitud fue 2021 0,99818; 2022 0,99862; 2023 0,99884; 2024 0,99879; 2025 0,99901. Las tres cohortes nuevas copian aún más que 2021-2022. El termómetro dice años flojos. Predicción: para las cohortes 2023, 2024 y 2025, (a) la mediana de _ret4 del mercado queda debajo de 1,315 (la mediana de las 13 cohortes 2010-2022) y (b) la diferencia cambiadas − quietas de #117 es negativa. Acierta si se cumplen (a) y (b) en al menos 2 de las 3 cohortes.
Total probadas: 124 (#102, #114 y #124 pasan; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123 no; #111 sin muestra).

## #125: el termómetro de #124 en años nunca usados, 1997-2009, contra el S&P 500. Escrita el 16-nov-2026 ANTES de bajar los 10-K
**Por qué:** #124 pasó en el borde y su predicción sellada tarda hasta 2029. Se puede probar ya hacia atrás: los 10-K están en EDGAR desde 1993 y el S&P 500 mensual es público (datos de Shiller). Las etiquetas por empresa empiezan en 2009, así que acá se prueba sólo la parte del mercado (ρ −0,76 en #124), no la diferencia cambiadas − quietas.
**Datos:** índices EDGAR full-index/AAAA/QTRn/form.gz; para cada año y de 1997 a 2009, las empresas (CIK) con un 10-K o 10-K405 en y y en y−1; muestra al azar de 300 por año (semilla 0). De cada presentación (archivo .txt completo) se toma sólo el primer documento (el 10-K, sin anexos), se le quitan las etiquetas y se mide la similitud coseno con el del año anterior (mismo vectorizador que #114). S&P 500: github.com/datasets/s-and-p-500 (datos de Shiller), precio mensual.
**Medida:** mediana de la similitud de la muestra de cada año. Rendimiento del mercado = S&P 500 de abril de y+4 / abril de y (sin dividendos).
**Prueba:** Spearman entre la mediana y el rendimiento a 4 años, 13 años (1997-2009). Permutación 10.000.
**Criterio:** ρ < 0 con p < 0,05 (una cola, la dirección de #124). Advertencias escritas antes: las ventanas de 4 años se superponen, así que el p real es más alto que el de la permutación; el formato de los 10-K cambia en esos años (texto plano a HTML). Si pasa, refuerza #124; si no, #124 queda sólo con su predicción sellada.
**Resultado #125 (16-nov-2026): no pasa.** 3.887 pares de 10-K (≈300 por año, 1997-2009, ningún error de bajada). Mediana de similitud contra el S&P 500 a 4 años: ρ −0,03 (p 0,47). Encajan 2003 (la economía reescribió más que nunca después de la caída de 2000-2002 y el S&P subió 64% en 4 años) y 2005-2007 (copiaron mucho y vinieron años flojos), pero no 2009: con una similitud de las más altas, el S&P subió 85%. Además la similitud sube casi sola de 2003 a 2008, lo que sugiere que mide también cambios de formato y no sólo la fase. En años nunca usados, el termómetro de #124 no anticipó al mercado. #124 queda debilitado: su predicción sellada sigue en pie sin cambios, pero no entra a Rt. Script: entrenar/viejo125.py; salida: sal-cab102/viejo125.log.
Total probadas: 125 (#102, #114 y #124 pasan; #124 no se sostuvo en 1997-2009 (#125); #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123 y #125 no; #111 sin muestra).

## #126: #125 con la vara correcta — mercado con todas las empresas pesando igual. Escrita el 16-nov-2026 ANTES de bajar los datos de French
**Por qué:** en #125 dije «#124 fue probablemente suerte»: fue una conclusión de más; lo correcto es «con este método no apareció». Y #125 midió otra cosa que #124: #124 usaba la mediana de las empresas (todas pesan igual) y #125 el S&P 500 (pesa por tamaño). En 1999-2004 las grandes cayeron y las chicas subieron, así que la vara cambia el resultado. **Aviso:** esta corrección se escribe DESPUÉS de ver #125 con el S&P (no con esta vara), así que aunque pase cuenta menos que una prueba limpia.
**Datos:** Kenneth French Data Library, «Portfolios Formed on Size» (Portfolios_Formed_on_ME_CSV.zip), rendimientos mensuales con todas las empresas pesando igual, 10 deciles. Medianas de similitud 1997-2009 de #125 (viejo125.jsonl, sin tocar).
**Medida:** mercado con peso igual = promedio de los 10 deciles cada mes, compuesto de abril de y a marzo de y+4 (48 meses).
**Prueba y criterio:** Spearman entre la mediana de similitud y ese rendimiento, 13 años 1997-2009, permutación 10.000. Pasa si ρ < 0 con p < 0,05 (una cola). Las ventanas se superponen: el p real es más alto.
**Resultado #126 (16-nov-2026): no pasa.** Con el mercado de peso igual (French) la vara cambia mucho (2001-2003: +62%, +66%, +141% en 4 años, contra un S&P casi plano), pero la relación sigue sin aparecer: ρ −0,13 (p 0,33). Encaja 2003 (la economía reescribió más que nunca y vino +141%) y 2005 (copiaron mucho y vino −31%); no encaja 2009 (copiaron casi todo en plena crisis y vino +170%). Con este método, en 1997-2009 el termómetro de #124 no anticipó al mercado ni con la vara del S&P ni con la de peso igual. Script: entrenar/peso126.py; salida: sal-cab102/peso126.log.
Total probadas: 126 (#102, #114 y #124 pasan; #124 no apareció en 1997-2009 (#125, #126); #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125 y #126 no; #111 sin muestra).

## #127: la crisis es la fase — cuánto está el mercado debajo de su máximo al comprar. Escrita el 16-nov-2026 ANTES de calcular
**Por qué:** Fabri: «vos estás diciendo que después de la crisis del 2008 no tiene nada que ver». #124-#126 trataban «copiar el informe» igual en cualquier año, y 2009 (copiaron en plena crisis) rompió la regla. En #126, los dos mejores cuatrienios de la tabla son justo los que siguen a una caída grande: 2003 (+141%) y 2009 (+170%). La reversión después de caídas largas está documentada (De Bondt y Thaler, 1985). **Aviso:** la idea sale de mirar #125/#126; 2003 y 2009 ya se vieron. Para que cuente, se prueba en los 25 años 1997-2021 y aparte en las cohortes 2010-2022 contra la diferencia de #117.
**Datos:** S&P 500 mensual (datos de Shiller, fuentes/sp500_shiller.csv) y mercado con peso igual de French (Portfolios_Formed_on_ME, 10 deciles).
**Medida:** caída desde el máximo = S&P de marzo de y / máximo del S&P en los 60 meses anteriores − 1 (se conoce al comprar; 0 si está en su máximo).
**Prueba A:** Spearman entre la caída y el mercado de peso igual de abril de y a marzo de y+4, años 1997-2021 (25). Pasa si ρ < 0 con p < 0,05, una cola (más abajo del máximo → mejores 4 años). Las ventanas se superponen: el p real es más alto.
**Prueba B:** Spearman entre la caída y la diferencia cambiadas − quietas de #117 (13 cohortes 2010-2022). Pasa si ρ < 0 con p < 0,05 (una cola). B es la que decidiría si Rt arriesga después de una crisis.
**Resultado #127 (16-nov-2026): A PASA y B PASA.** A (1997-2021, 25 años): cuanto más abajo de su máximo está el mercado al comprar, mejores los 4 años siguientes con peso igual: ρ −0,53 (p 0,004). Los años con caída de 20% o más (2001, 2002, 2003, 2004, 2009, 2010, 2020) dieron de 1,25 a 2,70 en 4 años, salvo 2005 (0,69, con −20%); los años en su máximo dieron de 0,95 a 1,90. B (2010-2022, contra la diferencia cambiadas − quietas de #117): ρ −0,55 (p 0,027). El lado riesgoso ganó justo en las dos cohortes que arrancaron más abajo del máximo (2010: −25% → +45,7; 2011: −15% → +12,7) y perdió en las que arrancaron en el máximo (2013, 2021: −37,1 y −35,8). **Advertencias:** la idea salió de mirar 2003 y 2009 en #125/#126 (las preguntó Fabri); las ventanas de 4 años se superponen y el p real es más alto; B tiene sólo dos cohortes de crisis de verdad (2010, 2020). Es la primera medida del ciclo que se sabe al comprar y que pasa en las dos partes. Script: entrenar/crisis127.py; salida: sal-cab102/crisis127.log.
Total probadas: 127 (#102, #114, #124 y #127 pasan; #124 no apareció en 1997-2009 (#125, #126); #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125 y #126 no; #111 sin muestra).

## #128: #127B en años nunca usados — riesgosas contra quietas después de caídas, 1964-1996. Escrita el 16-nov-2026 ANTES de bajar los datos
**Por qué:** #127 pasó, pero la idea salió de mirar 2003 y 2009 y B tenía sólo dos crisis. French publica carteras por volatilidad desde 1963: 33 años nunca mirados, con varias caídas grandes (1970, 1974, 1982, 1987, 1990).
**Datos:** Kenneth French Data Library, «Portfolios Formed on Variance» (Portfolios_Formed_on_VAR_CSV.zip), rendimientos mensuales con peso igual, quintiles. S&P 500 mensual (Shiller).
**Medida:** caída desde el máximo como en #127 (S&P de marzo de y contra su máximo de 60 meses). Diferencia riesgosas − quietas = log del rendimiento compuesto de abril de y a marzo de y+4 del quintil más volátil menos el del quintil menos volátil.
**Prueba:** Spearman entre la caída y esa diferencia, años 1964-1996 (33). Permutación 10.000.
**Criterio:** ρ < 0 con p < 0,05 (una cola: más abajo del máximo → las riesgosas le ganan a las quietas). Las ventanas se superponen: el p real es más alto. Si pasa, se escribe la regla para Rt (arriesgar después de caídas, esquivar riesgo en el máximo) y se prueba en su prueba hacia atrás antes de usarla.
**Resultado #128 (16-nov-2026): no pasa.** 1964-1996 (33 años): caída desde el máximo contra log(riesgosas/quietas) a 4 años: ρ −0,04 (p 0,42). Encaja 1974-1977 (caídas de 15-29%; las volátiles le ganaron a las quietas, +0,29 a +0,51) pero no 1982 (−18%; las volátiles perdieron −0,73) ni 1964-1965 (en el máximo; las volátiles ganaron +0,72 y +0,83). Con este método y en estos años, que el mercado esté abajo de su máximo no anticipó cuándo ganan las riesgosas. Ojo: «riesgosas» acá es el quintil más volátil de French, no las que reescriben su 10-K de #127B; es una vara parecida, no la misma. #127 sigue anotado como pasa, sin confirmación fuera de los años donde nació. Script: entrenar/vol128.py; salida: sal-cab102/vol128.log.
Total probadas: 128 (#102, #114, #124 y #127 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 con volatilidad (#128); #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126 y #128 no; #111 sin muestra).

## #129: predicción sellada 2026-2030 — se compra en el máximo, el lado riesgoso pierde. Escrita el 16-nov-2026 ANTES de bajar los 10-K de 2026
**Por qué:** hoy (16-nov-2026) el S&P 500 está en 7.466, 2,9% debajo de su máximo de 5 años (Yahoo, ^GSPC mensual): fase «en el máximo». En #127B, las dos cohortes compradas en el máximo (2013, 2021) dieron −37 y −36 para las cambiadas contra las quietas. En 146 años (S&P con dividendos 1881-2021), comprar en el máximo dio ×1,45 típico a 4 años y perdió 12% de las veces, contra ×1,64 y 6% después de caídas de 20% o más.
**Datos:** 10-K de 2026 y de 2025 bajados de la SEC para las empresas de sim122.jsonl con similitud 2025; mismo método que #114/#122 (texto entero).
**La lista:** cambiadas = quintil más bajo de similitud 2026 contra 2025; quietas = quintil más alto. Se publican las dos listas (CIK) en el repositorio el mismo día, antes de cualquier precio posterior.
**Predicción (se resuelve en noviembre de 2030, con rendimiento a 4 años desde la presentación del 10-K):** (a) las cambiadas se hunden (rendimiento ≤ 0,5) más que sus pares (año × SIC3 × decil de tamaño), por al menos 3 puntos; (b) la diferencia media de log-exceso cambiadas − quietas (como #117) es negativa. Acierta si se cumplen (a) y (b).
**Sellado #129 (16-nov-2026):** 2.716 empresas con 10-K 2026 y 2025 (de 3.029 buscadas). Listas en notas/prediccion-129-2026.json: 544 cambiadas y 543 quietas (CIK), sha256 del archivo 4306f04356bb90752d778e5fc289eb00a36f39ecd83ce79b183577830a87d64a. Se resuelve en noviembre de 2030. Script: entrenar/sim129.py y entrenar/sellar129.py.

## #130: el ciclo de vida de cada empresa (Dickinson 2011). Escrita el 16-nov-2026 ANTES de bajar los datos
**Por qué:** todo #117-#129 buscó el ciclo del mercado. Hay otro: el de cada empresa. Dickinson («Cash flow patterns as a proxy for firm life cycle», The Accounting Review, 2011) clasifica la etapa por el signo de los flujos de caja operativo (O), de inversión (I) y de financiación (F): nacimiento (O−, I−, F+), crecimiento (O+, I−, F+), madurez (O+, I−, F−), declive (O−, I+, cualquier F) y sacudón (el resto). Nunca se probó acá.
**Datos:** SEC XBRL frames (data.sec.gov/api/xbrl/frames/us-gaap/{concepto}/USD/CY{año}.json) para NetCashProvidedByUsedInOperatingActivities, NetCashProvidedByUsedInInvestingActivities y NetCashProvidedByUsedInFinancingActivities, años fiscales 2009-2021. El año fiscal y−1 se asigna a la cohorte de presentación y (etiquetas.csv), id = hash del CIK.
**Prueba:** hundidas a 4 años (_ret4 ≤ 0,5) de cada etapa contra sus pares de otras etapas (año × SIC3 × decil de tamaño, grupos ≥ 5), permutación dentro de grupos 2000, cohortes 2010-2022 juntas.
**Criterio:** pasa si las empresas en declive se hunden al menos 3 puntos más que sus pares con p < 0,05 (una cola) Y también en la mitad 2017-2022 sola (diferencia > 0). Las otras etapas se informan sólo para mirar.
**Resultado #130 (16-nov-2026): PASA.** 9.675 empresas-año con los tres flujos y etiqueta (2010-2022). Declive (O−, I+): se hundieron 33,3% contra 24,5% esperado por sus pares, +8,8 pts (p 0,0005); sólo 2017-2022: +8,0 (p 0,0005). Para mirar: nacimiento +10,9 (p 0,002), sacudón +0,1, crecimiento +0,2, madurez −5,6 (las maduras se hunden menos). Por cohorte, el declive se hunde más que el total en 10 de 13 (2010, 2011 y 2017 no; 2010-2011 con 1 y 4 empresas). **Advertencias:** es la réplica de un resultado publicado (Dickinson 2011), no una idea nueva; los frames de XBRL cubren sólo una parte de las empresas (las que reportan esos conceptos exactos). Es una señal de riesgo, como las anteriores: dice quién se hunde, no quién sube.
**Sellado #130 (16-nov-2026):** año fiscal 2025 (10-K de 2026), 5.174 empresas con los tres flujos: 558 en declive y 1.328 en nacimiento. Lista en notas/prediccion-130-2026.json (CIK), sha256 833cb6201d6cf6af947680b285bea4249749814e04f320593371094ba7b5061e. Predicción para noviembre de 2030: las de declive se hunden (_ret4 ≤ 0,5) al menos 3 puntos más que sus pares. Por la regla de #112, entra a Rt sólo como regla aparte y después de su prueba hacia atrás. Script: entrenar/vida130.py, entrenar/sellar130.py; salida: sal-cab102/vida130.log.
Total probadas: 130 (#102, #114, #124, #127 y #130 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126 y #128 no; #111 sin muestra).

## #131: Rt sin las empresas en declive (#130). Escrita el 16-nov-2026 ANTES de cruzar con las elegidas de Rt
**Por qué:** #130 pasó. Por la regla de #112, entra a Rt como regla aparte sólo si mejora su prueba hacia atrás.
**Datos:** las elegidas de Rt por camada 2017-2022 (rt_atras.py: 10% de arriba de Gemma en su industria) y la etapa de Dickinson del año fiscal anterior (frames de vida130.py). Sin etapa = se quedan.
**Comparación por camada:** elegidas sin filtro contra elegidas sin las que están en declive.
**Criterio (el mismo de #120):** hundidas a 4 años más bajas con filtro en al menos 5 de 6 camadas, Y rendimiento medio a 12 meses con filtro no más de 1 punto por debajo en promedio. Si las sacadas son menos de 30 en total, muestra insuficiente y Rt sigue igual. Si pasa, se programa en rt.py como regla aparte con fecha.
**Resultado #131 (16-nov-2026): no pasa, Rt sigue igual.** Rt casi no elige empresas en declive: el filtro saca entre 5 y 26 de las 279-341 elegidas por camada (72 en total). Hundidas a 4 años sin → con filtro: 2017 4,9 → 5,1; 2018 8,2 → 6,8; 2019 7,7 → 7,8; 2020 7,3 → 6,7; 2021 23,8 → 23,3; 2022 21,5 → 20,2. Bajan en 4 de 6 (pedía 5); rendimiento a 12 meses −0,6 pts. Las sacadas se hundieron 50% (2018), 43% (2021) y 41% (2022), pero en 2017 y 2019 ninguna. Lo que dice: Gemma ya esquiva casi todas las empresas en declive; el filtro tiene poco para sacar. Script: entrenar/rt131.py; salida: sal-cab102/rt131.log.
Total probadas: 131 (#102, #114, #124, #127 y #130 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128 y #131 no; #111 sin muestra).

## #132: lo que Tr ve es la etapa de vida de la empresa, y eso explica su ciclo. Escrita el 16-nov-2026 ANTES de cruzar
**Por qué:** Fabri, tras #131: «descartado todo sólo porque no entendiste lo que en realidad estaba pasando». #131 no es «nada»: muestra que el 10% de arriba de Gemma casi no tiene empresas en declive, o sea que Gemma, leyendo el texto, ve la etapa de vida. Hipótesis: Tr detecta empresas maduras; las maduras se hunden menos siempre (#130: −5,6) pero pierden contra las jóvenes cuando el mercado sube fuerte. Eso explicaría el patrón de 131 pruebas («ve quién se cae, no hacia dónde») y por qué Rt empata o pierde en 2020-2022.
**Datos:** puntaje de Gemma (gemma_1_1A_7_puntaje.csv + 2021-2022 como en rt120.py), etapas de vida130.py, etiquetas.csv.
**A (qué ve Tr):** proporción de cada etapa en el 10% de arriba de Gemma por industria contra el resto, 2017-2022. Pasa si la proporción de maduras arriba supera a la del resto en las 6 camadas Y la de nacimiento + declive queda debajo en las 6.
**B (el ciclo):** por cohorte 2010-2022, diferencia de log-exceso (como #117, contra la mediana de su grupo año × SIC3 × decil) maduras − (nacimiento + declive). Spearman contra la mediana del mercado a 4 años. Pasa si ρ < 0 con p < 0,05 (una cola; permutación 10.000): las maduras pierden contra las jóvenes cuando el mercado sube fuerte.
**C (se sabe antes):** la misma diferencia contra la caída desde el máximo al comprar (#127). Pasa si ρ > 0 con p < 0,05 (una cola): comprando en el máximo, las maduras ganan.
**Resultado #132 (16-nov-2026): A no pasa por un empate, B y C no pasan; pero se ve qué pasa.** A: en el 10% de arriba de Gemma hay menos empresas jóvenes (nacimiento + declive) que en el resto en las 6 camadas (2017: 10 contra 11%; 2022: 25 contra 32%), y más maduras en 5 de 6 (2017 empata 51 contra 51%). El criterio pedía las dos en las 6. B: la diferencia maduras − jóvenes (log-exceso contra pares) no sigue al mercado (ρ −0,28, p 0,18). C: tampoco sigue a la caída desde el máximo (ρ +0,10). **Lo que sí aparece, fuera del criterio y sin prueba propia todavía:** las maduras le ganan a las jóvenes de su mismo rubro y tamaño en 11 de 13 cohortes, por +17 a +82 puntos de log-exceso (las dos que no: 2010 con 1 sola joven, y 2017 con −2,7). No es un ciclo: es una ventaja casi constante, y Tr la ve en parte (elige menos jóvenes). Script: entrenar/vida132.py; salida: sal-cab102/vida132.log.
Total probadas: 132 (#102, #114, #124, #127 y #130 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131 y #132 no; #111 sin muestra).

## #133: las maduras le ganan a las jóvenes, en años nunca usados (2023-2025, a 12 meses). Escrita el 16-nov-2026 ANTES de bajar los flujos de 2022-2024
**Por qué:** #132 mostró, fuera de su criterio, que las maduras le ganan a las jóvenes (nacimiento + declive) de su rubro y tamaño en 11 de 13 cohortes. Se prueba limpio en cohortes que no tienen _ret4 todavía y nunca se usaron para esto.
**Datos:** SEC XBRL frames de los tres flujos, años fiscales 2022-2024 → cohortes 2023-2025; etiquetas.csv con _ret1.
**Medida:** log-exceso a 12 meses = log(max(_ret1, 0,01)) − mediana del grupo año × SIC3 × decil de tamaño (grupos ≥ 5). Diferencia = media de maduras − media de jóvenes.
**Criterio:** pasa si la diferencia es > 0 en las 3 cohortes Y en el total con p < 0,05 (permutación de etiquetas maduras/jóvenes dentro de grupos, 2000, una cola).
**Resultado #133 (16-nov-2026): no pasa.** Log-exceso a 12 meses contra pares, maduras − jóvenes: 2023 +8,6 (632 contra 589), 2024 +9,8 (652 contra 514), 2025 −2,7 (531 contra 475). Total +5,7 (p 0,18). Pedía las 3 cohortes arriba: falló 2025. Con este método y a 12 meses, la ventaja de las maduras apareció en 2 de 3 años nuevos y no alcanzó en el total. Script: entrenar/vida133.py; salida: sal-cab102/vida133.log.
Total probadas: 133 (#102, #114, #124, #127 y #130 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128 y #131-#133 no; #111 sin muestra).

## #134: euforia y resaca de las jóvenes. Escrita el 16-nov-2026 ANTES de calcular
**Por qué:** en #133, 2025 fue el único año en que las jóvenes le ganaron a las maduras a 12 meses. Mirando nombres sueltos (empresas con caja en criptomonedas, biotecnológicas) dije «es una manía» sin probarlo: queda retirado. Lo que se puede probar con datos que ya tienen 4 años: si cuando las jóvenes ganan el primer año, pierden los tres siguientes.
**Datos:** etapas de vida130.py (años fiscales 2009-2021 → cohortes 2010-2022), etiquetas.csv (_ret1, _ret4).
**Medida por cohorte:** log-exceso contra pares (año × SIC3 × decil, grupos ≥ 5) en el año 1 = log(_ret1) y en los años 2-4 = log(_ret4) − log(_ret1) (con piso 0,01). D1 y D234 = media de jóvenes (nacimiento + declive) − media de maduras en cada tramo.
**Prueba:** Spearman entre D1 y D234 en las 13 cohortes (las que tienen al menos 20 jóvenes y 20 maduras). Permutación 10.000.
**Criterio:** ρ < 0 con p < 0,05 (una cola). Si pasa, la #133 de 2025 se lee como el primer año de ese patrón y se sella para 2025-2028; si no, 2025 queda sin explicar.
**Resultado #134 (16-nov-2026): no pasa.** 11 cohortes 2012-2022 con ≥ 20 jóvenes y ≥ 20 maduras. D1 contra D234: ρ −0,05 (p 0,45). Lo que gana o pierde la joven el primer año no anticipa los años siguientes. **Qué muestra:** en los años 2-4 las jóvenes pierden contra las maduras en 10 de 11 cohortes (de −2 a −70 puntos de log-exceso; la única que no: 2019, +5,5), y eso pasa haya ganado o perdido el primer año (D1 da 6 positivas y 5 negativas). La desventaja de las jóvenes aparece después del primer año, casi siempre. Se conecta con #133: medir a 12 meses miraba justo el tramo en que todavía no aparece; el 2025 de #133 (−2,7 para las maduras) no la contradice. Queda sin probar si las jóvenes de 2023-2025 pierden en sus años 2-4: lo dirán 2027-2029. Script: entrenar/resaca134.py; salida: sal-cab102/resaca134.log.
Total probadas: 134 (#102, #114, #124, #127 y #130 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128 y #131-#134 no; #111 sin muestra).

## #135: ¿Tr es sólo calidad? Escrita el 16-nov-2026 ANTES de bajar rentabilidad y activos
**Por qué:** dije «Tr es un detector de calidad (Asness, Frazzini y Pedersen, 2019)» sin medirlo. Se mide: (A) si el puntaje de Gemma va con la rentabilidad, y (B) si Gemma sigue esquivando hundidas cuando se la compara con empresas de la misma rentabilidad y la misma etapa de vida.
**Datos:** SEC XBRL frames NetIncomeLoss (CY{año}) y Assets (CY{año}Q4I), años fiscales 2016-2021 → cohortes 2017-2022; etapas de #130; puntaje de Gemma como rt120.py; etiquetas.csv.
**Medida:** rentabilidad = NetIncomeLoss / Assets.
**A:** Spearman entre puntaje de Gemma y rentabilidad dentro de cada cohorte. Pasa si es > 0 en las 6.
**B:** pares = año × SIC2 × terciles de tamaño × quintil de rentabilidad (dentro del año) × etapa (madura / joven / otra), grupos ≥ 5. Hundidas a 4 años del 10% de arriba de Gemma (por industria, como Rt) contra sus pares. Permutación dentro de grupos, 2000. **Pasa si** el 10% de arriba se hunde al menos 2 puntos menos que sus pares con p < 0,05 (una cola): Gemma ve algo más que calidad. Si no pasa: con este método, lo que Tr esquiva se explica por rentabilidad y etapa.
**Resultado #135 (16-nov-2026): A pasa y B PASA.** A: el puntaje de Gemma va con la rentabilidad, pero poco: ρ de +0,11 a +0,15 en las 6 cohortes. B: comparadas con empresas de la misma rentabilidad, la misma etapa, el mismo rubro (SIC2) y el mismo tercil de tamaño, las del 10% de arriba de Gemma se hundieron 11,7% contra 15,8% esperado (−4,1 pts, p 0,0055), y menos en las 6 cohortes (2017: 3,1 contra 10,9; 2022: 20,4 contra 22,4). **Qué muestra:** mi frase «Tr es un detector de calidad» era de más: la calidad contable explica una parte chica; leyendo el informe, Gemma ve algo que la rentabilidad y la etapa no ven. La diferencia se achica en 2021-2022 (−2,7 y −2,0). Límites: 589 elegidas con todos los datos; pares más gruesos que en otras pruebas (SIC2, terciles). Script: entrenar/calidad135.py; salida: sal-cab102/calidad135.log.
Total probadas: 135 (#102, #114, #124, #127, #130 y #135 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128 y #131-#134 no; #111 sin muestra).

## Pendiente de #65, hecho el 16-nov-2026: los conceptos que más pesan en Gemma (no es una prueba)
entrenar/conceptos136.py; salida sal-cab102/conceptos136.log y .json (25 a favor, 25 en contra, descripciones automáticas de Neuronpedia, capa 12 de Gemma Scope 16k). Los pesos están muy repartidos (4.382 conceptos; el más fuerte pesa 0,054). A favor pesan productos y servicios concretos (odontología y estética, anteojos, salud aplicada, máquinas, mediciones, resultados trimestrales). En contra pesan ciencia de laboratorio (compuestos bioquímicos, física de partículas), juicios y procedimientos legales, bitcoin y comercio de criptomonedas, y lenguaje de «estrategia», «liderazgo innovador» y «soluciones tecnológicas». Lectura posible, sin probar: Gemma castiga a la empresa que vende una promesa y premia a la que describe una operación.

## #136: ¿lo que ve Gemma es «promesa contra operación»? Escrita el 16-nov-2026 ANTES de contar palabras
**Datos:** sección 1 («el negocio») de los 10-K 2021 y 2022 (fuentes/sec116/sec1.jsonl, 2.858 empresas), puntaje de Gemma de esos años (como rt120.py), etiquetas.csv.
**Medida:** tasa de promesa = apariciones por 10.000 palabras de: preclinical, clinical trial, clinical trials, investigational, product candidate, product candidates, phase 1, phase 2, phase 3, bitcoin, cryptocurrency, blockchain, digital asset, digital assets, litigation, lawsuit, lawsuits, plaintiff, plaintiffs, going concern, not generated any revenue, not yet generated revenue (minúsculas, palabras enteras).
**A:** Spearman entre tasa de promesa y puntaje de Gemma, dentro de cada año. Pasa si < 0 en los dos.
**B:** el quintil de más promesa (dentro del año) se hunde a 4 años más que sus pares (año × SIC3 × decil de tamaño, grupos ≥ 5): pasa si ≥ +3 pts con p < 0,05 (permutación dentro de grupos, 2000).
**C (lo que decide):** el 10% de arriba de Gemma contra pares de año × SIC2 × tercil de tamaño × quintil de promesa. Si se hunde 2 puntos menos o más con p < 0,05: Gemma ve algo más que la promesa. Si no: con este método, buena parte de lo que ve es esto.
**Resultado #136 (16-nov-2026): A pasa (débil), B no pasa, C no pasa.** 4.297 empresas-año 2021-2022. A: promesa contra puntaje de Gemma ρ −0,04 (2021) y −0,08 (2022): negativo como pedía, pero casi nada. B: el quintil de más promesa se hundió 35,4% contra 32,5% de sus pares, +2,9 (p 0,51). C: el 10% de arriba de Gemma contra pares de igual promesa: 23,2% contra 24,6%, −1,5 (p 0,40). **Qué muestra:** la frase que escribí antes para el caso C («buena parte de lo que ve es la promesa») no se sigue de este resultado: sin igualar la promesa, el 10% de arriba de Gemma en esta muestra tampoco se hundió menos que sus pares de SIC2 y tamaño (23,7% contra 21,6%). En 2021-2022, con estos textos, Gemma no tuvo ventaja que explicar (va con #135, donde la ventaja se achicó a −2,7 y −2,0 en esos años). Esta lista de palabras casi no va con lo que ve Gemma: con este método, «promesa contra operación» no apareció. Script: entrenar/promesa136.py; salida: sal-cab102/promesa136.log.
Total probadas: 136 (#102, #114, #124, #127, #130 y #135 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134 y #136 no; #111 sin muestra).

## #137: ¿en qué parte del informe está lo que ve Gemma? Escrita el 16-nov-2026 ANTES de calcular
**Por qué:** #135 mostró que Gemma ve algo más que rentabilidad y etapa; #136 no lo encontró adivinando palabras. Antes de adivinar qué es, se ubica dónde está: el puntaje suma tres secciones (1 el negocio, 1A riesgos, 7 dirección).
**Datos:** conceptos de Gemma Scope 2017-2020 (sal-junto3/sae2aT-AAAA-L12.npz, columnas 0-16.383 = sección 1, 16.384-32.767 = 1A, 32.768-49.151 = 7), modelo congelado gemma_1_1A_7 (aprendido con 2013-2016), etiquetas.csv.
**Medida:** puntaje parcial de cada sección = la parte del puntaje que viene de sus columnas. El 10% de arriba de cada parcial por industria (como Rt) contra pares año × SIC3 × decil de tamaño (grupos ≥ 5), hundidas a 4 años; permutación dentro de grupos, 2000. Se informa también el puntaje entero.
**Criterio:** una sección «lleva» la ventaja si su 10% de arriba se hunde al menos 3 puntos menos que sus pares con p < 0,05 (una cola). Se informan las tres; si es una sola, la prueba siguiente se hace dentro de esa sección.
**Resultado #137 (16-nov-2026): lleva la ventaja «el negocio» (sección 1).** 2017-2020, 397 elegidas por parcial (control: el puntaje rearmado coincide con el guardado, correlación 1,0). Hundidas a 4 años del 10% de arriba contra pares: entero 7,1% contra 11,8% (−4,8, p 0,004; los 4 años abajo); sólo el negocio −3,1 (p 0,02); sólo riesgos −2,8 (p 0,04, no llega a −3); sólo dirección −1,1 (p 0,35). **Qué muestra:** los tres parciales casi no se correlacionan entre sí (−0,02 a −0,05), y el entero (−4,8) esquiva más que cualquiera solo: no hay una sola cosa escondida, son al menos dos lecturas independientes que se suman, cómo describe la empresa su negocio y, en menor medida, sus riesgos. Lo que dice la dirección (sección 7) aporta poco y da vuelta en 2020. La prueba siguiente va dentro del negocio. Script: entrenar/seccion137.py; salida: sal-cab102/seccion137.log.
Total probadas: 137 (#102, #114, #124, #127, #130, #135 y #137 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134 y #136 no; #111 sin muestra).

## #138: ¿lo que ve Gemma en «el negocio» es cuán concreta es la descripción? Escrita el 16-nov-2026 ANTES de bajar la tabla de concreción
**Por qué:** #137 ubicó la ventaja sobre todo en la sección 1. Los conceptos con más peso a favor son concretos (anteojos, odontología, máquinas, mediciones) y en contra, abstractos o de laboratorio («estrategia», «innovación», ciencia). #136 usó una lista de 22 palabras y en años (2021-2022) en que Gemma no tenía ventaja. Medida estándar: Brysbaert, Warriner y Kuperman (2014, Behavior Research Methods), concreción de ~40.000 palabras de 1 (abstracta) a 5 (concreta).
**Datos:** vectores de la sección 1 2017-2020 (fuentes/edgar-corpus/m1_AAAA.npz, mismo HashingVectorizer de lazy112, filas = ciks de vec_AAAA.npz); tabla de Brysbaert (github ArtsEngine/concreteness); parcial «negocio» de #137; etiquetas.csv.
**Medida:** concreción de la descripción = promedio de la concreción de sus palabras, pesado por frecuencia, sólo palabras con puntaje de una sola palabra (Bigram = 0).
**A:** Spearman entre concreción y parcial «negocio», dentro de cada año. Pasa si > 0 en los 4.
**B:** el quintil más abstracto (dentro del año) se hunde a 4 años al menos 3 puntos más que sus pares (año × SIC3 × decil), p < 0,05 (permutación dentro de grupos, 2000).
**C (lo que decide):** el 10% de arriba del parcial «negocio» contra pares de año × SIC2 × tercil × quintil de concreción. Si la ventaja (−3,1 en #137, misma comparación sin concreción) queda en −1,5 o más cerca de cero, la concreción explica buena parte; se informa la comparación sin igualar en la misma muestra.
**Resultado #138 (16-nov-2026): A pasa (débil), B no pasa, C: la ventaja sigue con igual concreción.** 10.834 descripciones 2017-2020, 37.051 palabras con puntaje. A: concreción contra parcial «negocio» ρ +0,06 a +0,09 en los 4 años (positiva, casi nada). B: el quintil más abstracto se hundió 14,7% contra 13,0% de sus pares, +1,7 (p 0,12). C: el 10% de arriba del negocio contra pares sin igualar concreción −3,7 (p 0,002); igualando concreción −3,4 (p 0,005). **Qué muestra:** la concreción casi no explica la ventaja (de −3,7 a −3,4). La lectura «concreto contra abstracto» que saqué de los conceptos con más peso no se sostiene; con este método tampoco apareció qué ve Gemma. Los conceptos sueltos con más peso no la explican: la ventaja está repartida en muchos. Script: entrenar/concreto138.py; salida: sal-cab102/concreto138.log.
Total probadas: 138 (#102, #114, #124, #127, #130, #135 y #137 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136 y #138 no; #111 sin muestra).

## #139: destilar lo que ve Gemma en palabras. Escrita el 16-nov-2026 ANTES de entrenar
**Por qué:** #136 y #138 adivinaron qué ve Gemma a partir de sus conceptos y no apareció. En vez de adivinar: un modelo de palabras que imite el parcial «negocio» de Gemma, y mirar sus palabras.
**Datos:** vectores de palabras de la sección 1 (fuentes/edgar-corpus/m1_AAAA.npz, frecuencia normalizada, HashingVectorizer 2^20) y parcial «negocio» del modelo congelado (#137), 2013-2016 para aprender, 2017-2020 para probar. Palabras para traducir columnas: lista de Brysbaert (37.051).
**Modelo:** ridge (alfa 1, sin elegir mirando 2017-2020) de log(1 + 1.000·frecuencia) sobre las columnas presentes en ≥ 2% de las descripciones de 2013-2016, contra el parcial «negocio».
**Prueba (2017-2020):** (1) correlación entre el puntaje de palabras y el parcial de Gemma; (2) el 10% de arriba del puntaje de palabras por industria contra pares año × SIC3 × decil, hundidas a 4 años, permutación 2000.
**Criterio:** pasa si (2) da −2 puntos o menos con p < 0,05: lo que Gemma ve en el negocio se puede leer en palabras. Se informan las 30 palabras con más peso a favor y en contra.
**Resultado #139 (16-nov-2026): PASA.** Aprendido con 10.583 descripciones 2013-2016, 7.094 columnas de palabras. En 2017-2020 el puntaje de palabras se parece al parcial de Gemma sólo en parte (correlación 0,31), pero su 10% de arriba se hundió 7,6% contra 11,9% de sus pares (−4,3, p 0,012; 2017 −8,4, 2018 −1,9, 2019 −3,3, 2020 −3,5), más que el parcial de Gemma solo en #137 (−3,1). **Qué muestra:** lo que esquiva hundidas en la descripción del negocio se puede leer con palabras sueltas contadas, sin un modelo de lenguaje; está repartido en miles de palabras. Las palabras con más peso no forman un tema limpio (a favor: conclusive, inspects, compromised, fcpa, surgeries, subcontract…; en contra: qui [tam], whistleblower, glp, abatement, pollutant, pulmonary, injunctive…): en un ridge con miles de palabras parecidas cada peso suelto es inestable, así que no se lee una historia de ellas sin otra prueba. Aparecen palabras de juicios del Estado y ambientales en contra (qui tam, whistleblower, injunctive, abatement, pollutant), sin probar. Script: entrenar/palabras139.py; salida: sal-cab102/palabras139.log.
Total probadas: 139 (#102, #114, #124, #127, #130, #135, #137 y #139 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136 y #138 no; #111 sin muestra).

## #140: juicios del Estado y multas ambientales en la descripción del negocio. Escrita el 16-nov-2026 ANTES de contar
**Por qué:** en #139 entre las palabras con más peso en contra aparecieron qui [tam], whistleblower, injunctive, abatement, pollutant. Las palabras salen de pesos aprendidos con 2013-2016; se prueban solas en 2017-2020 y aparte en 2021-2022.
**Lista (fija):** qui, whistleblower, whistleblowers, injunctive, abatement, pollutant, pollutants, superfund, cercla, remediation, contamination, contaminated, hazardous, subpoena, subpoenas, indictment, settlement, settlements. (Palabras sueltas; en 2017-2020 se cuentan por la columna del HashingVectorizer de m1_AAAA.npz, en 2021-2022 en el texto de sec116/sec1.jsonl.)
**Medida:** apariciones de la lista por cada mil palabras de la sección 1 (en 2017-2020, como fracción de la frecuencia normalizada; el orden dentro del año es lo que cuenta).
**Prueba:** el quintil más alto (dentro del año) contra pares año × SIC3 × decil (grupos ≥ 5), hundidas a 4 años, permutación dentro de grupos 2000.
**Criterio:** pasa si en 2017-2020 el quintil alto se hunde al menos 3 puntos más con p < 0,05 (una cola) Y en 2021-2022 la diferencia también es positiva.
**Resultado #140 (16-nov-2026): no pasa.** 2017-2020: el quintil con más palabras de juicios y multas se hundió igual que sus pares (13,3% contra 13,4%, −0,0; por año −0,5, −3,2, +5,0, −0,9). 2021-2022: +3,0 (p 0,24). **Qué muestra:** estas palabras solas no llevan la ventaja de #139; que aparezcan entre las de más peso es una de esas lecturas sueltas de un ridge que no se sostienen solas. Va con #136 y #138: ningún tema por separado explica lo que esquiva Gemma; está repartido. Script: entrenar/juicios140.py; salida: sal-cab102/juicios140.log.
Total probadas: 140 (#102, #114, #124, #127, #130, #135, #137 y #139 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136, #138 y #140 no; #111 sin muestra).

## #141: Gemma + palabras juntas, ¿esquivan más que Gemma sola? Escrita el 16-nov-2026 ANTES de combinar
**Por qué:** #139 mostró que un modelo de palabras que imita a Gemma en el negocio esquiva hundidas (−4,3) y se parece a Gemma sólo en parte (correlación 0,31). Si lo que ven no es lo mismo, juntas deberían esquivar más. Sería útil para Rt (las palabras son baratas).
**Datos:** puntaje entero de Gemma (#137) y puntaje de palabras (#139), 2017-2020, ambos aprendidos con 2013-2016.
**Combinación (fija):** promedio de los percentiles por año de los dos puntajes.
**Prueba:** el 10% de arriba por industria (como Rt) de la combinación contra el de Gemma sola, en hundidas a 4 años contra pares año × SIC3 × decil.
**Criterio:** pasa si la combinación se hunde menos que Gemma sola en al menos 3 de 4 años Y en el total la diferencia contra pares es al menos 1 punto mejor. Si pasa, se anota como candidata para Rt (que corre con Gemma en GitHub) y se escribe su prueba hacia atrás.
**Resultado #141 (16-nov-2026): no pasa.** 2017-2020, 397 elegidas por puntaje: Gemma sola 7,1% hundidas contra 11,8% esperado (−4,8); palabras solas 7,3% contra 11,3% (−4,0); juntas 6,5% contra 11,6% (−5,0). Juntas se hunden menos que Gemma sola en 1 de 4 años y mejoran el total 0,2 puntos (pedía 3 de 4 y 1 punto). **Qué muestra:** sumar las palabras no agrega: aunque los dos puntajes se parecen poco en general (0,31), en la punta esquivan las mismas hundidas. Lo que ve Gemma y lo que ven las palabras contadas es, en lo que importa, lo mismo. Y un modelo de palabras contadas, mucho más barato, llega casi a lo de Gemma (−4,0 contra −4,8). Rt sigue igual. Script: entrenar/combina141.py; salida: sal-cab102/combina141.log.
Total probadas: 141 (#102, #114, #124, #127, #130, #135, #137 y #139 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136, #138, #140 y #141 no; #111 sin muestra).

## #142: el modelo de palabras de #139 en años que Gemma nunca leyó (2010-2012). Escrita el 16-nov-2026 ANTES de calcular
**Por qué:** #139/#141 mostraron que un conteo de palabras ve lo mismo que Gemma. Como no necesita a Gemma, se puede probar hacia atrás en cohortes que nunca entraron ni al aprendizaje ni a la prueba (Gemma leyó 2013-2020).
**Datos:** el mismo modelo de #139, sin cambiar nada (aprendido con 2013-2016), aplicado a los vectores de la sección 1 de 2010, 2011 y 2012 (fuentes/edgar-corpus/m1_AAAA.npz); etiquetas.csv.
**Prueba:** el 10% de arriba por industria contra pares año × SIC3 × decil (grupos ≥ 5), hundidas a 4 años, permutación dentro de grupos 2000.
**Criterio:** pasa si se hunde al menos 3 puntos menos que sus pares con p < 0,05 (una cola) en el total 2010-2012, y menos en al menos 2 de los 3 años.
**Resultado #142 (16-nov-2026): no pasa.** Con etiqueta: 368 (2010), 979 (2011), 2.054 (2012) empresas; 127 elegidas con pares. Se hundieron 6,3% contra 9,8% de sus pares, −3,5 (p 0,08). Por año: 2010 +0,0 (8 elegidas), 2011 +5,0 (32), 2012 −7,0 (87). **Qué muestra:** la dirección es la misma que en 2017-2020 y del mismo tamaño (−3,5 contra −4,0), pero la muestra es chica: en 2010-2011 hay pocas empresas con resultado a 4 años en etiquetas.csv, y con 8 y 32 elegidas un año no dice nada. El año con muestra parecida a los otros (2012) dio −7,0. Con este método y esta muestra, no alcanza para confirmar hacia atrás; tampoco lo contradice. Script: entrenar/palabras142.py; salida: sal-cab102/palabras142.log.
Total probadas: 142 (#102, #114, #124, #127, #130, #135, #137 y #139 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136, #138 y #140-#142 no; #111 sin muestra).

## #143: el modelo de palabras de #139 en 2021-2022. Escrita el 16-nov-2026 ANTES de calcular
**Por qué:** #142 fue en la dirección esperada con muestra chica. 2021-2022 tiene miles de empresas con resultado a 4 años y el modelo de palabras nunca lo vio (aprendió con 2013-2016). Aviso: en esos años Gemma esquivó menos (#135: −2,7 y −2,0).
**Datos:** texto de la sección 1 de 2021 y 2022 (fuentes/sec116/sec1.jsonl), pasado por el mismo HashingVectorizer (2^20, palabras de 2+ letras, norma l2) que m1_AAAA; el modelo de #139 sin cambios; etiquetas.csv.
**Prueba y criterio:** como #142: el 10% de arriba por industria contra pares año × SIC3 × decil, hundidas a 4 años, permutación 2000. Pasa si se hunde al menos 3 puntos menos con p < 0,05 (una cola) en el total y menos en los 2 años.
**Resultado #143 (16-nov-2026): no pasa.** 4.491 empresas con etiqueta (2021: 2.294; 2022: 2.197), 230 elegidas con pares: se hundieron 27,4% contra 25,7%, +1,7 (p 0,72); 2021 +3,6, 2022 −0,2. **Qué muestra:** en 2021-2022 el modelo de palabras no esquivó hundidas, igual que Gemma, que en esos años se debilitó (#135: −2,7 y −2,0; #120: las elegidas de Rt se hundieron 23,8% y 21,5%). Los dos métodos funcionan en 2012-2020 y fallan juntos en 2021-2022: lo que cambió es la camada, no el método. Dos lecturas posibles, sin probar: (1) esas camadas se compraron en el máximo, después del rally de 2020, y se hundió casi todo junto (25% de hundidas esperadas contra 10-12% en 2017-2020), lo que deja poco para separar; (2) el texto de 2021-2022 sale de otra extracción (sec116, por expresión regular) que el de 2013-2020 (EDGAR-CORPUS). Script: entrenar/palabras143.py; salida: sal-cab102/palabras143.log.
Total probadas: 143 (#102, #114, #124, #127, #130, #135, #137 y #139 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136, #138 y #140-#143 no; #111 sin muestra).

## #144: ¿2021-2022 falla por la camada o por cómo saqué el texto? Escrita el 16-nov-2026 ANTES de bajar
**Por qué:** #143 dejó dos lecturas. Se separan midiendo el mismo año con las dos extracciones.
**Datos:** 10-K presentados en 2020 por las empresas de sec116 (API submissions + Archives), sección 1 sacada con el mismo código de sing116.py (`bajar`); los vectores de EDGAR-CORPUS de 2020 (m1_2020) de las mismas empresas.
**Medida:** correlación de Spearman entre el puntaje de palabras de #139 calculado con cada extracción, mismas empresas, 2020.
**Criterio:** si la correlación es ≥ 0,8, la extracción no explica la caída de 2021-2022 (queda la camada); si es < 0,5, la extracción la puede explicar y 2021-2022 se rehace con EDGAR-CORPUS u otra extracción igual. Entre 0,5 y 0,8, no decide.
**Resultado #144 (16-nov-2026): no decide (Spearman 0,66).** 2.272 empresas con las dos extracciones del 10-K de 2020. El puntaje de palabras sólo coincide en parte (0,66): mi extracción por expresión regular cambia bastante lo que lee el modelo respecto de EDGAR-CORPUS. **Qué muestra:** la extracción no es un detalle; con 0,66 no se puede atribuir la caída de 2021-2022 ni a la camada ni al método. Lo que corresponde es rehacer 2021-2022 con la misma herramienta que armó EDGAR-CORPUS (edgar-crawler, Loukas y otros 2021), validándola antes contra 2020. Script: entrenar/bajar144.py, entrenar/extraccion144.py; salida: sal-cab102/extraccion144.log.
Total probadas: 144 (… #144 no decide).

## #145: rehacer 2021-2022 con la herramienta de EDGAR-CORPUS. Escrita el 16-nov-2026 ANTES de bajar
**Por qué:** #144: mi extracción coincide sólo 0,66 con EDGAR-CORPUS. EDGAR-CORPUS se armó con edgar-crawler (Loukas y otros, 2021; github lefterisloukas/edgar-crawler, clonado en herramientas/). Se usa esa herramienta tal cual (ExtractItems, ítem 1, sin tablas) sobre el documento principal de cada 10-K.
**Paso 1, validación (2020):** puntaje de palabras de #139 con el texto de edgar-crawler contra el de EDGAR-CORPUS, mismas empresas. Si Spearman ≥ 0,85, la herramienta reproduce EDGAR-CORPUS y se sigue; si no, se anota y no se usa.
**Paso 2 (2021-2022):** la misma prueba y el mismo criterio de #143 con el texto de edgar-crawler: el 10% de arriba por industria contra pares año × SIC3 × decil, hundidas a 4 años; pasa si −3 puntos o menos con p < 0,05 y menos en los 2 años.
**Resultado #145 (16-nov-2026): NO PASA el paso 1; el paso 2 no se corre.** Con las primeras empresas bajadas (425 con texto en 2020), el puntaje de palabras sacado del texto de edgar-crawler coincide 0,70 (Spearman) con el de EDGAR-CORPUS; con el mismo filtro de 300 palabras de los dos lados (EDGAR-CORPUS trae 6% de secciones vacías y 15% de menos de 300 palabras, y el primer cálculo filtraba sólo de un lado), 0,74. Debajo de 0,85: con este método la extracción no se usa. **Qué muestra:** el problema no es la herramienta: los textos son casi los mismos (coseno de palabras: mediana 0,991, 82% sobre 0,95). Lo que se rompe es el modelo de palabras de #139: cuando el texto es idéntico (coseno > 0,999, 129 empresas) los puntajes coinciden 0,997; con 1-2% de texto distinto (coseno 0,98-0,999, 191 empresas) ya coinciden sólo 0,71; con 2-10% distinto, 0,58. El ridge de 7.094 columnas con alfa 1 amplifica diferencias chicas del texto (un párrafo de más o de menos). Esto relee #144 (mi extracción coincidía 0,66) y #143 (el modelo de palabras no apareció en 2021-2022 con mi texto): parte de esa falla puede ser la fragilidad del modelo y no la camada. Diagnóstico: entrenar/diag145.py. Scripts: entrenar/crawler145.py, entrenar/medir145.py. La bajada de 2021-2022 sigue para usarla en #146.
Total probadas: 145 (#102, #114, #124, #127, #130, #135, #137 y #139 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136, #138, #140-#143 y #145 no; #144 no decide; #111 sin muestra).

## #146: un modelo de palabras que no se desarme con un párrafo de más. Escrita el 16-nov-2026 ANTES de calcular
**Por qué:** #145: el modelo de #139 (alfa 1, 7.094 columnas) cambia mucho el puntaje con 1-2% de texto distinto. Un modelo más regularizado debería ser estable y, si lo que ve es real, conservar la señal.
**Candidatos:** ridge con alfa 1, 10, 100, 1.000 y 10.000, sobre columnas con presencia ≥ 2% o ≥ 10% (10 modelos), todos aprendidos como #139 (2013-2016 contra el parcial «negocio» de Gemma).
**Elección (sin mirar retornos):** estabilidad = Spearman entre el puntaje con texto de edgar-crawler y con texto de EDGAR-CORPUS en 2020 (empresas con ≥ 300 palabras de los dos lados, las bajadas al momento de correr). Entre los modelos con estabilidad ≥ 0,90, el de mayor correlación con el parcial de Gemma en 2017-2020. Si ninguno llega a 0,90, el más estable, y se informa.
**Prueba A (2017-2020, texto EDGAR-CORPUS):** la de #139: 10% de arriba por industria contra pares año × SIC3 × decil, hundidas a 4 años, permutación 2000. Pasa con −2 o menos y p < 0,05.
**Prueba B (2021-2022, texto edgar-crawler, cuando termine la bajada):** la de #143: pasa con −3 o menos, p < 0,05 y negativa en los 2 años. Rt no cambia salvo que pase B.
**Resultado #146 A (16-nov-2026): PASA.** Estabilidad medida en 484 empresas 2020. Ningún candidato llegó a 0,90; el más estable fue alfa 10.000 con columnas ≥ 2% (0,866; el de #139 daba 0,745), y es también uno de los que más se parece a Gemma en 2017-2020 (0,46 contra 0,31 de #139). Su 10% de arriba en 2017-2020 se hundió 3,0% contra 11,3% de sus pares (−8,3, p 0,0005; 2017 −7,8, 2018 −8,9, 2019 −8,6, 2020 −7,8): el doble que #139 (−4,3) y parejo los cuatro años. **Qué muestra:** regularizar más no borró la señal, la limpió: el modelo frágil de #139 mezclaba la señal con ruido de palabras sueltas, y al obligarlo a usar direcciones amplias del vocabulario quedan juntas tres cosas: más estable, más parecido a Gemma y mejor separando hundidas. Lo que Gemma ve en el negocio es un rasgo amplio del texto, no un puñado de palabras. Falta saber si ese rasgo amplio es algo ya conocido (largo del texto, tamaño, rubro) y si aguanta en 2021-2022 (prueba B, cuando termine la bajada). Elección: sal-cab102/eleccion146.json; salida: sal-cab102/robusto146A.log; script: entrenar/robusto146.py.
Total probadas: 146 (#102, #114, #124, #127, #130, #135, #137, #139 y #146A pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136, #138, #140-#143 y #145 no; #144 no decide; #146B pendiente; #111 sin muestra).

## #147: ¿el rasgo amplio de #146 es sólo el largo de la descripción? Escrita el 16-nov-2026 ANTES de calcular
**Por qué:** #146 A: un modelo muy regularizado se apoya en direcciones amplias del vocabulario; la más obvia es el largo del texto (más palabras = más columnas encendidas). Tamaño y rubro ya están controlados por los pares (año × SIC3 × decil).
**Prueba (2017-2020, mismo modelo elegido en #146):** se informa la correlación del puntaje con log(cantidad de palabras de la sección 1, columna l1 de EDGAR-CORPUS). Se le saca al puntaje la parte que explica el largo (regresión por año) y se repite la prueba de #146 A con el resto.
**Criterio:** si el resto da −2 o menos con p < 0,05, el rasgo no es sólo el largo. Si no, se anota que con este método el largo explica la señal.
**Resultado #147 (16-nov-2026): PASA, no es el largo.** El puntaje casi no va con el largo de la descripción (correlación −0,04). Sin la parte que explica el largo, el 10% de arriba se hundió 3,0% contra 11,2% de sus pares (−8,2, p 0,0005; 2017 −7,5, 2018 −9,5, 2019 −8,2, 2020 −7,5), igual que antes. **Qué muestra:** el rasgo amplio está en qué dice la empresa, no en cuánto escribe. El largo solo, informativo, va para el otro lado y no alcanza (+2,6, p 0,92: las descripciones más largas no esquivan hundidas). Con rubro y tamaño controlados por los pares y el largo descartado, lo que queda es contenido; falta nombrarlo. Script: entrenar/largo147.py; salida: sal-cab102/largo147.log.
Total probadas: 147 (#102, #114, #124, #127, #130, #135, #137, #139, #146A y #147 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136, #138, #140-#143 y #145 no; #144 no decide; #146B pendiente; #111 sin muestra).

**Lectura (no es prueba), 17-nov-2026: palabras del modelo firme de #146.** A favor (esquivan hundidas): backlog, tools, trademarks, beverage, food, packaging, productivity, improvements, mechanical, rent, portfolio. En contra: explore, oil, offshore, proved [reservas], nda [pedido de aprobación de droga], healthcare, pending, targeting, opportunities, detection, dependent, exclusive, currently. Se lee como «negocio que ya opera y vende» contra «promesa que depende de algo que todavía no pasó» (pozos, aprobaciones, oportunidades). Es la idea de #136, que con una lista de conceptos elegida a mano no apareció; repartida en todo el vocabulario sí aparece. Traducción de columnas por hash con el vocabulario de 800 descripciones 2020: puede haber choques. Script: entrenar/nombre148.py.

**Resultado #146 B (17-nov-2026): PASA.** Con el texto de edgar-crawler de 2.858 empresas (5.454 descripciones 2021-2022) y el modelo elegido en #146 A sin tocar, el 10% de arriba se hundió 18,0% contra 24,0% de sus pares (−6,1, p 0,022; 2021 −8,4, 2022 −4,0). **Qué muestra:** la falla de 2021-2022 de #143 (y, en parte, la de Gemma) no era sólo la camada: era un modelo frágil leyendo un texto sacado de otra forma. Con un modelo firme y el texto sacado como la base de entrenamiento, la señal aparece en la camada más difícil (una de cada cuatro se hundió) y del mismo tamaño que en 2017-2020 medida en puntos. Pendiente: Gemma con este mismo texto 2021-2022 (por el turnero de la placa), y si Rt/Tr debe pasar a usar este modelo. Salida: sal-cab102/robusto146B.log.
Total probadas: 147 (#102, #114, #124, #127, #130, #135, #137, #139, #146 (A y B) y #147 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136, #138, #140-#143 y #145 no; #144 no decide; #111 sin muestra).

## #148: el modelo firme de #146 en 2010-2012, años que Gemma nunca leyó. Escrita el 17-nov-2026 ANTES de calcular
**Por qué:** #142 (modelo frágil) fue para el mismo lado en 2010-2012 sin alcanzar (−3,5, p 0,08). El modelo firme de #146 pasó en 2017-2020 y 2021-2022; esta es la prueba hacia atrás.
**Datos y prueba:** el modelo elegido en #146 A sin cambiar nada, sobre los vectores de la sección 1 de 2010, 2011 y 2012 de EDGAR-CORPUS; misma prueba de pares y permutación que #142.
**Criterio (el de #142):** pasa con −3 puntos o menos, p < 0,05 en el total, y negativa en al menos 2 de los 3 años.
**Resultado #148 (17-nov-2026): PASA.** 139 elegidas con pares en 2010-2012: se hundieron 3,6% contra 10,4% de sus pares (−6,8, p 0,0025; 2010 +0,0 con muy pocas elegidas, 2011 −8,2, 2012 −6,8). **Qué muestra:** el mismo modelo, sin tocar, separa hundidas en tres tramos que no se usaron para elegirlo: antes (2010-2012), durante (2017-2020) y después (2021-2022), con −6 a −8 puntos en cada uno. Donde el modelo frágil de #142 no alcanzaba (−3,5, p 0,08), el firme duplica la diferencia con la misma muestra chica. Script: entrenar/atras148.py; salida: sal-cab102/atras148.log.
Total probadas: 148 (#102, #114, #124, #127, #130, #135, #137, #139, #146 (A y B), #147 y #148 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136, #138, #140-#143 y #145 no; #144 no decide; #111 sin muestra).

**En juego (18-nov-2026): Tr v5 y Rt con el mismo criterio.** A pedido de Fabri, Tr pasó al modelo firme de #146: descripción del negocio de los 10-K 2026 (edgar-crawler, 4.387 de 4.440 empresas con texto), 10% de arriba por industria, cotizadas en Nueva York o Nasdaq, sin las 3 con venta de directivos en pico (#84): 413 empresas a partes iguales, 64 en común con la lista anterior. Lista sellada: datos/tr146_cartera_2026.csv, sha256 aa7b7fc2…; la anterior (597fe03a…) queda en el historial. Rt lee igual desde la misma fecha (notas/15-rt.md, cortes nuevos en rt/cortes.json). Scripts: entrenar/crawler_tr146.py, tr146.py, poner_tr146.py, guardar146.py.

## #149: ¿las elegidas del modelo firme rinden más, además de hundirse menos? Escrita el 18-nov-2026 ANTES de calcular
**Por qué:** #146-#148 miden hundidas (r4 ≤ 0,5). Para ganarle al mercado hace falta que el rendimiento total también sea mejor, no sólo menos desastres.
**Prueba:** mismo modelo, mismas elegidas (10% de arriba por industria) y mismos pares (año × SIC3 × decil) que #146; la variable es log(r4) (rendimiento a 4 años; quiebra = r4 0 se lleva a 0,01) en vez de hundida. Permutación dentro de grupos, 2000. Se mide en 2017-2020 (texto EDGAR-CORPUS) y en 2021-2022 (texto edgar-crawler) por separado.
**Criterio:** pasa si la diferencia de log(r4) contra pares es positiva con p < 0,05 (una cola) en los dos tramos. Se informa también la mediana de r4 elegidas contra pares.
**Resultado #149 (18-nov-2026): no pasa.** 2017-2020: las elegidas rindieron ×1,34 más que sus pares en log (+0,294, p 0,0005; mediana r4 1,555 contra 1,386), positivo los 4 años. 2021-2022: +0,078 (×1,08), p 0,20, positivo los 2 años pero sin alcanzar; mediana 0,978 contra 1,026 de sus pares. **Qué muestra:** en 2021-2022 el modelo sigue esquivando hundidas (#146 B) y eso solo empuja el promedio en log para arriba, pero la empresa típica que elige no rinde más que la de sus pares: es «menos desastres», no «mejores empresas». El mismo patrón que mostró Rt con Gemma (notas/15: se hunden menos en las 6 camadas, no le gana en promedio). Lo raro: la ventaja en rendimiento baja año por año (2017 +0,49, 2018 +0,34, 2019 +0,22, 2020 +0,14, 2021 +0,14, 2022 +0,03), mientras la de hundidas se mantiene (−6 a −9). Dos lecturas sin probar: el mercado aprendió a pagar por lo que el modelo ve, o la ventaja en rendimiento depende de la fase del mercado al comprar (las camadas 2021-2022 se compraron en el máximo, #127). Script: entrenar/rinde149.py; salida: sal-cab102/rinde149.log.
Total probadas: 149 (#102, #114, #124, #127, #130, #135, #137, #139, #146 (A y B), #147 y #148 pasan; #124 no apareció en 1997-2009 (#125, #126); #127B no apareció en 1964-1996 (#128); #129 sellada; #117 pasa la parte A y no la B; #104, #107-#110, #112, #113, #115, #116, #118-#123, #125, #126, #128, #131-#134, #136, #138, #140-#143, #145 y #149 no; #144 no decide; #111 sin muestra).

## #150: ¿la ventaja en rendimiento era mayor antes (2010-2012)? Escrita el 18-nov-2026 ANTES de calcular
**Por qué:** #149: la ventaja en log(r4) baja de +0,49 (2017) a +0,03 (2022). Si el mercado aprendió a pagar por lo que ve el modelo, en 2010-2012 tiene que ser al menos tan grande como en 2017-2020.
**Prueba:** la de #149 (log r4 contra pares, permutación 2000) con el texto EDGAR-CORPUS de 2010-2012, como #148.
**Criterio:** pasa si es positiva con p < 0,05 y no menor que la de 2017-2020 (+0,294). Si es positiva pero menor, la lectura del «aprendizaje del mercado» no se sostiene con este método.
**Resultado #150 (18-nov-2026): no pasa (la ventaja existe, pero no era mayor antes).** 2010-2012: +0,180 en log r4 (×1,20, p 0,03; mediana 1,656 contra 1,544), positiva los 3 años (2010 +0,10, 2011 +0,29, 2012 +0,15), menor que 2017-2020 (+0,294). **Qué muestra:** con este método la caída de #149 no es «el mercado aprendió»: antes de 2017 la ventaja en rendimiento era más chica, no más grande. La serie completa (2010 +0,10, 2011 +0,29, 2012 +0,15, 2017 +0,49, 2018 +0,34, 2019 +0,22, 2020 +0,14, 2021 +0,14, 2022 +0,03) sube y baja; la ventaja en hundidas, en cambio, aparece en todos los tramos. Lo firme del modelo es esquivar desastres; cuánto rinde además cambia de camada en camada, y falta saber de qué depende. Script: entrenar/antes150.py; salida: sal-cab102/antes150.log.
Total probadas: 150 (… #149 y #150 no; resto igual que arriba).

## #151: ¿el rendimiento extra del modelo firme depende de la fase del mercado al comprar? Escrita el 18-nov-2026 ANTES de calcular
**Por qué:** #149-#150: esquivar hundidas es parejo, pero el rendimiento extra cambia por camada (2010 +0,10 … 2017 +0,49 … 2022 +0,03). #127: comprar con el S&P lejos de su máximo rinde más a 4 años.
**Datos:** las 9 ventajas por camada ya medidas (log r4 contra pares, #149 y #150). Fase: caída del S&P 500 desde su máximo en marzo de cada año (Shiller mensual, fuentes/sp500_shiller.csv; la mayoría de los 10-K sale en febrero-marzo).
**Criterio:** pasa si la correlación de Spearman entre ventaja y caída desde el máximo es ≥ +0,6 con p < 0,05 (más ventaja cuanto más lejos del máximo). Se informa además, sin criterio, la correlación con el rendimiento del mercado en los 4 años de cada camada.
**Resultado #151 (18-nov-2026): no pasa.** Spearman entre la ventaja de cada camada y la caída del S&P desde su máximo en marzo: −0,42 (p 0,26), del signo contrario al esperado. Informativo: contra el rendimiento del mercado en los 4 años, +0,28 (p 0,46). **Qué muestra:** con 9 camadas, el rendimiento extra no sigue a lo barato del mercado al comprar: la camada con más ventaja (2017, +0,49) se compró en el máximo y la de 2010, con el S&P 25% abajo, tuvo poca (+0,10). Tampoco sigue claramente a si el mercado subió mucho o poco después. #127 (la caída predice el mercado entero) y la ventaja del modelo dentro de la industria parecen cosas separadas. Queda abierto de qué depende; con 9 camadas, cualquier explicación por año tiene poca muestra. Script: entrenar/fase151.py; salida: sal-cab102/fase151.log.
Total probadas: 151 (… #149-#151 no; resto igual que arriba).
**Relectura de #151 (18-nov-2026):** el criterio miró la fase del mercado y no vio lo que estaba en la tabla: desde 2017 la ventaja en rendimiento baja todos los años (2017 +0,49, 2018 +0,34, 2019 +0,22, 2020 +0,14, 2021 +0,14, 2022 +0,03), y el modelo aprendió con descripciones de 2013-2016. Cuanto más lejos del aprendizaje, menos rinde de más: el modelo envejece porque cambia cómo las empresas describen su negocio (o qué paga el mercado de eso).

## #152: el modelo firme reaprendido con años más nuevos. Escrita el 18-nov-2026 ANTES de calcular
**Por qué:** la relectura de #151: si la ventaja cae con la distancia a los años de aprendizaje, reaprender más cerca debería recuperarla.
**Modelo:** igual que #146 (ridge alfa 10.000, columnas presentes en ≥ 2% de las descripciones de aprendizaje, contra el parcial «negocio» de Gemma), pero aprendido con 2017-2020 en vez de 2013-2016. Sin mirar retornos.
**Prueba (2021-2022, texto edgar-crawler):** (A) hundidas contra pares, como #146 B; (B) log r4 contra pares, como #149.
**Criterio:** pasa si (B) da positivo con p < 0,05 y mayor que el del modelo 2013-2016 en los mismos años (+0,078), y (A) sigue pasando el criterio de #146 B (−3 o menos, p < 0,05, negativa en los 2 años).
**Resultado #152 (18-nov-2026): no pasa por el rendimiento promedio.** Aprendido con 10.834 descripciones 2017-2020 (7.227 columnas). En 2021-2022: (A) hundidas 18,7% contra 23,5% de sus pares (−4,8, p 0,043; 2021 −2,7, 2022 −6,7): sigue pasando; (B) log r4 +0,081 (×1,085, p 0,15), casi igual que el modelo viejo (+0,078). **Qué muestra:** el promedio no cambió, pero cambió la empresa típica: con el modelo nuevo la mediana de las elegidas rinde 1,103 contra 1,022 de sus pares (con el viejo, 0,978 contra 1,026); 2022 mejora (+0,026 → +0,097) y 2021 empeora (+0,137 → +0,064). El envejecimiento explica sólo una parte con este método. Lo que no se reaprendió es lo de fondo: el modelo de palabras imita al de Gemma, y el de Gemma eligió sus pesos con lo que pasó a las empresas de 2013-2016. Reaprender las palabras sin reaprender eso cambia el vocabulario pero no el criterio. Script: entrenar/nuevo152.py; salida: sal-cab102/nuevo152.log.
Total probadas: 152 (… #149-#152 no; resto igual que arriba).

## #153: palabras que aprenden directo del resultado, con camadas más nuevas. Escrita el 18-nov-2026 ANTES de calcular
**Por qué:** #152: reaprender el vocabulario no cambia el criterio, que sigue siendo el de Gemma (pesos elegidos con lo que pasó en 2013-2016). Acá el criterio se aprende del resultado mismo, con las camadas más nuevas que ya tienen 4 años cumplidos.
**Modelo:** mismas columnas y transformación que #146 (presentes en ≥ 2% de las descripciones de aprendizaje), ridge alfa 10.000, con objetivo = log(r4) (quiebra 0,01) menos el promedio de sus pares (año × SIC3 × decil, grupos ≥ 5): aprende qué separa a una empresa de sus pares, no la industria ni el año. Aprende con las camadas 2013-2017 (el resultado de 2017 se completa en 2021).
**Prueba:** 2022 decide (su resultado no se superpone con el aprendizaje); 2021 se informa aparte. Texto edgar-crawler. (A) hundidas contra pares; (B) log r4 contra pares, como #146 B y #149.
**Criterio:** pasa si en 2022 (B) da positivo con p < 0,05 y (A) da −3 o menos con p < 0,05.
**Resultado #153 (18-nov-2026): no pasa.** Aprendido con 4.434 empresas-año 2013-2017 (las que tienen resultado y pares), 6.935 columnas. 2022: hundidas −2,1 (p 0,38); log r4 +0,201 (×1,22, p 0,11; mediana 1,052 contra 1,101). 2021 (aparte): hundidas −1,0 (p 0,28); log r4 +0,074 (p 0,26). **Qué muestra:** aprender directo del resultado da en 2022 el rendimiento promedio más alto de los tres modelos (+0,20 contra +0,03 del original y +0,10 del reaprendido), pero pierde lo firme: casi no esquiva hundidas y la empresa típica rinde menos que sus pares (la ventaja viene de pocas que suben mucho). Imitar a Gemma es lo que le da al modelo su parte robusta (esquivar desastres); el resultado crudo es ruidoso y con 4.434 ejemplos aprende poco. Lo que mejora el rendimiento y lo que esquiva desastres parecen dos cosas distintas en el texto. Script: entrenar/directo153.py; salida: sal-cab102/directo153.log.
Total probadas: 153 (… #149-#153 no; resto igual que arriba).

## #154: el criterio de Gemma reaprendido con una camada más nueva. Escrita el 18-nov-2026 ANTES de calcular
**Por qué:** #152-#153: lo firme sale de imitar a Gemma, y el rendimiento extra se gasta con la distancia al aprendizaje. El propio modelo de Gemma ya mostraba ese desgaste (sal-junto3/out/gemma_1_1A_7_resultado.json: arriba contra abajo 2017 +1,13, 2018 +0,53, 2019 +0,31, 2020 −0,01). Se reaprende el criterio de Gemma con la misma receta, sumando la camada 2017.
**Modelo Gemma nuevo:** la receta de colab-sae/sae_analisis2.py sin cambios (rasgos de Gemma Scope de las tres secciones, columnas presentes en ≥ 2%, log1p/mediana, estandarizado, objetivo = log r4 menos la mediana de pares año × SIC3 × tercio de tamaño, recortado a ±3), alfa 1.000 fijo (el elegido entonces), aprendido con 2013-2017 en vez de 2013-2016.
**Modelo de palabras nuevo:** como #146 (alfa 10.000, columnas ≥ 2% de 2013-2016) pero imitando el parcial «negocio» del Gemma nuevo.
**Prueba (2022, que no se superpone con el aprendizaje):** palabras nuevas sobre el texto edgar-crawler: (A) hundidas contra pares; (B) log r4 contra pares. Se informa también Gemma nuevo directo (rasgos 2022 ya calculados), con las mismas dos medidas.
**Criterio (decide el de palabras, que es lo que usa Tr):** pasa si en 2022 (B) da positivo con p < 0,05 y (A) −3 o menos con p < 0,05.
**Resultado #154 (18-nov-2026): no pasa lo que decidía (las palabras); el Gemma reaprendido sí muestra lo buscado.** Gemma nuevo aprendido con 6.250 empresas-año 2013-2017 (4.395 columnas). Palabras que imitan su parcial «negocio», en 2022: hundidas −3,8 (p 0,14), log r4 −0,039 (p 0,66): no pasa. Informativo, en 2022 con los mismos rasgos y las mismas medidas: **Gemma viejo** (2013-2016) hundidas −0,3 (p 0,43), log r4 +0,095 (p 0,25), mediana 1,059 contra 1,079 de sus pares; **Gemma nuevo** (2013-2017) hundidas −6,1 (p 0,08), log r4 +0,233 (×1,26, p 0,047), mediana 1,101 contra 1,011. **Qué muestra:** el desgaste es del criterio y se arregla reaprendiéndolo: con una sola camada más, Gemma vuelve a separar en 2022, en hundidas y en rendimiento, y la empresa típica que elige le gana a la de sus pares. Lo que el modelo de palabras no copia es esa parte nueva: el parcial «negocio» solo no la lleva (puede estar en riesgos o en la explicación de la dirección, que las palabras no leen). Es una sola camada y un p justo; la prueba que decide es reaprender cada año (#155). Scripts: entrenar/gemma154.py, viejo154.py; salida: sal-cab102/gemma154.log, viejo154.log.

## #155: Gemma reaprendido cada año (como lo haría Tr). Escrita el 18-nov-2026 ANTES de calcular
**Por qué:** #154: sumar una camada devuelve la señal en 2022. Si Tr reaprende cada año con las camadas que ya cumplieron 4 años, ¿funciona en todos los años a prueba?
**Modelo:** la receta de #154 (sae_analisis2.py, alfa 1.000), aprendida con 2013 hasta y−5 para probar el año y (el resultado de y−5 se completa antes de que se presente el 10-K de y): 2021 con 2013-2016 (es el modelo viejo), 2022 con 2013-2017. Además, para tener más años a prueba con la misma regla: 2018 con 2013 (sólo un año; se informa aparte), 2019 con 2013-2014, 2020 con 2013-2015.
**Prueba:** rasgos de Gemma de cada año (2018-2020: sal-junto3; 2021-2022: sal-anon2124 y sal-lee). Hundidas y log r4 contra pares (año × SIC3 × decil, como #146 y #149), el 10% de arriba por industria.
**Criterio:** con 2019-2022 juntos, pasa si log r4 da positivo con p < 0,05 y hundidas −3 o menos con p < 0,05, y log r4 positivo en al menos 3 de los 4 años.
**Resultado #155 (18-nov-2026): PASA.** Reaprendido cada año con 2013..y−5 (de 1.232 empresas-año para 2018 a 6.250 para 2022). 2019-2022 juntos: hundidas 15,1% contra 18,5% de sus pares (−3,4, p 0,031; 2019 −3,4, 2020 −3,4, 2021 −0,7, 2022 −6,1); log r4 +0,106 (×1,11, p 0,040; 2019 +0,13, 2020 +0,10, 2021 −0,04, 2022 +0,23): positivo en 3 de 4 años. 2018 aparte (aprendido con un solo año): hundidas −1,4, log r4 +0,12, sin alcanzar. **Qué muestra:** el criterio de Gemma se gasta, y reaprenderlo cada año con lo que ya se sabe lo mantiene: rinde más y se hunde menos en cuatro camadas seguidas, incluida 2022, donde el modelo fijo ya no separaba. El año flojo es 2021, el único que usa el mismo modelo que antes (2013-2016) y la camada comprada en el máximo. Comparado con el modelo de palabras firme (#146 B, #149): las palabras esquivan más hundidas en 2021-2022 (−6,1) pero no rinden más (×1,08 sin alcanzar); Gemma reaprendido rinde más (×1,11) y esquiva menos. Script: entrenar/cadaanio155.py; salida: sal-cab102/cadaanio155.log.
Total probadas: 155 (#102, #114, #124, #127, #130, #135, #137, #139, #146 (A y B), #147, #148 y #155 pasan; … #149-#154 no; resto igual que arriba).

## #156: las dos señales juntas (palabras firmes + Gemma reaprendido cada año). Escrita el 19-nov-2026 ANTES de calcular
**Por qué:** #146-#149: las palabras firmes esquivan hundidas pero no rinden más en 2021-2022; #155: Gemma reaprendido rinde más y esquiva menos. Si son dos señales distintas, juntas deberían hacer las dos cosas.
**Puntaje:** promedio del percentil dentro de su industria (mismo grupo g que la elección: SIC3 con ≥ 10, si no SIC2) de las dos: palabras firmes de #146 (texto EDGAR-CORPUS en 2019-2020, edgar-crawler en 2021-2022) y Gemma reaprendido de #155 (2013..y−5). Sólo empresas con los dos puntajes. Elegidas: 10% de arriba de ese promedio por industria.
**Prueba (2019-2022 juntos):** hundidas y log r4 contra pares año × SIC3 × decil, permutación 2000. Se informan aparte las dos señales solas sobre las mismas empresas.
**Criterio:** pasa si hundidas −4 o menos con p < 0,05, log r4 positivo con p < 0,05, y log r4 positivo en al menos 3 de los 4 años.
**Resultado #156 (19-nov-2026): no pasa, por poco en hundidas.** 9.675 empresas-año con las dos señales. Juntas: hundidas 13,7% contra 17,5% (−3,8, p 0,041; pedía −4); log r4 +0,141 (×1,15, p 0,012), positivo los 4 años (2019 +0,26, 2020 +0,10, 2021 +0,07, 2022 +0,15). Sobre las mismas empresas: Gemma reaprendido solo, hundidas −3,4 (p 0,035) y ×1,12 (p 0,043); palabras solas, hundidas −6,5 (p 0,0025; negativa los 4 años) y ×1,11 (p 0,064). **Qué muestra:** juntar suma rendimiento (el más alto de los tres y el único positivo en los 4 años, incluido 2021) pero diluye lo de esquivar hundidas: el promedio de percentiles deja entrar empresas que sólo una de las dos señales ve bien. Y algo que no se veía: medidas sobre las mismas empresas 2019-2022, las palabras solas rinden casi lo mismo que Gemma reaprendido (×1,11 contra ×1,12) y esquivan el doble de hundidas; la ventaja de Gemma reaprendido se concentra en 2022. Con este método, Tr v5 (palabras) es la que mejor equilibra; juntar las dos es la que más rinde. Script: entrenar/juntas156.py; salida: sal-cab102/juntas156.log.
Total probadas: 156 (… #149-#154 y #156 no; #155 pasa; resto igual que arriba).

## #157: las dos señales en fila (filtro de palabras, después Gemma). Escrita el 19-nov-2026 ANTES de calcular
**Por qué:** #156: promediar diluye lo de esquivar hundidas. En fila, las palabras sacan los desastres y Gemma reaprendido elige entre lo que queda.
**Elección:** dentro de cada industria (grupo g), las del 20% de arriba en palabras firmes; de ésas, la mitad de arriba en Gemma reaprendido (≈ 10% de la industria). Mismos datos y empresas que #156.
**Prueba y criterio:** los de #156 (2019-2022: hundidas −4 o menos con p < 0,05, log r4 positivo con p < 0,05, positivo en al menos 3 de 4 años).
**Resultado #157 (19-nov-2026): PASA.** 387 elegidas en 2019-2022: hundidas 12,1% contra 17,7% de sus pares (−5,6, p 0,0025; 2019 −8,0, 2020 −5,6, 2021 −0,8, 2022 −8,0); log r4 +0,158 (×1,17, p 0,006; 2019 +0,18 p 0,04, 2020 +0,21 p 0,05, 2021 −0,02, 2022 +0,26 p 0,035): positivo en 3 de 4. **Qué muestra:** en fila no se diluye: las palabras sacan los desastres y Gemma reaprendido elige las que además rinden. Es lo mejor medido sobre estas empresas en las dos cosas a la vez (palabras solas −6,5 y ×1,11; Gemma solo −3,4 y ×1,12; promedio −3,8 y ×1,15). El año que no da es 2021 otra vez: la camada comprada en el máximo, y la única en que Gemma «reaprendido» es el mismo modelo de 2013-2016. Script: entrenar/fila157.py; salida: sal-cab102/fila157.log.
Total probadas: 157 (#102, #114, #124, #127, #130, #135, #137, #139, #146 (A y B), #147, #148, #155 y #157 pasan; … #149-#154 y #156 no; resto igual que arriba).

## #158: ¿2021 falla por el modelo o por la camada? Reaprender con la camada que cumple 4 años justo al comprar. Escrita el 19-nov-2026 ANTES de calcular
**Por qué:** en #155 y #157 el año que no da es 2021, el único en que Gemma «reaprendido» (2013..y−5) es el mismo modelo viejo de 2013-2016, y además la camada comprada en el máximo. Tr compra en noviembre: para entonces la camada y−4 (presentada casi toda en el primer trimestre de y−4) ya cumplió sus 4 años. Si 2021 mejora al reaprender con 2013..y−4, era el modelo; si no, era la camada.
**Modelo:** la receta de #155 sin cambios, aprendida con 2013..y−4 (2019: 2013-2015; 2020: 2013-2016; 2021: 2013-2017; 2022: 2013-2018). Aviso: las etiquetas no tienen fecha de presentación, así que para las que presentan tarde la ventana de 4 años de la camada y−4 puede terminar unas semanas después de que se presenta el 10-K de y (no es dato futuro de la empresa elegida, sí de otras).
**Prueba:** (A) en fila como #157 (palabras firmes 20% de arriba por industria, después la mitad de arriba en Gemma y−4), mismas empresas; (B) Gemma y−4 solo. Hundidas y log r4 contra pares, 2019-2022.
**Criterio:** pasa si (A) da hundidas −4 o menos con p < 0,05, log r4 positivo con p < 0,05, positivo en al menos 3 de 4 años, y log r4 de 2021 positivo. Se informa 2021 aparte en las dos.
**Resultado #158 (19-nov-2026): PASA.** En fila con Gemma reaprendido hasta y−4: 391 elegidas 2019-2022, hundidas 11,8% contra 17,8% de sus pares (−6,0, p 0,0025; 2019 −9,6, 2020 −5,3, 2021 −3,9, 2022 −5,5); log r4 +0,197 (×1,22, p 0,001), positivo los 4 años (2019 +0,30, 2020 +0,22, 2021 +0,08, 2022 +0,21). Gemma y−4 solo, en cambio: hundidas −1,3 (p 0,20), log r4 +0,007 (p 0,46); en 2021 −0,18 (eligió peor que sus pares), en 2022 +0,19. **Qué muestra:** dos cosas que van en contra. Solo, Gemma aprendido con la camada más fresca empeora (×1,01 contra ×1,12 con y−5), y en 2021 se da vuelta: la camada 2017 cerró sus 4 años en 2021, en el máximo, así que le enseñó «lo que ganó hasta el máximo», justo lo que después cayó. Era la camada, no el modelo. Pero detrás del filtro de palabras ese mismo Gemma suma: es lo mejor medido hasta ahora (−6,0 y ×1,22, los cuatro años positivos, 2021 incluido). Las palabras sacan las empresas de moda que se hunden, y lo que queda Gemma lo ordena bien aunque haya aprendido del máximo. Con este método, la versión en fila es la que mejor resiste una camada mala; sigue sin poder usarse en Tr porque reaprender cada año necesita las etiquetas de 4 años, que hoy se arman en esta computadora. Script: entrenar/menos4_158.py; salida: entrenar/sal-cab102/menos4_158.log.
Total probadas: 158 (#102, #114, #124, #127, #130, #135, #137, #139, #146 (A y B), #147, #148, #155, #157 y #158 pasan; … #149-#154 y #156 no; resto igual que arriba).

## #159: la amenaza de los competidores («fluidez», Hoberg, Phillips y Prabhala 2014). Escrita el 19-nov-2026 ANTES de calcular
**Por qué:** todo lo probado hasta ahora mira el informe de la empresa sola. Hoberg, Phillips y Prabhala (Journal of Finance 2014, «Product Market Threats, Payouts, and Financial Flexibility») miden cuánto se mueve el vocabulario de todo el mercado hacia las palabras con que una empresa describe sus productos: si los demás empiezan a hablar de lo que ella vende, la están amenazando. Nunca lo probamos.
**Medida:** para cada año t, palabras de la descripción del negocio en binario (usa / no usa), sólo palabras que usan entre 0,5% y 25% de las empresas ese año (el 25% como en el paper, para sacar las comunes). V_t = fracción de empresas que usa cada palabra; D_t = |V_t − V_{t−1}|. Fluidez de la empresa = coseno entre sus palabras y D_t. 2010-2020 con EDGAR-CORPUS (t−1 del mismo origen); 2021-2022 con edgar-crawler (crawler145: 2020-2022, mismo origen para t y t−1). Descripciones de 300 palabras o más.
**Elegidas:** el 10% de MENOR fluidez de cada industria (las menos amenazadas).
**Prueba:** hundidas y log r4 contra pares año × SIC3 × decil, como #146 y #149, permutación 2000.
**Criterio:** pasa si en 2010-2020 juntas da hundidas −3 o menos con p < 0,05 y log r4 positivo con p < 0,05, y en 2021-2022 las dos van para el mismo lado (sin exigir p). Se informa también el 10% de MAYOR fluidez.
**Resultado #159 (19-nov-2026): no pasa.** Fluidez calculada para 5.600-8.000 empresas por año en 2010-2020 y 2.700 en 2021-2022 (871 elegidas con etiqueta en 2010-2020). Menor fluidez, 2010-2020: hundidas 12,2% contra 11,5% (+0,7, p 0,74), log r4 −0,063 (×0,94, p 0,92), negativo en 8 de 11 años. 2021-2022: hundidas −4,4 (p 0,15), log r4 +0,131 (p 0,12), todo en 2022. Mayor fluidez, 2010-2020: hundidas −0,8 (p 0,27), log r4 +0,051 (×1,05, p 0,14). **Qué muestra:** con este método, la amenaza de los competidores no separa, y si algo, al revés de lo que suponía: las menos amenazadas rinden un poco menos que sus pares casi todos los años, y las más amenazadas un poco más. Encaja con lo que el propio paper advierte: el vocabulario se mueve hacia donde hay mercados que crecen, así que «amenaza» y «oportunidad» vienen juntas, y lo quieto es también lo estancado. 2021-2022 va para el otro lado y sólo por 2022, con otra extracción de texto y la mitad de empresas. Lo que Tr ve (#137-#139) no es la competencia: es cómo se describe la propia empresa. Script: entrenar/fluidez159.py; salida: entrenar/sal-cab102/fluidez159.log.
Total probadas: 159 (#102, #114, #124, #127, #130, #135, #137, #139, #146 (A y B), #147, #148, #155, #157 y #158 pasan; … #149-#154, #156 y #159 no; resto igual que arriba).

## #160: depender de pocos clientes. Escrita el 19-nov-2026 ANTES de bajar
**Por qué:** las normas contables (ASC 280) obligan a decir qué clientes pesan 10% o más de las ventas, y muchas empresas lo escriben en la descripción del negocio. Nunca lo miramos. La literatura va para los dos lados: más riesgo y costo de capital (Dhaliwal y otros, 2016) o más eficiencia (Patatoukas, 2012). Mi apuesta: depender de pocos clientes hace a la empresa frágil (perder uno es perder el negocio).
**Medida:** en la sección 1 (EDGAR-CORPUS 2010-2020, bajado de nuevo sin guardar el texto; edgar-crawler 2021-2022), oraciones que nombran a un cliente («customer», «client», «distributor», «accounted for») y un porcentaje «NN% of … revenue/sales». Concentración = el porcentaje más alto de esas oraciones, entre 10 y 100 (0 si no hay). Descripciones de 300 palabras o más.
**Elegidas:** el 10% de mayor concentración de cada industria (se informa cuántas tienen concentración > 0).
**Prueba:** hundidas y log r4 contra pares año × SIC3 × decil, permutación 2000.
**Criterio:** pasa si en 2010-2020 las concentradas se hunden 3 puntos o más que sus pares con p < 0,05 y log r4 negativo con p < 0,05, y en 2021-2022 las dos van para el mismo lado (sin exigir p). Si sale al revés (concentradas mejor), no pasa y se informa.
**Resultado #160 (19-nov-2026): no pasa.** Uno de cada cuatro informes nombra un cliente de 10% o más (25-27% por año en 2010-2019; 37% en 2021-2022 con edgar-crawler, que deja más texto de la sección). 823 elegidas con etiqueta en 2010-2020: hundidas 13,5% contra 12,3% (+1,2, p 0,20 de hundirse más), log r4 −0,098 (×0,91, p 0,03 de rendir menos), negativo en 8 de 11 años. 2021-2022: hundidas −0,3, log r4 −0,004: nada. **Qué muestra:** depender de pocos clientes no lleva al desastre que suponía (perder el cliente grande no hunde más a menudo), pero en 2010-2020 cuesta rendimiento de forma pareja: casi 10% menos a 4 años contra sus pares, año tras año. Encaja con el poder de negociación del cliente grande (aprieta precios y se queda con la ganancia) más que con la fragilidad. En 2021-2022 no aparece, con otra extracción que encuentra clientes en muchas más empresas, así que no está confirmado. Script: entrenar/clientes160.py, clientes160_medir.py; salida: entrenar/sal-cab102/clientes160.log.
Total probadas: 160 (#102, #114, #124, #127, #130, #135, #137, #139, #146 (A y B), #147, #148, #155, #157 y #158 pasan; … #149-#154, #156, #159 y #160 no; resto igual que arriba).

## #161: ¿Tr elige empresas atadas a un cliente grande, y le cuestan? Escrita el 19-nov-2026 ANTES de calcular
**Por qué:** #160 no hunde pero cuesta rendimiento parejo (×0,91 en 2010-2020): el cliente grande se queda con la ganancia. Si dentro de las elegidas de Tr pasa lo mismo, sacarlas mejora a Tr sin tocar su modelo.
**Elegidas de Tr:** modelo firme de palabras #146 (palabras146.npz), el 10% de arriba por industria (g), 2010-2020 sobre EDGAR-CORPUS y 2021-2022 sobre edgar-crawler, como en #148 y #149.
**Medida:** concentración de #160 (cliente de 10% o más nombrado en la sección 1).
**Prueba:** entre las elegidas de Tr, log r4 contra pares (año × SIC3 × decil) de las que tienen cliente grande menos el de las que no; permutación 2000 de la marca de cliente dentro de las elegidas de cada año. Se informa Tr entero y Tr sin las atadas (log r4 y hundidas contra pares).
**Criterio:** pasa si en 2010-2020 las atadas rinden menos que las otras elegidas con p < 0,05, y en 2021-2022 la diferencia va para el mismo lado (sin exigir p).
**Resultado #161 (19-nov-2026): no pasa, y al revés de lo que suponía.** Elegidas de Tr 2010-2020 con etiqueta: 866; atadas a un cliente grande: 383 (44%, contra 25% en todas las empresas). Contra sus pares, las atadas elegidas rinden +0,429 en log r4 y las otras +0,332 (dif +0,097, p 0,83 de que rindan menos); hundidas −9,6 y −9,8. Tr entero ×1,46, Tr sin atadas ×1,39 (2010-2020 incluye 2013-2016, años con que se aprendió el criterio de Gemma que las palabras imitan). 2021-2022: 245 elegidas, 33% atadas; atadas +0,037, otras +0,099 (dif −0,061, p 0,31); hundidas −7,7 y −5,3; Tr sin atadas ×1,10 contra ×1,08 entero. **Qué muestra:** Tr elige atadas casi el doble de lo normal, y las atadas que elige no pagan el costo de #160: rinden igual o más que las otras elegidas. El cliente grande cuesta en las empresas que Tr NO elige. La pista: lo que Tr lee como buena descripción (concreta, que dice qué vende y a quién, #138) incluye nombrar al cliente; entre las atadas, las que lo cuentan así son las que salen bien. Sacar a las atadas no mejora a Tr en 2010-2020; en 2021-2022 mejora apenas, sin alcanzar. Script: entrenar/atadas161.py; salida: entrenar/sal-cab102/atadas161.log.
Total probadas: 161 (… #149-#154, #156, #159, #160 y #161 no; resto igual que arriba).

## #162: ¿el cliente grande cuesta sólo cuando la empresa se describe mal? Escrita el 25-nov-2026 ANTES de calcular
**Por qué:** #160: depender de un cliente grande cuesta rendimiento (×0,91). #161: entre las elegidas de Tr no cuesta nada. Si el mecanismo es «cliente grande + descripción vaga = el cliente se queda con la ganancia», el costo tiene que estar en la mitad de abajo del puntaje de Tr y no en la de arriba.
**Datos:** los de #161 (puntaje de palabras #146 y concentración #160, 2010-2022), todas las empresas con etiqueta.
**Prueba:** en cada año e industria (g), mitad de abajo y mitad de arriba del puntaje de Tr. En cada mitad: log r4 contra pares (año × SIC3 × decil, media de las no atadas del grupo) de atadas menos no atadas; permutación 2000 de la marca de cliente dentro de cada año y mitad.
**Criterio:** pasa si en 2010-2020, en la mitad de abajo, las atadas rinden menos con p < 0,05 y esa diferencia es más negativa que la de la mitad de arriba; en 2021-2022 la de abajo va para el mismo lado (sin exigir p).
**Resultado #162 (25-nov-2026): no pasa, por 2021-2022.** 2010-2020: en la mitad de abajo del puntaje de Tr, las atadas rinden ×0,91 que las no atadas (−0,098, p 0,026; negativo en 8 de 11 años); en la mitad de arriba ×1,05 (+0,049). 2021-2022: abajo ×1,14 (+0,129, sobre todo 2021), arriba ×1,08. **Qué muestra:** en 2010-2020 el mecanismo aparece tal cual: el cliente grande cuesta sólo cuando la empresa se describe vago; descripta concreta, no cuesta y hasta suma. En 2021-2022 se da vuelta, y otra vez por 2021, la camada comprada en el máximo (como en #155, #157, #159): en esa camada las atadas a un cliente grande (proveedores, fabricantes por encargo) rindieron mejor que las otras, quizá porque el apuro de abastecimiento de 2021-2022 les dio poder a los proveedores. Con este método, la regla vale en tiempos normales y se rompe en 2021. Script: entrenar/vaga162.py; salida: entrenar/sal-cab102/vaga162.log.
Total probadas: 162 (… #149-#154, #156 y #159-#162 no; resto igual que arriba).
