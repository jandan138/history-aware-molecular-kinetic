.PHONY: test lint typecheck check native docs clean

test:
	python -m pytest

lint:
	ruff check src scripts tests

typecheck:
	mypy src

check: lint typecheck test
	python scripts/check_repo.py

native:
	cmake -S native -B build/native -DCMAKE_BUILD_TYPE=Release
	cmake --build build/native --parallel
	ctest --test-dir build/native --output-on-failure

docs:
	mkdocs build --strict

clean:
	rm -rf build .pytest_cache .mypy_cache .ruff_cache site
