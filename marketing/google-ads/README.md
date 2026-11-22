# Google Ads · Campañas de búsqueda W-IT (Chile y Perú)

Publicadas el 2026-10-13 con Google Ads Editor (cuenta 807-842-4837). Estado: activas, en aprendizaje.
Objetivo: que empresas que buscan implementar Microsoft Dynamics 365 o IA de Microsoft **envíen el formulario de contacto**, directamente o después de un autodiagnóstico.

## Estructura

| Campaña | Presupuesto diario | Máx. mensual (×30,4) | Landing |
|---|---|---|---|
| W-IT \| Búsqueda \| Dynamics 365 \| CL-PE | $4.200 | $127.680 | https://w-it.cl/implementacion/dynamics-365/ |
| W-IT \| Búsqueda \| IA y agentes Microsoft \| CL-PE | $2.300 | $69.920 | https://w-it.cl/implementacion/agentes-de-ia/ |
| **Total** | **$6.500** | **$197.600** | |

- Reparto 65/35 a favor de Dynamics 365: es la búsqueda con mayor intención de compra. Las búsquedas de IA traen más curiosos y estudiantes.
- Grupos de anuncios: Dynamics (Partner e implementación · Sales y Customer Service · Contact Center · Business Central y Finance) e IA (Copilot Studio y agentes · Microsoft 365 Copilot · Azure AI e IA empresarial).
- Solo concordancia de frase y exacta. La amplia gasta un presupuesto chico en búsquedas sin intención.
- Claude/Anthropic: descartado por ahora. "claude" y "anthropic" quedan como negativas de la campaña de IA.

Para editar el material, modifica `generar.py` y ejecuta `python marketing/google-ads/generar.py`. El script valida los límites de caracteres de Google y regenera los CSV.

## Pasos de configuración (en este orden)

### 1. Conversiones (antes de activar nada)
En Google Ads > Objetivos > Conversiones > Nueva acción de conversión > Sitio web > configurar manualmente:

| Acción | Categoría | Recuento | Ventana | Uso |
|---|---|---|---|---|
| Formulario de contacto W-IT | Enviar formulario de clientes potenciales | Una | 90 días | **Principal** |
| Autodiagnóstico completado | Otro / Contacto | Una | 90 días | Secundaria (solo observación) |

Elige "Configurar con Google tag" > "Instalar la etiqueta tú mismo" y copia el **ID (AW-…)** y la **etiqueta de conversión** de cada acción. Hay que pasarlos a `GOOGLE_ADS_ID` y `GOOGLE_ADS_CONVERSIONES` en `build/build.py` y publicar el sitio. Sin esos datos, el sitio no carga nada de Google.

El sitio carga la etiqueta de Google **solo a visitantes que llegaron desde un aviso** (gclid/gbraid/wbraid en la URL; se recuerda 90 días) y sin personalización de anuncios. El aviso de privacidad ya lo declara.

### 2. Configuración de cada campaña
- Tipo: **Búsqueda**. Sin Red de Display y sin socios de búsqueda.
- Ubicaciones: Chile y Perú, opción **"Presencia: personas que están o suelen estar en las ubicaciones"** (no "interés").
- Idiomas: español e inglés. Muchos ejecutivos usan el navegador en inglés.
- Programación: lunes a viernes, 08:00 a 20:00 hora de Chile. Perú está 2 horas atrás mientras Chile tiene horario de verano.
- Estrategia de oferta inicial: **Maximizar clics con límite de CPC máximo** = [placeholder: definir con el Planificador de palabras clave]. Pasar a "Maximizar conversiones" cuando haya ~15 conversiones en 30 días. Con este presupuesto, eso puede tomar varios meses.
- Etiquetado automático (gclid): **activado**. Es indispensable para medir.
- Sufijo de URL final (nivel campaña):
  - Dynamics: `utm_source=google&utm_medium=cpc&utm_campaign=dynamics-365&utm_term={keyword}&utm_content={adgroupid}`
  - IA: `utm_source=google&utm_medium=cpc&utm_campaign=ia-agentes&utm_term={keyword}&utm_content={adgroupid}`

  El formulario ya envía las UTM al Lead en Dynamics 365, así que Comercial verá en el CRM la campaña y la palabra clave de cada lead.

