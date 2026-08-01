# Storyboard and Shot Grammar — Molecular Echoes

> 本文件定义 active SIG 视频的叙事结构与 shot IDs。最终相机、branch IDs、时间和 renderer config 必须由 evidence manifest 冻结。

---

## 1. 总体视频结构

## Teaser：30–45 秒

核心记忆点：

> **Same resolved frame. Different collision histories. Opposite futures.**

建议结构：

```text
0–5 s    彩色分子图案在透明容器中开始扩散
5–10 s   到达 pivot；exact/chaotized 当前画面与 f1_h 审计匹配
10–17 s  exact reverse 重构图案，chaotized/DSMC 继续混合
17–23 s  history-budget slider + molecule/null-control 对比
23–31 s  点击一次碰撞，分叉为 Two Worlds，causal cone 扩散
31–38 s  选择未来的一笔，回溯碰撞原因，导演新的 branch
38–45 s  runtime/storage + title: Molecular Echoes
```

所有 fork 之后的画面都必须由 branch dynamics 向前生成。倒放视频只能作为明确标记的 baseline。

## Main video：3–5 分钟

1. Deng–Hani–Ma 启发：一粒子闭合遗忘什么；
2. Phase-I predictor 负结果与诚实转向；
3. exact reverse / chaotized / DSMC；
4. multi-resolution `f1_h` audit；
5. collision-molecule budget 与 null controls；
6. collision causal graph；
7. checkpoint / replay / persistent branch；
8. one-event and outcome-directed counterfactual edits；
9. correlation surgery authoring；
10. performance、limitations、failure cases。

---

## 2. 通用 shot grammar

Scientific shot：

```text
Pivot contract → controlled intervention → future response → mechanism control
```

Graphics shot：

```text
Past edit → branch fork → causal cone → recomputed future → full-reference audit → reuse benefit
```

每个镜头只承担一个主要问题。不要同时解释 `f1_h`、T-dynamics、branch storage 和 renderer。

---

## 3. Molecular Logo Echo

### ME-01 — Prepared pattern

- 透明周期盒/容器；
- passive colors 形成简单图案；
- 短暂显示 initial anisotropy；
- 不显示 graph。

**问题：**过去是什么？

### ME-02 — Mixing and pivot

- 图案逐渐消失；
- 到 `t_*` freeze；
- exact reverse 与 chaotized reverse 并排；
- 当前视觉一致。

**问题：**两个 branch 的现在看起来是否相同？

### ME-03 — Resolved-state audit

- 固定 pivot；
- 显示 spatial/velocity 多分辨率匹配表；
- density、momentum、temperature、color counts；
- 标注“same resolved present, not same microstate”。

**问题：**“same present”具体保持了什么？

### ME-04 — Opposite futures

- branch 向前播放；
- exact reverse 重构图案；
- chaotized/DSMC 继续混合；
- 同步 anisotropy/color curve。

**问题：**隐藏 history 是否改变未来？

### ME-05 — History budget

- full、small/medium budget、random count-matched、ghost；
- 同一时间与 camera；
- graph inset 显示 molecule 结构；
- collision count 单独显示。

**问题：**结构化 history 是否不只是更多碰撞？

### ME-06 — Limitation

- 展示一个 audit 过粗或 numerical reverse 失败的案例；
- 说明 claim boundary。

---

## 4. One Collision, Two Worlds

### TW-01 — Select event

- 播放原 branch；
- 用户暂停并点击一次 collision；
- 显示 event time、pair 和 immediate predecessors；
- 不展开全部 graph。

### TW-02 — Apply edit and fork

- 修改一颗入射速度或声明的 event 语义；
- branch tree 增加 child；
- parent 保持不变；
- checkpoint 被选中。

### TW-03 — Causal cone begins

- 差异从两颗粒子开始；
- affected set 用克制的 outline/trail 表示；
- 右侧小图显示 descendant graph；
- affected fraction 曲线开始增长。

### TW-04 — Two worlds diverge

- original 与 counterfactual 并排；
- passive-color transport / escape / residence 出现宏观差异；
- 不显示 full-screen mask。

### TW-05 — Correctness audit

三列：

```text
local causal branch | full resimulation | absolute difference
```

显示 state/event tolerance、fallback 状态。

### TW-06 — Cost and locality

- causal cone fraction；
- runtime；
- shared event/checkpoint storage；
- edit age/density 作为简洁 inset。

### TW-07 — Global-cone failure

- 选择一个老/强 edit；
- cone 迅速全局化；
- 系统明确 fallback 到 full replay。

---

## 5. Choose the Cause, Direct the Future

### CS-01 — Select the future feature

- recovered `E` 作为终局画面；
- 用户框选上横杠；
- 高亮该 feature 的 persistent particle IDs；
- 明确显示“我希望这里改变”。

### CS-02 — Trace to past causes

- timeline 回到过去，但不是倒放视频；
- 三个候选碰撞按 baseline descendant coverage/purity 高亮；
- 只显示必要的小图，不展开整张 graph。

### CS-03 — Browse exact previews

- 用户选择推荐碰撞并拨动 `-2°,-1°,+1°,+2°`；
- 左右使用相同相机显示原未来和预览未来；
- 标明 preview 是 exact local branch，而不是 renderer effect。

### CS-04 — Save and verify

```text
selected target → ranked cause → saved branch → full reference
```

- 显示 target 与 collateral 的改变比例；
- 显示 baseline-event reuse；
- 仅保存分支显示 local/full exactness inset。

几何编辑和 correlation surgery 只有在后续单独通过 gate 后，才会成为新的镜头。

---

## 6. 主图与镜头绑定

| Figure concept | Shot source |
|---|---|
| Teaser / first page | ME-02 + ME-04 |
| Deng-inspired information boundary | ME-03/04/05 |
| Collision causal representation | TW-01/02/03 |
| Counterfactual correctness | TW-05 |
| Outcome-to-cause authoring | CS-01/02/03/04 |
| Broader locality/performance | deferred after E4 |
| Past geometry edit | deferred after E4 |
| Correlation surgery | deferred after E4 or ME-03/04 |
| Limitations | ME-06 + TW-07 |

Composite figures must list run, branch, edit, frame time, camera hash, renderer hash, and metric artifact per panel.

---

## 7. Voice-over rules

不要说：

> “我们保存历史，所以牛顿方程可以倒放。”

要说：

> “Exact hard-sphere dynamics is reversible in principle. Our contribution is to make collision correlation a queryable branch representation, to audit what a resolved one-particle present forgets, and to support physically recomputed edits of the past.”

不要说：

> “这两个状态完全一样。”

要说：

> “They match the preregistered resolved one-particle state over the reported resolution sweep, while retaining different hidden multi-particle correlations.”

不要说：

> “我们只重算局部区域。”

要说：

> “We expand the causal cone conservatively and fall back to full replay when locality is lost.”
