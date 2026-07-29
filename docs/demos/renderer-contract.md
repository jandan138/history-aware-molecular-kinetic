# Renderer contract

## Inputs

The renderer accepts only canonical artifacts:

- particle bundle;
- block-state bundle;
- partition mask;
- collision/history features;
- geometry bundle;
- camera/render configuration.

## Outputs

- image sequence or video;
- render manifest;
- input artifact hashes;
- camera and transfer-function hash;
- display sample policy;
- timing.

## Display particles

Statistical display particles are explicitly marked non-physical. They may be
resampled for rendering but cannot enter conservation metrics or collision
history.

## Comparison lock

Primary comparison groups share:

- camera path;
- resolution and frame times;
- geometry and materials;
- transfer functions;
- display particle density;
- motion blur and temporal filtering.

## Forbidden behavior

- changing the physics state;
- deleting “ugly” particles by method-specific rules;
- applying different smoothing to different methods;
- using future frames to stabilize only the proposed result;
- rendering exact particles more densely than baselines without disclosure.
