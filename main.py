import os
from dotenv import load_dotenv  # Importiere load_dotenv
import openai
from moviepy.editor import TextClip, CompositeVideoClip

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Setze deine OpenAI API-Schlüssel hier
openai.api_key = os.getenv('OPENAI_API_KEY')  # Hole den API-Schlüssel aus der .env-Datei


def generate_quote():
    """Generiert ein inspirierendes Zitat mit der OpenAI API."""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Generate an inspirational quote",
        max_tokens=50
    )
    return response.choices[0].text.strip()

def create_video_with_quote(quote, output_path):
    """Erstellt ein Video mit dem gegebenen Zitat."""
    
    # Erstelle einen TextClip mit dem Zitat
    text_clip = TextClip(quote, fontsize=70, color='white', size=(720, 480))
    text_clip = text_clip.set_duration(10).set_position('center').set_bg_color('black')

    # Erstelle das Video
    video = CompositeVideoClip([text_clip])
    video.write_videofile(output_path, fps=24)

def main():
    """Hauptfunktion des Programms."""
    
    # Generiere ein Zitat
    quote = generate_quote()
    print(f"Generiertes Zitat: {quote}")

    # Erstelle ein Video mit dem Zitat
    output_path = 'output_video.mp4'
    create_video_with_quote(quote, output_path)
    print(f"Video erstellt: {output_path}")

if __name__ == "__main__":
    main()
