---
name: setup
description: "Check that Uplika is connected: list accounts, send the person to connect channels, check the Naver extension. Use first in a new session."
---

# Setup

Use this at the start of a session, when the person asks whether Uplika is connected, or when any other skill finds no accounts.

## Procedure

1. Call `list_accounts`. This first call is also what starts sign-in: if the agent is not authorized yet, it opens the Uplika approval screen in the person's browser. Tell them to sign in (or sign up), pick the workspace and the channels, and press Allow. Then call `list_accounts` again.
2. If the answer is `workspace_required`, the account has more than one workspace. Show the names it lists, ask which one, and pass that `workspaceId` on every later call in this session.
3. If the list is empty, no channel is connected in that workspace. Send the person to https://uplika.com/dashboard/connections, wait until they say it is done, then call `list_accounts` again.
4. Show what is connected: channel, handle, status. Only `active` accounts publish. For any other status (expired, revoked) say which account and send them to the same connections page to reconnect.
5. If a Naver Blog account is connected, call `bridge_status`. Naver Blog posts are written by the Uplika extension in the person's own Chrome. If it is offline, say that posts will wait in the queue until that Chrome is open, and show the `wake` command from the response for their system only if they want to run it.
6. When the person asks what a channel can do, call `list_platforms` and read its features table and rules. Do not answer from memory.

## Installed twice

If the person added Uplika earlier as a plain MCP server, the tools now show up twice (once from that server, once from this plugin). Ask them to remove the old entry, then reload:

- Claude Code: `claude mcp remove uplika`
- Codex: `codex mcp remove uplika`

## When something fails

Call `get_help` with the error code and pass its answer and link on. `reconsent_required`, `feature_in_review` and `account_disconnected` go to the `troubleshoot` skill.

## Tools

- `list_accounts`: what is connected, and the first call that triggers sign-in
- `bridge_status`: whether the Naver Blog extension is online
- `list_platforms`: channel rules, status and the features table
- `get_help`: the answer for an error code
