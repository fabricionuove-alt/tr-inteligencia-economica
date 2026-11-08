# Resultados del primer entrenamiento (2-nov-2026)

## Qué se hizo
- Datos: balances de la SEC (companyfacts + submissions, bajados nov-2026). 80.587 filas empresa-año de 10.505 empresas operativas, 2009-2026, incluidas las quebradas (5.496 filas) y las compradas.
- Anonimización: id con hash, sin nombre, sin ticker, sin fecha, sin montos. Sector sólo con 1 dígito. Todo pasado a percentil dentro de su año; empates y faltantes desarmados al azar.
- Cada dato sale del PRIMER 10-K que lo presentó (sin cifras corregidas después).
- Etiquetas (sin precios):
  - **sobrevive_10**: sin quiebra en 10 años y sigue presentando 10-K. Salir de la quiebra cuenta como muerte. Compradas: sin etiqueta.
  - **sobrevive_10_amplio**: además, dejar de presentar sin explicación cuenta como muerte.
  - **duplica_6**: patrimonio por acción + dividendos por acción cobrados, ×2 en 6 años.
- Partición: entrena 2012-2013, prueba 2015 (supervivencia) o 2019 (duplica, con hueco limpio: lo que aprende termina en 2019). La prueba se miró una vez por versión.
- Modelo: HistGradientBoosting (scikit-learn 1.9.1), en Kaggle (fabri9/ie-datos-a, ie-datos-b, ie-analisis). Cada corrida < 3 min.
- Reglas de los cinco escritas ANTES de ver resultados (entrenar/reglas_de_los_cinco.py) y no tocadas.

## Prueba de fuga (¿se adivina el año?)
| Rasgos | Acierta el año | Azar |
|---|---|---|
| ratios crudos | 25% | 9% |
| percentiles, primera versión | 42% | 9% |
| percentiles sin huellas (final) | 16% | 9% |
| sólo señales sí/no + sector | 10% | 9% |
Lo que queda está en la combinación de ratios (la huella real de la economía de cada año). Error medio 3,1 años ≈ adivinar el año del medio. Como el modelo no leyó nada de afuera, esa huella no le hace "recordar" nada. Para un modelo de lenguaje sí importaría.

## Resultados (AUC con intervalo 90% remuestreando empresas; 0,5 = azar)
| Etiqueta (tasa base) | Regla tonta: tamaño | Reglas de los cinco | Modelo |
|---|---|---|---|
| sobrevive_10 (86%) | 0,61 | 0,70 [0,68-0,72] | 0,81 [0,79-0,83] |
| sobrevive_10_amplio (62%) | 0,78 | 0,72 [0,70-0,73] | 0,84 [0,83-0,86] |
| duplica_6 (32%) | 0,46 | 0,57 [0,55-0,59] | 0,65 [0,64-0,68] |

Lo que significa en la práctica:
- Supervivencia: del 20% mejor puntuado por el modelo sobrevive el 99%; del 20% peor, el 63% (base 86%).
- Duplicar: del 20% mejor puntuado duplica el 50%; del 20% peor, el 19% (base 32%).

## Lo que aprendimos de las reglas
- **Funcionan, pero el modelo las supera** en las tres etiquetas.
- **Las mejores reglas solas** (supervivencia): cobertura de intereses (0,71), peor margen de 5 años (0,71-0,73, Quintana), recompras (0,71-0,74), rentabilidad sobre activos (0,68-0,73).
- **"Foso que se ensancha"** (Vinall) ayuda poco: 0,52-0,58.
- **Dos reglas salen mal escritas:** "calidad del beneficio" (devengos) da 0,32-0,35, al revés, porque las que se mueren tienen pérdidas grandes que hacen negativo el devengo. "Deuda neta / caja" no sirve (0,43-0,54) porque con caja negativa el cociente no tiene sentido.
- **Para duplicar, la poca deuda juega en contra** (0,45): con deuda el patrimonio crece más rápido (y también se pierde más rápido). Lo que más pesa es el ROE.
- **Las muertes silenciosas son de empresas chicas:** en la supervivencia amplia el tamaño solo ya da 0,78 y le gana a las reglas.

