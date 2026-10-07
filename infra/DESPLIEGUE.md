# Despliegue en Azure y conexión del formulario con Dynamics 365

```
Navegador ──► Azure Static Web Apps (sitio/)            HTTPS, CDN, dominio
                 └─► /api/contacto  (api/, Python 3.11)  valida, antispam, consentimiento
                        └─► Dataverse Web API ──► Lead en Dynamics 365 Sales
                 └─► /api/postulacion                    "Trabaja con nosotros": valida CV (PDF/Word ≤ 2 MB)
                        └─► Microsoft Graph sendMail ──► postulaciones@w-it.cl (CV adjunto)
```

| Recurso | Nombre propuesto | Notas |
|---|---|---|
| Grupo de recursos | `swa-wit-sitio-prod` | |
| Static Web App | `swa-wit-sitio-prod` | Plan **Standard** (SLA, dominios propios, secretos de app). Región `eastus2` (Static Web Apps no tiene región en Sudamérica). |
| App Registration (Entra ID) | `W-IT Sitio web → Dataverse` | Solo client credentials. Secreto con vencimiento de 12 meses. |
| Usuario de aplicación (Dataverse) | el mismo App Registration | Rol propio mínimo: ver paso 3. |

## 1. Azure

```bash
az login
az account set --subscription "<suscripción de W-IT>"
az group create -n swa-wit-sitio-prod -l eastus2 --tags proyecto=sitio-web owner=marketing
az staticwebapp create -n swa-wit-sitio-prod -g swa-wit-sitio-prod -l eastus2 --sku Standard
az staticwebapp secrets list -n swa-wit-sitio-prod -g swa-wit-sitio-prod --query properties.apiKey -o tsv   # token de despliegue → Azure DevOps
```

## 2. App Registration

```bash
az ad app create --display-name "W-IT Sitio web → Dataverse" --sign-in-audience AzureADMyOrg --query appId -o tsv
az ad sp create --id <appId>
az ad app credential reset --id <appId> --display-name swa-wit-sitio-prod --years 1 --query password -o tsv
```

No necesita permisos de API en Entra: el acceso lo da el usuario de aplicación en Dataverse.
Anotar la fecha de vencimiento del secreto y crear un recordatorio de rotación.

## 3. Dataverse (Power Platform admin center)

1. **Rol de seguridad** nuevo, copiado desde un rol vacío: `Sitio web – Formulario de contacto`
   - Lead (Cliente potencial): **Crear** (unidad de negocio), **Leer** (usuario).
   - Si los leads se asignan a un equipo (`DATAVERSE_OWNER_TEAM_ID`): además **Asignar** en Lead.
   - Nada más: el sitio no puede leer, modificar ni borrar otros registros del CRM.
2. Ambiente → Configuración → Usuarios y permisos → **Usuarios de aplicación** → Nuevo → App Registration del paso 2 → unidad de negocio raíz → rol anterior.

## 3b. Correo de postulaciones (Exchange Online)

"Trabaja con nosotros" envía cada postulación con el CV adjunto a `postulaciones@w-it.cl` usando el mismo App Registration.
El permiso se da con **RBAC para aplicaciones de Exchange**, limitado a un solo buzón: la app no puede enviar como ninguna otra persona.

`postulaciones@w-it.cl` es un **grupo de Microsoft 365** (equipo ":: Postulaciones ::"): sirve como destinatario, pero Graph no envía desde un grupo.
Por eso el remitente es un buzón compartido aparte, solo para el sitio:

1. Exchange admin center → Buzones → **Agregar un buzón compartido**: `sitio-web@w-it.cl` (nombre "W-IT Sitio web"). No necesita licencia ni miembros.
2. El grupo de postulaciones recibe correo del remitente sin cambios (es interno). Recomendado: dejar el equipo como **privado**, porque los CV son datos personales y en un equipo público cualquier persona de W-IT puede unirse y leerlos.
3. **No** agregar `Mail.Send` en los permisos de API de Entra: ese permiso vale para todos los buzones del tenant y se sumaría al de Exchange.
4. En PowerShell de Exchange Online (administrador de Exchange):

