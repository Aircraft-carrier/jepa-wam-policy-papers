from __future__ import annotations

import html
import json
import re
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
ASSETS = ROOT / "assets"


def section(text: str, number: int) -> str:
    match = re.search(rf"^## {number}\. .*?\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match.group(1).strip() if match else ""


def first_value(text: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}：(.+)$", text, re.M)
    return re.sub(r"\*\*|`", "", match.group(1)).strip() if match else ""


def clean_text(value: str) -> str:
    return re.sub(r"\[([^]]+)\]\([^)]*\)|[*`#]", r"\1", value).strip()


def tags_for(text: str) -> list[str]:
    lowered = text.lower()
    tags = []
    for needle, label in [
        ("i-jepa", "I-JEPA"),
        ("v-jepa", "V-JEPA"),
        ("dino", "DINO"),
        ("wam", "WAM"),
        ("policy", "Policy"),
        ("真机", "真机"),
        ("real-world", "真机"),
        ("robotwin", "RoboTwin"),
    ]:
        if needle in lowered or needle in text:
            tags.append(label)
    return list(dict.fromkeys(tags))


def parse_card(path: Path) -> dict:
    source = path.read_text(encoding="utf-8")
    title_match = re.search(r"^# (.+)$", source, re.M)
    title = title_match.group(1).strip() if title_match else path.stem
    summary = clean_text(section(source, 2))
    basic = section(source, 1)
    arxiv = re.search(r"https?://arxiv\.org/abs/[^)\s]+", basic)
    date = first_value(basic, "日期")
    paper_type = first_value(basic, "类型")
    benchmark = clean_text(section(source, 5)).split("\n")[0]
    real_world = clean_text(section(source, 7)).split("\n")[0]
    slug = path.stem
    body = markdown.markdown(
        source,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
        output_format="html5",
    )
    return {
        "slug": slug,
        "title": title,
        "summary": summary,
        "authors": clean_text(first_value(basic, "作者")),
        "date": date,
        "type": paper_type,
        "arxiv": arxiv.group(0) if arxiv else "",
        "benchmark": benchmark,
        "real_world": real_world,
        "tags": tags_for(source),
        "source": f"papers/{path.name}",
        "html": body,
    }


def page_shell(title: str, body: str, active: str = "") -> str:
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#101827">
  <title>{html.escape(title)} · JEPA / WAM Papers</title>
  <link rel="stylesheet" href="{'../' if active == 'paper' else ''}assets/styles.css">
</head>
<body>
  <header class="topbar"><a class="brand" href="{'../' if active == 'paper' else ''}index.html"><span class="brand-mark">◈</span> JEPA / WAM Papers</a><nav><a href="{'../' if active == 'paper' else ''}index.html">总览</a><a href="{'../' if active == 'paper' else ''}all-papers.md">完整汇编</a><a href="{'../' if active == 'paper' else ''}overview.md">研究索引</a></nav></header>
  {body}
  <footer>持续整理视觉表征、世界模型与机器人策略论文 · Markdown 源文件可在仓库中直接阅读</footer>
</body>
</html>'''


def card_html(paper: dict) -> str:
    tags = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in paper["tags"])
    return f'''<article class="paper-card" data-search="{html.escape((paper["title"] + paper["summary"] + paper["authors"] + " ".join(paper["tags"])).lower())}" data-tags="{' '.join(paper["tags"])}">
      <div class="card-top"><span class="paper-id">{html.escape(paper["slug"].split("-")[0])}</span><span class="date">{html.escape(paper["date"][:24])}</span></div>
      <h3><a href="papers/{html.escape(paper["slug"])}.html">{html.escape(paper["title"])}</a></h3>
      <p>{html.escape(paper["summary"][:220])}</p>
      <div class="tags">{tags}</div>
      <div class="card-links"><a href="papers/{html.escape(paper["slug"])}.html">阅读解读 →</a>{f'<a href="{html.escape(paper["arxiv"])}" target="_blank" rel="noreferrer">arXiv ↗</a>' if paper["arxiv"] else ''}</div>
    </article>'''


def build_index(papers: list[dict]) -> None:
    cards = "\n".join(card_html(paper) for paper in papers)
    tag_counts = {}
    for paper in papers:
        for tag in paper["tags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    filters = '<button class="filter active" data-filter="all">全部</button>' + "".join(
        f'<button class="filter" data-filter="{html.escape(tag)}">{html.escape(tag)} <small>{count}</small></button>'
        for tag, count in sorted(tag_counts.items())
    )
    body = f'''<main class="container">
  <section class="hero"><div><p class="eyebrow">LITERATURE MAP · UPDATED 2026</p><h1>JEPA、WAM 与<br><em>机器人策略</em>论文地图</h1><p class="lede">聚合视觉表征编码器、潜在世界模型和 policy learning 的论文解读，重点追踪 DINO、V-JEPA、I-JEPA 与 WAM 的连接。</p><div class="hero-actions"><a class="button primary" href="#papers">浏览全部论文</a><a class="button" href="all-papers.md">打开完整汇编</a></div></div><div class="hero-orbit"><div class="orbit-core">JEPA<br><span>→ WAM → Policy</span></div><i class="orb orb-a">DINO</i><i class="orb orb-b">V-JEPA</i><i class="orb orb-c">I-JEPA</i></div></section>
  <section class="stats"><div><strong>{len(papers)}</strong><span>篇论文卡片</span></div><div><strong>{len(tag_counts)}</strong><span>主题标签</span></div><div><strong>{sum('真机' in p['tags'] for p in papers)}</strong><span>含真机实验</span></div><div><strong>1</strong><span>统一阅读模板</span></div></section>
  <section class="section-head" id="papers"><div><p class="eyebrow">PAPER INDEX</p><h2>全部论文</h2></div><label class="search"><span>⌕</span><input id="search" type="search" placeholder="搜索标题、作者、编码器…"></label></section>
  <div class="filters">{filters}</div><div class="paper-grid" id="paper-grid">{cards}</div><p class="empty" id="empty">没有匹配的论文，请更换关键词或筛选条件。</p>
  <section class="resource-panel"><div><p class="eyebrow">RESEARCH KIT</p><h2>配套研究资料</h2><p>除了逐篇解读，仓库还保留编码器矩阵、证据矩阵、检索日志、评测协议和 BibTeX，便于继续扩展实验与写作。</p></div><div class="resource-links"><a href="encoder-matrix.md">编码器矩阵 <span>↗</span></a><a href="evidence-matrix.md">证据矩阵 <span>↗</span></a><a href="protocol.md">评测协议 <span>↗</span></a><a href="references.bib">BibTeX <span>↗</span></a></div></section>
</main>'''
    (ROOT / "index.html").write_text(page_shell("论文总览", body) + '<script src="assets/site.js"></script>', encoding="utf-8")


def build_paper_pages(papers: list[dict]) -> None:
    for paper in papers:
        tags = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in paper["tags"])
        meta = f'''<div class="paper-meta"><span>{html.escape(paper["date"])}</span><span>{html.escape(paper["type"])}</span><span>{tags}</span></div>'''
        links = f'<a class="button primary" href="{html.escape(paper["arxiv"])}" target="_blank" rel="noreferrer">打开 arXiv ↗</a>' if paper["arxiv"] else ""
        body = f'''<main class="container paper-container"><a class="back-link" href="../index.html">← 返回论文总览</a><article class="paper-article"><header class="paper-header"><p class="eyebrow">PAPER NOTE · {html.escape(paper["slug"].split("-")[0])}</p><h1>{html.escape(paper["title"])}</h1><p class="paper-summary">{html.escape(paper["summary"])}</p>{meta}<div class="hero-actions">{links}<a class="button" href="{html.escape('../' + paper['source'])}">查看 Markdown 源文件</a></div></header><div class="article-body">{paper["html"]}</div></article></main>'''
        (PAPERS / f'{paper["slug"]}.html').write_text(page_shell(paper["title"], body, "paper"), encoding="utf-8")


def main() -> None:
    papers = [parse_card(path) for path in sorted(PAPERS.glob("*.md"))]
    build_index(papers)
    build_paper_pages(papers)
    (ROOT / "data.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built website for {len(papers)} papers")


if __name__ == "__main__":
    main()
