# Molecular Time Machine E4 result — Choose the Cause, Direct the Future

**Decision:** `go`.

**Study:** `MOLECULAR-TIME-MACHINE-E4-v0`.

**Frozen recipe tag:** `molecular-time-machine-e4-recipe-v0`.

**Evidence commit:** `d5e4086ae0296647b1ba60e6602dfd0816feaf2f`, recorded with a
clean worktree by the run manifest.

## Result in ordinary language

E3 showed what happens after a paper hands an animator one past collision. E4 makes
that collision discoverable from the other direction.

The creator began at the recovered Molecular E, selected its upper horizontal
stroke, and thereby selected foreground particles `69`, `76`, `101`, and `106`.
Without inspecting any counterfactual result, the system traced these particles
through the original collision DAG and ranked the first 16 historical collisions by
how much of the target they reach and how much unrelated history they include.

The top recommendation was collision `#4`, pair `(101,111)`, at
`t=0.05512038650510776`. It covers two of the four target particles in its baseline
descendants. Collision `#2`—the hand-selected E3 Hero—is the second recommendation,
which is useful evidence that the E4 result is not simply replaying E3's answer.

The interaction exposed 12 cached exact local previews: four conservative velocity
angles for each of the three ranked collisions. The registered angle rule saved
`−1°` for collision `#4`. In the resulting future, target particles `76` and `101`
leave the selected upper stroke: **2 of 4 target particles (`50%`)**. Only one of the
other eight foreground E particles leaves the overall E pattern: **`12.5%`**. The
target-to-collateral ratio is therefore **`4.0x`**.

This is the required product moment: the user first points at a desired consequence,
then the system identifies a past physical cause that changes that consequence more
than the rest of the visible structure.

## Causal steering session

```text
select upper E stroke
→ rank original-history collisions #4, #2, #12
→ browse four exact angles for each candidate
→ select collision #4 at −1°
→ save one branch and verify it once
```

The ranking saw only baseline ancestry. It did not run edited branches to decide
which collision to recommend. The branch palette is part of the creator operation,
not a broad parameter study.

| Rank | Baseline collision | Target coverage | Target purity | Causal score |
|---:|---|---:|---:|---:|
| 1 | `#4`, pair `(101,111)` | `50%` | `13.333%` | `0.210526` |
| 2 | `#2`, pair `(101,118)` | `50%` | `10.000%` | `0.166667` |
| 3 | `#12`, pair `(61,111)` | `25%` | `7.692%` | `0.117647` |

The 12 local previews had a median reference time of **`0.074740 s`**, under the
registered `0.20 s` interaction gate. This is a bounded Python-reference
observation for the Hero, not a native-performance or broad scaling claim.

## One saved branch, one exact reference

Every preview uses the same conservative physical causal scheduler as E3. To avoid
turning the authoring palette into a set of unnecessary global checks, only the
saved collision-`#4`, `−1°` branch launches the complete resimulation oracle.

The saved local branch and full reference have the same `100` post-fork collision
pairs in the same order. Their maximum event-time difference is `2.008027e-11`; the
terminal position and velocity RMS errors are `6.568849e-11` and `7.335171e-10`.
The edit preserves pair kinetic energy exactly and has momentum error
`9.155134e-16`.

The branch directly reuses `79/103` baseline collisions (`76.699%`). It invalidates
24 obsolete events, computes 21 new events, and its affected set peaks at `28/128`
particles (`21.875%`). These are supporting facts for one authoring session, not a
claim that all future edits will remain local.

## Frozen gate

| Check | Frozen threshold | Result | Status |
|---|---:|---:|---|
| target ejection | `>= 0.50` | `0.500000` (`2/4`) | pass |
| target/collateral ratio | `>= 2.0` | `4.000000` | pass |
| exact-preview median | `<= 0.20 s` | `0.074740 s` | pass |
| saved-branch event reuse | `>= 0.50` | `0.766990` (`79/103`) | pass |
| local/full collision-pair agreement | `1.0` | `1.000000` (`100/100`) | pass |
| maximum collision-time error | `<= 1e-9` | `2.008027e-11` | pass |
| terminal position RMS | `<= 1e-9` | `6.568849e-11` | pass |
| terminal velocity RMS | `<= 1e-9` | `7.335171e-10` | pass |
| edit momentum error | `<= 1e-12` | `9.155134e-16` | pass |
| edit energy error | `<= 1e-12` | `0.0` | pass |

