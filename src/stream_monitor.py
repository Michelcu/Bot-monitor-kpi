"""
Monitor de streams que coordina la captura de thumbnails y detección de logos.
"""
import os
import json
import requests
from datetime import datetime
from pathlib import Path
from .twitch_client import TwitchClient
from .logo_detector import LogoDetector


class StreamMonitor:
    """Monitorea streams de Twitch y detecta logos."""
    
    def __init__(self, streamers_config_path, logo_path, threshold=0.6):
        """
        Inicializa el monitor de streams.
        
        Args:
            streamers_config_path: Ruta al archivo JSON con lista de streamers
            logo_path: Ruta al logo de referencia
            threshold: Umbral de detección
        """
        self.twitch_client = TwitchClient()
        self.logo_detector = LogoDetector(logo_path, threshold)
        
        # Cargar lista de streamers
        with open(streamers_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.streamers = config.get('streamers', [])
        
        # Crear directorios necesarios
        self.reports_dir = Path('reports')
        self.screenshots_dir = self.reports_dir / 'screenshots'
        self.data_dir = Path('data')
        
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.detections_file = self.data_dir / 'detections.json'
        self.detections = self._load_detections()
    
    def _load_detections(self):
        """Carga el historial de detecciones desde el archivo JSON."""
        if self.detections_file.exists():
            try:
                with open(self.detections_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def _save_detections(self):
        """Guarda el historial de detecciones en el archivo JSON."""
        with open(self.detections_file, 'w', encoding='utf-8') as f:
            json.dump(self.detections, f, indent=2, ensure_ascii=False)
    
    def _download_thumbnail(self, url, output_path):
        """
        Descarga un thumbnail de Twitch.
        
        Args:
            url: URL del thumbnail
            output_path: Ruta donde guardar la imagen
            
        Returns:
            True si se descargó correctamente, False en caso contrario
        """
        try:
            # Agregar timestamp para evitar cache
            url_with_timestamp = f"{url}?t={datetime.now().timestamp()}"
            response = requests.get(url_with_timestamp, timeout=10)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error descargando thumbnail: {e}")
            return False
    
    def check_streams(self):
        """
        Verifica los streams activos y detecta el logo.
        
        Returns:
            Diccionario con resultados del chequeo
        """
        print(f"\n{'='*60}")
        print(f"Iniciando chequeo de streams - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Obtener streams en vivo
        live_streams = self.twitch_client.get_live_streams(self.streamers)
        
        if not live_streams:
            print(f"✗ No hay streams activos en este momento")
            print(f"  Streamers monitoreados: {', '.join(self.streamers)}")
            return {
                'timestamp': datetime.now().isoformat(),
                'live_count': 0,
                'checked': [],
                'not_live': self.streamers
            }
        
        print(f"✓ Encontrados {len(live_streams)} stream(s) en vivo\n")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'live_count': len(live_streams),
            'checked': [],
            'not_live': [s for s in self.streamers if s not in [stream['user_login'] for stream in live_streams]]
        }
        
        # Procesar cada stream
        for stream in live_streams:
            print(f"Analizando: {stream['user_name']}")
            print(f"  Título: {stream['title']}")
            print(f"  Espectadores: {stream['viewer_count']}")
            
            # Generar nombres de archivo únicos
            timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
            username = stream['user_login']
            
            thumbnail_filename = f"{username}_{timestamp_str}_thumb.jpg"
            annotated_filename = f"{username}_{timestamp_str}_detected.jpg"
            
            thumbnail_path = self.screenshots_dir / thumbnail_filename
            annotated_path = self.screenshots_dir / annotated_filename
            
            # Descargar thumbnail
            thumbnail_url = self.twitch_client.get_thumbnail_url(
                stream['thumbnail_url'], 
                width=1920, 
                height=1080
            )
            
            if not self._download_thumbnail(thumbnail_url, thumbnail_path):
                print(f"  ✗ Error descargando thumbnail\n")
                continue
            
            # Detectar logo
            detection = self.logo_detector.detect(thumbnail_path)
            
            # Dibujar resultado
            self.logo_detector.draw_detection(thumbnail_path, detection, annotated_path)
            
            # Guardar resultado
            detection_record = {
                'timestamp': datetime.now().isoformat(),
                'streamer': stream['user_name'],
                'streamer_login': stream['user_login'],
                'title': stream['title'],
                'game': stream['game_name'],
                'viewers': stream['viewer_count'],
                'logo_detected': detection['detected'],
                'confidence': detection['confidence'],
                'thumbnail': str(thumbnail_filename),
                'annotated': str(annotated_filename),
                'started_at': stream['started_at']
            }
            
            self.detections.append(detection_record)
            results['checked'].append(detection_record)
            
            # Mostrar resultado
            if detection['detected']:
                print(f"  ✓ Logo DETECTADO (Confianza: {detection['confidence']:.2%})")
            else:
                print(f"  ✗ Logo NO detectado (Confianza: {detection['confidence']:.2%})")
            print()
        
        # Guardar detecciones
        self._save_detections()
        
        print(f"{'='*60}")
        print(f"Chequeo completado")
        print(f"{'='*60}\n")
        
        return results