## Límites
- Sin precios: predice cómo le va al negocio, no a la acción. No dice si está barata.
- Sólo empresas que presentan en EE.UU.; financieras mezcladas con el resto.
- 2012-2019 es casi una sola época (tasas bajas).
- duplica_6 usa valor contable: castiga a las que invierten vía gastos (I+D, marketing), justo lo que Quintana advierte.

## Cómo usarlo
`python entrenar/evaluar.py TICKER` → baja la empresa de la SEC, la compara contra el último año completo y muestra los tres puntajes y qué reglas cumple.

## Auditoría contra los riesgos (2-nov, segunda vuelta)
| Riesgo | Qué se hizo | Estado |
|---|---|---|
| Recordar en vez de razonar | prueba de fuga; dos fugas tapadas (empates y faltantes) | queda 16% vs 9%: huella de la economía del año |
| Fusión contada como muerte | muestra de 80 empresas revisada a mano con nombre | arreglado: quiebra de filial (LendingTree 2019) y reorganizaciones (Perrigo, Tessera) mal clasificadas. Ahora quiebra = 1.03 + cancelación de acciones / salida de bolsa / fin de balances; compra = cambio de control (5.01) o baja de acciones tras fusión. Hertz (los accionistas cobraron) ya no cuenta como quiebra |
| Números corregidos después | primer 10-K que presentó cada dato | hecho |
| Casualidades | reglas escritas antes; PERO el período de prueba se miró ~6 veces arreglando cosas | **prueba contaminada** → se congeló una prueba nueva (abajo) |
| Aprender la década | por sector (7 divisiones) y sin financieras | se sostiene: supervivencia 0,73-0,86 en todos los sectores; duplicar 0,62-0,69 |
| Precisión engañosa | contra la media y la regla tonta | hecho |
| Porcentajes falsos | calibración por deciles | supervivencia amplia bien calibrada; estricta algo optimista en el medio (dice 92%, pasa 83%); duplicar MAL (dice 67%, pasa 56%; dice 6%, pasa 17%). La herramienta ya no muestra el número crudo: muestra lo que pasó en la prueba con puntajes parecidos |
| Reglas rotas en la herramienta | devengos y deuda neta/caja | se muestran aparte y no cuentan |

Resultados finales (etiquetas corregidas): sobrevive_10 0,81 · amplio 0,85 · duplica_6 0,65 (modelo); reglas de los cinco 0,70 · 0,72 · 0,57; regla tonta 0,61 · 0,78 · 0,46.

Las "desconocidas" que quedan terminaron sobre todo en baja voluntaria del registro (15-12G/15-15D) o avisos de que no presentan a tiempo: casi todas muertes, pero ~1 de cada 4 de la muestra eran reorganizaciones. La etiqueta amplia exagera algo las muertes.

## Prueba congelada (la única limpia)
- v1 (datos/predicciones_congeladas_v1.csv): primera, con el error de los bancos grandes. v2 (datos/predicciones_congeladas_v2.csv, la que vale): corregida, sha256 b65e29fdcaae1b676975f9223d61d081062184b3f677d88cba0f3a4ebb796e9c. 4.101 empresas del año fiscal 2025, puntuadas el 2-nov-2026.
- Huella de la v1 (vieja, no vale): `1a6a97c282e81a62cf0075a36fa929db6508a821f9fc0ae701bb79e43ac4ec53`
- Si el archivo cambia un byte, la huella cambia. En 2031-2032 (duplica_6) y 2035-2036 (supervivencia) se compara contra lo que pasó.

## Contra qué se probó (2-nov, tercera vuelta)
### Modelos publicados, en las mismas empresas (AUC; los clásicos no se pueden calcular para todas)
| Pregunta | Altman Z'' | Ohlson O | Piotroski F | Reglas de los cinco | Nuestro modelo |
|---|---|---|---|---|---|
| Accionista vivo en 10 años | 0,70 | 0,71 | 0,67 | 0,68-0,72 | **0,78-0,83** |
| Sigue presentando en 10 años | 0,76 | 0,81 | 0,70 | 0,72-0,75 | **0,84-0,87** |
| Duplica en 6 años | 0,51 | 0,48 | 0,54 | 0,57 | **0,66** |
Le gana a los tres en las tres preguntas. Para duplicar, los clásicos no sirven (azar); fueron hechos para quiebras.

