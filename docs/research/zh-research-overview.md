# 硬球项目研究总览（中文）

> 项目暂名：**History-Aware Molecular–Kinetic**。目标不是“把 EDMD 和 DSMC 接起来”，而是检验一个更窄、更可能失败、但一旦成立就有论文价值的问题：**碰撞历史中携带的相关性，能否在强 state-only baseline 之外，额外预测粗粒化动理学模型的局部误差，并据此只在必要区域保留精确硬球身份？**

## 1. 我们究竟想省掉什么

精确硬球系统保存每个球的：

\[
(x_i,v_i,r_i,m_i,\mathrm{id}_i)
\]

以及谁在什么时间撞过谁。这样能够表示：

- 几何上真实发生的接触；
- 同一对粒子的重碰撞；
- A 撞 B、B 撞 C、C 又影响 A 的碰撞链；
- 狭窄腔体、移动壁面和回流几何制造的共同历史；
- 有限尺寸带来的排斥体积与 pair structure。

代价是粒子和事件都必须显式维护。

Boltzmann/DSMC 则主要近似单粒子分布：

\[
f(x,v,t).
\]

一个 DSMC superparticle 代表许多真实分子。碰撞对象通常从空间 cell 中随机抽样，不要求两个 simulation particles 在几何上真的接触。这样能够把巨大气体系统压缩到可计算规模，但会主动丢掉部分精确身份和多粒子相关性。

我们希望构造：

\[
\boxed{
\text{Exact hard spheres}
\rightleftarrows
\text{stochastic kinetic representation}
}
\]

并让 exact region 只出现在“丢掉这些信息会造成可观测误差”的地方。

## 2. 与邓煜硬球成果的真实关系

邓煜、Zaher Hani 和 Xiao Ma 的工作从低密度牛顿硬球动力学严格推出 Boltzmann 方程，并把经典的短时间结果扩展到相应 Boltzmann 解存在的任意预先给定有限时间区间。证明中使用了 cumulant、完整碰撞历史、collision-history molecules 与 cutting argument。

对本项目最有启发性的不是某一个可直接移植的公式，而是下面的信息边界：

```text
完整粒子身份 + 多粒子碰撞历史
                 ↓ 粗粒化
       单粒子 kinetic distribution
```

我们研究的是：有限规模、有限分辨率、复杂几何中的数值系统，何时会因为这次信息压缩而出现可测误差。

必须同时守住四条 claim 边界：

1. 证明中的 cumulant 不是现成的在线 feature；
2. cutting algorithm 不是 GPU 分区算法；
3. 理论越接近 Boltzmann–Grad 稀薄极限，相关性本来就越应该小，exact patch 反而可能没有必要；
4. 较高密度下 EDMD 与 DSMC 的差异可能主要来自 Enskog finite-density correction，而不是“碰撞历史”本身。

所以论文只能写成 **inspired by recent hard-sphere kinetic-limit theory**，不能写成“定理保证了我们的 LOD”。

## 3. 为什么普通的 EDMD–DSMC 拼接不够新

已有工作已经覆盖了很多相邻问题：

- DynamO：成熟的 event-driven molecular dynamics，可作为精确硬球 oracle；
- SPARTA：成熟的大规模并行 DSMC，可作为 Boltzmann/DSMC oracle；
- uniGasFoam：能够在 DSMC 与 SP/USP 粒子模型之间自动切换，是必须对比的 state-based adaptive baseline；
- Donev、Garcia、Alder 早在 2007 年就做过 EDMD–DSMC hybrid，因此不能宣称“首次耦合 EDMD 与 DSMC”；
- CFD/kinetic 社区已有 Knudsen-based、moment-based、wave-particle 与 continuum breakdown 方法；
- 图形学已有 continuous-scale kinetic fluid 与 HOME-LBM 等 kinetic graphics 工作。

因此下面这些 claim 都不成立：

- “我们第一次用 DSMC 做图形仿真”；
- “我们第一次做 adaptive rarefied-gas simulation”；
- “我们第一次耦合 EDMD 与 DSMC”；
- “GPU 上模拟大量硬球就是贡献”。

真正可能的新意必须集中在：

\[
\boxed{
\text{collision-history information 的增量预测价值}
+
\text{可运行时观测的 practical policy}
+
\text{守恒且稳定的 representation conversion}
}
\]

## 4. 最核心、也是最容易被自己骗到的实验

