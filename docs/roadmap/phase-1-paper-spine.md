# Phase I paper spine — closed exploratory study

**Decision (2026-07-31):** stop the Phase-I predictive-history claim as a
paper spine. The completed exploratory analysis found no reliable grouped/OOD
benefit from the scalar collision-history features: relative MAE change
\(-0.83\%\), 95% interval \([-2.21\%,0.52\%]\), and worse high-error coverage
for the history selection. The evidence remains useful as a negative result and
as a guard against returning to an under-motivated predictor story.

The active successor is
[Collision-History Echoes](../research/collision-history-echo-route.md):
construct the same resolved \(f_1\) with different multi-particle correlations,
then use a collision-molecule intervention to measure their causal role.

Everything below records the historical Phase-I protocol and its intended
decision rule. It is not an active implementation backlog.

## Historical one-sentence claim

Blocks with nearly matched present macroscopic state can carry different exact
collision histories, and those histories may predict a different finite-horizon
EDMD–kinetic discrepancy on held-out geometry and state families.

Phase I exists to accept or reject that sentence. It is not a general-purpose
hybrid-solver milestone.

## Historical narrative arc

1. **Different past:** prepare ensembles in an open channel, a single-baffle
   channel, and a Correlation Labyrinth.
2. **Same now:** remove all preparation obstacles, enter one shared observation
   geometry, and identify block pairs with matched density, velocity, temperature,
   stress, heat flux, geometry descriptors, numerical metadata, and current
   EDMD–DSMC discrepancy.
3. **Retained history:** show that exact repeated-pair, cycle, component, lineage,
   and pair-velocity-correlation summaries differ over a fixed history window.
4. **Different future:** measure a fixed-horizon discrepancy in density,
   temperature, mean velocity, and velocity-distribution shape.
5. **Predict before failure:** compare the same state-only model with and without
   exact-history features under leave-one-geometry-out and leave-one-state-out
   evaluation.
6. **Why it matters:** at the same exact-region budget, test whether the history
   model covers more of the truly high-error blocks. This is an oracle upper
   bound, not yet a dynamic hybrid claim.

## Historical primary figures

### Figure 1 — Matched state, different history

One open-channel block and one Correlation-Labyrinth block:

- side-by-side geometry and particles;
- matched current state table;
- rolling collision graph;
- future exact-versus-kinetic observable traces.

### Figure 2 — History predicts held-out future error

- state-only versus state+history grouped/OOD MAE;
- per-geometry and per-state-family deltas;
- grouped bootstrap interval;
- one compact feature-family ablation if the main result is positive.

### Figure 3 — Local exactness has potential value

At a fixed 20% block budget:

- state-only high-error coverage;
- history-aware high-error coverage;
- oracle residual discrepancy after treating selected blocks as exact.

This is the Phase-I bridge to later conversion/dynamic-LOD work.

## Historical minimum credibility checks

Only checks that protect the three figures are mandatory:

- analytic two-disk collision time and elastic response;
- EDMD/DSMC mass and energy conservation in the selected cases;
- matched snapshot times and shared observable definitions;
- complete-factorial geometry/state design;
- trajectory-disjoint grouped splits;
- explicit `oracle_only` label on exact-history features.

External-oracle reproduction, large convergence atlases, three-dimensional
solvers, bidirectional conversion, GPU optimization, and hero rendering are not
Phase-I blockers.

## Historical decision rule

- **Go:** history improves held-out prediction and high-error coverage by an
  operationally visible margin.
- **Pivot:** the result is geometry/state attribution without incremental history
  value.
- **Stop the history claim:** the interval is consistent with no useful gain.
