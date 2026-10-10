---
name: paper-literature-review
description: Review JEPA, DINO, V-JEPA, I-JEPA, WAM, world-model, and robot-policy papers; use it when a paper needs evidence-based extraction, comparison, or integration into this repository.
---

# Paper Literature Review

Use this skill when collecting or reviewing papers related to visual representation encoders, latent world models, world-action models, or robot policies. The output should be a reproducible Markdown card, not an unsupported summary.

## Scope and source priority

- Prefer the paper's arXiv HTML/PDF, supplementary material, official code, and official model pages.
- Use search results only to discover candidates; do not treat snippets, abstracts, or project-page claims as confirmed benchmark evidence.
- Record exact arXiv IDs, versions, dates, table/figure/appendix locations, and whether a claim is directly confirmed or still needs checking.
- Separate simulation success rate, real-robot success rate, task progress, and qualitative rollout evidence. Do not rank them as one metric.
- Distinguish encoder-only policy baselines from complete WAM/policy systems and distinguish frozen encoders from end-to-end trained encoders.

## Workflow

1. **Identify and deduplicate.** Record title, arXiv ID, version, authors, date, official links, and possible name collisions.
2. **Classify the connection.** Mark the paper as direct, adjacent, or background relative to JEPA/WAM/policy. Identify DINO, V-JEPA, I-JEPA, mixed, or other encoders.
3. **Extract the method.** Read the method and appendix for inputs, tokenization, frozen/trainable modules, prediction target, action parameterization, losses, conditioning, and inference procedure.
4. **Extract evidence.** For every reported number, capture benchmark, split, denominator, number of tasks/episodes, evaluation mode, baseline, table/figure, and whether the number is ablated or final.
5. **Check generalization.** Explicitly separate new task, object/color/geometry, scene/randomization, embodiment, instruction, and real-robot transfer.
6. **Write the card.** Follow `references/paper-card-template.md` and keep the nine fixed sections in the repository's existing order.
7. **Update indexes.** When the paper is accepted, update `overview.md`, `encoder-matrix.md`, `evidence-matrix.md`, `references.bib`, `search-log.md`, and `all-papers.md` as applicable.
8. **Regenerate the website.** Run `python scripts/build_site.py`; verify that the Markdown card and HTML detail page both exist and the homepage count increases as expected.

## OpenWAM comparison rules

- State whether the contribution is a visual encoder, latent dynamics/world model, action decoder, policy, data/evaluation protocol, or complete system.
- Compare only matched settings when possible: same dataset, task set, encoder size, training budget, and evaluation protocol.
- Preserve caveats about pretraining data, parameter count, checkpoint selection, demonstrations, simulation randomization, and real-robot metric definitions.
- If the paper does not show a requested experiment or visualization, write “未见明确分析” or “待核对”; do not infer absence from the abstract.

## Related files

- Card template: `references/paper-card-template.md`
- Repository workflow: `../add-paper/SKILL.md`
- Existing evidence rules: `evidence-matrix.md` and `protocol.md`
