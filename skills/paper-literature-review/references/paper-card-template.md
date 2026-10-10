# Paper Card Template

Copy this structure to `papers/<arxiv-id>-<short-slug>.md`. Replace every placeholder with source-backed content or mark it as `待核对`.

```markdown
# <论文标题>

## 1. 基本信息
- 作者：<作者>。
- 单位：<单位>。
- 日期：首次提交 <YYYY-MM-DD>；阅读版本 <vN>，更新于 <YYYY-MM-DD>。
- 链接：[arXiv](<URL>) · [HTML](<URL>) · [PDF](<URL>) · [代码](<URL 或待核对>) · [模型](<URL 或待核对>)。
- 类型：<直接相关 / 邻近 / 背景；encoder、WAM、policy 或组合>。

## 2. 一句话摘要
<一句话说明输入、预测目标、动作/策略输出和主要结论。>

## 3. 主要创新点
- <创新点及其对应证据位置>。

## 4. 方法与训练信号
- <encoder 是否冻结、token/feature、预测目标、动作表示、损失、条件化和推理流程>。

## 5. Benchmark / 测评方法 / 结果
<写清任务、split、episode/rollout 数、指标、baseline、表号和最终/消融结果。>

## 6. 可视化与表示分析
- <图、probe、attention、embedding 分析；没有则写“未见明确分析”。>

## 7. 真机实验与泛化
- <平台、任务、rollout、指标，以及新任务/物体/场景/embodiment/指令的具体泛化设置>。

## 8. 与 OpenWAM 的关系
<说明可复用模块、可比较变量和不应直接比较的设置。>

## 9. 局限与待核对项
- <证据缺口、预训练规模差异、指标定义、代码/正文差异和需要继续核对的内容>。
```

## Evidence wording

- `原文报告`：数字或设置在正文、表格、图注或附录中直接出现。
- `论文代码确认`：论文未明确，但官方代码或配置可以确认；同时保留代码链接。
- `待核对`：只有摘要、搜索结果或二手资料支持，不能写成已确认事实。
- `未见明确分析`：检查过正文/附录相关位置，但没有找到该类分析；不要写成“论文没有”。
