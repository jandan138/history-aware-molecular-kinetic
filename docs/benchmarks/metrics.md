# Metrics

## 1. Conservation

\[
\epsilon_M=\frac{|M(t)-M(0)|}{\max(|M(0)|,\epsilon)},
\]

\[
\epsilon_E=\frac{|E(t)-E(0)|}{\max(|E(0)|,\epsilon)},
\]

\[
\epsilon_P=\|P(t)-P(0)\|.
\]

Separate solver drift from conversion jumps and boundary work.

## 2. Field error

For scalar field \(q\):

\[
e_q=\frac{\|q-q_{\mathrm{ref}}\|_{L^2}}{
\max(\|q_{\mathrm{ref}}\|_{L^2},\epsilon)}.
\]

Report spatial maximum and region-conditioned errors as well.

## 3. Distribution error

Candidate metrics:

- total variation on a fixed histogram;
- Wasserstein distance;
- Jensen–Shannon divergence;
- projected moment error;
- characteristic-function distance.

Histogram bins and velocity normalization are frozen per case.

## 4. Stress and heat flux

Report tensor component error, invariant norms, and principal directions—not only
one scalar norm in anisotropic cases.

## 5. Pair structure

- radial distribution \(g(r)\);
- contact-value error;
- integrated pair discrepancy over a declared radius range;
- nearest-neighbor distribution;
- optional structure factor.

## 6. Collision statistics

- collision rate;
- inter-collision time distribution;
- impact-angle distribution;
- repeated-pair ratio in exact windows;
- graph circuit rank and component statistics;
- re-encounter time.

## 7. Indicator metrics

### Regression

- grouped MAE/RMSE;
- rank correlation;
- tail-weighted error;
- calibration and uncertainty coverage.

### Classification

- error-threshold recall;
- false-negative rate;
- precision;
- exact-region fraction;
- cost-weighted utility;
- grouped confidence intervals.

### Incremental value

\[
\Delta=\mathrm{metric}(S+H)-\mathrm{metric}(S).
\]

Report bootstrap confidence intervals over held-out groups.

## 8. Partition metrics

- exact/probe/kinetic volume fraction;
- switches per block per unit time;
- mean residence time;
- interface area;
- budget saturation time;
- oracle high-error coverage;
- conversion failure count.

## 9. Performance

- end-to-end wall time;
- time by solver/history/conversion/probe/IO/renderer;
- peak memory;
- events or collision samples per second;
- strong/weak scaling where relevant;
- cost per physical time and per accepted error.

## 10. Visual metrics

Visual metrics supplement, not replace, physical error:

- fixed-camera temporal image difference;
- popping at conversion frames;
- track continuity for exact particles;
- density/volume temporal consistency;
- matched-display-particle comparison.

## 11. Statistical reporting

Use independent seed families and grouped bootstrap intervals. Report sample
counts, missing runs, and outlier policy. Do not average model-not-applicable runs
into ordinary error.
