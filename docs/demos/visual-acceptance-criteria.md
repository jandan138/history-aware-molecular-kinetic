# Visual Acceptance Criteria

> 本文件把“看起来不错”改写成可审计的 B5 验收条件。阈值在 candidate 阶段可调整；进入 frozen case 后不得为了某个 method 临时修改。

---

## 1. 四类验收

### A. Evidence integrity

- 每个 frame 对应一个 frozen/candidate run ID；
- 输入 artifact 都有 content hash；
- render config、camera、comparison lock、display policy 均有 hash；
- manifest 声明 renderer name/version；
- 画面上的数值来自 metrics artifact，而不是手工输入；
- method label、seed、time、units 可追溯。

### B. Fairness

- comparison lock 全部一致；
- exact particle display radius 一致；
- statistical display sample policy 一致；
- volume transfer function 一致；
- frame time 一致；
- method-specific override 数量为 0，或 primary comparison 被标记为非正式。

### C. Temporal quality

- conversion frame 没有异常亮度/密度跳变；
- statistical display particles 不产生无规则 frame-wise boiling；
- exact identity track 连续；
- partition mask 的视觉 flicker 不超过 B4 policy chatter；
- volume integral 的显示变化与 artifact 中的物理变化一致。

### D. Scientific legibility

- 不看 partition mask 时，至少两个 declared physical observables 的差异可见；
- 打开 diagnostics 后，观众能解释差异来自哪里；
- neutral scientific render 与 hero render 指向同一结论；
- matched display density 后差异仍存在；
- difference view 与 quantitative metric 符号一致。

---

## 2. 必须记录的视觉指标

### 2.1 Comparison-lock pass

```text
comparison_lock_match ∈ {0,1}
```

Primary comparison 必须为 1。

### 2.2 Artifact-hash coverage

\[
\text{coverage}
=
\frac{\text{有 content hash 的输入 artifact 数}}
{\text{全部输入 artifact 数}}.
\]

冻结结果要求 1.0。

### 2.3 Display-density mismatch

对同一 comparison group：

\[
\epsilon_{display}
=
\frac{|N^{(a)}_{display}-N^{(b)}_{display}|}
{\max(N^{(a)}_{display},N^{(b)}_{display},1)}.
\]

Primary comparison 的统计显示粒子预算和 exact display scale 必须锁定；若实际 sample count 因权重/遮挡策略变化，需报告有效显示密度。

### 2.4 Frame discontinuity score

在 representation conversion 前后计算共享视图中的 normalized image/field difference：

\[
D_t = D(I_t,I_{t-1}).
\]

不直接用任意绝对阈值，而与同一序列非 conversion 时刻的自然分布比较：

\[
R_{pop}
=
\frac{D_{conversion}}
{\operatorname{median}(D_{natural})+\epsilon}.
\]

Candidate 内部目标：conversion 不成为序列中不可解释的极端 outlier。具体阈值由 V2 baseline 分布预注册。

### 2.5 Volume continuity

对 density/species volume：

\[
\epsilon_{volume}
=
\frac{|\int \rho_{rendered}^{+}dx-\int \rho_{rendered}^{-}dx|}
{\int \rho_{rendered}^{-}dx+\epsilon}.
\]

该指标检查显示混合，不替代物理 conservation report。

### 2.6 Camera–physics coupling audit

改变 camera path、FOV 或 display particle budget后：

```text
physics partition artifact hash unchanged = 1
```

Primary zoom shot 必须通过。

### 2.7 Physical-effect visibility

每个 claim 预注册一个可见 observable，例如：

- plume half-angle；
- density ridge position；
- species interface thickness；
- residence-time tracer occupancy；
- wall pressure pattern；
- escape probability；
- velocity-distribution anisotropy inset。

B5 总 gate 要求至少两个彼此独立的 observable 被恢复，且不是只在 mask 上可见。

---

## 3. 三个场景的最低要求

### Zoomable Mixing Chamber

- M/P/E conversion report 通过；
- species volume continuity 通过；
- camera–physics audit 通过；
- exact identity track 连续；
- naive frame-wise resampling baseline 明显更差，证明 temporal policy 有作用。

### Correlation Labyrinth

- matched-state pair 的 state distance 在预注册阈值内；
- history distance 与 future discrepancy 差异显著；
- proposed practical policy 在 held-out geometry 中改善 operational metric；
- 主画面至少显示一个可见的 residence/escape/mixing effect，而非只有 score heatmap。

### Expansion into Vacuum

- plume observable 对 reference 的误差下降；
- exact front 随物理状态移动；
- state-only、proposed、reference 在同一 camera/transfer function 下比较；
- cost–quality point 与画面使用同一 run；
- macro-to-micro shot 不改变 physics partition。

---

## 4. 人工可读性评审

这不是用主观打分替代物理指标，而是检查叙事失败。

内部 blind review 至少回答：

1. 不看 caption，能指出主画面的物理差异吗？
2. 看完 diagnostics，能说出为什么发生吗？
3. 能区分 species 与 representation 吗？
4. 能指出哪一层是 non-physical display particles 吗？
5. 是否误以为相机触发了 exact refinement？
6. 哪个 panel 是 declared reference？

若多数评审无法回答，先改视觉语法，不改物理数据。

---

## 5. Primary、secondary 与 hero evidence

### Primary evidence

- neutral scientific mode；
- comparison locked；
- 直接支撑论文 claim；
- 可复现；
- 不依赖复杂后处理。

### Secondary evidence

- diagnostics、difference view、plots；
- 解释 primary evidence；
- 可以使用更多 overlay。

### Hero evidence

- 更强构图和灯光；
- 用于传播和讲解；
- 必须链接到 primary result；
- 不能单独承担 scientific claim。

---

## 6. B5 No-Go

出现任一情况则停止 hero polish：

- 只看 mask 才知道方法不同；
- display density 匹配后差异消失；
- conversion popping 主要靠 method-specific temporal filter 隐藏；
- camera 改变 physics partition；
- hero render 与 neutral render 给出相反印象；
- 最漂亮 seed 是人工挑选且没有预注册选择规则；
- cost plot 与视频不是同一 run family；
- 需要复杂新物理才能让场景好看。
