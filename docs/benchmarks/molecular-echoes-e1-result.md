# Molecular Echoes E1 Result

**Decision:** `go` on 2026-07-31 for the preregistered, finite-resolution E1
claim.

**Protocol:** `MOLECULAR-ECHOES-E1-v0`, frozen at commit
`3da4eb203cd2daeeee23c56fe193557890662844` and annotated tag
`molecular-echoes-e1-preregistered-v0` before any primary result was generated.

## The result in one picture

A passive-color letter E is first dispersed by exact hard-disk dynamics. At the
pivot, the exact-reverse and chaotized-reverse branches have identical particle
positions and exactly the same declared 4×2 block-and-color velocity histogram.
The chaotized branch changes the hidden position–velocity pairing by permuting
reversed velocities within each block and passive-color class.

Both branches are then simulated forward. The exact-reverse branch reconstructs
the E; the chaotized-reverse and DSMC branches remain mixed. This is a molecular
echo, not a reversed movie and not a post-render particle correction.

The E1 result supports the paper's first scientific beat:

> A finite-resolution one-particle present does not determine this visible future
> response; microscopic pairing information discarded by the resolved description
> can carry the echo.

E1 does **not** yet identify collision-molecule topology as the mechanism. That is
the single purpose of E2 and its count/time-matched null controls.

## Frozen experiment

| Item | Registered value |
|---|---|
| Geometry | periodic 2D domain, `[0,4] × [0,2]` |
| Systems | `N=128, d=0.04` and `N=256, d=0.02` |
| Seeds | `0–5` for each system, 12 cases total |
| Preparation / future | `1.0 / 1.0` time units |
| Sampling | `0.02` time units |
| Construction state | 4×2 spatial blocks, passive-color partition |
| Audit states | 2×1, 4×2, and 8×4 spatial grids; 4 and 8 velocity bins |
| Primary readout | passive-color E recovery |
| Main branches | forward, exact reverse, chaotized reverse |
| Supporting branches | DSMC reverse; ballistic ghost as a diagnostic only |

The chaotization uses a deterministic Sattolo permutation within each
`(4×2 cell, passive color)` group. It therefore changes almost every particle's
velocity assignment without changing the registered construction histogram or
global invariants.

## Main numbers

| Quantity | `N=128` | `N=256` |
|---|---:|---:|
| Pivot color score, mean | 0.542864 | 0.570464 |
| Exact-reverse terminal score, median | 1.000000 | 1.000000 |
| Chaotized terminal score, mean | 0.548851 | 0.551582 |
| DSMC terminal score, mean | 0.549569 | 0.596231 |
| Exact-minus-chaotized gap, mean | 0.451149 | 0.448418 |
| Minimum changed-particle fraction | 0.976562 | 0.992188 |
| Maximum reverse position RMS error | 3.54e-8 | 2.77e-6 |
| Maximum reverse velocity RMS error | 2.03e-7 | 4.92e-5 |

Across both particle counts, the exact-minus-chaotized terminal gap is
`0.449784`, with a seed-bootstrap 95% interval of
`[0.436573, 0.460660]`. Every registered case is positive; the casewise range is
`[0.339080, 0.514368]`.

The exact-minus-DSMC terminal gap is also positive in every case, with a range of
`[0.365288, 0.510057]`. DSMC is supporting evidence that a history-forgetting
kinetic branch loses the visible echo; it is not, by itself, proof of the E2
collision-molecule mechanism.

## Preregistered gate

| Check | Registered threshold | Observed worst case | Result |
|---|---:|---:|---|
| Mirrored collision-pair agreement | exactly 1.0 | 1.0 | PASS |
| Reverse position RMS | ≤ 1e-5 | 2.77e-6 | PASS |
| Reverse velocity RMS | ≤ 1e-4 | 4.92e-5 | PASS |
| Mean pivot color score per `N` | ≤ 0.70 | 0.570464 | PASS |
| Median exact terminal score per `N` | ≥ 0.98 | 1.000000 | PASS |
| Changed-particle fraction | ≥ 0.80 | 0.976562 | PASS |
| 4×2 construction total variation | ≤ 1e-12 | 0.0 | PASS |
| Global invariant mismatch | ≤ 1e-12 | 5.57e-17 | PASS |
| Mean exact-chaotized gap | ≥ 0.30 | 0.449784 | PASS |
| Bootstrap interval lower bound | > 0.20 | 0.436573 | PASS |
| Every case has a positive gap | required | minimum 0.339080 | PASS |

