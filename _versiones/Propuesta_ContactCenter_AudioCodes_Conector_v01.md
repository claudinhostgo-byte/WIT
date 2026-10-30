# Cómo publicitar en w-it.cl la solución integral de contact center

Borrador para decisión de Claudio Castillo · 2026-10-30 · v01
Insumos: ficha de seguridad del conector WhatsApp (Carolina González, 29-10-2026), documento de arquitectura del canal Instagram de Coopeuch (uso interno del cliente, solo como referencia de lo que sabemos hacer), base de conocimiento GTD Contact Center (reuniones con Microsoft y aprendizajes de voz), página actual `/soluciones/contact-center/`.

---

## 0. Concepto de campaña (corto, para sitio, LinkedIn y Ads)

**Claim recomendado:** **Llamadas, WhatsApp e Instagram. Un escritorio, un responsable.**

Por qué funciona: dice qué canales entran (lo que el cliente ya vive), promete lo que hoy no tiene (todo en una pantalla) y nombra el diferencial de W-IT frente a comprar licencias por un lado, telefonía por otro y un proveedor de mensajería por otro (un solo responsable). Se entiende sin conocer Microsoft.

Alternativas:
- **Tu contact center completo sobre Microsoft. Con la telefonía y WhatsApp resueltos.** (más explícito con la marca Microsoft, mejor para búsquedas)
- **Deja de atender en tres pantallas.** (más emocional, sirve como gancho en redes; se acompaña del claim principal)

**Pitch de 20 segundos (para reuniones y post):**
Implementamos Dynamics 365 Contact Center y nos hacemos cargo de lo que normalmente queda fuera: la telefonía, con Microsoft Teams Phone y un SBC AudioCodes que conecta tu operador actual, y WhatsApp e Instagram, con un conector propio que los lleva al mismo escritorio del agente. Tus agentes atienden llamadas y mensajes en una sola pantalla, con el cliente identificado en el CRM y Copilot al lado. Un proyecto, un responsable.

**Tres mensajes (uno por pieza), para tarjetas o carrusel:**
1. **Atención en una sola pantalla.** Dynamics 365 Contact Center: colas unificadas, IVR conversacional, casos y Copilot para el agente.
2. **Tu telefonía conectada.** Microsoft Teams Phone y SBC AudioCodes: conservas tu operador y tus números.
3. **WhatsApp e Instagram dentro del CRM.** Conector W-IT: los mensajes llegan a la misma cola que las llamadas, con el cliente identificado.

**CTA:** Conversemos. Te mostramos la solución funcionando en nuestro ambiente de demostración. [confirmar demo con SBC operativa]

**Google Ads (verificar largos en el Editor; títulos ≤ 30, descripciones ≤ 90):**
- Títulos: "Contact Center Microsoft" · "Llamadas, WhatsApp e Instagram" · "Un escritorio, un responsable" · "Partner Microsoft en Chile" · "Telefonía Teams Phone incluida"
- Descripciones: "Dynamics 365 Contact Center con telefonía Teams Phone y WhatsApp en el mismo escritorio." · "Implementación completa por W-IT: plataforma, voz con SBC AudioCodes y canales Meta."

**Lo que el concepto evita a propósito:** nombrar a Twilio, prometer ahorro por mensaje, certificar seguridad del conector antes de la aprobación de compliance, usar el logo de AudioCodes sin su autorización (ver sección 4).

---

## 1. Qué vendemos (en una frase)

Un contact center completo sobre Microsoft Dynamics 365 Contact Center, con la telefonía resuelta mediante Microsoft Teams Phone y un SBC AudioCodes, y con WhatsApp e Instagram conectados al escritorio del agente mediante un conector propio de W-IT.

Tres piezas, tres preguntas del cliente:

| Pieza | Qué resuelve | Pregunta del cliente que responde |
|---|---|---|
| Dynamics 365 Contact Center (+ Customer Service, Copilot Studio) | Escritorio del agente, colas y enrutamiento unificado, IVR conversacional, casos, supervisión, Copilot para el agente | "¿Dónde trabajan mis agentes y cómo se gestiona la atención?" |
| Voz: Teams Phone Extensibility + Direct Routing + SBC AudioCodes | Que las llamadas del operador telefónico lleguen y salgan del contact center con calidad y con la numeración del cliente | "¿Cómo conecto mi telefonía actual?" |
| Conector W-IT para canales Meta (WhatsApp e Instagram) | Que los mensajes de WhatsApp e Instagram entren a las mismas colas que la voz y el chat, con el cliente identificado en el CRM | "¿Y WhatsApp? ¿Tengo que contratar otro proveedor?" |

