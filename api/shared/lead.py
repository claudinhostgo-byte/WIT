"""Formulario de contacto del sitio → Lead en Dynamics 365 (Dataverse Web API).

Sin dependencias externas para poder probarlo fuera de Azure Functions.
Configuración por variables de entorno (Static Web Apps > Configuración):

  DATAVERSE_URL           https://<org>.crm2.dynamics.com
  DATAVERSE_TENANT_ID     id del tenant de Entra ID
  DATAVERSE_CLIENT_ID     id del App Registration
  DATAVERSE_CLIENT_SECRET secreto del App Registration
  DATAVERSE_OWNER_TEAM_ID (opcional) equipo dueño de los leads, p. ej. Comercial
  LEAD_SOURCE_CODE        (opcional) valor de "Origen del cliente potencial"; 8 = Web
  POLITICA_VERSION        (opcional) versión de la política de privacidad aceptada
  CRM_PREFIJO             (opcional) prefijo de las columnas propias del Lead; wit_ por defecto
  ALLOWED_ORIGINS         (opcional) orígenes permitidos, separados por coma
  TURNSTILE_SECRET        clave secreta de Cloudflare Turnstile (captcha); sin ella no se exige
  AVISO_LEAD_DESTINO      (opcional) a quién avisar de cada lead nuevo (con los datos del formulario);
                          comercial@w-it.cl por defecto
                          (se envía con Graph desde POSTULACIONES_REMITENTE, ver postulacion.py)
"""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html import escape

# Mismos valores que los chips del formulario (build.py)
INTERESES = {
    'ia-y-agentes': 'IA y agentes',
    'ventas-servicio-y-contact-center': 'Ventas y servicio',
    'contact-center': 'Contact center',
    'finanzas-y-operaciones': 'Finanzas y operaciones',
    'datos-y-analitica': 'Datos y analítica',
    'automatizacion-y-apps': 'Automatización y apps',
    'nube-azure-e-infraestructura': 'Nube Azure',
    'seguridad-y-cumplimiento': 'Seguridad e identidades',
    'licencias': 'Licencias Microsoft',
    'soporte': 'Soporte',
}
PAISES = {'Chile', 'Perú', 'Otro'}

# Valores de las columnas de opción del Lead (ver infra/DESPLIEGUE.md); deben calzar con Dataverse
SITIO_WIT = 100000000                      # wit_sitioorigen: 100000001 es WITEDUCA
OPCION_INTERES = {slug: 100000000 + n for n, slug in enumerate(INTERESES)}   # wit_intereseswit
TAMANOS = {                                # wit_tamanoorganizacion (100000000-100000002 son de WITEDUCA)
    'Menos de 200 personas': 100000003,
    '200 a 1.000': 100000004,
    'Más de 1.000': 100000005,
}

# Largo máximo por campo (los de texto libre se recortan; los de Dataverse respetan su límite)
LARGOS = {
    'nombre': 100, 'email': 100, 'empresa': 100, 'cargo': 100, 'telefono': 50,
    'mensaje': 4000, 'origen_pagina': 300, 'origen_cta': 300,
    'diagnostico_herramienta': 200, 'diagnostico_resultado': 500,
    'diagnostico_detalle': 4000, 'utm': 500,
}
EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]{2,}$')
MIN_SEGUNDOS = 3  # un humano no completa el formulario en menos tiempo


class Rechazo(Exception):
    """Envío inválido: se responde 400 con los campos a corregir."""
    def __init__(self, campos):
        super().__init__(', '.join(campos))
        self.campos = campos


def _txt(data, campo):
    v = data.get(campo)
    if not isinstance(v, str):
        return ''
    return v.strip()[:LARGOS.get(campo, 200)]


def es_bot(data, ahora=None):
    """Campo trampa con contenido o envío más rápido de lo humanamente posible."""
    if _txt(data, 'sitio_web'):
        return True
    try:
        cargado = float(data.get('t') or 0) / 1000
    except (TypeError, ValueError):
        return True
    return cargado > 0 and (ahora or time.time()) - cargado < MIN_SEGUNDOS


