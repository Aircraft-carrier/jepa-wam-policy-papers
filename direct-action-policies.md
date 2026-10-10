# 直接动作策略分类：WAM、JEPA Policy 与 VLA

## 1. 这一类论文解决什么问题

规划器通过搜索得到动作，优点是可以显式比较候选轨迹，缺点是推理慢。直接动作策略则希望用一次或少数几次前向，从图像、语言、机器人状态和未来 latent 直接输出 action chunk。

这类论文的核心比较不是“有没有视觉 encoder”，而是：

- 未来 latent 是训练辅助，还是推理时真正输入 action head？
- 动作是单步回归、action chunk、diffusion/flow 采样，还是 policy-noise refinement？
- 语言、视觉目标和 proprioception 怎样进入策略？

## 2. 专有名词解释

### Policy、WAM 和 VLA

- **Policy：** 给定观测和任务条件，输出动作分布或动作序列的函数。
- **WAM（World Action Model）：** 同时关注“世界如何变化”和“应该采取什么动作”的模型；通常包含 future representation prediction 与 action generation。
- **VLA（Vision-Language-Action）：** 将视觉、语言和动作统一起来的策略模型。
- **Action chunk：** 一次预测连续的多步动作，而不是只输出一个时间步。
- **Flow matching：** 学习从噪声逐步变成目标动作的连续向量场；推理时通常比传统 diffusion 少一些离散 denoising steps。
- **Diffusion policy：** 从噪声开始反复去噪得到动作，能表达多峰动作分布，但推理通常较慢。

## 3. 逐篇比较

| 论文 | 动作生成方式 | 未来信息如何使用 | 额外实验/指标 | 可视化 |
|---|---|---|---|---|
| [JEPA Policy](papers/2609.09630-jepa-policy.md) | diffusion-free action chunk，paired action/future prediction | future error 还能做 failure ranking | 9 个仿真任务；平均 83.0%；action-only MIP 77.4%；Diffusion Policy 75.1%；3 seeds；真机 5 tasks/630 episodes | 训练曲线、collapse audit、future-error failure ranking |
| [V-JEPA Policy](papers/2609.37250-vjepa-policy.md) | V-JEPA 2.1 latent + future predictor + flow-matching action expert | predictive visual latent 作为 action expert 条件 | LIBERO 97.25%；LIBERO-Plus 79.25%；RoboCasa-GR1 50.92%；预训练 predictor 55.58%；DROID predictor 后 LIBERO-Plus 91.50%；Marvin 真机 20 trials/task | future latent、视觉基础模型横向比较、shift 结果 |
| [JEPA-WAM Joint](papers/2608.09381-jepa-wam-joint.md) | shared transition/action predictor 生成 action chunk | current–future joint target 与 action predictor 共同训练 | LIBERO 96.7%；LIBERO-Plus 79.2%；RoboTwin clean 79.9%、random 36.9%；真机 5 tasks、每设置 10 rollouts | temporal-gap、patch correlation、trajectory residual、latency |
| [JEPA-WAM Visual Instruction](papers/2609.20277-jepa-wam-visual-instruction.md) | WAM 使用视觉 instruction bank 和 goal tokens | 视觉目标作为语言到动作的中间接口 | 真机 11 tasks；ID 87.3%、OOD-S 74.5%、OOD-I 80.9%；J-1024 优于 KF-64 | 704 图像 UMAP、keyframe/generated-image 对比 |
| [ACG-WAM](papers/2610.06965-acg-wam.md) | action-conditioned geometric latent + action head | 用几何 future slot 约束动作后果 | RoboTwin 50 tasks：clean 93.46%、randomized 92.68%、均值 93.07%；真机 success 85.00%、partial completion 91.67% | geometric latent、多 horizon prediction、teacher removal |
| [PLaW-VLA](papers/2610.12285-plaw-vla.md) | structured causal attention + continuous action expert | learnable queries 预测 future latent，再给 action expert | RoboTwin Hard Horizon III 比 reactive +11.8 pp；LIBERO-Plus 72.7%；约 1/19 generative WAM latency | PCA future-state、horizon masking、future conditioning ablation |
| [GIFT](papers/2609.04193-gift-intermediate-feature.md) | 既有 VLA/WAM action head | intermediate token 通过几何、affordance、goal-region supervision 被塑形 | LIBERO、LIBERO-Plus、RoboCasa；7 类 LIBERO-Plus shift；真机协议待核 | intermediate feature guidance、attention、no-injection ablation |
| [HiPolicy](papers/2604.06067-hipolicy-multifrequency.md) | multi-frequency action chunks + entropy-guided execution | 不是 future world model，而是用 entropy 选择执行频率 | RoboTwin 24 tasks、100 episodes/task；真机 8 tasks×10 trials；报告频率、成功率、延迟 | hierarchical FiLM、global feature fusion、entropy execution |

