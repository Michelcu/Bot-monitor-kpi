"""
Script principal del bot de monitoreo de logos en Twitch.
Ejecuta chequeos periódicos, genera reportes y limpia datos antiguos.
"""
import os
import webbrowser
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

from src.stream_monitor import StreamMonitor
from src.report_generator import ReportGenerator

# Cargar variables de entorno
load_dotenv()


def cleanup_old_data(days=30):
    """
    Elimina detecciones y capturas más antiguas que el número de días especificado.
    
    Args:
        days: Número de días de retención
    """
    print(f"\n{'='*60}")
    print(f"Limpiando datos antiguos (>{days} días)")
    print(f"{'='*60}")
    
    data_file = Path('data/detections.json')
    screenshots_dir = Path('reports/screenshots')
    
    if not data_file.exists():
        print("✓ No hay datos para limpiar")
        return
    
    import json
    
    # Cargar detecciones
    with open(data_file, 'r', encoding='utf-8') as f:
        detections = json.load(f)
    
    # Calcular fecha límite
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Filtrar detecciones recientes
    original_count = len(detections)
    recent_detections = []
    old_screenshots = []
    
    for detection in detections:
        detection_date = datetime.fromisoformat(detection['timestamp'])
        if detection_date > cutoff_date:
            recent_detections.append(detection)
        else:
            # Marcar screenshots para eliminar
            old_screenshots.append(detection.get('thumbnail'))
            old_screenshots.append(detection.get('annotated'))
    
    # Guardar solo detecciones recientes
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(recent_detections, f, indent=2, ensure_ascii=False)
    
    removed_count = original_count - len(recent_detections)
    print(f"✓ Detecciones eliminadas: {removed_count}")
    
    # Eliminar screenshots antiguos
    deleted_files = 0
    if screenshots_dir.exists():
        for screenshot_name in old_screenshots:
            if screenshot_name:
                screenshot_path = screenshots_dir / screenshot_name
                if screenshot_path.exists():
                    screenshot_path.unlink()
                    deleted_files += 1
    
    print(f"✓ Capturas eliminadas: {deleted_files}")
    print(f"{'='*60}\n")


def run_monitoring_cycle():
    """Ejecuta un ciclo completo de monitoreo."""
    try:
        # Configuración
        threshold = float(os.getenv('DETECTION_THRESHOLD', 0.6))
        
        # Inicializar monitor
        monitor = StreamMonitor(
            streamers_config_path='config/streamers.json',
            logo_path='data/logos/lfa_logo.png',
            threshold=threshold
        )
        
        # Ejecutar chequeo
        results = monitor.check_streams()
        
        # Generar dashboard
        report_gen = ReportGenerator()
        dashboard_path = report_gen.generate_dashboard()
        
        return dashboard_path
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Asegúrate de:")
        print("  1. Guardar el logo en: data/logos/lfa_logo.png")
        print("  2. Configurar streamers en: config/streamers.json")
        return None
    except Exception as e:
        print(f"\n❌ Error en el ciclo de monitoreo: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Función principal del bot."""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║         🏁 BOT MONITOR DE LOGO KPI EN TWITCH 🏁           ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar configuración
    if not os.getenv('TWITCH_CLIENT_ID') or not os.getenv('TWITCH_CLIENT_SECRET'):
        print("❌ Error: Las credenciales de Twitch no están configuradas en .env")
        return
    
    logo_path = Path('data/logos/lfa_logo.png')
    if not logo_path.exists():
        print(f"❌ Error: No se encontró el logo en {logo_path}")
        print("Por favor, guarda la imagen del logo en esa ubicación.")
        return
    
    streamers_config = Path('config/streamers.json')
    if not streamers_config.exists():
        print(f"❌ Error: No se encontró la configuración en {streamers_config}")
        return
    
    # Cargar configuración
    check_interval_hours = int(os.getenv('CHECK_INTERVAL_HOURS', 1))
    data_retention_days = int(os.getenv('DATA_RETENTION_DAYS', 30))
    
    print(f"✓ Configuración cargada:")
    print(f"  • Intervalo de chequeo: cada {check_interval_hours} hora(s)")
    print(f"  • Umbral de detección: {os.getenv('DETECTION_THRESHOLD', 0.6)}")
    print(f"  • Retención de datos: {data_retention_days} días")
    print()
    
    # Ejecutar primer ciclo inmediatamente
    print("Ejecutando primer chequeo...")
    dashboard_path = run_monitoring_cycle()
    
    if dashboard_path:
        # Abrir dashboard en navegador solo si no estamos en Railway
        import os
        if not os.getenv('RAILWAY_ENVIRONMENT'):
            print(f"\n🌐 Abriendo dashboard en navegador...")
            webbrowser.open(f'file:///{dashboard_path}')
        print(f"📊 Dashboard: {dashboard_path}")
    
    # Limpieza inicial
    cleanup_old_data(data_retention_days)
    
    # Programar chequeos periódicos
    schedule.every(check_interval_hours).hours.do(run_monitoring_cycle)
    schedule.every().day.at("03:00").do(cleanup_old_data, days=data_retention_days)
    
    print(f"\n{'='*60}")
    print(f"🤖 Bot iniciado y monitoreando...")
    print(f"{'='*60}")
    print(f"Próximo chequeo programado en {check_interval_hours} hora(s)")
    print(f"Presiona Ctrl+C para detener el bot\n")
    
    # Loop principal
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Chequear cada minuto si hay tareas pendientes
    except KeyboardInterrupt:
        print("\n\n👋 Bot detenido por el usuario")
        print("Hasta luego!")


if __name__ == "__main__":
    main()
