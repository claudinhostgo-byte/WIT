"""Campañas de búsqueda de Google Ads de W-IT: genera los CSV para Google Ads Editor y valida los límites.

Uso: python marketing/google-ads/generar.py  →  escribe los CSV en esta misma carpeta.
Límites de Google Ads: título 30, descripción 90, ruta 15, texto de enlace 25, descripción de enlace 35, texto destacado 25.
"""
import csv
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SITIO = 'https://w-it.cl/'

# Presupuesto total: máx. $200.000 CLP al mes. Google gasta como máximo 30,4 × el presupuesto diario en un mes.
CAMPANAS = {
    'dynamics': dict(nombre='W-IT | Búsqueda | Dynamics 365 | CL-PE', diario=4200,
                     url=SITIO + 'implementacion/dynamics-365/', ruta=('dynamics-365', 'implementacion'),
                     sufijo='utm_source=google&utm_medium=cpc&utm_campaign=dynamics-365&utm_term={keyword}&utm_content={adgroupid}'),
    'ia': dict(nombre='W-IT | Búsqueda | IA y agentes Microsoft | CL-PE', diario=2300,
               url=SITIO + 'implementacion/agentes-de-ia/', ruta=('agentes-ia', 'copilot'),
               sufijo='utm_source=google&utm_medium=cpc&utm_campaign=ia-agentes&utm_term={keyword}&utm_content={adgroupid}'),
}

# Títulos comunes de cada campaña + propios de cada grupo (máx. 15 por anuncio)
COMUNES = {
    'dynamics': ['Implementación Dynamics 365', 'Dynamics 365 en Chile y Perú', 'Solutions Partner Microsoft',
                 '6 designaciones Microsoft', 'Partner Microsoft desde 2014', 'ISO 9001 e ISO/IEC 27001',
                 'Metodología Success by Design', 'Oficinas en Santiago y Lima', 'Autodiagnóstico gratuito',
                 'Conversemos sobre tu proyecto'],
    'ia': ['Agentes de IA con Microsoft', 'Implementación Copilot Studio', 'Agentes de IA para empresas',
           'Copilot Jumpstart Partner', 'Solutions Partner Microsoft', 'ISO 9001 e ISO/IEC 27001',
           'IA para Chile y Perú', 'Autodiagnóstico de IA gratis', 'Agentes sobre tus datos',
           'Conversemos sobre tu caso'],
}
DESCRIPCIONES = {
    'dynamics': ['Implementamos Dynamics 365 Sales, Customer Service, Contact Center y Business Central.',
                 'Solutions Partner for Microsoft Cloud, con las seis designaciones. ISO 9001 y 27001.',
                 'Haz el autodiagnóstico gratuito y descubre por dónde partir. Conversemos sin compromiso.',
                 'Oficinas en Santiago y Lima. Success by Design, el marco de Microsoft, en entregas cortas.'],
    'ia': ['Diseñamos y ponemos en producción agentes con Copilot Studio y Azure AI Foundry.',
           'Microsoft Copilot Jumpstart Partner y Solutions Partner for Microsoft Cloud. ISO 27001.',
           'Haz el autodiagnóstico de IA gratuito: nivel de preparación y próximo paso sugerido.',
           'Evaluamos cada agente antes de llevarlo a producción y lo monitoreamos de forma continua.'],
}

