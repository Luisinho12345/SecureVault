from PIL import Image, ImageDraw
import customtkinter as ctk


def _blank(size):
    return Image.new("RGBA", (size, size), (0, 0, 0, 0))


def _draw_home(draw, s, c):
    draw.polygon([(s*0.5, s*0.12), (s*0.9, s*0.45), (s*0.75, s*0.45), (s*0.75, s*0.88),
                  (s*0.25, s*0.88), (s*0.25, s*0.45), (s*0.1, s*0.45)], outline=c, width=2)


def _draw_vault(draw, s, c):
    draw.rounded_rectangle([s*0.22, s*0.45, s*0.78, s*0.9], radius=int(s*0.08), outline=c, width=2)
    draw.arc([s*0.32, s*0.1, s*0.68, s*0.55], start=180, end=360, fill=c, width=2)
    draw.ellipse([s*0.44, s*0.6, s*0.56, s*0.72], outline=c, width=2)


def _draw_dice(draw, s, c):
    draw.rounded_rectangle([s*0.15, s*0.15, s*0.85, s*0.85], radius=int(s*0.15), outline=c, width=2)
    for x, y in [(0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7), (0.5, 0.5)]:
        r = s*0.06
        draw.ellipse([s*x-r, s*y-r, s*x+r, s*y+r], fill=c)


def _draw_gear(draw, s, c):
    cx, cy, r = s*0.5, s*0.5, s*0.28
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c, width=2)
    draw.ellipse([cx-r*0.35, cy-r*0.35, cx+r*0.35, cy+r*0.35], outline=c, width=2)
    import math
    for i in range(8):
        angle = i * (360/8)
        x1 = cx + (r+2) * math.cos(math.radians(angle))
        y1 = cy + (r+2) * math.sin(math.radians(angle))
        x2 = cx + (r+s*0.12) * math.cos(math.radians(angle))
        y2 = cy + (r+s*0.12) * math.sin(math.radians(angle))
        draw.line([x1, y1, x2, y2], fill=c, width=3)


def _draw_eye(draw, s, c):
    draw.arc([s*0.05, s*0.15, s*0.95, s*0.85], start=200, end=340, fill=c, width=2)
    draw.arc([s*0.05, s*0.15, s*0.95, s*0.85], start=20, end=160, fill=c, width=2)
    draw.ellipse([s*0.4, s*0.4, s*0.6, s*0.6], outline=c, width=2)


def _draw_eye_off(draw, s, c):
    _draw_eye(draw, s, c)
    draw.line([s*0.1, s*0.1, s*0.9, s*0.9], fill=c, width=2)


def _draw_copy(draw, s, c):
    draw.rounded_rectangle([s*0.12, s*0.28, s*0.62, s*0.78], radius=int(s*0.08), outline=c, width=2)
    draw.rounded_rectangle([s*0.38, s*0.14, s*0.88, s*0.64], radius=int(s*0.08), outline=c, width=2)


def _draw_edit(draw, s, c):
    draw.line([s*0.2, s*0.8, s*0.65, s*0.35], fill=c, width=3)
    draw.polygon([(s*0.65, s*0.35), (s*0.8, s*0.2), (s*0.88, s*0.28), (s*0.73, s*0.43)], fill=c)
    draw.line([s*0.15, s*0.85, s*0.25, s*0.75], fill=c, width=3)


def _draw_trash(draw, s, c):
    draw.line([s*0.2, s*0.3, s*0.8, s*0.3], fill=c, width=2)
    draw.rounded_rectangle([s*0.28, s*0.3, s*0.72, s*0.88], radius=int(s*0.04), outline=c, width=2)
    draw.rectangle([s*0.4, s*0.15, s*0.6, s*0.3], outline=c, width=2)
    for x in (0.4, 0.5, 0.6):
        draw.line([s*x, s*0.4, s*x, s*0.78], fill=c, width=2)


def _draw_logout(draw, s, c):
    draw.rounded_rectangle([s*0.15, s*0.15, s*0.55, s*0.85], radius=int(s*0.06), outline=c, width=2)
    draw.line([s*0.4, s*0.5, s*0.88, s*0.5], fill=c, width=2)
    draw.polygon([(s*0.75, s*0.38), (s*0.9, s*0.5), (s*0.75, s*0.62)], fill=c)


def _draw_search(draw, s, c):
    draw.ellipse([s*0.15, s*0.15, s*0.65, s*0.65], outline=c, width=2)
    draw.line([s*0.6, s*0.6, s*0.88, s*0.88], fill=c, width=3)


def _draw_plus(draw, s, c):
    draw.line([s*0.5, s*0.15, s*0.5, s*0.85], fill=c, width=3)
    draw.line([s*0.15, s*0.5, s*0.85, s*0.5], fill=c, width=3)


def _draw_download(draw, s, c):
    draw.line([s*0.5, s*0.15, s*0.5, s*0.6], fill=c, width=2)
    draw.polygon([(s*0.3, s*0.5), (s*0.7, s*0.5), (s*0.5, s*0.75)], fill=c)
    draw.line([s*0.2, s*0.85, s*0.8, s*0.85], fill=c, width=2)


ICON_DRAWERS = {
    "home": _draw_home,
    "vault": _draw_vault,
    "dice": _draw_dice,
    "gear": _draw_gear,
    "eye": _draw_eye,
    "eye_off": _draw_eye_off,
    "copy": _draw_copy,
    "edit": _draw_edit,
    "trash": _draw_trash,
    "logout": _draw_logout,
    "search": _draw_search,
    "plus": _draw_plus,
    "download": _draw_download,
}

_cache = {}


def make_icon(name, size=20, color="#F8FAFC"):

    key = (name, size, color)

    if key in _cache:
        return _cache[key]

    img = _blank(size)
    draw = ImageDraw.Draw(img)
    ICON_DRAWERS[name](draw, size, color)

    ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
    _cache[key] = ctk_image

    return ctk_image
