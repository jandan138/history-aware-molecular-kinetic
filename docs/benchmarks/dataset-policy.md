# Dataset policy

## Dataset purpose

The B1/B2 dataset estimates model discrepancy and tests indicator generalization.
It is not a generic particle trajectory corpus.

## Required grouping keys

- geometry family;
- physical regime and packing band;
- initialization family;
- seed family;
- resolution configuration;
- time episode;
- oracle revision.

## Leakage prevention

Blocks from the same trajectory cannot be randomly split across train and test.
Overlapping history windows stay in one split. Normalization is fit on training
groups only.

## Feature visibility

Every feature is labeled `runtime_observable`, `shadow_probe`, or `oracle_only`.
Models and metrics preserve that label.

## Ground-truth uncertainty

Exact ensemble targets include uncertainty from finite particle count and finite
realizations. DSMC targets include sampling and discretization uncertainty.

## Versioning

A dataset release binds:

- frozen cases;
- raw run IDs;
- converter versions;
- feature definitions;
- split manifest;
- target definitions;
- license/redistribution notes.
