---
name: yt-viral
description: "Find what is working in a YouTube niche, ranked by how far each video beat its channel, and name the formula. For viral videos, competitor research."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-viral

Raw view counts rank channel size, not ideas. This ranks each video by how far it beat its own channel, which is the only version of the question that is about the video. Use it for "what's working right now", "find viral videos in my niche", "why did this blow up", competitor research, or a swipe file.

## With Uplika connected

If a call answers `workspace_required`, the account has more than one workspace: show the names it lists, ask which one, and pass that `workspaceId` on every later call in this session.

1. Call `search_youtube_videos` with the niche as a viewer would type it (`q`), `order` viewCount, a `period` that fits ("what's working right now" means a recent one), `format` if the person only makes Shorts or only long videos, and the largest `max` the tool accepts. The same search again is cached and free; each new combination spends one of the person's daily searches, shown in `quota`.
2. **Rank by `viewSubRatio`**: views divided by the channel's subscribers, so above 1 means the video pulled more people than the channel has. This is a different axis from this skill's original method, the multiple over the channel's own median: the ratio compares a video with the size of its channel's audience, not with the channel's other videos. Say which axis you used when you present the list.
3. `viewSubRatio` is null when a channel hides its subscriber count. List those separately, never as zero and never as winners.
4. **Name the formula** for each top title: put the titles one per line in a file and run `python3 ../yt-script/scripts/hookscore.py --json titles.txt`, then read each `formula` (the same 21 formulas swipe.py uses, with the Korean patterns for Korean titles). Without a shell, match them by eye against `../yt-script/scripts/hooks.json`.
5. Failures:
   - `research_tool_disabled`: only a research tool still in beta answers this. Ask the person once to turn it on at the `enableUrl` in the error, and do not retry until they say it is on.
   - `youtube_quota_exhausted` (the shared quota for today, back at `resetsAt`) or `research_quota_exceeded` (the person's own daily searches): when a shell is available, fall back to the method without Uplika below, collecting with `yt-dlp --flat-playlist -J`, and say the axis changed to the channel-median multiple. Without a shell, ask for a pasted list or wait for the reset.
   - `platform_error`: YouTube did not answer; try once more a minute later. Anything else: `get_help` with the code.

## Without Uplika

The original method ranks by **multiple over each channel's own median**. From this skill's folder:

```bash
python3 scripts/swipe.py collected.json --min 2.0
```

You need at least four videos per channel or a median means nothing, and the tool will skip the channel and tell you it did. Collect them however the person prefers: when a shell is available, `yt-dlp --flat-playlist -J` against a channel's videos page is the fastest, the public page works, a manual list works.

```json
[{"channel":"...","title":"...","views":412000,"url":"...","duration":613}]
```

**Read, do not scrape.** Public listings only, never a logged-in session, never the person's own account credentials.

## Reading the output

The multiple (or the ratio) is the signal. The formula line is a judgement about the TITLE, matched against [the 21 formulas](../yt-script/scripts/hooks.json): it is not a claim about why the video worked, and you should say so when you present it. A Korean title is matched with newly written Korean patterns and marked `Korean: heuristic, not calibrated`.

What to hand back: the top five with their multiples or ratios, the formula each used, and the ONE structural thing they share. Then the harder line: which of those the person could actually make this week, in their voice, with what they have. For a full plan built from the pattern, the `yt-benchmark` skill goes further.

## The gate

Nothing here publishes. This skill writes and the person publishes. Every output ends in a block they copy, and the last line of every run is the question: **ship it, or change it?**

## Tools

- `search_youtube_videos`: the niche's top videos with views, subscribers and their ratio
- `get_help`: the answer for any other error code
