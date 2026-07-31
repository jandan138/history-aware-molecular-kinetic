# 硬球项目研究总览（中文）

> 当前正式主线：**Molecular Echoes——基于碰撞历史图的可逆与反事实硬球动画**。

## 1. 项目经历了什么变化

最初路线是：

```text
碰撞历史特征
→ 预测 EDMD–DSMC 未来误差
→ 选择 exact region
→ exact/kinetic 动态 LOD
```

学生完成了内部二维 Phase-I pilot。结果没有支持“当前这组 scalar history features 能在强 state-only baseline 之外带来实用预测提升”这一主张。

这不是证明“碰撞历史永远没用”，但足以说明：现在继续开发 promotion/demotion、partition controller、GPU LOD 和旧 Hero Demo 不合理。

因此项目诚实保留负结果，并把问题改得更直接：

> **Boltzmann 一粒子闭合遗忘的碰撞关联，能否成为一种可看见、可反演、可分叉、可编辑的动画表示？**

正式决策见 [ADR 0009](../decisions/0009-pivot-to-molecular-echoes-sig.md)。

---

## 2. 邓煜的硬球数学成果没有被丢掉

精确硬球系统保存：

\[
X(t)=\{x_i(t),v_i(t),\mathrm{id}_i\}_{i=1}^{N}.
\]

Boltzmann/DSMC 主要保存一粒子分布：

\[
f_1(x,v,t).
\]

从完整微观状态压缩到 `f1` 时，被丢掉的是粒子之间的二阶、多阶相关性以及它们的共同碰撞历史。

邓煜、Zaher Hani 和 Xiao Ma 在从硬球长期推导 Boltzmann 方程时，传播 cumulants，保留完整 collision history，把相关结构组织成 collision-history molecules，再用 cutting argument 控制它们。

本项目从中提取的不是一个可以复制的求解器，而是一个信息边界：

```text
完整 collision history / cumulants
             ↓ 被粗粒化
        one-particle state f1
```

我们的有限系统实验要展示：

- 哪些普通前向状态可以被 `f1` 压缩；
- 哪些人为构造的高度相关反演态不能只靠当前 `f1_h` 区分；
- 需要多少 collision-molecule history 才能恢复某些未来；
- 怎样把这种隐藏信息变成图形动画工具。

必须守住 claim 边界：

- 不说实现了证明中的 cutting algorithm；
- 不说定理保证有限 branch/surgery；
- 不说反演态反驳 Boltzmann；
- 不说普通速度反号是新贡献。

---

## 3. 新主线的科学核心

在周期硬圆盘/硬球系统中准备一个非平衡状态，到 pivot `t_*` 后构造：

| Branch | 含义 |
|---|---|
| forward | 正常 exact EDMD 继续 |
| exact reverse | 所有速度反号后 exact EDMD，保留完整微观关联 |
| chaotized reverse | 保持登记分辨率 `f1_h`，置换粒子—速度配对，破坏隐藏关联 |
| DSMC reverse | 从 resolved state 运行随机碰撞，主动忘记真实 pair history |
| history-budget | 只允许一定规模/复杂度的 collision molecules |
| ghost | 无粒子碰撞下界 |

要严格审计：

\[
f_{1,h}^{\rm exact\ reverse}(t_*)
\approx
f_{1,h}^{\rm chaotized}(t_*),
\]

同时观察：

\[
A_{\rm exact}(t_*+\tau)
\neq
A_{\rm chaotized}(t_*+\tau).
\]

这里 `A` 可以是：

- 各向异性恢复；
- passive-color 图案恢复；
- 颜色输运；
- residence/escape；
- incoming-pair closure defect 对应的低维读出。

只能说 same **resolved one-particle present**，不能说 exact microstate 相同。

---

## 4. 为什么简单回声还不够 SIG

硬球动力学在理想条件下可逆；速度反号、Loschmidt echo、event log 和 generic rollback 都有大量 prior art。

因此论文不能只是：

```text
粒子散开
→ 速度反号
→ 图案回来
```

SIG 贡献必须来自一套新的 animation system：

1. collision-history causal multigraph；
2. checkpoints 与 deterministic replay；
3. persistent counterfactual branches；
4. 修改过去后的 expanding causal cone；
5. local branch 与 full resimulation 正确性对照；
6. 共享未修改历史的 runtime/storage 优势；
7. 保持当前 resolved state、只编辑隐藏 correlation 的 authoring primitive；
8. 三套 3D Hero Demo。

---

## 5. Collision Causal Graph 是什么

每次碰撞是事件节点：

\[
e_m=(t_m,i_m,j_m,n_m,v_i^-,v_j^-).
\]

如果粒子 `i` 先参加事件 `e_a`，后来参加 `e_b`，建立：

\[
e_a\rightarrow e_b.
\]

于是得到时间有向因果多重图。它保留：

- repeated pair events；
- shared ancestors；
- collision molecules；
- branch lineage；
- future descendants；
- causal cone；
- history budget。

它不是一张装饰性 graph，而是 replay、branch、edit 和 provenance 的核心数据结构。

---

## 6. “修改过去，只重算未来因果锥”是什么意思

用户回到过去：

