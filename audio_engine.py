import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Cargar claves
load_dotenv()

# Configuración
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

def generate_voice(text: str, filename: str) -> str:
    """
    Genera audio MP3 usando OpenAI TTS con la voz 'onyx'.
    Retorna la ruta del archivo generado.
    """
    print(f"🎙️ Generando voz para: '{text[:30]}...'")
    
    save_path = TEMP_DIR / f"{filename}.mp3"
    
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text,
            speed=1.15  # ⚡ 15% más rápido para retención en TikTok
        )
        
        # Guardar archivo
        response.stream_to_file(save_path)
        print(f"✅ Audio guardado en: {save_path}")
        return str(save_path)
        
    except Exception as e:
        print(f"❌ Error generando audio: {e}")
        return None

if __name__ == "__main__":
    # Prueba rápida si ejecutas este archivo directo
    generate_voice("Esto es una prueba de autoridad. El tiempo no espera a nadie.", "test_zero")