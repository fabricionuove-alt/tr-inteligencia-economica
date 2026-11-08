// CÓMO VIENE CADA JUGADOR: cada navegador publica su resultado (un archivo por jugador en el Blob privado
// «vos-contra-la-ia-jugadores») y la lista los devuelve todos, del que más le gana a Tr al que más pierde.
//   POST /api/jugadores {id, nombre, inicio, vos, tr, acciones}   GET /api/jugadores
const { put, list } = require('@vercel/blob');
const limpiar = (v, n) => String(v ?? '').replace(/[\u0000-\u001f]/g, '').trim().slice(0, n);
const leer = req => req.body !== undefined ? Promise.resolve(typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {}))
  : new Promise((ok, mal) => { let s = ''; req.on('data', d => s += d); req.on('end', () => { try { ok(JSON.parse(s || '{}')); } catch (e) { mal(e); } }); });
module.exports = async (req, res) => {
  try {
    if (req.method === 'POST') {
      const b = await leer(req);
      const id = limpiar(b.id, 24).replace(/[^a-z0-9]/gi, ''), vos = Number(b.vos), tr = Number(b.tr);
      if (id.length < 8 || !(vos >= 0 && vos < 1e8) || !(tr > 0 && tr < 1e8) || !/^\d{4}-\d{2}-\d{2}$/.test(String(b.inicio))) return res.status(400).json({ error: 'datos inválidos' });
      const j = { id, nombre: limpiar(b.nombre, 24) || 'Jugador', inicio: String(b.inicio), vos: Math.round(vos * 100) / 100, tr: Math.round(tr * 100) / 100,
        acciones: Math.max(0, Math.min(999, Number(b.acciones) | 0)), cuando: new Date().toISOString() };
      await put(`jugadores/${id}.json`, JSON.stringify(j), { access: 'private', contentType: 'application/json', addRandomSuffix: false, allowOverwrite: true });
      return res.status(200).json({ ok: true });
    }
    if (req.method === 'GET') {
      const blobs = []; let cursor;
      do { const r = await list({ prefix: 'jugadores/', limit: 1000, cursor }); blobs.push(...r.blobs); cursor = r.hasMore ? r.cursor : null; } while (cursor && blobs.length < 3000);
      const todos = await Promise.all(blobs.map(async bl => {
        const r = await fetch(bl.url, { headers: { authorization: `Bearer ${process.env.BLOB_READ_WRITE_TOKEN}` } }).catch(() => null);
        return r && r.ok ? r.json().catch(() => null) : null;
      }));
      const lista = todos.filter(Boolean).map(j => ({ ...j, ventaja: (j.vos - j.tr) / 10000 * 100 })).sort((a, b) => b.ventaja - a.ventaja);
      res.setHeader('Cache-Control', 's-maxage=20, stale-while-revalidate=60');
      return res.status(200).json(lista);
    }
    res.status(405).json({ error: 'método' });
  } catch (e) { res.status(500).json({ error: String(e && e.message || e).slice(0, 200) }); }
};
