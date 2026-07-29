# History-Aware Molecular–Kinetic

This repository studies whether exact hard-sphere identities and collision
histories can be retained only where they add measurable value over a cheaper
kinetic representation.

## Start with the research boundary

The project is inspired by the hard-sphere-to-Boltzmann result of Deng, Hani,
and Ma, but it does not treat proof diagrams as a ready-made algorithm.

Read in this order:

1. [硬球项目研究总览（中文）](research/zh-research-overview.md)
2. [Research thesis](vision/research-thesis.md)
3. [Deng–Hani–Ma connection](research/deng-hard-sphere-connection.md)
4. [Related work](research/related-work.md)
5. [Benchmark suite](benchmarks/suite.md)
6. [Eight-week feasibility spike](roadmap/eight-week-feasibility-spike.md)
7. [Go/No-Go gates](roadmap/go-no-go-gates.md)

## Evidence ladder

```text
R0: external references are reproducible
B0: each regime is numerically trustworthy
B1: exact-versus-kinetic disagreement is measured
B2: history adds held-out predictive value
B3: conversion preserves quantities and statistics
B4: online dynamic partitioning yields a cost-quality benefit
B5: the result is legible in a shared renderer
```

A beautiful B5 video cannot repair a failed B2 hypothesis.
