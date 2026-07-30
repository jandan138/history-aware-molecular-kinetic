# Evidence matrix

| Figure/table concept | Run families | Metrics | Primary interpretation | Alternative explanation to exclude |
|---|---|---|---|---|
| Exact/kinetic regime map | B1 all families | field/distribution/pair errors | where models diverge | numerical resolution/noise |
| Matched-state history pair | B1/B2 labyrinth | state distance, history distance, future error | history beyond local state | hidden geometry/state feature |
| Indicator generalization | B2 grouped splits | delta MAE/recall, calibration | held-out history value | row leakage/overfit |
| Enskog attribution | B1/B2 finite density | EDMD–DSMC vs EDMD–Enskog | model versus history | mismatched parameters |
| Demotion audit | B3-D | M/P/E, stress, heat flux, downstream error | conservative compression | trivial equilibrium case |
| Promotion audit | B3-P | overlap, transients, g(r), image pop | valid reconstruction | renderer smoothing |
| Dynamic Pareto | B4 | error/time/memory/exact fraction | adaptive benefit | unfair resolution/cost |
| Hero scene diagnostics | B5 all | physical + visual metrics | graphics value | display particle density |
| Mixing conversion shot | B5-ZOOM-MIX | conservation, distribution, pop, camera coupling | C5/C6/C9 | renderer smoothing or camera-driven physics |
| Labyrinth matched-state shot | B5-CORRELATION-LABYRINTH | matched-state distance, history increment, future error | C3/C4/C8 | hidden geometry, Enskog, leakage |
| Expansion flagship visual | B5-EXPANSION-VACUUM | two observable errors, exact fraction, runtime/memory | C4/C7/C8/C9 | unfair display budget or missing exact reference |

Every final figure recipe names frozen cases, exact run IDs, metric versions, and
renderer hashes.


B5 panel recipes additionally record shot ID, render-config hash, camera hash, display-policy hash, and the expected pixel change for the declared physical observable.
