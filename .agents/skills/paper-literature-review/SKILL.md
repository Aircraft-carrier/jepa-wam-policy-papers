---
name: paper-literature-review
description: Review JEPA, DINO, V-JEPA, I-JEPA, WAM, world-model, and robot-policy papers; use it when a paper needs evidence-based extraction, comparison, or integration into this repository.
---

# Paper Literature Review

Use this skill when collecting or reviewing papers related to visual representation encoders, latent world models, world-action models, or robot policies. The output should be a reproducible, reader-oriented Markdown card, not an unsupported summary. The reader should be able to answer four questions without opening the paper first: what problem is being solved, what information flows through the model, why the training signal is useful, and what the experiments actually prove.

## Scope and source priority

- Prefer the paper's arXiv HTML/PDF, supplementary material, official code, and official model pages.
- Use search results only to discover candidates; do not treat snippets, abstracts, or project-page claims as confirmed benchmark evidence.
- Record exact arXiv IDs, versions, dates, table/figure/appendix locations, and whether a claim is directly confirmed or still needs checking.
- Separate simulation success rate, real-robot success rate, task progress, and qualitative rollout evidence. Do not rank them as one metric.
- Distinguish encoder-only policy baselines from complete WAM/policy systems and distinguish frozen encoders from end-to-end trained encoders.

## Reader-first writing standard

Write each paper at two levels:

1. **Technical record.** Preserve exact source-backed facts: encoder, frozen/trainable status, tokens, predictor, loss, action representation, benchmark, split, denominator, metric, table/figure location, and unresolved evidence.
2. **Teaching explanation.** Translate the record into plain Chinese before using abbreviations. Explain terms such as latent representation, world model, action chunk, MPC, CEM, flow matching, diffusion policy, probe, and distribution shift the first time they appear.

Every card should contain the following reading path after the nine repository sections:

10. **先建立直觉**：用“输入 → 中间表示 → 预测/策略 → 动作 → 环境反馈”解释论文解决的问题。
11. **逐步读方法**：说明数据流、模块边界、哪些参数冻结、训练时看到什么、推理时真正运行什么。
12. **训练目标为什么合理**：把每个 loss 或 supervision 对应到希望得到的能力，并指出它可能没有约束到的东西。
13. **结果应该怎样读**：解释 benchmark、指标和对照组分别支持哪一个结论，避免把定性图、仿真成功率和真机成功率混为一谈。
14. **复现与对比清单**：列出数据、预训练 checkpoint、输入历史、预测 horizon、动作参数化、推理预算、随机种子和评测协议。
15. **读者 takeaway**：用三到五点总结“可直接借鉴”“不能直接推出”“最值得继续验证”的内容。

Do not pad a card with generic praise. If a paper does not report a field, state `原文未报告` or `待核对`. If a paragraph is an interpretation rather than a direct claim, label it `解读`.

## Workflow

1. **Identify and deduplicate.** Record title, arXiv ID, version, authors, date, official links, and possible name collisions.
2. **Classify the connection.** Mark the paper as direct, adjacent, or background relative to JEPA/WAM/policy. Identify DINO, V-JEPA, I-JEPA, mixed, or other encoders.
3. **Extract the method.** Read the method and appendix for inputs, tokenization, frozen/trainable modules, prediction target, action parameterization, losses, conditioning, and inference procedure.
4. **Extract evidence.** For every reported number, capture benchmark, split, denominator, number of tasks/episodes, evaluation mode, baseline, table/figure, and whether the number is ablated or final.
5. **Check generalization.** Explicitly separate new task, object/color/geometry, scene/randomization, embodiment, instruction, and real-robot transfer.
6. **Write the card.** Follow `references/paper-card-template.md`, keep the nine fixed sections in the repository's existing order, and append the reader-first sections 10–15.
7. **Update indexes.** When the paper is accepted, update `overview.md`, `encoder-matrix.md`, `evidence-matrix.md`, `references.bib`, `search-log.md`, and `all-papers.md` as applicable.
8. **Regenerate the website.** Run `python scripts/build_site.py`; verify that the Markdown card and HTML detail page both exist and the homepage count increases as expected.

## OpenWAM comparison rules

- State whether the contribution is a visual encoder, latent dynamics/world model, action decoder, policy, data/evaluation protocol, or complete system.
- Compare only matched settings when possible: same dataset, task set, encoder size, training budget, and evaluation protocol.
- Preserve caveats about pretraining data, parameter count, checkpoint selection, demonstrations, simulation randomization, and real-robot metric definitions.
- If the paper does not show a requested experiment or visualization, write “未见明确分析” or “待核对”; do not infer absence from the abstract.
- When expanding an existing card, preserve confirmed numbers and links. Add explanation around them rather than inventing new numbers.
- For every major conclusion, include a “what this does not show” sentence. A better latent prediction score does not automatically imply better action success, and a simulation result does not establish real-robot transfer.

## Related files

- Card template: `references/paper-card-template.md`
- Repository workflow: `../add-paper/SKILL.md`
- Existing evidence rules: `evidence-matrix.md` and `protocol.md`
