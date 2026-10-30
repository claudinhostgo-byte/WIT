# Cómo publicitar en w-it.cl el contact center integral y el conector de mensajería

Borrador para decisión de Claudio Castillo · 2026-10-30 · v02 (reemplaza la v01, en `_versiones/`)

Insumos: ficha de seguridad del conector (Carolina González, 29-10), reporte estratégico FlexConnect (Tomás Recalde, 30-10), consolidado del conector WhatsApp y RRSS, propuesta comercial "Conector Redes Sociales" (abril 2026), arquitectura SNMS Bridge, documento de arquitectura del canal Instagram de Coopeuch (uso interno del cliente; solo referencia), base de conocimiento GTD (voz con Teams Phone y AudioCodes), página actual `/soluciones/contact-center/`.

---

## 0. Lo que cambia con el nuevo material

1. **Son dos ofertas, no una.** El consolidado deja resuelto que el conector "debe comercializarse separado de la solución de voz y de la solución integral" y recomienda "separar claramente tres ofertas: conector de mensajería, voz/audio y solución integral". Tomás lo lleva más lejos: producto propio, con nombre, agnóstico del CRM y de la IA, con planes por tráfico y landing con calculadora. Entonces el sitio necesita **una solución integral de contact center** (lo que pediste para AudioCodes) y, aparte, **una página de producto para el conector**, enlazadas entre sí.
2. **El conector ya tiene tracción real:** en producción en Easy (WhatsApp con Copilot Studio) y MetroPago (Instagram con Omnichannel en AKS), piloto en Coopeuch, ofrecido a GTD y La Araucana. Eso permite hablar de "en uso en retail, medios de pago y cooperativas" sin nombrar clientes hasta tener su autorización.
3. **Hay un argumento comercial nuevo y fuerte, pendiente de confirmar con Microsoft:** el canal nativo de WhatsApp en Dynamics 365 corre sobre Azure Communication Services, y Microsoft cerró esos servicios a clientes nuevos el 23-10-2026 (retiro el 30-09-2028). Si se confirma (pendiente 9 del reporte de Tomás, con Iván Gómez), quien implemente WhatsApp en Dynamics 365 desde ahora necesita un BSP como Twilio o un conector como el nuestro. Es la razón de ser del producto, y hay que decirla con precisión, no como amenaza.
4. **Hay cosas que no se pueden publicar todavía:** X, TikTok y LinkedIn (sin evidencia técnica), moderación de comentarios (no validada), precios (recomendación de Tomás, no aprobada; además precios y condiciones los define Comercial), SLA 24x7 (no resuelto), logos de clientes (sin autorización), y cualquier afirmación de seguridad más allá de lo confirmado en la ficha.

---

## 1. Concepto comercial 1: contact center integral (campaña)

**Claim:** **Llamadas, WhatsApp e Instagram. Un escritorio, un responsable.**

Alternativas: "Tu contact center completo sobre Microsoft, con la telefonía y WhatsApp resueltos." · "Deja de atender en tres pantallas."

**Pitch de 20 segundos:** Implementamos Dynamics 365 Contact Center y nos hacemos cargo de lo que normalmente queda fuera: la telefonía, con Microsoft Teams Phone y un SBC AudioCodes que conecta tu operador actual, y WhatsApp e Instagram, con un conector propio que los lleva al mismo escritorio del agente. Tus agentes atienden llamadas y mensajes en una sola pantalla, con el cliente identificado en el CRM y Copilot al lado. Un proyecto, un responsable.

**Tres mensajes:**
1. **Atención en una sola pantalla.** Dynamics 365 Contact Center: colas unificadas, IVR conversacional, casos y Copilot para el agente.
2. **Tu telefonía conectada.** Microsoft Teams Phone y SBC AudioCodes: conservas tu operador y tus números.
3. **WhatsApp e Instagram dentro del CRM.** Conector W-IT: los mensajes llegan a la misma cola que las llamadas, con el cliente identificado.

**CTA:** Conversemos. Te mostramos la solución funcionando en nuestro ambiente de demostración. [confirmar demo de voz con SBC operativa]

