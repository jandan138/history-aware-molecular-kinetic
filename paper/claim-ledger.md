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
| C10 | Exact EDMD reversal and deterministic replay are trustworthy in the declared cases | E0 | return error, event/checksum agreement, invariants, grazing/tie cases | active; not yet frozen |
| C11 | Exact-reverse and chaotized branches can match a preregistered resolved `f1_h` while producing distinct futures | E1 | multi-resolution pivot audit, seed uncertainty, branch trajectories | proposed; must not claim continuous-`f1` or exact-state equality |
| C12 | DSMC/chaotization lose an observable response carried by hidden multi-particle collision correlation | E1/E2 | exact/chaotized/DSMC/ghost comparison, incoming-pair diagnostic | proposed |
| C13 | A structured `(Lambda,Gamma)` collision-molecule budget explains response beyond collision count | E2 | budget paths, count/time-matched random suppression, topology-shuffled control | proposed; extended dynamics is not exact EDMD |
| C14 | The incoming-pair closure-defect proxy tracks the missing correlated response | E2 | preregistered bins/observables, branch derivatives, uncertainty | proposed |
| C15 | A small fixed-`N epsilon` sequence has an interpretable finite-system budget trend | E2 | scale sequence and fixed observable tolerance | optional; not a kinetic-limit theorem |

## C. Active SIG graphics/system claims

| ID | Candidate claim | Benchmark | Required evidence | Status |
|---|---|---|---|---|
| C16 | A timestamped collision causal multigraph supports correct event ancestry, molecule, and descendant queries | E3 | graph reconstruction, repeated-event tests, query audit | proposed |
| C17 | Checkpoints plus event history support deterministic random access and persistent branch replay | E3 | replay checksums, latency/storage, copy-on-write vs full-copy | proposed |
| C18 | Expanding causal-cone recomputation matches complete resimulation after past edits | E4 | particle/collision/geometry edits, local-vs-full state/event error, fallback audit | proposed |
| C19 | At least two edit families retain useful causal locality and branch reuse | E4 | affected fraction, runtime, storage, edit-age/density sweeps | proposed; must report global-cone failures |
| C20 | Resolved-state-preserving correlation surgery enables repeatable alternate-future authoring | E5 | multi-resolution `f1_h` audit, invariants, random-surgery baseline, controllability | proposed |
| C21 | The system provides a novel animation workflow beyond reverse playback, keyframing, and generic rollback | E6 | interaction study/case tasks, three Hero Scenes, prior-art comparisons | proposed |
| C22 | The final visual evidence is physically recomputed, fair, and reproducible | E6 | branch/run/metric/render manifests, comparison lock, failure reel | proposed |

## D. Claim dependency graph

```text
C10 → C11 → C12/C13/C14
C10 → C16 → C17 → C18 → C19
C11/C13 + C17 → C20
C18/C19/C20 → C21 → C22
```

A failure of C13 removes the molecule-topology mechanism but does not automatically
invalidate C16–C19. A failure of C19 removes the local-speed claim but may leave
branch provenance and C20 authoring. A failure of C10 or C11 blocks the active paper
spine.

## E. Hero-scene ownership

| Claim family | Primary scene |
|---|---|
| C10–C15 | Molecular Logo Echo |
| C16–C19 | One Collision, Two Worlds |
| C18–C21 | Edit the Past |
| C20 | Logo Echo or optional same-present surgery shot |
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
