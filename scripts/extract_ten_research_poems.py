#!/usr/bin/env python3
"""Extract *Ten Research Poems* (ده شعر پژوهشی) from the author's docx into content data.

Deterministic: the same docx always yields the same JSON. Text is copied exactly as written
(no Unicode normalisation, no whitespace trimming, ZWNJ U+200C and LRM U+200E kept), so the
published page can be checked character for character against the source.

Structure read from the docx (6 Sep 2026 version):
  title · author · '—' · intro heading (bold) · intro paragraphs
  ten sequences, each: heading 'N. title' (bold, red) · source passage (optional bold red
  sub-labels 'یک.', 'دو.' …) · '───' separator · poem lines (blank paragraph = stanza break;
  bold red line = poem label; grey line = cross-reference note)
  'منابع' · per-sequence bibliography heading (bold) · entries (right-aligned = Latin, LTR)

Empty paragraphs in source passages and in the bibliography are page padding in the docx and are
not stored; the page gives every source passage the same space before its separator.

Usage:  python scripts/extract_ten_research_poems.py [--docx PATH] [--check]
  --check   fail if content/writing/ten-research-poems.json differs from a fresh extraction
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCX = Path(r"C:/Users/Zarinpal/Documents/Personal Formal Documents/Artworks/ده_شعر_پژوهشی_محمد_زارع.docx")
OUT = ROOT / "content" / "writing" / "ten-research-poems.json"
SEPARATOR = "───"
HEADING_RE = re.compile(r"^([۰-۹]+)\.(\s+)(.+)$")
FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"


def fa_to_int(s: str) -> int:
    return int("".join(str(FA_DIGITS.index(c)) for c in s))


def color(p) -> str | None:
    for r in p.runs:
        if r.text.strip() and r.font.color is not None and r.font.color.type is not None:
            return str(r.font.color.rgb)
    return None


def bold(p) -> bool:
    runs = [r for r in p.runs if r.text.strip()]
    return bool(runs) and all(r.bold for r in runs)


def paragraphs(docx_path: Path) -> list[dict]:
    import docx  # python-docx
    d = docx.Document(str(docx_path))
    out = []
    for p in d.paragraphs:
        align = p.alignment
        out.append({"text": p.text, "bold": bold(p), "color": color(p),
                    "align": None if align is None else int(align)})
    return out


def extract(docx_path: Path) -> dict:
    ps = paragraphs(docx_path)
    i = 0

    def take() -> dict:
        nonlocal i
        p = ps[i]; i += 1
        return p

    title = take(); author = take(); mark = take(); intro_head = take()
    assert title["bold"] and title["text"] == "ده شعر پژوهشی", title
    assert author["text"] == "محمد زارع", author
    assert mark["text"] == "—", mark
    assert intro_head["bold"], intro_head
    intro = []
    while not (ps[i]["bold"] and HEADING_RE.match(ps[i]["text"])):
        if ps[i]["text"]:
            intro.append(ps[i]["text"])
        i += 1

    sequences = []
    while ps[i]["text"] != "منابع":
        head = take()
        m = HEADING_RE.match(head["text"])
        assert head["bold"] and m, head
        n = fa_to_int(m.group(1))
        assert n == len(sequences) + 1, (n, head)
        source = []
        while ps[i]["text"] != SEPARATOR:
            p = take()
            if not p["text"]:
                continue
            source.append({"type": "label" if p["bold"] else "para", "text": p["text"]})
        take()  # separator
        poem = []
        while not (ps[i]["bold"] and (HEADING_RE.match(ps[i]["text"]) or ps[i]["text"] == "منابع")):
            p = take()
            if not p["text"]:
                poem.append({"type": "break"})
            elif p["bold"]:
                poem.append({"type": "label", "text": p["text"]})
            elif p["color"] == "646464":
                poem.append({"type": "note", "text": p["text"]})
            else:
                poem.append({"type": "line", "text": p["text"]})
        while poem and poem[-1]["type"] == "break":
            poem.pop()
        sequences.append({"number": n, "anchor": f"poem-{n}", "heading": head["text"],
                          "numeral": m.group(1) + ".", "title": m.group(3).strip(),
                          "source": source, "poem": poem, "bibliography": None})

    bib_head = take()
    assert bib_head["bold"] and bib_head["text"] == "منابع"
    current = None
    while i < len(ps):
        p = take()
        if not p["text"]:
            continue
        m = HEADING_RE.match(p["text"])
        if p["bold"] and m:
            current = sequences[fa_to_int(m.group(1)) - 1]
            assert current["bibliography"] is None, p
            current["bibliography"] = {"heading": p["text"], "entries": []}
            continue
        assert current is not None, p
        latin = p["align"] == 2 or bool(re.search(r"[A-Za-z]{3}", p["text"]) and not re.search(r"[\u0600-\u06FF]", p["text"]))
        current["bibliography"]["entries"].append({"lang": "en" if latin else "fa", "text": p["text"]})

    assert len(sequences) == 10, len(sequences)
    assert all(s["bibliography"] and s["bibliography"]["entries"] for s in sequences)
    return {
        "title": title["text"],
        "author": author["text"],
        "mark": mark["text"],
        "separator": SEPARATOR,
        "intro": {"heading": intro_head["text"], "paragraphs": intro},
        "sequences": sequences,
        "bibliography_heading": bib_head["text"],
    }


def source_texts(docx_path: Path) -> list[str]:
    """Every non-empty docx paragraph, in order, exactly as written (the verification reference)."""
    return [p["text"] for p in paragraphs(docx_path) if p["text"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", type=Path, default=DEFAULT_DOCX)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    text = extract(a.docx)
    if OUT.exists():
        page = json.loads(OUT.read_text(encoding="utf-8"))
    else:
        raise SystemExit(f"{OUT} missing: create it with the edition metadata first")
    if a.check:
        if page.get("text") != text:
            raise SystemExit("ten-research-poems.json text differs from the docx")
        print("OK: content/writing/ten-research-poems.json matches the docx")
        return
    page["text"] = text
    OUT.write_text(json.dumps(page, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n_chars = sum(len(t) for t in source_texts(a.docx))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(text['sequences'])} sequences, {n_chars} source characters")


if __name__ == "__main__":
    sys.exit(main())
