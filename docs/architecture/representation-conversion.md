# Representation conversion

## 1. Conversion is a scientific operator

Conversion changes what information exists. It must therefore be benchmarked as
carefully as a PDE or collision solver.

## 2. Exact to kinetic: demotion

Input:

\[
\{x_i,v_i,m_i,r_i\}_{i\in B}
\]

Output:

- weighted kinetic particles or a backend-specific distribution sample;
- moments and collision-model state;
- a conversion report;
- optional compact correlation descriptor for diagnostics or warm start.

### Required exact constraints

At minimum:

\[
M'=M,
\qquad
P'=P,
\qquad
E'=E
\]

within declared numerical tolerance.

### Secondary targets

- stress tensor;
- heat flux;
- velocity histogram or basis coefficients;
- species fractions;
- spatial density within the block;
- radial/pair structure when supported by the coarse backend.

### Candidate algorithm

1. stratify particles in position/velocity space;
2. select or cluster weighted representatives;
3. preserve total mass by weight construction;
4. apply affine velocity correction for momentum and kinetic energy;
5. reject negative weights or invalid collision-model parameters;
6. compare secondary statistics;
7. commit ownership only after audit.

## 3. Kinetic to exact: promotion

Promotion is harder because a one-particle distribution does not determine a
unique non-overlapping microstate or collision history.

### Required steps

1. sample positions from the local density while enforcing geometry and
   hard-sphere exclusion;
2. sample velocities from the kinetic representation;
3. correct mass, momentum, and energy;
4. match stress/heat-flux targets when feasible;
5. initialize event structures;
6. use a bounded warm-up or overlap buffer;
7. measure transient relaxation before accepting the patch.

### History semantics

New exact particles begin with new identity. Invented pre-promotion collision
history is prohibited. A warm-up interval may be tagged “history immature” and
excluded from history-triggered demotion.

## 4. Interface handling

Candidate strategies:

- overlapping buffer with one physical owner;
- flux exchange across a geometric interface;
- particle handoff with weight conversion;
- stochastic reservoir boundary for exact patches;
- moving patch remap with conservative accounting.

The first prototype should prefer a simple static interface over a complex
moving patch.

## 5. Conversion report

Every conversion emits:

```text
source and target representation
block IDs and time
input/output particle counts and weights
mass/momentum/energy before and after
secondary-statistic discrepancies
placement retries and failures
warm-up duration
random seed and algorithm version
source and output artifact hashes
accept/reject decision
```

## 6. Conversion acceptance

A conversion is rejected if:

- exact conservation tolerances fail;
- overlap-free placement fails;
- secondary errors exceed case thresholds;
- a backend applicability condition fails;
- interface buffer capacity is exceeded;
- output contains non-finite values.

The controller may respond by keeping the source representation, expanding a
buffer, or marking the block not applicable.
