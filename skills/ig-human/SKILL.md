---
name: ig-human
description: Humanize a draft. Strip em dashes, stock AI phrases and invisible characters, then score it on five checks before it is shown or posted.
---

Adapted from Jakeschincariol/instagram-agent-skill (MIT). Not affiliated with the original author.

# ig-human

Use whenever text needs to sound human: when the person says humanize, "does this sound like AI", "remove the em dashes", "de-slop this", "this sounds like ChatGPT", and before any caption, script, comment reply or DM is shown to the person.

Two scripts live in this skill's `scripts/` folder and they both actually run. Use them. Do not eyeball this. From this skill's folder:

```bash
python3 scripts/humanize.py draft.txt --report        # clean it, show what changed
python3 scripts/detect.py draft.txt                    # score it, five checks
python3 scripts/detect.py before.txt after.txt         # prove the delta
```

Both read `scripts/slop.json`: stock words and phrases with plain-English replacements, invisible character classes, typographic substitutions and structural tells. The last block of each list is Instagram-specific, the vocabulary that only shows up in captions and voiceovers. It is meant to be edited. If the person has a word they always use that the lexicon strips, take it out of the file.

The lexicon, the structural flags and the five scores are English. On Korean or other non-English text only the invisible-character and typography passes mean anything: run `scripts/humanize.py` for those, then read the draft yourself for stock phrasing, and do not report the human score as a verdict. Without a terminal the scripts cannot run: apply the same passes by reading and say that no score was computed.

## Why this matters more on Instagram than it looks

Captions are short and scripts get said out loud. A written-sounding line in a short caption is a larger share of the text than the same line in an essay, and a voiceover that nobody could say naturally is obvious in the first take. The tell here is not a detector flagging the post. The tell is a person scrolling past something that reads like a brand, or a creator stumbling over their own script.

## What gets fixed automatically

**1. Invisible characters.** Zero-width spaces and joiners, word joiners, soft hyphens, byte-order marks, Unicode tag characters, invisible separators, non-breaking and narrow spaces. A keyboard does not produce these. They survive copy-paste, they are invisible in every editor, and they are the most mechanical thing in generated text. `scripts/humanize.py` deletes every one, including any remaining Unicode format character it does not have a name for.

**2. Typography.** Em dash to comma, en dash to hyphen, curly quotes to straight, ellipsis to three dots, bullet character to hyphen. The em dash pass is the one that matters: it collapses the dash to a comma and then cleans up the double punctuation and orphaned periods that leaves behind.

**3. The slop lexicon.** delve, leverage, robust, seamless, crucial, testament to, "in today's fast-paced world", plus the Instagram block: "stop scrolling", "in today's video", "follow for more", "tag someone who needs this", "the algorithm loves", "run don't walk". Each swapped for a plain word or deleted, with capitalisation preserved and URLs left untouched.

## What does NOT get fixed automatically

Structural tells get **flagged, not rewritten**, because changing the shape of a sentence needs judgement:

- "It's not just X, it's Y" and "not only X but also Y"
- Rule-of-three triads
- Rhetorical one-word question lines: "The result?"
- The video preamble: "in this video I'm going to show you"
- Emoji bullet lists
- Three or more shouted words in a row
- Hashtag walls
- Reflex bait: "follow for more", "tag someone who", "double tap if"

That list is your job. Rewrite each flagged line by hand, keeping the meaning, then re-run `scripts/detect.py`. This is the part that moves the score from REVIEW to PASS, and it is the part a script cannot do.

## The five checks

`scripts/detect.py` scores five signals 0-100, higher is more human:

| check | what it measures | machine looks like |
| --- | --- | --- |
| BURSTINESS | sentence-length variation | every sentence the same length |
| SPECIFICITY | numbers, names, concrete markers per 100 words | abstract nouns, no figures |
| SLOP DENSITY | lexicon hits per 100 words | stock vocabulary |
| FINGERPRINT | invisible chars, em dashes, curly quotes per 1k chars | typographically perfect |
| VOICE | contractions, person, structural tells | no contractions, staged reveals |

The verdict weights the mean at 60% and the **weakest single check** at 40%, because one signal is enough. PASS needs an overall of 70+ with no check below 55. The script exits non-zero until the verdict is PASS; that is its answer, not a crash.

## Say this honestly

These are five local heuristics modelled on the signals public detectors key on. They run entirely on the person's machine and nothing is uploaded. They are **not** GPTZero, Originality, Copyleaks, Winston or Turnitin, they do not call those APIs, and they cannot promise those verdicts. Fixing what they measure does tend to move those numbers, because they are measuring the same underlying things. That is the claim. Do not make a bigger one on the person's behalf, and do not tell anyone their text is undetectable.

## Order of operations

1. `python3 scripts/humanize.py draft.txt -o clean.txt --report`
2. Read the structural flags. Rewrite those lines yourself.
3. `python3 scripts/detect.py draft.txt clean.txt` to show the before and after.
4. If the verdict is not PASS, fix the weakest check named in the output and go again. Two rounds is normal. Five means the draft was written by formula, and the fix is a different draft, not more passes.
5. Show the person the cleaned text and the score. Never the score alone.

## With Uplika connected

Nothing changes in how this runs: it works on text, on the person's machine, and Uplika does not run this check for you. Run it on anything another skill is about to send out through Uplika (a caption before it is published, a comment reply, a DM draft), and show the person the cleaned text before they approve the send.

## Without Uplika

Paste the draft and run the order of operations above. The person copies the cleaned text wherever it goes.

## Tools

None. This skill works on text on the person's machine and calls no Uplika tool.
