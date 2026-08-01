# Visual Production Roadmap — Molecular Echoes

> 目标：把“分子回声”从一个漂亮倒放现象，推进成一套可验证、可交互、可复现的 SIG 动画系统。

Visual production is an evidence client. It may reveal branch structure and causal
history, but it may not invent physical differences, replace simulation with reverse
video, or hide a global recomputation behind a local-looking overlay.

---

## 1. Active visual story

The active video no longer explains exact↔kinetic dynamic LOD. It tells one coherent
story:

```text
Boltzmann-style one-particle state forgets detailed collision correlation
→ same resolved present can hide different futures
→ collision history becomes a causal graph
→ users can rewind, edit, branch, and compare molecular animation
```

Three scenes have distinct responsibilities:

| Scene | Responsibility |
|---|---|
| **Molecular Logo Echo** | scientific hook and first-page visual |
| **One Collision, Two Worlds** | causal-graph and branch algorithm |
| **Choose the Cause** | outcome-to-cause interaction and scoped system value |

The old Zoomable Mixing, Correlation Labyrinth, and Expansion into Vacuum scenes are
retained as deferred LOD assets; they are not active paper evidence.

---

## 2. V0–V6 production ladder

## V0 — Event and Replay Diagnostic Viewer

**Begins during E0/E3.**

Minimum capabilities:

- render exact particles and passive colors;
- display collision events at their physical time;
- select particles/events;
- show event predecessors and descendants;
- show checkpoints and branch lineage;
- display resolved-state pivot audits;
- compare physical reverse, replay, and backward-video reference;
- export deterministic render manifests.

No hero material is required.

### Exit

The viewer can independently replay a frozen branch from artifacts and expose a
replay divergence without solver access.

---

## V1 — Scientific Echo Prototype

**Begins after G0/G1.**

Create a neutral split-screen:

```text
forward | exact reverse | chaotized reverse | DSMC | ghost
```

Required insets:

- pivot `f1_h` audit;
- anisotropy/color response;
- branch time;
- clear label distinguishing simulated reverse from reversed video.

### Exit

A viewer can understand “same resolved present, different future” before seeing any
collision graph. The effect survives matched particle display and finer pivot audits.

---

## V2 — History-Budget Microscope

**Begins after G2.**

Add a controlled history slider:

```text
no collisions
random count-matched suppression
small molecules
larger molecules
full EDMD
```

Visual language:

- particle colors encode passive material, not method;
- molecule membership uses temporary outlines/trails;
- graph overlays appear in linked insets, not over the entire scene;
- collision count and structured budget are shown separately.

### Exit

The neutral video shows that structured history and count-matched random suppression
are not visually or quantitatively interchangeable.

---

## V3 — One Collision, Two Worlds

**Begins after G3/G4.**

A user selects one past event and applies a bounded edit. The scene displays:

```text
original future | locally recomputed counterfactual | full-resimulation reference
```

Required visual elements:

- selected event;
- descendant causal cone;
- affected-particle fraction over time;
- local/full error indicator;
- fallback notification when the cone becomes global;
- branch tree with immutable parent.

### Exit

The split-screen branch matches the full reference under the registered tolerance,
and the interaction is understandable without reading the paper.

---

## V4 — Choose the Cause, Direct the Future

**Begins after E3 and is the active E4 visual gate.**

The creator does not begin with a hand-picked collision. They select a feature in
the terminal molecular image; the system traces that feature through the baseline
collision DAG, ranks a small set of past causes, and lets them browse an exact
preview palette.

Required visual elements:

- selected terminal feature and its persistent particle IDs;
- baseline-only causal ranking on the past timeline;
- physical-angle palette with a clear selected branch;
- original and directed futures under the same display;
- target-versus-collateral outcome readout;
- one explicit full-reference confirmation for the saved branch.

### Exit

A viewer can understand “choose the consequence first, then find the cause” without
reading a debug graph. The browser artifact may switch cached exact results but may
not imply that rendering itself performed a physical edit.

---

## V5 — Deferred geometry edit and correlation surgery

**Begins after G5/G6.**

Two interaction modes:

### Past geometry edit

Move or insert a simple obstacle/open an aperture, then recompute the future cone.

