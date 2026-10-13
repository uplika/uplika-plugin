---
name: performance-review
description: "Weekly or monthly review of your own posts: read real insights, compare to each channel's baseline, name what worked, propose next week."
---

# Performance review

Use this for "how did my posts do this week", a monthly report, or before planning the next batch.

## Procedure

If a call answers `workspace_required`, the account has more than one workspace: show the names it lists, ask which one, and pass that `workspaceId` on every later call in this session.

1. Window: ask for the period if the person did not say (this week, last 30 days).
2. Collect posts: `list_posts` with `since` and `until` for posts made through Uplika, and `list_channel_posts` for posts written in the channels' own apps when the person wants those too.
3. For each post, `get_insights`: views, likes, replies, reposts, quotes, shares. **Null is not zero**: some channels do not report views or shares, or not yet. Keep nulls out of averages and say which channel did not report.
4. Baseline per channel: compare each post to the median of the same channel's posts in the window, never across channels (a Threads post and a YouTube video do not share a scale). With too few posts on a channel, say the baseline is weak.
5. What worked: look at the top and bottom posts per channel and name concrete differences you can see in the posts themselves: the hook type (question, number, claim, story), length, chain or single post, media or text, posting time. Say how confident you are; one post is an anecdote.
6. Say what Uplika does not have: impressions per follower, click-through rate, watch time and retention curves are not in these tools (for YouTube retention, see `yt-retention`).

## Output

One table (post, channel, date, the metrics, against baseline), then three bullets for what worked, then three concrete things to try next week, each tied to a post in the table. Offer to draft next week with `schedule-week`.

## Tools

- `list_posts`: posts made through Uplika in the window
- `list_channel_posts`: posts on the channel, including ones written in the app
- `get_insights`: per-post metrics (null means not reported)
