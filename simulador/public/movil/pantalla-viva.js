// LA PANTALLA EN VIVO SOBRE LA FOTO (08-11, versión celular): sin 3D. Tres imágenes sacadas de la web con su misma cámara
// (index.html ?captura=…, ver dispositivo-rampa notas):
//   aparato-negro.webp  el aparato con la pantalla apagada (queda el vidrio con su reflejo)
//   pantalla-uv.webp    para cada píxel de la foto, qué punto de la pantalla muestra (u, v de la tela, 12 bits cada uno,
//                       empaquetados en RGB sin pérdida; 0 = no es pantalla)
// La pantalla se dibuja acá en un canvas -- la misma web del escritorio, con los números de verdad -- y un shader de
// WebGL la pega sobre la foto siguiendo ese mapa (con la curva de la pantalla incluida): foto + pantalla × brillo.
// Si no hay WebGL2, queda la foto común.
const W = 1280, H = 961, TOPE = 231, BARRA = 52, BANDA = 48, GANANCIA = 0.76;      // (la tela de la web a escala 1; ganancia medida: blanco suma ~200)
const C = { fondo: '#111', gris: '#8a8a85', lima: '#e2ff32', blanco: '#f6f5f0', salmon: '#ff6a5a', menta: '#dce7d8', negro: '#0b0b0b' };
const F = (peso, px) => `${peso} ${px}px "Inter Tight", system-ui, sans-serif`;
const ALTO_MAX = 2600;      // (la web entera: duelo, agente, cartera y pie; la pantalla muestra H - BANDA de alto)
const tela = document.createElement('canvas'); tela.width = W; tela.height = ALTO_MAX;
const cintaTela = document.createElement('canvas'); cintaTela.width = W; cintaTela.height = BANDA;
let g = tela.getContext('2d');

