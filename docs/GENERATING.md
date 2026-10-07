# Profile artwork

The README embeds self-contained SVG images. It uses no scripts, remote CSS, or third-party statistics servers. The `picture` elements choose full-width mobile artwork below 600px; the mobile heatmap shows the same complete calendar in two chronological strips.

The professional layout was designed for Wildan. The self-typing ASCII portrait, SVG-only animation, and daily contribution refresh were inspired by [Avi Vashishta's article](https://www.avivashishta.com/blog/build-animated-github-profile-readme).

## Generate locally

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-local.txt
.venv/bin/python -m scripts.generate_profile --offline
python3 -m unittest discover -s tests -v
python3 -m scripts.validate_artwork
```

Edit professional content in `scripts/domain/portfolio.py` and `scripts/domain/profile.py`. The existing approved photo cutout is the source for ASCII conversion. Original photo files are never modified.

- `--static-only`: regenerate hero, portrait, information card, projects, and competency artwork.
- `--activity-only`: update JSON and desktop/mobile heatmaps. Uses only Python's standard library; Pillow is not required.
- `--offline`: use the committed JSON snapshot.
- `--html-file /path/to/contributions.html`: parse a downloaded contribution fragment with normal TLS verification maintained by your downloader.

Daily Actions run at 06:17 UTC / 13:17 WIB, with manual dispatch also available. GitHub may delay scheduled workflows. Commit only changed contribution files. Repository/account restrictions, including billing locks, can prevent the runner from starting.

## Data contract

Observed 2026-10-07 using `curl --fail --silent --show-error --location https://github.com/users/wwdnn/contributions`: date/intensity are on `td[data-date][data-level]`; counts are in associated `tool-tip[for]` text. `data-count` is absent on current cells. The previous parser defaulted missing counts to zero; the new parser joins cells and tooltips by ID and fails on unknown, inconsistent, duplicate, or incomplete data. An excerpt of real markup is in `tests/fixtures/github-tooltip.html`.

SVG elements have accessible descriptions and reduced-motion support. Ordinary HTML text is available under the README's expandable experience summary. Animation defaults preserve the final visible state when a viewer disables CSS animation. No external resources are referenced from inside generated SVGs.

## Logo attribution

Technology logos are from [Devicon v2.16.0](https://github.com/devicons/devicon/tree/v2.16.0), retained locally under `assets/logos` with the original license. They represent the respective technologies, not endorsement. Architecture uses a TypeScript mark as a stack reference, not an invented brand logo.
