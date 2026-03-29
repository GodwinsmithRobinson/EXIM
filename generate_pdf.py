"""
EXIM DPR — Professional PDF Generator
Converts CONTEXT.md into a presentation-quality PDF report.
Uses markdown → HTML → xhtml2pdf pipeline with custom CSS.
"""

import markdown
import re
import os
from xhtml2pdf import pisa

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "CONTEXT.md")
PDF_PATH = os.path.join(SCRIPT_DIR, "EXIM_DPR.pdf")


# ---------------------------------------------------------------------------
# 1. Material Design 3 — "Ocean Depth" gradient theme
#    PDF-compatible base (xhtml2pdf) + browser-enhanced gradients & shadows
# ---------------------------------------------------------------------------

CSS = """
/* ===================================================================
   MATERIAL DESIGN 3 — "OCEAN DEPTH" THEME
   Palette: Slate-900 / Cyan-500 / Violet-500 / Pink-500
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
    background-color: #0f172a;
    background: linear-gradient(160deg, #0f172a 0%, #172554 45%, #0c4a6e 100%);
    min-height: 297mm;
    padding: 0;
    margin: 0;
}

.cover-accent-bar {
    background-color: #06b6d4;
    background: linear-gradient(90deg, #06b6d4 0%, #8b5cf6 50%, #ec4899 100%);
    height: 5mm;
    width: 100%;
}

.cover-content {
    padding: 58mm 34mm 30mm 34mm;
    text-align: center;
}

.cover-title {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 44pt;
    font-weight: bold;
    color: #ffffff;
    letter-spacing: 6px;
    margin: 0 0 6mm 0;
}

.cover-subtitle {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 15pt;
    color: #94a3b8;
    line-height: 1.9;
    margin: 0 0 15mm 0;
    letter-spacing: 0.5px;
}

.cover-divider {
    width: 55mm;
    height: 2px;
    background-color: #06b6d4;
    background: linear-gradient(90deg, transparent, #06b6d4, #8b5cf6, transparent);
    margin: 0 auto 12mm auto;
}

.cover-meta {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    color: #64748b;
    line-height: 2.4;
}

.cover-meta b {
    color: #22d3ee;
}

.cover-badge {
    margin-top: 24mm;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 8.5pt;
    color: #06b6d4;
    letter-spacing: 2.5px;
    border: 1.5px solid #06b6d4;
    border-radius: 4px;
    padding: 3mm 12mm;
    display: inline-block;
}

.cover-bottom-bar {
    background-color: #06b6d4;
    background: linear-gradient(90deg, #06b6d4, #8b5cf6, #ec4899);
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
    color: #0f172a;
    border-bottom: 3px solid #06b6d4;
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
    padding: 2.5mm 3mm;
    border-bottom: 1px dotted #cbd5e1;
    color: #334155;
    vertical-align: top;
}

.toc-num {
    width: 12mm;
    font-weight: bold;
    color: #0891b2;
    text-align: right;
    padding-right: 3mm;
    font-size: 10pt;
}

.toc-link {
    color: #334155;
    text-decoration: none;
}

/* ---------- POLICY CALLOUT ---------- */
.policy-callout {
    background-color: #f0fdfa;
    border-left: 5px solid #06b6d4;
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
    color: #0f172a;
    border-bottom: 3px solid #06b6d4;
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
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    border-left: 4px solid #06b6d4;
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
    color: #1e40af;
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
    border-left: 4px solid #06b6d4;
    margin: 5mm 0;
    padding: 4mm 6mm;
    background-color: #f0fdfa;
    border-radius: 0 8px 8px 0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    color: #334155;
    font-style: italic;
    font-size: 10pt;
    -pdf-keep-in-frame-mode: shrink;
}

blockquote p { margin: 0 0 2mm 0; }

/* ---------- TABLES ---------- */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 5mm 0 7mm 0;
    font-size: 9pt;
    line-height: 1.55;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
    -pdf-keep-in-frame-mode: shrink;
}

th {
    background-color: #1e293b;
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    color: #e2e8f0;
    font-family: Helvetica, Arial, sans-serif;
    font-weight: bold;
    padding: 3mm 3.5mm;
    text-align: left;
    border: 1px solid #334155;
    font-size: 9pt;
    letter-spacing: 0.3px;
}

td {
    padding: 2.5mm 3.5mm;
    border: 1px solid #e2e8f0;
    vertical-align: top;
    font-size: 9pt;
}

tr:nth-child(even) td {
    background-color: #f8fafc;
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

/* ---------- CODE BLOCKS ---------- */
pre {
    background-color: #1e293b;
    color: #e2e8f0;
    border: none;
    border-left: 4px solid #06b6d4;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.12);
    padding: 5mm 6mm;
    font-family: Courier, monospace;
    font-size: 8.5pt;
    line-height: 1.55;
    margin: 5mm 0;
    white-space: pre-wrap;
    -pdf-keep-in-frame-mode: shrink;
}

code {
    font-family: Courier, monospace;
    font-size: 9pt;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 0.5mm 2mm;
    border-radius: 3px;
}

pre code {
    background-color: transparent;
    color: #e2e8f0;
    padding: 0;
    border-radius: 0;
}

/* ---------- HR ---------- */
hr {
    border: 0;
    border-top: 2px solid #e2e8f0;
    margin: 7mm 0;
}

/* ---------- LINKS ---------- */
a {
    color: #2563eb;
    text-decoration: none;
}

strong {
    color: #0f172a;
    font-weight: bold;
}

em {
    color: #475569;
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
    border-top: 1px solid #e2e8f0;
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

def read_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_toc_items(md_text):
    """Extract section numbers and titles for the custom TOC page."""
    items = []
    for m in re.finditer(r'^## (\d+)\.\s+(.+)$', md_text, re.MULTILINE):
        num = m.group(1)
        title = m.group(2).strip()
        items.append((num, title))
    # Also capture APPENDIX sections
    for m in re.finditer(r'^## (APPENDIX [A-Z]):\s*(.+)$', md_text, re.MULTILINE):
        items.append((m.group(1), m.group(2).strip()))
    return items


def preprocess_md(md_text):
    """
    Remove the original H1 title + meta block and inline TOC
    (we build a custom cover page and TOC page instead).
    Also inject page-break hints before each ## section heading.
    """
    # Remove the first H1 heading block (title + meta)
    md_text = re.sub(
        r'^# EXIM BUSINESS.*?(?=\n## )',
        '',
        md_text,
        count=1,
        flags=re.DOTALL
    )

    # Remove inline TOC block (numbered links list)
    md_text = re.sub(
        r'## TABLE OF CONTENTS.*?(?=\n## )',
        '',
        md_text,
        count=1,
        flags=re.DOTALL
    )

    # Inject page-break div + named anchor before each numbered ## section
    # The anchor enables TOC href links to jump to the correct page in the PDF
    def inject_numbered(m):
        num   = m.group(2)   # e.g. "5"
        rest  = m.group(1)   # e.g. "## 5. "
        return f'\n<div class="section-break"></div>\n<a name="sec-{num}"></a>\n\n{rest}'

    md_text = re.sub(
        r'\n(## (\d+)\.\s)',
        inject_numbered,
        md_text
    )

    # Inject page-break div + named anchor before appendix headings
    def inject_appendix(m):
        label = m.group(2)                    # e.g. "APPENDIX A"
        letter = label.split()[-1].lower()    # e.g. "a"
        rest  = m.group(1)                    # e.g. "## APPENDIX A"
        return f'\n<div class="section-break"></div>\n<a name="appendix-{letter}"></a>\n\n{rest}'

    md_text = re.sub(
        r'\n(## (APPENDIX [A-Z]))',
        inject_appendix,
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
                <div class="cover-title">EXIM BUSINESS</div>
                <br/>
                <div class="cover-subtitle">
                    Detailed Project Report<br/>
                    Import–Export Operations from India
                </div>
                <div class="cover-divider">&nbsp;</div>
                <div class="cover-meta">
                    <b>Promoter Location:</b> Karur, Tamil Nadu, India<br/>
                    <b>Business Type:</b> Multi-product Export House<br/>
                    <b>Scope:</b> Sourcing from anywhere in India — Exporting worldwide<br/><br/>
                    <b>Prepared:</b> March 25, 2026 &nbsp;|&nbsp; <b>Version:</b> 3.0
                </div>
                <br/><br/>
                <div class="cover-badge">CONFIDENTIAL — FOR INTERNAL USE</div>
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
        if num.isdigit():
            href = f"#sec-{num}"
        else:
            # "APPENDIX A" -> "#appendix-a"
            letter = num.split()[-1].lower()
            href = f"#appendix-{letter}"
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


def build_policy_callout():
    return """
    <div class="policy-callout">
        <b>&#9888; Data Sourcing Policy (Section 34):</b>
        All information in this DPR is sourced exclusively from Government of India portals
        (DGFT, CBIC, RBI, ECGC, FIEO, Commerce Ministry, Indian Trade Portal, TIA Portal,
        EXIM Bank) and international institutional sources (ITC/WTO/UN/ICC/EU).
        <i>No social media, Reddit, Quora, blogs, or unverified platforms have been used.</i>
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
    # Replace checkbox syntax
    html = html.replace('[ ]', '&#9744;')
    html = html.replace('[x]', '&#9745;')
    return html


