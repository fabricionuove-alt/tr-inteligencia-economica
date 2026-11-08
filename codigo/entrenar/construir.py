"""Arma el dataset anonimizado desde los JSON de la SEC (companyfacts + submissions).

Una fila = una empresa en un año fiscal, con lo que se sabía el día que presentó su 10-K.
Salida: filas.csv con id anónimo, año (sólo para partir entrenamiento/prueba; NUNCA entra al modelo),
rasgos (ratios) y etiquetas.

Uso: python construir.py <dir_facts|facts.zip> <dir_subs|subs.zip> <salida.csv> [parte] [partes]
"""
import sys, os, json, zipfile, hashlib, math, csv
try:
    import orjson                      # 3-4 veces más rápido para leer los JSON grandes
    cargar = orjson.loads
except ImportError:
    cargar = json.loads
from collections import defaultdict

# Conceptos us-gaap (el primero que exista gana)
C = {
    'ventas': ['Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet',
               'RevenueFromContractWithCustomerIncludingAssessedTax', 'SalesRevenueGoodsNet'],
    'res_neto': ['NetIncomeLoss', 'ProfitLoss'],
    'res_op': ['OperatingIncomeLoss'],
    'bruto': ['GrossProfit'],
    'activos': ['Assets'],
    'pasivos': ['Liabilities'],
    'patrimonio': ['StockholdersEquity',
                   'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest'],
    'deuda_lp': ['LongTermDebtNoncurrent', 'LongTermDebt', 'LongTermDebtAndCapitalLeaseObligations'],
    'deuda_cp': ['DebtCurrent', 'LongTermDebtCurrent', 'ShortTermBorrowings'],
    'caja': ['CashAndCashEquivalentsAtCarryingValue',
             'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents'],
    'fco': ['NetCashProvidedByUsedInOperatingActivities'],
    'capex': ['PaymentsToAcquirePropertyPlantAndEquipment'],
    'recompras': ['PaymentsForRepurchaseOfCommonStock'],
    'dividendos': ['PaymentsOfDividendsCommonStock', 'PaymentsOfDividends'],
    'intereses': ['InterestExpense', 'InterestExpenseDebt'],
    'id': ['ResearchAndDevelopmentExpense'],
    'emisiones': ['ProceedsFromIssuanceOfCommonStock'],
    # cobrado por adelantado (el cliente paga antes) y ya contratado para los años siguientes (desde 2018)
    'diferido': ['ContractWithCustomerLiability', 'DeferredRevenue', 'ContractWithCustomerLiabilityCurrent', 'DeferredRevenueCurrent'],
    'rpo': ['RevenueRemainingPerformanceObligation'],
    'activos_cte': ['AssetsCurrent'],
    'pasivos_cte': ['LiabilitiesCurrent'],
    'ganancias_ret': ['RetainedEarningsAccumulatedDeficit'],
    'acciones': ['WeightedAverageNumberOfDilutedSharesOutstanding',
                 'WeightedAverageNumberOfSharesOutstandingBasic'],
}
FIN_DATOS = 2026  # último año con presentaciones en los datos (bajados nov-2026)
FLUJOS = {'emisiones', 'ventas', 'res_neto', 'res_op', 'bruto', 'fco', 'capex', 'recompras', 'dividendos',
          'intereses', 'id', 'acciones'}


def dias(a, b):
    from datetime import date
    y1, m1, d1 = map(int, a.split('-')); y2, m2, d2 = map(int, b.split('-'))
    return (date(y2, m2, d2) - date(y1, m1, d1)).days


def anuales(facts):
    """{año_fiscal: {campo: valor}} tomando cada valor del PRIMER 10-K que lo presentó
    (así no usamos cifras corregidas años después). También devuelve la fecha de presentación."""
    g = facts.get('facts', {}).get('us-gaap', {})
    filas = defaultdict(dict)
    presentado = {}
    for campo, nombres in C.items():
        for n in nombres:
            if n not in g:
                continue
            unidades = g[n]['units']
            serie = unidades.get('USD') or unidades.get('shares') or next(iter(unidades.values()), None)
            if not serie:
                continue
            mejor = {}  # fin_periodo -> (filed, val)
            for x in serie:
                if x.get('form') not in ('10-K', '10-K405', '10-KT'):
                    continue
                if campo in FLUJOS:
                    if 'start' not in x or not (330 <= dias(x['start'], x['end']) <= 400):
                        continue
                fin = x['end']
                if fin not in mejor or x['filed'] < mejor[fin][0]:
                    mejor[fin] = (x['filed'], x['val'])
            # Cada año usa el primer concepto de la lista que tenga dato ese año
            # (el nombre contable cambia con los años, ej. ventas en 2018).
            for fin, (filed, val) in mejor.items():
                anio = int(fin[:4]) if int(fin[5:7]) > 6 else int(fin[:4]) - 1  # año fiscal
                if campo not in filas[anio]:
                    filas[anio][campo] = val
                    if filed[:4] >= fin[:4]:
                        presentado[anio] = min(presentado.get(anio, '9999'), filed)
    return filas, presentado


