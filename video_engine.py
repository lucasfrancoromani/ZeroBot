import os
from pathlib import Path

# === 1. PARCHE DE COMPATIBILIDAD (PILLOW) ===
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

# === 2. CONFIGURACIÓN AUTOMÁTICA (IMAGE MAGICK 7) ===
from moviepy.config import change_settings

# Rutas estándar de ImageMagick 7
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
    print(f"🔧 Motor Gráfico configurado: {IMAGEMAGICK_BINARY}")
else:
    print("⚠️ No encontré magick.exe en rutas estándar. Confiando en el PATH...")

# ==========================================

from moviepy.editor import TextClip, AudioFileClip, CompositeVideoClip, VideoFileClip, ColorClip
import moviepy.video.fx.all as vfx
import font_manager 

def create_video(text, audio_path, output_filename, background_video_path):
    # 1. Fuente
    # Obtenemos la ruta y reemplazamos \ por / para evitar errores
    raw_font_path = font_manager.check_and_download_font()
    font_path = raw_font_path.replace("\\", "/") 
    
    print(f"🔤 Usando fuente en: {font_path}")

    # 2. Audio
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    # 3. Fondo
    if background_video_path and Path(background_video_path).exists():
        bg_clip = VideoFileClip(background_video_path)
        if bg_clip.duration < duration:
            bg_clip = vfx.loop(bg_clip, duration=duration)
        
        bg_clip = bg_clip.subclip(0, duration)
        bg_clip = bg_clip.resize(height=1920)
        bg_clip = bg_clip.crop(x1=bg_clip.w/2 - 540, y1=0, width=1080, height=1920)
        
        # Overlay oscuro (60% opacidad) para que el texto blanco resalte
        dark_layer = ColorClip(size=(1080, 1920), color=(0,0,0)).set_opacity(0.6).set_duration(duration)
        final_bg = CompositeVideoClip([bg_clip, dark_layer])
    else:
        final_bg = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(duration)

    # 4. Texto (LIMPIO, SIN BORDES QUE GENEREN PICOS)
    txt_clip = TextClip(
        text,
        fontsize=90,
        color='white',
        font=font_path,
        method='caption',
        size=(950, None),
        align='Center'
        # Eliminamos stroke_color y stroke_width para evitar los triángulos
    ).set_start(0).set_duration(duration).set_position('center')
    
    # 5. Exportar
    video = CompositeVideoClip([final_bg, txt_clip])
    video.audio = audio
    
    output_path = f"output/{output_filename}.mp4"
    Path("output").mkdir(exist_ok=True)
    
    video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", preset="medium", logger=None)
    
    return output_path