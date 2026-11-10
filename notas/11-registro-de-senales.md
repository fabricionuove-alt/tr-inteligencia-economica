# Registro de señales probadas (para no confundir suerte con hallazgo)

Cada señal se anota ANTES de mirar. Con muchas señales, alguna sale bien por azar: este registro lleva la cuenta.

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
