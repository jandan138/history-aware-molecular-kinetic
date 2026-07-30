# 从 GAMES103 与流体入门到 History-Aware Molecular–Kinetic Simulation

> **为本项目负责人定制的学习—实现路线**
> 当前基础：学过 GAMES103；接触过连续介质假设、流体物性、压强与应力、欧拉法与拉格朗日法、物质导数、流体微团旋转与变形、流函数与速度势、连续性方程和动量方程。
> 当前缺口：尚未系统学习硬球事件驱动动力学、概率统计、相空间分布、气体动理学、Boltzmann 方程、DSMC、pair correlation、Enskog、随机误差评估，以及 exact ↔ kinetic 动态表示转换。

这份文档不是一张“先修课清单”，也不是要求你先把统计力学和 Boltzmann 方程全部学完，半年后才允许碰代码。

它是一条和本仓库的 **R0–B5 benchmark、M1–M7 milestone 一一对应**的路线：

\[
\boxed{
\text{学一个概念}
\rightarrow
\text{手算一个最小例子}
\rightarrow
\text{写一个几十行实验}
\rightarrow
\text{设计一个会判错的 benchmark}
\rightarrow
\text{接入正式项目}
}
\]

目标不是让你立刻独立证明邓煜、Hani 与 Ma 的定理，而是让你能够真正承担研究负责人的工作：

- 明白代码里的每个状态量代表什么；
- 知道 EDMD 与 DSMC 为什么不同；
- 判断某个误差来自物理模型、离散参数、随机噪声，还是程序 bug；
- 看出“碰撞历史有用”是否只是数据泄漏或有限密度效应；
- 审核 AI 写出的算法，而不是只检查它能不能编译；
- 设计能够支持或推翻论文 claim 的实验。

---

## 0. 先说结论：你不是知识太少，而是还没有把已有知识接到“分子—统计”这条线

你已经熟悉的流体力学，大致沿着下面的方向组织世界：

\[
\text{大量分子}
\longrightarrow
\text{连续介质}
\longrightarrow
\rho(x,t),\,u(x,t),\,p(x,t)
\longrightarrow
\text{连续性方程与动量方程}.
\]

也就是说，你通常从宏观场量开始：

- 这个位置的密度是多少？
- 这个位置的平均速度是多少？
- 这个位置的压强是多少？

本项目却故意把镜头往下拉一层，研究：

\[
\boxed{
\text{精确硬球状态}
\longrightarrow
\text{单粒子相空间分布}
\longrightarrow
\text{宏观场量}
}
\]

写得更具体一点：

\[
\boxed{
\{x_i(t),v_i(t),\text{identity/history}_i\}_{i=1}^{N}
\longrightarrow
f(x,v,t)
\longrightarrow
\rho(x,t),u(x,t),T(x,t),\Pi(x,t),q(x,t)
}
\]

其中：

- 左边保存每一个硬球的位置、速度、身份，以及它曾经和谁碰过；
- 中间不再关心某颗球叫 17 号还是 928 号，只关心某处各种速度的粒子有多少；
- 右边进一步只保留密度、平均速度、温度、应力和热流等少数矩。

所以你接下来最需要补的，不是继续把整本传统流体力学学到湍流，而是五座桥：

1. **硬球与事件驱动动力学**：真实的两体碰撞、碰撞时间和 EDMD；
2. **概率与统计表示**：随机变量、分布、联合分布、独立性、相关性和 ensemble；
3. **相空间与气体动理学**：从 \(x_i,v_i\) 走到 \(f(x,v,t)\)，再从 \(f\) 取矩得到宏观量；
4. **Boltzmann 与 DSMC**：怎样用随机碰撞近似大量稀薄硬球的统计动力学；
5. **相关性与动态 LOD**：什么时候可以忘掉身份，什么时候必须恢复精确粒子和碰撞历史。

---

## 1. 先用一个故事看懂整个项目

想象一个透明盒子里装着十亿颗极小的弹性硬球。

### 1.1 第一台摄像机：逐球拍摄

它记录：

```text
球 1：位置、速度
球 2：位置、速度
...
球 N：位置、速度
```

如果球 8 撞了球 12，随后球 12 撞了球 93，我们都知道。

这就是 exact hard-sphere dynamics。计算上，我们希望用 EDMD（Event-Driven Molecular Dynamics）只跳到下一次碰撞，而不是每个极小时间步检查所有球。

### 1.2 第二台摄像机：看速度直方图

它不再辨认球的身份，而是在每个空间小格中统计：

```text
向右快速运动的球有多少？
向左慢速运动的球有多少？
向上的球有多少？
```

这就是：

\[
f(x,v,t).
\]

它同时依赖位置 \(x\) 和速度 \(v\)。在三维中，位置有三维、速度也有三维，因此它是一个六维分布。

### 1.3 第三台摄像机：只看宏观量

把速度直方图进一步压缩：

- 粒子总数给密度；
- 速度平均给流速；
- 相对平均速度的方差给温度；
- 不同方向的速度协方差给应力；
- 快粒子携带能量的偏向给热流。

### 1.4 本项目的问题

如果某块区域里的粒子近似互相独立，那么第二台摄像机已经够用，不需要保留每颗球的身份证。

如果某块区域出现：

```text
A 撞 B
B 撞 C
C 又回来撞 A
```

这些粒子共享了一段历史。此时只看各自的速度直方图，可能丢掉对未来有用的信息。

于是我们希望动态选择：

\[
\boxed{
\text{需要身份与真实历史的区域：exact EDMD}
}
\]

\[
\boxed{
\text{近似独立、只需统计描述的区域：DSMC / kinetic backend}
}
\]

研究生死问题不是“能否把两个 solver 拼起来”，而是：

> 在控制密度、Knudsen number、非平衡程度、应力、热流、几何和离散误差以后，碰撞历史是否仍能额外预测 EDMD 与 kinetic model 的差异？

---

## 2. 你已有的知识，分别会在项目哪里重新出现

| 你已经学过的内容 | 原来的直觉 | 在本项目中的新位置 |
|---|---|---|
| 质点位置、速度、动量 | 单个物体如何运动 | 每颗硬球的 \(x_i,v_i\) |
| 碰撞冲量与能量 | 碰撞前后满足守恒 | EDMD 的二体碰撞解析更新 |
| 欧拉法 | 固定空间点观察场量 | 每个 block 的 \(f(x,v,t)\)、\(\rho,u,T\) |
| 拉格朗日法 | 跟着质点走 | 跟随硬球轨迹；沿 phase-space characteristic 传播 |
| 物质导数 | 局部变化 + 对流变化 | free-transport operator \(\partial_t f+v\cdot\nabla_xf\) |
| 连续性方程 | 质量不会凭空出现 | EDMD、DSMC 和 representation conversion 的质量账本 |
| 动量方程 | 动量由通量和外力改变 | 碰撞冲量、墙面通量、block interface flux |
| 压强各向同性 | 平衡流体压强各方向相同 | Maxwellian 平衡下 pressure tensor 退化为标量压强 |
| 流体微团变形 | 速度梯度描述局部变形 | state-only baseline 中的应力、非平衡矩和梯度指标 |
| GAMES103 的时间积分 | 连续动力学如何离散 | DSMC/连续后端需要时间步；EDMD 则跳事件 |
| GAMES103 的碰撞检测 | 几何接触与约束 | 硬球连续碰撞时间、邻域结构、移动墙 |
| GAMES103 的能量/Hessian/模态意识 | 不能只看动画 | invariant、误差、收敛、统计不确定性 |

最值得注意的一点是：

> 你已经知道欧拉描述和拉格朗日描述。气体动理学不是把它们推翻，而是把“场”从三维位置空间扩展到了六维相空间。

---

## 3. 知识依赖图

```mermaid
flowchart TD
    A[GAMES103 + 流体入门] --> B[硬球二体碰撞]
    B --> C[连续碰撞时间]
    C --> D[EDMD 事件队列]
    A --> E[概率统计基础]
    E --> F[联合分布与相关性]
    A --> G[相空间分布 f(x,v,t)]
    E --> G
    G --> H[矩：密度/速度/温度/应力/热流]
    G --> I[自由输运与 Liouville 直觉]
    H --> J[Maxwellian / Knudsen]
    I --> K[Boltzmann gain-loss]
    J --> K
    K --> L[DSMC]
    D --> M[EDMD–DSMC paired benchmark]
    L --> M
    F --> N[Pair correlation / Cumulant / Collision graph]
    M --> N
    N --> O[History indicator + Enskog attribution]
    O --> P[Exact ↔ Kinetic conversion]
    P --> Q[Dynamic LOD + Hysteresis + Probes]
    Q --> R[Shared-renderer SIG evidence]
```

不要跳过中间层直接做最右边。否则你会看到很多代码都在跑，却无法回答：

- 为什么这个 block 被 refine？
- 为什么这个 histogram 的差异是模型误差而不是采样噪声？
- 为什么 repeated-pair ratio 不是 DSMC 自己伪造的？
- 为什么高密度误差不是 Enskog correction 能解释的？
- 为什么一次 promotion 没有凭空造能量？

---

## 4. 学习方式：每个概念都要经过“直观—公式—代码—反例”

对每一个主题，都坚持四步。

### 4.1 先讲人话

例如学习 pair correlation，不要先背 \(g(r)\) 定义，而先回答：

> 如果我已经知道 A 球在这里，那么 B 球出现在距离 A 很近的概率，会不会和随机撒点一样？

