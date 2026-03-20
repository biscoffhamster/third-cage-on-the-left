from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "Page 1 to 10 THIRD CAGE ON THE LEFT.pdf"
BOOK_DIR = ROOT / "book"

SOURCE_GROUPS = {
    "group1": {
        "title": "Preface and Life in the Zoo",
        "pages": (1, 12),
    },
    "group2": {
        "title": "The Duke of Bedford and George Cansdale",
        "pages": (13, 24),
    },
    "group3": {
        "title": "Pets at Home and Prep School High Days",
        "pages": (25, 36),
    },
    "group4": {
        "title": "Monkton Combe and the Big Freeze",
        "pages": (37, 43),
    },
}

CHAPTERS = [
    {
        "file": "01-preface.qmd",
        "title": "Preface",
        "source": "group1",
        "segments": [
            {"start": "## Preface", "end": "## Life in the Zoo", "start_after": True},
        ],
    },
    {
        "file": "02-life-in-the-zoo.qmd",
        "title": "Life in the Zoo",
        "source": "group1",
        "segments": [
            {
                "start": "## Life in the Zoo",
                "end": "My first two posts were my childhood memories until I was six",
                "start_after": True,
            },
        ],
    },
    {
        "file": "03-the-gold-coast-years.qmd",
        "title": "The Gold Coast Years",
        "source": "group1",
        "segments": [
            {
                "start": "My first two posts were my childhood memories until I was six",
                "end": "* * *",
                "start_after": False,
            },
            {
                "start": "George threw himself into his forestry work and soon learned the local language",
                "end": "Dear friends,",
                "start_after": False,
            },
        ],
    },
    {
        "file": "04-mr-ezra-and-mandarins.qmd",
        "title": "Mr. Ezra and Mandarins",
        "source": "group1",
        "segments": [
            {
                "start": "Mr. Ezra and Mandarins.",
                "end": "Dark times for many. Stay strong. Keep a diary and write up your story for your kids and friends.",
                "start_after": True,
            },
        ],
    },
    {
        "file": "05-the-duke-of-bedford-and-some-fishy-tales.qmd",
        "title": "The Duke of Bedford and Some Fishy Tales",
        "source": "group2",
        "segments": [
            {
                "start": "## The Duke of Bedford and Some Fishy Tales",
                "end": "This is George's obituary written by Biddy Baxter",
                "start_after": True,
            },
        ],
    },
    {
        "file": "06-george-cansdale.qmd",
        "title": "George Cansdale",
        "source": "group2",
        "segments": [
            {
                "start": "This is George's obituary written by Biddy Baxter",
                "end": "## Pets at Home",
                "start_after": False,
            },
        ],
    },
    {
        "file": "07-pets-at-home.qmd",
        "title": "Pets at Home",
        "source": "group2",
        "segments": [
            {"start": "## Pets at Home", "end": "* * *", "start_after": True},
            {
                "start": "I had been given my first Budgie by Mr. Palmer",
                "end": None,
                "start_after": False,
            },
        ],
    },
    {
        "file": "08-the-eagle-has-landed-and-family-fortunes.qmd",
        "title": "The Eagle Has Landed and Family Fortunes",
        "source": "group3",
        "segments": [
            {
                "start": "## The Eagle Has Landed and Family Fortunes",
                "end": "(Unedited first draft - but something to get on with.)",
                "start_after": True,
            },
        ],
    },
    {
        "file": "09-prep-school-high-days.qmd",
        "title": "Prep School High Days",
        "source": "group3",
        "segments": [
            {
                "start": "For the first two years after moving to Lyndale Avenue I remained at my Primary School",
                "end": "Good morning friends.",
                "start_after": False,
            },
            {
                "start": "Some people believe that I have a good memory for dates.",
                "end": "Monkton Combe School. 1960 - 1965",
                "start_after": False,
            },
        ],
    },
    {
        "file": "10-monkton-combe-school-1960-to-1961.qmd",
        "title": "Monkton Combe and the Big Freeze",
        "source": "group4",
        "segments": [
            {
                "start": "## Monkton Combe School, 1960 to 1961",
                "end": "* * *",
                "start_after": True,
            },
            {
                "start": "The winter of 1963 was cold.",
                "end": "## Gun Games with the CCF",
                "start_after": False,
            },
        ],
    },
    {
        "file": "11-gun-games-with-the-ccf.qmd",
        "title": "Gun Games with the CCF",
        "source": "group4",
        "segments": [
            {"start": "## Gun Games with the CCF", "end": None, "start_after": True},
        ],
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


def clean_chunk(text: str) -> list[str]:
    cleaned_lines: list[str] = []
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

    return cleaned_lines


def find_marker(lines: list[str], marker: str, start_index: int = 0) -> int:
    for index in range(start_index, len(lines)):
        if marker in lines[index]:
            return index
    raise ValueError(f"Could not find marker {marker!r}")


def trim_lines(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)

    while start < end and lines[start] == "":
        start += 1
    while end > start and lines[end - 1] == "":
        end -= 1

    return lines[start:end]


def extract_segment(
    lines: list[str],
    segment: dict[str, object],
    start_index: int,
) -> tuple[list[str], int]:
    start_marker = segment.get("start")
    end_marker = segment.get("end")
    start_after = bool(segment.get("start_after", True))

    if start_marker is None:
        segment_start = start_index
    else:
        marker_index = find_marker(lines, str(start_marker), start_index)
        segment_start = marker_index + (1 if start_after else 0)

    if end_marker is None:
        segment_end = len(lines)
    else:
        segment_end = find_marker(lines, str(end_marker), segment_start)

    return trim_lines(lines[segment_start:segment_end]), segment_end


def build_chapter(chapter: dict[str, object], sources: dict[str, list[str]]) -> str:
    lines = sources[str(chapter["source"])]
    body: list[str] = []
    search_from = 0

    for segment in chapter["segments"]:
        extracted, search_from = extract_segment(lines, segment, search_from)
        if body and extracted:
            body.append("")
        body.extend(extracted)

    trimmed_body = trim_lines(body)
    chapter_lines = [f"# {chapter['title']}", ""]
    chapter_lines.extend(trimmed_body)
    chapter_lines.append("")
    return "\n".join(chapter_lines)


def main() -> int:
    if not PDF_PATH.exists():
        print(f"Missing PDF: {PDF_PATH}", file=sys.stderr)
        return 1

    BOOK_DIR.mkdir(exist_ok=True)

    source_texts: dict[str, list[str]] = {}
    for key, source in SOURCE_GROUPS.items():
        first_page, last_page = source["pages"]
        raw_text = extract_page_range(first_page, last_page)
        source_texts[key] = clean_chunk(raw_text)

    expected_files = {chapter["file"] for chapter in CHAPTERS}
    for existing_file in BOOK_DIR.glob("*.qmd"):
        if existing_file.name not in expected_files:
            existing_file.unlink()

    for chapter in CHAPTERS:
        cleaned_text = build_chapter(chapter, source_texts)
        output_path = BOOK_DIR / chapter["file"]
        output_path.write_text(cleaned_text, encoding="utf-8")
        print(f"Wrote {output_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
