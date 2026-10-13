---
name: setup
description: "Check that Uplika is connected: list accounts, send the person to connect channels, check the Naver extension. Use first in a new session."
---

# Setup

Use this at the start of a session, when the person asks whether Uplika is connected, or when any other skill finds no accounts.

## Procedure

1. Call `list_accounts`. Sign-in differs by agent. In Claude Code the plugin's tools stay hidden until the server is authorized: Claude Code marks the server as needing authentication and offers an `authenticate` tool for it. Call that tool (or ask the person to run `/mcp` and pick Authenticate), give the person the URL it returns, and when they approve in the browser the real tools appear in the same session without a restart. If the browser could not reach the localhost callback, ask for the full callback URL and pass it to `complete_authentication`. In Codex and Hermes the first tool call opens the approval screen; in OpenClaw it opens at `openclaw mcp login uplika`. Tell the person to sign in (or sign up), pick the workspace and the channels, and press Allow. Then call `list_accounts` again.
2. If the answer is `workspace_required`, the account has more than one workspace. Show the names it lists, ask which one, and pass that `workspaceId` on every later call in this session.
3. If the list is empty, no channel is connected in that workspace. Send the person to https://uplika.com/dashboard/connections, wait until they say it is done, then call `list_accounts` again.
4. Show what is connected: channel, handle, status. Only `active` accounts publish. For any other status (expired, revoked) say which account and send them to the same connections page to reconnect.
5. If a Naver Blog account is connected, call `bridge_status`. Naver Blog posts are written by the Uplika extension in the person's own Chrome. If it is offline, say that posts will wait in the queue until that Chrome is open, and show the `wake` command from the response for their system only if they want to run it.
6. When the person asks what a channel can do, call `list_platforms` and read its features table and rules. Do not answer from memory.

## Installed twice

A server the person added earlier by hand needs nothing done. Claude Code hides the plugin's copy of a server it already has (`claude mcp list` then shows only the old `uplika`), and Codex merges entries with the same name. Leave it: removing it only means approving once more.

The tools do show up twice when Uplika arrives two other ways, for example the claude.ai connector (`claude.ai uplika`) next to this plugin, or a hand-added server under another name. Then ask the person to turn one off in `/mcp`, or to remove the extra entry by its name:

- Claude Code: `claude mcp remove <name>`
- Codex: `codex mcp remove <name>`

## When something fails

Call `get_help` with the error code and pass its answer and link on. `reconsent_required`, `feature_in_review` and `account_disconnected` go to the `troubleshoot` skill.

## Tools

- `list_accounts`: what is connected, and the call to make first (in Claude Code only after the server is authorized)
- `bridge_status`: whether the Naver Blog extension is online
- `list_platforms`: channel rules, status and the features table
- `get_help`: the answer for an error code
