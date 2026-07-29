# Scientific risks

## R1 — The theorem regime removes the need for refinement

In a sufficiently dilute Boltzmann–Grad regime, correlations become small and
DSMC should agree with exact dynamics. Exact patches may stay off.

**Response:** treat this as a correct negative control; seek transitional regimes
without falsely claiming theorem coverage.

## R2 — Enskog explains the discrepancy

At higher packing fraction, pair structure at contact may dominate.

**Response:** compare against a finite-density kinetic backend before attributing
error to history.

## R3 — Oracle-only leakage

Full EDMD history is used to train and run the indicator, making the adaptive
method circular.

**Response:** tag every feature by visibility and evaluate online policies with
runtime-observable or bounded probe features only.

## R4 — DSMC identity is misinterpreted

Repeated stochastic pairing of superparticles is treated as molecular
re-collision.

**Response:** never use coarse superparticle IDs as ground-truth history without
a justified model.

## R5 — Random train/test leakage

Adjacent blocks or times from one simulation appear in both train and test sets.

**Response:** split by geometry, regime, seed family, and transient type.

## R6 — Conversion dominates error

Promotion/demotion transients erase the value of better local physics.

**Response:** benchmark conversion independently before B4.

## R7 — Exact regions dominate

The controller refines almost everything in useful scenes.

**Response:** report the failure and pivot to faster exact EDMD rather than hiding
partition fractions.

## R8 — Visual difference is not physical

The result looks richer only because more particles are drawn.

**Response:** use shared rendering density and compare physical observables.

## R9 — Complex assets consume the project

A spacecraft or industrial chamber becomes the main workload.

**Response:** freeze canonical geometry primitives until B4 passes.
