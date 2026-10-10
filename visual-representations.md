# 视觉编码器与表示分类：DINO、V-JEPA、I-JEPA、几何和语义 latent

## 1. 为什么要比较表示，而不是只比较 policy

机器人策略看到的并不是“真实状态”，而是相机图像、视频和 proprioception。视觉 encoder 决定了下游模型能否从输入中读出物体、几何、运动和任务相关状态。相同的 policy head 换一个 encoder，可能出现完全不同的长时域预测和控制结果。

## 2. 专有名词解释

- **Encoder：** 把图像/视频转换成 feature 或 token 的网络。
- **Latent representation：** 不直接显示给人的内部向量，包含输入中被模型保留的信息。
- **Patch feature：** 图像切成小块后，每个 patch 对应一个局部向量，保留空间布局。
- **DINO / DINOv2 / DINOv3：** 以自监督视觉表征为核心的 encoder family，通常擅长对象和视觉语义，但不必然编码动作后果。
- **I-JEPA：** 在图像空间中预测被遮挡区域的表示，强调抽象语义结构。
- **V-JEPA：** 将 JEPA 思路扩展到视频，预测时空上下文中的未来/缺失视觉表示。
- **冻结 encoder：** 训练 policy/world model 时不更新 encoder 参数；优点是稳定和省数据，缺点是可能与机器人控制目标不匹配。
- **End-to-end：** 从图像到动作的所有模块共同更新，适应性强，但更容易过拟合和遗忘预训练能力。

## 3. 逐篇比较

| 论文 | 表示路线 | 主要保留的信息 | 额外实验/指标 | 可视化 |
|---|---|---|---|---|
| [DINO-WM](papers/2411.04983-dino-wm.md) | 冻结 DINOv2 patch feature | 对象/场景语义与空间 patch | encoder 比较、latent quality、SSIM、LPIPS、planning success | planned trajectory、goal/final、latent rollout |
| [RLA-WM](papers/2605.07079-rla-wm.md) | DINO feature + residual latent action | 动作引起的 feature residual | feature prediction、planning、LIBERO VLA、real-world datasets；LPIPS/SSIM/DINO-L1/FLOPs | residual latent、质量/速度对比 |
| [ReWAM](papers/2609.38163-rewam.md) | 表示中心的 DINO/WAM 比较 | 控制相关 feature，避免无关生成细节 | DINOv3/V-JEPA 2 对比；bottleneck、gradient routing、RoboTwin/RoboDojo | representation bottleneck、梯度路由、分布偏移 |
| [V-JEPA 2](papers/2506.09985-v-jepa-2.md) | 大规模 action-free V-JEPA + V-JEPA 2-AC | 视频时序、动作后果和视觉语义 | Something-Something、EK100、Video QA、机器人 goal-image planning | latent decoding、counterfactual、camera sensitivity |
| [V-JEPA Policy](papers/2609.37250-vjepa-policy.md) | 冻结 V-JEPA 2.1 predictive latent | 未来视觉状态与任务相关运动 | LIBERO、LIBERO-Plus、RoboCasa、DROID transfer、真机 shift | future latent、视觉基础模型比较 |
| [RoboJEPA](papers/2610.10515-robojepa.md) | V-JEPA 2.1 + multi-view/embodiment tokens | 多视角、proprioception、跨 embodiment 状态 | 12 embodiment scaling；imagination error；规划相关性；真机 zero-shot | scaling curve、rollout、imagination-error correlation |
| [Reconstruction or Semantics?](papers/2605.06388-reconstruction-or-semantics.md) | reconstruction latent 与 semantic latent 对照 | 像素细节、语义状态和控制相关信息的取舍 | fixed transition protocol、ID/OOD、bootstrap CI、VLM judge、policy performance | encoder ceiling、OOD rollout、probe |
| [VO-DP](papers/2510.15530-vo-dp-feature-fusion.md) | DINOv2 semantic + VGGT geometric | 物体语义、空间几何和场景压缩表示 | RoboTwin、真实四任务；size/appearance/background/illumination robustness | semantic-geometric fusion、VGGT/DINOv2 features |
| [ACG-WAM](papers/2610.06965-acg-wam.md) | geometric JEPA latent | action 后的空间几何变化 | RoboTwin clean/randomized；真机 success/partial completion | geometry latent、多 horizon prediction |

