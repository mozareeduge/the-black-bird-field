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
    return site


def _nonempty(value, where: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}: expected non-empty string")


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
    if not isinstance(items, list) or len(items) != 3 or any(not isinstance(x, list) or len(x) != 3 for x in items):
        raise ValueError(f"{name}.prelude.items: exactly three [label,title,note] records required")
    views = work["views"]
    _nonempty(views.get("title"), f"{name}.views.title")
    _nonempty(views.get("intro"), f"{name}.views.intro")
    items = views.get("items")
    if not isinstance(items, list) or len(items) != 3 or any(not isinstance(x, list) or len(x) != 5 for x in items):
        raise ValueError(f"{name}.views.items: exactly three [no,title,text,role,alt] records required")
    roles = {x[3] for x in items}
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


def load_protected_artifacts() -> dict:
    data = _read_json(CONTENT / "protected_artifacts.json")
    if data.get("schema_version") != "1.0.0" or not data.get("baseline_commit"):
        raise ValueError("protected_artifacts.json: invalid authority header")
    required = {"grave_machine_runtime", "academic_cv"}
    if set(data.get("artifacts", {})) != required:
        raise ValueError("protected_artifacts.json: artifact set must be exactly grave_machine_runtime + academic_cv")
    return data
