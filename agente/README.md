# Agente W-IT (clip del sitio) · Microsoft Copilot Studio

El clip flotante del sitio conversa con un agente de **Microsoft Copilot Studio** creado en el ambiente productivo de W-IT.
Primera etapa: el agente solo ayuda a encontrar información del sitio y responde con el enlace a la página
(por ejemplo, "¿Dónde dejo mi CV?" → [Trabaja con nosotros](/nosotros/trabaja-con-nosotros/)).

```
Navegador (main.js) ──► token endpoint del agente (Copilot Studio, sin autenticación)
                    └─► Direct Line 3.0 ──► Agente W-IT ──► conocimiento: conocimiento-sitio-w-it.md
```

## Archivos de esta carpeta

| Archivo | Qué es | Se genera |
|---|---|---|
| `instrucciones.txt` | Instrucciones del agente, con el mapa del sitio | Sí, en cada `python build/build.py` |
| `conocimiento-sitio-w-it.md` | Mapa, atajos de navegación y texto de cada página | Sí, en cada build |
| `README.md` | Esta guía | No |

Los enlaces son rutas relativas (`/contacto/`): funcionan igual en w-it.cl, en el dominio de Azure Static Web Apps y en la vista local.
Los atajos ("dejar el CV", "cotizar", etc.) se editan en `build/agente.py` (`ATAJOS`).

## Configuración en Copilot Studio (una vez)

1. **Crear el agente** en copilotstudio.microsoft.com, en el ambiente productivo de W-IT.
   Nombre: `Agente W-IT`. Idioma principal: español.
2. **Instrucciones**: pegar el contenido de `instrucciones.txt`.
3. **Conocimiento** → Agregar → Archivos → subir `conocimiento-sitio-w-it.md`.
   Si el portal no acepta `.md`, subirlo renombrado a `.txt`.
   No agregar el sitio web público como fuente mientras el sitio nuevo no esté publicado: esa fuente busca con Bing y hoy encontraría el sitio antiguo.
4. **Configuración → IA generativa**:
   - Desactivar el uso de conocimiento general del modelo y la búsqueda web, para que solo responda con el contenido del sitio.
   - Moderación de contenido: alta.
5. **Seguridad**:
   - Autenticación: **Sin autenticación** (sitio público).
   - Seguridad del canal web: **no** exigir acceso seguro. Si se exige, el token endpoint pide un secreto y el sitio no puede conectarse.
6. **Publicar** el agente.
7. **Canales → Aplicación móvil** (o la opción equivalente en tu versión del portal): copiar el **Token endpoint**.
8. Pegar esa URL en `build/build.py` → `AGENTE_TOKEN_URL`, ejecutar `python build/build.py` y hacer push a `main`.

El token endpoint es público por diseño: no es un secreto.

## Probar antes del lanzamiento

En local, sin tocar `build.py`:

```bash
AGENTE_TOKEN_URL="<token endpoint>" python build/build.py
```

```bash
python -m http.server 8080 --directory sitio
```

Después de probar, vuelve a ejecutar `python build/build.py` sin la variable para no dejar la URL en los HTML (salvo que ya esté definida en `build.py`).
También se puede probar en el panel de prueba de Copilot Studio y en el dominio de Azure Static Web Apps, antes de apuntar w-it.cl.

## Mantención

- Cada vez que cambia el contenido del sitio: volver a subir `conocimiento-sitio-w-it.md` (reemplazar el archivo) y, si cambió el mapa, volver a pegar `instrucciones.txt`. Después, publicar el agente.
- Revisar periódicamente las conversaciones en Analítica para detectar preguntas sin respuesta y agregarlas a `ATAJOS`.

## Pendientes y riesgos

- **Costo**: lo asume W-IT. Cada respuesta del agente consume mensajes de Copilot Studio y, como el token endpoint es público, cualquiera puede generar consumo: revisar el consumo en las primeras semanas. Si se ven abusos, la etapa siguiente es emitir el token desde `/api` con Turnstile y límite por IP.
- **Retención de conversaciones**: Copilot Studio guarda las transcripciones en Dataverse. El aviso de privacidad dice 30 días `[validar]`: confirmar la retención configurada en el ambiente con el **Encargado de Plataforma y Seguridad**.
- **Aviso de privacidad**: se agregó Microsoft Copilot Studio como proveedor y una sección sobre lo que se escribe en el asistente. Validar el texto antes de publicar.
