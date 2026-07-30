# Render configurations

Render configuration is versioned separately from physics cases.

```text
configs/render/
├── diagnostic.yml          fast scientific debugging
├── shared-comparison.yml   locked primary comparisons
├── hero.yml                shared Hero defaults after scientific gates
├── cameras/                versioned camera paths and shot keyframes
└── scenes/                 complete scene/shot plans
```

Rules:

- physics artifacts are immutable inputs;
- camera and display LOD never alter physical partitioning;
- primary method comparisons share one comparison-lock group;
- statistical display particles are marked non-physical;
- scene configs validate against `schemas/render-config.schema.json`;
- camera paths validate against `schemas/camera-path.schema.json`;
- every output records `schemas/render-manifest.schema.json` metadata.

Validation:

```bash
PYTHONPATH=src python scripts/validate_render_configs.py
```

Create a provenance-only manifest before a production renderer exists:

```bash
PYTHONPATH=src python scripts/create_render_manifest.py \
  --config configs/render/shared-comparison.yml \
  --artifacts schemas/examples/render-artifacts.json \
  --output results/render-manifest-smoke
```

For a final B5 evidence render, bind the immutable render plan to the actual
case, runs, claims, and metrics artifacts without editing the camera/material
configuration:

```bash
PYTHONPATH=src python scripts/create_render_manifest.py \
  --config configs/render/scenes/expansion-into-vacuum.yml \
  --artifacts results/B5-EXPANSION-VACUUM-v0/render-artifacts.json \
  --case-id B5-EXPANSION-VACUUM-v0 \
  --run-id run-expansion-reference \
  --run-id run-expansion-proposed \
  --claim-id C4 --claim-id C7 --claim-id C8 --claim-id C9 \
  --output results/B5-EXPANSION-VACUUM-v0/render
```

The generated manifest marks `evidence_links.complete=true` only when case,
shot, run, claim, and metrics links are all present.

Audit two or more primary comparison manifests:

```bash
PYTHONPATH=src python scripts/audit_render_manifests.py \
  results/reference/render-manifest.json \
  results/proposed/render-manifest.json \
  --require-complete-evidence
```