# Grupos de anuncios: títulos propios y palabras clave (F = frase, E = exacta). Sin concordancia amplia:
# con este presupuesto, la amplia gasta en búsquedas de estudiantes y de soporte.
GRUPOS = [
    ('dynamics', 'Dynamics 365 · Partner e implementación',
     ['Partner Dynamics 365 en Chile', 'Partner Dynamics 365 en Perú', 'Consultora Dynamics 365',
      'Premio Microsoft 2019 y 2020', 'Cofinanciamiento: consúltanos'],
     [('implementación dynamics 365', 'F'), ('partner dynamics 365', 'F'), ('consultora dynamics 365', 'F'),
      ('consultores dynamics 365', 'F'), ('partner microsoft dynamics', 'F'), ('implementador dynamics 365', 'F'),
      ('dynamics 365 chile', 'E'), ('dynamics 365 peru', 'E'), ('microsoft dynamics chile', 'E'), ('microsoft dynamics peru', 'E')]),
    ('dynamics', 'CRM · Sales y Customer Service',
     ['Dynamics 365 Sales', 'Dynamics 365 Customer Service', 'CRM de Microsoft para ventas',
      'De la venta a la postventa', 'Premio Microsoft 2019 y 2020'],
     [('dynamics 365 sales', 'F'), ('dynamics 365 customer service', 'F'), ('implementación crm microsoft', 'F'),
      ('crm microsoft dynamics', 'F'), ('dynamics crm', 'E'), ('crm dynamics 365', 'F')]),
    ('dynamics', 'Contact Center',
     ['Dynamics 365 Contact Center', 'Voz, chat, WhatsApp y correo', 'Contact center omnicanal',
      'IA para tu equipo de servicio', 'Premio Microsoft 2019 y 2020'],
     [('dynamics 365 contact center', 'F'), ('contact center microsoft', 'F'), ('contact center omnicanal', 'F'),
      ('omnichannel dynamics 365', 'F'), ('software contact center omnicanal', 'F')]),
    ('dynamics', 'ERP · Business Central y Finance',
     ['Dynamics 365 Business Central', 'Dynamics 365 Finance', '¿Business Central o Finance?',
      'ERP de Microsoft', 'Cofinanciamiento: consúltanos'],
     [('implementación business central', 'F'), ('partner business central', 'F'), ('business central chile', 'E'),
      ('business central peru', 'E'), ('dynamics 365 business central', 'F'), ('dynamics 365 finance', 'F'),
      ('dynamics 365 finance and operations', 'F'), ('erp microsoft dynamics', 'F')]),
    ('ia', 'Copilot Studio y agentes',
     ['Microsoft Copilot Studio', 'Agentes conectados a tu CRM', 'Del piloto a producción',
      'Cofinanciamiento: consúltanos', 'Partner Copilot Studio'],
     [('implementación copilot studio', 'F'), ('copilot studio partner', 'F'), ('agentes copilot studio', 'F'),
      ('microsoft copilot studio', 'F'), ('agentes de ia microsoft', 'F'), ('agentes de ia para empresas', 'F')]),
    ('ia', 'Microsoft 365 Copilot para empresas',
     ['Microsoft 365 Copilot empresas', 'Adopción de Copilot', 'Copilot en Word, Excel y Teams',
      'Cofinanciamiento: consúltanos', 'Partner Copilot Microsoft'],
     [('microsoft 365 copilot empresas', 'F'), ('implementar microsoft 365 copilot', 'F'), ('copilot para empresas', 'F'),
      ('partner copilot microsoft', 'F'), ('adopción copilot', 'F'), ('licencias microsoft 365 copilot', 'F')]),
    ('ia', 'Azure AI e IA empresarial',
     ['Azure AI Foundry', 'IA con datos en tu tenant', 'Evaluación y monitoreo de IA',
      'IA responsable en producción', 'Partner Microsoft Data & AI'],
     [('azure ai foundry', 'F'), ('microsoft foundry', 'F'), ('azure openai empresas', 'F'),
      ('implementación inteligencia artificial empresas', 'F'), ('consultora inteligencia artificial microsoft', 'F')]),
]

# Negativas (frase) para ambas campañas
NEGATIVAS_COMUNES = [
    'curso', 'cursos', 'capacitación', 'certificación', 'certificacion', 'examen', 'tutorial', 'manual', 'pdf',
    'gratis', 'gratuito', 'free', 'descargar', 'download', 'trabajo', 'empleo', 'empleos', 'sueldo', 'salario',
    'ofertas laborales', 'práctica profesional', 'linkedin', 'youtube', 'udemy', 'wikipedia', 'qué es', 'que es',
    'login', 'iniciar sesión', 'sign in', 'soporte técnico microsoft', 'mb-210', 'mb-230', 'mb-910', 'pl-900', 'ai-900',
]
NEGATIVAS = {
    'dynamics': ['dynamics ax 2009', 'navision gratis', 'dynamics gp'],
    'ia': ['chatgpt', 'gemini', 'claude', 'anthropic', 'github copilot', 'copilot app', 'copilot gratis', 'bing',
           'imagen', 'imágenes', 'prompt', 'prompts', 'cómo usar', 'como usar', 'estudiantes', 'tarea', 'windows',
           'tecla copilot', 'copilot key'],
}

