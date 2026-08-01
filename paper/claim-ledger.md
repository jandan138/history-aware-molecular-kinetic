# Claim Ledger

No abstract, introduction, caption, or video sentence may be stronger than the
corresponding row. Failed and deferred claims remain visible.

## A. Archived/deferred adaptive-LOD claims

| ID | Candidate claim | Required evidence | Status |
|---|---|---|---|
| C0 | External reference adapters reproduce documented behavior | raw hashes, normalization audit, scalar reproduction | planned infrastructure |
| C1 | Internal EDMD and kinetic primitives are trustworthy in declared regimes | analytic tests, convergence, invariants, external comparison | internal 2D checks pass; external comparison pending |
| C2 | Exact-versus-kinetic discrepancy has stable, attributable structure | discrepancy atlas, uncertainty, Boltzmann/Enskog attribution | planned/deferred |
| C3 | Scalar collision-history features add predictive value beyond state/geometry controls | grouped held-out delta, CI, ablations, leakage audit | **closed exploratory negative** in `PHASE1-HISTORY-STORY-v0`; relative MAE `-0.83%`, 95% CI `[-2.21%,0.52%]` |
| C4 | A practical probe/observable policy retains useful predictive history value | oracle upper bound vs practical policy, probe cost | deferred with predictor route |
| C5 | Exact→kinetic demotion preserves primary invariants and bounded statistics | conversion reports and downstream transients | deferred |
| C6 | Kinetic→exact promotion avoids invalid overlap and unacceptable transients | placement/warm-up studies | deferred |
| C7 | Dynamic exact/kinetic policy improves a cost-quality Pareto frontier | uniform/state-only/oracle policy sweeps | blocked/deferred after C3 |
| C8 | Dynamic LOD restores visible physical effects | old B5 shared-renderer evidence | deferred |
| C9 | Dynamic LOD supports camera-independent zoomable molecular visualization | old B5 camera/physics audit | deferred |

The old route may be reopened only through a new ADR and new evidence. It must not be
implicitly revived in the Molecular Echoes paper.

## B. Active scientific echo claims

| ID | Candidate claim | Benchmark | Required evidence | Status |
|---|---|---|---|---|
| C10 | Exact EDMD reversal and deterministic replay are trustworthy in the declared cases | E0 | return error, event/checksum agreement, invariants, grazing/tie cases | E1 declared cases pass: event-pair agreement 1.0, max position RMS 2.77e-6, max velocity RMS 4.92e-5; broader E0 replay/edge-case gate remains |
| C11 | Exact-reverse and chaotized branches can match a preregistered resolved `f1_h` while producing distinct futures | E1 | multi-resolution pivot audit, seed uncertainty, branch trajectories | **passes for E1-v0's 4×2 resolved state** across 12 cases; mean gap 0.449784, 95% interval [0.436573, 0.460660]; 8×4 mismatch disclosed, so no continuous-`f1` or exact-state claim |
| C12 | DSMC/chaotization lose an observable response carried by hidden multi-particle collision correlation | E1/E2 | exact/chaotized/DSMC/ghost comparison, incoming-pair diagnostic | E1 phenomenon passes; E2 shows a graded collision-budget response but does not identify molecule wiring beyond collision dose |
| C13 | A structured `(Lambda,Gamma)` collision-molecule budget explains response beyond collision count | E2 | budget paths, count/time-matched random suppression, topology-shuffled control | **closed negative in E2-v0**: selected-minus-random mean `-0.007636`, 95% CI `[-0.032264,0.016086]`; selected-minus-topology mean `-0.009639`, CI `[-0.049062,0.029519]` |
| C14 | The incoming-pair closure-defect proxy tracks the missing correlated response | E2 | preregistered bins/observables, branch derivatives, uncertainty | **not supported in E2-v0**: proxy does not discriminate the structured branch from registered controls and cannot rescue C13 |
| C15 | A small fixed-`N epsilon` sequence has an interpretable finite-system budget trend | E2 | scale sequence and fixed observable tolerance | cancelled after the E2 mechanism gate failed; not a kinetic-limit theorem |

