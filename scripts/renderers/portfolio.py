"""SVG artwork for approved project stories and competency cards."""

from scripts.domain.portfolio import COMPETENCIES, PROJECTS, Project
from scripts.renderers.primitives import document, logo, panel, paragraph, text


COLORS = {
    "blue": ("#161c26", "#2c3442", "#b6cff3"),
    "teal": ("#172129", "#2b3e49", "#bce2e6"),
    "lavender": ("#1c1b26", "#363142", "#d1c2e8"),
}


def project_card(project: Project, width: int, mobile: bool = False) -> tuple[str, int]:
    fill, stroke, accent = COLORS[project.color]
    parts = [text(project.period, 26, 36, 14 if mobile else 12, accent)]
    y = 78
    for line in project.title:
        p, y = paragraph(line, 26, y, width - 52, 23, "#edf0f6")
        parts.append(p)
    p, y = paragraph(project.subtitle, 26, y + 5, width - 52, 15 if mobile else 13, accent)
    parts.append(p)
    p, y = paragraph(project.description, 26, y + 20, width - 52, 16 if mobile else 14)
    parts.append(p)
    if project.outcomes:
        y += 22
        bottom = y
        for index, (value, caption) in enumerate(project.outcomes):
            x = 26 + index * ((width - 52) / 2)
            parts.append(text(value, x, y, 25, accent, 500))
            p, end = paragraph(caption, x, y + 24, (width - 52) / 2 - 12, 15 if mobile else 12)
            parts.append(p)
            bottom = max(bottom, end)
        y = bottom
    for heading, body in project.story:
        y += 24
        parts.append(text(heading, 26, y, 16 if mobile else 14, weight=500))
        p, y = paragraph(body, 26, y + 24, width - 52, 16 if mobile else 13)
        parts.append(p)
    y += 14
    x = 26
    for tag in project.tags:
        tag_width = len(tag) * 6.8 + 18
        if x + tag_width > width - 26:
            x = 26
            y += 32
        parts.append(f'<rect x="{x}" y="{y}" width="{tag_width}" height="25" rx="6" fill="{stroke}"/>')
        parts.append(text(tag, x + 9, y + 17, 12, accent))
        x += tag_width + 7
    height = int(y + 51)
    return panel(0, 0, width, height, fill, stroke) + "".join(parts), height


def render_projects(mobile: bool = False) -> str:
    width = 390 if mobile else 900
    card_width = width - 32 if mobile else 426
    cards = [project_card(project, card_width, mobile) for project in PROJECTS]
    parts = [text("Selected work", 16 if mobile else 24, 30, 22, weight=500), text("Delivered at PT Neural Technologies Indonesia", 16 if mobile else 24, 54, 13)]
    positions = [(16, 78), (16, 100 + cards[0][1]), (16, 122 + cards[0][1] + cards[1][1])] if mobile else [(16, 78), (458, 78), (458, 100 + cards[1][1])]
    height = 0
    for (content, card_height), (x, y) in zip(cards, positions):
        parts.append(f'<g transform="translate({x} {y})">{content}</g>')
        height = max(height, y + card_height + 16)
    return document(width, height, "".join(parts), "Selected projects and professional experience")


def render_competencies(logos: dict[str, str], mobile: bool = False) -> str:
    width, columns = (390, 1) if mobile else (900, 3)
    card_width = 358 if mobile else 276
    parts = [text("Tools I work with", 16, 34, 22, weight=500)]
    y = 60
    for row in range(0, len(COMPETENCIES), columns):
        rendered = []
        row_height = 0
        for index, competency in enumerate(COMPETENCIES[row:row + columns]):
            inner = [logo(logos[competency.logo], 22, 23)]
            p, end = paragraph(competency.title, 64, 40, card_width - 84, 15, "#edf0f6")
            inner.append(p)
            p, end = paragraph(competency.skills, 22, max(85, end + 20), card_width - 44, 16 if mobile else 13)
            inner.append(p)
            card_height = int(end + 22)
            row_height = max(row_height, card_height)
            rendered.append((index, "".join(inner)))
        for index, content in rendered:
            x = 16 + index * (card_width + 20)
            parts.append(f'<g transform="translate({x} {y})">{panel(0, 0, card_width, row_height)}{content}</g>')
        y += row_height + 20
    return document(width, y, "".join(parts), "Core competencies and technology stack")
