const { cotizacion } = require('../lib/yahoo');
module.exports = async (req, res) => {
  const s = String(req.query.s || '').toUpperCase().trim().replace('.', '-');
  if (!/^[A-Z0-9\-]{1,10}$/.test(s)) return res.status(400).json({ error: 'símbolo inválido' });
  try {
    const c = await cotizacion(s);
    if (!c) return res.status(404).json({ error: 'no encontrado' });
    if (c.moneda !== 'USD' || c.tipo !== 'EQUITY') return res.status(404).json({ error: 'sólo acciones de Estados Unidos en dólares' });
    res.setHeader('Cache-Control', 's-maxage=30, stale-while-revalidate=60');
    res.json(c);
  } catch (e) { res.status(502).json({ error: 'sin precio ahora' }); }
};