### 3. Importar con Google Ads Editor
Usar **`google-ads-editor.csv`**: un solo archivo con campañas, configuración, ubicaciones, grupos, palabras clave, negativas y anuncios (Cuenta > Importar > Desde archivo). Revisar la vista previa, "Conservar todo" y "Publicar". Los CSV sueltos (`palabras-clave.csv`, `anuncios.csv`, `negativas.csv`) quedan como referencia.

**Lecciones del 2026-10-13:**
- El asistente web de "Campaña nueva" falló 4 veces: al pedir "Confirme su identidad" en el paso de presupuesto deja de guardar y el borrador pierde nombre y tipo. Usar siempre Editor.
- Google rechaza "ISO 9001 e ISO/IEC 27001" (y "ISO 9001 y 27001") como "número de teléfono en el texto del anuncio". En los avisos se escribe "Certificados ISO por SGS"; los números van en la landing.
- La web de Google Ads no guarda recursos (vínculos, destacados) mientras la extensión de Claude depura Chrome: muestra "Turn off ad blockers" y descarta el guardado en silencio. Cargarlos con Editor.
- Vínculos en Editor: una fila por campaña con texto, líneas y URL (`google-ads-editor-recursos.csv`); una fila extra de asociación sin URL crea un vínculo vacío con error. Destacados: `google-ads-editor-destacados.csv` entra a la biblioteca (Editor lo reporta como "omitido" igual) y luego se asocian a la cuenta con "Agregar texto destacado".
- Publicado el 2026-10-13: 8 vínculos (4 por campaña), 6 destacados a nivel de cuenta, y se quitaron 2 vínculos antiguos rechazados de la cuenta ("Dynamics 365 · CRM" y "Noticias · Gold Certified Partner", sitio viejo). Quedan otros vínculos antiguos con URL http:// aprobados, por revisar.

### 4. Recursos (assets) a nivel de cuenta
- Enlaces de sitio: están en `ENLACES` de `generar.py` (Sales y Customer Service, Contact Center, Business Central/Finance, Copilot y agentes, Cofinanciamiento, Trust Center).
- Textos destacados: 6 designaciones Microsoft · ISO 9001 e ISO/IEC 27001 · Oficinas Santiago y Lima · Con Microsoft desde 2014 · Autodiagnóstico gratuito · Success by Design.
- Llamada: +56 2 2409 6112 (Chile). Perú: [placeholder si hay número local].
- Logo y nombre de la empresa: W-IT.

## Rutina de las primeras 6 semanas
- **2 veces por semana**: Estadísticas > Términos de búsqueda. Lo irrelevante se agrega como negativa en `generar.py`.
- **Semanal**: CPC real vs. límite, cuota de impresiones perdida por presupuesto, rendimiento por país (Informes > Ubicaciones).
- **Mensual**: leads en Dynamics 365 con `utm_source=google`. Hay que distinguir cuántos se volvieron oportunidad, no solo cuántos formularios llegaron.

## Riesgos y decisiones abiertas
- **Volumen bajo**: las búsquedas B2B de Dynamics en Chile y Perú son pocas y caras. Verifica volúmenes y CPC en el Planificador de palabras clave antes de fijar el límite; acá no se inventaron cifras.
- **Marcas registradas**: los anuncios usan "Microsoft", "Dynamics 365" y "Copilot". Google lo permite salvo reclamo del titular. Si algún anuncio queda "Aprobado (limitado)", hay que revisarlo.
- **"precio"** no está como negativa: puede traer compradores o solo personas que comparan licencias. Hay que decidirlo con los términos de búsqueda reales.
- **Cuenta en Gmail** (witchile.ads@gmail.com): conviene migrarla a una cuenta corporativa y sumar un segundo administrador.
- **Nombre del producto**: el sitio usa "Azure AI Foundry", pero Microsoft hoy lo llama "Microsoft Foundry". Las palabras clave cubren ambos nombres.

## Control semana 2 (2026-10-28)

- **IA** (13–27 oct): $34.913, 99 clics, CTR 8,6 %, CPC $353, 1 conversión. Los términos de búsqueda estaban dominados por compradores de licencias y precios ("copilot 365", "copilot pro precio", "cuanto cuesta copilot studio", "copilot planes de pago", "https copilot studio").
- **Dynamics** (13–27 oct): $65.361, 42 clics, CTR 4,5 %, CPC $1.556, 0 conversiones. Términos pertinentes (business central, crm dynamics, contact center).
- **Acción A aplicada:** negativas nuevas en IA `pro`, `precio`, `cuánto cuesta`, `cuanto cuesta`, `planes de pago`, `https`, `com`; se quitó la palabra clave `licencias microsoft 365 copilot`. Archivo para importar solo las negativas nuevas: `google-ads-editor-negativas-ia-s2.csv`. Quitar la palabra clave se hace a mano en Editor (la importación no borra).

