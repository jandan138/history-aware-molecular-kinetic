# Research hypotheses

## H1 — Incremental history value

History features improve held-out prediction of exact-versus-kinetic discrepancy
after controlling for state, geometry, and resolution.

**Falsifier:** no meaningful gain under grouped geometry/regime splits.

## H2 — Model specificity

The useful features and thresholds depend on the coarse kinetic backend.
Boltzmann DSMC and an Enskog-like backend should not be conflated.

**Falsifier:** history appears useful only because the baseline equation is wrong.

## H3 — Conservative demotion

Exact-to-kinetic conversion can preserve mass, momentum, and energy to numerical
precision while keeping stress, heat flux, and velocity-distribution error below
the downstream kinetic discretization error.

## H4 — Controlled promotion

Kinetic-to-exact sampling with excluded-volume placement, moment correction, and
a warm-up/blending policy avoids unacceptable transients and visual popping.

## H5 — Sparse observability

A practical online controller can use coarse runtime observables plus sparse
shadow EDMD probes; it does not require full exact collision history everywhere.

## H6 — Dynamic cost-quality benefit

For at least two nontrivial scenes, the method occupies a stable intermediate
exact-region fraction and improves error at fixed cost or cost at fixed error.

## H7 — Graphics value

Localized exactness restores a visible physical effect—not merely a diagnostic
mask—and the result remains legible under a shared renderer.
