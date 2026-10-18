---
name: inbox
description: Read DM conversations, draft replies in your voice, send after approval; respects the 24-hour window and pending-approval drafts.
---

# Inbox

Use this for "check my DMs", "answer my messages", "what is in my inbox". It reads the conversations Uplika receives (direct messages, and public threads such as mentions on Threads), drafts replies in the person's voice, and sends only what the person approves. Below, "the contact" is whoever wrote to the account.

## 1. Read

1. Start with `list_accounts` to see which accounts are connected; never assume one is. With nothing connected that receives messages, there is nothing to read: send the person to https://uplika.com/dashboard/connections. If a call answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId`.
2. `list_conversations` lists open conversations by default. Narrow it with `state` (`closed` for closed ones), `unread`, `kind` (`dm` or `mention`), `accountId`, or `search` (a name or words from the last message). Each item says whether the messaging window is open and how much of it is left.
3. Show the list with the conversations whose window closes soonest first, then mentions, then those whose window is closed.
4. `read_conversation` opens one: the recent messages and the contact (name, whether they follow the account on Instagram, tags, opt-out). AI drafts waiting for approval appear there with status `draft`.
5. `get_contact` when you need more about the contact: username, follow status in both directions (Instagram, and only for people who have messaged), follower count, tags, opt-out, and when their window closes. Pass `refresh: true` to re-read the profile from the channel.

## 2. Draft

Read `~/.uplika/<workspace-slug>/voice.md` first if it exists. If not, ask three questions (tone, how messages end, words to avoid) and offer to save the answers with the `voice-profile` skill.

- Answer what the contact asked, in the language they wrote in. Keep it short: one message unless the question needs more.
- Never invent prices, stock, dates, links or promises. When the answer needs something only the account owner knows, ask the person.
- Leave contacts who opted out alone: the contact shows it, and sending is refused with `opted_out`.

## 3. Show and get approval

Show each draft with the contact, the channel, and whether the window is open. The person approves, edits or drops each one. Nothing is sent before they approve it.

## 4. Send

- `send_dm` with the conversation id and the approved text.
- An AI draft the person approves: `send_dm` with its `draftId`. To send it edited, pass the edited `text` together with the `draftId`. Dropping an AI draft is done in the dashboard inbox (https://uplika.com/dashboard/inbox); no tool does it.
- A conversation whose window has `mode` `public_reply` (a mention thread on Threads, or a comment thread) has no messaging window: `send_dm` there posts a public reply, not a private message. Say so when you show the draft. Threads has no direct messages (`faq:threads-no-dm`).
- Sending as the person pauses the account's automations in that conversation for a while (the `send_dm` description says how long). Tell the person if an automation was answering there.

## The messaging window

Meta lets the account message a contact only inside the messaging window that opens when the contact writes (`faq:dm-24h-window`). Outside it `send_dm` is refused with `window_closed`, and nothing can be sent until the contact writes again. Say that plainly, keep the approved draft for when they do, and do not suggest a way around it.

When an AI automation wrote a reply while the window was closed, Uplika kept it as a draft waiting for approval instead of sending it. Sending that draft is still a message, so it also needs the window to be open again.

## Held replies on Threads

If the person uses Threads reply approval, replies to their Threads posts wait in a queue until approved. `approve_reply` with the account id and no reply id lists the queue. With a reply id it approves that reply, which makes it public, or ignores it with `approve: false`. Show each held reply and act only on the person's decision. Working through the replies under posts in general is the `comments` skill.

## Errors

- `reconsent_required`: the account was connected without the messaging permissions, or (on a mention list, as a `notice`) without the mentions permission. Reconnecting the account adds it; the `troubleshoot` skill walks the person through it (`faq:dm-reconnect`).
- `feature_in_review`: the permission is still in the platform's review and reconnecting does not help yet. The `troubleshoot` skill explains.
- `account_disconnected`: the `troubleshoot` skill.
- Anything else: call `get_help` with the code and pass its answer and url on.

## Tools

- `list_accounts`: which accounts are connected, before reading the inbox
- `list_conversations`: the inbox list, with the window state of each conversation
- `read_conversation`: one conversation, its contact and any AI drafts waiting for approval
- `get_contact`: one contact's details and when their window closes
- `send_dm`: send an approved message, or an approved AI draft with draftId
- `approve_reply`: Threads only: list held replies, then approve or ignore one after the person decides
- `get_help`: the answer for an error code
