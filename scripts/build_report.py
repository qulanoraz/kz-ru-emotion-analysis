"""Build the consolidated PDF report of all 11 pre-defense sections (DIP-19).

The PDF is generated from the Markdown sources in docs/, so it always matches the
repository version it was built from (required: "must match the version tagged prob-period-1").

Usage:
  python scripts/build_report.py \
      --repo https://github.com/<owner>/kz-ru-emotion-analysis \
      --youtrack https://<instance>.youtrack.cloud/projects/DIP \
      --representative Orazbek

Requires: pip install markdown playwright pypdf && playwright install chromium
"""
import argparse
import datetime as dt
import html
import pathlib
import re
import subprocess

import markdown
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SECTIONS = [
    ("01-project-proposal.md", "Project proposal"),
    ("02-evidence-of-relevance.md", "Evidence of relevance"),
    ("03-literature-review.md", "Literature review"),
    ("04-existing-systems.md", "Existing system comparison"),
    ("05-technology-comparison.md", "Technology comparison"),
    ("06-requirements.md", "Requirements specification"),
    ("07-architecture.md", "Architecture and diagrams"),
    ("08-ux-prototype.md", "UX / prototype and API"),
    ("09-verification-plan.md", "Verification and evaluation plan"),
    ("10-project-management.md", "Project management and risks"),
    ("11-supervisor-feedback.md", "Supervisor feedback"),
]

