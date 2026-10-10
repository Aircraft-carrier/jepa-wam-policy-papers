# 评测与可视化分类：怎样正确比较这些论文

## 1. 为什么同一个“成功率”不能直接横比

论文可能都写 success rate，但实际含义可能完全不同：仿真还是实机、每个任务多少 episode、是否允许重试、是 binary success 还是 normalized progress、是否使用目标环境数据、是否汇报 best checkpoint。比较之前必须先对齐 protocol。

## 2. 指标词典

### 控制指标

- **Success rate（SR）：** 完成任务的 episode 比例。必须记录分母，例如 20 trials、50 episodes/task。
- **Partial completion：** 任务部分完成比例，适合有阶段性进度的 manipulation；不能当作 full success。
- **Task progress：** 连续进度分数，例如完成折叠、搬运或整理的百分比；不同论文的归一化方法可能不同。
- **Goal reaching：** 是否到达目标状态，常见于导航和 image-goal planning。

### 表征/预测指标

- **SSIM：** 结构相似度，偏向图像局部结构。
- **LPIPS：** 深层感知距离，越小通常表示视觉感知上越接近。
- **DINO-L1：** DINO feature 的 L1 距离，用于表示层比较。
- **R² probe：** 线性 probe 能解释多少真实状态变化；高 R² 说明信息可读，不说明 policy 充分利用。
- **Imagination error：** 多步预测 latent 与真实 latent 的差异。

### 泛化指标

- **ID：** 训练分布内。
- **OOD-S：** scene/spatial shift，如新布局、相机、初始位置。
- **OOD-I：** instruction shift，如表达方式、任务指令改变。
- **Visual shift：** 颜色、纹理、背景、光照、噪声变化。
- **Embodiment shift：** 换机器人、关节配置、相机或身体形态。

### 统计与效率指标

- **Seed：** 独立训练随机种子；3 或 5 seeds 比单次 best result 更可信。
- **Confidence interval：** 对 success 不确定性的估计；bootstrap CI 常用于 episode 数有限时。
- **Latency：** 单次 forward、完整 action generation 或 planner loop 的时间，三者不要混为一谈。
- **FLOPs：** 浮点运算量，反映计算规模，但不等于真实 wall-clock latency。

## 3. 逐篇“多做了什么实验”

| 论文 | 额外实验 | 重点指标/问题 |
|---|---|---|
| DINO-WM | encoder、causal mask、decoder loss、数据规模、unseen configuration | latent quality、SSIM、LPIPS、goal success、planning time |
| V-JEPA 2 | 视频 understanding、action anticipation、Video QA、counterfactual、两实验室真机 | top-1、recall@5、QA accuracy、robot success |
| JEPA-WAM Joint | temporal-gap、patch correlation、trajectory residual、latency、ID/OOD | future representation、RoboTwin clean/random、真机 rollouts |
| JEPA-WAM Visual Instruction | visual bank 数量/构造、J-1024 vs KF-64、scene/instruction OOD | ID 87.3%、OOD-S 74.5%、OOD-I 80.9% |
| JEPA Policy | action-only、Diffusion Policy、future error ranking、collapse audit、训练/真机 | 平均 83.0%、77.4%、75.1%、630 real episodes |
| V-JEPA Policy | visual foundation model、predictor pretraining、DROID transfer、7 类 shift | LIBERO、LIBERO-Plus、RoboCasa、Marvin 20 trials |
| LeWAM | planner、linear probe、distractor、noise-space proposal、5 seeds | state R²、policy/DS-CEM success、250 rollouts |
| RoboJEPA | 12 embodiment scaling、teacher forcing vs rollout、planning correlation、真机 | imagination error、compute power law、goal-image planning |
| ACG-WAM | clean/randomized RoboTwin、几何 horizon、teacher/auxiliary removal、真机 | 93.46%、92.68%、85.00% success、91.67% partial |
| PLaW-VLA | future mask、horizon、world-model ablation、zero-shot objects、latency | +11.8 pp、72.7%、约 1/19 latency |
| RLA-WM | residual 表示、visual RL、planning、质量-速度对照 | LPIPS、SSIM、DINO-L1、FLOPs、policy improvement |
| VO-DP | semantic/geometric fusion、size、appearance、background、illumination robustness | RoboTwin、真实四任务、robustness success |
| HiPolicy | frequency、entropy threshold、multi-sampling、长时域和真机 | RoboTwin 24 tasks、100 episodes/task、8×10 real trials |
| Reconstruction or Semantics | fixed transition、encoder ceiling、ID/OOD、VLM judge、bootstrap CI | rollout quality、semantic score、policy success、CI |
| ReWAM | DINOv3/V-JEPA 2 comparison、bottleneck、gradient routing、distribution shift | representation/control metrics、RoboTwin/RoboDojo |
| LeWAM-IJEPA | prediction/policy/demo preference ablations、probe、rollout | policy/planning/progress；部分逐项指标待核对 |
| DUET-DINO | cross-view、encoder、action-conditioned rollout、view shift | Reach 92%、Angled Reach 72.5%、Lift 60.0% |
| GIFT | geometry、affordance、goal-region、injection/no-injection、LIBERO-Plus shifts | LIBERO/LIBERO-Plus/RoboCasa；真机协议待核 |

