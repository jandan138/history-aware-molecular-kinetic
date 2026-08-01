# Molecular Echoes：从邓煜的碰撞历史到分子时光机

**状态：** 当前正式主研究路线（2026-07-31）。

**第一目标：** SIGGRAPH / SIGGRAPH Asia。

**备选：** 只有当最强成果变成碰撞因果图与多分支历史的可视分析，而不是动画算法时，才重构为 IEEE VIS。

---

## 1. 为什么要转向

原路线希望证明：少量 collision-history scalar features 可以在强 state-only baseline 之外，预测 EDMD–DSMC 的未来误差，从而驱动动态 molecular LOD。

`PHASE1-HISTORY-STORY-v0` 内部二维 pilot 没有支持这个 operational claim。当前结果只说明“这套具体 predictor/feature/physics 配置没有实用增益”，并不证明碰撞历史永远无用；但它足以阻止我们继续盲目投入 conversion、partition controller、GPU LOD 和旧 Hero Demo。

因此项目不删除负结果，而是把问题改得更直接：

> 不再问“几个历史特征能否预测误差”，而是问“Boltzmann 一粒子闭合究竟遗忘了什么；这些隐藏的碰撞历史能否成为一种可反演、可分叉、可编辑的动画表示？”

正式决策见 [ADR 0009](../decisions/0009-pivot-to-molecular-echoes-sig.md)。

---

## 2. 邓煜的硬球成果在这里扮演什么角色

邓煜、Zaher Hani、Xiao Ma 从稀薄硬球牛顿动力学长期推导 Boltzmann 方程时，并没有假装碰撞从不制造相关性。他们传播 cumulant ansatz，保留完整 collision history，把相关结构组织成 collision-history molecules，再用 cutting argument 控制它们。

这给我们一个非常明确的科学主轴：

```text
完整硬球微观状态
    ↓ 压缩
一粒子分布 f1
    ↓ 被省略
二粒子/多粒子 cumulants 与碰撞历史
```

在通常的 Boltzmann–Grad、分子混沌前向情形中，这些相关性在目标极限下可以被控制，因此 `f1` 足以描述低阶统计。

但如果我们有意构造高度相关的反演态，当前的 `f1` 或有限分辨率 `f1_h` 看起来可以很普通，而粒子之间却藏着“未来应当按什么顺序重新相撞”的精细信息。

本项目不是反驳 Boltzmann，也不是实现证明算法，而是在有限系统里把这个信息边界变成：

1. 可测量的 counterfactual experiment；
2. 可计算的 history graph；
3. 可交互的 animation primitive。

---

## 3. 正式论文题目与一句话故事

推荐题目：

> **Molecular Echoes: Reversible and Counterfactual Hard-Sphere Animation with Collision-History Graphs**

中文：

> **分子回声：基于碰撞历史图的可逆与反事实硬球动画**

一句话：

> 我们把硬球碰撞历史组织成一张可查询的因果多重图，使用户能够回到过去、修改一次碰撞或一处几何、只重算受影响的未来，并在保持当前可分辨一粒子状态近似不变的情况下编辑隐藏关联，从同一个现在生成不同未来。

---

## 4. 两条必须同时成立的轨道

## Track S — Scientific Echo

负责回答：

- “same resolved present” 是否真的通过严格审计；
- exact reverse 和 chaotized reverse 是否稳健分离；
- incoming-pair correlation 是否与未来响应方向一致；
- `(Lambda, Gamma)` 碰撞分子预算是否捕捉到机制，而不只是允许了更多碰撞；
- 小型 Boltzmann–Grad 序列是否给出诚实、可解释的趋势。

## Track G — Graphics Time Machine

负责回答：

- 如何从 event log 构造 collision causal multigraph；
- 如何 checkpoint、随机访问和 deterministic replay；
- 修改过去后，如何找出并重算未来 causal cone；
- 如何让多条 branch 共享未修改历史，而不是复制全部轨迹；
- 如何保持当前可见 coarse state，只编辑隐藏 correlation；
- 如何把这些能力变成用户能理解的 SIG 动画与交互系统。

Track S 解释“为什么历史重要”；Track G 证明“历史怎样成为图形学工具”。缺一不可。

---

## 5. 第一幕：Same Resolved Present, Opposite Futures

