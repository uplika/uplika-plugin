---
name: voice-profile
description: "Create or update the voice file the writing skills read: tone, ending style, words to avoid, signature, examples from recent posts."
---

# Voice profile

Every writing skill in this plugin reads one file before it writes: `~/.uplika/<workspace-slug>/voice.md`. One file per workspace, because a workspace is one brand. Claude Code, Codex and the other agents all read the same path, so the voice stays the same whichever agent writes.

## When to use

- The person asks to set up or change how their posts should sound.
- A writing skill found no voice file and the person agreed to make one.

## Procedure

1. Find the workspace slug: `list_accounts` shows the workspace; if the account has several and the answer is `workspace_required`, ask which one and pass that `workspaceId` on every later call in this session.
2. If the file exists, read it and ask what to change. Otherwise start from `references/voice-template.md`.
3. Ask three questions first, in the person's language: the tone (two or three words), how posts usually end, and words they never use. Then the optional ones: who they talk to, what they will not claim, their signature (hashtags, sign-off, links).
4. Pull examples from what they actually wrote: call `list_channel_posts` for their main channel and take three to five recent posts (their best ones if they say which). Paste them as they are; do not rewrite them.
5. Show the whole file and save it only after they approve. Create the folder if needed.

## Agents that cannot write files

Keep the profile in the conversation for this session only and say so. Offer the text so the person can save it themselves.

## Tools

- `list_accounts`: which workspace (slug) the file belongs to
- `list_channel_posts`: the person's own recent posts as examples
