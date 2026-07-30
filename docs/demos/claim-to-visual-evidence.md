# Claim-to-Visual Evidence Matrix

这张矩阵回答：**每条论文 claim 最终怎样变成一个可观察的物理量、一个像素差异和一个具体 shot。**

| Claim | Scientific observable | Visual manifestation | Primary shot | Quantitative companion | Failure interpretation |
|---|---|---|---|---|---|
| C3 History adds value beyond state/geometry | matched-state future EDMD–kinetic discrepancy | state 相近的两个 chamber 未来 plume/residence/escape 不同 | CL-02/03/04 | state distance、history distance、future error、held-out delta | 只看到 graph 不同但未来 observable 不同不明显，则 graphics claim 不成立 |
| C4 Practical history/probe policy retains value | recall/calibration under probe budget | practical mask 接近 oracle upper bound，少于 full exact | CL-05/06, EV-03/05 | operational recall、probe cost、exact fraction | 只有 oracle history 有效，则在线 LOD claim 失败 |
| C5 Exact→kinetic demotion is conservative | M/P/E、stress、heat flux、downstream transient | volume/species 不跳，流动继续平滑 | ZM-04 | conversion report、field continuity、pop score | 画面平滑但指标跳变，说明 renderer 隐藏了物理错误 |
| C6 Kinetic→exact promotion is valid | overlap、g(r)、velocity distribution、warm-up transient | 新 exact particles 不爆开、不突然成团 | ZM-03/04 | overlap count、pair statistics、transient error | 靠淡入隐藏 invalid particles，不算通过 |
| C7 Dynamic policy improves Pareto frontier | physical error vs time/memory/exact fraction | plume/observable 接近 reference，exact region 只占局部 | EV-02/03/06 | Pareto curve、exact fraction、wall-clock、memory | 画面更好但成本接近 full EDMD，则 LOD 价值不足 |
| C8 At least two physical effects are visibly restored | two predeclared observables | plume angle/species ridge、labyrinth residence/escape 等 | EV-02 + CL-04/05 | metric error reductions | 只在 diagnostics 中可见，不足以支撑 SIG graphics value |
| C9 Zoomable macro/molecular view without camera coupling | partition invariant under camera change | volume → display particles → exact identities 无 popping | ZM-01/02/03/05, EV-04 | camera–physics hash audit、display continuity | 相机触发 refinement 或只靠重采样伪装 identity，则失败 |

---

## 1. Scene responsibility rule

- **Expansion into Vacuum** 不负责证明 C3 的全部因果性；它主要证明 C7/C8/C9 和视觉上限。
- **Correlation Labyrinth** 不负责做最漂亮 teaser；它主要证明 C3/C4。
- **Zoomable Mixing Chamber** 不负责证明 history-aware refinement 必要；它主要证明 C5/C6/C9。

场景职责分离可以防止每个 Hero Scene 都变成塞满所有 overlay 的大杂烩。

---

## 2. Pixel audit

每个 primary panel 在冻结前填写：

```text
claim_id:
run_id:
artifact_hashes:
physical_observable:
expected_pixel_change:
camera_hash:
comparison_lock_hash:
renderer_hash:
metric_version:
alternative_explanation:
```

若无法写出 `expected_pixel_change`，说明该 claim 还没有真正映射到图形证据。

---

## 3. Alternative explanations to exclude

### Display density

粒子更密会让 plume 或 mixing 看起来更“丰富”。必须锁定或报告有效显示密度。

### Transfer function

不同 opacity curve 会改变 apparent plume width。必须锁定。

### Temporal filtering

强滤波会让 proposed 看起来更稳定。必须共享。

### Seed selection

随机气体视觉差异可能来自 seed。Hero frame 的选择规则必须预注册，主结论使用 ensemble metric。

### Reference scaling

降尺度 full EDMD 不是自动 ground truth。必须声明分辨率和 convergence status。

### Geometry occlusion

不同相机或 cutaway 可能暴露/隐藏差异。Primary comparison 锁定相机。
