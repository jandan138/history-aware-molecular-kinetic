.PHONY: test lint typecheck check render-check render-manifest-smoke render-audit-smoke native docs clean

test:
	PYTHONPATH=src python -m pytest

lint:
	ruff check src scripts tests

typecheck:
	mypy src

check: lint typecheck test render-check render-manifest-smoke render-audit-smoke
	python scripts/check_repo.py

render-check:
	PYTHONPATH=src python scripts/validate_render_configs.py

render-manifest-smoke:
	rm -rf build/render-manifest-smoke
	PYTHONPATH=src python scripts/create_render_manifest.py \
		--config configs/render/shared-comparison.yml \
		--artifacts schemas/examples/render-artifacts.json \
		--output build/render-manifest-smoke

render-audit-smoke:
	rm -rf build/render-audit-smoke
	PYTHONPATH=src python scripts/create_render_manifest.py \
		--config configs/render/shared-comparison.yml \
		--artifacts schemas/examples/render-artifacts.json \
		--case-id B5-SHARED-COMPARISON-v0 \
		--run-id run-reference \
		--claim-id C7 \
		--output build/render-audit-smoke/reference
	PYTHONPATH=src python scripts/create_render_manifest.py \
		--config configs/render/shared-comparison.yml \
		--artifacts schemas/examples/render-artifacts.json \
		--case-id B5-SHARED-COMPARISON-v0 \
		--run-id run-proposed \
		--claim-id C7 \
		--output build/render-audit-smoke/proposed
	PYTHONPATH=src python scripts/audit_render_manifests.py \
		--require-complete-evidence \
		build/render-audit-smoke/reference/render-manifest.json \
		build/render-audit-smoke/proposed/render-manifest.json

native:
	cmake -S native -B build/native -DCMAKE_BUILD_TYPE=Release
	cmake --build build/native --parallel
	ctest --test-dir build/native --output-on-failure

docs:
	mkdocs build --strict

clean:
	rm -rf build .pytest_cache .mypy_cache .ruff_cache site