def destino(subs, ult_facts=None):
    """Cómo terminó: 'vive', 'quiebra', 'comprada', 'revocada', 'desconocido' + último año con 10-K
    + años de quiebra CONFIRMADA (la que borra al accionista).
    Auditoría 2-nov: una quiebra de filial (LendingTree 2019) usa el mismo ítem 1.03, y muchas
    'desconocidas' eran fusiones o reorganizaciones; por eso estas reglas."""
    r = subs.get('filings', {}).get('recent', {})
    forms, fechas, items = r.get('form', []), r.get('filingDate', []), r.get('items', [])
    ev = sorted(zip(fechas, forms, [it or '' for it in items]))          # viejo -> nuevo
    k = [f[:4] for f, fo, _ in ev if fo in ('10-K', '10-K405', '10-KT')]
    ult_10k = int(max(k)) if k else None
    if ult_facts is not None:
        ult_10k = max(ult_10k or 0, ult_facts)
    # Quiebra confirmada: 8-K 1.03 y, dentro de 2 años, cancelación de acciones (3.03),
    # salida de bolsa (25-NSE/25), baja del registro (15-12/15-15), revocación, o fin de los 10-K.
    quiebras = []
    for f, fo, it in ev:
        if fo == '8-K' and '1.03' in it:
            a = int(f[:4])
            sigue = [x for x in ev if a <= int(x[0][:4]) <= a + 2]
            confirma = any(('3.03' in x[2] and x[1] == '8-K') or x[1] in ('25-NSE', '25', 'REVOKED')
                           or x[1].startswith('15-12') or x[1].startswith('15-15') for x in sigue)
            if confirma or (ult_10k is not None and ult_10k <= a + 1):
                quiebras.append(a)
    quiebras = sorted(set(quiebras))
    finales = ev[-25:]
    compra = (any(fo in ('DEFM14A', 'SC 14D9', 'SC TO-T', 'DEFM14C') for _, fo, _ in ev)
              or any(fo == '8-K' and '5.01' in it for _, fo, it in finales)        # cambio de control
              or any(fo in ('S-8 POS', 'POS AM') for _, fo, _ in finales))         # baja de acciones tras fusión
    revocada = any(fo == 'REVOKED' for _, fo, _ in ev)
    if quiebras:
        estado = 'quiebra'
    elif ult_10k is not None and ult_10k >= FIN_DATOS - 1:
        estado = 'vive'
    elif revocada:
        estado = 'revocada'
    elif compra:
        estado = 'comprada'
    else:
        estado = 'desconocido'
    return estado, ult_10k, quiebras


def div(a, b):
    try:
        if a is None or b is None or b == 0:
            return None
        return a / b
    except Exception:
        return None


