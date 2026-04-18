"""
build_pdf.py — PDF builder for the college placement guidebook.
Adapted from the STEM guidebook v2 PDF builder.

Usage:
    python3 build_pdf.py              # Build all available chapters
    python3 build_pdf.py --chapters 1 2 3 4 5 6 7   # Specific chapters

Output:
    guidebook/output/college-placement-guidebook.pdf
"""

import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

import markdown

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
DIAGRAMS_DIR = os.path.join(OUTPUT_DIR, "diagrams")

CHAPTER_FILES = [
    ("01", "01-what-the-brochure-doesnt-say.md"),
    ("02", "02-reading-placement-data.md"),
    ("03", "03-the-athlete-hook.md"),
    ("04", "04-school-by-school.md"),
    ("05", "05-the-asian-parent-reality.md"),
    ("06", "06-private-vs-public.md"),
    ("07", "07-legacy-ed-hooks.md"),
    ("08", "08-the-spike-not-well-rounded.md"),
    ("09", "09-grade-by-grade.md"),
    ("10", "10-should-you-transfer.md"),
]

OUTPUT_PDF = os.path.join(OUTPUT_DIR, "college-placement-guidebook.pdf")

TITLE = "Where Do They Really Go?"
SUBTITLE = "Bay Area Private School College Placement &mdash; By the Numbers"
DATE = "April 2026"

# ---------------------------------------------------------------------------
# Diagram classification
# ---------------------------------------------------------------------------

DIAGRAM_PROFILES = {
    "normal":      {"width": 660,  "scale": 2, "font": "15px", "css_class": "size-normal"},
    "wide":        {"width": 860,  "scale": 2, "font": "14px", "css_class": "size-wide"},
    "complex":     {"width": 1050, "scale": 2, "font": "13px", "css_class": "size-complex"},
    "verycomplex": {"width": 1400, "scale": 2, "font": "12px", "css_class": "size-verycomplex"},
}


