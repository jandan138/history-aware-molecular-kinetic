# Demo strategy

## 1. The demo is an evidence client

The renderer consumes the same canonical artifacts used by metrics. It is not a
second simulation system and cannot contain hidden physical fixes.

## 2. Why this route is lower risk than a water demo

The first graphics layer needs only:

- sphere instancing;
- field/volume display;
- partition coloring;
- collision graph lines;
- simple transparent or cutaway geometry;
- plots and text overlays.

No free surface, foam, spray, caustics, breaking waves, or fluid-solid coupling is
required to explain the contribution.

## 3. Demo gates

### Gate D0 — Diagnostic render

A 2D/3D viewer displays exact particles, kinetic display samples, block IDs, and
collision events from recorded artifacts.

### Gate D1 — Shared comparison render

All baselines use identical camera, geometry, transfer functions, display density,
and temporal sampling.

### Gate D2 — Conversion continuity

Static promotion/demotion clips show conservation and temporal diagnostics.

### Gate D3 — Dynamic partition

Only after B4 passes, animate exact/kinetic/probe masks.

### Gate D4 — Hero polish

Add lighting, materials, captions, and final camera paths without changing
simulation data.

## 4. What not to build

Before B4:

- spacecraft asset pipeline;
- complex industrial CAD cleanup;
- path-traced smoke;
- chemistry/fire;
- full interactive editor;
- VR or real-time game integration;
- complex rigid-body coupling;
- custom production renderer.

## 5. Video grammar

Each result clip should answer in order:

1. What is the physical scene?
2. Where do full exact and coarse kinetic disagree?
3. What features trigger the proposed method?
4. What representation is active?
5. What physical error is recovered?
6. What does it cost?

A viewer should not need to infer novelty from a prettier cloud.

## 6. Camera and physics

Camera distance can change display particle count and rendering mode. It cannot
change physical representation in primary comparisons.

A separate optional perceptual policy can be studied only after the physical
policy is frozen and must be labeled clearly.

## 7. Asset budget

Hero scenes use primitives:

- box and divider;
- channels and rounded chambers;
- plate/cylinder;
- nozzle/opening;
- optional simple low-poly shell after algorithm freeze.

This keeps the demo workload proportional to the research contribution.
