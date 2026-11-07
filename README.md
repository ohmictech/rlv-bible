# RLV Bible

**The Bible: Real Life Version**

The World English Bible re-rendered into plain modern English, so the words do the work instead of the associations.

## This is a community project, and it is never finished

The sweep runs a chapter at a time, and there are always chapters left. Fork it, argue a ruling, sweep one chapter, or just tell us a sentence reads badly. Disagreement is the main way this text improves: the way to change a word is to make the case from the text, and if the case is good, the ruling changes and the change is recorded with the reasoning. Nothing here is anyone's property, and no chapter is beyond a better sentence.

## What this is

Most English Bibles are not written in English. They are written in a dialect that only exists inside churches: it sounds like English, borrows English words, and means something different by them. You can read a chapter of it and come away thinking you have understood, when what you have done is recognize the shape of sentences you have heard before.

This version removes that. It is not a new translation out of Greek and Hebrew; the WEB already put the text in English carefully, and the work here is the layer above it, taking what is accurate and making it sayable.

## The conviction

The words should speak what they mean. Every rule below follows from that. If a word has to be explained after it is read, it has failed. If it arrives carrying a picture nobody in the room is seeing, it has failed. If the sentence has to be untangled before it can be understood, it has failed, however correct it is.

**Christianese has to go.** *Repentance* has worn into a church word, *justification* into a doctrine, *sin* into rule breaking. Where a word still has force for someone who has never been inside a church it stays: *Christ*, *Lord*, *the gathering*, *spokesman*. *Heresy* and *baptism* do not survive that test.

**The mental images have to go.** A version can be plain and still be full of pictures nobody meant to draw. *Soul* summons a detachable ghost. *Glory* summons light. *Hell* summons a place and a temperature, and is not in the text at all: the Greek has Hades and Gehenna, two words with two histories, kept apart here instead of melted together.

**Small words get read up, big ones read down.** Tradition flattens what God does and inflates the machinery around it. *Blessed* becomes a mood when the Greek says flourishing. *Saved* becomes a status when the Greek says healed and made whole. *Eternal* becomes a philosophical property when the Greek says of the era. Meanwhile *glory* becomes a shining substance when the Hebrew is talking about weight, and *the kingdom of God* becomes a place when the Greek is talking about a reign, something a king is actually doing.

## The stance

This is written from a biblical universalist position: the scriptures teach restorative justice and the rescue of all, each in his own order (1 Cor 15:23). That is not smuggled into the text. No verse gets stretched toward the conclusion and none gets softened away from it. Where the text says everyone, it says everyone (1 Tim 2:6, "who gave himself as a ransom for everyone"). Where it says aionios, it says of the era, because that is the word. Where it describes judgment, the judgment stays as severe as it is. The version refuses later doctrinal furniture in first-century sentences, refuses to mistranslate a hard passage to protect endless punishment, and refuses the opposite error of turning every warning into a mist.

## How the English reads

The test is a person of about twenty in 2026 with no church background. Not "would they understand it," which is a much lower bar. Would they say it. So the prose is spoken rather than composed: contractions, short sentences where the Greek is short, *will* instead of *shall*, semicolons broken into full stops, the two-beat pairings kept because Hebrew and Greek both like them and they still work.

And no dashes, ever. Each one is resolved by asking what it was doing: apposition becomes a comma, two clauses become a full stop, a list becomes a colon. A dash is a shortcut, and a shortcut usually marks a place where the writer has not decided what the relation is.

## What it looks like

| Reference | The usual English | Here |
|---|---|---|
| Rom 3:23 | all have sinned and fall short of the glory of God | all have drifted, and fall short of the weight of God |
| Matt 4:17 | Repent, for the kingdom of heaven is at hand | Have a change of heart, because the reign of the sky is at hand |
| John 3:16 | should not perish but have eternal life | shouldn't be lost, but have the real life of the era |
| 1 John 2:2 | he is the propitiation for our sins | He's the sacrifice that makes things right for our mistakes |
| Matt 5:3 | Blessed are the poor in spirit | Flourishing are the ones who know they have nothing to offer God |

Each of those is a ruling with a reason and a precedent behind it. None is a preference.

## How it is made

There is a constitution, and it is law: a routing table with one line per word in the original languages, the English it is rendered as, and one sentence on why. Nothing changes without a row, and nothing gets a row without an argument.

1. Read the chapter cold and note what is accurate versus what is unreadable. Two different problems.
2. Check every rendering against the routing table, lemma by lemma, against the Greek and Hebrew themselves rather than a list of English words to swap.
3. Rewrite for speech, keeping the repetitions that are doing work.
4. Sweep for the debris mechanical passes leave: doubled articles, orphaned commas, a formula a contraction broke.
5. Read it three more times, once out loud, then commit that chapter and only that chapter.

The hardest discipline is the one that sounds trivial: never assume a rule is applied because it is written down. A search is case-sensitive or it is not, a word boundary is there or it is not, and most of the real work of this project has gone into that gap.

## Format

One folder per book in canonical order, one file per chapter, verses only:

```
01-genesis/genesis-ch-001.md
...
66-revelation/revelation-ch-022.md
```

Verse *V* sits on line *V*, so the verse number is the line number. Files are UTF-8 with BOM, LF only, newline at the end, one trailing space per line, straight quotes only, no em or en dashes.

## Source, and license

Rendered from the **World English Bible**, public domain, itself a modern-English update of the American Standard Version. The result is released under **CC BY-SA 4.0**: copy it, print it, read it aloud, quote it, change it, sell what you make from it, as long as you credit the source and let your version carry the same freedoms. The WEB is public domain, so nothing forces that condition. It is chosen, because a version of the scriptures is exactly the thing that should not become somebody's property.

## Status

- New Testament: 27 books, 260 chapters, 7,953 verses, readability pass finished through the Gospels.
- Old Testament: 39 books, 929 chapters, 23,145 verses, readability pass in progress from Genesis forward.
- Total: 1,189 chapters, 31,098 verses.

## Why bother

Because the text is better than the way it is usually said, and a person who has never been inside a church should be able to open it and meet the thing itself. Because the habit of explaining a sentence to yourself while reading it is a habit that hides the sentence.

If the words speak what they mean, there is nothing left to translate.
