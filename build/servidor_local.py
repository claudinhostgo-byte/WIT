"""Vista local del sitio con el formulario funcionando.

  python build/servidor_local.py            # modo prueba: muestra el Lead que se crearía, no llama a Dataverse
  (con DATAVERSE_URL, DATAVERSE_TENANT_ID, DATAVERSE_CLIENT_ID y DATAVERSE_CLIENT_SECRET definidas, crea el Lead real)

Las postulaciones (/api/postulacion) siempre quedan en modo prueba: muestra el correo sin enviarlo.
Usa la misma lógica que la API de Azure (api/shared/lead.py y api/shared/postulacion.py).
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, 'api'))
from shared import lead as L  # noqa: E402
from shared import postulacion as P  # noqa: E402

REAL = all(os.environ.get(v) for v in ('DATAVERSE_URL', 'DATAVERSE_TENANT_ID', 'DATAVERSE_CLIENT_ID', 'DATAVERSE_CLIENT_SECRET'))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=os.path.join(RAIZ, 'sitio'), **kw)

    def _json(self, status, cuerpo):
        b = json.dumps(cuerpo, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        if self.path not in ('/api/contacto', '/api/postulacion'):
            return self._json(404, {'ok': False})
        try:
            data = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'null')
            assert isinstance(data, dict)
        except Exception:
            return self._json(400, {'ok': False, 'campos': []})
        if L.es_bot(data):
            print('[antispam] envío descartado')
            return self._json(200, {'ok': True})
        if not L.captcha_valido(data):
            return self._json(400, {'ok': False, 'campos': ['captcha']})
        if self.path == '/api/postulacion':
            return self._postulacion(data)
        try:
            lead = L.armar_lead(L.validar(data))
        except L.Rechazo as e:
            return self._json(400, {'ok': False, 'campos': e.campos})
        if not REAL:
            print('[prueba] Lead que se crearía en Dataverse:\n' + json.dumps(lead, ensure_ascii=False, indent=2))
            return self._json(201, {'ok': True, 'prueba': True})
        try:
            print('[dataverse] lead creado', L.crear_lead(lead))
            return self._json(201, {'ok': True})
        except Exception as e:
            print('[dataverse] error', e, getattr(e, 'read', lambda: b'')()[:500])
            return self._json(502, {'ok': False})

    def _postulacion(self, data):
        try:
            correo = P.armar_correo(P.validar(data))
        except L.Rechazo as e:
            return self._json(400, {'ok': False, 'campos': e.campos})
        adj = correo['message']['attachments'][0]
        adj['contentBytes'] = f"<{len(adj['contentBytes'])} caracteres base64>"
        print('[prueba] Correo que se enviaría:\n' + json.dumps(correo, ensure_ascii=False, indent=2))
        return self._json(201, {'ok': True, 'prueba': True})


if __name__ == '__main__':
    sys.stdout.reconfigure(line_buffering=True)
    puerto = int(os.environ.get('PORT', '8080'))
    print(f"http://localhost:{puerto}  ·  modo {'Dataverse REAL' if REAL else 'prueba'}")
    ThreadingHTTPServer(('127.0.0.1', puerto), Handler).serve_forever()
