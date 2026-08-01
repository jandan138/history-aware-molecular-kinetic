# Research Hypotheses

## H0 — Archived predictor hypothesis

Compact collision-history scalar features improve held-out prediction of
exact-versus-kinetic discrepancy after controlling for state, geometry, resolution,
and finite-density effects.

**Outcome:** exploratory negative in `PHASE1-HISTORY-STORY-v0`.

The adaptive-LOD dependency chain is deferred. This outcome does not imply that all
collision history is information-free; it closes the tested predictor realization.

Record: [Phase-I paper spine](../roadmap/phase-1-paper-spine.md).

---

## Active scientific hypotheses

## H1 — Numerical reversal and replay

The registered periodic EDMD system can be advanced, velocity-reversed, and replayed
from checkpoints with bounded state/event error under a deterministic ordering
policy.

**Falsifier:** return/replay error exceeds preregistered tolerance or depends on
manual trajectory repair.

## H2 — Same resolved present, different correlated future

Exact-reverse and resolved-state-preserving chaotized branches can match a
preregistered finite-resolution `f1_h` over a reported resolution sweep while
separating in fixed-horizon anisotropy or passive-color observables.

**Falsifier:** the pivot audit fails, the separation disappears at finer resolution,
or the effect is seed/cherry-pick specific.

## H3 — DSMC/chaotization remove a history-carried response

A DSMC branch and a pair-chaotized exact branch lose a future response recovered by
the exact-reverse branch, consistent with missing multi-particle pairing rather than
a visible one-particle pivot difference.

**Falsifier:** the branches are distinguishable at the pivot or their future response
is statistically equivalent to exact reverse.

## H4 — Collision-molecule budget is a mechanism

A structured `(Lambda,Gamma)` history budget affects forward relaxation and reverse
echo differently and predicts branch recovery beyond collision-count/time-matched
random suppression.

**Falsifier:** collision count, mean free time, or random suppression explains the
same response.

## H5 — Incoming-pair closure defect tracks the response

A preregistered incoming-pair correlation proxy has a stable directional relation to
the derivative and budget dependence of the chosen future observable.

**Falsifier:** the relationship exists only after post-hoc binning/observable choice
or is unstable across seeds and scales.

## H6 — Finite-system history requirement has an interpretable scale trend

After H2–H5 pass, the required history budget for a fixed observable tolerance shows
a reportable trend over `N` and a small fixed-`N epsilon` sequence.

**Falsifier:** no stable trend or the finite-system mechanism disappears. Failure
removes the scale claim but need not invalidate H2/H4.

---

## Active graphics/system hypotheses

## H7 — Collision graph is a correct simulation representation

The timestamped event multigraph reconstructs particle event ancestry, repeated
collisions, shared ancestors, collision molecules, and descendants from the raw
ledger.

**Falsifier:** graph queries disagree with the event log or cannot drive deterministic
replay.

## H8 — Persistent replay shares history correctly

Checkpoint/event segments can be shared across immutable branches and reproduce the
full-copy branch while using less storage or lower random-access latency.

**Falsifier:** branch state diverges, provenance is incomplete, or full duplication is
equally efficient.

## H9 — Causal-cone branch recomputation is exact when declared exact

After a registered past edit, expanding dependency recomputation matches complete
resimulation within tolerance; uncertain dependencies expand the cone or trigger a
full fallback.

**Falsifier:** the local branch silently misses dependencies or materially disagrees
with full replay.

## H10 — Useful causal locality exists

At least two edit classes/scenes retain a non-global causal cone for a useful time
window, providing a meaningful latency or storage benefit.

**Falsifier:** every useful edit immediately becomes global or offers no benefit over
full resimulation.

## H11 — Correlation surgery is an authoring primitive

A sparse target-conditioned surgery preserves one declared current frame, cellwise
velocity multiset, and primary invariants while selectively suppressing the chosen
future stroke and retaining the rest of the glyph.

**Falsifier:** current mismatch is visible, the selected stroke does not change, or
the rest of the terminal glyph collapses with it.

## H12 — The workflow is a graphics contribution

Users can rewind, inspect, edit, branch, and compare physically recomputed molecular
futures in a way not reducible to backward playback, keyframing, or a decorative
collision graph.

**Falsifier:** the only compelling result is a reverse movie, the graph does not drive
computation, or the branch interaction has no practical/authoring value.

---

## Hypothesis dependency

```text
H1 → H2 → H3/H4/H5 → H6
H1 → H7 → H8 → H9 → H10
H2/H4 + H8 → H11
H9/H10/H11 → H12
```

## Preregistration rule

H1–H5 primary protocol, metrics, bins, controls, and stop conditions must be committed
and tagged before frozen results are generated. A post-result document may explain
but not retroactively redefine the primary hypothesis.