## C. Active SIG graphics/system claims

| ID | Candidate claim | Benchmark | Required evidence | Status |
|---|---|---|---|---|
| C16 | An addressable collision timeline supports event ancestry, descendant queries, checkpoints, and state hashes | E3 | raw-event reconstruction, stable IDs, graph queries, checkpoint hashes | **passes E3-v0 Hero**; 107 baseline events, periodic/forced checkpoints, hashed artifacts |
| C17 | The timeline can fork one conservative physical edit with complete branch provenance | E3 | edit/checkpoint/parent manifests, momentum and energy audit | **passes E3-v0 Hero**; `+1°` edit, momentum error `1.11e-15`, energy error `0` |
| C18 | Exact expanding-causal-cone recomputation matches complete resimulation while reusing independent baseline events | E3 | local-vs-full pair/time/state error, reused events, affected fraction | **passes E3-v0 Hero**; pair agreement `1.0`, `79/105` events reused, peak affected `33/128` |
| C19 | A creator can select a terminal feature, trace it to a ranked editable collision, and direct a scoped exact future | E4 | target membership, baseline-only causal ranking, exact preview palette, target/collateral change, one final full reference | **passes E4-v0 Hero**: collision #4, `−1°`, target/collateral `4.0x`, preview median `0.074740 s`, `100/100` exact reference pairs |
| C20 | A sparse velocity-ownership surgery can preserve one declared visible present while directing the selected E middle stroke toward a C-like future | E5 | exact declared-cell multiset/invariant audit, target reduction, collateral retention, matched physical branches | frozen recipe; formal run pending |
| C21 | Editing an addressable past collision provides an animation workflow beyond reverse playback, outcome browsing, and generic rollback | E3/E4/E6 | One Collision Hero, causal-steering interaction, exact branch evidence, Many-Worlds/Storyboard/Time-Warp comparison | E3 exact operation and E4 scoped causal-steering interaction pass; broad user value remains future |
| C22 | The final visual evidence is physically recomputed, fair, and reproducible | E6 | branch/run/metric/render manifests, comparison lock, failure reel | proposed |

## D. Claim dependency graph

```text
C10 → C11 → C12
C10 → C16 → C17 → C18
C18 → C19 → C21
C11 + C17 → C20
C18 → C21 → C22
C19/C20 strengthen C21 but do not block the first Hero gate
```

A failure of C13 removes the molecule-topology mechanism but does not automatically
invalidate C16–C19. A failure of C19 removes the local-speed claim but may leave
branch provenance and C20 authoring. A failure of C10 or C11 blocks the active paper
spine.

## E. Hero-scene ownership

| Claim family | Primary scene |
|---|---|
| C10–C12 | Molecular Logo Echo |
| C13–C15 closed/limitations | E2 limitation panel only |
| C16–C18 | One Collision, Two Worlds |
| C19/C21 | Choose the Cause, Direct the Future |
| C18–C21 geometry extension | deferred after E4 |
| C20 | Same Present, Chosen Future |
| C22 | all three scenes plus evidence release |

Every primary shot follows the active storyboard and must link to branch IDs,
artifacts, metrics, camera hashes, and renderer hashes.

## F. Mandatory wording boundaries

Allowed:

- “same preregistered resolved one-particle present”;
- “inspired by collision-history molecules and cumulants in the Deng–Hani–Ma
  derivation”;
- “local causal-cone recomputation with full-replay fallback”;
- “extended history-budget dynamics.”

Forbidden unless independently proven:

- “same exact state”;
- “we implement Deng's cutting algorithm”;
- “the theorem guarantees our branch method”;
- “first reversible hard-sphere simulation”;
- “the causal cone is always local”;
- “the original dynamic-LOD predictor works.”
