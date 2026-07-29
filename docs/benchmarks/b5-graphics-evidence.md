# B5 — Graphics evidence

## Goal

Show the method clearly without introducing new unvalidated physics or building a
full production rendering engine.

## Shared render channels

- instanced exact particles;
- statistically sampled display particles with explicit non-physical ownership;
- density/species/temperature volume;
- exact/kinetic/probe partition mask;
- collision-history graph and indicator overlays;
- error-reference difference view;
- velocity distribution and pair-statistics plots.

## Primary comparisons

Every hero scene uses the same camera, lighting, transfer functions, display
particle density, and temporal sampling for all methods.

## Temporal evidence

Measure and show:

- popping at representation changes;
- frame-to-frame image difference;
- particle-track continuity for exact identities;
- volume continuity;
- partition motion;
- physical observable error.

## Required video layout

A recommended four-panel layout:

```text
final shared render | representation mask
exact-reference diff | state/history diagnostics
```

## Exit gate

- at least two physical effects are visually restored;
- the effect remains after matched rendering density;
- no unexplained manual compositing;
- every clip maps to run IDs and metrics;
- failure cases are included in supplementary material.
