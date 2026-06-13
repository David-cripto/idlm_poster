from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


files = sorted(Path("work/slide_previews").glob("slide-*.png"))
thumb_w, thumb_h = 220, 124
label_h = 18
cols = 4
font = ImageFont.load_default()

thumbs = []
for idx, file in enumerate(files, start=1):
    image = Image.open(file).convert("RGB")
    image.thumbnail((thumb_w, thumb_h))
    canvas = Image.new("RGB", (thumb_w, thumb_h + label_h), "white")
    canvas.paste(image, ((thumb_w - image.width) // 2, 0))
    draw = ImageDraw.Draw(canvas)
    draw.text((4, thumb_h + 3), str(idx), fill=(0, 0, 0), font=font)
    thumbs.append(canvas)

rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "white")
for idx, thumb in enumerate(thumbs):
    sheet.paste(thumb, ((idx % cols) * thumb_w, (idx // cols) * (thumb_h + label_h)))

out = Path("work/slide_contact_sheet.jpg")
sheet.save(out, quality=92)
print(f"{len(files)} slides -> {out} {sheet.size}")
