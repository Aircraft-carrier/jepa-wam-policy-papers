# Encoder → WAM / Policy 索引

| Encoder 家族 | 论文 | 用法 | 控制/规划接口 | 代表性评测 | 真机/OOD |
|---|---|---|---|---|---|
| V-JEPA 2 / 2.1 | V-JEPA 2 | action-conditioned latent WM；image-goal planning | latent MPC / goal-image | Franka zero-shot pick-and-place | 两实验室 Franka、zero-shot |
| V-JEPA 2.1 | V-JEPA Policy | frozen latent + future predictor + flow action expert | future-informed KV → action | LIBERO、LIBERO-Plus、RoboCasa-GR1 | Marvin 双臂、DROID transfer |
| V-JEPA 2.1 | JEPA-WAM Joint | joint current-future target + shared predictor | transition/action shared backbone | LIBERO-Plus、RoboTwin、5 real tasks | ID/OOD bimanual |
| V-JEPA 2.1 | JEPA-WAM Visual Instruction | generated visual goal bank | goal tokens → video/action experts | 11-task ID/OOD-S/OOD-I | scene + instruction OOD |
| V-JEPA 2 | JEPA-VLA | visual foundation injection into VLA | concat / gated cross-attention | LIBERO、LIBERO-Plus、RoboTwin、CortexBench | Piper layout/light OOD |
| DINOv2 | DINO-WM | frozen patch features + latent dynamics | CEM/MPC to goal feature | PointMaze、PushT、Granular、6 environments | mainly simulation |
| DINOv2 / SimDINOv2 / iBOT | JEPA-Bisim | predictive latent + bisimulation | robust latent MPC | PointMaze、PushT、5 visual shifts | simulation OOD |
| DINO residual | RLA-WM | residual latent action + flow matching | RLA-WM / minimalist WAM | feature prediction、LIBERO、real-world data | real-world policy improvement |
| DINO-family | MCR DINO WM | autoregressive rollout + monotone cost ranking | CEM cost ordering | GNM image-goal navigation | unseen indoor/outdoor robot |
| DINOv3 + V-JEPA 2 comparison | DUET-DINO | cross-view latent dynamics | 7-DoF latent planning | Reach、Angled Reach、Lift | visual-shift robustness |
| DINO features | ReWAM | calibration + temporal bottleneck + action-gradient shaping | compact world state + action head | RoboTwin 2.0、RoboDojo | protocol待核 |
| V-JEPA / V-JEPA 2 + DINO comparisons | What Drives Success in JEPA-WMs | controlled encoder/planner study | CEM/GD/Nevergrad latent planning | MetaWorld、Maze、Push-T、Wall、RoboCasa | DROID real-world data |
| V-JEPA 2.1 + Web-DINO + SigLIP 2 | Reconstruction or Semantics? | fixed DiT world-model encoder ablation | policy-in-the-loop + CEM | BridgeV2 ID/OOD | hardware split待核 |
| I-JEPA-H/14 | LeWAM：Latent evolving World Action Model（2609.27455） | frozen encoder + AdaFuse + joint future/action + DemoDPO | shared predictor / flow action generation | RoboTwin Avg. 92.28% | 双 Piper；3 tasks、50 rollouts/task；真机 task progress |

## 选型结论

- **想复现 OpenWAM 的最直接对照**：V-JEPA Policy、JEPA-WAM Joint、JEPA-WAM Visual Instruction。
- **想做 frozen encoder ablation**：V-JEPA 2.1、DINOv2/DINOv3、Web-DINO、SigLIP 2 按统一 policy/WAM head 比较。
- **想研究 planner robustness**：DINO-WM、JEPA-Bisim、MCR DINO WM、What Drives Success in JEPA-WMs。
- **想研究 action-conditioned representation**：RLA-WM、DUET-DINO、ReWAM。
- **I-JEPA**：`2609.27455` 明确使用冻结 I-JEPA-H/14 做 WAM，并与 DINOv3/V-JEPA 2 比较。此前“没有找到”的表述是检索遗漏，已在用户提供该论文后纠正。
