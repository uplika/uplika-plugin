# Uplika agent plugin

Publish, schedule and manage posts on the social channels you connect to [Uplika](https://uplika.com), right from your AI agent. The plugin bundles the Uplika MCP server (`https://api.uplika.com/mcp`, OAuth, nothing to paste) with skills that know the order to call the tools in: check what is connected, read each channel's limits, fit the media, show you the post, publish only after you approve, and report the links. It also covers comments, direct-message automations, weekly performance reviews, Naver Blog keyword research and YouTube scripting.

## Install

| Agent | Run |
|---|---|
| Claude Code | `claude plugin marketplace add uplika/uplika-plugin` then `claude plugin install uplika@uplika --scope user` |
| Codex | `codex plugin marketplace add uplika/uplika-plugin` then `codex plugin add uplika@uplika` |
| OpenClaw | `openclaw plugins install uplika --marketplace uplika/uplika-plugin --force --accept-capabilities`, then `openclaw mcp set uplika '{"url":"https://api.uplika.com/mcp","transport":"streamable-http","auth":"oauth"}'` and `openclaw mcp login uplika` |
| Hermes | `npx skills add uplika/uplika-plugin -g -a hermes-agent -s '*' -y`, then in your terminal `hermes mcp add uplika --url https://api.uplika.com/mcp --auth oauth` (answer y) |

Or tell your agent: `Read https://github.com/uplika/uplika-plugin/blob/main/INSTALL_FOR_AGENTS.md and follow it.`

The first tool call opens the Uplika approval screen in your browser (OpenClaw opens it at `openclaw mcp login`). Connect your channels at <https://uplika.com/dashboard/connections>.

If you added Uplika earlier with `claude mcp add` or `codex mcp add uplika`, you can keep it: Claude Code hides the plugin's copy of a server you already have, and Codex merges entries with the same name. If the Uplika tools still show up twice (for example a claude.ai connector next to the plugin), turn one off in `/mcp`.

## What it sends and runs

- **One MCP server.** The plugin declares a single MCP server, `https://api.uplika.com/mcp`, run by Uplika. You sign in with OAuth in your browser and choose which channels the agent may use.
- **What goes to Uplika.** When you ask the agent to act, the request goes to that server: post text, media links, channel options, and the reply or DM text you approve. Uplika publishes it to the channels you connected and reads back your own posts, replies, messages and metrics. Uplika keeps your connected accounts and post history as described in the [privacy policy](https://uplika.com/en/privacy).
- **Media files.** To upload a file from your computer, an agent with a shell sends it to Uplika's media storage on Backblaze B2 through a one-hour signed link the server returns. An agent without a shell gives you an upload page on uplika.com instead.
- **Nothing goes out without your approval.** The skills show you the text, the channels and the time, and publish, reply, send or turn on an automation only after you say yes.
- **Local scripts.** A few YouTube and Instagram skills include small Python scripts (standard library only) that score hooks, titles and captions or read a transcript or analytics CSV you provide. They make no network calls.
- **Public YouTube data.** When a shell is available, some YouTube skills suggest `yt-dlp` or downloading thumbnail images to read public video data from YouTube. Your data is not sent there.
- **On your own disk.** The voice skill keeps your writing style in `~/.uplika/<workspace-slug>/voice.md`.

## Skills only

`npx skills add uplika/uplika-plugin` installs just the skills. Add the MCP server address `https://api.uplika.com/mcp` to your agent's settings yourself.

## License and sources

MIT. Some skills are adapted from MIT-licensed projects; each names its source in its first line and the license texts are in `THIRD_PARTY_LICENSES/`. This repository is a copy of the `plugin/` folder in Uplika's own codebase, where the skills are tested against the server's tool names and options. Please open issues here; changes are made upstream and copied over.
