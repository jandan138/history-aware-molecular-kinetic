# Scope and non-goals

## In scope for the first paper

- elastic equal- or few-species hard disks/spheres;
- two dimensions for the feasibility spike, three dimensions after B2;
- event-driven exact reference dynamics;
- Boltzmann DSMC as the first coarse backend;
- Enskog-compatible interfaces and selected finite-density references;
- local state and collision-history features;
- exact-to-kinetic demotion before full bidirectional conversion;
- simple reflective/moving geometry;
- instanced-particle, volume, partition, and graph visualization;
- conservative and statistically audited conversion;
- reproducible external reference adapters.

## Explicit non-goals for the first paper

- dense frictional sand, static friction, jamming, or force chains;
- chemically reacting gas, combustion, plasma, or radiation;
- arbitrary soft potentials;
- full Navier–Stokes continuum coupling;
- movie-quality smoke art direction;
- automatic theorem transfer from Deng–Hani–Ma to the algorithm;
- exact high-dimensional cumulant storage;
- claiming the first EDMD–DSMC hybrid;
- using camera distance as the only physical refinement signal;
- complex spacecraft, engines, or six-degree-of-freedom hero assets before B4.

## Model-domain language

Use “hard-sphere gas” only for elastic collision models covered by the stated
assumptions. Use “dilute granular gas” only when restitution or granular physics
is explicitly introduced. Do not use “sand” as a visual synonym for hard spheres.
