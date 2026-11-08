// Servidor local para probar: sirve public/ y ejecuta api/*.js como en Vercel.
const http = require('http'), fs = require('fs'), path = require('path'), url = require('url');
http.createServer(async (req, res) => {
  const u = url.parse(req.url, true);
  if (u.pathname.startsWith('/api/')) {
    const f = path.join(__dirname, 'api', path.basename(u.pathname) + '.js');
    if (!fs.existsSync(f)) { res.statusCode = 404; return res.end(); }
    req.query = u.query;
    res.status = c => { res.statusCode = c; return res; };
    res.json = o => { res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(o)); };
    return require(f)(req, res);
  }
  const f = path.join(__dirname, 'public', u.pathname === '/' ? 'index.html' : u.pathname);
  if (!fs.existsSync(f)) { res.statusCode = 404; return res.end(); }
  const T = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.glb': 'model/gltf-binary', '.png': 'image/png', '.json': 'application/json' };
  res.setHeader('Content-Type', T[path.extname(f)] || 'application/octet-stream');
  fs.createReadStream(f).pipe(res);
}).listen(5710, () => console.log('http://localhost:5710'));
