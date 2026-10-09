---
name: schedule-week
description: Plan a week of posts across your channels and schedule them in one pass; everything is shown for approval before anything is scheduled.
---

# Schedule a week

Use this for "plan next week's posts", "fill my content calendar", "schedule this week across my channels". It plans the week, writes every post the way that channel's skill writes it, shows the whole week for approval, then schedules all of it in one pass. Uplika's server holds each post and sends it at its time.

## 1. Channels, dates and time zone

1. Call `select_channels` with no scope to get the connected candidates and let the person choose (or `all`). Never assume a channel is connected; if nothing comes back, send them to https://uplika.com/dashboard/connections. Read out `skipped` (expired or not-yet-live channels, with the sentence and reconnect link it gives). If it answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId` on every later call.
2. Ask which time zone the times are in, and use the one the person states. Do not guess it from their language, their location or this machine.
3. Turn "next week" into real dates in that time zone and say them back.
4. Ask what the week should hold: topics or content pillars, source material, dates that matter (a launch, an event), how often each channel should post, and preferred times. If they have no times in mind, do not invent "best times": suggest times from their own past results (the `performance-review` skill reads them) and say that is where the suggestion came from. With no results to go on, say so and let them pick.

## 2. The plan table

Before writing any post, show a table with a row per day and a column per chosen channel. Each cell holds the topic, the format (single post, chain, carousel, reel, story, video, blog post) and the time, or stays empty.

- Read each channel's rules from `list_platforms` (limits, whether media is required, and the features table) so the plan only holds formats that channel takes. Do not plan from memory.
- Spread the formats. Do not stack the heavy pieces (a video, a blog post, a long chain) on one day, and space posts on the same account apart instead of sending several at the same minute.
- Leave a slot open for something timely if the person wants one.

Get the person's approval of the plan, or their changes, before writing.

## 3. Write each post the way its channel skill does

Read `~/.uplika/<workspace-slug>/voice.md` first if it exists. If not, ask three questions (tone, how posts end, words to avoid) and offer to save the answers with the `voice-profile` skill. Openings come from the `hooks` skill; vary the formula across the week.

| Channel | Write it the way this skill does | Always ask |
|---|---|---|
| Threads | `threads` | One post or a chain (`threadItems`) when the text is long |
| Naver Blog | `naver-post` | The form (`options.naver_blog.form`, or `options.naver_blog.layout` set to `as-is` when the person laid it out) and the category. Uplika never picks them |
| YouTube | `yt-upload` | The title (`options.youtube.title`) and whether it is made for kids (`options.youtube.madeForKids`) |
| TikTok | the publish skill's `references/tiktok.md` | The privacy level: call `get_publish_options` for that account and let the person pick one of the levels it returns (`options.tiktok.privacyLevel` has no default) |
| Any other channel | the publish skill's `references/<channel>.md` | What that file lists under "Always ask" |

Media: get media ids with the publish skill's media steps, right before the scheduling pass. A media id that no post holds yet expires (the upload's `mediaExpiresAt` says when); media held by a scheduled post is kept for it.

## 4. Show the whole week and get approval

Show every post in full, in date order: date and time with the time zone, channel and handle, the full text (every piece of a chain), the media, and the channel settings (title, privacy, form, category). Ask for approval of the whole week or for edits. Re-show what changed and ask again. Nothing is scheduled until the person approves.

## 5. Schedule in one pass

1. If the week has a Naver Blog post, call `bridge_status` first. Tell the person that Chrome with the Uplika extension has to be on and the computer awake at each Naver post's time, or that post goes out the next time Chrome opens (`faq:naver-schedule-chrome`). If it is not online now, relay its `userMessage`.
2. Call `publish` once per row, one after another, without asking again: the approval covered them. Pass `accountIds`, `content` (or `threadItems` for a chain), `mediaIds`, `options`, `scheduledAt`, and `workspaceId` when the person has more than one workspace. A row that sends the same post to several channels at the same time can be one call with all their `accountIds`.
3. `scheduledAt` is ISO 8601 with the offset of the person's time zone on that date. Work the offset out for each date, because it changes in a week when the clocks go forward or back. A time too soon or too far ahead is refused with `scheduled_at_range`, and its message says the allowed range.
4. Use `scheduledAt` on the post for every channel. The channels' own scheduling fields (`options.youtube.publishAt`, `options.facebook.scheduledPublishTime`, `options.naver_blog.scheduledAt`) are not needed for this.
5. Do not pass `automation` with a scheduled post: it is not attached. A comment automation for a scheduled post is set up with the `automations` skill after the post is live.
6. Keep each returned post id next to its row, and relay any `note` in the response (a Naver post carries one about Chrome).
7. If a call fails, finish the rest, then report the failed rows with the answer `get_help` gives for their code. Resume only rows that have no post id yet. `duplicate_post` means the same post is already queued for that account (the response names it): do not send a second copy. Do not change an approved text or time on your own to get past an error; ask the person.

## 6. Compare with what is scheduled

Call `list_posts` with status `scheduled`, `since` and `until` covering the week, and sort `scheduled` (soonest first). Compare it row by row with the approved week: time, channel, text, media. Report it as a table with each post id. If something differs or is missing, show it and fix only what the person confirms:

- `update_post` changes the text, media, settings or time of a scheduled post. Options you pass replace the whole options object, so send all of them. For a chain, pass the id of its first piece.
- `delete_post` cancels a scheduled post. Nothing is on any channel yet, so this only drops it from the schedule.

## During and after the week

- Moving or cancelling a post later works the same way: `update_post` or `delete_post`, after the person confirms.
- `list_posts` shows what went out (published, partial, failed). A failed target goes to the `troubleshoot` skill.
- At the end of the week, the `performance-review` skill reads how the posts did.

## Errors

- `workspace_required`: show the workspaces, ask which one, pass `workspaceId`.
- `feature_in_review`, `reconsent_required`, `account_disconnected`: the `troubleshoot` skill.
- Anything else: call `get_help` with the code and pass its answer and url on.

## Tools

- `select_channels`: the connected candidates, the chosen accountIds, skipped channels, the tightest limits and the Naver extension state
- `list_platforms`: each channel's rules and features table, read while planning
- `get_publish_options`: TikTok only, before every TikTok post, for the privacy levels to offer
- `bridge_status`: the Naver Blog extension before scheduling Naver posts
- `publish`: schedule each approved post with scheduledAt
- `list_posts`: compare what is scheduled with the approved week
- `update_post`: change or move a scheduled post after the person confirms
- `delete_post`: cancel a scheduled post after the person confirms
- `get_help`: the answer for an error code
