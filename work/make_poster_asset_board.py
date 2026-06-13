from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/david.li/Documents/Codex/2026-06-09/hi-codex-i-need-to-make")
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


BG = (248, 249, 250)
CARD = (255, 255, 255)
INK = (22, 27, 34)
MUTED = (94, 104, 118)
BLUE = (53, 101, 214)
ORANGE = (214, 126, 35)
GREEN = (84, 154, 97)
BORDER = (223, 228, 235)


def rounded_rect(draw, box, radius=24, fill=CARD, outline=BORDER, width=3):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def paste_fit(canvas, img_path, box, bg=(255, 255, 255)):
    img = Image.open(img_path).convert("RGBA")
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    panel = Image.new("RGBA", (w, h), bg + (255,))
    img.thumbnail((w, h), Image.LANCZOS)
    panel.alpha_composite(img, ((w - img.width) // 2, (h - img.height) // 2))
    canvas.alpha_composite(panel, (x0, y0))


def draw_wrapped(draw, text, xy, max_chars, fnt, fill=MUTED, line_gap=8):
    x, y = xy
    for line in wrap(text, max_chars):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def card(canvas, draw, box, title, subtitle, img_path, tag, tag_color, note):
    x0, y0, x1, y1 = box
    rounded_rect(draw, box)
    draw.rounded_rectangle((x0 + 28, y0 + 24, x0 + 158, y0 + 66), radius=18, fill=tag_color)
    draw.text((x0 + 48, y0 + 33), tag, font=font(24, True), fill=(255, 255, 255))
    draw.text((x0 + 180, y0 + 25), title, font=font(36, True), fill=INK)
    draw.text((x0 + 180, y0 + 66), subtitle, font=font(24), fill=MUTED)
    paste_fit(canvas, img_path, (x0 + 28, y0 + 104, x1 - 28, y1 - 120))
    draw.line((x0 + 28, y1 - 102, x1 - 28, y1 - 102), fill=BORDER, width=2)
    draw_wrapped(draw, note, (x0 + 32, y1 - 84), 56, font(23), fill=MUTED, line_gap=5)


canvas = Image.new("RGBA", (2400, 1880), BG + (255,))
draw = ImageDraw.Draw(canvas)

draw.text((80, 56), "IDLM Poster Visual Asset Board", font=font(64, True), fill=INK)
draw.text(
    (80, 128),
    "Use source figures as scientific anchors, but redraw/crop them into one clean poster system.",
    font=font(30),
    fill=MUTED,
)

assets = [
    {
        "title": "Hero Concept",
        "subtitle": "DLM chain vs IDLM compressed chain",
        "img": ROOT / "work/overleaf/images/teaser.png",
        "tag": "HERO",
        "color": ORANGE,
        "note": "Use as the conceptual source, but redraw simpler: 1024 denoising calls -> 16 calls, with the tagline 'Compress the chain, not the distribution.'",
    },
    {
        "title": "Training Mechanism",
        "subtitle": "teacher, fake model, student loss gap",
        "img": ROOT / "work/method_idlm_pipeline_cropped.png",
        "tag": "MAIN",
        "color": BLUE,
        "note": "Center of poster. Redraw with three colors only: frozen teacher, trainable fake model, and student generator. Put the IDLM loss directly below.",
    },
    {
        "title": "Masked Diffusion Result",
        "subtitle": "OpenWebText, MDLM -> IDLM-MDLM",
        "img": ROOT / "work/mdlm_bars_2.png",
        "tag": "DATA",
        "color": GREEN,
        "note": "Right-column primary evidence. Keep the 1024 -> 16 step contrast large; GenPPL and entropy stay visible as paired quality/diversity numbers.",
    },
    {
        "title": "Uniform Diffusion Result",
        "subtitle": "OpenWebText, Duo/DCD -> IDLM",
        "img": ROOT / "work/duo_greedy_bars_2.png",
        "tag": "DATA",
        "color": GREEN,
        "note": "Pair with masked result. Add a small caveat label that IDLM-DCD distills Duo-DCD, so the 4-step story is read correctly.",
    },
    {
        "title": "Entropy Frontier",
        "subtitle": "quality is not just collapse",
        "img": ROOT / "work/owt_genppl_entropy_tradeoff.png",
        "tag": "INSET",
        "color": BLUE,
        "note": "Use small. It supports the claim that low GenPPL is checked against entropy, but it is too dense to be the main results visual.",
    },
    {
        "title": "Sequence Semantics",
        "subtitle": "mixture view for correlations",
        "img": ROOT / "work/overleaf/images/sequence_semantics_mixture.png",
        "tag": "OPT",
        "color": ORANGE,
        "note": "Optional mini-panel only if space remains. Useful for answering 'how can factorized few-step generation keep correlations?'",
    },
]

card_w = 700
card_h = 530
x_positions = [80, 850, 1620]
y_positions = [230, 850]

for idx, item in enumerate(assets):
    x = x_positions[idx % 3]
    y = y_positions[idx // 3]
    card(
        canvas,
        draw,
        (x, y, x + card_w, y + card_h),
        item["title"],
        item["subtitle"],
        item["img"],
        item["tag"],
        item["color"],
        item["note"],
    )

draw.text((80, 1515), "Recommended poster composition", font=font(42, True), fill=INK)
draw.text((80, 1571), "Top band: hero 1024 -> 16. Center: simplified method + theorem. Right: two result bars + TinyGSM strip. Footer: QR links.", font=font(30), fill=MUTED)

layout_y = 1650
layout_x = 80
layout_w = 2240
layout_h = 150
draw.rounded_rectangle((layout_x, layout_y, layout_x + layout_w, layout_y + layout_h), radius=22, fill=(255, 255, 255), outline=BORDER, width=3)
segments = [
    ("Header", 0.08, (220, 220, 220)),
    ("Hero", 0.17, ORANGE),
    ("Motivation", 0.15, (148, 163, 184)),
    ("Method + Theorem", 0.30, BLUE),
    ("Results", 0.30, GREEN),
]
cur = layout_x + 18
usable = layout_w - 36
for name, frac, color in segments:
    w = int(usable * frac)
    draw.rounded_rectangle((cur, layout_y + 24, cur + w - 8, layout_y + 126), radius=16, fill=color)
    fill = (255, 255, 255) if name != "Header" else INK
    draw.text((cur + 18, layout_y + 61), name, font=font(27, True), fill=fill)
    cur += w

out = OUT / "idlm_poster_visual_asset_board.png"
canvas.convert("RGB").save(out, quality=95)
print(out)
