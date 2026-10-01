import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import build
from content import load_site, load_works


def test_build_rejects_docx_masquerading_as_protected_cv_pdf(tmp_path, monkeypatch):
    fake = tmp_path / "AcademicCV.pdf"
    fake.write_bytes(b"PK\x03\x04not a PDF")
    authority = copy.deepcopy(json.loads((ROOT / "content/protected_artifacts.json").read_text()))
    cv = authority["artifacts"]["academic_cv"]
    payload = fake.read_bytes()
    cv["size_bytes"] = len(payload)
    cv["git_blob_sha1"] = hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()
    grave = authority["artifacts"]["grave_machine_runtime"]
    monkeypatch.setattr(build, "protected_paths", lambda _: (ROOT / grave["source_path"], grave, fake, cv))

    with pytest.raises(SystemExit, match="protected CV is not a PDF"):
        build.validate_sources(load_site(), load_works(), authority)
