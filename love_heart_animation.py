import tkinter as tk
from tkinter import font
import math
import random

# -----------------------------
# SETTINGS
# -----------------------------
WIDTH = 800
HEIGHT = 800
BG = "black"
TEXT_COLOR = "#ff3b30"   # red/orange like the video
FONT_FAMILY = "Arial"

PHRASES = [
    "I love you",
    "Seni seviyorum",
    "Te amo",
    "Je t'aime",
    "Ich liebe dich",
    "Ti amo",
    "Eu te amo",
    "Я тебя люблю",
    "사랑해",
    "愛してる",
    "我爱你",
    "मैं तुमसे प्यार करता हूँ",
    "მე შენ მიყვარხარ",
    "Ik hou van jou",
    "Jag älskar dig",
    "Kocham cię",
    "ฉันรักเธอ",
    "Anh yêu em",
    "Aku cinta kamu",
    "Я тебя кохаю",
]

# -----------------------------
# WINDOW
# -----------------------------
root = tk.Tk()
root.title("Love Heart")
root.configure(bg=BG)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg=BG,
    highlightthickness=0
)
canvas.pack()

# Cache fonts so Tkinter doesn't recreate them repeatedly
fonts = {}

def get_font(size):
    if size not in fonts:
        fonts[size] = font.Font(
            family=FONT_FAMILY,
            size=size,
            weight="bold"
        )
    return fonts[size]


# -----------------------------
# HEART FUNCTION
# Based on the same heart
# parametric equation used in
# the reference video.
# -----------------------------
SCALE = 24
CX = WIDTH // 2
CY = HEIGHT // 2 + 20

def heart(a):
    x = 16 * math.sin(a) ** 3

    y = (
        13 * math.cos(a)
        - 5 * math.cos(2 * a)
        - 2 * math.cos(3 * a)
        - math.cos(4 * a)
    )

    # Flip y because screen coordinates go downward
    return (
        CX + x * SCALE,
        CY - y * SCALE
    )


# -----------------------------
# HEART OUTLINE / MASK
# -----------------------------
outline = [heart(i * 2 * math.pi / 1000)
           for i in range(1000)]


def point_inside_polygon(x, y, polygon):
    """Return True if a point is inside the heart."""
    inside = False
    j = len(polygon) - 1

    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]

        intersects = (
            (yi > y) != (yj > y)
            and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi
        )

        if intersects:
            inside = not inside

        j = i

    return inside


# -----------------------------
# CREATE TEXT POSITIONS
# -----------------------------
random.seed(11)

positions = []

# Generate lots of possible locations inside the heart.
# They are sorted from the upper part toward the lower
# part so the heart gradually appears.
for _ in range(2500):
    x = random.randint(150, WIDTH - 150)
    y = random.randint(120, HEIGHT - 100)

    if point_inside_polygon(x, y, outline):
        positions.append((x, y))

positions.sort(key=lambda p: (p[1], p[0]))


# -----------------------------
# MAKE THE TEXT FIT
# -----------------------------
def text_size(text):
    """Choose a small font size based on phrase length."""
    if len(text) >= 22:
        return 10
    if len(text) >= 16:
        return 11
    if len(text) >= 12:
        return 12
    return 13


# -----------------------------
# ANIMATION
# -----------------------------
index = 0

def draw_next():
    global index

    if index >= len(positions):
        return

    # Put several phrases on screen each frame.
    # This makes the heart build up smoothly.
    amount = 2

    for _ in range(amount):
        if index >= len(positions):
            break

        x, y = positions[index]

        phrase = PHRASES[index % len(PHRASES)]
        size = text_size(phrase)

        canvas.create_text(
            x,
            y,
            text=phrase,
            fill=TEXT_COLOR,
            font=get_font(size),
            anchor="center"
        )

        index += 1

    root.after(35, draw_next)


# -----------------------------
# START
# -----------------------------
draw_next()
root.mainloop()