All gates pass, so E4 may use the scoped term **causal steering** for this Hero.

## Visual and interaction evidence

The canonical package contains three linked outputs:

- `figure-causal-steering.svg/.pdf` — selected terminal stroke, past-collision
  ranking, original/edited future, and concise steering card;
- `causal-steering-erase-one-stroke.mp4` — a neutral 15.75-second split view of the
  original and directed physical branches under the same camera and times;
- `causal-steering.html` — a self-contained local browser artifact. It lets a
  reviewer select one of the three baseline-ranked collisions and browse its four
  cached exact preview branches.

The browser does not modify simulation state or pretend that canvas rendering is a
physical edit. The render manifest records cached exact local previews, a
simulator-applied edit, no temporal interpolation, no post-hoc correction, and one
full-reference check for the saved branch.

## Story consequence

The active paper spine is now a four-act argument:

1. **E1 — A frame is not a future.** The visible resolved present omits collision
   correlation that can change the echo.
2. **E2 — A slider is not a history.** Collision dose changes recovery, but does
   not identify a special causal wiring beyond its controls.
3. **E3 — Make one past collision editable.** A conservative microscopic edit
   creates an exact second future while reusing independent history.
4. **E4 — Choose the cause, direct the future.** A creator starts from a desired
   terminal feature; baseline ancestry locates a past collision, and an exact small
   preview palette lets them steer a scoped visual outcome.

The claim remains deliberately narrow. This result does not establish a generic
optimizer, a user study, geometry editing, native acceleration, or locality for all
edits. Those are not missing checks for E4; they are separate possible future work.

## Frozen artifact hashes

Artifacts were generated under `results/molecular-time-machine-e4-v0/` and are
excluded from Git by repository policy. The run manifest records the compact hashes:

| Artifact | SHA-256 |
|---|---|
| `authoring-session.json` | `4654fe8501477fe4ae73f4e72aeccde3bbfd7322bac12ff8b6110ab9f6c1a5a4` |
| `branch-palette.json` | `3a0af0a7aaea91dd68646c512d16adf4983cb915311a61a1d2fe93161da6ab66` |
| `causal-target.json` | `7b999fc12819e482514a76176e144fa0a6c7b59a667781a8286d155f719230c9` |
| `collision-ranking.json` | `bfc77a6bbbc1136ba2bac106ba2bbaf251d1010b02a6c207d2baeea3d5ca020f` |
| `selected-edit-manifest.json` | `c42d52aeb292def037d8f91f21d0ae0a50b8f75f816e21f4aaec9035d2e125bc` |
| `selected-causal-cone.json` | `bd160fe52af08f168f102099ba76e8345eecd52b7c0b07233c7b403ff7cffc50` |
| `selected-branch-comparison.json` | `055320c97a2d15fc43d41825cbb6e233ca485c74d8f19572487b974141bebce4` |
| `figure-causal-steering.svg` | `0ebefe9341c79a53c0cc31c15520f5f3c45fa52be105c1c9f027a4096711398c` |
| `figure-causal-steering.pdf` | `eefdd181fc179ec9fbe06a73133850cdec8bdff38654b1548982d5862b594d24` |
| `causal-steering-erase-one-stroke.mp4` | `aaa6345ca267d038bbf2457ac59c7393255296904fa514df028adebed00e2556` |
| `causal-steering.html` | `c060fd0afe02d3464385625ea4c2f1ba55515b5d6767238c009d10145ac4841e` |
| `render-manifest.json` | `9f1744f49ac23acb58c278ed7de47de565a52c2721fee2c21948424420025730` |
| `causal-steering-trajectories.json.gz` | `8112fafa8106d3da91072b726f106ccd1ad70306df6c705a4b3d0689765e4203` |
| `run-manifest.json` | `efff964da50446f017181a1dc13ce9cdba0313a01ad6240b84bf64bbdd0a9f0a` |

The frozen E4 protocol SHA-256 is
`f94b0ad61a26c4b09944162d8748c7dfc03ae4c005f87d80f981846f1d4ed5ac`.
