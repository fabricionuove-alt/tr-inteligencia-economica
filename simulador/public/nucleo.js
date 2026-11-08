const CAPITAL = 10000, CLAVE = 'vos-contra-la-ia-v1', MODELO = 'claude-sonnet-5-5';
const hoyNY = () => new Date().toLocaleDateString('en-CA', { timeZone: 'America/New_York' });
// (los formateadores se crean una vez: toLocaleString con opciones arma uno nuevo en cada llamada, y la pantalla
//  formatea cientos de números en cada redibujo)
const F_USD = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 }), F_PCT = new Intl.NumberFormat('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const usd = v => F_USD.format(v);
const pct = v => (v >= 0 ? '+' : '') + F_PCT.format(v) + '%';

// ---------- partida (en este navegador) ----------
function nueva() { return { inicio: hoyNY(), caja: CAPITAL, pos: {}, ops: [], chat: [] }; }
let P;
try { P = JSON.parse(localStorage.getItem(CLAVE)) || nueva(); } catch (e) { P = nueva(); }
const guardar = () => { try { localStorage.setItem(CLAVE, JSON.stringify(P)); } catch (e) {} };
guardar();

// ---------- el jugador en la lista de todos (07-11): un id y un nombre que sobreviven a reiniciar la partida ----------
let JUG;
try { JUG = JSON.parse(localStorage.getItem('vosvstr:jugador')); } catch (e) {}
if (!JUG || !JUG.id) { const az = () => Math.random().toString(36).slice(2, 8); JUG = { id: az() + az(), nombre: 'Jugador ' + az().slice(0, 4).toUpperCase() }; }
const guardarJug = () => { try { localStorage.setItem('vosvstr:jugador', JSON.stringify(JUG)); } catch (e) {} };
guardarJug();
let ultimoPublicado = '';
function publicar(vos, tr) {      // (se manda cuando cambia algo: valor redondeado, nombre o acciones)
  if (!(vos >= 0) || !(tr > 0)) return;
  const d = { id: JUG.id, nombre: JUG.nombre, inicio: P.inicio, vos, tr, acciones: Object.keys(P.pos).length };
  const firma = [d.nombre, d.inicio, Math.round(vos), Math.round(tr), d.acciones].join('|');
  if (firma === ultimoPublicado) return; ultimoPublicado = firma;
  fetch('/api/jugadores', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) }).catch(() => { ultimoPublicado = ''; });
}
const precios = {};                      // último precio conocido por símbolo
async function api(ruta) { const r = await fetch(ruta); const j = await r.json(); if (!r.ok) throw new Error(j.error || 'error'); return j; }
let elegida = null;                       // la última acción que se nombró: la usan los mandos COMPRAR y VENDER
async function precio(s, elegir = true) { const c = await api('/api/precio?s=' + encodeURIComponent(s)); precios[c.simbolo] = c.precio; if (elegir) { elegida = c; if (typeof alElegir === 'function') alElegir(c); } return c; }

