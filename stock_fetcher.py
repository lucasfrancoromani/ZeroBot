import os
import requests
import random
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")
HEADERS = {"Authorization": API_KEY}

# Conceptos visuales alineados con ZERO (Oscuro, Brutalista, Minimalista)
SEARCH_TERMS = [
    "dark abstract background",
    "black and white architecture",
    "dark fog",
    "minimalist dark",
    "shadows",
    "night city blur",
    "dark ocean",
    "concrete texture"
]

def search_and_download_video(query_override=None, filename="background_video"):
    """
    Busca un video vertical en Pexels y lo descarga.
    """
    if not API_KEY:
        print("❌ ERROR: No tienes PEXELS_API_KEY en tu archivo .env")
        return None

    # Si no especificamos tema, elige uno al azar de la lista Zero
    query = query_override if query_override else random.choice(SEARCH_TERMS)
    
    print(f"🔎 Buscando video de stock: '{query}'...")

    url = f"https://api.pexels.com/videos/search?query={query}&orientation=portrait&per_page=5&size=medium"
    
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        
        if not data.get("videos"):
            print("⚠️ No se encontraron videos.")
            return None
        
        # Elegimos un video al azar de los resultados
        video_data = random.choice(data["videos"])
        
        # Buscamos la mejor calidad HD (pero liviana para descargar rápido)
        video_files = video_data["video_files"]
        # Filtramos para obtener mp4 y ordenamos por calidad
        best_file = None
        for file in video_files:
            if file["file_type"] == "video/mp4" and file["width"] < 2000: # Evitamos 4K pesados
                best_file = file
                break
        
        if not best_file:
            best_file = video_files[0]

        download_url = best_file["link"]
        save_path = f"assets/{filename}.mp4"
        Path("assets").mkdir(exist_ok=True)

        # Descargar
        with requests.get(download_url, stream=True) as r:
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"✅ Video descargado en: {save_path}")
        return save_path

    except Exception as e:
        print(f"❌ Error descargando video: {e}")
        return None

if __name__ == "__main__":
    # Prueba rápida
    search_and_download_video("dark storm", "test_bg")