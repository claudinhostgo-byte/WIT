import base64
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared import lead as L  # noqa: E402
from shared import postulacion as P  # noqa: E402

PDF = b'%PDF-1.7\n' + b'x' * 100
BASE = {
    'nombre': 'María José Pérez', 'email': 'mj@correo.cl', 'telefono': '+56 9 1234 5678',
    'mensaje': 'Me interesa <Dynamics 365>.', 'ia': 'Sí, para revisar la redacción.', 'consentimiento': True,
    'cv': {'nombre': '../CV María José.pdf', 'contenido': base64.b64encode(PDF).decode()},
}


def cv(nombre, contenido):
    return {**BASE, 'cv': {'nombre': nombre, 'contenido': base64.b64encode(contenido).decode()}}


class Validacion(unittest.TestCase):
    def test_valido(self):
        d = P.validar(BASE)
        self.assertEqual(d['cv']['bytes'], PDF)
        self.assertEqual(d['cv']['nombre'], 'CV María José.pdf')
        self.assertEqual(d['cv']['tipo'], 'application/pdf')

    def test_obligatorios(self):
        with self.assertRaises(L.Rechazo) as e:
            P.validar({'nombre': ' ', 'email': 'x', 'ia': '  ', 'consentimiento': 'true'})
        self.assertEqual(e.exception.campos, ['nombre', 'email', 'ia', 'cv', 'consentimiento'])

    def test_formato_no_permitido(self):
        for nombre, contenido in [('cv.exe', b'MZ..'), ('cv.pdf', b'MZ no es pdf'), ('cv.docx', b'%PDF')]:
            with self.assertRaises(L.Rechazo) as e:
                P.validar(cv(nombre, contenido))
            self.assertEqual(e.exception.campos, ['cv'], nombre)

    def test_docx_y_doc(self):
        self.assertTrue(P.validar(cv('cv.DOCX', b'PK\x03\x04resto'))['cv']['tipo'].endswith('document'))
        self.assertEqual(P.validar(cv('cv.doc', b'\xd0\xcf\x11\xe0resto'))['cv']['tipo'], 'application/msword')

    def test_tamano(self):
        with self.assertRaises(L.Rechazo) as e:
            P.validar(cv('cv.pdf', b'%PDF' + b'x' * P.MAX_CV_BYTES))
        self.assertEqual(e.exception.campos, ['cv_tamano'])

    def test_base64_invalido(self):
        with self.assertRaises(L.Rechazo):
            P.validar({**BASE, 'cv': {'nombre': 'cv.pdf', 'contenido': '***'}})


class Correo(unittest.TestCase):
    def test_correo(self):
        m = P.armar_correo(P.validar(BASE))['message']
        self.assertEqual(m['toRecipients'][0]['emailAddress']['address'], 'postulaciones@w-it.cl')
        self.assertEqual(m['replyTo'][0]['emailAddress']['address'], 'mj@correo.cl')
        self.assertIn('&lt;Dynamics 365&gt;', m['body']['content'])
        self.assertIn('Sí, para revisar la redacción.', m['body']['content'])
        self.assertEqual(base64.b64decode(m['attachments'][0]['contentBytes']), PDF)

    def test_limite(self):
        registro = {}
        self.assertEqual([L.limitado('1.1.1.1', registro, 2) for _ in range(3)], [False, False, True])


if __name__ == '__main__':
    unittest.main()
