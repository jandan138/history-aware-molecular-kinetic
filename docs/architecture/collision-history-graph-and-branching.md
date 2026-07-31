# Collision-History Graph, Replay, and Counterfactual Branching

This document defines the active SIG-route architecture. It turns exact hard-sphere
collision history into a versioned simulation representation rather than a debug
log.

## 1. Design objective

The system must support four operations without confusing them:

1. **physical reversal** — negate velocities and integrate exact dynamics;
2. **deterministic replay** — reproduce a previously recorded branch event by
   event;
3. **counterfactual branching** — change an earlier particle, collision, or
   geometry condition and generate a new future;
4. **correlation surgery** — alter hidden particle pairing/correlation while
   preserving a preregistered resolved one-particle present.

A video played backward is not a simulation operation. A modified event log with an
unchanged exact microstate does not change the future. Every branch must correspond
to a declared state transformation and a valid subsequent dynamics.

## 2. Core state

### 2.1 Exact microstate

At time `t`:

\[
X(t)=\{x_i(t),v_i(t),r_i,m_i,\mathrm{id}_i\}_{i=1}^{N}.
\]

This state uniquely determines the future under the declared hard-sphere dynamics,
subject to deterministic numerical event ordering.

### 2.2 Resolved one-particle state

A surgery protocol declares a resolution `h` and computes:

\[
f_{1,h}(x,v,c),
\]

where `c` may be a passive color/species label. The corresponding audit records
block/bin counts and selected moments such as density, momentum, temperature, and
anisotropy.

`f1_h` is an operational finite-resolution contract. It is not the exact continuous
`f1`, and it is not the complete microstate.

### 2.3 Collision event

Each exact collision event is represented as:

```text
CollisionEvent
  event_id
  branch_id
  time
  particle_i
  particle_j
  contact_normal
  incoming_relative_normal_velocity
  pre_state_checksum
  post_state_checksum
  predecessor_event_i
  predecessor_event_j
  geometry_revision
  event_order_key
```

Repeated collisions between the same pair remain distinct event nodes.

## 3. Collision causal multigraph

For every particle, events involving that particle are linked in temporal order. If
particle `i` participates in event `a` and then event `b`, add:

\[
e_a\rightarrow e_b.
\]

A binary collision therefore has up to two immediate event predecessors and can
have many future descendants. The graph is acyclic when ordered by simulation time,
while repeated particle pairs create multiedges in the underlying particle-event
incidence structure.

The graph supports:

- shared collision ancestors;
- collision-history molecules;
- descendant causal cones;
- event-level random access;
- branch provenance;
- history-budget interventions;
- visual explanation of how a local perturbation spreads.

## 4. Checkpoints and deterministic replay

A replay package contains:

```text
checkpoint state
+ event segment
+ geometry revision history
+ deterministic event-order policy
+ numerical checksums
```

Checkpoints are placed by a policy balancing storage and replay latency. Replaying a
segment must verify:

- event IDs and pair IDs;
- event time within the declared tolerance;
- contact normal and incoming relative velocity;
- pre/post state checksums;
- invariant drift;
- geometry revision.

A mismatch produces a replay-divergence artifact; it must not be silently corrected
by snapping particles to logged states in primary evidence.

## 5. Branch store

A branch is persistent and shares immutable history with its parent until a fork:

```text
BranchRecord
  branch_id
  parent_branch_id
  fork_time
  fork_event_id
  edit_manifest
  base_checkpoint_id
  reused_history_range
  invalidated_event_set
  newly_simulated_event_range
  terminal_state_hash
```

The storage layer should use copy-on-write references to checkpoints and event
segments. Full state duplication per branch is a baseline, not the target design.

## 6. Counterfactual edit protocol

Supported first-paper edits are intentionally bounded:

1. perturb one particle velocity before an event;
2. suppress or modify one collision under an explicitly defined extended dynamics;
3. move, insert, or remove a simple analytic obstacle at a past time;
4. apply a declared correlation-surgery transformation at a pivot.

