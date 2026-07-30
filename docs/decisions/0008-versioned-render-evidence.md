# ADR 0008 — Versioned render evidence

## Status

Accepted.

## Context

The final graphics evidence must remain reproducible and fair across full exact,
full kinetic, state-only adaptive, history/probe-aware, and oracle-upper-bound
methods. A renderer configured informally at paper deadline can silently change
camera, display density, transfer functions, temporal filtering, or even the
interpretation of statistical display particles.

## Decision

Rendering is a versioned evidence subsystem:

- render configuration validates against `render-config.schema.json`;
- camera paths are explicit, versioned files;
- each output writes `render-manifest.schema.json` metadata;
- primary comparisons use a comparison-lock hash;
- renderer and physics communicate only through canonical artifacts;
- camera/display LOD cannot modify physical partitioning;
- statistical display identities are non-physical;
- Hero renders supplement but do not replace neutral shared comparisons.

A dependency-free manifest-only reference implementation is maintained so the
contract can be tested before a production renderer exists.

## Consequences

Positive:

- every figure and shot can be traced to inputs and settings;
- unfair method-specific visual overrides are detectable;
- renderer backends remain replaceable;
- visual work can start early without owning physics state.

Costs:

- more schemas and manifests;
- camera and display changes create new evidence revisions;
- final editing must preserve shot provenance.

## Rejected alternatives

- storing only final videos;
- allowing renderer-specific hidden configuration;
- coupling physical refinement to camera distance;
- treating visual display particles as actual molecules.
