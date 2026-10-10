# JEPA / WAM / Policy 文献整理

> **GitHub Pages 仓库建议名：`jepa-wam-policy-papers`**
>
> 仓库根目录已经包含可直接部署的静态网站：`index.html` 是论文总览，`papers/*.html` 是逐篇解读页。每篇论文的 Markdown 源文件仍然保留，方便继续编辑和审阅。

## 网站预览与部署

- 本地预览：执行 `python3 -m http.server 8000`，然后打开 `http://localhost:8000/`。
- 重新生成页面：执行 `python scripts/build_site.py`。
- GitHub Pages：将本目录作为仓库根目录推送到 `main` 分支，`.github/workflows/pages.yml` 会自动发布网站。
- 网站结构：`index.html` 汇总、`papers/*.html` 单篇模板、`assets/` 样式与筛选逻辑、`papers/*.md` 原始解读。

> 更新时间：2026-10-10（Asia/Shanghai）。范围优先覆盖 2026 年公开、直接讨论 JEPA latent、world-action model（WAM）或 predictive latent world model + robot policy 的论文。数字以论文 HTML/PDF 正文为准；尚未从正文确认的字段明确标为“待核对”。

## 固定论文卡片格式

每篇论文一个 Markdown 文件，字段顺序固定：

1. 基本信息：标题、作者、单位、日期、链接、论文类型
2. 一句话摘要
3. 主要创新点
4. 方法与训练信号
5. Benchmark / 测评方法 / 结果
6. 可视化与表示分析
7. 真机实验：平台、任务、指标、泛化设置
8. 与 OpenWAM 的关系
9. 局限与待核对项

## 文献卡片

- [V-JEPA Policy](papers/2609.37250-vjepa-policy.md)
- [LeWAM](papers/2610.12407-lewam.md)
- [RoboJEPA](papers/2610.10515-robojepa.md)
- [ACG-WAM](papers/2610.06965-acg-wam.md)
- [PLaW-VLA](papers/2610.12285-plaw-vla.md)
- [JEPA Policy](papers/2609.09630-jepa-policy.md)
- [JEPA-VLA](papers/2602.11832-jepa-vla.md)
- [V-JEPA 2](papers/2506.09985-v-jepa-2.md)
- [DreamZero / World Action Models are Zero-shot Policies](papers/2602.15922-dreamzero.md)
- [JEPA-WAM: Joint-Embedding World Modeling](papers/2608.09381-jepa-wam-joint.md)
- [JEPA-WAM: Generated Visual Instructions](papers/2609.20277-jepa-wam-visual-instruction.md)
- [DINO-WM](papers/2411.04983-dino-wm.md)
- [JEPA-Bisim](papers/2602.18639-jepa-bisim.md)
- [RLA-WM](papers/2605.07079-rla-wm.md)
- [MCR DINO World Model](papers/2608.09073-mcr-dino-world-model.md)
- [DUET-DINO](papers/2609.10506-duet-dino.md)
- [ReWAM](papers/2609.38163-rewam.md)
- [What Drives Success in Physical Planning with JEPA-WMs](papers/2512.24497-what-drives-jepa-wm.md)
- [Reconstruction or Semantics?](papers/2605.06388-reconstruction-or-semantics.md)

- [LeWAM：Latent evolving World Action Model（I-JEPA）](papers/2609.27455-lewam-ijepa.md)

## 推荐的检索、分析、整理技能

### 当前环境可直接复用

- `explain-code`：分析论文代码、训练/推理路径、tensor shape 和实现差异；位置：`/zsh/codex-shared/skills/explain-code`。
- `skill-installer`：安装或更新外部 Codex skill；适合把文献检索、PDF 解析、Zotero/Markdown 整理流程加入环境。
- `openai-docs`：只用于 Codex/OpenAI 产品文档，不适合作为领域论文检索器。

### 建议补充的外部能力（按论文收尾阶段优先级）

