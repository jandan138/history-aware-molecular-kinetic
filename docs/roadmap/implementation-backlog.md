# Initial Implementation Backlog

## INFRA

- **INFRA-001** Add run-manifest writer and host provenance.
- **INFRA-002** Add benchmark-case validation CLI.
- **INFRA-003** Add artifact hashing and immutable run close.
- **INFRA-004** Add external executable discovery without auto-download.
- **INFRA-005** Add grouped experiment registry and split manifests.

## R0-DYNAMO

- **DYN-001** Generate pinned upstream install instructions.
- **DYN-002** Reproduce official hard-sphere tutorial.
- **DYN-003** Parse temperature/pressure/collision outputs.
- **DYN-004** Convert radial distribution output.
- **DYN-005** Freeze dilute and anisotropic candidate cases.

## R0-SPARTA

- **SPA-001** Reproduce free box.
- **SPA-002** Reproduce collisional box.
- **SPA-003** Reproduce simple surface/sphere case.
- **SPA-004** Convert particle/grid/surface data.
- **SPA-005** Record DSMC resolution and sampling parameters.

## R0-UNIGAS

- **UNI-001** Pin OpenFOAM/uniGasFoam environment.
- **UNI-002** Run pure DSMC and USP/SP modes.
- **UNI-003** Export hybrid decomposition mask.
- **UNI-004** Reproduce transient expansion case.

## B0-EDMD

- **EDMD-001** Analytic two-body event.
- **EDMD-002** Periodic/reflection boundaries.
- **EDMD-003** Event invalidation.
- **EDMD-004** Collision log and checkpoint.
- **EDMD-005** Equilibrium convergence.

## B0-DSMC

- **DSMC-001** Ballistic transport.
- **DSMC-002** Cell collision sampling.
- **DSMC-003** Seeded random streams.
- **DSMC-004** Moment accumulation.
- **DSMC-005** Homogeneous relaxation comparison.

## HISTORY

- **HIST-001** Exact rolling graph reference.
- **HIST-002** Repeated-pair and component features.
- **HIST-003** Lineage and re-merging definitions.
- **HIST-004** Low-rank pair/C2 proxy candidates.
- **HIST-005** Visibility metadata and leakage test.

## B1/B2

- **DATA-001** Paired ensemble generator.
- **DATA-002** Canonical discrepancy targets.
- **DATA-003** Geometry/regime grouped splits.
- **DATA-004** State-only baseline suite.
- **DATA-005** Enskog attribution baseline.
- **DATA-006** Incremental-value report.
- **PROBE-001** Short exact shadow probe.

## B3

- **CONV-001** Exact-to-kinetic weighted resampling.
- **CONV-002** Momentum/energy correction.
- **CONV-003** Secondary-statistic audit.
- **CONV-004** Exclusion-aware promotion.
- **CONV-005** History maturity and warm-up.
- **CONV-006** Static interface flux.

## B4

- **LOD-001** Block representation state machine.
- **LOD-002** Promotion/demotion hysteresis and cooldown.
- **LOD-003** Exact-region budget and priority scheduler.
- **LOD-004** Shadow-probe scheduler and uncertainty.
- **LOD-005** Moving interface/buffer treatment.
- **LOD-006** State-only, practical, oracle-upper-bound policies.
- **LOD-007** Failure indicator and safe fallback.
- **LOD-008** Cost-quality/exact-fraction sweep.

## B5 and visual production

The detailed issue-ready track is in
[Demo Production Backlog](demo-production-backlog.md). Major groups:

- **RENDER-001–007** render contracts, manifests, hashes, comparison audit;
- **VIEW-001–009** artifact replay and diagnostic viewer;
- **SHARED-001–008** shared scientific renderer;
- **ZOOM-001–007** conversion/zoom temporal continuity;
- **SCENE-ZM-*** Zoomable Mixing;
- **SCENE-CL-*** Correlation Labyrinth;
- **SCENE-EV-*** Expansion into Vacuum;
- **VIDEO-001–009** teaser, full video, failure reel, provenance.

### Gate dependencies

- V0/VIEW can start with M1 artifacts.
- Shared comparison requires artifact joins from M3.
- Zoom/conversion production requires G4.
- Correlation Labyrinth hero polish requires G3.
- Expansion flagship polish requires G5 and neutral visible physics.
- Final teaser and art polish require G6.

## Explicitly deferred beyond the first paper

- production path tracer;
- complex 3D CAD asset pipeline;
- combustion/chemistry;
- general rigid-body coupling;
- interactive artist editor;
- VR/game integration;
- artist-authored plume turbulence.