// ---------- herramientas del agente ----------
const H = {
  async buscar_empresa({ texto }) { return await api('/api/buscar?q=' + encodeURIComponent(texto)); },
  async precio({ simbolo }) { return await precio(simbolo); },
  async comprar({ simbolo, cantidad, dolares }) {
    const c = await precio(simbolo);
    let n = cantidad != null ? Number(cantidad) : Number(dolares) / c.precio;
    n = Math.floor(n * 10000) / 10000;
    if (!(n > 0)) return { error: 'cantidad inválida' };
    const total = n * c.precio;
    if (total > P.caja + 1e-6) return { error: 'no alcanza la caja', caja: P.caja, costo: total, maximo: Math.floor(P.caja / c.precio * 10000) / 10000 };
    const p = P.pos[c.simbolo] || { cantidad: 0, costo: 0, nombre: c.nombre };
    p.cantidad += n; p.costo += total; P.pos[c.simbolo] = p; P.caja -= total;
    P.ops.push({ fecha: hoyNY(), hora: new Date().toISOString(), tipo: 'compra', simbolo: c.simbolo, cantidad: n, precio: c.precio });
    guardar(); nota(`Compra: ${n} ${c.simbolo} a ${usd(c.precio)} = ${usd(total)}`); refrescar();
    return { hecho: true, simbolo: c.simbolo, nombre: c.nombre, cantidad: n, precio: c.precio, total, caja: P.caja, hora_precio: c.hora };
  },
  async vender({ simbolo, cantidad, todo }) {
    const s = String(simbolo).toUpperCase().replace('.', '-'), p = P.pos[s];
    if (!p) return { error: 'no tenés ' + s };
    let n = todo ? p.cantidad : Math.floor(Number(cantidad) * 10000) / 10000;
    if (!(n > 0) || n > p.cantidad + 1e-9) return { error: 'cantidad inválida', tenes: p.cantidad };
    const c = await precio(s), total = n * c.precio, costoParte = p.costo * n / p.cantidad;
    p.cantidad -= n; p.costo -= costoParte; P.caja += total;
    if (p.cantidad < 1e-9) delete P.pos[s];
    P.ops.push({ fecha: hoyNY(), hora: new Date().toISOString(), tipo: 'venta', simbolo: s, cantidad: n, precio: c.precio });
    guardar(); nota(`Venta: ${n} ${s} a ${usd(c.precio)} = ${usd(total)}`); refrescar();
    return { hecho: true, simbolo: s, cantidad: n, precio: c.precio, total, resultado: total - costoParte, caja: P.caja };
  },
  async ver_cartera() {
    await Promise.all(Object.keys(P.pos).map(s => precio(s, false).catch(() => null)));
    const pos = Object.entries(P.pos).map(([s, p]) => ({ simbolo: s, nombre: p.nombre, cantidad: p.cantidad, precio: precios[s], valor: p.cantidad * (precios[s] || 0), costo: p.costo }));
    const total = P.caja + pos.reduce((a, x) => a + x.valor, 0);
    return { inicio: P.inicio, capital_inicial: CAPITAL, caja: P.caja, posiciones: pos, total, rendimiento_pct: (total / CAPITAL - 1) * 100 };
  },
  async comparar_con_ia() {
    const ia = await api(`/api/ia?desde=${P.inicio}&capital=${CAPITAL}`), yo = await H.ver_cartera();
    const v = ia.valores[ia.valores.length - 1];
    return { desde: P.inicio, vos: yo.total, vos_pct: yo.rendimiento_pct, ia: v, ia_pct: (v / CAPITAL - 1) * 100, empresas_de_la_ia: ia.empresas };
  },
  async cambiar_nombre({ nombre }) {
    const n = String(nombre || '').replace(/\s+/g, ' ').trim().slice(0, 24);
    if (!n) return { error: 'nombre vacío' };
    JUG.nombre = n; guardarJug(); ultimoPublicado = ''; refrescar();
    return { hecho: true, nombre: n };
  },
  async reiniciar_partida({ confirmado }) {
    if (!confirmado) return { error: 'pedile confirmación al jugador antes' };
    P = nueva(); guardar(); limpiarChat(); refrescar();
    return { hecho: true, inicio: P.inicio, caja: P.caja };
  },
};
const fn = (name, description, properties = {}, required = []) => ({ type: 'function', function: { name, description, parameters: { type: 'object', properties, required } } });
const TOOLS = [
  fn('buscar_empresa', 'Busca el símbolo bursátil de una empresa de EE. UU. por nombre.', { texto: { type: 'string' } }, ['texto']),
  fn('precio', 'Precio actual de una acción (símbolo, por ejemplo AAPL).', { simbolo: { type: 'string' } }, ['simbolo']),
  fn('comprar', 'Compra al precio actual. Usar cantidad (acciones) o dolares (monto).', { simbolo: { type: 'string' }, cantidad: { type: 'number' }, dolares: { type: 'number' } }, ['simbolo']),
  fn('vender', 'Vende al precio actual. Usar cantidad o todo=true.', { simbolo: { type: 'string' }, cantidad: { type: 'number' }, todo: { type: 'boolean' } }, ['simbolo']),
  fn('ver_cartera', 'Caja, posiciones, valor total y rendimiento del jugador.'),
  fn('comparar_con_ia', 'Cómo le va al jugador contra Tr desde el día que empezó.'),
  fn('cambiar_nombre', 'Cambia el nombre con el que el jugador aparece en la lista de todos los jugadores.', { nombre: { type: 'string' } }, ['nombre']),
  fn('reiniciar_partida', 'Borra la partida y empieza de nuevo con 10.000 dólares. Sólo con confirmación explícita del jugador.', { confirmado: { type: 'boolean' } }, ['confirmado']),
];
const SISTEMA = `Sos el agente de un simulador de bolsa con dinero ficticio. El jugador empezó con 10.000 dólares y opera acciones de EE. UU. sólo a través tuyo. Compite contra Tr, una IA que eligió su cartera con balances de la SEC y la mantiene un año.
Reglas:
- Resolvé vos y operá directo, sin pedir aclaraciones que puedas decidir solo:
  · Si pide un sector o tema («empresas de seguridad informática», «petroleras», «las de IA»), elegí vos 3 a 5 empresas representativas que coticen en EE. UU. (las conocés; confirmá cada símbolo con precio) y comprá.
  · Si no dice cuánto, poné 1.000 dólares en total, repartidos en partes iguales, y decilo.
  · Si no sabés el símbolo de una empresa, usá buscar_empresa.
- Preguntá sólo si no hay forma razonable de entender el pedido.
- Si dice cómo quiere llamarse o aparecer en la lista de jugadores, usá cambiar_nombre.
- Nunca inventes precios ni resultados: usá siempre las herramientas.
- Después de operar, decí en una o dos líneas qué se hizo, a qué precio y cuánta caja queda.
- Acá todo es dinero ficticio. Si quiere invertir dinero real, decile que use el candado de abajo de la página: abre una cuenta en Alpaca, un bróker regulado de EE. UU., y opera ahí, por fuera del juego.
- No sabés qué empresas tiene Tr: se revelan al cumplirse el año.
- Respondé corto, en castellano rioplatense.`;

