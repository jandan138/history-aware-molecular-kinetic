# Molecular Time Machine E5 — frozen Same Present, Chosen Future recipe

**Study:** `MOLECULAR-TIME-MACHINE-E5-v0`.

**Question:** Can a creator suppress one selected future stroke through a sparse
hidden velocity-ownership surgery while preserving the declared current frame and
the rest of the glyph?

## Paper act

```text
show the original future E
→ creator selects the middle-stroke extension
→ return to one common visible present at t=0.80
→ exchange velocity ownership inside declared cells
→ exact physical previews choose a sparse surgery
→ original future resolves to E; chosen future resolves to C
```

This is one Hero authoring session. It is not a breadth or robustness study.

## Frozen scene

The scene reuses the E1 exact-reverse world:

- particle count: `256`;
- seed: `4`;
- preparation time: `1.0`;
- reverse-future end time: `1.0`;
- authoring pivot: `t=0.80`;
- declared resolved spatial grid: `4×2`.

The denser seed-4 realization was chosen during excluded design calibration because
all three E strokes are visibly populated and every selected middle-stroke particle
belongs to a non-singleton `4×2` pivot cell. It was not chosen through a seed-wise
surgery outcome comparison.

## Frozen creator target

The creator selects the middle horizontal extension, excluding the vertical spine:

```text
x in (0.95, 1.75]
y in [0.90, 1.10]
```

Its registered terminal foreground membership is:

```text
15, 48, 65, 82, 99, 106, 174, 211
```

The target is resolved from the unedited terminal E before any candidate surgery is
selected. Collateral foreground is the other foreground membership inside the
baseline terminal E pattern.

## Frozen surgery palette

At `t=0.80`, group the eight selected particles by their current `4×2` spatial
cell. An atomic surgery transposes the two complete velocity values of one selected
pair in the same cell. Enumerate:

- every legal single transposition;
- every pair of legal, particle-disjoint transpositions.

The registered palette contains exactly `30` candidates. No cross-cell swap,
non-target donor, velocity perturbation, three-swap candidate, constrained
optimizer, or stochastic sampling is allowed.

Every preview runs complete hard-disk EDMD from the edited common pivot to
`t=1.0`. Preview timing is recorded for transparency, but it is not an E5 claim or
gate.

## Selection rule

First discard candidates whose collateral foreground retention is below `90%`.
Then choose deterministically by:

1. maximum selected-target ejection;
2. maximum collateral foreground retention;
3. minimum touched-particle count;
4. lexicographic swap tuple.

Calibration freezes the expected selected swaps as:

```text
(48,82) and (174,211)
```

The recipe raises an error if target membership, palette size, or selected swaps
drift before the clean evidence run.

## Operator contract

The selected surgery must establish at the pivot:

- positions and passive colors identical;
- radii, masses, IDs, and weights identical;
- complete velocity multiset identical inside every declared `4×2` cell;
- target-conditioned velocity multiset identical inside every declared cell;
- valid geometry;
- mass, momentum, and energy errors at most `1e-12`.

This contract supports **same declared resolved present**. It does not claim the
same exact microstate, continuous `f1`, or equality at unregistered finer grids.

## Outcome metrics and gate

| Check | Frozen threshold |
|---|---:|
| target-particle ejection | `>= 70%` |
| geometric target-region reduction | `>= 70%` |
| collateral foreground retention | `>= 90%` |
| touched particles | `<= 4` |
| pivot replay terminal position RMS | `<= 1e-9` |
| pivot replay terminal velocity RMS | `<= 1e-9` |
| pivot replay collision-pair agreement | `1.0` |
| mass / momentum / energy error | each `<= 1e-12` |

`go` requires every row. There is no rescue grid: a failed target or collateral
gate stops the E5 glyph-authoring claim.

## Required evidence package

```text
future-target.json
surgery-preview-palette.json
selected-surgery-manifest.json
resolved-present-audit.json
pivot-replay-audit.json
summary.json
decision.md
same-present-trajectories.json.gz
figure-same-present-chosen-future.svg/.pdf
same-present-two-letters.mp4
same-present-chosen-future.html
render-manifest.json
run-manifest.json
```

The figure, video, and browser use matched cameras, particle display, colors, and
time samples. The browser presents cached exact runs; it does not simulate physics
or alter terminal particle positions.

## Explicitly out of scope

- seed or particle-count sweeps;
- random-surgery and history-budget baselines;
- multi-resolution audit grids beyond the declared operator contract;
- alternative target letters or multi-step composition;
- geometry editing, 3D, user studies, native acceleration, or scaling claims.
