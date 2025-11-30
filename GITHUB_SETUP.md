# 🚀 Comandos para subir a GitHub

## Paso 1: Crear el repositorio en GitHub

Ve a: https://github.com/new

- Repository name: `Bot-monitor-kpi`
- Description: `Bot automatizado para monitorear logo KPI en streams de Twitch`
- Privado o Público (tu elección)
- **NO marques** "Add a README file"
- **NO marques** "Add .gitignore"
- Click "Create repository"

## Paso 2: Ejecuta estos comandos en tu terminal

```powershell
git remote add origin https://github.com/Michelcu/Bot-monitor-kpi.git
git branch -M main
git push -u origin main
```

## Paso 3: Desplegar en Railway

1. Ve a https://railway.app
2. Login con tu cuenta de GitHub (Michelcu)
3. Click "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Busca y selecciona `Bot-monitor-kpi`
6. Railway comenzará a desplegar automáticamente

## Paso 4: Configurar Variables de Entorno en Railway

Una vez desplegado, ve a tu proyecto → "Variables" → "Add Variable":

```
TWITCH_CLIENT_ID=soryjq3qaxsvfayfwm08hutdh4wdk0
TWITCH_CLIENT_SECRET=1ctzmup3yw5i30ziiec1mineosov5w
CHECK_INTERVAL_HOURS=1
DETECTION_THRESHOLD=0.6
DATA_RETENTION_DAYS=30
```

Railway redesplegará automáticamente con las nuevas variables.

## Paso 5: Obtener URL del Dashboard

Railway te dará una URL pública tipo:
`https://bot-monitor-kpi-production.up.railway.app`

¡Ahí podrás ver tu dashboard funcionando 24/7! 🎉

---

**Nota:** El archivo `.env` con tus credenciales NO se sube a GitHub (está en .gitignore), por eso las configuras directamente en Railway.
