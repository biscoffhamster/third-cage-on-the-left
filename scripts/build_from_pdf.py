from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "Page 1 to 10 THIRD CAGE ON THE LEFT.pdf"
BOOK_DIR = ROOT / "book"

CHAPTERS = [
    {
        "file": "01-preface-and-life-in-the-zoo.qmd",
        "title": "Preface and Life in the Zoo",
        "pages": (1, 12),
    },
    {
        "file": "02-fishy-tales-and-george-cansdale.qmd",
        "title": "The Duke of Bedford and George Cansdale",
        "pages": (13, 24),
    },
    {
        "file": "03-pets-and-prep-school.qmd",
        "title": "Pets at Home and Prep School High Days",
        "pages": (25, 36),
    },
    {
        "file": "04-monkton-years.qmd",
        "title": "Monkton Combe and the Big Freeze",
        "pages": (37, 43),
    },
]

HEADER_PATTERNS = [
    re.compile(r"^THIRD CAGE ON THE LEFT(?:\.| .*|)$", re.IGNORECASE),
    re.compile(r"^THIRD CAGE ON THE LEFT\.? page \d+(?: part \d+)?\.?$", re.IGNORECASE),
    re.compile(r"^Page \d+\.?$", re.IGNORECASE),
    re.compile(r"^Preface to THIRD CAGE ON THE LEFT\.? page \d+(?: part \d+)?\.?$", re.IGNORECASE),
    re.compile(r"^INSTEAD OF .*THIRD CAGE ON THE LEFT.*$", re.IGNORECASE),
    re.compile(r"^%$"),
]

HEADING_REWRITES = {
    "PREFACE to Richard Cansdale's story with the working title of": "## Preface",
    "Life in the Zoo.": "## Life in the Zoo",
    "THE DUKE OF BEDFORD AND SOME FISHY TALES.": "## The Duke of Bedford and Some Fishy Tales",
    "PETS AT HOME": "## Pets at Home",
    "PREP SCHOOL HIGH DAYS": "## Prep School High Days",
    "The Eagle Has Landed; and family Fortunes": "## The Eagle Has Landed and Family Fortunes",
    "Monkton Combe School. The first 4 terms 1960/61": "## Monkton Combe School, 1960 to 1961",
    "Gun Games with the CCF.": "## Gun Games with the CCF",
}

DROP_LINES = {
    "THIRD CAGE ON THE LEFT.",
    "THIRD CAGE ON THE LEFT.",
    "To be continued......",
    "Copy and share.",
    "HAPPY EASTER EVERYONE !",
    "😉",
}


def extract_page_range(first_page: int, last_page: int) -> str:
    result = subprocess.run(
        [
            "pdftotext",
            "-f",
            str(first_page),
            "-l",
            str(last_page),
            "-layout",
            str(PDF_PATH),
            "-",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.replace("\f", "\n")


def should_drop(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped in DROP_LINES:
        return True
    return any(pattern.match(stripped) for pattern in HEADER_PATTERNS)


def clean_chunk(text: str, chapter_title: str) -> str:
    cleaned_lines: list[str] = [f"# {chapter_title}", ""]
    blank_pending = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if should_drop(line):
            continue

        if not stripped:
            if cleaned_lines and cleaned_lines[-1] != "":
                blank_pending = True
            continue

        replacement = HEADING_REWRITES.get(stripped)
        if replacement:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            cleaned_lines.append(replacement)
            cleaned_lines.append("")
            blank_pending = False
            continue

        if stripped and stripped[0].isdigit() and "/" in stripped and len(stripped) < 20:
            continue

        if set(stripped) == {"*"}:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            cleaned_lines.append("* * *")
            cleaned_lines.append("")
            blank_pending = False
            continue

        if blank_pending and cleaned_lines and cleaned_lines[-1] != "":
            cleaned_lines.append("")
        cleaned_lines.append(stripped)
        blank_pending = False

    while cleaned_lines and cleaned_lines[-1] == "":
        cleaned_lines.pop()

    return "\n".join(cleaned_lines) + "\n"


def main() -> int:
    if not PDF_PATH.exists():
        print(f"Missing PDF: {PDF_PATH}", file=sys.stderr)
        return 1

    BOOK_DIR.mkdir(exist_ok=True)

    for chapter in CHAPTERS:
        first_page, last_page = chapter["pages"]
        raw_text = extract_page_range(first_page, last_page)
        cleaned_text = clean_chunk(raw_text, chapter["title"])
        output_path = BOOK_DIR / chapter["file"]
        output_path.write_text(cleaned_text, encoding="utf-8")
        print(f"Wrote {output_path.relative_to(ROOT)} from pages {first_page}-{last_page}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
