# RLV Bible

**The Bible: Real Life Version**

The World English Bible re-rendered into plain modern English.

## A community project, and an unfinished one

The readability work runs a chapter at a time and there are a great many chapters still to go. Anyone who wants to help can fork the repository and take a chapter, argue against a ruling that seems wrong, or simply report a sentence that reads badly. The rulings are open to argument. The way to change one is to make the case from the text, and if the case holds up the ruling changes and the reasoning joins everything else in the constitution. No chapter is treated as settled beyond improvement.

## What this is

A good deal of English Bible text does not read like English. It is written in a dialect that exists mainly inside churches, one that borrows ordinary words and means something else by them, so that it is possible to read a chapter and come away believing you have understood it when what you have really done is recognize the shape of sentences you have heard before.

This version starts from the World English Bible, which already did the careful work of translating from the Greek and Hebrew. What happens here is the layer above that, where accurate English is rewritten so that it can be read aloud without the reader having to translate it again in their head.

## What it is trying to do

The aim is easy enough to state. The words should mean what they say to a reader who has no church vocabulary, and no inherited picture should be doing work that the text itself does not do.

The first half of that concerns worn vocabulary. Where a word has collapsed into a religious label, the version looks for the everyday word that still carries the sense. Repentance now signals a church word more than a change of direction, so the text reads have a change of heart. Justification has become the name of a doctrine rather than the state of being put right. Some words have held up better than others, and where an old word still means something to someone outside the church it stays: Christ, Lord, the gathering, spokesman.

The second half concerns images. A version can use plain vocabulary and still leave the reader holding pictures the original never supplied. The English soul brings a detachable ghost along with it, glory brings light, and hell brings a place with a temperature. Hell in particular is not in the text at all; the Greek has two words behind it, Hades and Gehenna, with two different histories, and this version keeps them apart instead of merging them.

Running through both is a question of direction. Words that tradition tends to flatten, mostly the ones describing what God does, usually need to be read upward: blessed is closer to flourishing, saved is closer to healed and made whole, and eternal in the New Testament is usually closer to of the era. Words that tradition inflates, mostly the ones describing the structure around God, usually need to be read down, since the Hebrew behind glory is often closer to weight, and the kingdom of God is a reign, something a king is doing, rather than a place.

## The stance

The version is written from a biblical universalist position, holding that the scriptures teach restorative justice and the eventual rescue of all, each in his own order (1 Cor 15:23). The stance affects the translation mostly by ruling things out. It rules out reading a hard passage through the prior assumption of endless punishment and then adjusting the words to suit, and it equally rules out softening a warning until it has stopped saying anything. Where the text says everyone, as at 1 Tim 2:6, the version says everyone. Where it says aionios, it says of the era, because that is what the word means. Where it describes judgment, the judgment is left as severe as the text makes it.

## How the English reads

Every sentence is tested against a reader of about twenty in 2026 who has no church background. The question is whether they would say it themselves, which is a good deal stricter than whether they could work out what it meant. In practice that produces a spoken register: contractions, short sentences where the Greek is short, will in place of shall except inside a quotation of the law, and semicolons broken into full stops where they were only holding two clauses together. Hebrew and Greek both like pairings of two short phrases, and those are kept wherever they still work in English.

Dashes are removed entirely. Each one is dealt with by asking what it had been doing. Where it stood in place of an apposition it becomes a comma, where it joined two clauses it becomes a full stop, and where it introduced a list or a definition it becomes a colon.

## What it looks like

| Reference | The usual English | Here |
|---|---|---|
| Rom 3:23 | all have sinned and fall short of the glory of God | all have drifted, and fall short of the weight of God |
| Matt 4:17 | Repent, for the kingdom of heaven is at hand | Have a change of heart, because the reign of the sky is at hand |
| John 3:16 | should not perish but have eternal life | shouldn't be lost, but have the real life of the era |
| 1 John 2:2 | he is the propitiation for our sins | He's the sacrifice that makes things right for our mistakes |
| Matt 5:3 | Blessed are the poor in spirit | Flourishing are the ones who know they have nothing to offer God |

Each of these is a recorded ruling with a reason and a precedent behind it, arrived at the same way as every other one.

## How it is made

The whole thing is governed by a constitution, which is a routing table with one line per word in the original languages, the English it is rendered as, and a sentence explaining why. A word cannot be changed without a row, and a row cannot be added without an argument.

The pattern for a chapter is roughly this:

1. Read it cold in its present state, separating what is inaccurate from what is merely hard to read, since those are different problems with different fixes.
2. Check each rendering against the routing table, working from the Greek and Hebrew words themselves rather than from a list of English words to swap, which is one of the ways a version drifts over time.
3. Rewrite for speech, keeping the repetitions that are carrying weight and dropping the ones that are not.
4. Sweep for the damage a mechanical pass tends to leave: doubled articles, commas left orphaned after a deletion, a fixed formula broken by a contraction.
5. Read it through several more times, once aloud, then commit that chapter on its own.

Much of the difficulty turns out to be mundane. A rule can be entirely correct and still not be applied, because a search was case-sensitive when it needed not to be, or a word boundary was missing, and a fair amount of the work has gone into finding that sort of gap.

## Format

One folder per book in canonical order, one file per chapter, verses only:

```
01-genesis/genesis-ch-001.md
...
66-revelation/revelation-ch-022.md
```

Verse *V* sits on line *V*, so the verse number is the line number. Files are UTF-8 with BOM, LF line endings only, a newline at the end of the file, one trailing space on each line, straight quotes only, and no em or en dashes.

## Building a reading edition

`tools/build_pdf.py` turns the chapter files into a PDF. By default it makes one volume for the whole Bible at 6 by 9 inches, set in two columns at 8.5 point with the verses of a chapter running together, which comes to about 1,200 pages. It carries a title page, contents, running heads, page numbers, book and chapter headings, and the verse number set small at the start of each verse. `--columns 1` gives a single wider column, `--font-size 10` sets the type, `--layout verse` gives every verse a line of its own, `--justify` sets the lines to full measure instead of ragged right, `--book genesis` builds a single book, and `--per-book` writes a separate file for each book. Everything it writes goes to `build/`, which git ignores, so the text never has a second copy to fall out of step. It needs the packages in `tools/requirements.txt`.

## Source and license

The text is rendered from the World English Bible, which is in the public domain and is itself a modern English update of the American Standard Version. The result is released under CC BY-SA 4.0, which permits copying, printing, public reading, quotation, modification and commercial use, provided the source is credited and any derivative is released under the same terms. Public domain status does not oblige anyone to that condition; it is adopted here so that the text, and anything made from it, stays available.

## Status

- New Testament: 27 books, 260 chapters, 7,953 verses, readability pass finished through the Gospels.
- Old Testament: 39 books, 929 chapters, 23,145 verses, readability pass in progress from Genesis forward.
- Total: 1,189 chapters, 31,098 verses.

## Why the project exists

The reason is fairly ordinary. The text is better than the way it is usually presented, and someone with no church background ought to be able to open it and meet it directly. There is a smaller reason alongside that one, which is that reading a sentence while quietly explaining it to yourself is a habit that makes the sentence hard to hear.