function capsula(x, y, texto, px, color) {
  g.font = F(500, px); const w = g.measureText(texto).width + 32, h = px * 1.2 + 10;
  g.strokeStyle = color; g.fillStyle = color; g.lineWidth = 1.5; g.beginPath(); g.roundRect(x, y, w, h, h / 2); g.stroke();
  g.textBaseline = 'middle'; g.fillText(texto, x + 16, y + h / 2 + .5); g.textBaseline = 'alphabetic';
}
function curva(ys, x, y, w, h, lo, hi) {
  const n = ys.length; if (!n) return;
  const pts = (n === 1 ? [ys[0], ys[0]] : ys).map((v, i, a) => [x + i / (a.length - 1) * w, y + h - 10 - (v - lo) / (hi - lo || 1) * (h - 20)]);
  g.strokeStyle = C.negro; g.lineWidth = 1.6; g.lineCap = g.lineJoin = 'round'; g.beginPath(); g.moveTo(...pts[0]);
  for (let i = 1; i < pts.length; i++) { const p0 = pts[i - 2] || pts[i - 1], p1 = pts[i - 1], p2 = pts[i], p3 = pts[i + 1] || p2;
    g.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]); }
  g.stroke();
}
const colorDe = p => p >= 5 ? C.lima : p >= 0 ? C.blanco : C.salmon;
function carta(x, y, w, h, nombre, p, serie, lo, hi, datos) {      // (la carta de la web de escritorio)
  g.fillStyle = colorDe(p); g.beginPath(); g.roundRect(x, y, w, h, 18); g.fill();
  const ix = x + 22, iw = w - 44;
  capsula(ix, y + 22, nombre, 17, C.negro);
  { g.font = F(500, 14); const tx = nombre === 'Tr' ? 'Cómo piensa Tr →' : 'Todos los jugadores →', wc = g.measureText(tx).width + 28, hc = 14 * 1.2 + 10, cx = x + w - 22 - wc;
    g.fillStyle = C.negro; g.beginPath(); g.roundRect(cx, y + 24, wc, hc, hc / 2); g.fill(); g.fillStyle = '#fff'; g.textBaseline = 'middle'; g.fillText(tx, cx + 14, y + 24 + hc / 2 + .5); g.textBaseline = 'alphabetic'; }
  curva(serie, ix, y + 80, iw, 170, lo, hi);
  const gp = 79, yGrande = y + h - 20 - gp * .95 * .12;
  g.fillStyle = C.negro; g.font = F(700, gp); g.letterSpacing = (-.045 * gp) + 'px';
  const t = p == null ? '—' : pct(p).replace('%', ''); g.fillText(t, ix, yGrande); const wt = g.measureText(t).width; g.letterSpacing = '0px';
  if (p != null) { g.font = F(700, gp * .42); g.fillText('%', ix + wt + 2, yGrande); }
  const yDatos = y + h - 20 - gp * .95 - 18 - 92, cw = (iw - 14) / 2;
  g.font = F(400, 12.5);
  datos.forEach(([em, val], i) => {
    const cx = ix + (i % 2) * (cw + 14), cy = yDatos + Math.floor(i / 2) * 46;
    g.fillStyle = 'rgba(0,0,0,.55)'; g.fillRect(cx, cy, cw, 1); if (i >= 2) g.fillRect(cx, cy + 46, cw, 1);
    g.fillStyle = 'rgba(11,11,11,.65)'; g.fillText(em, cx, cy + 20); g.fillStyle = C.negro; g.fillText(val, cx, cy + 38);
  });
}
function renglones(t, ancho) {
  const out = [];
  for (const par of String(t).split('\n')) { let l = ''; for (const p of par.split(/\s+/)) { const k = l ? l + ' ' + p : p; if (g.measureText(k).width > ancho && l) { out.push(l); l = p; } else l = k; } out.push(l); }
  return out;
}
function chat(x, y, w, h, mensajes) {
  g.fillStyle = C.menta; g.beginPath(); g.roundRect(x, y, w, h, 18); g.fill();
  capsula(x + 22, y + 22, 'Agente', 17, C.negro);
  g.font = F(500, 16); const ab = g.measureText('Enviar').width + 40, fy = y + h - 18 - 45, ix = x + 18, iw = w - 36 - 8 - ab;
  g.strokeStyle = C.negro; g.lineWidth = 1.5; g.beginPath(); g.roundRect(ix, fy, iw, 45, 22.5); g.stroke();
  g.font = F(400, 16); g.fillStyle = 'rgba(0,0,0,.45)'; g.fillText('«Comprá 10 acciones de Apple»', ix + 18, fy + 28);
  g.fillStyle = C.negro; g.beginPath(); g.roundRect(ix + iw + 8, fy, ab, 45, 22.5); g.fill(); g.fillStyle = '#fff'; g.font = F(500, 16); g.fillText('Enviar', ix + iw + 28, fy + 28);
  const top = y + 68, maxW = (w - 44) * .9; let yy = fy - 24;
  g.save(); g.beginPath(); g.rect(x, top, w, yy - top + 10); g.clip();
  for (let i = mensajes.length - 1; i >= 0 && yy > top; i--) {
    const b = mensajes[i], yo = b.c === 'yo'; g.font = F(400, 15.5);
    const ls = renglones(b.t, maxW - 28).slice(0, 6), bh = ls.length * 22 + 18, bw = Math.min(maxW, Math.max(...ls.map(l => g.measureText(l).width)) + 28);
    yy -= bh; const bx = yo ? x + w - 22 - bw : x + 22;
    g.fillStyle = yo ? C.negro : b.c === 'pensando' ? C.lima : 'rgba(255,255,255,.65)'; g.beginPath(); g.roundRect(bx, yy, bw, bh, yo ? [16, 16, 4, 16] : [16, 16, 16, 4]); g.fill();
    g.fillStyle = yo ? '#fff' : C.negro; ls.forEach((l, k) => g.fillText(l, bx + 14, yy + 4 + (k + 1) * 22)); yy -= 10;
  }
  g.restore();
}
// dibuja la web entera (como la del escritorio) en la tela alta, desde y = 0; devuelve su alto
function dibujarTela(d) {
  g = tela.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = C.fondo; g.fillRect(0, 0, W, ALTO_MAX);
  g.fillStyle = '#262626'; g.fillRect(0, BARRA - 1, W, 1);
  g.font = F(600, 13); g.letterSpacing = (.06 * 13) + 'px'; g.fillStyle = '#fff'; g.fillText('VOS VS TR', 24, 32); g.letterSpacing = '0px';
  if (d.hora) { g.font = F(400, 15); g.fillStyle = C.gris; g.textAlign = 'right'; g.fillText(d.hora, W - 24, 33); g.textAlign = 'left'; }
  const y0 = 66, fr = (W - 48 - 40) / 3.25, Hc = 520;
  if (d.vos) {
    const todos = [...d.vos, ...d.ia], mid = (Math.min(...todos) + Math.max(...todos)) / 2, med = Math.max((Math.max(...todos) - Math.min(...todos)) / 2, CAPITAL * .01);
    carta(24, y0, fr, Hc, 'Vos', d.pV, d.vos, mid - med, mid + med, [['Valor', usd(d.vV)], ['Caja', usd(d.caja)], ['Desde', d.desde], ['Acciones', String(d.acciones)]]);
    carta(24 + fr + 20, y0, fr, Hc, 'Tr', d.pI, d.ia, mid - med, mid + med, [['Valor', usd(d.vI)], ['Empresas', String(d.empresas)], ['Desde', d.desde], ['Lista', d.lista]]);
  } else for (const [i, n] of [[0, 'Vos'], [1, 'Tr']]) carta(24 + i * (fr + 20), y0, fr, Hc, n, null, [], 0, 1, [['Valor', '—'], ['', '—'], ['Desde', '—'], ['', '—']]);
  chat(24 + 2 * (fr + 20), y0, fr * 1.25, Hc, d.mensajes || []);
  // la cartera (como la del escritorio: renglones grandes, monto a la derecha)
  let y = y0 + Hc + 40;
  capsula(24, y, 'Cartera', 16, '#fff'); y += 16 * 1.2 + 10 + 14;
  const gn = Math.min(56, Math.max(28, W * .042)), cMo = W - 24, corto = v => usd(v).replace(/,\d\d$/, '');
  for (const [i, f] of [...(d.filas || []), { s: 'USD', nom: 'Caja', v: d.caja, r: null }].entries()) {
    g.globalAlpha = i === 3 ? .75 : i === 4 ? .55 : i >= 5 ? .4 : 1;
    const base = y + 6 + gn * 1.1 * .8;
    g.font = F(400, gn); g.letterSpacing = (-.03 * gn) + 'px'; g.fillStyle = '#fff';
    g.textAlign = 'right'; g.fillText(corto(f.v || 0), cMo, base); const wMo = g.measureText(corto(f.v || 0)).width; g.textAlign = 'left';
    const xTk = cMo - wMo - 16 - 120 - 16 - 110, xVa = xTk + 110 + 16;
    let nom = f.nom; while (g.measureText(nom).width > xTk - 16 - 24 - 30 && nom.length > 2) nom = nom.slice(0, -2) + '…';
    g.fillText(nom, 24, base); g.letterSpacing = '0px';
    g.font = F(400, 14); g.fillStyle = C.gris; g.fillText(f.s, xTk, base);
    if (f.r != null) { g.fillStyle = f.r >= 0 ? C.lima : C.salmon; g.fillText(pct(f.r), xVa, base); }
    y += gn * 1.1 + 12;
  }
  g.globalAlpha = 1;
  y += 32; g.font = F(400, 12.5); g.fillStyle = C.gris;
  if (d.pie) { const ls = renglones(d.pie, 12.5 * 70 * .5); ls.forEach((l, i) => g.fillText(l, 24, y + 14 + i * 18)); y += ls.length * 18; }
  y += 96;
  // la cinta, fija abajo
  const c = cintaTela.getContext('2d'); c.fillStyle = C.fondo; c.fillRect(0, 0, W, BANDA); c.fillStyle = '#262626'; c.fillRect(0, 0, W, 1);
  c.font = F(600, 20); let x = 24;
  for (const [t, col] of d.cinta || []) { c.fillStyle = col; c.fillText(t, x, 31); x += c.measureText(t).width; if (x > W) break; }
  return Math.min(ALTO_MAX, y + BANDA);
}

