# Noche 09-11: pesquisa desde WikiLeaks (Fabri: «no frenes hasta que me despierte»)
Regla: leer abierto; lo que aparezca al lado se anota y se prueba. Cada prueba se anota en notas/11 ANTES de medir. Nada entra a Tr sin pasar 2021-2022.
Estado de cada paso: [ ] pendiente, [~] corriendo, [x] hecho (resultado en notas/11).

1. [~] (exploración hecha: ganó − sólo mencionada +26; confirmación pre-registrada en notas/11, espera los económicos) #102 lectura: Qwen lee los 1.387 cables BEXP (Kaggle ie-cables102 → entrenar/sal-cab102/lectura.jsonl). Después: mapear empresas a CIK (núcleos EDGAR, también los de nombre común) y medir a 4 años por papel: ayudada / ganó / perdió / en disputa / con problemas.
2. [~] (39.674 cables económicos 2004-2010 en entrenar/sal-econ/econ.jsonl; falta leerlos con el modelo) Ampliar a TODOS los cables 2004-2010 que nombran una empresa (no sólo BEXP): la etiqueta se quedaba corta.
3. [~] (#104 exploración: −13,8; espera los cables económicos) Planes de compra de cada país (procurement_plan: nuclear, aviones, trenes) → sector → rendimiento del sector a 4 años.
4. [x] (201 pedidos 2004-2010 en entrenar/sal-econ/pedidos.jsonl. Temas económicos: renovables (WIREC 2007-08, estímulo verde 2009), nuclear (bancos de combustible, Golfo, Turquía 2009), sanciones a bancos de Irán, piratería, espacio. Coincide en dirección con #89 —donde la élite se mete después rinde menos: solar desde 2008, nuclear desde 2011— pero son 3-4 temas: no se puede medir como prueba; queda como pista) La agenda privada de Washington: cables STATE que piden información a todas las embajadas (ej. planes nucleares dic-2008) → qué temas, y si anticipan sectores.
5. [ ] Lo que las empresas cuentan en confianza (pérdidas, irse del país) contra lo que dicen en su 10-K del mismo año.
6. [x] (#103: no pasa; créditos >100M dan +22 con 17 casos, sin probar) Fuente actual del mismo empuje, para Tr: EXIM Bank (créditos aprobados, data.exim.gov) y casos del Advocacy Center.
