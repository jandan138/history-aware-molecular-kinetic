# Molecular Time Machine E3 result — one collision, two worlds

**Decision:** `go`.

**Study:** `MOLECULAR-TIME-MACHINE-E3-v0`.

**Frozen recipe tag:** `molecular-time-machine-e3-recipe-v0`.

**Evidence commit:** `a3618573469283beb0454b8b414f659212c57c18` with a clean
worktree, as recorded by the run manifest.

## Result in ordinary language

The new paper route works in its first exact Hero.

We rewound the E1 molecular-echo scene to one microsecond before its third recorded
collision, between particles `101` and `118`. We changed only one thing: the pair's
relative velocity was rotated counterclockwise by one degree in its center-of-mass
frame. No particle position moved at the edit; pair momentum and kinetic energy
were preserved.

At the end of the original future, the passive colors reconstruct a perfect `E`
with score `1.000000`. After the one-degree edit, the score is `0.811782`; the
registered world gap is `0.188218`, and `33/128` particles have visibly different
terminal positions.

The causal engine did not secretly rerun everything. Of the `105` baseline
collisions after the fork, it directly reused `79` (`75.238%`). It invalidated `26`
obsolete baseline events and computed `27` edited events. The affected set grew from
the two edited particles to `33/128` particles (`25.781%`) and never became global.

Most importantly, the local result is the same physical branch as a complete
resimulation: all `106` post-fork collision pairs agree in order, event-pair
agreement is `1.0`, and the terminal state agrees within the frozen numerical
tolerances.

## Frozen gate

| Check | Frozen threshold | Result | Status |
|---|---:|---:|---|
| baseline terminal color score | `>= 0.99` | `1.000000` | pass |
| terminal color gap | `>= 0.15` | `0.188218` | pass |
| visibly changed fraction | `[0.15, 0.40]` | `0.2578125` (`33/128`) | pass |
| local/full collision-pair agreement | `>= 1.0` | `1.000000` (`106/106`) | pass |
| maximum collision-time error | `<= 1e-9` | `1.738287e-11` | pass |
| terminal position RMS | `<= 1e-9` | `8.676301e-11` | pass |
| terminal velocity RMS | `<= 1e-9` | `5.540079e-10` | pass |
| edit momentum error | `<= 1e-12` | `1.110223e-15` | pass |
| edit energy error | `<= 1e-12` | `0.0` | pass |
| baseline-event reuse | `>= 0.50` | `0.752381` (`79/105`) | pass |
| peak affected fraction | `<= 0.50` | `0.2578125` (`33/128`) | pass |

Every registered check passes, so the preregistered rule returns `go` rather than
`narrow` or `stop_e3`.

## What the graph is doing

The baseline graph says that collision #2 has `20` descendant particles along the
unedited history. The edited branch reaches `33` particles because the changed
trajectories create new collisions that did not exist in the baseline graph. This
difference is expected and useful:

- the baseline DAG answers “what inherited this event in the original world?”;
- the runtime affected set answers “what has inherited the edit in the new world?”

The yellow causal overlay therefore is not a precomputed decorative neighborhood.
It is the set that drove event invalidation and recomputation in the edited branch.

## Numerical and runtime interpretation

The local and full runs share the exact same pair-prediction, ballistic advection,
elastic impulse, periodic wrapping, and deterministic ordering kernel. That shared
kernel makes the comparison a test of causal scheduling rather than a comparison of
two subtly different physics implementations.

The canonical evidence was generated with CPython `3.12.12`. Supported CPython
`3.11` locates the same ordinal/pair and returns the same registered story metrics,
but the inherited E1 Gaussian/libm path shifts the absolute target time by about
`8.64e-10`. Runtime recipe validation therefore permits `1e-9` portability drift
for locating the already fixed event; this does not change the canonical artifact,
edit, or local/full correctness thresholds.

The run records `0.081733` seconds for the Python causal reference and `0.227533`
seconds for the Python full resimulation. This is a single reference observation,
not a performance headline or general speed claim. The scoped E3 claim is exact
history/event reuse. Native performance and locality breadth belong to E4 only
after this semantic gate.

## Paper-story consequence