**Google Ads** (verificar largos en el Editor): títulos "Contact Center Microsoft" · "Llamadas, WhatsApp e Instagram" · "Un escritorio, un responsable" · "Partner Microsoft en Chile" · "Telefonía Teams Phone incluida". Descripciones: "Dynamics 365 Contact Center con telefonía Teams Phone y WhatsApp en el mismo escritorio." · "Implementación completa por W-IT: plataforma, voz con SBC AudioCodes y canales Meta."

---

## 2. Concepto comercial 2: el conector como producto

### 2.1 Nombre

Tomás propone **W-IT FlexConnect**. Dos reparos antes de adoptarlo:
- **"FlexConnect" es el nombre de una función conocida de las redes inalámbricas de Cisco** y "Flex" es la marca del contact center de Twilio, justo el competidor del que queremos diferenciarnos. Hay riesgo de confusión y de objeción de marca. Tomás mismo pide validar dominio y marca; yo lo haría antes de usarlo en cualquier material, con una búsqueda en INAPI y en los registros de EE. UU. [Comercial / Legal].
- Es un nombre en inglés para un producto cuyo diferencial declarado es "soporte local LATAM en español".

Alternativas para evaluar (ninguna verificada en INAPI): **W-IT Bridge** (recoge el nombre técnico SNMS Bridge que ya usa el equipo), **W-IT Conecta**, **W-IT Canales**. Mi recomendación: W-IT Bridge, corto, pronunciable en español e inglés y coherente con cómo lo llama el equipo técnico. Mientras no haya nombre registrado, en el sitio se publica como "Conector W-IT para WhatsApp e Instagram", que además es lo que la gente busca en Google.

### 2.2 Claim y pitch

**Claim:** **WhatsApp e Instagram, conectados directo con Meta a tu CRM y a tu agente de IA.**

El tagline de Tomás ("Conecta cada conversación, sin quedar atado a un proveedor") usa el remate "sin X" que acordamos evitar en el sitio; la idea se conserva en el pitch con un dato concreto.

**Pitch de 20 segundos:** El conector W-IT recibe los mensajes de WhatsApp e Instagram directamente desde las APIs de Meta y los entrega a Dynamics 365 Omnichannel o a un agente de Copilot Studio, con el cliente identificado y la conversación registrada en el CRM. No hay un intermediario de mensajería en el medio: la cuenta de WhatsApp y las páginas siguen siendo del cliente, se pagan a Meta las tarifas de Meta y nada más. Decide por regla a dónde va cada conversación: bot, ejecutivo o sistema actual. Corre en la nube de W-IT o en la del cliente.

**Cuatro pilares (en español, a partir de los de Tomás):**
1. **Directo con Meta.** Conexión a las APIs oficiales de WhatsApp Business e Instagram; los activos quedan en el Business Manager del cliente.
2. **Instagram incluido.** Canal que Dynamics 365 Omnichannel no trae de forma nativa.
3. **Enrutamiento por regla.** Cada conversación al destino correcto antes de entrar al sistema: bot, ejecutivo, segmento VIP, migración gradual desde el proveedor actual.
4. **Tu nube, tu CRM, tu IA.** Dynamics 365 y Copilot Studio como especialidad; otros destinos por API.

**Lo que NO se publica aún:** comentarios públicos y moderación (validar con Pablo Medina), X/TikTok/LinkedIn, outbound por Kafka, planes y precios, SLA 24x7, nombres y logos de clientes, comparación nominal con Twilio.

**CTA:** Conversemos. (La "calculadora de precio" de Tomás es buena idea, pero solo cuando Comercial apruebe planes con margen validado.)

---

## 3. Dónde va cada cosa en el sitio

