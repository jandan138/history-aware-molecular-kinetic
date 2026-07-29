# Contributing

## Research changes are evidence-bearing changes

Every nontrivial solver, indicator, conversion, or benchmark change must state:

- the physical model and assumptions;
- the numerical method and expected invariants;
- the benchmark case that can falsify the change;
- the artifact schema written by the implementation;
- the claim, if any, that the evidence supports.

## Branch and commit discipline

Use focused branches and terse imperative commits. Do not mix generated results,
third-party source, and core code in one change.

## Definition of done

A change is complete only when:

1. relevant unit and contract tests pass;
2. schemas and examples remain valid;
3. new benchmark semantics are documented;
4. provenance fields are emitted;
5. third-party license boundaries are respected;
6. failures and non-applicable regimes are reported, not hidden.

## Scientific integrity

Do not describe collision-history molecules or the cutting algorithm from the
Deng–Hani–Ma proof as an online algorithmic guarantee. The project is inspired
by the distinction between factorized kinetic descriptions and correlated
collision histories; every computational proxy must be validated independently.
