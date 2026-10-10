---
name: add-paper
description: Add one JEPA/WAM/policy paper to this repository, update all derived indexes and citations, regenerate the GitHub Pages site, and validate the result.
---

# Add a Paper

Use this skill when the user provides a new paper, arXiv link, PDF, code repository, or title and wants it added to `/zsh/paper`. Do not overwrite an existing card until the paper identity and version have been checked.

## Inputs and identity

Resolve the canonical arXiv ID and version first. Check whether an existing file already represents the same work, including title variants and name collisions. Use an informative filename:

`papers/<arxiv-id>-<short-slug>.md`

Keep one card per distinct paper, not one card per arXiv version. Mention the version read and update date in the card.

## Required card

Create the nine sections in `references/paper-card-template.md`:

1. 基本信息
2. 一句话摘要
3. 主要创新点
4. 方法与训练信号
5. Benchmark / 测评方法 / 结果
6. 可视化与表示分析
7. 真机实验与泛化
8. 与 OpenWAM 的关系
9. 局限与待核对项

Use Chinese prose with original metric names and concise English identifiers where useful. Put source links in 基本信息. Every important result needs a source location such as Table 1, Figure 3, Section 4, or Appendix B.

## Repository synchronization

After writing the card, update only the entries supported by the source:

- `overview.md`: add one comparison-table row.
- `encoder-matrix.md`: add the paper under every encoder family it actually evaluates.
- `evidence-matrix.md`: add confirmed evidence, protocol, and unresolved fields.
- `references.bib`: add or update the arXiv-keyed BibTeX entry.
- `search-log.md`: record discovery query, source URL, inclusion reason, and date.
- `all-papers.md`: regenerate or update the complete digest so the new card appears exactly once.

Do not silently fill missing fields. Use “待核对”, “未见明确分析”, or “原文未报告” with a precise explanation.

## Build and validation

Run from the repository root:

```bash
python scripts/build_site.py
python -m py_compile scripts/build_site.py
```

Then verify:

- the new `papers/<slug>.md` exists;
- the generated `papers/<slug>.html` exists;
- `index.html` contains the paper exactly once;
- the total Markdown and HTML paper counts match;
- local links and arXiv links are not accidentally broken;
- `git diff --check` reports no whitespace errors.

Do not commit or push automatically unless the user asks. If requested, use a focused commit message such as `add <arxiv-id> paper card`.

## Completion report

Report the paper filename, sections updated, generated page, validation commands, unresolved evidence, and whether GitHub Pages files were regenerated. If the paper could not be confirmed from the primary source, say exactly which fields remain provisional.

## References

- Card template and field guidance: `references/paper-card-template.md`
- Full review workflow: `../paper-literature-review/SKILL.md`