| Pieza | Ubicación | Tipo de página |
|---|---|---|
| Contact center integral | `/soluciones/contact-center/` (existente) | Se agrega la sección "Cómo se arma la solución" con diagrama de tres capas (plataforma · voz · canales digitales) y una tarjeta por pieza; se reescribe la bajada con el claim. |
| Voz con Teams Phone y SBC AudioCodes | `/soluciones/contact-center/voz-teams-phone/` | Página de detalle colgando de la solución. No es producto propio. |
| Conector W-IT | `/productos/conector-whatsapp-instagram/` (nuevo; ruta definitiva con el nombre comercial cuando exista) | **Página de producto**, independiente de la solución: problema, cómo funciona (canales → conector → destinos), pilares, canales con estado (Disponible / En evaluación), modelos de despliegue, seguridad (solo lo confirmado), FAQ sobre cargos de Meta y requisitos, formulario. Enlazada desde Contact center, desde IA y agentes (Copilot Studio por WhatsApp) y desde el menú. |
| Landing de campaña | `/implementacion/contact-center/` (noindex) | Segundo paso, para Google Ads y para compartir con AudioCodes y Microsoft. |

Descartado: crear una novena solución "Contact center integral" (rompe la grilla de 8 y duplica el menú).

El sitio hoy no tiene sección de productos. Sería la primera página de "W-IT Products" en w-it.cl; conviene decidir si el menú gana una entrada "Productos" o si el conector cuelga de Soluciones como "producto propio". Recomiendo entrada "Productos" en el menú solo cuando haya al menos dos; mientras tanto, cuelga de Soluciones con etiqueta "Producto W-IT".

---

## 4. Lo que hay que resolver antes de publicar

| # | Tema | Bloquea a | Quién |
|---|---|---|---|
| 1 | Aprobación de compliance del conector (9 controles pendientes en la ficha). Mientras tanto solo se publica lo confirmado: no almacena conversaciones, cifrado en tránsito, base de configuración cifrada y sin acceso desde internet. | Página de producto | Claudio (aprobación), equipo del conector (respuestas), Encargado de Plataforma y Seguridad (alcance ISO) |
| 2 | Matriz certificada canal × función (texto, imagen, audio, documentos, plantillas, comentarios, routing, handoff). | Sección "Canales" de la página de producto | Pablo Medina |
| 3 | Confirmar con Microsoft el escenario de WhatsApp en Dynamics 365 tras el cierre de ACS a clientes nuevos. | El argumento central del producto | Carolina / Tomás con Iván Gómez |
| 4 | Nombre comercial del conector: búsqueda de marca y dominio. | Nombre en el sitio | Comercial / Legal |
| 5 | Uso de la marca y logo de AudioCodes; estatus de partner. Hasta entonces, "SBC certificado para Microsoft Teams". | Página de voz | Claudio con AudioCodes |
| 6 | Modelo con Meta (W-IT como Tech Provider o app del cliente) y hosting (W-IT o cliente). | Sección "Despliegue" | W-IT con el equipo del conector |
| 7 | Planes y precios: solo si Comercial los aprueba con unit economics validados. Si no, la página no muestra precios. | Calculadora | Tomás / Claudio / Comercial |
| 8 | Autorización de clientes para logos o referencias (Easy/Cencosud, MetroPago, Coopeuch, La Araucana). | Franja de clientes | Comercial |
| 9 | Corregir en la página actual la promoción de Azure Communication Services. | Independiente de todo lo demás | Claude, con tu OK |

Datos de clientes: el documento de Coopeuch y los manuales de MetroPago y Easy son material de esos clientes; en el sitio no se usa arquitectura, flujos ni cifras de ninguno.

---

## 5. Plan sugerido

1. **Esta semana:** corregir Azure Communication Services y reescribir la bajada de `/soluciones/contact-center/` con el claim integral. Publicar la sección "Cómo se arma la solución" nombrando "SBC certificado para Teams" y "conector W-IT".
2. **Con la matriz de Pablo y tu aprobación de compliance:** página de producto del conector con lo confirmado, sin precios ni logos.
3. **Con AudioCodes:** página de voz con marca y, si la dan, material co-marketing.
4. **Después:** landing de campaña, planes y calculadora cuando Comercial apruebe precios, y entrada "Productos" en el menú cuando haya un segundo producto.

Preguntas para ti:
- ¿De acuerdo con tratar el conector como producto aparte (página propia) y no como una capa dentro de la solución de contact center?
- ¿Avanzamos con "Conector W-IT para WhatsApp e Instagram" como nombre provisorio mientras Comercial revisa FlexConnect y las alternativas?
- ¿Partimos ya con el paso 1 (corrección de ACS y nueva bajada con el claim)?
