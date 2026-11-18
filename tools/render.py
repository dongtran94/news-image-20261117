"""Render entry.png: one picture of the world's news on Tuesday 17 November 2026.

Drawn from scratch with Pillow (shapes and DejaVu fonts only), at 2x and then
downsampled for clean edges. Run:  python3 tools/render.py entry.png
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W = H = 1024 * S
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

INK = (24, 24, 28)
PAPER = (247, 243, 233)
RED = (190, 30, 45)
MUTED = (92, 88, 82)
RULE = (40, 40, 44)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size * S)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS_CB = "DejaVuSansCondensed-Bold.ttf"
SANS_C = "DejaVuSansCondensed.ttf"


def p(*v):
    """Scale design-space (1024) coordinates to canvas pixels."""
    return tuple(int(round(x * S)) for x in v)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width * S or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
# Each icon draws inside a box (x, y, w, h) in design-space units.

def icon_mongolia(d, x, y, w, h):
    # podium with microphone, railway track running behind, "$25m?" tag
    cx = x + w / 2
    # rail track
    d.line(p(x + 6, y + h - 22, x + w - 6, y + h - 22), fill=MUTED, width=3 * S)
    d.line(p(x + 6, y + h - 10, x + w - 6, y + h - 10), fill=MUTED, width=3 * S)
    for i in range(10):
        tx = x + 12 + i * (w - 24) / 9
        d.line(p(tx, y + h - 26, tx, y + h - 6), fill=MUTED, width=2 * S)
    # podium
    d.polygon([p(cx - 34, y + 50), p(cx + 34, y + 50), p(cx + 26, y + h - 30), p(cx - 26, y + h - 30)], fill=INK)
    # national emblem roundel on podium (plain gold disc)
    d.ellipse(p(cx - 11, y + 62, cx + 11, y + 84), fill=(214, 170, 60))
    # microphone
    d.line(p(cx, y + 50, cx + 6, y + 24), fill=INK, width=3 * S)
    d.ellipse(p(cx + 1, y + 14, cx + 13, y + 28), fill=INK)
    # exit arrow
    ax = cx + 90
    d.line(p(ax - 22, y + 40, ax + 8, y + 40), fill=RED, width=6 * S)
    d.polygon([p(ax + 8, y + 28), p(ax + 26, y + 40), p(ax + 8, y + 52)], fill=RED)
    # price tag
    d.rounded_rectangle(p(cx - 140, y + 22, cx - 70, y + 50), radius=6 * S, outline=RED, width=3 * S)
    d.text(p(cx - 105, y + 36), "$25m?", font=font(SANS_CB, 15), fill=RED, anchor="mm")
    d.text(p(cx + 100, y + 76), "RESIGNS", font=font(SANS_CB, 14), fill=RED, anchor="mm")


def icon_gulf(d, x, y, w, h):
    # radar dish on a mast, two drones, a burst
    bx, by = x + w * 0.30, y + h - 12
    d.rectangle(p(bx - 30, by - 10, bx + 30, by), fill=INK)
    d.line(p(bx, by - 10, bx, by - 40), fill=INK, width=5 * S)
    # tilted parabolic dish facing up-right, with feed horn
    dish = Image.new("RGBA", p(100, 100), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dish)
    dd.chord(p(5, 30, 95, 90), start=0, end=180, fill=INK + (255,))
    dd.chord(p(12, 22, 88, 78), start=0, end=180, fill=(0, 0, 0, 0))
    dd.line(p(50, 70, 50, 22), fill=INK + (255,), width=3 * S)
    dd.ellipse(p(45, 16, 55, 26), fill=INK + (255,))
    dish = dish.rotate(-30, resample=Image.BICUBIC)
    canvas.alpha_composite(dish, p(bx - 50, by - 104))
    d.text(p(bx, y + 6), "US RADAR", font=font(SANS_CB, 13), fill=MUTED, anchor="mm")
    # intercept burst
    ex, ey = x + w * 0.72, y + 34
    for k in range(12):
        a = k * math.pi / 6
        r1, r2 = 8, 22 if k % 2 == 0 else 15
        d.line(p(ex + r1 * math.cos(a), ey + r1 * math.sin(a), ex + r2 * math.cos(a), ey + r2 * math.sin(a)),
               fill=RED, width=3 * S)
    # drones (delta wings)
    for (dx, dy) in [(x + w * 0.92, y + 24), (x + w * 0.88, y + 64)]:
        d.polygon([p(dx - 22, dy), p(dx + 6, dy - 10), p(dx + 6, dy + 10)], fill=MUTED)
        d.line(p(dx - 32, dy, dx - 22, dy), fill=MUTED, width=2 * S)
    # dashed tracks
    for i in range(4):
        d.line(p(ex + 26 + i * 12, ey + 4 + i * 2, ex + 32 + i * 12, ey + 5 + i * 2), fill=MUTED, width=2 * S)
    # water + tanker
    d.line(p(x + 6, y + h - 4, x + w - 6, y + h - 4), fill=(70, 110, 150), width=3 * S)
    tx = x + w * 0.80
    d.polygon([p(tx - 36, y + h - 30), p(tx + 36, y + h - 30), p(tx + 28, y + h - 8), p(tx - 30, y + h - 8)], fill=INK)
    d.rectangle(p(tx + 14, y + h - 44, tx + 28, y + h - 30), fill=INK)


def icon_apec(d, x, y, w, h):
    # skyline + handshake (two hands as blocks), red and white sleeve cuffs
    base = y + h - 6
    heights = [44, 70, 56, 92, 64, 50, 80, 40]
    bw = (w - 20) / len(heights)
    for i, bh in enumerate(heights):
        bx = x + 10 + i * bw
        d.rectangle(p(bx + 2, base - bh, bx + bw - 2, base), fill=(206, 200, 188))
    cx, cy = x + w / 2, y + h * 0.48
    # left sleeve (red) and right sleeve (dark)
    d.rectangle(p(cx - 92, cy - 14, cx - 46, cy + 14), fill=RED)
    d.rectangle(p(cx + 46, cy - 14, cx + 92, cy + 14), fill=INK)
    # clasped hands
    d.rounded_rectangle(p(cx - 48, cy - 18, cx + 10, cy + 18), radius=12 * S, fill=(222, 178, 140))
    d.rounded_rectangle(p(cx - 10, cy - 14, cx + 48, cy + 22), radius=12 * S, fill=(196, 150, 112))
    for k in range(3):
        d.line(p(cx - 4 + k * 10, cy - 8, cx - 4 + k * 10, cy + 14), fill=(150, 108, 76), width=2 * S)
    d.text(p(x + 2, y + 2), "APEC 2026 · SHENZHEN", font=font(SANS_CB, 14), fill=MUTED, anchor="lt")


def icon_markets(d, x, y, w, h):
    # falling price line with arrow, grid
    for i in range(5):
        gy = y + 10 + i * (h - 20) / 4
        d.line(p(x + 8, gy, x + w - 8, gy), fill=(214, 208, 196), width=1 * S)
    pts = [(0.00, 0.20), (0.12, 0.28), (0.22, 0.22), (0.34, 0.40), (0.46, 0.36),
           (0.58, 0.58), (0.70, 0.52), (0.82, 0.74), (0.92, 0.86)]
    xy = [p(x + 10 + a * (w - 30), y + 10 + b * (h - 20)) for a, b in pts]
    d.line(xy, fill=RED, width=5 * S, joint="curve")
    ex, ey = x + 10 + 0.92 * (w - 30), y + 10 + 0.86 * (h - 20)
    d.polygon([p(ex + 16, ey + 10), p(ex - 8, ey + 6), p(ex + 8, ey - 14)], fill=RED)
    d.text(p(x + 12, y + 14), "NYSE · NASDAQ", font=font(SANS_CB, 14), fill=MUTED, anchor="lm")


def icon_bridges(d, x, y, w, h):
    # river, broken arch bridge, two impact flashes
    wy = y + h - 18
    d.rectangle(p(x + 6, wy, x + w - 6, y + h - 4), fill=(120, 160, 196))
    deck = y + 46
    gap_l, gap_r = x + w * 0.46, x + w * 0.58
    d.rectangle(p(x + 6, deck, gap_l, deck + 10), fill=INK)
    d.rectangle(p(gap_r, deck + 6, x + w - 6, deck + 16), fill=INK)
    for px_ in (x + w * 0.18, x + w * 0.80):
        d.rectangle(p(px_ - 7, deck + 10, px_ + 7, wy), fill=INK)
    # arches
    d.arc(p(x + w * 0.18, deck + 6, x + w * 0.46 + 30, wy + 30), start=180, end=250, fill=INK, width=4 * S)
    d.arc(p(x + w * 0.58 - 30, deck + 12, x + w * 0.80, wy + 30), start=290, end=360, fill=INK, width=4 * S)
    # falling chunks
    for (cx, cy, s) in [(x + w * 0.50, deck + 30, 8), (x + w * 0.54, deck + 52, 6), (x + w * 0.49, deck + 70, 5)]:
        d.rectangle(p(cx - s, cy - s, cx + s, cy + s), fill=INK)
    # impact flashes
    for (fx, fy) in [(x + w * 0.52, deck - 6), (x + w * 0.88, y + 22)]:
        for k in range(10):
            a = k * math.pi / 5
            r2 = 18 if k % 2 == 0 else 11
            d.line(p(fx + 5 * math.cos(a), fy + 5 * math.sin(a), fx + r2 * math.cos(a), fy + r2 * math.sin(a)),
                   fill=RED, width=3 * S)
    d.text(p(x + 10, y + 12), "UA ⇄ RU", font=font(SANS_CB, 14), fill=MUTED, anchor="lm")


def icon_westbank(d, x, y, w, h):
    # tower crane over half-built blocks with a red "blacklisted" stamp
    x, w = x + w / 2 - 150, 330          # this icon is laid out at a fixed width, centred
    base = y + h - 6
    for i, (bw, bh) in enumerate([(46, 50), (40, 72), (52, 38)]):
        bx = x + 14 + i * 58
        d.rectangle(p(bx, base - bh, bx + bw, base), fill=(206, 200, 188), outline=MUTED, width=1 * S)
        for r in range(int(bh // 14)):
            for c in range(int(bw // 14)):
                d.rectangle(p(bx + 4 + c * 14, base - bh + 5 + r * 14, bx + 10 + c * 14, base - bh + 11 + r * 14),
                            fill=MUTED)
    mx = x + 120
    d.line(p(mx, base, mx, y + 14), fill=INK, width=4 * S)
    d.line(p(mx - 40, y + 18, mx + 80, y + 18), fill=INK, width=4 * S)
    d.line(p(mx, y + 6, mx - 40, y + 18), fill=INK, width=2 * S)
    d.line(p(mx, y + 6, mx + 80, y + 18), fill=INK, width=2 * S)
    d.line(p(mx + 64, y + 18, mx + 64, y + 46), fill=INK, width=2 * S)
    # stamp
    sx, sy = x + w - 70, y + h / 2 + 4
    stamp = Image.new("RGBA", p(140, 52), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle(p(2, 2, 138, 50), radius=6 * S, outline=RED + (255,), width=4 * S)
    sd.text(p(70, 26), "UK BAN ×8", font=font(SANS_B, 20), fill=RED + (255,), anchor="mm")
    stamp = stamp.rotate(12, resample=Image.BICUBIC, expand=True)
    canvas.alpha_composite(stamp, p(sx - 75, sy - 35))


# ---------------------------------------------------------------- stories
STORIES = [
    ("MONGOLIA", "Mongolia's president says he will resign",
     "Khurelsukh denies a rival's claim of a $25m railway bribe; parliament must accept", icon_mongolia),
    ("GULF", "Iran drones hit at US radar in Bahrain",
     "Bahrain says attack on Sheikh Isa base intercepted; Iran says two ships hit by mines in Hormuz", icon_gulf),
    ("CHINA / CANADA", "APEC week opens in Shenzhen",
     "CEO summit begins; Xi and Carney agree to widen tariff relief", icon_apec),
    ("MARKETS", "Wall Street slides before Nvidia results",
     "Broad sell-off; China internet stocks at lowest since 2022", icon_markets),
    ("UKRAINE / RUSSIA", "Russia and Ukraine trade strikes on key bridges",
     "Both sides target crossings that carry troops, supplies and commuters", icon_bridges),
    ("WEST BANK", "UK blacklists 8 Israeli settlement builders",
     "Sanctions over West Bank construction; Palestinians say settlers killed a woman, 72, near Jericho", icon_westbank),
]


def main(out_path):
    global canvas
    canvas = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(canvas)

    # masthead
    d.rectangle(p(0, 0, 1024, 10), fill=RED)
    d.text(p(512, 62), "THE WORLD TODAY", font=font(SERIF_B, 66), fill=INK, anchor="mm")
    d.line(p(32, 106, 992, 106), fill=RULE, width=3 * S)
    d.line(p(32, 112, 992, 112), fill=RULE, width=1 * S)
    d.text(p(512, 142), "TUESDAY, 17 NOVEMBER 2026", font=font(SANS_B, 34), fill=RED, anchor="mm")
    d.line(p(32, 172, 992, 172), fill=RULE, width=1 * S)

    # 2 x 3 grid of stories
    top, gx, gy = 184, 32, 12
    cw, ch = (1024 - 2 * gx - 24) / 2, 258
    f_kicker = font(SANS_CB, 17)
    f_head = font(SERIF_B, 27)
    f_deck = font(SANS_C, 17)
    for i, (kicker, head, deck, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = gx + col * (cw + 24)
        y0 = top + row * (ch + gy)
        # panel
        d.rectangle(p(x0, y0, x0 + cw, y0 + ch), fill=(252, 250, 244), outline=(200, 194, 182), width=1 * S)
        # kicker
        d.rectangle(p(x0, y0, x0 + 6, y0 + 28), fill=RED)
        d.text(p(x0 + 14, y0 + 14), kicker, font=f_kicker, fill=RED, anchor="lm")
        # icon area on left
        icon(d, x0 + 20, y0 + 32, cw - 40, 106)
        # headline (full width under icon)
        hy = y0 + 146
        for ln in wrap(d, head, f_head, cw - 24)[:2]:
            d.text(p(x0 + 12, hy), ln, font=f_head, fill=INK, anchor="la")
            hy += 31
        dy = hy + 4
        for ln in wrap(d, deck, f_deck, cw - 24)[:2]:
            d.text(p(x0 + 12, dy), ln, font=f_deck, fill=MUTED, anchor="la")
            dy += 20

    # footer
    d.line(p(32, 998, 992, 998), fill=RULE, width=1 * S)
    d.text(p(512, 1011), "World news of 17 Nov 2026, as reported that day · original illustration",
           font=font(SANS_C, 15), fill=MUTED, anchor="mm")

    img = canvas.convert("RGB").resize((1024, 1024), Image.LANCZOS)
    img.save(out_path, "PNG", optimize=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
