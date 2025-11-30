"""
Servidor web simple para servir el dashboard en Railway.
"""
from flask import Flask, send_file, send_from_directory
from pathlib import Path
import threading
import time
from main import run_monitoring_cycle, cleanup_old_data
import schedule
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    """Sirve el dashboard HTML."""
    dashboard_path = Path('reports/dashboard.html')
    if dashboard_path.exists():
        return send_file(dashboard_path)
    return "<h1>Dashboard aún no generado. Espera el primer chequeo...</h1>", 404

@app.route('/screenshots/<path:filename>')
def screenshots(filename):
    """Sirve las capturas de pantalla."""
    return send_from_directory('reports/screenshots', filename)

def run_bot():
    """Ejecuta el bot en segundo plano."""
    print("🤖 Iniciando bot de monitoreo...")
    
    # Ejecutar primer chequeo
    run_monitoring_cycle()
    
    # Configurar chequeos periódicos
    check_interval_hours = int(os.getenv('CHECK_INTERVAL_HOURS', 1))
    data_retention_days = int(os.getenv('DATA_RETENTION_DAYS', 30))
    
    schedule.every(check_interval_hours).hours.do(run_monitoring_cycle)
    schedule.every().day.at("03:00").do(cleanup_old_data, days=data_retention_days)
    
    # Loop del bot
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    # Iniciar bot en thread separado
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Iniciar servidor web
    port = int(os.getenv('PORT', 8080))
    print(f"🌐 Servidor web iniciado en puerto {port}")
    app.run(host='0.0.0.0', port=port)
