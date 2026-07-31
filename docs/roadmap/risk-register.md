# Risk Register — Molecular Echoes

| ID | Risk | Probability | Impact | Early signal | Mitigation / pivot |
|---|---|---:|---:|---|---|
| R0 | Exact numerical reversal is unreliable | Medium | Critical | return/event checksum error grows rapidly | deterministic ordering, higher precision/reference replay; stop echo claim if unresolved |
| R1 | “Same present” is only a coarse-binning illusion | High | Critical | branches become distinguishable under finer `f1_h` audit | preregister multi-resolution audit; narrow wording or redesign surgery |
| R2 | Future separation is seed/cherry-pick specific | Medium | High | weak/unstable CI across seeds and `N` | fixed seed families, held-out confirmation, simpler observable |
| R3 | Molecule-budget effect is only collision count | High | Critical | count-matched suppression gives same curve | null controls, collision-time matching, topology shuffle; drop mechanism claim |
| R4 | Incoming-pair diagnostic is post-hoc | Medium | High | only selected bins/observables correlate | preregister bins/observables and uncertainty; report negative result |
| R5 | Collision graph disagrees with raw event ledger | Medium | Critical | ancestry/repeated-event query mismatch | reference graph implementation, exhaustive small-case tests |
| R6 | Local branch silently misses dependencies | Medium | Critical | local/full resimulation diverge | conservative cone expansion and full fallback; label approximate policies |
| R7 | Causal cone becomes global immediately | High | High | affected fraction approaches 1 quickly | choose bounded edit horizons/scenes; remove speed claim; consider VIS pivot |
| R8 | Branch storage equals full trajectory duplication | Medium | High | copy-on-write overhead dominates | segment/checkpoint sharing, compression, honest full-copy baseline |
| R9 | Correlation surgery visibly changes the present | High | High | pivot mismatch is obvious or fails fine audit | constrained assignment/moment correction; narrow authoring claim |
| R10 | Surgery future is uncontrolled noise | Medium-high | High | low repeatability or no monotone control | expose bounded controls/retention budget; compare random surgery; stop authoring claim |
| R11 | Reviewer sees a classic Loschmidt echo only | High | Critical | teaser can be summarized as “reverse velocities” | foreground branching, causal edit algorithm, correctness, storage, interaction |
| R12 | Reviewer sees generic Time-Warp rollback | Medium | Critical | hard-sphere/correlation-specific contribution unclear | explicit prior-art boundary; physical edit semantics; surgery and molecule science |
| R13 | Deng link is overstated | Medium | Critical | proof language used as algorithm guarantee | ADR/claim review; “inspired by” language; null controls and finite-system limits |
| R14 | Demo becomes a graph-debugger video | Medium | High | physical difference invisible without overlays | hero gates require overlay-free visible outcomes |
| R15 | Demo consumes research time too early | High | High | 3D asset/material work before G0–G4 | enforce V0–V5 gates; primitive geometry first |
| R16 | 3D scale is too expensive for branch interaction | Medium | High | latency exceeds workflow target | 2D correctness + reduced 3D hero; acceleration only after algorithm passes |
| R17 | External EDMD reference mismatch | Medium | Medium | internal/DynamO definitions disagree | normalization audit, analytic cases, process isolation |
| R18 | VIS fallback is treated as a title change | Medium | High | no tasks, linked views, or expert evaluation | formal venue ADR/pivot; rebuild paper and evaluation |
| R19 | Old LOD route leaks into active claims | Medium | Medium | conversion/partition wording reappears | keep C3–C9 archived; docs/CI review against ADR 0009 |

## Top three immediate risks

1. **R0:** exact reversal and replay correctness;
2. **R1:** multi-resolution same-present validity;
3. **R3:** molecule topology versus collision-count confound.

No production-scale graphics work is justified until these are addressed.
