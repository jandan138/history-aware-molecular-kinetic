# uniGasFoam adapter

**Role:** state-based adaptive USP–DSMC baseline
**License boundary:** GPLv3-or-later; external process/container only.

The adapter lifecycle is:

```text
canonical case -> upstream input -> external execution -> raw output
-> audited canonical conversion -> metrics
```

The adapter must record the executable hash, upstream revision, command line,
environment, raw-output hashes, converter version, and any normalization choices.
No adapter may silently repair an invalid upstream run.
