# Uplika agent plugin

Publish, schedule and manage posts on the social channels you connect to [Uplika](https://uplika.com), right from your AI agent. The plugin bundles the Uplika MCP server (`https://api.uplika.com/mcp`, OAuth, nothing to paste) with skills that know the order to call the tools in: check what is connected, read each channel's limits, fit the media, show you the post, publish only after you approve, and report the links. It also covers comments, direct-message automations, weekly performance reviews, Naver Blog keyword research and YouTube scripting.

## Install

| Agent | Run |
|---|---|
| Claude Code | `claude plugin marketplace add uplika/uplika-plugin` then `claude plugin install uplika@uplika --scope user` |
| Codex | `codex plugin marketplace add uplika/uplika-plugin` then `codex plugin add uplika@uplika` |
| OpenClaw | `openclaw plugins install git:github.com/uplika/uplika-plugin@main` |
| Hermes | `hermes skills tap add uplika/uplika-plugin`, `hermes mcp add uplika` (URL `https://api.uplika.com/mcp`, auth oauth), `hermes mcp login uplika` |

Or tell your agent: `Read https://github.com/uplika/uplika-plugin/blob/main/INSTALL_FOR_AGENTS.md and follow it.`

The first tool call opens the Uplika approval screen in your browser. Connect your channels at <https://uplika.com/dashboard/connections>.

If you added Uplika earlier with `claude mcp add` or `codex mcp add`, remove that entry (`claude mcp remove uplika` or `codex mcp remove uplika`) so the tools do not show up twice.

## Skills only

`npx skills add uplika/uplika-plugin` installs just the skills. Add the MCP server address `https://api.uplika.com/mcp` to your agent's settings yourself.

## License and sources

MIT. Some skills are adapted from MIT-licensed projects; each names its source in its first line and the license texts are in `THIRD_PARTY_LICENSES/`. This repository is a copy of the `plugin/` folder in Uplika's own codebase, where the skills are tested against the server's tool names and options. Please open issues here; changes are made upstream and copied over.
