"""Convert the supplied Word eras to JSON and verify exact text preservation.

Only Python's standard library is used. Text runs are concatenated exactly;
paragraph boundaries and Heading 3 / Heading 4 order are represented in JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": WORD_NS}
W = f"{{{WORD_NS}}}"
EXPECTED_FILES = [
    "1859-1869.docx",
    "1870 - 1879.docx",
    "1880 - 1889.docx",
    "1890 - 1899.docx",
    "1900-1909.docx",
    "1910-1919.docx",
    "1920-1929.docx",
    "1930-1939.docx",
    "1940-1949.docx",
    "1950-1959.docx",
    "1960-1969.docx",
    "1970-1979.docx",
    "1980-1989.docx",
    "1990-1999.docx",
    "2000-2009.docx",
    "2010-2019.docx",
    "2020-2026.docx",
]


def paragraph_text(paragraph: ET.Element) -> str:
    """Return visible paragraph text without trimming or Unicode normalization."""
    pieces: list[str] = []

    def visit(node: ET.Element) -> None:
        for child in node:
            if child.tag == W + "t" or child.tag == W + "delText":
                pieces.append(child.text or "")
            elif child.tag == W + "tab":
                pieces.append("\t")
            elif child.tag in (W + "br", W + "cr"):
                pieces.append("\n")
            elif child.tag in (W + "drawing", W + "pict", W + "object"):
                # Images and embedded objects are not narrative text.
                continue
            else:
                visit(child)

    visit(paragraph)
    return "".join(pieces)


def extract_docx(path: Path) -> dict[str, Any]:
    """Extract one document into ordered title, introduction, and sections."""
    try:
        with ZipFile(path) as archive:
            document_xml = ET.fromstring(archive.read("word/document.xml"))
    except (BadZipFile, KeyError, ET.ParseError) as exc:
        raise ValueError(f"Cannot read Word document {path.name}: {exc}") from exc

    body = document_xml.find(".//w:body", NS)
    if body is None:
        raise ValueError(f"No Word document body found in {path.name}")

    content: list[tuple[str, str]] = []
    unsupported: list[tuple[str, str]] = []
    for element in body.iter(W + "p"):
        text = paragraph_text(element)
        if not text:
            continue
        style_node = element.find("./w:pPr/w:pStyle", NS)
        style = style_node.get(W + "val", "Normal") if style_node is not None else "Normal"
        content.append((style, text))
        if style.lower() not in {"heading3", "heading4", "normal"}:
            unsupported.append((style, text))

    if unsupported:
        raise ValueError(f"Unsupported paragraph style in {path.name}: {unsupported[0][0]}")
    if not content or content[0][0].lower() != "heading3":
        raise ValueError(f"Expected the first text paragraph to be Heading 3 in {path.name}")

    title = content[0][1]
    intro: list[str] = []
    sections: list[dict[str, Any]] = []
    active_section: dict[str, Any] | None = None

    for style, text in content[1:]:
        if style.lower() == "heading3":
            raise ValueError(f"Unexpected additional Heading 3 in {path.name}")
        if style.lower() == "heading4":
            active_section = {
                "order": len(sections) + 1,
                "heading": text,
                "paragraphs": [],
            }
            sections.append(active_section)
        elif active_section is None:
            intro.append(text)
        else:
            active_section["paragraphs"].append(text)

    year_range = re.search(r"(\d{4})\s*[-–]\s*(\d{4})", path.stem)
    if not year_range:
        raise ValueError(f"Cannot determine year range from filename {path.name}")

    return {
        "id": f"{year_range.group(1)}-{year_range.group(2)}",
        "title": title,
        "startYear": int(year_range.group(1)),
        "endYear": int(year_range.group(2)),
        "order": 0,  # Assigned across the complete collection below.
        "introParagraphs": intro,
        "sections": sections,
        "images": [],
        "sources": [],
    }


def load_source_collection(source_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    eras: list[dict[str, Any]] = []
    manifest: list[dict[str, str]] = []
    missing = [name for name in EXPECTED_FILES if not (source_dir / name).is_file()]
    if missing:
        raise ValueError("Missing source Word files: " + ", ".join(missing))

    for index, name in enumerate(EXPECTED_FILES, start=1):
        era = extract_docx(source_dir / name)
        era["order"] = index
        eras.append(era)
        manifest.append({"eraId": era["id"], "sourceFile": name})
    return eras, manifest


def compare(expected: Any, actual: Any, path: str = "$") -> list[str]:
    """Report exact structural or textual differences with a JSON-like path."""
    if type(expected) is not type(actual):
        return [f"{path}: expected {type(expected).__name__}, found {type(actual).__name__}"]
    if isinstance(expected, dict):
        problems: list[str] = []
        for key in expected.keys() | actual.keys():
            if key not in expected:
                problems.append(f"{path}.{key}: unexpected field")
            elif key not in actual:
                problems.append(f"{path}.{key}: missing field")
            else:
                problems.extend(compare(expected[key], actual[key], f"{path}.{key}"))
        return problems
    if isinstance(expected, list):
        if len(expected) != len(actual):
            return [f"{path}: expected {len(expected)} items, found {len(actual)}"]
        problems = []
        for index, (left, right) in enumerate(zip(expected, actual)):
            problems.extend(compare(left, right, f"{path}[{index}]"))
        return problems
    if expected != actual:
        return [f"{path}: text/value differs (expected {expected!r}, found {actual!r})"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True, help="Folder containing the 17 source DOCX files")
    parser.add_argument("--data", type=Path, default=Path("web/src/data/eras.json"), help="Era JSON path")
    parser.add_argument("--manifest", type=Path, default=Path("content/source-manifest.json"), help="Source manifest path")
    parser.add_argument("--write", action="store_true", help="Create JSON files; refuses to overwrite existing files")
    args = parser.parse_args()

    try:
        eras, manifest = load_source_collection(args.source_dir)
        if args.write:
            if args.data.exists() or args.manifest.exists():
                raise ValueError("Refusing to overwrite existing JSON output; move it aside explicitly first")
            args.data.parent.mkdir(parents=True, exist_ok=True)
            args.manifest.parent.mkdir(parents=True, exist_ok=True)
            args.data.write_text(json.dumps(eras, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Wrote {len(eras)} eras to {args.data}")
            print(f"Wrote source map to {args.manifest}")
            return 0

        stored_eras = json.loads(args.data.read_text(encoding="utf-8"))
        stored_manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        if len(stored_eras) != len(eras):
            raise ValueError(f"Expected {len(eras)} eras in {args.data}, found {len(stored_eras)}")
        errors: list[str] = []
        for index, (source_era, stored_era) in enumerate(zip(eras, stored_eras)):
            errors.extend(compare(source_era, stored_era, f"eras[{index}]"))
        errors.extend(compare(manifest, stored_manifest, "sourceManifest"))
        if errors:
            print("Content integrity check FAILED:", file=sys.stderr)
            for error in errors[:50]:
                print(f"- {error}", file=sys.stderr)
            if len(errors) > 50:
                print(f"... and {len(errors) - 50} more differences", file=sys.stderr)
            return 1
        print(f"Content integrity check passed: all {len(eras)} eras match the Word sources exactly.")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Content integrity check failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
