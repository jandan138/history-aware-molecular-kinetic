# Dependency and license boundaries

## Core license

Original project code and documentation use Apache-2.0.

## External software

| Source | Recorded license | Integration |
|---|---|---|
| DynamO | GPLv3 at pinned revision | external executable/container |
| SPARTA | GNU GPL at pinned revision | external executable/container |
| uniGasFoam | GPLv3-or-later | external OpenFOAM environment |
| Future Enskog code | source-specific | reference-only until reviewed |

The exact upstream license file is authoritative.

## Prohibited actions

- copying GPL implementation files into `src/` or `native/`;
- distributing combined binaries/images without license review;
- removing upstream notices;
- treating paper equations as permission to copy source code;
- committing generated proprietary geometry or datasets without rights.

## Allowed default integration

- users install the external tool separately;
- an adapter writes input files and launches a configured executable;
- outputs are converted to project-owned schemas;
- publication artifacts cite and identify the upstream tool and revision.

## Container images

A container that bundles external GPL software may have distribution obligations
beyond this repository. Container recipes and published images require separate
review.

## Source lock

`references/sources.yaml` records the revision used for reference generation.
Updating a revision requires adapter revalidation and an ADR if primary evidence
changes.