def validar(data):
    """Devuelve los campos limpios o lanza Rechazo."""
    d = {c: _txt(data, c) for c in LARGOS}
    errores = []
    if not d['nombre']:
        errores.append('nombre')
    if not EMAIL_RE.match(d['email']):
        errores.append('email')
    if data.get('consentimiento') is not True:
        errores.append('consentimiento')
    if errores:
        raise Rechazo(errores)
    d['pais'] = data.get('pais') if data.get('pais') in PAISES else ''
    d['tamano'] = data.get('tamano') if data.get('tamano') in TAMANOS else ''
    intereses = data.get('interes') if isinstance(data.get('interes'), list) else []
    d['interes'] = [i for i in intereses if i in INTERESES]
    return d


def _col(nombre):
    """Columnas propias del Lead (prefijo del editor de la solución en Dataverse)."""
    return os.environ.get('CRM_PREFIJO', 'wit_') + nombre


def _utm(texto):
    pares = dict(urllib.parse.parse_qsl(texto or '', keep_blank_values=False))
    return {k: pares.get(f'utm_{k}', '')[:200] for k in ('source', 'medium', 'campaign', 'term', 'content')}


def armar_lead(d, ahora=None):
    """Payload de la tabla lead: columnas estándar más las columnas propias de la solicitud web."""
    ahora = ahora or datetime.now(timezone.utc)
    partes = d['nombre'].split()
    nombre, apellido = (' '.join(partes[:-1]), partes[-1]) if len(partes) > 1 else ('', partes[0])
    etiquetas = [INTERESES[i] for i in d['interes']]
    temas = ', '.join(etiquetas) or 'Consulta general'

    lead = {
        'subject': f"Sitio web · {temas} · {d['empresa'] or d['nombre']}"[:300],
        'lastname': apellido[:50],
        'emailaddress1': d['email'],
        'description': d['mensaje'] or '(sin mensaje)',
        'leadsourcecode': int(os.environ.get('LEAD_SOURCE_CODE', '8')),
        _col('sitioorigen'): SITIO_WIT,
        _col('consentimiento'): True,
        _col('consentimientofecha'): ahora.strftime('%Y-%m-%dT%H:%M:%SZ'),
        _col('politicaversion'): os.environ.get('POLITICA_VERSION', 'vigente')[:20],
    }
    opcionales = {
        'firstname': nombre[:50], 'companyname': d['empresa'], 'jobtitle': d['cargo'],
        'telephone1': d['telefono'], 'address1_country': d['pais'],
        _col('tamanoorganizacion'): TAMANOS.get(d['tamano']),
        # Opción múltiple: Dataverse recibe los valores separados por coma
        _col('intereseswit'): ','.join(str(OPCION_INTERES[i]) for i in d['interes']),
        _col('paginaorigen'): d['origen_pagina'],
        _col('botonorigen'): d['origen_cta'],
        _col('diagnosticoherramienta'): d['diagnostico_herramienta'],
        _col('diagnosticoresultado'): d['diagnostico_resultado'],
        _col('diagnosticodetalle'): d['diagnostico_detalle'],
    }
    opcionales.update({_col(f'utm{k}'): v for k, v in _utm(d['utm']).items()})
    lead.update({k: v for k, v in opcionales.items() if v})
    equipo = os.environ.get('DATAVERSE_OWNER_TEAM_ID')
    if equipo:
        lead['ownerid@odata.bind'] = f'/teams({equipo})'
    return lead


# Colores de la marca (los mismos del sitio: --navy, --green, --ink, --muted, --line, --bg)
_NAVY, _VERDE, _TINTA, _GRIS, _LINEA, _FONDO = '#1B3A50', '#54BA00', '#242424', '#616161', '#EBEBEB', '#FAFAFA'


def _parrafo(texto):
    return escape(texto).replace('\n', '<br>')