## Campaña W-IT Bridge (2026-10-30)

- Producto nuevo: conector de WhatsApp e Instagram a Dynamics 365 (`/productos/w-it-bridge/`). Segmento muy acotado: solo búsquedas precisas, concordancia de frase.
- Campaña "W-IT | Búsqueda | W-IT Bridge · WhatsApp e Instagram | CL-PE": $3.200/día, CPC máx. $1.800, fin 2026-12-01 (máx. ≈ $97.000 en el mes). Presupuesto adicional a los $200.000 de Dynamics + IA.
- 3 grupos: WhatsApp en Dynamics 365 · Instagram y mensajería en el CRM · Alternativa a proveedores de mensajería (puja por búsquedas con "twilio"; el anuncio no lo nombra ni compara precios).
- Nombre provisorio: los anuncios venden "conector de WhatsApp e Instagram para Dynamics 365"; "W-IT Bridge" va como título secundario por si Comercial cambia la marca.
- Página: título simplificado y formulario de contacto en la misma página (`#contacto`, interés "Contact center" marcado, `data-en-pagina`), como en las landings.
- Archivos para Editor: `google-ads-editor-bridge.csv` (campaña, ubicaciones, negativas, grupos, palabras clave, anuncios), `google-ads-editor-recursos-bridge.csv` (vínculos) y `google-ads-editor-destacados-bridge.csv` (destacados de campaña). La columna `End Date` fija el término; si Editor la rechaza, poner la fecha a mano en la configuración de la campaña.
- Expectativa realista: 50–70 clics y 0–2 conversaciones calificadas en el mes. Es una prueba de demanda, no una campaña de volumen.

## Control semana 3 (2026-11-04, período 28 oct – 3 nov)

- **IA**: $14.578, 551 impr., 39 clics, CTR 7,1 %, CPC $374, 2 conv. (1 solo lead en el CRM: Fidelya, cotización de licencias Copilot + implementación). Términos de licencias/precios/planes: 6 clics, $2.298 (≈19 % de lo visible en el informe de términos; antes, la palabra clave de licencias sola era ≈50 % del gasto). Siguen entrando plurales y variantes que las negativas de frase no cubren ("precios", "planes", "valor", "costo", "licencia").
- **Dynamics**: $29.783, 383 impr., 21 clics, CTR 5,5 %, CPC $1.418, 0 conv., 0 leads.
- **Bridge**: 0 impresiones. Campaña "Apta (en aprendizaje)", 3 anuncios Aptos; de 25 palabras clave, 2 con "volumen bajo" (se revisaron 10 filas, el resto no se verificó una por una). Horario lun–vie 08–20: desde el 31-oct solo sirvió 2 días hábiles.
- **CRM**: 4 leads desde el 28-oct, todos con origen Web (8) y asignados. W-IT: 1 (IA). WITEDUCA: 3. Orgánico/directo W-IT: 0.
- Proyección Dynamics + IA: ≈ $190.000/mes (95 % del tope).
- Cloudflare no se leyó: pide iniciar sesión con Google.
- **Preparado tras el control (2026-11-04), pendiente de aprobación e importación:** `google-ads-editor-anuncios-dynamics-v2.csv` (un anuncio adicional por grupo de Dynamics con títulos cortos que repiten la búsqueda; el original sigue activo, Google rota) y `google-ads-editor-negativas-ia-s3.csv` (13 negativas de plurales y variantes de precio; "licencias" se mantiene porque trajo el lead de Fidelya). Decisión Bridge el viernes 7-nov; decisión de presupuesto Dynamics/IA el 10-nov.
- **Bridge s2 (2026-11-04):** nadie busca el nombre del producto; buscan conectar Dynamics con WhatsApp o Instagram, o Twilio. `google-ads-editor-bridge-s2.csv` agrega 14 palabras clave planteadas como problema ("conectar whatsapp con dynamics 365", "twilio whatsapp dynamics"…) y un anuncio v2 por grupo cuyo título abre con la pregunta ("¿WhatsApp en Dynamics 365?", "¿Pagas un BSP por WhatsApp?"); el producto queda al final. Los anuncios originales siguen activos.
- **Bridge, plan B preparado (2026-11-04), importar solo si el viernes 7-nov sigue en 0 impresiones:** `google-ads-editor-bridge-amplias.csv` (4 palabras centrales en concordancia amplia: whatsapp dynamics 365, whatsapp microsoft dynamics, instagram dynamics 365, twilio whatsapp dynamics; las negativas frenan lo ajeno) y `google-ads-editor-bridge-horario-7dias.csv` (fila de campaña con horario lunes a domingo 08–20). Tras importar la amplia, revisar términos de búsqueda a los 3 días y agregar negativas.

