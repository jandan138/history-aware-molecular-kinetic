# Scene Spec — Expansion into Vacuum

## 1. Role

这是 **visual flagship**，主要支撑 C7、C8、C9，并承载 teaser 与首页大图。

---

## 2. Geometry budget

- 单一 high-pressure chamber；
- 一个 aperture/nozzle；
- 大型 low-density exterior domain；
- 可选简单 plate 用于 plume impingement；
- 透明 cutaway shell；
- 不使用复杂 spacecraft CAD，除非 M7 后期只作为非 primary hero dressing。

---

## 3. Physical setup

- 初始 chamber 内均匀或已验证的 kinetic state；
- aperture 在固定时刻开启；
- exterior 初始为低密度或近真空；
- 同时存在 collisional、transitional 与 ballistic region；
- exact/kinetic partition 随误差与 probe evidence 移动；
- reference run 规模与 convergence status 明确。

---

## 4. Required methods

- full kinetic；
- state-only adaptive baseline；
- practical history/probe policy；
- oracle-history upper bound；
- full EDMD declared reference（可限域/降尺度，但需声明）；
- 可选 uniGasFoam baseline，取决于 canonical compatibility。

---

## 5. Primary observables

至少预注册两个：

- plume half-angle；
- centerline density decay；
- density ridge position；
- species front；
- velocity distribution anisotropy；
- aperture mass flux；
- plate pressure pattern；
- ballistic escape probability。

主画面优先使用 plume silhouette、species front 或 density ridge；velocity distribution 放 inset。

---

## 6. Required artifacts

```text
particle-bundle
kinetic-bundle
block-state
history/probe features
partition-mask
geometry-bundle
metrics-report
cost report
run-manifest
```

---

## 7. Shots

使用 EV-01 至 EV-07。

Scene render config：

```text
configs/render/scenes/expansion-into-vacuum.yml
```

Benchmark case：

```text
benchmarks/b5_graphics_evidence/cases/candidate/B5-EXPANSION-VACUUM-v0.yml
```

---

## 8. Visual acceptance

- plume physical difference 在 neutral render 中可见；
- proposed 与 reference 的 observable error 优于 state-only/full kinetic；
- exact front 不是单纯相机附近的一圈；
- EV-04 zoom 不改变 partition artifact；
- EV-06 的 Pareto point 与视频为同一 run family；
- display density 匹配后结论不变；
- exact/kinetic interface 不产生非物理 seam。

---

## 9. Failure reel

- exact fraction 接近 100%；
- state-only 与 proposed final plume 几乎相同；
- mask 看起来很动态但 physical observable 不变；
- coarse backend 在高密度区根本不适用却未触发 failure indicator；
- macro-to-micro 过渡出现亮度翻倍或 particle popping。

---

## 10. Stop condition

若该场景只有 representation mask 好看，最终 plume/flux/pressure 等 observable 没有稳定可见差异，则停止 hero polish。可以保留为系统展示，但不能作为 C8 的主要证据。
