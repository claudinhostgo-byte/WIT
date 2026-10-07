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
  AVISO_LEAD_DESTINO      (opcional) a quién avisar de cada lead nuevo; comercial@w-it.cl por defecto
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


def armar_aviso(lead, lead_id):
    """Correo de Graph (sendMail) que avisa a Comercial que hay un lead nuevo en el CRM.

    Solo lleva el asunto del lead y el enlace: los datos de contacto y el mensaje se revisan en Dynamics 365.
    """
    base = os.environ.get('DATAVERSE_URL', '').rstrip('/')
    enlace = f'{base}/main.aspx?pagetype=entityrecord&etn=lead&id={lead_id}' if base and lead_id else ''
    boton = (f'<p><a href="{escape(enlace)}">Abrir el cliente potencial en Dynamics 365</a></p>' if enlace
             else '<p>Búscalo en Dynamics 365 Sales → Clientes potenciales.</p>')
    return {
        'message': {
            'subject': f"Nuevo lead · {lead['subject']}"[:250],
            'body': {'contentType': 'HTML', 'content': (
                '<p>Llegó una solicitud desde el formulario de contacto de w-it.cl y quedó registrada en el CRM.</p>'
                f"<p><strong>{escape(lead['subject'])}</strong></p>{boton}"
                '<p style="color:#666">Los datos de la persona y su mensaje están en el registro del CRM.</p>')},
            'toRecipients': [{'emailAddress': {'address': os.environ.get('AVISO_LEAD_DESTINO', 'comercial@w-it.cl')}}],
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
