"""
build_pdf_cn.py — Generates a PDF from the first 4 Chinese-language chapters.

Embeds Noto Sans CJK SC font so the PDF renders correctly on all devices
(iPhone, Android, Windows) without requiring system CJK fonts.

Usage:
    python3 build_pdf_cn.py

Output:
    output/stem-guidebook-ch1-4-cn.pdf
"""

import os
import subprocess
import sys
import tempfile

import markdown

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

CHAPTERS = [
    os.path.join(SCRIPT_DIR, "cn_01-is-this-right-for-your-child.md"),
    os.path.join(SCRIPT_DIR, "cn_02-k12-roadmap.md"),
    os.path.join(SCRIPT_DIR, "cn_03-the-competition-landscape.md"),
    os.path.join(SCRIPT_DIR, "cn_04-building-the-foundation.md"),
]

OUTPUT_PDF = os.path.join(OUTPUT_DIR, "stem-guidebook-ch1-4-cn.pdf")

TITLE         = "培养STEM竞赛人才：家长实战指南"
SUBTITLE      = "从幼儿园到高中 — 竞赛、项目与真正有效的方法"
CHAPTER_RANGE = "第一至四章"
DATE          = "2026年4月"

# Noto Sans CJK SC — installed via: brew install font-noto-sans-cjk-sc
FONT_REGULAR = os.path.expanduser("~/Library/Fonts/NotoSansCJKsc-Regular.otf")
FONT_MEDIUM  = os.path.expanduser("~/Library/Fonts/NotoSansCJKsc-Medium.otf")
FONT_LIGHT   = os.path.expanduser("~/Library/Fonts/NotoSansCJKsc-Light.otf")

# ---------------------------------------------------------------------------
# CSS (single, clean string — no template substitution needed for font paths
# because we build the @font-face rules dynamically below)
# ---------------------------------------------------------------------------

BODY_FONT = "'NotoSansSC', sans-serif"

BASE_CSS = f"""
/* ── Headings */
h1 {{
    font-family: {BODY_FONT};
    font-size: 22pt;
    font-weight: 500;
    line-height: 1.4;
    color: #111;
    margin: 0 0 0.75em 0;
    padding-bottom: 0.3em;
    border-bottom: 2px solid #ddd;
}}
h2 {{
    font-family: {BODY_FONT};
    font-size: 15pt;
    font-weight: 500;
    color: #222;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    line-height: 1.5;
}}
h3 {{
    font-family: {BODY_FONT};
    font-size: 12pt;
    font-weight: 500;
    color: #333;
    margin-top: 1.25em;
    margin-bottom: 0.4em;
    line-height: 1.5;
}}
h4 {{
    font-family: {BODY_FONT};
    font-size: 11pt;
    font-weight: 500;
    color: #444;
    margin-top: 1em;
    margin-bottom: 0.3em;
}}

/* ── Body */
*, *::before, *::after {{ box-sizing: border-box; }}
body {{
    font-family: {BODY_FONT};
    font-size: 11pt;
    line-height: 1.8;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}}
p {{ margin: 0 0 0.85em 0; orphans: 3; widows: 3; }}
ul, ol {{ margin: 0 0 0.85em 0; padding-left: 1.5em; }}
li {{ margin-bottom: 0.3em; line-height: 1.8; }}
strong {{ font-weight: 500; color: #111; }}
em {{ font-style: italic; }}

/* ── Title page */
.title-page {{
    text-align: center;
    padding-top: 8cm;
    page-break-after: always;
}}
.title-page h1 {{
    font-family: {BODY_FONT};
    font-size: 26pt;
    font-weight: 500;
    line-height: 1.4;
    margin: 0 0 0.5em 0;
    color: #111;
    border-bottom: none;
    padding-bottom: 0;
}}
.title-page .subtitle {{
    font-family: {BODY_FONT};
    font-size: 14pt;
    color: #444;
    margin: 0 0 1.5em 0;
}}
.title-page .divider {{
    width: 60px;
    height: 2px;
    background: #999;
    margin: 0 auto 1.5em auto;
}}
.title-page .chapter-range {{
    font-family: {BODY_FONT};
    font-size: 12pt;
    color: #555;
    margin: 0 0 0.5em 0;
}}
.title-page .date {{
    font-family: {BODY_FONT};
    font-size: 10pt;
    color: #888;
}}

/* ── Chapters */
.chapter {{ page-break-before: always; }}

/* ── Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0 1.25em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}}
th {{
    background-color: #2c3e50;
    color: #fff;
    font-family: {BODY_FONT};
    font-weight: 500;
    text-align: left;
    padding: 6px 10px;
    border: 1px solid #1a252f;
    font-size: 9.5pt;
}}
td {{
    padding: 5px 10px;
    border: 1px solid #ccc;
    vertical-align: top;
    line-height: 1.8;
    font-family: {BODY_FONT};
}}
tr:nth-child(even) td {{ background-color: #f5f7fa; }}
tr:nth-child(odd)  td {{ background-color: #ffffff; }}

/* ── Blockquotes */
blockquote {{
    border-left: 4px solid #3498db;
    background-color: #eef6fc;
    margin: 1em 0;
    padding: 0.75em 1em;
    color: #2c3e50;
    font-style: normal;
    page-break-inside: avoid;
}}
blockquote p {{ margin: 0; }}

/* ── Code */
code {{
    font-family: 'Courier New', Courier, monospace;
    font-size: 9.5pt;
    background-color: #f4f4f4;
    padding: 1px 4px;
}}
pre {{
    background-color: #f4f4f4;
    border-left: 4px solid #888;
    padding: 0.75em 1em;
    font-size: 9pt;
    margin: 1em 0;
    page-break-inside: avoid;
}}
pre code {{ background: none; padding: 0; }}

/* ── Horizontal rules */
hr {{
    border: none;
    border-top: 1px solid #ccc;
    margin: 1.5em 0;
}}

/* ── Keep headings with content */
h1, h2, h3, h4 {{ page-break-after: avoid; }}
"""


