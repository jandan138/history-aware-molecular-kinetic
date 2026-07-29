# Milestones

## M0 — Repository and evidence architecture

**Status:** initialized.

Deliverables:

- research thesis and claim boundaries;
- source/license ledger;
- R0–B5 benchmark specifications;
- artifact schemas;
- Python/native semantic contracts;
- CI, docs, and reproducibility rules.

Exit:

- repository checks and tests pass;
- no third-party source is vendored;
- every major claim has a benchmark path.

---

## M1 — R0 external reference reproduction

Deliverables:

- DynamO adapter and equilibrium/dilute cases;
- SPARTA free/collisional/simple-surface cases;
- uniGasFoam pure/hybrid case;
- raw-to-canonical converters;
- revision and license audit;
- first shared diagnostic renders.

Exit:

- one documented result reproduced per source;
- unit/normalization audit complete;
- stochastic variation measured;
- raw output immutable and hashed.

---

## M2 — B0 exact and kinetic primitives

Deliverables:

- minimal 2D exact hard-disk EDMD;
- minimal 2D Boltzmann DSMC;
- analytic collision and transport tests;
- invariants and resolution studies;
- rolling collision-history correctness reference;
- initial Enskog reference plan.

Exit:

- EDMD event integrity passes;
- DSMC convergence envelope established;
- both match selected external references;
- no hidden renderer dependency.

---

## M3 — B1 discrepancy atlas

Deliverables:

- paired ensemble generator;
- canonical scene families;
- state and history extraction;
- exact/kinetic observable joins;
- grouped split manifest;
- Boltzmann versus Enskog attribution cases;
- discrepancy dashboard.

Exit:

- nontrivial target variation;
- stable uncertainty;
- matched definitions and convergence;
- no random-row leakage;
- at least one case discriminates explanations.

---

## M4 — B2 indicator study

Deliverables:

- strong state-only baselines;
- exact-history oracle model;
- sparse probe prototype;
- grouped/OOD evaluation;
- incremental-value and ablation report;
- online observability audit.

Exit:

- practical feature set improves an operational metric enough to change a
  partition policy;
- gain survives geometry/regime holdouts;
- Enskog/packing explanations controlled;
- no oracle-only feature leakage.

Decision:

- pass: continue to conversion and dynamic LOD;
- fail due finite density: pivot to EDMD–Enskog;
- fail due observability: study probes/error estimation;
- fail completely: stop the LOD claim.

---

## M5 — B3 static conversion

Deliverables:

- exact-to-kinetic demotion;
- conservative correction;
- secondary-statistics audit;
- promotion with exclusion placement;
- warm-up/history maturity;
- static interface flux test;
- conversion renderer diagnostics.

Exit:

- primary conservation passes;
- secondary errors are subordinate;
- overlap-free promotion succeeds in target range;
- interface bias converges;
- conversion failures are recoverable.

---

## M6 — B4 dynamic LOD

Deliverables:

- block state machine;
- hysteresis and cooldown;
- probe scheduler;
- exact-region budget;
- moving partitions and interfaces;
- state-only, oracle upper-bound, and practical policies;
- cost-quality sweeps.

Exit:

- practical policy improves a Pareto frontier;
- exact fraction occupies a useful intermediate regime;
- no uncontrolled chatter;
- failure indicators work;
- at least two physical effects restored.

---

## M7 — B5 paper evidence and hero scenes

Deliverables:

- strongest baselines and ablations;
- full resolution/sampling studies;
- three shared-renderer hero scenes;
- evidence freeze;
- figures, tables, and supplementary failures;
- artifact packaging;
- venue decision.

Exit:

- claim ledger fully linked;
- all primary results reproducible;
- no unresolved model/license boundary;
- graphics and scientific claims agree.
