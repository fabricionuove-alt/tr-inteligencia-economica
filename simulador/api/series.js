// Cierres diarios de las acciones del jugador, para dibujar su cartera.
const { cierres } = require('../lib/yahoo');
module.exports = async (req, res) => {
  const s = String(req.query.s || '').split(',').map(x => x.trim().toUpperCase()).filter(x => /^[A-Z0-9\-]{1,10}$/.test(x)).slice(0, 60);
  try { res.setHeader('Cache-Control', 's-maxage=600'); res.json(s.length ? await cierres(s) : {}); }
  catch (e) { res.status(502).json({ error: 'sin series' }); }
};
