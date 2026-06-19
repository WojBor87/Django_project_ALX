from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "class_diagram.png"
W, H = 1720, 980

BG = "white"
BORDER = "#111827"
HEADER = "#eef2ff"
TEXT = "#111827"
MUTED = "#6b7280"
DASHED = "#6b7280"


def load_font(paths, size):
    for path in paths:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            pass
    return ImageFont.load_default()


TITLE_FONT = load_font([r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"], 30)
CLASS_FONT = load_font([r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"], 22)
BODY_FONT = load_font([r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"], 16)
SMALL_FONT = load_font([r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"], 14)


def centered(draw, x, y, text, font, fill=TEXT):
    box = draw.textbbox((0, 0), text, font=font)
    draw.text((x - (box[2] - box[0]) / 2, y - (box[3] - box[1]) / 2), text, font=font, fill=fill)


def label(draw, x, y, text, fill=MUTED):
    box = draw.textbbox((0, 0), text, font=SMALL_FONT)
    draw.rounded_rectangle([x - 5, y - 2, x + box[2] - box[0] + 5, y + box[3] - box[1] + 2], radius=5, fill="white")
    draw.text((x, y), text, font=SMALL_FONT, fill=fill)


def draw_class(draw, x, y, w, h, name, attrs, methods=()):
    header_h = 48
    draw.rectangle([x, y, x + w, y + h], fill="white", outline=BORDER, width=2)
    draw.rectangle([x, y, x + w, y + header_h], fill=HEADER, outline=BORDER, width=2)
    centered(draw, x + w / 2, y + header_h / 2, name, CLASS_FONT)

    attr_y = y + header_h + 12
    for i, attr in enumerate(attrs):
        draw.text((x + 16, attr_y + i * 22), attr, font=BODY_FONT, fill=TEXT)

    if methods:
        method_y = attr_y + len(attrs) * 22 + 10
        draw.line([x, method_y - 6, x + w, method_y - 6], fill=BORDER, width=1)
        for i, method in enumerate(methods):
            draw.text((x + 16, method_y + i * 22), method, font=BODY_FONT, fill=TEXT)


def dashed_line(draw, p1, p2, color=DASHED, width=2):
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    dist = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / dist, dy / dist
    t = 0
    while t < dist:
        e = min(t + 12, dist)
        draw.line([x1 + ux * t, y1 + uy * t, x1 + ux * e, y1 + uy * e], fill=color, width=width)
        t += 20


def diamond(draw, center, vertical=True):
    x, y = center
    if vertical:
        points = [(x, y - 12), (x + 9, y), (x, y + 12), (x - 9, y)]
    else:
        points = [(x - 12, y), (x, y - 9), (x + 12, y), (x, y + 9)]
    draw.polygon(points, fill=BORDER, outline=BORDER)


def association(draw, p1, p2, start_mult, end_mult, text, dashed=False, composition=False, label_pos=None):
    if dashed:
        dashed_line(draw, p1, p2)
    else:
        draw.line([p1, p2], fill=BORDER, width=2)
    if composition:
        diamond(draw, (p1[0] + (p2[0] - p1[0]) * 0.12, p1[1] + (p2[1] - p1[1]) * 0.12), vertical=p1[0] == p2[0])
    label(draw, p1[0] + 4, p1[1] - 18, start_mult, DASHED if dashed else MUTED)
    label(draw, p2[0] - 34, p2[1] - 18, end_mult, DASHED if dashed else MUTED)
    if label_pos:
        label(draw, label_pos[0], label_pos[1], text, DASHED if dashed else MUTED)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    centered(draw, W / 2, 40, "Diagram klas DevBoard", TITLE_FONT)
    centered(draw, W / 2, 72, "Uproszczony diagram UML na podstawie `devboard.models`", SMALL_FONT, MUTED)

    draw_class(draw, 80, 110, 320, 210, "User", ["- id: int", "- username: str", "- email: str"])
    draw_class(draw, 500, 100, 420, 250, "Project", ["- name: str", "- description: text", "- owner: User", "- created_at: datetime", "- updated_at: datetime"], ["+ task_count(): int"])
    draw_class(draw, 500, 410, 570, 340, "Task", ["- title: str", "- description: text", "- project: Project", "- assignee: User [0..1]", "- status: Status", "- priority: Priority", "- due_date: date [0..1]", "- created_at: datetime", "- updated_at: datetime"], ["+ is_overdue(): bool"])
    draw_class(draw, 1140, 520, 410, 220, "Comment", ["- task: Task", "- author: User", "- body: text", "- created_at: datetime", "- updated_at: datetime"])

    association(draw, (400, 210), (500, 210), "1", "0..*", "owns", label_pos=(430, 178))
    association(draw, (710, 350), (710, 410), "1", "0..*", "contains", composition=True, label_pos=(730, 368))
    association(draw, (1070, 585), (1140, 585), "1", "0..*", "has", composition=True, label_pos=(1090, 552))
    association(draw, (240, 320), (500, 510), "0..*", "0..1", "assigned to", dashed=True, label_pos=(280, 402))
    association(draw, (250, 335), (1140, 620), "0..*", "1", "authors", dashed=True, label_pos=(640, 520))

    centered(draw, W / 2, H - 26, "Wygenerowano automatycznie w formacie PNG", SMALL_FONT, MUTED)
    img.save(OUT)
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()

