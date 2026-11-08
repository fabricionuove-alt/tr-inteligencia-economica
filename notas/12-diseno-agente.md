# Diseño del agente (propuesta, sin programar, 2-nov-2026)

## Qué hace
**La mesa de los cinco.** Le das una empresa y te devuelve lo que diría cada uno, apoyado en lo que sí se pudo probar.

Dos modos:
1. **Empresa que cotiza en EE.UU.** (símbolo): números probados + las cinco voces.
2. **Cualquier otra cosa** (un proyecto, un pitch, una empresa chica o extranjera): sólo las cinco voces, con lo que vos le cuentes.

## Lo que muestra (empresa que cotiza)
1. **Lo medible y validado** (precalculado en Kaggle, sin nombres al entrenar):
   - riesgo de que el accionista no sobreviva 10 años (0,81-0,86, le gana a Altman/Ohlson/Piotroski);
   - ¿suben las ganancias el año que viene? (62,7%);
   - calidad según las reglas de los cinco (cada regla con su percentil);
   - si reescribió su balance este año (texto que cambia → deterioro);
   - franqueza leída por IA (si pasa la prueba).
   Cada número dice qué tan probado está y contra qué.
2. **Las cinco voces**, cada una con su ficha (sus preguntas, reglas y frases, sacadas de las notas 01-05):
   - Quintana: ¿existirá en 10 años? ¿cuánto está ganado el 1 de enero? ¿pesimista a 5 años?
   - Vinall: ¿el foso se ensancha? ¿es la obra de vida de quien la dirige?
   - Paramés: ¿cuánto vale (número)? ¿dónde no entra capital? ¿deuda? ¿familia o ancla?
   - Pabrai: ¿deuda? ¿riesgo o sólo incertidumbre? ¿declive temporal o permanente?
   - Crescenta como contrapunto: ¿cuánto queda neto de comisiones? ¿me pagan la iliquidez?
3. **Dónde chocan** (de la síntesis): por ejemplo vender lo que subió (Paramés sí, Vinall y Pabrai no).
4. **Lo que NO sabe**, siempre visible: no predice el precio (33 señales públicas probadas, ninguna estable); no conoce a los directivos; no reemplaza ir a ver.

## Cómo funciona (sin claves)
- Página estática en Vercel.
- Números: un archivo precalculado en Kaggle por trimestre (la SEC no deja pedir datos desde el navegador).
- Voces: IA integrada con Puter.js (cada visitante usa su cuenta gratis; vos no ponés ninguna clave).
- La IA recibe la ficha del inversor + los números de la empresa y tiene prohibido inventar datos: cita sólo lo que se le dio y marca cuando opina.

## Lo que NO hace
No recomienda comprar ni vender. No da consejo financiero personalizado.

## A decidir con Fabri
- ¿Así, o con otra forma (el escéptico de pitches, el show)?
- ¿Identidad visual ODD o neutra?
