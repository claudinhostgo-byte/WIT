# Sitio web W-IT

Nuevo sitio de W-IT, Microsoft Solutions Partner en Chile y Perú. Sitio estático (HTML, CSS y JavaScript sin dependencias) generado con un script en Python.

> **Versión 1, en revisión.** Hay contenido marcado como `[placeholder]`, `[validar]` o `[estimación]` que debe confirmarse antes de publicar.

## Estructura

```
build/
  build.py      # plantillas (header, footer, páginas) y generador
  content.py    # contenido: soluciones, industrias, clientes, casos, etc.
sitio/          # sitio generado, listo para servir
  styles.css    # estilos (se edita directamente)
  main.js       # comportamiento (se edita directamente)
  assets/       # imágenes, logos, íconos y credenciales
```

Los archivos `index.html` de `sitio/` se generan: no se editan a mano.

## Uso

Regenerar el sitio después de cambiar `build/content.py` o `build/build.py`:

```bash
python build/build.py
```

Requiere Python 3.12+ y Pillow (`pip install pillow`). El script avisa si alguna clase usada en el HTML no tiene estilos en `styles.css`.

Vista local:

```bash
python -m http.server 8080 --directory sitio
```

Luego abrir http://localhost:8080

## Reglas de contenido y marca

- **Badges de Microsoft** (`assets/credenciales`): no recortar, recolorear ni modificar.
- **Íconos de productos Microsoft** (`assets/ms`): oficiales de learn.microsoft.com. Usarlos sin alterar y siempre con el nombre del producto al lado. No se usan íconos de Entra, Purview ni Defender (su guía prohíbe el uso en marketing).
- **Logos de clientes y casos de éxito**: validados por W-IT. No se publican montos contractuales sin autorización del cliente.
- **Premios Partner of the Year 2019 y 2020**: se muestran como trayectoria, no como credencial vigente.