```powershell
Connect-ExchangeOnline
New-ServicePrincipal -AppId <appId> -ObjectId <objectId de la aplicación empresarial> -DisplayName "W-IT Sitio web"
New-ManagementScope -Name "Sitio web - remitente" -RecipientRestrictionFilter "PrimarySmtpAddress -eq 'sitio-web@w-it.cl'"
New-ManagementRoleAssignment -App <appId> -Role "Application Mail.Send" -CustomResourceScope "Sitio web - remitente"
Test-ServicePrincipalAuthorization -Identity <appId> -Resource sitio-web@w-it.cl          # InScope = True
Test-ServicePrincipalAuthorization -Identity <appId> -Resource claudio.castillo@w-it.cl   # InScope = False
```

El `objectId` es el de la **aplicación empresarial** (Entra → Aplicaciones empresariales), no el del App Registration.
Los cambios de RBAC pueden tardar hasta 2 horas en aplicarse. El correo no queda en Elementos enviados; "Responder" va directo a la persona que postuló.
Los miembros del equipo ven las postulaciones en el correo del grupo; para recibirlas en su bandeja, cada uno activa "Seguir en la bandeja de entrada".

## 4. Configuración de la Static Web App

```bash
az staticwebapp appsettings set -n swa-wit-sitio-prod -g swa-wit-sitio-prod --setting-names \
  DATAVERSE_URL=https://<org>.crm2.dynamics.com \
  DATAVERSE_TENANT_ID=<tenant> \
  DATAVERSE_CLIENT_ID=<appId> \
  DATAVERSE_CLIENT_SECRET=<secreto> \
  LEAD_SOURCE_CODE=8 \
  POLITICA_VERSION=<fecha de la política vigente> \
  POSTULACIONES_REMITENTE=sitio-web@w-it.cl
# Opcionales: DATAVERSE_OWNER_TEAM_ID=<guid del equipo Comercial>  ALLOWED_ORIGINS=https://w-it.cl,https://www.w-it.cl
#             POSTULACIONES_DESTINO=<otro buzón>  GRAPH_TENANT_ID / GRAPH_CLIENT_ID / GRAPH_CLIENT_SECRET (si se usa otra app; por defecto, las DATAVERSE_*)
```

`LEAD_SOURCE_CODE=8` es "Web" en el conjunto de opciones estándar; confirmar si el ambiente lo personalizó.

## 5. Azure DevOps

1. En `https://dev.azure.com/<organización>`: proyecto nuevo `Sitio web W-IT` (privado). Crea un repo Git con el mismo nombre.
2. Subir el código: `git remote add azure <url del repo>` y `git push azure main`.
3. Pipelines → Library → grupo de variables `sitio-web-prod` → variable `AZURE_STATIC_WEB_APPS_API_TOKEN` = token del paso 1, marcada como secreta (candado).
4. Pipelines → New pipeline → Azure Repos Git → repo → *Existing Azure Pipelines YAML file* → `/azure-pipelines.yml` → Run. La primera vez pide autorizar el grupo de variables.
5. Repos → Branches → `main` → Branch policies: exigir pull request con al menos 1 revisor y que el pipeline pase.

Desde ahí, cada push a `main` corre las pruebas de la API y publica.

## 6. Prueba de punta a punta

1. Abrir `https://<nombre>.azurestaticapps.net/soluciones/contact-center/` → "Conversemos" → enviar el formulario.
2. En Dynamics 365 Sales → Clientes potenciales: debe aparecer `Sitio web · … · <empresa>` con origen Web, la descripción con origen, autodiagnóstico, UTM y consentimiento.
3. Abrir `/nosotros/trabaja-con-nosotros/`, adjuntar un PDF y enviar: debe llegar a `postulaciones@w-it.cl` con asunto `Postulación sitio web · <nombre>`.
4. Revisar errores: Static Web App → Application Insights (o `az staticwebapp functions`), mensajes `contacto:` y `postulacion:`. Los logs no incluyen datos personales.

## Prueba local

```bash
python build/servidor_local.py
```

Sin variables de Dataverse queda en modo prueba e imprime el Lead que crearía. Con las cuatro `DATAVERSE_*` definidas crea el Lead real.
Las postulaciones siempre quedan en modo prueba en local: imprime el correo sin el contenido del CV y no lo envía.

## Pendientes antes de apuntar w-it.cl

- Textos de Cookies y Términos (Administración y Finanzas).
- Cambio de DNS: dominio propio en la Static Web App y luego el CNAME/ALIAS de `www` y el apex.
- Siguiente etapa de seguridad: secreto en Key Vault, CAPTCHA (si llega spam) y Content-Security-Policy.
