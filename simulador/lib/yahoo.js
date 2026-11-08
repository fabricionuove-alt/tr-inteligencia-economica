// Precios de Yahoo Finance (públicos, sin clave). Se cachean unos minutos en la memoria de la función.
const UA = { 'User-Agent': 'Mozilla/5.0 (simulador inteligencia-economica)' };
const cache = new Map();
async function traer(url, seg) {
  const c = cache.get(url);
  if (c && Date.now() - c.t < seg * 1000) return c.v;
  const r = await fetch(url, { headers: UA });
  if (!r.ok) throw new Error('yahoo ' + r.status);
  const v = await r.json();
  cache.set(url, { t: Date.now(), v });
  return v;
}
// Cierres diarios de varios símbolos: { SIM: { fechas: ['2026-11-04', ...], cierres: [...], ultimo, hora } }
async function cierres(simbolos, rango = '1y') {
  const out = {};
  // (06-11: las tandas de 20 van de a 6 a la vez -- una por una, las 364 de Tr tardaban 6 s --)
  const lotes = [];
  for (let i = 0; i < simbolos.length; i += 20) lotes.push(simbolos.slice(i, i + 20));
  const resp = new Array(lotes.length);
  let sig = 0;
  await Promise.all(Array.from({ length: Math.min(6, lotes.length) }, async () => {
    while (sig < lotes.length) { const k = sig++;
      const url = `https://query1.finance.yahoo.com/v7/finance/spark?symbols=${lotes[k].map(encodeURIComponent).join(',')}&range=${rango}&interval=1d`;
      try { resp[k] = await traer(url, 600); } catch (e) { resp[k] = null; } }
  }));
  for (const j of resp) {
    if (!j) continue;
    for (const r of (j.spark && j.spark.result) || []) {
      const x = r.response && r.response[0];
      if (!x || !x.timestamp) continue;
      const q = x.indicators.quote[0].close;
      const f = [], c = [];
      x.timestamp.forEach((t, k) => {
        if (q[k] == null) return;
        f.push(new Date((t + x.meta.gmtoffset) * 1000).toISOString().slice(0, 10)); c.push(q[k]);
      });
      out[r.symbol] = { fechas: f, cierres: c, ultimo: x.meta.regularMarketPrice, hora: x.meta.regularMarketTime, moneda: x.meta.currency };
    }
  }
  return out;
}
async function cotizacion(sim) {
  const j = await traer(`https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(sim)}?range=1d&interval=5m`, 60);
  const m = j.chart && j.chart.result && j.chart.result[0] && j.chart.result[0].meta;
  if (!m || m.regularMarketPrice == null) return null;
  return { simbolo: m.symbol, nombre: m.longName || m.shortName || m.symbol, precio: m.regularMarketPrice, moneda: m.currency,
           bolsa: m.fullExchangeName, tipo: m.instrumentType, cierre_anterior: m.chartPreviousClose,
           hora: new Date(m.regularMarketTime * 1000).toISOString() };
}
async function buscar(q) {
  const j = await traer(`https://query1.finance.yahoo.com/v1/finance/search?q=${encodeURIComponent(q)}&quotesCount=8&newsCount=0`, 3600);
  return (j.quotes || []).filter(x => x.quoteType === 'EQUITY' && ['NMS', 'NYQ', 'NGM', 'NCM', 'ASE', 'PCX', 'BTS'].includes(x.exchange))
    .map(x => ({ simbolo: x.symbol, nombre: x.longname || x.shortname, bolsa: x.exchDisp }));
}
module.exports = { cierres, cotizacion, buscar };
