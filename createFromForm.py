import svgwrite
from PIL import Image


def create_svg(image_path, square_size, output_svg_path):
    # Bild einlesen
    image = Image.open(image_path)

    # Sicherstellen, dass das Bild im RGBA-Modus ist
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Bildgröße ermitteln
    width, height = image.size

    # SVG Zeichnung erstellen
    dwg = svgwrite.Drawing(output_svg_path, size=(width, height))

    # Jedes Quadrat im Raster durchlaufen
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            # Überprüfen, ob das Quadrat überwiegend schwarz ist
            black_count = 0
            total_count = 0
            for i in range(square_size):
                for j in range(square_size):
                    if x + i < width and y + j < height:
                        pixel = image.getpixel((x + i, y + j))
                        if pixel[3] > 128:  # Alpha-Wert überprüfen
                            total_count += 1
                            if pixel[0] < 128 and pixel[1] < 128 and pixel[2] < 128:  # RGB-Werte für Schwarz überprüfen
                                black_count += 1

            # Quadrat zeichnen, wenn es überwiegend schwarz ist
            if total_count > 0 and black_count / total_count > 0.5:
                dwg.add(dwg.rect(insert=(x, y), size=(square_size, square_size),
                                 fill='white', stroke='black', stroke_width=1))

    # SVG speichern
    dwg.save()


# Beispielaufruf
create_svg('images/308654.png', 25, 'output.svg')
