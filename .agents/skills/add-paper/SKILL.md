---
name: add-paper
description: Add one JEPA/WAM/policy paper to this repository, update all derived indexes and citations, regenerate the GitHub Pages site, and validate the result.
---

# Add a Paper

Use this skill when the user provides a new paper, arXiv link, PDF, code repository, or title and wants it added to `/zsh/paper`. The completed change must keep the Markdown library, comparison indexes, citations, figures, generated website, and validation counts consistent. Do not overwrite an existing card until the paper identity and version have been checked.

## Operating order

Follow this order and keep intermediate files reviewable:

1. **Discover and identify** the primary source.
2. **Extract and verify** evidence from HTML/PDF, appendix, official code, and model pages.
3. **Write one Markdown card** using the fixed template.
4. **Synchronize repository indexes** and citations.
5. **Select and attribute one core figure** when available.
6. **Regenerate every affected web page** and validate the complete corpus.

Do not start by editing generated HTML. Generated files must come from `scripts/build_site.py`.

## 1. Inputs and identity

Resolve the canonical arXiv ID and version first. Check whether an existing file already represents the same work, including title variants and name collisions. Use an informative filename:

`papers/<arxiv-id>-<short-slug>.md`

Keep one card per distinct paper, not one card per arXiv version. Mention the version read and update date in the card.

If the paper has a title collision, record the distinction in the card and `search-log.md`. If the source is not available from a primary page, stop the factual extraction at the confirmed fields and mark the rest `待核对`.

## 2. Evidence extraction

Before writing, collect these facts:

- title, authors, institutions, arXiv ID/version/date, official code/checkpoint links;
- encoder family and whether it is frozen, partially trainable, or end-to-end trained;
- visual tokens/features, action representation, predictor/backbone, conditioning, objective, and inference loop;
- benchmark name, task count, split, episode/rollout denominator, seeds, metric definition, baseline, and table/figure location;
- real-robot platform, tasks, number of trials, success/progress definition, and every explicit OOD axis;
- core architecture figure candidate, figure number, caption, source HTML/PDF URL, and local asset path.

Treat search snippets and project-page numbers as discovery hints only. Do not promote them to confirmed results without a primary-source location.

## 3. Required card

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
- `assets/figure-manifest.json` and `assets/figures/`: add one core architecture/method figure when the primary paper HTML exposes one, preserving the original caption, source URL, and local filename. Prefer an architecture/framework/overview figure over a result, rollout, or ablation plot.
- `README.md`: update repository-level text only when it becomes stale.

Do not silently fill missing fields. Use “待核对”, “未见明确分析”, or “原文未报告” with a precise explanation.

## 5. Figure workflow

Try the automated extractor first:

```bash
python scripts/extract_core_figures.py
```

The extractor scans all cards, so review the target paper's manifest entry and do not commit unrelated figure changes. If it selected the wrong figure, replace only the target asset and update its `caption`, `source_url`, and `asset_url` in `assets/figure-manifest.json`. If no architecture figure is available, omit the asset and write `核心结构图暂未提取` rather than using an arbitrary result plot.

## 6. Build and validation

Run from the repository root:

```bash
python scripts/build_site.py
python -m py_compile scripts/build_site.py
python -m py_compile scripts/extract_core_figures.py
git diff --check
```

Then verify:

- the new `papers/<slug>.md` exists;
- the generated `papers/<slug>.html` exists;
- `index.html`, `overview.html`, and `figures.html` contain the new paper or its generated figure entry;
- the total Markdown and HTML paper counts match;
- the figure manifest entry points to an existing asset, if a figure was added;
- local links and arXiv links are not accidentally broken;
- `git diff --check` reports no whitespace errors;
- `git status` contains only intended paper, index, citation, figure, and generated-site changes.

A compact corpus check is:

```bash
python - <<'PY'
from pathlib import Path
root = Path('.')
assert len(list((root / 'papers').glob('*.md'))) == len(list((root / 'papers').glob('*.html')))
print('paper Markdown/HTML counts match')
PY
```

Do not commit or push automatically unless the user asks. If requested, use a focused commit message such as `add <arxiv-id> paper card`.

## 7. Completion report

Report the paper filename, canonical arXiv/version, sections and indexes updated, generated pages, figure status, validation commands, unresolved evidence, and whether GitHub Pages files were regenerated. If the paper could not be confirmed from the primary source, say exactly which fields remain provisional. If no commit/push was requested, state that the changes are local only.

## References

- Card template and field guidance: `references/paper-card-template.md`
- Full review workflow: `../paper-literature-review/SKILL.md`