## Control 2026-11-09 (período 2–8 nov)

- Gasto 7 días: WITEDUCA $36.267 (27 clics, 2 conv., 3 leads), Dynamics $26.703 (18 clics, 0 conv.), IA $16.926 (40 clics, 2 conv. Ads, 0 leads W-IT por Ads), Bridge $0 (0 impresiones tras 6 días hábiles).
- Cloudflare 7 días: 299 visitas (w-it.cl 223, witeduca.cl 75); referentes directo 147, Google 99, Teams 17. "Trabaja con nosotros": 5 visitas. La API del sitio (contacto + postulación) registró 8 envíos en 2 semanas: los currículums que recibe Claudio NO llegan por el sitio ni por Ads (trabajo/empleo son negativas desde el inicio).
- Conversiones: "W-IT - Formulario de contacto" cuenta "Una" (correcto). "W-IT - Autodiagnóstico completado" está como acción **Principal** y suma a las conversiones de campaña: por eso IA muestra 2 conv. con 1 lead. Pendiente: pasarla a Secundaria (observación) en Objetivos → Conversiones. Existe además "Formulario de contacto - Enviar" (alojada en Google, sin datos), creada automáticamente; revisar si conviene quitarla.
- Decisiones: importar plan B de Bridge (amplias + 7 días); Dynamics baja a $2.000/día con 2 negativas (`google-ads-editor-dynamics-s3.csv`); IA se mantiene; WITEDUCA recibe 17 negativas de su revisión de 314 términos en 30 días (`google-ads-editor-negativas-witeduca.csv`): los términos con clic son casi todos pertinentes (cursos Claude/IA/Copilot); el desperdicio visible fue menor al 2 %, las negativas apuntan a competidores (hazloconia, centeia), licencias/precios, programadores y frases genéricas en inglés. Power Automate/Power BI/SENCE se mantienen porque WITEDUCA los ofrece.
- Si Dynamics sigue sin leads al 2026-11-24: pausar y trabajar la landing antes de volver a invertir.
- **WITEDUCA en Perú (prueba desde 2026-11-09):** `google-ads-editor-witeduca-peru.csv` agrega la ubicación Perú (ID 2604) a la campaña WITEDUCA. La campaña tenía "peru" como negativa: se quita a mano en Editor. Medir a 2 semanas: impresiones, clics y leads con país Perú; el horario (lun–vie 10–17 hora de Chile) equivale a 8–15 en Perú.
- **Bridge fase 1 internacional (2026-11-09):** `google-ads-editor-bridge-paises.csv` agrega 18 países (Hispanoamérica, España, EE. UU. y Puerto Rico) a la campaña Bridge, con los mismos anuncios en español. El horario 08–20 es hora de Chile (México 05–17, España 12–24): si la fase 1 muestra búsquedas, ampliar horario o separar por región. Fase 2 (pendiente de datos): campaña en inglés "Twilio alternative for Dynamics 365" con landing en inglés y presupuesto propio (~USD 15–20/día); con $1.800 de CPC máximo no se ganan subastas en inglés.

## Control 2026-11-10 (revisión completa en `GoogleAds_Cloudflare_revision_2026-11-10.md`)

