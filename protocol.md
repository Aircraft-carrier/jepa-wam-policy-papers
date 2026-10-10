# 文献检索与证据协议

## 检索范围

- 时间窗口：优先 2025-06-11 至当前日期 2026-10-09。
- 核心关键词：`JEPA`, `V-JEPA`, `JEPA policy`, `JEPA-VLA`, `world action model`, `WAM`, `predictive latent world model`, `robot policy`。
- 核心来源：arXiv、论文 HTML/PDF、官方项目页、官方代码仓库；搜索引擎结果只用于发现候选项。
- 纳入层级：
  - A：直接提出 JEPA latent + robot policy/WAM。
  - B：以 V-JEPA 2 等 predictive visual representation 改善 VLA/policy。
  - C：非 JEPA WAM 强基线，用来比较 video-generation prior、数据和真机泛化。

## 每篇论文必须回答

1. 作者与单位是否来自论文首页，而不是项目网页。
2. benchmark 是 simulation、real robot 还是两者；指标是 success、task progress、reward 还是 partial completion。
3. 是否给出 seed、episode/trial 数、checkpoint 选择协议和训练预算。
4. 泛化属于新任务、物体/颜色、布局/光照、场景扰动、embodiment 还是跨数据来源。
5. 可视化是 rollout qualitative、latent decoding、PCA/probe、scaling curve 还是 failure analysis。
6. 真机是否只是 seen-task demonstration，还是有明确 zero-shot / OOD protocol。

## 结果书写规则

- 不把 percentage point gain 写成相对百分比提升。
- 不把 simulation randomized scene 写成 real-world generalization。
- 不把摘要中的“超过 2×”替代逐任务表格；完整表格缺失时写“待核对”。
- success rate 与 task progress 分栏记录，不能直接排序。
- 对 checkpoint selection、seed 数过少、不同 embodiment 或不同训练数据保持显式警告。