La propuesta de valor no es ninguna pieza por separado: es que W-IT entrega y responde por las tres y por su integración. Eso es lo que hoy la página no dice.

---

## 2. Dónde ponerlo en el sitio: tres alternativas

### A. Profundizar la solución existente `/soluciones/contact-center/` (recomendada)

- Se mantiene la grilla de 8 soluciones (4 columnas) y la URL que ya posiciona Google Ads.
- Se agrega una sección nueva **"Cómo se arma la solución"** con un diagrama de tres capas (plataforma, voz, canales digitales) y una tarjeta por pieza.
- Cada pieza tiene su **página de detalle** colgando de la solución:
  - `/soluciones/contact-center/plataforma/` (Dynamics 365 Contact Center y Customer Service)
  - `/soluciones/contact-center/voz-teams-phone-audiocodes/`
  - `/soluciones/contact-center/conector-whatsapp-instagram/`
- Pros: coherente con la arquitectura del sitio, no compite con la página madre en buscadores, aprovecha la metodología Success by Design y el autodiagnóstico ya enlazados.
- Contras: el detalle queda a un clic de distancia; hay que diseñar un componente nuevo (diagrama de capas) sin recargar la página.

### B. Nueva solución "Contact center integral" como novena solución

- Pros: máxima visibilidad en el menú y el home.
- Contras: rompe la grilla de 4 columnas, duplica la solución actual de contact center y confunde en el menú (dos entradas casi iguales). No la recomiendo.

### C. Landing comercial aparte, sin indexar (`/implementacion/contact-center/`)

- Página larga tipo campaña, para enviar a los contactos de AudioCodes y Microsoft y para una futura campaña de Google Ads.
- Pros: se construye rápido con los componentes de las landings actuales; permite un discurso más agresivo sin tocar el sitio público.
- Contras: no mejora el sitio para quien llega orgánico.

**Recomendación:** A ahora, y C como segundo paso cuando haya campaña de Ads o material co-marketing con AudioCodes. B descartada.

---

## 3. Cómo contar cada pieza (borrador de copy)

Criterios: nombres oficiales de producto, títulos descriptivos, nada de "X, no Y" ni remates "sin X", CTA siempre "Conversemos".

### 3.1 Sección "Cómo se arma la solución" (en la página madre)

**Título:** Plataforma, voz y canales digitales en un solo escritorio.
**Bajada:** Implementamos Dynamics 365 Contact Center, conectamos tu telefonía con Microsoft Teams Phone y un SBC AudioCodes, e integramos WhatsApp e Instagram con un conector desarrollado por W-IT. Tú tratas con un solo responsable.

Diagrama de tres capas (de arriba hacia abajo): **Agente y supervisor** (Dynamics 365 Contact Center, Customer Service, Copilot) · **Voz** (Teams Phone, Direct Routing, SBC AudioCodes, operador telefónico) · **Canales digitales** (WhatsApp e Instagram vía conector W-IT, chat web, correo).

### 3.2 Página "Plataforma: Dynamics 365 Contact Center"

- Qué hace: colas y enrutamiento unificado para voz y digital, IVR conversacional con Copilot Studio, escritorio del agente con historial del cliente, casos y SLA con Customer Service, tableros de supervisión en tiempo real, Copilot para resumen y cierre de la conversación.
- Cuándo conviene: cuando el cliente ya usa Microsoft 365 o Dynamics 365 y quiere dejar de operar una central y un CRM separados.
- Enlace a la página oficial de Microsoft (como ya hacemos en las demás soluciones).

### 3.3 Página "Voz: Teams Phone y SBC AudioCodes"

- Qué hace: las llamadas entran y salen por Microsoft Teams Phone usando Direct Routing; un Session Border Controller (SBC) AudioCodes, físico o virtual en Azure, conecta las troncales SIP del operador telefónico del cliente con Teams y con el contact center. El cliente conserva su numeración y su operador.
- Qué hace W-IT: diseño de la arquitectura de voz, instalación y configuración del SBC junto al operador, pruebas de calidad y de carga, puesta en producción y soporte. Contamos con un ambiente de demostración propio con SBC AudioCodes en Azure [confirmar que se puede declarar].
- Cuándo conviene: cuando hay central telefónica o troncales SIP que se quieren conservar, o cuando el cliente es una empresa de telecomunicaciones que ya opera SBC.
- Nota de arquitectura que hay que incluir: esta es la ruta que Microsoft recomienda para nuevos proyectos. Azure Communication Services dejó de aceptar nuevos clientes en sus servicios independientes (incluido Direct Routing) el 23-10-2026 y los retira el 30-09-2028. **La página actual todavía promociona Azure Communication Services: hay que corregirlo aunque no se haga nada más.**

