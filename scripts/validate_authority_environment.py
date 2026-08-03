#!/usr/bin/env python3
"""Validate that the repository presents one current, non-competing authority.

Checks R-AUTHORITY-MIGRATION: a fresh session reading the repository must
reach current authorities without encountering a competing generic control
plane or stale four-work instructions presented as active guidance.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_CONTROL_PLANE_PATHS = [
    ".claude",
    "project-relay",
    "PROJECT_RELAY.md",
]

STALE_FOUR_WORK_PATTERN = re.compile(r"\bfour[\s-](?:browser-native\s+)?works?\b", re.IGNORECASE)


def fail(errors: list[str]) -> int:
    for e in errors:
        print(f"FAIL: {e}")
    return 1


def main() -> int:
    errors: list[str] = []

    claude_md = ROOT / "CLAUDE.md"
    if not claude_md.is_file():
        errors.append("CLAUDE.md is missing at repository root")
    else:
        text = claude_md.read_text(encoding="utf-8")
        required_sections = [
            "Authority order",
            "Protected artifacts",
            "Branch and external-action safety",
        ]
        for section in required_sections:
            if section not in text:
                errors.append(f"CLAUDE.md is missing required section: {section}")
        if len(text.split()) > 600:
            errors.append("CLAUDE.md is too long to be a short boundary pointer (over 600 words)")

    for rel in FORBIDDEN_CONTROL_PLANE_PATHS:
        if (ROOT / rel).exists():
            errors.append(f"forbidden generic control-plane path exists: {rel}")

    for rel in ["README.md", "docs/DEPLOYMENT.md"]:
        p = ROOT / rel
        if p.is_file() and STALE_FOUR_WORK_PATTERN.search(p.read_text(encoding="utf-8")):
            errors.append(f"{rel} still presents a stale four-work statement")

    domain_doc = ROOT / "docs" / "DOMAIN_MIGRATION_DECISION.md"
    if domain_doc.is_file():
        text = domain_doc.read_text(encoding="utf-8")
        if "Historical record" not in text and "historical record" not in text.lower():
            errors.append("docs/DOMAIN_MIGRATION_DECISION.md is not labelled as historical record")

    if errors:
        return fail(errors)

    print("PASS: repository presents one current authority with no competing control plane")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
