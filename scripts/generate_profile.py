from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from scripts.domain.contribution import ContributionDay
from scripts.domain.profile import WILDAN
from scripts.renderers.ascii_portrait import portrait_rows, render_ascii_portrait
from scripts.renderers.hero import render_hero
from scripts.renderers.portfolio import render_competencies, render_projects
from scripts.renderers.contribution_heatmap import render_heatmap
from scripts.renderers.info_card import render_info_card
from scripts.sources.github_contributions import fetch_contributions, parse_contributions


ROOT = Path(__file__).resolve().parent.parent


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def serialize_days(days: list[ContributionDay]) -> str:
    payload = [
        {"date": day.date.isoformat(), "count": day.count, "level": day.level}
        for day in days
    ]
    return json.dumps(payload, indent=4) + "\n"


def load_days(path: Path) -> list[ContributionDay]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [ContributionDay(date.fromisoformat(item["date"]), item["count"], item["level"]) for item in payload]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Wildan's GitHub Profile README artwork")
    parser.add_argument("--offline", action="store_true", help="Use the checked-in contribution snapshot")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--static-only", action="store_true", help="Only regenerate professional artwork")
    mode.add_argument("--activity-only", action="store_true", help="Only refresh contribution data and heatmap")
    parser.add_argument("--html-file", type=Path, help="Parse a previously downloaded GitHub contribution page")
    args = parser.parse_args()

    assets = ROOT / "assets"
    data_path = ROOT / "data" / "contributions.json"
    if not args.activity_only:
        write_text(assets / "info-card.svg", render_info_card(WILDAN))
        write_text(assets / "profile-ascii.svg", render_ascii_portrait(assets / "profile-cutout.png"))
        portrait = portrait_rows(assets / "profile-cutout.png")
        logos = {path.stem: path.read_text(encoding="utf-8") for path in (assets / "logos").glob("*.svg")}
        for mobile in (False, True):
            suffix = "-mobile" if mobile else ""
            write_text(assets / f"hero{suffix}.svg", render_hero(WILDAN, portrait, mobile))
            write_text(assets / f"projects{suffix}.svg", render_projects(mobile))
            write_text(assets / f"competencies{suffix}.svg", render_competencies(logos, mobile))

    if args.static_only:
        return
    if args.html_file:
        days = parse_contributions(args.html_file.read_text(encoding="utf-8"))
    elif args.offline:
        days = load_days(data_path)
    else:
        days = fetch_contributions(WILDAN.username)
    write_text(data_path, serialize_days(days))
    write_text(assets / "contribution-heatmap.svg", render_heatmap(days))
    write_text(assets / "contribution-heatmap-mobile.svg", render_heatmap(days, mobile=True))


if __name__ == "__main__":
    main()
