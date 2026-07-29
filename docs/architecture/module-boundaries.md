# Module boundaries

## Python package

### `historykinetic.contracts`

Small immutable semantic types: collision events, block summaries, history
features, conservation budgets, representation kinds, partition decisions, and
artifact references.

It must remain dependency-free.

### `historykinetic.ids`

Canonical serialization and content-derived identifiers. IDs must not depend on
JSON key order, file location, or process memory addresses.

### `historykinetic.graphs`

Correctness references for rolling collision graphs and feature extraction.
Production GPU sketches may approximate these results but must declare bias and
collision probability.

### `historykinetic.solvers`

Protocols and orchestration wrappers for internal backends. No external GPL code.

### `historykinetic.oracles`

External process adapter contracts. Raw upstream output is preserved before any
canonical conversion.

### `historykinetic.indicators`

State-only, history-aware, probe-aware, and learned indicators. Every indicator
publishes its feature-visibility requirements.

### `historykinetic.conversions`

Representation conversion requests and audited results. Conversion is a first-
class event, not a hidden side effect of the partition controller.

### `historykinetic.partition`

Hysteresis, cooldown, buffers, budgets, and representation decisions. It owns
policy, not numerical conversion details.

### `historykinetic.metrics`

Pure evaluation functions over canonical artifacts.

### `historykinetic.rendering`

Renderer protocol and artifact-to-render adapters. No physics callbacks.

## Native modules

The target native structure is:

```text
native/
├── exact/
│   ├── event_queue
│   ├── broad_phase
│   ├── hard_sphere_collision
│   └── boundary_events
├── kinetic/
│   ├── transport
│   ├── dsmc_collision
│   ├── enskog_collision
│   └── moments
├── history/
│   ├── exact_window
│   ├── pair_sketch
│   ├── component_sketch
│   └── lineage_sketch
├── conversion/
│   ├── demotion
│   ├── promotion
│   ├── moment_correction
│   └── exclusion_placement
├── partition/
│   ├── block_state
│   ├── interface_buffer
│   └── controller_runtime
└── io/
    ├── artifact_writer
    └── checkpoint
```

Only `history_window` and the stable solver interface exist at bootstrap.

## Prohibited coupling

- renderer importing solver-private device memory;
- indicator mutating state;
- converter deciding policy;
- metrics changing output data;
- adapter normalizing units without recording the transform;
- paper scripts parsing proprietary log text when a canonical artifact exists;
- benchmark files containing implementation-specific hard-coded paths.
