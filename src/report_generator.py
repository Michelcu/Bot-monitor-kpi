"""
Generador de dashboard HTML con estadísticas y visualización de detecciones.
"""
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class ReportGenerator:
    """Genera reportes HTML del monitoreo de logos."""
    
    def __init__(self, detections_file='data/detections.json'):
        """
        Inicializa el generador de reportes.
        
        Args:
            detections_file: Ruta al archivo JSON con detecciones
        """
        self.detections_file = Path(detections_file)
        self.detections = self._load_detections()
    
    def _load_detections(self):
        """Carga las detecciones desde el archivo JSON."""
        if self.detections_file.exists():
            try:
                with open(self.detections_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def _calculate_statistics(self):
        """Calcula estadísticas generales de las detecciones."""
        if not self.detections:
            return {
                'total_checks': 0,
                'logo_detected': 0,
                'logo_not_detected': 0,
                'detection_rate': 0.0,
                'streamers_stats': {}
            }
        
        total = len(self.detections)
        detected = sum(1 for d in self.detections if d['logo_detected'])
        
        # Estadísticas por streamer
        streamers_stats = defaultdict(lambda: {'total': 0, 'detected': 0, 'not_detected': 0})
        
        for detection in self.detections:
            streamer = detection['streamer']
            streamers_stats[streamer]['total'] += 1
            if detection['logo_detected']:
                streamers_stats[streamer]['detected'] += 1
            else:
                streamers_stats[streamer]['not_detected'] += 1
        
        # Calcular porcentajes
        for streamer in streamers_stats:
            total_checks = streamers_stats[streamer]['total']
            detected_count = streamers_stats[streamer]['detected']
            streamers_stats[streamer]['rate'] = (detected_count / total_checks * 100) if total_checks > 0 else 0
        
        return {
            'total_checks': total,
            'logo_detected': detected,
            'logo_not_detected': total - detected,
            'detection_rate': (detected / total * 100) if total > 0 else 0,
            'streamers_stats': dict(streamers_stats)
        }
    
    def generate_dashboard(self, output_path='reports/dashboard.html'):
        """
        Genera el dashboard HTML.
        
        Args:
            output_path: Ruta donde guardar el dashboard
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        stats = self._calculate_statistics()
        
        # Ordenar detecciones por fecha (más recientes primero)
        sorted_detections = sorted(
            self.detections, 
            key=lambda x: x['timestamp'], 
            reverse=True
        )
        
        html_content = self._generate_html(stats, sorted_detections)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Dashboard generado: {output_file.absolute()}")
        return str(output_file.absolute())
    
    def _generate_html(self, stats, detections):
        """Genera el contenido HTML del dashboard."""
        
        # Generar filas de la tabla de detecciones
        detection_rows = ""
        for detection in detections:
            timestamp = datetime.fromisoformat(detection['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            status_icon = "✓" if detection['logo_detected'] else "✗"
            status_class = "detected" if detection['logo_detected'] else "not-detected"
            confidence_pct = f"{detection['confidence']:.1%}"
            
            detection_rows += f"""
                <tr class="{status_class}">
                    <td>{timestamp}</td>
                    <td><strong>{detection['streamer']}</strong></td>
                    <td>{detection['title']}</td>
                    <td>{detection['game']}</td>
                    <td>{detection['viewers']}</td>
                    <td class="status-{status_class}">{status_icon}</td>
                    <td>{confidence_pct}</td>
                    <td>
                        <a href="screenshots/{detection['annotated']}" target="_blank">
                            <img src="screenshots/{detection['annotated']}" alt="Screenshot" class="thumbnail">
                        </a>
                    </td>
                </tr>
            """
        
        # Generar filas de estadísticas por streamer
        streamer_stats_rows = ""
        for streamer, stat in stats['streamers_stats'].items():
            streamer_stats_rows += f"""
                <tr>
                    <td><strong>{streamer}</strong></td>
                    <td>{stat['total']}</td>
                    <td class="detected">{stat['detected']}</td>
                    <td class="not-detected">{stat['not_detected']}</td>
                    <td><strong>{stat['rate']:.1f}%</strong></td>
                </tr>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Monitor de Logo KPI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #0a0a0a;
            padding: 0;
            color: #e5e5e5;
            min-height: 100vh;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
            padding: 40px 20px;
            border-bottom: 3px solid #f21717;
            box-shadow: 0 4px 20px rgba(242, 23, 23, 0.3);
        }}
        
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 30px;
        }}
        
        .logo-main {{
            height: 80px;
            width: auto;
            filter: drop-shadow(0 0 20px rgba(242, 23, 23, 0.6));
            animation: pulse 3s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ filter: drop-shadow(0 0 20px rgba(242, 23, 23, 0.6)); }}
            50% {{ filter: drop-shadow(0 0 30px rgba(242, 23, 23, 0.9)); }}
        }}
        
        .header-text {{
            text-align: left;
        }}
        
        .header-text h1 {{
            color: #ffffff;
            font-size: 2.2em;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 5px;
            text-transform: none;
        }}
        
        .header-text .subtitle {{
            color: #999;
            font-size: 0.95em;
            font-weight: 400;
            margin: 0;
            text-align: left;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: transparent;
            padding: 40px 20px;
        }}
        
        h1 {{
            color: #f21717;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-transform: uppercase;
            letter-spacing: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
        }}
        
        .logo-header {{
            height: 60px;
            width: auto;
            filter: drop-shadow(0 0 10px rgba(242,23,23,0.5));
        }}
        
        .subtitle {{
            text-align: center;
            color: #dbbfaf;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 50px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #1a1a1a 0%, #151515 100%);
            color: #e5e5e5;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            border: 1px solid #2a2a2a;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #f21717 0%, #ff3333 100%);
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(242, 23, 23, 0.3);
            border-color: #f21717;
        }}
        
        .stat-card h3 {{
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 15px;
            opacity: 0.7;
            font-weight: 600;
        }}
        
        .stat-card .value {{
            font-size: 3em;
            font-weight: 700;
            line-height: 1;
            color: #ffffff;
        }}
        
        .stat-card.success::before {{
            background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
        }}
        
        .stat-card.success .value {{
            color: #10b981;
        }}
        
        .stat-card.danger::before {{
            background: linear-gradient(90deg, #ef4444 0%, #f87171 100%);
        }}
        
        .stat-card.danger .value {{
            color: #ef4444;
        }}
        
        .section-title {{
            color: #ffffff;
            font-size: 1.5em;
            margin: 50px 0 25px 0;
            padding-bottom: 15px;
            border-bottom: 2px solid #2a2a2a;
            font-weight: 600;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-title::before {{
            content: '';
            width: 4px;
            height: 24px;
            background: linear-gradient(180deg, #f21717 0%, #ff3333 100%);
            border-radius: 2px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            background: #1a1a1a;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}
        
        th {{
            background: #0f0f0f;
            color: #ffffff;
            padding: 18px 20px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #f21717;
        }}
        
        td {{
            padding: 16px 20px;
            border-bottom: 1px solid #252525;
            color: #e5e5e5;
            font-size: 0.95em;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        tr:hover {{
            background-color: #202020;
        }}
        
        .thumbnail {{
            width: 180px;
            height: auto;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.4);
            border: 2px solid transparent;
        }}
        
        .thumbnail:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 20px rgba(242, 23, 23, 0.5);
            border-color: #f21717;
        }}
        
        .detected {{
            background-color: rgba(16, 185, 129, 0.05);
        }}
        
        .not-detected {{
            background-color: rgba(239, 68, 68, 0.05);
        }}
        
        .status-detected {{
            color: #10b981;
            font-size: 1.8em;
            font-weight: bold;
        }}
        
        .status-not-detected {{
            color: #ef4444;
            font-size: 1.8em;
            font-weight: bold;
        }}
        
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 60px;
            padding: 30px 20px;
            border-top: 1px solid #2a2a2a;
            font-size: 0.9em;
        }}
        
        .footer p {{
            margin: 5px 0;
        }}
        
        .no-data {{
            text-align: center;
            padding: 80px 40px;
            color: #666;
            font-size: 1.1em;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            table {{
                font-size: 0.85em;
            }}
            
            .thumbnail {{
                width: 100px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <svg class="logo-main" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1627.51 384.83">
                <defs>
                    <style>.cls-1{{fill:#f21717;}}</style>
                </defs>
                <g>
                    <g>
                        <path class="cls-1" d="M1321.24,1.47l-45.81,88.33C1263.26,53.84,1218.45.39,1146.48.39H481.96c-37.42,98.78-95.3,135.83-163.49,141.78L391.45,0h-218.38L0,331.44c204.51-101.56,402.58-144.77,620.33-185.82,72.69-15.04,126.86-45.41,159.72-93.39h30.68c-16.35,42.32-3.55,69.04,65.78,65.54,211.03-11.54,407.62.37,594.35,28.29L1546.12,1.47h-224.88Z"/>
                        <path class="cls-1" d="M664.19,331.92h-37.32c46.68-159.09-244.67-85.31-406.22,43.85,117.14-50.87,212.17-58.43,177.13,8.52h455.12l18.78-37.1c-22.26-13.79-20.77-34.88-4.18-60.61h248.38c28.59-.57,48.03-.57,62.6-9.89l-56.09,108.14h224.62l107.99-208.2c-390.44-43.87-674.24-7.34-790.81,155.28Z"/>
                    </g>
                    <path class="cls-1" d="M1598.26,58.87c-5.34,0-10.24-1.2-14.68-3.61-4.44-2.41-7.98-5.81-10.61-10.22-2.64-4.4-3.95-9.54-3.95-15.41s1.32-10.99,3.95-15.36c2.63-4.36,6.17-7.77,10.61-10.22,4.44-2.45,9.33-3.67,14.68-3.67s10.33,1.22,14.73,3.67c4.4,2.45,7.92,5.85,10.56,10.22,2.63,4.37,3.95,9.48,3.95,15.36s-1.32,11.01-3.95,15.41c-2.64,4.4-6.15,7.81-10.56,10.22-4.4,2.41-9.31,3.61-14.73,3.61ZM1598.26,52.55c4.29,0,8.15-.94,11.57-2.82,3.42-1.88,6.15-4.55,8.19-8.02,2.03-3.46,3.05-7.49,3.05-12.08s-1.02-8.71-3.05-12.14c-2.03-3.42-4.76-6.08-8.19-7.96-3.43-1.88-7.28-2.82-11.57-2.82s-8.05.94-11.52,2.82c-3.46,1.88-6.21,4.54-8.24,7.96-2.03,3.43-3.05,7.47-3.05,12.14s1.02,8.62,3.05,12.08c2.03,3.46,4.78,6.14,8.24,8.02,3.46,1.88,7.3,2.82,11.52,2.82ZM1588.89,45.77V13.37h10.84c3.91,0,6.74.85,8.47,2.54,1.73,1.69,2.6,3.97,2.6,6.83,0,2.33-.55,4.23-1.64,5.7-1.09,1.47-2.62,2.54-4.57,3.22l7.23,14.11h-6.66l-6.44-13.44h-3.73v13.44h-6.1ZM1595.1,26.92h3.95c1.5,0,2.82-.26,3.95-.79,1.13-.53,1.69-1.66,1.69-3.39s-.56-2.73-1.69-3.22c-1.13-.49-2.45-.73-3.95-.73h-3.95v8.13Z"/>
                </g>
            </svg>
            <div class="header-text">
                <h1>Stream Monitor Dashboard</h1>
                <p class="subtitle">Monitoreo en tiempo real de logo en streams de Twitch</p>
            </div>
        </div>
    </div>
    
    <div class="container">
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total de Chequeos</h3>
                <div class="value">{stats['total_checks']}</div>
            </div>
            <div class="stat-card success">
                <h3>Logo Detectado</h3>
                <div class="value">{stats['logo_detected']}</div>
            </div>
            <div class="stat-card danger">
                <h3>Logo NO Detectado</h3>
                <div class="value">{stats['logo_not_detected']}</div>
            </div>
            <div class="stat-card">
                <h3>Tasa de Detección</h3>
                <div class="value">{stats['detection_rate']:.1f}%</div>
            </div>
        </div>
        
        <h2 class="section-title">📊 Estadísticas por Streamer</h2>
        {"<table><thead><tr><th>Streamer</th><th>Total Chequeos</th><th>Detectado</th><th>No Detectado</th><th>Tasa</th></tr></thead><tbody>" + streamer_stats_rows + "</tbody></table>" if streamer_stats_rows else "<p class='no-data'>No hay datos disponibles aún</p>"}
        
        <h2 class="section-title">🔍 Historial de Detecciones</h2>
        {"<table><thead><tr><th>Fecha/Hora</th><th>Streamer</th><th>Título</th><th>Juego</th><th>Espectadores</th><th>Estado</th><th>Confianza</th><th>Captura</th></tr></thead><tbody>" + detection_rows + "</tbody></table>" if detection_rows else "<p class='no-data'>No hay detecciones registradas aún. El bot agregará datos aquí cuando detecte streams en vivo.</p>"}
        
        <div class="footer">
            <p>Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Bot de Monitoreo de Logo KPI - Presiona F5 para actualizar</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
