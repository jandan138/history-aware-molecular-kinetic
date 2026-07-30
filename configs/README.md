# configs

Reusable presets and schema-valid configurations.

- `examples/`: benchmark case examples;
- `render/`: renderer-only intent for diagnostic, shared-comparison, and Hero output.

Render configs must never contain solver parameters or alter physics/partition state.
They validate against `schemas/render-config.schema.json`.
