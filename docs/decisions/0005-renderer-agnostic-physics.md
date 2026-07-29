# Renderer-agnostic physics

**Status:** Accepted

## Context

Camera-driven LOD can hide whether refinement is physically necessary.

## Decision

Physics solvers emit artifacts; the renderer cannot mutate partition state. Screen-space display density is a separate logged policy.

## Consequences

Interactive coupling requires an explicit future ADR.