在二维周期硬圆盘系统中准备一个明显的非平衡状态，例如：

\[
T_x/T_y = 4,
\]

并使用不参与动力学的 passive color 形成可见图案。

在枢轴时刻 `t_*` 构造：

| Branch | 构造 | 预期未来 |
|---|---|---|
| forward | 正常 EDMD 继续 | 继续热化 |
| exact reverse | 所有速度反号后 exact EDMD | 恢复过去的各向异性/颜色结构 |
| chaotized reverse | 在登记的 block+color 内置换速度 | 保持 `f1_h`，破坏粒子配对关联，不精确回声 |
| DSMC reverse | 从 reversed resolved state 运行 DSMC | 忘掉真实 pair history |
| ghost | 无粒子碰撞 | 机制下界 |

主审计不是“图片看起来一样”，而是：

\[
f_{1,h}^{\rm reverse}(t_*)
\approx
f_{1,h}^{\rm chaotized}(t_*),
\]

并且这个结论要在多组 spatial blocks 与 velocity bins 上报告。

论文只能说 same **resolved one-particle present**，不能说 exact microscopic state 相同。

未来读出包括：

- normalized anisotropy；
- passive-color mode/图案恢复；
- residence/escape 类低维量；
- incoming-pair closure-defect proxy。

---

## 6. 第二幕：Collision-Molecule Surgery

单纯速度反演不是贡献。核心实验是历史结构干预。

对每个候选碰撞维护：

- timestamp；
- particle pair；
- contact normal；
- incoming normal relative velocity；
- event predecessors；
- molecule root/size；
- recollision/reconnection complexity；
- repeated-event multiplicity。

定义历史预算：

\[
(\Lambda,\Gamma),
\]

其中：

- `Lambda` 限制 collision molecule 的粒子数；
- `Gamma` 限制重碰撞/重新连接复杂度。

典型路径：

\[
(4,0)\rightarrow(8,0)\rightarrow(16,1)\rightarrow\text{full EDMD}.
\]

超预算事件使用显式的 extended-dynamics 语义，例如 ghost-through。该支路不是 exact EDMD，必须独立标记。

为了证明机制不是“碰撞越多越接近 full EDMD”，必须加入：

1. collision-count/time-matched random suppression；
2. topology-shuffled partner control；
3. no-collision ghost；
4. full EDMD。

只有 structured molecule budget 在控制 collision count 后仍表现出差异，才允许 claim collision-history topology。

---

## 7. 第三幕：Collision Causal Graph

每次碰撞是事件节点：

\[
e_m=(t_m,i_m,j_m,n_m,v_i^-,v_j^-).
\]

若粒子先参加 `e_a`、后参加 `e_b`，建立：

\[
e_a\rightarrow e_b.
\]

得到时间有向因果多重图。它支持：

- shared ancestors；
- collision molecules；
- repeated pair events；
- descendant causal cones；
- branch provenance；
- history budget；
- 可视化一次微小改动如何传播。

它不是普通 unique-pair graph，也不是纯 debug view。

---

## 8. 第四幕：Causal Rewind and Counterfactual Branching

用户可以在过去：

- 改变一颗粒子的速度；
- 修改/抑制一次声明语义下的碰撞；
- 插入、移动或删除简单障碍物；
- 打开或关闭 aperture；
- 应用 correlation surgery。

系统从编辑前 checkpoint 恢复，只重算 expanding causal cone：

1. 直接受影响粒子进入 affected set；
2. affected particle 与 unaffected particle 相遇时，后者被吸收；
3. 其旧未来事件失效；
4. 递归推进到目标时间；
5. 无法证明不受影响时扩大 cone；
6. cone 全局化时退化到 full replay。

主要正确性基线：

\[
X_{\rm local\ branch}(T)
\approx
X_{\rm full\ resimulation}(T).
\]

不能为了“局部”而截断不确定依赖；近似版本必须单独标记。

---

## 9. 第五幕：保持当前画面，编辑隐藏未来

若完整 exact microstate 完全相同，确定性未来也相同。因此“只改日志不改状态”没有物理意义。

真正的 history surgery 是：

\[
X(t_*)\mapsto\widetilde X(t_*),
\]

同时满足登记约束：

