---
name: yt-plan
description: "Plan a week or month of YouTube uploads sized to the hours the creator has, then schedule them. For 'plan my week', content calendar, what to post."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-plan

A plan that does not fit the week is a list of regrets. Ask two questions before writing anything: **how many hours do you actually have**, and **what is already half-made**. Use it for "plan my week", "content calendar", "what should I post", "I have no idea what to make next".

## Before you write

1. Read `~/.uplika/<workspace-slug>/voice.md` if it exists. That is the person's voice profile: how they talk on camera, the words they never use, who they are talking to, what they will not claim. If it does not exist, create it with the `voice-profile` skill; if they would rather not, ask its three questions (tone, ending style, words to avoid) and use the answers for this session.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have one, ask for it or write the line without it.

## With Uplika connected

1. **The rhythm so far.** Find the YouTube account in `list_accounts`, then call `list_channel_posts` with its `accountId`: the `timestamp` of each video is the real upload rhythm, and `get_insights` on the recent ones shows which held views (null means not reported, not zero). The best day to post is in YouTube Studio's audience data, not in Uplika: ask the person for it rather than assume.
2. **Plan** the week as below.
3. **Schedule**, after the person approves the whole table. For each slot whose video file is ready, prepare it the way the `yt-upload` skill does (media id, `options.youtube.title`, privacy, the made-for-kids answer) and call `publish` with `scheduledAt` set to the slot's time with a time zone offset. Ask which time zone they mean; do not guess. Uplika keeps the video and uploads it at that time. Slots without a finished video stay in the plan and nothing is scheduled for them.
4. Each `publish` answers with status scheduled and its time: show the person the list of what is booked.
5. If a call answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId` on every call, `publish` included. A channel that is not connected: https://uplika.com/dashboard/connections. Other errors: `get_help` with the code.
6. `youtube_quota_exhausted` from `list_channel_posts`, or `noteCode` `youtube_quota_exhausted` from `get_insights`: Uplika's daily YouTube limit, which everyone on Uplika shares, ran out: stop and do not repeat the call, tell the person when it refills (`resetsAt`, or the time in the message), and do not ask them to reconnect, because it is not their account (`faq:youtube-daily-limit`). A booked upload that comes due on such a day ends with `youtube_daily_cap` and is not sent; it goes again only when someone sends it after that time.

## Without Uplika

The person tells you their upload rhythm and their best day from YouTube Studio, and schedules the uploads in Studio themselves.

## The shape of a week

- **One anchor.** The video the week is for. It gets the most time and it goes out on the day the channel's own analytics say is best: ask for that, do not assume Tuesday.
- **One cheap one.** Built from something that exists: a clip, a reaction, a follow-up to the comment that got the most replies last week.
- **Shorts from the anchor.** Three, cut from the long video, not written separately. `yt-shorts` finds them.

Three uploads on a seven-day week, not seven. A plan that posts daily is not a plan anyone recognises, and the empty days are what make the filled ones survive a bad week.

## What to hand back

A table: day, format, working title, the one sentence it promises, and what already exists for it. Then the honest line at the bottom: how many hours this costs, and what to drop first if the week goes wrong.

## The gate

Nothing is scheduled until the person approves the table. Every output ends in a block they can copy, and the last line of every run is the question: **ship it, or change it?** With Uplika connected, "ship it" means you schedule the ready videos with `publish`.

## Tools

- `list_accounts`: the YouTube account id
- `list_channel_posts`: upload dates of the recent videos, the real rhythm
- `get_insights`: views and likes of recent videos
- `publish`: schedule a ready video with `scheduledAt`, after approval
- `get_help`: the answer for an error code
