---
name: naver-post
description: Write and publish a Naver Blog post from a keyword set. Grammar, media refs, person-picked form and category, preview, extension check. 네이버 블로그 발행.
---

# Naver post

Write a Naver Blog post, usually from a keyword set, and publish it through the Uplika extension in the person's own Chrome. The person picks the post type, the form and the category; you write, place the photos, preview, and publish after they approve.

Use it for any Naver Blog post. For a post meant to be cited in Naver's AI Briefing, run `naver-ai-cite` first and come back here to publish. To publish a draft already sitting in Naver's draft box, use `naver-drafts`.

## Before writing

1. **Voice.** Read `~/.uplika/<workspace-slug>/voice.md` if it exists. If not, ask three questions (tone, ending style such as 해요체 or 합니다체, words to avoid) and offer to save the answers with the `voice-profile` skill.
2. **Account.** Call `select_channels` with scope `["naver_blog"]`. It returns the `accountIds` to publish to and a `bridge` object with the extension's state. If it answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId` on this and every later call. If no Naver Blog is connected, send the person to https://uplika.com/dashboard/connections.
3. **Post type.** Ask this before anything about the content, because it changes the title and the structure:
   - Search post (검색형): written to be found for a keyword. It needs a keyword set: get one with the `naver-keywords` skill, or pick a saved one from `list_naver_keyword_reports`.
   - Home feed post (홈피드형): written to be opened by people who see it in Naver's home feed or their neighbors' feed rather than search for it, so the title and the first photo have to make them open it. A keyword set is optional.
4. **Brief.** For a search post, use the set's `draftPrompt` as the brief, unchanged. It already carries the keyword placement, the number of sections and the length, so do not restate those numbers in your own words. The voice file decides tone and endings; the brief decides where the keywords go. If the saved set has only `prompt`, use it for the skeleton, or get a fresh set from `naver-keywords`.
5. **The gap.** If you can browse, open Naver's blog search results for the main keyword and skim the top posts; otherwise ask the person to paste a few top titles or links. Name one thing those posts leave out and give it one subheading of its own.

## Writing

6. **Grammar.** Before the first Naver body in a session, call `describe_grammar` with `platform: "naver_blog"` for the overview, and again with a `topic` (`media`, `blocks`, `highlight`, `limits` and so on) when you need more. What it returns is what `publish` accepts, including the mistakes that fail silently. Length and media limits come from `describe_grammar` (topic `limits`) and `list_platforms`; never write them from memory.
7. **Clean the draft.** The brief's output format has parts that do not belong in the body as they are:
   - The `#` title line: move it to `options.naver_blog.title`. The title is not part of the body.
   - Notes after subheadings such as `(서브: 키워드)`: delete them.
   - The tag line at the end: move the tags to `options.naver_blog.tags` (no `#`, no spaces).
   - Each photo spot `[사진: 무엇을 찍은 사진인지]` and the caption line under it: handled in the next step.
8. **Photos.** Never publish a `[사진: …]` line. For each spot, get the person's real photo, or remove the spot and its caption line. Do not invent photos they did not take. Show the person the list of spots so they know what to shoot or capture.
   - With a terminal (Claude Code, Codex, OpenClaw, Hermes): `media_presign` with the file name, type and size, PUT the bytes to the returned `uploadUrl` with curl, then `media_complete`.
   - Without one (claude.ai, ChatGPT): `media_from_url` for a file at a public https address, or `media_upload_link` for files on the person's device, then poll `media_upload_status` until it is ready. Ready photos come back as images you can look at, so you can match each one to its paragraph.
   - Place a photo on a line of its own as `![캡션](media:ID)`: the alt text becomes the photo's caption, so the brief's caption line goes there. A video is `@video(media:ID)` and photos side by side are `@group(media:A, media:B)`. Add `{.ai}` at the end of a photo or group line when the image was made or substantially changed with AI (or pass `aiGenerated` when uploading). Media referenced in the body does not need to be repeated in `mediaIds`; media passed in `mediaIds` but never referenced goes at the end of the post.
9. **Keywords.** Put the set's main keyword and subs in `options.naver_blog.seoKeywords`, so the post keeps a record of what it targets.
10. **Other settings.** Font, size, alignment and photo size are in the Naver options schema that `list_platforms` returns. Set them only when the person asks.

