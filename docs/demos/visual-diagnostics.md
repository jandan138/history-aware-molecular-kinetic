# Visual diagnostics

## Required overlays

### Representation mask

Exact, Boltzmann DSMC, Enskog, probe, interface buffer, and unresolved blocks use
stable categorical labels.

### Indicator decomposition

Display state-only score, history/probe increment, uncertainty, thresholds, and
cooldown.

### Collision graph

For selected blocks, draw recent true exact collision edges with age fading.
Do not draw DSMC stochastic pairings as if they were exact molecular history.

### Conservation timeline

Mark every conversion and plot solver versus conversion contributions to mass,
momentum, and energy error.

### Distribution view

Show velocity histogram/phase-space slice, stress, heat flux, and pair structure
for selected regions.

### Reference error

Show a declared observable difference against full exact or another applicable
reference, with a fixed scale.

## Diagnostic-first rule

A scene is not ready for hero rendering until the diagnostic view makes the
method's success and failure understandable.


## Production linkage

Diagnostic layers are defined in `configs/render/diagnostic.yml`. They transition into the locked scientific renderer only through V1; dense overlays do not automatically enter Hero mode. See [Art Direction](art-direction.md) and [Visual Acceptance Criteria](visual-acceptance-criteria.md).
