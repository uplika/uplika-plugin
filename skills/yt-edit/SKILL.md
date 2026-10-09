---
name: yt-edit
description: "Turn a recording's transcript into an edit decision list: dead air, filler, retakes, with timecodes. For 'edit this', 'cut the dead air', tightening."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-edit

An edit decision list from a timestamped transcript. It prints the cuts. The person applies them. Use it for "edit this", "cut the dead space", "tighten this video", "I rambled", or any request to shorten footage from a transcript.

From this skill's folder:

```bash
python3 scripts/deadair.py transcript.srt              # srt, vtt or whisper json
python3 scripts/deadair.py transcript.srt --floor 0.35 --json
```

Without a shell (claude.ai, ChatGPT) the script cannot run: read the transcript, mark the same three things by hand, and say the timings were not computed.

## With Uplika connected

Nothing changes. Uplika has no transcript or editing tool and this skill calls none; it works the same for everyone.

## Without Uplika

No transcript yet? Ask for one, or produce one first: `whisper`, `faster-whisper`, or the caption track YouTube generates on an unlisted upload all work. When a shell is available and the video is already on YouTube (unlisted is fine), this saves YouTube's automatic captions as an srt file (use the video's language code):

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs ko --convert-subs srt "<video link>"
```

Do not guess at timings.

## What it finds

- **DEAD**: gaps longer than the floor, trimmed from the MIDDLE so both sides keep a breath. Cutting flush against speech is what makes a tightened take sound gasping.
- **FILLER**: cues that are nothing but "um", "so yeah", "basically".
- **REPEAT**: a sentence restarted. Compared against the last cue that was actually speech, not the literal previous cue, because most retakes have an "um" between the two attempts.

## Korean transcripts

`deadair.py` keeps Hangul (the original dropped it, so it never found a Korean retake). Korean hesitations and filler words (음, 어, 그러니까, 이제 and the like) count as FILLER. A cue that is only the retake marker 다시 or 아니, with or without fillers, is cut as FILLER and the take before it as REPEAT. A Korean restart is the same opening syllables twice. The run prints `Korean: heuristic, not calibrated`: the word lists are new and untested on real footage, so check each Korean cut against the recording before applying it.

## What it will not do

It does not touch media. It has no opinion about your B-roll. A 40% cut on the report is a 40% cut of SPEECH, and if the video has a long silent demo in it that number is wrong: check the report against the footage before you trust the runtime at the bottom.

## The gate

Nothing here publishes. This skill writes and the person edits. Every output ends in a block they copy, and the last line of every run is the question: **ship it, or change it?**

## Tools

None. This skill calls no Uplika tool; it runs `scripts/deadair.py` on a transcript.