令 \(e_B\) 表示 block \(B\) 中，full EDMD 与目标 kinetic backend 在一个固定未来时间窗内的 discrepancy。

state-only feature 可包含：

\[
s_B=(\rho,\phi,T,u,\mathrm{Kn}_{GLL},R_M,\Pi,q,
\text{geometry},\text{resolution}).
\]

history feature 可包含：

\[
h_B=(r_{\mathrm{repeat}},\beta_1(G),
\text{component re-merging},
\text{lineage depth},
\widehat C_2,\ldots).
\]

项目首先检验：

\[
\mathbb E[\ell(e_B,\hat e(s_B,h_B))]
<
\mathbb E[\ell(e_B,\hat e(s_B))]
\]

而且必须在 **held-out geometry、held-out transient 和 held-out physical regime** 上成立，不能把同一条 trajectory 的相邻 block 随机拆到训练集和测试集。

更严格地说，需要比较下面的 baseline ladder：

1. density / packing fraction；
2. Knudsen breakdown criterion；
3. 完整 state moments：stress、heat flux、Maxwellian residual；
4. state + geometry；
5. state + geometry + DSMC resolution metadata；
6. state + geometry + Enskog/finite-density attribution；
7. 上述全部 + oracle exact history；
8. 上述全部 + 实际可运行的 shadow-probe/history feature。

第 6 到第 7 的提升回答“history 在科学上有没有额外信息”；第 7 到第 8 的差距回答“这些信息能不能变成真正在线算法”。

## 5. Feature observability firewall

一个 kinetic block 中没有真实分子的精确身份。DSMC superparticle 被随机重复配对，并不等于真实分子发生了重碰撞。

所以所有 feature 必须带上可见性标签：

### `runtime_observable`

当前实际 representation 中无需额外 oracle 就能得到，例如 density、stress、heat flux、wall distance、coarse temporal derivative。

### `shadow_probe`

需要从 coarse state 采样一个短时、小区域 exact micro-simulation 才能估计。必须记录 probe horizon、seed、初始化方式、成本和不确定性。

### `oracle_only`

只有全域 full EDMD ground truth 才知道，例如 kinetic region 原本会发生的真实碰撞图。它只能用于建立理论上限和训练标签，严禁喂给在线 policy。

如果在线结果使用了 oracle-only history 来决定哪里需要 exact EDMD，那么整个 adaptive claim 都是数据泄漏。

## 6. 为什么 coarse backend 必须可替换

第一版最自然的 coarse model 是 Boltzmann DSMC，但架构不能写死为：

```text
EDMD ↔ DSMC
```

因为 EDMD–DSMC mismatch 可能来自：

- finite-density pair correlation；
- cell size 或 time step 不合适；
- simulation particle weight 太大；
- wall treatment；
- sampling noise；
- initial ensemble 未匹配；
- 真实 collision-history memory。

在 packing fraction 增大时，更合理的 coarse baseline 可能是 Enskog-like particle method。因此核心接口应是：

```text
Exact backend
├── internal EDMD
└── external DynamO oracle

Kinetic backend
├── Boltzmann DSMC
├── Enskog / finite-density particle model
└── future reduced or learned conservative model
```

只有在控制 Enskog correction 后 history 仍有增量价值，论文主线才站得住。

## 7. Benchmark ladder

### R0 — External oracles

固定 revision，复现 DynamO、SPARTA 和 uniGasFoam 的官方或已发表 case，建立 raw output 到 canonical artifact 的转换与 normalization audit。

### B0 — Single-regime primitives

分别验证内部 EDMD、DSMC 和未来 Enskog backend：两体碰撞解析解、周期/反射边界、自由输运、均匀 relaxation、质量/动量/能量与采样统计。

### B1 — Discrepancy atlas

系统扫描：density、packing fraction、mean free path、confinement、moving wall、initial anisotropy、cell/time resolution 与 geometry family，建立 exact-versus-kinetic discrepancy map。

### B2 — History indicator

用 grouped held-out evaluation 检验 history feature 的增量预测价值，并严格区分 oracle upper bound 与 practical shadow-probe policy。

### B3 — Representation conversion

先做静态 exact→kinetic demotion，再做 kinetic→exact promotion。转换不仅检查：

\[
M,\quad P,\quad E,
\]

还检查 velocity distribution、stress、heat flux、pair structure 和转换后的 downstream transient。

### B4 — Dynamic LOD

加入 hysteresis、cooldown、interface buffer、probe scheduling、exact-region budget 与 failure indicator，画出完整 cost–quality Pareto frontier。

