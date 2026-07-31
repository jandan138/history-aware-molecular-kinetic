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
