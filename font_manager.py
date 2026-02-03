import os
import requests
from pathlib import Path

# URL directa a la fuente Montserrat-Black en Google Fonts (GitHub raw)
FONT_URL = "https://fonts.google.com/specimen/Montserrat"

def check_and_download_font():
    """
    Verifica si existe la fuente. Si no, la descarga.
    Devuelve la RUTA ABSOLUTA (clave para que Windows no falle).
    """
    # Definimos rutas
    base_dir = Path(__file__).parent.resolve()
    fonts_dir = base_dir / "assets" / "fonts"
    font_path = fonts_dir / "Montserrat-Black.ttf"

    # Crear carpeta si no existe
    fonts_dir.mkdir(parents=True, exist_ok=True)

    # Si no existe el archivo, descargarlo
    if not font_path.exists():
        print(f"⬇️ Fuente no encontrada. Descargando Montserrat-Black...")
        try:
            response = requests.get(FONT_URL)
            response.raise_for_status()
            
            with open(font_path, 'wb') as f:
                f.write(response.content)
            print("✅ Fuente descargada correctamente.")
        except Exception as e:
            print(f"❌ Error descargando fuente: {e}")
            # Fallback a Arial si falla la descarga (pero avisando)
            return "Arial"
    else:
        print("✅ Fuente detectada en el sistema.")

    # Retornamos la ruta ABSOLUTA convertida a string
    return str(font_path)

if __name__ == "__main__":
    path = check_and_download_font()
    print(f"Ruta final de la fuente: {path}")