# Scope and Non-Goals

## In scope for the first SIG paper

### Physical model

- elastic equal-mass or few-species hard disks/spheres;
- two-dimensional preregistered feasibility and correctness studies;
- three-dimensional Hero Scenes only after scientific/branch gates;
- exact event-driven dynamics with deterministic event-order policy;
- periodic and simple analytic reflective/moving boundaries;
- passive color/tracer labels that do not affect dynamics.

### Scientific echo

- forward, exact-reverse, chaotized-reverse, DSMC, and ghost branches;
- preregistered finite-resolution `f1_h` and moment audits;
- collision event multigraph and molecule annotations;
- `(Lambda,Gamma)` extended history-budget dynamics;
- collision-count/time-matched and topology-shuffled null controls;
- low-dimensional incoming-pair closure-defect diagnostics;
- a small fixed-`N epsilon` study only after the finite mechanism passes.

### Graphics and systems

- checkpoints and deterministic random access;
- collision-history causal graph;
- immutable persistent branches and copy-on-write history reuse;
- past particle/collision/simple-geometry edits;
- exact expanding causal-cone recomputation;
- full-resimulation correctness and conservative fallback;
- resolved-state-preserving correlation surgery;
- interactive branch comparison;
- instanced particles, transparent analytic geometry, event/graph insets, and
  reproducible render manifests;
- Molecular Logo Echo, One Collision Two Worlds, and Edit the Past.

## Explicit non-goals for the first SIG paper

- claiming velocity reversal or Loschmidt echo as novel;
- claiming the first reversible hard-sphere simulator;
- implementing the Deng–Hani–Ma cutting proof as a simulator;
- proving a new Boltzmann or Boltzmann–Grad theorem;
- claiming exact equality of continuous `f1` or microstates after surgery;
- dense frictional sand, static friction, jamming, or force chains;
- arbitrary soft potentials, chemical reactions, plasma, combustion, or radiation;
- full Navier–Stokes coupling;
- online EDMD↔DSMC dynamic LOD in the active paper;
- promotion/demotion and exact/kinetic partition control;
- complex CAD, deformable obstacles, or six-degree-of-freedom assets before the
  analytic edit cases pass;
- a generic distributed Time-Warp implementation;
- a generic keyframe or trajectory optimizer;
- a full IEEE VIS analytics system before a formal venue pivot;
- using backward video or state snapping as simulation evidence.

## First-paper edit classes

The primary edit set is deliberately bounded:

1. perturb one particle before a selected event;
2. modify/suppress one event under explicitly labeled semantics;
3. insert/remove/move one analytic obstacle;
4. open/close one simple aperture;
5. apply one declared correlation-surgery operator at a pivot.

Additional edit types enter only after these pass correctness and locality studies.

## Model-domain language

Use **hard-sphere/hard-disk gas** only for the declared elastic collision model.
Use **extended history-budget dynamics** for ghost/suppressed-collision branches;
do not call them exact EDMD.

Use **same resolved present** only when the preregistered `f1_h`/moment audit passes.
Do not shorten it to “same state.”

Use **causal-cone recomputation** only when dependency expansion and full-reference
validation are implemented. A fixed visual neighborhood is not a causal cone.

## Venue boundary

The active work is a SIG animation/simulation system. A future IEEE VIS pivot is in
scope only after a formal decision and must add domain tasks, linked views, and an
evaluation appropriate to visualization research.
