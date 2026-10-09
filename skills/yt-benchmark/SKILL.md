---
name: yt-benchmark
description: "Find YouTube videos that beat their channel size (views over subscribers at least 3x by default) and plan your own video from the pattern."
---

# yt-benchmark

Find the videos on a topic that pulled far more viewers than their channel has subscribers, read what they share, and turn the pattern into a plan for the person's own video. Use it for "benchmark videos", "videos that blew up on small channels", "what should my next video be", or before `yt-script` when the person has a topic but no angle.

## 1. Ask first

- **Topic**, as a viewer would type it, and the video the person wants to make, in one line.
- **Format**: Shorts, long-form or both.
- **Period**: how recent (the tool takes 7d, 1m, 3m, 6m, 1y, or no limit).
- **Threshold**: views over subscribers. The default is **3**; if the person gives a value, theirs wins.

## 2. Search several ways

Call `search_youtube_videos` more than once: vary `order` (viewCount, relevance, date), `period` and `format` around what the person asked, and try one or two other ways a viewer would phrase the topic. Pass the one-line video as `topic` so each answer's `prompt` is filled in, and use the largest `max` the tool accepts.

- The same search again is cached and free; each new combination spends one of the person's daily searches. Read `quota` (`usedToday`, `dailyLimit`) in each answer, tell the person how many searches the sweep will take before you start, and stop before the allowance runs out.
- `research_tool_disabled`: ask the person once to turn the tool on at the `enableUrl` in the error, and do not retry until they say it is on.
- `research_quota_exceeded` (the person's own daily searches are used up): stop the sweep, work with what you have, and say so.
- `youtube_quota_exhausted` (the shared quota for today, back at `resetsAt`): stop and work with what you have. When a shell is available, the `yt-viral` skill's method without Uplika (`yt-dlp --flat-playlist -J` on each candidate channel, ranked by the multiple over the channel's own median) can stand in; say the axis changed.
- `platform_error`: YouTube did not answer; try once more a minute later. Anything else: `get_help` with the code.

## 3. Merge and filter

- Merge the answers by `videoId`: a video found by several searches counts once.
- Keep the videos whose `viewSubRatio` (views divided by subscribers) is at or above the threshold, sorted by ratio. These are the benchmark set.
- If fewer than five clear it, lower the threshold to 2, then to 1.5, and **say that you lowered it**, and to what.
- `viewSubRatio` is null when a channel hides its subscriber count. List those videos separately; never count them as passing, and never as zero.

## 4. Look at them

- Download each `thumbnail` address and look at it (with a shell, save it with curl; otherwise open the address if you can view images). Note the words on it, the face or object, and the contrast at small size.
- When a shell is available, this gets a benchmark video's captions so you can read its first fifteen seconds (use the video's language code). Without a shell, work from the titles and thumbnails.

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs ko --convert-subs srt "<video url>"
```

## 5. Name the pattern

From the benchmark set: the title structure (name each formula by running the titles through `../yt-script/scripts/hookscore.py --json` and reading `formula`), the hook words, the length (`durationSec`, and `isShort` as the answer labels it), the format, when they were published (`publishedAt`), and what the thumbnails share. Optional: compare with the person's own channel. Find their YouTube account in `list_accounts`, call `list_channel_posts` with it (each item's `text` starts with the title), and name what they have not tried yet.

## 6. Plan the person's video

The answer's `prompt` is the skeleton: the top results as a table, then patterns, titles, hooks and format. Fill it from the benchmark set rather than only the most viewed. Read `~/.uplika/<workspace-slug>/voice.md` first if it exists, so the titles and hooks sound like the person (the `voice-profile` skill creates it). Hand back:

- five titles, linted with `../yt-package/scripts/title.py`
- five hooks, scored with `../yt-script/scripts/hookscore.py` (Korean hooks get a rank-only score marked `Korean: heuristic, not calibrated`)
- an outline, a thumbnail brief, the length and format, and when to publish

Never invent a view count, a subscriber count or the reason a video worked: the formula line is a judgement about the title, not a cause. Without a shell the scripts cannot run; say the titles and hooks were not scored.

## 7. Hand over

The full script goes to `yt-script`, the title and thumbnail to `yt-package`, and the upload to `yt-upload`.

## Tools

- `search_youtube_videos`: the topic's top videos with views, subscribers, their ratio, thumbnails and the planning `prompt`
- `list_accounts`: the person's YouTube account, for the optional comparison
- `list_channel_posts`: the person's own recent titles, for the comparison
- `get_help`: the answer for an error code
