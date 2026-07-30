from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = (
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
    "docs/demos/visual-production-roadmap.md",
    "docs/demos/art-direction.md",
    "docs/demos/storyboard.md",
    "docs/demos/visual-acceptance-criteria.md",
    "docs/demos/claim-to-visual-evidence.md",
    "docs/demos/scene-specs/README.md",
    "docs/roadmap/demo-production-backlog.md",
    "references/sources.yaml",
    "paper/claim-ledger.md",
    "configs/render/README.md",
    "configs/render/diagnostic.yml",
    "configs/render/shared-comparison.yml",
    "configs/render/hero.yml",
    "scripts/create_render_manifest.py",
    "scripts/audit_render_manifests.py",
    "scripts/validate_render_configs.py",
    "schemas/benchmark-case.schema.json",
    "schemas/source-lock.schema.json",
    "schemas/camera-path.schema.json",
    "schemas/render-config.schema.json",
    "schemas/render-manifest.schema.json",
    "src/historykinetic/rendering/audit.py",
    "schemas/examples/camera-path.json",
    "schemas/examples/render-config.json",
    "schemas/examples/render-manifest.json",
    "schemas/examples/render-artifacts.json",
)

SCENE_SLUGS = (
    "zoomable-mixing",
    "correlation-labyrinth",
    "expansion-into-vacuum",
)

B5_CASES = (
    "B5-ZOOM-MIX-v0.yml",
    "B5-CORRELATION-LABYRINTH-v0.yml",
    "B5-EXPANSION-VACUUM-v0.yml",
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def check_required() -> list[str]:
    return [
        f"missing required path: {path}"
        for path in REQUIRED
        if not (ROOT / path).exists()
    ]


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
    forbidden = (ROOT / "third_party" / "checkouts", ROOT / "vendor")
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
        for relative in ("cases/candidate", "cases/frozen", "expected"):
            if not (suite / relative).is_dir():
                errors.append(f"missing benchmark lifecycle directory: {suite.name}/{relative}")
    return errors


def check_visual_production_layout() -> list[str]:
    required = [
        *(f"configs/render/scenes/{slug}.yml" for slug in SCENE_SLUGS),
        *(f"docs/demos/scene-specs/{slug}.md" for slug in SCENE_SLUGS),
        *(
            f"benchmarks/b5_graphics_evidence/cases/candidate/{case_name}"
            for case_name in B5_CASES
        ),
    ]
    errors = [
        f"missing visual-production path: {path}"
        for path in required
        if not (ROOT / path).exists()
    ]

    camera_files = list((ROOT / "configs" / "render" / "cameras").rglob("*.json"))
    if len(camera_files) < 3:
        errors.append("expected versioned camera paths under configs/render/cameras")
    return errors


def main() -> int:
    errors = (
        check_required()
        + check_markdown_links()
        + check_no_third_party_source()
        + check_case_layout()
        + check_visual_production_layout()
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
