import random
import svgwrite
import subprocess
import os


def generate_weighted_letter_grid(width, height):
    letters = (
            "E" * 100 +   # 16,11 %
            "N" * 100 +   # 10,33 %
            "I" * 91 +    # 9,05 %
            "R" * 67 +    # 6,72 %
            "T" * 63 +    # 6,34 %
            "S" * 62 +    # 6,23 %
            "A" * 56 +    # 5,60 %
            "H" * 52 +    # 5,20 %
            "D" * 42 +    # 4,17 %
            "U" * 37 +    # 3,70 %
            "C" * 34 +    # 3,40 %
            "L" * 32 +    # 3,24 %
            "G" * 29 +    # 2,94 %
            "M" * 28 +    # 2,80 %
            "O" * 23 +    # 2,32 %
            "B" * 22 +    # 2,19 %
            "F" * 17 +    # 1,71 %
            "W" * 14 +    # 1,39 %
            "Z" * 14 +    # 1,36 %
            "K" * 13 +    # 1,33 %
            "V" * 9 +     # 0,92 %
            "P" * 8 +     # 0,84 %
            "J" * 2 +     # 0,19 %
            "X" * 1 +     # 0,11 %
            "Q" * 1 +     # 0,07 %
            "Y" * 1       # 0,06 %
    )

    return [[random.choice(letters) for _ in range(width)] for _ in range(height)]


def create_svg(grid, file_name="word_search.svg", square_size=20):
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    dwg = svgwrite.Drawing(file_name, profile='tiny', size=(width * square_size, height * square_size))
    for i, row in enumerate(grid):
        for j, letter in enumerate(row):
            x = j * square_size
            y = i * square_size
            group = dwg.g()  # Erstellt eine Gruppe für jedes Rechteck und seinen Buchstaben
            group.add(dwg.rect(insert=(x, y), size=(square_size, square_size), fill='white', stroke='black'))
            group.add(dwg.text(letter, insert=(x + square_size / 2, y + square_size / 2 + 5), text_anchor="middle",
                               font_size=14))
            dwg.add(group)
    dwg.save()
    return file_name


# Beispiel: Erstellen eines Rätsels mit angegebener Breite und Höhe
width = 60  # Breite des Gitters
height = 30  # Höhe des Gitters
grid = generate_weighted_letter_grid(width, height)
svg_file = create_svg(grid, "random_letter_grid.svg")

# Finder am Speicherort öffnen (für macOS)
subprocess.Popen(["open", "-R", os.path.abspath(svg_file)])
