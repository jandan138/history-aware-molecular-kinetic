# Renderer Contract

## 1. Role

The renderer is a read-only evidence client. It accepts canonical artifacts and a
versioned render configuration, then emits images/videos plus a deterministic
manifest. It never calls a solver or a partition policy.

The repository defines:

- `schemas/render-config.schema.json`;
- `schemas/render-manifest.schema.json`;
- `configs/render/*.yml`;
- `src/historykinetic/rendering/` semantic contracts;
- a dependency-free `ManifestOnlyRenderer` that exercises provenance before a GPU
  backend exists.

---

## 2. Inputs

The renderer accepts only canonical artifacts:

- particle bundle;
- kinetic bundle/display sampling source;
- block-state bundle;
- partition mask;
- collision/history features;
- discrepancy/metrics report;
- conversion report;
- geometry bundle;
- camera/render configuration.

All paths are run-relative and all primary inputs must have content hashes before a
B5 case is frozen.

---

## 3. Outputs

Every renderer writes:

```text
render-manifest.json
frames/ or video
visual-metrics.json
comparison-lock report
optional contact sheet / diagnostics
```

The manifest records:

- renderer name/version;
- scene/config ID;
- config, camera, display-policy, and comparison-lock hashes;
- artifact references and hashes;
- frame schedule;
- output specification;
- shot IDs and optional case/run/claim/metric links;
- evidence flags.

Planning and diagnostic renders may carry incomplete evidence links. A frozen B5
primary frame or clip must set `evidence_links.complete=true`; the schema then
requires a case ID, at least one run ID, at least one claim ID, all shot IDs, and
at least one linked metrics artifact. The render configuration remains immutable;
the final run/claim binding is supplied when the manifest is created.

---

## 4. Display particles

Statistical display particles are explicitly marked non-physical. They may be
resampled for rendering but cannot enter:

- conservation metrics;
- collision history;
- partition decisions;
- exact identity tracks;
- scientific particle counts.

A temporal display policy may preserve synthetic IDs for visual continuity, but
those IDs must never be described as true molecular identities.

---

## 5. Comparison lock

Primary comparison groups share:

- camera path;
- resolution and frame times;
- geometry and materials;
- transfer functions;
- exact display radius;
- statistical display particle policy and seed;
- motion blur and temporal filtering;
- tone mapping;
- diagnostic layout.

`comparison_lock_digest()` hashes the locked fields. A changed camera or display
policy therefore produces a different lock hash.

---

## 6. Physics/rendering separation

Changing camera, FOV, output resolution, particle display budget, or diagnostic
visibility must not change the partition artifact hash.

Volume/particle blending may change with screen-space coverage, but it must avoid
visually double-counting the same mass. This is a display partition, not a physical
conversion.

---

## 7. Forbidden behavior

- changing physics state;
- deleting “ugly” particles by method-specific rules;
- applying different smoothing to different methods;
- using future frames to stabilize only the proposed result;
- rendering exact particles more densely than baselines without disclosure;
- using camera distance to trigger physical promotion;
- adding artist-authored plume noise absent from artifacts;
- hand-entering metric values into the final frame;
- selecting a favorable seed without a declared selection rule.

---

## 8. Backend evolution

The renderer interface is intentionally backend-independent. Candidate
implementations may include:

- a lightweight OpenGL/Vulkan replay viewer;
- Blender/Usd/Hydra offline rendering;
- a custom CUDA volume/particle renderer;
- a scientific plotting/contact-sheet backend.

All backends must preserve the same manifest and comparison-lock semantics.


## 9. Primary comparison audit

Before a primary panel, figure, or clip is frozen, every method manifest in the
comparison group is checked by `scripts/audit_render_manifests.py`. The audit
requires identical comparison-lock digest, renderer digest, scene ID, frame
schedule, output settings, and content-hashed camera paths. With
`--require-complete-evidence`, every manifest must also bind a benchmark case,
run IDs, claim IDs, shot IDs, and at least one metrics artifact.

A render that fails this audit may remain a diagnostic image, but it cannot enter
the primary paper/video evidence registry.
