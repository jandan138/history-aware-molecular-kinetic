# Molecular-echo first stage

**状态：** 拟定的主研究阶段。

**阶段目标：** 用一个周期性二维硬圆盘实验决定论文能否成立：

> 在相同可分辨单粒子状态下，反向支路与经过分子混沌手术的支路走向不同未来；有限的
> \((\Lambda,\Gamma)\) 碰撞分子预算以不同方式影响正向热化与反向回声。

完整的科学叙事、定义和主张边界见
[Collision-History Echoes](../research/collision-history-echo-route.md)。

## 交付物

| 交付物 | 内容 | 通过标准 |
|---|---|---|
| E1：事件账本 | 每个碰撞的时间、法向、入射相对速度、时间层、组件根、多重边和递碰撞秩 | 可由种子、初态和日志重建统计量；重复 pair 事件不丢失 |
| E2：回声协议 | 周期边界、非平衡准备、枢轴反演、block+color shuffle、\(f_{1,h}\) 审计 | 反向与 shuffle 分支在登记分辨率上匹配 |
| E3：最小 T-dynamics | full、\((8,0)\)、\((16,1)\)（必要时 \((4,0)\)） | 抑制规则、ghost 语义和事件排序可回放、可测试 |
| E4：闭合读出 | 各向异性/颜色观测量及 incoming-pair cumulant proxy | 读出定义独立于事后挑选的视觉效果 |
| E5：故事决定图 | 正向、exact reverse、chaotized reverse 在多个 \(N\) 下的轨迹与预算曲线 | 一张图可看出“same present, opposite futures, different budget” |

## 实现顺序

1. **锁定状态与审计。** 先定义周期盒、\(T_x/T_y\)、颜色、枢轴时刻、空间块和速度 bin；
   将 \(f_{1,h}\) 的 total-variation/计数差及一阶、二阶矩写入 manifest。这里的匹配标准
   先于图像和结果存在。
2. **扩展碰撞账本。** 事件图必须是带时间戳的多重图；不能只保留第一次接触或
   unique_pair_count。记录支持构造每个候选碰撞进入的分子、根及秩。
3. **完成 exact echo 与 chaos intervention。** 使用完全相同的初态、种子和观测时间；
   shuffle 只在登记的 \((\text{block},\text{color})\) 单元内置换速度，且保留全部
   \(f_{1,h}\) 审计。
4. **加入最小 T-dynamics。** 对超出预算的碰撞明确应用 ghost/穿越语义。该动力学允许
   后续几何重叠，因此不能复用“EDMD 永不重叠”的隐含不变量；要实现适用于扩展动力学的
   后续事件处理与单独的有效性测试。
5. **读取 \(d_\psi\) 并扩展 \(N\)。** 在 \(N=128,256\) 先稳定后，固定
   \(N\varepsilon=\alpha\) 做小型 Boltzmann–Grad 序列；不因结果好看而中途改观测窗或
   容限。

## 决策门

阶段结束时只回答三个问题：

| 问题 | 继续条件 | 失败时的动作 |
|---|---|---|
| same-present 是否成立？ | reverse 与 chaotized reverse 的 \(f_{1,h}\) 审计通过，并有稳定未来分离 | 修订状态分辨率或 shuffle；不添加更多指标掩盖不匹配 |
| 分子预算是否是机制？ | 预算曲线对 reverse 与 forward 呈可解释的差异，且与 incoming-pair 缺陷同向 | 停止 T-dynamics 主张，保留回声为演示而不写机制论文 |
| 是否有极限故事？ | 小型 BG 序列未破坏上述差异，并给出可报告的预算趋势 | 将工作收敛为有限系统 correlation/echo 实验，不声称 kinetic-limit 信息边界 |

## 非目标

本阶段不交付动态 LOD、EDMD↔DSMC 双向转换、误差预测网络、广泛几何泛化、
Enskog 归因、GPU 性能或完整视觉产品。它们属于已降级的工程路线，不能占用验证
“回声—手术—预算”因果链的时间。

## 最小测试矩阵

| 维度 | 固定选择 |
|---|---|
| 边界 | 单一二维周期盒 |
| 初始态 | 单一偶对称强各向异性速度分布，带被动颜色 |
| 支路 | forward、exact reverse、chaotized reverse |
| 动力学 | full、\((8,0)\)、\((16,1)\)，按需 \((4,0)\) |
| 尺度 | 先 \(N=128,256\)，后一个固定 \(N\varepsilon\) 序列 |
| 主读出 | \(\langle v_x^2-v_y^2\rangle\)、颜色模式、incoming-pair defect proxy |

这不是“缺少实验”，而是把实验数限制在论文叙事真正需要的反事实比较上。