- 改一颗粒子的速度；
- 修改一次碰撞；
- 移动挡板；
- 打开一个 aperture；
- 插入/删除简单障碍物。

系统从编辑前 checkpoint 恢复，先把直接受影响的粒子加入 affected set。每当 affected trajectory 与旧的 unaffected trajectory 相遇，后者也被吸收，旧未来事件失效，继续递归重算。

如果依赖范围不断扩大：

- 能证明局部时，复用未受影响历史；
- 不确定时，扩大 cone；
- cone 全局化时，退化到 full replay。

必须与完整重算比较：

\[
X_{\rm local\ branch}(T)
\approx
X_{\rm full\ resimulation}(T).
\]

不能为了“看起来局部”而偷偷截断物理依赖。

---

## 7. 保持当前画面、编辑未来

若完整微观状态 `X(t_*)` 完全一样，确定性未来也一样。只修改日志不会改变未来。

真正的 correlation surgery 是改变当前微观粒子—速度配对和隐藏 ancestry，同时保持登记的 coarse state：

\[
f_{1,h}[X]
\approx
f_{1,h}[\widetilde X],
\]

以及 mass、momentum、energy、color count 和 no-overlap 等约束。

于是用户可以：

> **让当前可见画面基本不变，但选择它未来走向哪一条 branch。**

这是新路线最有 SIG 味道的 authoring primitive。

---

## 8. History Budget 必须有 null controls

定义：

\[
(\Lambda,\Gamma),
\]

- `Lambda`：collision molecule 最大粒子数；
- `Gamma`：允许的重碰撞/重新连接复杂度。

但“预算越大越接近 full EDMD”可能只是因为允许的碰撞更多。

所以必须比较：

- full EDMD；
- structured molecule budget；
- collision-count/time-matched random suppression；
- topology-shuffled control；
- ghost dynamics。

只有 structured history 超过这些控制，才允许说 molecule topology 携带机制信息。

**E2-v0 已于 2026-08-01 完成，结论是 `stop_e2`。** budget ladder 本身呈现很强的
递增恢复（平均 Spearman `0.930574`），但 `(4,0)` 相比 count/time-matched random
和 topology-shuffled 的注册差值都略为负，置信区间也都跨零。因此当前证据只能说
“允许更多碰撞会保留更多 reverse echo”，不能说 molecule wiring 超越 collision
dose 解释了恢复。这个机制主张已经关闭，不再追加 seed、budget 或 `N=512` 救结果。

---

## 9. 三个最终 Hero Demo

### Molecular Logo Echo

彩色图案先散开。pivot 时 exact、chaotized、DSMC 在 resolved audit 上匹配；继续向前模拟后，只有保留正确 history 的 branch 重构图案。

### One Collision, Two Worlds

用户点击并编辑过去一次碰撞。差异从两个粒子开始沿 causal graph 扩散；original、local counterfactual 和 full-resimulation reference 并排比较。

### Edit the Past

透明 molecular maze 中，用户回到过去移动挡板或打开出口。系统共享 unaffected history，只重算 future cone，并显示 runtime/storage 与最终正确性。

---

## 10. Active E0–E6 ladder

```text
E0 exact reversal and replay
E1 same resolved present / opposite futures
E2 molecule budget and null controls [已完成，机制 no-go]
E3 collision graph and deterministic replay
E4 counterfactual branching
E5 correlation surgery
E6 SIG visual and interaction evidence
```

详见 [Active Echo and Branching Benchmark Suite](../benchmarks/echo-branching-suite.md)。

---

## 11. 第一目标 SIG，什么情况下才转 IEEE VIS

### 保持 SIG 路线

当最强贡献是：

- simulation/animation algorithm；
- causal rewind；
- physically recomputed branching；
- shared history；
- authoring different futures；
- runtime/storage/interactivity；
- 3D results。

### 转 IEEE VIS

只有当：

- causal cone 常常全局化，simulation speed claim 很弱；
- 但 event graph、branch tree、molecule budget 和 uncertainty 数据非常丰富；
- 能定义科学家的真实分析任务；
- 能做 linked views 和 expert evaluation。

VIS 稿必须重构成 visual analytics，不是 SIG 被拒后改标题。

详见 [Venue Strategy](../vision/venue-strategy.md)。

---

## 12. 当前最重要的下一步

E1 已正向通过，E2 已按冻结规则否定 molecule-topology 机制。现在不再扩展 E2，
而是只推进更窄的 graphics-system 验证：

1. E3 collision graph、checkpoint 与 deterministic replay；
2. E4 one-event branch 对 full resimulation 的正确性；
3. causal cone 的 locality、runtime 与 storage 是否真有系统价值；
4. 若这些也不成立，就停止 SIG 路线，而不是用更漂亮的 echo 视频替代算法贡献。

这一步通过后才投入 3D、交互 UI 和 SIG Hero polish。

入口：

- [Molecular Echoes route](collision-history-echo-route.md)
- [First stage](../roadmap/molecular-echo-first-stage.md)
- [Backlog](../roadmap/molecular-echoes-backlog.md)
- [Graph/branch architecture](../architecture/collision-history-graph-and-branching.md)
- [Hero scenes](../demos/hero-scenes.md)
