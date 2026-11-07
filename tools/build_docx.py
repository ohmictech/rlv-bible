#!/usr/bin/env python3
"""Build reading editions of the RLV as .docx.

The chapter files under NN-book/ are the only source of truth. This script never
writes to them and nothing it produces should ever be edited by hand: fix the
chapter file, rebuild, and the edition follows.

Usage:
    python tools/build_docx.py                 # every book plus one combined file
    python tools/build_docx.py --book genesis  # one book
    python tools/build_docx.py --single        # combined only
    python tools/build_docx.py --layout inline # verses run together in a chapter
    python tools/build_docx.py --list          # show the books it can build

Output goes to build/ and is ignored by git, because a .docx is a build artifact
and a second copy of the text is a second thing to get out of sync.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR_RE = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
CHAPTER_RE = re.compile(r"^[a-z0-9-]+-ch-(\d{3})\.md$")

TITLE = "The Bible"
SUBTITLE = "Real Life Version"
COLOPHON = (
    "Rendered from the World English Bible, which is in the public domain. "
    "This edition is released under the Creative Commons Attribution-ShareAlike 4.0 "
    "International License. Copy it, print it, read it aloud, change it, sell it, "
    "as long as you credit the source and let your version carry the same freedoms."
)

SMALL_WORDS = {"of", "the", "and", "in", "to", "a", "an", "for", "on"}

BODY_FONT = "Georgia"
GREY = RGBColor(0x80, 0x80, 0x80)


# --------------------------------------------------------------------------- io


def book_title(slug: str) -> str:
    """'1-corinthians' -> '1 Corinthians', 'song-of-solomon' -> 'Song of Solomon'."""
    words = []
    for index, word in enumerate(slug.split("-")):
        if word.isdigit() or (word in SMALL_WORDS and index):
            words.append(word)
        else:
            words.append(word.capitalize())
    return " ".join(words)


def find_books() -> list[tuple[int, str, Path]]:
    books = []
    for path in ROOT.iterdir():
        if not path.is_dir():
            continue
        match = BOOK_DIR_RE.match(path.name)
        if match:
            books.append((int(match.group(1)), match.group(2), path))
    books.sort(key=lambda item: item[0])
    return books


def read_chapter(path: Path) -> list[str]:
    """One verse per line, trailing space stripped, blank lines dropped."""
    text = path.read_text(encoding="utf-8-sig")
    return [line.strip() for line in text.split("\n") if line.strip()]


def chapter_files(book_dir: Path) -> list[tuple[int, Path]]:
    chapters = []
    for path in book_dir.glob("*-ch-*.md"):
        match = CHAPTER_RE.match(path.name)
        if match:
            chapters.append((int(match.group(1)), path))
    chapters.sort()
    return chapters


# ---------------------------------------------------------------------- docx bits


def shade(paragraph, hex_fill: str) -> None:
    element = OxmlElement("w:shd")
    element.set(qn("w:val"), "clear")
    element.set(qn("w:color"), "auto")
    element.set(qn("w:fill"), hex_fill)
    paragraph._p.get_or_add_pPr().append(element)


def field(paragraph, instruction: str, placeholder: str = "") -> None:
    """Insert a Word field (TOC, PAGE, ...) that Word resolves when it updates."""
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for piece in (begin, instr, separate, text, end):
        run._r.append(piece)


def update_fields_on_open(doc: Document) -> None:
    settings = doc.settings.element
    element = OxmlElement("w:updateFields")
    element.set(qn("w:val"), "true")
    settings.append(element)


def build_styles(doc: Document) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.15

    for name in ("Title", "Subtitle"):
        style = doc.styles[name]
        style.font.name = BODY_FONT

    doc.styles["Title"].font.size = Pt(30)
    doc.styles["Title"].paragraph_format.space_before = Pt(200)
    doc.styles["Title"].paragraph_format.space_after = Pt(6)
    doc.styles["Subtitle"].font.size = Pt(14)
    doc.styles["Subtitle"].font.italic = True
    doc.styles["Subtitle"].paragraph_format.space_after = Pt(0)

    heading1 = doc.styles["Heading 1"]
    heading1.font.name = BODY_FONT
    heading1.font.size = Pt(26)
    heading1.font.bold = True
    heading1.font.color.rgb = RGBColor(0, 0, 0)
    heading1.paragraph_format.space_before = Pt(0)
    heading1.paragraph_format.space_after = Pt(24)
    heading1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    heading1.paragraph_format.page_break_before = True
    heading1.paragraph_format.keep_with_next = True

    heading2 = doc.styles["Heading 2"]
    heading2.font.name = BODY_FONT
    heading2.font.size = Pt(12)
    heading2.font.bold = False
    heading2.font.italic = True
    heading2.font.color.rgb = RGBColor(0, 0, 0)
    heading2.paragraph_format.space_before = Pt(16)
    heading2.paragraph_format.space_after = Pt(6)
    heading2.paragraph_format.keep_with_next = True

    verse = doc.styles.add_style("Verse", WD_STYLE_TYPE.PARAGRAPH)
    verse.base_style = doc.styles["Normal"]
    verse.font.name = BODY_FONT
    verse.font.size = Pt(11)
    verse.paragraph_format.space_after = Pt(4)
    verse.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    verse_first = doc.styles.add_style("Verse First", WD_STYLE_TYPE.PARAGRAPH)
    verse_first.base_style = verse
    verse_first.paragraph_format.space_before = Pt(6)


def page_setup(doc: Document) -> None:
    for section in doc.sections:
        section.page_width = Inches(6)
        section.page_height = Inches(9)
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

        footer = section.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        field(footer, "PAGE", "")


def title_page(doc: Document) -> None:
    doc.add_paragraph(TITLE, style="Title")
    doc.add_paragraph(SUBTITLE, style="Subtitle")
    note = doc.add_paragraph()
    note.paragraph_format.space_before = Pt(300)
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = note.add_run(COLOPHON)
    run.font.size = Pt(8)
    run.font.color.rgb = GREY


def contents_page(doc: Document) -> None:
    heading = doc.add_paragraph(style="Title")
    heading.paragraph_format.space_before = Pt(0)
    heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
    heading.paragraph_format.page_break_before = True
    run = heading.add_run("Contents")
    run.font.size = Pt(18)

    body = doc.add_paragraph()
    field(body, r'TOC \o "1-1" \h \z \u', "Update this field to build the contents.")


def verse_number(paragraph, number: int) -> None:
    run = paragraph.add_run(str(number))
    run.font.superscript = True
    run.font.size = Pt(8)
    run.font.color.rgb = GREY


def add_chapter_verses(doc: Document, verses: list[str], layout: str) -> None:
    if layout == "inline":
        paragraph = doc.add_paragraph(style="Verse First")
        for index, verse in enumerate(verses, start=1):
            if index > 1:
                paragraph.add_run(" ")
            verse_number(paragraph, index)
            paragraph.add_run(" " + verse)
        return

    for index, verse in enumerate(verses, start=1):
        style = "Verse First" if index == 1 else "Verse"
        paragraph = doc.add_paragraph(style=style)
        verse_number(paragraph, index)
        paragraph.add_run(" " + verse)


def add_book(doc: Document, order: int, slug: str, book_dir: Path, layout: str) -> int:
    chapters = chapter_files(book_dir)
    doc.add_heading(book_title(slug), level=1)
    total = 0
    for number, path in chapters:
        verses = read_chapter(path)
        total += len(verses)
        if len(chapters) > 1:
            doc.add_heading(f"Chapter {number}", level=2)
        add_chapter_verses(doc, verses, layout)
    return total


def new_document() -> Document:
    doc = Document()
    build_styles(doc)
    page_setup(doc)
    return doc


# ------------------------------------------------------------------------- build


def build_combined(books, out_dir: Path, layout: str) -> tuple[Path, int, int]:
    doc = new_document()
    title_page(doc)
    contents_page(doc)
    verses_total = 0
    chapters_total = 0
    for order, slug, book_dir in books:
        verses_total += add_book(doc, order, slug, book_dir, layout)
        chapters_total += len(chapter_files(book_dir))
    end = doc.add_paragraph()
    end.paragraph_format.page_break_before = True
    end.paragraph_format.space_before = Pt(0)
    run = end.add_run(COLOPHON)
    run.font.size = Pt(9)
    run.font.color.rgb = GREY

    update_fields_on_open(doc)
    path = out_dir / "the-bible-real-life-version.docx"
    doc.save(path)
    return path, chapters_total, verses_total


def build_book(order: int, slug: str, book_dir: Path, out_dir: Path, layout: str) -> tuple[Path, int, int]:
    doc = new_document()
    verses = add_book(doc, order, slug, book_dir, layout)
    update_fields_on_open(doc)
    path = out_dir / f"{order:02d}-{slug}.docx"
    doc.save(path)
    return path, len(chapter_files(book_dir)), verses


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build .docx editions from the chapter files.")
    parser.add_argument("--book", action="append", default=None,
                        help="book slug, e.g. genesis or 1-corinthians. Repeatable.")
    parser.add_argument("--single", action="store_true", help="build only the combined edition")
    parser.add_argument("--layout", choices=("verse", "inline"), default="verse",
                        help="verse = one paragraph per verse (default), inline = verses run together")
    parser.add_argument("--out", default=str(ROOT / "build"), help="output directory")
    parser.add_argument("--list", action="store_true", help="list buildable books and exit")
    args = parser.parse_args(argv)

    books = find_books()
    if not books:
        print("no book folders found", file=sys.stderr)
        return 1

    if args.list:
        for order, slug, book_dir in books:
            print(f"{order:02d}  {slug:24s} {book_title(slug):24s} {len(chapter_files(book_dir)):3d} chapters")
        return 0

    if args.book:
        wanted = set(args.book)
        books = [book for book in books if book[1] in wanted]
        missing = wanted - {book[1] for book in books}
        if missing:
            print(f"unknown book(s): {', '.join(sorted(missing))}", file=sys.stderr)
            return 1

    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not args.single:
        for order, slug, book_dir in books:
            path, chapters, verses = build_book(order, slug, book_dir, out_dir, args.layout)
            print(f"{path.relative_to(ROOT)}  {chapters} chapters, {verses} verses")

    if args.single or not args.book:
        path, chapters, verses = build_combined(books, out_dir, args.layout)
        print(f"{path.relative_to(ROOT)}  {chapters} chapters, {verses} verses")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
