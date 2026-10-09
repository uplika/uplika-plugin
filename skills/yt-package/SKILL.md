---
name: yt-package
description: "Write and lint a YouTube title and thumbnail as one pairing (truncation, repeats, vagueness), then apply it. For titles, thumbnail text, low CTR."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-package

The title and the thumbnail are ONE unit. Writing them separately is why most packaging fails: the thumbnail repeats the title, and half the click surface says the same thing twice. Use it for "title ideas", "what should I call this", "thumbnail text", "my CTR is bad", packaging, or any request to rename or repackage a video.

From this skill's folder:

```bash
python3 scripts/title.py --title "..." --thumb "AI RAN IT"
python3 scripts/title.py titles.txt            # one per line, ranked
```

Without a shell (claude.ai, ChatGPT) the script cannot run: apply the rules below by hand and say the titles were not linted.

## Before you write

1. Read `~/.uplika/<workspace-slug>/voice.md` if it exists. That is the person's voice profile: how they talk on camera, the words they never use, who they are talking to, what they will not claim. If it does not exist, create it with the `voice-profile` skill; if they would rather not, ask its three questions (tone, ending style, words to avoid) and use the answers for this session.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have one, ask for it or write the line without it.

## Rules the tool enforces, and why

- **Two cut points.** The tool reports where desktop search cuts a title (around 60 characters of Latin text) and where a mobile home feed cuts it (around 40), because they fail differently: a desktop cut loses the tail, a mobile cut can lose the subject. YouTube's own title limit is a different thing; read it from `list_platforms`.
- **The thumbnail must not repeat the title.** Different words, same promise.
- **Three words maximum on the thumbnail.** At feed size a fourth word is a grey smear.
- **A number, a name or a date** beats every adjective available to you.
- **Two all-caps words is the ceiling** before a title reads as spam.

Korean titles: `title.py` reads Korean words with their particles attached (so 자동화 on the thumbnail and 자동화하는 in the title count as a repeat), never counts a Hangul word as all-caps, and flags hype words such as 진짜, 대박, 미쳤다, 레전드. It marks the result `Korean: heuristic, not calibrated`: the cut points were measured on Latin text and Hangul is wider, so a Korean title is cut earlier than its character count suggests. Check it on a phone before trusting the length line.

## Write ten, keep two

Generate ten titles, run them all through `scripts/title.py`, show the person the top three with their scores and the specific issue on each. For the winner, write the thumbnail brief: the expression, the framing, the three words, and what the background has to do to hold contrast at feed size.

## With Uplika connected

1. **What worked before.** Find the YouTube account in `list_accounts`, then call `list_channel_posts` with its `accountId`. Each item's `text` is the title, a blank line, then the description; `permalink` is the video link. Call `get_insights` on the last ten to put views and likes next to each title (null means YouTube did not report it, not zero). Uplika has no impressions or click-through rate: those are in YouTube Studio, so ask the person for CTR if they want it in the comparison.
2. **Write and lint** as above.
3. **Apply the winner**, only after the person approves the exact title:
   - Call `update_post` with the video link as `id`, `wait: true`, the new `options.youtube.title`, and the current description as `content` (from the `list_channel_posts` text, or pasted by the person for an older video). Send the description even though it is not changing: for a video uploaded through Uplika, Uplika otherwise re-sends its own copy and undoes edits made in YouTube Studio.
   - Send only the `options.youtube` fields you are changing; the rest stay as they are on YouTube.
   - To change the thumbnail image too, get a media id for the image the way the `yt-upload` skill does and pass it as `options.youtube.thumbnailMediaId` in the same call. It works on long-form videos on verified channels only (`list_platforms` has the Shorts rule).
   - Read the result and any warning out to the person.
4. If a call answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId`. A channel that is not connected cannot be changed from here: send the person to https://uplika.com/dashboard/connections. Other errors: `get_help` with the code; `account_disconnected` goes to the `troubleshoot` skill.

## Without Uplika

The person pastes the titles they are weighing (and their past titles with view counts, if they want the comparison) and pastes the winner into YouTube Studio themselves.

## The gate

Nothing goes out until the person says yes. Every output ends in a block they can copy, and the last line of every run is the question: **ship it, or change it?** With Uplika connected, "ship it" means you apply it with `update_post`.

## Tools

- `list_accounts`: the YouTube account id
- `list_channel_posts`: the channel's recent videos with their current title and description
- `get_insights`: views and likes per video, next to its title
- `update_post`: apply the approved title (and thumbnail) to the live video
- `list_platforms`: YouTube's own title limit and thumbnail rule
- `get_help`: the answer for an error code