- **Bridge: los 18 países no se importaron.** El historial de cambios del 9-nov solo registra en Bridge las 4 amplias y el horario de 7 días; Ubicaciones sigue en Chile y Perú. Volver a importar `google-ads-editor-bridge-paises.csv` y verificar.
- IA (30 días): los términos pelados "copilot 365", "copilot studio", "ia copilot", "copilot", "copilot ai", "copilot 365 ai" suman 124 clics y $44.686 (61 % del gasto) con 0 conversiones. Propuesta: negativas de concordancia exacta para esos términos (CSV s4 pendiente de generar).
- Conversiones sin corregir desde el 21-oct (Autodiagnóstico sigue Principal); vínculo "Casos de éxito" sigue rechazado; "Sales y Customer Service" duplicado en Dynamics.
- Cloudflare 7 días: 328 visitas (w-it.cl 223), ~un tercio bot (EE. UU./China/Singapur, navegador Unknown); 40 entradas por www; copia pública del sitio en GitHub Pages (`claudinhostgo-byte.github.io/WIT/sitio/`) recibiendo visitas.
- **Preparado tras el control (2026-11-11), pendiente de aprobación e importación:**
  - `google-ads-editor-negativas-ia-s4-exactas.csv`: 13 negativas de **concordancia exacta** en IA (`[copilot]`, `[copilot 365]`, `[copilot studio]`, `[ia copilot]`, `[copilot ai]`, `[copilot 365 ai]`, `[microsoft copilot]`, `[m365 copilot]`, `[copilot microsoft]`, `[copilot studio microsoft]`, `[microsoft copilot studio]`, `[copilot pro]`, `[copilot ia]`). Bloquean solo la consulta pelada; las largas con intención siguen pasando. "copilot office 365" queda fuera porque trajo el primer lead. La palabra clave de frase "microsoft copilot studio" sigue activa: seguirá captando "implementar copilot studio" y similares, pero no la búsqueda idéntica. Esperar que los clics de IA bajen a la mitad; es lo buscado.
  - `google-ads-editor-bridge-paises.csv`: se revisó y es idéntico en estructura al CSV de WITEDUCA-Perú que sí entró el 9-nov. No hay nada que corregir en el archivo: hay que volver a importarlo en Editor, confirmar que la vista previa muestre 18 ubicaciones nuevas en Bridge, publicar, y verificar en la web (Bridge → Ubicaciones).

## WITEDUCA s2 (2026-11-11): filtrar a quien busca formación a medida

Las búsquedas reales son "curso de…", "cursos de…", "clases de…"; nadie escribe "personalizado" y las palabras clave más calificadas ya quedaron sin volumen en septiembre. El filtro se reparte en capas. Archivo: `google-ads-editor-witeduca-s2.csv` (pendiente de aprobación e importación).

- **32 negativas de frase de autoaprendizaje**: tutorial, gratis, youtube, video, pdf, descargar, desde cero, principiantes, qué es, cómo usar/crear/hacer/automatizar, udemy, coursera, platzi, domestika, edx, linkedin learning, google, clases particulares, ejemplos.
- **23 palabras clave de frase**: curso/taller/clases/capacitación + IA, Copilot, Claude o Power Platform, la mayoría con "para empresas", "in company", "a medida" o "para equipos".
- **15 amplias a Pausa**: el 9-nov casi todas las palabras activas de la campaña eran de concordancia amplia; por ahí entran "como crear un agente en copilot" o "best ai platforms for business". Se mantienen las dos amplias que convirtieron en 30 días: "capacitacion inteligencia artificial" (6 conv.) y "capacitación ia empresas" (1). En la vista previa de Editor confirmar que las 15 figuren como **modificadas**, no como nuevas; si aparecen como nuevas, el texto no calzó (tildes) y hay que pausarlas a mano.
- **Un anuncio adicional que califica**: títulos "Grupos Cerrados por Empresa", "Programa a Medida por Rol", "Curso Cerrado para tu Empresa", "Para Equipos de tu Empresa". Todo lo que afirma está en witeduca.cl/oferta/. El anuncio original sigue activo; para que el filtro opere de verdad hay que pausarlo cuando el nuevo esté aprobado.
- **Formulario**: ya pide empresa y tamaño. Falta usar ese dato: mientras la puja sea Maximizar conversiones y cuente cualquier formulario, aprende también de personas.
- **Supuesto a confirmar**: la campaña apunta solo a formación in-company. La página ofrece además cursos abiertos de una jornada para personas y equipos chicos, y la línea Claude; "clases particulares" y "curso claude" (pausada) quedan fuera. Si se quiere vender el formato abierto por Ads, conviene una campaña aparte con su propio anuncio.
- Efecto esperado: menos impresiones y clics, CPC similar. Medir a 2 semanas leads con empresa y tamaño informados, no formularios totales.

## Cambios en la cuenta (2026-11-11 y 2026-11-12)

