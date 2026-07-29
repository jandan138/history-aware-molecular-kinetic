# Go/No-Go gates

## Gate G0 — Reference trust

**Go:** external cases reproduce documented behavior and converters are audited.

**No-Go:** normalization or licensing remains ambiguous.

## Gate G1 — Primitive correctness

**Go:** EDMD and kinetic backends pass independent invariant, convergence, and
sampling tests.

**No-Go:** model discrepancy is measured before numerical error is bounded.

## Gate G2 — Discrepancy exists and is attributable

**Go:** target observables show stable, nontrivial exact/kinetic differences in
well-resolved cases.

**No-Go:** differences vanish under convergence or are dominated by noise.

## Gate G3 — History adds value

**Go:** history features improve grouped held-out prediction beyond state,
geometry, and finite-density controls by a pre-registered operational margin.

**No-Go:** gain is absent, unstable, or only appears under random row splits.

### Pivot G3-E

If Enskog closes the gap, pivot to adaptive exact–Enskog rather than claiming
history causality.

### Pivot G3-P

If exact history helps but is not observable, investigate bounded shadow probes.

## Gate G4 — Conversion is subordinate

**Go:** conversion preserves primary invariants and secondary/statistical error is
below the benefit from local exactness.

**No-Go:** promotion/demotion transients dominate.

## Gate G5 — Dynamic benefit

**Go:** practical policy improves a cost-quality Pareto frontier, with stable
intermediate exact fraction and controlled chatter.

**No-Go:** exact fraction is almost always 0 or 1, or full exact cost remains.

## Gate G6 — Graphics value

**Go:** two physical effects are visibly restored under matched rendering and
clips map to quantitative evidence.

**No-Go:** only the partition mask looks different, or the effect disappears when
display density is matched.

## Suggested internal target, not a law

A useful scene might maintain an average exact volume/particle fraction around
5–30%, but this range is only an engineering target. It must not be presented as
a physical criterion.
