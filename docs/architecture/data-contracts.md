# Data contracts

## 1. Principles

Artifacts are:

- schema-versioned;
- immutable after a run closes;
- content-hashed;
- self-describing in units and normalization;
- separated into compact metadata and large array payloads;
- independent of renderer and backend-private memory layout.

## 2. Benchmark case

`benchmark-case.schema.json` declares physics, domain, species, initial ensemble,
methods, sampling, outputs, and acceptance criteria.

A frozen case may not change semantics under the same ID.

## 3. Run manifest

The run manifest records:

- repository commit and dirty state;
- case hash and method;
- executable/container hashes;
- upstream source revisions;
- host, CPU, GPU, memory, compiler, and libraries;
- parameters and random streams;
- artifact paths and hashes;
- terminal run status.

## 4. Particle bundle

Large arrays are stored in HDF5/Zarr/NPZ or another declared container. Metadata
must define:

```text
position convention and units
velocity convention and units
species, mass, radius, weight
particle identity semantics
owning versus ghost/probe/render samples
time and domain transform
array shapes and dtypes
```

## 5. Collision log

The row schema captures pre/post velocities and particle IDs. Production logs may
use a columnar binary format, but must be losslessly convertible to the canonical
schema for selected windows.

For DSMC, a stochastic collision log must be labeled `kinetic_collision`; it is
not merged with true `geometric_collision` history.

## 6. Block-state bundle

Block summaries include state moments, sampling counts, normalization, and
uncertainty. A zero sample count is distinct from physical zero.

## 7. History-feature bundle

Each feature row records:

- time window;
- feature definition version;
- block ID;
- value;
- visibility class;
- exact/probe/coarse source;
- estimator uncertainty and sketch parameters.

## 8. Discrepancy dataset

A discrepancy row joins:

```text
case + seed + block + time
state features
history/probe features
feature visibility
exact target observables
kinetic target observables
discrepancy targets
split group identifiers
```

Train/test group identifiers are created before model fitting.

## 9. Partition mask

A time-indexed block map contains representation, score, decision reason,
thresholds, cooldown state, and feature-policy hash.

## 10. Conversion report

The conversion report is the authoritative ledger for representation changes.
Global conservation accounting references its ID.

## 11. Metrics report

A metric row includes:

- name and version;
- scalar or aggregate value;
- units;
- aggregation axis;
- confidence interval or bootstrap method;
- valid sample count;
- exclusions and reason;
- threshold pass/fail.

## 12. Units

Internal native solvers may use reduced units. Canonical artifacts must either:

1. use SI units; or
2. include the complete reduced-unit scale and conversion.

Adapters may not guess units from filenames or tutorial defaults.


### 2.5 Visualization plane

The shared renderer consumes particle, field, partition, history, geometry, conversion, and metric artifacts. It may vary draw density and camera, but it cannot modify the physics partition.

Render inputs and provenance are themselves versioned:

- `render-config.schema.json` defines mode, frame schedule, camera paths, layers, display policy, comparison lock, postprocess, and evidence requirements;
- `render-manifest.schema.json` records renderer identity, input hashes,
  camera/display/comparison hashes, frame schedule, output specification, shot
  IDs, and optional case/run/claim/metric evidence links. Frozen B5 primary
  renders require those links to be complete.

A camera or display-policy change must never mutate B0–B4 artifacts. Statistical display particles have display ownership only and cannot enter physical metrics or collision history.
