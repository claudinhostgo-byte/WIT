/*
 * Video de presentación W-IT (1920×1080, 30 fps).
 *
 * Identidad de movimiento (skill motion-design):
 * - Personalidad: Corporate con toques Premium (público enterprise).
 * - Curva firma: bezier(0.2, 0, 0, 1) para entradas; bezier(0.3, 0, 1, 1) para salidas.
 * - Paleta de duraciones: rápida 10f · estándar 18f · lenta 30f.
 * - Entrada única: subir 32px + fundido (la opacidad llega antes que la posición).
 * - Tres capas por escena: primaria (texto/tarjetas), secundaria (líneas,
 *   foco, checks) y ambiental (Tierra con zoom lento o brillo verde a la deriva).
 * - Escalonamientos ≤ ~500 ms.
 */
import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

export const C = {
  navy: "#1B3A50",
  navyDeep: "#14293A",
  green: "#54BA00",
  greenDark: "#3E8A00",
  greenLight: "#A8D97C",
  greenTint: "#F0F9E4",
  ink: "#242424",
  muted: "#616161",
  line: "#EBEBEB",
  bg: "#FAFAFA",
};
export const FONT_DISPLAY = '"Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif';
export const FONT_TEXT = '"Segoe UI Variable Text", "Segoe UI", system-ui, sans-serif';

export const EASE = Easing.bezier(0.2, 0, 0, 1);
export const EASE_EXIT = Easing.bezier(0.3, 0, 1, 1);
export const SINE = Easing.inOut(Easing.sin);
export const T = { quick: 10, std: 18, slow: 30 };
export const SOLAPE = 10; // frames de fundido entre escenas

export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const progreso = (f: number, desde: number, dur = T.std, easing = EASE) =>
  interpolate(f, [desde, desde + dur], [0, 1], { ...clamp, easing });

/** Entrada estándar: sube y aparece. */
export const entrada = (f: number, desde: number, dur = T.std, dist = 32): React.CSSProperties => {
  const p = progreso(f, desde, dur);
  return {
    opacity: interpolate(p, [0, 0.6], [0, 1], clamp),
    transform: `translateY(${(1 - p) * dist}px)`,
  };
};

/* ---------- Estructura común ---------- */

export const Escena: React.FC<{
  dur: number;
  fondo: string;
  entraConFundido?: boolean;
  children: React.ReactNode;
}> = ({ dur, fondo, entraConFundido = true, children }) => {
  const f = useCurrentFrame();
  const fondoOp = entraConFundido ? progreso(f, 0, SOLAPE, SINE) : 1;
  const salida = progreso(f, dur - SOLAPE - 2, SOLAPE, EASE_EXIT);
  return (
    <AbsoluteFill style={{ background: fondo, opacity: fondoOp }}>
      <AbsoluteFill
        style={{
          opacity: 1 - salida,
          transform: `translateY(${-16 * salida}px)`,
        }}
      >
        {children}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Capa ambiental oscura: la Tierra del hero del sitio, con zoom lento. */
export const FondoTierra: React.FC<{ dur: number; desde?: number; hasta?: number }> = ({
  dur,
  desde = 1.12,
  hasta = 1.02,
}) => {
  const f = useCurrentFrame();
  const s = interpolate(f, [0, dur], [desde, hasta], { ...clamp, easing: SINE });
  return (
    <AbsoluteFill>
      <Img
        src={staticFile("hero-tierra-duotono.jpg")}
        style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${s})` }}
      />
      <AbsoluteFill
        style={{
          background: `linear-gradient(100deg, ${C.navyDeep} 18%, rgba(20,41,58,.72) 55%, rgba(20,41,58,.25) 100%)`,
        }}
      />
    </AbsoluteFill>
  );
};

/** Capa ambiental clara: brillo verde que deriva lentamente. */
export const BrilloAmbiental: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, dur], [0, 1], { ...clamp, easing: SINE });
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(900px 700px at ${78 - 10 * t}% ${12 + 8 * t}%, rgba(84,186,0,.10), transparent 70%)`,
      }}
    />
  );
};

