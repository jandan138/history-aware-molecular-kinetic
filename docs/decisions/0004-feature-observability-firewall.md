# Feature observability firewall

**Status:** Accepted

## Context

Full EDMD history is available to the oracle but not to a kinetic runtime block.

## Decision

Label features runtime-observable, shadow-probe, or oracle-only and reject online policies that consume disallowed tiers.

## Consequences

Upper bounds and practical policies become distinct evidence products.
