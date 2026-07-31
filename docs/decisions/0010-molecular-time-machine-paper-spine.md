# ADR 0010 — Make one editable collision the paper spine

- **Status:** accepted
- **Date:** 2026-08-01
- **Decision owner:** project lead

## Context

E1 established the hook: a molecular frame is not a complete future. Exact reversal
recovers the passive-color pattern, while a branch with the same registered
resolved present does not.

E2 then supplied a useful plot twist rather than the planned mechanism. Allowing
more collisions produces a strong graded echo, but the registered structured
collision molecule does not outperform controls with comparable collision dose.
The result rejects the sentence “this budget has found the special wiring.” It does
not reject collision history as an editable simulation representation.

Continuing to add E2 budgets, seeds, proxies, safety controls, or asymptotic studies
would make the paper more defensive and less coherent. Splitting graph construction
and causal branching into two distant engineering stages would have the same
problem: a collision graph is interesting only when it performs the edit.

## Decision

The active paper spine becomes:

> **One Collision, Two Worlds: Causal Rewind for Molecular Animation**

The system name and short description are:

> **Molecular Time Machine** turns every hard-sphere collision into an addressable
> event. A user rewinds to one event, makes a conservative physical edit, and the
> system reuses the untouched history while exactly recomputing the expanding
> causal future.

The paper has three acts:

1. **A frame is not a future.** E1 shows that hidden collision correlation changes
   what the same registered visible present can do.
2. **A slider is not a history.** E2 shows that collision dose grades the echo but
   does not identify a privileged molecule wiring. The result is one transition,
   not a failed-paper centerpiece.
3. **Make the past editable.** The contribution is an addressable collision
   timeline plus an exact conservative causal-branch algorithm, demonstrated by
   editing one past collision and producing two physical futures.

Graph representation and causal branching are combined into one E3 gate. The graph
must drive reuse and invalidation in the same experiment; a decorative graph does
not pass.

## Frozen first Hero recipe

The first E3 evidence uses the already frozen E1 exact-reverse hero:

```text
N = 128
seed = 0
target collision ordinal = 2
target pair = (101, 118)
target time = 0.03429093183046455
fork = target time - 1e-6
edit = rotate pair relative velocity +1 degree counterclockwise
frame = pair center of mass
horizon = 1.0
sample interval = 0.02
checkpoint interval = 16 collision events
```

The edit leaves positions unchanged and preserves pair momentum and kinetic energy.
The local branch is compared with one full resimulation from the same edited
checkpoint. That comparison is part of the algorithm claim, not an auxiliary
defensive experiment.

## First-paper claim boundary

The first gate may claim:

- stable event identity, predecessor/successor queries, checkpoints, and hashes;
- an explicit pair-relative-velocity edit with conserved momentum and energy;
- exact agreement of causal-cone recomputation with full resimulation within the
  registered numerical tolerance;
- measured reuse of baseline events and measured causal spread in the frozen hero;
- a physically recomputed visual fork under one locked renderer.

It does not yet claim:

- that every edit stays local;
- a wall-clock speedup in the Python reference implementation;
- generic rigid-body or geometry editing;
- a user study;
- a theorem-level consequence of Deng–Hani–Ma;
- novelty for velocity reversal, event logs, checkpoints, or generic rollback.

## Prior-art distinction

Many-Worlds Browsing already samples and interactively browses many physical
multibody outcomes. Physics Storyboards already summarizes and tunes procedural
animations through important space-time outcomes. Time Warp already establishes
checkpointed rollback for discrete-event systems.

The first-paper distinction is their combination at a different semantic unit:
the user edits an **addressable past hard-sphere collision**, and the collision
ancestry itself determines which exact future events can be reused and which must
be recomputed. The paper must compare against these strongest conceptual neighbors,
not present “multiple futures” or “rollback” as new categories.

## Consequences

- E2 remains fully reported in the supplement and receives only a short main-text
  bridge: “More collisions bring back more echo. But a slider cannot tell us which
  cause to edit. So we made every collision addressable.”
- E3 replaces the old E3/E4 split for the first Hero and decision gate.
- Geometry edits, 3D production, GPU work, scale sweeps, approximate cones, and a
  user study are postponed until the one-collision story passes.
- Runtime is recorded, but the first Python evidence claims history/event reuse,
  not optimized speed.
- The frozen recipe tag precedes the canonical result tag.