export const Eyebrow: React.FC<{ f: number; desde: number; oscuro?: boolean; children: React.ReactNode }> = ({
  f,
  desde,
  oscuro,
  children,
}) => (
  <div
    style={{
      ...entrada(f, desde, T.std, 16),
      fontFamily: FONT_TEXT,
      fontSize: 22,
      fontWeight: 600,
      letterSpacing: ".08em",
      textTransform: "uppercase",
      color: oscuro ? C.greenLight : C.greenDark,
    }}
  >
    {children}
  </div>
);

export const Titulo: React.FC<{
  f: number;
  desde: number;
  oscuro?: boolean;
  size?: number;
  maxWidth?: number;
  children: React.ReactNode;
}> = ({ f, desde, oscuro, size = 60, maxWidth = 1300, children }) => (
  <h2
    style={{
      ...entrada(f, desde),
      margin: "18px 0 0",
      fontFamily: FONT_DISPLAY,
      fontSize: size,
      lineHeight: 1.12,
      fontWeight: 600,
      letterSpacing: "-.015em",
      color: oscuro ? "#fff" : C.navy,
      maxWidth,
    }}
  >
    {children}
  </h2>
);

/** Línea verde que se dibuja (capa secundaria, follow-through del título). */
export const LineaAcento: React.FC<{ f: number; desde: number; ancho?: number }> = ({ f, desde, ancho = 120 }) => (
  <div
    style={{
      height: 6,
      borderRadius: 3,
      background: C.green,
      width: ancho * progreso(f, desde, T.slow),
      marginTop: 28,
    }}
  />
);

/* ---------- 1. Intro ---------- */

const Intro: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const pLogo = progreso(f, 8, T.slow);
  return (
    <Escena dur={dur} fondo={C.navyDeep} entraConFundido={false}>
      <FondoTierra dur={dur} desde={1.16} hasta={1.1} />
      <AbsoluteFill style={{ background: "rgba(20,41,58,.55)" }} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "column" }}>
        <Img
          src={staticFile("logo-white-mark.png")}
          style={{
            height: 220,
            opacity: interpolate(pLogo, [0, 0.5], [0, 1], clamp),
            transform: `translateY(${(1 - pLogo) * 24}px) scale(${0.94 + 0.06 * pLogo})`,
          }}
        />
        <LineaAcento f={f} desde={30} ancho={260} />
        <div
          style={{
            ...entrada(f, 42),
            marginTop: 30,
            display: "flex",
            alignItems: "center",
            gap: 16,
            fontFamily: FONT_TEXT,
            fontSize: 32,
            color: "rgba(255,255,255,.9)",
          }}
        >
          Microsoft Solutions Partner · Chile y Perú
          <Img src={staticFile("chile.svg")} style={{ height: 24, borderRadius: 3 }} />
          <Img src={staticFile("peru.svg")} style={{ height: 24, borderRadius: 3 }} />
        </div>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- 2. Hero ---------- */

