# 🏁 Bot Monitor KPI - Lista de Tareas

## ✅ Completado

1. ✅ Proyecto configurado y funcionando localmente
2. ✅ Dashboard con paleta de colores KPI
3. ✅ Logo SVG integrado en el dashboard
4. ✅ Archivos para Railway creados:
   - `Procfile`
   - `web_server.py`
   - `railway.json`
   - `.gitignore` actualizado
   - `requirements.txt` actualizado (Flask + opencv-headless)
5. ✅ Repositorio Git inicializado
6. ✅ Primer commit preparado

## 🔄 Siguiente Paso: Subir a GitHub

**Necesitas hacer esto manualmente:**

1. **Crear repositorio en GitHub:**
   - Ve a https://github.com/new
   - Nombre sugerido: `bot-monitor-kpi`
   - Hazlo privado si quieres (recomendado)
   - NO inicialices con README, .gitignore ni licencia

2. **Conectar y subir:**
   ```powershell
   git remote add origin https://github.com/TU_USUARIO/bot-monitor-kpi.git
   git branch -M main
   git push -u origin main
   ```

3. **Desplegar en Railway:**
   - Ve a https://railway.app
   - Login con GitHub
   - "New Project" → "Deploy from GitHub repo"
   - Selecciona `bot-monitor-kpi`
   - Añade las variables de entorno:
     * `TWITCH_CLIENT_ID`
     * `TWITCH_CLIENT_SECRET`
     * `CHECK_INTERVAL_HOURS=1`
     * `DETECTION_THRESHOLD=0.6`
     * `DATA_RETENTION_DAYS=30`

## 📝 Notas

- Git configurado con email/nombre temporal
- Puedes cambiarlos con: `git config user.email "tu_email_real"`
- El archivo `.env` NO se subirá (está en .gitignore)
- Las credenciales se configuran en Railway como variables de entorno
