# Molecular Echoes Implementation Backlog

This backlog is ordered by evidence dependency. IDs are suitable for GitHub Issues.
No 3D art task is allowed to outrun the scientific and branch-correctness gates.

## Track S — Scientific Echo

### ECHO-S-001 — Preregister E1/E2 protocol

Freeze before primary runs:

- periodic geometry and units;
- `N`, diameter, density, pivot time, observation window;
- initial anisotropy and passive-color pattern;
- spatial blocks and velocity bins;
- multi-resolution `f1_h` audit grid;
- branch definitions;
- observables and uncertainty;
- `(Lambda, Gamma)` budgets;
- null controls;
- success/stop criteria.

**Depends on:** none.

### ECHO-S-002 — Strict reversible EDMD audit

Implement forward/reverse tests with deterministic event ordering, checksums,
grazing cases, and near-simultaneous event cases.

**Depends on:** ECHO-S-001.

### ECHO-S-003 — Pivot and branch constructor

Create forward, exact-reverse, chaotized-reverse, DSMC, and ghost branches from one
registered pivot.

**Depends on:** ECHO-S-002.

### ECHO-S-004 — Multi-resolution resolved-state audit

Report discrete distribution and moment mismatch across all preregistered spatial
and velocity resolutions.

**Depends on:** ECHO-S-003.

### ECHO-S-005 — Collision-molecule event annotations

Extend the event log with molecule root, size, recollision/reconnection rank,
predecessors, incoming normal velocity, and event multiplicity.

**Depends on:** ECHO-S-002.

### ECHO-S-006 — History-budget dynamics

Implement full EDMD and the registered `(Lambda, Gamma)` extended-dynamics paths
with explicit ghost semantics.

**Depends on:** ECHO-S-005.

### ECHO-S-007 — Mechanism null controls

Implement collision-count/time-matched random suppression and topology-shuffled
partner controls.

**Depends on:** ECHO-S-006.

### ECHO-S-008 — Incoming-pair closure readout

Implement preregistered low-dimensional proxies for anisotropy and passive-color
transport.

**Depends on:** ECHO-S-003, ECHO-S-005.

### ECHO-S-009 — Scale and fixed-`N epsilon` study

Run `N=128,256,512` first; only after the mechanism passes, add a small fixed-
`N epsilon` sequence.

**Depends on:** ECHO-S-004, ECHO-S-007, ECHO-S-008.

## Track G — Graphics Time Machine

### ECHO-G-001 — Collision causal multigraph

Build event-predecessor/successor indices, repeated-pair support, shared-ancestor
queries, and causal descendant traversal.

**Depends on:** ECHO-S-005.

### ECHO-G-002 — Checkpoint and deterministic replay

Create checkpoint policy, random-access restore, event replay audit, and divergence
reports.

**Depends on:** ECHO-S-002, ECHO-G-001.

### ECHO-G-003 — Persistent branch store

Implement branch lineage, copy-on-write checkpoint/event references, edit manifests,
and immutable parent branches.

**Depends on:** ECHO-G-002.

### ECHO-G-004 — One-particle counterfactual edit

Perturb a particle before one event, generate a branch, and compare with a complete
resimulation.

**Depends on:** ECHO-G-003.

### ECHO-G-005 — Causal-cone recomputation

Implement exact expanding-cone invalidation/recomputation with conservative fallback
to full replay.

**Depends on:** ECHO-G-004.

### ECHO-G-006 — Geometry edit branching

Support simple obstacle insertion/removal/motion and aperture opening at a past time.

**Depends on:** ECHO-G-005.

### ECHO-G-007 — Correlation-surgery authoring API

Expose constrained velocity assignment/history-retention operations together with
resolved-state audits.

**Depends on:** ECHO-S-004, ECHO-G-003.

### ECHO-G-008 — Branch correctness and locality study

Measure local-vs-full correctness, affected fraction, runtime, memory, fallback rate,
density dependence, and edit-age dependence.

**Depends on:** ECHO-G-005, ECHO-G-006.

## Track V — SIG Visual Production

### ECHO-V-001 — Event/replay diagnostic viewer

Render particles, collision events, branch lineage, causal cone, and pivot audits.

**Depends on:** ECHO-G-002.

### ECHO-V-002 — Molecular Logo Echo prototype

Create a bounded 2D/3D passive-color pattern, mix it, then compare exact,
chaotized, DSMC, and history-budget branches.

**Depends on:** ECHO-S-004, ECHO-S-007.

### ECHO-V-003 — One Collision, Two Worlds prototype

Display one selected event, two recomputed futures, and the spreading causal cone.

**Depends on:** ECHO-G-005.

### ECHO-V-004 — Edit the Past prototype

Create a simple transparent molecular maze and past geometry edits with local/full
comparison.

**Depends on:** ECHO-G-006, ECHO-G-008.

### ECHO-V-005 — Shared scientific renderer lock

Freeze camera, time, particle display, trails, branch colors, graph overlays, and
comparison manifests.

**Depends on:** ECHO-V-001.

### ECHO-V-006 — 3D production pass

Add high-quality instancing, transparent analytic geometry, motion cues, lighting,
and bounded compositing only after neutral evidence passes.

**Depends on:** ECHO-V-002, ECHO-V-003, ECHO-V-004, ECHO-V-005.

### ECHO-V-007 — Teaser and main video

Produce:

- 30–45 second teaser;
- 3–5 minute technical video;
- neutral comparison reel;
- failure/limitation reel;
- per-shot evidence registry.

**Depends on:** ECHO-V-006.

## Track P — Paper Evidence

### ECHO-P-001 — Related-work and claim-boundary audit

Cover reversible collision simulation, Loschmidt echo, discrete-event rollback,
spacetime/particle control, kinetic correlation errors, and Deng–Hani–Ma.

### ECHO-P-002 — Figure and table registry

Bind every claim to frozen runs, metrics, camera hashes, and failure cases.

### ECHO-P-003 — SIG package decision

Choose Journal/TOG-level, Conference-level, or continue development based on the
venue gate in `docs/vision/venue-strategy.md`.

### ECHO-P-004 — VIS pivot package, only if triggered

Define domain tasks, linked-view system, expert evaluation, and case studies. Do not
reuse the SIG draft unchanged.

## Hard dependency summary

```text
S-001 → S-002 → S-003 → S-004
                 └────→ S-005 → S-006 → S-007
                         └────→ G-001 → G-002 → G-003 → G-004 → G-005 → G-006
S-004 + G-003 → G-007
G-005/G-006 → G-008
S-004/S-007 → V-002
G-005 → V-003
G-006/G-008 → V-004
V-002/V-003/V-004/V-005 → V-006 → V-007
```
