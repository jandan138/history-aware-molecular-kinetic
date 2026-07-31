# Molecular Echoes E2 result

**Decision:** `stop_e2` on 2026-08-01 under the frozen mechanism rule.

**Protocol:** `MOLECULAR-ECHOES-E2-v0`, frozen at commit
`0703c6dcf29930d35c45236351e40c0e38dd3e8c` and annotated tag
`molecular-echoes-e2-preregistered-v0` before primary seeds 0–5 were run.

## Result in one sentence

Allowing progressively more collisions produces a strong graded reverse echo, but
the registered `(4,0)` collision-molecule wiring does **not** outperform either a
count/time-matched random policy or a topology-shuffled policy. E2 therefore rejects
the stronger claim that this coarse finite molecule explains recovery beyond
collision dose.

This is not an E1 failure. E1 still establishes its scoped same-resolved-present,
opposite-futures phenomenon. E2 closes the proposed molecule-topology attribution
and prevents it from being promoted into the paper spine.

## Frozen experiment

| Item | Registered value |
|---|---|
| Geometry and pivot | inherited unchanged from E1-v0 |
| Systems | `N=128, d=0.04` and `N=256, d=0.02` |
| Primary seeds | `0–5`, 12 cases total |
| Excluded calibration | `N=128`, seeds `100,101`; collision counts only |
| Directions | forward pivot and exact velocity reversal |
| Budget ladder | `ghost → (4,0) → (8,0) → (16,1) → full` |
| Time-layer width | `0.1` |
| Selected controlled budget | `(4,0)`, calibration mean dose `0.571467` |
| Mechanism controls | count/time-matched random; topology-shuffled `(4,0)` |
| Primary response | passive-color E score and normalized recovery |
| Supporting readouts | collision dose, incoming-pair closure defect, mirrored-pair alignment |

Every post-pivot branch was simulated forward in time. Suppressed encounters use
the preregistered extended overlap/crossing semantics and are not labelled exact
hard-disk trajectories.

## What passed: a graded collision-budget response

The mean per-case Spearman correlation between registered budget order and terminal
reverse recovery is `0.930574`, above the frozen `0.7` threshold. The mean reverse
full-minus-ghost color-score gap is `0.359754`, above the frozen `0.3` threshold.

Mean terminal reverse recovery is:

| Branch | `N=128` | `N=256` | Combined |
|---|---:|---:|---:|
| ghost | 0.110741 | 0.262225 | 0.186483 |
| `(4,0)` | 0.326627 | 0.419209 | 0.372918 |
| `(8,0)` | 0.436778 | 0.558367 | 0.497573 |
| `(16,1)` | 0.642275 | 0.718563 | 0.680419 |
| full | 1.000000 | 1.000000 | 1.000000 |

This supports the descriptive statement that more permissive collision budgets
retain more of the reverse echo. It does not identify whether the relevant variable
is collision amount, collision timing, graph topology, or another correlated
property of the accepted event set.

The forward-direction negative check also passes: all five ladder branches remain
at non-positive mean normalized recovery, with a registered maximum of `-0.060761`.
All branches pass the frozen energy and momentum conservation threshold.

## What failed: wiring beyond dose

The selected `(4,0)` branch has combined mean terminal reverse recovery `0.372918`.
The count/time-matched random control reaches `0.385390`, and the topology-shuffled
control reaches `0.390176`. Consequently:

| Registered contrast | Mean color-score gap | Seed-bootstrap 95% interval | Result |
|---|---:|---:|---|
| `(4,0)` minus random | -0.007636 | [-0.032264, 0.016086] | FAIL |
| `(4,0)` minus topology-shuffled | -0.009639 | [-0.049062, 0.029519] | FAIL |

Both mean gaps have the opposite sign from the registered positive mechanism claim,
and both intervals cross zero. The result is therefore not a near miss on the
predeclared `0.03` effect threshold.

There is size heterogeneity that is disclosed but not promoted into a new claim.
At `N=128`, both controls recover more than `(4,0)`; at `N=256`, `(4,0)` recovers
more than both controls. The protocol pooled the two registered sizes and did not
register a size-interaction claim. No post-result `N=512`, new seed set, or budget
selection is added to rescue that pattern.

## Collision-dose and supporting diagnostics

Mean reverse collision doses are `0.560770` for `(4,0)`, `0.535286` for the random
control, and `0.584023` for the topology-shuffled control. Random matching remains
within `9.375%` in every case/direction. The topology-shuffled dynamics change the
endogenous encounter stream more strongly: its worst relative dose difference is
`25%`, failing the frozen `15%` audit.

That dose mismatch weakens any isolated interpretation of the topology-shuffled
branch, but it cannot reverse the registered decision: the better-matched random
control already fails to show a structured `(4,0)` advantage.

