# Publica el sitio y la API en producción (swa-wit-sitio-prod).
# El push a GitHub no despliega: correr este script tras cada push que deba llegar a w-it.cl.
# Requiere: az login hecho y Node (usa npx para la CLI de Static Web Apps).
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

Write-Host 'Pruebas de la API...'
python -m unittest discover -s api/tests
if ($LASTEXITCODE -ne 0) { throw 'Las pruebas de la API fallaron: no se publica.' }

$token = az staticwebapp secrets list -n swa-wit-sitio-prod --query properties.apiKey -o tsv
if (-not $token) { throw 'No se obtuvo el token de despliegue (¿az login?).' }

npx --yes @azure/static-web-apps-cli deploy ./sitio --api-location ./api --api-language python --api-version 3.11 --env production --deployment-token $token
if ($LASTEXITCODE -ne 0) { throw 'swa deploy falló.' }
Write-Host 'Publicado en producción: https://w-it.cl'
