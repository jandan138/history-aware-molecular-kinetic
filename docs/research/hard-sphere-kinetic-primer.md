# Hard-sphere to kinetic primer

## 1. Exact microscopic state

For \(N\) hard spheres, the exact state is:

\[
Z_N(t)=\{x_i(t),v_i(t)\}_{i=1}^N.
\]

Particles move ballistically between instantaneous elastic collisions. For equal
masses, a binary collision exchanges normal velocity components while preserving:

\[
P=\sum_i m v_i,
\qquad
E=\sum_i \frac12m|v_i|^2.
\]

Event-driven molecular dynamics predicts the next collision time, advances
exactly to that event, resolves it, invalidates affected predictions, and repeats.

## 2. One-particle kinetic state

The Boltzmann description does not retain every identity. It evolves:

\[
f(t,x,v),
\]

where \(f\,dx\,dv\) represents the expected number or probability of particles
near position \(x\) and velocity \(v\).

The equation is:

\[
\partial_t f+v\cdot\nabla_x f=Q(f,f).
\]

The transport term moves particles through space. The collision operator moves
probability mass through velocity space.

## 3. DSMC as a numerical representation

Direct Simulation Monte Carlo uses weighted simulation particles to approximate
\(f\). Transport and collisions are split in time. Collision partners are
sampled from spatial cells according to kinetic rates; they do not need to be at
geometric contact.

A DSMC particle therefore has a computational identity, but that identity is not
the persistent microscopic identity of a single molecule. Repeated DSMC pair
selection is not automatically evidence of real molecular re-collision.

## 4. Correlation and factorization

Let \(f_2(z_1,z_2)\) be a two-particle distribution. A factorized state satisfies:

\[
f_2(z_1,z_2)\approx f_1(z_1)f_1(z_2).
\]

Define the correlation error:

\[
C_2=f_2-f_1f_1.
\]

A one-particle equation is useful when the effect of discarded higher-order
correlations can be controlled. In finite simulations, however, observable error
may also arise from finite density, cells, time steps, weighting, boundaries,
rare sampling, or a mismatched kinetic equation.

## 5. Local macroscopic moments

Moments of \(f\) give:

\[
\rho=\int f\,dv,
\qquad
\rho u=\int vf\,dv,
\]

\[
\Pi=\int(v-u)(v-u)^T f\,dv,
\qquad
q=\int \tfrac12|v-u|^2(v-u)f\,dv.
\]

Density, velocity, temperature, stress, and heat flux are strong state-only
features. A history-aware method must beat baselines that already use them.

## 6. Boltzmann versus Enskog

The dilute Boltzmann equation neglects finite-size spatial correlations at
contact. At higher packing fraction, Enskog-type kinetic equations introduce
pair-correlation corrections and nonlocal collision sampling.

This matters for project interpretation:

```text
EDMD ≠ DSMC
```

may mean:

- collision-history memory matters;
- finite-density pair structure matters;
- DSMC resolution is insufficient;
- geometry and wall collisions dominate;
- sampling noise is too high;
- initial ensembles are not matched.

The discrepancy atlas must separate these possibilities.

## 7. What “molecular chaos” means here

It means approximate statistical independence of appropriate pre-collisional
particles in the kinetic limit. It does not mean deterministic chaos, sensitive
dependence, or visual disorder.

## 8. The graphics opportunity

Exact identity is expensive but visually and physically useful in selected
regions. Kinetic state is scalable but does not directly define a unique
microscopic scene. A graphics method can exploit both if it preserves physics
budgets and separates physical refinement from screen-space rendering density.
