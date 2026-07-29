# Eight-week feasibility spike

## Purpose

Answer the scientific kill question before building a dynamic LOD system:

> Does collision history add held-out predictive value beyond state, geometry,
> finite-density models, and numerical controls?

## Week 1 — DynamO reference

- pin and build/install DynamO externally;
- reproduce official hard-sphere tutorial;
- export temperature, pressure, event counts, and \(g(r)\);
- preserve raw outputs and command manifest;
- generate a diagnostic particle clip.

**Deliverable:** `R0-DYN-EQUIL-v0` candidate report.

## Week 2 — SPARTA and uniGasFoam references

- reproduce SPARTA free and collisional boxes;
- generate field/particle diagnostics;
- run one uniGasFoam pure/hybrid tutorial;
- document normalization and environment cost.

**Deliverable:** R0 adapter smoke matrix.

## Week 3 — Minimal 2D EDMD

Support only:

- equal-radius elastic disks;
- periodic and reflective boundaries;
- event queue and invalidation;
- collision log;
- checkpoints and deterministic seeds.

Validate analytic pair events and conservation.

## Week 4 — Minimal 2D DSMC

Support:

- ballistic transport;
- fixed cells;
- hard-sphere collision sampling;
- periodic/reflective boundary models;
- state moments and seeded random streams.

Match low-density equilibrium/relaxation behavior.

## Week 5 — Paired dataset

Run small versions of:

- homogeneous relaxation;
- two-color mixing;
- narrow cavity;
- correlation labyrinth;
- moving-wall shear if time permits.

Extract state, exact history, pair statistics, and discrepancy targets.

## Week 6 — Kill experiment

Fit/evaluate:

```text
S0: density + packing
S1: S0 + Kn_GLL + collision rate
S2: S1 + Maxwellian residual + stress + heat flux + geometry
S3: S2 + finite-density/Enskog controls
H-oracle: S3 + exact history
```

Use grouped geometry/regime splits and report confidence intervals.

**Primary decision:** does `H-oracle` materially beat `S3`?

## Week 7 — Practical observability

If oracle history helps:

- test short shadow EDMD probes;
- measure probe cost and uncertainty;
- test whether a practical feature set retains useful gain;
- create an oracle static partition upper bound.

If oracle history does not help, investigate attribution rather than continuing
hybrid engineering.

## Week 8 — Static demotion and decision report

Implement exact-to-kinetic demotion only. Audit mass, momentum, energy, stress,
and downstream transient.

Write one of four decisions:

1. proceed to full history-aware LOD;
2. pivot to EDMD–Enskog;
3. pivot to probe-based error estimation;
4. stop and preserve the benchmark platform.

## Resource rule

No production renderer, GPU optimization, complex asset, or bidirectional dynamic
partition is allowed during this spike.
