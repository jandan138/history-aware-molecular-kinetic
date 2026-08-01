# configs

Reusable presets and schema-valid configurations.

- `examples/`: benchmark case examples;
- `render/`: renderer-only intent for diagnostic, shared-comparison, and Hero output.
- `studies/`: immutable scientific/story recipes for E1, E2, the addressable
  collision E3 Hero, and the E4 causal-steering Hero.

Render configs must never contain solver parameters or alter physics/partition state.
They validate against `schemas/render-config.schema.json`.
