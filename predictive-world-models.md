# 预测式 Latent World Model 分类：从未来表示到动作后果

## 1. World model 到底是什么

World model 是一个学习环境变化规律的模型。给定当前状态和动作，它尝试预测下一状态或未来一段状态。在这些论文中，状态通常不是原始 RGB 图像，而是 encoder 输出的 latent。

```text
z_t = Encoder(o_t)
z_{t+1:t+H} = Predictor(z_t, a_{t:t+H-1}, language, proprioception)
```

使用 latent 的原因是机器人控制真正关心的是物体、姿态、接触和任务进度，而不是每个像素的光照变化。但 latent 越抽象，越需要证明它没有丢掉 action-relevant information。

## 2. 专有名词解释

- **Action-conditioned prediction：** 预测未来时显式输入动作，回答“执行这个动作会发生什么”。
- **Teacher forcing：** 预测第 `t+1` 步时使用真实的前一步状态；训练稳定，但可能掩盖长时域误差。
- **Autoregressive rollout：** 第一步预测结果作为下一步输入，反复滚动；更接近部署，但会累积误差。
- **Horizon：** 预测未来多少步。短 horizon 误差小但看不远，长 horizon 看得远但更难稳定。
- **Representation collapse：** 不同输入被映射成相似 latent，导致模型失去区分状态的能力。
- **Predictive latent：** 不是当前图像的静态 embedding，而是与未来状态/动作后果相关的表示。

## 3. 逐篇比较

| 论文 | world model 形式 | 预测目标 | 额外实验/指标 | 可视化 |
|---|---|---|---|---|
| [DINO-WM](papers/2411.04983-dino-wm.md) | DINOv2 latent dynamics | future patch feature | encoder、causal mask、decoder loss、数据规模；SSIM/LPIPS/goal success | rollout、轨迹和 goal matching |
| [V-JEPA 2](papers/2506.09985-v-jepa-2.md) | action-free V-JEPA + V-JEPA 2-AC | 视频未来 latent / action-conditioned future | 视频理解、anticipation、QA、image-goal robot planning | counterfactual、latent decoding、camera sensitivity |
| [RLA-WM](papers/2605.07079-rla-wm.md) | residual latent action world model | 动作引起的 residual feature change | feature prediction、planning、visual RL、LPIPS/SSIM/DINO-L1/FLOPs | residual rollout、质量-速度 |
| [JEPA-WAM Joint](papers/2608.09381-jepa-wam-joint.md) | joint current-future target + shared predictor | future target embedding | temporal gap、patch correlation、trajectory residual、latency | temporal gap、patch correlation |
| [RoboJEPA](papers/2610.10515-robojepa.md) | large multi-view/embodiment predictor | next-step feature grid + long rollout | teacher forcing vs rollout、12 embodiment scaling、imagination error 与 planning 相关性 | scaling curve、rollout |
| [JEPA Policy](papers/2609.09630-jepa-policy.md) | paired future representation branch | action 与 future representation 同时预测 | action-only、Diffusion Policy、future-error failure ranking、collapse audit | error 曲线和失败排序 |
| [V-JEPA Policy](papers/2609.37250-vjepa-policy.md) | frozen predictive visual latent + predictor | task-relevant future visual latent | predictor pretraining、DROID transfer、LIBERO/LIBERO-Plus/RoboCasa | future latent 和基础模型比较 |
| [PLaW-VLA](papers/2610.12285-plaw-vla.md) | future-state expert in frozen V-JEPA latent | query-based future states | future masking、horizon ablation、latency、RoboTwin Hard Horizon III | PCA、horizon masking |
| [LeWAM](papers/2610.12407-lewam.md) | unified bidirectional JEPA | forward/backward/inverse/policy modes | state R²、policy success、DS-CEM、distractor | probe 和 planner rollout |

## 4. 一样的地方

- **都把未来预测作为控制接口。** 未来不是为了制作视频，而是为了判断动作后果。
- **都需要 action conditioning。** 没有动作条件时，模型只能预测“可能发生什么”，不能回答“我采取这个动作会发生什么”。
- **都存在 teacher-forcing 与 rollout gap。** 单步预测好，不代表连续滚动稳定。
- **都必须区分 prediction metric 与 control metric。** feature error、图像质量和 success 是三种不同层次的证据。

## 5. 不一样的地方

### 预测目标不同

DINO-WM、V-JEPA 2、RoboJEPA 预测未来视觉 feature；RLA-WM 更强调 action residual；ACG-WAM 预测几何 future slot；JEPA Policy 和 PLaW-VLA 让未来预测直接进入 action generation；LeWAM 则进一步统一多种 prediction mode。

### world model 的使用时机不同

- **纯 planner：** DINO-WM、V-JEPA 2，预测后交给 CEM/MPC 搜索。
- **policy 内部模块：** JEPA-WAM、JEPA Policy、V-JEPA Policy、PLaW-VLA，预测结果直接条件化 action head。
- **分析/规模化重点：** What Drives Success、RoboJEPA、Reconstruction or Semantics，重点是研究哪些表示和训练 recipe 更值得用。

### 是否重建像素

JEPA 系列通常在 embedding space 预测，不强制恢复完整 RGB；RLA-WM/DINO-WM 可以报告解码或 perceptual metrics，但这些指标主要是辅助诊断。

## 6. 指标解释

- **One-step prediction error：** 单步未来 latent 的误差，适合检查局部动力学。
- **Rollout/imagination error：** 多步递归预测的误差，能暴露误差累积。
- **Temporal-gap ablation：** 改变当前与目标未来之间的时间间隔，检查模型能看多远。
- **Patch correlation：** 不同空间 patch 的表示相似度，帮助判断模型是否保留局部空间结构。
- **Trajectory residual：** 预测轨迹与真实轨迹/状态之间的差异，可用于检查动态一致性。
- **Planning success：** 预测模型被实际用于规划后的任务成功率，是最接近控制的指标，但仍受 planner 影响。

## 7. 可视化应该怎样读

1. **Teacher forcing vs rollout 曲线：** 如果前者很好、后者迅速恶化，说明模型依赖真实中间状态，部署会不稳定。
2. **不同 horizon 的预测图：** 看预测是否逐渐模糊/漂移，以及漂移是否集中在控制关键物体。
3. **Action counterfactual：** 在相同观测下输入不同动作，未来 latent 是否出现不同且合理的分支。
4. **未来 latent PCA/UMAP：** 看时间远近、任务阶段和动作类别是否形成有意义的结构。
5. **预测误差与失败案例：** 检查 error 是否能提前标记失败，而不是只在失败之后变大。

## 8. 对 OpenWAM 的启发

一个可信的 OpenWAM world model 至少要同时通过三道检查：

1. **表示检查：** latent 能否线性读出物体、位姿、接触和任务阶段？
2. **动力学检查：** action-conditioned rollout 是否在长 horizon 保持稳定？
3. **控制检查：** 把预测接到相同 policy/planner 后，是否真正提高 success 或 OOD 泛化？

