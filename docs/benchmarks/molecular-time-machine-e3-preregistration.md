# Molecular Time Machine E3 — frozen recipe

**Status:** preregistered implementation recipe; canonical evidence must be created
after tag `molecular-time-machine-e3-recipe-v0`.

**Study ID:** `MOLECULAR-TIME-MACHINE-E3-v0`.

## The one question

Can a one-degree physical edit to one past collision create a visibly different
future while an exact causal branch reuses most unaffected collision history and
matches a complete resimulation?

This is a story gate, not a parameter study. There is one frozen Hero, one edit,
and one necessary full-resimulation reference.

## Canonical scene

The scene inherits the frozen E1 `N=128`, seed `0`, exact-reverse branch. The target
is zero-based collision ordinal `2`, pair `(101,118)`, expected at
`t=0.03429093183046455`. A forced checkpoint is placed `1e-6` before that event.

At the checkpoint, rotate the pair relative velocity counterclockwise by `+1°` in
the pair center-of-mass frame. Do not change positions. The construction must
preserve pair momentum and kinetic energy. Run both the causal branch and the full
reference to `t=1.0`, with registered output samples every `0.02` time units.

The repository configuration is
`configs/studies/molecular-time-machine-e3-v0.json`.

## Exact causal-branch rule

The affected set starts with the edited pair and only grows.

1. Restore the fork checkpoint and apply the registered edit.
2. Recompute collision candidates for pairs touching an affected particle.
3. Reuse a baseline event when both participants remain unaffected.
4. Invalidate a baseline event as soon as either participant is affected; promote
   the other participant and skip the obsolete impulse.
5. When a newly computed affected–unaffected collision occurs, promote the latter
   particle and continue.
6. If independence is uncertain, promote the particle. The exact route never
   truncates an uncertain cone.
7. Use the same prediction, advection, elastic impulse, and event-order kernel as
   full EDMD.

## Registered readouts

The story has three numbers:

- **world split:** baseline terminal passive-color score minus edited score;
- **history reuse:** reused post-fork baseline events divided by all post-fork
  baseline events;
- **causal reach:** maximum affected particles divided by `128`.

Correctness is measured by post-fork collision-pair agreement, maximum collision
time error, and terminal position/velocity RMS against the full resimulation.

## Frozen gate

| Check | Threshold |
|---|---:|
| baseline terminal passive-color score | `>= 0.99` |
| edited terminal color gap | `>= 0.15` |
| visibly changed particle fraction | `[0.15, 0.40]` |
| local/full collision-pair agreement | `>= 1.0` |
| maximum collision-time error | `<= 1e-9` |
| terminal position RMS | `<= 1e-9` |
| terminal velocity RMS | `<= 1e-9` |
| edit momentum and energy error | each `<= 1e-12` |
| baseline event reuse | `>= 0.50` |
| peak affected fraction | `<= 0.50` |

Decision:

- `go`: correctness, visible split, history reuse, and causal locality all pass;
- `narrow`: correctness and visible split pass, but reuse/locality does not;
- `stop_e3`: the local branch differs from full resimulation or the edit fails to
  produce the registered visible split.

## Evidence outputs

The canonical run writes:

```text
collision-timeline.jsonl
checkpoints.json.gz
branch-events.jsonl
edit-manifest.json
causal-cone.json
branch-comparison.json
summary.json
decision.md
two-world-trajectories.json.gz
figure-one-collision-two-worlds.svg/.pdf
one-collision-two-worlds.mp4
run-manifest.json
render-manifest.json
```

The figure and 15–20 second neutral video must use identical world coordinates,
frame times, particle display, and passive colors. The renderer may highlight the
causal cone but may not move particles, interpolate physical states, or correct the
edited outcome.

## Explicitly not in this gate

No additional E2 variants, seed sweep, density sweep, `N=512`, geometry edit, 3D
scene, GPU implementation, approximate cone, performance headline, or user study is
required. Those are future-paper investments only after this narrative gate passes.
