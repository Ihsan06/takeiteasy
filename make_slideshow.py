import os
import csv
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import logging
from colorama import Fore, Style
import time
from PIL import Image, ImageDraw, ImageFont

########################################       LOG Section      ########################################

# Initialisiere das Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_with_color(message, color=Fore.WHITE, delay=0.5):
    """Fügt Farben und Verzögerungen zu den Log-Ausgaben hinzu."""
    print(color + message + Style.RESET_ALL)  # Farbiger Text
    time.sleep(delay)  # Verzögerung

########################################       PATH Section      ########################################

# Pfad zur CSV-Datei
csv_file = 'quote/quotes_slideshow.csv'

# Verzeichnis, in dem die Slideshow gespeichert werden soll
output_directory = 'slideshow/output/'

# Verzeichnis, in dem die Bilder gespeichert sind
image_directory = 'image/warrior/'

# Font-Einstellungen
font_path = 'arial.ttf'
font_size = 45

##########################################################################################################

########################################       CSV Section      ##########################################

##########################################################################################################


def get_data_from_csv(csv_file):
    """Liest alle Daten aus der CSV-Datei und gibt sie als Liste von Zeilen zurück."""
    log_with_color(f"\n Lade Daten aus {csv_file} ...\n", Fore.BLUE, 1.5)
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')  # Semikolon als Trennzeichen verwenden
        # Überspringe die erste Zeile (Header/Spaltennamen)
        next(reader, None)
        data = [[entry.replace('\\n', '\n') for entry in row] for row in reader]  # Ersetze \n durch echten Zeilenumbruch
    log_with_color(f"\nEs wurden {len(data)} Zeilen aus der CSV-Datei geladen.\n", Fore.BLUE, 1.5)
    return data


##########################################################################################################

########################################       IMAGE Section      ##########################################

##########################################################################################################

def convert_image_to_png(image_path):
    """Konvertiert ein Bild von .webp oder anderen Formaten zu .png."""
    log_with_color(f"\n Konvertierung des Bildes von .webp zu .png ...\n", Fore.RED, 1.0)
    
    img = Image.open(image_path)
    converted_image_path = image_path.replace('.webp', '.png')  # Für WebP-Konvertierung
    img.save(converted_image_path)
    
    log_with_color(f"\n Bild erfolgreich konvertiert und gespeichert unter: {converted_image_path}\n", Fore.RED, 1.0)
    
    return converted_image_path


def get_random_image():
    """Wählt ein zufälliges Bild aus dem Bildverzeichnis aus und gibt den Bildnamen zurück."""
    log_with_color(f"\n Wähle zufälliges Bild aus dem Verzeichnis {image_directory} ...\n", Fore.MAGENTA, 1.0)

    if not os.path.exists(image_directory):
        log_with_color(f"\n Bildverzeichnis {image_directory} nicht gefunden.\n", Fore.RED, 1.5)
        return None, None

    images = [img for img in os.listdir(image_directory) if img.endswith(('png', 'jpg', 'jpeg', 'webp'))]
    if not images:
        log_with_color(f"\n Keine Bilder im Verzeichnis {image_directory} gefunden.\n", Fore.RED, 1.5)
        return None, None

    chosen_image = os.path.join(image_directory, random.choice(images))

    # Prüfen, ob das Bild im .webp-Format vorliegt, und konvertieren
    if chosen_image.endswith('.webp'):
        chosen_image = convert_image_to_png(chosen_image)  # Konvertierung zu PNG
    
    image_name = os.path.splitext(os.path.basename(chosen_image))[0]  # Bildname ohne Erweiterung
    log_with_color(f"\n Ausgewähltes Bild: {chosen_image}\n", Fore.MAGENTA, 1.0)

    return chosen_image, image_name