- **Verificación del anunciante completada (2026-11-11):** cuestionario de organización enviado (nombre legal W-it; no administra cuentas de terceros; productos propios; industrias Informática y electrónica, Servicios para empresas y Capacitación empresarial) y documentos verificados. Ya no hay fecha límite.
- **Vínculo "Casos de éxito" eliminado (2026-11-12):** estaba a nivel de cuenta, rechazado por destino no operativo (sitio antiguo). Era la causa probable de "Apto (limitado)" en Dynamics e IA; revisar en unos días si el aviso "Es posible que se limiten algunos anuncios" desaparece. "Contáctanos" (nivel cuenta, sitio antiguo) sigue activo y aprobado.
- **CSV pendientes aplicados por la web de Google Ads (2026-11-12)**, no por Editor; cada cambio verificado recargando la página:
  - IA: 13 negativas de concordancia exacta (`google-ads-editor-negativas-ia-s4-exactas.csv`).
  - Bridge: 18 países agregados, ahora 20 ubicaciones. Al incluir España, Google pide declarar anuncios políticos de la UE en la campaña; se respondió "No". Por eso el primer intento no se guardó.
  - WITEDUCA: 32 negativas de frase (29 nuevas, 3 ya existían; la campaña pasó de 82 a 111), 23 palabras clave de frase (en revisión), amplias pausadas salvo "capacitacion inteligencia artificial" y "capacitación ia empresas" (se pausaron 28: las 15 previstas más 13 que ya estaban detenidas o sin volumen), y anuncio responsivo nuevo, apto sin problemas de políticas.
  - WITEDUCA (2026-11-12, tras lo anterior): anuncio original detenido (solo rota el nuevo) y redes reducidas a Búsqueda de Google, sin socios de búsqueda ni Display. Ambos verificados al recargar.

## Cambio en la cuenta (2026-11-16, Especialista en Ads)

- **«W-IT - Autodiagnóstico completado» pasó de Principal a Secundaria** (objetivo «Vistas de página»; ya no se incluye en los objetivos a nivel de cuenta). Motivo: terminar un autodiagnóstico no crea un lead (solo guarda respuestas en el navegador y dispara la conversión); en 30 días hubo 13 leads web y 0 con autodiagnóstico. Aprobado por Don Claudio por chat, aplicado por la web y verificado al recargar «Todas las conversiones». Se evalúa el 2026-11-30.
- Visto al leer la cuenta: «WITEDUCA - Formulario de contacto» figura en «Configuración incorrecta» (5 conv. en el período). Pendiente revisar la etiqueta de witeduca.cl.

## Control 2026-11-21 (período 13–18 nov, tras los cambios del 12-nov)

| Campaña | Costo | Impr. | Clics | Conv. Ads | Leads CRM con UTM Google |
|---|---|---|---|---|---|
| WITEDUCA | $30.735 | 178 | 18 | 1 | sin UTM (2 leads WITEDUCA en el período) |
| Bridge | $34.612 | 1.048 | 47 | 0 | 0 |
| IA y agentes | $13.808 | 757 | 36 | 1 | 1, sin intención de compra |
| Dynamics 365 | $11.020 | 371 | 9 | 0 | 0 |
| **Total** | **$90.175** | 2.354 | 110 | 2 | |

- **Bridge**: las 4 amplias se activan con búsquedas genéricas ("dynamics" 14 clics $8.713, "dynamics 365", "business central", "microsoft sharepoint", "power automate", "whatsapp business"). Ningún término visible es sobre conectar WhatsApp o Instagram con Dynamics. Es el 38 % del gasto y compite con la campaña Dynamics.
- **IA**: las negativas exactas funcionan, pero entran variantes de consumo ("microsoft copilot ai", "copilot 360 microsoft", "para que sirve copilot", "copilot microsoft en español").
- **WITEDUCA**: impresiones de ~98/día a ~30/día y clics de ~6 a 3 por día, como se esperaba. Muy pronto para medir calidad.
- **Currículums**: no vienen de Ads ni del formulario. Son correos escritos directo a postulaciones@w-it.cl (al menos 9 desde el 12-nov), dirección publicada en "Trabaja con nosotros". El formulario del sitio solo envió 1 postulación en noviembre.
- **CRM**: 5 leads desde el 11-nov. Granotec pasó a Calificado ("Implementación Dynamics Sales"). Los dos de IA por Ads no tienen intención de compra.
- Cloudflare no se revisó: la sesión expiró.

### Bridge redefinida (2026-11-21, decisión de Don Claudio)

