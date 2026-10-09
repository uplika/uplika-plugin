# Install Uplika (for AI agents)

You are an AI coding agent. Decide which agent you are running in, then follow only that section. Run the commands yourself; ask the person only when a step needs their browser.

The Uplika MCP server is `https://api.uplika.com/mcp`. It uses OAuth with dynamic client registration, so there is no key to paste. The browser approval screen opens the first time a tool is called (Claude Code, Codex, Hermes) or when you run the login command (OpenClaw). Tell the person to approve it and pick the channels to publish to.

## Claude Code

1. `claude plugin marketplace add uplika/uplika-plugin`
2. `claude plugin install uplika@uplika --scope user`
3. If `claude mcp list` still shows an `uplika` server added earlier with `claude mcp add`, leave it: Claude Code hides the plugin's copy of the same server. If Uplika shows up twice another way (for example a `claude.ai uplika` connector next to the plugin), ask the person to turn one off in `/mcp`.
4. Ask the person to reload plugins or restart the session.
5. Verify: call `list_accounts`; it answers with the connected accounts.

## Codex

1. `codex plugin marketplace add uplika/uplika-plugin`
2. `codex plugin add uplika@uplika`
3. An `uplika` server added earlier with `codex mcp add uplika` merges with the plugin's server of the same name; leave it. Only a second entry under another name doubles the tools; remove that one with `codex mcp remove <name>`.
4. Ask the person to start a new session.
5. Verify: call `list_accounts`; it answers with the connected accounts.

## OpenClaw

1. `openclaw plugins install uplika --marketplace uplika/uplika-plugin --force --accept-capabilities` (the source is outside ClawHub, so a shell without a terminal cancels the install unless these two flags are given)
2. `openclaw mcp set uplika '{"url":"https://api.uplika.com/mcp","transport":"streamable-http","auth":"oauth"}'` (the plugin brings the server too, but `openclaw mcp login` only signs in to servers set here; the same name replaces the plugin's copy)
3. `openclaw mcp login uplika` opens the approval screen. Wait for the person to approve it.
4. Verify: call `list_accounts`; it answers with the connected accounts.

## Hermes

1. `npx skills add uplika/uplika-plugin -g -a hermes-agent -s '*' -y` (installs the skills into `~/.hermes/skills`)
2. Ask the person to run `hermes mcp add uplika --url https://api.uplika.com/mcp --auth oauth` in their own terminal and answer `y`. It asks questions, and without a terminal it saves the server without sign-in.
3. Ask the person to start a new Hermes session.
4. Verify: call `list_accounts`. The first call opens the approval screen; after it is approved, it answers with the connected accounts.

## Other agents

1. `npx skills add uplika/uplika-plugin -g` (skills only)
2. Add the MCP server `https://api.uplika.com/mcp` (streamable HTTP, OAuth) in your own settings.
3. Verify: call `list_accounts`; it answers with the connected accounts.

## After installing

- No channels yet: send the person to <https://uplika.com/dashboard/connections>.
- `workspace_required`: show the choices it lists and pass `workspaceId` on later calls.
- Anything else that fails: call `get_help` with the error code and pass its answer and link on.
