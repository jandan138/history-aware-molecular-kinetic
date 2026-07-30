# Demo Strategy

## 1. The demo is an evidence client

The renderer consumes the same canonical artifacts used by metrics. It is not a
second simulation system and cannot contain hidden physical fixes.

The complete production path is documented in
[Visual Production Roadmap](visual-production-roadmap.md). The visual language,
shot plan, acceptance gates, and per-scene contracts live in:

- [Art direction](art-direction.md)
- [Storyboard](storyboard.md)
- [Visual acceptance criteria](visual-acceptance-criteria.md)
- [Claim-to-visual evidence matrix](claim-to-visual-evidence.md)
- [Hero scene specifications](scene-specs/README.md)

---

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

The risk is therefore not primarily asset production. The risk is whether the
history-aware policy restores a **visible physical observable**, rather than only
producing a more interesting partition mask.

---

## 3. Scientific gates D0–D4

### Gate D0 — Diagnostic render

A 2D/3D viewer displays exact particles, kinetic display samples, block IDs,
canonical fields, and collision events from recorded artifacts.

### Gate D1 — Shared comparison render

All baselines use identical camera, geometry, transfer functions, display density,
frame times, and temporal filtering. A comparison-lock hash is written to the
render manifest.

### Gate D2 — Conversion continuity

Static promotion/demotion clips show conservation, secondary statistics, volume
continuity, exact identity tracks, and a frame-discontinuity diagnostic.

### Gate D3 — Dynamic partition

Only after B4 passes, animate exact/kinetic/probe masks. The camera may change
rendering LOD but cannot change physical representation.

### Gate D4 — Hero polish

Add lighting, materials, captions, shared motion blur, and final camera paths
without changing simulation data or the scientific conclusion.

---

## 4. Production gates V0–V5

The scientific gates above are mirrored by an implementation track:

```text
V0 artifact replay viewer
V1 shared scientific renderer
V2 conversion and zoom prototype
V3 Expansion-into-Vacuum flagship prototype
V4 final three-scene production
V5 evidence packaging and release
```

V0 starts during M1. Hero polish remains blocked until V3 neutral comparison
passes. See [Visual Production Roadmap](visual-production-roadmap.md).

---

## 5. What not to build

Before B4/V3:

- spacecraft asset pipeline;
- complex industrial CAD cleanup;
- path-traced smoke;
- chemistry/fire;
- full interactive editor;
- VR or real-time game integration;
- complex rigid-body coupling;
- custom production renderer;
- artist-authored plume turbulence.

The first paper uses primitive geometry and a renderer no more complex than the
claim requires.

---

## 6. Video grammar

Each result clip should answer in order:

1. What is the physical scene?
2. Where do full exact and coarse kinetic disagree?
3. What features or probes trigger the proposed method?
4. What representation is active?
5. What physical observable is recovered?
6. What does it cost?

A viewer should not need to infer novelty from a prettier cloud. Each shot ID and
its responsibility are frozen in the [Storyboard](storyboard.md).

---

## 7. Camera, display LOD, and physics LOD

Camera distance can change:

- display particle count;
- volume/particle blending;
- label density;
- diagnostic visibility.

It cannot change:

- exact/kinetic ownership;
- probe scheduling;
- promotion/demotion time;
- physical particle state;
- metric artifacts.

The camera–physics audit requires the partition artifact hash to remain unchanged
when only the camera or display policy changes.

---

## 8. Asset budget

Hero scenes use primitives:

- box and divider;
- channels and rounded chambers;
- plate/cylinder;
- nozzle/opening;
- optional simple low-poly shell after algorithm freeze.

This keeps the demo workload proportional to the research contribution.

---

## 9. Scene priorities

1. **Expansion into Vacuum** — visual flagship and teaser.
2. **Correlation Labyrinth** — scientific flagship for history value.
3. **Zoomable Mixing Chamber** — conversion and macro/micro explanation.

Do not distribute art effort equally before the flagship prototype passes.

---

## 10. Demo No-Go

Stop hero production and return to the relevant scientific gate when:

- only the representation mask looks different;
- the effect disappears under matched display density;
- temporal continuity requires proposed-only filtering;
- a camera move changes the physical partition;
- the hero render gives a different conclusion from the neutral render;
- the cost plot and the displayed run do not refer to the same artifact family.