## 4. 相同指标应该怎样比较

### Success rate

只有在任务集合、episode 数、随机化、checkpoint 选择和 retry policy 一致时，success rate 才有较强可比性。LIBERO 97% 和 RoboTwin 93% 不能直接说前者/后者更强，因为任务和难度不同。

### Progress 与 success

progress 可以显示“模型完成了一半”，success 只能显示“完成/未完成”。长时域任务建议同时报告二者；但不能把 progress 91.67% 写成 success 91.67%。

### 仿真与真机

仿真可以做大量 controlled ablation，真机可以检查视觉噪声、摩擦、标定误差和执行延迟。二者是互补证据，不是同一尺度的结果。

### 预测误差与控制成功

一个模型可以有更低 LPIPS 或 imagination error，但 policy success 不升反降，因为它可能更擅长预测视觉细节，却没有预测接触和动作后果。反过来，低像素质量也不一定阻碍控制。

## 5. 可视化分类与解读方法

### 架构图

看输入、冻结模块、可训练模块、预测目标和 action head 的连接。重点不是图画得复杂，而是确认 future prediction 是否真的进入控制路径。

### Rollout / trajectory

看预测帧或 latent trajectory 是否在长 horizon 中漂移，错误是否集中在接触、遮挡、快速运动和目标切换处。成功案例不足以证明稳定性，应寻找失败 rollout。

### UMAP / PCA

看目标、任务阶段、时间 horizon 和 OOD 样本在表示空间中的相对关系。二维投影受降维方法、随机种子和颜色标注影响，不能单独作为性能证据。

### Attention / feature map

看模型是否关注手、物体、目标区域、接触点，而不是背景或水印。最好配合遮挡/扰动实验，而不是只凭肉眼判断。

### Counterfactual

固定同一观测，改变动作、夹爪状态或目标条件，比较预测未来。它可以说明模型对动作条件敏感，但还需要真实 rollout 验证反事实是否正确。

### Probe

冻结 latent，只训练轻量读出器预测位置、深度、物体类别或状态。Probe 高说明信息存在；如果 policy 不使用，仍然可能控制失败。

## 6. 推荐的统一评测表

对于 OpenWAM，建议每个 encoder/policy 组合都填写：

| 层次 | 必填内容 |
|---|---|
| Representation | DINO/V-JEPA/I-JEPA、冻结状态、token 数、latent dim、linear probe |
| Prediction | one-step error、rollout error、horizon、action conditioning |
| Planning/policy | CEM/MPC/DS-CEM 或 direct policy、action chunk、sampling/denoising steps |
| Control | benchmark、task 数、episode/trial、success、progress、失败类型 |
| Generalization | object、scene、instruction、camera、lighting、embodiment shift |
| Efficiency | parameter、FLOPs、forward latency、完整闭环频率 |
| Visualization | architecture、rollout、probe、attention、counterfactual、failure cases |

