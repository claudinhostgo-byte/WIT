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
