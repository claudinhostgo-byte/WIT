"""POST /api/postulacion: recibe "Trabaja con nosotros" y envía la postulación con el CV a postulaciones@w-it.cl."""
import json
import logging
import urllib.error

import azure.functions as func

from ..shared import lead as L
from ..shared import postulacion as P

_envios = {}
MAX_POR_HORA = 3


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

    if L.es_bot(data):
        logging.info('postulacion: envío descartado por antispam')
        return _json(200, {'ok': True})

    ip = (req.headers.get('X-Forwarded-For') or '').split(',')[0].split(':')[0].strip()
    if ip and L.limitado(ip, _envios, MAX_POR_HORA):
        return _json(429, {'ok': False})

    try:
        if not L.captcha_valido(data, ip):
            return _json(400, {'ok': False, 'campos': ['captcha']})
    except Exception:
        logging.exception('postulacion: no se pudo verificar el captcha')
        return _json(502, {'ok': False})

    try:
        datos = P.validar(data)
    except L.Rechazo as e:
        return _json(400, {'ok': False, 'campos': e.campos})

    try:
        P.enviar(P.armar_correo(datos))
    except urllib.error.HTTPError as e:
        # Sin datos personales en el log: solo el código y el mensaje de Graph
        logging.error('postulacion: Graph respondió %s %s', e.code, e.read()[:500])
        return _json(502, {'ok': False})
    except Exception:
        logging.exception('postulacion: error al enviar el correo')
        return _json(502, {'ok': False})

    logging.info('postulacion: correo enviado')
    return _json(201, {'ok': True})
