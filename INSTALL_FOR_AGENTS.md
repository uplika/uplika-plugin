# Install Uplika (for AI agents)

You are an AI coding agent. Decide which agent you are running in, then follow only that section. Run the commands yourself; ask the person only when a step needs their browser.

The Uplika MCP server is `https://api.uplika.com/mcp`. It uses OAuth with dynamic client registration, so there is no key to paste. The browser approval screen opens the first time a tool is called (Claude Code, Codex) or when you run the login command (OpenClaw, Hermes). Tell the person to approve it and pick the channels to publish to.

## Claude Code

1. `claude plugin marketplace add uplika/uplika-plugin`
2. `claude plugin install uplika@uplika --scope user`
3. If `claude mcp list` shows a plain `uplika` server from an earlier `claude mcp add`, run `claude mcp remove uplika` so the tools do not appear twice.
4. Ask the person to reload plugins or restart the session.
5. Verify: call `list_accounts`; it answers with the connected accounts.

## Codex

1. `codex plugin marketplace add uplika/uplika-plugin`
2. `codex plugin add uplika@uplika`
3. If uplika was added earlier with `codex mcp add`, run `codex mcp remove uplika`.
4. Ask the person to start a new session.
5. Verify: call `list_accounts`; it answers with the connected accounts.

## OpenClaw

1. `openclaw plugins install git:github.com/uplika/uplika-plugin@main`
2. If the uplika MCP server did not come with the plugin: `openclaw mcp set uplika '{"url":"https://api.uplika.com/mcp","transport":"streamable-http","auth":"oauth"}'`
3. `openclaw mcp login uplika`
4. Verify: call `list_accounts`; it answers with the connected accounts.

## Hermes

1. `hermes skills tap add uplika/uplika-plugin`
2. `hermes mcp add uplika` with URL `https://api.uplika.com/mcp` and auth `oauth`
3. `hermes mcp login uplika`
4. `/reload-mcp`
5. Verify: call `list_accounts`; it answers with the connected accounts.

## Other agents

1. `npx skills add uplika/uplika-plugin -g` (skills only)
2. Add the MCP server `https://api.uplika.com/mcp` (streamable HTTP, OAuth) in your own settings.
3. Verify: call `list_accounts`; it answers with the connected accounts.

## After installing

- No channels yet: send the person to <https://uplika.com/dashboard/connections>.
- `workspace_required`: show the choices it lists and pass `workspaceId` on later calls.
- Anything else that fails: call `get_help` with the error code and pass its answer and link on.
