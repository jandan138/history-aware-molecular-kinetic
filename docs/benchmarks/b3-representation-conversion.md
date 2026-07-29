# B3 — Representation conversion

## 1. Separate conversion from policy

B3 uses predeclared static blocks and conversion times. No adaptive indicator is
active. This isolates conversion error.

## 2. B3-D — Exact to kinetic demotion

### Cases

- equilibrium dilute gas;
- anisotropic velocity distribution;
- two-species mixture;
- spatial density gradient;
- confined block near wall;
- finite-density case with DSMC and Enskog targets.

### Metrics

Exact requirements:

\[
\epsilon_M,\quad \epsilon_P,\quad \epsilon_E.
\]

Secondary metrics:

- stress and heat flux error;
- velocity histogram/divergence;
- species and spatial distribution;
- collision-rate transient after demotion;
- pair-structure loss;
- downstream field error after a fixed horizon;
- compression ratio and conversion time.

### Baselines

- independent moment-matched resampling;
- random thinning with weight adjustment;
- velocity-space clustering;
- proposed structured/pair-aware conversion.

## 3. B3-P — Kinetic to exact promotion

### Cases

- dilute Maxwellian;
- anisotropic non-Maxwellian;
- near-wall block;
- moving interface;
- finite-density block.

### Metrics

- overlap and geometry violations;
- mass/momentum/energy error;
- stress/heat-flux mismatch;
- \(g(r)\) and contact behavior after warm-up;
- collision burst after initialization;
- relaxation time to exact reference envelope;
- particle popping / temporal image difference under fixed renderer;
- placement cost and failure rate.

### Baselines

- independent uniform positions + velocity sampling;
- Poisson-disk/exclusion placement;
- moment-corrected placement;
- proposed backend-aware structured promotion.

## 4. Interface flux

A static split-domain test measures:

- particle/mass flux across the interface;
- momentum and energy flux;
- reflection artifacts;
- interface density and temperature bias;
- repeated crossings and weight conversion;
- buffer-width sensitivity.

## 5. History maturity

Promoted blocks are tagged with an age. History-based demotion is disabled until:

- a minimum physical time or collision count passes;
- initialization transients fall below threshold;
- the history window contains enough real exact events.

## 6. Exit gate

B3 passes when:

- primary conservation meets fixed tolerances;
- secondary error is below downstream solver/reference error in target regimes;
- no invalid overlap exists;
- warm-up cost is bounded;
- interface bias converges with buffer/resolution;
- conversion reports fully explain all state changes.
