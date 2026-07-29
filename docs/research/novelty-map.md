# Novelty map

| Candidate contribution | Existing territory | Required distinction |
|---|---|---|
| EDMD solver | Mature event-driven MD packages | Not a claim; correctness infrastructure only |
| DSMC solver | Mature SPARTA and many codes | Not a claim; coarse backend only |
| EDMD–DSMC hybrid | SEDMD and related particle hybrids | Same-gas dynamic representation and discrepancy-driven partition |
| Adaptive rarefied flow | DSMC–CFD, USP–DSMC, UGKWP | History value beyond strong state-only breakdown criteria |
| Collision graph | Common simulation data structure | Validated predictor, streaming cost, observability labels |
| Exact→kinetic resampling | Particle coarsening literature | Conservation plus controlled non-equilibrium and pair statistics |
| Kinetic→exact sampling | Particle generation literature | Exclusion-aware, moment-corrected, low-transient promotion |
| Zoomable particles | Visual LOD literature | Physics partition independent of camera, same evidence state |
| GPU implementation | Many particle and kinetic GPU codes | Dynamic cross-representation system, not raw throughput |

## The central novelty test

A history feature is not novel merely because it has not appeared in a graphics
paper. It becomes scientifically relevant only if it predicts a pre-declared
model error on held-out cases beyond:

- density and packing fraction;
- local and gradient-length Knudsen numbers;
- Maxwellian residual;
- stress and heat flux;
- wall distance and geometry descriptors;
- local collision rate;
- numerical resolution and particle weight;
- finite-density kinetic alternatives.

## Minimum SIG/TOG package

A plausible full paper needs all of:

1. statistically defensible B2 gain;
2. a practical observability strategy;
3. conservative conversion;
4. a meaningful cost-quality curve;
5. two visually interpretable restored phenomena;
6. a shared renderer and strong baselines;
7. explicit failure regions.

Without items 4–6, the work is more naturally a computational physics paper.
