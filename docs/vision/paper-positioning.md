# Paper Positioning

## Working title

> **Molecular Echoes: Reversible and Counterfactual Hard-Sphere Animation with
> Collision-History Graphs**

Alternative title emphasizing interaction:

> **Molecular Time Machine: Causal Rewind and Hidden-State Editing for Hard-Sphere
> Animation**

## One-paragraph story

We introduce a history representation and animation system for exact hard-sphere
dynamics. A timestamped collision causal multigraph, deterministic checkpoints, and
copy-on-write branch storage support random access and physically recomputed
counterfactual futures after particle, collision, or geometry edits. An expanding
causal-cone algorithm reuses unaffected history and is verified against full
resimulation. A constrained correlation-surgery operator preserves a declared
resolved one-particle present while altering hidden particle pairing, enabling two
visually identical current states to evolve into different futures. Scientifically,
we compare exact, chaotized, DSMC, and collision-molecule-budget branches to expose
the multi-particle information discarded by kinetic closure. The system is
illustrated through molecular echo, one-collision branching, and edit-the-past Hero
Scenes.

## Why this belongs at SIGGRAPH

The intended contribution is not merely a statistical-mechanics phenomenon. It is a
new simulation and animation workflow:

- rewind to a past physical state;
- inspect the collision history causing the present;
- edit a past event or obstacle;
- generate a new physically simulated future;
- reuse unaffected history;
- compare persistent alternate branches;
- author a different future while preserving the current visible state.

The paper must therefore report:

- algorithmic correctness against full resimulation;
- runtime, storage, and causal-cone scaling;
- interaction latency;
- branch provenance and reproducibility;
- high-quality three-dimensional results;
- limitations when the cone becomes global or reversibility is numerically fragile.

## Scientific bridge to Deng–Hani–Ma

Deng, Hani, and Ma control cumulants and collision-history molecules in their
long-time derivation of Boltzmann from hard spheres. Our finite-system work uses
that structure as motivation for asking what one-particle closure forgets and for
building a collision-molecule intervention.

The paper should say:

> inspired by the cumulant and collision-history molecule structure used in the
> hard-sphere-to-Boltzmann derivation.

It must not say:

- we implement the proof's cutting algorithm;
- the theorem proves our finite simulation method;
- the finite history budget is a new kinetic-limit theorem;
- a reverse-correlated state contradicts Boltzmann.

## Claims allowed only after evidence

1. Exact numerical reversal and deterministic replay pass registered tolerances.
2. Exact-reverse and chaotized branches match the declared resolved `f1_h` over a
   resolution sweep yet exhibit robust future separation.
3. Structured molecule budgets explain the response beyond count-matched random
   suppression and topology-shuffled controls.
4. Local causal-cone branching matches complete resimulation or explicitly falls
   back.
5. At least two edit families provide useful reuse in runtime or storage.
6. Correlation surgery preserves the declared present and enables repeatable
   alternate-future authoring.
7. The Hero Scenes remain understandable without debug overlays or backward video.

## Claims we must not make

- velocity reversal is novel;
- collision logs or rollback are novel by themselves;
- the branch engine is always local;
- matching coarse bins means exact state equality;
- changing only a historical record changes a deterministic future;
- replaying recorded frames backward is a physically recomputed reverse branch;
- DSMC particle IDs carry true molecular histories;
- the original LOD predictor succeeded.

## Strongest prior-art boundaries

### Reversible collision simulation

Prior work already studies reversible elastic-collision algorithms. Our novelty
cannot be “hard spheres can be reversed.” The distinction must be the
collision-history representation, correlation surgery, causal future branching,
and animation authoring workflow.

### Discrete-event rollback

Time-Warp and related discrete-event systems already use checkpoints, causal
dependencies, and rollback. Our distinction must be hard-sphere-specific event
causality, exact branch validation, physical edit semantics, hidden-correlation
surgery, and visual authoring—not generic rollback terminology.

### Loschmidt echoes

A simple reverse movie or exact echo is the entrance demonstration, not the
contribution. The paper must progress to controlled chaotization, molecule budgets,
and counterfactual edits.

### Particle/spacetime control

Existing animation work controls particles or fluids toward keyframes. Our system
is not a generic optimizer; it edits collision ancestry and shares exact simulated
history across branches. Comparisons should distinguish direct physical branching
from optimization toward a target.

## Reviewer questions the paper must answer

- Is the “same present” claim stable under finer spatial and velocity bins?
- Is the history-budget effect just fewer collisions?
- How is local causal recomputation proven correct?
- When and how quickly does the causal cone become global?
- What is stored per event and per branch?
- Why is this better than full resimulation or storing full trajectories?
- Can the user predict/control the future, or only observe chaos?
- Is the result a graphics method or a physics visualization?
- What remains of the connection to the hard-sphere-to-Boltzmann mathematics?

## Required paper figures

1. **Same resolved present, opposite futures** with a multi-resolution pivot audit.
2. **Collision-molecule budget** versus null controls.
3. **Collision causal graph and branch representation**.
4. **One-event edit** with spreading causal cone and full-reference correctness.
5. **Geometry edit** with runtime/storage comparison.
6. **Correlation surgery** showing present-state preservation and future control.
7. **Three Hero Scenes**, limitations, and failure cases.

## Venue route

- **Primary:** SIGGRAPH / SIGGRAPH Asia.
- **Fallback:** IEEE VIS only after a true pivot to linked visual analytics of event
  graphs, branch provenance, molecule budgets, and uncertainty.

See [Venue Strategy](venue-strategy.md).
