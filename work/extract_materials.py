from __future__ import annotations

import html
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from pypdf import PdfReader


ROOT = Path("/Users/david.li/Documents/Codex/2026-06-09/hi-codex-i-need-to-make")
PPTX = Path("/Users/david.li/Downloads/IDLM.pptx")
PDF = Path("/Users/david.li/Downloads/IDLM.pptx.pdf")
OVERLEAF = ROOT / "work" / "overleaf"
OUT = ROOT / "work" / "extracted"


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?", " ", text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def pptx_slide_order(z: zipfile.ZipFile) -> list[str]:
    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }
    rels = ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
    rel_map = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels
        if rel.attrib.get("Type", "").endswith("/slide")
    }
    order = []
    for sld_id in pres.findall(".//p:sldIdLst/p:sldId", ns):
        rid = sld_id.attrib[f"{{{ns['r']}}}id"]
        target = rel_map[rid]
        order.append("ppt/" + target.lstrip("/"))
    return order


def extract_pptx() -> list[dict[str, object]]:
    ns = {
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    }
    slides = []
    with zipfile.ZipFile(PPTX) as z:
        for idx, name in enumerate(pptx_slide_order(z), start=1):
            root = ET.fromstring(z.read(name))
            texts = []
            for tx_body in root.findall(".//p:txBody", ns):
                runs = [t.text or "" for t in tx_body.findall(".//a:t", ns)]
                text = clean_text(" ".join(runs))
                if text:
                    texts.append(text)
            media_refs = []
            rel_path = name.rsplit("/", 1)[0] + "/_rels/" + name.rsplit("/", 1)[1] + ".rels"
            if rel_path in z.namelist():
                rels = ET.fromstring(z.read(rel_path))
                for rel in rels:
                    target = rel.attrib.get("Target", "")
                    if "media/" in target or target.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")):
                        media_refs.append(target)
            slides.append({"slide": idx, "text": texts, "media_refs": media_refs})
    return slides


def extract_pdf_pages() -> list[dict[str, object]]:
    reader = PdfReader(str(PDF))
    pages = []
    for idx, page in enumerate(reader.pages, start=1):
        text = clean_text(page.extract_text() or "")
        pages.append({"page": idx, "text": text})
    return pages


def extract_latex_sources() -> dict[str, str]:
    paths = [
        "sec/abstract.tex",
        "sec/introduction.tex",
        "sec/preliminaries.tex",
        "sec/method.tex",
        "sec/experiments.tex",
        "appendix/proofs.tex",
        "appendix/algorithm.tex",
        "appendix/additional_experimental_results.tex",
        "appendix/experimental_details.tex",
        "arxiv/sec/abstract.tex",
        "arxiv/sec/introduction.tex",
        "arxiv/sec/method.tex",
        "arxiv/sec/experiments.tex",
        "arxiv/sec/conclusion.tex",
    ]
    result = {}
    for rel in paths:
        path = OVERLEAF / rel
        if path.exists():
            result[rel] = clean_text(path.read_text(errors="ignore"))
    return result


def extract_html_pages() -> dict[str, str]:
    pages = {}
    for name in ["blog_idlm.html", "project_page.html"]:
        path = ROOT / "work" / name
        if path.exists():
            pages[name] = clean_text(path.read_text(errors="ignore"))
    return pages


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pptx = extract_pptx()
    pdf = extract_pdf_pages()
    latex = extract_latex_sources()
    html_pages = extract_html_pages()

    (OUT / "pptx_slides.json").write_text(json.dumps(pptx, indent=2), encoding="utf-8")
    (OUT / "pdf_pages.json").write_text(json.dumps(pdf, indent=2), encoding="utf-8")
    (OUT / "latex_sections.json").write_text(json.dumps(latex, indent=2), encoding="utf-8")
    (OUT / "web_pages.json").write_text(json.dumps(html_pages, indent=2), encoding="utf-8")

    slide_notes = []
    for slide in pptx:
        text = " | ".join(slide["text"])
        slide_notes.append(f"Slide {slide['slide']:02d}: {text}")
    (OUT / "pptx_slide_notes.txt").write_text("\n".join(slide_notes), encoding="utf-8")

    pdf_notes = []
    for page in pdf:
        text = page["text"].replace("\n", " ")
        pdf_notes.append(f"Page {page['page']:02d}: {text[:1200]}")
    (OUT / "pdf_page_notes.txt").write_text("\n".join(pdf_notes), encoding="utf-8")

    print(json.dumps({
        "slides": len(pptx),
        "pdf_pages": len(pdf),
        "latex_sections": len(latex),
        "html_pages": len(html_pages),
        "out": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
