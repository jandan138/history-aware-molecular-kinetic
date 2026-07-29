# Feasibility assessment

## High-confidence components

### External references

DynamO, SPARTA, and uniGasFoam provide mature starting points for exact,
stochastic kinetic, and state-adaptive reference behavior.

### Minimal two-dimensional EDMD

Equal-radius elastic hard disks with periodic/reflective boundaries are a
well-bounded implementation target and easy to inspect event by event.

### Collision-log analytics

Repeated pairs, graph components, circuit rank, lineage summaries, and pair
statistics can be computed offline before any GPU optimization.

### Conservation auditing

Mass, momentum, and energy budgets are straightforward to define and can be
made machine-readable from the first conversion prototype.

## Medium-risk components

### Exact-to-kinetic demotion

Primary invariants are manageable, but stress, heat flux, anisotropy, particle
weights, and pair structure require careful resampling.

### Kinetic-to-exact promotion

Excluded-volume placement and moment correction are feasible, but local
transients, overlap-free initialization, interface consistency, and history
warm-up are substantial research tasks.

### Dynamic partitioning

Hysteresis and buffers are standard tools; the hard part is an indicator that is
available in coarse regions and predicts future error rather than current oracle
history.

## Highest scientific risk

The history hypothesis itself may be false or redundant. Exact-versus-DSMC
error may be explained almost entirely by finite-density structure, state moments,
geometry, or numerical resolution.

This is why the first major deliverable is a grouped held-out prediction study,
not a dynamic renderer.

## Demo feasibility

The graphics workload is much lighter than a water-surface project:

- particles can be instanced;
- coarse state can be rendered as density/temperature volume;
- partitions and collision graphs are direct diagnostics;
- no free-surface reconstruction, foam, spray, or caustics are required.

However, a particle cloud is not automatically a SIG demo. The scene must expose
a physical discrepancy that viewers can understand.
