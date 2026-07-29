# B4 — Dynamic molecular–kinetic LOD

## 1. Online policies

Compare:

1. full exact EDMD;
2. full Boltzmann DSMC;
3. full Enskog/finite-density kinetic where applicable;
4. state-only adaptive policy;
5. oracle-history upper bound;
6. practical history/probe-aware policy;
7. camera-only rendering LOD with unchanged physics as a visual control.

## 2. Controller components

- promote and demote thresholds;
- hysteresis gap;
- minimum residence/cooldown time;
- exact-region budget;
- spatial dilation and interface buffers;
- probe scheduling;
- uncertainty escalation;
- conversion rejection handling;
- model-applicability fallback.

## 3. Primary metrics

### Physical error

The B1 observable set evaluated over time and space.

### Cost

- wall time;
- GPU/CPU time by subsystem;
- memory and peak particle count;
- exact event count;
- DSMC collision samples;
- probe cost;
- conversion cost;
- load imbalance.

### Partition quality

- exact-region fraction;
- oracle-error recall;
- false refinement;
- representation switches per block/time;
- interface surface area;
- time spent in immature history state;
- budget saturation.

### Stability

- global and conversion conservation;
- partition chatter;
- failed conversions;
- non-finite or overlapping states;
- controller determinism under fixed seeds.

## 4. Cost-quality curves

Do not compare one hand-picked configuration. Sweep budgets/thresholds and plot:

\[
\text{error versus wall time},
\quad
\text{error versus memory},
\quad
\text{error versus exact fraction}.
\]

The proposed method must improve the Pareto frontier relative to state-only
adaptivity and uniform baselines.

## 5. Online observability

The practical policy may use:

- runtime coarse state;
- exact history inside existing exact blocks;
- bounded shadow probes;
- prior conversion reports;
- uncertainty estimates.

It may not use future exact error, full-domain EDMD history, or renderer camera by
default.

## 6. Dynamic cases

- moving exact patch around a moving wall or object;
- transient expansion whose high-error region travels;
- labyrinth flow with persistent and disappearing correlated pockets;
- mixing chamber where physical and visual LOD are separately varied.

## 7. Exit gate

B4 passes only if:

- the practical policy retains meaningful B2 gain;
- exact fraction is neither nearly zero nor nearly one in target scenes;
- partition chatter is controlled;
- conversion/interface error stays subordinate;
- at least one cost-quality frontier is improved;
- failure indicators identify out-of-model regimes.
