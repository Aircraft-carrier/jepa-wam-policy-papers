# 论文分类阅读入口

这组文档不是简单按关键词分组，而是按“论文到底在哪个环节增加了能力”来组织：

| 分类 | 主要问题 | 文档 |
|---|---|---|
| 规划器：MPC / CEM / DS-CEM | 模型预测出未来以后，怎样搜索下一步动作？ | [planning-mpc-cem.md](planning-mpc-cem.md) |
| 直接动作策略与 WAM / VLA | 模型怎样从观测、语言和未来 latent 直接生成 action chunk？ | [direct-action-policies.md](direct-action-policies.md) |
| 视觉编码器与表示学习 | DINO、V-JEPA、I-JEPA、几何/语义表示分别保留了什么？ | [visual-representations.md](visual-representations.md) |
| 预测式 latent world model | 怎样训练 action-conditioned future predictor，以及预测结果如何服务 policy？ | [predictive-world-models.md](predictive-world-models.md) |
| 评测、泛化与可视化 | 应该怎样读 success、progress、OOD、probe、rollout 和结构图？ | [evaluation-and-visualization.md](evaluation-and-visualization.md) |

## 推荐阅读顺序

1. 先读 [visual-representations.md](visual-representations.md)，建立 encoder、latent 和 patch/token 的概念。
2. 再读 [predictive-world-models.md](predictive-world-models.md)，理解“预测未来状态”与“生成像素”的区别。
3. 接着读 [planning-mpc-cem.md](planning-mpc-cem.md) 或 [direct-action-policies.md](direct-action-policies.md)，看预测结果如何转成动作。
4. 最后读 [evaluation-and-visualization.md](evaluation-and-visualization.md)，避免把不同指标和实验协议混在一起。

## 一句话总图

```text
图像/视频/语言
      ↓
视觉 encoder：DINO / V-JEPA / I-JEPA / 几何-语义融合
      ↓
latent state：压缩但保留控制相关的信息
      ↓
action-conditioned predictor：预测动作后的未来 latent
      ├── MPC / CEM / DS-CEM：搜索动作，再执行第一段
      └── policy / WAM / VLA：直接生成 action chunk
      ↓
机器人执行 → 获得新观测 → 闭环重复
```

