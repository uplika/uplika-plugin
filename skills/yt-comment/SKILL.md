---
name: yt-comment
description: "Triage YouTube comments into four piles and reply in the creator's voice, sent after approval. For 'reply to my comments', a comment thread."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-comment

The comment section is a retention surface, not a chore. Replies in the first few hours are what decide whether a thread becomes a conversation other people read. Use it for "reply to my comments", "handle the comment section", "someone asked X", or a pasted comment thread.

## Before you write

1. Read `~/.uplika/<workspace-slug>/voice.md` if it exists. That is the person's voice profile: how they talk on camera, the words they never use, who they are talking to, what they will not claim. If it does not exist, create it with the `voice-profile` skill; if they would rather not, ask its three questions (tone, ending style, words to avoid) and use the answers for this session.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have one, ask for it or write the line without it.

## With Uplika connected

1. **Find the video.** Take the link from the person, or find the YouTube account in `list_accounts` and pick the video from `list_channel_posts` (each item has a `permalink`).
2. **Read the comments** with `list_replies` on the video link. `truncated` means the list stopped before the end; say so. YouTube does not mark which comments are the creator's own, so skip the ones written under the channel's own name. If the answer is `comments_closed`, comments are turned off on that video.
3. **Triage and write** as below.
4. **Show every reply and every hide** (the comment and what you will do with it) and send only what the person approves: `reply` with the video link as `id`, the comment's id from `list_replies` as `replyTo`, and `wait: true`. Bait the person wants out of sight goes through `hide_reply` with the comment id and the video as `postId`; `hide: false` shows it again.
5. Pinning and hearting are not among Uplika's tools: name the comment to pin and the ones to heart, and the person does it in YouTube Studio.
6. If a call answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId`. A channel that is not connected: https://uplika.com/dashboard/connections. Other errors: `get_help` with the code; `reconsent_required` and `account_disconnected` go to the `troubleshoot` skill.

## Without Uplika

The person pastes the comment thread, and posts the approved replies themselves.

## Triage first, always

Sort the comments into four piles and say how many are in each before writing anything:

1. **Questions**: answer them. These are the next video's topics, so note the repeats.
2. **Corrections**: if they are right, say so plainly and thank them. Never argue a fact you cannot check.
3. **Praise**: reply to a few, briefly, with something specific from their comment. A wall of identical "thank you!" replies reads as automated because it is.
4. **Bait**: do not reply. Say so and move on. Never write a comeback, however deserved.

## Writing the reply

- Under 30 words. A long reply in a comment thread is a blog post nobody asked for.
- Answer the actual question in the first sentence.
- One question back, only when it is real.
- No emoji unless the person's own replies use them. Check their voice file.
- Never promise a video they have not agreed to make.

## The heart and the pin

Say which ONE comment to pin and why. Pin the question the most people also have, not the nicest one. Heart generously: it costs nothing and it is visible.

## The gate

Nothing goes out until the person says yes. Every output ends in a block they can copy, and the last line of every run is the question: **ship it, or change it?** With Uplika connected, "ship it" means you send the approved replies with `reply`.

## Tools

- `list_accounts`: the YouTube account id
- `list_channel_posts`: the channel's videos and their links
- `list_replies`: the comments under a video
- `reply`: post an approved reply under a comment
- `hide_reply`: hide a comment the person wants out of sight, or show it again
- `get_help`: the answer for an error code
