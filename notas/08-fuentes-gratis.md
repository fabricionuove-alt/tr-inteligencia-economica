# Fuentes gratis verificadas (2-nov-2026)
Todas se bajaron o se listaron de verdad. Ninguna pide pagar ni crear cuenta.

## Precios, incluidas las empresas que desaparecieron
1. **SEC Fails-to-Deliver** — https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data
   Quincenal, julio 2009 → octubre 2026 (415 archivos). Columnas: fecha | CUSIP | símbolo | cantidad | nombre | **precio de cierre del día anterior**. ~74.000 filas por quincena. No están todas las acciones todos los días (sólo las que tuvieron fallas), pero casi todas aparecen seguido. La SEC aclara que no garantiza que el precio coincida con otras fuentes.
2. **SEC Form 13F Data Sets** — https://www.sec.gov/dera/data/form-13f
   Trimestral, 2013 → agosto 2026 (54 zips, ~85 MB c/u). Cada fondo declara acciones y valor por empresa: valor / acciones = precio. Sirve también para cruzar CUSIP con nombres y para sumar más inversores value (Berkshire, Himalaya, Markel, Fundsmith, Akre, Oakmark).
3. **Valor de mercado en la portada del 10-K** (dei:EntityPublicFloat), ya dentro de los datos de la SEC que bajamos. Una vez por año.

## Quiebras (para validar las etiquetas)
4. **Florida-UCLA-LoPucki Bankruptcy Research Database** — https://www.lopucki.law.ufl.edu/index.php
   Tabla de casos gratis: quiebras de grandes empresas públicas desde oct-1979 hasta dic-2022. **Para bajarla hay que aceptar sus términos: sólo investigación/enseñanza, prohibido el uso comercial.** Necesita el OK de Fabri.

## Otros países (la prueba más dura)
5. **Brasil, CVM dados abertos** — https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/
   Balances anuales estandarizados 2010-2026 (un zip por año) + registro de empresas con su situación (cancelada, motivo): cad_cia_aberta.csv.
6. **Reino Unido, Companies House Free Accounts Data** — https://download.companieshouse.gov.uk/en_accountsdata.html
   Archivos diarios y mensuales con los balances electrónicos (iXBRL) de las empresas británicas. Hay que leer los iXBRL uno por uno; no confirmé si incluye las disueltas.

## Segunda búsqueda: lo que miran los cinco más allá del balance (todo verificado 2-nov, responde sin clave)
| Para qué (quién lo usaría) | Fuente | Qué trae |
|---|---|---|
| Dueños que compran sus propias acciones (Quintana con Sagicor, "soul in the game" de Vinall) | **SEC Insider Transactions Data Sets** — https://www.sec.gov/dera/data/form-345 | Formularios 3/4/5 desde 2006, zips trimestrales hasta 2026q3: quién compra o vende, cuánto y a qué precio. También da precios. |
| Europa (Paramés, Cobas) | **filings.xbrl.org** — https://filings.xbrl.org/api/filings | 27.626 informes anuales ESEF de cotizadas europeas (desde 2021), en JSON, sin restricciones de uso. |
| Macro austríaca (Quintana, Paramés: dinero, deuda, inflación) | **FRED** — https://fred.stlouisfed.org/graph/fredgraph.csv?id=M2SL | Cualquier serie (M2, deuda pública, tasas, inflación) en CSV sin clave. |
| Macro de países (emergentes, clases medias: Huerta de Soto) | **Banco Mundial API** — https://api.worldbank.org/v2/ | PIB, población, energía por país, sin clave. |
| Innovación / foso por ejecución (Vinall) | **PatentsView (USPTO)** — https://patentsview.org/download/data-download-tables | Patentes concedidas desde 1976 con su empresa dueña, CC BY 4.0. |
| Lo que dicen los directivos (cultura, honestidad: Vinall, Quintana) | **EDGAR-CORPUS (Hugging Face)** — https://huggingface.co/datasets/eloukas/edgar-corpus | Todos los 10-K 1993-2020 partidos por sección (negocio, riesgos, MD&A), Apache 2.0. |
| Cómo hablan en las llamadas de resultados | **sp500_earnings_transcripts (Hugging Face)** — https://huggingface.co/datasets/kurry/sp500_earnings_transcripts | Transcripciones S&P 500, 2005-2025, licencia MIT. |
| Productos que la gente usa y ama (Pabrai: "hacé la lista de lo que consumís") | **Wikipedia pageviews** — https://wikimedia.org/api/rest_v1/ | Visitas mensuales por artículo (marca/producto), sin clave. |

Con registro gratis (clave de datos, no de IA): Corea **OpenDART** (gratis, 20.000 consultas/día), Japón **EDINET** (pide cuenta; no confirmé que sea gratis).
No responde a descarga automática: **FINRA short interest** (dio 503).

## Descartadas
- yfinance / Alpha Vantage: no guardan las que desaparecieron.
- Quandl WIKI: congelada en 2018 y pide clave.
- MarketParquet, Sharadar, Norgate, Historicaldata: pagos (sus "gratis" son muestras).
- Kaggle "Arandkei delisted archive": chico y con marca de suscripción.

## Plan
1. Precios desde Fails-to-Deliver (+13F para rellenar), cruzados por nombre/CUSIP con nuestras empresas → nueva etiqueta "el precio se duplicó en 6 años" y la pregunta "¿está barata?" (precio / caja, precio / ganancia).
2. Probar en los años del hueco que nunca se miraron (2014-2018).
3. Más carteras value desde los 13F.
4. Brasil como prueba fuera de EE.UU.
