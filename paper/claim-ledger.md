# Claim ledger

| ID | Candidate claim | Required benchmark | Required evidence | Status |
|---|---|---|---|---|
| C0 | External reference adapters reproduce documented behavior | R0 | raw hashes, normalization audit, scalar reproduction | planned |
| C1 | Internal EDMD and kinetic primitives are trustworthy in declared regimes | B0 | analytic tests, convergence, invariants, external comparison | internal 2D reference passes analytic/invariant/dilute-rate checks; external comparison pending |
| C2 | Exact-versus-kinetic discrepancy has stable, attributable structure | B1 | discrepancy atlas, uncertainty, Boltzmann/Enskog attribution | planned |
| C3 | Collision history adds predictive value beyond state/geometry controls | B2 | grouped held-out delta, CI, ablations, leakage audit | closed exploratory negative in PHASE1-HISTORY-STORY-v0; relative MAE \(-0.83\%\), 95% CI \([-2.21\%,0.52\%]\) |
| C4 | A practical probe/observable policy retains useful history value | B2 | oracle upper bound vs practical policy, probe cost | deferred with the predictor route |
| C5 | Exact→kinetic demotion preserves primary invariants and bounded statistics | B3 | conversion reports, downstream transient, baselines | deferred with the hybrid route |
| C6 | Kinetic→exact promotion avoids invalid overlap and unacceptable transients | B3 | placement/warm-up studies, temporal diagnostics | deferred with the hybrid route |
| C7 | Dynamic policy improves a cost-quality Pareto frontier | B4 | full sweeps vs uniform/state-only/upper-bound methods | blocked/deferred after C3 |
| C8 | The method restores at least two visible physical effects | B5 | neutral shared renderer, exact/reference comparison, matched display density, scene-specific observables, pixel audit | deferred with the hybrid route |
| C9 | The system supports zoomable molecular/macroscopic visualization without physics-camera coupling | B5 | camera–physics hash audit, conversion continuity, persistent display policy, ZM/EV shots | deferred with the hybrid route |
| C10 | Matched resolved \(f_{1,h}\) states can have distinct observable futures | molecular echo E2 | pivot matching manifest, trajectory-disjoint seeds, exact reverse vs chaotized reverse response | proposed; no continuous-\(f_1\) or one-trajectory ensemble claim |
| C11 | An incoming-pair closure-defect proxy tracks the missing correlated response | molecular echo E4 | preregistered bins/observables, branch derivatives, uncertainty | proposed |
| C12 | A \((\Lambda,\Gamma)\) collision-molecule budget distinguishes forward relaxation from reverse echo | molecular echo E3/E5 | full versus nested budget paths, explicit ghost semantics, matched branch audit | proposed; extended T-dynamics is not exact hard-sphere EDMD |
| C13 | The required history budget has an interpretable fixed-\(N\varepsilon\) trend | molecular echo E5 | small 2D Boltzmann–Grad sequence and fixed observable tolerance | proposed; not a kinetic-limit theorem |

## Claim review rule

No abstract or introduction sentence may be stronger than the corresponding row.
A failed or weakened claim remains in this ledger with the reason.


## B5 scene ownership

- C3/C4: `B5-CORRELATION-LABYRINTH-v0`
- C5/C6/C9: `B5-ZOOM-MIX-v0`
- C7/C8/C9: `B5-EXPANSION-VACUUM-v0`

Every B5 claim follows `docs/demos/claim-to-visual-evidence.md` and requires a render manifest plus comparison-lock audit.