### El paper de Chicago Booth (¿el beneficio por acción sube el año que viene?)
- Nuestro modelo: **60,0%** de aciertos (prueba 2018-2023, primera vez que se mira). Decir siempre lo más común: 53,8%.
- Paper: GPT-4 60,3% · red neuronal 60,1-60,5% · analistas 52,7-56,6% · regresión clásica 52,9% (base 55,5%).
- Empata con GPT-4 y con la red del paper. Ojo: otra muestra (SEC 2018-2023 vs Compustat 1968-2021), así que es una comparación de orden de magnitud, no exacta.
- Dato interesante: a un año, las reglas de los cinco y los clásicos dan AL REVÉS (0,44-0,47). Las empresas sanas tienen menos chance de mejorar el año siguiente (vuelta a la media). Encaja con los cinco: un año es ruido; su terreno es la década.

## Contra las carteras reales (2-nov, cuarta vuelta)
Pabrai (13F Dalal Street 2013-2025), Vinall (13F RV Capital 2018-2025), Quintana (posiciones que nombra en la carta 2025). Cada posición al 31-dic se compara con el balance del año anterior (lo que se sabía). Modelos entrenados sólo con 2012-2013 (fuera de muestra). Quedan afuera las extranjeras: Ferrari, POSCO, Fiat, AerCap, Brookfield Corp, H World, PDD, Wix, Sagicor, Secure Waste, Watches of Switzerland (y Goldman, que no cruzó). Paramés/Cobas no se probó: casi todo es europeo.
Error encontrado en el camino: las empresas con miles de presentaciones (bancos) no tienen ningún 10-K en la lista "recent" de la SEC; el último balance ahora sale también de los datos contables. Los resultados generales no cambiaron.

A = percentil mediano de sus elecciones dentro de su año (50 = como cualquiera). B = cuántas de sus elecciones lo lograron vs la media de esos años.
| | Vinall (47 posiciones, 13 empresas) | Pabrai (40, 18) | Quintana (12, 12) |
|---|---|---|---|
| A sobrevive (modelo) | 91 | 56 | 77 |
| A duplica (modelo) | 67 | 43 | 37 |
| A reglas de los cinco | 87 | 79 | 53 |
| A Piotroski | 77 | 66 | 55 |
| B duplica | 43% vs 33% (n=7) | 11% vs 29% (n=19) | todavía sin resultado |
| B sobrevive (estricta) | sin casos con 10 años | 76% vs 88% (n=17) | — |

Lectura:
- **Vinall es el que mejor capta el modelo:** sus elecciones caen arriba en todo. Calidad, sin sorpresas.
- **Pabrai engaña a las reglas pero no al modelo:** sus elecciones se ven bien en ratios sueltos (reglas p79, Piotroski p66), pero el modelo las pone en la media y le fue peor que a la media (Horsehead, Chesapeake y Valaris quebraron; carbón, plataformas petroleras). Son apuestas "Dhandho" de crisis: muchas mueren y pocas pagan mucho. Sus mayores aciertos (Reysas en Turquía, Ferrari) no entran en esta prueba porque son extranjeras, así que esto lo castiga de más. Además se cuenta cada empresa-año igual, no por cuánto pesó.
- **Quintana no elige por balance:** sobreviven alto, pero las reglas lo ponen en la media (p53). Encaja con lo que dice: "la imaginación es más importante que la contabilidad" (activos reales, Tesla, AST).
- Muestras chicas: sirven para ver la dirección, no para estadística fina.

