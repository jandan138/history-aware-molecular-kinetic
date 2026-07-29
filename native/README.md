# Native compute plane

This directory contains the stable C++20 semantic boundary and small correctness
references. It does **not** yet contain the production EDMD, DSMC, Enskog, CUDA,
or HIP implementations.

The first native code deliberately implements only a rolling collision-history
reference so that future GPU sketches can be compared against a simple exact
implementation.
