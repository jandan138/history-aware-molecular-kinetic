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