def rasgos(f, t):
    """Ratios del año t usando sólo años <= t. Nada de montos absolutos."""
    x = f.get(t, {})
    g = lambda k, a=t: f.get(a, {}).get(k)
    ventas = g('ventas')
    deuda = (g('deuda_lp') or 0) + (g('deuda_cp') or 0) if (g('deuda_lp') is not None or g('deuda_cp') is not None) else None
    fco, capex = g('fco'), g('capex')
    fcf = fco - (capex or 0) if fco is not None else None
    r = {
        'margen_neto': div(g('res_neto'), ventas),
        'margen_op': div(g('res_op'), ventas),
        'margen_bruto': div(g('bruto'), ventas),
        'roa': div(g('res_neto'), g('activos')),
        'roe': div(g('res_neto'), g('patrimonio')),
        'deuda_activos': div(deuda, g('activos')),
        'pasivo_activos': div(g('pasivos'), g('activos')),
        'caja_activos': div(g('caja'), g('activos')),
        'deuda_neta_fco': div((deuda or 0) - (g('caja') or 0), fco) if deuda is not None else None,
        'fco_activos': div(fco, g('activos')),
        'fcf_ventas': div(fcf, ventas),
        'capex_fco': div(capex, fco),
        'recompras_fco': div(g('recompras'), fco),
        'dividendos_fco': div(g('dividendos'), fco),
        'cobertura_int': div(g('res_op'), g('intereses')),
        'id_ventas': div(g('id'), ventas),
        'devengos': div((g('res_neto') or 0) - (fco or 0), g('activos')) if fco is not None else None,
        'rotacion': div(ventas, g('activos')),
        'diferido_ventas': div(g('diferido'), ventas),
        'rpo_ventas': div(g('rpo'), ventas),
        # tamaño: sólo se usa convertido a percentil dentro del año (el monto delataría la época)
        'log_activos': math.log(g('activos')) if (g('activos') or 0) > 0 else None,
        'patrimonio_neg': (1.0 if (g('patrimonio') is not None and g('patrimonio') < 0) else 0.0),
        'sin_deuda': (1.0 if deuda == 0 else 0.0) if deuda is not None else None,
        'perdida': (1.0 if (g('res_neto') or 0) < 0 else 0.0) if g('res_neto') is not None else None,
    }
    # Historia (foso que se ensancha, estabilidad, dilución)
    v3, v1 = g('ventas', t - 3), g('ventas', t - 1)
    r['crec_ventas_1'] = div(ventas, v1) - 1 if div(ventas, v1) is not None else None
    r['crec_ventas_3'] = (div(ventas, v3) ** (1 / 3) - 1) if (div(ventas, v3) or 0) > 0 else None
    roa3 = div(g('res_neto', t - 3), g('activos', t - 3))
    r['tendencia_roa'] = r['roa'] - roa3 if (r['roa'] is not None and roa3 is not None) else None
    mops = [div(g('res_op', a), g('ventas', a)) for a in range(t - 4, t + 1)]
    mops = [m for m in mops if m is not None]
    if len(mops) >= 3:
        m = sum(mops) / len(mops)
        r['estab_margen'] = math.sqrt(sum((v - m) ** 2 for v in mops) / len(mops))
        r['margen_op_min5'] = min(mops)
    a3 = g('acciones', t - 3)
    r['dilucion_3'] = (div(g('acciones'), a3) - 1) if div(g('acciones'), a3) is not None else None
    # 'años de historia' NO va: como los datos empiezan en 2009, delata el año.
    return r


def clasicos(f, t):
    """Modelos publicados, para comparar (NUNCA son rasgos del modelo).
    Altman Z'' (1995, versión con valor contable, sin precios): más alto = más sano.
    Ohlson O (1980): más alto = más riesgo de quiebra. El tamaño va como log(activos);
    como se compara dentro de un mismo año, no hace falta el deflactor del PIB.
    Piotroski F (2000): 0 a 9 señales de calidad."""
    g = lambda k, a=t: f.get(a, {}).get(k)
    A, L = g('activos'), g('pasivos')
    ac, pc = g('activos_cte'), g('pasivos_cte')
    wc = (ac - pc) if (ac is not None and pc is not None) else None
    out = {}
    if A and L and wc is not None and g('ganancias_ret') is not None and g('res_op') is not None and g('patrimonio') is not None:
        out['altman_z2'] = 6.56 * wc / A + 3.26 * g('ganancias_ret') / A + 6.72 * g('res_op') / A + 1.05 * g('patrimonio') / L
    ni, ni1 = g('res_neto'), g('res_neto', t - 1)
    if A and A > 0 and L is not None and wc is not None and ac and pc is not None and ni is not None and g('fco') is not None and ni1 is not None and L:
        x = 1 if L > A else 0
        y = 1 if (ni < 0 and ni1 < 0) else 0
        cambio = (ni - ni1) / (abs(ni) + abs(ni1)) if (abs(ni) + abs(ni1)) else 0
        out['ohlson_o'] = (-1.32 - 0.407 * math.log(A) + 6.03 * L / A - 1.43 * wc / A + 0.0757 * pc / ac
                           - 1.72 * x - 2.37 * ni / A - 1.83 * g('fco') / L + 0.285 * y - 0.521 * cambio)
    A1 = g('activos', t - 1)
    if A and A1 and ni is not None and g('fco') is not None and ni1 is not None:
        roa, roa1 = ni / A, ni1 / A1
        sen = [roa > 0, g('fco') > 0, roa > roa1, g('fco') / A > roa]
        d, d1 = g('deuda_lp'), g('deuda_lp', t - 1)
        sen.append((d or 0) / A <= (d1 or 0) / A1)
        ac1, pc1 = g('activos_cte', t - 1), g('pasivos_cte', t - 1)
        sen.append(bool(ac and pc and ac1 and pc1 and ac / pc > ac1 / pc1))
        s0, s1 = g('acciones'), g('acciones', t - 1)
        sen.append(bool(s0 and s1 and s0 <= s1))
        b, b1, v, v1 = g('bruto'), g('bruto', t - 1), g('ventas'), g('ventas', t - 1)
        sen.append(bool(b is not None and b1 is not None and v and v1 and b / v > b1 / v1))
        sen.append(bool(v and v1 and v / A > v1 / A1))
        out['piotroski_f'] = float(sum(sen))
    return out