## 4. 一样的地方

- **表示都不是最终动作。** encoder 只能提供接口，必须通过 predictor、planner 或 policy 证明这些信息对控制有用。
- **都面临信息取舍。** 保留更多像素细节可能增加计算和预测难度；过度压缩则可能丢失接触、遮挡和几何信息。
- **冻结与微调是关键变量。** 冻结更适合小数据和可复用研究，微调可能提高任务适配但降低跨任务泛化。
- **probe 只能证明可读性。** 线性 probe 能从 latent 恢复状态，不代表控制器会使用这部分信息。

## 5. 不一样的地方

### DINO 类：静态语义接口

DINO 特征通常提供对象和场景结构，适合 goal matching、feature prediction 和表示对照。但单独的 DINO 表示没有 action-conditioned temporal prior，需要额外的 world model 学动作后果。

### V-JEPA 类：时序预测接口

V-JEPA 直接从视频预测视觉表示，更自然地携带 motion 和 future 信息。V-JEPA 2 的 action-free 预训练与 V-JEPA 2-AC 的机器人动作适配应分开评价。

### I-JEPA 类：图像抽象和状态接口

I-JEPA 更强调在抽象表示空间预测图像上下文；在 LeWAM-IJEPA 等路线中，它被进一步接到 world-action model，需要额外验证是否具备动作可控性。

### 几何/语义融合

VO-DP 和 ACG-WAM 说明语义表示和几何表示并非二选一：语义回答“是什么/目标是什么”，几何回答“在哪里/动作后会怎样”。真正的难点是融合后是否改善 action success，而不是融合图看起来更复杂。

## 6. 指标和实验解释

- **DINO-L1：** feature 之间的 L1 距离，衡量预测表示差异。
- **LPIPS/SSIM：** 图像感知/结构相似度，适合衡量视觉重建，不应单独作为控制质量。
- **Imagination error：** world model rollout 与真实未来表示的偏差；越小通常越好，但要看 horizon。
- **Encoder ceiling：** 用理想或 oracle 表示估计下游模型的上限，帮助区分 encoder 瓶颈和 policy 瓶颈。
- **OOD：** 更换物体、颜色、背景、光照、相机、布局、语言或 embodiment 后的测试。
- **Bootstrap CI：** 通过重采样估计置信区间，帮助判断 success 差异是否可能只是样本波动。

## 7. 可视化详解

1. **Feature map / patch correlation：** 检查不同 patch 是否关注物体、手和接触区域；相关性过高可能表示空间信息被压平。
2. **Latent decoding：** 把 latent 解码回图像或可视化轨迹，帮助人理解模型保留了什么；解码效果差不等于控制差。
3. **PCA/UMAP：** 把高维 latent 投到二维，看时间、目标、动作或任务是否形成结构；它是探索工具，不是严格性能指标。
4. **Linear probe：** 冻结 latent，只训练一个线性读出器预测位置、物体或状态；用于测试信息是否存在。
5. **Counterfactual prediction：** 固定当前观测，改变“打开/关闭夹爪”等动作条件，看预测未来是否发生合理变化。
6. **Geometry rollout：** 查看未来几何 slot 是否随抓取、移动、接触而变化，特别适合 ACG-WAM 一类方法。

## 8. 对 OpenWAM 的建议

比较 encoder 时不要只报一个总 success。建议固定同一 action head，至少报告：

1. 单步 feature prediction error；
2. 多步 imagination error；
3. state/object linear probe；
4. distractor/OOD 下的 feature stability；
5. 最终 action success 与 latency。