## Con precios y directivos (2-nov, quinta vuelta) — todo gratis de la SEC
Precios: fails-to-deliver 2009-2026 + operaciones de directivos (1,2 M empresa-mes). Símbolo → empresa con los formularios de directivos (traen símbolo y CIK con fecha). Precio de compra = mes siguiente a presentar el balance. Etiqueta nueva **precio_duplica_6**: (valor de mercado a 6 años + dividendos + recompras − emisiones) / valor de mercado inicial ≥ 2 (lo que gana quien compra la empresa entera; los desdoblamientos no la afectan). 22.601 filas con etiqueta, tasa 35%.
Reglas de precio escritas antes de mirar (REGLAS_PRECIO en reglas_de_los_cinco.py).

Errores míos en el camino (anotados para no repetir): (1) mandé a Kaggle sin probar la cadena entera y las filas no tenían las columnas nuevas → 0 precios; ahora la cadena se prueba local con datos reales y el cuaderno FRENA si no entra ningún precio. (2) la barra "/" como argumento se convierte en ruta en la terminal de Windows.

### Resultado
- **El modelo NO predice si la inversión se duplica: 0,46** (entrenado con las camadas 2012-13, probado con 2019). Calibración al revés. No se usa.
- **Comprar barato, por camada (las reglas no se entrenan, así que cada año es una prueba limpia):**
| Camada | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|---|
| Flujo de caja / precio (Paramés) | 0,55 | 0,49 | 0,49 | 0,48 | 0,47 | 0,47 | 0,50 | 0,60 |
| Libros / precio (Pabrai) | 0,50 | 0,45 | 0,46 | 0,49 | 0,44 | 0,43 | 0,48 | 0,60 |
| Reglas de calidad de los cinco (sin precio) | 0,53 | 0,53 | 0,52 | 0,53 | 0,52 | 0,52 | 0,54 | 0,52 |
| Directivos que compran | 0,50 | 0,48 | 0,48 | 0,49 | 0,50 | 0,48 | 0,50 | 0,51 |
  → **Barato funcionó sólo en la camada 2019** (que atravesó el covid y la vuelta del value 2021-22). Entre 2013 y 2017 lo barato rindió PEOR (la década en que el crecimiento le ganó al valor). **La calidad de los cinco es chica pero estable: arriba de 0,5 en las 8 camadas.** Las compras de directivos no predicen nada.
- **Los precios sí mejoran lo demás:** duplicar el valor contable 0,66 → 0,70; ganancias del año siguiente 60,0% → **62,7%** (paper: GPT-4 60,3%). Supervivencia casi igual (0,81-0,86).
- Fuga con precios: 19% vs 9% (los precios llevan más huella de la época).
- Carteras con el modelo de precio: Vinall p71, Quintana p63, Pabrai p49.

Los modelos instalados en entrenar/modelos siguen siendo los SIN precio (evaluar.py no tiene precios en vivo).

## Texto que cambia (2-nov, sexta vuelta) — "Lazy Prices" con EDGAR-CORPUS
Parecido (coseno de palabras) del 10-K contra el del año anterior: todo el texto, riesgos (1A), juicios (3), explicación de la dirección (7). 36.535 filas con dato (camadas 2012-2019; el corpus termina en 2020). Cuadernos fabri9/ie-texto-2013 … 2020 (~4 min c/u). Reglas escritas antes (REGLAS_TEXTO). Etiqueta nueva **precio_gana_1**: el retorno de 12 meses le gana a la mediana de las compradas ese año.

Resultado por camada (AUC medio 2012-2019, y en cuántos años quedó arriba de 0,5):
| Señal | Gana a la mitad en 12 meses | Ganancias suben el año siguiente | Sobrevive 10 años |
|---|---|---|---|
| El texto no cambia (todo) | 0,513 (6 de 8) | 0,531 (7 de 8) | **0,613 (4 de 4)** |
| La explicación de la dirección no cambia | 0,514 (6 de 8) | **0,534 (7 de 8)** | **0,620 (4 de 4)** |
| Riesgos que no se reescriben | 0,512 (5 de 8) | 0,522 (7 de 8) | 0,583 (4 de 4) |
| Directivos que compran | 0,501 (3 de 8) | 0,506 | **0,435 (0 de 4: compran las que se mueren)** |
| Calidad de los cinco (balance) | 0,511 (6 de 8) | 0,469 (1 de 8) | 0,677 (4 de 4) |
- **El texto detecta el deterioro del negocio** (ganancias, supervivencia) de forma estable, pero para el **precio** el efecto es chico (0,51): el paper (1995-2014) daba ~22% anual; publicado en 2018-2020, el mercado ya lo usa. 2019 (covid) dio al revés.
- **Dato nuevo:** que los directivos compren acciones predice MÁS muerte (0,435 en las 4 camadas): compran en las empresas chicas en problemas, tratando de salvarlas.
- El modelo entrenado tampoco gana a 12 meses (0,537, por debajo del tamaño solo, 0,564).