// ---- WebGL2: foto + pantalla siguiendo el mapa ----
const VS = `#version 300 es
in vec2 a; out vec2 p; void main() { p = vec2(a.x * .5 + .5, .5 - a.y * .5); gl_Position = vec4(a, 0., 1.); }`;
const FS = () => `#version 300 es
precision highp float; precision highp int;
uniform sampler2D base, mapa, ui, cinta; uniform float gan, scroll; in vec2 p; out vec4 o;
void main() {
  vec3 b = texture(base, p).rgb;
  ivec2 t = ivec2(p * vec2(textureSize(mapa, 0)));
  ivec3 m = ivec3(texelFetch(mapa, t, 0).rgb * 255. + .5);
  int U = (m.r << 4) | (m.g >> 4), V = ((m.g & 15) << 8) | m.b;
  if (U == 0) { o = vec4(b, 1.); return; }
  float u = float(U - 1) / 4094., ty = float(V) / 4095. * ${H}.;      // (y en la tela del escritorio: ${H} de alto)
  vec3 s;
  if (ty >= ${H - BANDA}.) s = texture(cinta, vec2(u, (ty - ${H - BANDA}.) / ${BANDA}.)).rgb;
  else { float wy = ty + scroll; s = wy < 0. ? vec3(0.) : texture(ui, vec2(u, wy / ${ALTO_MAX}.)).rgb; }
  o = vec4(min(b + s * gan, 1.), 1.);
}`;
const imagen = async ruta => createImageBitmap(await (await fetch(ruta)).blob(), { colorSpaceConversion: 'none', premultiplyAlpha: 'none' });
export async function armar(contenedor, ruta = 'movil/') {
  const lienzo = document.createElement('canvas'), gl = lienzo.getContext('webgl2', { antialias: false, premultipliedAlpha: false });
  if (!gl) return null;
  const [base, mapa] = await Promise.all([imagen(ruta + 'aparato-negro.webp'), imagen(ruta + 'pantalla-uv.webp')]);
  lienzo.width = base.width; lienzo.height = base.height; lienzo.className = 'viva';
  const sh = (t, s) => { const x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); if (!gl.getShaderParameter(x, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(x)); return x; };
  const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS())); gl.linkProgram(pr); gl.useProgram(pr);
  const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const la = gl.getAttribLocation(pr, 'a'); gl.enableVertexAttribArray(la); gl.vertexAttribPointer(la, 2, gl.FLOAT, false, 0, 0);
  gl.pixelStorei(gl.UNPACK_COLORSPACE_CONVERSION_WEBGL, gl.NONE); gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
  const tex = (unidad, fuente, filtro) => { const t = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + unidad); gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, filtro); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, filtro);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, fuente); return t; };
  tex(0, base, gl.LINEAR); tex(1, mapa, gl.NEAREST); const tUi = tex(2, tela, gl.LINEAR), tCinta = tex(3, cintaTela, gl.LINEAR);
  gl.uniform1i(gl.getUniformLocation(pr, 'base'), 0); gl.uniform1i(gl.getUniformLocation(pr, 'mapa'), 1); gl.uniform1i(gl.getUniformLocation(pr, 'ui'), 2); gl.uniform1i(gl.getUniformLocation(pr, 'cinta'), 3);
  const uScroll = gl.getUniformLocation(pr, 'scroll'); let alto = H, fraccion = 0;
  // el scroll de la pantalla: de arriba de todo (SMIN, como entra el escritorio) hasta el pie, según cuánto bajó la página
  const correr = () => { gl.uniform1f(uScroll, -TOPE + fraccion * Math.max(0, alto - H + TOPE)); gl.drawArrays(gl.TRIANGLES, 0, 3); };
  gl.uniform1f(gl.getUniformLocation(pr, 'gan'), GANANCIA);
  gl.viewport(0, 0, lienzo.width, lienzo.height);
  contenedor.appendChild(lienzo);
  return {
    pintar(d) {      // (cada vez que cambian los números o el chat)
      alto = dibujarTela(d);
      gl.activeTexture(gl.TEXTURE2); gl.bindTexture(gl.TEXTURE_2D, tUi); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, tela);
      gl.activeTexture(gl.TEXTURE3); gl.bindTexture(gl.TEXTURE_2D, tCinta); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cintaTela);
      correr(); contenedor.classList.add('en-vivo');
    },
    scroll(f) { fraccion = Math.min(1, Math.max(0, f)); correr(); },      // (0 = arriba de todo, 1 = el pie; sólo corre, no redibuja)
  };
}
