---
name: troubleshoot
description: "When something did not work: read the error code, call get_help, then retry, refresh the account, wake the Naver extension or ask to reconnect."
---

# Troubleshoot

Use this when a call fails, a post is stuck, an automation did not react, a DM did not arrive, or the person asks why something happened.

## Procedure

1. Read the error code from the response (`error.code`), or the target's reason from `get_post`.
2. Call `get_help` with that `code` (or a short `query` in any language, and `platform` when it is one channel). Use `locale` for the person's language. Give them the answer's steps and its link.
3. Act on it with the table below. Never repeat the same failing call more than once without changing something.

## By code

| Code | What it means | What to do |
|---|---|---|
| `reconsent_required` | The connected account is missing a permission this action needs (`faq:dm-reconnect`) | Send the person to https://uplika.com/dashboard/connections to reconnect that account, then try again |
| `feature_in_review` | The permission is still in the platform's review (`faq:feature-in-review`) | Reconnecting does not help until the review passes. Say so and stop |
| `account_disconnected` | The post's account was disconnected (`faq:disconnected-posts`) | Reconnect the same account; the post comes back with it |
| `workspace_required` | The account has more than one workspace (`faq:workspace-required`) | Show the listed workspaces, ask which, pass `workspaceId` |
| `research_tool_disabled` | A research tool still in beta is turned off for agents (released tools never answer this) | Ask the person once to turn it on at the link in the error, and do not retry until they say it is on |
| `window_closed` | A DM outside the messaging window (`faq:dm-24h-window`) | Nothing can be sent until the person writes again |
| `naver_rate_limited` | Naver capped posts for that ID | Wait `retryAfterSeconds`; the draft is already in Naver, do not send again |
| `bridge_offline` | The Chrome running the Uplika extension is not connected right now (`faq:naver-extension-offline`) | Call `bridge_status` and follow its `nextStep` (see Naver Blog extension below). Naver posts wait in the queue (the FAQ says for how long), so do not publish again |
| a target still publishing | The post is still going out (`faq:publish-still-publishing`) | Check `get_post` later; do not publish again |
| a failed target | The channel refused it | Fix the cause the reason names, then `retry_post` |

## Naver Blog extension

Naver Blog posts are written by the Uplika extension in the person's Chrome (`faq:naver-extension-offline`). Call `bridge_status`. When a response carries `bridge.nextStep`:

- `run_wake`: Chrome with the extension is closed. Show the person `bridge.userMessage` and the `wake` command for their system. With a terminal on the same computer you may offer to run it, but ask first. Retry once after they say Chrome is open.
- `ask_user_login`, `ask_user_update`: tell the person `bridge.userMessage`.

A Naver category the person names but `list_accounts` does not show: `refresh_account` re-reads the blog's categories.

## Tools

- `get_help`: the answer, steps and link for a code or question
- `get_post`: per-channel status and the reason a target failed
- `retry_post`: retry failed targets after the cause is fixed
- `refresh_account`: re-read a Naver Blog account's categories
- `list_accounts`: confirm the categories (and accounts) after a refresh
- `bridge_status`: whether the Naver Blog extension is online, and the wake commands
