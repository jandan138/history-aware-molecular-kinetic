# Go / No-Go Gates

These gates govern the active Molecular Echoes route. The old dynamic-LOD gates are
retired with the Phase-I predictor result.

## Gate G0 — Numerical reversal and replay trust

**Go:**

- forward/reverse return error is below preregistered tolerance;
- event ordering is deterministic under the declared policy;
- checkpoint replay reproduces event/state checksums;
- grazing and near-simultaneous failures are characterized;
- invariant drift is bounded.

**No-Go:**

- the exact branch does not reliably reconstruct its own past;
- the result depends on manually repaired trajectories;
- a backward video is used instead of simulated reversal.

## Gate G1 — Same resolved present

**Go:**

- exact-reverse and chaotized branches pass the preregistered `f1_h` audit;
- matching is reported across multiple spatial and velocity resolutions;
- mass, momentum, energy, color counts, and overlap validity pass;
- future separation survives finer audit resolutions and seed variation.

**No-Go / narrow:**

- future separation disappears when the audit is refined;
- only one arbitrary binning supports the story;
- “same present” is stated more strongly than the measured resolved state.

## Gate G2 — Collision-history mechanism

**Observed E2-v0 decision:** **No-Go.** The budget response is systematic, but the
structured branch does not outperform either registered control; the incoming-pair
proxy is non-discriminating at this scope. The molecule-topology mechanism is
removed from the paper spine. E3/E4 can proceed only as a narrower graphics-system
route.

**Go:**

- `(Lambda,Gamma)` history budgets produce a systematic response;
- forward and reverse branches respond differently as preregistered;
- count/time-matched random suppression cannot explain the result;
- topology-shuffled controls are weaker;
- incoming-pair closure readout changes in the expected direction.

**No-Go / narrow:**

- the result is explained by collision count or mean free path alone;
- molecule labels are post-hoc and not reproducible;
- extended dynamics are presented as exact EDMD;
- only a visually attractive echo remains.

If G2 fails but G0/G1 pass, retain the echo as a demonstration and remove the
Deng-inspired mechanism claim from the paper spine.

## Gate G3 — Addressable collision and exact Hero branch

**Observed E3-v0 decision:** **Go.** All `106` post-fork collision pairs agree with
full resimulation, `79/105` baseline events are reused, peak affected fraction is
`33/128`, and the terminal color gap is `0.188218`.

**Go:**

- event predecessors/successors match the raw ledger;
- repeated-pair events are preserved;
- shared-ancestor and descendant queries are correct;
- the graph drives baseline-event reuse and invalidation;
- branch/checkpoint provenance is complete.
- the local branch matches full resimulation within the frozen tolerances;
- the registered one-event edit creates the visible split.

**No-Go:**

- the graph is only a visualization and cannot drive replay/branching;
- event log and branch state can diverge silently;
- random access requires storing full frames without an honest baseline.

## Gate G4 — Breadth and performance after the Hero

**Go:**

- E3 exact semantics remain unchanged in a native/optimized path;
- a second edit family or targeted edit-age range has useful locality;
- runtime/storage evidence supports only the breadth claim actually made;
- global-cone cases narrow the claim instead of triggering more E3 experiments.

**No-Go:**

- optimized execution changes the frozen physical result;
- every added edit immediately becomes global and offers no authoring value;
- a wall-clock headline is based only on the Python Hero observation.

## Gate G5 — Useful locality and system value

**Go:**

- at least two scenes retain a non-global causal cone for a useful time window;
- branch reuse provides a clear latency and/or storage benefit;
- fallback frequency is acceptable and reported;
- interaction remains responsive enough for the claimed workflow.

**No-Go / pivot:**

- every meaningful edit immediately affects the full system;
- branch storage is equivalent to duplicating all trajectories;
- full resimulation is simpler and equally fast;
- the only benefit is graph visualization.

If G5 fails, remove the local-speed claim. Continue toward SIG only if correlation
surgery and branch authoring remain strong; otherwise prepare a VIS analysis pivot.

## Gate G6 — Correlation surgery as authoring

**Go:**

- the declared current resolved state remains within tolerance;
- surgery produces repeatable and controllable future differences;
- random surgery of equal magnitude is a weaker baseline;
- users can understand what is preserved and what is edited;
- the method does more than select a random alternate seed.

**No-Go:**

- current-frame differences are already visible before playback;
- the future is uncontrollable noise;
- the operation violates declared invariants or creates overlaps;
- the claim depends on a single cherry-picked pattern.

## Gate G7 — SIG graphics value

**Go:**

- the paper contains a simulation/animation algorithm, not only a phenomenon;
- Molecular Logo Echo establishes the hook and One Collision, Two Worlds carries
  the central physically recomputed method;
- the central Hero is legible without debug overlays;
- branch correctness and performance are synchronized with the displayed run;
- the result cannot be reduced to backward playback or keyframing;
- every primary shot has a complete evidence manifest.

**No-Go:**

- the teaser is mostly a reverse movie;
- the graph is decorative;
- there is no meaningful edit/branch workflow;
- hero styling creates a difference absent from neutral rendering;
- limitations are hidden.

## Gate G8 — Venue decision

### Submit to SIGGRAPH / SIGGRAPH Asia when

- G0–G7 pass at the claim level used in the paper;
- animation, interaction, branch reuse, and visual results are the strongest
  contribution;
- the related-work boundary against reversible collision algorithms and generic
  rollback is convincing.

### Pivot to IEEE VIS when

- G0–G3 pass and the scientific event/branch data are rich;
- G5 local-speed value is weak or inconsistent;
- linked analysis of collision molecules, branches, causal cones, and uncertainty is
  more compelling than animation authoring;
- a real task analysis, expert evaluation, and linked-view design can be performed.

### Stop both when

- G0 or G1 fails;
- neither a graphics algorithm nor a visual-analytics workflow emerges;
- only a beautiful but scientifically ordinary reversal remains.

## Suggested engineering targets, not universal laws

For internal planning only:

- two edit scenes with median affected-particle fraction below roughly 30% over the
  demonstrated edit horizon;
- local branch speedup of roughly 3x or a comparably clear branch-storage benefit;
- interactive branch response within a few seconds for the flagship scale.

These are project management targets, not physical criteria or guaranteed paper
thresholds.