def armar_aviso(d, lead, lead_id):
    """Correo de Graph (sendMail) que avisa a Comercial que hay un lead nuevo en el CRM.

    Lleva los datos del formulario (contacto, intereses, mensaje y origen) para entender la solicitud
    sin abrir Dynamics 365, más el enlace al registro. Responder va directo a la persona (replyTo).
    """
    base = os.environ.get('DATAVERSE_URL', '').rstrip('/')
    enlace = f'{base}/main.aspx?pagetype=entityrecord&etn=lead&id={lead_id}' if base and lead_id else ''
    intereses = ', '.join(INTERESES[i] for i in d['interes']) or 'Consulta general'

    def fila(etiqueta, valor):
        if not valor:
            return ''
        return (f'<tr><td style="padding:6px 16px 6px 0;color:{_GRIS};white-space:nowrap;vertical-align:top">{etiqueta}</td>'
                f'<td style="padding:6px 0;color:{_TINTA};vertical-align:top">{valor}</td></tr>')

    def tabla(titulo, filas):
        cuerpo = ''.join(filas)
        if not cuerpo:
            return ''
        return (f'<p style="margin:24px 0 6px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;'
                f'color:{_VERDE};font-weight:700">{titulo}</p>'
                f'<table cellpadding="0" cellspacing="0" style="font-size:15px;line-height:1.4">{cuerpo}</table>')

    contacto = tabla('Contacto', [
        fila('Nombre', escape(d['nombre'])),
        fila('Empresa', escape(d['empresa'])),
        fila('Cargo', escape(d['cargo'])),
        fila('Email', f'<a href="mailto:{escape(d["email"])}" style="color:{_NAVY}">{escape(d["email"])}</a>'),
        fila('Teléfono', escape(d['telefono'])),
        fila('País', escape(d['pais'])),
        fila('Tamaño', escape(d['tamano'])),
    ])
    mensaje = _parrafo(d['mensaje']) if d['mensaje'] else f'<em style="color:{_GRIS}">(sin mensaje)</em>'
    solicitud = tabla('Solicitud', [fila('Interés', escape(intereses))]) + (
        f'<div style="margin:12px 0 0;padding:14px 16px;background:{_FONDO};border-left:3px solid {_VERDE};'
        f'font-size:15px;line-height:1.5;color:{_TINTA}">{mensaje}</div>')
    utm = _utm(d['utm'])
    campana = ' · '.join(v for v in (utm['source'], utm['medium'], utm['campaign']) if v)
    diagnostico = ' · '.join(v for v in (d['diagnostico_herramienta'], d['diagnostico_resultado']) if v)
    origen = tabla('Origen', [
        fila('Página', escape(d['origen_pagina'])),
        fila('Botón', escape(d['origen_cta'])),
        fila('Campaña', escape(campana)),
        fila('Diagnóstico', escape(diagnostico)),
    ])
    if d['diagnostico_detalle']:
        origen += (f'<div style="margin:12px 0 0;padding:14px 16px;background:{_FONDO};font-size:14px;line-height:1.5;'
                   f'color:{_TINTA}">{_parrafo(d["diagnostico_detalle"])}</div>')

    if enlace:
        boton = (f'<a href="{escape(enlace)}" style="display:inline-block;padding:12px 22px;background:{_NAVY};'
                 'color:#ffffff;text-decoration:none;font-weight:700;border-radius:6px">Abrir en Dynamics 365</a>')
    else:
        boton = f'<span style="color:{_GRIS}">Búscalo en Dynamics 365 Sales → Clientes potenciales.</span>'

    html = (
        f'<div style="margin:0;padding:24px 12px;background:{_FONDO}">'
        f'<table cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;margin:0 auto;background:#ffffff;'
        f'border:1px solid {_LINEA};border-radius:8px;font-family:Segoe UI,Arial,sans-serif;color:{_TINTA}">'
        f'<tr><td style="padding:20px 28px;background:{_NAVY};border-radius:8px 8px 0 0">'
        '<span style="font-size:18px;font-weight:700;color:#ffffff;letter-spacing:.04em">W-IT</span>'
        '<span style="font-size:13px;color:#A8D97C;float:right;padding-top:4px">Nuevo cliente potencial · w-it.cl</span>'
        '</td></tr>'
        f'<tr><td style="height:4px;background:{_VERDE};font-size:0;line-height:0">&nbsp;</td></tr>'
        '<tr><td style="padding:28px">'
        f'<h1 style="margin:0 0 4px;font-size:22px;line-height:1.3;color:{_NAVY}">{escape(d["empresa"] or d["nombre"])}</h1>'
        f'<p style="margin:0;font-size:15px;color:{_GRIS}">{escape(intereses)} · formulario de contacto del sitio</p>'
        f'{contacto}{solicitud}{origen}'
        f'<p style="margin:28px 0 0">{boton}</p>'
        '</td></tr>'
        f'<tr><td style="padding:16px 28px;border-top:1px solid {_LINEA};font-size:12px;line-height:1.5;color:{_GRIS}">'
        'El lead ya quedó registrado en el CRM. Para contactar a la persona, usa Responder: el correo va directo a su dirección. '
        'La persona aceptó la política de privacidad; estos datos son personales, úsalos solo para atender su solicitud '
        'y no los reenvíes fuera de W-IT.'
        '</td></tr></table></div>')

    return {
        'message': {
            'subject': f"Nuevo lead · {lead['subject']}"[:250],
            'body': {'contentType': 'HTML', 'content': html},
            'toRecipients': [{'emailAddress': {'address': os.environ.get('AVISO_LEAD_DESTINO', 'comercial@w-it.cl')}}],
            'replyTo': [{'emailAddress': {'address': d['email'], 'name': d['nombre']}}],
        },
        'saveToSentItems': False,
    }


