# Experiment lifecycle

## 1. Question

Every experiment begins with a falsifiable question and at least one alternative
explanation.

## 2. Candidate case

Candidate cases may change while being debugged. Their IDs include a revision and
must not be used as final paper evidence.

## 3. Smoke run

A smoke run verifies execution, artifact production, and obvious invariants. It
does not establish scientific accuracy.

## 4. Resolution and sampling study

Before comparison, each method receives its own convergence/sampling study.
Matched wall-clock cost is not a substitute for resolved references.

## 5. Freeze

A case becomes frozen only after:

- model and units are reviewed;
- initial ensemble generation is deterministic and audited;
- oracle/reference behavior is understood;
- metrics and split groups are fixed;
- acceptance thresholds are justified;
- artifact schemas are stable.

## 6. Registered experiment

A registered manifest specifies the full method/parameter/resolution/seed matrix.
Runs are immutable and content-addressed.

## 7. Evaluation

Metrics are generated from artifacts. Exclusions are machine-readable and applied
without seeing final method rankings when possible.

## 8. Evidence freeze

Primary figures and tables reference immutable run IDs. Any later rerun creates a
new evidence revision.

## 9. Retire

A flawed frozen case is retired with a reason and replacement ID. It is never
silently rewritten.
