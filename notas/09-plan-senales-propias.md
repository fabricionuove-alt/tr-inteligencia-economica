# Plan: señales que no usa todo el mundo (2-nov-2026)

Diagnóstico (Fabri): le di al modelo los mismos ratios que usan todos los fondos cuantitativos. Si todos miran lo mismo, el precio ya lo tiene (por eso "barato" no anduvo). Lo que distingue a los cinco no está en el balance: personas, franqueza, dueños con piel en el juego, clientes, ejecución.

Cambio de método: un "sentido" por inversor, con su propia fuente, probado solo, por camada (8 años), con reglas escritas antes. Se queda sólo lo que sobrevive. Después se combinan como expertos que discuten, no como un modelo con todo adentro.

| Sentido (de quién) | Fuente gratis | Qué se mide | Evidencia previa |
|---|---|---|---|
| Lo que cambian al escribir (Quintana: "directivos que explican con honestidad") | EDGAR-CORPUS 1993-2020 + edgar-crawler para después | cuánto cambia el texto del 10-K de un año al otro (riesgos, juicios, directivos) | "Lazy Prices", Cohen-Malloy-Nguyen, J. of Finance 2020: las que cambian su texto rinden mucho peor; el mercado no lo ve el día que sale |
| Franqueza (Vinall: cartas escritas para dueños) | llamadas de resultados S&P 500 2005-2025 + MD&A | admite errores, da números concretos, poca jerga; leído con un modelo de lenguaje abierto en Kaggle | Rittenhouse: los más francos le ganan a los menos (sin revisión independiente) |
| Dueños con piel en el juego (Paramés: familias y anclas) | formularios de directivos (ya bajados): acciones que tiene cada uno después de operar | % de la empresa en manos del mayor dueño interno; fundador al frente | Fahlenbrach 2009 sí; estudio 2010-2024 no: hay que probarlo |
| Clientes que lo aman (Pabrai: "la lista de lo que consumís") | visitas de Wikipedia 2015+ | crecimiento de la atención a la marca vs sus competidores | sin evidencia firme: experimento |
| Ejecución / innovación (Vinall: el foso que se ensancha) | PatentsView (USPTO) | patentes y citas por empresa, y si suben o bajan | literatura de innovación |
| Ingresos ya contratados (Quintana: "ganado el 1 de enero") | USAspending.gov (contratos federales) | contratos plurianuales por empresa | experimento |

Descartado: Violation Tracker (la descarga completa es paga).
Orden propuesto: 1) texto que cambia, 2) franqueza, 3) dueños. Son los que más se parecen a lo que hacen los cinco y donde casi nadie mira con este detalle.
Riesgo: Lazy Prices se publicó en 2018-2020; desde entonces muchos fondos lo usan y puede haberse gastado. Por eso la franqueza leída con IA es la apuesta más propia.
