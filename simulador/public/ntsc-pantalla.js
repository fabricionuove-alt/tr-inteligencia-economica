// COPIA de wbc-gelatina/src/viewer/ntsc.js (ntscqt de JargeZ pasado a la placa) para LA PANTALLA DEL APARATO: en vez de
// procesar la pantalla entera del navegador, procesa una imagen de W × H (la web que muestra el aparato). Único cambio:
// cada etapa se dibuja a ese tamaño fijo (rtt(nodo, W, H)). (06-11: toda lectura con .level(0) -- las etapas no tienen mipmaps y
// se leen 1:1, así que da igual, pero sin eso el compilador de Windows desenrollaba cada bucle: 1,5 s de carga --) Es el mismo shader que usa guidocampodonico.com (vhs.js).
// LA SEÑAL DE TELEVISIÓN VIEJA (15-10, Fabri: «un shader retrogaming como ntscqt»): el algoritmo de ntscqt
// (github.com/JargeZ/ntscqt, app/ntsc.py, a su vez de zhuker/ntsc) pasado a la placa de video. ntscqt es Python sobre el
// procesador, cuadro a cuadro (no da para el juego en vivo); acá van los MISMOS pasos y los mismos filtros:
//   A · a YIQ; sangrado del color; paso bajo del croma antes de codificar (I a 1,3 MHz, Q a 0,6 MHz); anillado del luma
//       (el corte de frecuencias de ntscqt = un sinc horizontal);
//   B · la señal COMPUESTA: el croma montado en el luma con la subportadora (4 muestras por ciclo, fase que se invierte
//       línea a línea) + ruido de video + el salto del cabezal abajo; y decodificada de vuelta (luma = promedio de 4
//       muestras, croma = lo que sobra, demodulado): de ahí salen los arcoíris y los puntitos en los bordes. Ruido de
//       croma y de fase de croma por línea;
//   C · la cinta VHS (SP/LP/EP): onda del borde, paso bajo del luma con su realce, paso bajo del croma con su retraso,
//       mezcla vertical del croma;
//   D · nitidez de la casetera, pérdida de croma por línea, paso bajo del croma del televisor, el croma a mitad de
//       definición (como yuv420) y de vuelta a RGB.
// Los filtros de ntscqt son de un polo, tres en cascada (LowpassFilter); en la placa son su respuesta al impulso exacta,
// truncada (a³·C(k+2,2)·(1−a)^k), con la tasa de muestreo de NTSC (4 × 3,58 MHz). Una muestra = un pixel de la imagen
// chica (con el retro prendido) o «muestras por línea» a lo ancho.
import * as THREE from 'three/webgpu';
import { Fn, Loop, If, float, int, vec2, vec3, vec4, uniform, uniformArray, screenUV, screenSize, screenCoordinate, hash, frameId, rtt, mix, sin, cos, texture } from 'three/tsl';

const TASA = 315000000.0 / 88 * 4;
const CINTAS = { SP: [2400000.0, 320000.0, 9], LP: [1900000.0, 300000.0, 12], EP: [1400000.0, 280000.0, 14] };
const MAX = 72;
const alfa = (hz) => { const dt = 1 / TASA, tau = 1 / (hz * 2 * Math.PI); return dt / (tau + dt); };
// (tres pasos bajos de un polo en cascada: su respuesta al impulso, normalizada a la parte que entra)
function pesos(hz, arr) {
  const a = alfa(hz); let s = 0, k = 0;
  for (; k < MAX; k++) { const w = a * a * a * ((k + 1) * (k + 2) / 2) * Math.pow(1 - a, k); arr[k] = w; s += w; if (k > 4 && w < 1e-4 * a) { k++; break; } }
  for (let j = 0; j < MAX; j++) arr[j] = j < k ? arr[j] / s : 0;
  return k;
}

