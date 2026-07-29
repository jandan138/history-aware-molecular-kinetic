# Hero scenes

## Hero 1 — Zoomable mixing chamber

Two colored gases are separated by a divider. The divider opens and the gases
mix.

### What it proves

- shared macroscopic/microscopic state;
- exact-to-kinetic and kinetic-to-exact continuity;
- screen-space display LOD separated from physics LOD;
- species and velocity-distribution consistency;
- no mass/momentum/energy jump at conversion.

### Required panels

```text
shared final render | representation mask
velocity/species plot | conservation + conversion timeline
```

### Avoid

Do not claim that mixing itself requires history-aware refinement. This is a
conversion and zoomability scene.

## Hero 2 — Correlation labyrinth

Gas flows through two regions designed to have similar local state moments but
different re-encounter topology.

### What it proves

- history features add information beyond state-only criteria;
- the proposed indicator localizes exact dynamics differently from Knudsen-only
  or packing-only baselines;
- exact refinement restores a declared future observable.

### Strongest visual

Show matched-state block pairs side by side with:

- state features nearly equal;
- collision graph/history different;
- full EDMD vs kinetic discrepancy different;
- proposed score aligned with the discrepancy.

This is the most important scientific scene.

## Hero 3 — Expansion into vacuum

A chamber opens through a small aperture into a larger low-density region.

### What it proves

- a high-error/transitional region moves over time;
- ballistic and collisional zones coexist;
- state-only adaptive and history/probe-aware policies can be compared;
- exact-region budget and dynamic conversion matter;
- coarse far field remains scalable.

### Baselines

- full EDMD at reduced scale;
- full DSMC;
- uniGasFoam or state-only hybrid;
- proposed practical policy;
- oracle-history upper bound.

## Optional fourth scene — Moving wall

A translating or oscillating plate creates a moving exact region. Use only if the
first three scenes already cover the claims and the interface needs an additional
stress test.
