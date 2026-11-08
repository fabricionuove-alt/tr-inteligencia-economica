# Plan: redes de influencia (7-nov-2026). Propuesta, nada corrido todavía

Pedido de Fabri: rastrear las afiliaciones a grupos de influencia (corporativos, transnacionales, supragubernamentales, familias, China, culturales) para aumentar las chances de predecir lo extraordinario.

## Por dónde entra
Hoy el modelo reconoce **cuánto** se va a mover una empresa (AUC 0,79-0,84), pero no **para qué lado** (0,54-0,69). Lo que sabe es suyo y no sale de inclinarse hacia las chicas (#51).
Las redes podrían dar justo el lado que falta. Hay evidencia publicada de que la conexión predice la dirección:
- Directorios centrales: +4,7% anual (Larcker, So y Wang, JAE 2013), más fuerte en empresas chicas, jóvenes y en apuros.
- Lazos de universidad entre fondos y directorios: ganancia concentrada alrededor de las noticias (Cohen, Frazzini y Malloy, JPE 2008).
- Más gasto en lobby se asocia a mejor rendimiento posterior (Chen, Parsley y Yang, JBFA 2015; hay estudios en contra).
- Directores conectados al partido ganador consiguen más contratos públicos después de la elección (Goldman, Rocholl y So, RF 2013).
- Los proveedores en EE.UU. de una empresa china que entra a la Entity List caen alrededor de 2,2 puntos (Allen, Business and Politics).

**La trampa ya conocida (#42):** casi todo lo que se mide en las personas termina marcando tamaño y seguridad (las grandes hacen lobby, tienen directorios célebres y fondos que aguantan). Por eso cada hipótesis se compara contra un placebo dentro del mismo decil de tamaño, como en #51, y no contra el universo.

## Fuentes, probadas en vivo el 7-nov
| Fuente | Estado | Desde | Uso |
|---|---|---|---|
| Formularios 3/4/5 de la SEC (marca de director, dueño de más del 10%) | ✅ 83 zips trimestrales | 2006 | red de directorios compartidos, control familiar |
| FEC (aportes de campaña, con el empleador) | ✅ con DEMO_KEY, sin cuenta | 1979 | dinero político de la empresa y sus directivos |
| USAspending (contratos federales) | ✅ | 2001 (fiable 2008) | dependencia del Estado |
| Lista Consolidada de EE.UU. (Entity List, SDN y otras), con fecha de alta | ✅ CSV | 1990s | listas negras, China |
| OpenSanctions | ✅ (licencia no comercial) | 2021 | sanciones de la UE y la ONU, personas políticamente expuestas |
| GLEIF (quién es dueño de quién) | ✅ | 2012 | grupos transnacionales |
| LittleSis (relaciones entre empresas y gobierno) | ✅ CC BY-SA | sin fechas sistemáticas | sólo para validar |
| ProPublica 990 (consejos de fundaciones, museos, universidades) | ✅ | 2011 | ámbito cultural |
| AKShare / CNINFO (bolsas chinas) | ✅ sin clave | 1990s | un mercado entero que nunca miramos |
| 13F (los tres gigantes de fondos) | ✅ ya bajado | 2013 | dueños compartidos |
| Registro de lobby del Senado (LDA) | ❌ bloquea las consultas automáticas | 1999 | falta: lo baja Fabri a mano o queda afuera |
| OpenSecrets | ❌ pide cuenta | — | afuera (regla: no crear cuentas) |
| Wikidata, títulos nobiliarios × directorios | ❌ sólo 2 personas en empresas que cotizan | — | **nobleza descartada por falta de datos** |

## Hipótesis (cada una con su criterio, escrito antes de correr)
Un bloque nuevo de rasgos por año, sin nombres (percentiles, como siempre). Se agrega a los modelos de #50 (P2 y PD a 12 meses), y cada camada aprende sólo con camadas de al menos dos años antes.

| # | Hipótesis | Rasgo | Lo que predice la literatura |
|---|---|---|---|
| H1 | **Directorio central** | grado, cercanía e intermediación en la red de directores (formularios 3/4/5) | más ×2, más fuerte en las chicas |
| H2 | **Contagio por la red** | a otra empresa con la que comparte un director le fue extraordinario (o desastroso) el año anterior | el lado viaja por la red |
| H3 | **Dinero político** | aportes de los directivos; parte puesta al partido que después ganó (elecciones 2008-2022) | más contratos y mejor rendimiento después de ganar |
| H4 | **Dependencia del Estado** | contratos federales sobre ventas, y su crecimiento | margen más alto, menos desastres |
| H5 | **Control familiar** | dueños personas o fideicomisos con más del 10%, y directores con el mismo apellido | familias: más largo plazo, menos riesgo |
| H6 | **Supracorporativo** | ser miembro del Pacto Global de la ONU, de Business Roundtable o de alianzas climáticas (altas y bajas con fecha) | sin evidencia sobre el precio: exploratoria |
| H7 | **China** | estar en una lista negra, o ser proveedora de una que entra (proveedores del 10-K) | evento negativo |
| H8 | **Cultural** | directores en consejos de museos, universidades y fundaciones (990) | sin evidencia: exploratoria |

**Criterio común, por hipótesis.** Los años 2019-2024 ya están vistos: sólo pueden descartar. Sobrevive si cumple las tres:
1. Con el bloque, la AUC del **lado** (×2 contra desastre, entre las de magnitud alta) sube al menos 0,01 en 5 de 6 camadas.
2. Con el bloque barajado dentro del decil de tamaño (100 veces), la cartera Kelly real supera el percentil 95 del placebo en 5 de 6 camadas.
3. No sube el peso puesto en desastres.

**Pruebas múltiples:** son 8 hipótesis más sobre años gastados. Lo que sobreviva no se cree: se congela su lista de 2025, con huella sha256, y se mide con los precios de 2026. Y se repite en China (abajo) sin cambiar nada.

## La prueba más fuerte: China
El mercado chino nunca se miró. Las bolsas de Shanghái y Shenzhen tienen balances, precios, directorios y empresas del Estado, gratis por AKShare y CNINFO. Si H1-H5 funcionan en EE.UU., se aplican tal cual en China (2010-2024) sin tocar nada: eso es una prueba fuera de muestra de verdad, sin esperar a 2026. Ahí además está la conexión que más estudios tiene: delegados del Congreso del Pueblo y empresas del Estado.

## Orden y costo
| Fase | Qué | Datos | Tiempo |
|---|---|---|---|
| 1 | H1, H2, H5 (red de directores, contagio, familias) | formularios 3/4/5, ya conocidos | 1 día; Kaggle < 20 min por corrida |
| 2 | H3, H4, H7 (FEC, contratos, listas negras) | APIs gratis; lo difícil es cruzar nombres de empresas | 2 días |
| 3 | China: bajar el mercado y repetir lo que sobrevivió | AKShare / CNINFO | 2-3 días |
| 4 | H6, H8 (exploratorias) | listas de miembros y 990 | sólo si 1-3 dan algo |

Límites éticos: sólo cargos y actos públicos de personas con cargos públicos o directivos. Nada de religión, etnia, salud ni vida privada, aunque figure en alguna lista. Nada de la red se muestra con nombres en el juego.
