/*
 * Versión vertical (1080×1920, 9:16) para Instagram Reels.
 *
 * Misma identidad de movimiento que el video horizontal, rediseñada para celular:
 * - Abre con la promesa (hook en el primer segundo); el logo va arriba y vuelve al cierre.
 * - Una idea por pantalla, una sola columna o grillas de 2, tipografía más grande.
 * - Zona segura de Reels: arriba ~250px (barra), abajo ~480px (texto y audio),
 *   derecha ~140px (botones). El contenido vive en x 72–940, y 250–1440.
 */
import React from "react";
import { AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
import {
  BrilloAmbiental,
  C,
  Check,
  clamp,
  DESIGNACIONES,
  DocIcono,
  EASE,
  EASE_EXIT,
  entrada,
  Escena,
  Escudo,
  Eyebrow,
  FONT_DISPLAY,
  FONT_TEXT,
  FondoTierra,
  LineaAcento,
  LOGOS,
  METODOS,
  progreso,
  Sello,
  SOLAPE,
  SOLUCIONES,
  T,
  Titulo,
} from "./WitPresentacion";

const ZONA: React.CSSProperties = { padding: "250px 140px 480px 72px", justifyContent: "center" };

/* ---------- 1. Hero (hook) ---------- */

const VHero: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const palabras = ["IA", "en", "producción", "sobre", "tus", "sistemas", "reales."];
  return (
    <Escena dur={dur} fondo={C.navyDeep} entraConFundido={false}>
      <FondoTierra dur={dur} desde={1.18} hasta={1.08} />
      <AbsoluteFill style={{ background: "rgba(20,41,58,.35)" }} />
      <AbsoluteFill style={ZONA}>
        <Img src={staticFile("logo-white-mark.png")} style={{ height: 96, alignSelf: "flex-start", ...entrada(f, 0, T.std, 20) }} />
        <div style={{ height: 70 }} />
        <Eyebrow f={f} desde={4} oscuro>
          Microsoft Solutions Partner · Chile y Perú
        </Eyebrow>
        <h1
          style={{
            margin: "26px 0 0",
            fontFamily: FONT_DISPLAY,
            fontSize: 128,
            lineHeight: 1.02,
            fontWeight: 600,
            letterSpacing: "-.03em",
            color: "#fff",
          }}
        >
          {palabras.map((p, i) => (
            <span
              key={p}
              style={{
                display: "inline-block",
                marginRight: "0.22em",
                color: i >= 5 ? C.green : "#fff",
                ...entrada(f, 8 + i * 2, T.std + 4, 48),
              }}
            >
              {p}
            </span>
          ))}
        </h1>
        <LineaAcento f={f} desde={30} ancho={160} />
        <p
          style={{
            ...entrada(f, 38),
            margin: "34px 0 0",
            fontFamily: FONT_TEXT,
            fontSize: 40,
            lineHeight: 1.38,
            color: "rgba(255,255,255,.85)",
          }}
        >
          Implementamos Dynamics 365, Power Platform, Azure y agentes de IA en grandes empresas y
          organismos públicos.
        </p>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- 2. Credenciales ---------- */

const VCredenciales: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const inicioConteo = 36;
  const paso = 7;
  const n = Math.max(0, Math.min(6, Math.floor((f - inicioConteo) / paso) + 1));
  const pop = n > 0 ? 1 + 0.06 * (1 - progreso(f, inicioConteo + (n - 1) * paso, T.quick)) : 1;
  const pSello = progreso(f, 6, T.slow);
  const sombra = progreso(f, 14, T.slow);
  return (
    <Escena dur={dur} fondo="#fff">
      <BrilloAmbiental dur={dur} />
      <AbsoluteFill style={ZONA}>
        <Img
          src={staticFile("WIT-MicrosoftCloud-color.png")}
          style={{
            width: 520,
            opacity: interpolate(pSello, [0, 0.5], [0, 1], clamp),
            transform: `translateY(${(1 - pSello) * 40}px)`,
            filter: `drop-shadow(0 ${18 * sombra}px ${26 * sombra}px rgba(20,41,58,${0.2 * sombra}))`,
          }}
        />
        <Titulo f={f} desde={16} size={62}>
          Microsoft validó nuestra capacidad en todas sus áreas de soluciones.
        </Titulo>
        <div style={{ ...entrada(f, 28), marginTop: 30, display: "flex", alignItems: "baseline", gap: 16, fontFamily: FONT_DISPLAY, color: C.navy }}>
          <span style={{ fontSize: 120, fontWeight: 700, color: C.green, display: "inline-block", transform: `scale(${pop})`, transformOrigin: "50% 80%", minWidth: 70 }}>
            {n}
          </span>
          <span style={{ fontSize: 46, fontWeight: 600 }}>de 6 designaciones</span>
        </div>
        <div style={{ marginTop: 18, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          {DESIGNACIONES.map((d, i) => {
            const desde = inicioConteo + i * paso;
            return (
              <div
                key={d}
                style={{
                  ...entrada(f, desde, T.std, 18),
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  padding: "16px 16px",
                  borderRadius: 12,
                  background: C.greenTint,
                  fontFamily: FONT_TEXT,
                  fontSize: 26,
                  fontWeight: 600,
                  color: C.navy,
                }}
              >
                <Check f={f} desde={desde + 6} color={C.greenDark} size={24} />
                {d}
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- 3. Soluciones ---------- */

const VSoluciones: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const inicioFoco = 60;
  const pasoFoco = 16;
  return (
    <Escena dur={dur} fondo={C.bg}>
      <BrilloAmbiental dur={dur} />
      <AbsoluteFill style={ZONA}>
        <Eyebrow f={f} desde={4}>Soluciones Microsoft</Eyebrow>
        <Titulo f={f} desde={10} size={62}>
          Implementamos Dynamics 365, Power Platform, Azure y Copilot.
        </Titulo>
        <div style={{ marginTop: 44, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          {SOLUCIONES.map((s, i) => {
            const inicio = inicioFoco + i * pasoFoco;
            const on = progreso(f, inicio, T.quick) * (1 - progreso(f, inicio + pasoFoco - 4, T.quick - 4, EASE_EXIT));
            return (
              <div
                key={s.nombre}
                style={{
                  ...entrada(f, 22 + i * 2, T.std + 4, 40),
                  height: 186,
                  background: "#fff",
                  borderRadius: 16,
                  border: `2px solid ${on > 0.01 ? `rgba(84,186,0,${on})` : C.line}`,
                  boxShadow: `0 ${2 + 12 * on}px ${4 + 24 * on}px rgba(0,0,0,${0.08 + 0.06 * on})`,
                  padding: "22px 22px",
                  position: "relative",
                  overflow: "hidden",
                }}
              >
                <div style={{ transform: `translateY(${-6 * on}px)` }}>
                  {s.icono ? <Img src={staticFile(`ms/${s.icono}.svg`)} style={{ width: 52, height: 52 }} /> : <div style={{ transform: "scale(.82)", transformOrigin: "top left", height: 52 }}><Escudo /></div>}
                  <div style={{ marginTop: 14, fontFamily: FONT_DISPLAY, fontSize: 25, lineHeight: 1.18, fontWeight: 600, color: C.navy }}>
                    {s.nombre.replace(/^Microsoft Dynamics 365 /, "Dynamics 365 ")}
                  </div>
                </div>
                <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 6, background: C.green, transform: `scaleY(${on})`, transformOrigin: "top" }} />
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- 4. Cómo trabajamos ---------- */

const VMetodologias: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const inicioRiel = 50;
  const durRiel = 80;
  return (
    <Escena dur={dur} fondo="#fff">
      <BrilloAmbiental dur={dur} />
      <AbsoluteFill style={ZONA}>
        <Eyebrow f={f} desde={4}>Cómo trabajamos</Eyebrow>
        <Titulo f={f} desde={10} size={62}>
          Cuatro marcos ágiles, uno para cada tipo de proyecto.
        </Titulo>
        <div style={{ marginTop: 44, display: "grid", gridTemplateColumns: "1fr 1fr", columnGap: 30, rowGap: 40 }}>
          {METODOS.map((m, i) => {
            const avance = interpolate(f, [inicioRiel + i * 4, inicioRiel + i * 4 + durRiel], [0, 1], clamp);
            return (
              <div key={m.titulo} style={{ ...entrada(f, 22 + i * 3, T.std + 4, 40) }}>
                <div style={{ fontFamily: FONT_DISPLAY, fontSize: 28, lineHeight: 1.18, fontWeight: 600, color: C.navy, minHeight: 66 }}>
                  {m.titulo}
                </div>
                <div style={{ position: "relative", marginTop: 16, paddingLeft: 38 }}>
                  <div style={{ position: "absolute", left: 11, top: 12, bottom: 12, width: 4, borderRadius: 2, background: C.line }} />
                  <div style={{ position: "absolute", left: 11, top: 12, width: 4, borderRadius: 2, background: C.green, height: `calc((100% - 24px) * ${avance})` }} />
                  {m.fases.map((fase, j) => {
                    const umbral = j / (m.fases.length - 1);
                    const activa = progreso(avance * durRiel, umbral * durRiel - 2, T.quick);
                    return (
                      <div key={fase} style={{ position: "relative", height: 50, display: "flex", alignItems: "center" }}>
                        <div
                          style={{
                            position: "absolute",
                            left: -38,
                            width: 26,
                            height: 26,
                            borderRadius: 13,
                            background: activa > 0.5 ? C.green : "#fff",
                            border: `3px solid ${activa > 0.5 ? C.green : C.line}`,
                            transform: `scale(${1 + 0.15 * Math.sin(Math.PI * activa)})`,
                          }}
                        />
                        <span style={{ fontFamily: FONT_TEXT, fontSize: 24, color: activa > 0.5 ? C.navy : C.muted, fontWeight: activa > 0.5 ? 600 : 400 }}>
                          {fase}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- 5. Trust Center ---------- */

const VTrust: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const circulo = (bg: string, hijo: React.ReactNode) => (
    <div style={{ width: 96, height: 96, borderRadius: 48, background: bg, display: "flex", alignItems: "center", justifyContent: "center" }}>{hijo}</div>
  );
  const items = [
    { visual: <Sello src="SGS_ISO_9001_round_TCL_LR.jpg" />, titulo: "ISO 9001", texto: "Gestión de calidad, certificada por SGS" },
    { visual: <Sello src="SGS_ISO-IEC_27001_TCL_LR.jpg" />, titulo: "ISO/IEC 27001", texto: "Seguridad de la información, certificada por SGS" },
    { visual: circulo("#fff", <Img src={staticFile("ms/azure.svg")} style={{ width: 58 }} />), titulo: "Azure Chile Central", texto: "Implementaciones en la región Azure de Chile" },
    { visual: circulo(C.green, <DocIcono />), titulo: "IA responsable", texto: "Política de IA responsable publicada" },
  ];
  return (
    <Escena dur={dur} fondo={C.navyDeep}>
      <FondoTierra dur={dur} desde={1.06} hasta={1.16} />
      <AbsoluteFill style={{ background: "rgba(20,41,58,.6)" }} />
      <AbsoluteFill style={ZONA}>
        <Eyebrow f={f} desde={4} oscuro>Trust Center</Eyebrow>
        <Titulo f={f} desde={10} oscuro size={70}>
          Todo lo que declaramos se puede verificar.
        </Titulo>
        <LineaAcento f={f} desde={22} />
        <div style={{ marginTop: 50, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18 }}>
          {items.map((it, i) => {
            const desde = 30 + i * 4;
            return (
              <div
                key={it.titulo}
                style={{
                  ...entrada(f, desde, T.std + 4, 40),
                  background: "rgba(255,255,255,.07)",
                  border: "1px solid rgba(255,255,255,.16)",
                  borderRadius: 18,
                  padding: "26px 22px",
                  minHeight: 330,
                }}
              >
                {it.visual}
                <div style={{ marginTop: 20, display: "flex", alignItems: "flex-start", gap: 8, fontFamily: FONT_DISPLAY, fontSize: 31, lineHeight: 1.18, fontWeight: 600, color: "#fff" }}>
                  <div style={{ marginTop: 3 }}>
                    <Check f={f} desde={desde + 14} color={C.green} size={28} />
                  </div>
                  {it.titulo}
                </div>
                <div style={{ marginTop: 10, fontFamily: FONT_TEXT, fontSize: 24, lineHeight: 1.38, color: "rgba(255,255,255,.8)" }}>
                  {it.texto}
                </div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- 6. Clientes ---------- */

const VFilaLogos: React.FC<{ logos: string[]; f: number; sentido: 1 | -1; desde: number }> = ({ logos, f, sentido, desde }) => {
  const ancho = 270;
  const total = logos.length * ancho;
  const x = (f * 2 * sentido) % total;
  const base = sentido === 1 ? -total : 0;
  return (
    <div style={{ ...entrada(f, desde, T.std + 4, 30), overflow: "hidden", width: "100%", height: 150 }}>
      <div style={{ display: "flex", transform: `translateX(${base + x}px)`, width: total * 2 }}>
        {[...logos, ...logos].map((l, i) => (
          <div
            key={i}
            style={{
              width: ancho - 20,
              marginRight: 20,
              height: 140,
              flexShrink: 0,
              background: "#fff",
              border: `1px solid ${C.line}`,
              borderRadius: 16,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Img src={staticFile(`clientes/${l}`)} style={{ maxHeight: 62, maxWidth: 180, filter: "grayscale(1)", opacity: 0.7 }} />
          </div>
        ))}
      </div>
    </div>
  );
};

const VClientes: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  return (
    <Escena dur={dur} fondo={C.bg}>
      <BrilloAmbiental dur={dur} />
      <AbsoluteFill style={{ padding: "250px 0 480px", justifyContent: "center" }}>
        <div style={{ padding: "0 140px 0 72px" }}>
          <Eyebrow f={f} desde={4}>Clientes</Eyebrow>
          <Titulo f={f} desde={10} size={70}>
            Grandes empresas y organismos públicos en Chile y Perú.
          </Titulo>
        </div>
        <div style={{ marginTop: 60, display: "flex", flexDirection: "column", gap: 18 }}>
          <VFilaLogos logos={LOGOS.slice(0, 8)} f={f} sentido={-1} desde={24} />
          <VFilaLogos logos={LOGOS.slice(8, 16)} f={f} sentido={1} desde={28} />
          <VFilaLogos logos={LOGOS.slice(16)} f={f} sentido={-1} desde={32} />
        </div>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- 7. Cierre ---------- */

const VCierre: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const presion = interpolate(f, [64, 68, 74, 84], [1, 0.97, 1.02, 1], { ...clamp, easing: EASE });
  return (
    <Escena dur={dur + SOLAPE} fondo={C.navyDeep}>
      <FondoTierra dur={dur} desde={1.08} hasta={1.16} />
      <AbsoluteFill style={{ background: "rgba(20,41,58,.5)" }} />
      <AbsoluteFill style={{ ...ZONA, padding: "250px 100px 480px", alignItems: "center", textAlign: "center" }}>
        <Img src={staticFile("logo-white-mark.png")} style={{ height: 150, ...entrada(f, 4, T.slow, 24) }} />
        <h2 style={{ ...entrada(f, 18), margin: "60px 0 0", fontFamily: FONT_DISPLAY, fontSize: 96, lineHeight: 1.06, fontWeight: 600, letterSpacing: "-.02em", color: "#fff" }}>
          Conversemos sobre tu proyecto.
        </h2>
        <p style={{ ...entrada(f, 30), margin: "30px 0 0", fontFamily: FONT_TEXT, fontSize: 38, lineHeight: 1.38, color: "rgba(255,255,255,.85)" }}>
          Te respondemos en menos de 1 día hábil.
        </p>
        <div
          style={{
            ...entrada(f, 42),
            marginTop: 56,
          }}
        >
          <div
            style={{
              transform: `scale(${presion})`,
              background: C.green,
              color: "#fff",
              fontFamily: FONT_TEXT,
              fontSize: 44,
              fontWeight: 600,
              padding: "26px 60px",
              borderRadius: 16,
              boxShadow: "0 10px 30px rgba(84,186,0,.35)",
            }}
          >
            w-it.cl
          </div>
        </div>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- Línea de tiempo ---------- */

const ESCENAS_V: { C: React.FC<{ dur: number }>; dur: number }[] = [
  { C: VHero, dur: 150 },
  { C: VCredenciales, dur: 180 },
  { C: VSoluciones, dur: 210 },
  { C: VMetodologias, dur: 210 },
  { C: VTrust, dur: 150 },
  { C: VClientes, dur: 150 },
  { C: VCierre, dur: 150 },
];

const iniciosV = ESCENAS_V.reduce<number[]>((acc, _e, i) => {
  acc.push(i === 0 ? 0 : acc[i - 1] + ESCENAS_V[i - 1].dur - SOLAPE);
  return acc;
}, []);

export const DURACION_VERTICAL = iniciosV[iniciosV.length - 1] + ESCENAS_V[ESCENAS_V.length - 1].dur;

export const WitVertical: React.FC = () => (
  <AbsoluteFill style={{ background: C.navyDeep }}>
    {ESCENAS_V.map(({ C: Comp, dur }, i) => (
      <Sequence key={i} from={iniciosV[i]} durationInFrames={dur}>
        <Comp dur={dur} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
