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
