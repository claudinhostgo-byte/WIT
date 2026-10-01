"""Genera las páginas HTML del sitio W-IT en ../sitio/.

Uso:  python build/build.py
styles.css, main.js y assets/ se editan directamente en sitio/; este script solo escribe los .html.
"""
import json
import os
from html import escape
from PIL import Image
from content import (MS, PLATAFORMAS, SOLUCIONES, INDUSTRIAS, CLIENTES, ALIANZAS, CASOS, METODOS, METODO, HERRAMIENTAS, FAQ_HOME,
                     COFIN_PROGRAMAS, COFIN_PROCESO, COFIN_COMPARA, COFIN_POC, COFIN_MVP, COFIN_FAQ, DIAG_IA, DIAG_ERP)

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sitio')
SOL = {s['slug']: s for s in SOLUCIONES}
IND = {i['slug']: i for i in INDUSTRIAS}
CASO = {c['slug']: c for c in CASOS}
# Programa Microsoft Copilot Jumpstart (W-IT: Ready Tier)
JUMPSTART_PAGE = 'microsoft-copilot-jumpstart/'
COFIN_PAGE = 'cofinanciamiento-microsoft/'
# Herramientas que aparecen en el menú «Autodiagnósticos»
DIAGNOSTICOS = ('autodiagnostico-ia', 'business-central-o-finance')
COPILOT_URL = 'https://www.microsoft.com/es-cl/microsoft-365/copilot'
IND_NOMBRE = {**{i['slug']: i['nombre'] for i in INDUSTRIAS}, 'otros': 'Telecomunicaciones y otros'}

CHEV = '<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<span aria-hidden="true">→</span>'
SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>'

_dims = {}

# Íconos de línea propios por industria (24x24, trazo 1.8, estilo Fluent/Lucide)
_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
IND_ICON = {
    'servicios-financieros': _SVG.format('<ellipse cx="9" cy="6" rx="6" ry="2.5"/><path d="M3 6v4c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5V6"/><path d="M3 10v4c0 1.4 2.7 2.5 6 2.5 1 0 2-.1 2.8-.3"/><path d="M15 21l3-3 2 2 3-4"/>'),
    'salud-y-seguros': _SVG.format('<path d="M20.8 8.6A5 5 0 0 0 12 5.5a5 5 0 0 0-8.8 3.1c0 5.3 8.8 11.4 8.8 11.4s3.6-2.5 6.1-5.6"/><path d="M3.5 12h4l1.5-2.5 2.5 5 2-3.5h6.5"/>'),
    'educacion': _SVG.format('<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5"/><path d="M22 9v6"/>'),
    'mineria': _SVG.format('<path d="M2 20.5l6.5-10 4 6 2.5-3.5 7 7.5z"/><path d="M14 3.5c2.5.3 4.6 1.6 6 3.5"/><path d="M17.5 3l-5 7"/>'),
    'bienes-de-consumo': _SVG.format('<path d="M5 8h14l-1 12.5H6z"/><path d="M9 10.5V6.5a3 3 0 0 1 6 0v4"/>'),
    'tecnologia-y-comunicaciones': _SVG.format('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/><path d="M9 11.5a4 4 0 0 1 6 0"/><path d="M12 9.5v.01"/>'),
    'sector-publico': _SVG.format('<path d="M3 9.5L12 4l9 5.5"/><path d="M4 9.5h16"/><path d="M6 10v8M10 10v8M14 10v8M18 10v8"/><path d="M3 20.5h18"/>'),
    'transporte-vehiculos-y-maquinaria': _SVG.format('<path d="M2 16.5V7h11v9.5"/><path d="M13 10h4.5l3.5 3.5v3H13"/><circle cx="6.5" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/>'),
    'proyectos-e-ingenieria': _SVG.format('<path d="M4 17a8 8 0 0 1 16 0"/><path d="M10 9.5V6h4v3.5"/><path d="M2.5 17h19v2.5h-19z"/>'),
    'deportes': _SVG.format('<path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4"/><path d="M12 14v3.5M8.5 20.5h7M9.5 20.5l.5-3h4l.5 3"/>'),
    'forestal-y-recursos-naturales': _SVG.format('<path d="M12 3l5 7h-3l4 6H6l4-6H7z"/><path d="M12 16v5"/>'),
}


def logo_file(slug):
    return f'assets/clientes/{slug}.svg' if slug == 'larrainvial' else f'assets/clientes/{slug}.png'


def logo(r, slug, cls='', max_h=None):
    f = logo_file(slug)
    if f not in _dims:
        if f.endswith('.svg'):
            _dims[f] = (94, 37)
        else:
            w0, h0 = Image.open(os.path.join(ROOT, f)).size
            k = 2 if h0 >= 80 else 1
            _dims[f] = (round(w0 / k), round(h0 / k))
    w, h = _dims[f]
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{r}{f}" alt="{escape(CLIENTES[slug])}" width="{w}" height="{h}" loading="lazy">'


def ms_icon(r, slug, size=32, alt=False):
    a = escape(MS[slug]) if alt else ''
    return f'<img class="ms-icon" src="{r}assets/ms/{slug}.svg" alt="{a}" width="{size}" height="{size}">'


def pills(items, dark=False):
    c = 'pill pill-dark' if dark else 'pill'
    return '<div class="pills">' + ''.join(f'<span class="{c}">{escape(p)}</span>' for p in items) + '</div>'


def sol_icons(r, s, size=28):
    if not s['iconos']:
        return f'<span class="icon-slot" aria-hidden="true">{SHIELD}</span>'
    return '<span class="icon-stack">' + ''.join(ms_icon(r, i, size) for i in s['iconos']) + '</span>'


def pais_attr(cl, pe):
    # Sin selector de país: se muestra siempre el texto base (Chile) y la presencia CL/PE se declara en el contenido
    return ''


# ---------------------------------------------------------------- layout

def header(r, active, solid):
    sol_cards = ''.join(f'''
          <a class="mega-card" href="{r}soluciones/{s['slug']}/">
            {sol_icons(r, s, 24)}
            <strong>{escape(s['plataforma'])}</strong>
            <span>{escape(s['nombre'])}</span>
          </a>''' for s in SOLUCIONES)
    ind_items = ''.join(f'''
          <a class="mega-ind" href="{r}industrias/{i['slug']}/">
            <span class="mega-ind-ico">{IND_ICON[i['slug']]}</span>
            <strong>{escape(i['nombre'])}</strong>
          </a>''' for i in INDUSTRIAS)

    def cur(key):
        return ' aria-current="page"' if active == key else ''

    def btn(key, label):
        return (f'<button class="nav-link{" is-active" if active == key else ""}" type="button" '
                f'aria-expanded="false" aria-controls="mega-{key}">{label}{CHEV}</button>')

    return f'''
<header class="site-header{' is-solid is-solid-page' if solid else ''}" id="header">
  <div class="container header-bar">
    <a class="brand" href="{r or './'}" aria-label="W-IT, inicio">
      <img class="brand-logo brand-logo-white" src="{r}assets/marca/logo-white-mark.png" alt="W-IT" width="54" height="40">
      <img class="brand-logo brand-logo-color" src="{r}assets/marca/logo-color-mark.png" alt="" width="54" height="40">
      <span class="brand-sep"></span>
      <span class="brand-tag">Microsoft Solutions Partner</span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Principal">
      <ul class="nav-list">
        <li class="nav-item">{btn('soluciones', 'Soluciones')}
          <div class="mega" id="mega-soluciones">
            <div class="container mega-inner">
              <div class="mega-head"><span class="eyebrow">Soluciones</span><a href="{r}soluciones/">Ver todas las soluciones {ARROW}</a></div>
              <div class="mega-grid">{sol_cards}
              </div>
              <a class="mega-foot" href="{r}herramientas/autodiagnostico-ia/">¿No sabes por dónde empezar? <strong>Autodiagnóstico de madurez en IA {ARROW}</strong></a>
            </div>
          </div>
        </li>
        <li class="nav-item">{btn('industrias', 'Clientes')}
          <div class="mega" id="mega-industrias">
            <div class="container mega-inner">
              <div class="mega-head"><span class="eyebrow">Clientes por industria</span><a href="{r}industrias/">Ver todos los clientes {ARROW}</a></div>
              <div class="mega-grid mega-grid-ind">{ind_items}
              </div>
            </div>
          </div>
        </li>
        <li class="nav-item">{btn('diagnosticos', 'Autodiagnósticos')}
          <div class="mega" id="mega-diagnosticos">
            <div class="container mega-inner mega-split mega-diag">
              <div class="mega-list">
                <span class="eyebrow">Autodiagnósticos gratuitos</span>
                {''.join(f'<a href="{r}herramientas/{h["slug"]}/"><strong>{escape(h["nombre"])}</strong><span>{escape(h["tiempo"])} · {escape(h["que"])}</span></a>' for h in HERRAMIENTAS if h['slug'] in DIAGNOSTICOS)}
              </div>
              <div class="mega-promo">
                <span class="eyebrow">Cofinanciamiento Microsoft</span>
                <strong>Algunos talleres, POC y MVP pueden contar con inversión de Microsoft.</strong>
                <a class="btn btn-primary" href="{r}{COFIN_PAGE}">Ver programas</a>
              </div>
            </div>
          </div>
        </li>
        <li class="nav-item"><a class="nav-link" href="{r}como-trabajamos/"{cur('metodo')}>Cómo trabajamos</a></li>
        <li class="nav-item">{btn('nosotros', 'Nosotros')}
          <div class="mega" id="mega-nosotros">
            <div class="container mega-inner mega-split">
              <div class="mega-list">
                <span class="eyebrow">Empresa</span>
                <a href="{r}nosotros/"><strong>Quiénes somos</strong><span>Historia, misión y valores.</span></a>
                <a href="{r}nosotros/confianza/"><strong>Trust Center</strong><span>Credenciales verificables, ISO y datos en Chile.</span></a>
                <a href="{r}nosotros/equipo/"><strong>Equipo</strong><span>Consultores propios y certificados.</span></a>
                <a href="{r}nosotros/trabaja-con-nosotros/"><strong>Trabaja con nosotros</strong><span>Proyectos enterprise e IA en el día a día.</span></a>
              </div>
              <div class="mega-list">
                <span class="eyebrow">Aprende</span>
                <a href="{r}recursos/"><strong>Recursos</strong><span>Observatorio IA, guías y eventos.</span></a>
                <a href="{r}nosotros/aprende/"><strong>Formación y adopción</strong><span>Nuestra unidad exclusiva para aprender y adoptar IA.</span></a>
                <a href="{r}{COFIN_PAGE}"><strong>Cofinanciamiento Microsoft</strong><span>POC y MVP con programas de inversión de Microsoft.</span></a>
              </div>
              <div class="mega-promo mega-promo-badge">
                <img src="{r}assets/credenciales/WIT-MicrosoftCloud-color.png" alt="Microsoft Solutions Partner for Microsoft Cloud" width="160" height="105">
                <a class="mega-js" href="{r}{JUMPSTART_PAGE}">Microsoft Copilot Jumpstart Partner · Ready Tier {ARROW}</a>
                <a href="{r}nosotros/confianza/">Ver todas las credenciales {ARROW}</a>
              </div>
            </div>
          </div>
        </li>
      </ul>
      <div class="drawer-foot">
        <a class="btn btn-lg btn-primary" href="{r}contacto/">Contáctanos</a>
      </div>
    </nav>
    <div class="header-actions">
      <span class="presence" title="Presencia en Chile y Perú"><img src="{r}assets/img/chile.svg" alt="Chile" width="21" height="14"><img src="{r}assets/img/peru.svg" alt="Perú" width="21" height="14"></span>
      <a class="btn header-cta" href="{r}contacto/">Contáctanos</a>
    </div>
    <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Abrir menú"><span></span><span></span><span></span></button>
  </div>
</header>'''


def footer(r):
    col = lambda t, items: f'<nav class="footer-col" aria-label="{t}"><strong>{t}</strong>' + ''.join(f'<a href="{h}">{escape(l)}</a>' for l, h in items) + '</nav>'
    return f'''
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col footer-brand">
        <img class="footer-logo" src="{r}assets/marca/logo-white-mark.png" alt="W-IT" width="64" height="48">
        <span class="claim">We Make It Simple</span>
        <img class="footer-ms" src="{r}assets/credenciales/WIT-MicrosoftPartner-singleline-white.png" alt="Microsoft Partner" width="200" height="40">
        <span>ISO 9001 · ISO 27001 (SGS)</span>
      </div>
      {col('Explora', [('Soluciones', f'{r}soluciones/'), ('Clientes por industria', f'{r}industrias/'), ('Productos', f'{r}productos/'), ('Herramientas', f'{r}herramientas/'), ('Cofinanciamiento Microsoft', f'{r}{COFIN_PAGE}')])}
      {col('Empresa', [('Quiénes somos', f'{r}nosotros/'), ('Cómo trabajamos', f'{r}como-trabajamos/'), ('Trust Center', f'{r}nosotros/confianza/'), ('Trabaja con nosotros', f'{r}nosotros/trabaja-con-nosotros/'), ('Observatorio IA', f'{r}recursos/')])}
      <address class="footer-col"><strong>Contacto</strong><span><b class="footer-pais"><img class="flag" src="{r}assets/img/chile.svg" alt="" width="21" height="14">Chile</b>Av. Apoquindo 3039<br>Las Condes, Santiago</span><span><b class="footer-pais"><img class="flag" src="{r}assets/img/peru.svg" alt="" width="21" height="14">Perú</b>Av. Circunvalación del Golf Los Incas 170, Int. 702<br>Santiago de Surco, Lima</span><a href="tel:+56224096112">+56 2 2409 6112</a><a href="mailto:info@w-it.cl">info@w-it.cl</a><a class="link-green" href="{r}contacto/">Escríbenos →</a></address>
    </div>
    <div class="footer-bottom">
      <nav aria-label="Legal"><a href="{r}privacidad/">Privacidad</a><a href="{r}cookies/">Cookies</a><a href="{r}terminos/">Términos</a></nav>
      <nav aria-label="Redes"><a href="#">LinkedIn</a><a href="#">YouTube</a><a href="#">Instagram</a></nav>
      <span>© 2026 W-IT SpA</span>
    </div>
  </div>
</footer>

<div class="agente" id="agente">
  <div class="agente-panel" id="agente-panel" role="dialog" aria-label="Agente W-IT" hidden>
    <strong>Agente W-IT</strong>
    <span>Soy un asistente de IA de W-IT. No cotizo ni doy asesoría legal; puedo derivarte a una persona.</span>
    <ul>
      <li><button type="button">¿Qué Copilot necesito?</button></li>
      <li><button type="button">¿Business Central o Finance?</button></li>
      <li><button type="button">Clientes en banca</button></li>
    </ul>
  </div>
  <button class="agente-fab" type="button" aria-controls="agente-panel" aria-expanded="false" aria-label="Abrir agente W-IT">
    <span class="clip-say" aria-hidden="true">¿Te ayudo?</span>
    <picture class="clip" aria-hidden="true"><source srcset="{r}assets/img/clippy.webp" type="image/webp"><img src="{r}assets/img/clippy.png" alt="" width="96" height="124"></picture>
  </button>
</div>'''


