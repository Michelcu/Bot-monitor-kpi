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
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            padding: 20px;
            color: #f7f2ec;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: #1e1e1e;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(242,23,23,0.3);
            padding: 30px;
            border: 2px solid #f21717;
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
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #f21717 0%, #c71414 100%);
            color: #f7f2ec;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(242,23,23,0.3);
            border: 1px solid #f21717;
        }}
        
        .stat-card h3 {{
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            opacity: 0.9;
        }}
        
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
        }}
        
        .stat-card.success {{
            background: linear-gradient(135deg, #dbbfaf 0%, #c7a58f 100%);
            color: #1e1e1e;
        }}
        
        .stat-card.danger {{
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            border: 2px solid #f21717;
        }}
        
        .section-title {{
            color: #f21717;
            font-size: 1.8em;
            margin: 40px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid #f21717;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            background: #2d2d2d;
            border: 1px solid #3d3d3d;
        }}
        
        th {{
            background: linear-gradient(135deg, #f21717 0%, #c71414 100%);
            color: #f7f2ec;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #3d3d3d;
            color: #f7f2ec;
        }}
        
        tr:hover {{
            background-color: #3d3d3d;
        }}
        
        .thumbnail {{
            width: 150px;
            height: auto;
            border-radius: 5px;
            cursor: pointer;
            transition: transform 0.2s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .thumbnail:hover {{
            transform: scale(1.05);
        }}
        
        .detected {{
            background-color: #2d3d2d;
        }}
        
        .not-detected {{
            background-color: #3d2d2d;
        }}
        
        .status-detected {{
            color: #dbbfaf;
            font-size: 1.5em;
            font-weight: bold;
        }}
        
        .status-not-detected {{
            color: #f21717;
            font-size: 1.5em;
            font-weight: bold;
        }}
        
        .footer {{
            text-align: center;
            color: #dbbfaf;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #3d3d3d;
        }}
        
        .no-data {{
            text-align: center;
            padding: 60px;
            color: #dbbfaf;
            font-size: 1.2em;
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
    <div class="container">
        <h1>
            <img src="../data/logos/kpi_logo.svg" alt="KPI Logo" class="logo-header">
            Monitor de Logo KPI
        </h1>
        <p class="subtitle">Dashboard de Detección en Streams de Twitch</p>
        
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