### 3.4 Página "Conector W-IT para WhatsApp e Instagram"

- Qué hace: conecta WhatsApp Business e Instagram (APIs de Meta) con Dynamics 365 Customer Service y Contact Center. Los mensajes llegan a las mismas colas que las llamadas y el chat; el agente responde desde el mismo escritorio; el cliente queda identificado en el CRM y la conversación vinculada a su contacto, caso u oportunidad.
- Cómo funciona (nivel cliente): el conector corre en Azure y actúa como paso entre Meta y Dynamics. No almacena conversaciones. La comunicación va cifrada en ambos sentidos; solo guarda configuraciones, cifradas y sin acceso desde internet.
- Opciones: operado por W-IT o desplegado en la suscripción de Azure del cliente [confirmar cuál se ofrece; la ficha lo marca pendiente].
- Cuándo conviene: cuando el cliente ya atiende por WhatsApp o Instagram fuera del CRM, o quiere incorporar un agente de IA de Copilot Studio en esos canales.
- Lo que NO decimos: no nombrar a Twilio ni a otros BSP, no prometer ahorro por mensaje (Meta cobra igual por conversación; lo que se evita es el intermediario y su margen, pero el modelo con Meta no está definido), no declarar ISO 27001 ni SOC 2 para el conector.

---

## 4. Lo que hay que resolver antes de publicar

| # | Tema | Por qué bloquea | Quién |
|---|---|---|---|
| 1 | **Aprobación de compliance del conector.** La ficha de Carolina dice que el conector se ofrece "sujeto a validación de compliance" y deja 9 controles pendientes (TLS mínimo, logs, webhooks, identidad, accesos, región, operación). | Publicarlo en el sitio es ofrecerlo a todo el mercado. Lo mínimo es que los controles pendientes estén respondidos y que tú firmes la aprobación interna. Mientras tanto, se puede publicar la pieza describiendo solo lo confirmado (no almacena, cifrado, base de configuración protegida). | Claudio (aprobación), equipo del conector (respuestas), Encargado de Plataforma y Seguridad (alcance ISO) |
| 2 | **Uso de la marca AudioCodes.** Nombrar el producto como componente es un uso descriptivo normal; usar el logo o decir "partner AudioCodes" requiere su autorización. | Marca de terceros. Además el sitio no tiene sección de alianzas por decisión tuya. | Claudio con AudioCodes en las reuniones en curso: pedir estatus de partner y kit de co-marketing |
| 3 | **Modelo con Meta** (W-IT como Tech Provider o app del propio cliente). | Cambia el texto de "Opciones" y la responsabilidad sobre los datos. | W-IT con el equipo del conector |
| 4 | **Instagram como canal generalizable.** Lo construido para Coopeuch es un canal personalizado específico (identificación del socio contra su core, flujos propios). | Hay que confirmar que el conector productizado cubre Instagram y no solo WhatsApp antes de prometerlo. | Carolina |
| 5 | **Ambiente de demo con SBC AudioCodes en el tenant W-IT.** | Es un argumento fuerte ("lo puedes ver funcionando"), pero hay que confirmar que está operativo y mostrable. | Carolina |
| 6 | **Corrección de Azure Communication Services** en la página actual. | Independiente de todo lo anterior; hoy promocionamos un servicio que ya no acepta clientes nuevos. | Claude, con tu OK |

Datos de clientes: el documento de Coopeuch es de uso interno de ese cliente. En el sitio solo se usa lo que ya está publicado en su ficha de cliente (omnicanalidad y redes sociales); nada de la arquitectura ni de los flujos.

---

## 5. Plan sugerido

1. Esta semana: corregir la mención a Azure Communication Services y reescribir la bajada de `/soluciones/contact-center/` con las tres piezas (sin nombrar AudioCodes todavía si no hay respuesta de ellos: "SBC certificado para Microsoft Teams").
2. Con tu aprobación de compliance y la respuesta de AudioCodes: publicar la sección "Cómo se arma la solución" y las tres páginas de detalle.
3. Después: landing comercial sin indexar para campaña y para compartir con AudioCodes y Microsoft; sumar la pieza de voz al autodiagnóstico de atención y ventas.

Preguntas para ti:
- ¿Confirmas la alternativa A (profundizar la solución actual) o prefieres la landing aparte como primer paso?
- ¿AudioCodes ya autorizó uso de marca o logo, o lo pedimos en la próxima reunión?
- ¿El conector se publica ya con lo confirmado, o esperamos las respuestas pendientes del equipo del conector?
