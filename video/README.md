# Video de presentación W-IT

Video de 49 s (1920×1080, 30 fps, sin audio) hecho con [Remotion](https://www.remotion.dev/) y los principios del skill `motion-design` (LottieFiles). El contenido sale del home del sitio (`sitio/index.html`).

## Escenas

1. Logo · Microsoft Solutions Partner · Chile y Perú
2. Hero: "IA en producción sobre tus sistemas reales."
3. Credenciales: 6 de 6 designaciones + sello Solutions Partner for Microsoft Cloud
4. Soluciones Microsoft (8 tarjetas con íconos oficiales; Purview/Entra sin ícono por la guía de Microsoft)
5. Cómo trabajamos: cuatro marcos ágiles
6. Trust Center: ISO 9001, ISO/IEC 27001 (SGS), Azure Chile Central, IA responsable
7. Clientes (logos en gris, como en el sitio)
8. Cierre: "Conversemos sobre tu proyecto." · w-it.cl

## Uso

Este equipo es Windows ARM64 y Remotion solo trae motor de render x64: se usa Node x64 portable (nodejs.org) en emulación.

```bash
npm run studio   # editor con vista previa
npm run render   # genera out/wit-presentacion.mp4
```

Los textos y la línea de tiempo están en `src/WitPresentacion.tsx` (`ESCENAS`).

## Anuncio Microsoft Cloud (RRSS)

`src/MicrosoftCloud.tsx`: 16,8 s, sin audio, en dos formatos (`MicrosoftCloudVertical` 1080×1920 para Reels/TikTok/Shorts y `MicrosoftCloudFeed` 1080×1350 para LinkedIn/feed). Badges de las 6 designaciones en `public/designaciones/` (extraídos de la presentación comercial; Modern Work recortado de la lámina compuesta).

```bash
npm run render:mscloud
```