The decision rule therefore returns `go`, and the DSMC support rule is also true.

## What “same present” does and does not mean

For all 12 cases and both registered velocity binnings:

- the 2×1 audit has total variation `0.0`;
- the construction 4×2 audit has total variation `0.0`;
- count, momentum, energy, and anisotropy mismatches at those resolutions are zero
  up to floating-point roundoff.

The unused 8×4 audit deliberately exposes the resolution boundary. Its total
variation ranges from `0.468750` to `0.648438` with four velocity bins and from
`0.648438` to `0.734375` with eight velocity bins. The finer subcell
position–velocity pairing is therefore different.

The supported wording is **“same preregistered 4×2 resolved one-particle
present.”** E1 does not support “same exact state,” “same continuous `f1`,” or a
resolution-independent equality claim. The fine-grid result is part of the main
disclosure, not a hidden robustness failure.

## Visual and provenance audit

The main figure and neutral video are generated from stored trajectories with one
fixed orthographic domain and identical particle display across branches. The
render manifest records:

- no temporal interpolation;
- no video reversal;
- no post-hoc particle correction;
- no mutation of the simulated physics state.

The neutral video is 1280×720 H.264 at 24 fps, 276 frames, and 11.5 seconds. Its
hero case is `N=128, seed=0`; the pooled curve and numerical decision use all 12
cases.

| Provenance item | Value |
|---|---|
| Study content ID | `echo-e1-48777e948d046ad1` |
| Clean run commit | `3da4eb203cd2daeeee23c56fe193557890662844` |
| Working tree at run time | clean |
| Protocol SHA-256 | `8b2268669697eae205c4c8bf08db9704b73ac5317cde94c8b8d3f554ac30e5e4` |
| Run-manifest SHA-256 | `60e8e5640f5646e0a5257486855f0f04c140770c9bdbb6062ff3f3276529e252` |
| Result tag | `molecular-echoes-e1-result-v0` |

Core artifact hashes:

| Artifact | SHA-256 |
|---|---|
| `summary.json` | `efdfe4e764053cfc87e9c5e10d9c990b9bd5375f8091625df97aae3739dabce5` |
| `reversal-audit.json` | `fd0ee64b605898d628b5a0e7eb29536a3cfd4aaed8d7c664d92cb8731d631317` |
| `pivot-audit.json` | `7eff7571d26f6d2cec1bd158f2a14b4654e90ef3376a7b0f9d64a8776f03aa1a` |
| `branch-metrics.jsonl` | `7f4cb8b67537d45a0f872e69430a515c96b4854c6e68da686ee2685bd4236597` |
| `particle-trajectories.npz` | `cdcb8aa7d688eae571180388a4e4b6156984347e06040aaa0fb39756927b0f07` |
| `figure-e1-main.svg` | `1275d1e4dc81719293645173b5c5d93909e3941ace7183ad853f5f8bc9f7a528` |
| `figure-e1-main.pdf` | `c6dc0d7c98fcfed3c0052ca86d9e92eca2c8539633bd1ed6b0678d8de455fc94` |
| `echo-e1-neutral.mp4` | `ead6228ff06a081872277b96bd4a23742909ede3a8f18bcbebd41146abdeed2d` |
| `render-manifest.json` | `4cea17fe18fe9e0e5ce278935a826f31362577ff3d022da8d0b09a375ddd2ce6` |

Large generated artifacts remain under ignored `results/`; this compact page and
the frozen hashes are committed. Reproduce them with:

```bash
PYTHONPATH=src python scripts/run_echo_e1.py \
  --config configs/studies/molecular-echoes-e1-v0.json \
  --output results/molecular-echoes-e1-v0
```

## Decision and next step

E1 is closed as a positive, scoped result. The next experiment is E2: test whether
a structured collision-molecule budget explains the lost response better than
collision-count/time-matched and topology-shuffled controls.

No extra E1 grid search, seed search, `N=512` confirmation, or 3D production is
needed before that mechanism gate. `N=512` remains an optional scale follow-up only
if E2 succeeds. If E2 fails its null controls, the paper must narrow the mechanism
claim rather than compensate with more E1 variants.
