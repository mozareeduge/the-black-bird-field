from __future__ import annotations
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

REQUIRED_WORK_KEYS = {
    "schema_version", "slug", "asset_slug", "order", "title", "mode", "form", "year",
    "summary", "responsibility", "meta_description", "live_url", "repository_url",
    "poster_caption", "feature_caption", "feature_image", "hero_lead", "prelude", "views",
    "context", "identity", "citation",
}


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: invalid JSON: {exc}") from exc


def load_site() -> dict:
    site = _read_json(CONTENT / "site.json")
    required = {"site_title", "site_origin", "artistic_name", "formal_name", "year", "shared", "practice", "about", "contact", "metadata", "documents"}
    missing = required - set(site)
    if missing:
        raise ValueError(f"site.json: missing required keys {sorted(missing)}")
    origin = urlparse(site["site_origin"])
    if origin.scheme != "https" or not origin.netloc or origin.path not in ("", "/"):
        raise ValueError("site.json: site_origin must be an HTTPS origin without a path")
    cv = site["documents"].get("cv", {})
    if not cv.get("path") or not cv.get("label"):
        raise ValueError("site.json: documents.cv requires path and label")
    for m in site["practice"].get("modules", []):
        for i, link in enumerate(m.get("links") or []):
            _nonempty(link.get("label"), f"site.json practice.modules[{m.get('id')}].links[{i}].label")
            _check_link_url(link.get("url", ""), f"site.json practice.modules[{m.get('id')}].links[{i}].url")
    return site


def _nonempty(value, where: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}: expected non-empty string")


def _check_link_url(url, where: str) -> None:
    """A link is either an HTTPS URL or a site route such as /research/<slug>/."""
    if isinstance(url, str) and re.fullmatch(r"/(?:[a-z0-9-]+/)+", url):
        return
    parsed = urlparse(url if isinstance(url, str) else "")
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"{where}: must be an HTTPS URL or a site route like /research/<slug>/")


def _validate_work(work: dict, path: Path) -> None:
    name = path.name
    missing = REQUIRED_WORK_KEYS - set(work)
    if missing:
        raise ValueError(f"{name}: missing required keys {sorted(missing)}")
    if work["schema_version"] != "1.0.0":
        raise ValueError(f"{name}: unsupported schema_version {work['schema_version']!r}")
    if work["slug"] != path.stem:
        raise ValueError(f"{name}: slug must equal filename stem")
    if not SLUG_RE.fullmatch(work["slug"]):
        raise ValueError(f"{name}: invalid slug {work['slug']!r}")
    if not SLUG_RE.fullmatch(work["asset_slug"]):
        raise ValueError(f"{name}: invalid asset_slug {work['asset_slug']!r}")
    if not isinstance(work["order"], int) or work["order"] < 1:
        raise ValueError(f"{name}: order must be an integer >= 1")
    if not isinstance(work["year"], int) or not (2000 <= work["year"] <= 2100):
        raise ValueError(f"{name}: year must be a plausible integer")
    for key in ("title", "mode", "form", "summary", "responsibility", "meta_description", "poster_caption", "feature_caption", "feature_image", "hero_lead"):
        _nonempty(work[key], f"{name}.{key}")
    for key in ("live_url", "repository_url"):
        parsed = urlparse(work[key])
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"{name}.{key}: must be an HTTPS URL")
    if urlparse(work["repository_url"]).netloc.lower() != "github.com":
        raise ValueError(f"{name}.repository_url: must point to github.com")
    prelude = work["prelude"]
    _nonempty(prelude.get("label"), f"{name}.prelude.label")
    items = prelude.get("items")
    if not isinstance(items, list) or len(items) != 3 or any(not isinstance(x, dict) or set(x) != {"label", "title", "note"} for x in items):
        raise ValueError(f"{name}.prelude.items: exactly three labeled condition records required")
    views = work["views"]
    _nonempty(views.get("title"), f"{name}.views.title")
    _nonempty(views.get("intro"), f"{name}.views.intro")
    items = views.get("items")
    if not isinstance(items, list) or len(items) != 3 or any(not isinstance(x, dict) or set(x) != {"number", "title", "text", "role", "alt"} for x in items):
        raise ValueError(f"{name}.views.items: exactly three labeled view records required")
    roles = {x["role"] for x in items}
    if work["feature_image"] not in roles:
        raise ValueError(f"{name}.feature_image: must name one selected-view role")
    context = work["context"]
    _nonempty(context.get("title"), f"{name}.context.title")
    if not isinstance(context.get("paragraphs"), list) or not context["paragraphs"]:
        raise ValueError(f"{name}.context.paragraphs: at least one paragraph required")
    for i, text in enumerate(context["paragraphs"]):
        _nonempty(text, f"{name}.context.paragraphs[{i}]")
    identity = work["identity"]
    for key in ("edition", "language", "encounter"):
        _nonempty(identity.get(key), f"{name}.identity.{key}")
    annex = work.get("annex")
    if annex is not None:
        _nonempty(annex.get("label"), f"{name}.annex.label")
        _nonempty(annex.get("title"), f"{name}.annex.title")
        if not isinstance(annex.get("paragraphs"), list) or not annex["paragraphs"]:
            raise ValueError(f"{name}.annex.paragraphs: at least one paragraph required")
        for i, text in enumerate(annex["paragraphs"]):
            _nonempty(text, f"{name}.annex.paragraphs[{i}]")
        for i, link in enumerate(annex.get("links", [])):
            _nonempty(link.get("label"), f"{name}.annex.links[{i}].label")
            if urlparse(link.get("url", "")).scheme != "https":
                raise ValueError(f"{name}.annex.links[{i}].url: must be an HTTPS URL")
    for i, link in enumerate(context.get("links", [])):
        _nonempty(link.get("label"), f"{name}.context.links[{i}].label")
        _check_link_url(link.get("url", ""), f"{name}.context.links[{i}].url")
    citation = work["citation"]
    for key in ("author", "title", "rest"):
        _nonempty(citation.get(key), f"{name}.citation.{key}")


