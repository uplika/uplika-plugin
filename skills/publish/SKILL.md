---
name: publish
description: "Publish or schedule one post to several channels: pick channels, read limits, fit media, confirm with the person, publish, report permalinks."
---

# Publish

One post, one or more channels, now or at a set time. For YouTube uploads use `yt-upload`; for Naver Blog posts use `naver-post`; for a week of posts use `schedule-week`.

## Procedure

1. **Channels.** Call `select_channels`. With no scope it returns the candidates: show them and let the person choose. With what they named (platform names, handles or account ids, or `all`), it returns `accountIds` to pass to `publish` unchanged, plus `skipped` (expired or not-yet-live channels, with a sentence to read out and a reconnect link) and `limits`, the tightest rules across the chosen channels. If it answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId` on this and every later call.
2. **Rules.** Write to `limits` from `select_channels`. When you need one channel's rules or what it can do (media required, chains, comments, edits after publishing), read `list_platforms` and its features table. Never write a limit from memory.
3. **Channel settings.** Open `references/<channel>.md` only for the channels in this post (`threads`, `instagram`, `facebook`, `youtube`, `tiktok`, `telegram`, `bluesky`, `naver_blog`). They say which `options.<channel>.*` fields exist and which ones you must ask about.
4. **Text.** If a voice file exists at `~/.uplika/<workspace-slug>/voice.md`, read it first; if not, write plainly and offer the `voice-profile` skill afterwards. A channel can get its own text with `options.<channel>.content`. A long post on a channel that supports chains goes in `threadItems` (first item is the root).
5. **Media.**
   - With a terminal (Claude Code, Codex, OpenClaw, Hermes) and a local file: `media_presign` with the file name, type and size, PUT the bytes to the returned `uploadUrl` with curl, then `media_complete`.
   - Without a terminal (claude.ai, ChatGPT): a public https file goes through `media_from_url`; a file on the person's device goes through `media_upload_link` (give them the link, then poll `media_upload_status` until it is ready).
   - Write `altText` when you can see the image. Pass `aiGenerated` when the media was made with AI.
6. **Show and confirm.** Before anything goes out, show the person the exact text per channel, the media, the channels and handles, and the time (now, or `scheduledAt` with its time zone). Publish only after they approve. A post they want to finish themselves can be saved with `draft: true`.
7. **Publish.** Call `publish` with `accountIds`, `content`, `mediaIds`, `options`, and `wait: true` so the response tells you whether it is really out. For a later time pass `scheduledAt` (ISO 8601 with offset). TikTok needs `get_publish_options` first (see `references/tiktok.md`).
8. **Report.** Call `get_post` with the returned id and give the person each channel's status and permalink. A target that failed has a reason: read it out, call `get_help` with its code, and offer `retry_post` once the cause is fixed. A wait that times out is not a failure: the post is usually still going out, so check with `get_post` or `list_posts` instead of publishing again.

## Things to know

- A scheduled post is kept by Uplika and sent at that time on every channel. `publish_now` sends a scheduled or draft post immediately.
- To attach a comment-to-DM automation, the post must be live: for a scheduled post, create the automation after it goes out, with the `automations` skill and the published post id.
- Posts that already went out can be changed on some channels only: `update_post` refuses where the channel has no edit, and the features table says which.
- Deleting is `delete_post`, after the person confirms, on their own posts only.
- Naver Blog: call `bridge_status` first (the extension in their Chrome writes the post) and use `naver-post`.

## Tools

- `select_channels`: candidates, chosen accountIds, skipped channels, tightest limits
- `list_platforms`: per-channel rules and the features table
- `get_publish_options`: TikTok only, before every TikTok post
- `media_presign`: upload slot when you can PUT bytes yourself
- `media_complete`: confirm an upload from media_presign
- `media_from_url`: attach a public https image or video
- `media_upload_link`: let the person upload from their device
- `media_upload_status`: wait for that upload to be ready
- `publish`: send or schedule (needs approval first)
- `get_post`: status, reasons and permalinks per channel
- `list_posts`: check what went out or is scheduled
- `publish_now`: send a scheduled or draft post now
- `retry_post`: retry failed targets after the cause is fixed
- `update_post`: change a post where the channel allows edits
- `delete_post`: remove the person's own post after they confirm
- `bridge_status`: Naver Blog extension status
- `get_help`: the answer for an error code
