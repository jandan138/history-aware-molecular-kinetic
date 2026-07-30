# Scene Spec — Correlation Labyrinth

## 1. Role

这是论文的 **scientific flagship**，主要支撑 C3 与 C4：碰撞历史或 bounded shadow probe 是否在强 state/geometry/finite-density controls 之外提供额外信息。

---

## 2. Geometry budget

- 两个或多个 rounded chambers；
- 狭窄通道；
- 一条促进 re-encounter 的回环路径；
- 一条 local moments 相近但 topology 不同的对照路径；
- 可选简单 moving gate；
- 所有几何由 boxes、capsules、cylinders、rounded channels 构成。

---

## 3. Scene design requirement

必须存在预注册的 matched-state block pairs：

\[
d_s(s_A,s_B)\le\tau_s,
\]

但：

\[
d_h(h_A,h_B)\ge\tau_h,
\]

并且未来 horizon 中：

\[
|e_A-e_B|\ge\tau_e.
\]

其中：

- \(s\)：runtime-observable state/geometry features；
- \(h\)：history/probe features；
- \(e\)：declared future exact–kinetic discrepancy。

这些阈值在 B1/B2 frozen case 中定义，B5 不能为了画面临时挑选。

---

## 4. Required methods

- full EDMD declared reference；
- full kinetic；
- state-only indicator；
- state + geometry + finite-density baseline；
- practical shadow-probe policy；
- oracle-history upper bound；
- proposed dynamic policy。

---

## 5. Primary observables

至少选择一个能进入主画面的物理量：

- tracer residence time；
- chamber occupancy；
- escape probability；
- species mixing front；
- wall collision/pressure pattern；
- local velocity anisotropy。

Collision graph 本身是解释层，不是最终物理 observable。

---

## 6. Required artifacts

```text
block-state
history-feature
collision-event window
discrepancy-sample
partition-mask
particle/kinetic bundle
geometry-bundle
metrics-report
split manifest
```

---

## 7. Shots

使用 CL-01 至 CL-06。

Scene render config：

```text
configs/render/scenes/correlation-labyrinth.yml
```

Benchmark case：

```text
benchmarks/b5_graphics_evidence/cases/candidate/B5-CORRELATION-LABYRINTH-v0.yml
```

---

## 8. Visual acceptance

- CL-02 清楚显示 matched-state，而不是隐藏 state 差异；
- CL-03 history graph 可读但不遮挡主画面；
- CL-04 未来 observable difference 在不看 mask 时可见；
- CL-05 practical policy 的改进不依赖 oracle-only features；
- CL-06 使用 held-out geometry/regime；
- state-only failure 不能由 DSMC resolution、packing fraction 或 unmodeled geometry 单独解释。

---

## 9. Failure reel

- random-row split 的虚假高分；
- oracle-history leakage；
- Enskog/finite-density explanation 关闭后 history gain 消失；
- history score 很高但 future observable 无差异；
- graph 太复杂导致 viewer 只看到线团。

---

## 10. Stop condition

若 history 只能改善离线 prediction score，却不能改变 partition policy、future observable 或 cost–quality frontier，则该场景保留为 scientific analysis，不包装成 SIG 核心 Hero Scene。