### 4.2 再手算一个最小例子

例如只算两个等质量球的一次正碰和一次斜碰。

### 4.3 再写几十行参考代码

代码要小到你能逐行解释。第一版禁止“AI 一次生成完整 GPU 框架”。

### 4.4 最后制造一个失败

例如：

- 把碰撞法向写反，检查能量或穿透是否暴露错误；
- 不 invalid event，观察 EDMD 何时出现鬼碰撞；
- 把 DSMC cell 设得过粗，观察流场和碰撞率如何偏差；
- 用随机行切分替代按 scene 切分，观察预测结果怎样虚高；
- promotion 后不校正动量，观察全局漂移。

能被故意破坏并由 benchmark 检出的代码，才开始具有研究可信度。

---

## 第一阶段：硬球力学——先把一颗球撞另一颗球彻底弄明白

### 5. 什么是“硬球”

硬球模型把粒子理想化为：

- 有有限半径；
- 内部不可穿透；
- 球与球之间没有远程力；
- 未接触时做匀速运动；
- 接触瞬间通过冲量改变速度；
- 最简单版本是完全弹性、无摩擦、无旋转。

因此它不是弹簧球。

软体/惩罚法通常写：

\[
F=-k\,\delta,
\]

允许少量重叠，再用很大的力推开。

硬球则要求：

\[
\|x_j-x_i\|\ge r_i+r_j,
\]

碰撞是一个瞬时事件。

这个模型的优点是：二体碰撞有解析解，而且在没有外力时，两次碰撞之间的轨迹也是解析的直线。

---

### 6. 二体弹性碰撞：真正变化的只有相对速度的法向部分

设两颗球质量为 \(m_i,m_j\)，碰撞瞬间球心连线方向为：

\[
n=\frac{x_j-x_i}{\|x_j-x_i\|},
\]

也就是从球 \(i\) 指向球 \(j\)。

定义相对速度：

\[
g=v_i-v_j.
\]

两球正在靠近的条件是：

\[
g\cdot n>0.
\]

为什么？球心距离的变化率是：

\[
\frac{d}{dt}\|x_j-x_i\|
=n\cdot(v_j-v_i)
=-g\cdot n.
\]

如果距离在减小，这个导数小于 0，于是 \(g\cdot n>0\)。

#### 6.1 把速度拆成法向和切向

\[
g=g_n+g_t,
\]

其中：

\[
g_n=(g\cdot n)n,
\qquad
 g_t=g-g_n.
\]

无摩擦硬球碰撞中：

- 切向相对速度不变；
- 法向相对速度反向；
- 总动量守恒；
- 完全弹性时总动能守恒。

这句话比记公式更重要。

#### 6.2 冲量公式

恢复系数为 \(e\) 时，冲量大小为：

\[
J=\frac{(1+e)(g\cdot n)}{1/m_i+1/m_j}.
\]

对球 \(i\) 施加 \(-Jn\)，对球 \(j\) 施加 \(+Jn\)：

\[
v_i'=v_i-\frac{J}{m_i}n,
\]

\[
v_j'=v_j+\frac{J}{m_j}n.
\]

当两球等质量、完全弹性 \(e=1\) 时：

\[
v_i'=v_i-(g\cdot n)n,
\]

\[
v_j'=v_j+(g\cdot n)n.
\]

直观上，就是两球交换了相对运动的法向部分。

#### 6.3 一个一维数值例子

两颗等质量球：

\[
v_i=3,\qquad v_j=1.
\]

完全弹性正碰后：

\[
v_i'=1,\qquad v_j'=3.
\]

它们交换速度。

这只是“一维、等质量”的特殊情况。二维斜碰中，它们只交换沿球心连线方向的分量，切向分量保留。

---

### 7. 碰撞时间：不是问“现在有没有撞”，而是问“下一次什么时候撞”

设当前球心相对位置：

\[
r=x_j-x_i,
\]

相对速度：

\[
w=v_j-v_i.
\]

总接触距离：

\[
\sigma=r_i+r_j.
\]

未来时间 \(t\) 的相对位置是：

\[
r(t)=r+wt.
\]

碰撞条件：

\[
\|r+wt\|^2=\sigma^2.
\]

展开得到二次方程：

\[
(w\cdot w)t^2+2(r\cdot w)t+(r\cdot r-\sigma^2)=0.
\]

定义：

\[
a=w\cdot w,
\quad b=2r\cdot w,
\quad c=r\cdot r-\sigma^2.
\]

判别式：

\[
\Delta=b^2-4ac.
\]

若：

- \(\Delta<0\)：直线轨迹不会相交；
- 两个根都不为正：碰撞只存在于过去；
- 当前已经分离且最近根为正：取最小正根作为下一次碰撞。

还要处理：

- 两球已经重叠；
- 相对速度近似为零；
- 擦边碰撞 \(\Delta\approx0\)；
- 浮点误差让接触点略早或略晚；
- 同一时刻发生多个事件。

这些不是边角问题。EDMD 的可信度常常就毁在事件退化处理上。

---

### 8. 为什么 EDMD 不等于普通刚体 time stepping

#### 普通时间步方法

```text
每隔 Δt：
1. 所有球向前走一步
2. 检测重叠
3. 解碰撞/约束
```

问题是：

- \(\Delta t\) 太大时会穿透；
- \(\Delta t\) 太小时大量时间没有碰撞却仍然计算；
- 很硬的接触需要高频求解；
- 误差与时间步强相关。

#### EDMD

```text
1. 预测所有可能的下一次事件
2. 取最早事件
3. 所有相关状态精确推进到该时间
4. 解析更新碰撞速度
5. 只重算受影响粒子的未来事件
```

它像一个“按事件跳转”的日历，而不是一部逐帧播放的电影。

#### 直观类比

如果你想记录一个人一天中所有会议：

- time stepping：每秒问一次“现在开会了吗？”；
- event driven：直接跳到日历里的下一场会议。

稀薄硬球大部分时间都在自由飞行，因此事件驱动很自然。

---

### 9. EDMD 的核心数据结构

#### 9.1 Event

一次事件至少包含：

```text
time
particle_i
particle_j or wall
version_i
version_j
event_type
```

#### 9.2 Priority queue

按照事件时间排序，最早事件在堆顶。

#### 9.3 为什么事件会失效

假设预测：

```text
A 将在 t=10 撞 B
```

但在 \(t=6\) 时 A 先撞了 C，A 的速度变了。

那么旧的 A–B 事件已经无效，却还躺在队列中。

常用办法是给每颗粒子维护 collision/version counter。创建事件时记录版本号；事件出队时发现版本不一致，就丢弃。

这叫 lazy invalidation。

#### 9.4 空间加速

不能给每对粒子都维护事件，否则候选对数量为：

\[
O(N^2).
\]

需要：

- cell lists；
- neighbor lists；
- spatial hashing；
- bounding cells；
- 对移动墙和周期边界单独处理。

第一版 2D reference 可以先小规模全对，但正式 benchmark 必须有明确扩展路径。

---

### 10. EDMD 里“精确”到底是什么意思

EDMD 经常被称为 exact event-driven dynamics，但要准确理解：

它对所选择的理想模型，能解析推进自由飞行和二体碰撞时间；并不意味着：

- 浮点运算没有误差；
- 同时多体碰撞永远无歧义；
- 高密度下事件顺序不会因舍入改变；
- 它就是现实分子的完整物理；
- 墙面粗糙、旋转、摩擦、分子力都已包含。

所以仓库里的 full EDMD 是**模型内 ground truth**，不是自然界的绝对真理。

---

### 11. 第一阶段最小实验

建议建立学习目录：

```text
learning/
├── 01_binary_collision.ipynb
├── 02_collision_time.ipynb
└── 03_minimal_edmd_2d/
```

完成：

1. 一维等质量正碰；
2. 二维斜碰，画出法向/切向分解；
3. 不同质量的碰撞；
4. 检查动量与能量；
5. 解两球碰撞时间；
6. 一颗球与反射墙；
7. 10–100 个圆盘的最小 EDMD；
8. 故意关闭 event invalidation，观察错误；
9. 比较 EDMD 与很小时间步的 time stepping；
10. 输出 collision log，而不只输出动画。

#### Gate L0：硬球力学过关问题

你应该能不看代码回答：

- 为什么只有相对速度的法向分量被改变？
- 如何判断两球是在靠近还是远离？
- 碰撞时间为什么来自二次方程？
- EDMD 为什么需要 event invalidation？
- “解析事件时间”为什么仍不等于绝对无误差？

对应项目：[`B0 Single-regime primitives`](../benchmarks/b0-single-regime-primitives.md)。

---

## 第二阶段：概率统计——从“一颗具体球”走向“许多可能世界”

### 12. 为什么本项目必须学概率，而不是只学更多碰撞检测

DSMC 不是一个确定性地追踪所有真实分子的算法。

它会随机：

- 采样初始粒子；
- 选择候选碰撞对；
- 采样碰撞散射方向；
- 用有限 simulation particles 估计宏观量。

因此同一个 case 换一个 seed，会得到不同曲线。

如果不会概率统计，你会犯下四种危险错误：

1. 把一次随机波动当成模型差异；
2. 把平均值接近当成所有统计结构都接近；
3. 用随机行切分数据，得到虚假的高预测准确率；
4. 看到一张漂亮速度直方图，却不知道误差条有多大。

---

### 13. 随机变量、分布与直方图

假设从箱子中随机选一颗粒子，记录它的 \(x\) 方向速度：

