"""
Detector de logo usando OpenCV con template matching multi-escala.
"""
import cv2
import numpy as np
from pathlib import Path


class LogoDetector:
    """Detecta logos en imágenes usando template matching."""
    
    def __init__(self, logo_path, threshold=0.6):
        """
        Inicializa el detector de logos.
        
        Args:
            logo_path: Ruta a la imagen del logo de referencia
            threshold: Umbral de confianza para la detección (0-1)
        """
        self.threshold = threshold
        self.logo_template = None
        
        logo_file = Path(logo_path)
        if not logo_file.exists():
            raise FileNotFoundError(f"No se encontró el logo en: {logo_path}")
        
        # Cargar logo en escala de grises
        self.logo_template = cv2.imread(str(logo_file))
        if self.logo_template is None:
            raise ValueError(f"No se pudo cargar la imagen del logo: {logo_path}")
        
        self.logo_gray = cv2.cvtColor(self.logo_template, cv2.COLOR_BGR2GRAY)
        self.logo_height, self.logo_width = self.logo_gray.shape
    
    def detect(self, image_path):
        """
        Detecta el logo en una imagen.
        
        Args:
            image_path: Ruta a la imagen donde buscar el logo
            
        Returns:
            Diccionario con resultado de detección:
            {
                'detected': bool,
                'confidence': float,
                'location': (x, y, w, h) o None,
                'scale': float o None
            }
        """
        # Cargar imagen
        image = cv2.imread(str(image_path))
        if image is None:
            return {
                'detected': False,
                'confidence': 0.0,
                'location': None,
                'scale': None
            }
        
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Realizar template matching en múltiples escalas
        best_match = None
        best_confidence = 0
        best_scale = 1.0
        best_location = None
        
        # Probar diferentes escalas (50% a 150% del tamaño original)
        scales = np.linspace(0.5, 1.5, 20)
        
        for scale in scales:
            # Redimensionar template
            width = int(self.logo_width * scale)
            height = int(self.logo_height * scale)
            
            if width > image_gray.shape[1] or height > image_gray.shape[0]:
                continue
            
            resized_template = cv2.resize(self.logo_gray, (width, height))
            
            # Template matching
            result = cv2.matchTemplate(image_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # Si encontramos un mejor match
            if max_val > best_confidence:
                best_confidence = max_val
                best_location = (*max_loc, width, height)
                best_scale = scale
        
        # Verificar si supera el umbral
        detected = best_confidence >= self.threshold
        
        return {
            'detected': detected,
            'confidence': float(best_confidence),
            'location': best_location if detected else None,
            'scale': float(best_scale) if detected else None
        }
    
    def draw_detection(self, image_path, detection_result, output_path):
        """
        Dibuja un rectángulo alrededor del logo detectado.
        
        Args:
            image_path: Ruta a la imagen original
            detection_result: Resultado del método detect()
            output_path: Ruta donde guardar la imagen anotada
            
        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        image = cv2.imread(str(image_path))
        if image is None:
            return False
        
        if detection_result['detected'] and detection_result['location']:
            x, y, w, h = detection_result['location']
            
            # Dibujar rectángulo verde
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            # Agregar texto con confianza
            confidence_text = f"Confianza: {detection_result['confidence']:.2%}"
            cv2.putText(image, confidence_text, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            # Si no se detectó, agregar texto indicándolo
            text = "Logo NO detectado"
            cv2.putText(image, text, (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        
        # Guardar imagen
        cv2.imwrite(str(output_path), image)
        return True
