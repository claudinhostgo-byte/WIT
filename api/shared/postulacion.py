"""Formulario "Trabaja con nosotros" → correo con el currículum adjunto a postulaciones@w-it.cl (Microsoft Graph).

Sin dependencias externas, igual que lead.py. Configuración por variables de entorno:

  POSTULACIONES_REMITENTE buzón desde el que se envía (p. ej. postulaciones@w-it.cl); la app solo puede
                          enviar desde ese buzón (RBAC de aplicaciones en Exchange, ver infra/DESPLIEGUE.md)
  POSTULACIONES_DESTINO   (opcional) a quién llega; postulaciones@w-it.cl por defecto
  GRAPH_TENANT_ID         (opcional) por defecto DATAVERSE_TENANT_ID
  GRAPH_CLIENT_ID         (opcional) por defecto DATAVERSE_CLIENT_ID
  GRAPH_CLIENT_SECRET     (opcional) por defecto DATAVERSE_CLIENT_SECRET

El antispam, el captcha y el control de origen son los mismos del formulario de contacto (lead.py).
"""
import base64
import binascii
import json
import os
import re
import time
import urllib.parse
import urllib.request
from html import escape

from .lead import EMAIL_RE, Rechazo

DESTINO = 'postulaciones@w-it.cl'
LARGOS = {'nombre': 100, 'email': 100, 'telefono': 50, 'mensaje': 4000, 'ia': 2000}

# Microsoft Graph acepta hasta 4 MB por solicitud en sendMail; el adjunto viaja en base64 (+33 %)
MAX_CV_BYTES = 2 * 1024 * 1024
# Extensión → (tipo MIME, firma de los primeros bytes)
FORMATOS = {
    'pdf': ('application/pdf', b'%PDF'),
    'docx': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', b'PK\x03\x04'),
    'doc': ('application/msword', b'\xd0\xcf\x11\xe0'),
}


def _txt(data, campo):
    v = data.get(campo)
    return v.strip()[:LARGOS[campo]] if isinstance(v, str) else ''


def _nombre_archivo(nombre, ext):
    base = re.sub(r'[^\w\-. ]+', '', os.path.splitext(nombre or '')[0], flags=re.UNICODE).strip(' .')[:80]
    return f"{base or 'curriculum'}.{ext}"


def validar(data):
    """Devuelve los campos limpios y el currículum decodificado, o lanza Rechazo."""
    d = {c: _txt(data, c) for c in LARGOS}
    errores = []
    if not d['nombre']:
        errores.append('nombre')
    if not EMAIL_RE.match(d['email']):
        errores.append('email')
    if not d['ia']:
        errores.append('ia')

    cv = data.get('cv') if isinstance(data.get('cv'), dict) else {}
    ext = os.path.splitext(cv.get('nombre') or '')[1].lower().lstrip('.')
    contenido = b''
    if ext in FORMATOS and isinstance(cv.get('contenido'), str):
        try:
            contenido = base64.b64decode(cv['contenido'], validate=True)
        except (binascii.Error, ValueError):
            contenido = b''
    if not contenido:
        errores.append('cv')
    elif len(contenido) > MAX_CV_BYTES:
        errores.append('cv_tamano')
    elif not contenido.startswith(FORMATOS[ext][1]):
        errores.append('cv')

    if data.get('consentimiento') is not True:
        errores.append('consentimiento')
    if errores:
        raise Rechazo(errores)
    d['cv'] = {'nombre': _nombre_archivo(cv.get('nombre'), ext), 'tipo': FORMATOS[ext][0], 'bytes': contenido}
    return d


def armar_correo(d):
    """Mensaje de Graph (sendMail): responde directo a la persona y lleva el currículum adjunto."""
    filas = [('Nombre', d['nombre']), ('Email', d['email']), ('Teléfono', d['telefono'] or '—')]
    tabla = ''.join(f'<tr><th align="left" style="padding:4px 12px 4px 0">{a}</th><td>{escape(b)}</td></tr>' for a, b in filas)
    parrafo = lambda t: escape(t).replace('\n', '<br>')
    mensaje = parrafo(d['mensaje']) if d['mensaje'] else '<em>(sin mensaje)</em>'
    return {
        'message': {
            'subject': f"Postulación sitio web · {d['nombre']}"[:250],
            'body': {'contentType': 'HTML', 'content': (
                '<p>Nueva postulación recibida desde Trabaja con nosotros en w-it.cl.</p>'
                f'<table>{tabla}</table><p><strong>Mensaje</strong><br>{mensaje}</p>'
                f"<p><strong>¿Usó IA para crear su currículum o llenar el formulario?</strong><br>{parrafo(d['ia'])}</p>"
                '<p style="color:#666">La persona aceptó la política de privacidad y el uso de sus datos para evaluar su postulación. '
                'Para responderle, usa Responder: el correo va directo a su dirección.</p>')},
            'toRecipients': [{'emailAddress': {'address': os.environ.get('POSTULACIONES_DESTINO', DESTINO)}}],
            'replyTo': [{'emailAddress': {'address': d['email'], 'name': d['nombre']}}],
            'attachments': [{
                '@odata.type': '#microsoft.graph.fileAttachment',
                'name': d['cv']['nombre'],
                'contentType': d['cv']['tipo'],
                'contentBytes': base64.b64encode(d['cv']['bytes']).decode(),
            }],
        },
        'saveToSentItems': False,
    }


# ---------- Microsoft Graph

_token = {'valor': None, 'vence': 0}


def _env(nombre):
    return os.environ.get(f'GRAPH_{nombre}') or os.environ[f'DATAVERSE_{nombre}']


def _token_graph():
    if _token['valor'] and time.time() < _token['vence'] - 120:
        return _token['valor']
    url = f"https://login.microsoftonline.com/{_env('TENANT_ID')}/oauth2/v2.0/token"
    body = urllib.parse.urlencode({
        'grant_type': 'client_credentials',
        'client_id': _env('CLIENT_ID'),
        'client_secret': _env('CLIENT_SECRET'),
        'scope': 'https://graph.microsoft.com/.default',
    }).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=15) as r:
        t = json.load(r)
    _token.update(valor=t['access_token'], vence=time.time() + int(t.get('expires_in', 3599)))
    return _token['valor']


def enviar(correo):
    """Envía el correo. Lanza urllib.error.HTTPError si Graph lo rechaza."""
    remitente = urllib.parse.quote(os.environ['POSTULACIONES_REMITENTE'])
    req = urllib.request.Request(f'https://graph.microsoft.com/v1.0/users/{remitente}/sendMail',
                                 data=json.dumps(correo).encode(), method='POST', headers={
                                     'Authorization': f'Bearer {_token_graph()}',
                                     'Content-Type': 'application/json; charset=utf-8',
                                 })
    with urllib.request.urlopen(req, timeout=30):
        pass
