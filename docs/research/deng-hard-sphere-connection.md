# Deng–Hani–Ma hard-sphere connection

## 1. The mathematical result

Deng, Hani, and Ma derive the Boltzmann equation from a rarefied Newtonian
hard-sphere system for long times under stated assumptions. The proof uses a
long-time cumulant ansatz that retains full collision histories; the associated
diagrams are organized as collision-history molecules and controlled with both
T-dynamics and a cutting argument. A companion work connects this program to
hydrodynamic limits in its stated setting.

Primary sources and explicit non-claims are pinned in the repository file
references/sources.yaml.

## 2. Transferable idea: a finite-system correlation microscope

The transferable idea is a question of information:

\[
\text{particle identities and correlated collision history}
\quad\longrightarrow\quad
\text{one-particle kinetic distribution}.
\]

What correlations are discarded by that closure, and can a controlled
intervention make their effect visible?

The active answer is **Collision-History Echoes**:

1. prepare a non-equilibrium hard-disk gas and reverse velocities at a pivot;
2. compare exact reversal with a velocity permutation that preserves a
   preregistered discrete one-particle marginal \(f_{1,h}\);
3. restrict collision connections by a finite \((\Lambda,\Gamma)\) budget;
4. measure an incoming-pair closure-defect proxy and its effect on a
   preregistered observable.

The simulator keeps a timestamped collision-event **multigraph**, with each
repeated pair event retained. This is a finite computational object for auditing
the intervention. It is not identified with the full analytic molecule of the
proof. The route is specified in
[Collision-History Echoes](collision-history-echo-route.md).

## 3. What is not transferable without new research

### Not a finite-system theorem

Computing a collision multigraph, seeing a Loschmidt echo, or measuring a
finite-\(N\) cumulant proxy does not inherit the theorem, verify its
assumptions, or produce a convergence rate.

### T-dynamics is distinct from the cutting argument

The cutting argument is a proof technique for estimates. It is not a partition,
GPU, or representation-conversion algorithm. T-dynamics is a separate modified
dynamics. A finite analogue may suppress a collision when a
\((\Lambda,\Gamma)\) budget is exhausted, but it must then explicitly adopt
ghost/crossing semantics and may permit overlaps. It is no longer an ordinary
hard-sphere EDMD trajectory.

### Not evidence for an engineering history controller

The prior proposal that compact history features predict EDMD–DSMC discrepancy
was an exploratory negative result. The new route studies a causal mechanism; it
does not establish that an online history-based LOD policy is useful.

### Not a Boltzmann counterexample or dense-gas theorem

The reversed state deliberately carries oriented many-particle correlations and
is not a new factorized initial condition for the kinetic-limit theorem.
Accordingly, an echo result is not a counterexample to Boltzmann closure. At
finite density, an Enskog-like correction may still be the relevant coarse
comparison; the route does not attribute every EDMD–DSMC discrepancy to history.

## 4. Allowed wording

Acceptable:

> Inspired by the distinction between factorized kinetic descriptions and
> collision-history correlations controlled in recent hard-sphere kinetic-limit
> theory, we construct matched resolved one-particle states with different
> correlated futures and measure the collision-molecule budget needed to
> preserve their response.

Unacceptable:

> We turn the Deng–Hani–Ma cutting algorithm into an adaptive simulator.

> The theorem guarantees our molecular-echo budget, makes velocity reversal
> novel, or proves that history-based LOD is useful.

## 5. Implementation audit boundary

- **Exact EDMD** is used for the reference/reversal branch.
- **Chaotization** may claim equality only for registered discrete
  \(f_{1,h}\), never for continuous pointwise \(f_1(x,v)\).
- **Finite T-dynamics** is labelled an extended causal intervention, never an
  exact-dynamics baseline.
- **Incoming-pair proxies** and response observables are registered before the
  curves are plotted.

These boundaries keep the theoretical inspiration useful without turning it into
an unjustified algorithmic guarantee.
