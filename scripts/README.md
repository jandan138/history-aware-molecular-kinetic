# scripts

Thin repository and experiment utilities.

Phase-I paper-story workflow:

- `run_phase1_story.py` generates the paired EDMD-DSMC discrepancy dataset;
- `evaluate_phase1_story.py` evaluates state-only versus state+history with
  trajectory-disjoint geometry/state/ensemble folds;
- `find_phase1_matched_pairs.py` produces descriptive matched-state candidates;
- `decide_phase1_story.py` applies the predeclared operational decision rule.

Molecular Echoes E1 workflow:

- `run_echo_e1.py` runs the frozen periodic same-present/opposite-futures
  experiment, writes audits and metrics, and produces the neutral figure/video
  when the `analysis` extra and `ffmpeg` are available.

Molecular Echoes E2 workflow:

- `calibrate_echo_e2.py` performs the excluded-seed, collision-dose-only budget
  selection without accessing the passive-color response;
- `run_echo_e2.py` runs the frozen molecule-budget ladder, the two selected-budget
  mechanism controls, and the neutral evidence render.

Molecular Time Machine E3 workflow:

- `run_time_machine_e3.py` runs the frozen one-collision edit, exact causal branch,
  full-resimulation comparison, hashed causal artifacts, main figure, and neutral
  15–20 second video.

Molecular Time Machine E4 workflow:

- `run_time_machine_e4.py` runs the frozen outcome-to-cause authoring session:
  terminal feature selection, baseline-only collision ranking, cached exact local
  preview palette, one saved branch/full-resimulation comparison, figure/video, and
  self-contained browser interaction artifact.

Molecular Time Machine E5 workflow:

- `run_time_machine_e5.py` runs the frozen Same Present, Chosen Future session:
  future middle-stroke selection, legal same-cell velocity-ownership palette,
  complete EDMD previews, selected E-to-C future, declared-present audit,
  figure/video, and self-contained browser artifact.

Molecular Time Machine E6 workflow:

- `export_e6_shot_bundle.py` packages frozen E1/E3/E4/E5 trajectories into one
  renderer-neutral binary/JSON contract with source hashes and comparison locks;
- `stage_e6_web_data.py` stages those bundles for the Three.js companion in
  `demos/e6-web`;
- `render_e6_genesis.py` performs a read-only neutral source-state render through
  the canonical local Genesis wrapper;
- `render_e6_blender.py` creates locked-camera Cycles style frames and physical
  trajectory animations without feeding changes back into simulation;
- `compose_e6_hero.py` retimes and captions the rendered E5 pixels into the
  45-second **Same Present, Chosen Future** Hero master.

Smoke mode checks pipeline integrity only and is never primary evidence.