const Hero: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const palabras = ["IA", "en", "producción", "sobre", "tus", "sistemas", "reales."];
  return (
    <Escena dur={dur} fondo={C.navyDeep}>
      <FondoTierra dur={dur} desde={1.1} hasta={1.0} />
      <AbsoluteFill style={{ padding: "0 160px", justifyContent: "center" }}>
        <Eyebrow f={f} desde={6} oscuro>
          Solutions Partner for Microsoft Cloud · Chile y Perú
        </Eyebrow>
        <h1
          style={{
            margin: "26px 0 0",
            fontFamily: FONT_DISPLAY,
            fontSize: 112,
            lineHeight: 1.04,
            fontWeight: 600,
            letterSpacing: "-.025em",
            color: "#fff",
            maxWidth: 1250,
          }}
        >
          {palabras.map((p, i) => (
            <span
              key={p}
              style={{
                display: "inline-block",
                marginRight: "0.24em",
                color: i >= 5 ? C.green : "#fff",
                ...entrada(f, 14 + i * 2, T.std + 4, 48),
              }}
            >
              {p}
            </span>
          ))}
        </h1>
        <p
          style={{
            ...entrada(f, 44),
            margin: "36px 0 0",
            fontFamily: FONT_TEXT,
            fontSize: 36,
            lineHeight: 1.4,
            color: "rgba(255,255,255,.82)",
            maxWidth: 1150,
          }}
        >
          Implementamos Dynamics 365, Power Platform, Azure y agentes de IA en grandes empresas y
          organismos públicos. Con equipo propio certificado y resultados medidos.
        </p>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- 3. Credenciales ---------- */

export const DESIGNACIONES = [
  "Business Applications",
  "Modern Work",
  "Data & AI",
  "Digital & App Innovation",
  "Infrastructure",
  "Security",
];

const Credenciales: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const inicioConteo = 40;
  const paso = 7; // cada designación aparece cuando el contador la alcanza
  const n = Math.max(0, Math.min(6, Math.floor((f - inicioConteo) / paso) + 1));
  const ultimoTick = inicioConteo + (n - 1) * paso;
  const pop = n > 0 ? 1 + 0.06 * (1 - progreso(f, ultimoTick, T.quick)) : 1;
  const pSello = progreso(f, 92, T.slow);
  const sombra = progreso(f, 100, T.slow); // la sombra llega después del sello
  return (
    <Escena dur={dur} fondo="#fff">
      <BrilloAmbiental dur={dur} />
      <AbsoluteFill style={{ padding: "0 140px", flexDirection: "row", alignItems: "center", gap: 100 }}>
        <div style={{ flex: 1.15 }}>
          <Eyebrow f={f} desde={4}>Credenciales verificables</Eyebrow>
          <Titulo f={f} desde={10} size={58}>
            Microsoft validó nuestra capacidad en todas sus áreas de soluciones.
          </Titulo>
          <div
            style={{
              ...entrada(f, 26),
              marginTop: 44,
              display: "flex",
              alignItems: "baseline",
              gap: 18,
              fontFamily: FONT_DISPLAY,
              color: C.navy,
            }}
          >
            <span
              style={{
                fontSize: 120,
                fontWeight: 700,
                color: C.green,
                display: "inline-block",
                transform: `scale(${pop})`,
                transformOrigin: "50% 80%",
                minWidth: 70,
              }}
            >
              {n}
            </span>
            <span style={{ fontSize: 44, fontWeight: 600 }}>de 6 designaciones</span>
          </div>
          <div style={{ marginTop: 26, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, maxWidth: 820 }}>
            {DESIGNACIONES.map((d, i) => {
              const desde = inicioConteo + i * paso;
              return (
                <div
                  key={d}
                  style={{
                    ...entrada(f, desde, T.std, 18),
                    display: "flex",
                    alignItems: "center",
                    gap: 14,
                    padding: "16px 22px",
                    borderRadius: 12,
                    background: C.greenTint,
                    fontFamily: FONT_TEXT,
                    fontSize: 27,
                    fontWeight: 600,
                    color: C.navy,
                  }}
                >
                  <Check f={f} desde={desde + 6} color={C.greenDark} />
                  {d}
                </div>
              );
            })}
          </div>
        </div>
        <div style={{ flex: 0.85, display: "flex", flexDirection: "column", alignItems: "center" }}>
          <Img
            src={staticFile("WIT-MicrosoftCloud-color.png")}
            style={{
              width: 620,
              opacity: interpolate(pSello, [0, 0.5], [0, 1], clamp),
              transform: `translateY(${(1 - pSello) * 40}px)`,
              // Sello oficial sin recorte: la sombra sigue su propia forma.
              filter: `drop-shadow(0 ${20 * sombra}px ${28 * sombra}px rgba(20,41,58,${0.2 * sombra}))`,
            }}
          />
          <div
            style={{
              ...entrada(f, 110),
              marginTop: 34,
              fontFamily: FONT_TEXT,
              fontSize: 30,
              fontWeight: 600,
              color: C.navy,
              textAlign: "center",
            }}
          >
            Un solo partner para todas tus soluciones Microsoft
          </div>
        </div>
      </AbsoluteFill>
    </Escena>
  );
};

/** Check que se dibuja (trazo SVG). */
export const Check: React.FC<{ f: number; desde: number; color: string; size?: number }> = ({
  f,
  desde,
  color,
  size = 26,
}) => {
  const p = progreso(f, desde, T.std);
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" style={{ flexShrink: 0 }}>
      <path
        d="M4 12.5l5 5L20 6.5"
        fill="none"
        stroke={color}
        strokeWidth={3}
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray={24}
        strokeDashoffset={24 * (1 - p)}
      />
    </svg>
  );
};

/* ---------- 4. Soluciones ---------- */