Every edit creates a new branch and never mutates frozen parent evidence.

## 7. Causal-cone recomputation

Let `S0` be particles or geometry directly modified at fork time. The affected set
is expanded whenever an affected trajectory interacts with an unaffected particle
or geometry dependency.

Conceptually:

```text
restore checkpoint before edit
apply edit
advance affected set
when affected meets unaffected:
    absorb newly affected state/history
invalidate its old descendants
continue until target time
```

The implementation may reuse old trajectories only while it can prove they remain
independent of the modified branch. When uncertainty exists, it expands the cone or
falls back to full replay.

Primary correctness compares local branch recomputation with a complete
resimulation from the same checkpoint:

\[
\epsilon_{\rm branch}
= D\bigl(X_{\rm local}(T),X_{\rm full}(T)\bigr).
\]

For exact deterministic evidence, event/state equivalence is required within the
registered numerical tolerance. Approximate cone policies must be labeled and
reported separately.

## 8. Correlation surgery

A surgery operator transforms the pivot microstate:

\[
X(t_*)\mapsto \widetilde X(t_*),
\]

subject to preregistered constraints such as:

\[
f_{1,h}[X]=f_{1,h}[\widetilde X],
\]

plus mass, momentum, energy, color counts, and overlap validity.

The initial operator permutes velocities within fixed `(space block, passive color)`
groups. Stronger versions may use constrained matching or optimal transport to
reduce finer-scale one-particle mismatch.

The audit must report matching error over a resolution grid—not only at the one
resolution used to construct the surgery.

## 9. Collision-molecule budget

The scientific intervention attaches a molecule label and complexity state to
candidate events. A budget `(Lambda, Gamma)` controls:

- maximum connected molecule size `Lambda`;
- permitted recollision/reconnection complexity `Gamma`.

Events exceeding the budget follow an explicit extended-dynamics rule, initially
`ghost-through`. Such a branch is not exact EDMD and must use a distinct backend and
artifact label.

Required null controls include:

- random collision suppression matched by count and time distribution;
- topology-shuffled partner reassignment with comparable event statistics;
- no-collision ghost dynamics;
- full exact EDMD.

These controls distinguish molecule topology from the trivial effect of allowing
more collisions.

## 10. Canonical artifacts

The active route requires versioned artifacts for:

```text
collision-event-log
collision-causal-graph
checkpoint-bundle
branch-record
edit-manifest
causal-cone-report
replay-audit
resolved-state-audit
correlation-surgery-report
history-budget-report
branch-comparison-report
```

Large arrays may be stored separately, but manifests must include shape, units,
hashes, branch lineage, solver revision, and numerical tolerances.

## 11. Metrics

### Reversal and replay

- position/velocity return error;
- event sequence agreement;
- checksum agreement;
- invariant drift;
- random-access latency.

### Branching

- local-vs-full resimulation error;
- affected particle fraction;
- invalidated event fraction;
- runtime speedup;
- branch storage per fork;
- fallback frequency.

### Surgery and scientific mechanism

- multi-resolution `f1_h` mismatch;
- selected moment mismatch;
- future observable divergence;
- echo recovery;
- incoming-pair closure-defect proxy;
- history-budget response relative to null controls.

## 12. Failure modes

The method must expose rather than hide:

- causal cones that rapidly become global;
- nearly simultaneous collision ordering instability;
- grazing collisions and floating-point reversibility limits;
- surgery that matches a coarse histogram but differs at finer resolution;
- history-budget effects explained only by collision count;
- branches whose visual difference is created by rendering rather than dynamics.

## 13. VIS extension boundary

A future IEEE VIS system may consume the same artifacts in linked views:

- particle space;
- event graph;
- branch tree;
- velocity space;
- causal-cone timeline;
- history-budget curves;
- uncertainty and replay divergence.

Those views are an extension client. They must not change the active SIG simulation
semantics or become a substitute for the graphics algorithm.
