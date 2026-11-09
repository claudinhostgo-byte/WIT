"""Versión en inglés del sitio (/en/).

El generador escribe cada página del núcleo dos veces: en español (como siempre) y en inglés bajo /en/.
La traducción se aplica sobre el HTML ya generado: cada texto visible (nodos de texto, alt, title, aria-label,
placeholder, meta description y JSON-LD) se busca en el diccionario EN de i18n_en.py (español → inglés).
Lo que no tiene traducción queda en español y se anota en i18n_faltan.txt para completarlo.

Reglas:
- El HTML en español no pasa por aquí: nada de lo que hoy reciben los avisos de Google Ads cambia.
- Los enlaces a páginas que existen en inglés se reescriben a /en/...; el resto sigue apuntando al español.
- Nunca se redirige por idioma del navegador: el cambio es solo con el selector del encabezado.
"""
import json
import os
import re
from html import escape, unescape

LANG = 'es'          # idioma de la página que se está generando (lo fija build.write)
EN_PAGES = set()     # rutas (sin /en/) que tienen versión en inglés (las fija build.py)
_FALTAN = {}         # texto en español -> páginas donde aparece sin traducción

try:
    from i18n_en import EN
except ImportError:   # primer build sin diccionario
    EN = {}

ATTRS = ('alt', 'title', 'aria-label', 'placeholder', 'data-mapa-titulo')
_SKIP_TAGS = ('script', 'style')
_TXT_RE = re.compile(r'(<[^>]+>)')
_ATTR_RE = re.compile(r'(\s(?:%s)=")([^"]*)(")' % '|'.join(re.escape(a) for a in ATTRS))
_META_RE = re.compile(r'(<meta name="description" content=")([^"]*)(")')
_LD_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def en():
    return LANG == 'en'


def clave(texto):
    return ' '.join(unescape(texto).split())


def t(texto, pagina=''):
    """Traduce un texto plano (sin HTML). Si falta, lo anota y devuelve el original."""
    k = clave(texto)
    if not k or not re.search(r'[A-Za-zÁÉÍÓÚáéíóúÑñ]', k):
        return texto
    if k in EN:
        return EN[k]
    _FALTAN.setdefault(k, set()).add(pagina)
    return texto


def _texto(tok, pagina):
    """Nodo de texto del HTML: conserva el espacio alrededor y las entidades."""
    core = tok.strip()
    if not core:
        return tok
    ini = tok[:len(tok) - len(tok.lstrip())]
    fin = tok[len(tok.rstrip()):]
    k = clave(core)
    if not re.search(r'[A-Za-zÁÉÍÓÚáéíóúÑñ]', k):
        return tok
    if k in EN:
        return ini + escape(EN[k], quote=False) + fin
    _FALTAN.setdefault(k, set()).add(pagina)
    return tok


def _attrs(tag, pagina):
    def rep(m):
        return m.group(1) + escape(t(unescape(m.group(2)), pagina), quote=True) + m.group(3)
    tag = _ATTR_RE.sub(rep, tag)
    tag = _META_RE.sub(rep, tag)
    return tag


def _enlaces(tag, r, path):
    """href="{r}pagina/" -> href="{r}en/pagina/" cuando la página existe en inglés."""
    if not tag.startswith('<a ') or 'data-nolang' in tag:
        return tag
    def rep(m):
        p = m.group(2)
        if p in EN_PAGES:
            return f'{m.group(1)}{r}en/{p}{m.group(3) or ""}"'
        return m.group(0)
    return re.sub(r'(href=")' + re.escape(r) + r'([^"#?]*)([#?][^"]*)?"', rep, tag)


_LD_FIJAS = {'@type', '@context', '@id', 'addressCountry', 'foundingDate', 'email', 'telephone', 'url', 'logo', 'sameAs', 'legalName'}


def _ld(texto, pagina, sitio_url):
    def walk(v):
        if isinstance(v, dict):
            return {k: ('en' if k == 'inLanguage' else x if k in _LD_FIJAS else walk(x)) for k, x in v.items()}
        if isinstance(v, list):
            return [walk(x) for x in v]
        if isinstance(v, str):
            if v.startswith(sitio_url):
                p = v[len(sitio_url):]
                return sitio_url + 'en/' + p if p in EN_PAGES else v
            if v.startswith(('http', '+', '#')) or '@' in v or re.fullmatch(r'[\d.\-/ ]+', v):
                return v
            return t(v, pagina)
        return v
    return json.dumps(walk(json.loads(texto)), ensure_ascii=False)


def translate_html(html, r, path, sitio_url):
    """Traduce el HTML completo de una página generada en español."""
    pagina = path or 'inicio'
    html = _LD_RE.sub(lambda m: m.group(1) + _ld(m.group(2), pagina, sitio_url) + m.group(3), html)
    out = []
    skip = None
    for tok in _TXT_RE.split(html):
        if not tok:
            continue
        if tok.startswith('<'):
            low = tok[:12].lower()
            if skip:
                if low.startswith(f'</{skip}'):
                    skip = None
                out.append(tok)
                continue
            for s in _SKIP_TAGS:
                if low.startswith(f'<{s}') and not tok.endswith('/>'):
                    skip = s
            if not tok.startswith('<!'):
                tok = _enlaces(_attrs(tok, pagina), r, path)
            out.append(tok)
        else:
            out.append(tok if skip else _texto(tok, pagina))
    return ''.join(out)


def informe(ruta):
    """Escribe los textos sin traducir, agrupados por página, y devuelve cuántos son."""
    if not _FALTAN:
        if os.path.exists(ruta):
            os.remove(ruta)
        return 0
    por_pagina = {}
    for k, pags in _FALTAN.items():
        por_pagina.setdefault(sorted(pags)[0], []).append(k)
    with open(ruta, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# Textos sin traducción al inglés: {len(_FALTAN)} (se muestran en la primera página donde aparecen)\n')
        for pag in sorted(por_pagina):
            f.write(f'\n## {pag}\n')
            for k in por_pagina[pag]:
                f.write(f'{k!r}: {""!r},\n')
    return len(_FALTAN)