1. **Scientific literature search / review**：封装 Semantic Scholar、OpenAlex、Crossref、arXiv API，支持去重、引用网络、按日期和主题筛选。
2. **PDF / HTML paper extraction**：抽取摘要、作者单位、表格、图注、实验设置，并保留页码/章节证据。
3. **Critical paper analysis**：固定检查创新是否有消融支持、benchmark 是否公平、sim-to-real 是否有分布偏移、结果是否可复现。
4. **Reference manager / BibTeX**：用 DOI/arXiv ID 去重并同步 BibTeX、Markdown 卡片和总表。
5. **Paper-to-notes / knowledge base**：将单篇卡片自动汇总到总表，并维护“待核对”队列。

建议安装来源：优先选择可审计的 GitHub skill 仓库，并先检查其 `SKILL.md`、网络权限、数据留存方式和是否支持 arXiv/OpenAlex/Semantic Scholar；不要把摘要搜索结果直接当作实验事实。

### 推荐组合

| 任务 | 推荐能力 | 用法 |
|---|---|---|
| 找论文、去重、追引用 | Semantic Scholar / OpenAlex / Crossref / arXiv API skill | 先用 DOI、arXiv ID 和标题去重，再按年份、主题词和引用网络扩展 |
| 读 PDF、抽表格和图注 | GROBID 或 marker/PDF extraction skill | 保留章节、表号、图号和页码，不只保存摘要 |
| 批判性分析 | systematic-review / critical-reading skill | 强制记录 baseline、训练预算、seed、episode 数、指标定义和统计协议 |
| 整理引用 | Zotero + Better BibTeX 或 BibTeX skill | 用 DOI/arXiv ID 作为唯一键，同步 `.bib` 与 Markdown 卡片 |
| 代码与复现核对 | `explain-code` + repository-inspection skill | 对照论文方法、官方代码、配置和 checkpoint，标记 paper/code discrepancy |

安装外部 skill 前建议执行 `skill-installer` 的仓库审查流程；本目录暂不自动安装未经审计的第三方 skill。

### 已检索到的具体候选仓库

以下仓库在 2026-10-09 通过 GitHub 仓库 API 检查过，均有 research/literature 相关说明；安装前仍应审查权限、依赖和输出格式：

- [Epsilon617/Codex-Academic-Skills](https://github.com/Epsilon617/Codex-Academic-Skills)：Codex 研究工作流集合，适合先找可复用的 literature-review / evaluation skill。
- [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills)：跨客户端的 `SKILL.md` catalog，覆盖 literature review、research design、project memory 和 manuscript writing。
- [xingtaxueshu/literature-review-skills](https://github.com/xingtaxueshu/literature-review-skills)：问题细化、方法比较、矛盾映射、研究空白发现，适合论文收尾阶段的批判性整理。
- [kasabulanka2019/zotero-review-matrix-skill](https://github.com/kasabulanka2019/zotero-review-matrix-skill)：Zotero review matrix 和 DOCX synthesis，适合把本文库扩展为可筛选的证据矩阵。
- [ViewWay/academic-research-skill](https://github.com/ViewWay/academic-research-skill)：跨学科检索与论文写作 skill pack，适合补充数据库检索和写作工作流。
- [tigerless-labs/paper-radar](https://github.com/tigerless-labs/paper-radar)：更偏 arXiv 监控/发现，不替代正文分析，但适合做 WAM/JEPA 新论文的增量扫描。

推荐优先级：`literature-review-skills` → `zotero-review-matrix-skill` → `Codex-Academic-Skills`；`paper-radar` 作为自动发现补充。

## 证据规则

- “作者单位”以论文 HTML/PDF 首页为准。
- “结果”必须记录指标、评测协议和分母/episode 数；只有宣传页数字时写明来源等级。
- “泛化”区分：新任务、新物体/颜色/几何、新场景/扰动、新 embodiment、真机 zero-shot。
- 没有明确可视化图或表示分析时写“未见明确分析”，不推断为没有。

## 维护文件

- [论文完整合辑](all-papers.md)：完整汇集 `papers/` 下所有论文卡片，带目录和源文件入口。
- [总览表](overview.md)：所有纳入论文的统一比较表。
- [证据矩阵](evidence-matrix.md)：正文来源、评测协议和待补证据。
- [检索记录](search-log.md)：查询词、纳入范围和增量扫描规则。
- [BibTeX](references.bib)：以 arXiv ID 为主键的引用索引。
- [Encoder 索引](encoder-matrix.md)：按 V-JEPA、DINO、I-JEPA 和混合路线组织论文。