The incoming-pair closure defect is also non-discriminating at this scope. In the
reverse direction its means are `0.396299` for `(4,0)`, `0.416362` for random,
`0.421514` for topology-shuffled, and `0.393603` for full. Mirrored-pair alignment
is higher for `(4,0)` (`0.839525`) than for random (`0.739460`) or topology-shuffled
(`0.738177`), yet this does not translate into a higher pooled recovery. These
supporting readouts cannot rescue the failed response controls.

## Preregistered gate

| Check | Result |
|---|---|
| Reverse budget ladder | PASS |
| Reverse full/ghost separation | PASS |
| Structured `(4,0)` beats random | FAIL |
| Structured `(4,0)` beats topology shuffle | FAIL |
| Random gap lower confidence bound > 0 | FAIL |
| Topology gap lower confidence bound > 0 | FAIL |
| Maximum control dose error ≤ 15% | FAIL |
| No forward echo | PASS |
| Conservation | PASS |

The frozen rule requires every check for `go`. `narrow` additionally requires a
positive registered pooled advantage over at least one wiring control; neither is
positive. The only valid decision is therefore `stop_e2`.

## Claim and roadmap consequence

- C13, “structured collision-molecule budget explains response beyond collision
  count,” is closed negative for E2-v0.
- C14's incoming-pair proxy does not provide the proposed discriminating mechanism
  evidence at this scope.
- The optional `N=512` and fixed-`Nε` follow-up are not run.
- E1 remains a valid phenomenon/demo result.
- E3/E4 may proceed only as a narrower collision-graph, replay, and counterfactual
  branching system route. They cannot cite E2 as proof that molecule topology
  carries the echo.

This is the intended function of the gate: keep a visually appealing budget ladder
from being mistaken for evidence that survives equal-dose mechanism controls.

## Visual and provenance audit

The final figure and video use outcome-neutral wording, a fixed orthographic camera,
identical time sampling, and identical particle display across branches. The video
is 1280×720 H.264 at 24 fps, 150 frames, and 6.25 seconds. No rendered frame mutates
the simulated state.

| Provenance item | Value |
|---|---|
| Study content ID | `echo-e2-402af7ed89d71b8a` |
| Preregistration commit | `0703c6dcf29930d35c45236351e40c0e38dd3e8c` |
| Clean run/render commit | `50796360e370e2f47be92a109751171df5fd00fb` |
| Protocol SHA-256 | `ed98997f548b03ad0566e642bb82ecc3d5a4d0720b928704748d134ec28d3a0b` |
| Calibration SHA-256 | `d7d5dde6b66dfa419d50b09dae71c58b4e095fc914a79c32c37c329ccc520289` |
| Run-manifest SHA-256 | `d817c5f810cb04e63a69795500254d20959f02f658fc2d082dc7342a98e56d31` |
| Result tag | `molecular-echoes-e2-result-v0` |

Core artifact hashes:

| Artifact | SHA-256 |
|---|---|
| `summary.json` | `c3f55c240375093f8f1d25eacee8e6c5e42e746006a320fe652064ca9a17381e` |
| `mechanism-audit.jsonl` | `a36b82002127b1d74cfdddb2ae01f6ced63f67ebf4108e575535ae79dbfb1432` |
| `branch-metrics.jsonl` | `545eb15a2b8f73757858a39d7bc0668ac05a7f8698a0f324085182ebbd2fe13c` |
| `encounter-events.jsonl.gz` | `d079682c6125b079e1fde01897d2cdc19875f105843c4d5fbb3be42a65027dae` |
| `particle-trajectories.npz` | `0d4d3e55c998324ecf53d73489378b44efdd6debbbe0e7dddcf4c114c5439e30` |
| `figure-e2-main.svg` | `db47eb6c058475017963096c39f241a664ec2408ec809369822abe181c8794d8` |
| `figure-e2-main.pdf` | `750e138bef73795d35e5f75b63fd8a1c4eca5a0c20633308c3b77f3e2efee054` |
| `echo-e2-collision-wiring.mp4` | `59cf80c4e937af897b86a4d2452520d0c22c774821e9a1c808bb0d82b0726090` |
| `render-manifest.json` | `8ca7ad1e41e962033015a02719c3d1919ec329459a8b87ffa04109fb53d2e086` |

Large generated artifacts remain under ignored `results/`; the compact result page,
frozen calibration, and hashes are committed. Reproduce them with:

```bash
PYTHONPATH=src python scripts/run_echo_e2.py \
  --config configs/studies/molecular-echoes-e2-v0.json \
  --calibration results/molecular-echoes-e2-v0/calibration-dose-only.json \
  --output results/molecular-echoes-e2-v0
```
