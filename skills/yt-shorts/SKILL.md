---
name: yt-shorts
description: "Find the Shorts inside a long YouTube video from its transcript, write a new first line for each, and upload them. For 'cut this into shorts', clips."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-shorts

A Short cut out of a long video is not a clip of the best moment. It is a moment that **survives without the video around it**, which is a much smaller set. Use it for "cut this into shorts", "clip this", "repurpose this video", "what should I clip".

The input is the long video's transcript (srt, vtt or whisper json). When a shell is available and the video is on YouTube, this saves its automatic captions (use the video's language code):

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs ko --convert-subs srt "<video link>"
```

## Before you write

Read `~/.uplika/<workspace-slug>/voice.md` if it exists, for the new first lines. If it does not exist, create it with the `voice-profile` skill, or ask its three questions (tone, ending style, words to avoid) and use the answers for this session.

## Picking

Read the transcript and find spans of roughly 20-55 seconds (the original pack's rule of thumb for a Short that holds; YouTube's own Shorts rule is in `list_platforms`) where all three are true:

1. It opens on a complete thought. If the first sentence needs the previous minute, it is not a Short.
2. There is a turn in it: a claim, then something that complicates or proves it.
3. It ends on a line, not a trail-off.

Rank the candidates and show the person the top five with their timecodes and first line, so they can reject one without reading the whole transcript.

## Writing each one

- **A NEW first line.** The long video's line assumes context this viewer does not have. Write the replacement and run it through `../yt-script/scripts/hookscore.py` (a Korean line gets a rank-only score marked `Korean: heuristic, not calibrated`).
- **On-screen text for the first two seconds**, different words from the spoken line.
- **A loop point**: what the last line sets up so the first line answers it.
- Vertical framing note: what gets cropped out of a 16:9 frame and whether that matters.

## With Uplika connected

Uplika cannot cut video: the person cuts each Short in their editor as a vertical clip. Then, for each Short:

1. `select_channels` with scope `youtube` gives the account id to post to, and `skipped` with a reconnect link if the connection needs it. Nothing connected: https://uplika.com/dashboard/connections.
2. The file: if it has a public https address, `media_from_url`; if it is on the person's computer or phone, upload it the way the `yt-upload` skill does.
3. Read YouTube's `shorts` rule in `list_platforms`: a vertical video inside that length goes up as a Short, and a custom thumbnail does not apply to it.
4. Show the person the title (`options.youtube.title`; the new first line is a good start), the description, the privacy (`options.youtube.privacyStatus`; left out, it goes up private), whether it is made for kids (`options.youtube.madeForKids`: ask, and send it only from their answer), and when it goes out. Only after they approve, call `publish` with the account id, the media id, `wait: true`, and `scheduledAt` with a time zone offset if it should go out later.
5. `get_post` gives the status, the link and any warning (for example the privacy YouTube actually applied). Read the warning out.
6. If a call answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId`. Errors: `get_help` with the code.

## Without Uplika

The person cuts and uploads the Shorts themselves: hand them the titles, first lines, on-screen text and timecodes.

## The gate

Nothing goes out until the person says yes. Every output ends in a block they can copy, and the last line of every run is the question: **ship it, or change it?** With Uplika connected, "ship it" means you upload the approved Shorts with `publish`.

## Tools

- `select_channels`: the YouTube account to post to
- `list_platforms`: YouTube's Shorts rule
- `media_from_url`: attach a Short that already has a public https address
- `publish`: upload an approved Short, now or at `scheduledAt`
- `get_post`: status, link and warnings after the upload
- `get_help`: the answer for an error code
