# Risk register

| ID | Risk | Probability | Impact | Early signal | Mitigation / pivot |
|---|---|---:|---:|---|---|
| R1 | History redundant with state | High | Critical | No grouped B2 gain | Stop LOD claim |
| R2 | Enskog explains error | Medium-high | High | B1 Enskog matches EDMD | Pivot coarse backend |
| R3 | Oracle-only feature leakage | Medium | Critical | Online policy needs full EDMD | Probe or stop |
| R4 | Conversion transient too large | Medium | High | B3 downstream error spike | Better conversion/static patches |
| R5 | Exact fraction near 100% | Medium | High | Budget always saturated | Parallel EDMD pivot |
| R6 | Exact fraction near 0% | Medium | Medium | Boltzmann regime everywhere | Negative result/new scenes |
| R7 | External tool build friction | Medium | Medium | R0 delay | Container/process isolation |
| R8 | Demo consumes research time | High | High | Asset/render work before B4 | Enforce demo gates |
| R9 | Stochastic uncertainty hides effect | Medium | High | Huge CI in B1/B2 | More seeds/target redesign |
| R10 | GPU history sketch biased | Medium | Medium | Disagrees with exact reference | Keep correctness reference |
| R11 | Reviewer sees only CFD | Medium | High | No visible restored phenomenon | Strengthen B5 or choose JCP route |
| R12 | Claim overstates theorem link | Medium | Critical | Proof terms used as guarantees | Claim-boundary review |
