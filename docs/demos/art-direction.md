# Art Direction and Visual Language

> 目的：让最终画面既像一篇高质量 SIGGRAPH/TOG 工作，又不牺牲科学可读性和 method fairness。

本项目不追求“把所有数据都画出来”，而是建立一套层次清楚的视觉语法：

1. **主画面先显示物理现象；**
2. **representation 与 diagnostics 只在需要解释时出现；**
3. **species、representation、error 三类信息不能抢用同一种颜色编码；**
4. **neutral comparison 与 hero render 必须来自同一 artifact。**

---

## 1. 两种正式视觉模式

## Scientific comparison mode

用于论文主对比和 supplementary：

- 中性背景；
- 固定相机；
- 固定 transfer function；
- 最少后处理；
- 同一 method group 严格锁定；
- diagnostics 可见；
- 允许 difference view 和 plots。

## Hero mode

用于 teaser、首页图和讲解：

- 可以使用更有层次的灯光；
- 可以使用共享 motion blur、depth cue 和 tone mapping；
- 可以重新构图，但不得改变 artifact、frame time 和 display sampling semantics；
- 不能用 hero mode 代替 primary comparison evidence。

每个重要现象必须先在 scientific mode 中成立，再进入 hero mode。

---

## 2. 信息编码分工

### Species 用 fill hue

建议默认：

- species A：coral/red family；
- species B：blue/cyan family；
- single-species gas：neutral pale gray/blue。

不要用 representation 颜色覆盖 species 颜色，否则观众无法同时判断“这是什么气体”和“它属于哪种表示”。

### Representation 用形态与轮廓

- **Exact particle**：清晰实体球、稳定 identity、薄高光边缘；
- **Statistical display particle**：更小、更透明、轻微 soft sprite/point-like appearance；
- **Shadow probe region**：空间 block 的细边框或局部 hatch，不改变粒子颜色；
- **Kinetic volume**：连续体积，不与 exact particle 重复累加亮度；
- **Unresolved/invalid**：只在 diagnostic mode 中用灰色警告纹理。

### Error 用独立的 diverging map

误差图不复用 species hue。建议只在 inset、difference view 或 surface strip 中使用 blue–neutral–orange 的 diverging map，并标明 zero/reference。

### History 用线和拓扑

- collision edge：短寿命、细线；
- repeated pair：线宽或 pulse 强调；
- connected component：局部轮廓；
- cycle/re-merging：只在 diagnostic inset 中突出；
- 不在 hero 主画面画出全部 collision graph，避免变成线团。

---

## 3. 背景、几何与材质

### 默认背景

- near-black neutral background；
- 不使用纯黑，以保留透明体积阴影层次；
- 科学模式保持固定；
- hero 模式可以加入非常弱的环境渐变，但不得改变 method 对比可见性。

### 容器与障碍物

- 使用薄、低饱和度、半透明或 cutaway geometry；
- 边界轮廓要清楚，但不能遮挡内部 plume；
- 几何材质不使用复杂纹理；
- moving wall/plate 用简单高反差边缘表达运动；
- 所有 primary scenes 优先使用 box、rounded chamber、channel、plate、nozzle 等 primitives。

### 粒子尺寸

必须区分：

- physical diameter；
- display radius scale。

Primary comparison 中 display radius scale 必须锁定。若为了可见性放大粒子，manifest 必须记录比例，并且所有方法一致。

---

## 4. Volume 与 particles 的组合

宏观体积和微观粒子不能简单相加，否则同一质量会被视觉上重复显示。

建议的过渡策略：

- 远景：volume 主导，particles 稀疏；
- 中景：volume opacity 下降，statistical display particles 增加；
- 近景 exact region：exact particles 主导，局部 volume 作为低频背景；
- 过渡权重由 display policy 和 screen-space coverage 决定，不改变物理状态。

同一 block 的显示权重满足概念上的 partition of unity：

\[
w_{\text{volume}}+w_{\text{display particles}}+w_{\text{exact particles}}\approx1,
\]

避免亮度突然翻倍。

---

## 5. Motion blur 与速度表达

- scientific mode 默认关闭或使用非常短、共享的 shutter；
- hero mode 可使用共享 motion blur；
- exact particle trail 只能由真实 identity 轨迹生成；
- statistical display particle 不得伪装成真实长期 identity；
- 若用 velocity streak 表达 kinetic distribution，应标注为 display glyph，而非分子轨迹。

---

## 6. Overlay 层级

Primary hero shot 最多同时保留：

1. 主物理画面；
2. 一个小型 representation mask 或 score strip；
3. 一个关键数字，如 error/exact fraction/speedup。

更多信息放在：

- 四 panel comparison；
- freeze-frame annotation；
- velocity-space inset；
- supplementary diagnostics。

不要在一个镜头中同时显示 partition、collision graph、velocity histogram、g(r)、error heatmap、性能曲线和字幕。

---

## 7. 字体、图例与排版

- 统一无衬线字体；
- 统一 method short names；
- 所有单位显式；
- 图例位置在 comparison group 内锁定；
- 数值采用固定有效位数；
- exact / kinetic / probe 的图例必须解释“物理表示”与“显示采样”的区别；
- 不用“ground truth”描述未收敛或降尺度 full EDMD，使用 declared reference。

---

## 8. 三个场景的视觉身份

### Zoomable Mixing Chamber

关键词：**清楚、教学、连续**。

- 红蓝 species；
- 简洁透明箱体；
- 平滑 zoom；
- conversion timeline；
- 微观 identity 与宏观 concentration 对齐。

### Correlation Labyrinth

关键词：**结构、对照、因果**。

- geometry 使用浅灰迷宫；
- matched blocks 用统一框选；
- 主画面保持简洁；
- history graph 与 future error 在 freeze-frame inset 中出现；
- state-only 与 history-aware mask 用并排小图而非覆盖主画面。

### Expansion into Vacuum

关键词：**尺度、方向、动态**。

- plume silhouette 是主角；
- chamber/nozzle 保持简洁；
- species 或 speed 使用单一明确编码；
- exact front 用轮廓/粒子形态表达，不用大面积荧光 mask；
- 相机沿 plume 方向推进，展示 macro → micro。

---

## 9. 禁止的视觉捷径

- proposed method 使用更高 particle display density；
- baseline 使用更透明或更暗的 transfer function；
- 只为 proposed method 使用 temporal denoising；
- 删除 baseline 中的 outlier particle；
- 只展示最有利的 seed 而不报告选择规则；
- 在 hero render 中加入 solver 没有输出的“补充涡流/噪声”；
- 用 representation mask 本身冒充物理改善；
- 用镜头移动触发 physics promotion；
- 对不同方法使用不同的 frame time。

---

## 10. Art review checklist

每次视觉评审先关闭所有 diagnostics，只看 final render：

- 物理差异是否仍然可见？
- 画面是否有唯一视觉焦点？
- species 与 representation 是否能同时读懂？
- volume/particle 过渡是否亮度守恒？
- 是否有 popping、boiling、闪烁或 mask chatter？

再打开 diagnostics：

- 它们是否解释了主画面，而不是制造第二套故事？
- 每个颜色和线型是否只有一个含义？
- 是否能追溯到 metric 和 run ID？
