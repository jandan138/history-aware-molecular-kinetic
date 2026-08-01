# Art Direction and Visual Language — Molecular Echoes

> 目的：让最终画面像一篇高质量 SIGGRAPH 工作，同时避免把物理 branch、被动颜色、方法标签和因果图混成一团。

## 1. 视觉层级

1. **先看粒子运动和未来差异；**
2. **再看 selected event 与 causal cone；**
3. **最后用 graph、audit 和曲线解释原因；**
4. neutral comparison 与 hero render 必须来自同一 branch artifacts。

## 2. 三类信息必须分开编码

### Passive physical color

用于最初图案、物种或 tracer。它属于物理状态，不能因 branch/method 改变调色。

建议使用两到三种高区分、色盲友好的饱和色，并保持亮度接近，避免某 branch 因颜色更亮显得恢复更好。

### Branch identity

不要重染粒子。使用：

- panel placement；
- border/background accent；
- stable branch label；
- branch-tree glyph；
- caption。

固定身份：

```text
original
exact reverse
chaotized
DSMC
history budget
local counterfactual
full-resimulation reference
```

### Causal/history information

使用短时、局部、克制的编码：

- selected collision：高亮 pulse/ring；
- direct descendants：短 trail；
- affected set：细轮廓或轻透明 halo；
- molecule membership：临时 hull/outline；
- graph：linked inset，而不是覆盖整个粒子画面；
- invalidated old events：graph 中去饱和，不从 evidence 中删除。

## 3. Molecular Logo Echo 风格

- 背景尽量简单；
- 透明或弱可见边界；
- 图案由 passive color 形成，不使用额外约束力维持；
- pivot 时不靠 blur 让两个 state 看起来一样；
- exact/chaotized/DSMC 使用相同 display policy；
- history-budget slider 显示预算文字和 collision count，避免误导。

首页图应在单帧中表达：

```text
same resolved pivot
→ exact future recovers
→ chaotized future does not
```

## 4. One Collision, Two Worlds 风格

- selected event 在过去 timeline 中清晰定位；
- fork moment 使用短暂分裂动画，而不是大爆炸；
- causal cone 作为一条逐渐生长的影响结构；
- original/local/full-reference 三列必须易对应；
- difference panel 只用于 correctness，不替代主画面；
- branch tree 保持稳定 layout。

## 5. Choose the Cause 风格

- 未来 target 用清晰但克制的框选和粒子 outline 表达；
- 过去 timeline 只突出三条推荐碰撞，不显示全图 hairball；
- 角度 palette 看起来像创作控制，而不是参数扫表；
- original 与 directed future 保持同一材质、相机和 particle density；
- cached exact preview 与最终 full-reference confirmation 需要清楚区分；
- 性能数字保持次要，不遮挡“未来选目标、过去找原因”的阅读顺序。

## 6. Graph visual design

事件 graph 不是普通 force-directed hairball。

推荐：

- 横轴表示时间；
- 纵向按 particle lane、molecule 或 compressed component 排列；
- selected causal cone 局部展开；
- 远处历史聚合；
- repeated events 保持可见；
- branch fork 使用共享 trunk + child lanes。

若规模过大，主画面只显示局部 cone，完整 graph 放在 linked analytics view 或 supplementary。

## 7. Neutral versus Hero

### Neutral render

用于判断 claim：

- 简单光照；
- 无景深；
- 无 branch-specific motion blur；
- 无镜头抖动；
- 无额外粒子；
- 可检查每个 event/particle。

### Hero render

允许：

- 更好的灯光和环境；
- bounded motion blur；
- 透明材质；
- cinematic camera；
- composited labels/insets。

不允许：

- 为 exact branch 添加更多粒子；
- 只平滑 proposed branch；
- 删除难看的冲突/失败粒子；
- 改变 branch 时间使其更像 reference；
- 用倒放帧替代模拟 reverse；
- 手工重建 logo。

## 8. Camera grammar

- ME：固定/对称镜头，避免 perspective 造成 pivot mismatch；
- TW：先近看 selected collision，再拉到 causal spread；
- EP：清晰显示 past edit、recomputed region 和最终结果；
- camera navigation 不得改变 physics branch 或 cone。

## 9. Text and annotation

画面上的方法词保持最少：

```text
Resolved pivot match
Exact reverse
Correlation surgery
Causal branch
Full resimulation
Fallback: global cone
```

复杂公式和完整统计放在 paper/supplementary，不在 teaser 屏幕堆满。

## 10. Failure presentation

失败案例与成功案例使用相同视觉质量：

- reverse divergence；
- fine-resolution pivot mismatch；
- count-matched control explains effect；
- causal cone becomes global；
- surgery visibly changes present；
- local branch falls back。

Failure reel 不是 debug dump，而是论文适用范围的一部分。
