import os
import sys
import time
import unittest
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared import lead as L  # noqa: E402

BASE = {
    'nombre': 'María José Pérez', 'email': 'mj@empresa.cl', 'empresa': 'Empresa S.A.',
    'cargo': 'Gerenta TI', 'telefono': '+56 9 1234 5678', 'pais': 'Chile',
    'tamano': '200 a 1.000', 'interes': ['contact-center', 'inventado'],
    'mensaje': 'Queremos evaluar Contact Center.', 'consentimiento': True,
    'origen_pagina': '/soluciones/contact-center/', 'origen_cta': 'Conversemos · cta',
    'utm': 'utm_source=google', 't': str(int((time.time() - 60) * 1000)), 'sitio_web': '',
}


class Validacion(unittest.TestCase):
    def test_valido(self):
        d = L.validar(BASE)
        self.assertEqual(d['interes'], ['Contact center'])
        self.assertEqual(d['pais'], 'Chile')

    def test_obligatorios(self):
        with self.assertRaises(L.Rechazo) as e:
            L.validar({**BASE, 'nombre': ' ', 'email': 'no-es-email', 'consentimiento': 'true'})
        self.assertEqual(e.exception.campos, ['nombre', 'email', 'consentimiento'])

    def test_valores_fuera_de_lista(self):
        d = L.validar({**BASE, 'pais': 'Narnia', 'tamano': 'x', 'interes': 'contact-center'})
        self.assertEqual((d['pais'], d['tamano'], d['interes']), ('', '', []))

    def test_recorta_largos(self):
        self.assertEqual(len(L.validar({**BASE, 'mensaje': 'a' * 9000})['mensaje']), 4000)


class Antispam(unittest.TestCase):
    def test_humano(self):
        self.assertFalse(L.es_bot(BASE))

    def test_campo_trampa(self):
        self.assertTrue(L.es_bot({**BASE, 'sitio_web': 'http://spam'}))

    def test_demasiado_rapido(self):
        self.assertTrue(L.es_bot({**BASE, 't': str(int(time.time() * 1000))}))

    def test_t_invalido(self):
        self.assertTrue(L.es_bot({**BASE, 't': 'abc'}))


class Payload(unittest.TestCase):
    def test_lead(self):
        os.environ.pop('DATAVERSE_OWNER_TEAM_ID', None)
        lead = L.armar_lead(L.validar(BASE), datetime(2026, 10, 1, 12, tzinfo=timezone.utc))
        self.assertEqual(lead['firstname'], 'María José')
        self.assertEqual(lead['lastname'], 'Pérez')
        self.assertEqual(lead['subject'], 'Sitio web · Contact center · Empresa S.A.')
        self.assertEqual(lead['leadsourcecode'], 8)
        self.assertIn('2026-10-01 12:00:00 UTC', lead['description'])
        self.assertIn('Página: /soluciones/contact-center/', lead['description'])
        self.assertNotIn('ownerid@odata.bind', lead)

    def test_nombre_de_una_palabra_y_sin_opcionales(self):
        lead = L.armar_lead(L.validar({'nombre': 'Cher', 'email': 'c@x.cl', 'consentimiento': True}))
        self.assertEqual(lead['lastname'], 'Cher')
        self.assertNotIn('firstname', lead)
        self.assertNotIn('companyname', lead)
        self.assertTrue(lead['subject'].startswith('Sitio web · Consulta general · Cher'))

    def test_equipo_duenio(self):
        os.environ['DATAVERSE_OWNER_TEAM_ID'] = '00000000-0000-0000-0000-000000000001'
        try:
            lead = L.armar_lead(L.validar(BASE))
            self.assertEqual(lead['ownerid@odata.bind'], '/teams(00000000-0000-0000-0000-000000000001)')
        finally:
            del os.environ['DATAVERSE_OWNER_TEAM_ID']



class Captcha(unittest.TestCase):
    def tearDown(self):
        os.environ.pop('TURNSTILE_SECRET', None)

    def test_sin_secreto_no_se_exige(self):
        os.environ.pop('TURNSTILE_SECRET', None)
        self.assertTrue(L.captcha_valido({}))

    def test_con_secreto_y_sin_token(self):
        os.environ['TURNSTILE_SECRET'] = 'x'
        self.assertFalse(L.captcha_valido({}))

    def test_respuesta_de_cloudflare(self):
        import io
        from unittest import mock
        os.environ['TURNSTILE_SECRET'] = 'x'
        for cuerpo, esperado in ((b'{"success": true}', True), (b'{"success": false}', False)):
            with mock.patch('urllib.request.urlopen', return_value=io.BytesIO(cuerpo)) as m:
                self.assertEqual(L.captcha_valido({'cf-turnstile-response': 'tok'}, '1.2.3.4'), esperado)
                enviado = m.call_args[0][0].data.decode()
                self.assertIn('response=tok', enviado)
                self.assertIn('remoteip=1.2.3.4', enviado)


if __name__ == '__main__':
    unittest.main()
