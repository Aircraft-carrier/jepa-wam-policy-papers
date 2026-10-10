# JEPA / WAM / Policy 论文完整合辑

> 合并日期：2026-10-10（Asia/Shanghai）。
> 来源：本目录 `papers/` 下的全部 19 篇 Markdown 论文卡片，按源文件名（arXiv ID）整理。
> 本文件完整保留各卡片内容，仅调整标题层级并增加目录、定位锚点和源文件入口；不是摘要版。
> 原文中的“待核对”、不确定性及指标口径一并保留；合并不代表新增事实核验。
> 本文件是当前快照；源卡片后续修改不会自动同步到合辑。

## 目录

1. [DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning](#paper-2411.04983-dino-wm) · [独立卡片](papers/2411.04983-dino-wm.md)
2. [V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning](#paper-2506.09985-v-jepa-2) · [独立卡片](papers/2506.09985-v-jepa-2.md)
3. [What Drives Success in Physical Planning with Joint-Embedding Predictive World Models?](#paper-2512.24497-what-drives-jepa-wm) · [独立卡片](papers/2512.24497-what-drives-jepa-wm.md)
7. [Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models](#paper-2605.06388-reconstruction-or-semantics) · [独立卡片](papers/2605.06388-reconstruction-or-semantics.md)
8. [Learning Visual Feature-Based World Models via Residual Latent Action](#paper-2605.07079-rla-wm) · [独立卡片](papers/2605.07079-rla-wm.md)
10. [JEPA-WAM: Learning Vision-Language-Action Policies with Joint-Embedding World Modeling](#paper-2608.09381-jepa-wam-joint) · [独立卡片](papers/2608.09381-jepa-wam-joint.md)
11. [JEPA Policy: Diffusion-Free Imitation Learning via Paired Action and Future Representation Prediction](#paper-2609.09630-jepa-policy) · [独立卡片](papers/2609.09630-jepa-policy.md)
12. [DUET-DINO: Simultaneous Cross-View World Modeling for Latent Planning in Robot Manipulation](#paper-2609.10506-duet-dino) · [独立卡片](papers/2609.10506-duet-dino.md)
13. [JEPA-WAM: Connecting Generated Visual Instructions to World Action Models through JEPA Latent Representations](#paper-2609.20277-jepa-wam-visual-instruction) · [独立卡片](papers/2609.20277-jepa-wam-visual-instruction.md)
14. [Latent evolving World Action Model（LeWAM，I-JEPA 路线）](#paper-2609.27455-lewam-ijepa) · [独立卡片](papers/2609.27455-lewam-ijepa.md)
15. [V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents](#paper-2609.37250-vjepa-policy) · [独立卡片](papers/2609.37250-vjepa-policy.md)
16. [Rethinking Representations for World-Action Modeling](#paper-2609.38163-rewam) · [独立卡片](papers/2609.38163-rewam.md)
17. [ACG-WAM: World-Action Modeling via Action-Conditioned Geometric Latent Prediction](#paper-2610.06965-acg-wam) · [独立卡片](papers/2610.06965-acg-wam.md)
18. [RoboJEPA: Scaling Robotic Latent World Models](#paper-2610.10515-robojepa) · [独立卡片](papers/2610.10515-robojepa.md)
19. [PLaW-VLA: Predictive Latent World Modeling for Vision-Language-Action Policies](#paper-2610.12285-plaw-vla) · [独立卡片](papers/2610.12285-plaw-vla.md)
20. [LeWAM: A JEPA World Action Model with Diffusion-Steering-Based MPC](#paper-2610.12407-lewam) · [独立卡片](papers/2610.12407-lewam.md)
21. [VO-DP: Semantic-Geometric Adaptive Diffusion Policy for Vision-Only Robotic Manipulation](#paper-2510.15530-vo-dp-feature-fusion) · [独立卡片](papers/2510.15530-vo-dp-feature-fusion.md)
22. [HiPolicy: Hierarchical Multi-Frequency Action Chunking for Policy Learning](#paper-2604.06067-hipolicy-multifrequency) · [独立卡片](papers/2604.06067-hipolicy-multifrequency.md)
23. [GIFT: Guided Intermediate Feature Training via Action-Oriented Structural Supervision for Robotic Manipulation](#paper-2609.04193-gift-intermediate-feature) · [独立卡片](papers/2609.04193-gift-intermediate-feature.md)

---

<a id="paper-2411.04983-dino-wm"></a>

来源：[papers/2411.04983-dino-wm.md](papers/2411.04983-dino-wm.md)

## DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning

### 1. 基本信息
- 作者：Gaoyue Zhou, Hengkai Pan, Yann LeCun, Lerrel Pinto
- 单位：Courant Institute, New York University；Meta AI
- 日期：2024-11-07（arXiv v2）
- 链接：[arXiv](https://arxiv.org/abs/2411.04983) · [HTML](https://arxiv.org/html/2411.04983)
- 类型：DINOv2 encoder + latent world model；WAM/policy 相关基础工作

### 2. 一句话摘要
冻结 DINOv2 patch features，离线预测 action-conditioned future features，并在测试时通过 CEM 优化动作序列实现 goal-conditioned zero-shot planning。

### 3. 主要创新点
- 不重建像素，直接在 pretrained DINOv2 patch-feature space 建模视觉动力学。
- 用 offline trajectories 训练，测试时以 goal feature 作为预测目标。
- 不依赖 expert demonstrations、reward model 或预学习 inverse model。
- 同一 world model 跨多类任务进行 task-agnostic planning。

### 4. 方法与训练信号
- 输入历史图像特征和 action sequence，预测未来 DINOv2 patch features。
- CEM 在 latent goal distance 上搜索动作；MPC 执行并滚动重规划。
- 论文比较 DINOv2、其他 pretrained encoders、causal mask、decoder loss 和数据规模。

### 5. Benchmark / 测评方法 / 结果
- 六类环境，覆盖 PointMaze、PushT manipulation、Granular 等任务族。
- 主要指标是 goal-reaching/planning success；另报告 decoded latent 的 SSIM、LPIPS 和推理/规划时间。
- 额外测试 unseen environment configurations，并比较不同 pretrained encoder。

### 6. 可视化与表示分析
有 PointMaze、PushT、Granular 的 planned trajectory visualization、start/goal/final 状态对比，以及 latent prediction quality 与 planning success 对照。

### 7. 真机实验与泛化
主要是仿真和离线数据实验；未将结果作为大规模真机 WAM 泛化验证。其核心贡献是证明 pretrained semantic feature 可以直接作为 planning interface。

### 8. 与 OpenWAM 的关系
是 DINO-family encoder → latent world model → planner 的基础参照，可用于和 OpenWAM 的 V-JEPA latent、action expert 以及 flow matching head 做结构对比。

### 9. 局限与待核对项
没有统一的 action-generating WAM head，也没有与现代 VLA/WAM benchmark 直接对齐；更适合作为 latent planning baseline。

---

<a id="paper-2506.09985-v-jepa-2"></a>

来源：[papers/2506.09985-v-jepa-2.md](papers/2506.09985-v-jepa-2.md)

## V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning

### 1. 基本信息
- 作者：Mido Assran et al.（完整作者见论文首页）
- 单位：FAIR at Meta；Mila – Quebec AI Institute；Polytechnique Montréal 等
- 日期：2025-06-11（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2506.09985) · [HTML](https://arxiv.org/html/2506.09985)
- 类型：基础方法；V-JEPA 2 / V-JEPA 2-AC world model

### 2. 一句话摘要
用超过 1 million hours 的互联网视频预训练 action-free V-JEPA 2，再用少量未标注机器人视频训练 latent action-conditioned world model，实现真机 goal-image planning。

### 3. 主要创新点
- 大规模视频预测表征同时覆盖 understanding、prediction 和 planning。
- V-JEPA 2-AC 只用 DROID 少于 62 小时未标注机器人视频进行 action-conditioned post-training。
- 真机部署不收集目标实验室机器人数据、不做 task-specific training、不用 reward。

### 4. 方法与训练信号
- action-free V-JEPA 2：互联网视频/图像自监督预训练。
- V-JEPA 2-AC：在 latent space 中进行 action-conditioned future prediction。
- 通过 image-goal planning 将预测 latent 用于控制。

### 5. Benchmark / 测评方法 / 结果
- Something-Something v2：motion understanding top-1 77.3。
- Epic-Kitchens-100：action anticipation recall-at-5 39.7。
- Video QA：PerceptionTest 84.0、TempCompass 76.9（8B scale）。
- 机器人：V-JEPA 2-AC 在两个不同实验室的 Franka arms 上 zero-shot pick-and-place；不依赖目标环境数据或任务奖励。
- Table 2：两实验室、每个任务 10 trials；平均 success 为 Reach 100%、Grasp 65%、Reach-with-object 25%、Pick-and-place/Cup 75%、Pick-and-place/Box 80%/65%（不同目标物）。

### 6. 可视化与表示分析
有 latent decoding、closed/open gripper counterfactual prediction、camera-position sensitivity 和 action-conditioned future representation 可视化。

### 7. 真机实验与泛化
- 平台：两个不同实验室的 Franka arms。
- 类型：image-goal pick-and-place planning。
- 泛化：跨实验室、跨机器人环境的 zero-shot deployment；没有目标环境 task-specific data。
- 该工作更像 OpenWAM 的 visual foundation / world-model pretraining 依据，而不是完整 action-generating WAM。

### 8. 与 OpenWAM 的关系
V-JEPA 2 是 V-JEPA Policy 的关键视觉基础；V-JEPA 2-AC 提供了 OpenWAM 可复用的 latent planning、goal-image 和 counterfactual visualization 评测范式。

### 9. 局限与待核对项
仍需补录两个实验室的相机布置和每个目标物的逐项失败类型；真机 trial 数、任务类型与 success 表已核对。

---

<a id="paper-2512.24497-what-drives-jepa-wm"></a>

来源：[papers/2512.24497-what-drives-jepa-wm.md](papers/2512.24497-what-drives-jepa-wm.md)

## What Drives Success in Physical Planning with Joint-Embedding Predictive World Models?

### 1. 基本信息
- 作者：Basile Terver, Tsung-Yen Yang, Jean Ponce, Adrien Bardes, Yann LeCun
- 单位：Meta FAIR；Inria Paris；École normale supérieure / PSL；New York University
- 日期：2025-12-30（arXiv v4）
- 链接：[arXiv](https://arxiv.org/abs/2512.24497) · [HTML](https://arxiv.org/html/2512.24497) · [代码/数据](https://github.com/facebookresearch/jepa-wms)
- 类型：JEPA-WM design study；DINO-WM / V-JEPA 2-AC comparison

### 2. 一句话摘要
系统研究 JEPA-WM 的 encoder、world-model architecture、training objective 和 planner，提出在 navigation 与 manipulation 上优于 DINO-WM 和 V-JEPA 2-AC 的组合 recipe。

### 3. 主要创新点
- 将 latent planning 设计拆为 encoder、transition model、loss、action representation 和 optimizer 等可控组件。
- 同时覆盖 simulated environments 与 real-world robotic DROID data。
- 比较 DINO-WM 与 V-JEPA-2-AC，并用 Spearman correlation 评估 validation metric 是否能预测 planning success。

### 4. 方法与训练信号
- 研究 DINO、V-JEPA/V-JEPA 2 等 visual encoder 的 frozen-feature world model。
- 比较 CEM、gradient descent 和 Nevergrad-style planning，及不同 rollout horizon/data scale。
- 推荐 recipe 按 navigation 与 real-world manipulation 分别选择。

### 5. Benchmark / 测评方法 / 结果
- 仿真：MetaWorld、Maze、Push-T、Wall；另有 RoboCasa Reach/Place。
- 真机/数据：DROID real-world videos；报告真实数据与 RoboCasa holdout 的 planning performance。
- Table 2 直接比较 best model、DINO-WM 和 V-JEPA-2-AC；另报告 2%/10%/50%/100% data scaling。

### 6. 可视化与表示分析
有 planned rollout 的 visual decoding、planner comparison、success-rate 与 validation metric 的 Spearman correlation，以及 image/video encoder 对比。

### 7. 真机实验与泛化
使用 DROID real-world robotic data 评估；重点是跨真实视频/仿真 holdout 的 planning transfer。需区分其“真实数据评估”与独立真实机器人闭环部署。

### 8. 与 OpenWAM 的关系
适合作为 OpenWAM 的系统性 ablation checklist：encoder、rollout loss、planner 和 validation metric 都应单独控制，而不是只报告一个最终 success。

### 9. 局限与待核对项
需补录最终推荐模型的逐任务 success、真机是否闭环执行、各 encoder 的 checkpoint 和每个 planner 的完整预算。

---




<a id="paper-2605.06388-reconstruction-or-semantics"></a>

来源：[papers/2605.06388-reconstruction-or-semantics.md](papers/2605.06388-reconstruction-or-semantics.md)

## Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models

### 1. 基本信息
- 作者：Nilaksh, Saurav Jha, Artem Zholus, Sarath Chandar
- 单位：Chandar Research Lab；Mila – Quebec AI Institute；Polytechnique Montréal；Canada CIFAR AI Chair
- 日期：2026-05-07（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2605.06388) · [HTML](https://arxiv.org/html/2605.06388) · [项目页](https://hskalin.github.io/semantic-wm/)
- 类型：encoder comparison；semantic latent WAM/policy evaluation

### 2. 一句话摘要
在 BridgeV2 固定 transition model、action conditioning 和数据协议下比较 VAE、Cosmos、V-JEPA 2.1、Web-DINO、SigLIP 2 等 latent encoder，分析 visual fidelity、planning 和 downstream policy 的关系。

### 3. 主要创新点
- 证明 visual reconstruction quality 不能单独作为 robotic world-model 选择标准。
- 将 encoder 质量拆成 visual fidelity、planning/downstream policy、latent representation quality 三个轴。
- 发现 semantic encoders（尤其 V-JEPA 2.1、Web-DINO、SigLIP 2）在 policy-relevant 指标上通常优于 reconstruction latent。

### 4. 方法与训练信号
- 固定 DiT world-model architecture，只替换 encoder/decoder path；部分 semantic encoder 使用 S-VAE adapter。
- 测试 DiT-S/B/L 多个规模、single/multi-view、CEM 与 inverse-dynamics probe。
- 用 VLM judge 评估 trajectory success，并报告 bootstrap confidence interval。

### 5. Benchmark / 测评方法 / 结果
- BridgeV2 world-model training/evaluation；包含 ID、OOD distractor、OOD instruction 以及 policy-in-the-loop episodes。
- 指标：PSNR/SSIM/LPIPS/t-LPIPS/FID/FVD、CEM controllability error、ID/OOD success、IDM action-recovery Pearson r、success-probe accuracy。
- DiT-L 的 per-instruction policy 表比较 V-JEPA 2.1、Web-DINO、VAE、Cosmos、SigLIP 2；semantic encoder family 在 policy-facing metrics 更强。

### 6. 可视化与表示分析
有 latent-space overview、OOD distractor/instruction rollout、per-instruction success、encoder-ceiling drop、inverse-dynamics recovery 和 representation quality 分析。

### 7. 真机实验与泛化
重点是 BridgeV2 policy-in-the-loop / OOD evaluation；是否包含真正硬件闭环需按正文区分，不能将 VLM-judged episodes 直接写成真机实验。

### 8. 与 OpenWAM 的关系
这是最适合 OpenWAM 做 encoder ablation 的协议参考：用相同 WAM/policy head 对比 V-JEPA、DINO、VAE 等，并同时报告 latent quality、planning 和 policy success。

### 9. 局限与待核对项
需补录 BridgeV2 的真实/仿真比例、每个 OOD 设置 episodes、V-JEPA 2.1/Web-DINO checkpoint 和硬件部署信息。

---

<a id="paper-2605.07079-rla-wm"></a>

来源：[papers/2605.07079-rla-wm.md](papers/2605.07079-rla-wm.md)

## Learning Visual Feature-Based World Models via Residual Latent Action

### 1. 基本信息
- 作者：Xinyu Zhang, Zhengtong Xu, Yutian Tao, Yeping Wang, Yu She, Abdeslam Boularias
- 单位：Rutgers University；Purdue University；University of Wisconsin–Madison
- 日期：2026-05-08（arXiv v2）
- 链接：[arXiv](https://arxiv.org/abs/2605.07079) · [HTML](https://arxiv.org/html/2605.07079) · [项目页](https://mlzxy.github.io/rla-wm)
- 类型：DINO feature world model + minimalist WAM/policy

### 2. 一句话摘要
从 DINO feature residual 中学习 Residual Latent Action（RLA），用 flow matching 预测 RLA，并将其用于 world-action modeling、VLA 改善和 offline visual RL。

### 3. 主要创新点
- RLA 从 DINO residual 中提取，编码 temporal progression 和 action effect。
- RLA-WM 避免直接回归高维 future feature 导致的模糊/塌缩。
- 提出 actionless video 学习的 minimalist WAM，改善 VLA 与 real-robot control。
- 另提出完全在 offline-video world model 内训练的 visual RL，不需要 online interaction。

### 4. 方法与训练信号
- frozen/feature-based visual state 与 action 输入 flow-matching predictor。
- 评估 future frame prediction、planning、policy learning 和 world-model visual reward。
- 对比 feature-based world model 与 video-diffusion world model 的质量和速度。

### 5. Benchmark / 测评方法 / 结果
- 仿真与 real-world datasets；报告 LPIPS、SSIM、DINO L1、pixel L1 和 FLOPs。
- RLA-WM 在 feature prediction 与 planning 上超过比较的 feature-based/video-diffusion baselines，并显著降低推理成本。
- minimalist WAM 改善 LIBERO VLA；完整 task-wise success 和真机表格应以正文实验表为准。

### 6. 可视化与表示分析
有 RLA residual、future feature prediction、planning rollout 和 speed/quality 对比；重点分析 latent action 的时间进展属性。

### 7. 真机实验与泛化
摘要确认包含 real-world datasets 和 real-robot policy improvement；具体平台、任务和 OOD 变量需按项目页/正文实验表区分，不将其泛化为 zero-shot。

### 8. 与 OpenWAM 的关系
非常适合做 OpenWAM 的 DINO-residual auxiliary baseline：比较直接 future latent prediction、RLA prediction 和 action-conditioned flow matching 的差异。

### 9. 局限与待核对项
需要补录 exact robot platform、LIBERO protocol、真实机器人 trials、数据是否 actionless，以及各 world-model baseline 的统一计算预算。

---


<a id="paper-2608.09381-jepa-wam-joint"></a>

来源：[papers/2608.09381-jepa-wam-joint.md](papers/2608.09381-jepa-wam-joint.md)

## JEPA-WAM: Learning Vision-Language-Action Policies with Joint-Embedding World Modeling

### 1. 基本信息
- 作者：Yihan Lin, Jiawei He, Shifeng Bao, Chen Zhao, Yang Li, Xiaobo Wang, Yan Wang, Cheng Chi, Jing Zhang
- 单位：School of Information, Renmin University of China；XYZ Embodied AI；Key Laboratory of Data Engineering and Knowledge Engineering；Engineering Research Center of Database and Business Intelligence；Shenzhen University of Advanced Technology；Institute for AI Industry Research (AIR), Tsinghua University
- 日期：2026-08-10（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2608.09381) · [HTML](https://arxiv.org/html/2608.09381) · [项目页](https://spritewithoutice.github.io/JEPA_WAM/)
- 类型：直接相关；latent JEPA-WAM

### 2. 一句话摘要
在冻结 V-JEPA 2.1 latent space 中构造 spatially structured joint current–future target，用共享 predictor 同时学习 latent transition 和 continuous action generation。

### 3. 主要创新点
- transition prediction 与 action generation 共享 predictor，避免预测分支与动作表征分离。
- joint current–future target 保留 dense patch correspondence，而非只预测全局未来 latent。
- transition supervision 直接塑造用于 action prediction 的 backbone。
- 同一监督方式可迁移到 pretrained π0.5，同时保留原始 perception/action pathway。

### 4. 方法与训练信号
- frozen V-JEPA 2.1 encoder；多视角视觉 token 构造联合当前-未来 target。
- target branch 仅训练时使用；部署时只保留 predictor/action pathway。
- 采用 continuous action generation，并比较无 robot-policy pretraining 与 pretrained VLA 两组设置。

### 5. Benchmark / 测评方法 / 结果
- LIBERO：无大规模 robot-policy pretraining 的 JEPA-WAM 平均 96.7%；π0.5 + JEPA objective 平均 97.8%。
- LIBERO-Plus：按 Camera、Robot initial state、Language、Light、Background、Noise、Layout 分组；JEPA-WAM 平均 79.2%，π0.5 + JEPA objective 86.3%。
- RoboTwin 2.0：20 tasks，Clean/Random；JEPA-WAM 全任务平均 79.9%/36.9%，π0.5 + JEPA objective 84.6%/37.5%。
- 真机任务：Bread placement、Fruit placement、Three-block placement、Three-block stacking、Drawer manipulation；每 task/setting 10 rollouts，报告 normalized completion score。

### 6. 可视化与表示分析
有 joint target 的 temporal-gap decoding、patch-wise correlation、trajectory residual/endpoint displacement 分析；还报告 inference latency/frequency 和 target construction ablation。

### 7. 真机实验与泛化
- 真机为双臂 manipulation；5 个任务覆盖放置、堆叠、抽屉多阶段操作。
- 同时测 ID 与视觉/空间 OOD；每个 task/setting 10 rollouts。
- OOD 具体协议与逐任务分数应以 Table 15 和 Appendix E 为准；这比单纯 randomized simulation 更接近真机泛化。

### 8. 与 OpenWAM 的关系
这是最直接的结构性参照之一：可用于比较 OpenWAM 是否需要 joint current–future target、dense patch correspondence 和共享 transition/action predictor。

### 9. 局限与待核对项
需补录 Table 15 的 ID/OOD 逐任务 normalized completion score，以及各 baseline 的真机逐项结果和训练预算。

---

<a id="paper-2609.09630-jepa-policy"></a>

来源：[papers/2609.09630-jepa-policy.md](papers/2609.09630-jepa-policy.md)

## JEPA Policy: Diffusion-Free Imitation Learning via Paired Action and Future Representation Prediction

### 1. 基本信息
- 作者：Jie Xu, Kangjin Yu, Ziyi Jin, Junjie Gao, Liqing Chen, Yixian Li, Shuai Tian, Zhongpu Xia
- 单位：Anyverse Dynamics
- 日期：2026-09-09（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2609.09630) · [HTML](https://arxiv.org/html/2609.09630)
- 类型：直接相关；JEPA-style future representation policy

### 2. 一句话摘要
将 action chunk 与其观测到的 future representation 作为配对训练目标，在共享 Transformer 中联合预测，得到无需扩散采样的低延迟 imitation policy。

### 3. 主要创新点
- future representation prediction 直接约束 action generation，而非只加独立 auxiliary head。
- dual-branch 与 gradient-routing ablation 用于区分共享拓扑和辅助损失的贡献。
- 训练/推理不依赖 diffusion policy 的迭代采样。
- future-prediction error 可作为 task-conditioned failure-ranking signal。

### 4. 方法与训练信号
- action token 与 future-representation token 在共享 Transformer 中交互。
- 两次 forward refinement；无单独 dynamics rollout，也不重建未来图像。
- LIBERO 使用 action horizon 16；robomimic/MimicGen 使用 horizon 10，执行前 8 个 action 后重规划；20 Hz action、2.5 Hz replanning。

### 5. Benchmark / 测评方法 / 结果
- LIBERO：MokaMoka、MugMug。
- robomimic：Square PH、Tool Hang PH、四相机 Transport PH。
- MimicGen：Coffee Preparation D1、Kitchen D1、Three Piece Assembly D1、Hammer Cleanup D1。
- 共 9 个仿真任务；三 seeds（41/42/43），报告 30 次评估中的 best-checkpoint success rate。
- 九任务平均：JEPA Policy 83.0%，action-only MIP 77.4%，Diffusion Policy 75.1%；相对 MIP +5.6 pp。
- 论文同时报告 last-checkpoint / checkpoint-selection protocol，指出绝对 success 会下降，但相对增益仍约 +4.7 至 +5.6 pp。
- 物理机器人：5 tasks、630 episodes；整体排序与仿真一致。

### 6. 可视化与表示分析
有训练曲线、future-prediction error 分析、representation-collapse audit，以及误差对失败排序的诊断信号。

### 7. 真机实验与泛化
- 类型：五项 physical-robot manipulation study：Cabinet、Cup Stack、Cup Upright、Plate Grape、Pen Insert。
- 63 sessions、630 episodes，无排除；每个 task 使用三个 checkpoint/arm，名义上 10 episodes/cell；实验在单一实验室、单一机器人和单一 operator 上完成。
- 重点是低延迟和跨任务排序复现；当前正文摘要未显示系统性的 unseen object/layout 真机泛化矩阵，需区别于仿真任务泛化。

### 8. 与 OpenWAM 的关系
适合作为 OpenWAM 的 diffusion-free action head 和 future-loss 诊断基线；也可用于比较 future prediction 是否必须经过完整 WAM 才能改善 policy。

### 9. 局限与待核对项
仍需补录 Table XI 的逐任务 success 数值；论文明确说明该 hardware study 没有系统的物体/光照/布局 OOD 矩阵，因此不能将其写成真机泛化验证。

---

<a id="paper-2609.10506-duet-dino"></a>

来源：[papers/2609.10506-duet-dino.md](papers/2609.10506-duet-dino.md)

## DUET-DINO: Simultaneous Cross-View World Modeling for Latent Planning in Robot Manipulation

### 1. 基本信息
- 作者：Nisarga Nilavadi, Ralf Römer, Moritz Reuss, Michael Krawez, Tobias Jülg, Angela P. Schoellig, Rudolf Lioutikov, Wolfram Burgard
- 单位：Artificial Intelligence and Robotics Lab, University of Technology Nuremberg；Learning Systems and Robotics Lab, Technical University of Munich；Intuitive Robots Lab, Karlsruhe Institute of Technology；NVIDIA；Robotics Institute Germany
- 日期：2026-09-09（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2609.10506) · [HTML](https://arxiv.org/html/2609.10506) · [项目页](https://utn-air.github.io/DUET-DINO)
- 类型：DINOv3/V-JEPA 2 cross-view latent world model

### 2. 一句话摘要
联合建模 side camera 与 wrist camera 的 action-conditioned latent dynamics，用 cross-view conditioning 支持完整 7-DoF manipulation planning。

### 3. 主要创新点
- 同时学习 global scene 与 gripper-centric local information，而不是独立训练两个视角。
- 针对细粒度空间/旋转 action 在单视角 latent prediction 中不可靠的问题设计 cross-view world model。
- 比较 V-JEPA 2 与 DINOv3，发现 DINOv3 更能捕捉 fine-grained action-conditioned scene change。

### 4. 方法与训练信号
- 使用 DROID 与 RoboArena 数据，从 scratch 训练 cross-view latent predictor。
- latent planning 在完整 7-DoF action space 中执行；任务包含 reach、angled reach、multi-goal grasp-and-lift。
- 与 single-view、independent dual-view baselines 比较。

### 5. Benchmark / 测评方法 / 结果
- RoboLab simulator：spatially diverse reach、orientation-intensive angled-reach、multi-goal lift。
- success rate：Reach 92.0%、Angled Reach 72.5%、Lift 60.0%。
- 报告 visual distribution shifts 下的鲁棒性，并比较 DINOv3 与 V-JEPA 2 的 downstream planning。

### 6. 可视化与表示分析
有 cross-view prediction、fine-grained action rollout 和不同 encoder 对 scene-change 捕捉能力的可视化/定性对比。

### 7. 真机实验与泛化
摘要重点是 simulator 与 dataset-level visual shifts；是否包含 physical robot deployment、平台和 trials 需以正文最终实验段落核对，不能仅凭项目页推断。

### 8. 与 OpenWAM 的关系
直接对应 OpenWAM 的多相机融合和 encoder choice：可以比较 shared temporal mixer、独立 view encoder 和 cross-view latent target 对 7-DoF 控制的影响。

### 9. 局限与待核对项
需补录 real-robot 是否存在、DROID/RoboArena 数据规模、每个 benchmark 的 episode 数和 DINOv3 具体版本。

---

<a id="paper-2609.20277-jepa-wam-visual-instruction"></a>

来源：[papers/2609.20277-jepa-wam-visual-instruction.md](papers/2609.20277-jepa-wam-visual-instruction.md)

## JEPA-WAM: Connecting Generated Visual Instructions to World Action Models through JEPA Latent Representations

### 1. 基本信息
- 作者：Tianbin Liu, Jian Zhu, Taiyi Su, Jianjun Zhang, Chong Ma, Zitai Huang, Yi Xu
- 单位：论文 HTML 正文未提供作者 affiliation 字段；单位暂记为“未公开/待 PDF 首页核对”，不据作者或项目名推断。
- 日期：2026-08-04（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2609.20277) · [HTML](https://arxiv.org/html/2609.20277)
- 类型：直接相关；visual-instruction-conditioned JEPA-WAM

### 2. 一句话摘要
用文本生成器为每条 instruction 生成视觉完成假设，再用 frozen V-JEPA 2.1 编码成 dense goal tokens，同时条件化 video/action experts，强化 WAM 的 instruction following。

### 3. 主要创新点
- 用 generated visual-instruction bank 补充稀疏、重复的轨迹级语言标注。
- V-JEPA 2.1 将生成图像中的任务语义与外观/布局 nuisance 解耦，并保留空间结构。
- 不训练图像生成器；通过 cross-attention 让 compact goal tokens 条件化 video/action experts。
- 构建 ID、scene OOD 和 instruction OOD 的真机 benchmark。

### 4. 方法与训练信号
- 每条文本 instruction 采样多张 task-completion image；默认 visual-instruction bank 为 1,024 张。
- V-JEPA 2.1 dense representations 经 learnable projector 压缩为 goal tokens。
- 与 real demonstration keyframe bank（KF-64）和不同规模 generated bank（J-64/J-512/J-1024）比较。

### 5. Benchmark / 测评方法 / 结果
- 真机 benchmark：11 个行为相关任务，包括 Give bread/pear/egg/carrot、PnP car/bread/carrot/egg/pear、Sort toys、Wipe table。
- ID 平均 success：π0 30.0%，Fast-WAM 77.3%，JEPA-WAM 87.3%。
- Scene OOD（OOD-S）：π0 7.3%，Fast-WAM 47.3%，JEPA-WAM 74.5%。
- Instruction OOD（OOD-I）：π0 23.6%，Fast-WAM 66.4%，JEPA-WAM 80.9%。
- Generated bank 对比：J-1024 平均 ID/OOD-S/OOD-I 为 82.5%/67.5%/75.0%，优于 KF-64 的 68.8%/47.5%/53.8%。

### 6. 可视化与表示分析
有 704 张生成图像的 UMAP：不同 task-level visual hypotheses 形成结构化区域；另有真实 keyframe 与 generated bank 的 qualitative 对比。

### 7. 真机实验与泛化
- 真机为共享 workspace manipulation，固定 box/plate/towel basket，随机化 object layout 与 container configuration。
- ID：训练分布；OOD-S：新场景组合；OOD-I：训练集中未出现的 instruction paraphrase。
- 这是明确区分 scene generalization 与 language generalization 的真机评测，而不是仅改变物体颜色。
- 所有模型使用同一套 1,370 demonstrations；真机推理在单张 NVIDIA RTX 5090 上，WAM 使用 10 action-denoising steps。

### 8. 与 OpenWAM 的关系
适合作为 OpenWAM instruction grounding 与 visual goal conditioning 的独立增强模块；可以在不改变 action/world backbone 的情况下测试“语言→视觉目标 latent”的收益。

### 9. 局限与待核对项
需从正文补充真实机器人本体型号、每个 task 的 rollout 数、生成器的完整型号及生成/推理时间成本；训练数据量和 GPU 推理设置已核对。

---

<a id="paper-2609.27455-lewam-ijepa"></a>

来源：[papers/2609.27455-lewam-ijepa.md](papers/2609.27455-lewam-ijepa.md)

## Latent evolving World Action Model（LeWAM，I-JEPA 路线）

### 1. 基本信息
- 作者：Xueji Fang, Boqiang Duan, Hua Wu, Jingdong Wang, Guo-Jun Qi。
- 单位：Zhejiang University；Westlake University；Baidu Inc.（论文首页列出的单位集合）。
- 日期：首次提交 2026-09-23；本卡片阅读版本 v2，更新于 2026-09-24。
- 链接：[arXiv](https://arxiv.org/abs/2609.27455) · [HTML v2](https://arxiv.org/html/2609.27455v2) · [PDF](https://arxiv.org/pdf/2609.27455) · [代码](https://github.com/XuejiFang/LeWAM) · [模型](https://huggingface.co/XuejiFang/LeWAM)。
- 类型：**直接相关；冻结 I-JEPA-H/14 encoder 的 latent WAM**。与 NVIDIA 的 `2610.12407` 同名 LeWAM 不是同一篇。

### 2. 一句话摘要
用 I-JEPA embeddings 同时作为动作生成的视觉输入和未来状态预测目标，联合学习 action velocity 与 future embeddings，无需预训练视频扩散 backbone。

### 3. 主要创新点
- 比较 frozen visual encoders 对动作学习的作用；I-JEPA-H 在本文设置中表现最好，但各 checkpoint 规模/预训练数据不同，不能推成所有任务下的普遍优越性。
- **AdaFuse** 自适应融合冻结 encoder 的多层特征。
- 共享 predictor 联合动作生成与未来 embedding prediction；attention mask 防止 clean action 泄漏到动作预测。
- **DemoDPO** 根据 demonstration guidance 排序候选动作，利用偏好优化提高策略，而无需额外环境交互。

### 4. 方法与训练信号
- Appendix C.2：I-JEPA-H/14 encoder 约 0.6B 参数，预训练于 ImageNet-22K，冻结；224×224 输入、14×14 patch，产生 256 image tokens。
- predictor + AdaFuse 共 402M 可训练参数；模型总参数约 1.0B。
- AdaLN-Zero 用 noise timestep 与 task embeddings 条件化 predictor；noisy action 使用噪声时间，visual/clean-action/future-query tokens 使用零时间。
- 对比 encoder 时禁用 future embedding prediction，固定 12-layer、width 1280 的 action predictor 和训练 recipe；V-JEPA 2 按 single-image protocol 重复当前图像 16 次。

### 5. Benchmark / 测评方法 / 结果
**RoboTwin 2.0，50 tasks，Clean/Random 各 100 evaluation cases/task（Table 2）。**

| 模型/消融 | Clean SR (%) | Random SR (%) | Avg. (%) |
|---|---:|---:|---:|
| I-JEPA Action Only | 88.42 | 83.92 | 86.17 |
| + WM | 88.86 | 85.18 | 87.02 |
| + WM + AdaFuse | 91.32 | 90.06 | 90.69 |
| LeWAM（含 DemoDPO） | 93.14 | 91.42 | 92.28 |

**Encoder-only policy 对照（Table 1；不是完整 WAM 的最终成绩）：** DINOv3-Large 67.54%，V-JEPA2-Large 72.17%，V-JEPA2-Huge 81.70%，I-JEPA-Huge 86.17%；这是与用户指定 encoder 家族最直接相关的受控比较。

### 6. 可视化与表示分析
- Figure 4/6：action-to-vision attention，展示 clean/randomized 场景中对交互物体的关注。
- Figure 7、Table 1：depth 与 instance segmentation probing；I-JEPA-Huge depth RMSE 0.445、correlation 0.853，AP@50 0.613、AP@75 0.323。
- Figure 5：DemoDPO threshold/coefficient/group-size 消融；Figure 8/9：真机 refinement 前后和跨方法 rollout。

### 7. 真机实验与泛化
- Appendix D：AgileX 双臂平台，由两台 Piper manipulators 组成；固定 front camera + wrist cameras。
- 任务：Stack Blocks、Fold Towel、Arrange Flowers；每方法每任务 **50 rollouts**，每次最多 3 分钟，30 Hz 执行，single A100 40 GB 部署。
- 指标是 **normalized task progress，不是完整任务成功率**：按里程碑和失败扣分计分，最大分数分别为 7/6/6，然后归一化到 0–100。
- DemoDPO 前后 task progress：Stack Blocks 81.1→84.9%；Fold Towel 58.3→60.7%；Arrange Flowers 50.7→53.0%。
- 初始 object configurations 按 rollout 采样。原文没有在该段定义独立的新物体/新材质/新场景/新指令真机 OOD split，因此只记录初始配置变化，不把它写成系统性真机 OOD 验证；RoboTwin Random 是仿真随机化。

### 8. 与 OpenWAM 的关系
是 **I-JEPA → future embedding prediction + action generation** 的直接 WAM 基线；可比较 I-JEPA vs V-JEPA vs DINO、multilayer AdaFuse、WM loss 和 DemoDPO 的独立作用。

### 9. 局限与待核对项
已核对 encoder、正文表格、可视化和真机评分协议。跨 encoder 的预训练数据与参数规模不完全匹配；真机 task-progress 与 success-rate benchmark 不应直接排序。来源定位：Table 1/2、Appendix C.2/C.5、Appendix D/D.1。

---

<a id="paper-2609.37250-vjepa-policy"></a>

来源：[papers/2609.37250-vjepa-policy.md](papers/2609.37250-vjepa-policy.md)

## V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents

### 1. 基本信息
- 作者：Yang Zhang, Jiangyuan Zhao, Chenyou Fan, Jiayu Hu, Xiu Yuan, Chenjia Bai, Xiu Li
- 单位：Tsinghua University；Shanghai Jiao Tong University；Fudan University；University of Science and Technology of China；Washington University in St. Louis；TeleAI；γ-Robotics
- 日期：2026-09-29（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2609.37250) · [HTML](https://arxiv.org/html/2609.37250) · [代码](https://github.com/breez3young/VJEPA-Policy)
- 类型：直接相关；JEPA latent WAM / policy

### 2. 一句话摘要
冻结 V-JEPA 2.1 encoder，在下游联合训练 instruction-conditioned future-latent predictor 与 flow-matching action expert，以较小的可训练参数建立 WAM。

### 3. 主要创新点
- 不依赖完整预训练视频生成器，而直接使用 predictive visual latent。
- predictor 的 future-informed context KV 条件化 action generation。
- DROID video–instruction pairs 可在无 action label 下预训练 predictor，再迁移到控制。
- 0.9B 总参数，其中 0.6B 可训练。

### 4. 方法与训练信号
- 输入：多视角 RGB、proprioception、language instruction。
- 冻结 V-JEPA 2.1 visual encoder；学习未来 latent 预测与 flow-matching action expert。
- 预训练阶段只使用 DROID 视频-指令；下游阶段使用机器人 demonstrations。

### 5. Benchmark / 测评方法 / 结果
- LIBERO：success rate 97.25%。
- LIBERO-Plus：79.25%；DROID predictor 预训练后 91.50%；扩展下游训练为 81.64%。
- RoboCasa-GR1：24 tasks，success rate 50.92%。
- RoboCasa-GR1 predictor-pretrained variant：55.58%。
- LIBERO-Plus 的 shift 维度包括 camera、initial state、language、lighting、texture、noise、layout；from-scratch V-JEPA Policy 平均 79.25%。
- 真机 TianJi Marvin 两项任务、每任务 20 trials：Table Cleanup 11/20（55%），Saucer Racking 7/20（35%）；DROID predictor 预训练后分别 15/20（75%）和 17/20（85%），平均从 45% 升至 80%。
- 另有 matched-framework / matched-budget 的视觉基础模型比较，强调分布偏移下 V-JEPA latent 的优势。

### 6. 可视化与表示分析
有跨视觉基础比较、future latent 预测/表示分析和控制结果分析；引用图表时以论文 HTML 章节为准。

### 7. 真机实验与泛化
- 平台：TianJi Marvin dual-arm platform。
- 任务：两项 multi-stage bimanual coordination。
- 泛化：LIBERO-Plus 等 distribution-shift benchmark；DROID 无动作预训练验证跨数据来源的 future-modeling transfer。

### 8. 与 OpenWAM 的关系
这是当前最直接的同路线参照：V-JEPA latent、future prediction、flow matching action、LIBERO-Plus 与真机泛化均可作为 OpenWAM 对比轴。

### 9. 局限与待核对项
仍需从附录补齐 LIBERO/RoboCasa 的训练 seed 与完整 baseline 表格，以及真机失败分类；核心真机 trial 数和任务名已核对。

---

<a id="paper-2609.38163-rewam"></a>

来源：[papers/2609.38163-rewam.md](papers/2609.38163-rewam.md)

## Rethinking Representations for World-Action Modeling

### 1. 基本信息
- 作者：Haoyi Jiang, Liu Liu, Xinjiang Wang, Zhihao Sun, Zequn Chen, Sen Wang, Xinjie Wang, Xia Chen, Jingfeng Yao, Weiheng Zhao, Shanglin Yuan, Zhizhong Su, Wei Sui, Wenyu Liu, Xinggang Wang
- 单位：Huazhong University of Science and Technology；Horizon Robotics；Fudan University；Xi’an Jiaotong University；D-Robotics
- 日期：2026-09-29（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2609.38163) · [HTML](https://arxiv.org/html/2609.38163)
- 类型：DINO feature WAM / representation-centric policy

### 2. 一句话摘要
提出 ReWAM，通过 feature calibration、temporal representation bottleneck 和 action-grounded representation shaping，把预训练 DINO features 组织成适合 dynamics 与 action 的紧凑状态。

### 3. 主要创新点
- 通过 controlled comparison 说明 reconstruction fidelity 或 pretrained perceptual feature 本身都不足以保证 policy learning。
- Temporal Representation Bottleneck 压缩 DINO features 并隔离 world-model dynamics。
- Action-Grounded Representation Shaping 只让 action loss 更新 bottleneck，使 representation 更贴近控制需求。
- 不使用 generative video pretraining。

### 4. 方法与训练信号
- 预训练 DINO feature → calibration → temporal bottleneck → world-action predictor/action policy。
- action loss 与 world-model loss 采用不同 gradient routing。
- 在 RoboTwin 2.0 和 RoboDojo 上验证 policy performance 与 large-scale embodied pretraining。

### 5. Benchmark / 测评方法 / 结果
- RoboTwin 2.0：success 93.6%。
- RoboDojo：约 600 小时 embodied pretraining，平均 score 12.29，success rate 8.28%。
- 论文重点比较 representation design，而不是只比较生成质量。

### 6. 可视化与表示分析
有 representation-space / bottleneck 分析、controlled encoder comparison 和 action-grounded feature shaping ablation；具体图表以 HTML 正文为准。

### 7. 真机实验与泛化
摘要明确报告 RoboDojo 结果，但平台、任务组成、真机/仿真比例和 OOD protocol 需从正文补录；RoboTwin randomized setting 不应自动等同真机泛化。

### 8. 与 OpenWAM 的关系
是 OpenWAM 当前架构最值得对照的 DINO-based alternative：尤其适合验证 action-gradient gating、temporal bottleneck 和 representation calibration。

### 9. 局限与待核对项
需补录 DINO 具体 checkpoint、RoboDojo task/score 定义、真机硬件和训练数据的 embodiment 构成。

---

<a id="paper-2610.06965-acg-wam"></a>

来源：[papers/2610.06965-acg-wam.md](papers/2610.06965-acg-wam.md)

## ACG-WAM: World-Action Modeling via Action-Conditioned Geometric Latent Prediction

### 1. 基本信息
- 作者：Jiangtao Liu, Zishang Xiang, Yage He, Lingguo Cui, Baihai Zhang, Runqi Chai, Senchun Chai
- 单位：School of Automation, Beijing Institute of Technology；LimX Dynamics
- 日期：2026-10-03（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2610.06965) · [HTML](https://arxiv.org/html/2610.06965) · [代码](https://github.com/RoboOpus/ACG-WAM)
- 类型：直接相关；action-conditioned geometric JEPA auxiliary objective

### 2. 一句话摘要
用当前观测和 actions 预测多时域几何 latent，以冻结 VGGT 对当前/未来图像对编码的 future slot 为 target，推理时移除辅助 teacher。

### 3. 主要创新点
- ACG-JEPA 显式监督 demonstration action 的几何后果。
- 监督施加在 temporal mixing 前的共享 visual embedding。
- head/wrist cameras 的多视角、多 horizon 几何预测。
- teacher 与 auxiliary modules inference 时移除。

### 4. 方法与训练信号
当前 observation + intervening actions → geometric future features；target 来自 frozen VGGT current/future image pair 的 future slot。

### 5. Benchmark / 测评方法 / 结果
- RoboTwin 2.0，50 tasks：clean success 93.46%；randomized success 92.68%；均值 93.07%。
- 真机 3 tasks：success 85.00%；partial completion 91.67%。
- 相对 Motus：真机 success +10.00 pp；partial completion +9.17 pp。
- RoboTwin 每 task/setting 100 episodes，使用 unseen instruction templates、evaluation seed 42；Clean/Random 表格是 50-task macro averages。
- 真机平台为 TRON2 + WUJI hands；每 task 100 demonstrations、15k fine-tuning updates、20 trials/task（总计 60 trials/policy）。
- PCS 将每 trial 记为 0/1/2：未完成/部分完成/完整完成，再归一化到 0–100；三任务平均等权。

### 6. 可视化与表示分析
有 geometric latent、多 horizon prediction 和 auxiliary ablation 分析；详细图号/定量 probe 待从正文表格补录。

### 7. 真机实验与泛化
- 真机：机器人 manipulation，3 tasks。
- 仿真泛化：clean vs randomized scenes。
- 摘要未说明真机是否做 unseen objects/geometry/scene 的独立泛化；不能将 randomized simulation 等同于真机泛化。

### 8. 与 OpenWAM 的关系
适合作为 OpenWAM auxiliary geometric prediction、camera fusion 和 action consequence supervision 的实验设计参考。

### 9. 局限与待核对项
需继续补齐 RoboTwin 的所有 task-wise 表格和具体随机化变量；真机硬件、任务、trial 数与 PCS 定义已核对。

---

<a id="paper-2610.10515-robojepa"></a>

来源：[papers/2610.10515-robojepa.md](papers/2610.10515-robojepa.md)

## RoboJEPA: Scaling Robotic Latent World Models

### 1. 基本信息
- 作者：Artem Zholus, Nicolas Beltran-Velez, Jianhao Yuan, Sarath Chandar, Tushar Nagarajan, Daniel Severo, Koustuv Sinha, Michal Drozdzal, Adriana Romero Soriano, Jeannette Bohg, Nicolas Ballas, Mahmoud Assran
- 单位：FAIR at Meta；Chandar Research Lab；Mila – Quebec AI Institute；Polytechnique Montréal
- 日期：2026-10-07（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2610.10515) · [HTML](https://arxiv.org/html/2610.10515)
- 类型：直接相关；JEPA robotic world model / scaling

### 2. 一句话摘要
在覆盖 12 种机器人 embodiment 的大规模数据上研究 JEPA latent world model scaling，并验证 imagination error 可作为真实机器人规划能力的代理指标。

### 3. 主要创新点
- 多 embodiment robotic world model 的 scaling law 视角。
- imagination error 随 compute 遵循二阶 power law，可外推模型质量。
- imagination error 与下游 robotic planning performance 强相关。
- 发布 checkpoint、训练和部署代码；8B predictor。

### 4. 方法与训练信号
核心是 JEPA latent future prediction；改变模型规模、数据和 compute，测量 latent rollout/imagination error 与规划性能的关系。

### 5. Benchmark / 测评方法 / 结果
- 多 embodiment robot data，重点是 scaling curve 而非单一 leaderboard。
- 指标：imagination error、compute scaling law、downstream planning performance。
- 摘要确认 zero-shot real-robot agent 能从单张 goal image 规划长时任务；具体任务/成功率待从实验表格补录。

### 6. 可视化与表示分析
有 scaling curves，以及 imagination error 与规划性能的相关性分析。

### 7. 真机实验与泛化
- 真机：zero-shot agent，single goal image conditioning，long-horizon planning。
- DROID/Franka 真机任务为 Grasp、Object Lift、Pick-and-Place；每个任务 10 episodes，goal 由 side/wrist camera 的单张图像指定。
- Table 12 报告 RoboJEPA-8B 三任务 success 为 67%/50%/27%，对应 task progress 为 67%/65%/42%；同时报告 22M–4B scaling variants。
- 泛化：跨 embodiment / zero-shot deployment；平台、任务和物体/场景变化需从正文核对。

### 8. 与 OpenWAM 的关系
适合建立 predictor quality proxy：除 action success 外，记录 rollout latent error、horizon degradation 和下游 planning correlation。

### 9. 局限与待核对项
需补齐 12 个 embodiment 的完整清单、仿真任务表、scaling fit 区间和不同模型的 planner success；Franka/DROID 真机任务与 10-episode protocol 已核对。

---

<a id="paper-2610.12285-plaw-vla"></a>

来源：[papers/2610.12285-plaw-vla.md](papers/2610.12285-plaw-vla.md)

## PLaW-VLA: Predictive Latent World Modeling for Vision-Language-Action Policies

### 1. 基本信息
- 作者：Yu Liu, Hetian Guo, Tianlv Huang, Ziyi Cai, Wudi Chen, Hantang Wang, Qiutong Liu, Yingzhi Peng, Wei Han, Peijun Tang, Jianan Wang, Zipei Fan, Zhiyuan Zha, Xuan Song
- 单位：Jilin University；Astribot；Harbin Institute of Technology, Shenzhen；The Hong Kong Polytechnic University；The University of Tokyo
- 日期：2026-10-08（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2610.12285) · [HTML](https://arxiv.org/html/2610.12285) · [项目页](https://rainyrobo.github.io/PLaW-VLA)
- 类型：相邻相关；predictive latent world model + VLA policy

### 2. 一句话摘要
在 prediction-oriented representation 中建模 task-relevant future states，并通过 structured causal attention 将历史、语言和未来状态用于 action generation。

### 3. 主要创新点
- 避免重建 control-irrelevant pixel details。
- Mixture-of-Transformers 同时处理 observation history、task semantics、predicted futures。
- 未来状态并行预测，约为 generative WAM 相当性能下的 1/19 inference latency。

### 4. 方法与训练信号
两阶段 predictive pretraining + robot-policy training；通过 future-state masking、representation 和 pretraining ablations 检查贡献。

### 5. Benchmark / 测评方法 / 结果
- RoboTwin Hard Horizon III：比 reactive policy +11.8 pp。
- zero-shot LIBERO-Plus：72.7% average success；相对 reconstruction-oriented latent prediction +1.77 pp。
- LIBERO：world-model ablation 96.28% vs 96.05%；mask all future states 97.40% → 93.05%。
- 报告 success/task progress；RoboTwin 使用 horizon 难度，LIBERO-Plus 使用 zero-shot distribution shift。

### 6. 可视化与表示分析
有 PCA visualization：current/near/far future features 随 robot arm motion 变化；有 horizon masking，far-future masking 影响略大。

### 7. 真机实验与泛化
- 平台：dual-arm wheeled humanoid robot。
- 任务：Fold Towel、Pack Toy、Play Basketball、Organize Stationery。
- 泛化：unseen towel materials/colors；将 pen holder 替换为不同高度、开口直径和颜色的 paper cup。
- 每个设置 10 spatial configurations × 3 trials；报告 normalized task progress。
- 真机训练使用每 task 约 50 epochs；推理在 RTX 5090 上，WAM baseline 使用 10 action-denoising steps；生成的 visual instruction 在语言指令不变时复用。

### 8. 与 OpenWAM 的关系
适合作为 OpenWAM 的效率和泛化对照：未来 latent 不必重建像素，但需证明 predicted future 真正改善 long-horizon control。

### 9. 局限与待核对项
真机逐任务图表主要报告 normalized task progress；仍需从 Figure 4/附录补录 π0/π0.5 的逐任务曲线数值和完整 latency 对照。

---

<a id="paper-2610.12407-lewam"></a>

来源：[papers/2610.12407-lewam.md](papers/2610.12407-lewam.md)

## LeWAM: A JEPA World Action Model with Diffusion-Steering-Based MPC

### 1. 基本信息
- 作者：Shashank Hegde, Alexander Popov, Elie Aljalbout, Nikolai Smolyanskiy
- 单位：论文 HTML 未给出可稳定抽取的 affiliation，待从 PDF 首页核对。
- 日期：2026-10-08（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2610.12407) · [HTML](https://arxiv.org/html/2610.12407)
- 类型：直接相关；JEPA WAM + MPC

### 2. 一句话摘要
用 decoder-free JEPA latent 端到端支持 forward、backward、inverse dynamics 和 policy prediction，并在 policy noise space 中用 diffusion-steering MPC 规划。

### 3. 主要创新点
- bidirectional transformer 统一四类预测模式。
- latent 同时追求状态可读性和对视觉 distractor 的不敏感。
- 指出 action-space MPC 会利用 dynamics model error，改在 policy noise space 规划。

### 4. 方法与训练信号
- 与 regular LeWM、reconstruction-based WAM 对比；flow-matching policy 使用匹配 encoder/规模。
- 采用 DS-CEM（diffusion-steering cross-entropy method）进行规划。

### 5. Benchmark / 测评方法 / 结果
- robosuite：Lift、Can、Square、ToolHang、Transport。
- closed-loop success；5 training seeds；每个 cell 50 episodes。
- 训练使用 90% 数据、300 epochs、5 seeds；其余 10% 作为评测 split，并在含视觉 distractor 的 simulator 中测试。
- 六项任务还包括 PushT；每个 world model/planner 组合共 250 rollouts（5 training seeds × 50 evaluation seeds）。
- Table 3 的 mode ablation 同时报告 ridge-probe state R²、policy success 与 DS-CEM success；Table 4 测试 policy-noise proposal 的 projection shell。
- 摘要结论：acting 与匹配规模的 flow-matching policy 相当；noise-space MPC 优于 raw-action 规划。

### 6. 可视化与表示分析
有 linear probe（robot/object state）、distractor 忽略对比和 latent/规划结果图。

### 7. 真机实验与泛化
重点为仿真闭环实验；作者将 real-world data/application 列为后续方向，未报告真机泛化结果。

### 8. 与 OpenWAM 的关系
适合作为 OpenWAM future predictor 是否能同时服务 policy 与 planning 的对照，并提醒评估 action-space MPC 的 model-error exploitation。

### 9. 局限与待核对项
作者单位已从正文确认是 NVIDIA；仍需补录六任务完整逐项 success 表和各 planner 的完整对照数值。

---

<a id="paper-2510.15530-vo-dp-feature-fusion"></a>

来源：[papers/2510.15530-vo-dp-feature-fusion.md](papers/2510.15530-vo-dp-feature-fusion.md)

## VO-DP: Semantic-Geometric Adaptive Diffusion Policy for Vision-Only Robotic Manipulation

### 1. 基本信息
- 作者：Zehao Ni, Yonghao He, Lingfeng Qian, Jilei Mao, Fa Fu, Wei Sui, Hu Su, Junran Peng, Zhipeng Wang, Bin He。
- 单位：D-Robotics；National Key Laboratory of Autonomous Intelligent Unmanned Systems；Frontiers Science Center for Intelligent Autonomous Systems；Shanghai Institute of Intelligent Science and Technology, Tongji University；Institute of Automation, Chinese Academy of Sciences；University of Science and Technology Beijing。
- 日期：首次提交 2025-10-17；阅读版本 v4，更新于 2026-10-10。
- 链接：[arXiv](https://arxiv.org/abs/2510.15530) · [HTML v4](https://arxiv.org/html/2510.15530v4) · [PDF](https://arxiv.org/pdf/2510.15530) · [代码/训练库](https://github.com/D-Robotics-AI-Lab/VO-DP)。
- 类型：直接相关；冻结视觉基础模型中间特征融合到 diffusion policy。

### 2. 一句话摘要
VO-DP 从 VGGT 内部的 DINOv2 语义特征和 geometric features 中提取多层视觉信息，用 Semantic-Geometric Fuser 与 cross-attention 融合，再通过 CNN compression 提供给 vision-only diffusion policy。

### 3. 主要创新点
- 不使用深度/点云作为 policy 输入，而是利用大视觉模型内部的语义与几何中间特征构造视觉条件。
- VGGT encoder 同时提供 DINOv2 patch-level semantic features 和 AA network 产生的 geometric features；Semantic-Geometric Fuser 通过残差 cross-attention 融合二者。
- 比较 multi-frame VO-DP 与 single-frame VO-DP-1，并做物体尺寸、外观、背景颜色和光照的真实世界鲁棒性评测。

### 4. 方法与训练信号
- 输入为单视角 RGB 图像；VGGT 对 patchified images 产生语义与几何特征，使用 cross-attention 做 per-frame semantic-geometric fusion。
- 融合后的视觉特征经过 CNN compression，再作为 diffusion policy 的条件；方法重点在 encoder intermediate feature extraction/fusion，而不是重新训练一个 point-cloud perception stack。
- VO-DP-1 使用单帧输入，VO-DP 使用时间窗口；正文 Table I/II 和 Figure 2 对应模型结构与训练配置。

### 5. Benchmark / 测评方法 / 结果
**RoboTwin 1.0 仿真，14 个双臂 manipulation tasks（Table II）。** 摘要报告 VO-DP 平均 success rate 64.6%，DP3 为 64.0%，DP 为 34.8%。

**真实世界四任务（Table V）。** VO-DP 平均 success rate 87.9%，DP3 为 67.5%，DP 为 11.2%；正文还报告尺寸、外观、背景颜色和光照 robustness。

### 6. 可视化与表示分析
- Figure 2 是 VO-DP overall architecture，展示 VGGT/DINOv2 semantic branch、geometric branch、Semantic-Geometric Fuser、CNN compression 和 policy head。
- Figure 3、Figure 6/9 展示 RoboTwin 任务、真实设备和四类 robustness 设置。

### 7. 真机实验与泛化
- 真实世界四个 manipulation tasks；比较 vision-only DP、point-cloud DP3 与 VO-DP。
- 测试 unseen cube size、cube appearance、background color 和 illumination；VO-DP 不依赖深度传感器点云。

### 8. 与 OpenWAM 的关系
可作为 OpenWAM 的 encoder-side baseline：比较 DINO/V-JEPA/几何 foundation features 的中间层融合、cross-attention 与 compression，并将 fused representation 作为 future-target 或 action expert 输入。

### 9. 局限与待核对项
- VGGT 内部特征的具体层位、冻结/微调状态和 feature dimension 需结合代码核对。
- 主要对照是 DP/DP3 与 vision-only manipulation，不能直接等同于 JEPA latent WAM 的 future prediction 结果。

---

<a id="paper-2604.06067-hipolicy-multifrequency"></a>

来源：[papers/2604.06067-hipolicy-multifrequency.md](papers/2604.06067-hipolicy-multifrequency.md)

## HiPolicy: Hierarchical Multi-Frequency Action Chunking for Policy Learning

### 1. 基本信息
- 作者：Jiyao Zhang, Zimu Han, Junhan Wang, Xionghao Wu, Shihong Lin, Jinzhou Li, Hongwei Fan, Ruihai Wu, Dongjiang Li, Hao Dong。
- 单位：CFCS, School of Computer Science, Peking University；National Key Laboratory for Multimedia Information Processing, Peking University；Xi'an Jiaotong University；Tsinghua University；Beijing University of Aeronautics and Astronautics；Jingdong Technology Information Technology Co., Ltd。
- 日期：首次提交 2026-04-07；阅读版本 v1，更新于 2026-10-10。
- 链接：[arXiv](https://arxiv.org/abs/2604.06067) · [HTML](https://arxiv.org/html/2604.06067) · [PDF](https://arxiv.org/pdf/2604.06067)。
- 类型：邻近相关；层级 observation feature fusion 与多频 action chunk policy。

### 2. 一句话摘要
HiPolicy 从不同时间频率的 observation history 提取层级特征，同时预测不同频率的 action chunks，并通过 hierarchical FiLM、global feature fusion 和 entropy-guided execution 平衡长时规划与精细闭环控制。

### 3. 主要创新点
- 将 imitation policy 的 temporal resolution 分成多个频率，联合建模 coarse long-horizon actions 与 fine-grained reactive actions。
- 用对应频率的 observation features 条件化对应频率的 action chunks，并通过 cross-attention 做 global feature fusion。
- 推理阶段通过多次 stochastic sampling 估计 action entropy，自适应选择执行频率。

### 4. 方法与训练信号
- 从 raw observation chunk 中按不同频率抽取历史帧，经 observation encoder 得到 hierarchical observation features；视觉输入可为 2D images 或 3D point clouds，proprioception 可选。
- hierarchical FiLM 将每个频率的 observation feature 与同频 action feature 对齐；global feature fusion 跨频率做 attention 通信。
- 多频 noisy action chunks 拼接后由 1D-CNN U-Net diffusion model 预测噪声。

### 5. Benchmark / 测评方法 / 结果
**仿真：RoboTwin 1.0 与 RoboTwin 2.0，共 24 个 manipulation tasks。** DP/DP+HiPolicy 每任务 100 episodes；DP3 变体遵循 DP3 protocol，每任务 100 episodes。移除 hierarchical feature fusion 会造成约 6% 的性能下降。

**真实世界（Figure 5、Table 5）。** Franka Panda 7-DoF + Robotiq 2F-85，8 个 manipulation tasks，每任务平均 10 trials；相对 DP baseline，HiPolicy 报告 42% relative higher success rate 和 14% faster execution speed。

### 6. 可视化与表示分析
- Figure 3 展示 hierarchical observation features、FiLM fusion、global cross-frequency fusion 和多频 action chunks。
- Figure 4 展示 entropy-guided execution；Table 2/3/4 及 Appendix E.3 分析 feature fusion、采样次数、history、chunk size 和 frequency levels。

### 7. 真机实验与泛化
- 使用 Franka Panda、Robotiq 2F-85 和三台 ZED 系列相机；8 个真实世界任务，每任务 10 次评测，随机化初始物体。
- 仿真覆盖 RoboTwin 1.0/2.0，重点测试 long-horizon 与 high-precision tasks。

### 8. 与 OpenWAM 的关系
HiPolicy 适合迁移到 OpenWAM 的 action expert：把不同历史时间尺度的 latent features 分层，再比较 FiLM、cross-attention/global fusion 对 future prediction 和 action generation 的影响。

### 9. 局限与待核对项
- “多层/多频”主要是不同时间频率的 observation features，不等同于 frozen foundation encoder 的 transformer intermediate-layer fusion。
- 具体 visual encoder backbone、history 采样和所有 task-wise success 数值需参考 Appendix 与代码核对。

---

<a id="paper-2609.04193-gift-intermediate-feature"></a>

来源：[papers/2609.04193-gift-intermediate-feature.md](papers/2609.04193-gift-intermediate-feature.md)

## GIFT: Guided Intermediate Feature Training via Action-Oriented Structural Supervision for Robotic Manipulation

### 1. 基本信息
- 作者：Yupeng Zheng, Xiang Li, Songen Gu, Yuhang Zheng, Shuai Tian, Weize Li, Linbo Wang, Chaoyue Li, Qichao Zhang, Haoran Li, Zhongpu Xia, Ya-Qin Zhang, Shuicheng Yan, Dongbin Zhao。
- 单位：Institute of Automation, Chinese Academy of Sciences；University of Chinese Academy of Sciences；National University of Singapore；Tsinghua University；Fudan University。
- 日期：首次提交 2026-09-03；阅读版本 v1，更新于 2026-10-10。
- 链接：[arXiv](https://arxiv.org/abs/2609.04193) · [HTML](https://arxiv.org/html/2609.04193) · [PDF](https://arxiv.org/pdf/2609.04193) · [项目页](https://openphoenix-team.github.io/GIFT-pages)。
- 类型：直接相关；面向 VLA 与 WAM 的中间视觉特征监督框架。

### 2. 一句话摘要
GIFT 用 geometry alignment、affordance prediction 和 goal-region reconstruction 训练共享于动作路径的中间视觉特征，使 VLA、Fast-WAM 和 inverse-dynamics WAM 保留更有控制价值的结构信息。

### 3. 主要创新点
- 将机器人控制中的中间特征结构化为几何、可供性和目标区域三类监督，形成跨架构的统一训练原则。
- 在 VLA、直接动作扩散 Fast-WAM 和 inverse-dynamics WAM 三种 action formulation 上实例化同一方法。
- injection/no-injection 对照支持“特征内化”而非单纯给 action head 额外条件的解释。

### 4. 方法与训练信号
- GIFT 直接监督 action pathway 使用的 intermediate visual features，不固定 decoder 或动作头。
- geometry guidance 对齐运动可行性相关的场景结构；affordance guidance 预测 instruction-relevant entities 与 object-centric end-effector 配置；goal guidance 重建语言指令确定的目标区域。
- 三类约束在训练期施加，并比较是否将辅助预测注入 action head。

### 5. Benchmark / 测评方法 / 结果
**LIBERO-Plus，标准 LIBERO 训练后 zero-shot transfer，七类 distribution shifts。** GIFT-VLA、GIFT-WAM-Fast、GIFT-WAM-IDM 分别达到 79.6%、72.6%、87.8%，相对匹配 baseline 提升 4.6、12.6、5.2 个百分点。

**RoboCasa。** GIFT-VLA、GIFT-WAM-Fast、GIFT-WAM-IDM 分别达到 61.4%、83.6%、82.3%；LIBERO 标准 ID 结果见 Table I，geometry/affordance/goal 消融见 Table IV。

### 6. 可视化与表示分析
- Figure 2 展示 GIFT 在 VLA 与两种 WAM action formulation 上的整体框架。
- Figure 3 对比 injection 与 no-injection；Figure 5 可视化 action-to-vision attention。

### 7. 真机实验与泛化
- 已确认的定量协议集中在 LIBERO、LIBERO-Plus 与 RoboCasa；LIBERO-Plus 覆盖七类视觉/空间 distribution shifts。
- 论文摘要提到 high-precision real-world manipulation，但独立真机平台、任务数和 trial-level success rate 仍待从正文/附录核对。

### 8. 与 OpenWAM 的关系
这是“中间特征监督”路线的直接基线：不改写 OpenWAM 的动作生成范式，而是给共享 encoder/predictor 的中间表示增加几何、可供性和目标区域约束，可用于 auxiliary representation loss、feature probing 和 no-injection ablation。

### 9. 局限与待核对项
- 不同 policy configuration 的 encoder、数据规模和 action head 细节需要按 Appendix 逐项对齐。
- 当前已核对摘要、方法、Figure 2/3/5、LIBERO/LIBERO-Plus/RoboCasa 结果；真机平台与完整 success 协议待继续核对。
