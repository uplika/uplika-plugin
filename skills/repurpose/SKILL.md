---
name: repurpose
description: Turn one long piece into a Shorts script, a carousel, a Threads chain and a Naver post, then publish each after approval.
---

# Repurpose

Use this for "turn this video into posts", "repurpose my blog post", "make a carousel and a Threads chain from this". One long piece (a video, a blog post, a newsletter, a talk, a podcast) becomes four pieces, each written for its own channel: a Shorts script, a carousel, a Threads chain and a Naver Blog post. Each piece is shown and published on its own, after the person approves it. Ask which of the four they want; by default, all four.

Repurpose the person's own work, or material they have the right to reuse.

## 1. Get the whole source

- Pasted text or a transcript: use it as it is.
- A post on one of the person's connected channels (their Naver Blog post, YouTube video, Threads post): `open_post` with the link reads it. A YouTube video comes back as its title and description, not what is said in it.
- A video without a transcript: with a terminal, `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs <language code> <url>` saves the subtitles. Without one, ask the person to paste the transcript.

Read all of it before writing anything.

## 2. Pull out what stands alone

List what the piece actually contains: the main claim, the steps of any process, the numbers (and where they come from), the stories (who, what happened, what it cost), the mistakes admitted, and the lines worth quoting as they are. Show the list and which piece each item will feed. If the source is thin, say so rather than stretching it into four.

Every piece has to make sense to someone who never saw the original. Never write "as I said in the video".

## 3. Write the four pieces

Read `~/.uplika/<workspace-slug>/voice.md` first if it exists. If not, ask three questions (tone, how posts end, words to avoid) and offer to save the answers with the `voice-profile` skill. Write in the person's language. Openings come from the `hooks` skill; give each piece a different formula. Read each channel's limits from `list_platforms` (or the `limits` of `select_channels`) instead of guessing them.

### Shorts script

One item from the list, for a vertical video. Write the spoken lines and the on-screen text side by side, beat by beat: the hook first, the payoff before the end, one closing line. Note what is on screen for each beat. Uplika does not cut or edit video: the person records or cuts it, and the `yt-shorts` skill helps find moments in their own long video. When they have the file, publish it the way the `yt-upload` skill does (`options.youtube.title`, and made-for-kids asked every time).

### Carousel

One feed post with several images. A cover slide that carries the hook, one idea per slide, a last slide that sums up or asks for the one action, and a caption. Keep slide text short enough to read in one look.

- The images: the person makes them, or you do if this session can render images. Mark AI-made images with `aiGenerated`.
- Media ids in slide order: a public https file goes through `media_from_url` (Google Drive and Dropbox share links are preview pages, not files: ask for a direct file link). A file on the person's device goes through the publish skill's upload steps.
- Pass the ids in `mediaIds` in slide order and write `altText` for each slide you can see.
- On Instagram several images in a feed post make the carousel (`options.instagram.contentType` feed, the default for images). An image outside the shape Instagram keeps in the feed is cropped, not refused, and the result carries a warning: say so before publishing if the edges matter. How many images a channel takes in one post is in `list_platforms`.

### Threads chain

Follow the `threads` skill: the hook first, one point per piece, each piece readable on its own, the pieces in `threadItems` (the first one is the root). Check every piece against the Threads limit from `list_platforms`, counted the way its `charCount` says. A topic tag only if the person wants one (`options.threads.topicTag`). The last piece can point to the original if it is public.

### Naver Blog post

Write the body the way the `naver-post` skill does (grammar, photos placed in the body, the title in `options.naver_blog.title`, a category the person chooses). Then preview it: `naver_layout` with the body and the `mediaIds`. To let the person choose a form, call it with `forms` set to `all` and show the layouts side by side; publish with `options.naver_blog.form` set to the id they pick. If they laid the post out themselves, `options.naver_blog.layout` set to `as-is` publishes it unchanged. Never pick the form for them.

## 4. Publish, one channel at a time

For each piece, in the order the person wants:

1. Find the account with `select_channels`. Never assume it is connected; if it is not, send the person to https://uplika.com/dashboard/connections. If it answers `workspace_required`, show the workspaces, ask which one, and pass `workspaceId` on every call.
2. Show the piece exactly as it will go out: the text (every chain piece, every slide), the media, the channel and handle, and the time. Publish only after the person approves that piece. A piece they do not approve is not published.
3. Naver Blog: call `bridge_status` first. If it is not online, relay its `userMessage`: the post waits in the queue until Chrome with the extension is on. If `publish` answers `naver_rate_limited`, wait for its `retryAfterSeconds` before trying again; the draft is already in Naver.
4. Call `publish` with `accountIds`, `content` or `threadItems`, `mediaIds`, `options` and `wait: true`. To spread the pieces over several days instead, pass `scheduledAt` (ISO 8601 with the offset of the time zone the person states), or hand the set to the `schedule-week` skill.
5. Report each piece's status and permalink. If the wait ended before the post was out, `get_post` reads the final status; a wait that ends early is not a failure, so check before publishing again. If the response carries a `bridge` object, relay its `userMessage` and do not say the post is live.

## Errors

- `feature_in_review`, `reconsent_required`, `account_disconnected`: the `troubleshoot` skill.
- Anything else: call `get_help` with the code and pass its answer and url on.

## Tools

- `open_post`: read the source when it is a post on a connected channel
- `select_channels`: the account for each piece, and its limits
- `list_platforms`: each channel's limits and what it can do
- `media_from_url`: slide images and other media from a public https address
- `naver_layout`: preview the Naver Blog post and the forms to choose from
- `bridge_status`: the Naver Blog extension, before publishing there
- `publish`: publish or schedule each approved piece
- `get_post`: the final status and permalink of a piece
- `get_help`: the answer for an error code
