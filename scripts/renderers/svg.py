from html import escape


BACKGROUND = "#0d1117"
PRIMARY = "#e6edf3"
SECONDARY = "#8b949e"
BORDER = "#30363d"


def svg_document(width: int, height: int, content: str, title: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
    <title id="title">{escape(title)}</title>
    <desc id="desc">{escape(title)} for Wildan Setya Nugraha</desc>
    <rect width="100%" height="100%" rx="14" fill="{BACKGROUND}" stroke="{BORDER}"/>
    {content}
</svg>
'''

