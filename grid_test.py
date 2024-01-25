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
    image = Image.open(image_path)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    width, height = image.size

    gridWidth = width // sqrSize
    gridHeight = height // sqrSize
    letterGrid = generateWeightedLetterGrid(gridWidth, gridHeight)

    return {
        "image": image,
        "width": width,
        "height": height,
        "gridWidth": gridWidth,
        "gridHeight": gridHeight,
        "letterGrid": letterGrid,
        "squareSize": sqrSize
    }

def generateRasterList(grid_height, grid_width, image, sqrSize, width, height):
    rasterList = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

    for i in range(grid_height):
        for j in range(grid_width):
            x = j * sqrSize
            y = i * sqrSize

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

            if totalCount > 0 and blackCount / totalCount > 0.5:
                rasterList[i][j] = 1

    return rasterList

def createSvgWithLetters(outputSvgPath, lineWidth, gData):
    image = gData["image"]
    width = gData["width"]
    height = gData["height"]
    grid_width = gData["gridWidth"]
    grid_height = gData["gridHeight"]
    letterGrid = gData["letterGrid"]
    sqrSize = gData["squareSize"]

    rasterList = generateRasterList(grid_height, grid_width, image, sqrSize, width, height)

    dwg = svgwrite.Drawing(outputSvgPath, size=(width, height))
    fontSize = int(sqrSize * 0.8)
    horizontalOffset = 0
    verticalOffset = (0.2852 * sqrSize) - 0.0254
    stroke_width = lineWidth

    for i in range(grid_height):
        for j in range(grid_width):
            x = j * sqrSize
            y = i * sqrSize

            if rasterList[i][j] == 1:
                group = dwg.g()
                group.add(dwg.rect(insert=(x, y), size=(sqrSize, sqrSize), fill='white', stroke='black', stroke_width=stroke_width))
                text = dwg.text(letterGrid[i][j], insert=(x + sqrSize / 2 + horizontalOffset, y + sqrSize / 2 + verticalOffset), text_anchor="middle", font_size=fontSize, font_family="Andika New Basic")
                text['dominant-baseline'] = 'middle'
                group.add(text)
                dwg.add(group)

    dwg.save()
    return rasterList

# Hier kannst du deine eigene Bildpfad und Quadratgröße einsetzen
imagePath = 'images/308654.png'
squareSize = 20

gridData = createGridData(imagePath, squareSize)

rasterList1 = createSvgWithLetters('output_with_letters_1.svg', 0.2, gridData)
rasterList0 = createSvgWithLetters('output_with_letters_0.svg', 0, gridData)

# Ausgabe der Rasterlisten
for list in rasterList1:
    print(list)

