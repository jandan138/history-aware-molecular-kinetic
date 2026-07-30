# History-Aware Molecular–Kinetic

This repository studies whether exact hard-sphere identities and collision histories can be retained only where they add measurable value over a cheaper kinetic representation.

## Start with the research boundary

The project is inspired by the hard-sphere-to-Boltzmann result of Deng, Hani, and Ma, but it does not treat proof diagrams as a ready-made algorithm.

Read in this order:

1. [从 GAMES103 与流体入门到 History-Aware Molecular–Kinetic Simulation](learning/from-games103-to-history-aware-molecular-kinetic.md)
2. [硬球项目研究总览（中文）](research/zh-research-overview.md)
3. [Research thesis](vision/research-thesis.md)
4. [Deng–Hani–Ma connection](research/deng-hard-sphere-connection.md)
5. [Related work](research/related-work.md)
6. [Benchmark suite](benchmarks/suite.md)
7. [Eight-week feasibility spike](roadmap/eight-week-feasibility-spike.md)
8. [Go/No-Go gates](roadmap/go-no-go-gates.md)
9. [SIG visual production roadmap](demos/visual-production-roadmap.md)

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

## Visual production

Rendering and final video production are a versioned evidence subsystem rather than an end-of-project polish task:

```text
V0 artifact replay viewer
→ V1 shared scientific renderer
→ V2 conversion/zoom prototype
→ V3 Expansion-into-Vacuum flagship prototype
→ V4 final three-scene production
→ V5 evidence packaging and release
```

Read:

1. [Visual Production Roadmap](demos/visual-production-roadmap.md)
2. [Art Direction](demos/art-direction.md)
3. [Storyboard](demos/storyboard.md)
4. [Visual Acceptance Criteria](demos/visual-acceptance-criteria.md)
5. [Claim-to-Visual Evidence Matrix](demos/claim-to-visual-evidence.md)
6. [Hero Scene Specifications](demos/scene-specs/README.md)
7. [Demo Production Backlog](roadmap/demo-production-backlog.md)

A polished video cannot bypass B2 history validation, B3 conversion, or B4 dynamic-benefit gates.
