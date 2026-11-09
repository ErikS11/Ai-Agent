"""Assemble docs/p2/sections/*.md into the P2 PDF (docs/p2/CS3354_P2_Group1.pdf).

Run from the repository root:
    pip install markdown
    python docs/p2/build_pdf.py
Needs Google Chrome (or Chromium) installed; it prints the HTML to PDF headlessly.
"""

import datetime
import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
SECTIONS = HERE / "sections"
OUT_HTML = HERE / "CS3354_P2_Group1.html"
OUT_PDF = HERE / "CS3354_P2_Group1.pdf"

# Required order (template numbering). Missing files are reported and skipped.
ORDER = [
    "0-records.md", "1-introduction.md", "2-overall.md", "3-requirements.md", "4-use-cases.md",
    "5-1-domain.md", "5-2-uc01.md", "5-2-uc02.md", "5-3-crosscheck.md",
    "6-design.md", "7-rationale.md", "8-spike.md", "9-traceability.md", "10-12-plan.md",
]

MEMBERS = [  # name, NetID, GitHub username
    ("John Bramlet", "dal222463", "JohnDavid-B"),
    ("Erik Sandoval", "eas220006", "ErikS11"),
    ("Omor Igiehon", "ooi180001", ""),
    ("Daniel Habib", "dxh230020", "danielrhabib"),
    ("Ahmad Zghier", "dal901977", "azghier1"),
    ("Zaid Abusamra", "dal304926", "zabusamra1"),
]

CSS = """
@page { size: Letter; margin: 0.8in 0.75in; }
body { font: 10.5pt/1.45 "Helvetica Neue", Arial, sans-serif; color: #1d2125; }
h1 { font-family: Georgia, serif; color: #1f3864; border-bottom: 2px solid #1f3864; padding-bottom: 4px;
     font-size: 20pt; margin-top: 28px; }
.newpage { page-break-before: always; }
h1.cover-title { page-break-before: avoid; border: none; font-size: 26pt; margin-bottom: 2px; }
h2 { font-family: Georgia, serif; color: #1f3864; font-size: 14pt; margin-top: 18px; }
h3 { color: #2e74b5; font-size: 12pt; } h4 { font-size: 11pt; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; page-break-inside: auto; font-size: 9.5pt; }
tr { page-break-inside: avoid; }
th { background: #dbe5f1; color: #1f3864; text-align: left; }
th, td { border: 1px solid #bfbfbf; padding: 4px 6px; vertical-align: top; }
img { max-width: 100%; max-height: 7.5in; display: block; margin: 8px auto; }
code { font-family: Menlo, Consolas, monospace; font-size: 9pt; background: #f2f2f2; padding: 0 3px; }
pre { background: #f2f2f2; padding: 8px; overflow-wrap: anywhere; white-space: pre-wrap; }
.cover-sub { color: #2e74b5; font-weight: 600; font-size: 13pt; margin: 0; }
.cover-proj { font-style: italic; color: #555; font-size: 15pt; margin: 2px 0 18px; }
.header { color: #777; font-size: 9pt; text-align: right; }
"""


def cover(date: str) -> str:
    rows = "".join(f"<tr><td>{n}</td><td>{i}</td><td>{g}</td></tr>" for n, i, g in MEMBERS)
    return f"""
<p class="header" style="margin-top:0">CE/CS/SE 3354 · Software Engineering · Fall 2026</p>
<p class="cover-sub">Project Milestone P2</p>
<h1 class="cover-title">Analysis and High-Level Design</h1>
<p class="cover-proj">LMS AI Agent</p>
<table>
<tr><th>Team</th><td>Group 1, section .010</td></tr>
<tr><th>Document version</th><td>1.0 (baseline for P2; grows from the P1 baseline, v0.5)</td></tr>
<tr><th>Date</th><td>{date}</td></tr>
<tr><th>Repository URL</th><td>https://github.com/azghier1/Ai-Agent</td></tr>
<tr><th>Git tag for this milestone</th><td>p2 (points at the commit that contains this exact PDF)</td></tr>
<tr><th>Submitted on Canvas by</th><td>John Bramlet</td></tr>
</table>
<table><tr><th>Team member</th><th>NetID</th><th>GitHub username</th></tr>{rows}</table>
"""


def section_html(path: Path) -> str:
    text = path.read_text()
    # Image paths in sections are relative to docs/p2/sections; make them relative to docs/p2.
    text = re.sub(r"\]\(\.\./", "](", text)
    return markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])


def find_chrome() -> str:
    for c in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chrome")]:
        if c and Path(c).exists():
            return c
    sys.exit("Chrome/Chromium not found")


def main():
    missing = [f for f in ORDER if not (SECTIONS / f).exists()]
    body = [cover(datetime.date.today().strftime("%B %d, %Y"))]
    first = True
    for f in ORDER:
        if (SECTIONS / f).exists():
            html_part = section_html(SECTIONS / f)
            if first:
                html_part = html_part.replace("<h1>", "<h1 class=\"newpage\">", 1)
                first = False
            body.append(html_part)
    # Sub-sections that share a top-level number should not each start a new page.
    html = "\n".join(body)
    html = re.sub(r"<h1>(5\.[23][^<]*)</h1>", r"<h2>\1</h2>", html)
    OUT_HTML.write_text(f"<!doctype html><html><head><meta charset='utf-8'><title>CS3354 P2 Group 1</title>"
                        f"<style>{CSS}</style></head><body>{html}</body></html>")
    subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    OUT_HTML.unlink()
    print(f"Wrote {OUT_PDF.relative_to(HERE.parent.parent)}")
    if missing:
        print("MISSING sections (not in the PDF):", ", ".join(missing))
    leftovers = sorted(set(re.findall(r"\[(?:TBD|NOT [A-Z ]+|COUNTS|PR #\[?n\]?|Member \d)\]|placeholder", html, re.I)))
    if leftovers:
        print("WARNING placeholders still in the text:", ", ".join(leftovers))


if __name__ == "__main__":
    main()
