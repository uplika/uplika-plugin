---
name: yt-retention
description: "Read a YouTube Studio audience-retention CSV: hook leak, cliffs, slide, and the one change to make. For 'why do people stop watching', pacing."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-retention

The retention graph is the only honest feedback YouTube gives you. Almost nobody exports it. Use it for "why do people stop watching", "my retention is bad", a pasted retention chart or CSV, or "fix my pacing".

From this skill's folder:

```bash
python3 scripts/retention.py retention.csv --duration 600
python3 scripts/retention.py retention.csv --transcript transcript.srt
```

Getting the file: Studio -> a video -> Analytics -> Engagement -> the audience-retention chart -> the download icon -> "Audience retention".

Without a shell (claude.ai, ChatGPT) the script cannot run: read the pasted numbers for the same three problems by hand and say the figures were not computed.

## With Uplika connected

Studio CSV only, Uplika has no retention curve. Its metrics for a video are views, likes and comments, not where people left, so the input stays the export above. The transcript for `--transcript` is the same one `yt-edit` uses; when a shell is available and the video is on YouTube, this saves YouTube's automatic captions (use the video's language code):

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs ko --convert-subs srt "<video link>"
```

A Korean transcript works as it is: the tool only prints what was being said at each drop.

## Without Uplika

The same: the person exports the CSV from Studio and, for `--transcript`, gives you the transcript.

## Three different problems

- **HOOK LEAK**: what is lost in the first 30 seconds. Under 25% is healthy. This is always the first thing to fix and it is always the first fifteen seconds of script, never the edit.
- **CLIFFS**: single steep drops. A cliff is a moment: a topic change with no signposting, a sponsor read, a long setup. With `--transcript` the tool prints what was being said there, which is what makes the report actionable instead of interesting.
- **SLIDE**: the steady bleed across the middle. A flat slide is pacing. The fix is cutting, not rewriting.

## What to hand back

Name the single biggest leak and one change for it. Not a list of five. Then, only if asked, the rest. And if the hook leak is healthy and the slide is flat, say the video is fine and the problem is packaging: send them to `yt-package`.

## The gate

Nothing here publishes. This skill writes and the person publishes. Every output ends in a block they copy, and the last line of every run is the question: **ship it, or change it?**

## Tools

None. Uplika has no retention data; this skill runs `scripts/retention.py` on the person's Studio export.
