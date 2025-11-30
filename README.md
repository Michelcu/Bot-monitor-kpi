# 🎮 Bot Monitor de Logo LFA en Twitch

Bot automatizado que monitorea streams de Twitch para detectar la presencia del logo LFA en transmisiones en vivo. Genera reportes visuales en formato HTML con estadísticas y capturas.

## 🌟 Características

- ✅ Monitoreo automático de múltiples streamers de Twitch
- 🔍 Detección de logo usando OpenCV con template matching
- 📊 Dashboard web con estadísticas en tiempo real
- 📸 Capturas automáticas con anotaciones
- 🗑️ Limpieza automática de datos antiguos (30 días)
- ⏰ Chequeos programados cada hora

## 📋 Requisitos Previos

- Python 3.8 o superior
- Credenciales de Twitch API (Client ID y Client Secret)
- Imagen del logo LFA para detección

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd "c:\Proyectos VScode\IA Logo Rotativo"
```

### 2. Crear entorno virtual (recomendado)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Configurar credenciales

Las credenciales ya están configuradas en el archivo `.env`:

```env
TWITCH_CLIENT_ID=soryjq3qaxsvfayfwm08hutdh4wdk0
TWITCH_CLIENT_SECRET=1ctzmup3yw5i30ziiec1mineosov5w
```

### 5. Guardar el logo de referencia

**IMPORTANTE:** Debes guardar manualmente la imagen del logo LFA en:

```
data/logos/lfa_logo.png
```

### 6. Configurar streamers a monitorear

Edita el archivo `config/streamers.json` y reemplaza los ejemplos con los nombres de usuario reales:

```json
{
  "streamers": [
    "nombre_streamer1",
    "nombre_streamer2",
    "nombre_streamer3"
  ]
}
```

## ▶️ Uso

### Iniciar el bot

```powershell
python main.py
```

El bot:
1. Ejecutará un primer chequeo inmediatamente
2. Abrirá automáticamente el dashboard en tu navegador
3. Continuará monitoreando cada hora
4. Generará capturas y estadísticas automáticamente

### Dashboard

El dashboard se genera en `reports/dashboard.html` y muestra:

- 📈 Estadísticas generales (total chequeos, detecciones, tasa de éxito)
- 👥 Estadísticas por streamer
- 📋 Historial completo de detecciones con capturas
- 🖼️ Miniaturas con anotaciones (logo detectado o no)

Para actualizar el dashboard, simplemente presiona **F5** en tu navegador.

## 📁 Estructura del Proyecto

```
IA Logo Rotativo/
├── main.py                      # Script principal
├── requirements.txt             # Dependencias Python
├── .env                         # Credenciales (NO compartir)
├── .gitignore                  # Archivos ignorados por Git
├── README.md                   # Este archivo
├── config/
│   └── streamers.json          # Lista de streamers a monitorear
├── data/
│   ├── logos/
│   │   └── lfa_logo.png        # Logo de referencia (DEBES GUARDARLO)
│   └── detections.json         # Historial de detecciones
├── reports/
│   ├── dashboard.html          # Dashboard web generado
│   └── screenshots/            # Capturas con anotaciones
└── src/
    ├── twitch_client.py        # Cliente API de Twitch
    ├── logo_detector.py        # Detector de logo con OpenCV
    ├── stream_monitor.py       # Monitor de streams
    └── report_generator.py     # Generador de dashboard HTML
```

## ⚙️ Configuración Avanzada

Puedes modificar estos parámetros en el archivo `.env`:

```env
# Intervalo de chequeo (en horas)
CHECK_INTERVAL_HOURS=1

# Umbral de confianza para detección (0.0 - 1.0)
DETECTION_THRESHOLD=0.6

# Días de retención de datos
DATA_RETENTION_DAYS=30
```

## 🔧 Solución de Problemas

### Error: "No se encontró el logo"
- Asegúrate de guardar el logo en `data/logos/lfa_logo.png`
- Verifica que sea un archivo PNG válido

### Error: "Las credenciales de Twitch no están configuradas"
- Verifica que el archivo `.env` exista en la raíz del proyecto
- Comprueba que las credenciales sean correctas

### No detecta ningún stream
- Verifica que los nombres de usuario en `config/streamers.json` sean correctos
- Asegúrate de que al menos un streamer esté en vivo
- Los nombres deben ser exactos (sin @, sin espacios)

### El logo no se detecta correctamente
- Prueba ajustar el `DETECTION_THRESHOLD` en `.env`
- Valores más bajos (ej: 0.5) detectan más, pero con menos precisión
- Valores más altos (ej: 0.7) son más estrictos

## 📊 Ejemplo de Salida

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║         🎮 BOT MONITOR DE LOGO LFA EN TWITCH 🎮           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

✓ Configuración cargada:
  • Intervalo de chequeo: cada 1 hora(s)
  • Umbral de detección: 0.6
  • Retención de datos: 30 días

============================================================
Iniciando chequeo de streams - 2025-11-30 15:30:45
============================================================
✓ Encontrados 2 stream(s) en vivo

Analizando: NombreStreamer1
  Título: Jugando con el logo LFA
  Espectadores: 150
  ✓ Logo DETECTADO (Confianza: 87.50%)

Analizando: NombreStreamer2
  Título: Stream casual
  Espectadores: 89
  ✗ Logo NO detectado (Confianza: 45.20%)

============================================================
Chequeo completado
============================================================

✓ Dashboard generado: C:\Proyectos VScode\IA Logo Rotativo\reports\dashboard.html

🤖 Bot iniciado y monitoreando...
Próximo chequeo programado en 1 hora(s)
Presiona Ctrl+C para detener el bot
```

## 🛑 Detener el Bot

Presiona `Ctrl+C` en la terminal para detener el bot de forma segura.

## 📝 Notas

- El bot usa la API pública de Twitch, no necesita permisos de los streamers
- Los datos se guardan localmente en tu máquina
- Las capturas se almacenan en `reports/screenshots/`
- El historial se limpia automáticamente después de 30 días

## 🤝 Soporte

Si encuentras problemas:
1. Verifica que todos los archivos de configuración estén presentes
2. Revisa que las dependencias estén instaladas correctamente
3. Comprueba que el logo esté guardado en la ubicación correcta

## 📜 Licencia

Este proyecto es de uso personal.
