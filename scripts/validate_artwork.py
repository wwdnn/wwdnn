"""Validate the actual committed SVG artifacts before publication."""

from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
REQUIRED = (
    "hero.svg", "hero-mobile.svg", "projects.svg", "projects-mobile.svg",
    "competencies.svg", "competencies-mobile.svg",
    "contribution-heatmap.svg", "contribution-heatmap-mobile.svg",
)


def main() -> None:
    for name in REQUIRED:
        path = ROOT / "assets" / name
        root = ET.parse(path).getroot()
        if root.tag != "{http://www.w3.org/2000/svg}svg":
            raise ValueError(f"Not an SVG: {name}")
        if not root.findtext("{http://www.w3.org/2000/svg}title"):
            raise ValueError(f"Missing accessible title: {name}")
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1] in {"script", "foreignObject"}:
                raise ValueError(f"Unsupported embedded content: {name}")
            for key, value in element.attrib.items():
                if key.rsplit("}", 1)[-1] == "href":
                    if not value.startswith("#"):
                        raise ValueError(f"External resource in SVG: {name}")
        print(f"Validated: {name}")


if __name__ == "__main__":
    main()
