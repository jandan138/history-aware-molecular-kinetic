# Paper positioning

## Working title

**History-Aware Molecular LOD: Adaptive Exact–Kinetic Simulation from Collision
Correlations**

Alternative graphics title:

**Zoomable Gas: Correlation-Aware Hard-Sphere–Kinetic Simulation**

## One-paragraph story

We introduce a benchmark-driven adaptive simulator that couples exact
hard-sphere dynamics with pluggable stochastic kinetic representations. A
streaming history sketch and optional sparse exact probes estimate where a
factorized kinetic model loses observable accuracy beyond what can be explained
by traditional state-only breakdown criteria. Conservative conversion operators
move blocks between representations, while a hysteretic controller localizes
exact particle identity and collision history. The method is evaluated against
DynamO, SPARTA, uniGasFoam, full exact references, and finite-density alternatives,
and rendered through a shared zoomable visualization pipeline.

## Claims we may make only after evidence

1. History features provide statistically significant held-out predictive gain.
2. The gain persists after strong state and geometry controls.
3. Conversion preserves primary invariants and bounds secondary-statistic error.
4. Dynamic partitioning reaches a better cost-quality point than uniform methods.
5. At least two physical effects are visibly restored by localized exactness.

## Claims we must not make

- the proof cutting algorithm is implemented online;
- the theorem guarantees the adaptive method;
- any EDMD–DSMC coupling is novel by itself;
- a superparticle collision history equals a molecular collision history;
- DSMC is valid in every correlated finite-density regime;
- the method is a general replacement for CFD, MD, or granular solvers.

## Strongest reviewer questions

- Why is packing fraction or Enskog not sufficient?
- How can history be known in a coarse region?
- Does the indicator generalize to unseen geometry and transients?
- Is the benefit physical, or merely a visualization LOD?
- Does conversion create more error than it removes?
- Why is the method graphics rather than only kinetic CFD?

The benchmark suite is built around answering these questions directly.
