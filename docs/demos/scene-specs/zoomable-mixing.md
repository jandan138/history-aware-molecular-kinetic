# Scene Spec — Zoomable Mixing Chamber

## 1. Role

该场景是 **representation conversion 与 zoomability 教程场景**，主要支撑 C5、C6、C9。

它不负责证明 collision history 对 mixing 必不可少。

---

## 2. Geometry budget

- 长方体透明 chamber；
- 中央 divider；
- 可选 rounded edge；
- 不使用复杂 CAD；
- 无 rigid-body dynamics；
- divider motion 由预定义轨迹控制。

---

## 3. Physical setup

- 两种等质量/等直径 species；
- 初始温度一致；
- 左右 concentration 不同；
- divider 在固定时刻打开；
- packing fraction 位于 B3/B4 已验证范围；
- exact/kinetic conversion 由 frozen B4 policy 决定。

---

## 4. Required methods

- full exact reference（可在受控规模）；
- full kinetic；
- naive conversion baseline；
- state-only dynamic LOD；
- practical history/probe dynamic LOD；
- proposed temporal display policy；
- frame-wise independent display resampling baseline。

---

## 5. Primary observables

- species mass；
- concentration profile；
- velocity distribution；
- M/P/E conversion budget；
- overlap count；
- local pair statistics after promotion；
- volume integral continuity；
- exact identity track continuity；
- camera–physics partition invariance。

---

## 6. Required artifacts

```text
particle-bundle
kinetic-bundle
block-state
partition-mask
conversion-report
geometry-bundle
metrics-report
run-manifest
```

---

## 7. Shots

使用 [Storyboard](../storyboard.md) 中的 ZM-01 至 ZM-05。

Scene render config：

```text
configs/render/scenes/zoomable-mixing.yml
```

Benchmark case：

```text
benchmarks/b5_graphics_evidence/cases/candidate/B5-ZOOM-MIX-v0.yml
```

---

## 8. Visual acceptance

- conversion frame 不是 frame-difference 极端 outlier；
- species volume 在表示切换时连续；
- exact identities 不被 display resampling 替换；
- camera path 改变后 partition artifact hash 不变；
- proposed temporal display 相对 frame-wise resampling 明显减少 boiling；
- neutral 与 hero mode 结论一致。

---

## 9. Failure reel

必须保留：

- naive independent resampling；
- 无 hysteresis 的 rapid switching；
- promotion overlap failure；
- volume/particle double-counting 造成的亮度跳变；
- camera-triggered physics refinement 作为禁止示例。

---

## 10. Stop condition

若 conversion 的主要视觉连续性只能依靠未来帧滤波，而物理/统计 artifact 本身不连续，停止 B5，返回 B3/B4。
