"""DIP-15: traceability checks across the documentation set.

* every test ID referenced in the requirements (DOC-06) is defined in the verification plan (DOC-09);
* every YouTrack ID mentioned anywhere in the docs exists in the backlog;
* every "DOC-xx §n.m" cross-reference points to an existing section;
* the backlog generator's own consistency checks pass (dependencies, dates, commit format).
"""
import csv
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = sorted((ROOT / "docs").glob("[0-9][0-9]-*.md"))
TEXT = {p: p.read_text(encoding="utf-8") for p in DOCS + [ROOT / "README.md"]}


def _expand_test_ids(text: str) -> set[str]:
    ids = set()
    for m in re.finditer(r"TC-([A-Z]+)-(\d{2})(?:…TC-[A-Z]+-(\d{2})|…(\d{2}))?", text):
        start = int(m.group(2))
        end = int(m.group(3) or m.group(4) or start)
        ids |= {f"TC-{m.group(1)}-{i:02d}" for i in range(start, end + 1)}
    return ids


def test_all_referenced_tests_are_defined():
    req = (ROOT / "docs" / "06-requirements.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs" / "09-verification-plan.md").read_text(encoding="utf-8")
    defined = set(re.findall(r"^\| (TC-[A-Z]+-\d{2}) \|", plan, re.M))
    missing = _expand_test_ids(req) - defined
    assert not missing, f"tests referenced in DOC-06 but not defined in DOC-09: {sorted(missing)}"


def test_all_youtrack_ids_exist_in_backlog():
    with open(ROOT / "docs" / "pm" / "backlog.csv", encoding="utf-8-sig") as f:
        backlog = {int(row["Issue ID"].split("-")[1]) for row in csv.DictReader(f)}
    # compare by number, so the legacy form "DIP-01" in the first commit message matches DIP-1
    used = {int(m) for t in TEXT.values() for m in re.findall(r"DIP-(\d+)\b", t)}
    assert not used - backlog, f"unknown issues: {sorted(used - backlog)}"


def test_cross_document_section_references_resolve():
    headings = {}
    for p in DOCS:
        headings[f"DOC-{p.name[:2]}"] = set(re.findall(r"^#{2,4} (\d+(?:\.\d+)+)", TEXT[p], re.M))
    broken = []
    for p, t in TEXT.items():
        for doc, sec in re.findall(r"(DOC-\d\d)\s*§\s*(\d+(?:\.\d+)+)", t):
            if doc in headings and sec not in headings[doc]:
                broken.append(f"{p.name}: {doc} §{sec}")
    assert not broken, broken


def test_backlog_generator_checks_pass():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "backlog.py"), "--check"],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
