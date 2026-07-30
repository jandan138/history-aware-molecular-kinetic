# Milestones

The scientific and visual-production tracks advance together, but visual polish is
strictly gated by scientific evidence.

```text
Scientific: M0 → M1 → M2 → M3 → M4 → M5 → M6 → M7
Visual:         V0 ───────→ V1 ─────→ V2 → V3 → V4 → V5
```

See [Visual Production Roadmap](../demos/visual-production-roadmap.md).

---

## M0 — Repository and evidence architecture

**Status:** initialized.

Deliverables:

- research thesis and claim boundaries;
- source/license ledger;
- R0–B5 benchmark specifications;
- artifact schemas;
- Python/native semantic contracts;
- CI, docs, and reproducibility rules;
- render-config/render-manifest contracts;
- initial visual-production plan and scene responsibilities.

Exit:

- repository checks and tests pass;
- no third-party source is vendored;
- every major claim has a benchmark path;
- every B5 claim has a declared scene and visual observable.

---

## M1 — R0 external reference reproduction

Deliverables:

- DynamO adapter and equilibrium/dilute cases;
- SPARTA free/collisional/simple-surface cases;
- uniGasFoam pure/hybrid case;
- raw-to-canonical converters;
- revision and license audit;
- first shared diagnostic renders;
- **V0:** canonical artifact replay for particles, fields, geometry, and masks.

Exit:

- one documented result reproduced per source;
- unit/normalization audit complete;
- stochastic variation measured;
- raw output immutable and hashed;
- V0 can replay at least one case from each external source without solver access.

---

## M2 — B0 exact and kinetic primitives

Deliverables:

- minimal 2D exact hard-disk EDMD;
- minimal 2D Boltzmann DSMC;
- analytic collision and transport tests;
- invariants and resolution studies;
- rolling collision-history correctness reference;
- initial Enskog reference plan;
- particle/field/collision diagnostic layers in V0.

Exit:

- EDMD event integrity passes;
- DSMC convergence envelope established;
- both match selected external references;
- no hidden renderer dependency;
- diagnostic views expose numerical failures rather than smoothing them away.

---

## M3 — B1 discrepancy atlas

Deliverables:

- paired ensemble generator;
- canonical scene families;
- state and history extraction;
- exact/kinetic observable joins;
- grouped split manifest;
- Boltzmann versus Enskog attribution cases;
- discrepancy dashboard;
- **V1:** shared scientific renderer, reference-difference view, comparison lock.

Exit:

- nontrivial target variation;
- stable uncertainty;
- matched definitions and convergence;
- no random-row leakage;
- at least one case discriminates explanations;
- full exact/kinetic comparison can be reproduced from manifest and hashes.

---

## M4 — B2 indicator study

Deliverables:

- strong state-only baselines;
- exact-history oracle model;
- sparse probe prototype;
- grouped/OOD evaluation;
- incremental-value and ablation report;
- online observability audit;
- Correlation Labyrinth matched-state diagnostic prototype.

Exit:

- practical feature set improves an operational metric enough to change a
  partition policy;
- gain survives geometry/regime holdouts;
- Enskog/packing explanations controlled;
- no oracle-only feature leakage;
- CL-02/03/04 can visually link matched state, history difference, and future
  physical discrepancy.

Decision:

- pass: continue to conversion and dynamic LOD;
- fail due finite density: pivot to EDMD–Enskog;
- fail due observability: study probes/error estimation;
- fail completely: stop the LOD claim and do not hero-polish the Labyrinth.

---

## M5 — B3 static conversion

Deliverables:

- exact-to-kinetic demotion;
- conservative correction;
- secondary-statistics audit;
- promotion with exclusion placement;
- warm-up/history maturity;
- static interface flux test;
- conversion renderer diagnostics;
- **V2:** zoom/conversion prototype with persistent display sampling and
  camera–physics audit.

Exit:

- primary conservation passes;
- secondary errors are subordinate;
- overlap-free promotion succeeds in target range;
- interface bias converges;
- conversion failures are recoverable;
- `B5-ZOOM-MIX-v0` passes neutral visual continuity criteria before hero styling.

---

## M6 — B4 dynamic LOD

Deliverables:

- block state machine;
- hysteresis and cooldown;
- probe scheduler;
- exact-region budget;
- moving partitions and interfaces;
- state-only, oracle upper-bound, and practical policies;
- cost-quality sweeps;
- **V3:** Expansion-into-Vacuum neutral flagship prototype and synchronized
  Pareto visualization.

Exit:

- practical policy improves a Pareto frontier;
- exact fraction occupies a useful intermediate regime;
- no uncontrolled chatter;
- failure indicators work;
- at least two physical effects restored;
- proposed/reference difference is visible in neutral shared rendering without
  relying on the partition mask.

---

## M7 — B5 paper evidence and hero scenes

Deliverables:

- strongest baselines and ablations;
- full resolution/sampling studies;
- **V4:** three shared-renderer hero scenes;
- **V5:** evidence registry, frame recipes, release package, and reproduction audit;
- 30–45 second teaser and 3–5 minute result video;
- evidence freeze;
- figures, tables, and supplementary failures;
- per-shot provenance and frame recipes;
- artifact packaging;
- venue decision.

Exit:

- claim ledger fully linked;
- all primary results reproducible;
- no unresolved model/license boundary;
- graphics and scientific claims agree;
- comparison locks, artifact hashes, camera hashes, and renderer hashes are
  complete;
- failure reel is included;
- no new physics is introduced for the first time in B5.

---

## Parallel-track rules

Can proceed early:

- V0 artifact replay;
- render schemas and manifests;
- neutral diagnostic layers;
- primitive scene geometry;
- camera/physics separation tests.

Blocked until gates:

- conversion zoom shot: G4;
- flagship dynamic scene: G5;
- Correlation Labyrinth hero polish: G3;
- final art direction and teaser: G6;
- complex optional assets: after evidence freeze only.