def valor_duenio_ps(f, t):
    """Patrimonio por acción. Las etiquetas suman los dividendos por acción cobrados en el medio."""
    return div(g2(f, t, 'patrimonio'), g2(f, t, 'acciones'))


def g2(f, t, k):
    return f.get(t, {}).get(k)


def etiquetas(f, t, estado, ult_10k, quiebras):
    e = {}
    # sobrevive_10 = el ACCIONISTA sobrevive: sin quiebra en los 10 años y sigue presentando 10-K.
    # Una empresa que sale de la quiebra cuenta como muerte (al accionista lo borraron).
    # Las compradas no son ni vida ni muerte: quedan sin etiqueta.
    h = t + 10
    q = [a for a in quiebras if t < a <= h]
    if q:
        e['sobrevive_10'] = 0
    elif h + 1 <= FIN_DATOS and ult_10k is not None and ult_10k >= h + 1:
        e['sobrevive_10'] = 1
    # duplica_6: patrimonio por acción + dividendos por acción cobrados, ×2 en 6 años
    # gana_mas_1: la pregunta del paper de Chicago Booth (Kim, Muhn, Nikolaev 2024):
    # ¿el beneficio por acción del año siguiente es mayor que el de este año?
    e0 = div(g2(f, t, 'res_neto'), g2(f, t, 'acciones'))
    e1 = div(g2(f, t + 1, 'res_neto'), g2(f, t + 1, 'acciones'))
    if e0 is not None and e1 is not None and e1 != e0:
        e['gana_mas_1'] = 1 if e1 > e0 else 0
    v0 = valor_duenio_ps(f, t)
    if v0 and v0 > 0:
        if t + 6 in f and valor_duenio_ps(f, t + 6) is not None:
            divs = 0.0
            for a in range(t + 1, t + 7):
                d = div(g2(f, a, 'dividendos'), g2(f, a, 'acciones'))
                divs += d or 0
            e['duplica_6'] = 1 if (valor_duenio_ps(f, t + 6) + divs) >= 2 * v0 else 0
        if any(t < a <= t + 6 for a in quiebras):
            e['duplica_6'] = 0
    return e


def anonimo(cik):
    return hashlib.sha256(('sal-ie-' + str(cik)).encode()).hexdigest()[:12]


def iterar(fuente, parte=0, partes=1):
    """Devuelve (nombre_archivo, json) desde carpeta o zip; sólo descomprime los de esta parte."""
    mia = lambda n: n.endswith('.json') and n.startswith('CIK') and int(n[3:13]) % partes == parte
    if os.path.isdir(fuente):
        for n in sorted(os.listdir(fuente)):
            if mia(n):
                yield n, json.load(open(os.path.join(fuente, n), encoding='utf-8'))
    else:
        z = zipfile.ZipFile(fuente)
        for n in sorted(z.namelist()):
            if mia(n):
                yield n, cargar(z.read(n))


def leer_subs(fuente, ciks):
    out = {}
    if os.path.isdir(fuente):
        for c in ciks:
            p = os.path.join(fuente, f'CIK{c}.json')
            if os.path.exists(p):
                out[c] = json.load(open(p, encoding='utf-8'))
    else:
        z = zipfile.ZipFile(fuente)
        nombres = set(z.namelist())
        for c in ciks:
            n = f'CIK{c}.json'
            if n in nombres:
                out[c] = cargar(z.read(n))
    return out


