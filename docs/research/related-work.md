# Related work

## 1. Exact event-driven hard-sphere simulation

DynamO is the primary external EDMD reference. It is an open-source event-driven
particle simulator with hard-sphere models, large-system support, analysis
plugins, and visualization. Its official hard-sphere tutorial and radial
distribution output provide convenient reproducible reference cases.

DynamO occupies the “exact microscopic oracle” role. We do not copy its GPLv3
source into the Apache core.

## 2. Direct Simulation Monte Carlo

SPARTA is the primary Boltzmann/DSMC reference. It provides parallel DSMC,
Cartesian grids, embedded surfaces, standard benchmark inputs, post-processing,
Python support, and Kokkos acceleration paths.

SPARTA occupies the “mature stochastic kinetic oracle” role. Our first DSMC
implementation must reproduce selected SPARTA results before it becomes an
adaptive backend.

## 3. Existing adaptive rarefied-gas methods

uniGasFoam couples DSMC with stochastic particle and unified stochastic particle
models inside OpenFOAM. It is an especially important baseline because it avoids
a conventional particle/continuum interface and includes adaptive algorithms and
published validation cases.

Other multiscale approaches include DSMC–CFD hybrids, unified gas-kinetic
wave-particle methods, adaptive velocity-space methods, and stochastic
particle/continuum couplings. Consequently, “adaptive rarefied gas solver” is not
itself a novel claim.

## 4. Prior EDMD–DSMC hybrid

Donev, Garcia, and Alder proposed stochastic event-driven molecular dynamics,
using EDMD for polymer/solvent hard interactions and DSMC for solvent–solvent
collisions. It achieved substantial efficiency relative to full molecular
dynamics in the studied setting.

Therefore we must not claim the first EDMD–DSMC hybrid. Our distinction is:

- the same gas can change representation spatially and temporally;
- refinement is tied to predicted model discrepancy;
- collision-history information is tested against strong state-only controls;
- conversion and zoomable graphics are primary research problems.

## 5. Finite-density kinetic models

Enskog particle schemes extend DSMC-like methods to dense hard-sphere gases and
can preserve momentum and energy. Dense or strongly confined cases may reveal
Boltzmann-model error rather than a need for exact identities. An Enskog baseline
is therefore mandatory before attributing discrepancy to history.

## 6. Kinetic fluid simulation in graphics

Continuous-scale kinetic fluid simulation and HOME-LBM demonstrate that kinetic
representations can produce high-quality graphics and exploit GPU hardware.
Their target is primarily incompressible continuum flow via lattice Boltzmann
models, not exact hard-sphere identity or molecular collision correlation.

They set a visual and systems standard but are not molecular ground truth.

## 7. Particle adaptivity and LOD in graphics

Graphics has extensive literature on adaptive particles, SPH resolution,
multiresolution fluids, model reduction, and temporally coherent detail. These
works establish that:

- conversion artifacts are a first-class problem;
- screen-space and physics adaptivity should be separated;
- a cost-quality curve and stable transitions matter more than maximum particle
  count;
- a compelling video requires diagnostic clarity, not just more particles.

## 8. Collision statistics and correlations

Molecular-dynamics studies compare hard-sphere systems with DSMC/Enskog models
using velocity distributions, stress, collision rates, inter-collision times,
radial distribution, autocorrelation, and transport coefficients. These metrics
inform B1 and prevent the indicator from being trained on a single arbitrary
scalar error.

## 9. Novelty gap

We found adjacent work in every component:

```text
EDMD                    yes
DSMC                    yes
EDMD–DSMC coupling      yes
adaptive kinetic flow   yes
finite-density kinetic  yes
GPU kinetic graphics    yes
particle LOD            yes
```

The plausible gap is the complete evidence chain:

```text
paired exact/kinetic discrepancy atlas
+ incremental history-value test
+ runtime-observable/probe-aware indicator
+ conservative bidirectional conversion
+ stable dynamic molecular LOD
+ shared-renderer graphics evidence
```

The project must earn this gap experimentally.
