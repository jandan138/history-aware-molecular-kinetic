# E6 render toolchain lock

The cinematic renderer is installed outside the repository; the repository never
vendors Blender.

Frozen local install:

- archive: `blender-5.2.0-linux-x64.tar.xz`;
- archive SHA-256: `96f6c181a30f4950607839dc84d42a354b250d8a0231b098b59b7bc69c351c48`;
- Blender: `5.2.0 LTS`, build hash `fbe6228777e7`;
- GPU: NVIDIA GeForce RTX 4090, driver `591.86`;
- actual E6 device backend: Cycles CUDA, explicitly selected and recorded.

Required runtime:

- Blender `5.2.0` official Linux x64 archive;
- RTX 4090 visible through WSL;
- Cycles GPU rendering for final output;
- Three.js for real-time style checks; this WSL's eight-SSBO OpenGL context cannot
  run Blender 5.2 Eevee reliably, so even the verified Blender preview uses Cycles
  CUDA at 24 samples;
- ffmpeg for delivery encoding;
- Node/npm versions pinned by the E6 companion lockfile.

Final rendering may not silently fall back to CPU. OptiX initialization returns
driver-bridge error `7805` in the current WSL runtime, while Blender enumerates the
RTX 4090 as a CUDA device. E6 therefore selects CUDA explicitly; every render
manifest records `device_backend` and `enabled_devices`. A missing requested GPU
device is a hard error.

Blender 5.2 requires OpenGL 4.3 for scene setup. The current WSL D3D12 Mesa path
exposes only OpenGL 3.3, so batch rendering uses an Xvfb llvmpipe setup context and
Cycles CUDA for the actual render computation. The local compatibility library is
outside the repository and does not affect bundle or scene content.

Genesis neutral validation follows the local Genesis skill wrapper and must resolve
`genesis` to `/home/zhuzihou/dev/Genesis/genesis/__init__.py`.

The verified Genesis runtime is `0.4.4`, CPU + OSMesa Rasterizer. Software OSMesa
does not support shadows or plane reflections here, so Genesis is intentionally a
neutral source-state validation image—not a candidate cinematic renderer.

## WSL production incident and permanent rule

On 2026-08-01, after the complete `960×540`, 151-frame Cycles/CUDA source animation
had rendered successfully, a `3840×2160`, 384-sample still launch coincided with
termination of the WSL instance. Persistent journal evidence does **not** show a
Linux OOM killer, `Killed process blender`, or an abrupt kernel failure. Instead it
records:

```text
Operation canceled @p9io.cpp:258 (AcceptAsync)
systemd-logind: System is powering down
...
Reached target Power-Off
```

The guest had a `24 GB` memory limit and `8 GB` swap. This evidence means the WSL
host channel was cancelled and the guest received an orderly power-off; it does
not establish whether the initiating Windows-side event was a WSL service reset,
sleep/shutdown, or a DXG/CUDA bridge failure. A high-resolution GPU launch is only
a temporal correlate and must not be reported as a proven cause.

Permanent production rule:

- WSL may generate shot bundles, Web builds, Genesis neutral checks, and Cycles
  CUDA previews no larger than 1080p;
- WSL final delivery is limited to the already verified 151-frame source preview
  and 45-second H.264 animatic;
- 4K, EXR, and high-sample final batches run in native Windows Blender from the
  same read-only shot bundle;
- every GPU render must name its requested device, and a missing device is a hard
  failure rather than a CPU fallback;
- disk-resident PNG frames are not treated as resident memory; resource diagnosis
  must rely on OOM/DXG/host logs rather than file size or intuition.

This is a production reliability boundary, not a new scientific experiment and
not an excuse to expand E6 with defensive benchmark grids.