def build_full_html(cover, toc, policy, body_html):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>EXIM Business — Detailed Project Report</title>
<style>
{CSS}
</style>
</head>
<body>
{cover}
{toc}
{policy}
{body_html}
<div id="page-footer">
    Page <pdf:pagenumber/> of <pdf:pagecount/>
    <span class="right-text">EXIM DPR — Confidential</span>
</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# 4. Main
# ---------------------------------------------------------------------------

def main():
    print("[1/5] Reading CONTEXT.md ...")
    raw_md = read_markdown(MD_PATH)

    print("[2/5] Building Table of Contents ...")
    toc_items = build_toc_items(raw_md)
    print(f"       Found {len(toc_items)} sections.")

    print("[3/5] Pre-processing Markdown ...")
    processed_md = preprocess_md(raw_md)

    print("[4/5] Converting Markdown -> HTML -> PDF (this may take 30-60 seconds) ...")
    body_html = md_to_html(processed_md)

    cover_html = build_cover_html()
    toc_html = build_toc_html(toc_items)
    policy_html = build_policy_callout()

    full_html = build_full_html(cover_html, toc_html, policy_html, body_html)

    # Save HTML — index.html for GitHub Pages serving
    html_path = os.path.join(SCRIPT_DIR, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"       HTML saved to {html_path}")

    # Generate PDF using xhtml2pdf
    with open(PDF_PATH, "w+b") as pdf_file:
        status = pisa.CreatePDF(full_html, dest=pdf_file, encoding='utf-8')

    if status.err:
        print(f"[ERROR] PDF generation encountered {status.err} errors.")
    else:
        size_mb = os.path.getsize(PDF_PATH) / (1024 * 1024)
        print(f"[5/5] PDF generated: {PDF_PATH}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
