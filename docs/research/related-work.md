# Related Work

## 1. Hard-sphere kinetic limits and collision correlation

Deng, Hani, and Ma derive the Boltzmann equation from rarefied Newtonian
hard-sphere dynamics over the lifespan of the Boltzmann solution. Their proof
propagates cumulants carrying complete collision histories and organizes correlated
structures as collision-history molecules before controlling them with a cutting
argument.

Related kinetic-theory work studies backward collision clusters and correlation
errors in Boltzmann–Grad limits. These works motivate the scientific information
boundary in Molecular Echoes, but they do not provide a finite animation branch
algorithm or user interface.

## 2. Velocity inversion and Loschmidt echoes

Velocity inversion and return/echo experiments in hard-disk systems are established
prior art. A plain sequence in which particles disperse, velocities are reversed,
and the past pattern reappears is not a novel contribution.

Molecular Echoes uses exact reversal as a controlled entrance experiment. The active
novelty requires:

- a preregistered resolved-state audit;
- a chaotized branch with different hidden correlation;
- history-budget and null-control experiments;
- collision causal graph;
- counterfactual branch recomputation;
- correlation surgery and animation authoring.

## 3. Reversible elastic-collision algorithms

Perumalla and Protopopescu study reversible simulations of elastic collisions and
show algorithms that recover pre-collision states with essentially no accumulating
history storage in their studied settings.

This prevents claims such as “the first reversible hard-sphere simulator” or
“history storage is required for physical reversibility.” Our distinction is not
reversibility alone; it is a versioned collision-history representation that
supports causal queries, past edits, branch sharing, resolved-state surgery, and
visual authoring.

## 4. Discrete-event rollback and Time Warp

Time Warp and related optimistic discrete-event simulation systems use checkpoints,
causal dependency tracking, rollback, replay, anti-messages, and recovery.

Therefore checkpointing and rollback are not novel by themselves. The active
hard-sphere distinction must include:

- event causality induced by particle collision ancestry;
- exact expanding-cone recomputation validated against full resimulation;
- physical particle/collision/geometry edit semantics;
- persistent counterfactual animation branches;
- correlation surgery under resolved-state constraints;
- graphics interaction and visual evidence.

## 5. Exact event-driven hard-sphere simulation

DynamO is the primary external EDMD reference. It provides mature hard-sphere event
dynamics, analysis plugins, large-system support, and visualization. It is an exact
microscopic oracle and solver-engineering reference, not code vendored into the
Apache core.

The internal EDMD must reproduce selected analytic and DynamO behavior before
supporting exact reversal or branch correctness claims.

## 6. Direct Simulation Monte Carlo

SPARTA is the primary Boltzmann/DSMC reference. In the active route DSMC is not the
runtime half of an LOD method. It is a controlled baseline that samples collisions
without preserving the exact molecular pair history.

This makes DSMC useful in the exact/chaotized/DSMC comparison, while still requiring
normalization, convergence, and sampling audits.

## 7. Existing adaptive rarefied-gas and EDMD–DSMC methods

uniGasFoam, DSMC–continuum hybrids, unified gas-kinetic methods, and prior stochastic
event-driven MD/DSMC work establish that adaptive rarefied simulation and EDMD–DSMC
coupling are not novel categories.

The repository retains these references for the deferred LOD route and for avoiding
false “first hybrid” claims.

## 8. Finite-density kinetic models

Enskog and non-ideal stochastic particle schemes address finite-density pair
structure. They remain relevant when interpreting EDMD/DSMC differences, but they
are not the active graphics system.

The same-present echo experiment must avoid attributing a density-model mismatch to
collision history. Density/packing and numerical parameters remain controlled.

## 9. Strongest graphics neighbors: many worlds and storyboards

[Many-Worlds Browsing](https://graphics.cs.cmu.edu/projects/mwb/) already computes
many multibody simulations and lets a user browse and modify candidate outcomes.
[Physics Storyboards](https://research.adobe.com/publication/physics-storyboards/)
already uses important space-time outcomes to summarize and tune procedural
animations. These are closer conceptual neighbors than a generic simulation viewer.

Consequently, “we show multiple physical futures,” “the user can modify a scene,”
and “we present a timeline of important events” are not sufficient distinctions.
Molecular Time Machine instead makes an individual past hard-sphere collision the
editable semantic object. Shared-particle ancestry drives exact event reuse and
invalidation, and the resulting branch is compared event-by-event with a complete
resimulation.

## 10. Particle and spacetime animation control

Graphics contains extensive work on particle control, keyframe matching, adjoint or
optimization-based simulation control, spacetime constraints, retiming, and target
formation.

Molecular Echoes is not intended as a general target optimizer. Its distinction is:

- edits are made to actual past collision/geometry state;
- alternate futures are physically resimulated;
- branch history is shared and queryable;
- correlation surgery preserves a declared current state rather than optimizing
  toward a future keyframe;
- branch correctness is compared against full resimulation.

Related-work review must include the strongest relevant particle/fluid editing
papers before submission.

## 11. Causal graphs and provenance visualization

Event graphs, provenance graphs, branch trees, and causal visualizations are common
across debugging, distributed systems, workflow analysis, and visual analytics.

A collision graph figure alone is not a SIG contribution. The graph must drive
checkpoint replay, descendant invalidation, counterfactual recomputation, and
interaction. For a possible IEEE VIS route, linked views and expert analysis tasks
would be required beyond the simulation system.

## 12. Kinetic and particle simulation in graphics

Continuous-scale kinetic fluids and HOME-LBM demonstrate high-quality kinetic
simulation and GPU systems in graphics. They set a systems and visual standard but
do not provide exact hard-sphere collision identity or the active causal branching
workflow.

## 13. Positioning summary

The active paper occupies the intersection:

```text
hard-sphere correlation / kinetic closure
+ addressable collision events
+ exact ancestry-driven history reuse and recomputation
+ animation authoring through physical edits to the past
```

It is not sufficiently novel if any one of the following is the entire story:

- velocity reversal;
- event logging;
- generic rollback;
- a collision graph visualization;
- an EDMD solver;
- a DSMC solver;
- a pretty molecular logo;
- a theorem-inspired physics experiment without an animation algorithm.

The minimum distinction is the combined scientific and graphics chain documented in
[Novelty Map](novelty-map.md) and [Paper Positioning](../vision/paper-positioning.md).
