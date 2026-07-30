# Hero Scene Specifications

每个 Hero Scene 都有独立规范，避免“做视频时再临时决定场景”。

- [Zoomable Mixing Chamber](zoomable-mixing.md)
- [Correlation Labyrinth](correlation-labyrinth.md)
- [Expansion into Vacuum](expansion-into-vacuum.md)

每份规范固定：

- 论文职责；
- primitive geometry budget；
- required methods；
- frozen artifacts；
- primary observables；
- shot IDs；
- render config；
- visual acceptance；
- failure cases；
- stop conditions。

场景可以在 candidate 阶段调整；进入 frozen B5 case 后，任何改变物理语义的修改都必须创建新 case version。
