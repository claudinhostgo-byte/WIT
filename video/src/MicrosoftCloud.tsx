/*
 * Anuncio RRSS: W-IT es Solutions Partner for Microsoft Cloud (6 de 6 designaciones).
 * 16 s · 30 fps · se adapta a 1080×1920 (Reels/TikTok/Shorts) y 1080×1350 (LinkedIn/feed).
 *
 * Identidad de movimiento (skill motion-design):
 * - Personalidad Premium: curva firma bezier(0.2, 0, 0, 1), sin rebote salvo el "pop" de logro.
 * - Narrativa: planteamiento (seis áreas) → acción (se suman las 6 designaciones)
 *   → resolución (convergen en el sello Microsoft Cloud) → firma (logo W-IT).
 * - Tres capas: primaria (badges, sello, texto), secundaria (checks, contador, órbita,
 *   brillo, onda de choque) y ambiental (luces a la deriva + partículas).
 * - Entradas: subir + desenfoque → nitidez. Salidas: acelerar hacia el centro o hacia arriba.
 */
import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { C, EASE, FONT_DISPLAY, FONT_TEXT, SINE, clamp, progreso } from "./WitPresentacion";

export const DURACION_MSCLOUD = 504;

const EASE_IN = Easing.bezier(0.55, 0, 0.75, 0.2);
const FONDO = "#0B1C28";

const BADGES = [
  { archivo: "business-applications", alto: 544 },
  { archivo: "modern-work", alto: 544 },
  { archivo: "data-ai", alto: 634 },
  { archivo: "digital-app-innovation", alto: 634 },
  { archivo: "infrastructure", alto: 634 },
  { archivo: "security", alto: 544 },
];

/* Línea de tiempo (frames) */
const T0 = {
  hookFin: 96,
  badge0: 102,
  pasoBadge: 18,
  converge: 246,
  sello: 276,
  selloSalida: 410,
  logo: 424,
};

/** Aparece subiendo y pasando de desenfocado a nítido. */
const revela = (f: number, desde: number, dur = 20, dist = 28, blur = 14): React.CSSProperties => {
  const p = progreso(f, desde, dur);
  return {
    opacity: interpolate(p, [0, 0.7], [0, 1], clamp),
    transform: `translateY(${(1 - p) * dist}px)`,
    filter: `blur(${(1 - p) * blur}px)`,
  };
};

/** Sale hacia arriba, acelerando y desenfocándose. */
const despide = (f: number, desde: number, dur = 14): React.CSSProperties => {
  const p = progreso(f, desde, dur, EASE_IN);
  return { opacity: 1 - p, transform: `translateY(${-30 * p}px)`, filter: `blur(${10 * p}px)` };
};

/* ---------- Capa ambiental ---------- */

const Ambiente: React.FC = () => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const t = f / DURACION_MSCLOUD;
  // Se intensifica cuando aparece el sello.
  const energia = 0.55 + 0.45 * progreso(f, T0.sello, 40, SINE);
  return (
    <AbsoluteFill style={{ background: FONDO }}>
      <AbsoluteFill
        style={{
          background: [
            `radial-gradient(${width * 0.9}px ${width * 0.8}px at ${20 + 25 * t}% ${18 + 10 * t}%, rgba(84,186,0,${0.16 * energia}), transparent 70%)`,
            `radial-gradient(${width}px ${width}px at ${85 - 20 * t}% ${78 - 12 * t}%, rgba(46,96,140,${0.42 * energia}), transparent 70%)`,
          ].join(","),
        }}
      />
      {/* Grilla de puntos muy tenue: textura tecnológica sin ruido */}
      <AbsoluteFill
        style={{
          backgroundImage: "radial-gradient(rgba(255,255,255,.07) 1.4px, transparent 1.6px)",
          backgroundSize: "36px 36px",
          backgroundPosition: `0 ${-f * 0.25}px`,
          maskImage: "radial-gradient(circle at 50% 45%, #000 0%, transparent 75%)",
          WebkitMaskImage: "radial-gradient(circle at 50% 45%, #000 0%, transparent 75%)",
        }}
      />
      {Array.from({ length: 46 }).map((_, i) => {
        const x = random(`x${i}`) * width;
        const vel = 0.25 + random(`v${i}`) * 0.7;
        const y = ((random(`y${i}`) * (height + 80) - f * vel) % (height + 80) + height + 80) % (height + 80) - 40;
        const r = 1.2 + random(`r${i}`) * 2.6;
        const parpadeo = 0.5 + 0.5 * Math.sin(f / (14 + random(`t${i}`) * 20) + i);
        const verde = random(`c${i}`) > 0.6;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: r * 2,
              height: r * 2,
              borderRadius: "50%",
              background: verde ? C.green : "#CFE3F2",
              opacity: (0.12 + 0.35 * parpadeo) * energia,
              boxShadow: verde ? `0 0 ${r * 4}px rgba(84,186,0,.8)` : "none",
            }}
          />
        );
      })}
      <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 45%, transparent 45%, rgba(5,12,18,.6) 100%)" }} />
    </AbsoluteFill>
  );
};

