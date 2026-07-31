# Milestones

The active route is Molecular Echoes. Scientific validity and graphics-system value
advance together, while polished rendering remains gated.

```text
Scientific: M0 → M1 → M2 → M3
Graphics:        M1 → M4 → M5 → M6
Production:                     V0 → V1 → V2 → V3
Paper:                                      M7
```

The old dynamic-LOD milestones are archived in Git history and deferred by
[ADR 0009](../decisions/0009-pivot-to-molecular-echoes-sig.md).

---

## M0 — Pivot, preregistration, and evidence contracts

**Status:** active.

Deliverables:

- preserve Phase-I predictor negative result;
- freeze the active Molecular Echoes thesis and claim boundaries;
- preregister E1/E2 geometry, state, bins, observables, controls, and stop criteria;
- define branch, checkpoint, edit, replay, and graph artifact contracts;
- add prior-art boundaries for reversal and generic rollback;
- select SIG as primary target and VIS as a real fallback.

Exit:

- ADR 0009 accepted;
- no old LOD claim remains marked active;
- primary E1/E2 config is committed/tagged before results;
- claim ledger and benchmark suite agree.

---

## M1 — E0 strict exact dynamics and replay

Deliverables:

- periodic 2D EDMD at `N=128,256,512`;
- deterministic event-order policy;
- grazing and near-simultaneous collision tests;
- forward/reverse return audit;
- collision event checksums;
- checkpoints and random-access replay;
- DynamO comparison where definitions align;
- **V0:** event/replay diagnostic viewer.

Exit:

- return error and invariant drift meet preregistered tolerances;
- replay reproduces event/state checksums;
- failure cases are visible, not snapped away;
- checkpoint interval/latency trade-off is measured.

Decision:

If numerical reversal is not trustworthy, stop the echo paper before adding
scientific interpretation or graphics polish.

---

## M2 — E1 same resolved present, opposite futures

Deliverables:

- registered non-equilibrium pivot protocol;
- forward, exact-reverse, chaotized-reverse, DSMC, and ghost branches;
- passive-color pattern;
- spatial/velocity multi-resolution `f1_h` audit;
- anisotropy, color, and branch-divergence metrics;
- seed uncertainty;
- a neutral 30–45 second internal echo clip.

Exit:

- reverse and chaotized branches pass the declared pivot audit;
- future separation survives finer audit resolutions;
- result is stable over seeds and at least two `N` values;
- video difference is caused by simulated dynamics, not backward playback.

Decision:

If separation vanishes under finer `f1_h`, narrow or stop the same-present claim.

---

## M3 — E2 collision-molecule mechanism

Deliverables:

- timestamped event multigraph with repeated events;
- molecule root, size, and recollision/reconnection complexity;
- full and `(Lambda,Gamma)` extended dynamics;
- count/time-matched random suppression;
- topology-shuffled control;
- incoming-pair closure-defect proxy;
- forward/reverse budget curves;
- first small fixed-`N epsilon` study only after finite-system mechanism passes.

Exit:

- structured molecule budget differs from count-matched controls;
- forward and reverse branches respond differently in a preregistered way;
- closure readout has the expected direction and uncertainty;
- extended dynamics are clearly labeled, tested, and not confused with EDMD.

Decision:

If collision count explains the result, remove the molecule-topology claim. The
project may retain a visual echo demo but cannot use Deng-inspired mechanism as the
paper spine.

---

## M4 — E3 collision causal graph and persistent replay

Deliverables:

- predecessor/successor indices;
- shared-ancestor and descendant queries;
- checkpoint store;
- immutable parent branches;
- copy-on-write event/checkpoint sharing;
- edit and branch manifests;
- event graph visualization;
- storage and query benchmarks.

Exit:

- graph reconstruction matches raw event logs;
- repeated-pair events are preserved;
- deterministic replay and branch lineage pass checksum audits;
- full-copy and copy-on-write baselines are compared.

---

## M5 — E4 causal rewind and counterfactual branching

Deliverables:

- one-particle edit;
- one-collision edit under declared semantics;
- simple obstacle/aperture edits;
- expanding causal-cone invalidation/recomputation;
- conservative fallback to full replay;
- local-vs-full correctness study;
- affected fraction, latency, storage, edit-age, and density sweeps;
- **V1:** One Collision, Two Worlds prototype.

Exit:

- exact local branches match complete resimulation within tolerance;
- approximate variants are labeled separately;
- at least two edit families retain useful locality for a nontrivial time window;
- fallback behavior is correct and reported;
- the interaction is more than a replayed movie.

Decision:

If all cones immediately become global, remove the local-speed claim and assess
whether branch provenance and correlation surgery still form a sufficient graphics
contribution.

---

## M6 — E5 correlation surgery and authoring

Deliverables:

- block+color velocity surgery;
- constrained moment-matching refinement;
- multi-resolution resolved-state audit;
- primary invariant and no-overlap audit;
- partial history/molecule retention controls;
- repeatable alternate-future authoring;
- **V2:** Molecular Logo Echo prototype;
- **V3:** Edit the Past prototype.

Exit:

- current resolved state stays within registered tolerance;
- future branches are controllably different;
- the effect survives matched rendering;
- interaction and visual language are understandable without exposing every debug
  statistic;
- random surgery of equal magnitude is a weaker control.

---

## M7 — E6 SIG paper evidence and production

Deliverables:

- strongest prior-art baselines and ablations;
- numerical/scaling studies;
- full-resimulation correctness;
- runtime/storage/interactivity results;
- three 3D Hero Scenes;
- 30–45 second teaser;
- 3–5 minute technical video;
- failure/limitation reel;
- evidence registry and per-shot manifests;
- artifact packaging;
- SIG Journal/Conference-level package decision;
- VIS pivot decision only if triggered.

Exit:

- every active claim maps to frozen evidence;
- no old LOD claim is silently revived;
- neutral and hero rendering agree;
- no primary visual relies on backward video as a simulation result;
- local branch claims are validated against full resimulation;
- the Deng connection is accurate and bounded;
- SIG graphics contribution is legible without the scientific appendix.

---

## Visual production gates

### V0 — Scientific event viewer

Particles, event ledger, checkpoints, pivot audit, branch timeline.

### V1 — Branch comparison renderer

Original/counterfactual/full-reference views with shared camera and time.

### V2 — Molecular Logo Echo

Exact/chaotized/DSMC/history-budget branches; neutral first, hero polish later.

### V3 — Final three-scene production

Molecular Logo Echo, One Collision Two Worlds, Edit the Past, plus evidence release.

---

## Parallel-track rules

Can proceed early:

- primitive particle/event viewer;
- graph layout experiments;
- checkpoint serialization;
- passive-color pattern design;
- simple analytic geometry assets;
- render/evidence schemas.

Blocked until gates:

- polished echo teaser: M2;
- molecule-budget narrative: M3;
- local-edit performance claim: M5;
- history-surgery authoring claim: M6;
- full 3D production: M5/M6 neutral evidence;
- IEEE VIS interface/user study: only after formal venue pivot.
