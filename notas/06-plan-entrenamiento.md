# Plan de entrenamiento (propuesta 2-nov-2026, sin aprobar)

## En qué se apoya (ya existe)
- Kim, Muhn, Nikolaev (Chicago Booth 2024, arXiv 2407.17866): estados contables anonimizados y estandarizados (sin nombre ni fecha) → GPT-4 predice la dirección de las ganancias mejor que analistas. Es exactamente el truco anti-sesgo.
- ChronoGPT/ChronoBERT (arXiv 2502.21206): modelos entrenados sólo con texto hasta cada año (Hugging Face: manelalab). Look-Ahead-Bench (arXiv 2601.13770): para medir si el modelo "recuerda" en vez de razonar.
- virattt/ai-hedge-fund: agentes con la persona de cada inversor (incluye uno de Pabrai). TauricResearch/TradingAgents: agentes que debaten y un gestor que decide.
- Datos: SEC EDGAR "Financial Statement Data Sets" (gratis, sin clave, todas las empresas que presentan, desde 2009, incluye las que después desaparecen). Open Source Asset Pricing (Chen-Zimmermann, 212 señales). Precios con empresas quebradas/deslistadas: pagos (MarketParquet ~79 $, Sharadar, CRSP).
- Cómputo: Kaggle (cuenta fabri9), corrida corta de prueba antes de la larga.

## Idea central
Etiquetas sin precios: con EDGAR solo se puede responder las dos preguntas de la síntesis:
- "¿Sigue existiendo y presentando balances 10 años después?" (separar quiebra de fusión).
- "¿Duplicó su valor para el dueño en 6 años?" (patrimonio + dividendos + recompras, o flujo de caja libre por acción).
Así no hace falta comprar precios ni hay sesgo de supervivencia.

## Sesgos a cuidar (además de nombres y fechas)
- Supervivencia: incluir las que murieron.
- Punto en el tiempo: usar la fecha de presentación, no la de cierre.
- La época se filtra por los números: pasar todo a ratios y tamaños relativos, sin montos absolutos ni tasas de interés.
- Pocos casos independientes: con horizonte de 6-10 años, entrenamiento 2009-2015 y prueba 2016-2019.