Bridge sigue activa y sin fecha de término. Criterio: solo búsquedas que junten WhatsApp (o Instagram) con Dynamics, o que busquen reemplazar Twilio.
- Detenidas 17 palabras: las 4 amplias (la culpable era "instagram dynamics 365" amplia: 45 clics y $33.086 en 13–18 nov por búsquedas como "dynamics" o "business central") y 13 frases sin Dynamics ni intención de reemplazo ("bsp whatsapp chile", "twilio whatsapp chile", "instagram crm empresas", etc.).
- Agregadas 19 frases: 10 en "WhatsApp en Dynamics 365" ("whatsapp dynamics", "dynamics whatsapp", "dynamics 365 whatsapp", "whatsapp en/con/para/y dynamics", "dynamics con/y whatsapp", "whatsapp dynamics crm") y 9 en "Alternativa a proveedores de mensajería" ("alternativa(s) a twilio", "alternativa twilio", "reemplazo/reemplazar twilio", "twilio alternative(s)", "alternative to twilio", "twilio dynamics").
- Fecha de término quitada (antes 2026-12-01). Presupuesto sin cambio ($3.200/día); con solo frases el gasto real será bajo y depende de que exista la búsqueda.
- Verificado al recargar: 62 palabras (17 detenidas, 19 en revisión).
- La campaña Dynamics ya tiene "dynamics crm", "crm dynamics 365", "partner microsoft dynamics", "implementación dynamics 365" y similares. No tiene palabras de Power Platform.

## Dynamics s4: grupo Power Platform (publicado y cargado 2026-11-22)

Decisión de Don Claudio (2026-11-21): Dynamics 365 y Power Platform son el negocio central; la campaña Dynamics **no se pausa el 24-nov**.
- **Landing nueva** `/implementacion/power-platform/` (generada con `build/build.py`, lista `LANDINGS`): noindex, fuera del sitemap, formulario en la misma página con "Automatización y apps" marcado. Contenido tomado de `/soluciones/automatizacion-y-apps/`. Como no hay autodiagnóstico de Power Platform, `landing_page` ahora omite esa sección cuando la lista de herramientas está vacía. Las otras dos landings no cambiaron. **Falta publicar el sitio**: si se importa el grupo antes, Google rechaza el anuncio por destino no operativo.
- **`google-ads-editor-dynamics-power-platform.csv`** (campaña Dynamics): grupo "Power Platform · Apps y automatización", 13 frases y 3 exactas (implementación, partner y consultora de Power Platform, Power Apps y Power Automate; [power platform chile], [power platform peru], [power apps chile]), 15 negativas del grupo (licencias, precios, plantillas, exámenes PL-200/300/400/600, developer plan, community, desktop) y un anuncio propio de 15 títulos y 4 descripciones. Cursos, empleo y certificaciones ya están negados a nivel de campaña.
- **Revisión de la landing de Dynamics 365**: formulario visible en la primera pantalla del móvil; solo nombre, email y consentimiento son obligatorios. Defecto: el botón flotante del agente tapa parte de los campos en móvil. No se encontró otra causa técnica de los 0 leads; con ~80 clics en 30 días, el volumen es el límite principal.
- Presupuesto Dynamics sin cambio ($2.000/día). Si se importa el grupo, conviene subirlo (p. ej. a $3.200/día) para que Power Platform no le quite impresiones al resto.
- **Aplicado el 2026-11-22**: sitio publicado (commit 7eae1fb, `infra/publicar.ps1`); https://w-it.cl/implementacion/power-platform/ responde 200. Grupo "Power Platform · Apps y automatización" creado por la web de Google Ads en la campaña Dynamics (adGroupId 205204085951): 16 palabras clave, 15 negativas a nivel de grupo y el anuncio (apto). Verificado al recargar. Presupuesto de la campaña sin cambio ($2.000/día).
- Lección: en el formulario de grupo nuevo, "Borrar todos los recursos precompletados" también vacía las palabras clave ya escritas; cargarlas después de limpiar el anuncio.
- **Presupuesto y horario de Dynamics (2026-11-22, decisión de Don Claudio)**: $5.000/día (antes $2.000) y programación lunes a viernes de 10:00 a 17:00 hora de Chile (antes 08:00–20:00). En Perú equivale a 08:00–15:00 mientras Chile tenga horario de verano. Aplicado en la web y verificado al recargar. Máximo mensual ≈ $152.000 (×30,4).
