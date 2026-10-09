---
name: naver-ai-cite
description: Write or rework a Naver Blog post so AI Briefing is likely to cite it, per Naver's official guide. Asks for real experience. AI 브리핑 인용, 네이버 메이트.
---

# Naver AI Briefing citation

Write a new Naver Blog post, or rework an old one, along the lines Naver Search published for content that its AI Briefing (AI 브리핑) cites. Naver decides what gets cited. This skill makes a post meet Naver's stated criteria and says plainly where it does not; it never promises a citation.

Sources, all on Naver Search's official blog:

- Content guide (2026-05-26): https://blog.naver.com/naver_search/224296857688 (five principles, five things to avoid, FAQ)
- Practical guide (2026-06-04): https://blog.naver.com/naver_search/224305800678 (five self-checks, good and bad examples)
- Background (2026-05-28): https://blog.naver.com/naver_search/224290490478 (Naver Mate, 네이버 메이트: creators are picked every month by topic, mainly on how often their content is cited in AI Briefing)

Open `references/official-guide.md` before checking a draft: it has Naver's item titles in Korean, Naver's own check questions, and a line on each.

## Two layers, three results

- **Official, 15 items:** the five principles, the five self-checks and the five things to avoid, from the two guides.
- **Common practice, 3 items, not in Naver's text:** the conclusion in the first paragraph, question-style subheadings, and a short FAQ at the end. Recommend them, and label each one "not in Naver's text" wherever you show it. Naver's own guide ends with an FAQ, but none of its criteria asks a post to have one.

Every item gets exactly one result:

- **pass**: quote the line of the draft that earns it.
- **gap**: say what is missing and what would close it.
- **n/a**: the item does not apply to this post, with the reason.

Never add the results up or turn them into a number, a percentage, a grade or a rating. Naver publishes no such measure, and a made-up one would mislead the person.

## Procedure

1. **Voice.** Read `~/.uplika/<workspace-slug>/voice.md` if it exists. If not, ask three questions (tone, ending style such as 해요체 or 합니다체, words to avoid) and offer to save the answers with the `voice-profile` skill.
2. **Material first.** Before writing anything, ask for what only the person has. Naver's guide says this is what makes content worth citing, and that text an AI produced without a person's experience and final edit is what gets filtered out. Ask for:
   - Real experience: what they did themselves, when, where, for how long, in what situation.
   - Numbers they measured or paid: prices, times, distances, counts, before and after.
   - Alternatives they compared, and why they chose what they chose.
   - Trial and error: what went wrong, what surprised them, what they would do differently.
   - Sources: statistics, studies or official documents they relied on, with links.
   - Sponsorship: whether anything was paid for, provided or sponsored (원고료, 협찬, 업체 지원), or bought with their own money (내돈내산).
   - Photos and videos they took that belong in the post.

   Whatever they cannot give stays empty and becomes a gap. Never invent experience, numbers, comparisons, sources or a sponsorship status, and do not paper over a gap with vague sentences.
3. **Keyword set.** For a search post, take the set from the `naver-keywords` skill, or a saved report from `list_naver_keyword_reports`. Its `draftPrompt` decides where the keywords go; the structure below decides what each section holds.
4. **Topic consistency.** Call `diagnose_naver_blog` with the person's blog. Its categories and posts per month show what the blog is mostly about. If this post's topic sits outside the blog's core, mark principle 2 (일관된 주제) as a gap and say why: one post cannot fix it, steady posting on the core topic does.
5. **Structure.** Build the post in this order, which follows the self-checks:
   1. Reader and situation in one line: who it is for, in what situation (TPO), for what purpose.
   2. The procedure in the order it happened, with the measured numbers and the tips only someone who did it knows.
   3. The alternatives they compared, as a table of choices by situation (예: 커플에게는 A, 가족 여행엔 B), with the deciding reason.
   4. The results, including what fell short and the trial and error.
   5. Evidence: links to the sources they relied on, with the author named.
   6. Sponsorship or 내돈내산, stated where a reader sees it at once.
   7. For every photo or video, its key point written in the text as well.

   Use headings, short paragraphs and tables so a reader finds the key information fast. If the person agrees to the three common practices, the opening also states the conclusion next to the reader line, subheadings are phrased as the reader's questions, and a short FAQ closes the post.
