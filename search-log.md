# 检索记录

## 当前批次

- 检索日期：2026-10-09（Asia/Shanghai）。
- 主要来源：arXiv API、arXiv HTML/PDF、官方项目页和官方代码仓库。
- 去重键：优先使用 arXiv ID；标题只用于人工复核。
- 主查询：`JEPA robotics policy`、`V-JEPA robotics`、`JEPA-WAM`、`world action model`、`JEPA-VLA`、`V-JEPA 2`。
- 纳入策略：优先纳入直接提出 JEPA/WAM/policy 方法的工作；同时保留 V-JEPA 2 foundation 和 DreamZero 作为基础模型/非 JEPA WAM 对照。

## 已纳入

| 日期 | arXiv ID | 类别 | 处理状态 |
|---|---|---|---|
| 2025-06-11 | 2506.09985 | V-JEPA 2 foundation / latent world model | 已整理 |
| 2026-02-12 | 2602.11832 | JEPA-VLA | 已整理 |
| 2026-02-17 | 2602.15922 | DreamZero / WAM baseline | 已整理 |
| 2026-08-04 | 2609.20277 | JEPA-WAM / visual instruction | 已整理 |
| 2026-08-10 | 2608.09381 | JEPA-WAM / joint transition-action | 已整理 |
| 2026-09-09 | 2609.09630 | JEPA Policy | 已整理 |
| 2026-09-29 | 2609.37250 | V-JEPA Policy | 已整理 |
| 2026-10-03 | 2610.06965 | ACG-WAM | 已整理 |
| 2026-10-07 | 2610.10515 | RoboJEPA | 已整理 |
| 2026-10-08 | 2610.12285 | PLaW-VLA | 已整理 |
| 2026-10-08 | 2610.12407 | LeWAM | 已整理 |
| 2024-11-07 | 2411.04983 | DINO-WM | 已整理 |
| 2026-02-20 | 2602.18639 | JEPA-Bisim | 已整理 |
| 2026-05-08 | 2605.07079 | RLA-WM | 已整理 |
| 2026-08-10 | 2608.09073 | DINO-family MCR world model | 已整理 |
| 2026-09-09 | 2609.10506 | DUET-DINO | 已整理 |
| 2026-09-29 | 2609.38163 | ReWAM | 已整理 |
| 2025-12-30 | 2512.24497 | JEPA-WM design study | 已整理 |
| 2026-05-07 | 2605.06388 | Semantic vs reconstruction encoder study | 已整理 |
| 2026-09-03 | 2609.04193 | GIFT / guided intermediate feature training | 已整理 |
| 2025-10-17 | 2510.15530 | VO-DP / semantic-geometric intermediate feature fusion | 已整理 |
| 2026-04-07 | 2604.06067 | HiPolicy / hierarchical multi-frequency feature fusion | 已整理 |

## 后续增量扫描

1. 每周按 `JEPA-WAM`、`world action model`、`V-JEPA policy` 扫描 arXiv 新提交。
2. 对标题相同但版本不同的条目只保留最新版本，同时在卡片记录版本变化。
3. 新论文先进入候选表，只有完成作者单位、实验协议和真机泛化核对后才加入总览表。
4. 对只给 demo/项目页、不提供可复核实验协议的工作，单独标记为“候选，不进入主表”。

## Encoder-specific notes

- V-JEPA/V-JEPA 2：已有多篇直接用于 WAM、VLA 或 action-conditioned world model。
- DINOv2/DINOv3：已有 DINO-WM、DINO residual/RLA-WM、DUET-DINO、ReWAM 等路线。
- I-JEPA：补录用户指出的 `2609.27455`（Latent evolving World Action Model），直接使用 I-JEPA-H/14；此前未发现直接应用的判断属于漏检，不是不存在的证据。

## 用户补充核查（2026-10-10）

- `2609.27455`，首次提交 2026-09-23，阅读 v2（2026-09-24）。已新增卡片、总表、encoder 索引及 BibTeX。
- 关键消歧：I-JEPA LeWAM（Xueji Fang 等，2609.27455）≠ NVIDIA LeWAM（Shashank Hegde 等，2610.12407）。

## 中间多层/层级特征融合补充（2026-10-10）

- `2609.04193` GIFT：直接研究 action pathway 共享的 intermediate visual features，用 geometry、affordance、goal 三类结构监督覆盖 VLA 与 WAM。
- `2510.15530` VO-DP：融合 VGGT 内的 DINOv2 semantic features 与 geometric features，使用 cross-attention 和 CNN compression 进入 diffusion policy。
- `2604.06067` HiPolicy：融合不同 temporal frequency 的 observation features；属于层级/多频 feature fusion，需与 frozen foundation encoder 的 transformer intermediate-layer fusion 分开标记。
