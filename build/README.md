# Sitio W-IT · generador

- `content.py`: textos, soluciones, industrias, casos, clientes (fuente: `Brief_Claude_Design_w-it_v01.md`).
- `build.py`: plantillas (header con mega-menús, footer, páginas) → escribe los `index.html` en `../sitio/`.
- `../sitio/styles.css`, `../sitio/main.js` y `../sitio/assets/` se editan directamente.

```bash
python build/build.py
```

Vista local: `python -m http.server 8080 --directory sitio` → http://localhost:8080

## Reglas de assets
- Badges Microsoft (`assets/credenciales`): no recortar, recolorear ni modificar.
- Íconos de productos Microsoft (`assets/ms`): descargados de learn.microsoft.com (Dynamics 365, Power Platform, Azure).
  Sus términos permiten uso en diagramas, capacitación o documentación; usarlos siempre sin alterar y con el nombre del producto al lado.
  **Validar con Microsoft Partner Marketing / Comercial antes de publicar.** No se usan íconos de Entra/Purview/Defender
  (la guía de Entra prohíbe su uso en marketing) ni de Power BI (paquete de Fabric no descargado).
- Logos de clientes (`assets/clientes`): cada uno requiere autorización vigente.