6. **Filter.** Before showing the draft, remove the five things to avoid: copied or stitched-together content and unedited AI text, heavy ads and promotional outbound links, keywords that do not fit the context, images and videos unrelated to the text, and unverified or inaccurate information.
7. **Check.** Run the 15 official items and the 3 practices against the draft and show one table: item, result (pass, gap or n/a), and the quoted line or what is missing. Self-check by quoting: a pass you cannot back with a quote from the draft is a gap.
8. **Hand off.** Give the draft, the checklist and the photos to the `naver-post` skill, which picks the form and category with the person, previews, checks the extension and publishes after approval. A comparison-led post suits a form meant for comparisons (such as `table-explain`) and a step-by-step one a walkthrough form (such as `divider-tutorial`), but the person decides. A form changes the layout, never the text, so the structure above survives either way.

## Refresh an old post

Principle 5 (최신성 유지) asks that posts be updated when their information changes. Uplika rewrites a published Naver post in place, at the same URL.

1. Find candidates with `list_channel_posts` on the Naver account: posts whose prices, dates, versions or availability have likely changed. Read one with `open_post` and its permalink.
2. Ask the person what changed. Their update is the only source for new facts.
3. Call `bridge_status`: the extension in their Chrome reads the post from Naver and does the rewrite. If `state` is not `online`, relay `userMessage` word for word and wait until the person says Chrome is open before calling `update_post`.
4. Draft the new version and run the checklist on it. Show the person what will change (old lines and new lines) and send it only after they approve.
5. Call `update_post` with the post's link or id, the new `content` and `wait: true` (editing a live post is asynchronous; if the wait runs out, read the result with `get_post`).
   - A post written in Naver's editor: the first call answers `naver_source_required` with the post's current `source` and its `sourceVersion`. Make the edit on that source. Keep every `@keep(...)` line for blocks you are not rewriting (photos, videos, cards, tables, styled text); deleting such a line removes that block. Send the edited source as `content` together with `sourceVersion`.
   - If it answers `naver_source_required` again, the post changed on Naver after you read it: start over from the new `source`, never send the older copy.
   - A post published through Uplika: send the whole new body. Its `media:` references are the post's photo list, so keep every photo line that should stay; a photo the new body no longer places is removed from the post.

## When something fails

- `research_tool_disabled` (from `diagnose_naver_blog` or `list_naver_keyword_reports`): ask the person once to open the link in the error and turn keyword research on for MCP connectors, and do not retry until they say it is on. Meanwhile mark principle 2 as a gap with the reason "blog not diagnosed".
- `naver_keep_unknown`: a `@keep` id that is not in the post's current source. Use the ids from the source.
- `naver_rate_limited`: do not call again before `retryAfterSeconds`.
- `extension_outdated`: the extension in that Chrome is too old for source edits; relay the message with `faq:extension-not-updating`.
- `post_not_editable`: Uplika could not turn this post into a source it can rewrite without losing parts of it. The person edits it in Naver's editor.
- `workspace_required`: show the workspaces it lists, ask which one, and pass `workspaceId`.
- `account_disconnected`: hand over to the `troubleshoot` skill.
- Anything else: call `get_help` with the error code and pass its answer and link on.

## Tools

- `diagnose_naver_blog`: the blog's categories and posts per month, for topic consistency
- `list_naver_keyword_reports`: a saved keyword set and its `draftPrompt`
- `list_channel_posts`: the blog's existing posts, to find ones worth refreshing
- `open_post`: read an old post before refreshing it
- `bridge_status`: whether the extension that rewrites the post is online
- `update_post`: rewrite a published post at the same URL (after approval)
- `get_post`: the result of an edit when the wait runs out
- `get_help`: the answer for an error code
