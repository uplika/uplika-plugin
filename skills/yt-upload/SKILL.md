---
name: yt-upload
description: "Upload a video to YouTube with the right options: title, description, tags, language, privacy, thumbnail; asks about made-for-kids."
---

# yt-upload

One video to the person's connected YouTube channel, with every option set on purpose. Use it whenever a video goes to YouTube through Uplika: a finished long video, a Short (`yt-shorts` sends the file here), or a slot from `yt-plan`. For the title and thumbnail use `yt-package` first; for the description and tags, `yt-seo`.

## Before you start

1. Read YouTube's rules from `list_platforms` (the YouTube entry), never from memory: the title limit and how it is counted, the description limit and how it is counted, the accepted video files, the `shorts` rule, and `options`, the schema of every `options.youtube` field. (Uplika's publish-options tool is for TikTok only; it does not apply to YouTube.)
2. Call `select_channels` with scope `youtube`. It returns the `accountIds` to pass to `publish`, and `skipped` with a sentence and a reconnect link when the connection has expired. Nothing connected: send the person to https://uplika.com/dashboard/connections.
3. If a call answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId` on every later call, `publish` included.
4. If a voice file exists at `~/.uplika/<workspace-slug>/voice.md`, write the title and description in that voice; if not, the `voice-profile` skill can create it.

## The options

The post's `content` is the video description. Everything else goes in `options.youtube`:

| Field | What to do |
|---|---|
| `options.youtube.title` | Required. Write it with `yt-package` if the person has none |
| `options.youtube.tags` | Search tags. The list has a total length limit (`list_platforms`). Tags barely matter; `yt-seo` says which are worth having |
| `options.youtube.categoryId` | Leave it out unless the person names a category |
| `options.youtube.defaultLanguage` | The language the title and description are written in, one BCP-47 code such as en-US or ko. Left out, none is sent |
| `options.youtube.privacyStatus` | public, unlisted or private. Ask. Left out, the video goes up private and the result says so |
| `options.youtube.madeForKids` | **Ask every time the person has not said** whether the video is made for kids, and send true or false only from their answer. Never send it on your own. If they will not say, leave it out: the channel's own default applies, and if the channel has none either, YouTube Studio will not save other edits to the video until someone picks an audience, so tell them |
| `options.youtube.containsSyntheticMedia` | true when the video has realistic altered or AI-generated people, places or events; ask when it might. A media id uploaded with `aiGenerated` turns it on unless you send false |
| `options.youtube.thumbnailMediaId` | A JPEG or PNG media id. Long-form only, and only on a verified channel: a Short takes no custom thumbnail (the `shorts` rule in `list_platforms`) |
| `options.youtube.publishAt` | YouTube's own release time: the video uploads now as private and YouTube makes it public then. Only with `options.youtube.privacyStatus` private, on a video that was never public |

## When it goes out

- `scheduledAt` on the post (ISO 8601 with a time zone offset): Uplika keeps the file and uploads it at that time, the way it schedules every channel. Use it when the video should go out together with posts on other channels.
- `options.youtube.publishAt`: the upload happens now and YouTube makes it public later, so the video is processed and can be checked in YouTube Studio before it goes live.
- Ask which time zone the person means; do not guess.

## The file

- With a shell (Claude Code, Codex, OpenClaw, Hermes) and a local file: `media_presign` with the file name, content type, size and `aiGenerated` when it applies; PUT the bytes to the returned `uploadUrl` with curl and the same content type; then `media_complete`.
- A file at a public https address: `media_from_url`. Google Drive and Dropbox share links are preview pages, not files; ask for a direct link.
- No shell and the file is on the person's device: `media_upload_link`, give them the link, and poll `media_upload_status` until it is ready.
- A thumbnail image goes through the same steps; its media id goes in `options.youtube.thumbnailMediaId`, not in `mediaIds`.
- `mediaIds` holds the one video file: a YouTube post carries no images.

## Confirm, then upload

1. Show the person everything that will go out: the channel and handle, the title, the full description, tags, language, privacy, the made-for-kids answer, the synthetic-media flag, the thumbnail, and when (now, `scheduledAt` or `publishAt`, with the time zone).
2. Upload only after they approve: `publish` with `accountIds`, `content`, `mediaIds`, `options`, and `wait: true`, plus `scheduledAt` for a later time. Before several uploads in a row, `get_quota` shows how much of today's allowance is already used.
3. A wait that runs out is not a failure: a video takes time. Check with `get_post` instead of uploading again.

## Report

Call `get_post` with the returned id: the status, the link and the warning. Read the warning out as it is: it says when YouTube applied a different privacy than you asked for, when the video went up private because no privacy was set, when a thumbnail could not be applied, and when the channel's audience is not set. Do not tell the person the video is public until the result says so.

## After it is up

`update_post` changes the title, description, tags, language, privacy (private to public, for example) or thumbnail of the same video, at the same link; pass `wait: true`. Always send `options.youtube.title` (on a video uploaded through Uplika, `options` replaces what Uplika has on record and YouTube needs a title) and the full current description as `content`, so an edit made in YouTube Studio is not overwritten. The file itself cannot be replaced (`youtube_video_not_replaceable`): a new cut is a new upload.

## When something fails

Call `get_help` with the error code and pass its answer and link on (for example `youtube_title_required`, `youtube_title_too_long` or `media_expired`). `account_disconnected` and `reconsent_required` go to the `troubleshoot` skill.

## Tools

- `list_platforms`: YouTube's rules and the `options.youtube` schema
- `select_channels`: the YouTube account to upload to
- `media_presign`: upload slot when you can PUT the file yourself
- `media_complete`: confirm that upload
- `media_from_url`: a video or thumbnail at a public https address
- `media_upload_link`: let the person upload from their device
- `media_upload_status`: wait until that upload is ready
- `publish`: upload the approved video, now or at `scheduledAt`
- `get_quota`: today's upload allowance before several uploads
- `get_post`: status, link and warnings
- `update_post`: change the title, description, tags, privacy or thumbnail afterwards
- `get_help`: the answer for an error code
