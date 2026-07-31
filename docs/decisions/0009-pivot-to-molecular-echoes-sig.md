# ADR 0009 — Pivot the active paper route to Molecular Echoes

- **Status:** accepted
- **Date:** 2026-07-31
- **Decision owner:** project lead

## Context

The original paper route proposed a collision-history predictor for deciding where an
EDMD–kinetic dynamic LOD should retain exact molecular identities. The internal
`PHASE1-HISTORY-STORY-v0` pilot did not support the operational claim: the tested
scalar history features did not improve grouped/OOD discrepancy prediction by the
predeclared useful margin.

Continuing directly to representation conversion, a partition controller, GPU
optimization, and polished LOD scenes would therefore build an expensive graphics
system on top of an unsupported premise.

At the same time, the pilot and the follow-up echo smoke test exposed a stronger and
more direct phenomenon: states that match a declared resolved one-particle present
can carry different multi-particle collision correlations and therefore evolve into
very different futures. This phenomenon connects naturally to the cumulants and
collision-history molecules used by Deng, Hani, and Ma to control correlations in
the long-time hard-sphere derivation of Boltzmann.

## Decision

The active first-paper route becomes:

> **Molecular Echoes: Reversible and Counterfactual Hard-Sphere Animation with
> Collision-History Graphs**

The route has two inseparable tracks.

### Scientific track

1. establish exact numerical reversibility;
2. construct exact-reverse, marginal-preserving chaotized, DSMC, and
   history-budgeted branches;
3. audit the declared resolved state `f1_h` across multiple resolutions;
4. measure future branch separation and incoming-pair closure-defect proxies;
5. test collision-molecule budgets `(Lambda, Gamma)` against count-matched and
   topology-shuffled null controls.

### Graphics track

1. represent the event history as a timestamped collision causal multigraph;
2. support deterministic replay and random access through checkpoints plus event
   logs;
3. support causal rewind and counterfactual branching after particle, collision, or
   geometry edits;
4. recompute only the expanding future causal cone when correct, falling back to a
   full replay when the cone becomes global;
5. provide coarse-state-preserving correlation surgery for authoring different
   futures from the same declared visible present;
6. produce three bounded Hero Scenes: **Molecular Logo Echo**, **One Collision, Two
   Worlds**, and **Edit the Past**.

## Relationship to the original LOD route

The original R0–B5 benchmark infrastructure, exact/kinetic solvers, artifacts,
render manifests, and negative result remain in the repository. They are not erased
or rewritten as success.

The following items are deferred rather than active:

- history-error predictor;
- online exact/kinetic region selection;
- promotion/demotion engineering;
- dynamic molecular LOD;
- the old Zoomable Mixing / Correlation Labyrinth / Expansion-into-Vacuum paper
  spine.

DSMC remains important, but its active role changes from runtime coarse backend to a
controlled baseline that deliberately forgets exact collision pairing.

## Claim boundary

The project may say that it is **inspired by** the cumulant and collision-history
molecule structure in the Deng–Hani–Ma proof.

It must not say that:

- the proof's cutting algorithm has been implemented as an animation algorithm;
- the theorem guarantees the finite-system surgery or branching method;
- velocity reversal or a Loschmidt echo is novel by itself;
- an event log alone is a novel causal simulation method;
- matching a discretized `f1_h` means matching the exact microscopic state or the
  continuous one-particle distribution.

## Venue policy

The first target is SIGGRAPH / SIGGRAPH Asia. The paper must contain a graphics
algorithm—not only a physics phenomenon—including causal rewind, branch reuse,
interaction, correctness, performance, and high-quality three-dimensional demos.

IEEE VIS is a deliberate fallback only if the strongest result becomes an
interactive visual-analytics system for collision molecules, branch comparison,
and causal provenance. A VIS submission would require linked views, explicit
analysis tasks, domain evaluation, and a different paper structure; it is not a
simple venue rename.

## Consequences

- new active milestones and Go/No-Go gates replace the LOD milestones;
- the first three weeks are preregistered feasibility work, not hero rendering;
- graphical polish is blocked until numerical reversal, state matching, and branch
  correctness pass;
- the repository keeps the old route as an auditable negative/deferred branch;
- the architecture must add history graph, checkpoint, branch-store, causal-cone,
  and surgery contracts while retaining solver and renderer independence.
