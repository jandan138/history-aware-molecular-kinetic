# Molecular Time Machine E6 companion

This static Three.js client reads the same renderer-neutral shot bundles used by
Blender. It does not run or modify physics.

```bash
.venv/bin/python scripts/stage_e6_web_data.py
cd demos/e6-web
npm install
npm run dev
```

The four views follow the paper spine: Reveal, Branch, Trace, and Author. Generated
shot data, dependencies, and `dist/` remain untracked; the package lock is tracked.
