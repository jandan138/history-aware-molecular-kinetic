# Paper Positioning

## Working title

> **One Collision, Two Worlds: Causal Rewind for Molecular Animation**

System name:

> **Molecular Time Machine**

## The story before the method

The paper begins with a question a creator can understand: if one molecular frame
does not contain enough information to determine its visible future, can we expose
and edit the missing history?

E1 supplies the hook. Two branches share the registered resolved present but do not
share the same future. E2 supplies the plot twist. A collision-budget slider grades
the echo, yet registered wiring controls show that the slider has not located a
special cause. The paper therefore stops treating “how much history?” as the main
interaction and makes one past collision addressable.

The climax is one physical gesture: rewind to collision #2, rotate the pair's
relative velocity by one degree, and watch one world become two. A timestamped
collision timeline, checkpoints, and an exact expanding-causal-cone algorithm reuse
the old events that remain independent and recompute the events that inherit the
edit. The branch is validated against complete resimulation under the same hard-disk
kernel and shown under a locked renderer.

## One-paragraph contribution statement

We introduce an exact counterfactual branching representation for event-driven
hard-sphere animation. Every collision receives stable identity, state hashes, and
links to the preceding collisions of its two particles. A conservative edit in a
pair center-of-mass frame forks this timeline. Our branch executor replays baseline
events between unaffected particles and recomputes only pairs touching a monotonically
growing affected set; any uncertain dependency expands that set. In the frozen Hero,
a one-degree edit to one early collision produces a visible alternate future while
the local event sequence and terminal state match a complete resimulation within
registered tolerances. The result turns hidden collision correlation—motivated by
the collision-history structures in Deng–Hani–Ma—from a scientific observation into
an animation operation.

## Contributions in paper order

### 1. Collision-addressable molecular timeline

Each accepted pair collision stores event ID, deterministic order key, time, pair,
contact normal, incoming relative normal speed, causal predecessors, and pre/post
state hashes. Periodic checkpoints support exact forks. Repeated collisions remain
distinct events.

### 2. Exact conservative causal branch

An edit starts a growing affected-particle set. Old events between unaffected
particles are reused. An old event touching the set is invalidated and its other
participant is promoted. New affected–unaffected contacts also promote particles.
The exact method never truncates an uncertain cone. The same prediction, advection,
impulse, and ordering kernel is shared with full EDMD.

### 3. One-collision authoring interaction and evidence

The user chooses an event rather than an opaque budget. The edit manifest records
the checkpoint, target pair, physical transformation, conservation audit, branch
lineage, and hashes. A main figure and 15–20 second neutral video show the selected
event, the one-degree edit, two terminal worlds, and the causal reach under an
identical camera and timeline.

## Why this belongs at SIGGRAPH

The contribution is a simulation/animation workflow, not merely a statistical-
mechanics plot:

```text
rewind to a meaningful physical event
→ edit that event conservatively
→ reuse the independent past/future segments
→ exactly recompute inherited consequences
→ inspect two reproducible physical worlds
```

The first evidence claims event reuse rather than optimized wall-clock speed. A
native implementation and interactive latency study become worthwhile only after
the semantic operation and story pass.

## Scientific role of Deng–Hani–Ma

Deng, Hani, and Ma propagate cumulants carrying complete collision histories and
organize correlated structures as collision-history molecules in their derivation
of Boltzmann from hard spheres. This motivates the information boundary: a cheap
one-particle present omits structured multi-particle history that may determine a
carefully correlated future.

The paper says “inspired by the collision-history and cumulant structure.” It does
not say that we implement their cutting argument, that their theorem proves our
finite branch method, or that E2 identified their molecule topology in the Hero.

## Strongest prior-art boundaries

### Many-Worlds Browsing

Twigg and James already compute and browse many multibody futures. Multiple
simulations and interactive outcome selection are not the novelty. Our distinct
semantic unit is an addressable past collision whose particle ancestry drives exact
reuse and recomputation.

### Physics Storyboards and animation control

Physics Storyboards and broader spacetime/particle control already summarize,
retime, tune, or optimize physical animation. We do not claim generic animation
control. Our operation edits a realized collision history and follows the altered
initial-value problem without optimizing toward a target frame.

### Time Warp and reversible collision simulation

Checkpoint rollback, causal recovery, and reversible elastic collision algorithms
are established. We do not claim them individually. The contribution is the
hard-sphere collision-event representation tied to a creator-facing physical edit,
exact ancestry-driven branch reuse, and visual evidence.

### Loschmidt echoes

Velocity reversal is the entrance demonstration. E1 makes the missing-history
question visible; it is not the algorithmic claim.

## What the first gate may say

- one registered past-collision edit produces the registered visible world split;
- the edit preserves momentum and kinetic energy within tolerance;
- causal recomputation matches full resimulation event-by-event and at the terminal
  state within tolerance;
- the frozen Hero reuses the registered fraction of baseline events and retains the
  registered causal locality;
- every visual output is tied to branch/edit/checkpoint hashes.

## What it may not yet say

- causal cones are always local;
- the Python implementation is faster than full resimulation;
- all collision, geometry, and rigid-body edit families are supported;
- a user study establishes authoring benefit;
- the method is the first multiple-futures or rollback system;
- the E2 molecule wiring mechanism succeeded;
- a discretized resolved present is an identical exact state.

## Main-paper figure spine

1. **A frame is not a future.** One compact E1 image establishes the hidden-history
   hook.
2. **A slider is not a history.** One small E2 transition plot states the graded
   dose result and the failed wiring contrast.
3. **Make every collision addressable.** Timeline data model and selected event.
4. **One Collision, Two Worlds.** The one-degree edit, causal cone, original world,
   and edited world.
5. **Exact reuse.** A compact event-reuse/correctness diagram and numerical table.
6. **Same Present, Chosen Future.** One common pivot, four touched particles, and
   matched E/C physical futures close the authoring loop.

The complete E2 negative, fine-grid E1 limitation, engineering diagnostics, and
other future edit families belong in the supplement. They support honesty without
interrupting the main narrative.

## Venue route

- **Primary:** SIGGRAPH / SIGGRAPH Asia.
- **Fallback:** IEEE VIS only after a real pivot to linked analysis of event graphs,
  branch provenance, and causal cones; it is not a renamed version of this paper.

See [ADR 0010](../decisions/0010-molecular-time-machine-paper-spine.md) and the
[E3 frozen recipe](../benchmarks/molecular-time-machine-e3-preregistration.md).
The canonical gate returned `go`; numerical evidence and hashes are in the
[E3 result](../benchmarks/molecular-time-machine-e3-result.md).
E4 causal steering and the frozen E5 same-present recipe extend that first gate into
the complete creator-facing story.
