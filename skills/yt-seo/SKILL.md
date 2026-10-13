---
name: yt-seo
description: "Write a YouTube description, tags and search text aimed at what people type, and apply them to the video. For descriptions, tags, SEO, getting found."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-seo

Search is a smaller lever than packaging and a bigger one than people think for evergreen videos. For a video aimed at the subscriber feed, say so and spend the effort on `yt-package` instead. Use it for "write my description", "tags", "SEO", "help this video get found", "nobody is finding this".

## Before you write

1. Read `~/.uplika/<workspace-slug>/voice.md` if it exists. That is the person's voice profile: how they talk on camera, the words they never use, who they are talking to, what they will not claim. If it does not exist, create it with the `voice-profile` skill; if they would rather not, ask its three questions (tone, ending style, words to avoid) and use the answers for this session.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have one, ask for it or write the line without it.

## The description

- **The first two lines are the only ones anyone reads.** They show above "...more" and they are the search snippet. Say what the video gives them, in the words they would have typed.
- Then the link or the resource, if there is one, so it is above the fold.
- Then chapters (`yt-chapters` writes them).
- Then the long version: what is covered, who it is for, what it assumes.

YouTube measures the description with its own rule, in bytes rather than characters, so Korean text reaches the limit sooner: read the rule from `list_platforms` before writing a long one.

## Tags, honestly

Tags are a weak signal and YouTube has said so. Use them for disambiguation (spellings, the tool names, the abbreviations people actually type) and stop. Fifteen is plenty. A wall of tags is not a strategy and stuffing unrelated ones is against the terms. The tag list also has a total length limit, given in the `options.youtube.tags` schema in `list_platforms`.

## The query test

Before handing anything over, write the three search queries this video should win, and check the title and first two description lines contain the words in those queries. If they do not, the problem is the title, not the description.

## With Uplika connected

1. **Check each query.** Call `search_youtube_videos` with each of the three queries as `q`: `order` relevance shows what YouTube ranks for it, viewCount what got watched. Read the titles and `viewSubRatio`; a query where the top results are all large channels with low ratios is hard to win. Uplika's search has no search volume: say so, and do not invent one. The same search again is cached and free; each new one spends one of the person's daily searches (`quota`).
   - `research_tool_disabled`: only a research tool still in beta answers this. Ask the person once to turn it on at the `enableUrl` in the error, and do not retry until they say it is on. Write without it meanwhile.
   - `research_quota_exceeded` or `youtube_quota_exhausted`: skip the check and say so.
2. **Apply**, only after the person approves the description and tags:
   - Find the YouTube account in `list_accounts` and read the video's current title from `list_channel_posts` (each item's `text` is the title, a blank line, then the description).
   - Call `update_post` with the video link as `id`, `wait: true`, the new description as `content`, `options.youtube.title` (the current one if it is not changing: for a video uploaded through Uplika, `options` replaces what Uplika has on record and YouTube needs a title), `options.youtube.tags`, and `options.youtube.defaultLanguage`, the language the title and description are written in as one BCP-47 code such as en-US or ko.
   - Send only the `options.youtube` fields you are changing; the rest stay as they are on YouTube.
   - Read the result and any warning out to the person.
3. If a call answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId`. A channel that is not connected: https://uplika.com/dashboard/connections. Other errors: `get_help` with the code; `account_disconnected` goes to the `troubleshoot` skill.

## Without Uplika

The person gives the topic and the queries they care about, and pastes the description and tags into YouTube Studio themselves.

## The gate

Nothing goes out until the person says yes. Every output ends in a block they can copy, and the last line of every run is the question: **ship it, or change it?** With Uplika connected, "ship it" means you apply it with `update_post`.

## Tools

- `search_youtube_videos`: what already ranks and gets watched for each target query
- `list_accounts`: the YouTube account id
- `list_channel_posts`: the video's current title
- `update_post`: apply the approved description, tags and language to the video
- `list_platforms`: YouTube's description and tag rules
- `get_help`: the answer for an error code
