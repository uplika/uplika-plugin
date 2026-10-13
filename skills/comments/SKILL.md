---
name: comments
description: Read replies on your posts, sort them into answer, hide, idea, ignore, draft replies in your voice, and send after approval.
---

# Comments

Use this for "check my comments", "reply to the comments on yesterday's post", or a weekly comment round.

## Procedure

If a call answers `workspace_required`, the account has more than one workspace: show the names it lists, ask which one, and pass that `workspaceId` on every later call in this session.

1. Find the post: a link or id from the person goes straight to `open_post` (text, replies and metrics in one call). Without one, `list_posts` (posts made through Uplika) or `list_channel_posts` (everything on the channel, including posts written in the app) and let them pick.
2. Read the thread with `list_replies` (nested replies included; `truncated` means it stopped early).
3. Sort every reply into four groups and show them as a short table:
   - **Answer**: questions and comments that deserve a reply.
   - **Hide**: spam, abuse, scams. Hiding keeps it out of sight and can be undone.
   - **Idea**: a question or objection worth a post of its own. Collect these for the person.
   - **Ignore**: thanks, emoji, chatter.
4. Draft replies for the Answer group. Read `~/.uplika/<workspace-slug>/voice.md` first if it exists; if not, keep replies short and plain, and offer the `voice-profile` skill. Never invent facts, prices or promises; when the answer needs something only the person knows, ask.
5. Show the drafts and the hide list. Send only what the person approves:
   - `reply` with the post id and `replyTo` (the reply id) to nest under that comment; `wait: true` to confirm it is live.
   - `hide_reply` for the Hide group.
   - `delete_reply` only when the person explicitly asks to delete; it cannot be undone and reaches different things per channel (read the features table in `list_platforms`). Prefer hiding.
6. Report what was sent, hidden and collected as ideas.

## Channel notes

- What each channel allows (hiding, deleting, nested replies) is in the features table of `list_platforms`. On a Facebook Page the Page's own comment is deleted instead of hidden.
- Threads reply approval: when the account holds replies for approval, `approve_reply` with the account id and no reply id lists the queue; approving makes a reply public. Ask before approving.
- Naver Blog comments go through the person's Chrome extension; if a response carries `bridge`, follow `bridge.nextStep` (see the `troubleshoot` skill).
- Direct messages are the `inbox` skill. Automatic replies (comment-to-DM, keyword replies, AI replies) are the `automations` skill.

## Tools

- `open_post`: one post with its replies and metrics
- `list_posts`: posts made through Uplika
- `list_channel_posts`: everything on the channel
- `list_replies`: the reply thread under a post
- `reply`: send an approved reply
- `hide_reply`: hide (or unhide) a reply
- `delete_reply`: delete a reply for good, only on explicit request
- `approve_reply`: Threads held replies (list the queue, approve or ignore)
- `list_platforms`: which comment actions each channel supports
