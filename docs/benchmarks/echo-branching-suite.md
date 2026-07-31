# Active E0–E6 Echo and Branching Benchmark Suite

This suite replaces dynamic molecular LOD as the active first-paper evidence ladder.
The older R0–B5 suite remains available as deferred infrastructure and negative
history.

```mermaid
flowchart LR
    E0[E0 Exact dynamics + reversal] --> E1[E1 Same resolved present]
    E1 --> E2[E2 Molecule-budget mechanism]
    E0 --> E3[E3 Addressable collision + exact causal branch]
    E3 --> E4[E4 Breadth + performance]
    E1 --> E5[E5 Correlation surgery]
    E2 --> E5
    E4 --> E6[E6 SIG graphics evidence]
    E5 --> E6
```

## E0 — Exact dynamics, numerical reversal, and replay primitives

### Question

Can the internal EDMD reproduce an exact forward/reverse experiment and a recorded
event segment within declared numerical tolerances?

### Cases

- two-disk analytic collision;
- periodic multi-disk gas at `N=128, 256, 512`;
- grazing-collision stress cases;
- near-simultaneous event-order cases;
- checkpoint/random-access replay.

### Evidence

- position/velocity return error;
- event-pair and event-time agreement;
- pre/post checksum agreement;
- invariant drift;
- replay latency versus checkpoint interval.

### Gate

No scientific echo or graphics branching claim proceeds if exact reversal is not
numerically trustworthy.

## E1 — Same resolved present, opposite futures

### Question

Can exact-reverse and chaotized-reverse branches match a preregistered finite
one-particle state while producing robustly different futures?

### Branches

```text
forward exact EDMD
exact reverse EDMD
resolved-state-preserving chaotized reverse EDMD
DSMC from the reversed resolved state
no-collision ghost baseline
```

### Audit

At pivot time, report matching over a grid of:

- spatial block sizes;
- velocity-bin resolutions;
- passive-color partitions;
- one- and two-moment summaries.

The claim is about the declared resolved present `f1_h`; it does not assert identical
exact microstates or continuous `f1`.

### Outputs

- normalized anisotropy/echo response;
- passive-color pattern recovery;
- future branch divergence;
- multi-resolution pivot mismatch;
- seed uncertainty.

## E2 — Collision-molecule budget and mechanism controls

**Result:** complete with `stop_e2`. The registered budget ladder is systematic,
but `(4,0)` does not outperform count/time-matched random or topology-shuffled
controls. The topology-beyond-dose interpretation is closed; see the
[E2 result](molecular-echoes-e2-result.md).

### Question

Does a structured collision-history budget explain echo recovery beyond the trivial
effect of allowing more collisions?

### Dynamics

- full exact EDMD;
- `(Lambda, Gamma)` paths such as `(4,0)`, `(8,0)`, `(16,1)`;
- no-collision ghost dynamics;
- count/time-matched random collision suppression;
- topology-shuffled collision partners.

### Required evidence

- forward and reverse budget-response curves;
- collision count/time distributions;
- incoming-pair closure-defect proxy;
- branch observable error relative to full exact;
- uncertainty across seeds and `N`;
- small fixed-`N epsilon` sequence if the finite-system mechanism passes.

### Gate

A molecule-budget claim fails if random suppression or a collision-count-only model
explains the same response.

## E3 — One addressable collision, two exact worlds

### Question

Can the event multigraph serve as a correct provenance index **and** drive an exact
counterfactual branch after one past-collision edit?

### Cases

- frozen E1 `N=128`, seed `0` exact-reverse Hero;
- collision ordinal `2`, pair `(101,118)`;
- forced checkpoint `1e-6` before contact;
- `+1°` pair-relative-velocity rotation in the center-of-mass frame;
- exact expanding affected set and complete-resimulation reference.

### Evidence

- stable event IDs, causal predecessors, state hashes, and checkpoints;
- local/full collision pair and time agreement;
- terminal position and velocity agreement;
- conserved edit momentum and energy;
- terminal visual split, reused baseline events, and peak affected fraction;
- one locked figure/video manifest.

### Gate

The graph passes only if it performs the branch. The frozen thresholds and artifact
list are in the [E3 recipe](molecular-time-machine-e3-preregistration.md).

## E4 — Breadth, performance, and additional edit families

### Question

After the single-collision Hero passes, over what edit ages, densities, and edit
families does causal reuse remain useful, and when does a native implementation
deliver interactive latency?

### Edits

1. later or larger pair edits;
2. a second physical edit family;
3. optional simple obstacle/aperture edits;
4. native/parallel implementation after semantics are frozen.

### Baselines

- full resimulation from the checkpoint;
- full state duplication per branch;
- replay-only video editing, which is not physically recomputed;
- approximate fixed-radius local recomputation.

### Evidence

- local-vs-full terminal state/event error;
- affected particle and event fractions over time;
- runtime and storage;
- fallback-to-full frequency;
- scaling with edit age and density.

### Gate

The local algorithm must never claim exactness when it truncates an uncertain cone.
It either expands the cone, marks the result approximate, or falls back to full
replay.

## E5 — Resolved-state-preserving correlation surgery

### Question

Can a user alter hidden correlations while preserving the declared visible present,
and thereby author a different future?

### Operators

- block+color velocity permutation;
- constrained moment matching;
- optional finer-scale assignment minimizing `f1_h` mismatch;
- partial history retention or molecule-targeted surgery.

### Evidence

- multi-resolution resolved-state audit;
- mass/momentum/energy preservation;
- overlap validity;
- branch divergence under the same renderer;
- controllability and repeatability;
- comparison with random surgery of equal magnitude.

## E6 — SIG graphics evidence

### Hero scenes

1. **Molecular Logo Echo** — the same resolved pivot produces recovery or continued
   mixing depending on hidden history;
2. **One Collision, Two Worlds** — one past event forks two futures and the causal
   influence spreads through the event graph;
3. **Edit the Past** — a past geometry edit reuses unaffected history and
   recomputes only the future cone.

### Required comparison discipline

- shared camera, renderer, display density, and frame times;
- no backward video used as a substitute for simulated reversal;
- original branch, edited branch, local recomputation, and full-resimulation
  reference linked to frozen runs;
- causal graph and diagnostics explain the physical branch rather than create the
  visual difference;
- every primary shot has a render manifest and quantitative evidence link.

### Primary graphics metrics

- visible echo/branch divergence;
- local-vs-full correctness;
- branch latency and storage;
- causal-cone fraction;
- interactive response time;
- temporal continuity;
- reviewer-visible contribution without debug overlays.

## Deferred R0–B5 suite

The following remain valuable but are no longer the active dependency chain:

```text
R0 external oracles
B0 exact/kinetic primitives
B1 discrepancy atlas
B2 history predictor
B3 representation conversion
B4 dynamic LOD
B5 old LOD graphics scenes
```

R0/B0 continue to support solver trust. The Phase-I B2 result remains recorded as an
exploratory negative. B3–B5 are deferred until a future project reopens the LOD
question with new evidence.

## Case lifecycle

```text
candidate -> preregistered -> smoke -> converged -> reviewed -> frozen -> evidence
                                     \-> retired with reason
```

A preregistration commit/tag must precede result generation for E1 and E2 primary
evidence.
