import os
import csv
import time
from dotenv import load_dotenv
import openai
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
import logging
from colorama import Fore, Style, init

# Initialisiere colorama für Windows-Kompatibilität (nicht nötig für Unix-basierte Systeme)
init(autoreset=True)

# Initialisiere das Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Setze deine OpenAI API-Schlüssel hier
openai.api_key = os.getenv('OPENAI_API_KEY')

# Pfad zur CSV-Datei
csv_file = 'quotes/quotes_example.csv'

def log_with_color(message, color=Fore.WHITE, delay=0.5):
    """Fügt Farben und Verzögerungen zu den Log-Ausgaben hinzu."""
    print(color + message + Style.RESET_ALL)  # Farbiger Text
    time.sleep(delay)  # Verzögerung

def generate_quote():
    """Generiert ein inspirierendes Zitat mit der OpenAI API."""
    log_with_color("Generiere Zitat mit OpenAI API...", Fore.CYAN, 1.5)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Generate an inspirational quote",
        max_tokens=50
    )
    quote = response.choices[0].text.strip()
    log_with_color(f"Generiertes Zitat: {quote}", Fore.GREEN, 1.5)
    return quote

def save_quote_to_csv(quote, csv_file):
    """Speichert das Zitat in einer CSV-Datei."""
    log_with_color(f"Speichere Zitat in {csv_file} ...", Fore.YELLOW, 1.5)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([quote])
    log_with_color(f"Zitat erfolgreich in {csv_file} gespeichert.", Fore.GREEN, 1.5)

def get_quotes_from_csv(csv_file):
    """Liest alle Zitate aus der CSV-Datei und gibt sie als Liste zurück."""
    log_with_color(f"Lade Zitate aus {csv_file} ...", Fore.RED, 1.5)
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        quotes = [row[0] for row in reader]
    log_with_color(f"\n\nEs wurden {len(quotes)} Zitate aus der CSV-Datei geladen.\n\n", Fore.MAGENTA, 1.5)
    return quotes

def create_video_with_quote(quote, output_path):
    """Erstellt ein Video mit dem angegebenen Zitat."""
    log_with_color(f"\n\nErstelle Video für Zitat: {quote}\n\n", Fore.CYAN, 1.5)
    
    # Erstelle einen schwarzen Hintergrundclip
    bg_clip = ColorClip(size=(720, 480), color=(0, 0, 0)).set_duration(10)

    # Erstelle den TextClip
    text_clip = TextClip(quote, fontsize=70, color='white', size=(720, 480))
    text_clip = text_clip.set_duration(10).set_position('center')

    # Kombiniere den TextClip mit dem HintergrundClip
    video = CompositeVideoClip([bg_clip, text_clip])

    log_with_color(f"Schreibe Video zu {output_path} ...", Fore.YELLOW, 1.5)
    video.write_videofile(output_path, fps=24)
    log_with_color(f"Video erfolgreich erstellt: {output_path}", Fore.GREEN, 1.5)

def main():
    """Hauptfunktion des Programms."""
    
    log_with_color("\n\nStarte den Hauptprozess...\n\n", Fore.MAGENTA, 1.5)

    # Lade Zitate aus der CSV und erstelle Videos
    quotes = get_quotes_from_csv(csv_file)
    if quotes:
        for idx, quote in enumerate(quotes):
            output_path = f'output_video_{idx + 1}.mp4'
            create_video_with_quote(quote, output_path)
    else:
        log_with_color("Keine Zitate in der CSV gefunden.", Fore.RED, 1.5)
    
    log_with_color("Hauptprozess abgeschlossen.", Fore.GREEN, 1.5)

if __name__ == "__main__":
    main()