def font_face_rules():
    """Build @font-face blocks with embedded file paths."""
    rules = []
    for weight, path in [(400, FONT_REGULAR), (500, FONT_MEDIUM), (300, FONT_LIGHT)]:
        if not os.path.exists(path):
            print(f"WARNING: font not found: {path}", file=sys.stderr)
            continue
        rules.append(f"""@font-face {{
    font-family: 'NotoSansSC';
    font-weight: {weight};
    src: url('file://{path}');
}}""")
    return "\n".join(rules)


def page_rules():
    return f"""@page {{
    size: A4;
    margin: 2.5cm 2.5cm 2.5cm 2.5cm;
    @bottom-center {{
        content: counter(page);
        font-family: {BODY_FONT};
        font-size: 9pt;
        color: #666;
    }}
}}"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def md_to_html(md_text):
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br"],
    )


def build_title_page():
    return f"""<div class="title-page">
    <h1>{TITLE}</h1>
    <p class="subtitle">{SUBTITLE}</p>
    <div class="divider"></div>
    <p class="chapter-range">{CHAPTER_RANGE}</p>
    <p class="date">{DATE}</p>
</div>"""


def build_full_html(chapters_md):
    parts = [build_title_page()]
    for md_text in chapters_md:
        parts.append(f'<div class="chapter">\n{md_to_html(md_text)}\n</div>')

    full_css = f"{font_face_rules()}\n\n{page_rules()}\n\n{BASE_CSS}"

    body_content = "\n".join(parts)
    return f"""<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="UTF-8">
<title>{TITLE}</title>
<style>
{full_css}
</style>
</head>
<body>
{body_content}
</body>
</html>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Reading chapters...")
    chapters_md = []
    for path in CHAPTERS:
        if not os.path.exists(path):
            sys.exit(f"ERROR: not found: {path}")
        text = read_file(path)
        chapters_md.append(text)
        print(f"  {os.path.basename(path)} ({len(text):,} chars)")

    print("Building HTML...")
    html = build_full_html(chapters_md)
    print(f"  HTML size: {len(html):,} chars")

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", encoding="utf-8", delete=False, prefix="stem_cn_"
    ) as tmp:
        tmp.write(html)
        tmp_path = tmp.name

    print(f"Running WeasyPrint -> {OUTPUT_PDF}")
    try:
        result = subprocess.run(
            ["weasyprint", tmp_path, OUTPUT_PDF],
            capture_output=True, text=True, check=True,
        )
        for line in (result.stderr or "").splitlines():
            if line.strip():
                print(f"  [wp] {line}")
    except subprocess.CalledProcessError as e:
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    finally:
        os.unlink(tmp_path)

    if os.path.exists(OUTPUT_PDF):
        size_kb = os.path.getsize(OUTPUT_PDF) / 1024
        print(f"\nDone: {OUTPUT_PDF}  ({size_kb:.0f} KB)")
    else:
        sys.exit("ERROR: PDF not created.")


if __name__ == "__main__":
    main()
