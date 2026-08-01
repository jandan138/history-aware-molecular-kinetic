# Molecular Time Machine E5 result — Same Present, Chosen Future

**Decision:** `go`.

**Study:** `MOLECULAR-TIME-MACHINE-E5-v0`.

**Frozen recipe tag:** `molecular-time-machine-e5-recipe-v0`.

**Evidence commit:** `2e12520c6c825f3b8554fcec41e8214233e7a102`, recorded with a
clean worktree by the run manifest.

## Result in ordinary language

E1 showed that a visible resolved frame does not uniquely specify its future. E5
turns that information boundary into one creator operation.

The creator first inspected the exact physical future, where the passive-color
particles recovered the Molecular E, and selected the horizontal extension of its
middle stroke. The system returned to the reverse branch at `t=0.80`. At that
moment the letter was not yet visible. Original and edited branches had exactly the
same particle positions, passive colors, radii, masses, IDs, and weights.

The frozen palette contained 30 legal surgeries: one or two particle-disjoint
velocity transpositions between selected target particles occupying the same
declared `4×2` cell. Every option ran complete EDMD from the common pivot. Among
the candidates retaining at least 90% of the rest of the E, the registered rule
selected swaps `(48,82)` and `(174,211)`.

Only four of 256 particles (`1.5625%`) changed velocity ownership. The target
middle-stroke region fell from eight foreground particles to two: a **75% geometric
reduction**. Six of the eight original target particles left the region, also
`75%`. All 19 non-target foreground particles remained inside the E pattern:
**100% collateral glyph retention**.

The matched visual shorthand is therefore **E → C**. The operational claim is the
more precise one: a sparse hidden surgery selectively suppresses the chosen middle
stroke while preserving the declared present and the rest of the glyph.

## Same declared present

The selected surgery changes velocity ownership, so it does not claim the same
exact microstate. It does establish the frozen resolved-state contract:

| Pivot property | Result |
|---|---:|
| positions identical | yes |
| passive colors identical | yes |
| radii, masses, IDs, and weights identical | yes |
| complete velocity multiset identical in every declared `4×2` cell | yes |
| target-conditioned velocity multiset identical in every declared cell | yes |
| valid geometry | yes |
| mass error | `0` |
| momentum error | `3.552714e-15` |
| energy error | `0` |

Because each edit exchanges complete velocity values inside one cell, the declared
cellwise velocity distribution is an exact operator invariant rather than a fitted
moment approximation. The allowed phrase is **same declared `4×2` resolved
present**, not same exact state or same distribution at arbitrary resolution.

## Authoring session

```text
inspect the original future E
→ select the middle-stroke extension
→ return to the common t=0.80 visible present
→ generate 30 legal same-cell velocity-ownership previews
→ require at least 90% collateral glyph retention
→ select (48,82) + (174,211)
→ play matched E and C-like physical futures
```

The 30 complete-EDMD previews had a median Python reference time of
`0.302616 s`. This is recorded for transparency only. E5 makes no interactive
latency, native-performance, local-recomputation, or scaling claim.

## Pivot replay continuity

Before applying surgery, a fresh EDMD run from the stored `t=0.80` pivot reproduced
the original terminal branch with:

- `1.0` collision-pair agreement;
- terminal position RMS `1.028478e-13`;
- terminal velocity RMS `1.879095e-12`.

This confirms that the common pivot is a valid continuation state rather than a
rendered or snapped frame.

## Frozen gate

| Check | Frozen threshold | Result | Status |
|---|---:|---:|---|
| target-particle ejection | `>= 70%` | `75%` (`6/8`) | pass |
| target-region reduction | `>= 70%` | `75%` (`8→2`) | pass |
| collateral foreground retention | `>= 90%` | `100%` (`19/19`) | pass |
| touched particles | `<= 4` | `4/256` | pass |
| positions / colors unchanged | exact | exact | pass |
| declared cell velocity multisets | exact | exact | pass |
| target-conditioned cell velocity multisets | exact | exact | pass |
| valid geometry | required | yes | pass |
| pivot replay collision pairs | `1.0` | `1.0` | pass |
| pivot replay position RMS | `<= 1e-9` | `1.028478e-13` | pass |
| pivot replay velocity RMS | `<= 1e-9` | `1.879095e-12` | pass |
| mass / momentum / energy error | each `<= 1e-12` | `0 / 3.55e-15 / 0` | pass |

