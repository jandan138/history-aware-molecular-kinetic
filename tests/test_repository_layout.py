from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_primary_planes_exist() -> None:
    primary_planes = [
        "adapters",
        "benchmarks",
        "docs",
        "native",
        "paper",
        "references",
        "schemas",
        "src",
        "tests",
    ]
    for path in primary_planes:
        assert (ROOT / path).exists(), path


def test_benchmark_lifecycle_layout() -> None:
    for suite in (ROOT / "benchmarks").iterdir():
        if not suite.is_dir():
            continue
        for relative in ["cases/candidate", "cases/frozen", "expected"]:
            assert (suite / relative).is_dir(), f"{suite.name}/{relative}"


def test_visual_production_layout() -> None:
    required = [
        "configs/render",
        "docs/demos/scene-specs",
        "docs/demos/visual-production-roadmap.md",
        "docs/demos/art-direction.md",
        "docs/demos/storyboard.md",
        "docs/demos/visual-acceptance-criteria.md",
        "docs/roadmap/demo-production-backlog.md",
        "scripts/audit_render_manifests.py",
        "src/historykinetic/rendering/audit.py",
    ]
    for path in required:
        assert (ROOT / path).exists(), path

    candidate_root = ROOT / "benchmarks/b5_graphics_evidence/cases/candidate"
    b5_cases = {path.name for path in candidate_root.glob("*.yml")}
    assert {
        "B5-ZOOM-MIX-v0.yml",
        "B5-CORRELATION-LABYRINTH-v0.yml",
        "B5-EXPANSION-VACUUM-v0.yml",
    }.issubset(b5_cases)