// ---------- EL AGENTE, POR SERVICIOS GRATIS SIN CUENTA NI CLAVE (06-11, ampliado) ----------
// Los gratis sin clave tienen un tope de ~2 pedidos por minuto POR MODELO y por IP: por eso se rota entre muchos modelos
// (cada pedido arranca por el siguiente) y el que responde 429 descansa un minuto. Dos caminos:
//   directo desde el navegador (la IP de cada jugador): OVHcloud AI Endpoints y LLM7
//   por /api/chat (la IP del servidor): Kilo -- no acepta pedidos del navegador -- y los mejores de OVH y LLM7 otra vez
// Todos probados con las herramientas del agente el 06-11. 07-11: re-probados uno por uno (scratchpad motores.mjs, «comprá 2
// acciones de Coca-Cola», dos vueltas): 14 de 15 bien en 1,7-5 s; Qwen3.8-27B y Qwen3.6-27B quitados (se colgaban >25 s).
const OVH = 'https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/chat/completions', LLM7 = 'https://api.llm7.io/v1/chat/completions';
const IA = {
  POOL: [
    { url: OVH, modelo: 'Qwen3.5-397B-A17B' },
    { puente: 'kilo:kilo-auto/free' },
    { url: OVH, modelo: 'Meta-Llama-3_3-70B-Instruct' },
    { puente: 'kilo:nemotron-ultra' },
    { url: OVH, modelo: 'gpt-oss-120b' },
    { puente: 'kilo:openrouter/free' },
    { puente: 'ovh:Qwen3.5-397B-A17B' },
    { puente: 'kilo:nemotron-super' },
    { url: OVH, modelo: 'Mistral-Small-3.2-24B-Instruct-2506' },
    { puente: 'ovh:Meta-Llama-3_3-70B-Instruct' },
    { url: LLM7, modelo: 'default', auth: true },
    { puente: 'kilo:nemotron-lightning' },
    { url: OVH, modelo: 'gpt-oss-20b' },
    { puente: 'ovh:gpt-oss-120b' },
    { puente: 'llm7:default' },
  ],
  i: 0,
  listo() { return true; },
  async entrar() {},
  async uno(m, mensajes, herramientas) {
    const corte = new AbortController(), reloj = setTimeout(() => corte.abort(), 12000);
    const r = await (m.puente
      ? fetch('/api/chat', { method: 'POST', signal: corte.signal, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ motor: m.puente, messages: mensajes, tools: herramientas }) })
      : fetch(m.url, { method: 'POST', signal: corte.signal, headers: Object.assign({ 'Content-Type': 'application/json' }, m.auth ? { Authorization: 'Bearer sin-clave' } : {}),      // (OVHcloud rechaza una clave inventada: sin encabezado)
          body: JSON.stringify({ model: m.modelo, messages: mensajes, tools: herramientas, tool_choice: 'auto' }) })).finally(() => clearTimeout(reloj));
    const j = await r.json().catch(() => ({}));
    if (!r.ok || !j.choices || !j.choices[0] || !j.choices[0].message) { m.hasta = Date.now() + (r.status === 429 ? 60000 : 20000); throw new Error((j.error && (j.error.message || j.error)) || j.message || ('error ' + r.status)); }
    const msg = j.choices[0].message; delete msg.reasoning; delete msg.reasoning_content; delete msg.reasoning_details; delete msg.refusal;
    if (!msg.content && !(msg.tool_calls && msg.tool_calls.length)) { m.hasta = Date.now() + 20000; throw new Error('respuesta vacía'); }
    return { message: msg };
  },
  async chat(mensajes, herramientas) {
    let ultimo = null;
    for (let vuelta = 0; vuelta < 2; vuelta++) {
      const n0 = IA.i; IA.i = (IA.i + 1) % IA.POOL.length;          // (cada pedido arranca por otro modelo: reparte el tope)
      for (let k = 0; k < IA.POOL.length; k++) {
        const m = IA.POOL[(n0 + k) % IA.POOL.length];
        if (vuelta === 0 && m.hasta > Date.now()) continue;
        try { return await IA.uno(m, mensajes, herramientas); } catch (e) { ultimo = e; }
      }
      if (vuelta === 0) await new Promise(ok => setTimeout(ok, 8000));
    }
    throw new Error('los servicios gratis no respondieron ahora (' + String(ultimo && (ultimo.message || ultimo)).slice(0, 60) + '). Probá de nuevo en un minuto');
  },
};

