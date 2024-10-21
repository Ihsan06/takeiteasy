import os
import csv
import time
import random
from datetime import datetime
from dotenv import load_dotenv
import openai
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ImageClip
import logging
from colorama import Fore, Style, init
from PIL import Image

# Initialisiere colorama für Windows-Kompatibilität (nicht nötig für Unix-basierte Systeme)
init(autoreset=True)

########################################       LOG Section      ########################################

# Initialisiere das Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_with_color(message, color=Fore.WHITE, delay=0.5):
    """Fügt Farben und Verzögerungen zu den Log-Ausgaben hinzu."""
    print(color + message + Style.RESET_ALL)  # Farbiger Text
    time.sleep(delay)  # Verzögerung

########################################       OPENAI Section      ########################################

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Setze deine OpenAI API-Schlüssel hier
openai.api_key = os.getenv('OPENAI_API_KEY')

########################################       PATH Section      ########################################

# Pfad zur CSV-Datei
csv_file = 'quote/quotes_example.csv'

# Verzeichnis, in dem die Videos gespeichert werden sollen
video_directory = 'videos/'

# Verzeichnis, in dem die Bilder gespeichert sind
image_directory = 'image/'

# Verzeichnis, in dem die Audiodatei gespeichert ist
audio_file_path = 'audio/idea10.mp3'  # Beispielpfad zur Audiodatei

##########################################################################################################

########################################       QUOTE Section      ########################################

##########################################################################################################

def generate_quote():
    """Generiert ein inspirierendes Zitat mit der OpenAI API."""
    log_with_color("\nGeneriere Zitat mit OpenAI API...\n", Fore.CYAN, 1.5)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Generate an inspirational quote",
        max_tokens=50
    )
    quote = response.choices[0].text.strip()
    log_with_color(f"\nGeneriertes Zitat: {quote}\n", Fore.GREEN, 1.5)
    return quote

def save_quote_to_csv(quote, csv_file):
    """Speichert das Zitat in einer CSV-Datei."""
    log_with_color(f"\nSpeichere Zitat in {csv_file} ...\n", Fore.YELLOW, 1.5)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([quote])
    log_with_color(f"Zitat erfolgreich in {csv_file} gespeichert.", Fore.MAGENTA, 1.5)

def get_quotes_from_csv(csv_file):
    """Liest alle Zitate aus der CSV-Datei und gibt sie als Liste zurück."""
    log_with_color(f"\nLade Zitate aus {csv_file} ...\n", Fore.RED, 1.5)
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        quotes = [row[0] for row in reader]
    log_with_color(f"\nEs wurden {len(quotes)} Zitate aus der CSV-Datei geladen.\n", Fore.MAGENTA, 1.5)
    return quotes

##########################################################################################################

########################################       Image Section      ########################################

##########################################################################################################

def resize_image(image_path, size=(720, 480)):
    """Öffne ein Bild mit Pillow und ändere die Größe vor der Übergabe an MoviePy."""
    log_with_color(f"\nÄndere die Größe des Bildes {image_path} auf {size} ...\n", Fore.BLUE, 1.0)
    img = Image.open(image_path)
    img = img.resize(size, Image.Resampling.LANCZOS)  # Verwende LANCZOS für bessere Qualität
    resized_image_path = image_path.replace('.webp', '_resized.png')  # Für WebP-Konvertierung oder andere Formate
    img.save(resized_image_path)
    log_with_color(f"\nBild erfolgreich konvertiert und gespeichert unter: {resized_image_path}\n", Fore.GREEN, 1.0)
    return resized_image_path

def get_random_background_image():
    """Wählt ein zufälliges Bild aus dem Hintergrundverzeichnis aus und konvertiert .webp falls nötig."""
    log_with_color(f"\nWähle zufälliges Hintergrundbild aus dem Verzeichnis {image_directory} ...\n", Fore.CYAN, 1.0)
    
    if not os.path.exists(image_directory):
        log_with_color(f"\nHintergrundverzeichnis {image_directory} nicht gefunden.\n", Fore.RED, 1.5)
        return None

    images = [img for img in os.listdir(image_directory) if img.endswith(('png', 'jpg', 'jpeg', 'webp'))]
    if not images:
        log_with_color(f"\nKeine Hintergrundbilder im Verzeichnis {image_directory} gefunden.\n", Fore.RED, 1.5)
        return None

    chosen_image = os.path.join(image_directory, random.choice(images))
    log_with_color(f"\nAusgewähltes Bild: {chosen_image}\n", Fore.YELLOW, 1.0)
    
    # Bildgröße anpassen und konvertieren, falls nötig
    resized_image_path = resize_image(chosen_image)
    return resized_image_path

##########################################################################################################

########################################       VIDEO Section      ########################################

##########################################################################################################

def create_video_with_quote(quote, output_path):
    """Erstellt ein Video mit dem angegebenen Zitat und einer Audiodatei."""
    log_with_color(f"\nErstelle Video für Zitat: {quote}\n", Fore.CYAN, 1.5)

    # Hintergrundbild zufällig auswählen und konvertieren
    resized_image_path = get_random_background_image()
    
    if resized_image_path is None:
        log_with_color("\nKein Hintergrundbild gefunden. Video kann nicht erstellt werden.\n", Fore.RED, 1.5)
        return

    # Erstelle den TextClip
    text_clip = TextClip(quote, fontsize=15, color='black', size=(520, 380))
    text_clip = text_clip.set_duration(10).set_position('center')

    # Erstelle den ImageClip
    image_clip = ImageClip(resized_image_path).set_duration(10)

    # Kombiniere den TextClip mit dem HintergrundClip
    video = CompositeVideoClip([image_clip, text_clip])

    # Lade die Audiodatei
    if os.path.exists(audio_file_path):
        log_with_color(f"\nLade Audiodatei {audio_file_path} ...\n", Fore.CYAN, 1.0)
        audio_clip = AudioFileClip(audio_file_path).set_duration(video.duration)
        # Füge die Audiodatei zum Video hinzu
        video = video.set_audio(audio_clip)
        log_with_color(f"\nAudiodatei {audio_file_path} erfolgreich hinzugefügt.\n", Fore.GREEN, 1.5)
    else:
        log_with_color(f"\nAudiodatei {audio_file_path} nicht gefunden.\n", Fore.RED, 1.5)

    log_with_color(f"\Speichere Video zu {output_path} ...\n", Fore.YELLOW, 1.5)
    video.write_videofile(output_path, fps=24)
    log_with_color(f"\nVideo erfolgreich erstellt: {output_path}\n", Fore.GREEN, 1.5)

##########################################################################################################

########################################       MAIN Section      ########################################

##########################################################################################################    

def main():
    """Hauptfunktion des Programms."""
    
    log_with_color("\nStarte den Hauptprozess...\n", Fore.GREEN, 1.5)

    # Lade Zitate aus der CSV und erstelle Videos
    quotes = get_quotes_from_csv(csv_file)
    if quotes:
        for idx, quote in enumerate(quotes):
            # Erstelle einen Zeitstempel für den Videonamen
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f'{video_directory}/video_{timestamp}_{idx + 1}.mp4'
            create_video_with_quote(quote, output_path)
    else:
        log_with_color("\nKeine Zitate in der CSV gefunden.\n", Fore.RED, 1.5)
    
    log_with_color("\n\nHauptprozess abgeschlossen.\n\n", Fore.GREEN, 1.5)

if __name__ == "__main__":
    main()
