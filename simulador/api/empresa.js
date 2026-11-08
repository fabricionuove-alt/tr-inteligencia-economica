// Qué es una empresa, para el desplegable de la cartera: sector e industria (Yahoo Finance) y el resumen de su artículo en
// Wikipedia en castellano (en inglés si no hay). Las dos fuentes son públicas y sin clave.
const UA = { 'User-Agent': 'simulador-vos-vs-tr/1.0 (herramienta educativa)' };
const SECTOR = { 'Technology': 'Tecnología', 'Healthcare': 'Salud', 'Financial Services': 'Servicios financieros', 'Consumer Cyclical': 'Consumo discrecional',
  'Consumer Defensive': 'Consumo básico', 'Energy': 'Energía', 'Industrials': 'Industria', 'Basic Materials': 'Materiales', 'Real Estate': 'Inmobiliario',
  'Utilities': 'Servicios públicos', 'Communication Services': 'Comunicaciones' };
const cache = new Map();
const json = async u => { const r = await fetch(u, { headers: UA }); if (!r.ok) throw new Error(r.status); return r.json(); };
const limpio = n => String(n || '').replace(/,?\s+(Inc\.?|Corporation|Corp\.?|Company|Co\.?|Ltd\.?|plc|S\.A\.|N\.V\.|Holdings?|Incorporated|Class [A-C])\b\.?/gi, '').replace(/\s*\(The\)|^The\s+/i, '').trim();
// (el buscador de rest.php trae la descripción corta de cada artículo: se elige el de la EMPRESA, no el del producto)
const EMPRESA = /empresa|compañ[ií]a|corporaci[oó]n|conglomerado|holding|banco|fabricante|minorista|cadena|multinacional|company|corporation|conglomerate|bank|manufacturer|retailer|multinational/i;
async function wiki(lengua, nombre) {
  const b = `https://${lengua}.wikipedia.org`;
  const s = await json(`${b}/w/rest.php/v1/search/page?q=${encodeURIComponent(nombre)}&limit=5`);
  const h = (s.pages || []).find(p => EMPRESA.test(p.description || '')); if (!h) return null;
  const r = await json(`${b}/api/rest_v1/page/summary/${encodeURIComponent(h.key)}`);
  return r.extract && r.extract.length > 40 ? { texto: r.extract, url: r.content_urls && r.content_urls.desktop.page } : null;
}
module.exports = async (req, res) => {
  const s = String(req.query.s || '').toUpperCase().trim().replace('.', '-');
  if (!/^[A-Z0-9\-]{1,10}$/.test(s)) return res.status(400).json({ error: 'símbolo inválido' });
  const c = cache.get(s); if (c && Date.now() - c.t < 864e5) { res.setHeader('Cache-Control', 's-maxage=86400'); return res.json(c.v); }
  try {
    const y = await json(`https://query1.finance.yahoo.com/v1/finance/search?q=${encodeURIComponent(s)}&quotesCount=5&newsCount=0`);
    const q = (y.quotes || []).find(x => x.symbol === s) || {};
    const nombre = q.longname || q.shortname || s, corto = limpio(nombre) || nombre;
    let w = null;
    for (const [l, n] of [['es', nombre], ['es', corto], ['en', nombre], ['en', corto]]) {
      if (w) break; try { w = await wiki(l, n); } catch (e) {}
    }
    const v = { simbolo: s, nombre, sector: SECTOR[q.sector] || q.sectorDisp || q.sector || null, industria: q.industryDisp || q.industry || null,
      bolsa: q.exchDisp || null, texto: w ? w.texto : null, fuente: w ? w.url : null };
    if (v.texto) { cache.set(s, { t: Date.now(), v }); res.setHeader('Cache-Control', 's-maxage=86400, stale-while-revalidate=604800'); }
    else res.setHeader('Cache-Control', 's-maxage=60');      // (sin texto puede ser que Wikipedia frenó: no se guarda)
    res.json(v);
  } catch (e) { res.status(502).json({ error: 'sin datos ahora' }); }
};