const texto = r => typeof r === 'string' ? r : (r?.message?.content?.[0]?.text ?? r?.message?.content ?? r?.text ?? String(r));
async function conversar(entrada) {
  P.chat.push({ role: 'user', content: entrada }); guardar();
  const hist = () => { let h = P.chat.slice(-30); const i = h.findIndex(m => m.role === 'user'); h = i > 0 ? h.slice(i) : h; return [{ role: 'system', content: SISTEMA }, ...h]; };
  for (let vuelta = 0; vuelta < 8; vuelta++) {
    let r;
    r = await IA.chat(hist(), TOOLS);
    let msg = r.message || { role: 'assistant', content: texto(r) };
    let calls = msg.tool_calls || [];
    if (!calls.length && Array.isArray(msg.content)) {                        // formato de Anthropic: bloques tool_use
      calls = msg.content.filter(b => b.type === 'tool_use').map(b => ({ id: b.id, type: 'function', function: { name: b.name, arguments: JSON.stringify(b.input || {}) } }));
      if (calls.length) msg = { role: 'assistant', content: msg.content.filter(b => b.type === 'text').map(b => b.text).join('\n'), tool_calls: calls };
    }
    P.chat.push(calls.length ? msg : { role: 'assistant', content: texto(r) });
    if (!calls.length) { guardar(); burbuja(texto(r), 'agente'); return; }
    for (const tc of calls) {
      let out;
      try { const ar = JSON.parse(tc.function.arguments || '{}'); for (const k of ['cantidad', 'dolares']) if (typeof ar[k] === 'string' && ar[k].trim() !== '') ar[k] = Number(ar[k]); if (typeof ar.todo === 'string') ar.todo = ar.todo === 'true';
        out = await H[tc.function.name](ar); } catch (e) { out = { error: String(e.message || e) }; }
      P.chat.push({ role: 'tool', tool_call_id: tc.id, content: JSON.stringify(out) });
    }
    guardar();
  }
}
// el historial no puede empezar con respuestas de herramientas huérfanas
const recortar = () => { while (P.chat.length > 60) P.chat.shift(); while (P.chat.length && P.chat[0].role !== 'user') P.chat.shift(); };

// ---------- datos para las vistas: series de Vos y de Tr desde el día que empezó ----------
// (06-11: los tres pedidos van a la vez, y el primero sale apenas carga la página -- precargar --, sin esperar al 3D)
let PRE = null;
function precargar(extra = []) {
  const simbolos = [...new Set(P.ops.map(o => o.simbolo))];
  PRE = { clave: P.inicio + '|' + P.ops.length + '|' + extra.join(','), t: Date.now(),
    ia: api(`/api/ia?desde=${P.inicio}&capital=${CAPITAL}`),
    S: api('/api/series?s=' + [...new Set([...simbolos, ...extra])].join(',')).catch(() => ({})),
    p: Promise.all(Object.keys(P.pos).map(s => precio(s, false).catch(() => null))) };
  PRE.ia.catch(() => {});
}
async function datos(extra = []) {
  const clave = P.inicio + '|' + P.ops.length + '|' + extra.join(',');
  if (!PRE || PRE.clave !== clave || Date.now() - PRE.t > 30000) precargar(extra);
  const pr = PRE; PRE = null;
  const [ia, S] = await Promise.all([pr.ia, pr.S, pr.p]);
  const hoy = hoyNY(), ultima = ia.fechas.length - 1;
  const cierre = (s, f) => { const x = S[s]; if (!x) return null; let p = null; for (let k = 0; k < x.fechas.length && x.fechas[k] <= f; k++) p = x.cierres[k]; return p; };
  const vos = ia.fechas.map((f, i) => {
    let c = CAPITAL; const q = {};
    for (const o of P.ops) if (o.fecha <= f) { const d = o.tipo === 'compra' ? 1 : -1; c -= d * o.cantidad * o.precio; q[o.simbolo] = (q[o.simbolo] || 0) + d * o.cantidad; }
    return c + Object.entries(q).reduce((a, [s, n]) => a + n * ((i === ultima && f >= hoy ? precios[s] : null) ?? cierre(s, f) ?? precios[s] ?? 0), 0);
  });
  return { ia, vos, S, fechas: ia.fechas, vV: vos[vos.length - 1], vI: ia.valores[ultima] };
}