\[
V_x.
\]

它是随机变量。

概率密度 \(p(v_x)\) 回答：

> 随机抽到的粒子，速度落在 \(v_x\) 附近的可能性有多大？

程序中没有无限粒子，只能画经验直方图：

\[
\hat p(v_x)
=
\frac{\text{落入该 bin 的样本数}}
{\text{总样本数}\times\text{bin width}}.
\]

样本越少，直方图越抖。

所以“曲线有毛刺”不一定是 solver 不稳定，也可能只是 sample count 不足。

---

### 14. 期望、方差与协方差

#### 14.1 期望

\[
\mathbb E[V]
\]

表示重复抽样时的平均值。

#### 14.2 方差

\[
\mathrm{Var}(V)
=
\mathbb E[(V-\mathbb E[V])^2].
\]

它衡量样本围绕平均值有多分散。

温度本质上就与粒子相对平均流速的速度方差有关。

#### 14.3 协方差

对两个分量：

\[
\mathrm{Cov}(V_x,V_y)
=
\mathbb E[(V_x-\bar V_x)(V_y-\bar V_y)].
\]

它回答：

> 当 \(V_x\) 偏大时，\(V_y\) 是否也倾向偏大？

速度协方差组成一个张量，直接连接 pressure/stress tensor。

---

### 15. 联合分布与独立性：这是理解 molecular chaos 的入口

一个粒子的状态记为：

\[
z=(x,v).
\]

两颗粒子的联合分布记为：

\[
f_2(z_1,z_2).
\]

如果两者独立：

\[
f_2(z_1,z_2)=f_1(z_1)f_1(z_2).
\]

这句话的直观含义是：

> 知道第一颗粒子的状态，不会帮助你预测第二颗粒子的状态。

如果 A 刚撞过 B，知道 A 的速度通常会对 B 有额外信息，于是联合分布不能简单拆开。

可以定义二阶相关缺陷：

\[
C_2(z_1,z_2)
=
f_2(z_1,z_2)-f_1(z_1)f_1(z_2).
\]

当 \(C_2=0\) 时完全独立；非零时存在统计相关。

项目里的 collision-history features，本质上是在尝试廉价估计：

> 哪些区域的 \(C_2\) 或更高阶相关信息，可能已经大到影响未来可观察量？

---

### 16. Correlation 不等于 causation，也不等于 collision history

这里必须分清三件事。

#### 16.1 空间排斥相关

硬球不能重叠。知道 A 在某处，就知道 B 不可能出现在 A 的球体内部。

这即使在平衡状态也存在，主要由有限尺寸和 packing fraction 造成。

#### 16.2 非平衡状态相关

例如两股粒子束交叉，速度分布本身就可能双峰、各向异性。

只要完整保存 \(f(x,v)\)，这种非 Maxwellian 状态未必需要额外 history。

#### 16.3 动态碰撞历史相关

A 撞 B、B 撞 C、C 再撞 A，形成共享 lineage 或循环。

这类历史可能是项目想捕捉的增量信息。

如果我们不区分三者，就会把有限密度的 excluded-volume effect 错写成“邓煜启发的历史相关性”。因此 Enskog baseline 是必须的，而不是可选装饰。

---

### 17. Ensemble：一次世界不够，要比较许多平行世界

假设同一个宏观初态：

- 同样的密度；
- 同样的温度；
- 同样的平均流速；
- 同样的几何。

但微观粒子位置和速度可以有很多不同随机 realization。

第 \(s\) 个 realization 的观测量记为：

\[
Y^{(s)}(t).
\]

经验平均：

\[
\bar Y(t)=\frac1S\sum_{s=1}^{S}Y^{(s)}(t).
\]

标准误差通常大致随：

\[
\frac{1}{\sqrt S}
\]

下降，而不是随 \(1/S\) 下降。

想把随机误差缩小十倍，往往需要一百倍样本，这是为什么 B1/B2 的统计设计可能比单次仿真更贵。

---

### 18. 第二阶段最小实验

```text
learning/
├── 04_random_variables_and_histograms.ipynb
├── 05_joint_distribution.ipynb
└── 06_ensemble_uncertainty.ipynb
```

完成：

1. 从已知 Gaussian 分布采样，比较 100、1000、100000 个样本的直方图；
2. 计算均值、方差、协方差；
3. 构造两个边缘分布相同但联合相关不同的数据集；
4. 观察 \(f_1\) 相同而 \(f_2\) 不同；
5. 用 bootstrap 估计置信区间；
6. 比较随机行切分和按完整 case 切分的预测结果；
7. 用不同 seed 运行同一小型粒子实验。

#### Gate L1：概率统计过关问题

- 一次 realization 和 ensemble average 有什么区别？
- 两个系统均值、温度相同，为什么仍可能不同？
- 边缘分布相同为什么不代表联合分布相同？
- sampling noise 与 numerical instability 怎样区分？
- 为什么随机行切分容易泄漏同一轨迹的信息？

---

## 第三阶段：相空间分布——把你熟悉的欧拉场扩展一层

### 19. 从 \(u(x,t)\) 到 \(f(x,v,t)\)

传统流体在每个位置保存一个平均速度：

\[
u(x,t).
\]

但想象同一位置有两股粒子束：

- 一半以 \(+10\) 向右；
- 一半以 \(-10\) 向左。

平均速度是：

\[
u=0.
\]

如果只看 \(u=0\)，你可能误以为气体静止；实际上它包含两股高速对冲粒子。

所以 kinetic description 在每个位置保存完整速度分布：

\[
f(x,v,t).
\]

它回答：

> 在位置 \(x\) 附近、速度 \(v\) 附近，有多少粒子？

这就是为什么 kinetic model 能描述强非平衡、多峰和弹道运动，而单纯 \(\rho,u,T\) 可能不够。

---

### 20. 相空间：每颗粒子不是空间中的一个点，而是状态空间中的一个点

三维粒子有：

\[
x=(x,y,z),
\qquad
v=(v_x,v_y,v_z).
\]

所以一颗粒子的状态是六维点：

\[
z=(x,v).
\]

所有粒子在六维相空间形成一团点云。

- 位置接近但速度不同的粒子，在相空间中可以离得很远；
- 速度接近但位置很远的粒子，也不是同一局部状态。

DSMC 的空间 cell 只是在 \(x\) 维上分箱；每个 cell 内的 simulation particles 隐式采样速度维度。

---

### 21. 从 \(f\) 取矩，恢复你熟悉的宏观量

以下先写 number distribution 的常见形式。不同软件的 \(f\) normalization 可能不同，项目中必须明确单位。

#### 21.1 数密度

\[
n(x,t)=\int f(x,v,t)\,dv.
\]

质量密度：

\[
\rho=mn.
\]

#### 21.2 平均速度

\[
u(x,t)
=
\frac{1}{n}
\int v f(x,v,t)\,dv.
\]

#### 21.3 热运动速度

定义 peculiar velocity：

\[
c=v-u.
\]

它表示粒子速度减去局部平均流速。

#### 21.4 温度

在 \(d\) 维中：

\[
\frac{d}{2}nk_BT
=
\int \frac12 m|c|^2 f\,dv.
\]

所以温度不是“平均速度大”，而是相对平均速度的随机运动强。

整团气体以 \(1000\) m/s 匀速飞行，如果内部速度都几乎相同，它可以具有很低温度。

#### 21.5 Pressure/stress tensor

\[
P
=
m\int cc^T f\,dv.
\]

平衡各向同性时：

\[
P=pI.
\]

非平衡时三个方向可能不同，还可能有剪切分量。

这里写的是由单粒子速度分布得到的 **kinetic contribution**。对有限密度硬球，总压强还可能包含碰撞冲量/virial contribution；这部分与接触 pair structure 有关，不能总由单粒子 \(f\) 完整恢复。这个区别正是后续 Enskog attribution 与 EDMD oracle 必须保留的原因之一。

#### 21.6 Heat flux

\[
q
=
\int \frac12m|c|^2c\,f\,dv.
\]

它表示热运动能量更倾向被哪些粒子带向哪个方向。

这些高阶矩正是强 state-only baseline。我们的 history feature 必须在控制它们后仍有增量价值，才有研究意义。

---

### 22. 自由输运：物质导数在相空间里的亲戚

先忽略碰撞和外力。

每颗粒子做：

\[
x(t)=x_0+vt.
\]

沿着这条轨迹，粒子携带的相空间密度不变：

\[
\frac{df}{dt}=0.
\]

展开：

\[
\boxed{
\frac{\partial f}{\partial t}
+v\cdot\nabla_x f
=0
}
\]

这和你学过的物质导数非常像：

\[
\frac{D\phi}{Dt}
=
\frac{\partial\phi}{\partial t}
+u\cdot\nabla\phi.
\]

区别是：

- 流体场用局部平均速度 \(u(x,t)\) 对流；
- kinetic distribution 对每个速度坐标 \(v\) 分别输运。

有外力 \(F\) 时，还会在速度空间移动：

\[
\frac{\partial f}{\partial t}
+v\cdot\nabla_x f
+\frac{F}{m}\cdot\nabla_v f
=0.
\]

所以相空间里的“流动”同时发生在位置维和速度维。

---

### 23. Maxwellian：局部平衡时的速度钟形分布

在三维、局部平衡的理想气体中：

\[
f_M(v)
=
n
\left(\frac{m}{2\pi k_BT}\right)^{3/2}
\exp\left(
-\frac{m|v-u|^2}{2k_BT}
\right).
\]

