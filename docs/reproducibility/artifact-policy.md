# Artifact policy

## Committed

- schemas and compact examples;
- case and experiment manifests;
- small derived data supporting tests;
- figure/table recipes;
- source and license ledgers.

## Not committed by default

- external source checkouts;
- raw solver outputs;
- large particle/field arrays;
- videos and image sequences;
- build products;
- private assets.

## Released artifacts

A publication artifact may use GitHub Releases, Zenodo, or institutional storage
and must include checksums and a manifest connecting each file to run IDs.

## Raw preservation

Oracle raw output is preserved until the canonical converter and primary metrics
are independently audited.


## Render evidence

Render configs, camera paths, manifests, frame recipes, comparison-lock reports, and small contact sheets are committed when compact. Large image sequences and videos remain external artifacts with checksums. Every released primary frame maps to run IDs, input artifact hashes, render config hash, camera hash, display-policy hash, and renderer version.
