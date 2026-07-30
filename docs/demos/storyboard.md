# Storyboard and Shot Grammar

> 本文件定义最终视频的叙事结构和 shot IDs。具体相机参数由 `configs/render/scenes/*.yml` 冻结。

---

## 1. 总体视频结构

### Teaser：30–45 秒

目标不是解释全部算法，而是留下一个清晰记忆点：

> 同一个大尺度稀薄气体场景中，只有局部区域保留真实硬球身份与碰撞历史；表示边界随物理误差移动，而不是随相机移动。

建议结构：

```text
0–5 s   Expansion into Vacuum 全景，plume 形成
5–12 s  沿 plume 推进，volume 过渡到 particles
12–19 s exact/kinetic boundary 与真实 collision identities
19–27 s state-only vs proposed vs reference 三联对比
27–35 s Correlation Labyrinth matched-state freeze frame
35–45 s cost–quality / exact fraction + title
```

### Main video：3–5 分钟

1. 研究问题；
2. exact 与 kinetic 表示；
3. collision history indicator；
4. conversion；
5. dynamic LOD；
6. 三场景结果；
7. performance、limitations、failure cases。

---

## 2. 通用 shot grammar

每个 result 段落遵循：

```text
Context → Failure → Trigger → Representation → Recovered physics → Cost
```

每个 shot 只承担一个主要问题。若一个镜头需要同时解释三个新概念，就拆开。

---

## 3. Zoomable Mixing Chamber

### ZM-01 — Macro context

- 远景；
- 两种 species 被 divider 分开；
- 只显示 volume/species concentration；
- divider 打开；
- 不显示 mask。

**问题：**场景是什么？

### ZM-02 — Shared state

- 固定相机；
- volume 与 statistical display particles 做平滑混合；
- 显示 display policy legend。

**问题：**宏观体积和微观显示来自同一状态吗？

### ZM-03 — Exact identity reveal

- 相机进入一个已经由 physics policy 选中的 exact block；
- exact particles 保持 identity；
- 短 collision trails；
- 屏幕边角显示“camera does not trigger promotion”。

**问题：**真实粒子身份在哪里被保留？

### ZM-04 — Conversion continuity

- freeze camera；
- 显示 conversion timeline；
- 画 volume integral、species mass、M/P/E error；
- 在同一时刻比较有/无 warm-up 或 naive baseline。

**问题：**conversion 是否 popping，是否守恒？

### ZM-05 — Zoom audit

- 相机往返 zoom；
- 并排显示 physics partition 与 display LOD；
- physics mask 保持不受相机影响。

**问题：**visual zoom 是否和 physical refinement 解耦？

---

## 4. Correlation Labyrinth

### CL-01 — Geometry and flow

- 俯视或轻透视；
- 显示两个设计为 local state 相近的 chamber；
- tracer 展示不同 re-encounter topology。

### CL-02 — State-only ambiguity

- freeze frame；
- 框选 matched block A/B；
- 显示 density、temperature、stress、Knudsen 等 state features；
- 数值接近。

**问题：**传统局部状态为什么难区分？

### CL-03 — History difference

- 同一两个 block；
- 显示 rolling collision graph；
- repeated pair、cycle rank、lineage/re-merging；
- 图形只在 inset 中显示。

**问题：**历史结构有什么不同？

### CL-04 — Future discrepancy

- 从相同当前时刻向前播放 declared horizon；
- full EDMD reference 与 kinetic prediction 并排；
- 显示 future observable error。

**问题：**history difference 是否对应真正的未来误差？

### CL-05 — Policy comparison

四列或两组切换：

```text
state-only | practical history/probe | oracle upper bound | reference
```

显示 partition 与 recovered observable。

### CL-06 — Held-out evidence

- 不再展示训练场景；
- 显示 held-out geometry/regime；
- 小型 calibration/recall plot；
- 强调 operational improvement，而不是单纯 ML score。

---

## 5. Expansion into Vacuum

### EV-01 — Establishing shot

- 透明 chamber + aperture + low-density exterior；
- 气体释放；
- plume silhouette 清楚；
- 不显示 diagnostics。

### EV-02 — Method-neutral comparison

- 固定相机和 transfer function；
- full kinetic、state-only LOD、proposed、reference；
- 优先显示 plume angle、density ridge、species front 或 declared observable。

### EV-03 — Moving refinement front

- proposed 单画面；
- exact boundary 用轻轮廓或粒子形态显示；
- probe blocks 用小边框；
- mask 作为小地图，而非覆盖 plume。

### EV-04 — Macro-to-micro travel

- 相机沿 plume 推进；
- volume → statistical display particles → exact identities；
- camera 不改变 physics mask；
- exact particles 显示真实 collision event。

### EV-05 — Why state-only fails

- 选择一个 transitional block；
- 显示 state-only score 与 history/probe score；
- 对应 velocity distribution 或 escape probability；
- 未来误差对比。

### EV-06 — Cost–quality result

- 同一镜头背景；
- 右侧显示 Pareto curve；
- 标出 full EDMD、full kinetic、state-only、proposed；
- 同时显示平均 exact fraction 和 wall-clock/memory。

### EV-07 — Failure indicator

- 展示一个 policy 不确定或 coarse backend 不适用的区域；
- 方法明确标记并回退，而不是隐藏失败。

---

## 6. Figures and contact sheets

每个主图对应固定 shot：

| Figure concept | Shot source |
|---|---|
| Teaser / first page | EV-01 + EV-04 composite, shared artifact time |
| Representation overview | ZM-02/03/05 |
| History adds value | CL-02/03/04 |
| Policy comparison | CL-05 or EV-02/03 |
| Conversion continuity | ZM-04 |
| Dynamic Pareto | EV-06 |
| Limitations | EV-07 + supplementary failure reel |

Composite figure 必须在 recipe 中列出每个 panel 的 run ID、time、camera hash 和 renderer config hash。

---

## 7. Voice-over rule

不要说：

> “红色区域更复杂，所以我们切到 EDMD。”

要说：

> “这两个区域的局部密度、温度和 Knudsen 指标接近，但过去一个窗口内的碰撞重遇结构不同。右侧区域在未来 horizon 中出现更大的 kinetic discrepancy，因此 practical probe policy 只在这里保留 exact dynamics。”

视频语言必须与 claim ledger 一样严格。