这是三维写法；二维硬圆盘实验的归一化前因子会随维数改变。项目里的 artifact 和 oracle adapter 必须把空间维数写进元数据，不能把 2D/3D normalization 混用。

直观上：

- 中心在平均流速 \(u\)；
- 温度越高，分布越宽；
- 远离平均速度的极快粒子更少；
- 平衡时各方向宽度相同。

#### 23.1 两股对冲粒子不是 Maxwellian

即使它们：

- 平均速度为 0；
- 总能量对应某个温度；

速度分布仍可能是双峰，而不是一个 Gaussian 峰。

所以只比较 \(\rho,u,T\) 会漏掉重要信息。

#### 23.2 Maxwellian residual

可以定义某种距离：

\[
R_M=D(f,f_M).
\]

它是重要的 state-only feature，但仍不自动等于“碰撞历史相关性”。

---

### 24. Mean free path 与 Knudsen number

平均自由程 \(\lambda\) 是粒子两次碰撞间平均飞行距离。

选择场景特征长度 \(L\)，定义：

\[
\mathrm{Kn}=\frac{\lambda}{L}.
\]

直观分类：

- \(\mathrm{Kn}\ll1\)：粒子在宏观变化尺度内碰很多次，局部平衡和 continuum 描述较合理；
- \(\mathrm{Kn}\sim1\)：输运与几何尺度相当，强 kinetic/non-equilibrium；
- \(\mathrm{Kn}\gg1\)：粒子近似弹道飞行，碰撞稀少。

但本项目不是单纯做 continuum ↔ DSMC 切换。

我们的 exact ↔ kinetic 问题更细：即使 kinetic description 必须保留，是否还需要保留真实粒子身份和历史？

---

### 25. 第三阶段最小实验

```text
learning/
├── 07_phase_space_cloud.ipynb
├── 08_moments_from_particles.ipynb
├── 09_free_transport.ipynb
└── 10_maxwellian_and_bimodal.ipynb
```

完成：

1. 在 \((x,v_x)\) 二维相空间画点云；
2. 从粒子样本计算 \(n,u,T,P,q\)；
3. 构造平均速度和温度相同、但一个 Maxwellian、一个双峰的两组样本；
4. 实现无碰撞自由输运；
5. 验证沿 characteristic 分布平移；
6. 观察空间 histogram 和速度 histogram 的关系；
7. 检查单位与 normalization。

#### Gate L2：相空间过关问题

- 为什么 \(u=0\) 不代表粒子都不动？
- \(f(x,v,t)\) 比 \(\rho,u,T\) 多保存了什么？
- 温度为什么与相对平均速度有关？
- pressure tensor 为什么在非平衡时不一定是 \(pI\)？
- free transport 方程与物质导数有什么联系？

---

## 第四阶段：Boltzmann 方程——把自由输运和随机碰撞放在一起

### 26. 方程的整体结构

\[
\boxed{
\frac{\partial f}{\partial t}
+v\cdot\nabla_x f
=Q(f,f)
}
\]

左边：粒子带着自己的速度穿过空间。

右边：碰撞把粒子从某些速度搬到另一些速度。

你可以把一个速度 bin 想成地铁站：

- loss：原来在这个速度站的粒子碰完后离开；
- gain：别的速度组合碰完后进入这个站。

所以 \(Q\) 是 gain–loss operator。

---

### 27. 一次硬球碰撞在速度空间里做了什么

给定碰撞前速度：

\[
v,v_*.
\]

碰撞后速度：

\[
v',v_*'.
\]

满足：

\[
v+v_*=v'+v_*',
\]

\[
|v|^2+|v_*|^2=|v'|^2+|v_*'|^2
\]

（等质量、完全弹性情况下）。

碰撞算子会积分所有可能的：

- 对手速度；
- 碰撞方向；
- 相对速度；
- 截面权重。

不用第一遍就掌握完整积分形式，但必须知道它不是简单的“往 Maxwellian 拉一下”。

---

### 28. Molecular chaos：Boltzmann closure 偷偷做了什么

真正的碰撞率依赖两粒子联合分布：

\[
f_2(z_1,z_2).
\]

为了只用单粒子分布 \(f_1\) 封闭方程，需要近似即将碰撞的粒子统计独立：

\[
f_2(z_1,z_2)
\approx
f_1(z_1)f_1(z_2).
\]

这就是 molecular chaos 的核心。

它并不是说：

- 粒子轨迹不混沌；
- 所有粒子永远互不相关；
- 碰撞后不会产生相关性。

而是说，在目标极限中，进入碰撞的粒子对可以用单粒子分布的乘积近似，相关项对宏观动力学的影响可控。

邓煜、Hani 与 Ma 的工作深刻之处，就在于长期碰撞会不断产生相关性，他们需要显式组织 cumulants 和 collision-history molecules，再证明这些相关项在相应低密度极限中仍能被控制。

本项目只能说受此概念启发，不能说他们的 cutting proof 已经给出了我们的在线 indicator。

---

### 29. 微观可逆，宏观为什么像不可逆

硬球碰撞在理想条件下时间可逆：把所有速度取反，系统会沿原轨迹返回。

Boltzmann 方程却有趋向平衡和熵增的方向性。

直观原因是：

\[
\text{完整微观状态}
\rightarrow
\text{只保留单粒子统计}
\]

丢掉了精细的多粒子相关信息。

要让混合气体自己“倒放分离”，不只需要把每个速度分布反过来，还需要恢复极端精细的粒子间相位/历史相关性。

这个不可逆性故事对项目很重要，因为 exact → kinetic demotion 本身就是一次信息压缩。我们必须明确：

- 哪些量被严格保留；
- 哪些统计被近似保留；
- 哪些历史被主动丢弃；
- 之后若 promotion，哪些信息已经无法唯一恢复。

---

### 30. 从 Boltzmann 取矩，为什么会回到流体方程

对 Boltzmann 方程分别乘：

\[
1,
\qquad v,
\qquad |v|^2
\]

再对速度积分，可以得到：

- 质量守恒；
- 动量守恒；
- 能量守恒。

这和你已经学过的连续性方程、动量方程不是两套互不相干的理论。

它们是同一层级链：

\[
\text{hard spheres}
\rightarrow
\text{Boltzmann}
\rightarrow
\text{moment equations / fluid equations}.
\]

难点在于矩方程通常不封闭：低阶矩的演化依赖更高阶矩。这就是 closure problem。

---

## 第五阶段：DSMC——用随机粒子数值近似 Boltzmann

### 31. DSMC 粒子不是一颗真实分子的长期身份证

一个 DSMC simulation particle 往往代表许多真实分子。

它保存：

- 位置；
- 速度；
- species；
- statistical weight。

但它的“粒子 ID”主要是数值样本身份，不应被解释成某颗真实分子跨越很长时间的精确身份。

特别是 DSMC 中同一 cell 内的碰撞对象是随机抽取的，通常并不要求两颗 simulation particles 在几何上真的接触。

所以：

> DSMC collision log 不是 exact hard-sphere collision history。

这也是为什么不能简单在 DSMC 区域统计 repeated pair，然后声称检测到了真实历史相关性。

---

### 32. DSMC 的基本循环

一个典型时间步可以理解为：

```text
A. Move
   每个 simulation particle 按当前速度移动

B. Boundary
   处理墙面、入口、出口、周期边界

C. Bin
   按空间 cell 对粒子分组

D. Collide
   每个 cell 中随机抽候选对
   根据相对速度与截面接受/拒绝碰撞
   采样散射方向并更新速度

E. Sample
   统计密度、速度、温度、应力、热流等
```

它常把 transport 与 collision 分裂处理。

---

### 33. 为什么随机抽碰撞能够近似 Boltzmann collision operator

Boltzmann 方程关心的是某类速度组合的统计碰撞率，而不是哪两颗带身份证的粒子真的相遇。

在足够小、状态近似均匀的 cell 中：

- simulation particles 是局部 \(f(v)\) 的样本；
- 随机抽对近似从 \(f(v)f(v_*)\) 取样；
- 接受概率编码相对速度和碰撞截面；
- 散射规则编码碰撞后速度分布。

大量样本和时间平均后，随机碰撞统计逼近 \(Q(f,f)\)。

这就是 Monte Carlo 的思路：不直接计算高维积分，而用随机样本估计积分。

---

### 34. DSMC 的四类误差

#### 34.1 模型误差

Boltzmann/molecular-chaos/稀薄假设本身不适用。

#### 34.2 空间离散误差

cell 太大，内部状态并不均匀，却被当作一个局部池随机配对。

#### 34.3 时间离散误差

时间步太大，transport 与 collision 分裂失真，粒子一步跨越太多结构。

#### 34.4 统计误差

每 cell simulation particles 太少，估计量噪声大。

项目必须先控制后三类，才有资格把 EDMD–DSMC discrepancy 归因于第一类，更不能直接归因于 history。

---

### 35. DSMC 的关键分辨率直觉

第一遍不要只背固定阈值，而要理解：

- cell 应足以解析宏观空间变化；
- 碰撞池不能跨越物理上明显不同的区域；
- 时间步应解析平均碰撞/输运时间；
- particle weight 和每 cell 样本数决定噪声；
- wall model 与边界通量可能主导局部误差。

在论文里，必须用 convergence envelope 说明：继续减小 cell/time step 或增加 particles 后，结果已趋于稳定。

---

### 36. EDMD 与 DSMC 的最直观对比

