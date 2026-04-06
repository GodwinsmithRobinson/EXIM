"""
Japan Family Itinerary — Professional PDF Generator
Converts JAPAN_ITINERARY.md into a presentation-quality PDF report.
Uses markdown → HTML → xhtml2pdf pipeline with custom CSS.
"""

import markdown
import re
import os
from xhtml2pdf import pisa

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH    = os.path.join(SCRIPT_DIR, "JAPAN_ITINERARY.md")
PDF_PATH   = os.path.join(SCRIPT_DIR, "Japan_Family_Itinerary.pdf")
HTML_PATH  = os.path.join(SCRIPT_DIR, "japan_itinerary.html")


# ---------------------------------------------------------------------------
# 1. "Sakura Sunset" theme — warm pink/red/cream palette
#    Evokes cherry blossoms and Japan's flag; PDF-compatible base colours
# ---------------------------------------------------------------------------

CSS = """
/* ===================================================================
   JAPAN ITINERARY — "SAKURA SUNSET" THEME
   Palette: Deep Navy / Sakura Pink / Vermillion / Cream
   Gradients degrade gracefully to solid colors in PDF
   =================================================================== */

@page {
    size: A4;
    margin: 25mm 20mm 28mm 20mm;

    @frame footer {
        -pdf-frame-content: page-footer;
        bottom: 0mm;
        margin-left: 20mm;
        margin-right: 20mm;
        height: 12mm;
    }
}

@page coverpage {
    size: A4;
    margin: 0;
    @frame footer { }
}

/* ---------- GLOBAL ---------- */
body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.72;
    color: #1e293b;
}

/* ---------- COVER PAGE ---------- */
.cover-page {
    -pdf-page-break: before;
    page: coverpage;
    width: 100%;
    height: 100%;
}

.cover-outer {
    background-color: #1a1a2e;
    background: linear-gradient(160deg, #1a1a2e 0%, #2d1b3d 45%, #8b1a2e 100%);
    min-height: 297mm;
    padding: 0;
    margin: 0;
}

.cover-accent-bar {
    background-color: #e8294e;
    background: linear-gradient(90deg, #e8294e 0%, #f472b6 50%, #fbbf24 100%);
    height: 5mm;
    width: 100%;
}

.cover-content {
    padding: 45mm 34mm 30mm 34mm;
    text-align: center;
}

.cover-flag {
    font-size: 56pt;
    margin-bottom: 6mm;
}

.cover-title {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 36pt;
    font-weight: bold;
    color: #ffffff;
    letter-spacing: 4px;
    margin: 0 0 3mm 0;
}

.cover-title-sub {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 16pt;
    font-weight: bold;
    color: #f9a8d4;
    letter-spacing: 3px;
    margin: 0 0 8mm 0;
}

.cover-subtitle {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 13pt;
    color: #e2c4d4;
    line-height: 2.0;
    margin: 0 0 12mm 0;
    letter-spacing: 0.5px;
}

.cover-divider {
    width: 55mm;
    height: 2px;
    background-color: #e8294e;
    background: linear-gradient(90deg, transparent, #e8294e, #f472b6, transparent);
    margin: 0 auto 12mm auto;
}

.cover-meta {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    color: #c4a3b5;
    line-height: 2.4;
}

.cover-meta b {
    color: #fbbf24;
}

.cover-badge {
    margin-top: 20mm;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 8.5pt;
    color: #f472b6;
    letter-spacing: 2.5px;
    border: 1.5px solid #f472b6;
    border-radius: 4px;
    padding: 3mm 12mm;
    display: inline-block;
}

.cover-bottom-bar {
    background-color: #e8294e;
    background: linear-gradient(90deg, #e8294e, #f472b6, #fbbf24);
    height: 3mm;
    width: 100%;
    position: absolute;
    bottom: 0;
}

/* ---------- TOC PAGE ---------- */
.toc-page {
    -pdf-page-break: before;
}

.toc-heading {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 22pt;
    font-weight: bold;
    color: #1a1a2e;
    border-bottom: 3px solid #e8294e;
    padding-bottom: 4mm;
    margin-bottom: 8mm;
}

.toc-table {
    width: 100%;
    border-collapse: collapse;
}

.toc-table td {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10pt;
    padding: 2mm 1.5mm;
    border-bottom: 1px dotted #f9c4d4;
    color: #334155;
    vertical-align: top;
}

.toc-num {
    width: 14mm;
    font-weight: bold;
    color: #be123c;
    text-align: right;
    padding-right: 2mm;
    font-size: 10pt;
}

.toc-link {
    color: #334155;
    text-decoration: none;
}

/* ---------- INFO CALLOUT ---------- */
.info-callout {
    background-color: #fff1f5;
    border-left: 5px solid #e8294e;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
    padding: 5mm 7mm;
    margin: 6mm 0 8mm 0;
    font-size: 10pt;
    line-height: 1.7;
}

/* ---------- HEADINGS ---------- */
h1 {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 22pt;
    font-weight: bold;
    color: #1a1a2e;
    border-bottom: 3px solid #e8294e;
    padding-bottom: 3mm;
    margin-top: 10mm;
    margin-bottom: 6mm;
    letter-spacing: 0.3px;
    -pdf-keep-with-next: true;
}

h2 {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 15pt;
    font-weight: bold;
    color: #1a1a2e;
    border-bottom: 2px solid #fce7f3;
    border-left: 4px solid #e8294e;
    padding-bottom: 2.5mm;
    padding-left: 4mm;
    margin-top: 9mm;
    margin-bottom: 5mm;
    -pdf-keep-with-next: true;
}

h3 {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 12.5pt;
    font-weight: bold;
    color: #9f1239;
    margin-top: 7mm;
    margin-bottom: 3mm;
    -pdf-keep-with-next: true;
}

h4 {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 11pt;
    font-weight: bold;
    color: #475569;
    margin-top: 5mm;
    margin-bottom: 2.5mm;
    -pdf-keep-with-next: true;
}

/* ---------- PARAGRAPHS ---------- */
p {
    margin: 0 0 3.5mm 0;
    text-align: justify;
}

/* ---------- BLOCKQUOTES ---------- */
blockquote {
    border-left: 4px solid #e8294e;
    margin: 5mm 0;
    padding: 4mm 6mm;
    background-color: #fff1f5;
    border-radius: 0 8px 8px 0;
    color: #334155;
    font-style: italic;
    font-size: 10pt;
}

blockquote p { margin: 0 0 2mm 0; }

/* ---------- TABLES ---------- */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 5mm 0 7mm 0;
    font-size: 8.5pt;
    line-height: 1.5;
}

th {
    background-color: #1a1a2e;
    background: linear-gradient(135deg, #1a1a2e 0%, #3b1a3a 100%);
    color: #f9e8ee;
    font-family: Helvetica, Arial, sans-serif;
    font-weight: bold;
    padding: 2mm 2mm;
    text-align: left;
    border: 1px solid #3b1a3a;
    font-size: 8.5pt;
    letter-spacing: 0.3px;
}

td {
    padding: 1.5mm 2mm;
    border: 1px solid #fce7f3;
    vertical-align: top;
    font-size: 8.5pt;
}

tr:nth-child(even) td {
    background-color: #fff8fb;
}

/* ---------- LISTS ---------- */
ul, ol {
    margin: 3mm 0 5mm 0;
    padding-left: 7mm;
    font-size: 11pt;
}

li {
    margin-bottom: 2mm;
    line-height: 1.7;
}

/* ---------- TASK LIST (checkboxes) ---------- */
ul li input[type="checkbox"] {
    margin-right: 2mm;
}

/* ---------- HR ---------- */
hr {
    border: 0;
    border-top: 2px solid #fce7f3;
    margin: 7mm 0;
}

/* ---------- LINKS ---------- */
a {
    color: #be123c;
    text-decoration: none;
}

strong {
    color: #1a1a2e;
    font-weight: bold;
}

em {
    color: #6b4a5a;
}

/* ---------- SECTION BREAK ---------- */
.section-break {
    -pdf-page-break: before;
}

/* ---------- PAGE FOOTER ---------- */
#page-footer {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 8pt;
    color: #94a3b8;
    text-align: center;
    border-top: 1px solid #fce7f3;
    padding-top: 2mm;
}

#page-footer .right-text {
    float: right;
    font-size: 8pt;
    color: #cbd5e1;
}
"""