## Franqueza (2-nov, séptima vuelta) — explicación de la dirección (sección 7), medida con palabras
franqueza.py (listas propias basadas en Rittenhouse, Li 2008, Larcker-Zakolyukina 2012), 4 cuadernos ie-franq-*. 36.415 filas con dato. Reglas escritas antes (REGLAS_FRANQUEZA). Trampas encontradas al probar: "outstanding" (= acciones en circulación) y "US" (= el país); la terminal convertía \b en caracteres invisibles (se arregló escribiendo el archivo sin pasar por la terminal).

| Señal (media 2012-2019, años arriba de 0,5) | Gana a la mitad en 12 meses | Inversión ×2 en 6 años | Ganancias suben | Sobrevive 10 años |
|---|---|---|---|---|
| **Escriben "nosotros", no "la Compañía"** | **0,526 (8 de 8)** | **0,550 (8 de 8)** | 0,514 (7 de 8) | 0,49 |
| Frases con números | 0,487 | 0,469 | 0,495 | 0,453 (al revés) |
| Jerga / frases hechas | 0,492 | 0,493 | 0,497 | 0,484 |
| Euforia | 0,503 | 0,509 | 0,506 | 0,476 |
| Admite problemas | 0,483 | 0,493 | 0,496 | **0,445: los problemas que admiten son reales** |
| Texto difícil (niebla) | 0,481 | 0,494 | 0,501 | 0,55 (fácil = sobrevive, como Li 2008) |
| Largo | 0,492 | 0,501 | 0,495 | 0,499 |

### Control de "nosotros": ¿es un disfraz de tamaño o de sector?
AUC dentro de cada tercio de tamaño y dentro de cada sector, por camada (inversión ×2 en 6 años):
2012 0,55/0,54/0,56 · 2013 0,58/0,58/0,58 · 2014 0,55/0,56/0,56 · 2015 0,56/0,55/0,56 · 2016 0,57/0,57/0,57 · 2017 0,55/0,55/0,55 · 2018 0,54/0,54/0,54 · 2019 0,50/0,50/0,51 (todas / dentro de tamaño / dentro de sector).
→ **No es tamaño ni sector**: dentro de cada grupo da lo mismo. A 12 meses (camadas independientes): 0,50-0,55, arriba de 0,5 en todos los años.

Cautelas: se encontró mirando 11 señales (texto + franqueza); que una salga 8 de 8 por azar es ~4%. Las ventanas de 6 años se pisan entre camadas (no son 8 pruebas independientes; las de 12 meses sí). Puede ser un disfraz de otra cosa no medida (estilo de los abogados que redactan, empresas dirigidas por sus dueños). **La prueba que falta es fuera de muestra: 10-K de 2021-2025, que no están en el corpus (bajarlos con edgar-crawler).**

### IA para leer franqueza
Qwen2.5-1.5B en T4 de Kaggle: 0,38 s por texto, puntajes variados (2 a 9). Los 36.000 textos = ~4 horas de placa. No lanzado.

## #39 La contradicción (superficie frágil, fondo sano), 2-nov-2026
No pasa. Superficie y fondo coinciden (correlación ~0,7): el cuadrante contradictorio es el 1-3% de las empresas y no junta más ×3 que el azar (1,18 veces, pocas empresas). Sí sirve para otra cosa: entre las que se ven frágiles, las de fondo sano tienen un tercio de los desastres. Detalle en notas/11.