| 维度 | EDMD | DSMC |
|---|---|---|
| 粒子身份 | 真实、持续 | 数值样本身份 |
| 碰撞对象 | 几何上真正接触的球 | cell 内随机候选对 |
| 时间推进 | 事件驱动 | 离散时间步 |
| 主要目标 | 精确模拟给定硬球微观模型 | 数值求解 Boltzmann 型统计动力学 |
| 噪声 | 初态 ensemble 有随机性，但单轨迹确定 | 算法本身含 Monte Carlo 噪声 |
| 高密度 | 硬球模型可继续运行，但事件密集 | Boltzmann DSMC 物理模型可能失效 |
| 历史 | 可记录真实碰撞链 | 随机配对历史不等于真实分子历史 |
| 成本瓶颈 | 事件队列、频繁碰撞、邻域更新 | 粒子数、cell、时间步、统计采样 |

---

### 37. 第四、五阶段最小实验

```text
learning/
├── 11_boltzmann_gain_loss_toy.ipynb
├── 12_minimal_dsmc_2d/
├── 13_homogeneous_relaxation.ipynb
└── 14_edmd_dsmc_first_pair.ipynb
```

完成：

1. 一个离散速度的 gain–loss 玩具模型；
2. 最小 DSMC：move、bin、random collide、sample；
3. 无空间梯度的各向异性速度 relaxation；
4. 检查质量、动量、能量；
5. cell-size sweep；
6. time-step sweep；
7. particle-count/weight sweep；
8. 多 seed 置信区间；
9. 与最小 EDMD 在低密度下比较速度分布和矩；
10. 跑通 SPARTA 外部 case，再对齐单位和输出定义。

#### Gate L3：Boltzmann/DSMC 过关问题

- Boltzmann 方程左边和右边分别做什么？
- molecular chaos 实际近似了哪个联合分布？
- DSMC 粒子为什么不等于真实硬球身份？
- cell、time step、particle count 分别影响什么？
- 看到 EDMD 与 DSMC 不同，为什么还不能说 history 有用？

对应项目：[`R0 External oracles`](../benchmarks/r0-external-oracles.md) 与 [`B0 Single-regime primitives`](../benchmarks/b0-single-regime-primitives.md)。

---

## 第六阶段：Pair correlation、Enskog 与碰撞历史——项目最容易混淆的核心

### 38. Pair correlation function \(g(r)\)

设粒子整体数密度为 \(n\)。如果粒子位置完全独立，知道 A 在原点后，在距离 \(r\) 的小壳层找到 B 的概率只由壳层体积和 \(n\) 决定。

定义 \(g(r)\) 比较：

\[
g(r)
=
\frac{\text{实际粒子对在距离 }r\text{ 出现的概率}}
{\text{独立均匀分布下的概率}}.
\]

- \(g(r)=1\)：该距离近似无额外空间相关；
- \(g(r)>1\)：粒子更倾向出现在该距离；
- \(g(r)<1\)：粒子更不倾向出现在该距离；
- 对硬球，\(r<\sigma\) 时 \(g(r)=0\)，因为不能重叠。

因此即使没有复杂历史，硬球有限尺寸也自动产生 pair structure。

---

### 39. 为什么 Boltzmann 在有限密度下可能不够

Boltzmann–Grad 极限强调低密度、短程二体碰撞和近似独立的入射粒子。

当 packing fraction 增大：

- 接触附近 \(g(\sigma^+)\) 不再接近 1；
- 粒子有限尺寸影响碰撞率和空间输运；
- 多次近邻碰撞更常见；
- 简单 DSMC 的随机、局部、factorized 配对可能偏差。

如果 EDMD–DSMC discrepancy 主要来自这些有限密度效应，那么更合适的 coarse model 可能是 Enskog 型 kinetic model，而不是开启 exact patch。

---

### 40. Enskog 思想的直观版本

Boltzmann 碰撞率大致使用：

\[
f(x,v)f(x,v_*).
\]

Enskog 会考虑有限球直径和接触位置偏移，并用接触 pair-correlation 修正碰撞概率。

直观上：

> 在拥挤房间里，人与人相撞的概率不仅由各自速度直方图决定，还由人群在接触距离附近怎样排布决定。

项目必须比较：

```text
Boltzmann/DSMC discrepancy
vs
Enskog-corrected discrepancy
```

如果 Enskog 已经解释了差异，history indicator 的新颖性会显著减弱，但项目可以诚实转向 EDMD–Enskog adaptive solver。

---

### 41. 碰撞图：把历史压缩成一个时窗内的网络

在 rolling time window \([t-\tau,t]\) 内：

- 顶点：参与碰撞的粒子；
- 边：一次碰撞；
- 时间戳：碰撞发生时间；
- 可选方向：按时间先后形成 lineage/DAG。

候选特征包括：

#### 41.1 Repeated-pair ratio

\[
r_{\mathrm{repeat}}
=
\frac{\text{重复粒子对碰撞次数}}
{\text{总碰撞次数}}.
\]

#### 41.2 Connected component size

一段时间内有多少粒子被碰撞链连在一起。

#### 41.3 Cycle rank

对无向图：

\[
\beta_1=|E|-|V|+C,
\]

其中 \(C\) 是连通分量数。仓库当前 reference feature 把 \(|E|\) 定义为 **unique collision pairs** 的边数；同一粒子对重复碰撞由 repeated-pair ratio 另行记录。若以后改成 multigraph 或 time-directed graph，cycle 的定义和数值都必须版本化，不能静默更换。

树状传播时 \(\beta_1=0\)；出现回环后 \(\beta_1>0\)。

#### 41.4 Lineage depth / shared ancestor

两颗即将碰撞的粒子，近期是否通过碰撞链共享过祖先信息。

#### 41.5 Low-dimensional cumulant proxy

不直接存高维 \(C_2(z_1,z_2)\)，而用：

- velocity-pair covariance；
- kernel features；
- random Fourier features；
- small basis projection；
- shadow EDMD probe；

近似相关强度。

---

### 42. 为什么 collision graph feature 可能没用

必须主动考虑失败：

1. 真正低密度时，循环和重碰撞本来就极少；
2. 高密度时，packing/Enskog 已解释大部分误差；
3. 图特征可能只是密度的昂贵替代品；
4. 时间窗口和 block 大小可能让结果任意；
5. oracle EDMD history 在线上 coarse region 中不可观测；
6. feature 可能预测当前误差，却不能预测未来 horizon；
7. 图统计可能对粒子重标号、block crossing 和边界处理敏感。

所以 B2 不是“训练一个分类器”，而是验证 history 是否有**条件增量信息**。

---

### 43. Feature observability firewall

所有 feature 必须分成三类。

#### 43.1 Runtime-observable

coarse solver 当前真实能看到：

- density、temperature；
- stress、heat flux；
- Maxwellian residual；
- Knudsen/gradient indicators；
- geometry、wall distance；
- coarse collision statistics；
- temporal derivatives。

#### 43.2 Shadow-probe

需要从 coarse block 临时生成一个小型 exact micro-simulation 才能估计：

- short-horizon repeated collisions；
- cycle growth；
- exact–kinetic local divergence；
- pair/cumulant proxy。

必须把 probe 成本计入总成本。

#### 43.3 Oracle-only

只有 full EDMD ground truth 才知道：

- 全域真实 collision lineage；
- future exact discrepancy；
- 所有微观身份。

它们可以当标签或理论上界，不能偷偷输入在线 policy。

---

### 44. 第六阶段最小实验

```text
learning/
├── 15_radial_distribution.ipynb
├── 16_collision_graph.ipynb
├── 17_enskog_attribution.ipynb
└── 18_observability_audit.md
```

完成：

1. 从 EDMD 粒子位置估计 \(g(r)\)；
2. 验证硬球内部 \(g(r)=0\)；
3. 比较不同 packing fraction 的接触峰；
4. 维护 rolling collision graph；
5. 手工构造树、重复边和 cycle，验证图特征；
6. 改变 time window/block size，检查 feature 稳健性；
7. 比较 state-only、Enskog-aware 与 history-aware 特征；
8. 给每个 feature 打上 runtime/shadow/oracle 标签。

#### Gate L4：相关性过关问题

- \(g(r)\) 与 collision history 是同一件事吗？
- 为什么有限密度可能让 DSMC 失效？
- Enskog 主要补了什么？
- cycle rank 为什么只是 proxy，不是 \(C_2\) 本身？
- 为什么 oracle-only history 不能直接用于在线 refinement？

对应项目：[`B1 Discrepancy atlas`](../benchmarks/b1-discrepancy-atlas.md) 与 [`B2 History indicator`](../benchmarks/b2-history-indicator.md)。

---

## 第七阶段：如何科学地证明“history 有额外价值”

### 45. 先定义要预测的误差，而不是先堆 feature

对空间 block \(B\)，定义未来 horizon \(\Delta T\) 上的 discrepancy：

\[
e_B(t,\Delta T)
=
D\left(
Y^{\mathrm{EDMD}}_B(t+\Delta T),
Y^{\mathrm{kinetic}}_B(t+\Delta T)
\right).
\]

其中 \(Y\) 可以包含：

- velocity distribution；
- density/temperature；
- stress tensor；
- heat flux；
- collision rate；
- pair structure；
- wall force；
- tracer transport。

不同应用关心的 \(D\) 不同。不能含糊地说“两个结果不一样”。

---

### 46. 强 state-only baseline

至少应包含：

