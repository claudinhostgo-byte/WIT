# Despliegue en Azure y conexión del formulario con Dynamics 365

```
Navegador ──► Azure Static Web Apps (sitio/)            HTTPS, CDN, dominio
                 └─► /api/contacto  (api/, Python 3.11)  valida, antispam, consentimiento
                        └─► Dataverse Web API ──► Lead en Dynamics 365 Sales
```

| Recurso | Nombre propuesto | Notas |
|---|---|---|
| Grupo de recursos | `rg-wit-sitio-prod` | |
| Static Web App | `swa-wit-sitio-prod` | Plan **Standard** (SLA, dominios propios, secretos de app). Región `eastus2` (Static Web Apps no tiene región en Sudamérica). |
| App Registration (Entra ID) | `W-IT Sitio web → Dataverse` | Solo client credentials. Secreto con vencimiento de 12 meses. |
| Usuario de aplicación (Dataverse) | el mismo App Registration | Rol propio mínimo: ver paso 3. |

## 1. Azure

```bash
az login
az account set --subscription "<suscripción de W-IT>"
az group create -n rg-wit-sitio-prod -l eastus2 --tags proyecto=sitio-web owner=marketing
az staticwebapp create -n swa-wit-sitio-prod -g rg-wit-sitio-prod -l eastus2 --sku Standard
az staticwebapp secrets list -n swa-wit-sitio-prod -g rg-wit-sitio-prod --query properties.apiKey -o tsv   # token de despliegue → Azure DevOps
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

## 4. Configuración de la Static Web App

```bash
az staticwebapp appsettings set -n swa-wit-sitio-prod -g rg-wit-sitio-prod --setting-names \
  DATAVERSE_URL=https://<org>.crm2.dynamics.com \
  DATAVERSE_TENANT_ID=<tenant> \
  DATAVERSE_CLIENT_ID=<appId> \
  DATAVERSE_CLIENT_SECRET=<secreto> \
  LEAD_SOURCE_CODE=8 \
  POLITICA_VERSION=<fecha de la política vigente>
# Opcionales: DATAVERSE_OWNER_TEAM_ID=<guid del equipo Comercial>  ALLOWED_ORIGINS=https://w-it.cl,https://www.w-it.cl
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
3. Revisar errores: Static Web App → Application Insights (o `az staticwebapp functions`), mensajes `contacto:`. Los logs no incluyen datos personales.

## Prueba local

```bash
python build/servidor_local.py
```

Sin variables de Dataverse queda en modo prueba e imprime el Lead que crearía. Con las cuatro `DATAVERSE_*` definidas crea el Lead real.

## Pendientes antes de apuntar w-it.cl

- Textos de Cookies y Términos (Administración y Finanzas).
- Cambio de DNS: dominio propio en la Static Web App y luego el CNAME/ALIAS de `www` y el apex.
- Siguiente etapa de seguridad: secreto en Key Vault, CAPTCHA (si llega spam) y Content-Security-Policy.
