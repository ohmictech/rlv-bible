#!/usr/bin/env python3
"""Build the RLV as a PDF.

The chapter files under NN-book/ are the only source of truth. This script reads
them and never writes to them.

Usage:
    python tools/build_pdf.py                    # one PDF of the whole Bible
    python tools/build_pdf.py --book genesis     # one book
    python tools/build_pdf.py --per-book         # also a PDF for each book
    python tools/build_pdf.py --layout inline    # verses run together per chapter
    python tools/build_pdf.py --no-contents      # skip the contents pages
    python tools/build_pdf.py --list

Output goes to build/, which git ignores, because a PDF is a build artifact and a
second copy of the text is a second thing to get out of sync.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR_RE = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
CHAPTER_RE = re.compile(r"^[a-z0-9-]+-ch-(\d{3})\.md$")

TITLE = "The Bible"
SUBTITLE = "Real Life Version"
COLOPHON = (
    "Rendered from the World English Bible, which is in the public domain. "
    "This edition is released under the Creative Commons Attribution-ShareAlike 4.0 "
    "International License. Copy it, print it, read it aloud, change it, sell it, as long "
    "as you credit the source and let your version carry the same freedoms."
)

SMALL_WORDS = {"of", "the", "and", "in", "to", "a", "an", "for", "on"}

SERIF = "Times-Roman"
SERIF_ITALIC = "Times-Italic"
SERIF_BOLD = "Times-Bold"

PAGE_WIDTH = 6 * inch
PAGE_HEIGHT = 9 * inch
MARGIN_SIDE = 0.75 * inch
MARGIN_TOP = 0.8 * inch
MARGIN_BOTTOM = 0.8 * inch

GREY = colors.HexColor("#808080")


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
        if path.is_dir():
            match = BOOK_DIR_RE.match(path.name)
            if match:
                books.append((int(match.group(1)), match.group(2), path))
    books.sort(key=lambda item: item[0])
    return books


def read_chapter(path: Path) -> list[str]:
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


# ---------------------------------------------------------------------- flowables


class BookMarker(Flowable):
    """Zero-height flowable that sets the running head and opens a bookmark."""

    def __init__(self, book_state: dict, title: str, key: str, level: int = 0):
        super().__init__()
        self.book_state = book_state
        self.title = title
        self.key = key
        self.level = level
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        self.book_state["current"] = self.title
        self.canv.bookmarkPage(self.key)
        self.canv.addOutlineEntry(self.title, self.key, level=self.level, closed=False)


class TocMarker(Flowable):
    """Zero-height flowable that registers a contents entry for the current page."""

    def __init__(self, document, level: int, text: str, key: str):
        super().__init__()
        self.document = document
        self.level = level
        self.text = text
        self.key = key
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        self.document.notify("TOCEntry", (self.level, self.text, self.document.page, self.key))


# -------------------------------------------------------------------- styles


def styles(justify: bool = False) -> dict[str, ParagraphStyle]:
    body = ParagraphStyle(
        "Body",
        fontName=SERIF,
        fontSize=10.5,
        leading=14.6,
        alignment=TA_JUSTIFY if justify else TA_LEFT,
        spaceAfter=3.4,
    )
    return {
        "body": body,
        "body_first": ParagraphStyle("BodyFirst", parent=body, spaceBefore=4),
        "chapter": ParagraphStyle(
            "Chapter",
            fontName=SERIF_ITALIC,
            fontSize=12,
            leading=15,
            spaceBefore=16,
            spaceAfter=6,
            alignment=TA_LEFT,
            keepWithNext=1,
        ),
        "book": ParagraphStyle(
            "Book",
            fontName=SERIF_BOLD,
            fontSize=26,
            leading=30,
            alignment=TA_CENTER,
            spaceBefore=0,
            spaceAfter=18,
            keepWithNext=1,
        ),
        "title": ParagraphStyle(
            "TitlePage",
            fontName=SERIF_BOLD,
            fontSize=34,
            leading=40,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "SubtitlePage",
            fontName=SERIF_ITALIC,
            fontSize=15,
            leading=20,
            alignment=TA_CENTER,
        ),
        "colophon": ParagraphStyle(
            "Colophon",
            fontName=SERIF,
            fontSize=8,
            leading=11,
            alignment=TA_CENTER,
            textColor=GREY,
        ),
        "contents_head": ParagraphStyle(
            "ContentsHead",
            fontName=SERIF_BOLD,
            fontSize=18,
            leading=22,
            spaceAfter=18,
            alignment=TA_LEFT,
        ),
        "toc1": ParagraphStyle(
            "TOC1",
            fontName=SERIF,
            fontSize=10.5,
            leading=15,
            leftIndent=0,
            firstLineIndent=0,
        ),
    }


# ------------------------------------------------------------------- templates


def draw_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont(SERIF, 8.5)
    canvas.setFillColor(GREY)
    canvas.drawCentredString(PAGE_WIDTH / 2, MARGIN_BOTTOM / 2, str(canvas.getPageNumber()))
    canvas.restoreState()


def draw_running_head(canvas, doc, book_state: dict) -> None:
    name = book_state.get("current")
    if not name:
        return
    canvas.saveState()
    canvas.setFont(SERIF_ITALIC, 8.5)
    canvas.setFillColor(GREY)
    canvas.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - MARGIN_TOP / 2 - 2, name)
    canvas.restoreState()


def make_documents(out_path: Path, book_state: dict, title: str):
    """Return a document with the front matter and body page templates registered."""

    doc = BaseDocTemplate(
        str(out_path),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=MARGIN_SIDE,
        rightMargin=MARGIN_SIDE,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title=title,
        author="RLV contributors",
        subject="The Bible: Real Life Version",
        creator="tools/build_pdf.py",
    )

    front_frame = Frame(
        MARGIN_SIDE,
        MARGIN_BOTTOM,
        PAGE_WIDTH - 2 * MARGIN_SIDE,
        PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM,
        id="front",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    body_frame = Frame(
        MARGIN_SIDE,
        MARGIN_BOTTOM,
        PAGE_WIDTH - 2 * MARGIN_SIDE,
        PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM,
        id="body",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    doc.addPageTemplates(
        [
            PageTemplate(id="front", frames=[front_frame], onPageEnd=draw_footer),
            PageTemplate(
                id="body",
                frames=[body_frame],
                onPageEnd=lambda canvas, doc: (draw_running_head(canvas, doc, book_state), draw_footer(canvas, doc)),
            ),
        ]
    )
    return doc


# ----------------------------------------------------------------------- story


def verse_markup(verses: list[str], layout: str) -> list[str]:
    """Return paragraph markup strings, one per verse or one per chapter."""

    def marker(number: int) -> str:
        return f'<super><font size="6.5" color="#7F7F7F">{number}</font></super>&nbsp;'

    if layout == "inline":
        pieces = [f"{marker(index)}{escape(verse, {'\"': '&quot;'})}" for index, verse in enumerate(verses, start=1)]
        return [" ".join(pieces)]

    return [f"{marker(index)}{escape(verse, {'\"': '&quot;'})}" for index, verse in enumerate(verses, start=1)]


def book_story(doc, book_state: dict, order: int, slug: str, book_dir: Path, layout: str, style: dict):
    story: list = [PageBreak()]
    title = book_title(slug)
    key = f"book-{order:02d}"
    story.append(BookMarker(book_state, title, key))
    story.append(TocMarker(doc, 0, title, key))
    story.append(Paragraph(escape(title), style["book"]))
    chapters = chapter_files(book_dir)
    for number, path in chapters:
        verses = read_chapter(path)
        if len(chapters) > 1:
            story.append(Paragraph(f"Chapter {number}", style["chapter"]))
        for index, chunk in enumerate(verse_markup(verses, layout)):
            paragraph_style = style["body_first"] if index == 0 else style["body"]
            story.append(Paragraph(chunk, paragraph_style))
    return story


def front_matter(doc, style: dict, include_contents: bool) -> list:
    story: list = [NextPageTemplate("front")]
    story.append(Spacer(1, 190))
    story.append(Paragraph(TITLE, style["title"]))
    story.append(Paragraph(SUBTITLE, style["subtitle"]))
    story.append(Spacer(1, 230))
    story.append(Paragraph(COLOPHON, style["colophon"]))

    if include_contents:
        story.append(PageBreak())
        story.append(Paragraph("Contents", style["contents_head"]))
        toc = TableOfContents()
        toc.levelStyles = [style["toc1"]]
        toc.dotsMinLevel = 0
        story.append(toc)

    story.append(NextPageTemplate("body"))
    return story


def build_pdf(out_path: Path, books, layout: str, include_contents: bool, label: str, justify: bool) -> tuple[int, int]:
    book_state: dict = {"current": None}
    doc = make_documents(out_path, book_state, label)
    style = styles(justify)

    story = front_matter(doc, style, include_contents)
    for index, (order, slug, book_dir) in enumerate(books):
        story.extend(book_story(doc, book_state, order, slug, book_dir, layout, style))

    story.append(PageBreak())
    story.append(Paragraph(COLOPHON, style["colophon"]))

    if include_contents:
        doc.multiBuild(story)
    else:
        doc.build(story)

    chapters = sum(len(chapter_files(book_dir)) for _, _, book_dir in books)
    return chapters, doc.page


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build PDF editions from the chapter files.")
    parser.add_argument("--book", action="append", default=None,
                        help="book slug, e.g. genesis or 1-corinthians. Repeatable.")
    parser.add_argument("--per-book", action="store_true", help="also write one PDF per book")
    parser.add_argument("--layout", choices=("verse", "inline"), default="verse",
                        help="verse = one paragraph per verse (default), inline = verses run together")
    parser.add_argument("--no-contents", action="store_true", help="skip the contents pages")
    parser.add_argument("--justify", action="store_true", help="justify the verse lines instead of ragged right")
    parser.add_argument("--out", default=str(ROOT / "build"), help="output directory")
    parser.add_argument("--list", action="store_true", help="list buildable books and exit")
    args = parser.parse_args(argv)

    books = find_books()
    if not books:
        print("no book folders found", file=sys.stderr)
        return 1

    if args.list:
        total = 0
        for order, slug, book_dir in books:
            count = len(chapter_files(book_dir))
            total += count
            print(f"{order:02d}  {slug:24s} {book_title(slug):24s} {count:3d} chapters")
        print(f"    {len(books)} books, {total} chapters")
        return 0

    if args.book:
        wanted = set(args.book)
        selected = [book for book in books if book[1] in wanted]
        missing = wanted - {book[1] for book in selected}
        if missing:
            print(f"unknown book(s): {', '.join(sorted(missing))}", file=sys.stderr)
            return 1
    else:
        selected = books

    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.book or args.per_book:
        for order, slug, book_dir in selected:
            out_path = out_dir / f"{order:02d}-{slug}.pdf"
            chapters, pages = build_pdf(out_path, [(order, slug, book_dir)], args.layout,
                                        not args.no_contents, book_title(slug), args.justify)
            print(f"{out_path.relative_to(ROOT)}  {chapters} chapters, {pages} pages", flush=True)

    if not args.book:
        out_path = out_dir / "the-bible-real-life-version.pdf"
        chapters, pages = build_pdf(out_path, selected, args.layout, not args.no_contents,
                                    f"{TITLE}: {SUBTITLE}", args.justify)
        print(f"{out_path.relative_to(ROOT)}  {chapters} chapters, {pages} pages", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
