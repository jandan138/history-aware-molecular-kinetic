# Research thesis

## 1. Core problem

An exact hard-sphere system stores the identity, position, velocity, and collision
history of every particle. A Boltzmann or DSMC representation stores a much
cheaper approximation to the one-particle phase-space distribution:

\[
f(x,v,t).
\]

The exact system can reproduce re-encounters, collision chains, excluded-volume
structure, and other correlations. The kinetic model intentionally discards much
of that information to gain scale.

The central question is not simply “which solver is more accurate?” It is:

> Can we identify, online and locally, where the information discarded by the
> kinetic representation materially changes observables that matter to a
> scientific or graphics application?

## 2. Proposed state decomposition

The runtime domain is decomposed into blocks. Each block owns one physical
representation at a time:

### Exact hard-sphere state

\[
\mathcal X_B(t)=\{x_i(t),v_i(t),r_i,m_i,\mathrm{id}_i\}_{i\in B}
\]

plus a finite collision-history window. It is used where particle identity,
geometry-exact collisions, or correlation memory is required.

### Boltzmann/DSMC state

A weighted set of stochastic superparticles approximates:

\[
f_B(x,v,t).
\]

Collisions are sampled statistically within cells. A superparticle is not the
persistent identity of one real molecule.

### Finite-density kinetic state

When packing and pair structure matter, a Boltzmann DSMC backend may be the wrong
coarse model. The architecture therefore admits Enskog-like or other non-ideal
particle schemes.

### Shadow probe state

A sparse, short-lived exact micro-simulation can be spawned from a coarse block
to estimate local model error or correlation growth without refining the entire
region.

## 3. Primary scientific hypothesis

Let \(e_B\) be a local discrepancy between exact hard-sphere and kinetic
predictions, measured over a finite future horizon and a fixed observable set.
Let \(s_B\) contain state-only features:

\[
s_B=(\rho,\phi,T,u,\mathrm{Kn}_{GLL},R_M,\|\Pi\|,\|q\|,\text{geometry}).
\]

Let \(h_B\) contain collision-history features:

\[
h_B=(r_{\mathrm{repeat}},\beta_1(G),d_{\mathrm{lineage}},
|C_2|_{\mathrm{proxy}},\ldots).
\]

The project tests whether:

\[
\mathbb E[\ell(e_B,\hat e(s_B,h_B))]
<
\mathbb E[\ell(e_B,\hat e(s_B))]
\]

on held-out geometries, densities, and transients—not merely on randomly split
samples from the same run.

This is a prediction question before it becomes an adaptive simulation method.

## 4. Why this could be a graphics contribution

A successful system would provide:

1. **physics-driven molecular LOD** rather than camera-driven particle spawning;
2. **zoomable visualization** from macroscopic fields to exact collisions;
3. **localized exactness** around complex collision history, moving geometry, or
   ballistic transitions;
4. **a shared artifact and renderer pipeline** that makes the refinement reason
   visible rather than hiding it behind smoke;
5. **a cost-quality curve** unavailable to full EDMD or uniform DSMC alone.

## 5. Proposed method contributions

### C1. Strong discrepancy benchmark

A paired EDMD–kinetic dataset that controls for state, geometry, resolution, and
sampling uncertainty.

### C2. Observable-aware history indicator

A compact streaming sketch that predicts chosen model discrepancies and labels
each feature as runtime-observable, shadow-probe, or oracle-only.

### C3. Conservative representation conversion

Demotion and promotion operators that preserve mass, momentum, and energy while
controlling stress, heat flux, velocity-distribution, pair-structure, and
warm-up errors.

### C4. Stable dynamic partitioning

Hysteresis, cooldown, interface buffers, probe scheduling, and an explicit
failure indicator.

### C5. Graphics evidence without physics contamination

A renderer that can show particles, macroscopic fields, partitions, and
collision graphs but cannot silently change the physical representation.

## 6. Crucial negative thesis

This project should be rejected or redirected if any of the following is true:

- state-only features explain the discrepancy as well as history;
- useful history features require a full exact simulation everywhere;
- correlations become visible only where Boltzmann DSMC is already the wrong
  coarse equation and an Enskog backend removes the discrepancy;
- conversion transients dominate the error saved by adaptive refinement;
- exact regions occupy almost the entire useful scene;
- the only visible benefit is a diagnostic mask rather than a physical effect.

## 7. Publication routes

The project is deliberately decomposed so failure is informative:

- B2 succeeds and B4/B5 succeed: SIGGRAPH/TOG candidate;
- B2 succeeds but graphics evidence is weak: JCP/CMAME/SISC-style numerical route;
- B2 fails but Enskog explains the gap: adaptive EDMD–Enskog route;
- online refinement fails but collision DAGs are useful: editing/replay route;
- exact regions dominate: parallel collision-history EDMD route.
