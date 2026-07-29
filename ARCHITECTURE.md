# Architecture

The authoritative architecture is maintained in
[`docs/architecture/overview.md`](docs/architecture/overview.md).

The repository separates five planes:

1. Python control and evidence orchestration;
2. native molecular/kinetic compute backends;
3. isolated third-party oracle adapters;
4. versioned scientific artifacts and metrics;
5. renderer-agnostic visualization.

No renderer may own simulation state, no external GPL solver is vendored into
the core library, and no paper claim may exist without a benchmark and artifact
path in `paper/claim-ledger.md`.
