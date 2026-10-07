"""POST /api/contacto: recibe el formulario del sitio, crea un Lead en Dynamics 365 y avisa a Comercial."""
import json
import logging
import urllib.error

import azure.functions as func

from ..shared import lead as L
from ..shared import postulacion as P

# Límite simple por IP y por instancia (complementa el campo trampa; no reemplaza un WAF)
_envios = {}
MAX_POR_HORA = 5


def _json(status, cuerpo):
    return func.HttpResponse(json.dumps(cuerpo, ensure_ascii=False), status_code=status,
                             mimetype='application/json', charset='utf-8')


def main(req: func.HttpRequest) -> func.HttpResponse:
    if not L.origen_permitido(req.headers.get('Origin', '')):
        return _json(403, {'ok': False})
    try:
        data = req.get_json()
        if not isinstance(data, dict):
            raise ValueError
    except ValueError:
        return _json(400, {'ok': False, 'campos': []})

    # A un bot se le responde como si todo hubiera salido bien, para que no insista
    if L.es_bot(data):
        logging.info('contacto: envío descartado por antispam')
        return _json(200, {'ok': True})

    ip = (req.headers.get('X-Forwarded-For') or '').split(',')[0].split(':')[0].strip()
    if ip and L.limitado(ip, _envios, MAX_POR_HORA):
        return _json(429, {'ok': False})

    try:
        if not L.captcha_valido(data, ip):
            return _json(400, {'ok': False, 'campos': ['captcha']})
    except Exception:
        logging.exception('contacto: no se pudo verificar el captcha')
        return _json(502, {'ok': False})

    try:
        datos = L.validar(data)
    except L.Rechazo as e:
        return _json(400, {'ok': False, 'campos': e.campos})

    lead = L.armar_lead(datos)
    try:
        lead_id = L.crear_lead(lead)
    except urllib.error.HTTPError as e:
        # Sin datos personales en el log: solo el código y el mensaje de Dataverse
        logging.error('contacto: Dataverse respondió %s %s', e.code, e.read()[:500])
        return _json(502, {'ok': False})
    except Exception:
        logging.exception('contacto: error al crear el lead')
        return _json(502, {'ok': False})

    logging.info('contacto: lead creado %s', lead_id)

    # El lead ya quedó en el CRM: si el aviso falla, solo se registra y la persona igual recibe su confirmación
    try:
        P.enviar(L.armar_aviso(lead, lead_id))
    except urllib.error.HTTPError as e:
        logging.error('contacto: aviso a Comercial, Graph respondió %s %s', e.code, e.read()[:500])
    except Exception:
        logging.exception('contacto: no se pudo enviar el aviso a Comercial')
    return _json(201, {'ok': True})
