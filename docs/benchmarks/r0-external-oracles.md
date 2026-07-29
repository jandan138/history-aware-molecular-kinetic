# R0 — External oracles

## Goal

Establish reproducible exact, kinetic, and existing-adaptive references before
implementing a competing hybrid.

## R0-DYN — DynamO

### R0-DYN-EQUIL-v0

Reproduce the official 1372-particle hard-sphere tutorial at reduced density 0.5
and reduced temperature 1.

Record:

- upstream revision and executable hash;
- generated and equilibrated configurations;
- collision counts and wall time;
- temperature and pressure outputs;
- radial distribution \(g(r)\);
- exact command lines;
- a diagnostic particle render.

This dense equilibrium case is an adapter and finite-density sanity check, not a
Boltzmann-regime case.

### R0-DYN-DILUTE-v0

Create a dilute counterpart with the same analysis outputs and a convergence
study in particle count and sampling duration.

### R0-DYN-ANISO-v0

Initialize anisotropic velocities and measure relaxation, stress, and collision
statistics.

## R0-SPA — SPARTA

### R0-SPA-FREE-v0

Documented free-molecular box. Verify transport and boundary interactions with
collisions disabled.

### R0-SPA-COLLIDE-v0

Documented collisional box. Verify density, velocity, temperature, collision
rate, and particle-number sensitivity.

### R0-SPA-SPHERE-v0

Documented flow around a sphere or simple embedded surface. Verify force/surface
outputs and field conversion.

## R0-UNI — uniGasFoam

### R0-UNI-PURE-v0

Run pure DSMC and pure USP/SP modes on a documented tutorial case.

### R0-UNI-HYBRID-v0

Run the published hybrid mode and export the state-based decomposition mask,
macroscopic fields, particle count, and wall time.

### R0-UNI-EXPANSION-v0

Transient expansion into vacuum, chosen because the regime changes strongly in
space and time.

## Adapter acceptance

An adapter passes only if:

1. the exact upstream revision is recorded;
2. raw output is preserved and hashed;
3. canonical conversion is unit-audited;
4. at least one published/documented scalar is reproduced within tolerance;
5. repeated runs quantify stochastic variation;
6. the repository can regenerate adapter inputs without editing upstream source.

## Non-goal

R0 does not declare any external code “ground truth” across models. It establishes
reference behavior and exposes normalization differences.