The three-act route is now connected:

1. **E1 — A frame is not a future.** A registered visible present omits collision
   correlation that can determine the echo.
2. **E2 — A slider is not a history.** Collision dose grades recovery, but the
   structured budget does not identify special wiring beyond its controls.
3. **E3 — Make the past editable.** An animator can select one collision, apply a
   conservative edit, and obtain a second exact future while reusing the independent
   part of history.

E2's full negative remains in the supplement. Its main-text role is one honest
turn: “More collisions bring back more echo. But a slider cannot tell us which
cause to edit. So we made every collision addressable.”

## Render audit

The main figure shows, in order: fork state and selected pair, addressable timeline,
the one-degree edit, original world, edited world, and the runtime causal set. The
neutral split-screen video is `15.75` seconds.

The render manifest records:

- fixed orthographic camera and identical world coordinates;
- identical physical frame times and particle display;
- passive colors inherited from E1;
- a simulator-applied physical edit;
- no renderer mutation of physical state;
- no temporal interpolation;
- no post-hoc particle correction.

## Claim boundary after E3

Supported for the frozen Hero:

- addressable collision events, predecessor/descendant queries, checkpoints, and
  state hashes;
- one conservative pair-relative-velocity edit;
- exact causal recomputation against full resimulation;
- `75.238%` baseline-event reuse with a `25.781%` peak affected fraction;
- a physically recomputed, manifest-locked visual fork.

Not supported yet:

- every edit remains local;
- a broad runtime speedup or interactive native performance;
- generic geometry, rigid-body, or fluid editing;
- authoring benefit established by a user study;
- an implementation of the Deng–Hani–Ma cutting proof;
- a successful E2 molecule-wiring mechanism.

These are not missing “safety experiments” for E3. They are possible E4–E6
extensions after the core story has passed.

## Frozen artifact hashes

Artifacts are generated under `results/molecular-time-machine-e3-v0/` and excluded
from Git by policy. The compact hashes are committed here.

| Artifact | SHA-256 |
|---|---|
| `run-manifest.json` | `559319b700ee111d29368da406a164e6daef36d874902446f03a45c5277871c6` |
| `summary.json` | `5efed8f5583abc1ca7c3d643c6ca8dedf935df8b9a49c3cd54d48f66eeeafd87` |
| `collision-timeline.jsonl` | `08daaaf3c6d8910b3bc2051cac90e9e03c4cc644a469fcc3e3ac7c291f888064` |
| `checkpoints.json.gz` | `325db862e9ea88152898cb992509c3ac2d34e830742e5c6349ceabddb1306f54` |
| `edit-manifest.json` | `03f31a2204742d005affc57960c4b41e4bb58f0f58a85faaaddf4eda94041d1d` |
| `branch-events.jsonl` | `ec5e7c23e1ac278913754c6ea39b56bd00df1f07367fd7e5536653fc6c51dd80` |
| `causal-cone.json` | `ef2e1cd8f12e084fed11d22ba169b016cde4fd4fdaf53b6926a577b3c7a12cee` |
| `branch-comparison.json` | `df145939a66c04c88f9c2f0cdac1aa65d742751888b4e3a9c0f76d6dcb746cc8` |
| `figure-one-collision-two-worlds.svg` | `2f2d1b2a2a9097855d896bff4e79c7f4a83deb2cb4ad47be6ff1f212811bcf9f` |
| `figure-one-collision-two-worlds.pdf` | `899e5984d7d59cd5785c6674302d6e07c0c337c5a9ee04c65ec2fb472011af7c` |
| `one-collision-two-worlds.mp4` | `c1ac982a5d80a4953ef91fd23f76346abb031e7c0220d441a8593c3871f80d66` |
| `render-manifest.json` | `df60eda8ef801bf759125d72b9c8b66b585f72e41d3cf57ac5570186670a0bdb` |
| `two-world-trajectories.json.gz` | `4a33f5273ec2ca75c36fdcefc5ff379e4840d34d5d755eff6a94dd088224b255` |

The E3 protocol SHA-256 is
`ce9943e9bb367810bb8baa62a00635180f3006dceedf36bb79c055aa44868f1d`.
