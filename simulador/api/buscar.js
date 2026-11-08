const { buscar } = require('../lib/yahoo');
module.exports = async (req, res) => {
  const q = String(req.query.q || '').slice(0, 60);
  if (!q) return res.status(400).json({ error: 'falta q' });
  try { res.setHeader('Cache-Control', 's-maxage=3600'); res.json(await buscar(q)); }
  catch (e) { res.status(502).json({ error: 'búsqueda caída' }); }
};
