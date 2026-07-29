# B2 — History indicator

## 1. Core test

Does collision-history information improve prediction of exact-versus-kinetic
error beyond strong state-only features on held-out groups?

## 2. Feature tiers

### Tier S — State-only runtime features

- density and packing fraction;
- velocity and temperature;
- local/gradient-length Knudsen indicators;
- Maxwellian residual;
- stress deviator and heat flux;
- collision rate;
- wall distance, confinement, and geometry descriptors;
- kinetic cell size, time step, and particle weight;
- recent coarse temporal derivatives.

### Tier H-Exact — Exact history features

- repeated-pair ratio;
- unique-pair fraction;
- graph circuit rank;
- component-size distribution;
- component re-merging;
- lineage depth;
- re-encounter time;
- low-rank pair/cumulant proxies.

These are oracle-only when the block is kinetic.

### Tier H-Probe — Shadow-probe features

The same or reduced features estimated from a short exact micro-probe initialized
from a coarse state.

### Tier H-Coarse — Coarse-history candidates

Only features with a justified kinetic meaning belong here. DSMC superparticle
pair repetition is not admitted by default.

## 3. Baseline hierarchy

Evaluate in this order:

1. constant/global prior;
2. density and packing fraction;
3. Knudsen breakdown indicator;
4. full state/moment model;
5. state + geometry;
6. state + geometry + Enskog discrepancy;
7. state + geometry + exact history oracle;
8. state + geometry + practical probe/history features.

The scientific result is the incremental gain from 6 to 7, and the practical
result is how much of that gain survives in 8.

## 4. Models

Begin with interpretable models:

- linear/generalized linear model;
- decision tree / gradient-boosted trees;
- monotone model where appropriate;
- calibrated classifier for threshold exceedance.

A neural model is not justified until the dataset and split logic are stable.

## 5. Evaluation

For continuous error:

- MAE/RMSE normalized by reference scale;
- rank correlation;
- calibration by predicted uncertainty;
- worst-decile recall;
- spatially grouped bootstrap confidence intervals.

For refine/no-refine classification:

- precision/recall at a declared error threshold;
- false-negative rate weighted by physical consequence;
- exact-region fraction;
- expected cost under policy;
- calibration curve.

## 6. Incremental-value tests

Report:

- delta metric with confidence interval;
- permutation importance conditional on state groups;
- ablation by each history family;
- matched-state pair analysis;
- leave-geometry-out generalization;
- Enskog-controlled comparison;
- sensitivity to history-window duration.

## 7. Matched-state experiment

The strongest visual/scientific case contains two block populations with similar:

\[
\rho,\phi,T,u,\mathrm{Kn},\Pi,q
\]

but different geometry-conditioned collision histories and future discrepancy.

If such a pair cannot be created without changing unobserved state variables, the
claim should be weakened.

## 8. Observability audit

Every trained policy is serialized with an allowed feature set. Evaluation fails
if an online policy consumes `oracle_only` features.

## 9. Go threshold

B2 unlocks B4 only if practical features show a robust held-out improvement that
is large enough to alter the cost-quality partition—not merely a statistically
significant but operationally tiny delta.

The exact numerical threshold is frozen after B1 scale analysis and before final
B2 evaluation.
