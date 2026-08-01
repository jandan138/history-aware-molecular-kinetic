# Molecular Time Machine E6 integration result

## Decision

**`go_e6_integration`** on 2026-08-01.

E6 turns the frozen E1/E3/E4/E5 evidence into one visual system without adding a
new scientific experiment suite. The result is a complete renderer-neutral data
path, a real-time companion, a neutral Genesis validation, a Blender/Cycles source
animation, and an exact 45-second Hero preview master.

The paper story remains:

```text
E1  a frame is not a future
E2  a slider is not a history
E3  one past collision is editable
E4  choose the consequence and find its cause
E5  same visible present, chosen physical future
E6  make that positive authoring result legible and memorable
```

No seed grid, density sweep, random-surgery baseline, second edit family, geometry
edit, user study, failure reel, or 3D physics rewrite was added.

## Shared shot contract

All consumers read frozen coordinates and metadata from the same E6 bundle schema.
The bundle carries particle IDs, common frame times, planar coordinates, physical
radius, branch labels, roles, events, metrics, source hashes, and a comparison
lock. It explicitly declares that the renderer cannot modify physics or apply
post-hoc particle correction.

| Shot | Bundle ID | Manifest SHA-256 |
|---|---|---|
| Reveal / E1 | `e6-shot-946c374040091e5b` | `d8d220b1d612bd89f8dd94254643a02b9a3fb852f5d94d9b6449815ff230f53d` |
| Branch / E3 | `e6-shot-9fd3ed33c1526fbb` | `3bb0f6fe31072281f7eaa7a08d17049ecac2cf33f54f6a708f340f3147cc8737` |
| Trace / E4 | `e6-shot-0816814e2f66fafe` | `dd5d1075c0a6efa32be598d8e52340242c971ad1119ba3633b8910765c0cf46a` |
| Author / E5 | `e6-shot-05dd14049871a525` | `f43d685f116ad3916ef386c20718506a31ecf0826d04cb90933bb400ebb736d1` |

The E5 Author bundle contains two branches, 51 common samples, and 256 particles.
The branches have identical particle positions at the registered `t=0.80` pivot.

## Visual deliverables

### Blender/Cycles source

- Blender `5.2.0 LTS`, build `fbe6228777e7`;
- Cycles CUDA explicitly selected;
- enabled device: NVIDIA GeForce RTX 4090;
- `960×540`, 24 fps, 151 frames, 6.291667 seconds;
- physical coordinates are linearly sampled between frozen bundle frames;
- output SHA-256:
  `0f9446ef55724acc89e6752a8f2fe9024f38396be3905ef4cf9dcba684edd0e9`;
- render manifest records `physics_state_mutated=false`.

### Forty-five-second Hero preview

- title: **Same Present, Chosen Future**;
- exact duration: `45.000000` seconds;
- exact cadence: `24/1` fps;
- exact frame count: `1080`;
- operations: trim, retime, hold, caption, encode;
- particle pixels are never spatially warped;
- output SHA-256:
  `03820a1167c56efb3855d378cd74cd02110229a815f8906110e649a39b09655f`;
- composition manifest records `physics_state_mutated=false`.

The 45-second sequence selects the desired future, returns to the common pivot,
shows the bounded 30-preview authoring palette, exposes two hidden
velocity-ownership swaps touching `4/256` particles, and resolves the original E
against the selected C-like future. The final card reports the frozen E5 outcome:
`75%` target reduction and `100%` collateral retention.

### Three.js companion

The static companion exposes Reveal, Branch, Trace, and Author views with a shared
black-obsidian visual language, locked branch framing, a physical-time scrubber,
and concise claim-linked metrics. It renders cached exact trajectories and runs no
browser physics. The pinned npm install reports zero known vulnerabilities and the
Vite production build succeeds.

Tracked client hashes:

- `package-lock.json`:
  `f832059346a63090f1921e05dd9b545064ee24836d9441d331c268abdafe05cb`;
- `src/main.js`:
  `bf241b7310010d6307d5dd90872c49f4230c3ba81a91f19cb086b2921e41324f`;
- `src/style.css`:
  `be9a923c58e8bdf65f43ac9a375d07e775a764c1eb5dc629de3432fe56dab006`.

### Genesis neutral validation

The canonical wrapper resolves Genesis to
`/home/zhuzihou/dev/Genesis/genesis/__init__.py`, version `0.4.4`, and passes its
local frame/video smoke verification. The E5 terminal bundle is then instantiated
as read-only fixed spheres under the CPU/OSMesa Rasterizer.

The neutral output SHA-256 is
`4483690a140f7d9752cc287c9fb3de924dbc602834e7069502e55e1192d07119`.
OSMesa lacks shadows and plane reflections on this host, so the frame validates
source-state consumption rather than cinematic quality.

## Production boundary

The WSL pipeline is validated through the 1080p-or-smaller CUDA preview class. A
4K/384-sample launch coincided with an orderly host-initiated WSL power-off; the
persistent journal contains no Linux OOM-killer evidence. The exact incident and
the resulting native-Windows 4K export rule are recorded in the
[E6 render toolchain](../reproducibility/e6-render-toolchain.md).

Therefore this result closes E6's data, interaction, story, and reproducibility
integration gate. It does not falsely label the preview encode as the final 4K/EXR
submission master. That final export consumes the same bundle and scene in native
Windows Blender; it creates no new claim and requires no new experiment.

## Verification

At the E6-v0 integration checkpoint:

- Ruff: pass;
- strict mypy: pass over 83 source files;
- pytest: `70 passed`;
- MkDocs strict build: pass;
- npm audit: zero known vulnerabilities;
- Vite production build: pass;
- Hero probe: `45.000000 s`, `1080` frames, `24/1` fps.

The frozen E5 numbers remain the scientific and authoring result. E6 changes how
that result is communicated, not what was simulated.