CSS = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm; }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', 'Noto Sans', Arial, sans-serif; font-size: 9.2pt; line-height: 1.42; color: #1d2330; }
h1 { font-size: 17pt; margin: 0 0 6pt; color: #0f2a5c; border-bottom: 2px solid #0f2a5c; padding-bottom: 4pt; }
h2 { font-size: 12.5pt; margin: 14pt 0 5pt; color: #0f2a5c; break-after: avoid; }
h3 { font-size: 10.5pt; margin: 11pt 0 4pt; break-after: avoid; }
h4 { font-size: 9.6pt; margin: 9pt 0 3pt; break-after: avoid; }
p, li { orphans: 2; widows: 2; }
a { color: #1f4fbf; text-decoration: none; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8pt; background: #f1f3f7; padding: 0 2px; border-radius: 2px; }
pre { background: #f5f6f9; border: 1px solid #dde1e8; border-radius: 4px; padding: 6pt 8pt; font-size: 7.6pt; line-height: 1.35; white-space: pre-wrap; word-break: break-word; break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 7.6pt; }
table { border-collapse: collapse; width: 100%; margin: 5pt 0 9pt; font-size: 7.6pt; line-height: 1.3; }
th, td { border: 1px solid #cfd5df; padding: 2.5pt 4pt; vertical-align: top; text-align: left; overflow-wrap: break-word; hyphens: auto; }
td code { overflow-wrap: anywhere; }
table.backlog { font-size: 6.7pt; }
table.backlog td:nth-child(-n+5), table.backlog th:nth-child(-n+5) { white-space: nowrap; }
table.backlog td:nth-child(2) { white-space: normal; min-width: 70pt; }
table.backlog td:last-child { min-width: 92pt; }
th { background: #eaf0fa; font-weight: 700; }
tr { break-inside: avoid; }
blockquote { margin: 6pt 0; padding: 4pt 9pt; border-left: 3px solid #9fb4dc; background: #f6f8fc; color: #333; }
img { max-width: 100%; display: block; margin: 6pt auto; break-inside: avoid; }
hr { border: none; border-top: 1px solid #dde1e8; margin: 8pt 0; }
.section { break-before: page; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: space-between; }
.cover .top { margin-top: 30mm; }
.cover .kicker { font-size: 10pt; letter-spacing: .08em; text-transform: uppercase; color: #5a6476; }
.cover h1 { font-size: 22pt; border: none; line-height: 1.25; margin-top: 6pt; }
.cover .alt { font-size: 11pt; color: #3c4658; margin: 4pt 0; }
.cover table { font-size: 9.5pt; width: auto; min-width: 60%; }
.cover td { border: none; padding: 3pt 12pt 3pt 0; }
.cover td:first-child { color: #5a6476; }
.links td:first-child { width: 34%; font-weight: 600; }
.toc { list-style: none; padding: 0; font-size: 10.5pt; }
.toc li { display: flex; align-items: baseline; margin: 6pt 0; }
.toc .num { width: 22pt; color: #5a6476; }
.toc .dots { flex: 1; border-bottom: 1px dotted #9aa3b2; margin: 0 6pt; transform: translateY(-3pt); }
.note { font-size: 8.5pt; color: #5a6476; }
"""


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return ""


def md_to_html(md_text: str, base: pathlib.Path, repo: str, ref: str) -> str:
    md_text = re.sub(r"```mermaid.*?```", "", md_text, flags=re.S)
    out = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])

    def fix_src(m):
        src = m.group(1)
        if re.match(r"https?://", src):
            return m.group(0)
        return f'src="{(base / src).resolve().as_uri()}"'
    out = re.sub(r'src="([^"]+)"', fix_src, out)

    def fix_href(m):
        href = m.group(1)
        if re.match(r"(https?:|mailto:|#)", href) or not repo.startswith("http"):
            return m.group(0)
        target = (base / href).resolve()
        try:
            rel = target.relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        kind = "tree" if target.is_dir() or href.endswith("/") else "blob"
        return f'href="{repo.rstrip("/")}/{kind}/{ref}/{rel}"'
    out = re.sub(r'href="([^"]+)"', fix_href, out)
    # keep identifiers such as AC-04.2, FR-05, DIP-23 on one line inside table cells
    def nowrap_ids(cell):
        parts = re.split(r"(<[^>]+>)", cell.group(0))
        parts = [p if p.startswith("<") else
                 re.sub(r"\b([A-Z]{1,5}-\d[\d.]*[a-z]?)", r'<span style="white-space:nowrap">\1</span>', p)
                 for p in parts]
        return "".join(parts)
    out = re.sub(r"<td>.*?</td>", nowrap_ids, out, flags=re.S)
    # compact layout for the backlog tables of DOC-10
    out = re.sub(r'<table>(\s*<thead>\s*<tr>(?:(?!</tr>).)*Branch / commit example)', r'<table class="backlog">\1', out, flags=re.S)
    return out


def build_html(a, toc_pages=None):
    today = dt.date.today().strftime("%d.%m.%Y")
    commit = git("rev-parse", "--short", "HEAD")
    ref = a.tag
    tree = f"{a.repo.rstrip('/')}/tree/{ref}" if a.repo.startswith("http") else a.repo

    def L(path, label=None):
        url = f"{tree}/{path}" if a.repo.startswith("http") else f"{a.repo}/{path}"
        return f'<a href="{html.escape(url)}">{html.escape(label or url)}</a>'

    cover = f"""
<div class="cover">
 <div class="top">
  <div class="kicker">Diploma project · Probationary period 1 · Group {html.escape(a.group)}</div>
  <h1>Identifying emotions from text (sentiment analysis) for the Kazakh and Russian languages</h1>
  <div class="alt">Определение эмоций по тексту (анализ тональности) для казахского и русского языков</div>
  <div class="alt">Мәтіннен эмоцияларды анықтау (көңіл-күйді талдау) қазақ және орыс тілдерінде</div>
 </div>
 <table>
  <tr><td>Team</td><td>Nurgaly Kuanyshevich Ashkenov — ML/NLP Engineer<br>Ulan Abzalovich Orazbek — Backend Developer &amp; System Integrator</td></tr>
  <tr><td>Supervisor</td><td>Kamila Tanyrbergenova</td></tr>
  <tr><td>Submission</td><td>First submission of materials (pre-defense 1), deadline 24.10.2026</td></tr>
  <tr><td>Repository version</td><td>tag <b>{html.escape(a.tag)}</b> (alias pre-defense-1){', commit ' + html.escape(commit) if commit else ''}</td></tr>
  <tr><td>Report generated</td><td>{today} from the Markdown sources in <code>docs/</code> by <code>scripts/build_report.py</code></td></tr>
 </table>
 <div class="note">All sections of this report are generated from the repository files of the tagged version; the repository is the authoritative source. Diagram images are exported from the editable PlantUML sources listed on the next page.</div>
</div>"""

    links = f"""
<div class="section">
<h1>Links to the repository and supporting materials</h1>
<table class="links">
 <tr><th>Material</th><th>Link</th></tr>
 <tr><td>GitHub repository</td><td>{L('', a.repo) if a.repo.startswith('http') else html.escape(a.repo)}</td></tr>
 <tr><td>Version submitted (tag {html.escape(a.tag)})</td><td>{html.escape(tree)}</td></tr>
 <tr><td>YouTrack project (tasks, board)</td><td>{html.escape(a.youtrack)}</td></tr>
 <tr><td>Prototype — wireframes SCR-01…SCR-06</td><td>{L('docs/mockups')}</td></tr>
 <tr><td>Prototype source (HTML)</td><td>{L('docs/mockups/src/wireframes.html')}</td></tr>
 <tr><td>REST API contract (OpenAPI 3.1)</td><td>{L('docs/api/openapi.yaml')}<br><span class="note">Open in https://editor.swagger.io for interactive documentation</span></td></tr>
 <tr><td>Editable diagram sources (PlantUML)</td><td>{L('docs/diagrams/src')}</td></tr>
 <tr><td>Rendered diagrams (SVG / PNG)</td><td>{L('docs/diagrams/export')}</td></tr>
 <tr><td>Bibliography (BibTeX)</td><td>{L('docs/literature/references.bib')}</td></tr>
 <tr><td>YouTrack backlog export (CSV)</td><td>{L('docs/pm/backlog.csv')}</td></tr>
 <tr><td>Interview guide and consent form</td><td>{L('docs/evidence')}</td></tr>
 <tr><td>Automated tests and CI</td><td>{L('tests')} · {L('.github/workflows/ci.yml')}</td></tr>
</table>
<h2>Table of contents</h2>
<ul class="toc">
"""
    for i, (_, title) in enumerate(SECTIONS, 1):
        page = toc_pages.get(i, "") if toc_pages else ""
        links += f'<li><span class="num">{i}.</span><a href="#s{i}">{html.escape(title)}</a><span class="dots"></span><span>{page}</span></li>\n'
    links += "</ul></div>"

    body = []
    for i, (fname, _) in enumerate(SECTIONS, 1):
        text = (DOCS / fname).read_text(encoding="utf-8")
        body.append(f'<div class="section" id="s{i}">{md_to_html(text, DOCS, a.repo, ref)}</div>')

    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{cover}{links}{''.join(body)}</body></html>"


def render(page, html_text, out):
    tmp = ROOT / "docs" / ".report_tmp.html"
    tmp.write_text(html_text, encoding="utf-8")
    page.goto(tmp.as_uri(), wait_until="networkidle")
    page.pdf(path=str(out), format="A4", print_background=True, display_header_footer=True,
             header_template="<span></span>",
             footer_template=("<div style='font-size:7pt;width:100%;padding:0 14mm;color:#6b7280;"
                              "display:flex;justify-content:space-between'>"
                              "<span>SE-2406 · KZ-RU Emotion Analysis · Probationary period 1</span>"
                              "<span><span class='pageNumber'></span> / <span class='totalPages'></span></span></div>"),
             margin={"top": "16mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
    tmp.unlink()


def find_section_pages(pdf_path):
    reader = PdfReader(str(pdf_path))
    texts = [(p.extract_text() or "") for p in reader.pages]
    pages = {}
    for i in range(1, len(SECTIONS) + 1):
        marker = f"Document ID: DOC-{i:02d}"      # first line under every section title
        for n, t in enumerate(texts, 1):
            if marker in t:
                pages[i] = n
                break
    return pages, len(texts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="<GITHUB_REPOSITORY_URL>")
    ap.add_argument("--youtrack", default="<YOUTRACK_PROJECT_URL>")
    ap.add_argument("--tag", default="prob-period-1")
    ap.add_argument("--group", default="SE-2406")
    ap.add_argument("--representative", default="Orazbek")
    ap.add_argument("--out-dir", default=str(ROOT / "dist"))
    a = ap.parse_args()
    out_dir = pathlib.Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{a.group}_{a.representative}_ProbPeriod1.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        render(page, build_html(a), out)            # pass 1: find where sections start
        pages, total = find_section_pages(out)
        render(page, build_html(a, pages), out)     # pass 2: TOC with page numbers
        b.close()
    print(f"written {out} ({total} pages); section start pages: {pages}")


if __name__ == "__main__":
    main()
