"""
build_pdf.py — Generates a PDF from the first 4 chapters of the STEM guidebook.

Usage:
    python3 build_pdf.py

Output:
    output/stem-guidebook-ch1-4.pdf
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
    os.path.join(SCRIPT_DIR, "01-is-this-right-for-your-child.md"),
    os.path.join(SCRIPT_DIR, "02-k12-roadmap.md"),
    os.path.join(SCRIPT_DIR, "03-the-competition-landscape.md"),
    os.path.join(SCRIPT_DIR, "04-building-the-foundation.md"),
]

OUTPUT_PDF = os.path.join(OUTPUT_DIR, "stem-guidebook-ch1-4.pdf")

TITLE = "Raising a STEM Kid: A Parent&#8217;s Guide to Competitive Math and Physics"
SUBTITLE = "K through 12 &#8212; Competitions, Programs, and What Actually Works"
CHAPTER_RANGE = "Chapters 1&#8211;4"
DATE = "April 2026"

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = """
@page {
    size: letter;
    margin: 1in 1in 1in 1in;
    @bottom-center {
        content: counter(page);
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 9pt;
        color: #666;
    }
}

/* Reset */
*, *::before, *::after {
    box-sizing: border-box;
}

body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}

/* Title page */
.title-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 9in;
    page-break-after: always;
}

.title-page h1 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 28pt;
    font-weight: bold;
    line-height: 1.25;
    margin: 0 0 0.5em 0;
    color: #111;
}

.title-page .subtitle {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 14pt;
    font-style: italic;
    color: #444;
    margin: 0 0 1.5em 0;
}

.title-page .chapter-range {
    font-family: system-ui, -apple-system, sans-serif;
    font-size: 12pt;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 0 0 3em 0;
}

.title-page .divider {
    width: 80px;
    height: 2px;
    background: #888;
    margin: 0 auto 3em auto;
}

.title-page .date {
    font-family: system-ui, -apple-system, sans-serif;
    font-size: 10pt;
    color: #888;
    margin: 0;
}

/* Chapter content */
.chapter {
    page-break-before: always;
}

.chapter:first-of-type {
    page-break-before: avoid;
}

/* Headings */
h1 {
    font-family: system-ui, -apple-system, Helvetica, Arial, sans-serif;
    font-size: 24pt;
    font-weight: 700;
    line-height: 1.2;
    color: #111;
    margin: 0 0 0.75em 0;
    padding-bottom: 0.3em;
    border-bottom: 2px solid #ddd;
}

h2 {
    font-family: system-ui, -apple-system, Helvetica, Arial, sans-serif;
    font-size: 16pt;
    font-weight: 600;
    color: #222;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    line-height: 1.3;
}

h3 {
    font-family: system-ui, -apple-system, Helvetica, Arial, sans-serif;
    font-size: 13pt;
    font-weight: 600;
    color: #333;
    margin-top: 1.25em;
    margin-bottom: 0.4em;
    line-height: 1.3;
}

h4 {
    font-family: system-ui, -apple-system, Helvetica, Arial, sans-serif;
    font-size: 11pt;
    font-weight: 600;
    color: #444;
    margin-top: 1em;
    margin-bottom: 0.3em;
}

/* Paragraphs */
p {
    margin: 0 0 0.85em 0;
    orphans: 3;
    widows: 3;
}

/* Lists */
ul, ol {
    margin: 0 0 0.85em 0;
    padding-left: 1.5em;
}

