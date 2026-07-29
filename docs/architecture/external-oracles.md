# External oracles

## 1. Why process isolation

DynamO, SPARTA, and uniGasFoam are mature tools with licenses and internal data
models that differ from this project. Treating them as external executables:

- avoids accidental source/license coupling;
- preserves upstream behavior;
- makes version pinning explicit;
- allows raw-output auditing;
- prevents our core abstractions from mirroring one solver.

## 2. Adapter stages

```text
canonical case
  -> upstream case generator
  -> external executable/container
  -> immutable raw output
  -> canonical converter
  -> metric audit
```

Each stage has its own version and logs.

## 3. DynamO adapter

Primary use:

- equilibrium hard spheres;
- event counts and pressure/temperature;
- radial distribution \(g(r)\);
- exact trajectory/collision-history reference where available;
- visual smoke checks through upstream tools.

The adapter must not assume that every upstream output plugin is enabled or that
reduced units equal SI units.

## 4. SPARTA adapter

Primary use:

- free-molecular and collisional boxes;
- flow around simple surfaces;
- DSMC collision rates and moments;
- grid/surface/particle output;
- CPU/GPU reference scaling where reproducible.

The first adapter targets documented benchmark inputs rather than custom hero
scenes.

## 5. uniGasFoam adapter

Primary use:

- pure DSMC, USP/SP, and hybrid comparison;
- state-based adaptive masks;
- transient expansion and other published/tutorial cases;
- strongest existing particle-based adaptive baseline.

OpenFOAM environment details are part of provenance.

## 6. Raw-output policy

Raw upstream output is never overwritten by the converter. The converter writes
to a separate canonical directory and stores raw hashes.

## 7. Oracle disagreement

External software is a reference implementation, not mathematical truth.
When two references disagree, the report must retain both results and investigate:

- model differences;
- units and normalization;
- discretization/resolution;
- sampling uncertainty;
- boundary conditions;
- version changes.