def add_text_to_image(image_path, text, output_path):
    """Fügt Text zu einem Bild hinzu und speichert es."""
    log_with_color(f"\n Füge Text hinzu: {text}\n", Fore.YELLOW, 1.0)
    
    # Öffne das Bild
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Verwende die Arial Unicode Schriftart
    font_path = "/Library/Fonts/Arial Unicode.ttf"
    font = ImageFont.truetype(font_path, 60)  # Verwende die TrueType-Schriftart

    # Definiere das Padding und die maximal zulässige Breite für den Text
    padding = 55  # Randabstand
    max_width = img.width - 2 * padding  # Maximale Breite für den Text
    line_padding = 30  # Abstand zwischen den Zeilen

    def wrap_text(text, font, max_width):
        lines = []
        paragraphs = text.split("\n")  # Aufteilen des Textes anhand von Zeilenumbrüchen
        for paragraph in paragraphs:
            words = paragraph.split()
            current_line = ""
            for word in words:
                bbox = font.getbbox(current_line + " " + word)
                line_width = bbox[2] - bbox[0]
                if line_width <= max_width:
                    current_line += " " + word
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)
            lines.append("")  # Leere Zeile hinzufügen, um einen Absatz zu erzeugen
        return lines

    # Wickle den Text um
    wrapped_text = wrap_text(text, font, max_width)

    # Berechne die Höhe des Textblocks
    text_height = sum([font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_text])

    # Berechne die Textposition (mit leicht nach unten verschobenem Startpunkt)
    y_position = (img.height // 3) - (text_height // 3 - 20)
    
    # Füge die schwarze Umrandung für bessere Lesbarkeit hinzu
    for line in wrapped_text:
        text_bbox = font.getbbox(line)
        text_width = text_bbox[2] - text_bbox[0]
        line_height = text_bbox[3] - text_bbox[1]
        x_position = (img.width - text_width) // 2
        
        # Zeichne die Umrandung (in Schwarz) um den Text
        for offset in [(-5, -5), (-5, 5), (5, -5), (5, 5)]:
            draw.text((x_position + offset[0], y_position + offset[1]), line, font=font, fill='black')
        
        # Zeichne den weißen Text
        draw.text((x_position, y_position), line, font=font, fill='white')
        y_position += line_height + line_padding  # Vergrößere den Abstand zwischen den Zeilen

    # Speichere das Bild mit dem Text
    img.save(output_path)
    log_with_color(f"\n Bild mit Text gespeichert unter: {output_path}\n", Fore.GREEN, 1.0)


##########################################################################################################

########################################       SLIDESHOW Section      ##########################################

##########################################################################################################


def create_slideshow(data):
    """Erstellt eine Fotoslideshow basierend auf den CSV-Daten und fügt am Ende einen fixen Text hinzu."""
    log_with_color("\n Starte Erstellung der Slideshow...\n", Fore.GREEN, 1.5)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Für jede Zeile in der CSV
    for idx, row in enumerate(data):
        log_with_color(f"\n Erstelle Slideshow für Zeile {idx + 1}...\n", Fore.YELLOW, 1.5)
        
        # Zufälliges Bild auswählen und Bildnamen erhalten
        image_path, image_name = get_random_image()
        if not image_path:
            log_with_color(f"\n Fehler: Kein Bild für Zeile {idx + 1} gefunden. Überspringe...\n", Fore.RED, 1.5)
            continue
        
        # Für jede Spalte (Text) in der Zeile
        for col_idx, text in enumerate(row):
            # Prüfen, ob der Text leer ist, und nur dann fortfahren, wenn er Inhalt hat
            if text.strip():
                # Erstelle einen Dateinamen für das Bild unter Berücksichtigung des Bildnamens
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = f'{output_directory}/slideshow_{timestamp}_{image_name}_{idx+1}_{col_idx+1}.png'
                
                # Füge den Text dem Bild hinzu und speichere es
                add_text_to_image(image_path, text, output_path)
        
        # Füge am Ende einen fixen Eintrag hinzu (z.B. "Für mehr Content...")
        log_with_color(f"\n Füge fixen Eintrag für Slideshow {idx + 1} hinzu...\n", Fore.YELLOW, 1.5)
        fixed_text = "Folge für mehr Content \n --> \n easyy_mindset :)"
        fixed_output_path = f'{output_directory}/slideshow_{timestamp}_{image_name}_{idx+1}_final.png'
        add_text_to_image(image_path, fixed_text, fixed_output_path)

    log_with_color("\n Slideshow-Erstellung abgeschlossen.\n", Fore.GREEN, 1.5)


##########################################################################################################

########################################       MAIN Section      ##########################################

##########################################################################################################

def main():
    """Hauptfunktion des Programms."""
    
    log_with_color("\n Starte den Hauptprozess...\n", Fore.GREEN, 1.5)

    # Lade Daten aus der CSV und erstelle Slideshow-Bilder
    data = get_data_from_csv(csv_file)
    if data:
        create_slideshow(data)
    else:
        log_with_color("\n Keine Daten in der CSV gefunden.\n", Fore.RED, 1.5)
    
    log_with_color("\n Hauptprozess abgeschlossen.\n", Fore.GREEN, 1.5)

if __name__ == "__main__":
    main()
