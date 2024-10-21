import os
import csv
import time
import random
from datetime import datetime
from dotenv import load_dotenv
import openai
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ImageClip, ColorClip
import logging
from colorama import Fore, Style, init
from PIL import Image

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
    log_with_color(f"\n [1/7]] Lade Zitate aus {csv_file} ...\n", Fore.RED, 1.5)
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        quotes = [row[0] for row in reader]
    log_with_color(f"\nEs wurden {len(quotes)} Zitate aus der CSV-Datei geladen.\n", Fore.MAGENTA, 1.5)
    return quotes


##########################################################################################################

########################################       Image Section      ########################################

##########################################################################################################


def resize_image(image_path):
    """Öffne ein Bild mit Pillow und ändere die Größe vor der Übergabe an MoviePy."""
    log_with_color(f"\n [3/7]] Konvertierung des Bildes von .webp zu .png ...\n", Fore.BLUE, 1.0)
    img = Image.open(image_path)
    resized_image_path = image_path.replace('.webp', '.png')  # Für WebP-Konvertierung oder andere Formate
    img.save(resized_image_path)
    log_with_color(f"\nBild erfolgreich konvertiert und gespeichert unter: {resized_image_path}\n", Fore.GREEN, 1.0)
    return resized_image_path

def get_random_background_image():
    """Wählt ein zufälliges Bild aus dem Hintergrundverzeichnis aus und konvertiert .webp falls nötig."""
    log_with_color(f"\n [2/7]] Wähle zufälliges Hintergrundbild aus dem Verzeichnis {image_directory} ...\n", Fore.CYAN, 1.0)
    
    if not os.path.exists(image_directory):
        log_with_color(f"\nHintergrundverzeichnis {image_directory} nicht gefunden.\n", Fore.RED, 1.5)
        return None, None

    images = [img for img in os.listdir(image_directory) if img.endswith(('png', 'jpg', 'jpeg', 'webp'))]
    if not images:
        log_with_color(f"\nKeine Hintergrundbilder im Verzeichnis {image_directory} gefunden.\n", Fore.RED, 1.5)
        return None, None

    chosen_image = os.path.join(image_directory, random.choice(images))
    log_with_color(f"\nAusgewähltes Bild: {chosen_image}\n", Fore.YELLOW, 1.0)

    # Extrahiere den Bildnamen ohne Pfad und Erweiterung
    image_name = os.path.splitext(os.path.basename(chosen_image))[0]

    # Bildgröße anpassen und konvertieren, falls nötig
    resized_image_path = resize_image(chosen_image)
    return resized_image_path, image_name


##########################################################################################################

########################################       VIDEO Section      ########################################

##########################################################################################################


def create_video_with_quote(quote, output_path, resized_image_path, image_name):
    """Erstellt ein Video mit dem angegebenen Zitat und einer Audiodatei."""
    log_with_color(f"\n [4/7]]Erstelle Video für Zitat: {quote}\n", Fore.CYAN, 1.5)

    # Verwende das übergebene Hintergrundbild und den Bildnamen
    
    if resized_image_path is None:
        log_with_color("\nKein Hintergrundbild gefunden. Video kann nicht erstellt werden.\n", Fore.RED, 1.5)
        return

    # Erstelle den ImageClip
    image_clip = ImageClip(resized_image_path).set_duration(10)


########################################       BOX Section      ########################################


    # Füge eine halbtransparente weiße Box mit abgerundeten Ecken hinzu
    box_height = int(1920 * 0.33)  
    box_width = int(1080 * 0.66)

    # Erstelle den BoxClip
    box_clip = ColorClip(size=(box_width, box_height), color=(255, 255, 255)).set_duration(10).set_opacity(0.65)

    # Berechne die neue Y-Position, um die Box auf 2/3 der Höhe zu platzieren
    y_position = int(1920 * (2/5)) - (box_height // 2)  # 2/3 der Höhe minus die Hälfte der Box-Höhe

    # Setze die Box auf 2/3 der Höhe
    box_clip = box_clip.set_position(('center', y_position))


########################################       TEXT Section      ########################################


    # Erstelle den TextClip und füge Padding hinzu, indem die Größe des Textclips etwas verkleinert wird
    text_padding = 25
    text_clip = TextClip(
        quote, 
        fontsize=45, 
        color='black', 
        font='Arial-Bold',
        size=(box_width - text_padding * 2, box_height - text_padding * 2),
        method='caption'
    )
    text_clip = text_clip.set_duration(10).set_position(('center', y_position))

    # Kombiniere den Hintergrund, die Box und den Text
    video = CompositeVideoClip([image_clip, box_clip, text_clip])


########################################       AUDIO Section      ########################################


    # Lade die Audiodatei
    if os.path.exists(audio_file_path):
        log_with_color(f"\n [5/7] Lade Audiodatei {audio_file_path} ...\n", Fore.CYAN, 1.0)
        audio_clip = AudioFileClip(audio_file_path).set_duration(video.duration)
        # Füge die Audiodatei zum Video hinzu
        video = video.set_audio(audio_clip)
        log_with_color(f"\nAudiodatei {audio_file_path} erfolgreich hinzugefügt.\n", Fore.GREEN, 1.5)
    else:
        log_with_color(f"\nAudiodatei {audio_file_path} nicht gefunden.\n", Fore.RED, 1.5)

    log_with_color(f"\n [6/7]]Speichere Video zu {output_path} ...\n", Fore.YELLOW, 1.5)
    video.write_videofile(output_path, fps=24)
    log_with_color(f"\nVideo erfolgreich erstellt: {output_path}\n", Fore.GREEN, 1.5)


##########################################################################################################

########################################       MAIN Section      ########################################

##########################################################################################################    


def main():
    """Hauptfunktion des Programms."""
    
    log_with_color("\n [0/7]] Starte den Hauptprozess...\n", Fore.GREEN, 1.5)

    # Lade Zitate aus der CSV und erstelle Videos
    quotes = get_quotes_from_csv(csv_file)
    if quotes:
        for idx, quote in enumerate(quotes):
            # Hintergrundbild zufällig auswählen
            resized_image_path, image_name = get_random_background_image()
            if resized_image_path and image_name:
                # Erstelle einen Zeitstempel für den Videonamen
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = f'{video_directory}/video_{timestamp}_{image_name}_{idx + 1}.mp4'
                create_video_with_quote(quote, output_path, resized_image_path, image_name)
    else:
        log_with_color("\nKeine Zitate in der CSV gefunden.\n", Fore.RED, 1.5)
    
    log_with_color("\n\n [7/7]]Hauptprozess abgeschlossen.\n\n", Fore.GREEN, 1.5)

if __name__ == "__main__":
    main()
