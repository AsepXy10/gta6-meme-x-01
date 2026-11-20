"""Build meme.png for the make.fun GTA 6 meme bounty.

Composition (1080x1080, must read at 480x480):
  - Background: centre crop of our own game Neon Bay's night-city
    screenshot (the HUD at the edges is cropped away).
  - Top caption: WAITED 13 YEARS / FOR GTA 6
  - Bottom caption: SO MY AI AGENT BUILT / ITS OWN VICE CITY
  - make.fun's ghost, standing on the road in the middle of the scene
    with a soft shadow, and "make.fun" written under it.
The joke: GTA V came out 13 years ago; instead of waiting, an AI agent
built its own Vice City. That is also the make.fun pitch in the meme's
own voice: agents build things and earn real money in bounties there.
"""

from PIL import Image, ImageDraw, ImageFont

SRC = "4-night-base.jpg"          # Neon Bay night screenshot, copied in
GHOST = "ghost-source.png"        # make.fun ghost mark (magenta disc)
OUT = "meme.png"
SIZE = 1080

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fit_font(draw, text, start, max_width):
    size = start
    while size > 20:
        font = ImageFont.truetype(FONT_BOLD, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(FONT_BOLD, 20)


def draw_centered(draw, cx, y, text, font, fill, stroke=6):
    draw.text((cx, y), text, font=font, fill=fill, anchor="ma",
              stroke_width=stroke, stroke_fill=(0, 0, 0))


def main():
    base = Image.open(SRC).convert("RGB")          # 1280x800
    # Centre 800x800 crop: dodges the HUD (money bar, stars, speedo,
    # minimap) that sits at the frame edges.
    crop = base.crop((300, 0, 1100, 800)).resize((SIZE, SIZE), Image.LANCZOS)
    img = crop.convert("RGBA")

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # Caption bars, solid black: the screenshot's mission banner would
    # otherwise ghost through a translucent bar.
    d.rectangle([0, 0, SIZE, 250], fill=(0, 0, 0, 255))
    d.rectangle([0, 828, SIZE, SIZE], fill=(0, 0, 0, 255))
    # Thin neon rules under the top bar / above the bottom bar.
    d.rectangle([0, 250, SIZE, 256], fill=(34, 211, 238, 255))
    d.rectangle([0, 822, SIZE, 828], fill=(255, 46, 166, 255))

    # The ghost, standing on the horizontal road mid-scene.
    ghost = Image.open(GHOST).convert("RGBA").resize((270, 270), Image.LANCZOS)
    gx, gy = 690, 330
    d.ellipse([gx + 25, gy + 245, gx + 245, gy + 275], fill=(0, 0, 0, 140))
    overlay.paste(ghost, (gx, gy), ghost)
    # Name tag under the ghost, so the mark is unmistakable at 480px.
    tag_font = fit_font(d, "make.fun", 54, 300)
    d.text((gx + 135, gy + 278), "make.fun", font=tag_font, fill=(255, 255, 255),
           anchor="ma", stroke_width=4, stroke_fill=(0, 0, 0))

    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)

    # Top caption.
    top1 = fit_font(d, "WAITED 13 YEARS", 104, 1000)
    top2 = fit_font(d, "FOR GTA 6", 104, 1000)
    draw_centered(d, SIZE // 2, 18, "WAITED 13 YEARS", top1, (255, 255, 255))
    draw_centered(d, SIZE // 2, 132, "FOR GTA 6", top2, (34, 211, 238))

    # Bottom caption.
    bot1 = fit_font(d, "SO MY AI AGENT BUILT", 84, 1000)
    bot2 = fit_font(d, "ITS OWN VICE CITY", 84, 1000)
    draw_centered(d, SIZE // 2, 848, "SO MY AI AGENT BUILT", bot1, (255, 255, 255))
    draw_centered(d, SIZE // 2, 946, "ITS OWN VICE CITY", bot2, (255, 46, 166))

    img.convert("RGB").save(OUT, optimize=True)
    print("saved", OUT)

    # 480px legibility preview for the check.
    Image.open(OUT).resize((480, 480), Image.LANCZOS).save("meme-480.png")
    print("saved meme-480.png")


if __name__ == "__main__":
    main()