# ---------- Dataverse

_token = {'valor': None, 'vence': 0}


def _token_dataverse():
    if _token['valor'] and time.time() < _token['vence'] - 120:
        return _token['valor']
    url = f"https://login.microsoftonline.com/{os.environ['DATAVERSE_TENANT_ID']}/oauth2/v2.0/token"
    body = urllib.parse.urlencode({
        'grant_type': 'client_credentials',
        'client_id': os.environ['DATAVERSE_CLIENT_ID'],
        'client_secret': os.environ['DATAVERSE_CLIENT_SECRET'],
        'scope': f"{os.environ['DATAVERSE_URL'].rstrip('/')}/.default",
    }).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=15) as r:
        t = json.load(r)
    _token.update(valor=t['access_token'], vence=time.time() + int(t.get('expires_in', 3599)))
    return _token['valor']


def crear_lead(lead):
    """Crea el lead y devuelve su id. Lanza urllib.error.HTTPError si Dataverse lo rechaza."""
    url = f"{os.environ['DATAVERSE_URL'].rstrip('/')}/api/data/v9.2/leads"
    req = urllib.request.Request(url, data=json.dumps(lead).encode(), method='POST', headers={
        'Authorization': f'Bearer {_token_dataverse()}',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'OData-Version': '4.0',
        'OData-MaxVersion': '4.0',
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        entidad = r.headers.get('OData-EntityId', '')
    m = re.search(r'\(([0-9a-f-]{36})\)', entidad)
    return m.group(1) if m else ''


def captcha_valido(data, ip=''):
    """Verifica el token de Cloudflare Turnstile. Sin TURNSTILE_SECRET (pruebas locales) no se exige."""
    secreto = os.environ.get('TURNSTILE_SECRET')
    if not secreto:
        return True
    token = data.get('cf-turnstile-response')
    if not isinstance(token, str) or not token:
        return False
    campos = {'secret': secreto, 'response': token}
    if ip:
        campos['remoteip'] = ip
    req = urllib.request.Request('https://challenges.cloudflare.com/turnstile/v0/siteverify',
                                 data=urllib.parse.urlencode(campos).encode())
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r).get('success') is True


def limitado(ip, registro, maximo=5):
    """Límite simple de envíos por IP y por hora, en memoria de la instancia (no reemplaza un WAF)."""
    ahora = time.time()
    recientes = [t for t in registro.get(ip, []) if ahora - t < 3600]
    registro[ip] = recientes + [ahora]
    return len(recientes) >= maximo


def origen_permitido(origin):
    permitidos = [o.strip() for o in os.environ.get('ALLOWED_ORIGINS', '').split(',') if o.strip()]
    return not permitidos or origin in permitidos