def main():
    ff, fs, salida = sys.argv[1], sys.argv[2], sys.argv[3]
    parte, partes = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 1)
    import time
    t0 = time.time()
    filas_out, n = [], 0
    pendientes = []
    # Se guarda cada 500 empresas (JSON por línea): si el reloj corta, lo hecho queda.
    fh = open(salida, 'w', encoding='utf-8')
    # Acciones en circulación (portada de cada 10-K y 10-Q): para el valor de mercado en cualquier fecha.
    # 'presentado' = cuándo se supo. Archivo aparte: <salida>-acciones.csv
    fa = open(salida.rsplit('.', 1)[0] + '-acciones.csv', 'w', encoding='utf-8')
    fa.write('id,fecha,presentado,acciones' + chr(10))
    total = 0
    def volcar(lote):
        nonlocal total
        for r in procesar(lote, fs):
            fh.write(json.dumps(r) + chr(10)); total += 1
        fh.flush()
        for cik, facts in lote:
            serie = (facts.get('facts', {}).get('dei', {}).get('EntityCommonStockSharesOutstanding', {})
                     .get('units', {}).get('shares', []))
            for x in serie:
                if x.get('val') and x.get('filed') and x.get('end'):
                    fa.write(f"{anonimo(cik)},{x['end']},{x['filed']},{x['val']}" + chr(10))
        fa.flush()
    for nombre, facts in iterar(ff, parte, partes):
        pendientes.append((nombre[3:13], facts)); n += 1
        if len(pendientes) >= 500:
            volcar(pendientes); pendientes = []
            print(f'{n} empresas, {total} filas, {time.time()-t0:.0f}s', flush=True)
    volcar(pendientes)
    fh.close(); fa.close()
    print(f'LISTO {n} empresas, {total} filas en {time.time()-t0:.0f}s -> {salida}', flush=True)


def procesar(lote, fs):
    subs = leer_subs(fs, [c for c, _ in lote])
    out = []
    for cik, facts in lote:
        try:
            out += una_empresa(cik, facts, subs.get(cik, {}))
        except Exception as e:      # una empresa rara no frena al resto
            print('salteo', cik, type(e).__name__, flush=True)
    return out


def una_empresa(cik, facts, s):
    out = []
    if True:
        sic = str(s.get('sic') or '')
        if not sic or s.get('entityType') not in (None, '', 'operating'):
            return out
        f, presentado = anuales(facts)
        # Las empresas que presentan miles de documentos (bancos grandes) no tienen ningún 10-K en la lista
        # 'recent' de la SEC: el último balance se toma también de los datos contables mismos.
        ult_facts = max((int(v[:4]) for v in presentado.values() if v and v[0] != '9'), default=None)
        estado, ult_10k, quiebras = destino(s, ult_facts)
        for t in sorted(f):
            if t < 2009 or 'activos' not in f[t] or 'ventas' not in f[t]:
                continue
            r = rasgos(f, t)
            r.update(etiquetas(f, t, estado, ult_10k, quiebras))
            r.update(clasicos(f, t))
            # Montos crudos OCULTOS (empiezan con _): nunca son rasgos; sólo sirven para calcular
            # valor de mercado y retorno con precios (precio.py). La fecha es la de presentación del balance.
            x = f[t]
            deuda = (x.get('deuda_lp') or 0) + (x.get('deuda_cp') or 0)
            for k in ('acciones', 'res_neto', 'fco', 'capex', 'patrimonio', 'caja', 'res_op',
                      'dividendos', 'recompras', 'emisiones'):
                r['_' + k] = x.get(k)
            r['_deuda'] = deuda
            r['_presentado'] = presentado.get(t) if presentado.get(t, '9')[0] != '9' else None
            r['id'] = anonimo(cik)
            r['anio'] = t                      # sólo para partir; nunca es rasgo
            r['sector'] = sic[:1]              # división SIC de un dígito, nada más fino
            r['financiera'] = 1 if sic[:2] in ('60', '61', '62', '63', '64', '65', '66', '67') else 0
            r['estado_final'] = estado         # sólo para auditar; nunca es rasgo
            out.append(r)
    return out


if __name__ == '__main__':
    main()