def load_works() -> list[dict]:
    works = []
    for path in sorted((CONTENT / "works").glob("*.json")):
        work = _read_json(path)
        _validate_work(work, path)
        works.append(work)
    if not works:
        raise ValueError("No work manifests found")
    orders = [w["order"] for w in works]
    slugs = [w["slug"] for w in works]
    asset_slugs = [w["asset_slug"] for w in works]
    if len(set(orders)) != len(orders):
        raise ValueError("Work order values must be unique")
    if sorted(orders) != list(range(1, len(works) + 1)):
        raise ValueError(f"Work order values must be contiguous 1..{len(works)}")
    if len(set(slugs)) != len(slugs):
        raise ValueError("Work slugs must be unique")
    if len(set(asset_slugs)) != len(asset_slugs):
        raise ValueError("Work asset_slug values must be unique")
    return sorted(works, key=lambda w: w["order"])


def load_research() -> list[dict]:
    """Research pages: cleared text stored as data in content/research/<slug>.json.

    Paragraphs and record texts carry inline Markdown only (*em*, **strong**, `code`, [text](url)).
    They are not works: no images, modes or order; they render at /research/<slug>/.
    """
    pages = []
    for path in sorted((CONTENT / "research").glob("*.json")):
        page = _read_json(path)
        name = path.name
        if page.get("schema_version") != "1.0.0":
            raise ValueError(f"{name}: unsupported schema_version {page.get('schema_version')!r}")
        if page.get("slug") != path.stem or not SLUG_RE.fullmatch(page.get("slug", "")):
            raise ValueError(f"{name}: slug must equal filename stem")
        for key in ("title", "subtitle", "meta_description"):
            _nonempty(page.get(key), f"{name}.{key}")
        if not isinstance(page.get("paragraphs"), list) or not page["paragraphs"]:
            raise ValueError(f"{name}.paragraphs: at least one paragraph required")
        for i, text in enumerate(page["paragraphs"]):
            _nonempty(text, f"{name}.paragraphs[{i}]")
        for i, row in enumerate(page.get("record", [])):
            _nonempty(row.get("term"), f"{name}.record[{i}].term")
            _nonempty(row.get("text"), f"{name}.record[{i}].text")
        pages.append(page)
    return pages


def load_writing() -> list[dict]:
    """Writing editions: complete literary texts stored as data in content/writing/<slug>.json.

    `text` is produced only by scripts/extract_ten_research_poems.py from the author's docx; do not
    hand-edit it. Editions are not works (not counted, no images or modes); they render at
    /writing/<slug>/ in their own language and direction.
    """
    pages = []
    for path in sorted((CONTENT / "writing").glob("*.json")):
        page = _read_json(path)
        name = path.name
        if page.get("schema_version") != "1.0.0":
            raise ValueError(f"{name}: unsupported schema_version {page.get('schema_version')!r}")
        if page.get("slug") != path.stem or not SLUG_RE.fullmatch(page.get("slug", "")):
            raise ValueError(f"{name}: slug must equal filename stem")
        for key in ("title_en", "title_fa", "author_en", "author_fa", "meta_description"):
            _nonempty(page.get(key), f"{name}.{key}")
        ed = page.get("edition") or {}
        for key in ("version", "years", "first_published", "copyright_fa", "copyright_en", "rights_fa", "rights_en", "license_en", "citation_fa", "citation_en"):
            _nonempty(ed.get(key), f"{name}.edition.{key}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", ed["first_published"]):
            raise ValueError(f"{name}.edition.first_published: ISO date required")
        pdf = page.get("pdf") or {}
        if not re.fullmatch(r"documents/[A-Za-z0-9_.-]+\.pdf", pdf.get("path", "")) or not re.fullmatch(r"[0-9a-f]{64}", pdf.get("sha256", "")):
            raise ValueError(f"{name}.pdf: ASCII documents/<file>.pdf path and sha256 required")
        text = page.get("text") or {}
        seqs = text.get("sequences") or []
        if not seqs or [s.get("number") for s in seqs] != list(range(1, len(seqs) + 1)):
            raise ValueError(f"{name}.text.sequences: numbered sequences required (run the extract script)")
        for s in seqs:
            if s.get("anchor") != f"poem-{s['number']}" or not s.get("poem") or not (s.get("bibliography") or {}).get("entries"):
                raise ValueError(f"{name}.text.sequences[{s['number']}]: anchor, poem and bibliography required")
        pages.append(page)
    return pages


def load_protected_artifacts() -> dict:
    data = _read_json(CONTENT / "protected_artifacts.json")
    if data.get("schema_version") != "1.0.0" or not data.get("baseline_commit"):
        raise ValueError("protected_artifacts.json: invalid authority header")
    required = {"grave_machine_runtime", "academic_cv"}
    if set(data.get("artifacts", {})) != required:
        raise ValueError("protected_artifacts.json: artifact set must be exactly grave_machine_runtime + academic_cv")
    return data
