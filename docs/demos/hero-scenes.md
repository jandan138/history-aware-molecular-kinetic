# Hero Scenes

The three scenes have deliberately different responsibilities. They are not three
variants of the same generic gas cloud.

Detailed contracts:

- [Zoomable Mixing Chamber](scene-specs/zoomable-mixing.md)
- [Correlation Labyrinth](scene-specs/correlation-labyrinth.md)
- [Expansion into Vacuum](scene-specs/expansion-into-vacuum.md)

Shot IDs and timing are defined in the [Storyboard](storyboard.md).

---

## Hero 1 — Zoomable Mixing Chamber

Two colored gases are separated by a divider. The divider opens and the gases
mix.

### Primary responsibility

Explain conversion and zoomability, not history causality.

### What it proves

- shared macroscopic/microscopic state;
- exact-to-kinetic and kinetic-to-exact continuity;
- screen-space display LOD separated from physics LOD;
- species and velocity-distribution consistency;
- no mass/momentum/energy jump at conversion;
- persistent exact identity and non-physical statistical display samples are not
  confused.

### Required panels

```text
shared final render | representation/display policy
velocity/species plot | conservation + conversion timeline
```

### Avoid

Do not claim that mixing itself requires history-aware refinement. This is a
conversion and camera-decoupling scene.

---

## Hero 2 — Correlation Labyrinth

Gas flows through regions designed to have similar runtime-observable state
moments but different re-encounter topology.

### Primary responsibility

Provide the strongest visual/scientific evidence for C3/C4.

### What it proves

- history/probe features add information beyond state, geometry, and finite-density
  controls;
- the proposed indicator localizes exact dynamics differently from Knudsen-only
  or packing-only baselines;
- practical online information recovers a declared future observable;
- the result survives held-out geometry/regime evaluation.

### Strongest visual

Show preregistered matched-state block pairs with:

- state features nearly equal;
- collision graph/history different;
- full EDMD versus kinetic future discrepancy different;
- practical score aligned with the discrepancy;
- a visible residence, escape, mixing, or wall-impact effect.

Collision graphs explain the result; they are not the result.

---

## Hero 3 — Expansion into Vacuum

A chamber opens through a small aperture into a larger low-density region.

### Primary responsibility

Serve as the visual flagship, teaser, and dynamic Pareto scene.

### What it proves

- a high-error/transitional region moves over time;
- ballistic and collisional zones coexist;
- state-only adaptive and history/probe-aware policies can be compared;
- exact-region budget and dynamic conversion matter;
- coarse far field remains scalable;
- macro volume, statistical display particles, and exact identities can be viewed
  continuously without camera-driven physics.

### Baselines

- full EDMD declared reference at an audited scale;
- full DSMC/kinetic;
- uniGasFoam or another state-only hybrid when canonically comparable;
- proposed practical policy;
- oracle-history upper bound.

### Required visible observable

At least two preregistered quantities such as plume half-angle, density ridge,
species front, aperture flux, pressure pattern, or escape probability must remain
visible under matched rendering.

---

## Optional fourth scene — Moving Wall

A translating or oscillating plate creates a moving exact region. Use only if the
first three scenes already cover the claims and the interface needs an additional
stress test. It is supplementary, not a new main story.
