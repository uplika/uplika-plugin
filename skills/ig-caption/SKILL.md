---
name: ig-caption
description: Write and lint an Instagram caption (the line before the more cut, body, one ask, search terms, a few hashtags). Use for captions and hashtags.
---

Adapted from Jakeschincariol/instagram-agent-skill (MIT). Not affiliated with the original author.

# ig-caption

Use when the person says "write the caption", "caption this", "what do I put in the description", has a reel or a carousel ready and needs the text, or asks about hashtags.

One script lives in this skill's `scripts/` folder and it runs. From this skill's folder:

```bash
python3 scripts/caption.py caption.txt
python3 scripts/caption.py caption.txt --keywords "client proposals,agency pricing"
```

It prints the caption the way the feed prints it: the part shown before "... more" in a box, everything else behind the tap. That cut-off is an approximation that moves with the device and the font size, and `--truncate` tests a tighter one. Read that box before you read anything else you wrote. The script exits non-zero until the verdict is READY; that is its answer, not a crash.

On Korean captions the length, first-line and search-term checks still work. The hashtag counter only sees tags written in Latin letters, and the ask and concreteness checks look for English patterns (a number written together with a Korean unit is not counted), so check those by reading. Without a terminal the script cannot run: apply the checks by reading and say the lint was not run.

Read the voice file `~/.uplika/<workspace-slug>/voice.md` first if it exists. If it does not, ask three questions (tone, how they end a line, words they avoid) and offer to save the answers with the `voice-profile` skill.

## First, decide which job this caption has

This is the decision that ruins captions when it is skipped.

**Job A: the video already hooked them.** A Reel carries its own hook in the first two seconds, spoken and on screen. The caption is not a second hook and competing with the video is how you lose both. Its job is the ask, the context that makes the ask make sense, and the words people search.

**Job B: the caption is the content.** A photo, a single image, a carousel cover that opens a loop. Here line one is the hook and it works exactly like a Reel hook: concrete, short, and cut off at a cliff rather than mid-clause.

Ask which one you are writing. If the person has a Reel with a strong hook, write A and say why.

## The shape

```
Line 1      the space the feed shows before "... more". Job A: the ask,
            plainly. Job B: the hook.
            Never a greeting, never a hashtag, never an emoji as the first
            character.
Body        short paragraphs, one line of white space between each. Two to six
            of them. This is where the search terms live.
The ask     one. Comment a keyword, save it, or DM. One.
Hashtags    a few, on their own line at the bottom, or none.
```

How long a caption may be, and how Instagram counts its characters, comes from `list_platforms`. Almost nothing needs the whole limit. A caption that earns the tap and then delivers a few tight paragraphs beats one that fills the box.

## Hashtags, honestly

Hashtags are not a reach lever any more, and the platform has now said so with a product change. In December 2025 Instagram cut how many hashtags a post can carry, telling creators that fewer, more targeted hashtags perform better than many generic ones. Adam Mosseri had already said in February 2025 that hashtags do not work to increase reach and are a label, not a distribution lever.

So: a few, specific, as topic labels. If the person has a long block saved in their notes app, that block is now dead weight and the linter will fail it. `scripts/caption.py` carries the cap the original author checked when writing it. Uplika's `list_platforms` does not carry a hashtag cap, so if Instagram's own guidance has moved since, Instagram is right.

`#viral`, `#fyp`, `#explorepage`, `#foryou` describe nothing. Cut them.

## Search terms matter more than hashtags now

Instagram search reads the caption text. So the phrase the person wants to be found for goes in the caption as a phrase a human would type, in a sentence that reads normally. "Client proposals" as words in line three, not "#clientproposals" in a block at the bottom.

Ask for two or three of those terms, then pass them to the linter:

```bash
python3 scripts/caption.py draft.txt --keywords "client proposals,agency pricing"
```

## Rules

- **No link in the caption.** Captions are not clickable. A URL in the body is dead text that says "I do not use this platform". Bio or DM.
- **One ask.** Two asks is the same as none. `scripts/caption.py` counts them.
- **The keyword ask needs a keyword people can type.** One word, no spaces, no emoji, and say it out loud in the video too. `Comment CONTRACT` works. `Comment "the contract guide"` does not.
- **Write the first comment separately** if there is a link. Say so in the receipt.
- **Emoji as punctuation, not decoration.** The linter flags heavy emoji use.
- **Alt text is worth 20 seconds.** For carousels and photos, write it. It is read by screen readers and by Instagram.

## The loop

1. Decide Job A or Job B and say which.
2. Draft it.
3. Run `ig-human` on it. Captions are short, so slop is louder here than anywhere else.
4. Run `scripts/caption.py` with the person's search terms. Fix every FAIL. Decide on every WARN out loud rather than silently.
5. Print the copy-ready block, then the receipt:

```
CAPTION READY
job:        A - the reel carries the hook
visible:    118 characters used before the cut
ask:        one, comment CONTRACT
hashtags:   3
search:     "client proposals" in line 3, "agency pricing" in line 5
linter:     READY
```

## With Uplika connected

This skill writes the caption and does not publish. The caption becomes the `content` of the post that `ig-reel`, `ig-carousel` or the publish skill sends, after the person approves it there.

- Check the length against Instagram in `list_platforms` (its character limit and `charCount` rule). Emoji can count differently there than in `scripts/caption.py`; when the two disagree, `list_platforms` wins.
- Instagram captions cannot be edited after the post goes out (the features table in `list_platforms` says so). The linted, approved text is the final text.
- The separate first comment goes in `options.instagram.firstComment`. Uplika posts it right after the post (not on stories), and if it fails the post still goes up with a warning.
- Stories show no caption; their words go on the frames (`ig-story`).
- A keyword ask ("Comment CONTRACT") needs the automation that sends the thing: the `automations` skill sets up `template:comment_to_dm`. Use the exact same keyword in both places.
- Alt text travels with each image when it is uploaded (`altText`), not in the caption.

## Without Uplika

Print the block and the receipt. The person pastes the caption into Instagram.

## Tools

- `list_platforms`: Instagram's caption limit and counting rule, the option schema, and the features table (no edits after publishing)
