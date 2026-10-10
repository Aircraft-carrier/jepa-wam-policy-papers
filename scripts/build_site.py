from __future__ import annotations

import html
import json
import re
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
ASSETS = ROOT / "assets"
MANIFEST = ASSETS / "figure-manifest.json"


def section(text: str, number: int) -> str:
    match = re.search(rf"^## {number}\. .*?\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match.group(1).strip() if match else ""


def first_value(text: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}：(.+)$", text, re.M)
    return re.sub(r"\*\*|`", "", match.group(1)).strip() if match else ""


def clean_text(value: str) -> str:
    return re.sub(r"\[([^]]+)\]\([^)]*\)|[*`#]", r"\1", value).strip()


def compact(value: str, limit: int = 520) -> str:
    value = clean_text(value)
    value = re.sub(r"^[-|> ]+", "", value, flags=re.M)
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[:limit].rstrip() + "…"


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
    institution = first_value(basic, "单位")
    method = compact(section(source, 4), 650)
    analysis = compact(section(source, 6), 420)
    limitations = compact(section(source, 9), 420)
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
        "institution": compact(institution, 300),
        "date": date,
        "type": paper_type,
        "arxiv": arxiv.group(0) if arxiv else "",
        "method": method,
        "benchmark": compact(benchmark, 600),
        "analysis": analysis,
        "real_world": compact(real_world, 600),
        "limitations": limitations,
        "tags": tags_for(source),
        "source": f"papers/{path.name}",
        "html": body,
    }


def page_shell(title: str, body: str, active: str = "", scripts: tuple[str, ...] = ()) -> str:
    prefix = "../" if active == "paper" else ""
    script_tags = "".join(f'<script src="{prefix}{script}"></script>' for script in scripts)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#101827">
  <title>{html.escape(title)} · JEPA / WAM Papers</title>
  <link rel="stylesheet" href="{prefix}assets/styles.css?v=20261010">
  <link rel="stylesheet" href="{prefix}assets/figures.css?v=20261010">
</head>
<body>
  <header class="topbar"><a class="brand" href="{prefix}index.html"><span class="brand-mark">◈</span> JEPA / WAM Papers</a><nav><a href="{prefix}index.html">卡片总览</a><a href="{prefix}overview.html">综合表格</a><a href="{prefix}figures.html">架构图画廊</a><a href="{prefix}all-papers.md">完整汇编</a><a href="{prefix}overview.md">研究索引</a></nav></header>
  {body}
  <footer>持续整理视觉表征、世界模型与机器人策略论文 · Markdown 源文件可在仓库中直接阅读</footer>
{script_tags}
</body>
</html>'''


def card_html(paper: dict) -> str:
    tags = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in paper["tags"])
    preview = figure_preview(paper, "card-figure")
    return f'''<article class="paper-card" data-search="{html.escape((paper["title"] + paper["summary"] + paper["authors"] + " ".join(paper["tags"])).lower())}" data-tags="{' '.join(paper["tags"])}">
      <div class="card-top"><span class="paper-id">{html.escape(paper["slug"].split("-")[0])}</span><span class="date">{html.escape(paper["date"][:24])}</span></div>
      <h3><a href="papers/{html.escape(paper["slug"])}.html">{html.escape(paper["title"])}</a></h3>
      {preview}
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
  <section class="hero"><div><p class="eyebrow">LITERATURE MAP · UPDATED 2026</p><h1>JEPA、WAM 与<br><em>机器人策略</em>论文地图</h1><p class="lede">聚合视觉表征编码器、潜在世界模型和 policy learning 的论文解读，重点追踪 DINO、V-JEPA、I-JEPA 与 WAM 的连接。</p><div class="hero-actions"><a class="button primary" href="#papers">浏览全部论文</a><a class="button" href="overview.html">打开综合表格</a><a class="button" href="all-papers.md">完整汇编</a></div></div><div class="hero-orbit"><div class="orbit-core">JEPA<br><span>→ WAM → Policy</span></div><i class="orb orb-a">DINO</i><i class="orb orb-b">V-JEPA</i><i class="orb orb-c">I-JEPA</i></div></section>
  <section class="stats"><div><strong>{len(papers)}</strong><span>篇论文卡片</span></div><div><strong>{len(tag_counts)}</strong><span>主题标签</span></div><div><strong>{sum('真机' in p['tags'] for p in papers)}</strong><span>含真机实验</span></div><div><strong>1</strong><span>统一阅读模板</span></div></section>
  <section class="section-head" id="papers"><div><p class="eyebrow">PAPER INDEX</p><h2>全部论文</h2></div><label class="search"><span>⌕</span><input id="search" type="search" placeholder="搜索标题、作者、编码器…"></label></section>
  <div class="filters">{filters}</div><div class="paper-grid" id="paper-grid">{cards}</div><p class="empty" id="empty">没有匹配的论文，请更换关键词或筛选条件。</p>
  <section class="resource-panel"><div><p class="eyebrow">RESEARCH KIT</p><h2>配套研究资料</h2><p>除了逐篇解读，仓库还保留编码器矩阵、证据矩阵、检索日志、评测协议和 BibTeX，便于继续扩展实验与写作。</p></div><div class="resource-links"><a href="encoder-matrix.md">编码器矩阵 <span>↗</span></a><a href="evidence-matrix.md">证据矩阵 <span>↗</span></a><a href="protocol.md">评测协议 <span>↗</span></a><a href="references.bib">BibTeX <span>↗</span></a></div></section>
