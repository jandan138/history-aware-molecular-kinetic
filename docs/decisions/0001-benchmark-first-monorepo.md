# Benchmark-first monorepo

**Status:** Accepted

## Context

We need one evidence chain across exact, kinetic, indicator, conversion, and graphics modules. Separate repositories would encourage incompatible cases and ad-hoc result transfer.

## Decision

Use one monorepo with strict module boundaries and versioned artifacts. Benchmark suites remain independent and can be extracted later.

## Consequences

Shared contracts and CI improve traceability; the repository must resist becoming a tightly coupled solver monolith.
