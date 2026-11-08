# Prueba fuera de muestra de "nosotros" — criterio escrito ANTES de bajar los datos (2-nov-2026)

**Hipótesis:** las empresas cuya explicación de la dirección (sección 7 del 10-K) usa "nosotros/nuestro" en vez de "la Compañía" rinden mejor. Se descubrió mirando las camadas 2012-2019 (10-K presentados 2013-2020).

**Datos nuevos, nunca mirados:** 10-K presentados en 2021-2025 (camadas 2020-2024), bajados directo de la SEC. Muestra al azar de empresas con 10-K cada año (semilla fija 7), sección 7 recortada del documento.

**Medida:** exactamente la misma de franqueza.py (`franq_nosotros` = nosotros / (nosotros + "la Compañía" y parecidas)), sin cambiar nada.

**Etiqueta:** `precio_gana_1` (el retorno de 12 meses del dueño de toda la empresa le gana a la mediana de las compradas ese año). Es la única con resultado para 2020-2024; las camadas a 12 meses no se pisan.

**Éxito (las tres):**
1. AUC medio de las 5 camadas ≥ 0,52.
2. Al menos 4 de las 5 camadas por encima de 0,50.
3. Se sostiene dentro de tamaño y dentro de sector (diferencia < 0,02 contra "todas").

**Fracaso:** si no se cumple cualquiera de las tres, la señal se declara casualidad y no se usa.

**Calibración previa (no es la prueba):** sobre 10-K de 2020, comparar la medida de mi recorte contra la del corpus para las mismas empresas. Si no se parecen (correlación < 0,8), primero se arregla el recorte.

## Resultado (2-nov-2026, mismo día; criterio escrito antes)
Calibración: mi recorte vs el corpus en 2020, 215 empresas: correlación de `franq_nosotros` 0,96 (pasa, mínimo 0,8).
Datos: 10 cuadernos ie-fuera-AÑO-{0,500}, 1.000 balances al azar por año 2021-2025, ~79% recortados → ~600 por camada con precio.

| Camada (compra) | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|
| "nosotros", todas | 0,528 | 0,524 | 0,574 | 0,494 | 0,468 |
| dentro de tamaño | 0,522 | 0,517 | 0,564 | 0,480 | 0,472 |
| dentro de sector | 0,549 | 0,532 | 0,539 | 0,488 | 0,489 |

- Criterio 1 (media ≥ 0,52): **0,518 → NO**.
- Criterio 2 (≥ 4 de 5 arriba de 0,5): **3 de 5 → NO**.
- Criterio 3 (diferencia < 0,02 dentro de tamaño/sector): casi (2022 sector 0,035).

**Veredicto: falla. Según lo escrito antes, la señal se declara casualidad y no se usa.**
Lectura: funcionó en 2020-2022 y se dio vuelta en 2023-2024 (los años en que unas pocas gigantes de IA se llevaron todo). Con ~600 empresas por año el margen de error por camada es ~±0,025, así que tampoco se puede descartar un efecto chico; pero agrandar la muestra ahora sería mover el arco después de patear, y no se hace.
