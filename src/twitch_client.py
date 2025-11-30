"""
Cliente para la API de Twitch que maneja autenticación y consultas de streams.
"""
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class TwitchClient:
    """Cliente para interactuar con la API de Twitch."""
    
    def __init__(self):
        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.client_secret = os.getenv('TWITCH_CLIENT_SECRET')
        self.access_token = None
        self.token_expires_at = None
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Las credenciales de Twitch no están configuradas en .env")
    
    def _get_access_token(self):
        """Obtiene un token de acceso OAuth de Twitch."""
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            self.access_token = data['access_token']
            expires_in = data['expires_in']
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
            
            return self.access_token
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo token de acceso: {e}")
            return None
    
    def get_live_streams(self, usernames):
        """
        Obtiene información de streams en vivo para una lista de usuarios.
        
        Args:
            usernames: Lista de nombres de usuario de Twitch
            
        Returns:
            Lista de diccionarios con información de streams activos
        """
        token = self._get_access_token()
        if not token:
            return []
        
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {token}"
        }
        
        # La API de Twitch permite hasta 100 usuarios por consulta
        live_streams = []
        
        for i in range(0, len(usernames), 100):
            batch = usernames[i:i+100]
            url = "https://api.twitch.tv/helix/streams"
            params = {"user_login": batch}
            
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                for stream in data.get('data', []):
                    stream_info = {
                        'user_name': stream['user_name'],
                        'user_login': stream['user_login'],
                        'title': stream['title'],
                        'viewer_count': stream['viewer_count'],
                        'started_at': stream['started_at'],
                        'thumbnail_url': stream['thumbnail_url'],
                        'game_name': stream.get('game_name', 'Sin categoría')
                    }
                    live_streams.append(stream_info)
            except requests.exceptions.RequestException as e:
                print(f"Error consultando streams: {e}")
                continue
        
        return live_streams
    
    def get_thumbnail_url(self, thumbnail_template, width=1920, height=1080):
        """
        Genera URL del thumbnail con dimensiones específicas.
        
        Args:
            thumbnail_template: URL template del thumbnail
            width: Ancho deseado
            height: Alto deseado
            
        Returns:
            URL del thumbnail con dimensiones especificadas
        """
        return thumbnail_template.replace('{width}', str(width)).replace('{height}', str(height))