/* ---------- Piezas ---------- */

const Check: React.FC<{ f: number; desde: number; size?: number }> = ({ f, desde, size = 52 }) => {
  const { fps } = useVideoConfig();
  const pop = spring({ frame: f - desde, fps, config: { damping: 12, mass: 0.6, stiffness: 160 } });
  const trazo = progreso(f, desde + 4, 12);
  return (
    <div
      style={{
        width: size,
        height: size,
        borderRadius: "50%",
        background: C.green,
        boxShadow: `0 0 ${24 * pop}px rgba(84,186,0,.75), 0 0 0 4px ${FONDO}`,
        transform: `scale(${pop})`,
        display: "grid",
        placeItems: "center",
      }}
    >
      <svg width={size * 0.56} height={size * 0.56} viewBox="0 0 24 24">
        <path
          d="M4 12.5l5 5L20 6.5"
          fill="none"
          stroke="#fff"
          strokeWidth={3.4}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray={26}
          strokeDashoffset={26 * (1 - trazo)}
        />
      </svg>
    </div>
  );
};

/** Barrido de luz recortado a la silueta de la imagen. */
const Brillo: React.FC<{ f: number; desde: number; src: string; dur?: number; fuerza?: number }> = ({
  f,
  desde,
  src,
  dur = 26,
  fuerza = 0.7,
}) => {
  const p = progreso(f, desde, dur, Easing.bezier(0.4, 0, 0.2, 1));
  if (p <= 0 || p >= 1) return null;
  const mascara = `url(${src})`;
  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(105deg, transparent 35%, rgba(255,255,255,${fuerza}) 50%, transparent 65%)`,
        backgroundSize: "300% 100%",
        backgroundPosition: `${100 - p * 100}% 0`,
        mixBlendMode: "overlay",
        maskImage: mascara,
        WebkitMaskImage: mascara,
        maskSize: "100% 100%",
        WebkitMaskSize: "100% 100%",
      }}
    />
  );
};

/* ---------- Escena principal ---------- */

export const WitMicrosoftCloud: React.FC = () => {
  const f = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const vertical = height > 1600;

  // Escenario de 1080×1190 dentro de la zona segura (Reels: deja libre barra superior,
  // textos inferiores y botones de la derecha).
  const ESC_H = 1190;
  const escTop = vertical ? 300 : (height - ESC_H) / 2;
  const escLeft = vertical ? -28 : 0;
  const centroSello = { x: 540, y: 420 };

  /* --- 1. Hook: la marca primero --- */
  const pLogo = progreso(f, 2, 26);
  const halo = interpolate(f, [8, 22, 60], [0, 1, 0.35], clamp);
  const hook = (
    <div style={{ position: "absolute", left: 0, right: 0, top: 250, display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center", ...despide(f, T0.hookFin - 14) }}>
      <div
        style={{
          width: 300,
          height: 224,
          clipPath: `inset(${(1 - pLogo) * 100}% 0 0 0)`,
          transform: `translateY(${(1 - pLogo) * 36}px)`,
          filter: `drop-shadow(0 0 ${30 * halo}px rgba(84,186,0,${0.55 * halo}))`,
        }}
      >
        <Img src={staticFile("logo-white-mark.png")} style={{ width: "100%", height: "100%" }} />
      </div>
      <div style={{ marginTop: 70, fontFamily: FONT_DISPLAY, fontSize: 112, lineHeight: 1.02, fontWeight: 700, letterSpacing: "-.035em", color: "#fff" }}>
        {["¡Subimos", "de"].map((p, i) => (
          <span key={p} style={{ display: "inline-block", margin: "0 .12em", ...revela(f, 18 + i * 4, 22, 40, 18) }}>
            {p}
          </span>
        ))}
        <br />
        {/* "categoría" sube desde más abajo: el movimiento repite el mensaje */}
        <span style={{ display: "inline-block", color: C.green, ...revela(f, 28, 30, 110, 20) }}>categoría!</span>
      </div>
      <div
        style={{
          margin: "40px auto 0",
          height: 4,
          borderRadius: 2,
          width: 200 * progreso(f, 46, 24),
          background: `linear-gradient(90deg, transparent, ${C.green}, transparent)`,
        }}
      />
      <div
        style={{
          ...revela(f, 50, 18, 16, 8),
          marginTop: 34,
          fontFamily: FONT_TEXT,
          fontSize: 26,
          fontWeight: 600,
          letterSpacing: ".16em",
          textTransform: "uppercase",
          color: C.greenLight,
        }}
      >
        Microsoft Cloud Partner Program
      </div>
    </div>
  );

  /* --- 2. Seis designaciones --- */
  const anchoBadge = 436;
  const gap = 24;
  const altoCelda = 266;
  const gridTop = 236;
  const gridLeft = (1080 - (anchoBadge * 2 + gap)) / 2;
  const llegadas = BADGES.map((_, i) => T0.badge0 + i * T0.pasoBadge);
  const n = llegadas.filter((l) => f >= l + 8).length;
  const ultimo = n > 0 ? llegadas[n - 1] + 8 : 0;
  const popNum = n > 0 ? 1 + 0.12 * (1 - spring({ frame: f - ultimo, fps, config: { damping: 14 } })) : 1;
  const salidaContador = despide(f, T0.converge - 4, 14);

  const contador = f >= T0.badge0 - 6 && f < T0.converge + 20 && (
    <div style={{ position: "absolute", left: 0, right: 0, top: 20, textAlign: "center", ...revela(f, T0.badge0 - 6, 18), ...(f >= T0.converge - 4 ? salidaContador : {}) }}>
      <div style={{ display: "inline-flex", alignItems: "baseline", gap: 18, fontFamily: FONT_DISPLAY, color: "#fff" }}>
        <span
          style={{
            fontSize: 132,
            fontWeight: 700,
            lineHeight: 1,
            color: C.green,
            display: "inline-block",
            minWidth: 80,
            transform: `scale(${popNum})`,
            transformOrigin: "50% 80%",
            textShadow: `0 0 ${30 * (popNum - 1) * 8}px rgba(84,186,0,.6)`,
          }}
        >
          {n}
        </span>
        <span style={{ fontSize: 50, fontWeight: 600, color: "rgba(255,255,255,.92)" }}>de 6 designaciones</span>
      </div>
      <div style={{ margin: "22px auto 0", width: 520, height: 4, borderRadius: 2, background: "rgba(255,255,255,.12)", overflow: "hidden" }}>
        <div
          style={{
            height: "100%",
            width: `${(100 / 6) * interpolate(f, llegadas.map((l) => l + 8).concat(llegadas[5] + 26), [0, 1, 2, 3, 4, 5, 6], { ...clamp, easing: EASE })}%`,
            background: C.green,
            boxShadow: `0 0 12px ${C.green}`,
          }}
        />
      </div>
    </div>
  );

  const badges =
    f >= T0.badge0 && f < T0.sello + 10 &&
    BADGES.map((b, i) => {
      const col = i % 2;
      const fila = Math.floor(i / 2);
      const x = gridLeft + col * (anchoBadge + gap);
      const y = gridTop + fila * (altoCelda + gap);
      const alto = (anchoBadge * b.alto) / 1039;
      const cx = x + anchoBadge / 2;
      const cy = y + alto / 2;
      const src = staticFile(`designaciones/${b.archivo}.png`);

      const llega = llegadas[i];
      const p = progreso(f, llega, 22);
      const brilloVerde = progreso(f, llega + 8, 6) * (1 - progreso(f, llega + 14, 30, SINE));
      // Convergencia hacia el sello: de afuera hacia adentro.
      const orden = [0, 5, 1, 4, 2, 3].indexOf(i);
      const c = progreso(f, T0.converge + orden * 3, 24, EASE_IN);

      return (
        <div
          key={b.archivo}
          style={{
            position: "absolute",
            left: x,
            top: y,
            width: anchoBadge,
            height: alto,
            opacity: interpolate(p, [0, 0.6], [0, 1], clamp) * (1 - interpolate(c, [0.6, 1], [0, 1], clamp)),
            transform: [
              `translate(${(centroSello.x - cx) * c}px, ${(centroSello.y - cy) * c + (1 - p) * 70}px)`,
              `scale(${(0.9 + 0.1 * p) * (1 - 0.82 * c)})`,
              `rotate(${(col === 0 ? -1 : 1) * 4 * c}deg)`,
            ].join(" "),
            filter: [
              `blur(${(1 - p) * 12 + c * 6}px)`,
              `drop-shadow(0 ${14 * p}px ${30 * p}px rgba(0,0,0,.35))`,
              `drop-shadow(0 0 ${36 * brilloVerde}px rgba(84,186,0,${0.9 * brilloVerde}))`,
            ].join(" "),
          }}
        >
          <Img src={src} style={{ width: "100%", height: "100%", display: "block" }} />
          <Brillo f={f} desde={llega + 6} src={src} fuerza={0.9} />
          <div style={{ position: "absolute", right: -16, top: -16, opacity: 1 - c }}>
            <Check f={f} desde={llega + 8} />
          </div>
        </div>
      );
    });

  /* --- 3. Onda de choque y sello Microsoft Cloud --- */
  const choque = progreso(f, T0.sello - 4, 34, Easing.bezier(0.1, 0.6, 0.3, 1));
  const destello = interpolate(f, [T0.sello - 6, T0.sello + 2, T0.sello + 40], [0, 1, 0.3], clamp);
  const anchoSello = 560;
  const altoSello = (anchoSello * 685) / 1043;
  const ps = progreso(f, T0.sello, 30);
  const salidaSello = progreso(f, T0.selloSalida, 18, EASE_IN);
  const radio = 372;
  const traza = progreso(f, T0.sello + 6, 40, Easing.bezier(0.4, 0, 0.2, 1));
  const giro = (f - T0.sello) * 0.12;
  const srcSello = staticFile("WIT-MicrosoftCloud-color.png");

  const sello = f >= T0.sello - 8 && f < T0.logo + 10 && (
    <>
      {/* Halo */}
      <div
        style={{
          position: "absolute",
          left: centroSello.x - 520,
          top: centroSello.y - 520,
          width: 1040,
          height: 1040,
          borderRadius: "50%",
          background: `radial-gradient(circle, rgba(140,220,80,${0.55 * destello}) 0%, rgba(84,186,0,${0.22 * destello}) 30%, transparent 62%)`,
          opacity: 1 - salidaSello,
        }}
      />
      {/* Onda de choque */}
      {choque > 0 && choque < 1 && (
        <div
          style={{
            position: "absolute",
            left: centroSello.x - 700 * choque,
            top: centroSello.y - 700 * choque,
            width: 1400 * choque,
            height: 1400 * choque,
            borderRadius: "50%",
            border: `${2 + 6 * (1 - choque)}px solid rgba(168,217,124,${0.8 * (1 - choque)})`,
          }}
        />
      )}
      <div style={{ position: "absolute", inset: 0, ...(salidaSello > 0 ? despide(f, T0.selloSalida, 18) : {}) }}>
        {/* Órbita: seis puntos, uno por designación */}
        <svg
          width={radio * 2 + 40}
          height={radio * 2 + 40}
          style={{ position: "absolute", left: centroSello.x - radio - 20, top: centroSello.y - radio - 20, overflow: "visible" }}
        >
          <defs>
            <linearGradient id="orbita" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stopColor={C.green} stopOpacity={0.9} />
              <stop offset="0.5" stopColor="#CFE3F2" stopOpacity={0.25} />
              <stop offset="1" stopColor={C.green} stopOpacity={0.7} />
            </linearGradient>
          </defs>
          <g transform={`rotate(${-90 + giro} ${radio + 20} ${radio + 20})`}>
            <circle
              cx={radio + 20}
              cy={radio + 20}
              r={radio}
              fill="none"
              stroke="url(#orbita)"
              strokeWidth={2}
              strokeDasharray={2 * Math.PI * radio}
              strokeDashoffset={2 * Math.PI * radio * (1 - traza)}
            />
            {BADGES.map((_, i) => {
              const a = (i / 6) * Math.PI * 2;
              const on = progreso(f, T0.sello + 10 + i * 5, 12);
              return (
                <g key={i} transform={`translate(${radio + 20 + Math.cos(a) * radio} ${radio + 20 + Math.sin(a) * radio})`}>
                  <circle r={16 * on} fill="rgba(84,186,0,.25)" />
                  <circle r={7 * on} fill={C.green} />
                </g>
              );
            })}
          </g>
        </svg>
        {/* Sello */}
        <div
          style={{
            position: "absolute",
            left: centroSello.x - anchoSello / 2,
            top: centroSello.y - altoSello / 2,
            width: anchoSello,
            height: altoSello,
            opacity: interpolate(ps, [0, 0.5], [0, 1], clamp),
            transform: `scale(${0.8 + 0.2 * ps})`,
            filter: `blur(${(1 - ps) * 16}px) drop-shadow(0 24px 50px rgba(0,0,0,.45)) drop-shadow(0 0 ${40 * destello}px rgba(84,186,0,.6))`,
          }}
        >
          <Img src={srcSello} style={{ width: "100%", height: "100%", display: "block" }} />
          <Brillo f={f} desde={T0.sello + 26} src={srcSello} dur={34} fuerza={0.85} />
        </div>
        {/* Mensaje */}
        <div style={{ position: "absolute", left: 40, right: 40, top: 860, textAlign: "center" }}>
          <div style={{ ...revela(f, T0.sello + 30, 20, 20, 8), fontFamily: FONT_TEXT, fontSize: 36, fontWeight: 600, color: "rgba(255,255,255,.88)" }}>
            W-IT alcanzó las <span style={{ color: C.green }}>6 designaciones</span>
          </div>
          <div
            style={{
              marginTop: 18,
              fontFamily: FONT_DISPLAY,
              fontSize: 70,
              lineHeight: 1.06,
              fontWeight: 700,
              letterSpacing: "-.025em",
              color: "#fff",
            }}
          >
            <span style={{ display: "inline-block", ...revela(f, T0.sello + 38, 22, 30, 14) }}>Solutions Partner for</span>{" "}
            <span style={{ display: "inline-block", color: C.green, ...revela(f, T0.sello + 44, 22, 30, 14) }}>Microsoft Cloud</span>
          </div>
        </div>
      </div>
    </>
  );

  /* --- 4. Firma --- */
  const pl = progreso(f, T0.logo, 30);
  const firma = f >= T0.logo && (
    <div style={{ position: "absolute", left: 0, right: 0, top: 330, display: "flex", flexDirection: "column", alignItems: "center" }}>
      <div
        style={{
          width: 400,
          height: 299,
          clipPath: `inset(${(1 - pl) * 100}% 0 0 0)`,
          transform: `translateY(${(1 - pl) * 40}px) scale(${1.04 - 0.04 * pl})`,
        }}
      >
        <Img src={staticFile("logo-white-mark.png")} style={{ width: "100%", height: "100%" }} />
      </div>
      <div style={{ ...revela(f, T0.logo + 14, 20, 16, 8), marginTop: 26, fontFamily: FONT_TEXT, fontSize: 34, fontWeight: 400, letterSpacing: ".02em", color: "rgba(255,255,255,.8)" }}>
        We Make It Simple
      </div>
      <div
        style={{
          ...revela(f, T0.logo + 24, 20, 16, 8),
          marginTop: 70,
          padding: "16px 34px",
          borderRadius: 999,
          border: `1.5px solid rgba(84,186,0,.6)`,
          background: "rgba(84,186,0,.1)",
          fontFamily: FONT_TEXT,
          fontSize: 30,
          fontWeight: 600,
          color: "#fff",
        }}
      >
        Solutions Partner for <span style={{ color: C.green }}>Microsoft Cloud</span>
      </div>
      <div style={{ ...revela(f, T0.logo + 32, 20, 16, 8), marginTop: 44, fontFamily: FONT_DISPLAY, fontSize: 44, fontWeight: 600, color: C.green, letterSpacing: ".01em" }}>
        w-it.cl
      </div>
    </div>
  );

  return (
    <AbsoluteFill style={{ background: FONDO, overflow: "hidden" }}>
      <Ambiente />
      <div style={{ position: "absolute", left: (width - 1080) / 2 + escLeft, top: escTop, width: 1080, height: ESC_H }}>
        {f < T0.hookFin + 4 && hook}
        {contador}
        {badges}
        {sello}
        {firma}
      </div>
    </AbsoluteFill>
  );
};
