"""Las reglas de la síntesis, escritas el 2-nov-2026 ANTES de ver cualquier resultado.
No se tocan después de mirar la prueba. Cada regla es (rasgo, signo, de quién viene).
El puntaje es el promedio de los percentiles (dentro del mismo año) con su signo.
Lo que NO se puede probar acá: precio pagado (no hay cotizaciones), directivos, cultura, temperamento."""

REGLAS = [
    # La deuda es lo que mata (Pabrai n.º 1, Paramés 5% del fondo, Vinall)
    ('deuda_activos',  -1, 'Pabrai/Paramés/Vinall: poca deuda'),
    ('deuda_neta_fco', -1, 'Pabrai: deuda que se paga con la caja de pocos años'),
    ('cobertura_int',  +1, 'Pabrai: los intereses no ahogan'),
    # Calidad: rentabilidad alta sobre el capital (Paramés: ROCE 25-30%)
    ('roa',            +1, 'Paramés: alta rentabilidad sobre el capital'),
    ('fco_activos',    +1, 'Paramés: caja contante y sonante, no beneficio ajustado'),
    ('fcf_ventas',     +1, 'Paramés/Quintana: flujo de caja libre'),
    ('devengos',       -1, 'calidad del beneficio: que el resultado sea caja'),
    # Recurrencia y estabilidad (Quintana: el 80% aburrido, beneficio ganado el 1 de enero)
    ('estab_margen',   -1, 'Quintana: margen estable = recurrencia'),
    ('margen_op_min5', +1, 'Quintana: el peor año de los últimos cinco no fue un desastre'),
    # El foso que se ensancha (Vinall)
    ('tendencia_roa',  +1, 'Vinall: la rentabilidad mejora, el foso se agranda'),
    # Asignación de capital para el dueño (Paramés con Repsol, Pabrai, Quintana)
    ('recompras_fco',  +1, 'Paramés/Pabrai: recompra acciones'),
    ('dilucion_3',     -1, 'Pabrai/Vinall: no diluye al accionista'),
]

# Reglas de TEXTO, escritas el 2-nov-2026 ANTES de ver cualquier resultado con texto.
# Parecido (coseno de frecuencia de palabras) entre el 10-K de un año y el del anterior, como "Lazy Prices"
# (Cohen-Malloy-Nguyen, J. of Finance 2020): las que NO cambian su texto rinden mejor. Más parecido = mejor.
REGLAS_TEXTO = [
    ('texto_igual_total',   +1, 'Lazy Prices / Quintana: directivos que cuentan lo mismo y cumplen (todo el texto)'),
    ('texto_igual_riesgos', +1, 'Lazy Prices: los riesgos que se reescriben avisan algo (sección 1A)'),
    ('texto_igual_juicios', +1, 'Lazy Prices: cambios en juicios y litigios (sección 3)'),
    ('texto_igual_mdna',    +1, 'Vinall: la explicación de la dirección, escrita para dueños (sección 7)'),
]

# Reglas de FRANQUEZA, escritas el 2-nov-2026 ANTES de ver cualquier resultado de franqueza.
# Sobre la explicación de la dirección (sección 7 del 10-K). Listas de palabras propias (franqueza.py),
# basadas en Rittenhouse (datos concretos vs "generalidades ofuscadoras"), Li 2008 (largo y difícil = peor)
# y Larcker-Zakolyukina 2012 (los que engañan: más euforia, menos "nosotros", más frases impersonales).
REGLAS_FRANQUEZA = [
    ('franq_numeros',  +1, 'Rittenhouse/Vinall: frases con datos concretos, no generalidades'),
    ('franq_cliches',  -1, 'Rittenhouse: jerga y frases hechas (líder del sector, sinergias, clase mundial)'),
    ('franq_euforia',  -1, 'Larcker-Zakolyukina: euforia extrema (excepcional, récord, extraordinario)'),
    ('franq_admite',   +1, 'Vinall/Quintana: admite problemas y errores ("por debajo de lo esperado")'),
    ('franq_nosotros', +1, 'Larcker-Zakolyukina: hablan en primera persona, no "la Compañía"'),
    ('franq_niebla',   -1, 'Li 2008: frases largas y palabras difíciles (índice de niebla de Gunning)'),
    ('franq_largo',    -1, 'Li 2008: las que esconden escriben más largo'),
]

# Reglas de PRECIO y DUEÑOS, escritas el 2-nov-2026 ANTES de ver cualquier resultado con precios.
# Precio = mes siguiente a la presentación del balance (nunca antes). No se tocan después de mirar.
REGLAS_PRECIO = [
    ('rinde_fcf',        +1, 'Paramés: comprar a pocas veces el flujo de caja libre (5x vs 18x)'),
    ('rinde_ganancia',   +1, 'Paramés: PER 6-7, la mitad que el mercado'),
    ('ebit_ev',          +1, 'Quintana: EV/EBIT bajo (FRP vs Vulcan a 26x)'),
    ('libro_precio',     +1, 'Pabrai: comprar por debajo de lo que vale (Reysas al 2%)'),
    ('directivos_compran', +1, 'Quintana: compras de directivos confirman (Sagicor); Vinall: soul in the game'),
    ('compra_neta_mcap', +1, 'Vinall/Quintana: los de adentro ponen su plata, neto de lo que venden'),
]


# Reglas de RECURRENCIA y DUEÑOS, escritas el 2-nov-2026 ANTES de mirar (notas/11-registro-de-senales.md, #30-33).
REGLAS_DUENOS = [
    ('diferido_ventas', +1, 'Quintana: ingresos ganados el 1 de enero; Vinall: el cliente paga antes (Wix)'),
    ('rpo_ventas',      +1, 'Quintana: ingresos ya contratados para los próximos años'),
    ('dueno_mayor_pct', +1, 'Paramés: familia o ancla con mucho en juego; Vinall: la obra de su vida'),
    ('duenos_grandes',  +1, 'Paramés: varios de adentro con más de 5%'),
]

# Señal #34 (notas/11): franqueza leída por IA (Qwen2.5-3B), escrita antes de mirar.
REGLAS_IA = [
    ('franq_ia', +1, 'Vinall/Quintana/Rittenhouse: franqueza de la dirección leída por una IA (1 a 10)'),
]
