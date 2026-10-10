# 证据矩阵

| 论文 | 论文正文来源 | 结果是否有协议 | 真机是否有 | 真机泛化类型 | 可视化/表示分析 | 待补证据 |
|---|---|---|---|---|---|---|
| LeWAM（I-JEPA，2609.27455） | HTML v2 Table 1/2、Appendix C.2/D | RoboTwin 100 cases/task/setting；真机 50/task；progress milestones | 有：AgileX 双 Piper | 初始配置变化；无独立真机 OOD split 定义 | attention、depth/segmentation probes、rollout | encoder 预训练规模不匹配；不可将 progress 当 SR |
| V-JEPA Policy | arXiv HTML + tables | 有：LIBERO 50 episodes/task；RoboCasa 50/task；真机 20/task | 有 | 7 类 LIBERO-Plus shift；DROID transfer；Marvin 双臂 | future latent、视觉基础比较 | LIBERO seed/完整 baseline |
| LeWAM | arXiv HTML + tables | 有：90/10 split、300 epochs、5 seeds、250 rollouts | 无 | 不适用；作者列为后续 | linear probe、distractor、MPC | 六任务完整 planner 表 |
| RoboJEPA | arXiv HTML + tables | 有：真机 10 episodes/task；scaling holdout | 有 | zero-shot goal-image、跨 embodiment | scaling curve、imagination correlation | 12 embodiment 清单、仿真 task 表 |
| ACG-WAM | arXiv HTML + tables | 有：RoboTwin 100/task/setting；真机 20/task | 有 | simulation clean/randomized；真机三任务 PCS | geometric latent、多 horizon | RoboTwin 完整 task-wise 表 |
| PLaW-VLA | arXiv HTML + 摘要 | 部分；真机 10 × 3 | 有 | unseen towel；receptacle geometry/color | PCA、horizon masking | 真机逐任务数值 |
| JEPA Policy | arXiv HTML | 有：3 seeds、30 eval、best/last checkpoint | 有 | 真机泛化矩阵待核 | error/failure ranking、collapse audit | 真机任务和逐项表 |
| JEPA-VLA | arXiv HTML | 有：LIBERO-Plus 4 checkpoints avg；真机 10 trials | 有 | layout、lighting、1/5 data | fusion/representation/trajectory | 真机 baseline 逐项数值 |
| V-JEPA 2 | arXiv HTML + 摘要 | 部分 | 有 | 两实验室 Franka zero-shot | latent decoding、counterfactual、camera sensitivity | 真机 task/episode 表 |
| DreamZero | arXiv HTML + 摘要 | 部分；task-progress ± standard error | 有 | unseen object/task/env、cross-embodiment、30-min adaptation | rollout、数据分布、速度 | affiliation、完整 task-progress 表 |
| JEPA-WAM（Joint） | arXiv HTML + tables | 有：RoboTwin 100 episodes/setting；真机 10 rollouts/task/setting | 有 | visual/spatial OOD；真机 ID/OOD | temporal-gap、patch correlation、residual | 真机 Table 15 逐任务数值 |
| JEPA-WAM（Visual Instruction） | arXiv HTML + tables | 有：11-task ID/OOD-S/OOD-I；bank ablation；1,370 demos；RTX 5090 inference | 有 | scene OOD、instruction OOD | UMAP、visual-bank qualitative | 机器人本体、task-wise trial 数、生成器完整型号 |
| DINO-WM | arXiv HTML + tables | 有：多环境 offline planning | 主要无 | 仿真 unseen configurations | trajectory/latent quality | 真机不适用；不是 action-generating WAM |
| JEPA-Bisim | arXiv HTML + tables | 有：PointMaze/PushT、5 visual shifts | 无 | background/distractor shift | paired failure/success rollouts | 不是完整 WAM policy |
| RLA-WM | arXiv HTML + abstract | 部分；指标定义已确认 | 有/待正文核对 | real-world policy improvement 待核 | RLA residual/quality-speed | 平台、trials、OOD |
| MCR DINO WM | arXiv HTML + abstract | 部分 | 有 | unseen indoor/outdoor | cost/latent geometry | platform、trials、完整 success 表 |
| DUET-DINO | arXiv HTML + abstract | 部分 | 待核 | visual distribution shifts | cross-view encoder comparison | physical deployment、episodes |
| ReWAM | arXiv HTML + abstract | 部分 | 待核 | RoboTwin/RoboDojo shift 待核 | bottleneck/gradient routing | DINO checkpoint、RoboDojo protocol |
| What Drives Success in JEPA-WMs | arXiv HTML + tables | 有：多 planner、data scaling、3 seeds | 有真实 DROID data；闭环待核 | real-to-sim / holdout transfer | rollout decoding、metric correlation | final task tables、hardware |
| Reconstruction or Semantics? | arXiv HTML + tables | 有：fixed protocol、ID/OOD episodes、bootstrap CI | 待核 | distractor/instruction OOD | encoder-ceiling、OOD rollout、probe | BridgeV2 real/sim split、hardware |
