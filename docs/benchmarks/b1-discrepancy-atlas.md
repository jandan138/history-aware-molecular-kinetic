# B1 — Exact–kinetic discrepancy atlas

## 1. Question

Where do exact hard-sphere dynamics and a selected kinetic model disagree, in
which observables, and over what prediction horizon?

B1 does not yet train an adaptive policy.

## 2. Matched physical definitions

Pairing EDMD and DSMC requires matching:

- dimension and domain;
- sphere diameter, mass, and species;
- number density and packing fraction;
- initial one-particle distribution;
- wall collision model;
- observation windows;
- reduced/SI unit conversion;
- ensemble interpretation.

One EDMD microstate is not paired to one DSMC realization as a deterministic
trajectory. The comparison is statistical.

## 3. Parameter axes

Sweep at least:

- packing fraction \(\phi\);
- mean free path / Knudsen regime;
- particle count and DSMC weight;
- DSMC cell size and time step;
- velocity anisotropy;
- wall distance and confinement;
- transient strength;
- geometry topology;
- prediction horizon;
- elastic versus optional weakly inelastic extension only after the elastic core.

## 4. Canonical scene families

### Homogeneous relaxation

Separates velocity-space kinetics from geometry.

### Two-color mixing

Tests transport and species concentration without adding chemistry.

### Narrow cavity

Encourages wall returns and confined collision patterns.

### Correlation labyrinth

Contains matched state regions with different path topology and re-encounter
opportunity.

### Moving-wall shear

Tests anisotropic stress and collision statistics.

### Transient expansion

Moves through collisional, transitional, and ballistic behavior.

## 5. Observable targets

No single scalar defines model error. Record:

- density, mean velocity, and temperature;
- pressure/stress tensor;
- heat flux;
- velocity-distribution distances;
- species concentration;
- collision rate and inter-collision time;
- radial distribution and contact value;
- velocity autocorrelation / transport proxy where feasible;
- surface force;
- future-horizon field error.

## 6. Discrepancy targets

For block \(B\), target examples include:

\[
e_\rho(B),\ e_u(B),\ e_T(B),\ e_\Pi(B),\ e_q(B),
\ D(f^{\mathrm{EDMD}}_B,f^{\mathrm{kin}}_B),\ e_{g(r)}(B).
\]

A composite score may be used for control only after all components remain
available in reports.

## 7. Attribution matrix

Each disagreement is tested against:

```text
physical-model axis:
  Boltzmann vs Enskog vs exact

numerical axis:
  cell size, time step, weight, particle count

sampling axis:
  ensemble size, averaging window

geometry axis:
  walls, confinement, moving boundary

history axis:
  repeated/reconnected collision structure
```

## 8. Dataset splitting

Random row splits are prohibited. Use grouped splits such as:

- leave-one-geometry-family-out;
- leave-one-packing-fraction-band-out;
- leave-one-transient-type-out;
- disjoint seed families;
- train early horizons, test later horizon only as an explicit extrapolation task.

## 9. Exit gate

B1 passes when:

- reference convergence is documented;
- stochastic confidence intervals are stable;
- discrepancy targets have nontrivial dynamic range;
- at least one case separates candidate explanations;
- exact and kinetic data join without hidden normalization choices;
- model-not-applicable regimes are labeled rather than scored as ordinary error.