## #40 La insistencia (desmentir lo esperado año tras año), 3-nov-2026
No pasa el criterio completo, pero es lo primero que muestra una huella real: la insistencia existe 2,5-4,5 veces más que por azar (8 de 8 camadas), y a 6 años las insistentes tienen más ×3 (22,7/21,5/33,3% contra 14,3/15,8/28,9%) y la mitad de desastres que el universo, en 3 de 3 camadas que se pisan. A 12 meses no gana. Falta confirmarlo con camadas no vistas. Detalle en notas/11.

## #41 Confirmación de la insistencia en 2013-2016, 4-nov-2026
No confirma. La insistencia existe (4 de 4), pero las sorpresas a 6 años no se repiten (2 de 4 contra el universo, 1 de 4 contra la foto de calidad). Y repitiendo 2017-2019 con lo seguro entrenado con más años, el exceso de ×3 de #40 casi desaparece: era frágil. Queda firme que las insistentes casi no se hunden (como la calidad) y que las "al revés" se hunden el doble o el triple.

## #42 Los que creen y aguantan (13F y directivos en las caídas), 4-nov-2026
No pasa ninguno. Fondos que suben su parte mientras cae: menos sorpresas que las caídas abandonadas (son empresas grandes; las chicas abandonadas rebotan más). Directivos que compran sin que nadie venda: más ×3 que donde venden, pero más desastres, y contra otras caídas igual de chicas da lo mismo. El tamaño explica casi todo. Detalle en notas/11.

## #43 La interrelación (números + trayectoria + personas en un solo modelo), 4-nov-2026
No pasa, pero cambia el mapa: lo extraordinario SÍ se reconoce de antemano dentro del mismo tamaño (AUC 0,65; su 10% de arriba se triplica el doble que el universo), solo que junto con los desastres: el modelo aprende "va a un extremo", no "va para arriba". El cruce de bloques agrega poco (0,650 contra 0,645 de números solos). Siguiente: cruzar este modelo de extremos con el de muerte.

## #44 Extremo × no hundirse, 4-nov-2026: PASA (la primera de 44)
Cruce del modelo de extremos (#43) con un modelo de desastre a 6 años: de la mitad más segura, las de extremo más alto. En 6 de 7 camadas tiene más ×3 que el universo (15-37% contra 11-28%) con un cuarto a la mitad de los desastres (0,5-7% contra 10-19%) y mejor promedio a 6 años. No es tamaño. A 12 meses no se nota. Cautela: validación por empresa dentro de los mismos años; falta la prueba fuera de tiempo y la lista congelada. Detalle en notas/11.

## #45 El cruce fuera de tiempo + lista congelada, 4-nov-2026
Fuera de tiempo no pasa: el cruce corta los desastres a un tercio pero sus ×3 quedan como el universo y el promedio, abajo (0 de 5). Lo que sí se sostiene: el modelo de extremos solo tiene más ×3 y más promedio que el universo en 5 de 5 (con más desastres), y el de desastre acierta 0,74-0,83. El #44 se apoyaba en compartir la época. Lista congelada 2025 (4.101 empresas, 410 elegidas): datos/congelada_cruce_2025.csv, sha256 b55867ce…9378.

## #46 Magnitud × dirección (2020-2021, a 4 años), 4-nov-2026
No pasa. Quién va a un extremo se reconoce muy bien también en años nuevos (AUC 0,75-0,77); hacia qué lado, entre las extremas, poco (0,60-0,63). Además se arregló un error que hacía que dos corridas iguales dieran listas distintas; la lista congelada vigente es datos/congelada_cruce_2025.csv, sha256 216d486c…36f7.

## #47 quién financia el salto (4-nov-2026)
No pasa. Emisión, dilución, años de caja, deuda nueva y entregas fallidas (FTD, bajadas en ie-fallas-2008/2017) casi no mejoran la dirección dentro de los extremos (AUC 0,54-0,69 en 2022-2024 a 12 meses). Las elegidas: ×2 de 2 a 3 veces el universo y promedio mayor en 3 de 3, pero 1,5-2 veces más desastres. Detalle en notas/11.
