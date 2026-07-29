# Deng–Hani–Ma hard-sphere connection

## 1. The mathematical result

Deng, Hani, and Ma derive the Boltzmann equation from a rarefied Newtonian
hard-sphere system for any fixed time interval over which the corresponding
Boltzmann solution exists. This extends the classical short-time derivation.
A companion work connects the result to hydrodynamic limits for compressible
Euler and incompressible Navier–Stokes–Fourier equations in the stated setting.

The proof uses a long-time cumulant ansatz that retains memory of full collision
histories. Associated diagrams are organized as collision-history molecules and
controlled through a cutting algorithm.

Primary sources are pinned in [`references/sources.yaml`](../../references/sources.yaml).

## 2. The transferable idea

The transferable idea is a question of information:

```text
exact particle identities + collision history
                 ↓ coarse-graining
one-particle kinetic distribution
```

What correlations are discarded, when are they small, and how can their effect
be quantified?

This motivates our benchmark variables:

- repeated-pair events;
- graph circuit rank;
- component growth and re-merging;
- lineage depth and recent shared ancestors;
- low-dimensional pair-correlation or cumulant proxies.

## 3. What is not transferable without new research

### Not an online indicator

The proof's cumulants and diagrams are analytic objects in a limiting argument.
Computing a finite rolling collision graph does not inherit the theorem.

### Not a partition algorithm

The cutting algorithm establishes estimates. It does not choose GPU blocks,
convert representations, or guarantee a local error bound.

### Not evidence that history refinement is useful

In the Boltzmann–Grad limit, the theorem says the factorized description becomes
valid. The closer a numerical scene is to that regime, the less need there may be
for an exact patch.

### Not a dense-gas theorem

When finite-size pair structure is large, an Enskog model may be the correct
coarse comparison. Attributing all EDMD–DSMC discrepancy to collision history
would be scientifically wrong.

## 4. How the paper should describe the connection

Acceptable wording:

> Inspired by the distinction between factorized kinetic descriptions and the
> collision-history correlations controlled in recent hard-sphere kinetic-limit
> theory, we investigate whether compact history features predict finite-system
> model discrepancy.

Unacceptable wording:

> We turn the Deng–Hani–Ma cutting algorithm into an adaptive simulator.

or:

> The theorem guarantees our history-based LOD.

## 5. Benchmark consequence

Every history feature has a visibility label:

- `runtime_observable`: available in the actual current representation;
- `shadow_probe`: available only after a bounded exact micro-probe;
- `oracle_only`: available only from full EDMD and forbidden to the online policy.

This prevents a common research error: using exact ground-truth history to decide
where exact ground truth was needed, then reporting the result as an online method.
