import random
import svgwrite
from PIL import Image


def generate_weighted_letter_grid(width, height):
    letters = (
            "E" * 100 +  # 16,11 %
            "N" * 100 +  # 10,33 %
            "I" * 91 +  # 9,05 %
            "R" * 67 +  # 6,72 %
            "T" * 63 +  # 6,34 %
            "S" * 62 +  # 6,23 %
            "A" * 56 +  # 5,60 %
            "H" * 52 +  # 5,20 %
            "D" * 42 +  # 4,17 %
            "U" * 37 +  # 3,70 %
            "C" * 34 +  # 3,40 %
            "L" * 32 +  # 3,24 %
            "G" * 29 +  # 2,94 %
            "M" * 28 +  # 2,80 %
            "O" * 23 +  # 2,32 %
            "B" * 22 +  # 2,19 %
            "F" * 17 +  # 1,71 %
            "W" * 14 +  # 1,39 %
            "Z" * 14 +  # 1,36 %
            "K" * 13 +  # 1,33 %
            "V" * 9 +  # 0,92 %
            "P" * 8 +  # 0,84 %
            "J" * 2 +  # 0,19 %
            "X" * 1 +  # 0,11 %
            "Q" * 1 +  # 0,07 %
            "Y" * 1  # 0,06 %
    )

    return [[random.choice(letters) for _ in range(width)] for _ in range(height)]


def create_svg_with_letters(image_path, square_size, output_svg_path):
    # Bild einlesen und vorbereiten
    image = Image.open(image_path)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    width, height = image.size

    # Gewichtete Buchstaben generieren
    grid_width = width // square_size
    grid_height = height // square_size
    letter_grid = generate_weighted_letter_grid(grid_width, grid_height)

    # SVG Zeichnung erstellen
    dwg = svgwrite.Drawing(output_svg_path, size=(width, height))

    # Schriftgröße basierend auf Quadratgröße festlegen
    font_size = int(square_size * 0.8)

    # Parameter festlegen
    horizontal_offset = 0
    vertical_offset = (0.2852 * square_size) - 0.0254
    stroke_width = 0.2

    # Jedes Quadrat im Raster durchlaufen
    for i in range(grid_height):
        for j in range(grid_width):
            x = j * square_size
            y = i * square_size

            # Farbe des Quadrats überprüfen
            black_count = 0
            total_count = 0
            for dx in range(square_size):
                for dy in range(square_size):
                    if x + dx < width and y + dy < height:
                        pixel = image.getpixel((x + dx, y + dy))
                        if pixel[3] > 128:  # Alpha-Wert
                            total_count += 1
                            if pixel[0] < 128:  # RGB-Werte für Schwarz
                                black_count += 1

            # Quadrat mit Buchstabe füllen, wenn überwiegend schwarz
            if total_count > 0 and black_count / total_count > 0.5:
                group = dwg.g()
                group.add(dwg.rect(insert=(x, y),
                                   size=(square_size, square_size),
                                   fill='white',
                                   stroke='black',
                                   stroke_width=stroke_width,
                                   ))
                # Text zentrieren
                text = dwg.text(letter_grid[i][j],
                                insert=(x + square_size / 2 + horizontal_offset, y + square_size / 2 + vertical_offset),
                                text_anchor="middle",
                                font_size=font_size,
                                font_family="Andika New Basic")
                # Anpassen der Vertikalen Zentrierung
                text['dominant-baseline'] = 'middle'
                group.add(text)
                dwg.add(group)

    # SVG speichern
    dwg.save()

create_svg_with_letters('images/308654.png', 10, 'output_with_letters.svg')
