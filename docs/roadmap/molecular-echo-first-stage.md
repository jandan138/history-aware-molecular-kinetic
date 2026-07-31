# Molecular Time Machine — first-stage decision

**Status:** complete with `go`. E1 passed, E2 closed its planned mechanism, and the
combined E3 timeline/causal-branch Hero passed every frozen check.

**Purpose:** finish one coherent paper arc before investing in breadth, performance,
3D production, or user evaluation.

## The stage in one line

```text
E1: a frame is not a future
→ E2: a slider is not a history
→ E3: make one collision editable
```

## Act 1 complete — Molecular Echoes E1

`MOLECULAR-ECHOES-E1-v0` returned `go`. Across `N=128,256` and six seeds, the
mean exact-minus-chaotized terminal color gap is `0.449784`, with seed-bootstrap
95% interval `[0.436573,0.460660]`. The exact branch reconstructs the pattern while
the branch with the same frozen 4×2 resolved present does not.

This result is the scientific hook and is limited to the registered resolved
present. The finer 8×4 mismatch remains disclosed. See the
[E1 result](../benchmarks/molecular-echoes-e1-result.md).

## Act 2 complete — Molecular Echoes E2

E2's collision-budget ladder is strong (`0.930574` mean reverse Spearman), but its
selected structured molecule does not beat count/time-matched random or
topology-shuffled controls. The registered decision is `stop_e2`.

The project will not add E2 budgets, seeds, `N=512`, new proxies, or asymptotic
sequences. The full negative stays in the supplement. In the main story it provides
one transition: more collision dose can restore more echo, but a dose slider does
not tell an animator which cause to edit. See the
[E2 result](../benchmarks/molecular-echoes-e2-result.md).

## Act 3 complete — One Collision, Two Worlds E3

E3 combines the graph and branch gates. A graph passes only if it performs the edit.

The frozen run returned `go`: terminal color gap `0.188218`, `33/128` visibly
changed particles, `106/106` local/full collision-pair agreement, `79/105` reused
baseline events, and `33/128` peak affected particles. See the
[E3 result](../benchmarks/molecular-time-machine-e3-result.md).

### Frozen Hero

```text
source = E1 exact-reverse, N=128, seed=0
target = collision #2, pair (101,118)
fork = 1e-6 before the target
edit = +1 degree pair-relative-velocity rotation in the COM frame
horizon = 1.0
```

### Required implementation

1. stable collision IDs, ordering keys, predecessor links, and state hashes;
2. initial, periodic, fork, and terminal checkpoints;
3. a momentum/energy-preserving physical edit;
4. a monotone affected set that reuses only provably independent baseline events;
5. the same numerical collision kernel for local and full runs;
6. one complete resimulation for event/state correctness;
7. collision timeline, edit, causal-cone, comparison, and render manifests;
8. one main figure and one 15–20 second neutral two-world video.

The exact rule never truncates uncertain dependencies. It promotes the involved
particle and continues. The first reference implementation claims event/history
reuse, not optimized wall-clock speed.

### Decision

- **Go:** local/full correctness, visible world split, at least 50% baseline-event
  reuse, and less than 50% peak affected particles all pass.
- **Narrow:** correctness and world split pass, but reuse/locality does not. Keep
  the history-provenance authoring story and drop the locality claim.
- **Stop:** the local branch disagrees with full resimulation or the registered edit
  does not visibly split the worlds.

The exact thresholds and artifact contract are frozen in the
[E3 preregistration](../benchmarks/molecular-time-machine-e3-preregistration.md).

## What does not belong before this decision

- additional E1/E2 defensive experiments;
- density, seed, or parameter sweeps;
- geometry edits and obstacle zoos;
- approximate fixed-radius cones;
- `N=512`, 3D hard spheres, GPU/native optimization;
- a full editor UI or user study;
- path-traced production assets.

Those may become E4–E6 work only if the one-collision story earns them.

## Stage handoff after E3 passed

The next phase should deepen the contribution in this order:

1. native/parallel branch execution and interactive latency;
2. one genuinely different physical edit family;
3. a small locality/performance map chosen to support the algorithm claim;
4. 3D art direction and creator-facing interaction;
5. only then, a focused user evaluation if the paper needs it.

The first stage ends with a single result report and frozen evidence package—not a
collection of unrelated safety studies.
