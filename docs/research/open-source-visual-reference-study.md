# Open-source visual reference study for E6

This study records implementation patterns that can improve the Molecular Time
Machine Hero. It is not a visual-style shopping list and does not authorize copying
code or assets without respecting their licenses.

## Reference matrix

| Project | What its implementation demonstrates | E6 decision |
|---|---|---|
| [Molecular Nodes](https://github.com/BradyAJohnston/MolecularNodes) | A translation layer turns scientific trajectory data into point attributes, then Blender Geometry Nodes instances and styles the geometry efficiently. | Use one animated point cloud plus instanced spheres and role attributes. Do not create one heavyweight animated object per particle. Study the architecture; do not copy GPL source into HAMK. |
| [Many-Worlds Browsing](https://graphics.cs.cmu.edu/projects/mwb/) | Browse and edit modes separate exploration from scene changes; motion can be summarized as long-exposure paths. | Present E5's 30 legal previews as a compact future fan and keep the selected world visually dominant. |
| [Unified Many-Worlds Browsing](https://graphics.stanford.edu/papers/umwb/) | Cached simulation ensembles support interactive spatiotemporal queries, ranking, and GPU visualization. | Reuse the target-region/query grammar in the companion, while distinguishing HAMK's collision history and same-resolved-present surgery from sample browsing. |
| [Neural Flow Maps](https://github.com/yitongdeng-projects/neural_flow_maps_code) | The solver writes renderer-neutral frame caches and a dedicated visualization tool consumes them. | Make the versioned E6 shot bundle the only boundary between physics and Blender/Three.js. |
| [Incremental Potential Contact](https://ipc-sim.github.io/) | One unmistakable physical phenomenon anchors the teaser, paper figure, video, source, and data release. | Keep E5 E→C-like as the single signature phenomenon rather than a montage of defensive cases. |
| [Mitsuba 3](https://www.mitsuba-renderer.org/) | A research renderer separates scene data, materials, lights, cameras, and integrators. | Keep camera/material/render settings versioned and hashable. Mitsuba is a quality reference, not a second production dependency. |
| [Fresnel](https://fresnel.readthedocs.io/en/latest/) | A compact path tracer targets publication-quality soft-matter particle images with intuitive material controls. | Use restrained roughness, specular response, outline hierarchy, and global illumination rather than texture-heavy assets. |
| [Three.js post-processing](https://threejs.org/manual/en/post-processing.html) | A pass-based real-time pipeline composes tone mapping, bloom, and other effects after the scene render. | Use WebGL2 instancing with selective bloom and ACES tone mapping for the companion; the cinematic master remains offline Cycles. |

## Reusable implementation pattern

The closest successful projects share one production shape:

```text
scientific computation
  → immutable cache with stable IDs
  → renderer-specific translation layer
  → instanced geometry and attribute-driven styling
  → one signature camera sequence
  → separate cinematic and interactive outputs
```

E6 adopts that shape directly. The scientific artifact owns positions, velocities,
IDs, roles, events, and metrics. The renderer owns only world-space embedding,
camera, light, material, annotation, and post-processing.

## Visual techniques to borrow

- Instance particles from one point geometry and update the point coordinates per
  frame.
- Encode passive color, target membership, causal membership, and edited membership
  as separate attributes; never overwrite passive physical color to indicate a
  branch.
- Use only selective trails. A full 256-particle trail field is reserved for a
  short long-exposure transition, not the comparison view.
- Use a future fan for the 30 cached E5 candidates, then collapse it into the
  selected branch.
- Render object-ID/Cryptomatte passes so target and edited particles remain
  selectable in compositing.
- Produce a neutral locked comparison from the same shot bundle as the cinematic
  view.

## License and asset policy

- External projects in this document are references unless a separate source lock
  explicitly declares a dependency.
- Blender is the production tool; Blender project files and scripts remain HAMK
  artifacts.
- Three.js dependencies are pinned by the JavaScript lockfile.
- Final materials and lights are procedural. Any font, audio, HDRI, or mesh asset
  must be listed in the E6 asset ledger with source, author, license, and hash.
- No external project footage appears in the final teaser.
