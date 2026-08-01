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

**Status:** E1 and E2 protocols are frozen and executed; E2's mechanism claim is
closed negative.

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

**Status:** the E1 declared reversal cases pass; full E0 replay, external comparison,
and adversarial edge cases remain.

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

**Status:** passed on 2026-07-31 for the preregistered 4×2 resolved-state claim.
The 8×4 mismatch is an explicit limitation. E2 subsequently failed its stronger
mechanism controls without invalidating this scoped phenomenon.

Deliverables:

- registered non-equilibrium pivot protocol;
- forward, exact-reverse, chaotized-reverse, DSMC, and ghost branches;
- passive-color pattern;
- spatial/velocity multi-resolution `f1_h` audit;
- anisotropy, color, and branch-divergence metrics;
- seed uncertainty;
- a neutral internal echo clip with a frozen comparison lock.

Exit:

- reverse and chaotized branches pass the declared pivot audit;
- future separation survives finer audit resolutions;
- result is stable over seeds and at least two `N` values;
- video difference is caused by simulated dynamics, not backward playback.

Decision:

If separation vanishes under finer `f1_h`, narrow or stop the same-present claim.

---

## M3 — E2 collision-molecule mechanism

**Status:** complete with `stop_e2` on 2026-08-01. The reverse budget ladder passes,
but `(4,0)` does not beat count/time-matched random or topology-shuffled controls.
The molecule-topology claim and optional scale study are closed.

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

## M4 — E3 addressable collision and exact causal branch

**Status:** complete with `go` on 2026-08-01. The one-collision Hero combines graph,
checkpoint, edit, reuse, and local/full correctness in one gate.

Deliverables:

- predecessor/successor indices;
- shared-ancestor and descendant queries;
- checkpoint store;
- immutable parent timeline and fork checkpoint;
- baseline-event reuse with an expanding affected set;
- edit and branch manifests;
- event graph visualization;
- locked One Collision, Two Worlds figure/video.

Exit:

- graph reconstruction matches raw event logs;
- repeated-pair events are preserved;
- branch lineage and edit invariants pass;
- local branch matches complete resimulation;
- visible split, event reuse, and causal reach pass the frozen Hero thresholds.

Result: `106/106` event-pair agreement, `79/105` baseline events reused, peak
affected set `33/128`, terminal color gap `0.188218`. See the
[E3 result](../benchmarks/molecular-time-machine-e3-result.md).

---

## M5 — E4 causal steering interaction

**Status:** complete with `go` on 2026-08-01. The registered target-to-cause Hero
selects the upper E stroke, ranks collision #4 from baseline ancestry, and saves a
`−1°` branch with `4.0x` target-to-collateral change, `79/103` event reuse, and
`100/100` local/full collision-pair agreement. See the
[E4 result](../benchmarks/molecular-time-machine-e4-result.md).

Deliverables:

- terminal feature selection with persistent particle membership;
- baseline-only causal ranking from descendant coverage and purity;
- a compact cached exact-preview branch palette;
- one selected branch/full-resimulation comparison;
- target-versus-collateral outcome readout;
- a self-contained creator-facing interaction artifact;
- **V1:** Choose the Cause, Direct the Future interaction.

Exit:

- the E3 exact semantics remain unchanged;
- ranking sees baseline ancestry, not edited outcomes;
- exact previews are physical branches, not renderer changes;
- the selected target changes more than collateral foreground;
- the one saved branch matches full resimulation;
- the interaction is more than a replayed movie.

Decision:

If the exact interaction works but selectivity does not, call it causal exploration
rather than causal steering. Do not add a breadth grid to rescue the Hero.

---

## M6 — E5 correlation surgery and authoring

**Status:** complete with `go` on 2026-08-01. The registered Hero touches four of
256 particles, reduces middle-stroke occupancy from 8 to 2, and retains all 19
collateral foreground particles. See the
[E5 result](../benchmarks/molecular-time-machine-e5-result.md).

Deliverables:

- selected future middle-stroke target with persistent particle membership;
- one common `N=256`, seed-4 pivot at `t=0.80`;
- one/two legal same-cell target-only velocity transpositions;
- 30 cached complete-EDMD previews and a deterministic sparse selection rule;
- exact visible-state, declared-cell multiset, invariant, and geometry contract;
- matched E-versus-C future evidence;
- **V5:** Same Present, Chosen Future figure, video, and browser artifact.

Exit:

- the declared current frame and `4×2` velocity multisets are preserved;
- middle-stroke occupancy falls by at least 70%;
- at least 90% of non-target glyph membership remains;
- at most four particles are touched;
- all candidate and selected futures are complete EDMD runs under matched rendering.

No seed grid, random-surgery baseline, alternate edit family, geometry scene, or
user study is part of this gate.

---

## M7 — E6 SIG paper evidence and production

**Status:** E6-v0 integration implementation passes under
[ADR 0013](../decisions/0013-e6-sig-hero-integration.md). The shared bundles,
Three.js companion, Genesis neutral check, Cycles/CUDA source animation, and exact
45-second preview master are complete. Native-Windows 4K/EXR delivery and the
3–5-minute technical cut remain production exports, not new experiments.

Deliverables:

- a versioned renderer-neutral E6 shot bundle built from frozen E1/E3/E4/E5 artifacts;
- one Black Obsidian Time Laboratory visual language;
- a 4K Same Present, Chosen Future signature Hero;
- a real-time 3D companion for Reveal, Trace & Branch, and Author;
- locked 3D paper figures backed by the same evidence bundle;
- 30–45 second teaser;
- 3–5 minute technical video;
- evidence registry and per-shot manifests;
- source and asset license ledger;
- provisional SIGGRAPH 2027 Conference paper spine.

Exit:

- every active claim maps to frozen evidence;
- no old LOD claim is silently revived;
- neutral and hero rendering agree;
- no primary visual relies on backward video as a simulation result;
- the E3/E4 local/full evidence remains linked rather than rerun as a new grid;
- SIG graphics contribution is legible without the scientific appendix.

No seed or density sweep, new baseline, random-surgery control, second edit family,
geometry edit, user study, failure reel, or 3D physics rewrite belongs to this
milestone.

---

## Visual production gates

### V0 — Scientific event viewer

Particles, event ledger, checkpoints, pivot audit, branch timeline.

### V1 — Branch comparison renderer

Original/counterfactual/full-reference views with shared camera and time.

### V2 — Molecular Logo Echo

Exact/chaotized/DSMC/history-budget branches; neutral first, hero polish later.

### V3 — Final integrated production

Same Present, Chosen Future is the signature Hero. Molecular Logo Echo and causal
branching appear as supporting acts in the technical video and companion.

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