## 4. 一样的地方

- **都试图减少纯 reactive policy 的短视问题。** 未来 latent、几何目标、视觉 instruction 或多频率动作都在帮助策略理解“接下来会发生什么”。
- **都输出连续动作序列。** action chunk 能提高时间一致性，但一次错误预测也可能连续执行多步错误动作。
- **都需要 OOD 评测。** 训练任务上的 success 不能说明模型能处理新物体、新布局、光照、语言或机器人 embodiment。
- **都应该报告推理成本。** action steps、flow/diffusion steps、future predictor latency 和实际控制频率必须分开统计。

## 5. 不一样的地方

### 未来预测的位置

JEPA Policy 和 V-JEPA Policy 让 future representation 与 action prediction 成对；JEPA-WAM Joint 更强调共享 transition/action predictor；PLaW-VLA 用独立 future expert 与 structured attention；GIFT 则不预测未来，而是直接塑造中间 feature。

### 是否需要搜索

JEPA Policy、V-JEPA Policy、PLaW-VLA 主要是直接生成动作；MPC/CEM 类论文需要在线搜索。直接策略通常更快，但对训练分布和 action head 的依赖更强。

### 未来目标的形式

- **未来视觉 latent：** V-JEPA Policy、PLaW-VLA。
- **当前—未来 joint target：** JEPA-WAM Joint。
- **几何 future slot：** ACG-WAM。
- **视觉目标图/视觉 instruction：** JEPA-WAM Visual Instruction。
- **辅助中间特征：** GIFT。
- **执行频率不确定性：** HiPolicy。

## 6. 指标解释

- **平均 success：** 所有任务/episode 的成功比例，要看是否宏平均、微平均以及每个任务是否同样多 episode。
- **pp（percentage points）：** 绝对百分点差。例如 72% 到 80% 是 +8 pp，不是 +8%。
- **ID：** in-distribution，训练分布内测试。
- **OOD：** out-of-distribution，测试分布发生改变。
- **OOD-S：** 通常指 scene/spatial 变化；**OOD-I：** 通常指 instruction 变化，具体定义以对应论文为准。
- **Partial completion / task progress：** 没有完全成功时完成了多少任务进度，不能和 binary success 直接等价。
- **Latency：** 一次推理或完整控制周期的时间；“1/19 latency”必须确认比较的是哪一段 pipeline。

## 7. 可视化应该看什么

1. **Future latent 可视化：** 看不同时间 horizon 的表示是否随动作后果变化，而不是只按当前场景聚类。
2. **Action chunk rollout：** 看动作是否平滑、是否在接触时出现抖动、错误是否会连续累积。
3. **UMAP/PCA：** 看不同目标、场景或时间的表示是否分离；不能把二维投影直接当成真实语义空间证明。
4. **Failure ranking：** 看 future prediction error 高的片段是否真的更容易失败；这比单独展示成功案例更有价值。
5. **Attention/feature guidance：** 看模型是否关注物体、接触区域和目标区域，而不是背景。

## 8. 对 OpenWAM 的启发

如果目标是低延迟部署，建议优先比较：

1. action-only policy；
2. action + future latent；
3. action + geometric future；
4. action + visual goal；
5. action + MPC safety layer。

所有版本使用相同 encoder、数据、action chunk 和硬件测量 latency，才能判断收益到底来自 future modeling 还是模型变大。

