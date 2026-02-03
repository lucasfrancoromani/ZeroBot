import audio_engine
import video_engine
import stock_fetcher
from moviepy.editor import concatenate_videoclips, VideoFileClip
import os

def crear_video_zero(id_video, script_texto, tema_visual="dark abstract"):
    """
    Orquesta la creación del video completo.
    """
    print(f"\n🚀 === INICIANDO PRODUCCIÓN: {id_video} ===")

    # 1. CONSEGUIR EL ASSET VISUAL (FONDO)
    print("📥 Descargando material visual de alta calidad...")
    bg_video_path = stock_fetcher.search_and_download_video(tema_visual, f"bg_{id_video}")
    
    if not bg_video_path:
        print("❌ Error fatal: No se pudo descargar el fondo.")
        return

    clips_de_video = []

    # 2. GENERAR CADA ESCENA
    for i, bloque in enumerate(script_texto):
        texto = bloque["texto"]
        print(f"\n🎬 Escena {i+1}: {texto[:30]}...")
        
        # A. Audio
        audio_filename = f"{id_video}_part_{i}"
        audio_path = audio_engine.generate_voice(texto, audio_filename)
        
        if not audio_path:
            continue
        
        # B. Video (Usando el fondo descargado)
        video_temp_name = f"clip_{id_video}_{i}"
        
        # Aquí pasamos el bg_video_path al motor
        video_engine.create_video(texto.upper(), audio_path, video_temp_name, bg_video_path)
        
        # C. Cargar clip
        path_clip = f"output/{video_temp_name}.mp4"
        if os.path.exists(path_clip):
            clip = VideoFileClip(path_clip)
            clips_de_video.append(clip)

    # 3. UNIÓN FINAL
    if clips_de_video:
        print("\n🔗 Uniendo escenas finales...")
        final_video = concatenate_videoclips(clips_de_video)
        final_path = f"output/{id_video}_FINAL.mp4"
        
        final_video.write_videofile(final_path, fps=30, codec="libx264", audio_codec="aac")
        
        print(f"\n✅✅✅ ¡ÉXITO! Video listo en: {final_path}")
        print("➡️  Este video está listo para subirse a TikTok.")
        
        # Limpieza de memoria
        for clip in clips_de_video:
            clip.close()
    else:
        print("⚠️ Algo falló, no hay video final.")

if __name__ == "__main__":
    # === GUION DE PRUEBA REAL (ESTRATEGIA ZERO) ===
    guion_zero = [
        {"texto": "No necesitás más motivación."},
        {"texto": "Necesitás disciplina para cuando no tengas ganas."},
        {"texto": "La motivación es un sentimiento, la disciplina es un sistema."},
        {"texto": "Descargá la guía en el perfil y empezá hoy."}
    ]
    
    # Ejecutar
    # Puedes cambiar "dark abstract" por "storm", "fog", "night city"
    crear_video_zero("ZERO_TEST_FINAL", guion_zero, tema_visual="dark foggy atmosphere")