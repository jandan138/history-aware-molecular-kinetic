# External oracle process isolation

**Status:** Accepted

## Context

Primary references use GPL software and distinct internal models.

## Decision

Invoke external tools through configured executables/containers, preserve raw output, and convert into canonical artifacts. Do not vendor source into the Apache core.

## Consequences

Build friction remains, but license and behavioral boundaries stay explicit.
