# Novelty map

## Active route: collision-history echoes

| Candidate contribution | Existing territory | Required distinction |
|---|---|---|
| Velocity reversal / Loschmidt echo | Classical reversible hard-particle dynamics | Not novel by itself; it is only the controlled entrance to the problem |
| Collision clusters and correlation errors | BBGKY, Lanford-style and backward-cluster literature | A finite, observable-oriented intervention rather than a new kinetic-limit theorem |
| Collision multigraph | Common MD bookkeeping | Timestamped multigraph retains repeated events and supports a registered \((\Lambda,\Gamma)\) intervention |
| T-dynamics-inspired surgery | Deng–Hani–Ma proof framework | Explicitly distinguish finite ghost/crossing dynamics from their cutting argument and from exact EDMD |
| Pair correlation diagnostic | Kinetic theory and cumulant methods | Time-oriented incoming-pair closure defect linked to a visible reverse/forward response |
| Boltzmann–Grad sweep | Standard rarefied-gas methodology | A budget-to-observable information boundary across matched forward/reverse branches |

## The active novelty test

The paper is not novel if it merely shows a reversible trajectory, a collision
network, or an attractive animation. It needs the following causal chain:

1. a predeclared discrete \(f_{1,h}\) match at the pivot;
2. a robust future separation after marginal-preserving chaotization;
3. a \((\Lambda,\Gamma)\) budget curve that distinguishes the two futures;
4. an incoming-pair closure readout with the same direction of change;
5. a small fixed-\(N\varepsilon\) sequence that keeps the interpretation honest.

The contribution is a *counterfactual cumulant microscope* for a finite
hard-sphere system, not a new Boltzmann derivation, a new Loschmidt echo, or a
production kinetic solver.

## Deferred route: adaptive molecular–kinetic hybrid

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

## The central novelty test for the deferred route

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

## Minimum SIG/TOG package for the deferred route

A plausible full paper needs all of:

1. statistically defensible B2 gain;
2. a practical observability strategy;
3. conservative conversion;
4. a meaningful cost-quality curve;
5. two visually interpretable restored phenomena;
6. a shared renderer and strong baselines;
7. explicit failure regions.

Without items 4–6, the work is more naturally a computational physics paper.
