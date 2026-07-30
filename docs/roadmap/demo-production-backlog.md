# Demo Production Backlog

> 该 backlog 将视觉生产从“B4/B5 deferred”改成受 gate 控制的正式工作流。编号可以直接转成 GitHub Issues。

---

## 1. Contracts and reproducibility

- **RENDER-001** 定义 `render-config.schema.json`。
- **RENDER-002** 定义 `render-manifest.schema.json`。
- **RENDER-003** 实现 deterministic config/artifact/comparison-lock hashing。
- **RENDER-004** 实现 manifest-only reference renderer。
- **RENDER-005** 增加 render config/schema CI validation。
- **RENDER-006** 记录 renderer version、host、GPU、driver 与 output hashes。
- **RENDER-007** 实现 comparison-lock audit CLI。

Dependencies: INFRA-001/003。

---

## 2. V0 Artifact Replay Viewer

- **VIEW-001** exact particle bundle playback。
- **VIEW-002** kinetic display sample playback。
- **VIEW-003** block state 与 partition mask overlay。
- **VIEW-004** density/temperature/species volume slice/raymarch。
- **VIEW-005** geometry bundle playback。
- **VIEW-006** collision-event temporal window viewer。
- **VIEW-007** block inspection panel：velocity histogram、stress、heat flux。
- **VIEW-008** deterministic frame scheduler。
- **VIEW-009** image sequence/contact-sheet export。

Dependencies: R0 converters、artifact schemas。可与 M1/M2 并行。

---

## 3. V1 Shared Scientific Renderer

- **SHARED-001** camera path/config loader。
- **SHARED-002** exact/statistical display radius and density lock。
- **SHARED-003** shared volume transfer function。
- **SHARED-004** difference view 与 declared reference pairing。
- **SHARED-005** four-panel comparison layout。
- **SHARED-006** render manifest + comparison-lock report。
- **SHARED-007** method-specific override detector。
- **SHARED-008** frame-to-run/metric provenance overlay。

Dependencies: VIEW-001–009、B1 artifact joins。

---

## 4. V2 Conversion and Zoom

- **ZOOM-001** persistent statistical display IDs 或共享 temporal sampling。
- **ZOOM-002** volume/particle partition-of-unity display blending。
- **ZOOM-003** exact identity trail rendering。
- **ZOOM-004** camera–physics decoupling audit。
- **ZOOM-005** frame discontinuity/pop metric。
- **ZOOM-006** naive frame-wise resampling baseline。
- **ZOOM-007** conversion timeline panel。
- **SCENE-ZM-001** 冻结 Zoomable Mixing geometry and camera。
- **SCENE-ZM-002** 完成 ZM-01–ZM-05 shots。

Dependencies: G4 conversion pass、SHARED track。

---

## 5. V3 Flagship Expansion into Vacuum

- **SCENE-EV-001** 冻结 primitive chamber/nozzle geometry。
- **SCENE-EV-002** 预注册 plume observables。
- **SCENE-EV-003** 生成 full kinetic/state-only/proposed/oracle/reference artifact family。
- **SCENE-EV-004** 实现 EV-01–EV-03 neutral comparison。
- **SCENE-EV-005** 实现 EV-04 macro-to-micro shot。
- **SCENE-EV-006** 实现 EV-05 state/history diagnostic inset。
- **SCENE-EV-007** 实现 EV-06 Pareto synchronization。
- **SCENE-EV-008** 实现 EV-07 failure indicator shot。
- **ART-001** 透明 chamber/nozzle hero material。
- **ART-002** shared motion blur/tone mapping。

Dependencies: G5 dynamic benefit、ZOOM track。ART tasks 只有 EV-01–03 neutral pass 后解锁。

---

## 6. Correlation Labyrinth

- **SCENE-CL-001** 生成 matched-state geometry families。
- **SCENE-CL-002** 冻结 matched block selection rule。
- **SCENE-CL-003** collision graph simplification/layout。
- **SCENE-CL-004** future discrepancy playback。
- **SCENE-CL-005** state-only/practical/oracle policy panel。
- **SCENE-CL-006** held-out geometry shot。
- **SCENE-CL-007** residence/escape physical visualization。

Dependencies: G3 history value。若 G3 fail，不做 hero polish。

---

## 7. Final video and paper assets

- **VIDEO-001** 30–45 s teaser edit。
- **VIDEO-002** 3–5 min full video edit。
- **VIDEO-003** voice-over script 与术语审计。
- **VIDEO-004** captions、units、method names lock。
- **VIDEO-005** supplementary failure reel。
- **VIDEO-006** per-shot provenance manifest。
- **VIDEO-007** primary figure frame recipes。
- **VIDEO-008** artifact package 与 reproduction instructions。
- **VIDEO-009** final comparison-lock audit。
- **RELEASE-001** 建立 shot/figure evidence registry。
- **RELEASE-002** 冻结 camera file content hashes 与 renderer digest。
- **RELEASE-003** 生成 primary frame recipes 和 contact sheets。
- **RELEASE-004** 从 clean output directory 做 release reproduction smoke test。
- **RELEASE-005** 打包 neutral/hero 对照、failure reel 与 `reproduce.md`。

Dependencies: G6 graphics value、三场景 primary shots。

---

## 8. Prioritization

### Must-have for a credible paper

```text
RENDER-001–007
VIEW-001–009
SHARED-001–008
ZOOM-001–007
SCENE-EV-001–008
SCENE-CL-001–007
VIDEO-005–009
RELEASE-001–005
```

### Hero polish, only after gates

```text
ART-001–002
VIDEO-001–004
```

### Explicitly out of scope for the first paper

- production path tracer；
- complex spacecraft/industrial CAD；
- interactive editor；
- VR；
- combustion/chemistry；
- general rigid-body coupling；
- artist-authored turbulence；
- real-time game integration。
