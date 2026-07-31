# Venue Strategy: SIG First, IEEE VIS Only as a Real Pivot

## 1. Primary target

The active paper is designed first for **SIGGRAPH / SIGGRAPH Asia**.

The current SIGGRAPH Technical Papers program explicitly seeks novel research that
advances computer graphics and interactive techniques, with a Journal/TOG-level
track and a Conference track. Future calls may change, so the exact track rules and
deadlines must be rechecked for the target year.

Official reference:

- https://s2026.siggraph.org/program/technical-papers/

## 2. What the SIG version must be

The paper cannot be only:

- a Loschmidt echo;
- a hard-sphere physics visualization;
- a collision graph viewer;
- an event-log replay tool;
- a theorem-inspired numerical experiment.

It must introduce a graphics/animation method with at least:

1. a collision-history causal multigraph and versioned branch representation;
2. deterministic rewind/random access;
3. physically recomputed counterfactual branches after past edits;
4. a causal-cone algorithm with correctness against full resimulation;
5. persistent history sharing and measurable runtime/storage benefit;
6. coarse-state-preserving correlation surgery as a novel authoring primitive;
7. three-dimensional, high-quality Hero Scenes and a clear interaction story.

## 3. Recommended submission shape

### Journal/TOG-level package

Requires the full scientific and graphics package:

- strict numerical reversal;
- multi-resolution `f1_h` audit;
- molecule-budget and null-control experiments;
- local branch correctness and scaling;
- several edit classes;
- persistent branching/storage analysis;
- three polished 3D scenes;
- strong limitations and reproducibility.

### Conference-level package

If the target-year SIGGRAPH program retains a separate conference track, a smaller
but still novel package may be viable:

- one robust scientific echo mechanism;
- collision graph + deterministic replay;
- one-event and one-geometry counterfactual edit;
- correctness against full resimulation;
- two strong Hero Scenes;
- transparent limits on scale and branch locality.

This is not permission to submit a demo without an algorithm.

## 4. SIG acceptance gate

**Current status:** the full gate is not met because E2 did not beat its registered
controls. A SIG route now requires an explicitly narrower graphics-system thesis;
the Deng-inspired molecule mechanism cannot be used to satisfy this gate.

Before paper production, require all of:

- E0 numerical reversal passes;
- E1 same-resolved-present audit passes at multiple resolutions;
- E2 structured history budget beats count-matched null controls;
- E4 local branching matches full resimulation or explicitly falls back;
- at least two edit families exhibit useful causal-cone locality;
- branch reuse provides a clear runtime or memory advantage;
- two visible phenomena remain understandable without debug overlays;
- the three Hero Scenes have frozen evidence manifests.

If the science passes but local branching has no useful locality, remove the
performance claim and assess whether history surgery plus branch authoring is still
a sufficient graphics contribution. Do not hide a global cone behind a local-edit
interface.

## 5. IEEE VIS fallback

IEEE VIS is a legitimate fallback only if the strongest outcome becomes a visual
analytics contribution rather than an animation algorithm.

The current IEEE VIS area model includes:

- Systems & Rendering;
- Representations & Interaction;
- Data Transformations;
- Analytics & Decisions;

Official references:

- https://ieeevis.org/year/2026/info/call-participation/area-model/
- https://ieeevis.org/year/2026/info/call-participation/call-for-participation/

A VIS pivot would become:

> **Collision-Molecule Explorer: Visual Analytics for Hidden Correlations and
> Counterfactual Futures**

It would require linked views for:

- particle space;
- collision-event graph;
- branch tree;
- causal-cone timeline;
- velocity space and resolved-state mismatch;
- history-budget curves;
- replay divergence and uncertainty.

It would also require:

- explicit domain analysis tasks;
- design rationale;
- kinetic-theory or simulation experts;
- case studies and/or a user study;
- evidence that linked interaction enables insights that static plots do not.

A rejected SIG paper cannot be sent to VIS unchanged. The research question,
evaluation, related work, and interface contribution would all need to be rebuilt.

## 6. Decision timeline

### Stay on SIG route when

- the branch engine and editing algorithm are the strongest contribution;
- local recomputation or shared history provides measurable system value;
- the main evidence is animation quality, control, and simulation performance;
- users can author futures that ordinary playback/keyframing cannot produce.

### Prepare VIS pivot when

- the causal cone is often global, weakening the simulation speed claim;
- the event graph, branch comparison, and molecule-budget analysis reveal strong
  scientific insights;
- expert exploration tasks are more compelling than animation authoring;
- linked-view interaction becomes the main contribution.

### Stop both routes when

- exact numerical reversal is unreliable;
- same-present separation disappears under finer audits;
- structured history intervention is no better than count-matched suppression;
- the only attractive result is a video played backward;
- neither branch editing nor visual analysis provides a novel workflow.