# ---------------------------------------------------------------------------
# 2. Read & pre-process the Markdown
# ---------------------------------------------------------------------------

def read_markdown_file(path):
    """Read a Markdown file from *path* and return its contents as a string."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_toc_items(md_text):
    """Extract section numbers and titles for the custom TOC page."""
    items = []
    for m in re.finditer(r'^## (\d+)\.\s+(.+)$', md_text, re.MULTILINE):
        num   = m.group(1)
        title = m.group(2).strip()
        items.append((num, title))
    return items


def preprocess_md(md_text):
    """
    Remove the original H1 title + meta block and inline TOC
    (we build a custom cover page and TOC page instead).
    Also inject page-break hints before each ## section heading.
    """
    # Remove the first H1 heading block (title + meta)
    md_text = re.sub(
        r'^# JAPAN FAMILY TRAVEL.*?(?=\n## )',
        '',
        md_text,
        count=1,
        flags=re.DOTALL
    )

    # Remove inline TOC block
    md_text = re.sub(
        r'## TABLE OF CONTENTS.*?(?=\n## )',
        '',
        md_text,
        count=1,
        flags=re.DOTALL
    )

    # Inject page-break div + named anchor before each numbered ## section
    def inject_numbered(m):
        num  = m.group(2)
        rest = m.group(1)
        return f'\n<div class="section-break"></div>\n<a name="sec-{num}"></a>\n\n{rest}'

    md_text = re.sub(
        r'\n(## (\d+)\.\s)',
        inject_numbered,
        md_text
    )

    return md_text


# ---------------------------------------------------------------------------
# 3. Build the full HTML document
# ---------------------------------------------------------------------------

def build_cover_html():
    return """
    <div class="cover-page">
        <div class="cover-outer">
            <div class="cover-accent-bar"></div>
            <div class="cover-content">
                <div class="cover-flag">&#127471;&#127477;</div>
                <div class="cover-title">JAPAN</div>
                <div class="cover-title-sub">FAMILY TRAVEL ITINERARY</div>
                <div class="cover-subtitle">
                    5 Days &bull; 4 Nights &bull; Tokyo<br/>
                    A Complete First International Trip Guide
                </div>
                <div class="cover-divider">&nbsp;</div>
                <div class="cover-meta">
                    <b>Travellers:</b> 2 Adults + 1 Child (7 yrs) + 1 Infant (7 months)<br/>
                    <b>Trip Type:</b> First International Family Vacation<br/>
                    <b>Highlights:</b> Tokyo Disneyland &bull; Asakusa &bull; Ueno Zoo &bull; Shibuya<br/><br/>
                    <b>Prepared:</b> April 2026 &nbsp;|&nbsp; <b>Version:</b> 1.0
                </div>
                <br/><br/>
                <div class="cover-badge">PROFESSIONALLY PLANNED &mdash; FAMILY TRAVEL</div>
            </div>
        </div>
    </div>
    """


def build_toc_html(items):
    """Build a 2-column TOC table where every entry links to its section anchor."""

    def make_cell(num, title):
        if not num:
            return '<td></td><td></td>'
        display = f"{num}." if num.isdigit() else num
        href    = f"#sec-{num}" if num.isdigit() else f"#appendix-{num.split()[-1].lower()}"
        return (
            f'<td class="toc-num">{display}</td>'
            f'<td><a href="{href}" class="toc-link">{title}</a></td>'
        )

    rows = ""
    mid   = (len(items) + 1) // 2
    left  = items[:mid]
    right = items[mid:]
    for i in range(mid):
        l_num, l_title = left[i]  if i < len(left)  else ("", "")
        r_num, r_title = right[i] if i < len(right) else ("", "")
        rows += f"<tr>{make_cell(l_num, l_title)}{make_cell(r_num, r_title)}</tr>\n"

    return f"""
    <div class="toc-page">
        <div class="toc-heading">Table of Contents</div>
        <table class="toc-table">
            {rows}
        </table>
    </div>
    """


def build_info_callout():
    return """
    <div class="info-callout">
        <b>&#9992; First International Trip — Key Reminder:</b>
        Apply for Japan Tourist Visa at the Embassy of Japan at least <b>4–6 weeks before travel.</b>
        Purchase <b>Travel Insurance</b> covering all 4 family members (including infant) with minimum
        USD 50,000 medical coverage. Carry <b>sufficient JPY cash</b> — Japan is still largely
        a cash-first country. Book <b>Tokyo Disneyland tickets online</b> well in advance to avoid sellout.
    </div>
    """


def md_to_html(md_text):
    """Convert Markdown text to HTML using Python-Markdown with extensions."""
    extensions = [
        'tables',
        'fenced_code',
        'toc',
        'sane_lists',
        'smarty',
    ]
    html = markdown.markdown(md_text, extensions=extensions)
    # xhtml2pdf needs self-closing br and hr tags
    html = html.replace('<br>', '<br/>')
    html = html.replace('<hr>', '<hr/>')
    # Replace checkbox markdown syntax
    html = html.replace('[ ]', '&#9744;')
    html = html.replace('[x]', '&#9745;')
    html = html.replace('[X]', '&#9745;')
    # xhtml2pdf/reportlab crashes with a ValueError ("negative availWidth") when a
    # table with 4+ columns contains an empty <td></td> cell.  During column-width
    # calculation reportlab divides the available width among columns; an empty cell
    # gets width=0, and after subtracting leftPadding+rightPadding the result goes
    # negative.  Replacing empty cells with a non-breaking space gives every cell a
    # non-zero minimum width and prevents the crash.
    html = re.sub(r'<td>\s*</td>', '<td>&nbsp;</td>', html)
    return html


def build_full_html(cover, toc, callout, body_html):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Japan Family Travel Itinerary — 5 Days Tokyo</title>
<style>
{CSS}
</style>
</head>
<body>
{cover}
{toc}
{callout}
{body_html}
<div id="page-footer">
    Page <pdf:pagenumber/> of <pdf:pagecount/>
    <span class="right-text">Japan Family Itinerary 2026 &#127471;&#127477;</span>
</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# 4. Main
# ---------------------------------------------------------------------------

def main():
    print("[1/5] Reading JAPAN_ITINERARY.md ...")
    raw_md = read_markdown_file(MD_PATH)

    print("[2/5] Building Table of Contents ...")
    toc_items = build_toc_items(raw_md)
    print(f"       Found {len(toc_items)} sections.")

    print("[3/5] Pre-processing Markdown ...")
    processed_md = preprocess_md(raw_md)

    print("[4/5] Converting Markdown -> HTML -> PDF (this may take 30-60 seconds) ...")
    body_html = md_to_html(processed_md)

    cover_html   = build_cover_html()
    toc_html     = build_toc_html(toc_items)
    callout_html = build_info_callout()

    full_html = build_full_html(cover_html, toc_html, callout_html, body_html)

    # Save HTML for browser preview
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"       HTML saved to {HTML_PATH}")

    # Generate PDF using xhtml2pdf
    with open(PDF_PATH, "w+b") as pdf_file:
        status = pisa.CreatePDF(full_html, dest=pdf_file, encoding='utf-8')

    if status.err:
        print(f"[ERROR] PDF generation encountered {status.err} errors.")
    else:
        size_mb = os.path.getsize(PDF_PATH) / (1024 * 1024)
        print(f"[5/5] PDF generated: {PDF_PATH}  ({size_mb:.1f} MB)")
        print()
        print("  ✈  Japan Family Itinerary PDF is ready!")
        print("  ✈  HTML preview saved to japan_itinerary.html")


if __name__ == "__main__":
    main()