def classify_diagram(code):
    subgraphs = code.count("subgraph")
    is_lr = "graph LR" in code or "graph RL" in code or "flowchart LR" in code
    node_count = len(re.findall(r'\b\w+\s*[\[{(]', code))

    if subgraphs >= 4:
        return "verycomplex"
    elif subgraphs >= 2:
        return "complex"
    elif subgraphs >= 1 or (is_lr and node_count >= 5):
        return "wide"
    else:
        return "normal"


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = """
@page {
    size: letter;
    margin: 0.9in 0.9in 1in 0.9in;
    @bottom-center {
        content: counter(page);
        font-family: system-ui, Helvetica, Arial, sans-serif;
        font-size: 9pt;
        color: #666;
    }
}

*, *::before, *::after { box-sizing: border-box; }

body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}

/* ── Title page ───────────────────────────────────────────────── */
.title-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 8.5in;
    page-break-after: always;
}
.title-page h1 {
    font-family: system-ui, Helvetica, Arial, sans-serif;
    font-size: 28pt;
    font-weight: 700;
    line-height: 1.2;
    margin: 0 0 0.3em;
    color: #111;
}
.title-page .subtitle {
    font-family: Georgia, serif;
    font-size: 13pt;
    font-style: italic;
    color: #444;
    margin: 0 0 1.5em;
    max-width: 5in;
}
.title-page .divider {
    width: 80px;
    height: 2px;
    background: #2c3e50;
    margin: 0 auto 1.5em;
}
.title-page .chapter-range {
    font-family: system-ui, Helvetica, Arial, sans-serif;
    font-size: 10pt;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 0 0 0.75em;
}
.title-page .date {
    font-family: system-ui, Helvetica, Arial, sans-serif;
    font-size: 9pt;
    color: #999;
}
.title-page .disclaimer {
    font-family: system-ui, Helvetica, Arial, sans-serif;
    font-size: 8pt;
    color: #999;
    margin-top: 2em;
    max-width: 4.5in;
    line-height: 1.4;
}

/* ── Chapters ─────────────────────────────────────────────────── */
.chapter { page-break-before: always; }

/* ── Headings ─────────────────────────────────────────────────── */
h1 {
    font-family: system-ui, Helvetica, Arial, sans-serif;
    font-size: 20pt;
    font-weight: 700;
    line-height: 1.2;
    color: #111;
    margin: 0 0 0.6em;
    padding-bottom: 0.25em;
    border-bottom: 2px solid #2c3e50;
    page-break-after: avoid;
    break-after: avoid;
}
h2 {
    font-family: system-ui, Helvetica, Arial, sans-serif;
    font-size: 14pt;
    font-weight: 600;
    color: #222;
    margin-top: 1.4em;
    margin-bottom: 0.4em;
    line-height: 1.3;
    page-break-after: avoid;
    break-after: avoid;
}
h3 {
    font-family: system-ui, Helvetica, Arial, sans-serif;
    font-size: 12pt;
    font-weight: 600;
    color: #333;
    margin-top: 1.1em;
    margin-bottom: 0.3em;
    page-break-after: avoid;
    break-after: avoid;
}

/* ── Body text ────────────────────────────────────────────────── */
p { margin: 0 0 0.75em; orphans: 3; widows: 3; }
ul, ol { margin: 0 0 0.75em; padding-left: 1.4em; }
li { margin-bottom: 0.25em; line-height: 1.5; }
strong { font-weight: 700; color: #111; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.3em 0; }

/* ── Tables ───────────────────────────────────────────────────── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.8em 0 1em;
    font-size: 9pt;
    break-inside: avoid;
    page-break-inside: avoid;
}
th {
    background-color: #2c3e50;
    color: #fff;
    font-family: system-ui, Helvetica, Arial, sans-serif;
    font-weight: 600;
    text-align: left;
    padding: 5px 8px;
    border: 1px solid #1a252f;
    font-size: 8.5pt;
}
td {
    padding: 4px 8px;
    border: 1px solid #ccc;
    vertical-align: top;
    line-height: 1.4;
}
tr:nth-child(even) td { background-color: #f5f7fa; }

/* ── Blockquotes ──────────────────────────────────────────────── */
blockquote {
    border-left: 4px solid #2c3e50;
    background-color: #eef2f7;
    margin: 0.8em 0;
    padding: 0.6em 0.9em;
    color: #2c3e50;
    font-style: normal;
    font-size: 10pt;
    break-inside: avoid;
    page-break-inside: avoid;
}
blockquote p { margin: 0; }

/* ── Code ─────────────────────────────────────────────────────── */
code {
    font-family: 'Courier New', monospace;
    font-size: 9pt;
    background-color: #f4f4f4;
    padding: 1px 3px;
    border-radius: 2px;
}
pre {
    background-color: #f4f4f4;
    border-left: 4px solid #888;
    padding: 0.6em 0.8em;
    font-size: 8.5pt;
    margin: 0.8em 0;
    break-inside: avoid;
}
pre code { background: none; padding: 0; }

/* ── Diagrams ─────────────────────────────────────────────────── */
.diagram-wrap {
    break-inside: avoid;
    page-break-inside: avoid;
    margin: 1em 0 0;
    text-align: center;
}
.diagram-wrap.size-normal img { max-width: 84%; height: auto; display: block; margin: 0 auto; }
.diagram-wrap.size-wide img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
.diagram-wrap.size-complex img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
.diagram-wrap.size-verycomplex img { max-width: 100%; height: auto; display: block; margin: 0 auto; }

.figure-caption {
    font-family: system-ui, Helvetica, Arial, sans-serif;
    font-size: 8pt;
    color: #555;
    font-style: italic;
    text-align: center;
    break-before: avoid;
    margin: 0.3em 0 1.2em;
    line-height: 1.35;
}

.mermaid-fallback {
    background: #f8f8f8;
    border-left: 4px solid #aaa;
    padding: 0.6em 0.8em;
    font-size: 7.5pt;
    color: #666;
    break-inside: avoid;
}
"""

# ---------------------------------------------------------------------------
# Mermaid rendering
# ---------------------------------------------------------------------------

MMDC_PATH = None


def _find_mmdc():
    global MMDC_PATH
    if MMDC_PATH:
        return MMDC_PATH
    for candidate in ["/usr/local/bin/mmdc", "/opt/homebrew/bin/mmdc",
                      os.path.expanduser("~/.npm-global/bin/mmdc"), "mmdc"]:
        try:
            subprocess.run([candidate, "--version"], capture_output=True, check=True)
            MMDC_PATH = candidate
            return MMDC_PATH
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
    return None


def _mermaid_config(font_size):
    config = {
        "theme": "default",
        "themeVariables": {
            "fontSize": font_size,
            "fontFamily": "Arial, Helvetica, sans-serif",
            "primaryColor": "#e3f2fd",
            "primaryTextColor": "#1a1a1a",
            "lineColor": "#555",
        },
    }
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(config, f)
    return path