## Category, form, preview

11. **Category.** Read the blog's categories from `list_accounts` (`naverBlog.categories`) and let the person pick one. Pass it as `options.naver_blog.categoryId`, or by name as `options.naver_blog.category`. There is no default. If a category they just created is missing, call `refresh_account` for that account and read again.
12. **Form.** A Naver post goes out in a form (a house layout) unless it is kept exactly as written. If the person dictated the structure or wants the body exactly as written, set `options.naver_blog.layout` to `as-is`. Otherwise call `naver_layout` with the body, the media ids and `forms: "all"`: it lays the post out in every form side by side, each with its name, when to use it and a summary. Show them, let the person pick, and pass the id as `options.naver_blog.form`. Never pick for them. A form changes the layout, never the text.
13. **Preview.** Call `naver_layout` with the same content, media ids and the chosen form, and show the person the result.
14. **Extension.** Call `bridge_status`. The extension in the person's Chrome writes the post, so nothing goes out while that Chrome is closed. If `state` is not `online`, relay `userMessage` word for word and say the post will wait in the queue until that Chrome is open and logged in to Naver. With a terminal on the same computer, show the `wake` command for their system and run it only if they say yes; without one, ask them to open Chrome.

## Confirm and publish

15. **Confirm.** Show the person the title, the body as it will go out, the photos, the category, the form (or `as-is`), the tags, who can see it (`options.naver_blog.openType`, public unless they say otherwise) and the time (now, or `scheduledAt` with its time zone). Publish only after they approve.
16. **Publish.** Send Naver Blog in a `publish` call of its own, not mixed with other channels: media references would reach other channels as literal text, so the server refuses the mix. Pass `accountIds`, `content`, `mediaIds` if any, `options.naver_blog`, `workspaceId` when the person has more than one workspace, and `wait: true`.
   - Later: pass `scheduledAt` on the post (ISO 8601 with an offset; ask which time zone they mean). Chrome has to be on at that time (`faq:naver-schedule-chrome`).
   - For the person to finish by hand in Naver: set `options.naver_blog.draftOnly`. The `naver-drafts` skill publishes it later.
17. **Report.** If the response carries `bridge`, the post is queued: relay `bridge.userMessage` and do not say it was published. Otherwise call `get_post` with the returned id for the status and the permalink. A wait that runs out is not a failure (`faq:publish-still-publishing`): check with `get_post` instead of publishing again.

## When something fails

- `naver_form_required`: the response lists `forms` (id, name, when). Show them, let the person pick, and publish again with `options.naver_blog.form`.
- `naver_category_required` or `naver_category_unknown`: show the categories from `list_accounts` and let the person pick.
- `naver_media_kind_mismatch`: a video id sits on a photo line or the other way round; the error names the line and the line to write.
- `naver_rate_limited`: Naver capped how much this ID publishes. Do not call again before `retryAfterSeconds`; the draft is already in Naver.
- `extension_outdated`: the response carries the installed and required versions, and Uplika asks that Chrome to update at the same moment. Relay it with `faq:extension-not-updating` and try again after the person says it updated.
- Queued because the extension is offline: `faq:naver-extension-offline`.
- `research_tool_disabled` from `list_naver_keyword_reports`: ask the person once to turn keyword research on at the link in the error, and do not retry until they say it is on.
- `account_disconnected`: hand over to the `troubleshoot` skill.
- Anything else: call `get_help` with the error code and pass its answer and link on.

## Tools

- `select_channels`: the Naver Blog account to publish to, plus the extension state
- `list_naver_keyword_reports`: a saved keyword set and its `draftPrompt`
- `describe_grammar`: Naver body syntax, media lines and limits
- `list_platforms`: Naver limits and the options schema
- `media_presign`: upload slot when you can PUT bytes yourself
- `media_complete`: confirm an upload from media_presign
- `media_from_url`: attach a photo or video from a public https address
- `media_upload_link`: let the person upload from their device
- `media_upload_status`: wait for that upload and see the photos
- `list_accounts`: the blog's categories
- `refresh_account`: re-read categories the person just created
- `naver_layout`: forms side by side, and the preview of the chosen one
- `bridge_status`: whether the extension in the person's Chrome is online
- `publish`: send or schedule the post (needs approval first)
- `get_post`: final status and permalink
- `get_help`: the answer for an error code
