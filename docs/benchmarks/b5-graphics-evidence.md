# B5 — Graphics Evidence

## 1. Goal

Show the method clearly without introducing new unvalidated physics or building a
full production rendering engine.

B5 does not rescue a failed B2–B4. It freezes already validated artifact families
and asks whether the recovered physical effects are legible under a shared
renderer.

---

## 2. Candidate scene set

```text
B5-ZOOM-MIX-v0
B5-CORRELATION-LABYRINTH-v0
B5-EXPANSION-VACUUM-v0
```

Their scene contracts are in [Hero Scene Specifications](../demos/scene-specs/README.md).

---

## 3. Shared render channels

- instanced exact particles;
- statistically sampled display particles with explicit non-physical ownership;
- density/species/temperature volume;
- exact/kinetic/probe partition mask;
- collision-history graph and indicator overlays;
- error-reference difference view;
- velocity distribution and pair-statistics plots;
- conversion/conservation timeline;
- cost–quality and exact-fraction insets.

---

## 4. Required methods

Depending on the scene:

- full exact declared reference;
- full kinetic;
- state/geometry/finite-density baseline;
- state-only dynamic LOD;
- practical history/shadow-probe policy;
- oracle-history upper bound;
- proposed dynamic LOD;
- naive conversion/display baselines for the zoom scene.

A method may be omitted only with a documented applicability reason.

---

## 5. Primary comparisons

Every comparison group uses the same:

- camera and shot time;
- lighting and materials;
- transfer functions;
- display particle density policy;
- exact particle display scale;
- temporal sampling;
- motion blur/filtering;
- output color management.

The group is invalid if the comparison-lock hashes differ.

---

## 6. Temporal evidence

Measure and show:

- popping at representation changes;
- frame-to-frame image/field difference relative to natural motion;
- particle-track continuity for exact identities;
- statistical display temporal continuity;
- volume/species continuity;
- partition motion/chatter;
- physical observable error;
- camera–physics decoupling.

---

## 7. Required layouts

### Four-panel scientific layout

```text
final shared render | representation mask
exact-reference diff | state/history/conversion diagnostics
```

### Flagship layout

The main image remains visually clean. A small representation mini-map and one
metric/Pareto inset may be shown; dense diagnostics move to a freeze frame or
supplementary panel.

---

## 8. Claim mapping

B5 follows [Claim-to-Visual Evidence Matrix](../demos/claim-to-visual-evidence.md):

- C3/C4 → Correlation Labyrinth;
- C5/C6/C9 → Zoomable Mixing;
- C7/C8/C9 → Expansion into Vacuum.

Each final clip has a pixel audit naming run IDs, artifact hashes, physical
observable, expected pixel change, renderer hash, and alternative explanations.

---

## 9. Render reproducibility

Every output records a `render-manifest.json` validating against
`schemas/render-manifest.schema.json`.

Candidate configs live in:

```text
configs/render/
configs/render/scenes/
```

Frozen B5 cases copy or content-address the exact config used; they never refer to
an unversioned “latest” preset.

---

## 10. Exit gate

- all three candidate scene families have complete manifests;
- at least two independent physical effects are visually restored;
- effects remain after matched rendering density;
- neutral and hero renders agree;
- no unexplained manual compositing;
- every clip maps to run IDs and metrics;
- camera–physics audit passes;
- conversion is not hidden by proposed-only filtering;
- failure cases are included in supplementary material;
- the displayed Pareto point and video use the same run family.

Detailed thresholds and No-Go conditions are in
[Visual Acceptance Criteria](../demos/visual-acceptance-criteria.md).