li {
    margin-bottom: 0.3em;
    line-height: 1.5;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0 1.25em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

th {
    background-color: #2c3e50;
    color: #fff;
    font-family: system-ui, -apple-system, Helvetica, Arial, sans-serif;
    font-weight: 600;
    text-align: left;
    padding: 6px 10px;
    border: 1px solid #1a252f;
    font-size: 9.5pt;
}

td {
    padding: 5px 10px;
    border: 1px solid #ccc;
    vertical-align: top;
    line-height: 1.45;
}

tr:nth-child(even) td {
    background-color: #f5f7fa;
}

tr:nth-child(odd) td {
    background-color: #ffffff;
}

/* Blockquotes — used for callout/sidebar blocks */
blockquote {
    border-left: 4px solid #3498db;
    background-color: #eef6fc;
    margin: 1em 0;
    padding: 0.75em 1em;
    color: #2c3e50;
    font-style: normal;
    page-break-inside: avoid;
}

blockquote p {
    margin: 0;
}

/* Code */
code {
    font-family: 'Courier New', Courier, monospace;
    font-size: 9.5pt;
    background-color: #f4f4f4;
    padding: 1px 4px;
    border-radius: 2px;
}

pre {
    background-color: #f4f4f4;
    border: 1px solid #ddd;
    border-left: 4px solid #888;
    padding: 0.75em 1em;
    font-size: 9pt;
    overflow-x: auto;
    margin: 1em 0;
    page-break-inside: avoid;
}

pre code {
    background: none;
    padding: 0;
}

/* Horizontal rules */
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 1.5em 0;
}

/* Strong / em */
strong {
    font-weight: 700;
    color: #111;
}

em {
    font-style: italic;
}

/* Footnote / small text */
.footnote {
    font-size: 9pt;
    color: #777;
    font-style: italic;
    margin-top: 1.5em;
    border-top: 1px solid #ddd;
    padding-top: 0.5em;
}

/* Keep headings with their following content */
h1, h2, h3, h4 {
    page-break-after: avoid;
}
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def md_to_html(md_text: str) -> str:
    """Convert markdown to HTML with tables and fenced code blocks enabled."""
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br"],
        extension_configs={
            "nl2br": {},
        },
    )


def build_title_page() -> str:
    return f"""
<div class="title-page">
    <h1>{TITLE}</h1>
    <p class="subtitle">{SUBTITLE}</p>
    <div class="divider"></div>
    <p class="chapter-range">{CHAPTER_RANGE}</p>
    <p class="date">{DATE}</p>
</div>
"""


def build_chapter_html(md_text: str, chapter_index: int) -> str:
    """Wrap a chapter's HTML in a div with page-break-before."""
    html = md_to_html(md_text)
    css_class = "chapter"
    return f'<div class="{css_class}">\n{html}\n</div>\n'


def build_full_html(chapters_md: list) -> str:
    body_parts = [build_title_page()]
    for i, md_text in enumerate(chapters_md):
        body_parts.append(build_chapter_html(md_text, i))

    body = "\n".join(body_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raising a STEM Kid — Chapters 1-4</title>
    <style>
{CSS}
    </style>
</head>
<body>
{body}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Read all chapters
    print("Reading chapter files...")
    chapters_md = []
    for path in CHAPTERS:
        if not os.path.exists(path):
            print(f"ERROR: Chapter file not found: {path}", file=sys.stderr)
            sys.exit(1)
        text = read_file(path)
        chapters_md.append(text)
        print(f"  Read: {os.path.basename(path)} ({len(text):,} chars)")

    # Build HTML
    print("Converting markdown to HTML...")
    full_html = build_full_html(chapters_md)
    print(f"  HTML size: {len(full_html):,} chars")

    # Write to temp file
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".html",
        encoding="utf-8",
        delete=False,
        prefix="stem_guidebook_",
    ) as tmp:
        tmp.write(full_html)
        tmp_path = tmp.name

    print(f"  Temp HTML: {tmp_path}")

    # Run WeasyPrint
    print(f"Running WeasyPrint -> {OUTPUT_PDF}")
    try:
        result = subprocess.run(
            ["weasyprint", tmp_path, OUTPUT_PDF],
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            # WeasyPrint writes warnings to stderr even on success
            for line in result.stderr.splitlines():
                if line.strip():
                    print(f"  [weasyprint] {line}")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: WeasyPrint failed (exit {e.returncode})", file=sys.stderr)
        if e.stdout:
            print(e.stdout, file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)
    finally:
        os.unlink(tmp_path)

    # Verify output
    if os.path.exists(OUTPUT_PDF):
        size_kb = os.path.getsize(OUTPUT_PDF) / 1024
        print(f"\nDone. PDF written to: {OUTPUT_PDF}")
        print(f"File size: {size_kb:.1f} KB")
    else:
        print("ERROR: Output PDF was not created.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
