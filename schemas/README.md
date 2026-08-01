# Scientific artifact schemas

This directory contains versioned JSON Schema Draft 2020-12 contracts. Solvers,
adapters, metrics, renderers, and paper scripts exchange artifacts through these
contracts rather than through backend-specific in-memory structures.

| Schema | Purpose |
|---|---|
| `benchmark-case.schema.json` | Immutable benchmark inputs, declared observables, and acceptance metadata |
| `run-manifest.schema.json` | Code, environment, configuration, seed, hardware, and artifact provenance |
| `collision-event.schema.json` | Exact hard-sphere binary collision log records |
| `block-state.schema.json` | Runtime-observable local moments and discretization metadata |
| `history-feature.schema.json` | Exact/probe history features with observability labels |
| `discrepancy-sample.schema.json` | Paired exact–kinetic targets and grouped-split metadata |
| `partition-mask.schema.json` | Representation ownership and refinement decisions over blocks |
| `conversion-report.schema.json` | Exact↔kinetic conversion budgets and secondary-statistic diagnostics |
| `particle-bundle.schema.json` | Canonical exact-particle artifact metadata |
| `kinetic-bundle.schema.json` | Canonical weighted kinetic-particle/cell artifact metadata |
| `geometry-bundle.schema.json` | Canonical domain and boundary geometry metadata |
| `metrics-report.schema.json` | Metric values, uncertainty, applicability, and evidence provenance |
| `source-lock.schema.json` | Pinned external source identity, revision, license, and integration boundary |
| `camera-path.schema.json` | Versioned keyframed camera paths used by locked scientific and Hero shots |
| `render-config.schema.json` | Renderer mode, camera, layers, comparison locks, temporal policy, and outputs |
| `render-manifest.schema.json` | Shot plus optional case/run/claim linkage, input hashes, renderer provenance, comparison locks, frames, and outputs |
| `e6-shot-bundle.schema.json` | Frozen renderer-neutral E6 trajectories, roles, events, metrics, coordinate map, and source hashes |

## Rules

- Breaking semantic changes require a new schema version.
- Array payloads live in separately hashed files; JSON documents describe their
  semantics, shapes, units, axes, and provenance.
- Paths are relative to a run or artifact root.
- A field is never silently repurposed. Add a new field or schema version.
- Candidate benchmark cases must validate before review; frozen cases are
  immutable and content-addressed.
- External source locks must agree with `references/sources.yaml`.
- Planning or diagnostic renders may have incomplete evidence links. A frozen
  B5 primary render must set `evidence_links.complete=true`, which requires a
  benchmark case, run IDs, claim IDs, shot IDs, and at least one metrics artifact.
