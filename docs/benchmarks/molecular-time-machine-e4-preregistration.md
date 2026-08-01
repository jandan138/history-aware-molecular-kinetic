# Molecular Time Machine E4 preregistration — Choose the Cause, Direct the Future

**Status:** frozen recipe; canonical evidence returned `go`. See the
[E4 result](molecular-time-machine-e4-result.md).

**Study:** `MOLECULAR-TIME-MACHINE-E4-v0`.

**Story question:** can an animator point at a desired future feature, have the
collision history identify an editable past cause, and obtain a directed exact
counterfactual without turning the session into a global recomputation?

This is E4's only question. It is not a breadth study, a second-edit-family study,
or a parameter sweep.

## Hero: Erase One Stroke

The source world is the same E1 exact-reverse Molecular E used by E3:

```text
source = E1 exact reverse, N=128, seed=0
terminal feature = upper horizontal stroke of the recovered E
target rectangle = x in [0.65, 1.75], y in [1.45, 1.65]
target membership = foreground particle IDs (69, 76, 101, 106)
```

The `N=128` E sample has no foreground particles in the interior of the middle
horizontal stroke, so the upper stroke is the fixed nonempty target. This choice is
about visible target membership, not an edit outcome.

The intended session is:

```text
select the upper stroke
→ trace its baseline ancestors
→ inspect ranked past collisions
→ browse a small exact angle palette
→ save one branch
→ verify that one saved branch against full resimulation
```

## Baseline-only causal ranking

The ranking never reads an edited future. It considers only the first 16 baseline
collisions, and for each collision computes:

- **coverage** — fraction of target particles among its baseline descendants;
- **purity** — fraction of its descendants belonging to the target;
- **causal score** — harmonic mean of coverage and purity.

The top three baseline candidates are frozen by ordinal as `(4, 2, 12)`. The first
recommendation must remain collision `#4`, pair `(101, 111)`, at approximately
`t=0.05512038650510776`. A recommendation drift stops the recipe instead of
silently replacing the Hero.

## Exact preview palette

Each shortlist collision receives exactly four physical previews:

```text
-2°, -1°, +1°, +2°
```

The operation remains the E3 conservative pair-relative-velocity rotation in the
pair centre-of-mass frame. It does not move particle positions at the edit, and it
preserves pair momentum and kinetic energy.

Each preview runs the exact local causal scheduler and is cached by
`(event_id, angle_degrees)`. It does **not** run a complete global reference. The
recommended collision's saved angle is selected by this registered rule:

```text
maximize target ejection − collateral ejection
tie-break: smaller absolute angle, then signed angle
```

`target ejection` is the fraction of selected upper-stroke particles leaving the
selected rectangle. `collateral ejection` is the fraction of all other foreground
E particles leaving the analytic E pattern. These two quantities directly encode
the only story requirement: change the chosen feature more than the rest.

## The one required global reference

Only the saved branch runs `fork_causal_branch`, which performs the full
resimulation oracle. The final local and full branch must satisfy the same
pair/time/terminal tolerances used in E3. This is essential correctness evidence,
not a preview-by-preview safety exercise.

## Frozen gates

| Gate | Threshold | Why it matters to the story |
|---|---:|---|
| target ejection | `>= 0.50` | at least half of the selected stroke visibly leaves it |
| target/collateral ratio | `>= 2.0` | change is more targeted than generic E damage |
| preview median | `<= 0.20 s` | bounded Hero is responsive enough to browse |
| saved-branch baseline reuse | `>= 0.50` | it remains a history branch, not a new whole-world run |
| local/full pair agreement | `1.0` | one saved branch is the same physical branch as full replay |
| max collision-time error | `<= 1e-9` | exact event sequence agreement |
| terminal position RMS | `<= 1e-9` | exact terminal state agreement |
| terminal velocity RMS | `<= 1e-9` | exact terminal state agreement |
| edit momentum / energy error | `<= 1e-12` | physical edit contract remains intact |

Decision:

- `go`: all gates pass; E4 may use the scoped phrase **causal steering**;
- `narrow`: final exactness and responsiveness pass but target selectivity fails;
  phrase the result as **causal exploration**;
- `stop_e4`: final local branch disagrees with full resimulation or the interaction
  latency gate fails.

## Evidence package

The canonical command writes:

```text
causal-target.json
collision-ranking.json
branch-palette.json
authoring-session.json
selected-edit-manifest.json
selected-causal-cone.json
selected-branch-events.jsonl
selected-branch-comparison.json
causal-steering-trajectories.json.gz
figure-causal-steering.svg/.pdf
causal-steering-erase-one-stroke.mp4
causal-steering.html
run-manifest.json
render-manifest.json
```

The browser artifact is intentionally honest: it browses cached exact local
previews; it does not pretend that a renderer changed the simulation. The final
selection and its one complete reference are recorded in `authoring-session.json`.

## Explicitly not in this gate

No random collision control, density or seed sweep, large angle scan, `N=512`,
second edit family, obstacle/geometry edit, 3D scene, GPU/native rewrite, user
study, or renewed E2 wiring experiment is required.

Those are later research choices, not missing checks for this story gate.