ENLACES = [  # (texto ≤25, descripción 1 ≤35, descripción 2 ≤35, ruta)
    ('Sales y Customer Service', 'Dynamics 365 Sales y Customer', 'Service, de la venta a la postventa', 'soluciones/ventas-servicio-y-contact-center/'),
    ('Contact Center', 'Voz, chat, WhatsApp y correo', 'Dynamics 365 Contact Center', 'soluciones/contact-center/'),
    ('Business Central/Finance', 'ERP de Microsoft para tu empresa', '¿Business Central o Finance?', 'soluciones/finanzas-y-operaciones/'),
    ('Copilot y agentes de IA', 'Microsoft 365 Copilot y', 'agentes con Copilot Studio', 'soluciones/ia-y-agentes/'),
    ('Cofinanciamiento', 'Programas de inversión de', 'Microsoft para POC y MVP', 'cofinanciamiento-microsoft/'),
    ('Trust Center', 'Credenciales Microsoft e ISO', 'verificables', 'nosotros/confianza/'),
]
DESTACADOS = ['6 designaciones Microsoft', 'ISO 9001 e ISO/IEC 27001', 'Oficinas Santiago y Lima',
              'Con Microsoft desde 2014', 'Autodiagnóstico gratuito', 'Success by Design']

LIMITES = {'titulo': 30, 'descripcion': 90, 'ruta': 15, 'enlace': 25, 'enlace_desc': 35, 'destacado': 25}


def validar():
    errores = []

    def chk(tipo, texto, donde):
        if len(texto) > LIMITES[tipo]:
            errores.append(f'{donde}: «{texto}» tiene {len(texto)} caracteres (máx. {LIMITES[tipo]})')

    for c, cfg in CAMPANAS.items():
        for p in cfg['ruta']:
            chk('ruta', p, c)
        for d in DESCRIPCIONES[c]:
            chk('descripcion', d, c)
    for c, g, titulos, _ in GRUPOS:
        todos = COMUNES[c] + titulos
        if len(todos) > 15:
            errores.append(f'{g}: {len(todos)} títulos (máx. 15)')
        if len(set(todos)) != len(todos):
            errores.append(f'{g}: títulos repetidos')
        for t in todos:
            chk('titulo', t, g)
    for t, d1, d2, _ in ENLACES:
        chk('enlace', t, 'enlace')
        chk('enlace_desc', d1, t)
        chk('enlace_desc', d2, t)
    for t in DESTACADOS:
        chk('destacado', t, 'destacado')
    if errores:
        raise SystemExit('\n'.join(errores))


def escribir(nombre, filas, columnas):
    with open(os.path.join(AQUI, nombre), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=columnas)
        w.writeheader()
        w.writerows(filas)


def main():
    validar()
    tipo = {'F': 'Phrase', 'E': 'Exact'}
    escribir('palabras-clave.csv',
             [{'Campaign': CAMPANAS[c]['nombre'], 'Ad Group': g, 'Keyword': k, 'Criterion Type': tipo[m]}
              for c, g, _, kws in GRUPOS for k, m in kws],
             ['Campaign', 'Ad Group', 'Keyword', 'Criterion Type'])
    escribir('negativas.csv',
             [{'Campaign': cfg['nombre'], 'Keyword': k, 'Criterion Type': 'Campaign Negative Phrase'}
              for c, cfg in CAMPANAS.items() for k in NEGATIVAS_COMUNES + NEGATIVAS[c]],
             ['Campaign', 'Keyword', 'Criterion Type'])
    cols = (['Campaign', 'Ad Group', 'Ad type'] + [f'Headline {i}' for i in range(1, 16)]
            + [f'Description {i}' for i in range(1, 5)] + ['Path 1', 'Path 2', 'Final URL'])
    filas = []
    for c, g, titulos, _ in GRUPOS:
        cfg = CAMPANAS[c]
        fila = {'Campaign': cfg['nombre'], 'Ad Group': g, 'Ad type': 'Responsive search ad',
                'Path 1': cfg['ruta'][0], 'Path 2': cfg['ruta'][1], 'Final URL': cfg['url']}
        fila.update({f'Headline {i}': t for i, t in enumerate(titulos + COMUNES[c], 1)})
        fila.update({f'Description {i}': d for i, d in enumerate(DESCRIPCIONES[c], 1)})
        filas.append(fila)
    escribir('anuncios.csv', filas, cols)
    total = sum(cfg['diario'] for cfg in CAMPANAS.values())
    clp = lambda n: f'${n:,}'.replace(',', '.')
    print(f'OK: {sum(len(k) for *_, k in GRUPOS)} palabras clave, {len(GRUPOS)} anuncios, '
          f'presupuesto diario total {clp(total)} CLP (máx. {clp(round(total * 30.4))} CLP al mes)')

if __name__ == '__main__':
    main()
