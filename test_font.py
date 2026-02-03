import os
from moviepy.config import change_settings
from moviepy.editor import TextClip
import font_manager

# === 1. CONFIGURACIÓN DE IMAGEMAGICK (Vital para que funcione) ===
# Buscamos dónde está instalado (Rutas comunes de v7)
POSSIBLE_PATHS = [
    r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe",
    r"C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe",
    r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe",
]

IMAGEMAGICK_BINARY = None
for path in POSSIBLE_PATHS:
    if os.path.exists(path):
        IMAGEMAGICK_BINARY = path
        break

if IMAGEMAGICK_BINARY:
    change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})
    print(f"🔧 ImageMagick encontrado en: {IMAGEMAGICK_BINARY}")
else:
    print("⚠️ ADVERTENCIA: No encontré magick.exe automáticamente.")

# ================================================================

# 2. Obtenemos la fuente y corregimos las barras para Windows
ruta_raw = font_manager.check_and_download_font()
ruta_ok = ruta_raw.replace("\\", "/") # ESTO ES CLAVE

print(f"Probando fuente en ruta corregida: {ruta_ok}")

try:
    # PRUEBA A: Usando la ruta directa al archivo .ttf
    # Si esta sale con letra "gorda", es que la ruta funciona.
    print("📸 Generando prueba con RUTA DE ARCHIVO...")
    clip = TextClip(
        "ZERO (Ruta)", 
        font=ruta_ok, 
        fontsize=100, 
        color='white', 
        size=(1080, 300),
        bg_color='black',
        stroke_color='white', # Truco: un borde del mismo color engrosa la letra
        stroke_width=2
    )
    clip.save_frame("prueba_ruta.png")
    print("✅ ¡Éxito! Mirá 'prueba_ruta.png'")

    # PRUEBA B: Usando el nombre instalado en Windows
    # Si esta sale "gorda", es que Windows la reconoció.
    print("📸 Generando prueba con NOMBRE DE SISTEMA...")
    clip2 = TextClip(
        "ZERO (Sistema)", 
        font="Montserrat-Black", 
        fontsize=100, 
        color='white', 
        size=(1080, 300),
        bg_color='blue'
    )
    clip2.save_frame("prueba_sistema.png")
    print("✅ ¡Éxito! Mirá 'prueba_sistema.png'")

except Exception as e:
    print(f"❌ Error creando imagen: {e}")