\[
s_B=
(
\rho,
\phi,
T,
u,
\mathrm{Kn},
R_M,
P,
q,
\nabla\rho,
\nabla T,
\text{geometry},
\text{resolution}
).
\]

这里的 \(\phi\) 表示 packing fraction，不是你在势流中见过的速度势；\(P\) 表示 pressure/stress tensor。项目中应优先使用带语义的字段名，避免只靠单字母在代码里传播。

history-aware model 输入：

\[
(s_B,h_B).
\]

核心问题：

\[
\text{Does }h_B\text{ improve held-out prediction beyond }s_B\text{?}
\]

而不是：

\[
\text{Can a large model fit the training set?}
\]

---

### 47. 为什么必须 grouped split

假设同一次长仿真每个时间步都产生样本。

若随机按行切分：

- \(t=1.000\) 的 block 进入训练集；
- \(t=1.001\) 的同一 block 进入测试集。

两者几乎相同，模型看似泛化，其实记住了轨迹。

必须按：

- 完整 run；
- geometry family；
- density/Kn regime；
- transient family；
- seed family；

分组切分。

最有说服力的是 leave-geometry-out 与 leave-regime-out。

---

### 48. Matched-state pairs：最强的直观实验

找到两块区域，使它们的：

\[
\rho,T,u,P,q,R_M,\mathrm{Kn}
\]

尽可能接近，但历史特征不同。

然后观察未来 EDMD–kinetic discrepancy 是否不同。

如果能稳定找到这种 pair，论文故事会非常清楚：

> 局部状态看起来相同，但因为近期碰撞网络不同，factorized kinetic model 的未来误差不同。

如果找不到，history claim 应被降级。

---

### 49. 数值误差必须先从模型误差中剥离

对 DSMC 做：

- cell-size convergence；
- time-step convergence；
- particles-per-cell convergence；
- seed uncertainty。

对 EDMD 做：

- event precision audit；
- conservation；
- tie handling；
- finite-size/ensemble study。

只有当：

\[
\text{observed discrepancy}
>
\text{numerical uncertainty + sampling uncertainty}
\]

时，模型差异才可解释。

---

### 50. 预测准确不等于 adaptive policy 有价值

即使模型能预测 \(e_B\)，还要问：

- 高误差区域是否占合适比例？
- 提前量是否足够完成 promotion？
- false positive 会不会让 exact region 爆炸？
- false negative 是否错过关键物理？
- probe 成本是否抵消加速？
- policy 是否改善 cost–quality Pareto frontier？

所以 B2 的终点不是高 \(R^2\)，而是能改变实际 partition decision。

---

### 51. 第七阶段最小实验

```text
learning/
├── 19_discrepancy_metrics.ipynb
├── 20_grouped_splits.ipynb
├── 21_matched_state_pairs.ipynb
└── 22_incremental_value_report.md
```

完成：

1. 为 velocity histogram 实现 L1、Wasserstein 或 JS 型距离；
2. 为 tensor/moment 实现归一化误差；
3. 构建 paired EDMD–DSMC dataset；
4. 做随机行切分和 grouped split 对比；
5. 训练简单线性/树模型作为 baseline；
6. 加入 history feature 做增量 ablation；
7. bootstrap held-out confidence interval；
8. 找 matched-state pairs；
9. 做 Enskog attribution；
10. 写一页诚实的 negative result 模板。

#### Gate L5：实验设计过关问题

- target discrepancy 是当前误差还是未来误差？
- 为什么同一轨迹相邻帧不能跨 train/test？
- 怎样证明 history 不是 density proxy？
- 怎样证明误差不是 DSMC 分辨率不足？
- prediction metric 怎样转化为 partition/cost metric？

---

## 第八阶段：Exact ↔ Kinetic 表示转换

### 52. Demotion：从很多真实球压缩成统计粒子

假设 exact block 中有粒子：

\[
\{x_i,v_i,m_i\}_{i=1}^{N}.
\]

需要变成较少 kinetic superparticles。

至少要保留：

\[
M=\sum_i m_i,
\]

\[
P=\sum_i m_i v_i,
\]

\[
E=\sum_i\frac12m_i|v_i|^2.
\]

但只保这三项仍可能破坏：

- velocity distribution shape；
- stress tensor；
- heat flux；
- species concentration；
- spatial pair structure；
- wall-near distribution。

所以 demotion 是有损压缩，不是简单删粒子。

---

### 53. 一个直观的动量—能量校正方法

假设先从目标速度分布采样出 \(N_s\) 个等权速度 \(\tilde v_i\)。

#### 53.1 校正平均速度

计算样本均值：

\[
\tilde u=\frac1{N_s}\sum_i\tilde v_i.
\]

将速度平移：

\[
v_i^{(1)}=\tilde v_i-\tilde u+u_{\mathrm{target}}.
\]

这样总动量匹配目标。

#### 53.2 校正热能

定义相对目标平均速度：

\[
c_i=v_i^{(1)}-u_{\mathrm{target}}.
\]

计算当前热能并用比例 \(s\) 缩放：

\[
v_i^{(2)}
=
u_{\mathrm{target}}+s c_i.
\]

选择 \(s\) 使热能匹配。

这只是最简单的 equal-weight correction。它可能改变高阶分布，需要进一步优化或 constrained resampling。

---

### 54. Promotion：从统计分布生成有身份的硬球

promotion 比 demotion 更难，因为 kinetic state 没有唯一微观实现。

必须决定：

- 生成多少颗真实球；
- 放在什么位置；
- 如何避免重叠；
- 怎样匹配局部 \(f(v)\)；
- 怎样严格匹配动量与能量；
- 是否匹配 \(g(r)\) 或 contact structure；
- 新生成粒子的 collision history 从何时开始成熟。

#### 54.1 位置采样

稀薄区域可以近似均匀随机放置，再做 rejection。

有限密度时需要：

- sequential inhibition；
- packing-aware sampling；
- local relaxation；
- 从已有模板/微结构采样；
- Enskog/contact statistics 约束。

#### 54.2 速度采样

从 local velocity distribution 采样，而不一定从 Maxwellian 采样。

之后做守恒校正。

#### 54.3 History maturity

刚 promotion 的粒子没有真实过去。

不能立刻把“history score 低”解释为 molecular chaos，因为它只是还没积累历史。

因此 block 状态需要 warm-up/maturity 标记。

---

### 55. Interface：一半 exact、一半 kinetic 时谁和谁碰

动态 LOD 最棘手的地方往往是边界。

需要定义：

- exact 粒子穿入 kinetic 区域时何时 demote；
- kinetic superparticle 穿入 exact 区域时何时展开；
- interface buffer 有多宽；
- 两侧是否重复计算质量/动量；
- collision partner 能否跨 representation；
- flux 如何匹配；
- moving interface 是否产生人工压缩或稀释。

所以 B3 先做静态 conversion 和静态 interface，禁止一上来同时调 dynamic policy。

---

### 56. Physics LOD 与 Rendering LOD 必须分开

相机靠近时多显示一些球，这是 rendering refinement。

某区域因为模型误差需要 exact，是 physics refinement。

两者不能混淆：

- 相机移开，不代表物理上可以 demote；
- 相机靠近，也不应自动改变物理模型；
- 可以在 kinetic 区域为显示采样“visual particles”，但它们不能偷偷参与 physics；
- exact particles 的 identity 与 display instance 必须明确区分。

这是 SIG demo 中非常容易被不小心破坏的边界。

---

### 57. Hysteresis 与 block state machine

如果只用一个阈值 \(\tau\)：

```text
score > τ → exact
score < τ → kinetic
```

score 在阈值附近抖动会导致频繁切换。

使用两个阈值：

\[
\tau_{\mathrm{promote}}>\tau_{\mathrm{demote}}.
\]

并加入：

- cooldown；
- minimum dwell time；
- warm-up；
- exact budget；
- neighbor dilation；
- failure state。

可能的状态机：

```text
KINETIC
  ↓ trigger
PROMOTING
  ↓ valid
EXACT_WARMUP
  ↓ mature
EXACT
  ↓ low score for long enough
DEMOTING
  ↓ valid
KINETIC
```

任何 conversion 失败都必须有可恢复路径，而不是 silently drop particles。

---

### 58. 第八阶段最小实验

```text
learning/
├── 23_demotion_conservation.ipynb
├── 24_promotion_sampling.ipynb
├── 25_static_interface.ipynb
└── 26_block_state_machine.ipynb
```

完成：

1. exact sample → fewer weighted particles；
2. 精确校正 mass/momentum/energy；
3. 检查 stress、heat flux、histogram 的副作用；
4. kinetic distribution → overlap-free hard disks；
5. 检查 \(g(r)\) 与 velocity distribution；
6. 设置 history maturity；
7. 静态 interface 通量测试；
8. threshold sweep；
9. hysteresis 与 cooldown；
10. 记录每次 conversion report。

#### Gate L6：转换与 LOD 过关问题

- 保住 \(M,P,E\) 为什么仍可能得到错误状态？
- promotion 为什么没有唯一答案？
- 新生成粒子的 history 为什么不能马上使用？
- physics LOD 与 screen-space LOD 有什么区别？
- interface 怎样产生人工质量或动量通量？

对应项目：[`B3 Representation conversion`](../benchmarks/b3-representation-conversion.md) 与 [`B4 Dynamic LOD`](../benchmarks/b4-dynamic-lod.md)。

---

## 第九阶段：工程实现——什么时候再进入 C++、GPU 和大规模 Demo