export function crearNTSC(W, H) {
  const RTT = (n) => rtt(n, W, H);
  const U = {
    muestras: uniform(640), sangradoH: uniform(0), sangradoV: uniform(0), anillo: uniform(1), ruido: uniform(2), cabezal: uniform(0),
    ruidoCroma: uniform(0), faseCroma: uniform(0), onda: uniform(0), nitidezVHS: uniform(1.5), perdida: uniform(0), subportadora: uniform(1),
  };
  // los filtros, como arreglos (cambian con la cinta)
  const F = {};
  const filtro = (n, hz) => { const arr = new Array(MAX).fill(0), nodo = uniformArray(arr, 'float'), k = uniform(int(pesos(hz, arr))); F[n] = { arr, nodo, k, hz }; };
  filtro('I', 1300000.0); filtro('Q', 600000.0); filtro('tv', 2600000.0); filtro('luma', CINTAS.SP[0]); filtro('croma', CINTAS.SP[1]); filtro('nitidez', CINTAS.SP[0] * 4);
  const retrasoCroma = uniform(CINTAS.SP[2]);
  const preA = uniform(alfa(CINTAS.SP[0]));
  // el anillado: corte ideal de frecuencias horizontal (ntscqt: dft × máscara) = sinc truncado, ±16 muestras
  const SINC = 16, sincArr = new Array(2 * SINC + 1).fill(0), sincNodo = uniformArray(sincArr, 'float');
  const ponerAnillo = (al) => { let s = 0; for (let k = -SINC; k <= SINC; k++) { const x = Math.PI * al * k, w = k === 0 ? 1 : Math.sin(x) / x; sincArr[k + SINC] = w; s += w; } for (let j = 0; j < sincArr.length; j++) sincArr[j] /= s; };
  ponerAnillo(1);
  const cinta = (nombre) => {
    const c = CINTAS[nombre] ?? CINTAS.SP;
    for (const [n, hz] of [['luma', c[0]], ['croma', c[1]], ['nitidez', c[0] * 4]]) { F[n].k.value = pesos(hz, F[n].arr); F[n].hz = hz; }
    retrasoCroma.value = c[2]; preA.value = alfa(c[0]);
  };

  // (una muestra = paso pixeles; la línea = paso pixeles de alto)
  const paso = screenSize.x.div(U.muestras).max(1);
  const du = paso.div(screenSize.x), dv = paso.div(screenSize.y);
  const n0 = screenCoordinate.x.div(paso).floor(), linea = screenCoordinate.y.div(paso).floor();
  const uvM = (n, l) => vec2(n.add(0.5).mul(du), l.add(0.5).mul(dv));
  const azar = (n, l, k) => hash(n.add(l.mul(1031)).add(float(frameId.mod(509)).mul(7919)).add(k * 104729));

  const aYIQ = (c) => { const y = c.r.mul(0.30).add(c.g.mul(0.59)).add(c.b.mul(0.11)); return vec3(y, c.b.sub(y).mul(-0.27).add(c.r.sub(y).mul(0.74)), c.b.sub(y).mul(0.41).add(c.r.sub(y).mul(0.48))); };
  const aRGB = (q) => vec3(q.x.add(q.y.mul(0.956)).add(q.z.mul(0.621)), q.x.sub(q.y.mul(0.272)).sub(q.z.mul(0.647)), q.x.sub(q.y.mul(1.106)).add(q.z.mul(1.703))).clamp(0, 1);
  // filtro causal con retraso, sobre un canal: Σ h[k] · x[n + retraso − k]
  const causal = (leer, f, retraso) => Fn(() => {
    const acc = float(0).toVar();
    Loop({ start: int(0), end: f.k, type: 'int' }, ({ i }) => { acc.addAssign(f.nodo.element(i).mul(leer(n0.add(retraso).sub(float(i))))); });
    return acc;
  })();

  // ---------- las etapas ----------
  function etapaA(entrada, e) {
    const leerRGB = (n, l) => entrada.sample(uvM(n.sub(e.sangrado ? U.sangradoH : 0), l.sub(e.sangrado ? U.sangradoV : 0))).level(0).rgb;
    return RTT(Fn(() => {
      const q = aYIQ(leerRGB(n0, linea)).toVar();
      if (e.sangrado) {      // (composite_in_chroma_lowpass: I a 1,3 MHz con 2 de retraso, Q a 0,6 MHz con 4)
        q.y.assign(causal((n) => aYIQ(leerRGB(n, linea)).y, F.I, 2));
        q.z.assign(causal((n) => aYIQ(leerRGB(n, linea)).z, F.Q, 4));
      }
      if (e.anillo) {
        const acc = float(0).toVar();
        Loop({ start: int(0), end: int(2 * SINC + 1), type: 'int' }, ({ i }) => { acc.addAssign(sincNodo.element(i).mul(aYIQ(entrada.sample(uvM(n0.add(float(i)).sub(SINC), linea)).level(0).rgb).x)); });
        q.x.assign(mix(q.x, acc, float(1).sub(U.anillo).mul(40).min(1)));      // (anillo = 1: sin anillado, como en ntscqt)
      }
      return vec4(q, 1);
    })());
  }
  // LA SEÑAL COMPUESTA (chroma_into_luma + chroma_from_luma): el croma montado en el luma con la subportadora —4 muestras
  // por ciclo, fase que se invierte línea por medio (video_scanline_phase_shift 180, con el número de campo)— y decodificado
  // de vuelta: luma = promedio de 4 muestras, croma = lo que sobra, demodulado. De ahí los arcoíris y los puntitos.
  const xi = linea.add(float(frameId.mod(2))).mod(2).mul(2);
  const u = (n) => { const p = n.add(xi).mod(4); return p.equal(0).select(float(1), p.equal(2).select(float(-1), float(0))); };
  const v = (n) => { const p = n.add(xi).mod(4); return p.equal(1).select(float(1), p.equal(3).select(float(-1), float(0))); };
  function decodificar(tex, ruido, corre) {
    const s = (n) => { const m = n.sub(corre), a = tex.sample(uvM(m, linea)).level(0).xyz; const x = a.x.add(a.y.mul(u(m)).add(a.z.mul(v(m))).mul(U.subportadora)); return ruido ? x.add(ruido(n)) : x; };
    const sv = [-2, -1, 0, 1, 2, 3, 4].map((k) => s(n0.add(k)).toVar());
    const luma = (j) => sv[j - 1].add(sv[j]).add(sv[j + 1]).add(sv[j + 2]).mul(0.25);      // (j = índice en sv; 2 = n0)
    const c = (j) => sv[j].sub(luma(j));
    let I = float(0), Q = float(0);
    for (let j = 1; j <= 4; j++) { const m = n0.add(j - 2); I = I.add(c(j).mul(u(m))); Q = Q.add(c(j).mul(v(m))); }
    return vec3(luma(2), I.mul(0.5).div(U.subportadora), Q.mul(0.5).div(U.subportadora));
  }
  function etapaB(texA, e) {
    return RTT(Fn(() => {
      const q = texA.sample(uvM(n0, linea)).level(0).xyz.toVar();
      if (e.compuesto) {
        // el salto del cabezal: las últimas líneas corridas, cada vez menos (× 7/8 por línea)
        const lineas = screenSize.y.div(paso), desdeAbajo = lineas.sub(linea);
        const corre = float(e.cabezal ? 1 : 0).mul(desdeAbajo.lessThan(9).toFloat()).mul(U.cabezal).mul(float(0.875).pow(float(8).sub(desdeAbajo).max(0))).mul(azar(float(0), linea, 7).mul(0.4).add(0.8)).floor();
        const ruidoV = (n) => azar(n, linea, 1).mul(0.5).add(azar(n.sub(1), linea, 1).mul(0.25)).add(azar(n.sub(2), linea, 1).mul(0.125)).add(azar(n.sub(3), linea, 1).mul(0.0625)).sub(0.47).mul(2).mul(U.ruido).div(256);
        q.assign(decodificar(texA, ruidoV, corre));
      }
      if (e.ruidoCroma) {
        const rc = (k) => azar(n0, linea, k).mul(0.5).add(azar(n0.sub(1), linea, k).mul(0.25)).add(azar(n0.sub(2), linea, k).mul(0.125)).sub(0.44).mul(2).mul(U.ruidoCroma).div(256);
        q.y.addAssign(rc(2)); q.z.addAssign(rc(3));
        const ang = azar(float(0), linea, 4).sub(0.5).add(azar(float(0), linea.sub(1), 4).sub(0.5).mul(0.5)).mul(U.faseCroma).mul(Math.PI / 100);
        const cs = cos(ang), sn = sin(ang);
        q.assign(vec3(q.x, q.y.mul(cs).sub(q.z.mul(sn)), q.y.mul(sn).add(q.z.mul(cs))));
      }
      return vec4(q, 1);
    })());
  }
  function etapaC(texB) {
    return RTT(Fn(() => {
      const ondaL = (l) => azar(float(0), l, 5).mul(U.onda).floor();
      const corre = ondaL(linea).mul(0.5).add(ondaL(linea.sub(1)).mul(0.25)).add(ondaL(linea.sub(2)).mul(0.25)).floor();
      const leer = (n, l) => texB.sample(uvM(n.sub(corre), l)).level(0).xyz;
      // el luma: tres pasos bajos y el realce de la casetera (+ su paso alto × 1,6)
      const y3 = causal((n) => leer(n, linea).x, F.luma, 0);
      const y3a = causal((n) => leer(n.sub(1), linea).x, F.luma, 0);
      const Y = y3.add(y3.sub(y3a.mul(float(1).sub(preA)).add(y3.mul(preA))).mul(1.6));
      const I = causal((n) => leer(n, linea).y.add(leer(n, linea.sub(1)).y).mul(0.5), F.croma, retrasoCroma);      // (con la mezcla vertical del croma)
      const Q = causal((n) => leer(n, linea).z.add(leer(n, linea.sub(1)).z).mul(0.5), F.croma, retrasoCroma);
      return vec4(Y, I, Q, 1);
    })());
  }
  // la nitidez de la casetera (vhs_sharpen: luma + (luma − su paso bajo a 4 × el corte) × fuerza × 2)
  const etapaNitidez = (tex) => RTT(Fn(() => { const q = tex.sample(uvM(n0, linea)).level(0).xyz.toVar(); const ts = causal((n) => tex.sample(uvM(n, linea)).level(0).x, F.nitidez, 0); q.x.assign(q.x.add(q.x.sub(ts).mul(U.nitidezVHS).mul(2))); return vec4(q, 1); })());
  // LA SEGUNDA CODIFICACIÓN DE LA CASETERA (emulate_vhs, sin «svideo_out»): la casetera saca la imagen otra vez por la
  // salida compuesta, así que el croma se vuelve a montar en el luma y a decodificar, sin ruido nuevo
  const etapaRecompuesta = (tex) => RTT(Fn(() => vec4(decodificar(tex, null, float(0)), 1))());
  function etapaD(tex, e) {
    return Fn(() => {
      const q = tex.sample(uvM(n0, linea)).level(0).xyz.toVar();
      if (e.perdida) { If(azar(float(0), linea, 6).mul(100000).lessThan(U.perdida), () => { q.y.assign(0); q.z.assign(0); }); }
      if (e.salida) {
        // el croma del televisor (2,6 MHz, 1 de retraso) y a mitad de definición en los dos sentidos (yuv420)
        const cr = (dn, dl) => vec2(causal((n) => tex.sample(uvM(n.add(dn), linea.add(dl))).level(0).y, F.tv, 1), causal((n) => tex.sample(uvM(n.add(dn), linea.add(dl))).level(0).z, F.tv, 1));
        const m = cr(0, 0).mul(0.4).add(cr(1, 0).mul(0.15)).add(cr(-1, 0).mul(0.15)).add(cr(0, 1).mul(0.15)).add(cr(0, -1).mul(0.15));
        q.y.assign(m.x); q.z.assign(m.y);
      }
      return vec4(aRGB(q), 1);
    })();
  }
  // EL ENTRELAZADO: ntscqt procesa un solo campo y rellena las líneas impares con el promedio de sus vecinas («ntscqt»; su
  // InterlacedRenderer quedó sin hacer). «campos»: como la tele de verdad, cada cuadro dibuja sólo las líneas de su campo
  // (pares o impares, alternando) y las otras quedan del cuadro anterior: lo que se mueve se peina.
  const historia = new THREE.RenderTarget(1, 1, { type: THREE.HalfFloatType, depthBuffer: false });
  const verHistoria = texture(historia.texture);
  let paraCopiar = null;
  // e = { sangrado, anillo, compuesto, cabezal, ruidoCroma, vHS, nitidezVHS, recompuesto, perdida, salida, entrelazado: 'no' | 'ntscqt' | 'campos' }
  function armar(entrada, e) {
    const A = etapaA(entrada, e), B = etapaB(A, e);
    let C = e.vHS ? etapaC(B) : B;
    if (e.nitidezVHS) C = etapaNitidez(C);
    if (e.vHS && e.recompuesto) C = etapaRecompuesta(C);
    salida.ultimo = { A, B, C, entrada };      // (para medir desde la consola del navegador)
    paraCopiar = null;
    if (e.entrelazado === 'ntscqt') {
      const Dt = RTT(etapaD(C, e));
      return Fn(() => { const r = Dt.sample(uvM(n0, linea)).level(0).rgb.toVar(); If(linea.mod(2).equal(1), () => { r.assign(Dt.sample(uvM(n0, linea.sub(1))).level(0).rgb.add(Dt.sample(uvM(n0, linea.add(1))).level(0).rgb).mul(0.5)); }); return vec4(r, 1); })();
    }
    if (e.entrelazado === 'campos') {
      const D = etapaD(C, e);
      const Ft = RTT(Fn(() => { const r = verHistoria.sample(screenUV).level(0).rgb.toVar(); If(linea.mod(2).equal(float(frameId.mod(2))), () => { r.assign(D.rgb); }); return vec4(r, 1); })());
      paraCopiar = Ft; salida.ultimo.F = Ft;
      return vec4(Ft.sample(screenUV).level(0).rgb, 1);
    }
    return etapaD(C, e);
  }
  // (después de dibujar: lo que salió queda como el cuadro anterior para el campo que no se dibuja)
  function despues(ren) {
    if (!paraCopiar?.renderTarget) return;
    const src = paraCopiar.renderTarget;
    if (historia.width !== src.width || historia.height !== src.height) { historia.setSize(src.width, src.height); const antes = ren.getRenderTarget(); ren.setRenderTarget(historia); ren.clear(); ren.setRenderTarget(antes); }
    ren.copyTextureToTexture(src.texture, historia.texture);
  }
  const salida = { U, armar, cinta, ponerAnillo, despues, ultimo: null };
  return salida;
}
