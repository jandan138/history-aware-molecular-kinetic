# Security policy

This is research software, not a safety-certified simulator. Report security
issues privately to the repository owner before public disclosure.

External solver adapters execute user-configured binaries. Treat configuration,
geometry, and post-processing scripts as untrusted input. The project does not
download or execute third-party solvers automatically in CI.
