// La cartera de Tr: su lista congelada de 2025 (Tr con Gemma), con los pesos de su cartera Kelly, comprada el día que empezó el jugador.
// Devuelve sólo el valor, nunca las empresas.
const { cierres } = require('../lib/yahoo');
const IA = require('../lib/ia.json');
module.exports = async (req, res) => {
  const desde = String(req.query.desde || '').slice(0, 10);
  const capital = Number(req.query.capital) || 10000;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(desde)) return res.status(400).json({ error: 'falta desde' });
  try {
    const C = await cierres(IA.tickers, '2y');
    const hoy = new Date().toISOString().slice(0, 10);
    const fechas = [...new Set(Object.values(C).flatMap(x => x.fechas))].filter(f => f >= desde).sort();
    if (!fechas.length || fechas[fechas.length - 1] < hoy) fechas.push(hoy);
    // precio de compra: el último cierre hasta 'desde' (si empezó hoy, el precio de ahora)
    const precioEn = (x, f) => { let p = null; for (let k = 0; k < x.fechas.length && x.fechas[k] <= f; k++) p = x.cierres[k]; return p; };
    const peso = {}; IA.tickers.forEach((t, i) => { peso[t] = IA.pesos ? IA.pesos[i] : 1; });
    const lista = Object.entries(C).map(([t, x]) => ({ x, w: peso[t] ?? 0, compra: precioEn(x, desde) ?? x.ultimo })).filter(o => o.compra > 0 && o.w > 0);
    const n = lista.length, total = lista.reduce((s, o) => s + o.w, 0);
    const valores = fechas.map(f => lista.reduce((s, o) => s + capital * (o.w / total) * ((f === hoy ? o.x.ultimo : precioEn(o.x, f)) ?? o.compra) / o.compra, 0));
    res.setHeader('Cache-Control', 's-maxage=600, stale-while-revalidate=1200');
    res.json({ desde, capital, empresas: n, fechas, valores: valores.map(v => Math.round(v * 100) / 100), sha256: IA.sha256 });
  } catch (e) { res.status(502).json({ error: 'sin precios ahora' }); }
};