### Same-present future edit

At the pivot, apply a surgery that preserves registered `f1_h`/moments while changing
hidden particle pairing or retained molecule structure.

Required audit views:

- what is preserved;
- what is edited;
- pivot mismatch at multiple resolutions;
- original and alternate futures;
- random surgery baseline;
- branch provenance.

### Exit

A user can deliberately create and compare alternate futures rather than observe
uncontrolled chaos.

---

## V6 — SIG Production and Evidence Release

**Begins after G7.**

Final deliverables:

- 30–45 second teaser;
- 3–5 minute technical video;
- neutral comparison reel;
- interaction capture;
- failure/limitation reel;
- per-shot evidence registry;
- frozen cameras, render configs, branch IDs, metrics, and frame hashes;
- commands that reconstruct all primary contact sheets.

No new physical branch, edit class, or metric may debut in V6.

---

## 3. Teaser structure

Suggested 40-second structure:

```text
0–5 s    colorful molecular pattern disperses
5–10 s   pivot: exact and chaotized states appear identical under the audit
10–17 s  exact history reconstructs the pattern; other branches do not
17–24 s  history-budget slider and collision molecules
24–32 s  select one collision: two futures and spreading causal cone
32–38 s  select a future stroke, trace it to a past collision, and direct a branch
38–40 s  title: Molecular Echoes
```

The teaser may use temporal compression, but every branch must be a forward-rendered
simulation after its fork. A reversed frame sequence must be labeled and used only
as an explanatory baseline.

---

## 4. Shared-renderer fairness

All primary branch comparisons freeze:

- camera and frame times;
- particle radius and display density;
- passive-color mapping;
- trail length and motion blur;
- lighting and tone mapping;
- event/graph overlay policy;
- branch time alignment;
- spatial crop;
- output resolution.

Method-specific hidden smoothing, deleted particles, or manually adjusted branch
times invalidate a primary comparison.

---

## 5. Visual language

### Physical particles

- passive color encodes the prepared pattern/species;
- exact identity is persistent;
- history budget is not encoded by changing particle count or brightness.

### Events and causal influence

- selected collision: compact high-contrast pulse;
- direct descendants: short-lived line/trail;
- affected causal cone: restrained halo/outline or linked inset;
- invalidated old events: desaturated in the graph view, not deleted from evidence.

### Branches

Use stable branch identities across all scenes:

```text
original
exact reverse
chaotized
DSMC
counterfactual local
full-resimulation reference
```

Color should not conflict with passive particle color; branch identity should rely on
layout, labels, borders, or background accents.

---

## 6. Hero-polish gate

Do not begin production materials or complex 3D assets until:

1. exact reverse/replay passes;
2. multi-resolution same-present audit passes;
3. structured history survives null controls;
4. local branch matches full resimulation;
5. at least one edit retains useful locality;
6. neutral footage already tells the story.

Primitive geometry, sphere instancing, transparent walls, and clean lighting are
sufficient for the first paper. The renderer must not become a separate product.

---

## 7. Claim-to-pixel mapping

| Claim | Required visible evidence |
|---|---|
| same resolved present | pivot split-screen + multi-resolution audit |
| hidden history changes future | exact/chaotized divergence under shared rendering |
| molecule topology matters | structured budget vs count-matched control |
| event graph drives the method | selected event, descendants, replay/branch provenance |
| local branch is correct | local branch visually and numerically matches full reference |
| branch reuse has value | affected fraction + latency/storage synchronized with the shot |
| surgery is an authoring tool | preserved present + user-selected alternate future |

---

## 8. VIS-ready artifacts without premature pivot

The viewer should record event graph, branch tree, causal-cone timeline,
resolved-state audit, and uncertainty as reusable artifacts. These can support a
future linked-view VIS system, but the active production remains SIG animation and
interaction evidence.

Related documents:

- [Hero Scenes](hero-scenes.md)
- [Storyboard](storyboard.md)
- [Visual Acceptance Criteria](visual-acceptance-criteria.md)
- [Graph and Branching Architecture](../architecture/collision-history-graph-and-branching.md)
- [Molecular Echoes Backlog](../roadmap/molecular-echoes-backlog.md)
