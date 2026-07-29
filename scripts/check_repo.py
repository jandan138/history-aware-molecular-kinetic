from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "mkdocs.yml",
    "docs/vision/research-thesis.md",
    "docs/research/deng-hard-sphere-connection.md",
    "docs/research/related-work.md",
    "docs/architecture/overview.md",
    "docs/benchmarks/suite.md",
    "docs/roadmap/go-no-go-gates.md",
    "references/sources.yaml",
    "paper/claim-ledger.md",
    "schemas/benchmark-case.schema.json",
    "schemas/source-lock.schema.json",
]

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def check_required() -> list[str]:
    return [f"missing required path: {path}" for path in REQUIRED if not (ROOT / path).exists()]


def check_markdown_links() -> list[str]:
    errors: list[str] = []
    for file in ROOT.rglob("*.md"):
        if ".git" in file.parts:
            continue
        text = file.read_text(encoding="utf-8")
        for raw in MARKDOWN_LINK.findall(text):
            target = raw.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (file.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"broken link in {file.relative_to(ROOT)}: {raw}")
    return errors


def check_no_third_party_source() -> list[str]:
    forbidden = [ROOT / "third_party" / "checkouts", ROOT / "vendor"]
    errors: list[str] = []
    for path in forbidden:
        if path.exists() and any(path.rglob("*")):
            errors.append(f"third-party source must not be committed: {path.relative_to(ROOT)}")
    return errors


def check_case_layout() -> list[str]:
    errors: list[str] = []
    for suite in (ROOT / "benchmarks").iterdir():
        if not suite.is_dir() or suite.name.startswith("."):
            continue
        if suite.name == "README.md":
            continue
        for relative in ("cases/candidate", "cases/frozen", "expected"):
            if not (suite / relative).is_dir():
                errors.append(f"missing benchmark lifecycle directory: {suite.name}/{relative}")
    return errors


def main() -> int:
    errors = (
        check_required()
        + check_markdown_links()
        + check_no_third_party_source()
        + check_case_layout()
    )
    if errors:
        print("repository check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("repository check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