def write(path, title, desc, body, active=None, solid=True):
    depth = path.strip('/').count('/') + 1 if path else 0
    r = '../' * depth
    html = f'''<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="icon" type="image/png" href="{r}assets/marca/favicon.png">
<link rel="apple-touch-icon" href="{r}assets/marca/apple-touch-icon.png">
<link rel="stylesheet" href="{r}styles.css">
<script src="{r}main.js" defer></script>
</head>
<body{' class="has-solid-header"' if solid else ''}>
<a class="skip" href="#main">Saltar al contenido</a>
{header(r, active, solid)}
<main id="main">
{body(r) if callable(body) else body}
</main>
{footer(r)}
</body>
</html>
'''
    out = os.path.join(ROOT, path, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    return path


# ---------------------------------------------------------------- componentes

def page_hero(r, crumbs, eyebrow, h1, bajada, ctas=True, extra='', h1_pe=None, aside='', cls='', ver_href=None):
    bc = ''.join(f'<li><a href="{r}{h}">{escape(l)}</a></li>' for l, h in crumbs)
    h1_attr = pais_attr(h1, h1_pe) if h1_pe else ''
    cta = (f'<div class="btn-row"><a class="btn btn-lg btn-primary" href="{r}contacto/">Agenda un diagnóstico de 30 min</a>'
           f'<a class="btn btn-lg btn-outline" href="{ver_href or r + 'industrias/'}">Ver clientes</a></div>') if ctas else ''
    return f'''
<section class="page-hero{(" " + cls) if cls else ""}">
  <div class="page-hero-trazo" aria-hidden="true"></div>
  <div class="container page-hero-inner{' has-aside' if aside else ''}">
    <div class="page-hero-copy">
      <nav aria-label="Ruta"><ol class="crumbs"><li><a href="{r or './'}">Inicio</a></li>{bc}</ol></nav>
      <span class="eyebrow">{eyebrow}</span>
      <h1{h1_attr}>{escape(h1)}</h1>
      <p class="lead">{bajada}</p>
      {cta}{extra}
    </div>{aside}
  </div>
</section>'''


def cta_final(r, titulo='¿Conversamos sobre tu caso?', texto='Agenda un diagnóstico de 30 minutos. Revisamos tu escenario y te decimos qué conviene y qué no.'):
    return f'''
<section class="cta-band">
  <div class="container cta-band-inner">
    <div><h2>{escape(titulo)}</h2><p>{texto}</p></div>
    <div class="btn-row"><a class="btn btn-lg btn-green" href="{r}contacto/">Agenda un diagnóstico</a><a class="btn btn-lg btn-ghost-light" href="#agente" data-open-agente>Conversa con nuestro agente</a></div>
  </div>
</section>'''


def plataformas_strip(r):
    return '<ul class="plat-strip">' + ''.join(
        f'<li><a href="{r}soluciones/{sol}/">{ms_icon(r, ico, 40)}<span>{escape(n)}</span></a></li>' for ico, n, sol in PLATAFORMAS) + '</ul>'


def sol_card(r, s):
    linea = s['linea']
    attr = pais_attr(linea, s['linea_pe']) if s.get('linea_pe') else ''
    return f'''
      <a class="card sol-card" href="{r}soluciones/{s['slug']}/">
        {sol_icons(r, s)}
        <span class="sol-area">{escape(s['nombre'])}</span>
        <h3>{escape(s['plataforma'])}</h3>
        <p{attr}>{escape(linea)}</p>
        {pills(s['pills'])}
        <span class="card-cta">Ver solución {ARROW}</span>
      </a>'''


def caso_card(r, c):
    return f'''
      <a class="card caso-card" href="{r}casos-de-exito/{c['slug']}/" data-industria="{c['industria']}" data-solucion="{c['solucion']}">
        <span class="caso-logo-wrap">{logo(r, c['cliente'], 'caso-logo')}</span>
        <span class="metrica">{escape(c['metrica'])}</span>
        <span class="metrica-txt">{escape(c['metrica_txt'])}</span>
        <span class="titulo">{escape(c['titulo'])}</span>
        <span class="caso-tags">{escape(IND_NOMBRE[c['industria']])} · {escape(SOL[c['solucion']]['corto'])}</span>
      </a>'''


def logo_wall(r, slugs):
    return '<ul class="logo-wall">' + ''.join(f'<li>{logo(r, s)}</li>' for s in slugs) + '</ul>'


def section_head(eyebrow, h2, lead='', link=''):
    l = f'<p class="lead">{lead}</p>' if lead else ''
    head = f'<div class="section-head"><span class="eyebrow">{eyebrow}</span><h2 class="h2">{h2}</h2>{l}</div>'
    return f'<div class="section-head-row">{head}{link}</div>' if link else head


# Ilustración de "Señales": dos globos de conversación (pregunta y alerta) en colores de marca, SVG propio
SENALES_ART = """<svg class="sen-art" viewBox="0 0 160 132" aria-hidden="true" focusable="false">
  <path d="M22 10h76a18 18 0 0 1 18 18v44a18 18 0 0 1-18 18H52L34 106V90H22A18 18 0 0 1 4 72V28a18 18 0 0 1 18-18z" fill="#1B3A50"/>
  <text x="60" y="68" text-anchor="middle" font-family="Segoe UI, system-ui, sans-serif" font-size="52" font-weight="700" fill="#fff">?</text>
  <path d="M106 64h36a14 14 0 0 1 14 14v20a14 14 0 0 1-14 14h-8v14l-14-14h-14a14 14 0 0 1-14-14V78a14 14 0 0 1 14-14z" fill="#54BA00" stroke="#fff" stroke-width="4"/>
  <text x="124" y="101" text-anchor="middle" font-family="Segoe UI, system-ui, sans-serif" font-size="30" font-weight="700" fill="#fff">!</text>
</svg>"""


def senales_section(r, senales):
    """Señales de que lo necesitas: texto e ilustración a la izquierda, lista uniforme a la derecha.
    El foco (borde verde + barra) recorre la lista cada 3,5 s (main.js)."""
    items = ''.join(
        f'<li class="sen-item{" is-on" if n == 0 else ""}"><span class="sen-ico" aria-hidden="true">?</span>'
        f'<div class="sen-txt"><h3>{escape(t)}</h3><p>{escape(d)}</p></div></li>' for n, (t, d) in enumerate(senales))
    return f"""<section class="section bg-white senales" aria-labelledby="sen-title">
  <div class="container senales-inner">
    <div class="sen-head">
      {SENALES_ART}
      <span class="eyebrow">Señales de que lo necesitas</span>
      <h2 class="h2" id="sen-title">¿Te identificas con alguna de estas <em>situaciones</em>?</h2>
      <p class="lead">Son las situaciones que más vemos al iniciar un proyecto. En un diagnóstico de 30 minutos sabemos por dónde empezar.</p>
      <a class="btn btn-green" href="{r}contacto/">Agenda un diagnóstico</a>
    </div>
    <ol class="sen-list">{items}</ol>
  </div>
</section>"""

METODO_H2 = 'Cuatro marcos ágiles, uno para cada tipo de proyecto.'
METODO_LEAD = 'Trabajamos sobre los marcos de implementación de Microsoft, con entregas cortas, los usuarios dentro del equipo y la adopción medida en cada etapa.'


def metodo_html(r, m):
    """Línea de tiempo interactiva de una metodología (acordeón vertical en móvil). Fase 1 abierta; main.js maneja el resto.
    Los ids llevan el slug para poder mostrar varias metodologías en una misma página."""
    def lis(xs):
        return ''.join(f'<li>{escape(x)}</li>' for x in xs)
    k = m['slug']
    steps = ''.join(f"""
    <li class="mt-step{' is-on' if n == 0 else ''}">
      <button class="mt-btn{' is-on' if n == 0 else ''}" type="button" id="mt-{k}-b{n + 1}" aria-controls="mt-{k}-p{n + 1}" aria-expanded="{'true' if n == 0 else 'false'}">
        <span class="mt-dot" aria-hidden="true">{n + 1}</span><span class="mt-name">{escape(f['nombre'])}</span><span class="mt-sbd">{escape(f['marco'])}</span>
      </button>
      <div class="mt-panel" id="mt-{k}-p{n + 1}" role="region" aria-labelledby="mt-{k}-b{n + 1}"{'' if n == 0 else ' hidden'}>
        <div class="mt-panel-head"><p class="mt-linea">{escape(f['linea'])}</p><span class="mt-hito">{escape(m['hito_prefijo'])} · {escape(f['hito'])}</span></div>
        <div class="mt-cols">
          <div><h4>Qué hacemos</h4><ul>{lis(f['hacemos'])}</ul></div>
          <div><h4>Qué recibes</h4><ul>{lis(f['recibes'])}</ul></div>
          <div class="mt-ia"><h4><span class="{m.get('tag_cls', 'tag-ia')}">{escape(m.get('tag', 'IA'))}</span>{escape(m['col3'])}</h4><p>{escape(f['col3'])}</p></div>
        </div>
      </div>
    </li>""" for n, f in enumerate(m['fases']))
    fuentes = ' · '.join(f'<a href="{u}" target="_blank" rel="noopener">{escape(t)} ↗</a>' for t, u in m['fuentes'])
    variante = f" metodo-{m['variante']}" if m.get('variante') else ''
    return f"""<div class="metodo{variante}" data-metodo>
  <ol class="mt-rail" style="--i:0;--n:{len(m['fases'])}">{steps}
  </ol>
  <div class="mt-foot">
    <span class="mt-src">{escape(m['base'])} {fuentes}</span>
    <div class="mt-nav"><button type="button" data-mt="prev">← Anterior</button><span class="mt-count">1 / {len(m['fases'])}</span><button type="button" data-mt="next">Siguiente →</button></div>
  </div>
</div>"""


def cofin_strip(r):
    """Franja: Microsoft cofinancia el primer paso (misma estética que la franja Jumpstart)."""
    return f'''
    <div class="jumpstart cofin-strip">
      <img src="{r}assets/credenciales/WIT-MicrosoftPartner-singleline-white.png" alt="Microsoft Partner" width="144" height="48">
      <div class="js-txt">
        <span class="js-tier">Cofinanciamiento Microsoft</span>
        <strong>Microsoft cofinancia el primer paso: taller, POC o MVP.</strong>
        <p>Como Solutions Partner estamos habilitados en los programas de inversión de Microsoft. Evaluamos si tu empresa califica y gestionamos la solicitud.</p>
      </div>
      <a class="btn btn-outline" href="{r}{COFIN_PAGE}">POC y MVP cofinanciados {ARROW}</a>
    </div>'''


def cofinanciamiento(r):
    """Página: programas de inversión de Microsoft, cómo funciona, POC vs MVP y las etapas de cada una."""
    programas = ''.join(
        f'<article class="prog-card"><span class="eyebrow">{escape(p["area"])}</span><h3>{escape(p["nombre"])}</h3><p>{escape(p["que"])}</p>'
        f'<div class="pills">{"".join(f"<span class=\"pill\">{escape(u)}</span>" for u in p["usos"])}</div>'
        + (f'<a class="link-strong" href="{r}{p["href"]}">Conoce el programa {ARROW}</a>' if p.get('href') else '') + '</article>' for p in COFIN_PROGRAMAS)
    filas = ''.join(
        f'<div class="cmp-label">{escape(c)}</div><div class="cmp-cell cmp-poc"><span class="cmp-mini">POC</span>{escape(a)}</div><div class="cmp-cell cmp-mvp"><span class="cmp-mini">MVP</span>{escape(b)}</div>'
        for c, a, b in COFIN_COMPARA)
    faq = ''.join(
        f'<div class="faq-item"><h3><button type="button" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="faq-{i}">{escape(q)}</button></h3>'
        f'<p id="faq-{i}"{"" if i == 0 else " hidden"}>{escape(a)}</p></div>' for i, (q, a) in enumerate(COFIN_FAQ))
    return page_hero(r, [('Cómo trabajamos', 'como-trabajamos/'), ('Cofinanciamiento Microsoft', COFIN_PAGE)], 'Cofinanciamiento Microsoft',
                     'Microsoft cofinancia el primer paso.',
                     'Como Solutions Partner, W-IT está habilitado en los programas de inversión de Microsoft que financian total o parcialmente talleres, pruebas de concepto (POC) y productos mínimos viables (MVP). Estar habilitados es nuestro lado; la elegibilidad de cada cliente la evalúa Microsoft caso a caso, y lo revisamos contigo antes de prometer nada.',
                     ctas=False, extra=f'<div class="btn-row"><a class="btn btn-lg btn-primary" href="{r}contacto/">Evalúa si tu proyecto califica</a><a class="btn btn-lg btn-outline" href="#poc-mvp">POC o MVP: la diferencia</a></div>') + f'''
<section class="section bg-white"><div class="container stack-40">
  {section_head('Cómo funciona', COFIN_PROCESO['titulo'], COFIN_PROCESO['resumen'])}
  {metodo_html(r, COFIN_PROCESO)}
</div></section>
<section class="section bg-blue"><div class="container stack-40">
  {section_head('Programas habilitados', 'Lo que Microsoft puede financiar contigo.', 'Familias de programas en las que W-IT está habilitado como partner. Cada uno tiene reglas de elegibilidad propias y se solicita por proyecto.')}
  <div class="prog-grid">{programas}</div>
  <p class="disclaimer">Los nombres, alcances y condiciones de los programas los define Microsoft y pueden cambiar. Confirmamos la elegibilidad y el financiamiento disponible por escrito antes de empezar.</p>
</div></section>
<section class="section bg-white" id="poc-mvp"><div class="container stack-40">
  {section_head('POC o MVP', 'Diferencias entre una POC y un MVP.', 'Una POC responde preguntas; un MVP entrega un producto. Ambos se pueden hacer con cofinanciamiento de Microsoft, pero se planifican, se ejecutan y se cierran de forma distinta.')}
  <div class="cmp">
    <div class="cmp-head cmp-corner" aria-hidden="true"></div>
    <div class="cmp-head cmp-poc"><span class="cmp-tag">Laboratorio</span><h3>POC · Prueba de concepto</h3><p>Valida hipótesis antes de invertir.</p></div>
    <div class="cmp-head cmp-mvp"><span class="cmp-tag">Producto</span><h3>MVP · Producto mínimo viable</h3><p>Pequeño, completo y en producción.</p></div>
    {filas}
  </div>
</div></section>
<section class="section bg-blue" id="poc"><div class="container stack-40">
  {section_head('Prueba de concepto', COFIN_POC['titulo'], COFIN_POC['resumen'])}
  {metodo_html(r, COFIN_POC)}
</div></section>
<section class="section bg-white" id="mvp"><div class="container stack-40">
  {section_head('Producto mínimo viable', COFIN_MVP['titulo'], COFIN_MVP['resumen'])}
  {metodo_html(r, COFIN_MVP)}
</div></section>
<section class="section bg-white faq" id="faq"><div class="container stack-32">
  {section_head('Preguntas frecuentes', 'Lo que suelen preguntarnos.')}
  <div>{faq}</div>
</div></section>
{cta_final(r, '¿Tu proyecto califica para cofinanciamiento?', 'Agenda un diagnóstico de 30 minutos. Revisamos tu escenario, los programas que aplican y si conviene partir por una POC o un MVP.')}'''


def metodos_cards(r):
    """Home: las cuatro metodologías como tarjetas uniformes que llevan a /como-trabajamos/#slug."""
    return '<div class="metodos-grid">' + ''.join(
        f'<a class="metodo-card" href="{r}como-trabajamos/#{m["slug"]}">'
        f'<span class="eyebrow">{escape(m["para"])}</span><h3>{escape(m["titulo"])}</h3><p>{escape(m["resumen"].split(". Sobre ")[0].rstrip(".") + ".")}</p>'
        f'<ol class="mc-steps">{"".join(f"<li>{escape(f['nombre'])}</li>" for f in m["fases"])}</ol>'
        f'<span class="card-cta">Ver metodología {ARROW}</span></a>' for m in METODOS) + '</div>'


def badge_img(r, f, h=96):
    alt = {'WIT-MicrosoftCloud-color.png': 'Microsoft Solutions Partner for Microsoft Cloud',
           'WIT-AIBusinessSolutions-Agentic-color.png': 'Microsoft Solutions Partner for AI Business Solutions, especialización Agentic',
           'WIT-CloudAIPlatforms-color.png': 'Microsoft Solutions Partner for Cloud & AI Platforms',
           'WIT-Security-color.png': 'Microsoft Solutions Partner for Security'}[f]
    w, hh = Image.open(os.path.join(ROOT, 'assets/credenciales', f)).size
    return f'<img class="ms-badge" src="{r}assets/credenciales/{f}" alt="{alt}" width="{round(w * h / hh)}" height="{h}">'


VERIFICAR = 'https://marketplace.microsoft.com/en-us/partners/dcdbe467-cd53-4233-a80c-6c8510c2f60a/overview'
# Las seis designaciones Solutions Partner (Microsoft Cloud desde 2026-09-28).
DESIGNACIONES = ['Business Applications', 'Modern Work', 'Data &amp; AI', 'Digital &amp; App Innovation', 'Infrastructure', 'Security']
# False mientras el perfil de Marketplace no refleje Microsoft Cloud: la tarjeta enlaza al Trust Center en vez de "Verificar".
MS_CLOUD_EN_MARKETPLACE = True


def hero_trust(r):
    """Opción A: sello oficial Microsoft Partner + áreas en texto + ISO, dentro del hero."""
    return f'''
    <div class="hero-trust">
      <img class="ms-lockup" src="{r}assets/credenciales/WIT-MicrosoftPartner-singleline-white.png" alt="Microsoft Partner" width="312" height="104">
      <div class="ht-areas">
        <span>Microsoft Cloud · 6 de 6 designaciones</span>
        <ul>{''.join(f'<li>{d}</li>' for d in DESIGNACIONES)}</ul>
      </div>
      <div class="ht-iso">
        <img src="{r}assets/credenciales/SGS_ISO_9001_round_TCL_LR.jpg" alt="Sello SGS ISO 9001" width="48" height="48">
        <img src="{r}assets/credenciales/SGS_ISO-IEC_27001_TCL_LR.jpg" alt="Sello SGS ISO/IEC 27001" width="48" height="48">
        <div><strong>ISO 9001 · ISO 27001</strong><small>Certificación SGS</small></div>
      </div>
    </div>'''


def jumpstart_strip(r, extra_cls=''):
    """Programa Microsoft Copilot Jumpstart · Ready Tier (texto + ícono oficial de Copilot; sin sello de terceros)."""
    return f'''
    <div class="jumpstart{extra_cls}">
      <img class="ms-icon" src="{r}assets/ms/m365-copilot.svg" alt="" width="48" height="48">
      <div class="js-txt">
        <span class="js-tier">Ready Tier</span>
        <strong>Microsoft Copilot Jumpstart Partner</strong>
        <p>Somos parte del programa oficial de Microsoft que acelera la adopción de IA con Copilot y agentes, con recursos, talleres y engagements financiados por Microsoft para evaluar, planificar e implementar.</p>
      </div>
      <a class="btn btn-outline" href="{r}{JUMPSTART_PAGE}">Conoce el programa {ARROW}</a>
    </div>'''


PREMIOS = [
    dict(anio='2019', categoria='Microsoft Dynamics 365 for Sales', region='Latinoamérica y el Caribe',
         programa='Microsoft Latin America and the Caribbean Partners Awards', foto='premio-2019', pos='50% 8%',
         alt='Entrega del premio Microsoft Partner of the Year 2019 a W-IT en la categoría Dynamics 365 for Sales'),
    dict(anio='2020', categoria='Proactive Customer Service', region='Latinoamérica y el Caribe',
         programa='Microsoft Latin America and the Caribbean Partner of the Year Award', foto='premio-2020', pos='50% 78%',
         alt='Trofeo Microsoft Latin America and the Caribbean Award 2020, categoría Proactive Customer Service, entregado a W-IT'),
]
TROFEO = '''<svg class="award-trophy" viewBox="0 0 48 48" aria-hidden="true"><path d="M16 6h16v9a8 8 0 0 1-16 0z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/><path d="M16 9H9a6 6 0 0 0 7 7M32 9h7a6 6 0 0 1-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/><path d="M24 23v7M18 40h12M19.5 40l1-10h7l1 10" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'''


def premio_card(p):
    return (f'<article class="award"><div class="award-top">{TROFEO}<span class="award-kicker">Microsoft Partner of the Year</span></div>'
            f'<span class="award-year">{p["anio"]} <em>Winner</em></span>'
            f'<strong class="award-cat">{escape(p["categoria"])}</strong>'
            f'<span class="award-region">{escape(p["region"])}</span></article>')


def premios_strip(r):
    """Franja discreta: premios como trayectoria, no como credencial vigente."""
    items = ''.join(f'<li>{TROFEO}<span><b>Partner of the Year {p["anio"]}</b> · {escape(p["categoria"])}</span></li>' for p in PREMIOS)
    return (f'<div class="awards-strip"><span class="eyebrow">Reconocimientos Microsoft · Latinoamérica y el Caribe</span>'
            f'<ul>{items}</ul><a href="{r}nosotros/#premios">Ver trayectoria {ARROW}</a></div>')


def premios_section(r, fotos=True, bg='bg-dark'):
    cards = ''.join(premio_card(p) for p in PREMIOS)
    galeria = ''
    if fotos:
        galeria = '<div class="award-photos">' + ''.join(
            f'<figure><picture><source srcset="{r}assets/img/{p["foto"]}.webp" type="image/webp"><img src="{r}assets/img/{p["foto"]}.jpg" alt="{escape(p["alt"])}" loading="lazy" style="object-position:{p['pos']}"></picture>'
            f'<figcaption>{p["anio"]} · {escape(p["programa"])}</figcaption></figure>' for p in PREMIOS) + '</div>'
    return f'''
<section class="section {bg}" id="premios"><div class="container stack-40">
  {section_head('Reconocimientos', 'Microsoft Partner of the Year en Latinoamérica y el Caribe, dos años seguidos.', 'Premiados por Microsoft en 2019 por nuestras implementaciones de Dynamics 365 for Sales y en 2020 por servicio al cliente proactivo.')}
  <div class="awards">{cards}</div>
  {galeria}
</div></section>'''


def credenciales_section(r):
    """Opción B: tarjetas con el badge oficial completo y qué significa para el cliente."""
    def card(f, nombre, que):
        return (f'<article class="cred-card-b"><div class="cc-img">{badge_img(r, f, 170)}</div>'
                f'<div class="cc-txt"><h3>{nombre}</h3><p>{que}</p>'
                f'<div class="cc-meta"><span>Designación Microsoft</span><a href="{VERIFICAR}" target="_blank" rel="noopener">Verificar ↗</a></div></div></article>')
    return f'''
<section class="creds" aria-labelledby="creds-title">
  <div class="container">
    <div class="creds-head">
      <div><span class="eyebrow">Credenciales verificables</span><h2 class="h2" id="creds-title">Microsoft validó nuestra capacidad en todas sus áreas de soluciones.</h2></div>
      <a class="link-strong" href="{VERIFICAR}" target="_blank" rel="noopener">Verifícalo en Microsoft ↗</a>
    </div>
    <article class="cred-cloud">
      <div class="cc-img">{badge_img(r, 'WIT-MicrosoftCloud-color.png', 170)}</div>
      <div class="cc-txt"><span class="eyebrow">6 de 6 designaciones</span><h3>Solutions Partner for Microsoft Cloud</h3>
        <p>Tenemos las seis designaciones Solutions Partner de Microsoft. Un solo partner para todas tus soluciones Microsoft: aplicaciones de negocio, trabajo moderno, datos e IA, aplicaciones, infraestructura y seguridad.</p>
        <ul class="cc-desig">{''.join(f'<li>{d}</li>' for d in DESIGNACIONES)}</ul>
        <div class="cc-meta"><span>Designación Microsoft</span>{f'<a href="{VERIFICAR}" target="_blank" rel="noopener">Verificar ↗</a>' if MS_CLOUD_EN_MARKETPLACE else f'<a href="{r}nosotros/confianza/">Ver credenciales {ARROW}</a>'}</div></div>
    </article>
    <div class="creds-grid">
      {card('WIT-AIBusinessSolutions-Agentic-color.png', 'AI Business Solutions', 'Dynamics 365, Power Platform, Microsoft 365 y Copilot. Con especialización en soluciones agénticas.')}
      {card('WIT-CloudAIPlatforms-color.png', 'Cloud &amp; AI Platforms', 'Azure: datos e IA, innovación de aplicaciones e infraestructura.')}
      {card('WIT-Security-color.png', 'Security', 'Protección de identidades, información y amenazas con tecnología Microsoft.')}
    </div>
    {jumpstart_strip(r)}
    <div class="creds-iso">
      <img src="{r}assets/credenciales/SGS_ISO_9001_round_TCL_LR.jpg" alt="Sello SGS ISO 9001" width="64" height="62">
      <img src="{r}assets/credenciales/SGS_ISO-IEC_27001_TCL_LR.jpg" alt="Sello SGS ISO/IEC 27001" width="64" height="63">
      <div><strong>ISO 9001 · ISO/IEC 27001</strong><span>Calidad y seguridad de la información, certificadas por SGS.</span></div>
      <a href="{r}nosotros/confianza/">Ver en el Trust Center {ARROW}</a>
    </div>
    {premios_strip(r)}
  </div>
</section>'''


# ---------------------------------------------------------------- home

def home(r):
    marquee_logos = [c for c in CLIENTES if c not in ALIANZAS]
    rows = [marquee_logos[0::2], marquee_logos[1::2]]
    marquee = ''.join(
        f'<div class="marquee-row"><ul class="marquee{" marquee-rev" if i else ""}">' +
        ''.join(f'<li>{logo(r, s)}</li>' for s in row) + '</ul></div>' for i, row in enumerate(rows))
    faq = ''.join(
        f'<div class="faq-item"><h3><button type="button" aria-expanded="{"true" if i == 1 else "false"}" aria-controls="faq-{i}">{escape(q)}</button></h3>'
        f'<p id="faq-{i}"{"" if i == 1 else " hidden"}>{escape(a)}</p></div>' for i, (q, a) in enumerate(FAQ_HOME))
    return f'''
<section class="hero" id="hero">
  <div class="hero-bg hero-media" aria-hidden="true">
    <picture>
      <source srcset="{r}assets/img/hero-fondo.webp" type="image/webp">
      <img src="{r}assets/img/hero-fondo.jpg" alt="" width="1672" height="941" fetchpriority="high">
    </picture>
  </div>
  <div class="hero-bg hero-trazo" aria-hidden="true"></div>
  <div class="container hero-body">
    <div class="hero-grid">
      <div class="hero-copy">
        <span class="eyebrow">Solutions Partner for Microsoft Cloud · Chile y Perú</span>
        <h1>IA en producción sobre tus <em>sistemas reales</em>.</h1>
        <p class="hero-lead">Implementamos Dynamics 365, Power Platform, Azure y agentes de IA en grandes empresas y organismos públicos. Con equipo propio certificado y resultados medidos.</p>
        <div class="btn-row">
          <a class="btn btn-lg btn-green" href="{r}contacto/">Agenda un diagnóstico de 30 min</a>
          <a class="btn btn-lg btn-ghost-light" href="#agente" data-open-agente>Conversa con nuestro agente</a>
        </div>
      </div>
      <div class="hero-demo">
        <div class="console" id="console" data-canal="web" aria-label="Ejemplo ilustrativo de un agente de IA trabajando sobre sistemas de negocio">
          <div class="console-bar">
            <span class="console-dots" aria-hidden="true"><i></i><i></i><i></i></span>
            <span class="avatar-b" aria-hidden="true">W</span>
            <span class="console-title"><span class="console-name"><span class="live-dot" aria-hidden="true"></span>Agente W-IT</span><span class="console-sub" data-c="sub">en producción</span></span>
            <span class="console-tabs" role="tablist" aria-label="Escenarios"></span>
          </div>
          <div class="console-body" aria-live="polite">
            <div class="msg msg-user">
              <span class="avatar-u" aria-hidden="true">Tú</span>
              <div class="bubble"><span class="sender">Tú <time data-c="time"></time></span><p class="console-prompt" data-c="prompt"></p><span class="meta"><time data-c="time"></time><i class="ticks" aria-hidden="true"></i></span></div>
            </div>
            <div class="msg msg-bot">
              <span class="avatar-b" aria-hidden="true">W</span>
              <div class="bubble"><span class="sender">Agente W-IT <b class="app-badge">App</b> <time data-c="time"></time></span><ol class="console-steps" data-c="steps"></ol><div class="console-result" data-c="result"></div></div>
            </div>
          </div>
          <div class="console-foot"><span>Ejemplo ilustrativo · no son datos de clientes</span><span class="console-human">Supervisión humana</span></div>
          <div class="console-input" aria-hidden="true"><span data-c="placeholder">Escribe un mensaje</span><i class="send"></i></div>
        </div>
        <div class="canales" role="group" aria-label="Cómo se ve en cada canal">
          <button type="button" data-canal="web" aria-pressed="true" aria-label="Web"><span class="tip">Web</span><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#54BA00" d="M12 2.5C6.5 2.5 2 6.3 2 11c0 2.4 1.2 4.6 3.1 6.1L4 21.5l4.6-2.2c1.1.3 2.2.5 3.4.5 5.5 0 10-3.8 10-8.5S17.5 2.5 12 2.5z"/><circle cx="8.3" cy="11" r="1.3" fill="#14293A"/><circle cx="12" cy="11" r="1.3" fill="#14293A"/><circle cx="15.7" cy="11" r="1.3" fill="#14293A"/></svg></button>
          <button type="button" data-canal="teams" aria-pressed="false" aria-label="Microsoft Teams"><span class="tip">Microsoft Teams</span><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#5B5FC7" d="M20.625 8.127q-.55 0-1.025-.205-.475-.205-.832-.563-.358-.357-.563-.832Q18 6.053 18 5.502q0-.54.205-1.02t.563-.837q.357-.358.832-.563.474-.205 1.025-.205.54 0 1.02.205t.837.563q.358.357.563.837.205.48.205 1.02 0 .55-.205 1.025-.205.475-.563.832-.357.358-.837.563-.48.205-1.02.205zm0-3.75q-.469 0-.797.328-.328.328-.328.797 0 .469.328.797.328.328.797.328.469 0 .797-.328.328-.328.328-.797 0-.469-.328-.797-.328-.328-.797-.328zM24 10.002v5.578q0 .774-.293 1.46-.293.685-.803 1.194-.51.51-1.195.803-.686.293-1.459.293-.445 0-.908-.105-.463-.106-.85-.329-.293.95-.855 1.729-.563.78-1.319 1.336-.756.557-1.67.861-.914.305-1.898.305-1.148 0-2.162-.398-1.014-.399-1.805-1.102-.79-.703-1.312-1.664t-.674-2.086h-5.8q-.411 0-.704-.293T0 16.881V6.873q0-.41.293-.703t.703-.293h8.59q-.34-.715-.34-1.5 0-.727.275-1.365.276-.639.75-1.114.475-.474 1.114-.75.638-.275 1.365-.275t1.365.275q.639.276 1.114.75.474.475.75 1.114.275.638.275 1.365t-.275 1.365q-.276.639-.75 1.113-.475.475-1.114.75-.638.276-1.365.276-.188 0-.375-.024-.188-.023-.375-.058v1.078h10.875q.469 0 .797.328.328.328.328.797zM12.75 2.373q-.41 0-.78.158-.368.158-.638.434-.27.275-.428.639-.158.363-.158.773 0 .41.158.78.159.368.428.638.27.27.639.428.369.158.779.158.41 0 .773-.158.364-.159.64-.428.274-.27.433-.639.158-.369.158-.779 0-.41-.158-.773-.159-.364-.434-.64-.275-.275-.639-.433-.363-.158-.773-.158zM6.937 9.814h2.25V7.94H2.814v1.875h2.25v6h1.875zm10.313 7.313v-6.75H12v6.504q0 .41-.293.703t-.703.293H8.309q.152.809.556 1.5.405.691.985 1.19.58.497 1.318.779.738.281 1.582.281.926 0 1.746-.352.82-.351 1.436-.966.615-.616.966-1.43.352-.815.352-1.752zm5.25-1.547v-5.203h-3.75v6.855q.305.305.691.452.387.146.809.146.469 0 .879-.176.41-.175.715-.48.304-.305.48-.715t.176-.879Z"/></svg></button>
          <button type="button" data-canal="whatsapp" aria-pressed="false" aria-label="WhatsApp"><span class="tip">WhatsApp</span><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#25D366" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg></button>
          <button type="button" data-canal="gchat" aria-pressed="false" aria-label="Google Chat"><span class="tip">Google Chat</span><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#00AC47" d="M1.637 0C.733 0 0 .733 0 1.637v16.5c0 .904.733 1.636 1.637 1.636h3.955v3.323c0 .804.97 1.207 1.539.638l3.963-3.96h11.27c.903 0 1.636-.733 1.636-1.637V5.592L18.408 0Zm3.955 5.592h12.816v8.59H8.455l-2.863 2.863Z"/></svg></button>
        </div>
      </div>
    </div>
    {hero_trust(r)}
  </div>
</section>
{credenciales_section(r)}

<section class="logos" aria-label="Clientes" id="marquee">
  <div class="container logos-head">
    <span>Más de 60 organizaciones han confiado en W-IT</span>
    <a href="{r}industrias/">Ver clientes por industria {ARROW}</a>
  </div>
  {marquee}
</section>

<section class="cifras" aria-label="W-IT en cifras">
  <div class="container">
    <dl class="cifras-grid">
      <div class="cifra"><dd>+400</dd><dt>proyectos implementados</dt></div>
      <div class="cifra"><dd>+200 mil</dd><dt>horas de consultoría en proyectos</dt></div>
      <div class="cifra"><dd>+35</dd><dt>personas certificadas en Dynamics 365, Power Platform, Copilot y Azure</dt></div>
      <div class="cifra"><dd>6 de 6</dd><dt>designaciones Microsoft Solutions Partner</dt><span class="nota">Solutions Partner for Microsoft Cloud</span></div>
      <div class="cifra"><dd>2014</dd><dt>Partner Microsoft desde 2014</dt><span class="nota">Microsoft Partner Network</span></div>
      <div class="cifra"><dd>ISO</dd><dt>9001 · 27001, certificadas con SGS</dt><span class="nota">SGS</span></div>
    </dl>
    <p class="fuente">Fuente: Partner Center y registros internos.</p>
  </div>
</section>

<section class="section bg-soft" id="soluciones">
  <div class="container stack-48">
    {section_head('Soluciones Microsoft', 'Implementamos Microsoft Dynamics 365, Power Platform, Azure y Copilot.', 'Primero entendemos el proceso. Después elegimos la tecnología Microsoft que corresponde.', f'<a class="link-strong" href="{r}herramientas/autodiagnostico-ia/">¿No sabes por dónde empezar? Autodiagnóstico {ARROW}</a>')}
    {plataformas_strip(r)}
    <div class="grid sol-grid">{''.join(sol_card(r, s) for s in SOLUCIONES)}
    </div>
  </div>
</section>

<section class="section bg-blue" id="metodo">
  <div class="container stack-48">
    {section_head('Cómo trabajamos', METODO_H2, METODO_LEAD, '<span class="chip-live">Adopción medida en cada proyecto</span>')}
    {metodos_cards(r)}
    <a class="link-strong" href="{r}como-trabajamos/">Conoce las cuatro metodologías {ARROW}</a>
    {cofin_strip(r)}
  </div>
</section>

<section class="section bg-green" id="herramientas">
  <div class="container stack-40">
    {section_head('Herramientas', 'Estima, compara y diagnostica en pocos minutos.', link=f'<a class="link-strong" href="{r}herramientas/">Todas las herramientas {ARROW}</a>')}
    <div class="grid grid-280">{''.join(tool_card(r, h) for h in HERRAMIENTAS[:3])}
    </div>
    <p class="disclaimer">Los resultados no son una cotización ni asesoría legal.</p>
  </div>
</section>

<section class="section bg-dark" id="confianza">
  <div class="container grid grid-2 trust-grid">
    <div class="trust-copy">
      <span class="eyebrow">Trust Center</span>
      <h2 class="h2">Todo lo que declaramos se puede verificar.</h2>
      <p>Designaciones Microsoft, ISO 9001 e ISO 27001 con SGS, datos en Azure Chile Central y una política de IA responsable publicada.</p>
      <div class="btn-row">
        <a class="link-green" href="{VERIFICAR}" target="_blank" rel="noopener">Verifícalo en Microsoft ↗</a>
        <a class="link-light" href="{r}nosotros/confianza/">Ir al Trust Center {ARROW}</a>
      </div>
    </div>
    {trust_items()}
  </div>
</section>

<section class="section bg-white">
  <div class="container grid grid-2">
    <figure class="testimonio">
      <div class="placeholder-box">video testimonial 60–90 s [placeholder + autorización]</div>
      <blockquote>“[placeholder: cita del cliente, 1–2 frases, con autorización escrita]”</blockquote>
      <figcaption><span class="avatar"></span><span><strong>[Nombre Apellido]</strong>[Cargo], [Empresa]</span></figcaption>
    </figure>
    <div class="presencia">
      <span class="eyebrow">Presencia</span>
      <h2 class="h2">Proyectos en Chile y Perú</h2>
      <div class="placeholder-box mapa">mapa SVG Chile–Perú, puntos por región e industria<br>[placeholder de datos internos]
        <i style="left:38%;top:22%"></i><i style="left:52%;top:58%"></i><i style="left:55%;top:78%"></i>
      </div>
    </div>
  </div>
</section>

<section class="section bg-soft">
  <div class="container stack-40">
    {section_head('Recursos · Observatorio IA Chile/Perú', 'Análisis y guías sobre IA en Chile y Perú.', link=f'<a class="link-strong" href="{r}recursos/">Todos los recursos {ARROW}</a>')}
    {recursos_grid(r)}
  </div>
</section>

<section class="section bg-white" id="contacto">
  <div class="container grid grid-2 cta-grid">
    <div class="cta">
      <h2 class="h2">Agenda un diagnóstico de 30 minutos.</h2>
      <p class="lead">Revisamos tu escenario y te decimos qué conviene y qué no. Te respondemos en menos de 1 día hábil.</p>
      <div class="btn-row"><a class="btn btn-lg btn-primary" href="{r}contacto/">Agendar</a><a class="btn btn-lg btn-outline" href="#">WhatsApp</a></div>
      <span class="cta-contacto">Av. Apoquindo 3039, Las Condes, Santiago · +56 2 2409 6112</span>
    </div>
    <div class="faq" id="faq"><span class="eyebrow">Preguntas frecuentes</span>{faq}</div>
  </div>
</section>'''


def tool_card(r, h):
    return f'''
      <a class="card tool-card" href="{r}herramientas/{h['slug']}/">
        <div class="tool-top"><span>{escape(h['tiempo'])}</span><span class="pill">{h['estado']}</span></div>
        <h3>{escape(h['nombre'])}</h3>
        <p>{escape(h['que'])}</p>
        <span class="card-cta">Empezar {ARROW}</span>
      </a>'''


def trust_items():
    items = [('Microsoft', 'Solutions Partner for Microsoft Cloud', 'Las seis designaciones Solutions Partner de Microsoft.'),
             ('Microsoft', 'AI Business Solutions', 'Business Applications y Modern Work, con especialización en Agentic Business Solutions.'),
             ('Microsoft', 'Cloud &amp; AI Platforms · Security', 'Data &amp; AI, Digital &amp; App Innovation, Infrastructure y Security.'),
             ('SGS', 'ISO 9001 · ISO/IEC 27001', 'Calidad y seguridad de la información. Certificado descargable [PDF].'),
             ('Azure Chile Central', 'Datos en Chile, en tu tenant', 'Implementaciones en la región desde 2025.'),
             ('Política publicada', 'IA responsable', 'Supervisión humana, trazabilidad y datos que no entrenan modelos.')]
    return '<div class="trust-items">' + ''.join(
        f'<div class="trust-item"><span class="meta">{m}</span><strong>{t}</strong><span>{d}</span></div>' for m, t, d in items) + '</div>'


def recursos_grid(r):
    items = [('portada Observatorio [placeholder]', 'Observatorio IA', 'Observatorio IA Chile/Perú · Primer número', '[placeholder]'),
             ('foto real: Hackathon Agrosuper 2024', 'Evento', 'Hackathon Agrosuper 2024: agentes en 48 horas', '2024')]
    return '<div class="grid grid-280">' + ''.join(
        f'<a class="recurso" href="{r}recursos/"><div class="placeholder-box">{a}</div><span class="tipo">{b}</span><h3>{c}</h3><span class="fecha">{d}</span></a>'
        for a, b, c, d in items) + '</div>'


# ---------------------------------------------------------------- páginas internas

def soluciones_index(r):
    return page_hero(r, [('Soluciones', 'soluciones/')], 'Soluciones Microsoft', 'Microsoft Dynamics 365, Power Platform, Azure y Copilot, implementados por especialistas.',
                     'Primero entendemos el proceso. Después elegimos la tecnología Microsoft que corresponde y la implementamos con equipo propio.') + f'''
<section class="section bg-soft"><div class="container stack-40">{plataformas_strip(r)}<div class="grid sol-grid">{''.join(sol_card(r, s) for s in SOLUCIONES)}</div></div></section>
{cta_final(r)}'''


def solucion_page(s):
    def body(r):
        prods = ''.join(
            f'''<div class="product-card">{ms_icon(r, i, 40) if i else f'<span class="icon-slot" aria-hidden="true">{SHIELD}</span>'}
              <div><h3>{escape(MS[i]) if i else escape(d.split(':')[0])}</h3><p>{escape(d.split(': ', 1)[1] if (not i and ': ' in d) else d)}</p><p class="cuando"><strong>Cuándo conviene:</strong> {escape(c)}</p></div></div>'''
            for i, d, c in s['productos'])
        senales = senales_section(r, s['senales'])
        aside = f'<div class="page-hero-aside">{"".join(f"<span class=\"hero-prod\">{ms_icon(r, i, 44)}<span>{escape(MS[i])}</span></span>" for i in s["iconos"])}</div>' if s['iconos'] else ''
        return page_hero(r, [('Soluciones', 'soluciones/'), (s['nombre'], f"soluciones/{s['slug']}/")], f"{escape(s['plataforma'])} · {escape(s['nombre'])}", s['h1'], s['bajada'],
                         h1_pe=s.get('h1_pe'), aside=aside) + f'''
{senales}
<section class="section bg-soft"><div class="container stack-40">
  {section_head('Qué implementamos', 'Tecnología Microsoft, elegida según tu proceso.')}
  <div class="product-grid">{prods}</div>
  {f'<div class="note">{s["alianza"]}</div>' if s.get('alianza') else ''}
  {premios_strip(r) if s['slug'] == 'ventas-servicio-y-contact-center' else ''}
  <p class="disclaimer">Los íconos y nombres de productos son marcas de Microsoft y se usan solo para identificar los productos que implementamos.</p>
</div></section>
<section class="section bg-blue"><div class="container stack-40">
  {section_head('Cómo lo hacemos', METODO[s['metodo']]['titulo'], METODO[s['metodo']]['resumen'], f'<a class="link-strong" href="{r}como-trabajamos/">Cómo trabajamos {ARROW}</a>')}
  {metodo_html(r, METODO[s['metodo']])}
  {cofin_strip(r)}
</div></section>
<section class="section bg-soft"><div class="container grid grid-2 aligned">
  <div class="cred-card"><span class="eyebrow">Credencial que respalda esta solución</span>{badge_img(r, s['credencial'], 110)}<p>{escape(s['credencial_txt'])}</p><a href="{r}nosotros/confianza/">Ver Trust Center {ARROW}</a></div>
  <a class="card tool-card" href="{r}{s['herramienta'][1]}"><div class="tool-top"><span>Herramienta relacionada</span><span class="pill">Gratis</span></div><h3>{escape(s['herramienta'][0])}</h3><p>Resultados orientativos. No son una cotización ni asesoría legal.</p><span class="card-cta">Empezar {ARROW}</span></a>
</div></section>
{cta_final(r)}'''
    return body


def industrias_index(r):
    cards = ''.join(f'''
      <a class="card ind-card" href="{r}industrias/{i['slug']}/">
        <span class="mega-ind-ico">{IND_ICON[i['slug']]}</span>
        <h3>{escape(i['nombre'])}</h3><p>{escape(i['h1'])}</p>
        <div class="ind-logos">{''.join(logo(r, c) for c in i['clientes'][:4])}</div>
        <span class="card-cta">Ver clientes {ARROW}</span>
      </a>''' for i in INDUSTRIAS)
    return page_hero(r, [('Clientes por industria', 'industrias/')], 'Clientes por industria', 'Conocemos tu industria porque ya trabajamos en ella.',
                     'Más de 60 organizaciones en once industrias, de la banca y el sector público a la minería, el retail y los deportes.') + f'''
<section class="section bg-soft"><div class="container"><div class="grid grid-300">{cards}</div></div></section>
{cta_final(r)}'''


def industria_img(r, slug):
    """Imagen del hero de industria. Fuente: assets/img/industrias/<slug>.png|jpg (p. ej. exportada de ChatGPT).
    Genera <slug>-hero.webp/.jpg a 1200 px de ancho cuando la fuente es más nueva. Sin fuente: sin imagen."""
    d = os.path.join(ROOT, 'assets', 'img', 'industrias')
    src = next((os.path.join(d, f'{slug}.{e}') for e in ('png', 'jpg', 'jpeg', 'webp') if os.path.exists(os.path.join(d, f'{slug}.{e}'))), None)
    if not src:
        return ''
    webp, jpg = (os.path.join(d, f'{slug}-hero.{e}') for e in ('webp', 'jpg'))
    if not os.path.exists(webp) or os.path.getmtime(webp) < os.path.getmtime(src):
        im = Image.open(src).convert('RGB')
        if im.width > 1200:
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        im.save(webp, 'WEBP', quality=82, method=6)
        im.save(jpg, 'JPEG', quality=84, optimize=True, progressive=True)
    w, h = Image.open(webp).size
    return (f'<div class="page-hero-aside ind-hero-media"><picture>'
            f'<source srcset="{r}assets/img/industrias/{slug}-hero.webp" type="image/webp">'
            f'<img src="{r}assets/img/industrias/{slug}-hero.jpg" alt="" width="{w}" height="{h}" fetchpriority="high">'
            f'</picture></div>')


def industria_panel(r, i):
    """Panel del hero de industria: desafíos más comunes del sector y su regulación."""
    items = ''.join(f'<li><span class="ind-panel-n">0{n}</span><p>{escape(d)}</p></li>' for n, d in enumerate(i['desafios'], 1))
    reg = f'<p class="ind-panel-reg"><strong>Regulación relevante:</strong> {escape(i["regulacion"])}</p>' if i['regulacion'] else ''
    return f'''<aside class="page-hero-aside ind-panel" aria-label="Desafíos más comunes">
      <span class="eyebrow">Desafíos más comunes de la industria</span>
      <ol class="ind-panel-list">{items}</ol>
      {reg}
    </aside>'''


def industria_page(i):
    def body(r):
        return page_hero(r, [('Clientes por industria', 'industrias/'), (i['nombre'], f"industrias/{i['slug']}/")], i['nombre'], i['h1'],
                         'Soluciones Microsoft implementadas por un equipo que conoce los procesos y la regulación de tu sector.',
                         aside=industria_panel(r, i), ver_href='#clientes') + f'''
<section class="section bg-white" id="clientes"><div class="container stack-40">
  {section_head('Clientes', f'Han confiado en W-IT en {escape(i["nombre"].lower())}.')}
  {logo_wall(r, i['clientes'])}
</div></section>
<section class="section bg-soft"><div class="container stack-40">
  {section_head('Soluciones Microsoft', 'Productos y soluciones que podrían aplicar.')}
  <div class="grid grid-300">{''.join(sol_card(r, SOL[s]) for s in i['soluciones'])}</div>
</div></section>
{cta_final(r)}'''
    return body


def casos_index(r):
    opts_i = ''.join(f'<button type="button" data-filter="industria" data-value="{k}">{escape(v)}</button>' for k, v in IND_NOMBRE.items() if any(c['industria'] == k for c in CASOS))
    opts_s = ''.join(f'<button type="button" data-filter="solucion" data-value="{s["slug"]}">{escape(s["corto"])}</button>' for s in SOLUCIONES if any(c['solucion'] == s['slug'] for c in CASOS))
    return page_hero(r, [('Casos de éxito', 'casos-de-exito/')], 'Casos de éxito', 'Grandes clientes, grandes implementaciones.',
                     'Proyectos reales de W-IT con grandes organizaciones de Chile, sobre Microsoft Dynamics 365, Power Platform y Azure.', ctas=False) + f'''
<section class="section bg-soft"><div class="container stack-32">
  <div class="filters" id="filtros">
    <div class="filter-group"><span>Industria</span><button type="button" class="is-on" data-filter="industria" data-value="*">Todas</button>{opts_i}</div>
    <div class="filter-group"><span>Solución</span><button type="button" class="is-on" data-filter="solucion" data-value="*">Todas</button>{opts_s}</div>
  </div>
  <div class="grid grid-280" id="casos-grid">{''.join(caso_card(r, c) for c in CASOS)}</div>
  <p class="filters-empty" hidden>No hay casos para esa combinación todavía.</p>
</div></section>
{cta_final(r, '¿Tienes un desafío parecido?')}'''


def caso_page(c):
    def body(r):
        s = SOL[c['solucion']]
        stack = ''.join(f'<span class="hero-prod">{ms_icon(r, i, 36)}<span>{escape(MS[i])}</span></span>' for i in c['stack'])
        stack_html = f'<div class="hero-prods">{stack}</div>' if stack else ''
        rel = [x for x in CASOS if x['slug'] != c['slug'] and (x['solucion'] == c['solucion'] or x['industria'] == c['industria'])][:3]
        kpis = ''.join(f'<div class="signal kpi"><b>{escape(v)}</b><p>{escape(t)}</p></div>' for v, t in c['metricas'])
        alcance = ''.join(f'<li>{escape(a)}</li>' for a in c['alcance'])
        return f'''
<section class="page-hero">
  <div class="page-hero-trazo" aria-hidden="true"></div>
  <div class="container page-hero-inner">
    <div class="page-hero-copy">
      <nav aria-label="Ruta"><ol class="crumbs"><li><a href="{r}">Inicio</a></li><li><a href="{r}casos-de-exito/">Casos de éxito</a></li><li><a href="{r}casos-de-exito/{c['slug']}/">{escape(CLIENTES[c['cliente']])}</a></li></ol></nav>
      {logo(r, c['cliente'], 'caso-hero-logo')}
      <h1>{escape(c['titulo'])}</h1>
      <p class="lead">{escape(c['resumen'])}</p>
      <dl class="caso-facts">
        <div><dt>Cliente</dt><dd>{escape(CLIENTES[c['cliente']])}</dd></div>
        <div><dt>Industria</dt><dd>{escape(IND_NOMBRE[c['industria']])}</dd></div>
        <div><dt>País</dt><dd>Chile</dd></div>
        <div><dt>Solución</dt><dd>{escape(s['nombre'])}</dd></div>
      </dl>
    </div>
  </div>
</section>
<section class="section bg-white"><div class="container grid grid-2 aligned">
  <div class="caso-metric"><span class="metrica-xl">{escape(c['metrica'])}</span><span>{escape(c['metrica_txt'])}</span></div>
  <div class="stack-20">
    <span class="eyebrow">Qué hicimos</span>
    <p class="lead">{escape(c['texto'])}</p>
    {stack_html}
  </div>
</div></section>
<section class="section bg-soft"><div class="container stack-40">
  {section_head('En números', 'La escala de la operación.')}
  <div class="signals signals-3 kpis">{kpis}</div>
  <div class="stack-20"><span class="eyebrow">Alcance</span><ul class="checks checks-grid">{alcance}</ul></div>
</div></section>
<section class="section bg-white"><div class="container stack-40">
  {section_head('Casos relacionados', 'Más proyectos como este.')}
  <div class="grid grid-280">{''.join(caso_card(r, x) for x in rel)}</div>
</div></section>
{cta_final(r, '¿Tienes un desafío parecido?')}'''
    return body


def productos_index(r):
    items = [('agentes-w-it', 'Agentes W-IT', 'Agentes y aceleradores publicados en Microsoft Marketplace.')]
    cards = ''.join(f'<a class="card" href="{r}productos/{a}/"><span class="icon-slot" aria-hidden="true">{SHIELD}</span><h3>{b}</h3><p>{c}</p><span class="card-cta">Conocer {ARROW}</span></a>' for a, b, c in items)
    return page_hero(r, [('Productos', 'productos/')], 'Productos W-IT', 'Soluciones propias sobre la nube de Microsoft.',
                     'Productos desarrollados por W-IT y publicados en Microsoft Marketplace.', ctas=False) + f'''
<section class="section bg-soft"><div class="container"><div class="grid grid-300">{cards}</div></div></section>
{cta_final(r)}'''


def agentes(r):
    items = [('Agente CV – Recruit Intelligence', 'Live'), ('Gestor de Puestos W-it', 'Live'),
             ('Implementación Rápida de Automatización con Power Automate', 'Live')]
    cards = ''.join(f'<div class="card"><div class="tool-top"><span>Microsoft Marketplace</span><span class="pill">{e}</span></div><h3>{escape(n)}</h3><p>[placeholder: descripción breve de la ficha]</p><a class="card-cta" href="https://marketplace.microsoft.com" target="_blank" rel="noopener">Ver ficha ↗</a></div>' for n, e in items)
    return page_hero(r, [('Productos', 'productos/'), ('Agentes W-IT', 'productos/agentes-w-it/')], 'Productos · Agentes W-IT',
                     'Agentes y aceleradores listos para tu tenant.', 'Publicados en Microsoft Marketplace. <span class="ph">[confirmar el resto del catálogo]</span>', ctas=False) + f'''
<section class="section bg-soft"><div class="container"><div class="grid grid-280">{cards}</div></div></section>
{cta_final(r)}'''


def herramientas_index(r):
    return page_hero(r, [('Herramientas', 'herramientas/')], 'Herramientas', 'Estima, compara y diagnostica en pocos minutos.',
                     'Herramientas gratuitas para estimar, diagnosticar y comparar. Los resultados no son una cotización ni asesoría legal.', ctas=False) + f'''
<section class="section bg-green"><div class="container"><div class="grid grid-280">{''.join(tool_card(r, h) for h in HERRAMIENTAS)}</div></div></section>
{cta_final(r)}'''


def diag_layout(r, h, wid, lead, obtienes, datos, steps=''):
    """Hero de herramienta interactiva: intro a la izquierda y wizard a la derecha (lo dibuja main.js)."""
    datos = json.dumps(datos, ensure_ascii=False).replace('</', r'<\/')
    return f'''
<section class="page-hero diag-hero">
  <div class="page-hero-trazo" aria-hidden="true"></div>
  <div class="container diag-layout">
    <div class="diag-intro">
      <nav aria-label="Ruta"><ol class="crumbs"><li><a href="{r}">Inicio</a></li><li><a href="{r}herramientas/">Herramientas</a></li><li><a href="{r}herramientas/{h['slug']}/">{escape(h['nombre'])}</a></li></ol></nav>
      <span class="eyebrow">Herramienta · {escape(h['tiempo'])}</span>
      <h1>{escape(h['nombre'])}</h1>
      <p class="lead">{lead}</p>
      <ul class="diag-gets">{''.join(f'<li><strong>{escape(a)}</strong><span>{escape(b)}</span></li>' for a, b in obtienes)}</ul>
      <p class="disclaimer">Estimación orientativa. No es una cotización ni un compromiso de plazo.</p>
    </div>
    <div class="wizard diag-wizard" id="{wid}" data-contacto="{r}contacto/" data-cofin="{r}{COFIN_PAGE}" data-sol="{r}soluciones/finanzas-y-operaciones/">
      <ol class="diag-steps" aria-hidden="true">{steps}</ol>
      <div class="diag-step" aria-live="polite">
        <noscript><p class="lead">Esta herramienta necesita JavaScript. También puedes <a href="{r}contacto/">hablar con un especialista</a>.</p></noscript>
      </div>
    </div>
  </div>
  <script type="application/json" id="{wid}-data">{datos}</script>
</section>'''


def diag_ia(r, h):
    return diag_layout(r, h, 'diag-ia', 'Responde 5 preguntas y obtén una primera lectura de tu punto de partida.',
                       [('Nivel de preparación', 'Dónde estás hoy, de 0 a 10.'),
                        ('Plazo estimado', 'Semanas hasta un primer caso en producción.'),
                        ('Próximo paso', 'Qué resolver primero y por dónde partir.')],
                       DIAG_IA, ''.join(f'<li>{escape(q["tag"])}</li>' for q in DIAG_IA['preguntas']))


def diag_erp(r, h):
    return diag_layout(r, h, 'diag-erp', 'Cuéntanos desde qué rol evalúas el ERP y te hacemos las preguntas que importan para tu área.',
                       [('Recomendación', 'Dynamics 365 Business Central, Finance o evaluar ambos.'),
                        ('Por qué', 'Las razones detrás, según tus respuestas.'),
                        ('Plazo típico', 'Meses de implementación y si calza con tu fecha.')],
                       DIAG_ERP)


def herramienta_page(h):
    def body(r):
        if h['slug'] == 'autodiagnostico-ia':
            return diag_ia(r, h) + cta_final(r)
        if h['slug'] == 'business-central-o-finance':
            return diag_erp(r, h) + cta_final(r)
        return page_hero(r, [('Herramientas', 'herramientas/'), (h['nombre'], f"herramientas/{h['slug']}/")], f"Herramienta · {h['tiempo']}",
                         h['nombre'], escape(h['que']), ctas=False) + f'''
<section class="section bg-soft"><div class="container">
  <div class="wizard">
    <div class="wizard-bar"><span style="width:10%"></span></div>
    <span class="eyebrow">Paso 1</span>
    <h2 class="h2">[placeholder: primera pregunta del wizard]</h2>
    <div class="wizard-opts"><button type="button">Opción A</button><button type="button">Opción B</button><button type="button">Opción C</button></div>
    <p class="disclaimer">Herramienta en construcción. Esto no es una cotización ni asesoría legal.</p>
  </div>
</div></section>
{cta_final(r)}'''
    return body


def como_trabajamos(r):
    principios = [('Entregas cortas', 'Olas, sprints y prototipos: algo usable en producción lo antes posible, no al final.'),
                  ('Usuarios en el equipo', 'Los dueños del proceso participan desde el taller inicial hasta el go-live.'),
                  ('Gobierno desde el inicio', 'Seguridad, datos y IA responsable se diseñan al inicio, no se agregan al final.'),
                  ('Adopción medida', 'Uso real, calidad y valor se miden desde el primer día y guían la siguiente iteración.')]
    principios_html = ''.join(f'<li><span class="pr-n">{k:02d}</span><div><strong>{escape(t)}</strong><p>{escape(d)}</p></div></li>' for k, (t, d) in enumerate(principios, 1))
    marcos = ''.join(f'''<a class="marco" href="#{m['slug']}">
      <span class="marco-top"><span class="marco-n">{k:02d}</span><span class="marco-para">{escape(m['corto'])}</span></span>
      <strong>{escape(m['titulo'].rstrip('.'))}</strong>
      <span class="marco-fases">{' <i>→</i> '.join(escape(f['nombre']) for f in m['fases'])}</span>
    </a>''' for k, m in enumerate(METODOS, 1))
    metodos_html = ''.join(f'''
<section class="section {'bg-blue' if n % 2 == 0 else 'bg-white'}" id="{m['slug']}"><div class="container stack-40">
  {section_head(m['para'], m['titulo'], m['resumen'])}
  {metodo_html(r, m)}
</div></section>''' for n, m in enumerate(METODOS)) + f'''
<section class="section bg-white"><div class="container">{cofin_strip(r)}</div></section>'''
    return page_hero(r, [('Cómo trabajamos', 'como-trabajamos/')], 'Cómo trabajamos', METODO_H2, METODO_LEAD,
                     aside=f'<div class="marcos">{marcos}</div>', cls='metodo-hero') + f'''
<section class="principios-band"><div class="container">
  <ul class="principios">{principios_html}</ul>
</div></section>{metodos_html}
<section class="section bg-white"><div class="container grid grid-2">
  <div class="stack-20"><span class="eyebrow">Ingeniería asistida por IA</span><h2 class="h2">IA en nuestro propio trabajo.</h2>
    <p class="lead">Usamos IA para analizar entornos, redactar diseños, acelerar personalizaciones y probar. El consumo de tokens se transparenta en la propuesta.</p></div>
  <div class="stack-20"><span class="eyebrow">Soporte y AMS</span><h2 class="h2">Soporte después del go-live.</h2>
    <p class="lead">Soporte con SLA, portal de soporte y mejora continua. <span class="ph">[+15.400 HH de soporte, verificar]</span></p></div>
  <div class="stack-20"><span class="eyebrow">Licenciamiento Microsoft</span><h2 class="h2">Licencias Microsoft con un solo proveedor.</h2>
    <p class="lead">CSP como revendedor indirecto. <span class="ph">[+6.000 gestiones de licencias, verificar]</span></p></div>
  <div class="stack-20"><span class="eyebrow">Equipo propio</span><h2 class="h2">Nuestros consultores son de W-IT.</h2>
    <p class="lead">No subcontratamos tu proyecto. <span class="ph">[confirmar que es 100% cierto]</span></p></div>
</div></section>
{cta_final(r)}'''


def nosotros(r):
    hitos = [('2013', 'Nace W-IT, consultora especialista en Microsoft.'), ('2014', 'W-IT se convierte en partner de Microsoft.'),
             ('2019', 'Microsoft Partner of the Year Latinoamérica y el Caribe: Dynamics 365 for Sales.'), ('2020', 'Microsoft Partner of the Year Latinoamérica y el Caribe: Proactive Customer Service.'), ('2023', 'ISO 9001 e ISO 27001 con SGS.'),
             ('2026', 'Solutions Partner for Microsoft Cloud: las seis designaciones Microsoft y especialización Agentic Business Solutions.')]
    tl = ''.join(f'<li><span class="tl-year">{a}</span><p>{escape(b)}</p></li>' for a, b in hitos)
    valores = ['Simpleza y Calidad', 'Confianza y Cercanía', 'Competitividad e Innovación', 'Honestidad y Responsabilidad', 'Respeto y Colaboración']
    return page_hero(r, [('Nosotros', 'nosotros/')], 'Nosotros', 'Consultores especialistas en Microsoft desde 2013.',
                     'Visión: ser la consultora especialista en Microsoft de la región que aporta simpleza y calidad. <span class="ph">[validar redacción]</span>', ctas=False) + f'''
<section class="section bg-white"><div class="container stack-40">
  {section_head('Historia', 'Nuestra trayectoria.')}
  <ol class="timeline">{tl}</ol>
</div></section>
{premios_section(r)}
<section class="section bg-soft"><div class="container stack-40">
  {section_head('Valores', 'Nuestros valores.')}
  <ul class="values">{''.join(f'<li>{v}</li>' for v in valores)}</ul>
</div></section>
<section class="section bg-white"><div class="container grid grid-2">
  <div class="stack-20"><span class="eyebrow">Liderazgo</span><div class="placeholder-box" style="min-height:220px">[placeholder: fotos y cargos del equipo líder]</div></div>
  <div class="stack-20"><span class="eyebrow">Presencia</span><h2 class="h2">Chile y Perú</h2><p class="lead">W-IT SpA, en Av. Apoquindo 3039, Las Condes, Santiago, y W-IT LATAM S.A.C., en Av. Circunvalación del Golf Los Incas 170, Int. 702, Santiago de Surco, Lima.</p></div>
</div></section>
{cta_final(r)}'''


def confianza(r):
    return f'''
<section class="page-hero page-hero-dark">
  <div class="container page-hero-inner"><div class="page-hero-copy">
    <nav aria-label="Ruta"><ol class="crumbs"><li><a href="{r}">Inicio</a></li><li><a href="{r}nosotros/">Nosotros</a></li><li><a href="{r}nosotros/confianza/">Trust Center</a></li></ol></nav>
    <span class="eyebrow">Trust Center</span>
    <h1>Todo lo que declaramos se puede verificar.</h1>
    <p class="lead">Credenciales Microsoft, certificaciones ISO, residencia de datos y principios de IA responsable.</p>
    <div class="btn-row"><a class="btn btn-lg btn-green" href="https://marketplace.microsoft.com/en-us/partners/dcdbe467-cd53-4233-a80c-6c8510c2f60a/overview" target="_blank" rel="noopener">Verifica nuestro perfil en Microsoft ↗</a></div>
  </div></div>
</section>
<section class="section bg-white"><div class="container stack-40">
  {section_head('Microsoft', 'Las seis designaciones Solutions Partner y especialización.')}
  <div class="badge-row">
    <figure>{badge_img(r, 'WIT-MicrosoftCloud-color.png', 120)}<figcaption>Microsoft Cloud · Las seis designaciones Solutions Partner</figcaption></figure>
    <figure>{badge_img(r, 'WIT-AIBusinessSolutions-Agentic-color.png', 150)}<figcaption>AI Business Solutions (Business Applications y Modern Work) · Especialización Agentic Business Solutions</figcaption></figure>
    <figure>{badge_img(r, 'WIT-CloudAIPlatforms-color.png', 120)}<figcaption>Cloud &amp; AI Platforms</figcaption></figure>
    <figure>{badge_img(r, 'WIT-Security-color.png', 120)}<figcaption>Security</figcaption></figure>
  </div>
</div></section>
<section class="section bg-white"><div class="container">{jumpstart_strip(r)}</div></section>
{premios_section(r, fotos=False, bg='bg-blue')}
<section class="section bg-soft"><div class="container grid grid-2 aligned">
  <div class="stack-20"><span class="eyebrow">ISO · SGS</span><h2 class="h2">ISO 9001 e ISO/IEC 27001</h2>
    <p class="lead">Calidad y seguridad de la información, certificadas por SGS. Certificado descargable <span class="ph">[PDF]</span>.</p></div>
  <div class="iso-row"><img src="{r}assets/credenciales/SGS_ISO_9001_round_TCL_LR.jpg" alt="SGS ISO 9001" width="140" height="136"><img src="{r}assets/credenciales/SGS_ISO-IEC_27001_TCL_LR.jpg" alt="SGS ISO/IEC 27001" width="140" height="137"></div>
</div></section>
<section class="section bg-dark"><div class="container stack-40">
  {section_head('Datos e IA', 'Cómo protegemos tu información.')}
  {trust_items()}
  <div class="trust-ley">
    <h3>Protección de datos personales en cada implementación</h3>
    <p>La protección de datos forma parte de nuestra forma de implementar. En cada proyecto consideramos la Ley 21.719 en Chile y la Ley 29733 en Perú: accedemos solo a los datos personales que el proyecto necesita, preferimos ambientes de prueba sin datos reales y acordamos con el cliente los permisos, la retención y la trazabilidad de la solución. Cuando el cliente necesita asesoría legal, la complementamos con <a href="https://www.regulatec.cl" target="_blank" rel="noopener">RegulaTec</a>, empresa legal aliada. <span class="ph">[validar con Legal y con el Encargado de Plataforma y Seguridad]</span></p>
  </div>
  <p class="disclaimer" style="color:rgba(255,255,255,.7)">Encargado de datos <span class="ph">[placeholder]</span>. Certificaciones del equipo: conteo agregado por área <span class="ph">[placeholder]</span>.</p>
</div></section>
{cta_final(r)}'''


def simple_page(eyebrow, h1, bajada, crumbs, contenido):
    def body(r):
        return page_hero(r, crumbs, eyebrow, h1, bajada, ctas=False) + f'''
<section class="section bg-white"><div class="container prose">{contenido}</div></section>
{cta_final(r)}'''
    return body


def contacto(r):
    temas = [(s['slug'], s['corto']) for s in SOLUCIONES] + [('licencias', 'Licencias Microsoft'), ('soporte', 'Soporte')]
    sols = ''.join(f'<label class="chip"><input type="checkbox" name="interes" value="{v}"><span>{escape(t)}</span></label>' for v, t in temas)
    pasos = [('Te respondemos', 'En menos de 1 día hábil, al correo que nos dejes.'),
             ('Te conectamos con un especialista', 'Del área que te interesa, en una reunión breve si hace falta.'),
             ('Te proponemos un camino', 'Un primer enfoque, plazos típicos y si aplica cofinanciamiento de Microsoft.')]
    req = '<abbr class="req" title="obligatorio">*</abbr>'
    return f'''
<section class="page-hero contact-hero">
  <div class="page-hero-trazo" aria-hidden="true"></div>
  <div class="container contact-layout">
    <div class="contact-intro">
      <nav aria-label="Ruta"><ol class="crumbs"><li><a href="{r}">Inicio</a></li><li><a href="{r}contacto/">Contacto</a></li></ol></nav>
      <span class="eyebrow">Contacto</span>
      <h1>Cuéntanos qué necesitas.</h1>
      <p class="lead">Un proyecto nuevo, licencias, soporte o una consulta: te respondemos en menos de 1 día hábil.</p>
      <ol class="contact-pasos">{''.join(f'<li><strong>{escape(a)}</strong><span>{escape(b)}</span></li>' for a, b in pasos)}</ol>
      <div class="contact-cards">
        <div class="contact-card"><span class="contact-pais"><img class="flag" src="{r}assets/img/chile.svg" alt="" width="21" height="14">Chile · W-IT SpA</span><span>Av. Apoquindo 3039, Las Condes, Santiago</span></div>
        <div class="contact-card"><span class="contact-pais"><img class="flag" src="{r}assets/img/peru.svg" alt="" width="21" height="14">Perú · W-IT LATAM S.A.C.</span><span>Av. Circunvalación del Golf Los Incas 170, Int. 702, Santiago de Surco, Lima</span></div>
        <div class="contact-card contact-card-links"><a href="tel:+56224096112">+56 2 2409 6112</a><a href="mailto:info@w-it.cl">info@w-it.cl</a></div>
      </div>
    </div>
    <form class="form contact-form" id="form-contacto" novalidate>
      <div class="form-head"><strong>Escríbenos</strong><span>Los campos con {req} son obligatorios.</span></div>
      <div class="form-row"><label><span>Nombre {req}</span><input name="nombre" required autocomplete="name" placeholder="Nombre y apellido"></label><label><span>Email corporativo {req}</span><input type="email" name="email" required autocomplete="email" placeholder="nombre@empresa.cl"></label></div>
      <div class="form-row"><label>Empresa<input name="empresa" autocomplete="organization"></label><label>Cargo<input name="cargo" autocomplete="organization-title"></label></div>
      <div class="form-row form-row-3"><label>Teléfono<input type="tel" name="telefono" autocomplete="tel" placeholder="+56 9"></label>
        <label>País<select name="pais"><option>Chile</option><option>Perú</option><option>Otro</option></select></label>
        <label>Tamaño<select name="tamano"><option>Menos de 200 personas</option><option>200 a 1.000</option><option>Más de 1.000</option></select></label></div>
      <fieldset><legend>¿Qué te interesa?</legend><div class="chips">{sols}</div></fieldset>
      <label>Mensaje<textarea name="mensaje" rows="3" placeholder="Cuéntanos brevemente tu consulta"></textarea></label>
      <label class="check"><input type="checkbox" name="consentimiento" required> <span>Acepto la <a href="{r}privacidad/">política de privacidad</a> y el tratamiento de mis datos para responder esta solicitud. {req}</span></label>
      <!-- Contexto para el CRM: lo completa main.js según desde dónde llegó la persona; no se muestra en pantalla -->
      <input type="hidden" name="origen_pagina">
      <input type="hidden" name="origen_cta">
      <input type="hidden" name="diagnostico_herramienta">
      <input type="hidden" name="diagnostico_resultado">
      <input type="hidden" name="diagnostico_detalle">
      <input type="hidden" name="utm">
      <button class="btn btn-lg btn-primary" type="submit">Enviar solicitud</button>
      <p class="form-msg" role="status" hidden>Formulario de demostración: aún no está conectado. <span class="ph">[conectar a Dynamics 365 y registrar el consentimiento]</span></p>
    </form>
  </div>
</section>'''



def jumpstart_page(r):
    """Página propia del programa Microsoft Copilot Jumpstart (fuente: propuesta comercial W-IT, láminas 7 y 8)."""
    beneficios = [
        ('Talleres y pilotos con apoyo de Microsoft', 'Evaluaciones, talleres y pilotos que pueden contar con financiamiento de Microsoft, según la elegibilidad de cada organización.'),
        ('Seguridad y gobierno primero', 'Revisamos permisos, protección de la información y cumplimiento antes de encender Copilot o un agente.'),
        ('Casos de uso con valor de negocio', 'Priorizamos procesos donde la IA ahorra tiempo o mejora decisiones, y descartamos los que no lo justifican.'),
        ('Adopción medida', 'Gestión del cambio y capacitación, con medición del uso real después del despliegue.'),
        ('Coordinación directa con Microsoft', 'Como partner Ready Tier gestionamos junto a Microsoft los recursos del programa para tu proyecto.'),
    ]
    pasos = [
        ('Evaluación de preparación', 'Datos, licencias, seguridad y procesos candidatos.'),
        ('Taller de casos de uso', 'Priorización con las áreas de negocio y definición de métricas.'),
        ('Piloto', 'Copilot o un agente funcionando con usuarios reales y datos reales.'),
        ('Despliegue y adopción', 'Escalamiento gobernado, capacitación y gestión del cambio.'),
        ('Medición y mejora', 'Uso, impacto y siguientes casos de uso.'),
    ]
    faq = [
        ('¿Mi organización califica para el financiamiento?', 'La elegibilidad y los montos los define Microsoft para cada cliente y proyecto. En la evaluación inicial revisamos tu caso y te decimos qué aplica. [validar criterios con Comercial]'),
        ('¿Qué es la asociación CPOR / PAL?', 'Es el mecanismo con que Microsoft reconoce la participación de W-IT en tu proyecto: CPOR para soluciones como Microsoft 365, Dynamics 365 y Power Platform, y PAL para suscripciones de Azure. Habilita los beneficios del programa, incluido el financiamiento.'),
        ('¿Tiene costo asociar a W-IT como partner?', 'No. La asociación no tiene costo, no implica contrato ni compromiso comercial adicional, y la configura tu equipo con nuestro apoyo.'),
        ('¿Reemplaza a mi partner actual?', 'No. La asociación es exclusiva para el proyecto y no reemplaza ni invalida a otros partners que ya trabajen con tu organización.'),
        ('¿Qué tecnologías cubre?', 'Copilot y agentes de IA en el ecosistema Microsoft: Microsoft 365 Copilot, Copilot Studio y agentes sobre Dynamics 365, Power Platform y Azure.'),
    ]
    faq_html = ''.join(
        f'<div class="faq-item"><h3><button type="button" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="faq-{i}">{escape(q)}</button></h3>'
        f'<p id="faq-{i}"{"" if i == 0 else " hidden"}>{escape(a)}</p></div>' for i, (q, a) in enumerate(faq))
    prods = ''.join(f'<span class="hero-prod">{ms_icon(r, i, 36)}<span>{escape(MS[i])}</span></span>' for i in ('m365-copilot', 'copilot-studio', 'agent-365'))
    aside = f"""<div class="page-hero-aside js-aside">
      <div class="js-badge"><img class="ms-icon" src="{r}assets/ms/m365-copilot.svg" alt="" width="64" height="64"><span class="js-tier">Ready Tier</span><strong>Microsoft Copilot Jumpstart Partner</strong><span>Copilot &amp; Agents at Work · FY26</span></div>
      {prods}
    </div>"""
    beneficios_html = ''.join(f'<div class="signal"><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for t, d in beneficios)
    pasos_html = ''.join(f'<li><span class="flow-n">{n}</span><strong>{escape(t)}</strong><span>{escape(d)}</span></li>' for n, (t, d) in enumerate(pasos, 1))
    return page_hero(r, [('Nosotros', 'nosotros/'), ('Microsoft Copilot Jumpstart', JUMPSTART_PAGE)],
                     'Programa Microsoft Copilot Jumpstart · Ready Tier',
                     'De la prueba a resultados con Copilot y agentes, con el respaldo de Microsoft.',
                     'W-IT es partner Ready Tier del programa oficial de Microsoft para acelerar la adopción de IA con Copilot y agentes. Te acompañamos desde la evaluación hasta la implementación, con acceso a talleres y engagements financiados por Microsoft.',
                     aside=aside) + f"""
<section class="section bg-white"><div class="container grid grid-2 aligned">
  <div class="stack-20">
    <span class="eyebrow">Qué es el programa</span>
    <h2 class="h2">Una iniciativa de Microsoft para adoptar IA con método.</h2>
    <p class="lead">El Microsoft Copilot Jumpstart Program entrega recursos, talleres y financiamiento para que las organizaciones evalúen, planifiquen e implementen Copilot y agentes de IA con éxito, trabajando con partners validados por Microsoft.</p>
  </div>
  <div class="stack-20">
    <span class="eyebrow">Qué significa ser Ready Tier</span>
    <ul class="checks">
      <li>Reconocimiento de Microsoft a nuestra experiencia técnica en IA con Copilot.</li>
      <li>Acceso a talleres y engagements financiados por Microsoft para nuestros clientes.</li>
      <li>Acompañamiento experto desde la evaluación hasta la implementación.</li>
    </ul>
    <p class="disclaimer">W-IT avanzó del nivel Community al Ready Tier en la iniciativa FY26 Copilot &amp; Agents at Work Jumpstart.</p>
  </div>
</div></section>
<section class="section bg-soft"><div class="container stack-40">
  {section_head('Qué gana tu organización', 'De la evaluación a la puesta en producción.')}
  <div class="signals signals-5">{beneficios_html}</div>
</div></section>
<section class="section bg-blue"><div class="container stack-40">
  {section_head('Cómo lo trabajamos', 'Cinco pasos, de la evaluación a la medición.')}
  <ol class="flow">{pasos_html}</ol>
</div></section>
<section class="section bg-white"><div class="container grid grid-2 cta-grid">
  <div class="cta">
    <h2 class="h2">¿Tu organización puede aprovechar el programa?</h2>
    <p class="lead">Agenda una evaluación de 30 minutos. Revisamos tu escenario, los casos de uso candidatos y qué beneficios del programa pueden aplicar.</p>
    <div class="btn-row"><a class="btn btn-lg btn-primary" href="{r}contacto/">Agenda una evaluación</a><a class="btn btn-lg btn-outline" href="{r}soluciones/ia-y-agentes/">IA y agentes</a></div>
    <a class="link-strong" href="{COPILOT_URL}" target="_blank" rel="noopener">Más sobre Microsoft 365 Copilot en microsoft.com ↗</a>
  </div>
  <div class="faq" id="faq"><span class="eyebrow">Preguntas frecuentes</span>{faq_html}</div>
</div></section>
<section class="section bg-soft js-legal"><div class="container"><p class="disclaimer">La elegibilidad, los montos y las condiciones del programa los define Microsoft y pueden cambiar. Esta página no constituye una oferta ni una cotización.</p></div></section>
{cta_final(r)}"""



def aprende_page(r):
    """Nosotros > Aprende: explica WITEDUCA y redirige a witeduca.cl (fuente: witeduca.cl)."""
    programas = [
        ('Adopción Garantizada', 'Programa ancla para elevar el uso real de Copilot, Dynamics 365 y Power Platform.'),
        ('Nivelación Tecnológica', 'Formación por dotación, con diagnóstico de brechas y medición antes y después.'),
        ('Formación In-Company', 'Cursos cerrados en Copilot, Power Platform, Dynamics 365 e IA para líderes.'),
        ('Cursos Abiertos', 'Jornadas sobre Copilot e IA aplicada.'),
        ('Certificaciones Claude', 'Preparación para las certificaciones de Anthropic: Associate, Developer y Architect.'),
        ('Asesorías en IA', 'Diagnóstico de madurez, gobernanza y acompañamiento en cumplimiento normativo.'),
        ('Construcción de Agentes', 'Diseño de agentes de IA conectados a los datos y sistemas de la organización.'),
    ]
    enfoque = [
        'Ejercicios sobre tus propios documentos, procesos y plataforma, no sobre un demo de laboratorio.',
        'Medición real: diagnóstico previo, evaluación antes y después, y uso efectivo en telemetría.',
        'Refuerzo a 90 días para que el cambio no se diluya.',
        'Formación sobre el mismo stack que W-IT implementa en proyectos reales.',
    ]
    prog_html = ''.join(f'<div class="signal"><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for t, d in programas)
    enf_html = ''.join(f'<li>{escape(e)}</li>' for e in enfoque)
    aside = """<div class="page-hero-aside"><div class="edu-card">
      <span class="edu-name">WITEDUCA</span>
      <span class="edu-tag">Aprende IA con quienes la implementan</span>
      <a class="btn btn-green" href="https://witeduca.cl" target="_blank" rel="noopener">Ir a witeduca.cl ↗</a>
    </div></div>"""
    return page_hero(r, [('Nosotros', 'nosotros/'), ('Aprende', 'nosotros/aprende/')], 'Nosotros · Aprende',
                     'Formación y adopción, con una unidad dedicada.',
                     'WITEDUCA es la unidad de W-IT dedicada exclusivamente a la formación y adopción de IA y tecnologías Microsoft. Nació de nuestros proyectos: la tecnología solo genera valor cuando las personas la usan bien.',
                     ctas=False, aside=aside,
                     extra='<div class="btn-row" style="margin-top:8px"><a class="btn btn-lg btn-primary" href="https://witeduca.cl" target="_blank" rel="noopener">Conoce WITEDUCA ↗</a><a class="btn btn-lg btn-outline" href="https://witeduca.cl/oferta/" target="_blank" rel="noopener">Ver la oferta completa ↗</a></div>') + f"""
<section class="section bg-white"><div class="container grid grid-2 aligned">
  <div class="stack-20">
    <span class="eyebrow">Para quién</span>
    <h2 class="h2">Para organizaciones y para personas.</h2>
    <p class="lead"><strong>Organizaciones</strong> que ya usan IA y necesitan que sus equipos la adopten y la usen bien. <strong>Personas</strong> que deben tomar decisiones sobre IA y quieren formar criterio propio.</p>
  </div>
  <div class="stack-20">
    <span class="eyebrow">Cómo enseña</span>
    <ul class="checks">{enf_html}</ul>
  </div>
</div></section>
<section class="section bg-soft"><div class="container stack-40">
  {section_head('Programas', 'Siete formas de aprender y adoptar.', link='<a class="link-strong" href="https://witeduca.cl/oferta/" target="_blank" rel="noopener">Ver la oferta en witeduca.cl ↗</a>')}
  <div class="signals">{prog_html}</div>
  <p class="disclaimer">Formatos presenciales e in-company, cursos abiertos de una jornada y rutas de certificación en vivo y en español.</p>
</div></section>
<section class="cta-band">
  <div class="container cta-band-inner">
    <div><h2>Conversemos sobre tu organización.</h2><p>Los programas, fechas e inscripciones se gestionan en el sitio de WITEDUCA.</p></div>
    <div class="btn-row"><a class="btn btn-lg btn-green" href="https://witeduca.cl" target="_blank" rel="noopener">Ir a witeduca.cl ↗</a></div>
  </div>
</section>"""



def privacidad_page(r):
    """Aviso de privacidad: copia del de witeduca.cl/privacidad/ (11-09-2026), con las referencias propias de WITEDUCA adaptadas a W-IT."""
    proveedores = [
        ('Microsoft Dynamics 365', 'Es nuestro CRM: ahí queda tu consulta para que el equipo comercial la atienda', 'Todo lo que enviaste en el formulario'),
        ('Microsoft Azure', 'Aloja este sitio y procesa el envío del formulario', 'El envío, en tránsito'),
        ('Cloudflare (Turnstile y Web Analytics)', 'Verifica que quien envía el formulario es una persona, y cuenta las visitas al sitio', 'Señales técnicas de tu navegador, tu IP y la página visitada. No recibe lo que escribiste ni te identifica'),
        ('Google Ads', 'Nos dice si quien envió el formulario llegó desde uno de nuestros avisos, para no gastar en avisos que no sirven', 'Que hubo un envío de formulario y desde qué aviso, mediante la cookie _gcl_au. No recibe tu nombre, tu correo ni lo que escribiste'),
    ]
    filas = ''.join(f'<tr><th scope="row">{escape(a)}</th><td>{escape(b)}</td><td>{escape(c)}</td></tr>' for a, b, c in proveedores)
    mail = '<a href="mailto:info@w-it.cl">info@w-it.cl</a>'
    return f"""
<section class="page-hero">
  <div class="page-hero-trazo" aria-hidden="true"></div>
  <div class="container page-hero-inner">
    <div class="page-hero-copy">
      <nav aria-label="Ruta"><ol class="crumbs"><li><a href="{r}">Inicio</a></li><li><a href="{r}privacidad/">Privacidad</a></li></ol></nav>
      <span class="eyebrow">Legal</span>
      <h1>Aviso de privacidad y tratamiento de datos</h1>
      <p class="lead">Qué datos recolectamos en este sitio, para qué los usamos, con quién los compartimos y cómo puedes controlarlos.</p>
      <p class="disclaimer">Última actualización: 11 de septiembre de 2026</p>
    </div>
  </div>
</section>
<section class="section bg-white"><div class="container legal">

  <h2>Quién es responsable de tus datos</h2>
  <p>El responsable es W-IT SpA, con domicilio en Apoquindo 3039, Las Condes, Santiago de Chile.</p>
  <p>Para cualquier consulta sobre tus datos, escribe a {mail}.</p>

  <h2>Qué datos recolectamos</h2>
  <p>Medimos cuánta gente visita el sitio con Cloudflare Web Analytics, que no usa cookies ni identifica personas: cuenta páginas vistas, país aproximado, tipo de dispositivo y desde qué sitio llegaste. Datos personales solo recolectamos cuando tú decides enviarnos un formulario.</p>
  <p>Además, este sitio usa una cookie publicitaria de Google Ads (_gcl_au). Su único fin es saber si quien nos escribió por el formulario llegó desde un aviso nuestro en Google, y así no seguir pagando por avisos que no funcionan. No la usamos para mostrarte publicidad en otros sitios ni para armar un perfil tuyo. Si prefieres evitarla, puedes bloquear las cookies de terceros en tu navegador: el sitio y el formulario funcionan igual.</p>
  <h3>Los que tú escribes en el formulario:</h3>
  <ul class="legal-list">
    <li>Nombre y correo electrónico. Son los únicos obligatorios.</li>
    <li>Empresa u organización, cargo, teléfono, país, tamaño de tu organización y temas de interés, si decides completarlos.</li>
    <li>El mensaje que nos escribas, si escribes uno.</li>
  </ul>
  <h3>Los que el sitio registra junto a tu envío:</h3>
  <ul class="legal-list">
    <li>La página desde la que enviaste el formulario, incluidos los parámetros de campaña si llegaste por un enlace de marketing.</li>
    <li>La página y el botón del sitio desde los que llegaste al formulario.</li>
    <li>Si antes usaste uno de nuestros autodiagnósticos, sus respuestas y el resultado, para que el especialista llegue a la reunión con ese contexto.</li>
    <li>La dirección web desde la que llegaste a nuestro sitio, si venías de otra.</li>
    <li>Tu dirección IP, que se usa de forma temporal y solo para limitar envíos masivos automatizados. No se guarda junto a tu registro.</li>
  </ul>

  <h2>Para qué los usamos</h2>
  <p>Para responder tu consulta y hacerte seguimiento comercial sobre lo que nos preguntaste: cotizarte un proyecto, coordinar una reunión o enviarte la información que pediste.</p>
  <p>No usamos tus datos para otra cosa. No los vendemos, no los cedemos a terceros con fines comerciales y no te vamos a inscribir en una lista de correos por haber enviado un formulario.</p>
  <p>La base que nos habilita a tratarlos es tu propio envío del formulario: tú nos entregas los datos con el fin explícito de que te contactemos.</p>

  <h2>Con quién los compartimos</h2>
  <p>Con cuatro proveedores de tecnología, cada uno para una función específica. Ninguno los usa para fines propios.</p>
  <div class="legal-table-wrap"><table class="legal-table">
    <caption>Proveedores que procesan datos de este sitio y para qué.</caption>
    <thead><tr><th scope="col">Proveedor</th><th scope="col">Para qué</th><th scope="col">Qué recibe</th></tr></thead>
    <tbody>{filas}</tbody>
  </table></div>
  <p>Elegimos Turnstile en vez de otras herramientas de verificación precisamente porque no perfila a los visitantes para publicidad.</p>
  <p>Estos servicios operan en infraestructura global, por lo que tus datos pueden procesarse y almacenarse fuera de Chile, bajo los compromisos contractuales de protección de datos de cada proveedor.</p>

  <h2>Cuánto tiempo los conservamos</h2>
  <p>Mantenemos tu consulta en nuestro CRM mientras siga vigente la relación comercial o el interés que la originó, y hasta que nos pidas eliminarla.</p>
  <p>Si nos escribiste y decidiste no seguir adelante, puedes pedirnos que borremos tus datos en cualquier momento y no necesitas darnos una razón.</p>

  <h2>Tus derechos</h2>
  <p>Sobre los datos que tenemos tuyos, puedes pedirnos:</p>
  <ul class="checks">
    <li>Acceder a ellos y saber qué tenemos y de dónde salió.</li>
    <li>Corregirlos si están equivocados o incompletos.</li>
    <li>Eliminarlos.</li>
    <li>Oponerte a que los sigamos usando para contacto comercial.</li>
    <li>Una copia de lo que nos entregaste, en un formato que puedas reutilizar.</li>
  </ul>
  <p>Escribe a {mail} indicando qué necesitas. Te respondemos al mismo correo desde el que nos escribas, y si es otro te vamos a pedir cómo verificar que los datos son tuyos, para no entregárselos a quien no corresponde.</p>

  <h2>Cambios a este aviso</h2>
  <p>Si cambiamos cómo tratamos los datos, actualizamos este aviso y la fecha del encabezado. Si el cambio es relevante para quienes ya nos escribieron, se los avisamos por correo.</p>

  <h2>¿Algo no te calza?</h2>
  <p>Si crees que estamos tratando tus datos de una forma que no corresponde, escríbenos primero a {mail}: es lo más rápido para resolverlo. También puedes recurrir a la autoridad de protección de datos que corresponda.</p>

</div></section>"""


# ---------------------------------------------------------------- build

def main():
    pages = []
    pages.append(write('', 'W-IT · Partner Microsoft Dynamics 365, Power Platform, Azure y Copilot en Chile y Perú',
                       'Solutions Partner for Microsoft Cloud, con las seis designaciones Microsoft, en Chile y Perú. Implementamos Dynamics 365, Power Platform, Azure y agentes de IA.', home, solid=False))
    pages.append(write('soluciones/', 'Soluciones Microsoft Dynamics 365, Power Platform, Azure y Copilot · W-IT', 'Partner Microsoft en Chile y Perú: implementamos Dynamics 365, Power Platform, Azure y Copilot.', soluciones_index, 'soluciones'))
    for s in SOLUCIONES:
        pages.append(write(f"soluciones/{s['slug']}/", f"{s['plataforma']}: {s['nombre'].lower()} · W-IT Chile", f"{s['plataforma']}. {s['linea']}", solucion_page(s), 'soluciones'))
    pages.append(write('industrias/', 'Clientes por industria · W-IT', 'Clientes de W-IT por industria.', industrias_index, 'industrias'))
    for i in INDUSTRIAS:
        pages.append(write(f"industrias/{i['slug']}/", f"{i['nombre']} · W-IT", i['h1'], industria_page(i), 'industrias'))
    # Casos de éxito fuera del sitio (2026-10-01): la información se reserva para reuniones comerciales.
    # Los datos siguen en content.py (CASOS) y casos_index/caso_page quedan sin uso.
    pages.append(write('productos/', 'Productos · W-IT', 'Productos W-IT en Microsoft Marketplace.', productos_index, 'productos'))
    pages.append(write('productos/agentes-w-it/', 'Agentes W-IT', 'Agentes y aceleradores de W-IT.', agentes, 'productos'))
    pages.append(write('herramientas/', 'Herramientas · W-IT', 'Herramientas gratuitas de W-IT.', herramientas_index, 'diagnosticos'))
    for h in HERRAMIENTAS:
        pages.append(write(f"herramientas/{h['slug']}/", f"{h['nombre']} · W-IT", h['que'], herramienta_page(h), 'diagnosticos'))
    pages.append(write('como-trabajamos/', 'Cómo trabajamos · W-IT', 'Cuatro metodologías ágiles sobre marcos probados de Microsoft.', como_trabajamos, 'metodo'))
    pages.append(write(COFIN_PAGE, 'Cofinanciamiento Microsoft: POC y MVP · W-IT', 'Programas de inversión de Microsoft que cofinancian talleres, pruebas de concepto (POC) y productos mínimos viables (MVP) con W-IT. Evaluamos tu elegibilidad.', cofinanciamiento, 'metodo'))
    pages.append(write('nosotros/', 'Nosotros · W-IT', 'Historia, valores y equipo de W-IT.', nosotros, 'nosotros'))
    pages.append(write(JUMPSTART_PAGE, 'Microsoft Copilot Jumpstart Partner · Ready Tier · W-IT', 'W-IT es partner Ready Tier del programa Microsoft Copilot Jumpstart: talleres y engagements financiados por Microsoft para adoptar Copilot y agentes.', jumpstart_page, 'nosotros'))
    pages.append(write('nosotros/aprende/', 'Aprende: formación y adopción de IA con WITEDUCA · W-IT', 'WITEDUCA es la unidad de W-IT dedicada exclusivamente a la formación y adopción de IA y tecnologías Microsoft.', aprende_page, 'nosotros'))
    pages.append(write('nosotros/confianza/', 'Trust Center · W-IT', 'Credenciales verificables de W-IT.', confianza, 'nosotros'))
    pages.append(write('nosotros/equipo/', 'Equipo · W-IT', 'Equipo W-IT.', simple_page('Nosotros · Equipo', 'Consultores propios y certificados.', 'Conteo agregado de certificaciones por área, sin nombres. <span class="ph">[placeholder]</span>', [('Nosotros', 'nosotros/'), ('Equipo', 'nosotros/equipo/')], '<div class="placeholder-box" style="min-height:260px">[placeholder: equipo líder y certificaciones por área]</div>'), 'nosotros'))
    pages.append(write('nosotros/trabaja-con-nosotros/', 'Trabaja con nosotros · W-IT', 'Empleos en W-IT.', simple_page('Nosotros · Talento', 'Trabaja con nosotros.', 'Certificaciones pagadas, proyectos enterprise e IA en el día a día. <span class="ph">[validar]</span>', [('Nosotros', 'nosotros/'), ('Trabaja con nosotros', 'nosotros/trabaja-con-nosotros/')], '<p class="lead">Vacantes publicadas en LinkedIn o ATS. <span class="ph">[placeholder: enlace]</span></p><div class="placeholder-box" style="min-height:220px">[placeholder: fotos reales y testimonios internos]</div>'), 'nosotros'))
    pages.append(write('recursos/', 'Recursos · W-IT', 'Observatorio IA, guías y eventos.', simple_page('Recursos', 'Análisis y guías sobre IA en Chile y Perú.', 'Observatorio IA Chile/Perú, guías descargables y eventos.', [('Recursos', 'recursos/')], '{recursos}'), 'nosotros'))
    pages.append(write('contacto/', 'Contacto · W-IT', 'Contacta a W-IT: proyectos, licencias y soporte Microsoft en Chile y Perú.', contacto))
    pages.append(write('privacidad/', 'Aviso de privacidad y tratamiento de datos · W-IT', 'Qué datos recolectamos en w-it.cl, para qué los usamos, con quién los compartimos y cómo puedes controlarlos.', privacidad_page))
    for slug, t in [('cookies', 'Política de cookies'), ('terminos', 'Términos de uso')]:
        pages.append(write(f'{slug}/', f'{t} · W-IT', t, simple_page('Legal', t, 'Documento en redacción.', [(t, f'{slug}/')], '<p class="lead">[Redacción por Administración y Finanzas]</p>')))
    # recursos: grilla real
    p = os.path.join(ROOT, 'recursos', 'index.html')
    s = open(p, encoding='utf-8').read().replace('{recursos}', recursos_grid('../'))
    open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print(f'{len(pages)} páginas generadas')
    check_css()


def check_css():
    """Avisa si alguna clase usada en el HTML generado no tiene reglas en styles.css."""
    import glob, re
    css = open(os.path.join(ROOT, 'styles.css'), encoding='utf-8').read()
    defined = set(re.findall(r'\.([a-zA-Z][\w-]*)', re.sub(r'url\([^)]*\)', '', css)))
    used = set()
    for f in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True):
        for cl in re.findall(r'class="([^"]+)"', open(f, encoding='utf-8').read()):
            used.update(cl.split())
    missing = sorted(used - defined - {'is-solid-page'})
    if missing:
        print('AVISO: clases sin estilos en styles.css ->', ' '.join(missing))
    else:
        print('CSS: todas las clases usadas tienen estilos')


if __name__ == '__main__':
    main()
