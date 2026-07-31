# Research Thesis

## 1. Active thesis

The active project is no longer an online EDMD–kinetic LOD predictor. The Phase-I
pilot did not support the tested scalar-history predictor at an operationally useful
level, so the dependent conversion and dynamic-LOD route is deferred.

The new thesis is:

> **Collision history is not only a statistic to predict model error. It can be a
> first-class animation representation that explains, replays, reverses, and edits
> hidden multi-particle correlations.**

The scientific and graphics questions are:

\[
\boxed{
\text{What information does a resolved one-particle state forget?}
}
\]

and

\[
\boxed{
\text{How can that information become a reversible, branchable animation tool?}
}
\]

## 2. Scientific foundation

An exact hard-sphere state is:

\[
X(t)=\{x_i(t),v_i(t),r_i,m_i,\mathrm{id}_i\}_{i=1}^{N}.
\]

A kinetic description keeps a one-particle distribution:

\[
f_1(x,v,t),
\]

while higher-order distributions and cumulants carry particle-pair and
multi-particle correlations.

Deng, Hani, and Ma's long-time hard-sphere derivation of Boltzmann propagates
cumulants with complete collision histories and organizes correlated structures as
collision-history molecules before controlling them. This motivates our focus on
collision history as the hidden information separating exact molecular dynamics
from a factorized kinetic closure.

The theorem does not provide our finite-system algorithm, and our method is not an
implementation of its cutting proof.

## 3. Same resolved present, different futures

We declare a finite resolution `h` and measure:

\[
f_{1,h}(x,v,c),
\]

including passive color `c` when used for visualization.

At a pivot time `t_*`, we construct:

- a forward exact branch;
- an exact velocity-reversed branch;
- a resolved-state-preserving chaotized branch;
- a DSMC branch from the reversed resolved state;
- optional history-budgeted branches.

The operational claim is:

\[
f_{1,h}^{\rm reverse}(t_*)
\approx
f_{1,h}^{\rm chaotized}(t_*),
\]

while selected future observables separate:

\[
A_{\rm reverse}(t_*+\tau)
\neq
A_{\rm chaotized}(t_*+\tau).
\]

This is a claim about a preregistered resolved present. It is not a claim that the
exact microscopic states or the continuous `f1` are identical.

## 4. Graphics representation

### 4.1 Collision causal multigraph

Each collision is a timestamped event node linked through the particles that carry
its consequences forward. Repeated collisions remain distinct events.

The graph stores:

- event predecessors and descendants;
- shared collision ancestors;
- collision-history molecules;
- branch provenance;
- causal cones;
- history-budget annotations.

### 4.2 Checkpoints and deterministic replay

Checkpoints plus event segments support random access, replay, and reversal audits.
A replay mismatch is evidence, not something the renderer or solver may silently
repair.

### 4.3 Persistent counterfactual branches

A user edits a past particle, collision, aperture, or obstacle. The system forks an
immutable branch, reuses common history, and recomputes the expanding future causal
cone. It falls back to full replay if locality cannot be guaranteed.

### 4.4 Correlation surgery

A surgery operator changes particle–velocity assignment and collision ancestry while
preserving a declared resolved current state and primary invariants. This creates a
new animation primitive:

> **edit a hidden future while preserving the visible present.**

## 5. Proposed SIG contributions

### C1. History representation

A versioned collision causal multigraph and branch store for hard-sphere animation,
with deterministic replay and queryable collision molecules.

### C2. Causal rewind and branch recomputation

An exact expanding-cone algorithm for counterfactual edits, with correctness against
full resimulation, conservative fallback, and copy-on-write history reuse.

### C3. Resolved-state-preserving future authoring

A constrained correlation-surgery framework that produces alternate futures from
the same declared one-particle present.

### C4. Scientific history microscope

A controlled exact/chaotized/DSMC/history-budget experiment, including
collision-count-matched and topology-shuffled null controls, that links visible
future separation to missing incoming-pair correlation.

### C5. Interaction and visual evidence

A user-facing molecular time machine with three high-quality scenes, versioned
render evidence, and a direct connection between every visible branch and a frozen
simulation run.

## 6. Primary hypotheses

- **H1 — Numerical reversibility:** exact EDMD can forward/reverse and replay the
  registered cases within declared tolerances.
- **H2 — Resolved-state separation:** exact-reverse and chaotized branches pass a
  multi-resolution `f1_h` audit while exhibiting robust future separation.
- **H3 — Structured-history mechanism:** a `(Lambda, Gamma)` molecule budget explains
  recovery better than count/time-matched random collision suppression.
- **H4 — Branch correctness:** local causal-cone recomputation matches complete
  resimulation or explicitly falls back.
- **H5 — Useful locality:** at least two edit families retain sufficiently local
  cones to provide a meaningful latency or storage benefit.
- **H6 — Graphics value:** history surgery and branching create animations that are
  difficult to author by ordinary playback, keyframing, or a backward video.

## 7. Negative thesis and stop conditions

The paper route must stop or narrow if:

- exact reversal is numerically unreliable;
- future separation disappears under finer `f1_h` audits;
- history-budget curves are explained only by collision count;
- incoming-pair diagnostics do not align with the branch response;
- causal cones become global immediately in all useful scenes;
- local branch results do not match full resimulation;
- the only compelling footage is a video played backward;
- the event graph is merely a debug overlay with no algorithmic or authoring value.

## 8. Deferred route

The previous adaptive exact–kinetic route remains recorded:

```text
history predictor
→ exact/kinetic conversion
→ online partition
→ dynamic LOD
```

It is not deleted, but it is not an active paper spine after the Phase-I negative
result. R0/B0 external and primitive validation remain useful infrastructure.

## 9. Venue identity

The first target is SIGGRAPH / SIGGRAPH Asia because the intended contribution is a
new simulation, animation, and interaction system.

IEEE VIS is a fallback only if the principal contribution becomes linked visual
analysis of collision molecules, causal cones, branch provenance, and uncertainty.
That route requires a separate task analysis and evaluation.

See [Venue Strategy](venue-strategy.md).
