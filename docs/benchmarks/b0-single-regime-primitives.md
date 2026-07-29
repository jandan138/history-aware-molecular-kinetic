# B0 — Single-regime primitives

## B0-EDMD

### Elastic two-body collision

Verify collision time, contact geometry, momentum, and energy against an analytic
pair collision.

### Periodic free flight

Verify ballistic motion and periodic wrapping without collisions.

### Multi-particle event invalidation

Construct simultaneous/near-simultaneous events that invalidate queued
predictions. Verify deterministic tie policy and absence of overlap.

### Equilibrium hard disks/spheres

Compare temperature, pressure, collision rate, and \(g(r)\) to DynamO or theory
in selected regimes.

### Event-log integrity

Every collision must have:

- nondecreasing time;
- distinct valid particle IDs;
- pre/post state consistent with the owning checkpoint;
- local momentum/energy conservation;
- no double resolution.

## B0-DSMC

### Free transport

Disable collisions and compare with analytic advection.

### Homogeneous relaxation

Start from a non-Maxwellian velocity distribution and compare relaxation trends
with SPARTA/reference output.

### Equilibrium sampling

Measure moment bias and variance versus particle weight, cell size, time step,
and sampling duration.

### Boundary interaction

Verify specular/diffuse wall models independently.

## B0-Enskog

Before any finite-density backend enters B1:

- verify equilibrium wall density or another published reference;
- verify momentum and energy conservation;
- document pair-correlation closure;
- distinguish the modeled contact value from measured exact \(g(r)\).

## B0-history

The rolling graph correctness reference receives hand-constructed event streams:

- tree: circuit rank 0;
- triangle: circuit rank 1;
- repeated pair: ratio known exactly;
- disconnected components;
- window expiry;
- particle-ID recycling rejection.

## Exit gate

No B1 model comparison begins until each participating backend has a resolution
and sampling envelope in the target parameter range.
