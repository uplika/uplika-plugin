---
name: threads
description: Write Threads posts and chains in your voice, add a topic tag, reply to comments, and learn from your real insights what works.
---

# Threads

Short posts and chains on Threads, written hook first, sent after approval, and improved from the account's own numbers.

## Before writing

1. Read `~/.uplika/<workspace-slug>/voice.md` if it exists. If not, ask three questions (tone, how posts end, words to avoid) and offer to save them with the `voice-profile` skill.
2. Find the Threads account with `select_channels` (scope `threads`). If it answers `workspace_required`, ask which workspace and pass `workspaceId`.
3. Read the limits from `select_channels` or `list_platforms`. Count characters the way `charCount` says.

## Writing

- **Hook first.** The first line is all most people see. Lead with the most specific thing: a number, a claim, a question, or the moment in a story. The `hooks` skill has formulas and Korean patterns.
- **One idea per post.** A second idea is a second post or the next piece of a chain.
- **Chains** for anything longer than one post: put the pieces in `threadItems` on `publish` (the first item is the root, the rest are replies under it in order). Each piece should stand on its own when someone lands on it.
- **Topic tag** only when the person wants one: `options.threads.topicTag`, one topic, no periods or ampersands. It goes on the first piece.
- **Check for machine-sounding text** before showing a draft, and rewrite when you find: the same bullet shape repeated, a summary sentence closing every paragraph, symmetrical "not X, but Y" contrasts, a philosophical closing line, and stacked connectors ("Moreover", "Additionally", "In addition").

## Sending

Show the full text (every chain piece), the account and the time. Publish only after the person approves: `publish` with `accountIds`, `threadItems` or `content`, `wait: true`; for later, `scheduledAt`. Then give them the permalink.

## Replies

- Read with `list_replies` on the post (or `open_post` from a link). Draft replies in the same voice, show them, send approved ones with `reply`.
- Mentions of the account come from `list_mentions` when the account holds that permission; if it answers `feature_in_review`, the permission is still in review and reconnecting does not help (the `troubleshoot` skill explains).
- Threads has no direct messages (`faq:threads-no-dm`). Liking and mentions depend on permissions shown in the features table of `list_platforms`; read it rather than promising.

## Weekly review

Call `list_channel_posts` for the account and `get_insights` per post. Compare each post to the account's own median, never to other channels. Name the patterns behind the top posts (hook type, length, chain or single, posting time) and suggest the next three posts from them. Nulls are not zeros.

## Tools

- `select_channels`: the Threads account and its limits
- `list_platforms`: rules and the features table
- `publish`: send or schedule a post or chain after approval
- `list_replies`: replies under a post
- `open_post`: a post from a link with replies and metrics
- `reply`: send an approved reply
- `list_mentions`: posts that mention the account
- `list_channel_posts`: the account's posts for the weekly review
- `get_insights`: per-post metrics