All registered checks pass, so E5 may use **Same Present, Chosen Future** for this
Hero and the scoped C20 future-authoring claim.

## Visual and interaction evidence

The canonical package contains:

- `figure-same-present-chosen-future.svg/.pdf` — selected future stroke, common
  pivot, exact resolved-present contract, and matched E/C futures;
- `same-present-two-letters.mp4` — a neutral 15.75-second matched comparison. Both
  sides are identical through the pivot, after which complete physical futures
  separate;
- `same-present-chosen-future.html` — a self-contained browser artifact containing
  the 30 cached complete-EDMD terminal previews.

The browser does not run physics or move particles. The renderer uses identical
camera, particle radius, passive colors, and time samples, with no terminal
correction or compositing.

## Story consequence

The active paper spine is now a five-act argument:

1. **E1 — A frame is not a future.** A declared one-particle present omits
   collision correlation that can change the echo.
2. **E2 — A slider is not a history.** Collision dose grades recovery, but does not
   identify special molecule wiring beyond its controls.
3. **E3 — One past collision is editable.** A conservative microscopic edit
   creates an exact alternate world with reusable independent history.
4. **E4 — A desired future can locate its cause.** A creator selects a terminal
   feature and baseline ancestry recommends an editable past collision.
5. **E5 — The same present can be authored into a chosen future.** Four particles
   exchange hidden velocity ownership; the frame stays fixed while E becomes C-like.

This closes the scientific and creator-facing loop. E5 does not establish a generic
glyph optimizer, arbitrary targets, exact-microstate equality, multi-step editing,
a user study, 3D, or broad performance. Those are not missing E5 checks.

## Frozen artifact hashes

Artifacts were generated under `results/molecular-time-machine-e5-v0/` and are
excluded from Git by repository policy. The run manifest records:

| Artifact | SHA-256 |
|---|---|
| `decision.md` | `1bee95327a1fb5360964cfdb67d776347821427471f3c5920b5b871332c05443` |
| `figure-same-present-chosen-future.pdf` | `aa6fb7c8bd37581a32f19e57aa599cb9d77765f5fb5957feeb2adee4b9ff6b01` |
| `figure-same-present-chosen-future.svg` | `115afdeda7373e5b8d5bbbfdc1aead970b34db706f09c82ac683495002a422aa` |
| `future-target.json` | `afe44286fcfbeefa2784403eea8e01c50a60cb923e586e84ebd5e8a0d75bc610` |
| `pivot-replay-audit.json` | `04fcd8665eac68dbc52cae86b0414c0a8abfb4d192dae4726c723ae89e84d1f2` |
| `render-manifest.json` | `5f3292f9954e43e618e0a80799969c9e95c449abb24d3179c273e14aed2ecf97` |
| `resolved-present-audit.json` | `a36a310ea80e1ba495da77fca4c8608745e2e794c70ca05c1cd134b5588ed7a2` |
| `same-present-chosen-future.html` | `ae74a761c785f41fcf20f17431d242d64af124f86c2eedb5ed07afbe50439d46` |
| `same-present-trajectories.json.gz` | `1c34a4a079d457d8b28c3f7b9a7f4095315c4d24dc7eafc36a75c441e6f46724` |
| `same-present-two-letters.mp4` | `6cfef859f33c11ecad8db4b586395146112c736f1b795f21bcfe58a29d6a76c5` |
| `selected-surgery-manifest.json` | `331aa33111ed2813887b7b6b557c9f16029f7e81897e5869a90a3a5ab40ea104` |
| `summary.json` | `c79ef098424b673105b0f0e69e1a41232f035700a27a74d29163981d57eadee8` |
| `surgery-preview-palette.json` | `6e892e225b929a75fd2ad067f538670b32bfb50cc96222b8a5c27a04eb834c42` |

The frozen E5 protocol SHA-256 is
`fb0977a745cfcf21518eef4265c952955b073def2ef84729d7a6b0dd182ccf47`.