export const SOLUCIONES: { icono: string | null; nombre: string; texto: string }[] = [
  { icono: "m365-copilot", nombre: "Microsoft 365 Copilot y agentes de IA", texto: "Copilot y agentes que trabajan sobre tus datos, con gobierno desde el inicio." },
  { icono: "d365-sales", nombre: "Microsoft Dynamics 365 Sales y Customer Service", texto: "Una sola vista del cliente, de la venta a la postventa." },
  { icono: "d365-contact-center", nombre: "Microsoft Dynamics 365 Contact Center", texto: "Voz, chat, WhatsApp y correo en una sola plataforma, con IA para tus agentes." },
  { icono: "d365-business-central", nombre: "Microsoft Dynamics 365 Business Central y Finance", texto: "ERP que cierra a tiempo y escala contigo." },
  { icono: "fabric", nombre: "Microsoft Fabric y Power BI", texto: "Datos unificados para decidir." },
  { icono: "power-platform", nombre: "Microsoft Power Platform", texto: "Procesos sin planillas paralelas." },
  { icono: "azure", nombre: "Microsoft Azure", texto: "Migración, modernización y operación en Azure, con costos bajo control." },
  // Sin ícono oficial: la guía de Microsoft no permite usar los de Entra/Purview en marketing.
  { icono: null, nombre: "Microsoft Purview y Microsoft Entra", texto: "Identidades, accesos y cargas en la nube protegidos con el modelo Zero Trust." },
];