### 59. 第一版必须有一个“慢但透明”的参考实现

在优化前，保留：

- Python/NumPy 小规模 reference；
- C++ 单线程 reference；
- 完整 collision log；
- 可重复 seed；
- 每一步 invariant；
- 简单 CSV/NPZ artifact。

GPU kernel 速度再快，如果无法逐事件重放，就很难定位：

- event queue bug；
- block crossing；
- race condition；
- history window 错误；
- conversion double counting。

---

### 60. 后续 native/GPU 模块的合理分解

```text
native/
├── geometry/
│   ├── hard_sphere_contact
│   ├── walls
│   └── periodic_domain
├── edmd/
│   ├── event_prediction
│   ├── event_queue
│   ├── invalidation
│   └── neighborhood
├── kinetic/
│   ├── transport
│   ├── collision_sampling
│   ├── moments
│   └── enskog_backend
├── history/
│   ├── rolling_graph
│   ├── streaming_sketch
│   └── shadow_probe
├── conversion/
│   ├── demotion
│   ├── promotion
│   └── interface
└── runtime/
    ├── block_state_machine
    ├── scheduler
    └── budgets
```

不要把 renderer、solver、indicator 和 policy 全塞进一个 `Simulation.cpp`。

---

### 61. Collision history 为什么适合 streaming sketch

完整保存所有历史会无限增长。

实际在线系统只关心有限时间/空间窗口：

- 最近 \(\tau\) 时间；
- 当前 block 与邻域；
- 特定粒子 lineage 深度；
- 近似 graph statistics。

可以使用：

- ring buffer；
- time-to-live edges；
- rolling hash；
- union-find 的窗口近似；
- count-min/bloom-like pair sketch；
- reservoir sampling；
- sparse shadow probe。

但任何 sketch 都要先和精确小规模 graph 对拍，测 bias 与 variance。

---

### 62. 何时值得 GPU 化

只有当：

1. B0 reference 正确；
2. B1 discrepancy 非平凡；
3. B2 history hypothesis 有信号；
4. profiler 显示具体瓶颈；

才进入 GPU 优化。

优先候选：

- particle binning/sorting；
- DSMC collision batches；
- histogram/moment reduction；
- history feature aggregation；
- block-level conversion；
- instanced sphere output。

EDMD 的全局最早事件队列并不天然 GPU-friendly，可能需要：

- spatially local queues；
- conservative time windows；
- speculative batches；
- rollback；
- graph coloring。

这可能成为后续论文线，但不应在 feasibility spike 中同时解决。

---

## 第十阶段：Demo 不再成为无底洞

### 63. 共享 renderer 只负责“看见证据”

第一版只支持四层：

1. instanced spheres；
2. density/temperature/species volume；
3. exact/kinetic mask；
4. collision graph、histogram、conservation overlay。

禁止第一阶段加入：

- 电影级烟雾；
- 火焰与化学反应；
- 复杂路径追踪；
- 多种材质系统；
- 真实航天器资产；
- 大量后期特效。

论文核心不是“球渲染得像分子”，而是表示切换与物理差异可被看懂。

---

### 64. 三个 Hero Scene 分别证明什么

#### 64.1 Zoomable Mixing Chamber

证明：

- macro field 与 exact particles 无缝切换显示；
- conversion 不导致质量/动量跳变；
- 不是相机决定 physics refinement。

#### 64.2 Correlation Labyrinth

证明：

- state moments 相近的区域可有不同 history；
- state-only policy 与 history-aware policy 做出不同决策；
- refine 后恢复了可测的未来 observable。

这是最关键的科学场景。

#### 64.3 Expansion into Vacuum

证明：

- 强非平衡区域随时间移动；
- kinetic/free-molecular transition；
- 动态 region、moving interface 和成本收益。

B5 不能首次引入新物理；所有现象必须先在 B0–B4 被定量验证。

对应项目：[`B5 Graphics evidence`](../benchmarks/b5-graphics-evidence.md) 与 [`Demo strategy`](../demos/demo-strategy.md)。

---

## 20 周第一轮学习—实现计划

### 65. 总目标

20 周结束时，你不需要成为 Boltzmann 数学专家，但应该能够：

- 独立实现并验证小规模 2D EDMD；
- 独立解释并审查最小 DSMC；
- 从粒子计算 \(f\) 的矩；
- 区分 sampling、discretization、model discrepancy；
- 解释 molecular chaos、pair correlation、Enskog 和 collision history；
- 审核 B1/B2 dataset 是否泄漏；
- 理解 promotion/demotion 的守恒与信息损失；
- 参与 dynamic LOD policy 和 SIG claim 决策。

#### 65.1 第 1–4 周：硬球与 EDMD

| 周 | 理论 | 最小实践 | 项目连接 |
|---|---|---|---|
| 1 | 冲量、动量/能量、法向切向分解 | 二体正碰/斜碰 notebook | B0 collision primitive |
| 2 | 连续碰撞时间、墙面与周期边界 | quadratic event prediction | B0 event tests |
| 3 | priority queue、version invalidation | 10–100 hard disks EDMD | internal exact backend |
| 4 | 守恒、退化事件、DynamO oracle | 与外部 equilibrium case 对齐 | R0 DynamO |

#### 65.2 第 5–8 周：概率与相空间

| 周 | 理论 | 最小实践 | 项目连接 |
|---|---|---|---|
| 5 | 随机变量、PDF、均值、方差 | histogram sampling | stochastic evidence |
| 6 | 联合分布、独立性、covariance | 同边缘不同联合分布 | molecular chaos 入门 |
| 7 | phase space、\(f(x,v,t)\) | \((x,v)\) 点云与 bins | canonical kinetic state |
| 8 | moments、Maxwellian、free transport | 从粒子算 \(n,u,T,P,q\) | artifact/metric definitions |

#### 65.3 第 9–12 周：Boltzmann 与 DSMC

| 周 | 理论 | 最小实践 | 项目连接 |
|---|---|---|---|
| 9 | gain–loss、碰撞守恒、closure | discrete-velocity toy | Boltzmann intuition |
| 10 | DSMC move/bin/collide/sample | minimal 2D DSMC | internal kinetic backend |
| 11 | cell/dt/particle convergence | homogeneous relaxation | B0 DSMC envelope |
| 12 | SPARTA、Knudsen、uniGasFoam | external adapters smoke | R0 oracle/baseline |

#### 65.4 第 13–16 周：相关性与研究假设

| 周 | 理论 | 最小实践 | 项目连接 |
|---|---|---|---|
| 13 | \(g(r)\)、packing、Enskog | radial distribution sweep | finite-density attribution |
| 14 | collision graph、cycle、lineage | rolling graph reference | history feature pipeline |
| 15 | EDMD–DSMC paired discrepancy | canonical paired runs | B1 atlas |
| 16 | grouped split、matched states、ablation | incremental-value report | B2 Go/No-Go |

#### 65.5 第 17–20 周：转换与动态 LOD

| 周 | 理论 | 最小实践 | 项目连接 |
|---|---|---|---|
| 17 | demotion、moment correction | exact → weighted kinetic | B3 demotion |
| 18 | promotion、overlap、maturity | kinetic → hard disks | B3 promotion |
| 19 | interface、hysteresis、state machine | static then dynamic block | B4 LOD |
| 20 | shared renderer、cost-quality、口试 | diagnostic hero smoke | B5 preparation |

---

### 66. 每周 8–12 小时怎样分配

#### 2–3 小时：概念学习

只读当前任务需要的章节，不通读整本高级教材。

#### 2 小时：手推与单位检查

至少写一页：

- 公式来源；
- 符号定义；
- 单位；
- 极限情况；
- 一个具体数字例子。

#### 3–5 小时：最小代码

代码必须能单独运行、输出数值诊断、可被故意破坏。

#### 1–2 小时：复盘

回答：

- 哪个结论通过了？
- 误差条多大？
- 哪个假设仍未验证？
- 结果是否能被另一种解释说明？
- 哪段 AI 代码你还无法亲自解释？

---

## 与仓库 milestone 的对应关系

| 学习 Gate | 你能够承担的工作 | Repository milestone |
|---|---|---|
| L0 硬球力学 | 审核 collision/event tests | M2/B0 exact |
| L1 概率统计 | 审核 seed/CI/ensemble | 全部 stochastic suites |
| L2 相空间 | 定义 artifact 与 observables | M2–M3 |
| L3 DSMC | 审核 kinetic convergence | M1–M3 |
| L4 相关性/Enskog | 审核 history claim 边界 | M3–M4 |
| L5 实验设计 | 主持 B2 Go/No-Go | M4 |
| L6 conversion/LOD | 审核 B3/B4 算法 | M5–M6 |
| L7 graphics evidence | 冻结共享渲染证据 | M7/B5 |

详细 milestone 见 [`Roadmap`](../roadmap/milestones.md)。

---

## 项目负责人“口试”清单

### 67. Gate L0：硬球与 EDMD

你可以在白板上：

- 推出等质量弹性碰撞；
- 解释法向/切向分解；
- 写出碰撞时间二次方程；
- 解释 event invalidation；
- 设计能抓住鬼碰撞的测试。

### 68. Gate L1：概率

你可以解释：

- realization、ensemble、expectation；
- variance 与 standard error；
- joint distribution 与 independence；
- 为什么均值/温度相同仍可能不同；
- grouped split 为什么必要。

### 69. Gate L2：相空间与矩

你可以从 \(f\) 得到：

