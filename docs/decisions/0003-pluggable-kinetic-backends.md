# Pluggable kinetic backends

**Status:** Accepted

## Context

Boltzmann DSMC may fail because of finite-density physics rather than collision-history memory.

## Decision

Treat DSMC as the first backend and admit Enskog/other kinetic representations through the same semantic contracts.

## Consequences

More interfaces are required, but the central scientific attribution remains valid.
