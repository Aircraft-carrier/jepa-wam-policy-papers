# JEPA / WAM / Policy 论文完整汇编

> 本文件自动汇总 `papers/` 下全部论文精读卡片。每篇包含基本信息、问题直觉、方法数据流、训练目标、实验解读、复现清单、OpenWAM 对比和局限。网页详情页由同一批 Markdown 自动生成。

## 阅读路线

1. 先看第 2 节的一句话摘要和第 10 节的直觉解释。
2. 再看第 11–12 节，理解数据流、训练/推理差异和 loss 的作用。
3. 最后看第 13–15 节，判断实验到底证明了什么，以及是否值得复现。

## 论文目录

- [DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning](#2411.04983-dino-wm)
- [V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning](#2506.09985-v-jepa-2)
- [VO-DP: Semantic-Geometric Adaptive Diffusion Policy for Vision-Only Robotic Manipulation](#2510.15530-vo-dp-feature-fusion)
- [What Drives Success in Physical Planning with Joint-Embedding Predictive World Models?](#2512.24497-what-drives-jepa-wm)
- [HiPolicy: Hierarchical Multi-Frequency Action Chunking for Policy Learning](#2604.06067-hipolicy-multifrequency)
- [Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models](#2605.06388-reconstruction-or-semantics)
- [Learning Visual Feature-Based World Models via Residual Latent Action](#2605.07079-rla-wm)
- [JEPA-WAM: Learning Vision-Language-Action Policies with Joint-Embedding World Modeling](#2608.09381-jepa-wam-joint)
- [GIFT: Guided Intermediate Feature Training via Action-Oriented Structural Supervision for Robotic Manipulation](#2609.04193-gift-intermediate-feature)
- [JEPA Policy: Diffusion-Free Imitation Learning via Paired Action and Future Representation Prediction](#2609.09630-jepa-policy)
- [DUET-DINO: Simultaneous Cross-View World Modeling for Latent Planning in Robot Manipulation](#2609.10506-duet-dino)
- [JEPA-WAM: Connecting Generated Visual Instructions to World Action Models through JEPA Latent Representations](#2609.20277-jepa-wam-visual-instruction)
- [Latent evolving World Action Model（LeWAM，I-JEPA 路线）](#2609.27455-lewam-ijepa)
- [V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents](#2609.37250-vjepa-policy)
- [Rethinking Representations for World-Action Modeling](#2609.38163-rewam)
- [ACG-WAM: World-Action Modeling via Action-Conditioned Geometric Latent Prediction](#2610.06965-acg-wam)
- [RoboJEPA: Scaling Robotic Latent World Models](#2610.10515-robojepa)
- [PLaW-VLA: Predictive Latent World Modeling for Vision-Language-Action Policies](#2610.12285-plaw-vla)
- [LeWAM: A JEPA World Action Model with Diffusion-Steering-Based MPC](#2610.12407-lewam)

---

<a id="2411.04983-dino-wm"></a>
# DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning

## 1. 基本信息
- 作者：Gaoyue Zhou, Hengkai Pan, Yann LeCun, Lerrel Pinto
- 单位：Courant Institute, New York University；Meta AI
- 日期：2024-11-07（arXiv v2）
- 链接：[arXiv](https://arxiv.org/abs/2411.04983) · [HTML](https://arxiv.org/html/2411.04983)
- 类型：DINOv2 encoder + latent world model；WAM/policy 相关基础工作

## 2. 一句话摘要
冻结 DINOv2 patch features，离线预测 action-conditioned future features，并在测试时通过 CEM 优化动作序列实现 goal-conditioned zero-shot planning。

## 3. 主要创新点
- 不重建像素，直接在 pretrained DINOv2 patch-feature space 建模视觉动力学。
- 用 offline trajectories 训练，测试时以 goal feature 作为预测目标。
- 不依赖 expert demonstrations、reward model 或预学习 inverse model。
- 同一 world model 跨多类任务进行 task-agnostic planning。

## 4. 方法与训练信号
- 输入历史图像特征和 action sequence，预测未来 DINOv2 patch features。
- CEM 在 latent goal distance 上搜索动作；MPC 执行并滚动重规划。
- 论文比较 DINOv2、其他 pretrained encoders、causal mask、decoder loss 和数据规模。

## 5. Benchmark / 测评方法 / 结果
- 六类环境，覆盖 PointMaze、PushT manipulation、Granular 等任务族。
- 主要指标是 goal-reaching/planning success；另报告 decoded latent 的 SSIM、LPIPS 和推理/规划时间。
- 额外测试 unseen environment configurations，并比较不同 pretrained encoder。

## 6. 可视化与表示分析
有 PointMaze、PushT、Granular 的 planned trajectory visualization、start/goal/final 状态对比，以及 latent prediction quality 与 planning success 对照。

## 7. 真机实验与泛化
主要是仿真和离线数据实验；未将结果作为大规模真机 WAM 泛化验证。其核心贡献是证明 pretrained semantic feature 可以直接作为 planning interface。

## 8. 与 OpenWAM 的关系
是 DINO-family encoder → latent world model → planner 的基础参照，可用于和 OpenWAM 的 V-JEPA latent、action expert 以及 flow matching head 做结构对比。

## 9. 局限与待核对项
没有统一的 action-generating WAM head，也没有与现代 VLA/WAM benchmark 直接对齐；更适合作为 latent planning baseline。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
DINO-WM 关注的是一个很具体但很关键的问题：机器人能不能不把视频还原成像素，而只在一个已经有语义的视觉特征空间里预测未来？传统像素世界模型需要解释颜色、纹理和光照等大量与控制无关的细节；本文把这些细节压缩掉，把规划目标改成“预测出来的未来特征是否接近目标图像特征”。

### 10.2 读者可以先记住的类比
可以把 DINOv2 看成一个已经学会“看懂物体和场景”的测量仪，把 world model 看成在这个测量仪读数上预测未来的模拟器，而 CEM/MPC 则像一个不断试算动作方案、执行第一小段并重新测量的驾驶员。

## 11. 逐步读方法
### 11.1 数据流
当前图像先经过冻结的 DINOv2，得到带空间 patch 结构的视觉特征；离线轨迹中的动作序列与历史特征一起输入预测器，产生未来特征。测试时把目标图像也编码成特征，CEM 采样多组动作、滚动预测未来特征、按 latent goal distance 排序，再执行最有希望的第一段动作。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。训练信号不是像素重建，而是预测未来 DINOv2 特征与真实未来特征之间的误差。这样做直接强调“未来状态是否可用于规划”，但也意味着模型可能忽略某些对像素质量重要、对任务却不重要的细节；因此不能只看视觉重建质量判断它是否适合控制。

### 11.3 关键模块与张量含义
需要区分三个模块：DINOv2 是视觉表示接口，预测器是动作条件的 latent dynamics，CEM/MPC 是推理时的规划器。论文的 policy 并不是一个一次前向就直接输出动作的 WAM head，而是 world model 加搜索算法的组合。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。训练信号不是像素重建，而是预测未来 DINOv2 特征与真实未来特征之间的误差。这样做直接强调“未来状态是否可用于规划”，但也意味着模型可能忽略某些对像素质量重要、对任务却不重要的细节；因此不能只看视觉重建质量判断它是否适合控制。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
PointMaze、PushT 和 Granular 等任务回答“语义特征能否支撑不同类型的 goal-conditioned planning”；encoder、causal mask、decoder loss 和数据规模消融回答“性能来自预训练表示还是来自预测器容量”；SSIM/LPIPS 与 success 的对比则帮助区分“预测得像”与“规划得对”。

### 13.2 不要过度解读的地方
主要证据来自仿真和离线数据。即便 latent goal distance 与成功率相关，也不能直接推出它能在真实相机噪声、遮挡和动力学误差下稳定工作。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：重点固定 DINOv2 checkpoint、patch 特征的空间布局、预测 horizon、CEM 的采样/筛选预算、MPC 重规划频率和 goal distance 定义。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 冻结 DINOv2 作为 planning interface；用 latent goal distance 做任务无关规划；把 encoder、dynamics 和 planner 分开做消融。
- **不能直接推出：** 它没有证明 DINOv2 特征可以直接替代 action policy，也没有证明无需目标环境数据就能完成真实机器人上的复杂操作。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 最值得继续验证的是：同一套 latent planner 是否能在真实机器人上面对视觉 distractor 和 embodiment shift；以及 feature prediction loss 与最终控制成功率之间的相关性是否在更多任务上成立。

---

<a id="2506.09985-v-jepa-2"></a>
# V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning

## 1. 基本信息
- 作者：Mido Assran et al.（完整作者见论文首页）
- 单位：FAIR at Meta；Mila – Quebec AI Institute；Polytechnique Montréal 等
- 日期：2025-06-11（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2506.09985) · [HTML](https://arxiv.org/html/2506.09985)
- 类型：基础方法；V-JEPA 2 / V-JEPA 2-AC world model

## 2. 一句话摘要
用超过 1 million hours 的互联网视频预训练 action-free V-JEPA 2，再用少量未标注机器人视频训练 latent action-conditioned world model，实现真机 goal-image planning。

## 3. 主要创新点
- 大规模视频预测表征同时覆盖 understanding、prediction 和 planning。
- V-JEPA 2-AC 只用 DROID 少于 62 小时未标注机器人视频进行 action-conditioned post-training。
- 真机部署不收集目标实验室机器人数据、不做 task-specific training、不用 reward。

## 4. 方法与训练信号
- action-free V-JEPA 2：互联网视频/图像自监督预训练。
- V-JEPA 2-AC：在 latent space 中进行 action-conditioned future prediction。
- 通过 image-goal planning 将预测 latent 用于控制。

## 5. Benchmark / 测评方法 / 结果
- Something-Something v2：motion understanding top-1 77.3。
- Epic-Kitchens-100：action anticipation recall-at-5 39.7。
- Video QA：PerceptionTest 84.0、TempCompass 76.9（8B scale）。
- 机器人：V-JEPA 2-AC 在两个不同实验室的 Franka arms 上 zero-shot pick-and-place；不依赖目标环境数据或任务奖励。
- Table 2：两实验室、每个任务 10 trials；平均 success 为 Reach 100%、Grasp 65%、Reach-with-object 25%、Pick-and-place/Cup 75%、Pick-and-place/Box 80%/65%（不同目标物）。

## 6. 可视化与表示分析
有 latent decoding、closed/open gripper counterfactual prediction、camera-position sensitivity 和 action-conditioned future representation 可视化。

## 7. 真机实验与泛化
- 平台：两个不同实验室的 Franka arms。
- 类型：image-goal pick-and-place planning。
- 泛化：跨实验室、跨机器人环境的 zero-shot deployment；没有目标环境 task-specific data。
- 该工作更像 OpenWAM 的 visual foundation / world-model pretraining 依据，而不是完整 action-generating WAM。

## 8. 与 OpenWAM 的关系
V-JEPA 2 是 V-JEPA Policy 的关键视觉基础；V-JEPA 2-AC 提供了 OpenWAM 可复用的 latent planning、goal-image 和 counterfactual visualization 评测范式。

## 9. 局限与待核对项
仍需补录两个实验室的相机布置和每个目标物的逐项失败类型；真机 trial 数、任务类型与 success 表已核对。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
V-JEPA 2 的核心问题不是“如何让机器人直接输出动作”，而是先训练一个足够通用的时空视觉表示，让它能理解视频中的动作、预测未来，并在少量机器人数据上变成可规划的世界模型。它把大规模互联网视频学到的“视频常识”与少量机器人交互数据连接起来。

### 10.2 读者可以先记住的类比
可以把 action-free V-JEPA 2 看成通过大量视频学会物体运动语法的视觉大脑；V-JEPA 2-AC 则像给这个大脑补上“如果我执行这个动作，未来会怎样”的分支预测能力；goal-image planner 最后负责从候选动作中挑选能走向目标图像的方案。

## 11. 逐步读方法
### 11.1 数据流
预训练阶段输入视频和图像，通过 masked video prediction 学习上下文与未来之间的关系；机器人适配阶段冻结或基本复用视觉 encoder，在 DROID 等未标注机器人视频上训练 action-conditioned predictor；部署时输入当前观测、目标图像和候选动作，比较预测未来 latent 与目标 latent 的距离，形成 image-goal planning。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。预训练的预测目标让表示保留运动和时序信息，而不是只保留静态类别语义；V-JEPA 2-AC 的动作条件训练让 latent 变化与机器人动作建立联系。这个设计降低了机器人标注成本，但不等于模型学会了所有任务的动作策略，规划器仍需要可靠的目标距离和短期预测。

### 11.3 关键模块与张量含义
论文需要分开阅读三个层次：V-JEPA 2 是通用视频 encoder；V-JEPA 2-AC 是 action-conditioned latent world model；真机系统是基于 image goal 的 planner。前两个模块的能力评测覆盖视频理解和预测，不能直接与最后的机器人 success rate 当成同一个指标。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。预训练的预测目标让表示保留运动和时序信息，而不是只保留静态类别语义；V-JEPA 2-AC 的动作条件训练让 latent 变化与机器人动作建立联系。这个设计降低了机器人标注成本，但不等于模型学会了所有任务的动作策略，规划器仍需要可靠的目标距离和短期预测。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
Something-Something、Epic-Kitchens 和 Video QA 验证通用视频理解/预测能力；counterfactual、camera-position 和 latent decoding 分析验证表示是否编码了动作后果；两个实验室 Franka 的 pick-and-place 则回答少量机器人数据能否迁移到不同环境。

### 13.2 不要过度解读的地方
真机结果是 image-goal pick-and-place，不是开放指令的 action-generating WAM。报告的成功率还受到目标物、实验室、相机和 planner 设置影响，应与其他论文按相同任务和协议比较。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 V-JEPA 2 checkpoint、机器人适配数据时长、action chunk/horizon、goal matching 方式、planner 采样预算、实验室/机器人划分和每项任务的 trial denominator。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 大规模 action-free 视频预训练后再进行小规模 action-conditioned post-training；用 goal-image planning 测试 latent 是否真正具有控制价值；同时报告 understanding、prediction 和 robot control 三类证据。
- **不能直接推出：** 它没有证明仅靠互联网视频就能解决机器人控制，也没有证明 V-JEPA 2 latent 在所有 embodiment 和长时域任务上都比专门训练的 policy 更好。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 后续最值得做的是把 V-JEPA 2-AC 与直接 action policy、V-JEPA Policy 和 JEPA-WAM 在同一机器人平台、同一数据预算下对齐比较。

---

<a id="2510.15530-vo-dp-feature-fusion"></a>
# VO-DP: Semantic-Geometric Adaptive Diffusion Policy for Vision-Only Robotic Manipulation

## 1. 基本信息
- 作者：Zehao Ni, Yonghao He, Lingfeng Qian, Jilei Mao, Fa Fu, Wei Sui, Hu Su, Junran Peng, Zhipeng Wang, Bin He。
- 单位：D-Robotics；National Key Laboratory of Autonomous Intelligent Unmanned Systems；Frontiers Science Center for Intelligent Autonomous Systems；Shanghai Institute of Intelligent Science and Technology, Tongji University；Institute of Automation, Chinese Academy of Sciences；University of Science and Technology Beijing。
- 日期：首次提交 2025-10-17；阅读版本 v4，更新于 2026-10-10。
- 链接：[arXiv](https://arxiv.org/abs/2510.15530) · [HTML v4](https://arxiv.org/html/2510.15530v4) · [PDF](https://arxiv.org/pdf/2510.15530) · [代码/训练库](https://github.com/D-Robotics-AI-Lab/VO-DP)。
- 类型：**直接相关；冻结视觉基础模型中间特征融合到 diffusion policy**。

## 2. 一句话摘要
VO-DP 从 VGGT 内部的 DINOv2 语义特征和 geometric features 中提取多层视觉信息，用 Semantic-Geometric Fuser 与 cross-attention 融合，再通过 CNN compression 提供给 vision-only diffusion policy。

## 3. 主要创新点
- 不使用深度/点云作为 policy 输入，而是利用大视觉模型内部的语义与几何中间特征构造视觉条件。
- VGGT encoder 同时提供 DINOv2 patch-level semantic features 和 AA network 产生的 geometric features；Semantic-Geometric Fuser 通过残差 cross-attention 融合二者。
- 比较 multi-frame VO-DP 与 single-frame VO-DP-1，并做物体尺寸、外观、背景颜色和光照的真实世界鲁棒性评测。

## 4. 方法与训练信号
- 输入为单视角 RGB 图像；VGGT 对 patchified images 产生语义与几何特征，使用 cross-attention 做 per-frame semantic-geometric fusion。
- 融合后的视觉特征经过 CNN compression，再作为 diffusion policy 的条件；方法重点在 encoder intermediate feature extraction/fusion，而不是重新训练一个 point-cloud perception stack。
- VO-DP-1 使用单帧输入，VO-DP 使用时间窗口；正文 Table I/II 和 Figure 2 对应模型结构与训练配置。

## 5. Benchmark / 测评方法 / 结果
**RoboTwin 1.0 仿真，14 个双臂 manipulation tasks（Table II）。** 摘要报告 VO-DP 平均 success rate 64.6%，DP3 为 64.0%，DP 为 34.8%；正文还区分 VO-DP 与单帧 VO-DP-1，具体 task-wise 数值以 Table II 为准。

**真实世界四任务（Table V）。** VO-DP 平均 success rate 87.9%，DP3 为 67.5%，DP 为 11.2%。正文还报告尺寸、外观、背景颜色和光照 robustness，尺寸泛化平均 success 65.0%，光照测试平均 success 83.3%。

## 6. 可视化与表示分析
- Figure 2 是 VO-DP overall architecture，明确展示 VGGT/DINOv2 semantic branch、geometric branch、Semantic-Geometric Fuser、CNN compression 和 policy head。
- Figure 3 展示 RoboTwin 仿真任务与 VGGT 重建点云；Figure 6/9 展示真实设备、物体和四类 robustness 设置。
- 论文重点是语义-几何特征对照与鲁棒性，而不是对单独 encoder layer 的全面 probing；“多层”应理解为 foundation model 内部特征与多分支特征融合，不能写成逐层 feature pyramid 已被完整消融验证。

## 7. 真机实验与泛化
- 真实世界四个 manipulation tasks；比较 vision-only DP、point-cloud DP3 与 VO-DP。
- 明确测试 unseen cube size、cube appearance、background color 和 illumination；正文给出测试网格/随机化协议与对应表格。
- 真实部署不依赖深度传感器点云，论文将这一点作为从仿真到复杂真实环境迁移的主要卖点。

## 8. 与 OpenWAM 的关系
VO-DP 是“中间视觉特征融合 → policy”而非 JEPA-WAM，但可作为 OpenWAM 的 encoder-side baseline：比较 DINO/V-JEPA/几何 foundation features 的中间层融合、cross-attention 与 compression；也可把 fused representation 作为 WAM future-target 或 action expert 的输入。

## 9. 局限与待核对项
- VGGT 内部特征与 DINOv2 特征的具体层位、冻结/微调状态和 feature dimension 需要结合代码进一步核对。
- 论文的主要对照是 DP/DP3 与 vision-only manipulation，不能直接等同于 JEPA latent WAM 的 future prediction 结果。
- 当前已核对摘要、Figure 1/2、RoboTwin Table II、真实世界 Table V 和 robustness Table VI–IX。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
VO-DP 解决的不是“是否使用视觉特征”，而是“语义信息和几何信息应该怎样共同进入一个视觉策略”。只看语义特征可能知道物体是什么却不准确知道距离和姿态；只看几何特征又可能缺少任务相关的物体语义。

### 10.2 读者可以先记住的类比
可以把语义特征理解为“这是什么、该抓哪里”，把几何特征理解为“它在哪里、空间关系怎样”。VO-DP 的 fuser 像一个翻译器，把两种描述对齐后压缩成 policy 能使用的场景状态。

## 11. 逐步读方法
### 11.1 数据流
图像先经过 VGGT/DINOv2 路径分别得到语义和几何特征；残差 cross-attention 与 FFN 进行跨模态融合；空间压缩模块减少 token 数，再与 proprioception 拼接；最后 diffusion policy 根据场景表示生成连续动作。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。监督信号最终来自动作生成误差，融合模块通过 policy loss 学会保留对抓取和操作有用的语义-几何关系。它不等于显式地监督每个 3D 几何量，因此分析结果应关注几何特征是否真的改善动作成功，而不是只看融合后的 embedding。

### 11.3 关键模块与张量含义
这篇论文的贡献主要在 encoder/fuser 和 policy conditioning，不是 world model。它没有 action-conditioned future predictor；与 JEPA/WAM 比较时应把它当作“中间视觉表示如何影响 policy”的相邻基线。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。监督信号最终来自动作生成误差，融合模块通过 policy loss 学会保留对抓取和操作有用的语义-几何关系。它不等于显式地监督每个 3D 几何量，因此分析结果应关注几何特征是否真的改善动作成功，而不是只看融合后的 embedding。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
不同语义/几何分支、融合位置和空间压缩设置回答“哪类信息真正有用”；vision-only manipulation 任务回答融合后的表示能否转成动作；若只报告 success，应同时关注场景复杂度和是否使用 proprioception。

### 13.2 不要过度解读的地方
语义-几何融合的收益可能依赖 VGGT、DINOv2 和 policy backbone 的容量，不能把一次消融直接解释成普遍的 encoder 结论。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定语义/几何 encoder checkpoint、输入视角、空间下采样倍率、proprioception 是否使用、diffusion steps 和任务随机化。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 把语义与几何表示显式分支；在进入 policy 前做可控的 cross-attention 融合；把 token 数和 proprioception 作为单独变量做消融。
- **不能直接推出：** 它没有证明预测未来 latent 对操作一定有帮助，也没有提供 WAM 式长时域规划或 zero-shot goal-conditioned control。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 可继续测试将 VO-DP 的语义-几何 fuser 放到 JEPA-WAM 或 V-JEPA Policy 的 action-conditioned predictor 前后，观察几何信息是否改善 long-horizon prediction。

---

<a id="2512.24497-what-drives-jepa-wm"></a>
# What Drives Success in Physical Planning with Joint-Embedding Predictive World Models?

## 1. 基本信息
- 作者：Basile Terver, Tsung-Yen Yang, Jean Ponce, Adrien Bardes, Yann LeCun
- 单位：Meta FAIR；Inria Paris；École normale supérieure / PSL；New York University
- 日期：2025-12-30（arXiv v4）
- 链接：[arXiv](https://arxiv.org/abs/2512.24497) · [HTML](https://arxiv.org/html/2512.24497) · [代码/数据](https://github.com/facebookresearch/jepa-wms)
- 类型：JEPA-WM design study；DINO-WM / V-JEPA 2-AC comparison

## 2. 一句话摘要
系统研究 JEPA-WM 的 encoder、world-model architecture、training objective 和 planner，提出在 navigation 与 manipulation 上优于 DINO-WM 和 V-JEPA 2-AC 的组合 recipe。

## 3. 主要创新点
- 将 latent planning 设计拆为 encoder、transition model、loss、action representation 和 optimizer 等可控组件。
- 同时覆盖 simulated environments 与 real-world robotic DROID data。
- 比较 DINO-WM 与 V-JEPA-2-AC，并用 Spearman correlation 评估 validation metric 是否能预测 planning success。

## 4. 方法与训练信号
- 研究 DINO、V-JEPA/V-JEPA 2 等 visual encoder 的 frozen-feature world model。
- 比较 CEM、gradient descent 和 Nevergrad-style planning，及不同 rollout horizon/data scale。
- 推荐 recipe 按 navigation 与 real-world manipulation 分别选择。

## 5. Benchmark / 测评方法 / 结果
- 仿真：MetaWorld、Maze、Push-T、Wall；另有 RoboCasa Reach/Place。
- 真机/数据：DROID real-world videos；报告真实数据与 RoboCasa holdout 的 planning performance。
- Table 2 直接比较 best model、DINO-WM 和 V-JEPA-2-AC；另报告 2%/10%/50%/100% data scaling。

## 6. 可视化与表示分析
有 planned rollout 的 visual decoding、planner comparison、success-rate 与 validation metric 的 Spearman correlation，以及 image/video encoder 对比。

## 7. 真机实验与泛化
使用 DROID real-world robotic data 评估；重点是跨真实视频/仿真 holdout 的 planning transfer。需区分其“真实数据评估”与独立真实机器人闭环部署。

## 8. 与 OpenWAM 的关系
适合作为 OpenWAM 的系统性 ablation checklist：encoder、rollout loss、planner 和 validation metric 都应单独控制，而不是只报告一个最终 success。

## 9. 局限与待核对项
需补录最终推荐模型的逐任务 success、真机是否闭环执行、各 encoder 的 checkpoint 和每个 planner 的完整预算。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
这篇工作更像一项“实验诊断”而不是单一新模型。它问：JEPA world model 在真实物理规划中为什么有时成功、有时失败？到底是 encoder、预测 horizon、动作条件、数据、planner 还是 loss 在起作用？

### 10.2 读者可以先记住的类比
如果把 world model 看成驾驶模拟器，这篇论文不是再造一辆车，而是把轮胎、地图、传感器、驾驶策略逐项替换，找出哪一个部件决定了车辆能否到达目标。

## 11. 逐步读方法
### 11.1 数据流
编码器把视频和可选 proprioception 转成 latent；predictor 在动作条件下并行预测未来 latent；planner 采样动作序列并用 planning cost 排序，然后执行一段再重规划。论文围绕这条链路做受控对比，而不是只看一个最终 success 数字。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。JEPA loss 让预测 latent 接近真实未来表示；planning loss/采样策略决定预测误差如何转化成动作选择。关键点是 latent 的好坏必须用 downstream planning 验证，单独降低 representation loss 可能并不会降低控制失败率。

### 11.3 关键模块与张量含义
阅读时要把 encoder quality、dynamics accuracy、planning cost 和 physical execution 四层分开。论文的价值在于给出不同任务族的 recipe 和失败原因，而不是宣称一个固定架构在所有场景都最优。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。JEPA loss 让预测 latent 接近真实未来表示；planning loss/采样策略决定预测误差如何转化成动作选择。关键点是 latent 的好坏必须用 downstream planning 验证，单独降低 representation loss 可能并不会降低控制失败率。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
navigation 与 real-world manipulation 的对照用于观察任务结构差异；预测 horizon、proprioception、planner 和表示选择的消融用于定位瓶颈；若某项只改善 latent metric 却不改善 success，说明表示指标与控制指标存在脱节。

### 13.2 不要过度解读的地方
跨论文比较时必须对齐数据量、机器人平台、目标定义、planner 预算和是否使用 proprioception。不同任务上的 success 不能简单平均成“JEPA 好坏”。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：记录任务族、数据来源、输入模态、预测 horizon、planning cost、采样预算、是否重规划、真机/仿真边界及每个 ablation 的控制变量。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 把 world model 研究拆成可诊断的 encoder、predictor、planner 和 execution 四层；优先报告 planning-oriented evidence；为不同任务选择不同的训练 recipe。
- **不能直接推出：** 它不等于一个新的通用 WAM，也不能仅凭 recipe 证明某种 encoder 在所有机器人上都占优。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 后续可将这套诊断协议作为 OpenWAM 的统一 benchmark，避免只报告一张 success 表而无法知道失败发生在哪一层。

---

<a id="2604.06067-hipolicy-multifrequency"></a>
# HiPolicy: Hierarchical Multi-Frequency Action Chunking for Policy Learning

## 1. 基本信息
- 作者：Jiyao Zhang, Zimu Han, Junhan Wang, Xionghao Wu, Shihong Lin, Jinzhou Li, Hongwei Fan, Ruihai Wu, Dongjiang Li, Hao Dong。
- 单位：CFCS, School of Computer Science, Peking University；National Key Laboratory for Multimedia Information Processing, Peking University；Xi'an Jiaotong University；Tsinghua University；Beijing University of Aeronautics and Astronautics；Jingdong Technology Information Technology Co., Ltd。
- 日期：首次提交 2026-04-07；阅读版本 v1，更新于 2026-10-10。
- 链接：[arXiv](https://arxiv.org/abs/2604.06067) · [HTML](https://arxiv.org/html/2604.06067) · [PDF](https://arxiv.org/pdf/2604.06067)。
- 类型：**邻近相关；层级 observation feature fusion 与多频 action chunk policy**。

## 2. 一句话摘要
HiPolicy 从不同时间频率的 observation history 提取层级特征，同时预测不同频率的 action chunks，并通过 hierarchical FiLM、global feature fusion 和 entropy-guided execution 平衡长时规划与精细闭环控制。

## 3. 主要创新点
- 将 imitation policy 的 temporal resolution 分成多个频率，联合建模 coarse long-horizon actions 与 fine-grained reactive actions。
- 用对应频率的 observation features 条件化对应频率的 action chunks，并通过 cross-attention 做 global feature fusion。
- 推理阶段通过多次 stochastic sampling 估计 action entropy，自适应选择执行频率，降低固定高频执行的成本。

## 4. 方法与训练信号
- 从 raw observation chunk 中按不同频率抽取历史帧，经 observation encoder 得到 hierarchical observation features；视觉输入可为 2D images 或 3D point clouds，proprioception 可选。
- hierarchical FiLM 将每个频率的 observation feature 与同频 action feature 对齐；global feature fusion 跨频率做 attention 通信，再与 local features 拼接。
- 多频 noisy action chunks 拼接后由 1D-CNN U-Net diffusion model 预测噪声；训练目标仍是 diffusion policy 的 action denoising。

## 5. Benchmark / 测评方法 / 结果
**仿真：RoboTwin 1.0 与 RoboTwin 2.0，共 24 个 manipulation tasks。** DP/DP+HiPolicy 在 epoch 600、每任务 100 independent episodes 评测；DP3 变体遵循 DP3 protocol，在 epoch 3000、每任务 100 episodes 评测。Table 2/3 报告多频结构和 entropy-guided execution 消融；移除 hierarchical feature fusion 会造成约 6% 的性能下降。

**真实世界（Figure 5、Table 5）。** Franka Panda 7-DoF + Robotiq 2F-85，8 个 manipulation tasks，每任务平均 10 trials，并随机化 object initialization；相对 DP baseline，HiPolicy 报告 42% relative higher success rate 和 14% faster execution speed。

## 6. 可视化与表示分析
- Figure 3 展示 HiPolicy 总体结构、hierarchical observation features、FiLM fusion、global cross-frequency fusion 和多频 action chunks。
- Figure 4 展示 entropy-guided execution；Figure 5 展示 8 个真实机器人任务。
- Table 2/3/4 及 Appendix E.3 分析 hierarchical feature fusion、entropy sampling 次数、observation history、chunk size 和 frequency levels。

## 7. 真机实验与泛化
- 明确使用 Franka Panda、Robotiq 2F-85 和三台 ZED 系列相机；8 个真实世界任务，每任务 10 次评测，随机化初始物体。
- 仿真覆盖 RoboTwin 1.0/2.0；论文强调 long-horizon 与 high-precision tasks，但没有把它包装成独立的 encoder OOD benchmark。

## 8. 与 OpenWAM 的关系
HiPolicy 不使用 JEPA/DINO/V-JEPA 作为核心 encoder 贡献，主要贡献在 encoder 输出的 temporal multi-frequency feature fusion 和 action chunk policy。它适合迁移到 OpenWAM 的 action expert：把不同历史时间尺度的 latent features 分层，再比较 FiLM/cross-attention/global fusion 对 future prediction 和 action generation 的影响。

## 9. 局限与待核对项
- “多层/多频”主要是不同时间频率的 observation features，不等同于 frozen foundation encoder 的 transformer intermediate layer fusion；应与 GIFT、VO-DP、LeWAM AdaFuse 分开归类。
- 具体 visual encoder backbone、不同频率的 history 采样和所有 task-wise success 数值需参考 Appendix 与代码进一步核对。
- 当前已核对 Figure 3/4/5、Table 2/3/4/5 及真实世界硬件与评测协议。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
HiPolicy 关注执行节奏：策略并不总应该以相同频率执行动作。有些阶段需要快速修正，有些阶段可以一次执行更长的 action chunk。固定频率会在稳定阶段浪费推理，在接触和不确定阶段又可能反应太慢。

### 10.2 读者可以先记住的类比
它像一个会根据“自己有多犹豫”来决定说话速度的人：预测很确定时一次说一长句，预测不确定时缩短句子并更频繁确认环境。

## 11. 逐步读方法
### 11.1 数据流
模型接收分层的观测历史，同时预测不同时间尺度的 action chunks；通过多次采样估计 action entropy；执行器根据 entropy 选择高频或低频动作，并在下一次观测后重新判断。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。训练目标要求不同频率的动作预测都能解释演示行为；推理阶段的 entropy 不是额外的环境奖励，而是模型自身不确定性的代理。它可能把“多峰但合理的动作”误判为不确定，因此要结合执行成功和 action diversity 一起分析。

### 11.3 关键模块与张量含义
层级历史、multi-frequency action head、entropy estimator 和 adaptive execution 是四个可拆分模块。它不是 latent world model，核心贡献在 policy 的时间抽象与执行策略。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。训练目标要求不同频率的动作预测都能解释演示行为；推理阶段的 entropy 不是额外的环境奖励，而是模型自身不确定性的代理。它可能把“多峰但合理的动作”误判为不确定，因此要结合执行成功和 action diversity 一起分析。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
固定频率与自适应频率的比较回答动态执行是否有益；不同 entropy 阈值、chunk 长度和采样次数的消融回答收益来自策略本身还是额外推理预算；任务级 success 需要配合动作平滑性和推理延迟解释。

### 13.2 不要过度解读的地方
多次采样本身会增加计算量，因此不能只比较 success；必须报告 wall-clock latency、控制频率和实际执行的动作数量。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定历史长度、各频率 chunk horizon、采样次数、entropy 定义/阈值、控制周期、动作平滑后处理和硬件推理延迟。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 把 execution frequency 当作 policy 的一等公民；用不确定性决定 action chunk 长度；在评测中同时报告成功率和实时性。
- **不能直接推出：** 它没有说明未来 latent prediction 是否必要，也没有证明 entropy 在不同 embodiment 上都是可靠的不确定性指标。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 可将 HiPolicy 的自适应执行器接在 JEPA-WAM 或 PLaW-VLA 后，测试预测不确定性是否能更可靠地触发 replanning。

---

<a id="2605.06388-reconstruction-or-semantics"></a>
# Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models

## 1. 基本信息
- 作者：Nilaksh, Saurav Jha, Artem Zholus, Sarath Chandar
- 单位：Chandar Research Lab；Mila – Quebec AI Institute；Polytechnique Montréal；Canada CIFAR AI Chair
- 日期：2026-05-07（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2605.06388) · [HTML](https://arxiv.org/html/2605.06388) · [项目页](https://hskalin.github.io/semantic-wm/)
- 类型：encoder comparison；semantic latent WAM/policy evaluation

## 2. 一句话摘要
在 BridgeV2 固定 transition model、action conditioning 和数据协议下比较 VAE、Cosmos、V-JEPA 2.1、Web-DINO、SigLIP 2 等 latent encoder，分析 visual fidelity、planning 和 downstream policy 的关系。

## 3. 主要创新点
- 证明 visual reconstruction quality 不能单独作为 robotic world-model 选择标准。
- 将 encoder 质量拆成 visual fidelity、planning/downstream policy、latent representation quality 三个轴。
- 发现 semantic encoders（尤其 V-JEPA 2.1、Web-DINO、SigLIP 2）在 policy-relevant 指标上通常优于 reconstruction latent。

## 4. 方法与训练信号
- 固定 DiT world-model architecture，只替换 encoder/decoder path；部分 semantic encoder 使用 S-VAE adapter。
- 测试 DiT-S/B/L 多个规模、single/multi-view、CEM 与 inverse-dynamics probe。
- 用 VLM judge 评估 trajectory success，并报告 bootstrap confidence interval。

## 5. Benchmark / 测评方法 / 结果
- BridgeV2 world-model training/evaluation；包含 ID、OOD distractor、OOD instruction 以及 policy-in-the-loop episodes。
- 指标：PSNR/SSIM/LPIPS/t-LPIPS/FID/FVD、CEM controllability error、ID/OOD success、IDM action-recovery Pearson r、success-probe accuracy。
- DiT-L 的 per-instruction policy 表比较 V-JEPA 2.1、Web-DINO、VAE、Cosmos、SigLIP 2；semantic encoder family 在 policy-facing metrics 更强。

## 6. 可视化与表示分析
有 latent-space overview、OOD distractor/instruction rollout、per-instruction success、encoder-ceiling drop、inverse-dynamics recovery 和 representation quality 分析。

## 7. 真机实验与泛化
重点是 BridgeV2 policy-in-the-loop / OOD evaluation；是否包含真正硬件闭环需按正文区分，不能将 VLM-judged episodes 直接写成真机实验。

## 8. 与 OpenWAM 的关系
这是最适合 OpenWAM 做 encoder ablation 的协议参考：用相同 WAM/policy head 对比 V-JEPA、DINO、VAE 等，并同时报告 latent quality、planning 和 policy success。

## 9. 局限与待核对项
需补录 BridgeV2 的真实/仿真比例、每个 OOD 设置 episodes、V-JEPA 2.1/Web-DINO checkpoint 和硬件部署信息。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
这篇论文追问 latent world model 最容易被忽略的选择：latent 到底应该像素级可重建，还是应该保留对任务和语义有用的信息？重建目标偏好视觉细节，语义目标偏好可区分的状态，但控制真正需要的是“动作后果相关的信息”。

### 10.2 读者可以先记住的类比
像给机器人一张地图：重建型 latent 试图保存地图上的每块纹理，语义型 latent 更像只保存道路、障碍物和可通行区域；好的控制表示还要保证地图上的路线变化与真实动作后果一致。

## 11. 逐步读方法
### 11.1 数据流
论文固定 transition model、action conditioning 和训练数据，只更换 encoder、可选 compression adapter 及 decoder path，再比较 latent diffusion rollout、VLM judge 和 policy performance。这样把“表示接口”的影响从 transition model 影响中隔离出来。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。重建 loss 让 latent 能恢复视觉内容，语义/预训练表示则提供对象和状态结构；最终的 action-conditioned prediction 约束 latent 具有可预测的动力学。每一种 loss 都可能丢失另一类信息，因此需要用 rollout quality 和 action success 共同判断。

### 11.3 关键模块与张量含义
实验设计的关键不是某个新 policy，而是固定下游模型后替换表示接口。阅读时要关注 encoder、compression adapter、decoder 和 transition model 的边界，否则容易把表示优劣误归因给模型容量。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。重建 loss 让 latent 能恢复视觉内容，语义/预训练表示则提供对象和状态结构；最终的 action-conditioned prediction 约束 latent 具有可预测的动力学。每一种 loss 都可能丢失另一类信息，因此需要用 rollout quality 和 action success 共同判断。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
latent reconstruction、语义评测、trajectory visual quality 和 downstream policy 共同回答“哪种 latent 更适合机器人世界模型”；VLM judge 的结果适合做语义/轨迹可读性证据，但不能单独替代真实控制指标。

### 13.2 不要过度解读的地方
不同 encoder 的预训练数据、尺度和 token 数可能不完全匹配；VLM judge 也可能偏好更容易描述的轨迹。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 transition model、action conditioning、数据和训练预算；记录 encoder checkpoint、latent 尺寸、adapter、decoder、rollout horizon 和 judge protocol。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 在相同 transition/policy 下比较 encoder interface；同时测重建、语义、动态预测和控制；显式检查 compression adapter 的作用。
- **不能直接推出：** 语义 latent 并不自动保证动作可控；更好的可视化或 VLM 评分不等于更高的 real-robot success。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 值得进一步研究能否用 action-oriented supervision 学到同时具备语义稳定性和动力学精度的 latent。

---

<a id="2605.07079-rla-wm"></a>
# Learning Visual Feature-Based World Models via Residual Latent Action

## 1. 基本信息
- 作者：Xinyu Zhang, Zhengtong Xu, Yutian Tao, Yeping Wang, Yu She, Abdeslam Boularias
- 单位：Rutgers University；Purdue University；University of Wisconsin–Madison
- 日期：2026-05-08（arXiv v2）
- 链接：[arXiv](https://arxiv.org/abs/2605.07079) · [HTML](https://arxiv.org/html/2605.07079) · [项目页](https://mlzxy.github.io/rla-wm)
- 类型：DINO feature world model + minimalist WAM/policy

## 2. 一句话摘要
从 DINO feature residual 中学习 Residual Latent Action（RLA），用 flow matching 预测 RLA，并将其用于 world-action modeling、VLA 改善和 offline visual RL。

## 3. 主要创新点
- RLA 从 DINO residual 中提取，编码 temporal progression 和 action effect。
- RLA-WM 避免直接回归高维 future feature 导致的模糊/塌缩。
- 提出 actionless video 学习的 minimalist WAM，改善 VLA 与 real-robot control。
- 另提出完全在 offline-video world model 内训练的 visual RL，不需要 online interaction。

## 4. 方法与训练信号
- frozen/feature-based visual state 与 action 输入 flow-matching predictor。
- 评估 future frame prediction、planning、policy learning 和 world-model visual reward。
- 对比 feature-based world model 与 video-diffusion world model 的质量和速度。

## 5. Benchmark / 测评方法 / 结果
- 仿真与 real-world datasets；报告 LPIPS、SSIM、DINO L1、pixel L1 和 FLOPs。
- RLA-WM 在 feature prediction 与 planning 上超过比较的 feature-based/video-diffusion baselines，并显著降低推理成本。
- minimalist WAM 改善 LIBERO VLA；完整 task-wise success 和真机表格应以正文实验表为准。

## 6. 可视化与表示分析
有 RLA residual、future feature prediction、planning rollout 和 speed/quality 对比；重点分析 latent action 的时间进展属性。

## 7. 真机实验与泛化
摘要确认包含 real-world datasets 和 real-robot policy improvement；具体平台、任务和 OOD 变量需按项目页/正文实验表区分，不将其泛化为 zero-shot。

## 8. 与 OpenWAM 的关系
非常适合做 OpenWAM 的 DINO-residual auxiliary baseline：比较直接 future latent prediction、RLA prediction 和 action-conditioned flow matching 的差异。

## 9. 局限与待核对项
需要补录 exact robot platform、LIBERO protocol、真实机器人 trials、数据是否 actionless，以及各 world-model baseline 的统一计算预算。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
RLA-WM 试图让 visual world model 不只做预测，还能在离线视频中学习如何选择动作。它的关键思路是把动作对 latent 的影响显式分解成 residual，让模型更容易学习“执行某个动作相对于当前状态改变了什么”。

### 10.2 读者可以先记住的类比
把每个动作看成在当前状态地图上画一个箭头：不是重新画整张地图，而是预测这个箭头会把状态推向哪里。world model 提供想象环境，visual RL 再在想象中试动作。

## 11. 逐步读方法
### 11.1 数据流
视觉观测经过预训练特征 encoder；residual latent action 模块将动作影响编码为状态变化；transition/world model 预测后续 latent；offline visual RL 在这个模型内优化 policy，必要时通过 planner 或 imagined rollout 选择动作。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。residual prediction 让动作与 latent 变化对齐，world-model loss 约束多步 rollout，RL objective 则偏向高回报行为。三者之间可能存在模型利用错误：policy 可能找到 world model 的漏洞，因此必须报告真实环境或 held-out dynamics 上的验证。

### 11.3 关键模块与张量含义
这篇工作同时涉及 encoder、residual dynamics 和 imagined policy learning。它与普通 latent planning 的区别在于 policy 训练也发生在 learned model 内，而不只是测试时搜索动作。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。residual prediction 让动作与 latent 变化对齐，world-model loss 约束多步 rollout，RL objective 则偏向高回报行为。三者之间可能存在模型利用错误：policy 可能找到 world model 的漏洞，因此必须报告真实环境或 held-out dynamics 上的验证。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
不同 residual/action representation 的消融回答动作建模是否更容易；visual RL 与 offline planning 的比较回答模型是否支持策略改进；任务成功率必须结合 held-out rollout 和 model error 分析。

### 13.2 不要过度解读的地方
在模型内训练出的 policy 可能过拟合模型误差；若没有足够的真实环境验证，不能把 imagined return 当成真实控制效果。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 offline 数据覆盖、feature encoder、residual parameterization、rollout horizon、RL algorithm、模型更新频率及 held-out evaluation。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 显式建模 action-induced residual；把 offline world model 用作 policy learning substrate；同时设置模型外评测来检查 exploitation。
- **不能直接推出：** 它没有证明离线视频 world model 可以无偏地替代真实环境，也不保证 residual 在大幅动作或长 horizon 上稳定。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 重要方向是研究 uncertainty-aware imagined rollout，限制 policy 利用 latent dynamics 的系统性误差。

---

<a id="2608.09381-jepa-wam-joint"></a>
# JEPA-WAM: Learning Vision-Language-Action Policies with Joint-Embedding World Modeling

## 1. 基本信息
- 作者：Yihan Lin, Jiawei He, Shifeng Bao, Chen Zhao, Yang Li, Xiaobo Wang, Yan Wang, Cheng Chi, Jing Zhang
- 单位：School of Information, Renmin University of China；XYZ Embodied AI；Key Laboratory of Data Engineering and Knowledge Engineering；Engineering Research Center of Database and Business Intelligence；Shenzhen University of Advanced Technology；Institute for AI Industry Research (AIR), Tsinghua University
- 日期：2026-08-10（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2608.09381) · [HTML](https://arxiv.org/html/2608.09381) · [项目页](https://spritewithoutice.github.io/JEPA_WAM/)
- 类型：直接相关；latent JEPA-WAM

## 2. 一句话摘要
在冻结 V-JEPA 2.1 latent space 中构造 spatially structured joint current–future target，用共享 predictor 同时学习 latent transition 和 continuous action generation。

## 3. 主要创新点
- transition prediction 与 action generation 共享 predictor，避免预测分支与动作表征分离。
- joint current–future target 保留 dense patch correspondence，而非只预测全局未来 latent。
- transition supervision 直接塑造用于 action prediction 的 backbone。
- 同一监督方式可迁移到 pretrained π0.5，同时保留原始 perception/action pathway。

## 4. 方法与训练信号
- frozen V-JEPA 2.1 encoder；多视角视觉 token 构造联合当前-未来 target。
- target branch 仅训练时使用；部署时只保留 predictor/action pathway。
- 采用 continuous action generation，并比较无 robot-policy pretraining 与 pretrained VLA 两组设置。

## 5. Benchmark / 测评方法 / 结果
- LIBERO：无大规模 robot-policy pretraining 的 JEPA-WAM 平均 96.7%；π0.5 + JEPA objective 平均 97.8%。
- LIBERO-Plus：按 Camera、Robot initial state、Language、Light、Background、Noise、Layout 分组；JEPA-WAM 平均 79.2%，π0.5 + JEPA objective 86.3%。
- RoboTwin 2.0：20 tasks，Clean/Random；JEPA-WAM 全任务平均 79.9%/36.9%，π0.5 + JEPA objective 84.6%/37.5%。
- 真机任务：Bread placement、Fruit placement、Three-block placement、Three-block stacking、Drawer manipulation；每 task/setting 10 rollouts，报告 normalized completion score。

## 6. 可视化与表示分析
有 joint target 的 temporal-gap decoding、patch-wise correlation、trajectory residual/endpoint displacement 分析；还报告 inference latency/frequency 和 target construction ablation。

## 7. 真机实验与泛化
- 真机为双臂 manipulation；5 个任务覆盖放置、堆叠、抽屉多阶段操作。
- 同时测 ID 与视觉/空间 OOD；每个 task/setting 10 rollouts。
- OOD 具体协议与逐任务分数应以 Table 15 和 Appendix E 为准；这比单纯 randomized simulation 更接近真机泛化。

## 8. 与 OpenWAM 的关系
这是最直接的结构性参照之一：可用于比较 OpenWAM 是否需要 joint current–future target、dense patch correspondence 和共享 transition/action predictor。

## 9. 局限与待核对项
需补录 Table 15 的 ID/OOD 逐任务 normalized completion score，以及各 baseline 的真机逐项结果和训练预算。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
JEPA-WAM 的目标是把“预测未来”从辅助任务变成动作策略的一部分。普通 policy 根据当前观测直接输出动作，容易在长时域任务中缺少对未来状态的显式判断；本文让模型先在 joint-embedding space 预测未来，再用未来表示帮助 action generation。

### 10.2 读者可以先记住的类比
它像一个下棋者：不是看到当前棋盘就立刻落子，而是先想象几步之后的局面，再选择当前动作。latent 不是要生成漂亮视频，而是保留足以指导动作的未来状态信息。

## 11. 逐步读方法
### 11.1 数据流
视觉/语言/历史观测先编码成 joint latent；action-conditioned predictor 预测未来 latent；policy head 使用当前与未来表示生成 action chunk；执行后获得新观测，再循环预测。应特别区分 teacher-forcing 训练看到的真实未来和部署时只能依赖预测未来。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。联合 embedding prediction 提供未来状态监督，action imitation 或 action loss 让预测表示服务于动作生成。若只优化未来预测，latent 可能对控制不敏感；若只优化动作，future branch 可能退化成旁路，因此需要 ablation 验证两者是否互相贡献。

### 11.3 关键模块与张量含义
核心模块是 joint encoder、future predictor 和 action head。它与“先训练 world model、再接 planner”不同，更接近 policy 内部集成的 WAM。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。联合 embedding prediction 提供未来状态监督，action imitation 或 action loss 让预测表示服务于动作生成。若只优化未来预测，latent 可能对控制不敏感；若只优化动作，future branch 可能退化成旁路，因此需要 ablation 验证两者是否互相贡献。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
主结果回答联合未来预测是否改善 policy；未来 horizon、loss 权重和是否使用 language 的消融回答真正起作用的路径；长时域任务和 OOD 物体/指令测试未来表示是否提升泛化。

### 13.2 不要过度解读的地方
action success 提升可能来自额外参数或训练数据，而不一定来自 future latent；比较时要对齐 backbone、数据和推理 steps。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 encoder 是否冻结、历史长度、future horizon、action chunk、loss 权重、语言条件、teacher forcing/scheduled sampling 和推理延迟。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 把 future latent 作为 action policy 的显式条件；训练时同时约束 representation prediction 和 action imitation；部署时保持预测闭环。
- **不能直接推出：** 未来表示更准确不必然代表动作更好；若没有 matched baseline 和 horizon ablation，不能断言 JEPA 是收益来源。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 可进一步研究预测未来 token 的数量、空间粒度和不确定性如何影响动作头，及其与 diffusion/flow policy 的组合。

---

<a id="2609.04193-gift-intermediate-feature"></a>
# GIFT: Guided Intermediate Feature Training via Action-Oriented Structural Supervision for Robotic Manipulation

## 1. 基本信息
- 作者：Yupeng Zheng, Xiang Li, Songen Gu, Yuhang Zheng, Shuai Tian, Weize Li, Linbo Wang, Chaoyue Li, Qichao Zhang, Haoran Li, Zhongpu Xia, Ya-Qin Zhang, Shuicheng Yan, Dongbin Zhao。
- 单位：Institute of Automation, Chinese Academy of Sciences；University of Chinese Academy of Sciences；National University of Singapore；Tsinghua University；Fudan University（作者页列出的单位集合）。
- 日期：首次提交 2026-09-03；阅读版本 v1，更新于 2026-10-10。
- 链接：[arXiv](https://arxiv.org/abs/2609.04193) · [HTML](https://arxiv.org/html/2609.04193) · [PDF](https://arxiv.org/pdf/2609.04193) · [项目页](https://openphoenix-team.github.io/GIFT-pages)。
- 类型：**直接相关；面向 VLA 与 WAM 的中间视觉特征监督框架**。

## 2. 一句话摘要
GIFT 不规定统一的 action head，而是用 geometry alignment、affordance prediction 和 goal-region reconstruction 训练共享于动作路径的中间视觉特征，使 VLA、Fast-WAM 和 inverse-dynamics WAM 保留更有控制价值的结构信息。

## 3. 主要创新点
- 将机器人控制中的中间特征结构化为几何、可供性和目标区域三类监督，形成跨架构的统一训练原则。
- 在语义中心的 VLA、直接动作扩散 Fast-WAM 和 inverse-dynamics WAM 三种 action formulation 上实例化同一方法。
- 对比 injection / no-injection 设计，区分“改善中间特征”与“把辅助预测直接喂给 action head”的贡献；no-injection 版本更好，支持特征内化解释。

## 4. 方法与训练信号
- GIFT 直接监督 action pathway 使用的 intermediate visual features，而不是固定某种 decoder 或动作头；正文 Section 3 明确强调其 architecture-flexible 设计。
- geometry guidance 对齐运动可行性相关的场景结构；affordance guidance 预测 instruction-relevant entities 与 object-centric end-effector 配置；goal guidance 重建由语言指令确定的目标区域。
- 三类约束在训练期施加，推理时比较是否将辅助预测注入 action head；目标是让中间表示本身保留控制相关信息。

## 5. Benchmark / 测评方法 / 结果
**LIBERO-Plus，标准 LIBERO 训练后 zero-shot transfer，七类 distribution shifts（摘要与 Table II）。** GIFT-VLA、GIFT-WAM-Fast、GIFT-WAM-IDM 分别达到 79.6%、72.6%、87.8%，相对匹配 baseline 提升 4.6、12.6、5.2 个百分点。

**RoboCasa（Table III）。** GIFT-VLA、GIFT-WAM-Fast、GIFT-WAM-IDM 分别达到 61.4%、83.6%、82.3%；WAM 变体相对对应 baseline 提升 9.0 和 8.4 个百分点。LIBERO 的标准 ID 结果见 Table I，geometry/affordance/goal 消融见 Table IV。

## 6. 可视化与表示分析
- Figure 2 展示 GIFT 在 VLA 与两种 WAM action formulation 上的整体框架。
- Figure 3 对比 injection 与 no-injection 变体；正文还分析 geometry、affordance、goal 三类监督的独立与组合消融。
- Figure 5 可视化 action-to-vision attention，分析中间特征对控制相关区域的关注。

## 7. 真机实验与泛化
- 论文摘要提到 high-precision real-world manipulation，但当前可核对的主要定量协议集中在 LIBERO、LIBERO-Plus 与 RoboCasa；独立真机平台、任务数和 trial-level success rate 在本卡片中标为待核对。
- 已确认的泛化轴是 LIBERO-Plus 的七类视觉/空间 distribution shifts，以及 RoboCasa 的不同 embodiment、视觉域和交互动力学。

## 8. 与 OpenWAM 的关系
这是目前最直接的“中间特征监督”路线之一：不改写 OpenWAM 的动作生成范式，而是给共享 encoder/predictor 的中间表示增加几何、可供性和目标区域约束。可作为 OpenWAM 的 auxiliary representation loss、feature probing 和 no-injection ablation 基线。

## 9. 局限与待核对项
- 不同 policy configuration 的 encoder、数据规模和 action head 细节需要按 Appendix 逐项对齐，不能只比较摘要中的总成功率。
- 当前卡片已核对摘要、方法、Figure 2/3/5、LIBERO/LIBERO-Plus/RoboCasa 结果；真机平台与完整 success 协议待继续核对。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
GIFT 解决的是策略网络内部表征“知道什么但不会用”的问题。很多 VLA/policy 的中间视觉 token 已经包含几何和对象信息，却没有被动作 loss 充分塑形；GIFT 用动作相关的辅助监督引导这些中间 token。

### 10.2 读者可以先记住的类比
像训练学生时不仅看最终答案，还要求他在草稿中标出物体位置、可达区域和几何关系；这些草稿不直接替他写动作，但会让最终答案更稳定。

## 11. 逐步读方法
### 11.1 数据流
观测、指令和 robot state 进入 policy；在中间视觉 token 上附加几何对齐、object-centric affordance 和 instruction-conditioned goal-region 预测；默认 no-injection 设计不把辅助预测结果直接喂给 action head，只通过梯度改变共享表示。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。辅助目标分别约束几何、可操作性和指令相关目标区域，action loss 仍负责最终行为。no-injection 的重要性在于它测试的是“representation shaping”而不是额外输入；但辅助标签质量和任务相关性会影响收益。

### 11.3 关键模块与张量含义
GIFT 可以叠加在 VLA、WAM 或其他 action policy 上，贡献位置是 intermediate feature supervision，而不是新的 world model。阅读时要区分 auxiliary head 在训练时存在、推理时移除的事实。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。辅助目标分别约束几何、可操作性和指令相关目标区域，action loss 仍负责最终行为。no-injection 的重要性在于它测试的是“representation shaping”而不是额外输入；但辅助标签质量和任务相关性会影响收益。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
VLA 和两类 WAM formulation 的结果验证方法是否跨架构；去掉几何/affordance/goal-region 分支的消融定位贡献；OOD 物体、空间配置和指令测试辅助监督是否改善泛化。

### 13.2 不要过度解读的地方
辅助监督需要额外标注或 teacher model；若 teacher 与评测分布相关，收益可能不是纯粹的表示泛化。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定插入层、teacher model、辅助标签生成、loss 权重、是否 injection、policy backbone 和所有 OOD 划分。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 在中间 token 上做 action-oriented auxiliary supervision；采用 no-injection 设计保持推理开销；分别消融每种结构性目标。
- **不能直接推出：** 更强的中间表示不等于 world model 更准确，也不意味着辅助 head 可以在没有 action supervision 时独立产生策略。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 可测试 GIFT 监督是否能改善 JEPA future token 的可控性，或能否减少 WAM 对大规模机器人预训练的依赖。

---

<a id="2609.09630-jepa-policy"></a>
# JEPA Policy: Diffusion-Free Imitation Learning via Paired Action and Future Representation Prediction

## 1. 基本信息
- 作者：Jie Xu, Kangjin Yu, Ziyi Jin, Junjie Gao, Liqing Chen, Yixian Li, Shuai Tian, Zhongpu Xia
- 单位：Anyverse Dynamics
- 日期：2026-09-09（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2609.09630) · [HTML](https://arxiv.org/html/2609.09630)
- 类型：直接相关；JEPA-style future representation policy

## 2. 一句话摘要
将 action chunk 与其观测到的 future representation 作为配对训练目标，在共享 Transformer 中联合预测，得到无需扩散采样的低延迟 imitation policy。

## 3. 主要创新点
- future representation prediction 直接约束 action generation，而非只加独立 auxiliary head。
- dual-branch 与 gradient-routing ablation 用于区分共享拓扑和辅助损失的贡献。
- 训练/推理不依赖 diffusion policy 的迭代采样。
- future-prediction error 可作为 task-conditioned failure-ranking signal。

## 4. 方法与训练信号
- action token 与 future-representation token 在共享 Transformer 中交互。
- 两次 forward refinement；无单独 dynamics rollout，也不重建未来图像。
- LIBERO 使用 action horizon 16；robomimic/MimicGen 使用 horizon 10，执行前 8 个 action 后重规划；20 Hz action、2.5 Hz replanning。

## 5. Benchmark / 测评方法 / 结果
- LIBERO：MokaMoka、MugMug。
- robomimic：Square PH、Tool Hang PH、四相机 Transport PH。
- MimicGen：Coffee Preparation D1、Kitchen D1、Three Piece Assembly D1、Hammer Cleanup D1。
- 共 9 个仿真任务；三 seeds（41/42/43），报告 30 次评估中的 best-checkpoint success rate。
- 九任务平均：JEPA Policy 83.0%，action-only MIP 77.4%，Diffusion Policy 75.1%；相对 MIP +5.6 pp。
- 论文同时报告 last-checkpoint / checkpoint-selection protocol，指出绝对 success 会下降，但相对增益仍约 +4.7 至 +5.6 pp。
- 物理机器人：5 tasks、630 episodes；整体排序与仿真一致。

## 6. 可视化与表示分析
有训练曲线、future-prediction error 分析、representation-collapse audit，以及误差对失败排序的诊断信号。

## 7. 真机实验与泛化
- 类型：五项 physical-robot manipulation study：Cabinet、Cup Stack、Cup Upright、Plate Grape、Pen Insert。
- 63 sessions、630 episodes，无排除；每个 task 使用三个 checkpoint/arm，名义上 10 episodes/cell；实验在单一实验室、单一机器人和单一 operator 上完成。
- 重点是低延迟和跨任务排序复现；当前正文摘要未显示系统性的 unseen object/layout 真机泛化矩阵，需区别于仿真任务泛化。

## 8. 与 OpenWAM 的关系
适合作为 OpenWAM 的 diffusion-free action head 和 future-loss 诊断基线；也可用于比较 future prediction 是否必须经过完整 WAM 才能改善 policy。

## 9. 局限与待核对项
仍需补录 Table XI 的逐任务 success 数值；论文明确说明该 hardware study 没有系统的物体/光照/布局 OOD 矩阵，因此不能将其写成真机泛化验证。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
JEPA Policy 试图去掉 diffusion policy 的多步去噪，把 imitation learning 改写成“同时预测动作和未来表示”。直觉是：如果动作会把当前场景推向某个未来状态，那么未来状态预测可以帮助模型筛掉不合理动作。

### 10.2 读者可以先记住的类比
普通 policy 像看到路口直接转弯；JEPA Policy 像先想象转弯后的画面，再检查这个未来是否符合任务，最后输出动作。它不需要在推理时反复 denoise，而是用一次或少数几次 forward 完成 refinement。

## 11. 逐步读方法
### 11.1 数据流
当前视觉观测和任务条件编码成 representation；动作分支预测 action chunk，future branch 预测 paired future representation；两者在 refinement 中互相约束，并可用 future-prediction error 对候选行为做 failure ranking。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。action loss 保证模仿演示，future representation loss 保证动作和未来状态成对一致。future error 可作为筛选信号，但它依赖表征空间的质量：如果未来 latent 对任务无关，低误差也不表示动作正确。

### 11.3 关键模块与张量含义
论文的重点是 diffusion-free policy head 与 paired action/future prediction，不是一个独立的 planner。两次 forward refinement 和 failure ranking 是推理侧机制，必须与训练目标分开读。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。action loss 保证模仿演示，future representation loss 保证动作和未来状态成对一致。future error 可作为筛选信号，但它依赖表征空间的质量：如果未来 latent 对任务无关，低误差也不表示动作正确。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
与 diffusion policy 的成功率、推理步数和延迟比较回答“是否可以更快”；paired/unpaired future、refinement 和 ranking ablation 回答未来监督是否真正作用于 policy；应同时看长时域和 OOD 任务。

### 13.2 不要过度解读的地方
更少的 forward steps 不自动等于更低的端到端延迟，还要考虑 encoder、候选动作数量和后处理；future error 也可能与任务 success 不一致。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 action chunk、future horizon、refinement 次数、候选数、encoder 冻结状态、diffusion baseline steps 和真实 wall-clock latency。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 用 action-future pair 训练 policy；把预测误差用作低成本的行为一致性检查；用 diffusion-free head 降低推理复杂度。
- **不能直接推出：** 它没有证明 JEPA policy 在所有任务上优于 diffusion，尤其不能忽略 diffusion policy 的动作多峰建模能力。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 值得研究 future prediction 是否可以与 uncertainty calibration 结合，把 failure ranking 变成可靠的在线风险估计。

---

<a id="2609.10506-duet-dino"></a>
# DUET-DINO: Simultaneous Cross-View World Modeling for Latent Planning in Robot Manipulation

## 1. 基本信息
- 作者：Nisarga Nilavadi, Ralf Römer, Moritz Reuss, Michael Krawez, Tobias Jülg, Angela P. Schoellig, Rudolf Lioutikov, Wolfram Burgard
- 单位：Artificial Intelligence and Robotics Lab, University of Technology Nuremberg；Learning Systems and Robotics Lab, Technical University of Munich；Intuitive Robots Lab, Karlsruhe Institute of Technology；NVIDIA；Robotics Institute Germany
- 日期：2026-09-09（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2609.10506) · [HTML](https://arxiv.org/html/2609.10506) · [项目页](https://utn-air.github.io/DUET-DINO)
- 类型：DINOv3/V-JEPA 2 cross-view latent world model

## 2. 一句话摘要
联合建模 side camera 与 wrist camera 的 action-conditioned latent dynamics，用 cross-view conditioning 支持完整 7-DoF manipulation planning。

## 3. 主要创新点
- 同时学习 global scene 与 gripper-centric local information，而不是独立训练两个视角。
- 针对细粒度空间/旋转 action 在单视角 latent prediction 中不可靠的问题设计 cross-view world model。
- 比较 V-JEPA 2 与 DINOv3，发现 DINOv3 更能捕捉 fine-grained action-conditioned scene change。

## 4. 方法与训练信号
- 使用 DROID 与 RoboArena 数据，从 scratch 训练 cross-view latent predictor。
- latent planning 在完整 7-DoF action space 中执行；任务包含 reach、angled reach、multi-goal grasp-and-lift。
- 与 single-view、independent dual-view baselines 比较。

## 5. Benchmark / 测评方法 / 结果
- RoboLab simulator：spatially diverse reach、orientation-intensive angled-reach、multi-goal lift。
- success rate：Reach 92.0%、Angled Reach 72.5%、Lift 60.0%。
- 报告 visual distribution shifts 下的鲁棒性，并比较 DINOv3 与 V-JEPA 2 的 downstream planning。

## 6. 可视化与表示分析
有 cross-view prediction、fine-grained action rollout 和不同 encoder 对 scene-change 捕捉能力的可视化/定性对比。

## 7. 真机实验与泛化
摘要重点是 simulator 与 dataset-level visual shifts；是否包含 physical robot deployment、平台和 trials 需以正文最终实验段落核对，不能仅凭项目页推断。

## 8. 与 OpenWAM 的关系
直接对应 OpenWAM 的多相机融合和 encoder choice：可以比较 shared temporal mixer、独立 view encoder 和 cross-view latent target 对 7-DoF 控制的影响。

## 9. 局限与待核对项
需补录 real-robot 是否存在、DROID/RoboArena 数据规模、每个 benchmark 的 episode 数和 DINOv3 具体版本。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
DUET-DINO 解决多视角机器人规划中的两个问题：不同相机看到的状态如何对齐，以及 world model 是否能同时保持跨视角一致性和动作可预测性。单视角表示可能遮挡关键物体，多视角直接拼接又会带来 token 和冗余。

### 10.2 读者可以先记住的类比
像两个人从房间不同角落描述同一个搬运过程：模型要先判断他们说的是同一个物体和同一个时刻，再预测动作之后两个人各自会看到什么。

## 11. 逐步读方法
### 11.1 数据流
多视角图像分别经过 DINO 特征提取；cross-view/world-model 模块联合建模视角关系和动作条件未来；planner 在 latent trajectory 上搜索动作，并通过执行后的新观测继续修正。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。跨视角一致性约束让同一状态在不同相机下有可对齐表示，action-conditioned prediction 约束 latent 随动作变化。两种目标可能冲突：过度不变会丢失视角相关的遮挡信息，因此需要看跨视角 ablation 和遮挡场景。

### 11.3 关键模块与张量含义
关键边界是 DINO encoder、跨视角融合、latent predictor 和 planner。它更偏 world-model/planning，而不是直接 action policy；多视角输入的计算预算也是公平比较的一部分。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。跨视角一致性约束让同一状态在不同相机下有可对齐表示，action-conditioned prediction 约束 latent 随动作变化。两种目标可能冲突：过度不变会丢失视角相关的遮挡信息，因此需要看跨视角 ablation 和遮挡场景。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
跨视角、视角缺失和 latent planning 结果回答多视角是否真正改善可观测性；单视角、拼接和 cross-view ablation 区分收益来自更多像素还是更好的融合。

### 13.2 不要过度解读的地方
多相机系统可能拥有比 baseline 更多信息；必须记录相机数量、视角是否固定、遮挡分布和推理 token 数，避免把信息优势当成算法优势。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定相机数量/标定、DINO checkpoint、视角 dropout、融合 token 数、预测 horizon、planner budget 和遮挡设置。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 将多视角一致性和 action-conditioned prediction 联合训练；对视角缺失做测试；把遮挡作为专门泛化轴。
- **不能直接推出：** 跨视角 latent 一致并不保证多步动作规划成功，也不代表可以无成本扩展到任意数量相机。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 可把 DUET-DINO 的跨视角 latent 与 V-JEPA/JEPA predictor 结合，研究多视角是否降低未来预测不确定性。

---

<a id="2609.20277-jepa-wam-visual-instruction"></a>
# JEPA-WAM: Connecting Generated Visual Instructions to World Action Models through JEPA Latent Representations

## 1. 基本信息
- 作者：Tianbin Liu, Jian Zhu, Taiyi Su, Jianjun Zhang, Chong Ma, Zitai Huang, Yi Xu
- 单位：论文 HTML 正文未提供作者 affiliation 字段；单位暂记为“未公开/待 PDF 首页核对”，不据作者或项目名推断。
- 日期：2026-08-04（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2609.20277) · [HTML](https://arxiv.org/html/2609.20277)
- 类型：直接相关；visual-instruction-conditioned JEPA-WAM

## 2. 一句话摘要
用文本生成器为每条 instruction 生成视觉完成假设，再用 frozen V-JEPA 2.1 编码成 dense goal tokens，同时条件化 video/action experts，强化 WAM 的 instruction following。

## 3. 主要创新点
- 用 generated visual-instruction bank 补充稀疏、重复的轨迹级语言标注。
- V-JEPA 2.1 将生成图像中的任务语义与外观/布局 nuisance 解耦，并保留空间结构。
- 不训练图像生成器；通过 cross-attention 让 compact goal tokens 条件化 video/action experts。
- 构建 ID、scene OOD 和 instruction OOD 的真机 benchmark。

## 4. 方法与训练信号
- 每条文本 instruction 采样多张 task-completion image；默认 visual-instruction bank 为 1,024 张。
- V-JEPA 2.1 dense representations 经 learnable projector 压缩为 goal tokens。
- 与 real demonstration keyframe bank（KF-64）和不同规模 generated bank（J-64/J-512/J-1024）比较。

## 5. Benchmark / 测评方法 / 结果
- 真机 benchmark：11 个行为相关任务，包括 Give bread/pear/egg/carrot、PnP car/bread/carrot/egg/pear、Sort toys、Wipe table。
- ID 平均 success：π0 30.0%，Fast-WAM 77.3%，JEPA-WAM 87.3%。
- Scene OOD（OOD-S）：π0 7.3%，Fast-WAM 47.3%，JEPA-WAM 74.5%。
- Instruction OOD（OOD-I）：π0 23.6%，Fast-WAM 66.4%，JEPA-WAM 80.9%。
- Generated bank 对比：J-1024 平均 ID/OOD-S/OOD-I 为 82.5%/67.5%/75.0%，优于 KF-64 的 68.8%/47.5%/53.8%。

## 6. 可视化与表示分析
有 704 张生成图像的 UMAP：不同 task-level visual hypotheses 形成结构化区域；另有真实 keyframe 与 generated bank 的 qualitative 对比。

## 7. 真机实验与泛化
- 真机为共享 workspace manipulation，固定 box/plate/towel basket，随机化 object layout 与 container configuration。
- ID：训练分布；OOD-S：新场景组合；OOD-I：训练集中未出现的 instruction paraphrase。
- 这是明确区分 scene generalization 与 language generalization 的真机评测，而不是仅改变物体颜色。
- 所有模型使用同一套 1,370 demonstrations；真机推理在单张 NVIDIA RTX 5090 上，WAM 使用 10 action-denoising steps。

## 8. 与 OpenWAM 的关系
适合作为 OpenWAM instruction grounding 与 visual goal conditioning 的独立增强模块；可以在不改变 action/world backbone 的情况下测试“语言→视觉目标 latent”的收益。

## 9. 局限与待核对项
需从正文补充真实机器人本体型号、每个 task 的 rollout 数、生成器的完整型号及生成/推理时间成本；训练数据量和 GPU 推理设置已核对。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
这篇工作研究的是“视觉指令如何进入 WAM”。与只把语言 token 拼到 policy 输入不同，它先把生成的视觉 instruction 与 JEPA latent 对齐，再让 world-action model 用这些未来/目标视觉状态指导动作。

### 10.2 读者可以先记住的类比
语言指令是“把杯子放到左边”，视觉指令更像给出一张可观察的目标草图；JEPA latent 则把当前画面和目标草图变成同一种可比较的内部坐标。

## 11. 逐步读方法
### 11.1 数据流
语言或任务描述先生成视觉目标/视觉 instruction；当前观测和目标图像分别进入 JEPA 表示空间；WAM 预测动作条件的未来 latent，并用目标 latent 作为 action generation 或 planning 条件。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。视觉目标对齐让语义指令落到可感知的未来状态，future prediction 让动作与目标状态之间建立联系。风险是生成视觉 instruction 可能出现错误或偏差，因此需要区分语言理解失败、视觉生成失败和控制失败。

### 11.3 关键模块与张量含义
论文组合了 instruction generation/grounding、JEPA representation 和 WAM policy。它的新增点更偏接口设计：如何把高层指令转换成 world model 能消费的视觉状态，而不是单独提出新的 encoder。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。视觉目标对齐让语义指令落到可感知的未来状态，future prediction 让动作与目标状态之间建立联系。风险是生成视觉 instruction 可能出现错误或偏差，因此需要区分语言理解失败、视觉生成失败和控制失败。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
视觉 instruction 的消融回答生成目标是否比纯语言更容易控制；不同任务/物体和语言表达测试 grounding 泛化；应查看失败案例是否来自目标图像不准确而非 WAM 本身。

### 13.2 不要过度解读的地方
如果视觉 instruction 使用额外模型或目标信息，比较时必须说明这些信息是否在 baseline 中可用；生成图像质量也不应直接等同于可执行性。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 instruction generator、目标图像来源、JEPA checkpoint、目标 latent 距离、WAM horizon、语言模板和失败分类标准。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 用可比较的视觉目标作为语言到控制的中间接口；在 latent space 检查当前状态、目标状态和预测未来的一致性。
- **不能直接推出：** 它没有证明视觉指令一定比语言 token 更好，也没有消除目标生成模型和 WAM 的累计误差。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 可研究是否可以直接预测目标 latent，绕过像素级视觉 instruction 生成，降低错误传播。

---

<a id="2609.27455-lewam-ijepa"></a>
# Latent evolving World Action Model（LeWAM，I-JEPA 路线）

## 1. 基本信息
- 作者：Xueji Fang, Boqiang Duan, Hua Wu, Jingdong Wang, Guo-Jun Qi。
- 单位：Zhejiang University；Westlake University；Baidu Inc.（论文首页列出的单位集合）。
- 日期：首次提交 2026-09-23；本卡片阅读版本 v2，更新于 2026-09-24。
- 链接：[arXiv](https://arxiv.org/abs/2609.27455) · [HTML v2](https://arxiv.org/html/2609.27455v2) · [PDF](https://arxiv.org/pdf/2609.27455) · [代码](https://github.com/XuejiFang/LeWAM) · [模型](https://huggingface.co/XuejiFang/LeWAM)。
- 类型：**直接相关；冻结 I-JEPA-H/14 encoder 的 latent WAM**。与 NVIDIA 的 `2610.12407` 同名 LeWAM 不是同一篇。

## 2. 一句话摘要
用 I-JEPA embeddings 同时作为动作生成的视觉输入和未来状态预测目标，联合学习 action velocity 与 future embeddings，无需预训练视频扩散 backbone。

## 3. 主要创新点
- 比较 frozen visual encoders 对动作学习的作用；I-JEPA-H 在本文设置中表现最好，但各 checkpoint 规模/预训练数据不同，不能推成所有任务下的普遍优越性。
- **AdaFuse** 自适应融合冻结 encoder 的多层特征。
- 共享 predictor 联合动作生成与未来 embedding prediction；attention mask 防止 clean action 泄漏到动作预测。
- **DemoDPO** 根据 demonstration guidance 排序候选动作，利用偏好优化提高策略，而无需额外环境交互。

## 4. 方法与训练信号
- Appendix C.2：I-JEPA-H/14 encoder 约 0.6B 参数，预训练于 ImageNet-22K，冻结；224×224 输入、14×14 patch，产生 256 image tokens。
- predictor + AdaFuse 共 402M 可训练参数；模型总参数约 1.0B。
- AdaLN-Zero 用 noise timestep 与 task embeddings 条件化 predictor；noisy action 使用噪声时间，visual/clean-action/future-query tokens 使用零时间。
- 对比 encoder 时禁用 future embedding prediction，固定 12-layer、width 1280 的 action predictor 和训练 recipe；V-JEPA 2 按 single-image protocol 重复当前图像 16 次。

## 5. Benchmark / 测评方法 / 结果
**RoboTwin 2.0，50 tasks，Clean/Random 各 100 evaluation cases/task（Table 2）。**

| 模型/消融 | Clean SR (%) | Random SR (%) | Avg. (%) |
|---|---:|---:|---:|
| I-JEPA Action Only | 88.42 | 83.92 | 86.17 |
| + WM | 88.86 | 85.18 | 87.02 |
| + WM + AdaFuse | 91.32 | 90.06 | 90.69 |
| LeWAM（含 DemoDPO） | 93.14 | 91.42 | 92.28 |

**Encoder-only policy 对照（Table 1；不是完整 WAM 的最终成绩）：** DINOv3-Large 67.54%，V-JEPA2-Large 72.17%，V-JEPA2-Huge 81.70%，I-JEPA-Huge 86.17%；这是与用户指定 encoder 家族最直接相关的受控比较。

## 6. 可视化与表示分析
- Figure 4/6：action-to-vision attention，展示 clean/randomized 场景中对交互物体的关注。
- Figure 7、Table 1：depth 与 instance segmentation probing；I-JEPA-Huge depth RMSE 0.445、correlation 0.853，AP@50 0.613、AP@75 0.323。
- Figure 5：DemoDPO threshold/coefficient/group-size 消融；Figure 8/9：真机 refinement 前后和跨方法 rollout。

## 7. 真机实验与泛化
- Appendix D：AgileX 双臂平台，由两台 Piper manipulators 组成；固定 front camera + wrist cameras。
- 任务：Stack Blocks、Fold Towel、Arrange Flowers；每方法每任务 **50 rollouts**，每次最多 3 分钟，30 Hz 执行，single A100 40 GB 部署。
- 指标是 **normalized task progress，不是完整任务成功率**：按里程碑和失败扣分计分，最大分数分别为 7/6/6，然后归一化到 0–100。
- DemoDPO 前后 task progress：Stack Blocks 81.1→84.9%；Fold Towel 58.3→60.7%；Arrange Flowers 50.7→53.0%。
- 初始 object configurations 按 rollout 采样。原文没有在该段定义独立的新物体/新材质/新场景/新指令真机 OOD split，因此只记录初始配置变化，不把它写成系统性真机 OOD 验证；RoboTwin Random 是仿真随机化。

## 8. 与 OpenWAM 的关系
是 **I-JEPA → future embedding prediction + action generation** 的直接 WAM 基线；可比较 I-JEPA vs V-JEPA vs DINO、multilayer AdaFuse、WM loss 和 DemoDPO 的独立作用。

## 9. 局限与待核对项
已核对 encoder、正文表格、可视化和真机评分协议。跨 encoder 的预训练数据与参数规模不完全匹配；真机 task-progress 与 success-rate benchmark 不应直接排序。来源定位：Table 1/2、Appendix C.2/C.5、Appendix D/D.1。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
这篇 LeWAM/I-JEPA 路线工作把 world action model 视为一个会逐渐形成“状态表征—动作后果—策略”的统一模型。重点不只是预测未来，而是让 latent 同时支持 planning、policy learning 和 demonstration-guided action selection。

### 10.2 读者可以先记住的类比
它像一个不断整理内部地图的机器人：一边根据视频判断状态，一边学习动作会怎样改变地图，再用示范告诉它哪些路线更值得选择。

## 11. 逐步读方法
### 11.1 数据流
视觉序列经过 I-JEPA 风格的预测表示；action-conditioned predictor 产生未来 latent；policy/action module 从当前与预测状态生成候选动作；DemoDPO 或类似排序机制利用 demonstration guidance 选择更符合示范的行为。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。未来表征预测让 latent 保留时序结构，动作监督让它可执行，示范偏好/排序让候选行为具有任务方向。多目标训练的风险是不同 loss 互相竞争，因此需要看每个分支去掉后的控制结果。

### 11.3 关键模块与张量含义
应区分 I-JEPA encoder、latent dynamics、policy/action head 和 demonstration preference module。它不是只有一个 encoder 替换，而是从 representation 到 action selection 的完整链路。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。未来表征预测让 latent 保留时序结构，动作监督让它可执行，示范偏好/排序让候选行为具有任务方向。多目标训练的风险是不同 loss 互相竞争，因此需要看每个分支去掉后的控制结果。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
主任务回答统一 latent 是否能同时服务预测和动作；DemoDPO/偏好模块消融回答示范 guidance 是否超过单纯 imitation；不同任务与 OOD 设置验证 latent 是否可迁移。

### 13.2 不要过度解读的地方
论文版本、标题命名和同名 LeWAM 工作容易混淆；必须以 arXiv ID 和版本为准。若结果来自不同数据预算或 policy backbone，不能直接横向排序。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 arXiv 版本、I-JEPA checkpoint、示范数据、候选动作数量、偏好排序温度、预测 horizon 和 policy sampling budget。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 让预测 latent 同时进入 policy 和 planner；利用 demonstration 做候选动作排序；报告 prediction、action 和 planning 三层证据。
- **不能直接推出：** I-JEPA 表示本身并不自动带来更好的控制；若没有 matched encoder/policy 对照，收益可能来自额外训练信号。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 值得验证 demonstration guidance 是否可以用 uncertainty-aware ranking 替代，以及长时域 rollout 中 preference 信号是否稳定。

---

<a id="2609.37250-vjepa-policy"></a>
# V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents

## 1. 基本信息
- 作者：Yang Zhang, Jiangyuan Zhao, Chenyou Fan, Jiayu Hu, Xiu Yuan, Chenjia Bai, Xiu Li
- 单位：Tsinghua University；Shanghai Jiao Tong University；Fudan University；University of Science and Technology of China；Washington University in St. Louis；TeleAI；γ-Robotics
- 日期：2026-09-29（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2609.37250) · [HTML](https://arxiv.org/html/2609.37250) · [代码](https://github.com/breez3young/VJEPA-Policy)
- 类型：直接相关；JEPA latent WAM / policy

## 2. 一句话摘要
冻结 V-JEPA 2.1 encoder，在下游联合训练 instruction-conditioned future-latent predictor 与 flow-matching action expert，以较小的可训练参数建立 WAM。

## 3. 主要创新点
- 不依赖完整预训练视频生成器，而直接使用 predictive visual latent。
- predictor 的 future-informed context KV 条件化 action generation。
- DROID video–instruction pairs 可在无 action label 下预训练 predictor，再迁移到控制。
- 0.9B 总参数，其中 0.6B 可训练。

## 4. 方法与训练信号
- 输入：多视角 RGB、proprioception、language instruction。
- 冻结 V-JEPA 2.1 visual encoder；学习未来 latent 预测与 flow-matching action expert。
- 预训练阶段只使用 DROID 视频-指令；下游阶段使用机器人 demonstrations。

## 5. Benchmark / 测评方法 / 结果
- LIBERO：success rate 97.25%。
- LIBERO-Plus：79.25%；DROID predictor 预训练后 91.50%；扩展下游训练为 81.64%。
- RoboCasa-GR1：24 tasks，success rate 50.92%。
- RoboCasa-GR1 predictor-pretrained variant：55.58%。
- LIBERO-Plus 的 shift 维度包括 camera、initial state、language、lighting、texture、noise、layout；from-scratch V-JEPA Policy 平均 79.25%。
- 真机 TianJi Marvin 两项任务、每任务 20 trials：Table Cleanup 11/20（55%），Saucer Racking 7/20（35%）；DROID predictor 预训练后分别 15/20（75%）和 17/20（85%），平均从 45% 升至 80%。
- 另有 matched-framework / matched-budget 的视觉基础模型比较，强调分布偏移下 V-JEPA latent 的优势。

## 6. 可视化与表示分析
有跨视觉基础比较、future latent 预测/表示分析和控制结果分析；引用图表时以论文 HTML 章节为准。

## 7. 真机实验与泛化
- 平台：TianJi Marvin dual-arm platform。
- 任务：两项 multi-stage bimanual coordination。
- 泛化：LIBERO-Plus 等 distribution-shift benchmark；DROID 无动作预训练验证跨数据来源的 future-modeling transfer。

## 8. 与 OpenWAM 的关系
这是当前最直接的同路线参照：V-JEPA latent、future prediction、flow matching action、LIBERO-Plus 与真机泛化均可作为 OpenWAM 对比轴。

## 9. 局限与待核对项
仍需从附录补齐 LIBERO/RoboCasa 的训练 seed 与完整 baseline 表格，以及真机失败分类；核心真机 trial 数和任务名已核对。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
V-JEPA Policy 关注“预测视觉 latent 能否直接变成一个有效的 world-action policy”。与只做 image-goal planner 的工作不同，它把 predictive visual latent 作为 action policy 的输入或内部条件，让策略在输出动作前显式考虑未来。

### 10.2 读者可以先记住的类比
当前图像告诉机器人“我在哪里”，V-JEPA latent prediction 让它先想象“执行动作后会到哪里”，policy 再选择一组能让未来接近任务目标的动作。

## 11. 逐步读方法
### 11.1 数据流
观测历史进入冻结或部分微调的 V-JEPA encoder；action-conditioned predictor 预测未来 patch/token features；policy/action head 根据当前、语言/目标和未来 latent 产生 action chunk；执行反馈进入下一轮闭环。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。future latent regression/embedding prediction 建立视觉未来与动作的联系，action imitation 或 policy objective 保证输出可执行。预测目标可能过于宽泛，所以必须用 task success 证明它保留了控制相关因素。

### 11.3 关键模块与张量含义
关键是 V-JEPA encoder、predictive head 和 action decoder 的接口。阅读时确认 predictor 是训练辅助、推理必需，还是只用于 planner；这会改变它与普通 VLA 的计算成本和能力边界。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。future latent regression/embedding prediction 建立视觉未来与动作的联系，action imitation 或 policy objective 保证输出可执行。预测目标可能过于宽泛，所以必须用 task success 证明它保留了控制相关因素。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
主结果比较 predictive latent policy 与 reactive/standard policy；horizon、冻结状态、未来 token 和 loss ablation 分析设计选择；OOD 任务/物体测试预测是否改善泛化而非只提升训练分布拟合。

### 13.2 不要过度解读的地方
V-JEPA 预训练规模、policy backbone 和 action chunk 可能显著影响结果；不能只根据模型名称比较。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 V-JEPA 版本、冻结/微调策略、历史帧、future horizon、action chunk、推理 steps、数据预算和 OOD protocol。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 把 V-JEPA 作为 predictive visual interface；将未来 latent 接入 policy；报告 latent quality、动作 success 和推理延迟三类结果。
- **不能直接推出：** 它没有说明任何 V-JEPA checkpoint 都适合控制，也没有证明预测未来一定优于更大的 reactive policy。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 可研究未来 token 的选择性预测、预测不确定性和 action head 的计算共享，以降低部署成本。

---

<a id="2609.38163-rewam"></a>
# Rethinking Representations for World-Action Modeling

## 1. 基本信息
- 作者：Haoyi Jiang, Liu Liu, Xinjiang Wang, Zhihao Sun, Zequn Chen, Sen Wang, Xinjie Wang, Xia Chen, Jingfeng Yao, Weiheng Zhao, Shanglin Yuan, Zhizhong Su, Wei Sui, Wenyu Liu, Xinggang Wang
- 单位：Huazhong University of Science and Technology；Horizon Robotics；Fudan University；Xi’an Jiaotong University；D-Robotics
- 日期：2026-09-29（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2609.38163) · [HTML](https://arxiv.org/html/2609.38163)
- 类型：DINO feature WAM / representation-centric policy

## 2. 一句话摘要
提出 ReWAM，通过 feature calibration、temporal representation bottleneck 和 action-grounded representation shaping，把预训练 DINO features 组织成适合 dynamics 与 action 的紧凑状态。

## 3. 主要创新点
- 通过 controlled comparison 说明 reconstruction fidelity 或 pretrained perceptual feature 本身都不足以保证 policy learning。
- Temporal Representation Bottleneck 压缩 DINO features 并隔离 world-model dynamics。
- Action-Grounded Representation Shaping 只让 action loss 更新 bottleneck，使 representation 更贴近控制需求。
- 不使用 generative video pretraining。

## 4. 方法与训练信号
- 预训练 DINO feature → calibration → temporal bottleneck → world-action predictor/action policy。
- action loss 与 world-model loss 采用不同 gradient routing。
- 在 RoboTwin 2.0 和 RoboDojo 上验证 policy performance 与 large-scale embodied pretraining。

## 5. Benchmark / 测评方法 / 结果
- RoboTwin 2.0：success 93.6%。
- RoboDojo：约 600 小时 embodied pretraining，平均 score 12.29，success rate 8.28%。
- 论文重点比较 representation design，而不是只比较生成质量。

## 6. 可视化与表示分析
有 representation-space / bottleneck 分析、controlled encoder comparison 和 action-grounded feature shaping ablation；具体图表以 HTML 正文为准。

## 7. 真机实验与泛化
摘要明确报告 RoboDojo 结果，但平台、任务组成、真机/仿真比例和 OOD protocol 需从正文补录；RoboTwin randomized setting 不应自动等同真机泛化。

## 8. 与 OpenWAM 的关系
是 OpenWAM 当前架构最值得对照的 DINO-based alternative：尤其适合验证 action-gradient gating、temporal bottleneck 和 representation calibration。

## 9. 局限与待核对项
需补录 DINO 具体 checkpoint、RoboDojo task/score 定义、真机硬件和训练数据的 embodiment 构成。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
RE-WAM 重新审视 WAM 最核心的表示选择：世界模型是否真的需要生成视频，还是只要学习对动作有用的 latent dynamics？它试图把 representation、prediction 和 action learning 的关系拆开分析。

### 10.2 读者可以先记住的类比
如果机器人的任务是判断门是否打开，没必要预测每个像素的光照变化；RE-WAM 更像只画出与行动相关的状态变化，同时保留足够信息让 policy 知道下一步怎么做。

## 11. 逐步读方法
### 11.1 数据流
视觉输入经过非生成式表征 encoder；world model 根据动作预测未来 representation；policy 或 planner 使用 predicted latent 产生动作；闭环执行后重新编码观测。论文的重点是这种表示接口与 generative video pretraining 的比较。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。representation/dynamics loss 约束 latent 可预测，action loss 约束其控制相关性。非生成式目标可以减少无关视觉细节，但也可能丢失遮挡、接触或细粒度几何，因此需要通过控制和 OOD 实验验证。

### 11.3 关键模块与张量含义
分开看 encoder、latent predictor、action policy 和 optional planner。RE-WAM 的问题意识是“生成像素是否必要”，不是简单宣称所有语义 latent 都足够。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。representation/dynamics loss 约束 latent 可预测，action loss 约束其控制相关性。非生成式目标可以减少无关视觉细节，但也可能丢失遮挡、接触或细粒度几何，因此需要通过控制和 OOD 实验验证。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
与 generative video pretraining、不同 encoder 和 action modeling 的比较回答生成目标是否带来控制收益；表示 probe、长时域 rollout 和 real/sim transfer 分别验证状态信息、动力学和泛化。

### 13.2 不要过度解读的地方
非生成式方法的计算优势必须与输入 token 数、模型参数和训练数据对齐；较低的图像重建质量不能直接视为缺点。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定视觉预训练数据、encoder frozen status、latent dimension、predictor horizon、policy head、planner budget 和 generative baseline。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 优先做 action-oriented representation；显式检查生成像素与控制成功的关系；将 encoder 与 policy 解耦比较。
- **不能直接推出：** 更轻的 latent model 不自动说明其在复杂视觉变化和真实世界上更稳健。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 可将 RE-WAM 的表示实验扩展到同一任务上的 DINO、V-JEPA、I-JEPA 和 intermediate feature supervision。

---

<a id="2610.06965-acg-wam"></a>
# ACG-WAM: World-Action Modeling via Action-Conditioned Geometric Latent Prediction

## 1. 基本信息
- 作者：Jiangtao Liu, Zishang Xiang, Yage He, Lingguo Cui, Baihai Zhang, Runqi Chai, Senchun Chai
- 单位：School of Automation, Beijing Institute of Technology；LimX Dynamics
- 日期：2026-10-03（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2610.06965) · [HTML](https://arxiv.org/html/2610.06965) · [代码](https://github.com/RoboOpus/ACG-WAM)
- 类型：直接相关；action-conditioned geometric JEPA auxiliary objective

## 2. 一句话摘要
用当前观测和 actions 预测多时域几何 latent，以冻结 VGGT 对当前/未来图像对编码的 future slot 为 target，推理时移除辅助 teacher。

## 3. 主要创新点
- ACG-JEPA 显式监督 demonstration action 的几何后果。
- 监督施加在 temporal mixing 前的共享 visual embedding。
- head/wrist cameras 的多视角、多 horizon 几何预测。
- teacher 与 auxiliary modules inference 时移除。

## 4. 方法与训练信号
当前 observation + intervening actions → geometric future features；target 来自 frozen VGGT current/future image pair 的 future slot。

## 5. Benchmark / 测评方法 / 结果
- RoboTwin 2.0，50 tasks：clean success 93.46%；randomized success 92.68%；均值 93.07%。
- 真机 3 tasks：success 85.00%；partial completion 91.67%。
- 相对 Motus：真机 success +10.00 pp；partial completion +9.17 pp。
- RoboTwin 每 task/setting 100 episodes，使用 unseen instruction templates、evaluation seed 42；Clean/Random 表格是 50-task macro averages。
- 真机平台为 TRON2 + WUJI hands；每 task 100 demonstrations、15k fine-tuning updates、20 trials/task（总计 60 trials/policy）。
- PCS 将每 trial 记为 0/1/2：未完成/部分完成/完整完成，再归一化到 0–100；三任务平均等权。

## 6. 可视化与表示分析
有 geometric latent、多 horizon prediction 和 auxiliary ablation 分析；详细图号/定量 probe 待从正文表格补录。

## 7. 真机实验与泛化
- 真机：机器人 manipulation，3 tasks。
- 仿真泛化：clean vs randomized scenes。
- 摘要未说明真机是否做 unseen objects/geometry/scene 的独立泛化；不能将 randomized simulation 等同于真机泛化。

## 8. 与 OpenWAM 的关系
适合作为 OpenWAM auxiliary geometric prediction、camera fusion 和 action consequence supervision 的实验设计参考。

## 9. 局限与待核对项
需继续补齐 RoboTwin 的所有 task-wise 表格和具体随机化变量；真机硬件、任务、trial 数与 PCS 定义已核对。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
ACG-WAM 把几何信息放到 world-action modeling 的中心：动作不仅改变视觉内容，也改变物体之间的空间关系。相比直接预测高维视觉 token，它希望用 action-conditioned geometric latent 让模型更容易学习可控的变化。

### 10.2 读者可以先记住的类比
像机器人在脑中维护一张简化的 3D 草图：它不必预测每片纹理，但必须知道手、物体和目标之间的相对位置会如何随动作变化。

## 11. 逐步读方法
### 11.1 数据流
视觉输入提取几何/结构特征；动作条件模块预测下一时刻 geometric latent；policy/action head 使用当前和未来几何状态生成动作。teacher 与 auxiliary modules 主要在训练时提供监督，推理时移除以降低负担。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。几何 latent supervision 让模型学习空间关系，action-conditioned prediction 让这些关系与动作绑定，policy loss 则保证最终可执行。去掉 teacher/auxiliary modules 后仍能工作是设计的关键，但要检查训练-推理 gap。

### 11.3 关键模块与张量含义
核心是 geometric representation、action-conditioned predictor、teacher/auxiliary training branch 和 action head。它与纯语义 JEPA 的差异在于强调可操作的空间结构。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。几何 latent supervision 让模型学习空间关系，action-conditioned prediction 让这些关系与动作绑定，policy loss 则保证最终可执行。去掉 teacher/auxiliary modules 后仍能工作是设计的关键，但要检查训练-推理 gap。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
几何表示与基线 WAM 的比较回答空间 inductive bias 是否有益；teacher/auxiliary ablation 检查是否能低成本部署；任务和 OOD 几何变化测试泛化。

### 13.2 不要过度解读的地方
几何特征质量依赖相机、深度或 teacher 估计；若几何信息在 baseline 中不可用，比较需要明确额外输入和标注成本。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定几何 teacher、相机/深度输入、latent 构造、auxiliary loss、推理时移除模块、动作 horizon 和 OOD 几何设置。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 把几何关系作为中间 latent；训练时使用 teacher、部署时移除；单独报告几何 prediction 与 action success。
- **不能直接推出：** 几何 latent 不会自动解决遮挡、语义指令理解或长时域规划。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 可研究几何 latent 与 V-JEPA 语义 latent 的互补融合，而不是二选一。

---

<a id="2610.10515-robojepa"></a>
# RoboJEPA: Scaling Robotic Latent World Models

## 1. 基本信息
- 作者：Artem Zholus, Nicolas Beltran-Velez, Jianhao Yuan, Sarath Chandar, Tushar Nagarajan, Daniel Severo, Koustuv Sinha, Michal Drozdzal, Adriana Romero Soriano, Jeannette Bohg, Nicolas Ballas, Mahmoud Assran
- 单位：FAIR at Meta；Chandar Research Lab；Mila – Quebec AI Institute；Polytechnique Montréal
- 日期：2026-10-07（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2610.10515) · [HTML](https://arxiv.org/html/2610.10515)
- 类型：直接相关；JEPA robotic world model / scaling

## 2. 一句话摘要
在覆盖 12 种机器人 embodiment 的大规模数据上研究 JEPA latent world model scaling，并验证 imagination error 可作为真实机器人规划能力的代理指标。

## 3. 主要创新点
- 多 embodiment robotic world model 的 scaling law 视角。
- imagination error 随 compute 遵循二阶 power law，可外推模型质量。
- imagination error 与下游 robotic planning performance 强相关。
- 发布 checkpoint、训练和部署代码；8B predictor。

## 4. 方法与训练信号
核心是 JEPA latent future prediction；改变模型规模、数据和 compute，测量 latent rollout/imagination error 与规划性能的关系。

## 5. Benchmark / 测评方法 / 结果
- 多 embodiment robot data，重点是 scaling curve 而非单一 leaderboard。
- 指标：imagination error、compute scaling law、downstream planning performance。
- 摘要确认 zero-shot real-robot agent 能从单张 goal image 规划长时任务；具体任务/成功率待从实验表格补录。

## 6. 可视化与表示分析
有 scaling curves，以及 imagination error 与规划性能的相关性分析。

## 7. 真机实验与泛化
- 真机：zero-shot agent，single goal image conditioning，long-horizon planning。
- DROID/Franka 真机任务为 Grasp、Object Lift、Pick-and-Place；每个任务 10 episodes，goal 由 side/wrist camera 的单张图像指定。
- Table 12 报告 RoboJEPA-8B 三任务 success 为 67%/50%/27%，对应 task progress 为 67%/65%/42%；同时报告 22M–4B scaling variants。
- 泛化：跨 embodiment / zero-shot deployment；平台、任务和物体/场景变化需从正文核对。

## 8. 与 OpenWAM 的关系
适合建立 predictor quality proxy：除 action success 外，记录 rollout latent error、horizon degradation 和下游 planning correlation。

## 9. 局限与待核对项
需补齐 12 个 embodiment 的完整清单、仿真任务表、scaling fit 区间和不同模型的 planner success；Franka/DROID 真机任务与 10-episode protocol 已核对。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
RoboJEPA 关注规模化：如果 JEPA world model 要覆盖多视角、多机器人和多种 embodiment，如何在不生成像素的情况下训练一个足够大的 latent predictor？它将视觉表示、动作和 proprioception 统一到可扩展的 token 序列中。

### 10.2 读者可以先记住的类比
可以把它看成一个多语言翻译器：不同相机、不同机器人和不同身体状态是不同“方言”，模型通过 view/embodiment identifier 把它们翻译到同一个未来状态空间。

## 11. 逐步读方法
### 11.1 数据流
冻结的 V-JEPA 2.1 encoder 将多视角图像变成 feature grid；predictor 接收多视角 visual token、action token、proprioceptive token 以及 view/embodiment ID；teacher-forcing 和 autoregressive rollout 两种训练路径预测下一时刻 feature。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。teacher-forcing 让单步预测准确，rollout loss 强迫模型在缺少真实中间帧时也能长期预测；KV-cache 支持高效自回归 rollout。两者的差异直接对应短期拟合与长时域稳定性。

### 11.3 关键模块与张量含义
RoboJEPA 的重点是 frozen encoder + large predictor + multi-view/embodiment conditioning。它是 world model，不是完整的 action policy；要把预测质量与下游规划/策略性能分开看。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。teacher-forcing 让单步预测准确，rollout loss 强迫模型在缺少真实中间帧时也能长期预测；KV-cache 支持高效自回归 rollout。两者的差异直接对应短期拟合与长时域稳定性。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
跨视角、跨 embodiment、长时域 rollout 和 checkpoint/code release 共同回答模型是否可扩展；teacher-forcing 与 rollout 的对比检查模型是否只会单步复制而不会闭环预测。

### 13.2 不要过度解读的地方
规模化模型的收益可能来自参数量、数据量和 tokenizer/encoder 变化；跨 embodiment 的统一并不代表无需任务或机器人适配。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 V-JEPA 2.1 checkpoint、视角数、embodiment ID、proprioception、teacher-forcing/rollout mask、KV-cache 和模型规模。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 将 view/embodiment ID 显式加入 latent predictor；同时训练 teacher-forcing 与 rollout；使用 KV-cache 做长时域预测。
- **不能直接推出：** 大型 predictor 的 latent prediction 结果不等于零样本 policy success；还需要 planner 或 action head 验证可控性。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 下一步是把 RoboJEPA predictor 与 action policy 共同训练，验证统一 latent 是否真的能带来跨机器人控制迁移。

---

<a id="2610.12285-plaw-vla"></a>
# PLaW-VLA: Predictive Latent World Modeling for Vision-Language-Action Policies

## 1. 基本信息
- 作者：Yu Liu, Hetian Guo, Tianlv Huang, Ziyi Cai, Wudi Chen, Hantang Wang, Qiutong Liu, Yingzhi Peng, Wei Han, Peijun Tang, Jianan Wang, Zipei Fan, Zhiyuan Zha, Xuan Song
- 单位：Jilin University；Astribot；Harbin Institute of Technology, Shenzhen；The Hong Kong Polytechnic University；The University of Tokyo
- 日期：2026-10-08（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2610.12285) · [HTML](https://arxiv.org/html/2610.12285) · [项目页](https://rainyrobo.github.io/PLaW-VLA)
- 类型：相邻相关；predictive latent world model + VLA policy

## 2. 一句话摘要
在 prediction-oriented representation 中建模 task-relevant future states，并通过 structured causal attention 将历史、语言和未来状态用于 action generation。

## 3. 主要创新点
- 避免重建 control-irrelevant pixel details。
- Mixture-of-Transformers 同时处理 observation history、task semantics、predicted futures。
- 未来状态并行预测，约为 generative WAM 相当性能下的 1/19 inference latency。

## 4. 方法与训练信号
两阶段 predictive pretraining + robot-policy training；通过 future-state masking、representation 和 pretraining ablations 检查贡献。

## 5. Benchmark / 测评方法 / 结果
- RoboTwin Hard Horizon III：比 reactive policy +11.8 pp。
- zero-shot LIBERO-Plus：72.7% average success；相对 reconstruction-oriented latent prediction +1.77 pp。
- LIBERO：world-model ablation 96.28% vs 96.05%；mask all future states 97.40% → 93.05%。
- 报告 success/task progress；RoboTwin 使用 horizon 难度，LIBERO-Plus 使用 zero-shot distribution shift。

## 6. 可视化与表示分析
有 PCA visualization：current/near/far future features 随 robot arm motion 变化；有 horizon masking，far-future masking 影响略大。

## 7. 真机实验与泛化
- 平台：dual-arm wheeled humanoid robot。
- 任务：Fold Towel、Pack Toy、Play Basketball、Organize Stationery。
- 泛化：unseen towel materials/colors；将 pen holder 替换为不同高度、开口直径和颜色的 paper cup。
- 每个设置 10 spatial configurations × 3 trials；报告 normalized task progress。
- 真机训练使用每 task 约 50 epochs；推理在 RTX 5090 上，WAM baseline 使用 10 action-denoising steps；生成的 visual instruction 在语言指令不变时复用。

## 8. 与 OpenWAM 的关系
适合作为 OpenWAM 的效率和泛化对照：未来 latent 不必重建像素，但需证明 predicted future 真正改善 long-horizon control。

## 9. 局限与待核对项
真机逐任务图表主要报告 normalized task progress；仍需从 Figure 4/附录补录 π0/π0.5 的逐任务曲线数值和完整 latency 对照。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
PLaW-VLA 解决的是 VLA 中的时间尺度问题：语言提供任务语义，policy 需要输出动作，但长时域任务不能只依赖当前画面反应。论文引入 predictive latent world modeling，让模型先预测与任务相关的未来状态，再交给 action expert。

### 10.2 读者可以先记住的类比
像一个项目经理：语言模块确定目标，world model 先写出未来几步的计划草图，action expert 再把草图变成连续控制；草图不需要是完整视频，只需包含会影响行动的状态。

## 11. 逐步读方法
### 11.1 数据流
历史视觉和语言进入 structured attention；world-model expert 用 learnable queries 在冻结 V-JEPA 2 latent 中预测 future representation；action expert 同时读取当前上下文和未来 prediction tokens，生成连续动作。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。predictive pretraining 学会未来状态结构，policy training 学会把 future tokens 转成动作。mask future states 的消融用于测试模型是否真的依赖预测，而不是只利用当前观测 shortcut。

### 11.3 关键模块与张量含义
Mixture-of-Transformers 的三个角色要分清：semantic grounding、future latent prediction、continuous action generation。structured causal attention 决定谁能看见谁，是避免未来信息泄漏的关键。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。predictive pretraining 学会未来状态结构，policy training 学会把 future tokens 转成动作。mask future states 的消融用于测试模型是否真的依赖预测，而不是只利用当前观测 shortcut。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
RoboTwin Hard Horizon III 测 long-horizon progress，LIBERO-Plus 测 zero-shot distribution shift，mask 和 world-model ablation 测未来预测的因果贡献；延迟结果则回答并行 latent prediction 是否提高效率。

### 13.2 不要过度解读的地方
RoboTwin 的 normalized progress 与 LIBERO success 不是同一种指标；不同 baseline 的 denoising steps、训练数据和 backbone 也影响 latency 和 success。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 V-JEPA checkpoint、future mask/horizon、MoT attention mask、action denoising steps、GPU、训练数据和每个任务的 trial protocol。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 用 learnable queries 预测未来 latent；通过 causal attention 把未来 token 接到 action expert；同时报告任务成功/进度和推理延迟。
- **不能直接推出：** 预测未来 token 的存在不保证其内容准确，也不证明 reconstruction-based 方法在所有分布偏移下都更差。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 值得研究未来 token 的不确定性、查询数量和 action expert 共享层数对实时控制的影响。

---

<a id="2610.12407-lewam"></a>
# LeWAM: A JEPA World Action Model with Diffusion-Steering-Based MPC

## 1. 基本信息
- 作者：Shashank Hegde, Alexander Popov, Elie Aljalbout, Nikolai Smolyanskiy
- 单位：论文 HTML 未给出可稳定抽取的 affiliation，待从 PDF 首页核对。
- 日期：2026-10-08（arXiv v1）
- 链接：[arXiv](https://arxiv.org/abs/2610.12407) · [HTML](https://arxiv.org/html/2610.12407)
- 类型：直接相关；JEPA WAM + MPC

## 2. 一句话摘要
用 decoder-free JEPA latent 端到端支持 forward、backward、inverse dynamics 和 policy prediction，并在 policy noise space 中用 diffusion-steering MPC 规划。

## 3. 主要创新点
- bidirectional transformer 统一四类预测模式。
- latent 同时追求状态可读性和对视觉 distractor 的不敏感。
- 指出 action-space MPC 会利用 dynamics model error，改在 policy noise space 规划。

## 4. 方法与训练信号
- 与 regular LeWM、reconstruction-based WAM 对比；flow-matching policy 使用匹配 encoder/规模。
- 采用 DS-CEM（diffusion-steering cross-entropy method）进行规划。

## 5. Benchmark / 测评方法 / 结果
- robosuite：Lift、Can、Square、ToolHang、Transport。
- closed-loop success；5 training seeds；每个 cell 50 episodes。
- 训练使用 90% 数据、300 epochs、5 seeds；其余 10% 作为评测 split，并在含视觉 distractor 的 simulator 中测试。
- 六项任务还包括 PushT；每个 world model/planner 组合共 250 rollouts（5 training seeds × 50 evaluation seeds）。
- Table 3 的 mode ablation 同时报告 ridge-probe state R²、policy success 与 DS-CEM success；Table 4 测试 policy-noise proposal 的 projection shell。
- 摘要结论：acting 与匹配规模的 flow-matching policy 相当；noise-space MPC 优于 raw-action 规划。

## 6. 可视化与表示分析
有 linear probe（robot/object state）、distractor 忽略对比和 latent/规划结果图。

## 7. 真机实验与泛化
重点为仿真闭环实验；作者将 real-world data/application 列为后续方向，未报告真机泛化结果。

## 8. 与 OpenWAM 的关系
适合作为 OpenWAM future predictor 是否能同时服务 policy 与 planning 的对照，并提醒评估 action-space MPC 的 model-error exploitation。

## 9. 局限与待核对项
作者单位已从正文确认是 NVIDIA；仍需补录六任务完整逐项 success 表和各 planner 的完整对照数值。


## 10. 先建立直觉
### 10.1 这篇论文到底要解决什么问题
这篇 LeWAM 的核心问题是：如果 world model 同时学 forward dynamics、inverse dynamics 和 policy prediction，如何让 MPC 使用它而不被模型误差带偏？作者进一步把规划变量从原始 action space 移到 policy 的 noise space。

### 10.2 读者可以先记住的类比
直接在动作空间规划像让驾驶员随意改方向盘；在 policy-noise space 规划更像先改变一个已经会驾驶的控制器的“意图”，让它产生合理动作，再在这些动作附近搜索。

## 11. 逐步读方法
### 11.1 数据流
统一的 bidirectional transformer 根据 mask 形式切换 forward、backward、inverse 和 policy prediction；policy/flow-matching 分支把 noise 映射为 action；DS-CEM 在 noise space 采样、steer 和筛选候选，再闭环执行。

### 11.2 训练时与推理时
训练阶段要把论文提供的未来帧、未来表示、动作、语言或辅助标签看成监督信号；部署阶段通常只有当前观测、任务条件和历史预测，不能偷看真实未来。不同 mask 对应不同任务，迫使同一 latent 支持状态预测和动作预测；policy-space planning 利用匹配的 flow policy 作为 action prior，减少 raw-action MPC 走到不合理区域的机会。

### 11.3 关键模块与张量含义
必须区分 regular LeWM/WAM 表征、flow-matching policy、四种 mask mode 和 DS-CEM planner。论文比较的不是单一模型，而是“同一个 world model 是否能服务 acting 与 planning”。

## 12. 训练目标为什么合理
- **想学到的能力：** 让表示包含任务相关状态，让 predictor 学会动作导致的未来变化，再让 policy 或 planner 把这些变化转成可执行动作。不同 mask 对应不同任务，迫使同一 latent 支持状态预测和动作预测；policy-space planning 利用匹配的 flow policy 作为 action prior，减少 raw-action MPC 走到不合理区域的机会。
- **可能的漏洞：** latent loss、重建质量、VLM judge 或 imagined return 都只是代理指标；如果没有 matched downstream control，模型可能学会与成功无关的 shortcut。

## 13. 结果应该怎样读
### 13.1 哪个实验回答哪个问题
robosuite 六类任务和多 seed 评测 acting/DS-CEM；linear probe 检查 latent 是否包含状态；distractor 与 projection-shell ablation 检查表示和 noise-space proposal 是否减少模型误差利用。

### 13.2 不要过度解读的地方
主要证据为仿真；5 seeds、每 cell 50 episodes 等协议必须与其他工作区分。摘要中的“相当”不等于所有任务逐项领先。 论文的主结果、消融、表示分析和定性图分别回答不同问题；不要把它们压缩成一个“模型更强”的结论。

## 14. 复现与对比清单
- 数据与预处理：以第 5、7 节记录的任务、数据和划分为准，补齐未报告的 episode/rollout 数。
- 表征与模型：固定 mask mode、policy noise parameterization、DS-CEM population/iterations、projection shell、seed、episode 数和 distractor 设置。
- 训练与推理：记录 frozen/trainable 模块、history、prediction horizon、action chunk、sampling/denoising/规划预算。
- 评测：固定 benchmark、split、seed、success/progress 定义，并区分仿真、离线和真机。
- 公平对比：同时对齐 encoder checkpoint、参数规模、训练数据、推理延迟和额外目标信息。

## 15. 读者 takeaway
- **可以直接借鉴：** 统一多模式 latent model；在 policy noise space 做 MPC；用 probe、distractor 和 held-out rollout 同时诊断表示和 planner。
- **不能直接推出：** noise-space MPC 并不消除 model error，也没有证明一定能迁移到真实机器人；它还依赖一个足够好的 flow-matching policy prior。
- **最值得复现：** 在单一任务上固定 encoder 和 policy，只打开/关闭本文新增的 predictor、fusion、planner 或辅助监督。
- **最值得继续验证：** 下一步是把 noise-space planning 与 V-JEPA/ I-JEPA latent 结合，并在真实机器人上验证其对接触动力学的鲁棒性。
