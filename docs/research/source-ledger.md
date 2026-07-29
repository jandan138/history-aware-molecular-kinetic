# Source ledger

The machine-readable source of truth is
[`references/sources.yaml`](../../references/sources.yaml).

It records:

- paper and software identifiers;
- exact upstream repository revisions;
- license boundaries;
- project role;
- integration method;
- claims supported and claims explicitly not supported.

External revisions are updated intentionally through an ADR and adapter
revalidation. “Latest main” is never a reproducible oracle.
