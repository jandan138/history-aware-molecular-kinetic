# Reproducibility contract

A primary result is reproducible only if another machine can determine:

- exact repository commit and dirty state;
- frozen case content hash;
- method and parameter hash;
- random seed family and stream policy;
- external executable/container hash and revision;
- compiler, libraries, CPU/GPU, and precision;
- raw and canonical artifact hashes;
- metric and figure recipe versions;
- all exclusions and failures.

## Stochastic results

Report ensemble size, independent seed definition, confidence interval method,
and grouped resampling unit.

## Determinism

Bitwise determinism is not required for all parallel solvers. The expected
reproducibility level—bitwise, statistically equivalent, or tolerance-based—is
recorded per method.

## External sources

External reference behavior is bound to pinned revisions. A new upstream version
creates a new adapter evidence revision.


## Graphics evidence

A primary visual result additionally records the B5 case and shot ID, render-config and camera-path hashes, comparison-lock group/hash, display particle policy/seed, transfer function, temporal filtering, renderer version, frame times, and links to the physical metric displayed.


## Render comparison audit

Frozen primary comparisons must pass `scripts/audit_render_manifests.py` with
complete evidence links. This prevents camera, timeline, renderer, or display
settings from drifting between methods after metrics have been selected.
