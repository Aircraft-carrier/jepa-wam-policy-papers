# 规划器分类：MPC、CEM 与 Diffusion-Steering MPC

## 1. 这一类论文解决什么问题

这一类工作通常已经有一个视觉 encoder 和 world model，但模型本身只回答“如果执行这组动作，未来可能是什么样”。它还没有回答“我现在究竟应该执行哪组动作”。规划器负责在候选动作中搜索一条让预测未来接近目标的轨迹。

这里的共同结构是：

```text
当前观测 → encoder 得到 latent
动作候选 a[0:H] → world model 预测未来 latent
预测未来与目标/代价比较 → 选动作
只执行前几步 → 新观测 → 再规划
```

## 2. 专有名词解释

### MPC 是什么

MPC（Model Predictive Control，模型预测控制）是一种滚动规划方法。它不会一次规划到任务结束，而是：

1. 用模型预测未来一小段时间；
2. 选出当前看来最好的动作序列；
3. 只执行序列前面的一小段；
4. 获取新的相机/状态观测后重新规划。

这样可以用新观测纠正模型误差。代价是每一步都要重新推理，实时性和规划预算很重要。

### CEM 是什么

CEM（Cross-Entropy Method，交叉熵方法）是一个黑盒动作搜索算法。它先随机采样很多动作序列，用 world model 计算每条序列的 cost，保留表现最好的 elite samples，再根据 elite 的均值和方差重新采样。重复多轮以后，采样分布会集中到高质量动作附近。

它不需要对环境或 planner cost 求梯度，适合离散、非光滑或预测模型较复杂的场景；缺点是采样数量大时计算昂贵，也可能被错误的 world model 预测误导。

### DS-CEM 是什么

DS-CEM（Diffusion-Steering CEM）不是在原始 action space 中完全随机采样，而是利用已经训练好的 flow-matching/diffusion policy 作为动作先验，在 policy noise space 或其附近做 CEM 搜索。这样候选动作更像“策略认为合理的动作”，比直接搜索每个关节的任意值更容易稳定。

## 3. 共同点与不同点

| 论文 | 规划方式 | 规划目标 | 额外实验/指标 | 可视化 |
|---|---|---|---|---|
| [DINO-WM](papers/2411.04983-dino-wm.md) | latent goal distance + CEM + MPC | 预测 DINOv2 future feature 接近 goal feature | PointMaze、PushT、Granular 等 6 类环境；success；latent quality；SSIM、LPIPS、规划时间；unseen configuration | planned trajectory、start/goal/final 状态、latent 预测质量与规划成功对照 |
| [V-JEPA 2](papers/2506.09985-v-jepa-2.md) | V-JEPA 2-AC + image-goal planning | 预测未来 latent 接近目标图像 latent | Something-Something top-1 77.3；EK100 recall@5 39.7；PerceptionTest 84.0；TempCompass 76.9；Frankas 真机 pick-and-place success | latent decoding、closed/open gripper counterfactual、camera sensitivity |
| [LeWAM](papers/2610.12407-lewam.md) | DS-CEM，在 policy noise space 规划 | 通过 flow policy prior 搜索更可靠的候选动作 | robosuite 的 PushT、Lift、Can、Square、ToolHang、Transport；5 seeds；每 cell 50 episodes；linear probe state R²；policy success；DS-CEM success；distractor | state linear probe、distractor 忽略、不同 planner 的 latent/轨迹对比 |
| [What Drives Success](papers/2512.24497-what-drives-jepa-wm.md) | 多 planner / planning recipe 对比 | 分析 prediction cost 如何转成 physical planning | 不只报单一 success，还比较数据规模、horizon、proprioception、planner 和任务族 | rollout decoding、prediction metric 与 planning success 相关性 |
| [LeWAM-IJEPA](papers/2609.27455-lewam-ijepa.md) | latent policy/planning + demonstration guidance | 用示范对候选动作排序 | 记录预测、policy 和 demonstration preference 的消融；具体协议以卡片待核字段为准 | attention、depth/segmentation probes、rollout |

## 4. 一样的地方

- **都把视觉规划从像素空间移到 latent space。** 规划器比较的是 feature/embedding 距离或 latent cost，而不是逐像素生成质量。
- **都使用闭环思想。** 即使一次搜索得到完整 action sequence，也通常只执行前缀，随后用新观测重新规划。
- **都依赖 prediction horizon。** horizon 太短看不到任务后果，太长则误差累积，规划器可能追逐错误的未来。
- **都需要把模型误差纳入评测。** latent prediction 更准确不一定意味着动作成功率更高。

## 5. 不一样的地方

### 搜索空间不同

DINO-WM 和 V-JEPA 2 更接近直接在动作序列上搜索；LeWAM 则用 flow-matching policy 把搜索放到 noise space。后者的候选动作带有 policy prior，通常更容易满足动作分布，但会受 policy 本身偏差限制。

### 目标定义不同

DINO-WM 和 V-JEPA 2 使用 goal-image/goal-feature；LeWAM 更强调 task cost、policy prior 和 model-error exploitation；recipe study 则把 planner 当作受控变量进行诊断。

### 控制能力边界不同

CEM/MPC 系统本身不一定是 action-generating policy。它可以在没有大量 task-specific demonstrations 时进行 goal-conditioned planning，但推理成本通常高于一次前向的 policy。

## 6. 这些指标应该怎么读

- **Success rate：** 完成任务的 episode 比例，必须同时看任务定义、episode 数和是否为仿真。
- **Goal distance：** 预测最终 latent 与目标 latent 的距离，越小通常越好，但它只是 proxy，不等于成功。
- **SSIM：** 像素结构相似度，较高表示图像结构更接近；不直接说明动作是否正确。
- **LPIPS：** 感知特征距离，用深层视觉特征衡量图像差异；同样不能替代控制指标。
- **State linear-probe R²：** 用线性模型从 latent 恢复真实状态的解释度，说明状态可读性，不说明 planner 一定会使用这些信息。
- **Planning latency：** 生成一次动作所需时间；CEM 的采样数、迭代数和 world-model rollout 都会影响它。

## 7. 可视化应该看什么

1. **轨迹图：** 看规划路径是否平滑、是否绕开障碍、最终状态是否真的接近目标。
2. **latent rollout：** 看模型对短期和长期未来的预测是否逐步漂移。
3. **goal/start/final 拼图：** 适合判断“latent cost 变小”是否对应可见的任务进展。
4. **distractor 对照：** 如果加入背景变化后 latent 仍主要跟随机器人和物体，而不是跟随背景，说明表示更接近控制相关因素。
5. **cost-success 曲线：** 若预测 cost 与成功率相关，latent cost 才有资格作为 planner objective；若两者不相关，规划器可能只是在优化错误的代理目标。

## 8. 对 OpenWAM 的启发

- 若目标是 image-goal 或长时域控制，MPC/CEM 可以作为 policy 的外层安全检查器。
- 若已有强大的 flow/diffusion policy，优先尝试在 policy noise space 规划，而不是从零搜索关节动作。
- 评测必须同时报告 planner budget、单步延迟、success、预测误差和失败类型。
- 不要把“有 MPC”直接等同于“有 WAM”；WAM 还需要明确的 action-conditioned representation/policy 接口。