\[
n,u,T,P,q.
\]

并解释：

- 双峰分布；
- free transport；
- Maxwellian residual；
- normalization 与单位。

### 70. Gate L3：Boltzmann 与 DSMC

你可以解释：

- gain/loss；
- molecular chaos；
- DSMC 随机配对；
- cell/time/particle convergence；
- DSMC identity 为什么不是真实 history。

### 71. Gate L4：Correlation 与 Enskog

你可以区分：

- excluded-volume pair structure；
- non-Maxwellian state；
- dynamic collision history；
- Enskog correction；
- oracle-only 与 runtime feature。

### 72. Gate L5：研究证据

你可以设计：

- paired EDMD–kinetic runs；
- discrepancy metric；
- grouped/OOD split；
- matched-state pairs；
- incremental-value ablation；
- uncertainty report。

### 73. Gate L6：Conversion 与 dynamic LOD

你可以说明：

- demotion 丢了什么信息；
- promotion 为什么不唯一；
- 怎样保 \(M,P,E\)；
- history maturity；
- interface flux；
- hysteresis 与 budget。

### 74. Gate L7：SIG evidence

你可以回答：

- 每个 hero scene 支持哪条 claim；
- shared renderer 如何保证公平；
- 哪些画面只是 diagnostic，哪些是物理现象；
- 为什么不用普通 state-only adaptive method；
- 如果 B2 失败，应该如何转向。

---

## AI 可以做什么，你必须亲自掌握什么

### 75. 适合交给 AI 加速的工作

- 工程骨架；
- schema 与数据转换；
- 参数 sweep；
- 单元测试模板；
- plotting/dashboard；
- 外部 solver adapter；
- 文献初筛；
- 重复性脚本；
- baseline 代码移植；
- profiler 与日志整理。

### 76. 不能外包给 AI 的判断

#### 76.1 状态量语义

- 这个 \(f\) 是 number density 还是 probability density？
- simulation particle 的 weight 是什么？
- temperature 是哪个维度和单位？
- stress 是 kinetic part 还是含 collisional part？

#### 76.2 模型适用性

- 当前 density 还是 Boltzmann regime 吗？
- discrepancy 能否由 Enskog 解释？
- wall model 是否一致？
- EDMD 和 DSMC 是否真的表示同一物理参数？

#### 76.3 证据边界

- 误差是否超过采样/离散不确定性？
- feature 是否泄漏 oracle future？
- held-out case 是否真正独立？
- 预测收益是否转化为实际 Pareto 改善？

#### 76.4 论文 claim

- 实验实际证明了什么？
- 它没有证明什么？
- 与邓煜成果是概念启发、数值验证，还是严格推论？
- visual difference 是否来自 renderer 而非 physics？

---

## 每个 PR 合并前的审查模板

### 77. Model

1. 连续/离散模型是什么？
2. 状态变量、单位、normalization 是什么？
3. 边界条件和假设是什么？
4. 当前 case 在适用范围内吗？

### 78. Numerics

1. 时间怎样推进？
2. 空间怎样分区？
3. event/collision 怎样采样？
4. 稳定或收敛条件是什么？
5. random seed 与 weight 怎样处理？

### 79. Validation

1. 解析解或外部 oracle 是什么？
2. conservation error 是多少？
3. resolution/seed sweep 是否完成？
4. 故意破坏代码时 test 会失败吗？
5. artifact 是否记录 commit、config、seed 与 raw source？

### 80. Research integrity

1. 是否使用 oracle-only feature？
2. 是否把同一 run 泄漏到 train/test？
3. 是否控制 finite-density/Enskog explanation？
4. 是否只报告最好 seed/最好阈值？
5. failure case 是否保留？

---

## 暂时不要优先学习什么

在 M1–M4 以前，不要把主时间投入：

- 完整 Navier–Stokes 湍流理论；
- RANS、LES、\(k\)-\(\varepsilon\)；
- 可压缩激波高阶有限体积全套；
- 燃烧与化学反应 DSMC；
- 量子统计；
- 测度论概率完整体系；
- Boltzmann 方程严格解的全部泛函分析；
- 邓煜证明中的全部组合估计；
- 摩擦颗粒、jamming、force chains；
- 复杂分子势和长程相互作用；
- 全 GPU parallel EDMD；
- 电影级体积渲染和复杂资产。

这些都可能在未来有用，但不会解除当前最关键的瓶颈：

\[
\boxed{
\text{能否可信地比较 exact hard spheres 与 kinetic model，
并验证 history 的条件增量价值？}
}
\]

---

## 推荐材料怎样使用，而不是怎样囤积

### 81. 第一层：现在就用

#### 81.1 GAMES103 回看

优先回看：

- 质点/刚体碰撞；
- 时间积分；
- 空间加速结构；
- 约束和能量；
- 数值验证思维。

不要重新从第一讲完整刷一遍，只围绕 EDMD 所需知识回看。

#### 81.2 本科概率统计

目标章节：

- random variable；
- PDF/CDF；
- expectation/variance；
- joint/conditional distribution；
- covariance/correlation；
- law of large numbers；
- central limit theorem；
- confidence interval；
- bootstrap。

#### 81.3 热学/统计物理入门

只先学习：

- ideal gas microscopic picture；
- Maxwell velocity distribution；
- temperature and kinetic energy；
- mean free path；
- transport intuition。

#### 81.4 外部项目文档

- DynamO：理解 EDMD case、输出和事件模型；
- SPARTA：理解 DSMC 输入、cell、particle、sampling；
- uniGasFoam：理解现有 state/Knudsen-based hybrid baseline。

### 82. 第二层：进入 B1/B2 时用

- kinetic theory 教材中 Boltzmann equation、collision operator、H-theorem、moment equations；
- DSMC 专著中 collision sampling、cell/time criteria、variance reduction；
- Enskog theory 的入门章节；
- graph/streaming algorithms 的基础；
- statistical learning 中 grouped CV、calibration、OOD evaluation。

### 83. 第三层：论文方法稳定后再读

- BBGKY hierarchy；
- cumulants 与 propagation of chaos；
- Deng–Hani–Ma 的完整证明技术；
- fluctuating hydrodynamics；
- parallel/speculative EDMD；
- advanced rarefied-gas numerical analysis。

原论文应当作为研究边界和理论来源阅读，而不是第一本气体动理学教材。

---

## 核心术语小词典

| 术语 | 直观解释 |
|---|---|
| Hard sphere | 有有限半径、不可重叠、接触瞬时交换冲量的理想粒子 |
| EDMD | 不按固定帧推进，而直接跳到下一次碰撞事件的分子动力学 |
| Phase space | 同时包含位置和速度的状态空间 |
| Distribution \(f(x,v,t)\) | 某处各种速度粒子有多少的统计描述 |
| Moment | 对速度分布加权积分得到的密度、速度、温度等宏观量 |
| Maxwellian | 局部平衡理想气体的 Gaussian 型速度分布 |
| Mean free path | 粒子平均两次碰撞间飞行距离 |
| Knudsen number | 平均自由程与场景尺度之比 |
| Boltzmann equation | 自由输运 + 统计碰撞的 kinetic 方程 |
| Molecular chaos | 入射碰撞粒子近似按单粒子分布独立抽样 |
| DSMC | 用随机 simulation particles 和碰撞采样求 Boltzmann 型动力学 |
| Pair correlation \(g(r)\) | 知道一颗粒子后，另一颗在距离 \(r\) 出现概率相对独立分布的变化 |
| Enskog | 对有限尺寸、接触 pair structure 进行修正的 kinetic 理论族 |
| Cumulant | 去掉低阶独立乘积后剩下的真正连通相关部分 |
| Collision graph | 以粒子为点、碰撞为边记录近期交互网络 |
| Shadow probe | 在 coarse block 中短暂启动 exact micro-simulation 估计误差 |
| Demotion | exact particles 压缩为较便宜的 kinetic representation |
| Promotion | 从 kinetic state 生成有明确位置、速度和身份的 exact particles |
| Hysteresis | 使用不同升/降阈值避免表示频繁抖动 |
| Physics LOD | 由模型误差决定的物理表示细化 |
| Rendering LOD | 仅由屏幕/相机决定的显示细化 |

---

## 最后：你真正需要成为哪种“懂项目的人”

你不需要变成能够从头证明 Boltzmann–Grad limit 的数学家，才有资格推进项目。

你需要成为能够守住以下三条底线的人：

\[
\boxed{
\text{这个状态量到底表示什么？}
}
\]

\[
\boxed{
\text{这个数值差异为什么可信，而不是离散误差或随机噪声？}
}
\]

\[
\boxed{
\text{这个实验实际支持了哪条 claim，又没有支持什么？}
}
\]

当你依次打通：

```text
hard-sphere mechanics
→ EDMD
→ probability
→ phase-space distribution
→ Boltzmann/DSMC
→ pair correlation/Enskog/history
→ paired evidence
→ conversion/dynamic LOD
```

这个项目就不会再是一团由 AI 自动生成的黑箱。

你会开始真正看见：

- 为什么 R0 要先复现外部 oracle；
- 为什么 B0 要把 exact 和 kinetic 分开验证；
- 为什么 B1 必须先建 discrepancy atlas；
- 为什么 B2 是整条路线的生死门；
- 为什么 B3/B4 的守恒与 observability 比漂亮视频更重要；
- 为什么 B5 只是证据展示，而不是用画面掩盖失败假设。

这正是本仓库采用 benchmark-first 架构的原因。
