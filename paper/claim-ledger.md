# Claim ledger

| ID | Candidate claim | Required benchmark | Required evidence | Status |
|---|---|---|---|---|
| C0 | External reference adapters reproduce documented behavior | R0 | raw hashes, normalization audit, scalar reproduction | planned |
| C1 | Internal EDMD and kinetic primitives are trustworthy in declared regimes | B0 | analytic tests, convergence, invariants, external comparison | planned |
| C2 | Exact-versus-kinetic discrepancy has stable, attributable structure | B1 | discrepancy atlas, uncertainty, Boltzmann/Enskog attribution | planned |
| C3 | Collision history adds predictive value beyond state/geometry controls | B2 | grouped held-out delta, CI, ablations, leakage audit | unproven |
| C4 | A practical probe/observable policy retains useful history value | B2 | oracle upper bound vs practical policy, probe cost | unproven |
| C5 | Exact→kinetic demotion preserves primary invariants and bounded statistics | B3 | conversion reports, downstream transient, baselines | planned |
| C6 | Kinetic→exact promotion avoids invalid overlap and unacceptable transients | B3 | placement/warm-up studies, temporal diagnostics | planned |
| C7 | Dynamic policy improves a cost-quality Pareto frontier | B4 | full sweeps vs uniform/state-only/upper-bound methods | blocked by C3–C6 |
| C8 | The method restores at least two visible physical effects | B5 | shared renderer, exact reference, matched display density | blocked by C7 |
| C9 | The system supports zoomable molecular/macroscopic visualization without physics-camera coupling | B5 | renderer/physics policy audit and continuity metrics | planned |

## Claim review rule

No abstract or introduction sentence may be stronger than the corresponding row.
A failed or weakened claim remains in this ledger with the reason.
