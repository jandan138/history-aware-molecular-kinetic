# Molecular Time Machine / History-Aware Molecular–Kinetic

The active project makes individual hard-sphere collisions addressable: rewind to
one event, edit it physically, reuse unaffected history, and recompute its exact
causal future.

## Current route

The Phase-I scalar-history predictor did not support the original dynamic-LOD claim.
That negative result is preserved; conversion and online exact/kinetic partitioning
are deferred.

The active paper route is:

> **One Collision, Two Worlds: Causal Rewind for Molecular Animation**

Read the initial pivot in
[ADR 0009](decisions/0009-pivot-to-molecular-echoes-sig.md) and the sharpened
story decision in
[ADR 0010](decisions/0010-molecular-time-machine-paper-spine.md).

E1 passed its scoped same-resolved-present phenomenon gate. E2 then returned
`stop_e2`: collision budget grades reverse recovery, but structured molecule wiring
does not beat the registered controls. That becomes the paper's turn—“a slider is
not a history”—rather than a reason to add more E2 experiments. E3 freezes one
collision, one one-degree edit, and one exact branch/full comparison. See the
[E3 recipe](benchmarks/molecular-time-machine-e3-preregistration.md).

The frozen E3 run returned `go`: one one-degree edit produces a `0.188218`
terminal color gap and changes `33/128` terminal particle positions. The causal
branch matches all `106` full-resimulation collision pairs, reuses `79/105`
baseline events, and peaks at `33/128` affected particles. See the
[E3 result](benchmarks/molecular-time-machine-e3-result.md).

E4 returned `go`: the creator selects four particles forming the recovered E's
upper stroke, baseline ancestry recommends collision #4, and the saved `−1°` branch
changes `2/4` target particles while only `1/8` other foreground particles leave the
E. Its 12 exact previews have a `0.074740 s` median, the saved branch reuses
`79/103` baseline collisions, and all `100/100` collision pairs agree with the
complete reference. See the [E4 result](benchmarks/molecular-time-machine-e4-result.md).

## Read in this order

1. [从 GAMES103 与流体入门到 Molecular–Kinetic Simulation](learning/from-games103-to-history-aware-molecular-kinetic.md)
2. [中文研究总览](research/zh-research-overview.md)
3. [Research thesis](vision/research-thesis.md)
4. [Molecular Time Machine route](research/molecular-time-machine-route.md)
5. [E3 frozen recipe](benchmarks/molecular-time-machine-e3-preregistration.md)
6. [E3 result](benchmarks/molecular-time-machine-e3-result.md)
7. [E4 frozen recipe](benchmarks/molecular-time-machine-e4-preregistration.md)
8. [E4 result](benchmarks/molecular-time-machine-e4-result.md)
9. [Deng–Hani–Ma connection](research/deng-hard-sphere-connection.md)
10. [Paper positioning](vision/paper-positioning.md)
11. [Venue strategy](vision/venue-strategy.md)
12. [Active E0–E6 suite](benchmarks/echo-branching-suite.md)
13. [Graph and branching architecture](architecture/collision-history-graph-and-branching.md)
14. [First stage](roadmap/molecular-echo-first-stage.md)
15. [Go/No-Go gates](roadmap/go-no-go-gates.md)
16. [Hero scenes](demos/hero-scenes.md)

## Scientific and graphics bridge

```text
Deng–Hani–Ma:
  cumulants + complete collision histories + collision-history molecules
  explain what must be controlled in the hard-sphere → Boltzmann derivation

This project:
  collision causal graph + replay + branch + correlation surgery
  turns hidden history into a graphics and animation tool
```

The theorem motivates the information boundary. It does not guarantee the finite
branching algorithm, and the proof cutting argument is not implemented as a
simulator.

## Active evidence ladder

```text
E0 exact reversal and deterministic replay
→ E1 same resolved present / opposite futures
→ E2 collision-molecule mechanism and null controls [closed negative]
→ E3 addressable collision + exact causal branch + One Collision, Two Worlds
→ E4 causal steering: select a future feature, find its past cause, direct a branch
→ E5 correlation surgery and future authoring
→ E6 SIG graphics evidence
```

A beautiful reverse movie is not the method, and a decorative graph cannot replace
E3 branch correctness.

## Active visual production

```text
V0 event/replay viewer
→ V1 scientific echo prototype
→ V2 history-budget microscope
→ V3 One Collision, Two Worlds
→ V4 Choose the Cause, Direct the Future
→ V5 deferred geometry/correlation surgery
→ V6 SIG production and evidence release
```

Read:

1. [Visual Production Roadmap](demos/visual-production-roadmap.md)
2. [Art Direction](demos/art-direction.md)
3. [Storyboard](demos/storyboard.md)
4. [Visual Acceptance Criteria](demos/visual-acceptance-criteria.md)
5. [Claim-to-Visual Evidence](demos/claim-to-visual-evidence.md)
6. [Molecular Echoes Backlog](roadmap/molecular-echoes-backlog.md)

## Venue

The first target is SIGGRAPH / SIGGRAPH Asia. IEEE VIS is a fallback only after a
real pivot to linked visual analytics of event graphs, branch provenance, causal
cones, and uncertainty.

See [Venue Strategy](vision/venue-strategy.md).

## Deferred infrastructure

The older R0–B5 exact/kinetic LOD documents, schemas, and adapters remain available
for reproducibility and future work. Their old claims and Hero Scenes are not active
paper evidence.