### B5 — Graphics evidence

所有方法使用同一个 renderer、同一显示密度和同一相机。只有 B2–B4 通过后才投入最终视频。

## 8. Demo 为什么比海浪方向更容易控制

早期统一 renderer 只需要四类图层：

1. instanced spheres；
2. density / temperature / species volume；
3. exact–kinetic representation mask；
4. collision graph、velocity histogram、conservation timeline 等诊断图层。

第一篇不做：

- 火焰和化学反应；
- 电影级烟雾艺术控制；
- 复杂火箭或飞船资产；
- granular friction、堆积和 force chains；
- 高质量路径追踪；
- 一开始就做三维动态复杂网格。

### Hero 1：Zoomable Mixing Chamber

证明 representation conversion、宏观/微观连续性和 physics LOD 与 display LOD 分离。这个场景本身不用于证明 history 有价值。

### Hero 2：Correlation Labyrinth

设计 state moments 相近但 collision/re-encounter topology 不同的区域。它是最重要的科学场景，用于展示 state-only baseline 与 proposed history score 的差异。

### Hero 3：Expansion into Vacuum

展示 ballistic、collisional 和 transitional 区域同时存在，refinement region 随时间移动，并与 uniGasFoam/state-only policy 对比。

## 9. 八周 feasibility spike

### 第 1 周：DynamO oracle

跑通官方硬球 case，导出 temperature、pressure、collision count、radial distribution 与基础视频。

### 第 2 周：SPARTA / uniGasFoam oracle

跑通 free/collisional DSMC case，记录 particle/grid statistics；固定 uniGasFoam 环境与至少一个 hybrid case。

### 第 3 周：最小二维 EDMD

只支持等半径弹性硬圆盘、周期/反射边界、事件队列、collision log 和 checkpoint。

### 第 4 周：最小二维 DSMC

与 EDMD 使用匹配的一粒子初始分布、物理参数、统计时刻和 observable definitions。

### 第 5 周：paired discrepancy dataset

以 geometry/regime/trajectory 为组生成 paired samples，并估计 ensemble 与 sampling uncertainty。

### 第 6 周：state-only vs history-aware

先用可解释模型比较 held-out performance，不急着上神经网络。

### 第 7 周：oracle partition 与 shadow probe

先测 full-history 上限，再测短时 exact probe 能保留多少价值，并把 probe cost 加入预算。

### 第 8 周：静态 demotion

实现 exact→kinetic conversion，严格核对守恒量、secondary statistics 和下游 relaxation transient。

## 10. Go / No-Go

只有满足下面条件才进入完整动态 LOD：

- 控制 state、geometry、resolution 与 finite-density baseline 后，history 仍有稳定的 held-out 增益；
- practical probe/observable policy 保留了足够多的 oracle-history 增益；
- exact region 不是长期 0% 或 100%；
- conversion error 小于被 refinement 修复的 model error；
- 在固定误差下形成显著性能收益；
- 至少两个场景能肉眼解释“不 refine 错在哪里，refine 恢复了什么”。

出现下面情况就应转向：

- Enskog correction 吸收了几乎全部 discrepancy：转 EDMD–Enskog；
- 只有全域 EDMD 才知道哪里需要 EDMD：转 shadow-probe/error-estimation 或 collision-history editing；
- exact region 占据大部分场景：转 parallel collision-history EDMD；
- 数值收益明确但视觉差异弱：转 JCP/CMAME/SISC 等 numerical route；
- 只有漂亮 mask，没有被恢复的物理 observable：停止 SIG 包装。

## 11. 当前最诚实的可行性判断

- **复现 DynamO/SPARTA/uniGasFoam、建立 paired benchmark：把握高。**
- **做出守恒的静态 particle↔kinetic conversion：技术上可行，但 pair statistics 和 warm-up 是研究点。**
- **证明 history 比强 state-only baseline 更有增量价值：最大未知数。**
- **完成可运行的 dynamic LOD：取决于 practical observability，而不只是 oracle-history 结果。**
- **达到 SIGGRAPH/TOG：必须同时具备科学增量、性能 Pareto、稳定转换和可见物理效果。**

因此这条路线值得立项，但正确的启动方式不是先开发大型 GPU demo，而是先完成 B1/B2 的判死刑实验。这样，即使核心假设失败，损失也是一个可复用的硬球/kinetic benchmark 平台，而不是半年后的 demo 归零。
