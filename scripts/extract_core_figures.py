from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

import requests


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
FIGURES = ROOT / "assets" / "figures"
MANIFEST = ROOT / "assets" / "figure-manifest.json"


def text_only(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def arxiv_url(source: str) -> str | None:
    match = re.search(r"https?://arxiv\.org/html/[^)\s]+", source)
    if match:
        return match.group(0)
    match = re.search(r"https?://arxiv\.org/abs/([^)/\s]+)", source)
    return f"https://arxiv.org/html/{match.group(1)}" if match else None


def figures_from_html(source: str) -> list[dict]:
    found = []
    for block in re.findall(r"<figure\b.*?</figure>", source, flags=re.I | re.S):
        caption_match = re.search(r"<figcaption\b[^>]*>(.*?)</figcaption>", block, flags=re.I | re.S)
        caption = text_only(caption_match.group(1) if caption_match else "")
        asset_match = re.search(r"<(?:img|object)\b[^>]*(?:src|data)=\"([^\"]+)\"", block, flags=re.I | re.S)
        if not asset_match:
            continue
        asset = html.unescape(asset_match.group(1))
        lowered = caption.lower()
        score = 0
        figure_number = re.search(r"(?:figure|fig\.)\s*(\d+)", lowered)
        if figure_number and int(figure_number.group(1)) >= 10:
            score -= 12
        for keyword, points in [
            ("architecture", 14), ("framework", 14), ("overview", 12), ("overall", 10),
            ("model", 8), ("method", 8), ("training", 7), ("pipeline", 7),
            ("world action", 8), ("world model", 6), ("schematic", 6), ("joint video", 6),
        ]:
            if keyword in lowered:
                score += points
        for keyword, points in [
            ("result", 8), ("rollout", 7), ("evaluation", 7), ("benchmark", 7),
            ("task", 4), ("visualization", 4), ("ablation", 4),
        ]:
            if keyword in lowered:
                score -= points
        if re.search(r"(?:arch|framework|overview|pipeline|method|model)", asset, re.I):
            score += 5
        if re.search(r"(?:schema|flowchart|teaser|architecture|framework)", asset, re.I):
            score += 6
        if asset.lower().endswith(".svg"):
            score += 1
        found.append({"caption": caption, "asset": asset, "score": score})
    return sorted(found, key=lambda item: item["score"], reverse=True)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    manifest = {}
    session = requests.Session()
    session.headers.update({"User-Agent": "jepa-wam-policy-papers/1.0 figure extractor"})
    for path in sorted(PAPERS.glob("*.md")):
        source = path.read_text(encoding="utf-8")
        page_url = arxiv_url(source)
        if not page_url:
            print(f"SKIP {path.stem}: no arXiv HTML/abs link", file=sys.stderr)
            continue
        try:
            response = session.get(page_url, timeout=45)
            response.raise_for_status()
            candidates = figures_from_html(response.text)
            if not candidates:
                print(f"SKIP {path.stem}: no figure found", file=sys.stderr)
                continue
            selected = candidates[0]
            asset_url = urljoin("https://arxiv.org/html/", selected["asset"])
            image = session.get(asset_url, timeout=45)
            image.raise_for_status()
            suffix = Path(selected["asset"].split("?")[0]).suffix.lower() or ".png"
            if suffix not in {".png", ".jpg", ".jpeg", ".svg", ".webp"}:
                suffix = ".png"
            output = FIGURES / f"{path.stem}{suffix}"
            output.write_bytes(image.content)
            manifest[path.stem] = {
                "path": f"assets/figures/{output.name}",
                "caption": selected["caption"],
                "source_url": page_url,
                "asset_url": asset_url,
                "score": selected["score"],
            }
            print(f"OK {path.stem}: {selected['caption'][:100]}")
        except Exception as exc:
            print(f"SKIP {path.stem}: {exc}", file=sys.stderr)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(manifest)} core figures to {MANIFEST}")


if __name__ == "__main__":
    main()
