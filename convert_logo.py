"""
Utilidad para convertir el logo SVG a PNG usando inkscape o navegador.
Como alternativa, puedes usar una herramienta online o Inkscape para convertir el SVG a PNG.
"""
from pathlib import Path
import subprocess

def convert_svg_to_png():
    """Instrucciones para convertir el logo SVG a PNG."""
    svg_path = Path('data/logos/kpi_logo.svg')
    png_path = Path('data/logos/lfa_logo.png')
    
    print("="*60)
    print("Para convertir el logo SVG a PNG, tienes 3 opciones:")
    print("="*60)
    print("\n1. Usar una herramienta online:")
    print("   - https://cloudconvert.com/svg-to-png")
    print("   - https://svgtopng.com/")
    print(f"   - Sube: {svg_path.absolute()}")
    print(f"   - Guarda como: {png_path.absolute()}")
    print("   - Tamaño recomendado: 800px de ancho")
    
    print("\n2. Usar Inkscape (si lo tienes instalado):")
    print(f'   inkscape --export-type="png" --export-width=800 "{svg_path.absolute()}" -o "{png_path.absolute()}"')
    
    print("\n3. Abrir el SVG en un navegador y tomar captura:")
    print(f"   - Abre en navegador: {svg_path.absolute()}")
    print("   - Usa herramienta de captura de Windows (Win+Shift+S)")
    print(f"   - Guarda como: {png_path.absolute()}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    convert_svg_to_png()