\[
f_{1,h}[X]\approx f_{1,h}[\widetilde X],
\]

以及 mass、momentum、energy、color count、no-overlap 等审计。

但改变：

- 哪个速度属于哪个粒子；
- shared collision ancestors；
- incoming pair correlation；
- retained molecule structure。

这形成新的 authoring primitive：

> **保持当前可见状态，编辑它将走向的未来。**

---

## 10. 三个 SIG Hero Demo

## Hero 1 — Molecular Logo Echo

一个 passive-color 图案先被气体运动打散。在同一 resolved pivot 上并排播放 exact reverse、chaotized、DSMC 与不同 history budget。只有保留正确历史的支路重构图案。

主句：

> **Same resolved frame. Different collision histories. Opposite futures.**

## Hero 2 — One Collision, Two Worlds

用户点击并修改过去一次碰撞。差异从两个粒子开始，沿 collision causal graph 像闪电一样扩散。并排显示 original future、counterfactual future、affected fraction 与 full-resimulation validation。

## Hero 3 — Choose the Cause, Direct the Future

用户先在未来的 Molecular E 上选择一个笔画。系统沿原始 collision DAG 回溯，
推荐最能触及该笔画的过去碰撞，再展示少量 exact local previews。保存的 branch
才与 full global resimulation 比较。E4 的 Hero 使用上横杠，避免把 interaction
扩成新的几何求解器工程。

这些场景分别承担：科学直觉、算法核心、交互与性能，不能平均堆满所有 diagnostics。

---

## 11. 正式贡献候选

### C1 — Collision-history representation

可版本化 event multigraph、checkpoints、branch lineage 与 collision molecules。

### C2 — Exact causal branch recomputation

局部 expanding-cone 算法、full-resimulation correctness、conservative fallback。

### C3 — Coarse-state-preserving future authoring

在 `f1_h` 与主要守恒量受控时编辑隐藏 correlation。

### C4 — Counterfactual cumulant microscope

exact/chaotized/DSMC/budget/null-control 机制实验。

### C5 — Interactive molecular time machine

可回退、可分叉、可比较、可复现实验与 3D Hero Demo。

---

## 12. 不能 claim 什么

- “我们首次发现硬球可以时间反演”；
- “记录历史以后牛顿方程才可逆”；
- “普通 event log/rollback 是新算法”；
- “我们实现了邓煜的 cutting algorithm”；
- “邓煜定理保证了 finite history surgery”；
- “same `f1_h` 等于 same exact state”；
- “反演态是 Boltzmann 方程的反例”；
- “causal cone 永远局部”；
- “Phase-I predictor 成功”。

---

## 13. 当前 smoke evidence 的地位

已有 `N=64` 反射盒 smoke test 显示 exact reversed、chaotized、DSMC 和 ghost 支路可能产生清晰差异。这只用于决定值得进行正式 feasibility stage：

- 边界尚非正式周期设置；
- 样本小；
- 没有 multi-resolution `f1_h` audit；
- 没有 molecule budget/null controls；
- 没有 branch algorithm。

它不能进入摘要，也不能当 frozen evidence。

---

## 14. 第一阶段与判死刑条件

先用 2–3 周完成：

1. preregistration commit/tag；
2. `N=128,256,512` 周期 EDMD 严格反演；
3. multi-resolution `f1_h` audit；
4. exact/chaotized/DSMC/ghost；
5. `(Lambda,Gamma)` 与两类 null control；
6. incoming-pair proxy；
7. one-event counterfactual branch 与 full replay 对照；
8. 一个中性 60–90 秒 internal demo。

立即停止/收窄，如果：

- numerical reverse 本身不可靠；
- branch separation 在细化 `f1_h` 后消失；
- molecule budget 与 count-matched random suppression 无差别；
- one-event local branch 无法匹配 full replay；
- 所有 causal cone 都立刻全局化；
- 唯一好看的结果只是把录像倒放。

详细路线见：

- [Active E0–E6 suite](../benchmarks/echo-branching-suite.md)
- [First stage](../roadmap/molecular-echo-first-stage.md)
- [Implementation backlog](../roadmap/molecular-echoes-backlog.md)
- [Graph and branching architecture](../architecture/collision-history-graph-and-branching.md)
- [Venue strategy](../vision/venue-strategy.md)