export const Escudo: React.FC = () => (
  <svg width={64} height={64} viewBox="0 0 24 24">
    <path d="M12 2.5l7.5 3v6c0 4.6-3.2 8.4-7.5 10-4.3-1.6-7.5-5.4-7.5-10v-6z" fill={C.navy} />
    <path d="M8.5 12l2.4 2.4 4.6-4.8" fill="none" stroke="#fff" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const Soluciones: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const inicioFoco = 84;
  const pasoFoco = 18;
  return (
    <Escena dur={dur} fondo={C.bg}>
      <BrilloAmbiental dur={dur} />
      <AbsoluteFill style={{ padding: "110px 140px 0" }}>
        <Eyebrow f={f} desde={4}>Soluciones Microsoft</Eyebrow>
        <Titulo f={f} desde={10} size={56} maxWidth={1500}>
          Implementamos Microsoft Dynamics 365, Power Platform, Azure y Copilot.
        </Titulo>
        <div style={{ marginTop: 60, display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 26 }}>
          {SOLUCIONES.map((s, i) => {
            const desde = 26 + i * 2;
            // Foco que recorre las tarjetas (como en el sitio): sube y se enciende el borde.
            const inicio = inicioFoco + i * pasoFoco;
            const on = progreso(f, inicio, T.quick) * (1 - progreso(f, inicio + pasoFoco - 4, T.quick - 4, EASE_EXIT));
            return (
              <div
                key={s.nombre}
                style={{
                  ...entrada(f, desde, T.std + 4, 40),
                  height: 300,
                  background: "#fff",
                  borderRadius: 18,
                  border: `2px solid ${on > 0.01 ? `rgba(84,186,0,${on})` : C.line}`,
                  boxShadow: `0 ${2 + 14 * on}px ${4 + 30 * on}px rgba(0,0,0,${0.08 + 0.06 * on})`,
                  padding: "30px 30px",
                  position: "relative",
                  overflow: "hidden",
                }}
              >
                <div style={{ transform: `translateY(${-8 * on}px)` }}>
                  {s.icono ? (
                    <Img src={staticFile(`ms/${s.icono}.svg`)} style={{ width: 64, height: 64 }} />
                  ) : (
                    <Escudo />
                  )}
                  <div style={{ marginTop: 22, fontFamily: FONT_DISPLAY, fontSize: 28, lineHeight: 1.2, fontWeight: 600, color: C.navy }}>
                    {s.nombre}
                  </div>
                  <div style={{ marginTop: 12, fontFamily: FONT_TEXT, fontSize: 22, lineHeight: 1.4, color: C.muted }}>
                    {s.texto}
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

/* ---------- 5. Cómo trabajamos ---------- */

export const METODOS = [
  { tag: "CRM, ERP y Contact Center", titulo: "Success by Design, por olas", fases: ["Descubrir", "Diseñar", "Construir", "Adoptar", "Operar"] },
  { tag: "Apps, automatización, Power BI y Fabric", titulo: "Fusion teams y sprints", fases: ["Idear", "Prototipar", "Construir", "Publicar", "Escalar"] },
  { tag: "Nube, infraestructura y seguridad", titulo: "Cloud Adoption Framework, por olas", fases: ["Estrategia", "Planificar", "Preparar", "Adoptar", "Gobernar y operar"] },
  { tag: "Copilot, Copilot Studio y Azure AI Foundry", titulo: "Del prototipo a producción, con evaluación continua", fases: ["Explorar", "Gobernar", "Construir y evaluar", "Desplegar", "Operar y expandir"] },
];

const Metodologias: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const inicioRiel = 60;
  const durRiel = 90;
  return (
    <Escena dur={dur} fondo="#fff">
      <BrilloAmbiental dur={dur} />
      <AbsoluteFill style={{ padding: "0 140px", justifyContent: "center" }}>
        <Eyebrow f={f} desde={4}>Cómo trabajamos</Eyebrow>
        <Titulo f={f} desde={10} size={56}>
          Cuatro marcos ágiles, uno para cada tipo de proyecto.
        </Titulo>
        <div style={{ marginTop: 60, display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 34 }}>
          {METODOS.map((m, i) => {
            // Ola: cada riel parte un poco después del anterior.
            const avance = interpolate(f, [inicioRiel + i * 4, inicioRiel + i * 4 + durRiel], [0, 1], clamp);
            return (
              <div key={m.titulo} style={{ ...entrada(f, 26 + i * 3, T.std + 4, 40) }}>
                <div style={{ fontFamily: FONT_TEXT, fontSize: 19, fontWeight: 600, letterSpacing: ".04em", textTransform: "uppercase", color: C.greenDark, minHeight: 54 }}>
                  {m.tag}
                </div>
                <div style={{ marginTop: 10, fontFamily: FONT_DISPLAY, fontSize: 30, lineHeight: 1.2, fontWeight: 600, color: C.navy, minHeight: 76 }}>
                  {m.titulo}
                </div>
                <div style={{ position: "relative", marginTop: 30, paddingLeft: 44 }}>
                  <div style={{ position: "absolute", left: 13, top: 14, bottom: 14, width: 4, borderRadius: 2, background: C.line }} />
                  <div style={{ position: "absolute", left: 13, top: 14, width: 4, borderRadius: 2, background: C.green, height: `calc((100% - 28px) * ${avance})` }} />
                  {m.fases.map((fase, j) => {
                    const umbral = j / (m.fases.length - 1);
                    const activa = progreso(avance * durRiel, umbral * durRiel - 2, T.quick);
                    return (
                      <div key={fase} style={{ position: "relative", height: 76, display: "flex", alignItems: "center" }}>
                        <div
                          style={{
                            position: "absolute",
                            left: -44,
                            width: 30,
                            height: 30,
                            borderRadius: 15,
                            background: activa > 0.5 ? C.green : "#fff",
                            border: `3px solid ${activa > 0.5 ? C.green : C.line}`,
                            transform: `scale(${1 + 0.15 * Math.sin(Math.PI * activa)})`,
                            color: "#fff",
                            fontFamily: FONT_TEXT,
                            fontSize: 15,
                            fontWeight: 700,
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                          }}
                        >
                          {j + 1}
                        </div>
                        <span style={{ fontFamily: FONT_TEXT, fontSize: 25, color: activa > 0.5 ? C.navy : C.muted, fontWeight: activa > 0.5 ? 600 : 400 }}>
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

/* ---------- 6. Trust Center ---------- */

export const DocIcono: React.FC = () => (
  <svg width={72} height={72} viewBox="0 0 24 24">
    <rect x="4.5" y="2.5" width="15" height="19" rx="2.5" fill="#fff" />
    <path d="M8 8h8M8 11.5h8M8 15h5" stroke={C.navy} strokeWidth={1.6} strokeLinecap="round" />
  </svg>
);

/** Sello de certificación sin recortar, sobre fondo blanco. */
export const Sello: React.FC<{ src: string }> = ({ src }) => (
  <div style={{ width: 96, height: 96, borderRadius: 16, background: "#fff", display: "flex", alignItems: "center", justifyContent: "center" }}>
    <Img src={staticFile(src)} style={{ width: 84, height: 84, objectFit: "contain" }} />
  </div>
);

const Trust: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const items: { visual: React.ReactNode; titulo: string; texto: string }[] = [
    { visual: <Sello src="SGS_ISO_9001_round_TCL_LR.jpg" />, titulo: "ISO 9001", texto: "Gestión de calidad, certificada por SGS" },
    { visual: <Sello src="SGS_ISO-IEC_27001_TCL_LR.jpg" />, titulo: "ISO/IEC 27001", texto: "Seguridad de la información, certificada por SGS" },
    { visual: <div style={{ width: 96, height: 96, borderRadius: 48, background: "#fff", display: "flex", alignItems: "center", justifyContent: "center" }}><Img src={staticFile("ms/azure.svg")} style={{ width: 58 }} /></div>, titulo: "Azure Chile Central", texto: "Implementaciones en la región Azure de Chile" },
    { visual: <div style={{ width: 96, height: 96, borderRadius: 48, background: C.green, display: "flex", alignItems: "center", justifyContent: "center" }}><DocIcono /></div>, titulo: "IA responsable", texto: "Política de IA responsable publicada" },
  ];
  return (
    <Escena dur={dur} fondo={C.navyDeep}>
      <FondoTierra dur={dur} desde={1.0} hasta={1.08} />
      <AbsoluteFill style={{ background: "rgba(20,41,58,.6)" }} />
      <AbsoluteFill style={{ padding: "0 140px", justifyContent: "center" }}>
        <Eyebrow f={f} desde={4} oscuro>Trust Center</Eyebrow>
        <Titulo f={f} desde={10} oscuro size={64}>
          Todo lo que declaramos se puede verificar.
        </Titulo>
        <LineaAcento f={f} desde={24} />
        <div style={{ marginTop: 80, display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 30 }}>
          {items.map((it, i) => {
            const desde = 34 + i * 4;
            return (
              <div
                key={it.titulo}
                style={{
                  ...entrada(f, desde, T.std + 4, 40),
                  background: "rgba(255,255,255,.06)",
                  border: "1px solid rgba(255,255,255,.14)",
                  borderRadius: 20,
                  padding: "34px 30px",
                  minHeight: 330,
                }}
              >
                {it.visual}
                <div style={{ marginTop: 26, display: "flex", alignItems: "flex-start", gap: 12, fontFamily: FONT_DISPLAY, fontSize: 34, lineHeight: 1.2, fontWeight: 600, color: "#fff" }}>
                  <div style={{ marginTop: 4 }}><Check f={f} desde={desde + 14} color={C.green} size={32} /></div>
                  {it.titulo}
                </div>
                <div style={{ marginTop: 12, fontFamily: FONT_TEXT, fontSize: 24, lineHeight: 1.4, color: "rgba(255,255,255,.78)" }}>
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

/* ---------- 7. Clientes ---------- */

export const LOGOS = [
  "codelco.png", "bhp.png", "arauco.png", "sqm.png", "latam.png", "entel.png", "cencosud.png", "agrosuper.png",
  "antofagasta-minerals.png", "mallplaza.png", "banco-ripley.png", "teleton.png",
  "banchile.png", "coopeuch.png", "transbank.png", "redbanc.png", "mutual.png", "unacem.png", "cibertec.png",
  "chileatiende.png", "corfo.png", "sence.png", "udechile.png", "umayor.png", "larrainvial.svg",
];

export const FilaLogos: React.FC<{ logos: string[]; f: number; sentido: 1 | -1; desde: number }> = ({ logos, f, sentido, desde }) => {
  const ancho = 300;
  const total = logos.length * ancho;
  const x = (f * 2.2 * sentido) % total; // deriva continua (capa ambiental)
  const base = sentido === 1 ? -total : 0;
  return (
    <div style={{ ...entrada(f, desde, T.std + 4, 30), overflow: "hidden", width: "100%", height: 160 }}>
      <div style={{ display: "flex", transform: `translateX(${base + x}px)`, width: total * 2 }}>
        {[...logos, ...logos].map((l, i) => (
          <div
            key={i}
            style={{
              width: ancho - 24,
              marginRight: 24,
              height: 150,
              flexShrink: 0,
              background: "#fff",
              border: `1px solid ${C.line}`,
              borderRadius: 18,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Img
              src={staticFile(`clientes/${l}`)}
              style={{ maxHeight: 64, maxWidth: 190, filter: "grayscale(1)", opacity: 0.7 }}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

const Clientes: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  return (
    <Escena dur={dur} fondo={C.bg}>
      <BrilloAmbiental dur={dur} />
      <AbsoluteFill style={{ justifyContent: "center" }}>
        <div style={{ padding: "0 140px" }}>
          <Eyebrow f={f} desde={4}>Clientes</Eyebrow>
          <Titulo f={f} desde={10} size={60}>
            Grandes empresas y organismos públicos en Chile y Perú.
          </Titulo>
        </div>
        <div style={{ marginTop: 80, display: "flex", flexDirection: "column", gap: 26 }}>
          <FilaLogos logos={LOGOS.slice(0, 12)} f={f} sentido={-1} desde={26} />
          <FilaLogos logos={LOGOS.slice(12)} f={f} sentido={1} desde={32} />
        </div>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- 8. Cierre ---------- */

const Cierre: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  // Botón: anticipación (0.97) → leve sobrepaso (1.02) → reposo, como un "clic" invitando a conversar.
  const presion = interpolate(f, [70, 74, 80, 90], [1, 0.97, 1.02, 1], { ...clamp, easing: EASE });
  return (
    <Escena dur={dur + SOLAPE} fondo={C.navyDeep}>
      <FondoTierra dur={dur} desde={1.04} hasta={1.12} />
      <AbsoluteFill style={{ background: "rgba(20,41,58,.5)" }} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "column", textAlign: "center" }}>
        <Img src={staticFile("logo-white-mark.png")} style={{ height: 130, ...entrada(f, 6, T.slow, 24) }} />
        <h2
          style={{
            ...entrada(f, 20),
            margin: "54px 0 0",
            fontFamily: FONT_DISPLAY,
            fontSize: 88,
            fontWeight: 600,
            letterSpacing: "-.02em",
            color: "#fff",
          }}
        >
          Conversemos sobre tu proyecto.
        </h2>
        <p style={{ ...entrada(f, 32), margin: "22px 0 0", fontFamily: FONT_TEXT, fontSize: 34, color: "rgba(255,255,255,.82)" }}>
          Cuéntanos qué tienes en mente y te respondemos en menos de 1 día hábil.
        </p>
        <div
          style={{
            ...entrada(f, 46),
            marginTop: 54,
            display: "flex",
            alignItems: "center",
            gap: 34,
          }}
        >
          <div
            style={{
              transform: `scale(${presion})`,
              background: C.green,
              color: "#fff",
              fontFamily: FONT_TEXT,
              fontSize: 34,
              fontWeight: 600,
              padding: "22px 48px",
              borderRadius: 14,
              boxShadow: `0 ${10 * presion}px 30px rgba(84,186,0,.35)`,
            }}
          >
            Conversemos
          </div>
          <span style={{ fontFamily: FONT_TEXT, fontSize: 40, fontWeight: 600, color: "#fff" }}>w-it.cl</span>
        </div>
      </AbsoluteFill>
    </Escena>
  );
};

/* ---------- Línea de tiempo ---------- */

const ESCENAS: { C: React.FC<{ dur: number }>; dur: number }[] = [
  { C: Intro, dur: 120 },
  { C: Hero, dur: 180 },
  { C: Credenciales, dur: 210 },
  { C: Soluciones, dur: 270 },
  { C: Metodologias, dur: 240 },
  { C: Trust, dur: 180 },
  { C: Clientes, dur: 180 },
  { C: Cierre, dur: 150 },
];

const inicios = ESCENAS.reduce<number[]>((acc, e, i) => {
  acc.push(i === 0 ? 0 : acc[i - 1] + ESCENAS[i - 1].dur - SOLAPE);
  return acc;
}, []);

export const DURACION_TOTAL = inicios[inicios.length - 1] + ESCENAS[ESCENAS.length - 1].dur;

export const WitPresentacion: React.FC = () => (
  <AbsoluteFill style={{ background: C.navyDeep }}>
    {ESCENAS.map(({ C: Comp, dur }, i) => (
      <Sequence key={i} from={inicios[i]} durationInFrames={dur}>
        <Comp dur={dur} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