</main>'''
    (ROOT / "index.html").write_text(page_shell("论文总览", body, scripts=("assets/site.js",)), encoding="utf-8")


def build_overview(papers: list[dict]) -> None:
    rows = []
    for paper in papers:
        tags = " ".join(paper["tags"])
        tag_html = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in paper["tags"])
        rows.append(f'''<tr data-search="{html.escape((paper["title"] + paper["authors"] + paper["institution"] + paper["method"] + paper["benchmark"] + paper["real_world"] + paper["limitations"] + tags).lower())}" data-tags="{html.escape(tags)}" data-year="{html.escape(paper["date"][:4])}">
          <td class="col-title"><span class="paper-id">{html.escape(paper["slug"].split("-")[0])}</span><a href="papers/{html.escape(paper["slug"])}.html">{html.escape(paper["title"])}</a><div class="table-links"><a href="papers/{html.escape(paper["slug"])}.html">解读</a>{f' · <a href="{html.escape(paper["arxiv"])}" target="_blank" rel="noreferrer">arXiv ↗</a>' if paper["arxiv"] else ''}</div><div class="tags">{tag_html}</div></td>
          <td><strong>{html.escape(paper["date"])}</strong><br><span class="muted">{html.escape(paper["authors"][:170])}</span><br><span class="muted">{html.escape(paper["institution"][:240])}</span></td>
          <td>{html.escape(paper["summary"])}</td>
          <td>{figure_preview(paper, "table-figure")}{html.escape(paper["method"])}</td>
          <td>{html.escape(paper["benchmark"])}</td>
          <td>{html.escape(paper["analysis"])}</td>
          <td>{html.escape(paper["real_world"])}</td>
          <td>{html.escape(paper["limitations"])}</td>
        </tr>''')
    years = sorted({paper["date"][:4] for paper in papers if paper["date"][:4].isdigit()}, reverse=True)
    year_filters = '<button class="table-filter active" data-year="all">全部年份</button>' + "".join(f'<button class="table-filter" data-year="{year}">{year}</button>' for year in years)
    tag_filters = '<button class="table-filter active" data-tag="all">全部路线</button>' + "".join(f'<button class="table-filter" data-tag="{html.escape(tag)}">{html.escape(tag)}</button>' for tag in ["I-JEPA", "V-JEPA", "DINO", "WAM", "Policy", "真机"])
    body = f'''<main class="container overview-container"><section class="overview-hero"><p class="eyebrow">COMPARISON MATRIX · {len(papers)} PAPERS</p><h1>所有论文综合对照表</h1><p class="lede">将每篇论文的基本信息、方法、实验、评测、表示分析、真机泛化和局限放到同一张可检索表格中。横向滚动查看完整字段，点击标题进入逐篇解读。</p><div class="overview-kpis"><span><strong>{len(papers)}</strong>论文</span><span><strong>8</strong>核心字段</span><span><strong>2</strong>种筛选</span></div></section><section class="table-tools"><label class="search wide-search"><span>⌕</span><input id="overview-search" type="search" placeholder="搜索标题、机构、方法、Benchmark、实验或局限…"></label><div class="filter-line"><span class="filter-label">路线</span>{tag_filters}</div><div class="filter-line"><span class="filter-label">年份</span>{year_filters}</div><p class="table-count" id="table-count">显示 {len(papers)} / {len(papers)} 篇</p></section><div class="table-wrap"><table class="comparison-table"><thead><tr><th>论文 / 链接</th><th>时间 / 作者 / 机构</th><th>一句话摘要</th><th>方法与训练信号</th><th>实验与评测结果</th><th>可视化 / 表示分析</th><th>真机 / 泛化</th><th>局限与待核对</th></tr></thead><tbody id="comparison-body">{"".join(rows)}</tbody></table></div><p class="empty" id="overview-empty">没有匹配的论文，请调整搜索词或筛选条件。</p><p class="overview-note">表格内容由 `papers/*.md` 自动生成；数字和协议以论文卡片中的来源定位为准。若需要完整表格、消融表或图注，请进入对应论文详情页。</p></main>'''
    (ROOT / "overview.html").write_text(page_shell("所有论文综合对照表", body, scripts=("assets/overview.js",)), encoding="utf-8")


def figure_preview(paper: dict, css_class: str) -> str:
    figure = paper.get("figure")
    if not figure:
        return ""
    return f'<a class="{css_class}" href="papers/{paper["slug"]}.html#core-figure"><img src="{html.escape(figure["path"])}" alt="{html.escape(paper["title"])}：核心结构图" loading="lazy"></a>'


def figure_html(paper: dict, prefix: str = "", anchor: bool = True) -> str:
    figure = paper.get("figure")
    if not figure:
        return '<p class="figure-missing">核心结构图暂未提取，请查看原论文。</p>'
    image_path = html.escape(prefix + figure["path"])
    caption = html.escape(figure["caption"])
    source_url = html.escape(figure["source_url"])
    figure_id = ' id="core-figure"' if anchor else ""
    return f'''<figure class="core-figure"{figure_id}><a href="{image_path}" target="_blank" rel="noreferrer" aria-label="打开原尺寸结构图"><img src="{image_path}" alt="{caption}" loading="lazy"></a><figcaption><p>{caption}</p><div class="figure-links"><a href="{image_path}" target="_blank" rel="noreferrer">查看原尺寸 ↗</a><a href="{source_url}" target="_blank" rel="noreferrer">原论文 / 图来源 ↗</a></div><small>原图及图注归论文作者所有；保留出处供研究阅读，不代表获得再分发授权。</small></figcaption></figure>'''


def build_gallery(papers: list[dict]) -> None:
    entries = []
    for paper in papers:
        entries.append(f'''<article class="gallery-entry"><header><span class="paper-id">{html.escape(paper["slug"].split("-")[0])}</span><h2><a href="papers/{paper["slug"]}.html">{html.escape(paper["title"])}</a></h2></header>{figure_html(paper, anchor=False)}</article>''')
    total = sum(bool(paper.get("figure")) for paper in papers)
    body = f'''<main class="container gallery-container"><section class="overview-hero"><p class="eyebrow">ARCHITECTURE GALLERY · {total} / {len(papers)} PAPERS</p><h1>核心结构图画廊</h1><p class="lede">集中浏览核心架构与方法总览。点击图片打开原尺寸，点击标题进入完整解读；每张图保留原论文版本、图注与来源。</p></section><div class="gallery-grid">{"".join(entries)}</div></main>'''
    (ROOT / "figures.html").write_text(page_shell("核心结构图画廊", body), encoding="utf-8")


def build_paper_pages(papers: list[dict]) -> None:
    for paper in papers:
        tags = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in paper["tags"])
        meta = f'''<div class="paper-meta"><span>{html.escape(paper["date"])}</span><span>{html.escape(paper["type"])}</span><span>{tags}</span></div>'''
        links = f'<a class="button primary" href="{html.escape(paper["arxiv"])}" target="_blank" rel="noreferrer">打开 arXiv ↗</a>' if paper["arxiv"] else ""
        body = f'''<main class="container paper-container"><a class="back-link" href="../index.html">← 返回论文总览</a><article class="paper-article"><header class="paper-header"><p class="eyebrow">PAPER NOTE · {html.escape(paper["slug"].split("-")[0])}</p><h1>{html.escape(paper["title"])}</h1><p class="paper-summary">{html.escape(paper["summary"])}</p>{meta}<div class="hero-actions">{links}<a class="button" href="{html.escape('../' + paper['source'])}">查看 Markdown 源文件</a></div></header><div class="article-body">{paper["html"]}</div></article></main>'''
        architecture = f'<section class="architecture-section"><h2>核心结构 / 方法总览</h2>{figure_html(paper, "../")}</section>'
        body = body.replace('<div class="article-body">', architecture + '<div class="article-body">', 1)
        (PAPERS / f'{paper["slug"]}.html').write_text(page_shell(paper["title"], body, "paper"), encoding="utf-8")


def main() -> None:
    papers = [parse_card(path) for path in sorted(PAPERS.glob("*.md"))]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    for paper in papers:
        figure = manifest.get(paper["slug"])
        if figure and not (ROOT / figure["path"]).is_file():
            raise FileNotFoundError(figure["path"])
        paper["figure"] = figure
    build_index(papers)
    build_overview(papers)
    build_gallery(papers)
    build_paper_pages(papers)
    (ROOT / "data.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built website for {len(papers)} papers")


if __name__ == "__main__":
    main()
