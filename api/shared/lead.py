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
  ALLOWED_ORIGINS         (opcional) orígenes permitidos, separados por coma
"""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

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
TAMANOS = {'Menos de 200 personas', '200 a 1.000', 'Más de 1.000'}

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
    d['interes'] = [INTERESES[i] for i in intereses if i in INTERESES]
    return d


def armar_lead(d, ahora=None):
    """Payload de la tabla lead. Lo que no tiene columna estándar va en la descripción."""
    ahora = ahora or datetime.now(timezone.utc)
    partes = d['nombre'].split()
    nombre, apellido = (' '.join(partes[:-1]), partes[-1]) if len(partes) > 1 else ('', partes[0])
    temas = ', '.join(d['interes']) or 'Consulta general'
    asunto = f"Sitio web · {temas} · {d['empresa'] or d['nombre']}"[:300]

    linea = lambda etiqueta, valor: f'{etiqueta}: {valor}' if valor else None
    descripcion = '\n'.join(x for x in [
        d['mensaje'] or '(sin mensaje)',
        '',
        '— Datos del formulario —',
        linea('Intereses', temas),
        linea('Tamaño de la empresa', d['tamano']),
        linea('País', d['pais']),
        '',
        '— Origen —',
        linea('Página', d['origen_pagina']),
        linea('Botón', d['origen_cta']),
        linea('UTM', d['utm']),
        linea('Autodiagnóstico', d['diagnostico_herramienta']),
        linea('Resultado', d['diagnostico_resultado']),
        linea('Detalle', d['diagnostico_detalle']),
        '',
        '— Consentimiento —',
        f"Aceptó la política de privacidad (versión {os.environ.get('POLITICA_VERSION', 'vigente')}) "
        f"el {ahora.strftime('%Y-%m-%d %H:%M:%S')} UTC desde el formulario de contacto del sitio.",
    ] if x is not None)

    lead = {
        'subject': asunto,
        'lastname': apellido[:50],
        'emailaddress1': d['email'],
        'description': descripcion,
        'leadsourcecode': int(os.environ.get('LEAD_SOURCE_CODE', '8')),
    }
    opcionales = {
        'firstname': nombre[:50], 'companyname': d['empresa'], 'jobtitle': d['cargo'],
        'telephone1': d['telefono'], 'address1_country': d['pais'],
    }
    lead.update({k: v for k, v in opcionales.items() if v})
    equipo = os.environ.get('DATAVERSE_OWNER_TEAM_ID')
    if equipo:
        lead['ownerid@odata.bind'] = f'/teams({equipo})'
    return lead


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


def origen_permitido(origin):
    permitidos = [o.strip() for o in os.environ.get('ALLOWED_ORIGINS', '').split(',') if o.strip()]
    return not permitidos or origin in permitidos
