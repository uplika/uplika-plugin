---
name: yt-chapters
description: "Write YouTube chapters from a transcript, checked against YouTube's chapter rules so they render, and add them to the video. For chapters, timestamps."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-chapters

Chapters from a timestamped transcript. Use it for "add chapters", "timestamps", "break this video into sections". From this skill's folder:

```bash
python3 scripts/chapters.py transcript.srt --target 8
```

The input is the transcript (srt, vtt or whisper json). When a shell is available and the video is on YouTube, this saves its automatic captions (use the video's language code):

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs ko --convert-subs srt "<video link>"
```

Without a shell (claude.ai, ChatGPT) the script cannot run: draft the boundaries by hand from the transcript and check the rules below yourself.

## The rules, which are not optional

A chapter list that breaks any of these silently does not become chapters at all: the block just sits in the description doing nothing.

- The first entry must be **00:00**.
- There must be **at least three**.
- Each must be **at least 10 seconds** long.

These are YouTube's chapter rules as `chapters.py` checks them; no Uplika tool returns them. The tool checks all three and tells you when a list is invalid rather than letting you paste it.

## Retitle every line

`chapters.py` finds the BOUNDARIES well: it scores the pauses the speaker actually took by how much the vocabulary shifts across them. The titles it emits are the topic words, and they are a draft. A chapter called "Thumbnails Titles Packaging" is a placeholder. Rewrite each one as the promise of that section, in the person's voice (read `~/.uplika/<workspace-slug>/voice.md` if it exists; if not, the `voice-profile` skill can create it), three to five words.

Chapters are also a retention diagnostic: if a section cannot be named in five words, it is two sections or it is filler.

Korean transcripts: `chapters.py` reads Hangul words for the vocabulary shift and the draft titles (the original read none, so every Korean title came out as "Section"). The words keep their particles, and the run is marked `Korean: heuristic, not calibrated`. Rewrite every title anyway.

## With Uplika connected

The chapter block goes in the description. After the person approves the block and where it sits:

1. Find the YouTube account in `list_accounts` and read the video's current title and description from `list_channel_posts` (each item's `text` is the title, a blank line, then the description). For an older video that is not in the list, ask the person to paste the current description.
2. Put the block into that description (after the first two lines and any link, the way the `yt-seo` skill lays it out) and show the whole new description.
3. Call `update_post` with the video link as `id`, `wait: true`, the new description as `content`, and the current `options.youtube.title`. Always send the title: for a video uploaded through Uplika, `options` replaces what Uplika has on record and YouTube needs a title. Send no other `options.youtube` field; the rest stay as they are on YouTube.
4. YouTube measures the description with its own rule (`list_platforms` has it); if the new one is too long, the call says so. Read the result and any warning out to the person.
5. If a call answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId`. A channel that is not connected: https://uplika.com/dashboard/connections. Other errors: `get_help` with the code; `account_disconnected` goes to the `troubleshoot` skill.

## Without Uplika

The person pastes the block under the video in YouTube Studio themselves.

## The gate

Nothing goes out until the person says yes. Every output ends in a block they can copy, and the last line of every run is the question: **ship it, or change it?** With Uplika connected, "ship it" means you add the block with `update_post`.

## Tools

- `list_accounts`: the YouTube account id
- `list_channel_posts`: the video's current title and description
- `update_post`: put the approved chapter block into the description
- `list_platforms`: YouTube's description rule
- `get_help`: the answer for an error code
