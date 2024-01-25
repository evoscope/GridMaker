import random
import svgwrite
from PIL import Image


def generateWeightedLetterGrid(width, height):
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


def createGridData(image_path, sqrSize):
    # Bild einlesen und vorbereiten
    image = Image.open(image_path)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    width, height = image.size

    # Gewichtete Buchstaben generieren
    gridWidth = width // sqrSize
    gridHeight = height // sqrSize
    letterGrid = generateWeightedLetterGrid(gridWidth, gridHeight)

    return {"image": image,
            "width": width,
            "height": height,
            "gridWidth": gridWidth,
            "gridHeight": gridHeight,
            "letterGrid": letterGrid,
            "squareSize": sqrSize}


def createSvgWithLetters(outputSvgPath, lineWidth, gridData):
    image = gridData["image"]
    width = gridData["width"]
    height = gridData["height"]
    grid_width = gridData["gridWidth"]
    grid_height = gridData["gridHeight"]
    letterGrid = gridData["letterGrid"]
    sqrSize = gridData["squareSize"]

    # SVG Zeichnung erstellen
    dwg = svgwrite.Drawing(outputSvgPath, size=(width, height))

    # Schriftgröße basierend auf Quadratgröße festlegen
    fontSize = int(sqrSize * 0.8)

    # Parameter festlegen
    horizontalOffset = 0
    verticalOffset = (0.2852 * sqrSize) - 0.0254
    stroke_width = lineWidth

    # Jedes Quadrat im Raster durchlaufen
    for i in range(grid_height):
        for j in range(grid_width):
            x = j * sqrSize
            y = i * sqrSize

            # Farbe des Quadrats überprüfen
            blackCount = 0
            totalCount = 0
            for dx in range(sqrSize):
                for dy in range(sqrSize):
                    if x + dx < width and y + dy < height:
                        pixel = image.getpixel((x + dx, y + dy))
                        if pixel[3] > 128:  # Alpha-Wert
                            totalCount += 1
                            if pixel[0] < 128:  # RGB-Werte für Schwarz
                                blackCount += 1

            # Quadrat mit Buchstabe füllen, wenn überwiegend schwarz
            if totalCount > 0 and blackCount / totalCount > 0.5:
                group = dwg.g()
                group.add(dwg.rect(insert=(x, y),
                                   size=(sqrSize, sqrSize),
                                   fill='white',
                                   stroke='black',
                                   stroke_width=stroke_width,
                                   ))
                # Text zentrieren
                text = dwg.text(letterGrid[i][j],
                                insert=(x + sqrSize / 2 + horizontalOffset, y + sqrSize / 2 + verticalOffset),
                                text_anchor="middle",
                                font_size=fontSize,
                                font_family="Andika New Basic")
                # Anpassen der Vertikalen Zentrierung
                text['dominant-baseline'] = 'middle'
                group.add(text)
                dwg.add(group)

    # SVG speichern
    dwg.save()


imagePath = 'images/308654.png'
squareSize = 50

gridData = createGridData(imagePath, squareSize)

createSvgWithLetters('output_with_letters_1.svg', 0.2, gridData)
createSvgWithLetters('output_with_letters_0.svg', 0, gridData)
