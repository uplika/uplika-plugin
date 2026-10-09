---
name: yt-audit
description: "Audit a YouTube channel from its recent videos and metrics (packaging, hooks, rhythm) and end in one fix. For 'audit my channel', 'why not growing'."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-audit

An audit that lists twenty problems is a way of avoiding the one that matters. This ends in ONE fix. Use it for "audit my channel", "why isn't my channel growing", "review my videos", or a pasted channel URL.

## Before you write

1. Read `~/.uplika/<workspace-slug>/voice.md` if it exists. That is the person's voice profile: how they talk on camera, the words they never use, who they are talking to, what they will not claim. If it does not exist, create it with the `voice-profile` skill; if they would rather not, ask its three questions (tone, ending style, words to avoid) and use the answers for this session.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have one, ask for it or write the line without it.

## With Uplika connected

The input is the person's own connected channel instead of a pasted URL.

- Find the YouTube account in `list_accounts`, then call `list_channel_posts` with its `accountId`. Each item's `text` is the title, a blank line, then the description; `timestamp` is the upload date; `thumbnailUrl` is the thumbnail image; `permalink` is the link.
- Call `get_insights` on each of the last ten (the link works as `id`): views, likes and comments. Null means YouTube did not report it, not zero.
- What Uplika cannot see: impressions, click-through rate and retention. Ask the person for those from YouTube Studio, or send them to `yt-retention` with the export.
- If a call answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId`. A channel that is not connected: https://uplika.com/dashboard/connections, or use the steps without Uplika. Other errors: `get_help` with the code.

## Without Uplika

The person pastes the channel URL or the last ten titles with their views. When a shell is available, `yt-dlp --flat-playlist -J "<channel url>/videos"` lists the recent uploads with their titles and view counts.

## What to look at, in this order

1. **The last ten titles, as a set.** Read them as a list, the way the channel page shows them. Do they promise different things? Run them through `../yt-package/scripts/title.py`. A channel where every title is the same shape has a format problem, not a title problem.
2. **The thumbnails, at feed size.** Shrink them. What survives? If three of them are unreadable at that size, that is the fix and nothing else matters yet. With Uplika, download each `thumbnailUrl` and look at it small if you can view images; otherwise ask the person for screenshots of the channel page.
3. **The first fifteen seconds of the three most recent.** Transcribe them and score with `../yt-script/scripts/hookscore.py`. This is where most channels lose. When a shell is available, `yt-dlp --skip-download --write-auto-subs --sub-langs ko --convert-subs srt "<video link>"` gets YouTube's captions (use the video's language code). Korean openings get a rank-only score marked `Korean: heuristic, not calibrated`.
4. **Upload rhythm.** Not frequency: CONSISTENCY. Six videos in one week and then nothing for a month is worse than one a fortnight forever. With Uplika, the `timestamp` of each video is the rhythm.
5. **The retention shape**, if they can export it. `yt-retention`.

## What to hand back

- The single biggest fix, named, with what to do this week.
- Three things that are already working, so they do not break them. Be specific; "your energy is good" is not an observation.
- What NOT to do yet, and why.

Never open an audit with praise you do not mean, and never end one with a list of twenty things.

## The gate

Nothing here publishes. This skill writes and the person publishes. Every output ends in a block they copy, and the last line of every run is the question: **ship it, or change it?**

## Tools

- `list_accounts`: the YouTube account id
- `list_channel_posts`: the last videos with title, description, date, thumbnail and link
- `get_insights`: views, likes and comments per video
- `get_help`: the answer for an error code
