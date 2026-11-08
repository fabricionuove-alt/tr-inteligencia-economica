// Puente al agente para los servicios gratis que no aceptan pedidos directos del navegador (Kilo) y para los mismos de
// OVH/LLM7 pero saliendo con la IP del servidor (sus topes gratis son por IP y por modelo). Sólo modelos de esta lista.
const OVH = 'https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/chat/completions';
const KILO = 'https://api.kilo.ai/api/openrouter/chat/completions';
const LLM7 = 'https://api.llm7.io/v1/chat/completions';
const PERMITIDOS = {
  'kilo:kilo-auto/free': [KILO, 'kilo-auto/free'],
  'kilo:openrouter/free': [KILO, 'openrouter/free'],
  'kilo:nemotron-ultra': [KILO, 'nvidia/nemotron-3-ultra-550b-a55b:free'],
  'kilo:nemotron-super': [KILO, 'nvidia/nemotron-3.5-super-vl:free'],
  'kilo:nemotron-lightning': [KILO, 'nvidia/nemotron-3.5-lightning:free'],
  'ovh:Qwen3.5-397B-A17B': [OVH, 'Qwen3.5-397B-A17B'],
  'ovh:Meta-Llama-3_3-70B-Instruct': [OVH, 'Meta-Llama-3_3-70B-Instruct'],
  'ovh:gpt-oss-120b': [OVH, 'gpt-oss-120b'],
  'llm7:default': [LLM7, 'default', true],
};
const leer = req => req.body !== undefined ? Promise.resolve(typeof req.body === 'string' ? JSON.parse(req.body) : req.body)
  : new Promise((ok, mal) => { let s = ''; req.on('data', d => s += d); req.on('end', () => { try { ok(JSON.parse(s)); } catch (e) { mal(e); } }); });
module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'sólo POST' });
  let b; try { b = await leer(req); } catch (e) { return res.status(400).json({ error: 'pedido ilegible' }); }
  const m = PERMITIDOS[b && b.motor];
  if (!m || !Array.isArray(b.messages)) return res.status(400).json({ error: 'motor desconocido' });
  const corte = new AbortController(), reloj = setTimeout(() => corte.abort(), 25000);
  try {
    const r = await fetch(m[0], { method: 'POST', signal: corte.signal, headers: { 'Content-Type': 'application/json', ...(m[2] ? { Authorization: 'Bearer sin-clave' } : {}) },
      body: JSON.stringify({ model: m[1], messages: b.messages.slice(-60), tools: b.tools, tool_choice: 'auto' }) });
    const t = await r.text();
    res.statusCode = r.status; res.setHeader('Content-Type', 'application/json'); res.setHeader('Cache-Control', 'no-store'); res.end(t);
  } catch (e) { res.status(502).json({ error: 'el servicio no respondió' }); }
  finally { clearTimeout(reloj); }
};
