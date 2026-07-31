# Molecular Echoes E2 preregistration

Status: **frozen before primary seeds 0–5 are run**.

E2 is a mechanism gate, not a second E1 robustness sweep. Its paper question is:

> Starting from the same mixed pivot, does a structured finite
> collision-molecule retain more of the reversible color echo than an equal-dose
> but differently wired set of collisions?

The intended one-sentence result is “same present, same collision dose, different
collision wiring, different future.” If the two wiring controls do not separate,
that sentence is rejected.

## Frozen scientific scope

- Geometry, particle sizes, anisotropic initialization, passive-color pattern,
  preparation time, horizon, sampling interval, primary particle counts
  `N=128,256`, and primary seeds `0,…,5` are inherited unchanged from E1-v0.
- Both the forward pivot velocity and its exact velocity reversal are evaluated.
  The reverse direction is the positive echo test; the forward direction is the
  preregistered negative-direction check.
- The extended-dynamics ladder is `ghost → (4,0) → (8,0) → (16,1) → full`.
- Time layers have width `0.1`.
- There is no `N=512`, three-dimensional scene, fixed-`Nε` extrapolation, dense
  sweep, or extra null family in E2-v0.

The executable protocol is
`configs/studies/molecular-echoes-e2-v0.json`.

## Modified dynamics and molecule budget

Every particle starts as a singleton collision molecule at the pivot. Accepted
collisions are multigraph edges on particle identities. A component records its
particle count and circuit rank (independent-cycle count).

For budget `(Λ,Γ)`:

1. an encounter between distinct components is accepted exactly when their
   combined size is at most `Λ` and their combined circuit rank is at most `Γ`;
2. an encounter inside one component is accepted exactly when its circuit rank is
   smaller than `Γ`, after which the rank increases by one;
3. a rejected encounter receives no collision impulse and the disks pass through
   each other; entry and exit of the resulting overlap are explicit events;
4. a rejected overlap never changes molecule membership, rank, or collision-event
   predecessors.

This is an extended causal intervention inspired by the T-dynamics budget in
Deng–Hani–Ma. It is not ordinary hard-disk EDMD, a finite-system theorem, or an
implementation of their cutting proof. The `full` branch is separately checked
event by event against the existing periodic EDMD reference.

## Dose-only calibration, completed before freezing

Seeds `100,101` at `N=128` are excluded from every primary interval and figure.
Calibration is allowed to inspect only accepted-collision counts relative to the
full branch, over both directions. Passive-color observables are not computed.

The frozen rule selects the candidate whose mean dose is closest to `0.5`, with a
lexical tie break. The observed excluded-seed means were:

| Budget | Mean collision dose |
|---|---:|
| `(4,0)` | 0.571467 |
| `(8,0)` | 0.682053 |
| `(16,1)` | 0.789534 |

Therefore `(4,0)` is the only budget receiving mechanism controls. The complete
allowed calibration output is stored as `calibration-dose-only.json` in the E2
result directory.

## Two mechanism controls, and no more

For each case and direction, the accepted and total encounter counts of `(4,0)` are
recorded in `0.1`-wide time layers.

1. **Count/time-matched random:** encounters are selected sequentially without
   replacement toward the `(4,0)` accepted quota in every layer. The policy sees
   event ordinal, time layer, and target counts only; it never sees color labels,
   color score, molecule membership, or the scientific response.
2. **Topology-shuffled `(4,0)`:** at each new time layer, particle-to-component
   membership is shuffled deterministically while preserving the multiset of
   component `(size, circuit-rank)` states. Physical geometric encounter partners
   are not replaced. This destroys the hidden molecule wiring while retaining the
   same budget law.

Because dynamics diverge after an altered impulse, exact collision-count equality
is not assumed. The maximum relative dose discrepancy is audited and is itself a
frozen gate.

## Registered measurements

Primary response:

- passive-color E score and normalized color recovery through time;
- terminal reverse recovery along the five-point budget ladder;
- terminal `(4,0)` minus random and `(4,0)` minus topology-shuffled gaps.

Supporting mechanism readouts:

- accepted collision dose and per-layer encounter/accept counts;
- incoming-pair closure defect, defined as the absolute covariance of the two
  incoming normal-velocity components divided by their mean marginal variance;
- mirrored-pair alignment with the same direction's full branch, matched by time
  layer and particle-pair multiplicity;
- molecule root/size/rank before the encounter, predecessor events, repeated-pair
  multiplicity, suppression reason, and maximum simultaneous overlaps.

The closure and alignment readouts support interpretation. They cannot rescue a
failed color-response/control gate.

## Frozen decision rule

Seed bootstrap intervals resample the six primary seed identities after averaging
the two particle counts within a seed. There are 10,000 resamples.

`go` requires every item below:

- mean per-case Spearman correlation between budget order and terminal reverse
  recovery at least `0.7`;
- mean reverse full-minus-ghost color-score gap at least `0.3`;
- mean `(4,0)` advantage over each control at least `0.03`;
- lower endpoint of each seed-bootstrap 95% control-gap interval strictly above
  zero;
- maximum relative collision-dose mismatch of either control at most `0.15`;
- maximum mean forward-direction recovery across the five ladder branches at most
  `0.35`;
- relative energy drift and absolute momentum drift at most `1e-12`.

`narrow` requires the ladder and full/ghost separation plus a positive registered
advantage over at least one control, while one or more full gates fail. The paper
may then discuss only the passing, explicitly scoped mechanism. Otherwise the
decision is `stop_e2`, and the collision-wiring claim is removed.

No threshold or branch family may be changed after primary execution starts. Any
new diagnostic is labelled post hoc and cannot change this decision.