def render_mermaid(code, cache_dir):
    mmdc = _find_mmdc()
    size_class = classify_diagram(code)
    profile = DIAGRAM_PROFILES[size_class]

    digest = hashlib.md5((code + str(profile)).encode()).hexdigest()[:14]
    out_path = os.path.join(cache_dir, f"diag_{digest}.png")

    if not os.path.exists(out_path) and mmdc:
        cfg_path = _mermaid_config(profile["font"])
        fd, mmd_path = tempfile.mkstemp(suffix=".mmd")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(code)
        try:
            subprocess.run(
                [mmdc, "-i", mmd_path, "-o", out_path,
                 "--width", str(profile["width"]),
                 "--scale", str(profile["scale"]),
                 "--backgroundColor", "white",
                 "--configFile", cfg_path],
                capture_output=True, check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"  [mmdc] failed: {e.stderr.decode()[:200]}", file=sys.stderr)
        finally:
            for p in [mmd_path, cfg_path]:
                try: os.unlink(p)
                except: pass

    if os.path.exists(out_path):
        with open(out_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{b64}", profile["css_class"]

    return None, profile["css_class"]


# ---------------------------------------------------------------------------
# Markdown preprocessing
# ---------------------------------------------------------------------------

_MERMAID_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
_CAPTION_RE = re.compile(r"^\*\*(Figure\s+[\d.]+[:：])(.*?)\*\*(.*)$", re.MULTILINE)


def preprocess_md(md_text, cache_dir):
    def render_block(m):
        code = m.group(1).strip()
        data_uri, css_class = render_mermaid(code, cache_dir)
        if data_uri:
            return (f'<div class="diagram-wrap {css_class}">'
                    f'<img src="{data_uri}" alt="diagram"/></div>')
        escaped = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<pre class="mermaid-fallback">{escaped}</pre>'

    text = _MERMAID_RE.sub(render_block, md_text)

    def mark_caption(m):
        return f'<FIGCAPTION>**{m.group(1)}**{m.group(2)}{m.group(3)}</FIGCAPTION>'

    text = _CAPTION_RE.sub(mark_caption, text)
    return text


def md_to_html(md_text, cache_dir):
    preprocessed = preprocess_md(md_text, cache_dir)
    html = markdown.markdown(preprocessed, extensions=["tables", "fenced_code", "nl2br"])
    html = re.sub(
        r'<p>\s*<FIGCAPTION>(.*?)</FIGCAPTION>\s*</p>',
        r'<p class="figure-caption">\1</p>',
        html, flags=re.DOTALL
    )
    return html


# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------

def build_title_page(chapter_range):
    return f"""
<div class="title-page">
  <h1>{TITLE}</h1>
  <p class="subtitle">{SUBTITLE}</p>
  <div class="divider"></div>
  <p class="chapter-range">{chapter_range}</p>
  <p class="date">{DATE}</p>
  <p class="disclaimer">All data sourced from official school publications, UC InfoCenter,
  and public competition results. Verified against original sources.
  See Appendix A for full methodology.</p>
</div>"""


def build_full_html(chapters_md, chapter_range, cache_dir):
    parts = [build_title_page(chapter_range)]

    for md_text in chapters_md:
        parts.append(f'<div class="chapter">\n{md_to_html(md_text, cache_dir)}\n</div>')

    body = "\n".join(parts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{TITLE}</title>
<style>
{CSS}
</style>
</head>
<body>
{body}
</body>
</html>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapters", nargs="+", type=int, help="Chapter numbers to include (default: all available)")
    parser.add_argument("--output", type=str, default=None, help="Output PDF path")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)

    mmdc = _find_mmdc()
    if mmdc:
        print(f"Mermaid renderer: {mmdc}")
    else:
        print("WARNING: mmdc not found — diagrams will render as text fallback")

    # Select chapters
    if args.chapters:
        selected = [(num, fname) for num, fname in CHAPTER_FILES if int(num) in args.chapters]
    else:
        selected = [(num, fname) for num, fname in CHAPTER_FILES
                     if os.path.exists(os.path.join(SCRIPT_DIR, fname))]

    if not selected:
        print("ERROR: No chapter files found", file=sys.stderr)
        sys.exit(1)

    chapter_nums = [int(n) for n, _ in selected]
    chapter_range = f"Chapters {min(chapter_nums)}&ndash;{max(chapter_nums)}"

    # Read chapters
    print(f"Reading {len(selected)} chapters...")
    chapters_md = []
    for num, fname in selected:
        path = os.path.join(SCRIPT_DIR, fname)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        chapters_md.append(text)
        print(f"  Ch {num}: {fname} ({len(text):,} chars)")

    # Build HTML
    print("Building HTML + rendering diagrams...")
    html = build_full_html(chapters_md, chapter_range, DIAGRAMS_DIR)
    print(f"  HTML size: {len(html):,} chars")

    # Write temp HTML
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", encoding="utf-8", delete=False, prefix="placement_"
    ) as tmp:
        tmp.write(html)
        tmp_path = tmp.name

    # Run WeasyPrint
    output_pdf = args.output or OUTPUT_PDF
    print(f"Running WeasyPrint → {output_pdf}")
    try:
        subprocess.run(
            ["weasyprint", tmp_path, output_pdf],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"ERROR: WeasyPrint failed (exit {e.returncode})", file=sys.stderr)
        print(e.stderr[:2000], file=sys.stderr)
        sys.exit(1)
    finally:
        try: os.unlink(tmp_path)
        except: pass

    if os.path.exists(output_pdf):
        size_kb = os.path.getsize(output_pdf) / 1024
        print(f"\nDone: {output_pdf}  ({size_kb:.0f} KB)")
    else:
        print("ERROR: PDF was not created.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
