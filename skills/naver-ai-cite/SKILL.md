---
name: naver-ai-cite
description: Write or rework a Naver Blog post so AI Briefing is likely to cite it, per Naver's guide and Uplika's checks. AI 브리핑 인용, 네이버 메이트.
---

# Naver AI Briefing citation

Write a new Naver Blog post, or rework an old one, along the lines Naver Search published for content that its AI Briefing (AI 브리핑) cites, look at what AI Briefing shows for the keyword today, and check afterwards whether the post was cited. Naver decides what gets cited. This skill makes a post meet Naver's stated criteria and says plainly where it does not; it never promises a citation.

Sources, all on Naver Search's official blog:

- Content guide (2026-05-26): https://blog.naver.com/naver_search/224296857688 (five principles, five things to avoid, FAQ)
- Practical guide (2026-06-04): https://blog.naver.com/naver_search/224305800678 (five self-checks, good and bad examples)
- Background (2026-05-28): https://blog.naver.com/naver_search/224290490478 (Naver Mate, 네이버 메이트: creators are picked every month by topic, mainly on how often their content is cited in AI Briefing)

Open `references/official-guide.md` before checking a draft: it has Naver's item titles in Korean, Naver's own check questions, and a line on each.

## Three layers, three results

- **Official, 15 items:** the five principles, the five self-checks and the five things to avoid, from the two guides.
- **Common practice, 3 items, not in Naver's text:** the conclusion in the first paragraph, question-style subheadings, and a short FAQ at the end. Recommend them, and label each one "not in Naver's text" wherever you show it. Naver's own guide ends with an FAQ, but none of its criteria asks a post to have one. Uplika compared posts AI Briefing quoted with posts it did not: question-style subheadings and an FAQ made no difference, and an early conclusion helped only a little. Offer them; do not insist.
- **Measured by Uplika:** what Uplika measured about the sentences AI Briefing actually quoted. It comes with one tool, not with this skill: `check_naver_visibility` returns it as `citationRules`, in two parts. `rules` are the confirmed ones (grade A): check them like the items above, label them "measured by Uplika", and keep them apart from Naver's items. `suggestions` are weaker (grade B, each with its evidence and caveat): treat them like the common practices and only offer them, label each one "measured by Uplika, weaker", and never mark them pass or gap. Use both exactly as that tool gave them in this conversation. If the tool has not returned them, leave this layer out and say so; do not recall rules from memory. A keyword set's `draftPrompt` ends with Naver's six self-check lines and a short version of these measured rules, both offered as suggestions. They are the same rules, so do not count them as another layer; the full set with grades and evidence comes from `check_naver_visibility`.

Every item in these layers gets exactly one result, except the measured `suggestions`, which are only offered:

- **pass**: quote the line of the draft that earns it.
- **gap**: say what is missing and what would close it.
- **n/a**: the item does not apply to this post, with the reason.

Never add the results up or turn them into a number, a percentage, a grade or a rating. Naver publishes no such measure, and a made-up one would mislead the person. The axes in the visibility tools' report card are on Uplika's own scale; they are not a measure Naver publishes, and they are not these results.

## Procedure

1. **Voice.** Read `~/.uplika/<workspace-slug>/voice.md` if it exists. If not, ask three questions (tone, ending style such as 해요체 or 합니다체, words to avoid) and offer to save the answers with the `voice-profile` skill.
2. **Material: fill in first, ask last.** Naver's guide says experience and a person's final edit are what make content worth citing, and that unedited AI text, patchwork with unclear sources and inaccurate information get filtered out. So gather what can be confirmed, keep where each piece came from, and ask the person only for what is still missing:
   - **Numbers**, in this order: values Uplika already has (search volume, document counts and posts per month from the keyword set, the AI Briefing's sources from `check_naver_visibility`); figures from official documents, statistics, reports or price lists you find, with the link; values you measured by doing it yourself, when you can run it (steps, time taken, file size, what the screen shows); then ask the person for that number alone. If nobody has it, write the post without that number.
   - **Experience**, in this order: what the person tells you; what you actually did, written as it happened ("실행해 보니 설치는 2분이 걸렸습니다"); other people's experiences from your sources, summarized with the source named ("~라는 후기가 많습니다"); confirmed facts rewritten as what the reader goes through ("해 보면 2단계에서 시간이 가장 오래 걸립니다", "설치가 끝나면 터미널에 버전이 뜹니다"); at the end, one or two optional questions to the person.
   - **Alternatives**: compare only what official feature lists, price lists or documents say, as a table with the sources linked.
   - **Sources**: the official documents, statistics or studies the post relies on, with links and the author named.
   - **Sponsorship**: use what the workspace already says (a post about the person's own product says they run it); if nothing says, ask once whether anything was paid for, provided or sponsored (원고료, 협찬, 업체 지원) or bought with their own money (내돈내산).
   - **Photos and videos**, in this order: what the person took; AI-generated images, marked with Naver's AI label (`{.ai}` on the image line when you hand off to `naver-post`); images you make yourself, such as a definition card, a step card, a comparison table or a capture of a public screen. Never images unrelated to the text and never other people's photos.

   The line: never write first-person events, periods or results that did not happen (no "제가 3주 써 보니 매출이 30% 올랐어요"), never a number with no source and no measurement, never a comparison review of things nobody tried, and never 내돈내산 when it is not true. Rewriting confirmed facts as the reader's experience is allowed. What stays empty becomes a gap in the check, not a vague sentence.
3. **Keyword set.** For a search post, take the set from the `naver-keywords` skill, or a saved report from `list_naver_keyword_reports`. Its `draftPrompt` decides where the keywords go and ends with Naver's self-checks and a short version of Uplika's measured rules, both as suggestions (the same items as this skill's first and third layers); the structure below decides what each section holds.
4. **Today's AI Briefing.** Call `check_naver_visibility` with the set's main keyword, and the person's blog so their posts are marked. The extension in the person's Chrome reads Naver's public search page, and every new read spends their daily allowance of search pages, so check the keywords that matter, not every sub keyword. Show the person:
   - whether an AI Briefing answers the keyword, and in which form;
   - the sources it uses (blogs, official documents, others), and whether any is theirs;
   - where blog posts sit in the integrated search results;
   - the related questions it lists.

   Decide with them whether the post also answers some of the related questions. This is information, not a rule: covering them is never marked pass or gap. When the tool's `suggestions` include the one about covering the subtopics AI Briefing answers, bring it up here, next to the related questions, and pick with the person the questions this post can answer from their own facts; it stays a suggestion. If no AI Briefing answers the keyword, say so; the post then aims for the blog results. If the answer comes back `partial: true`, the extension keeps reading in the background: carry on, and read the rest later with `get_naver_visibility` and the `runId`.
5. **Topic consistency.** Call `diagnose_naver_blog` with the person's blog. Its categories and posts per month show what the blog is mostly about. If this post's topic sits outside the blog's core, mark principle 2 (일관된 주제) as a gap and say why: one post cannot fix it, steady posting on the core topic does.
6. **Structure.** Build the post in this order, which follows the self-checks:
   1. Reader and situation in one line: who it is for, in what situation (TPO), for what purpose.
   2. The procedure in the order it happens, with the numbers and the tips only someone who did it knows.
   3. The alternatives, as a table of choices by situation (예: 커플에게는 A, 가족 여행엔 B), with the deciding reason.
   4. The results, including what fell short and the trial and error.
   5. Evidence: links to the sources, with the author named.
   6. Sponsorship or 내돈내산, stated where a reader sees it at once.
   7. For every photo or video, its key point written in the text as well.

   Use headings, short paragraphs and tables so a reader finds the key information fast, and write the sentences by Uplika's measured rules when a tool returned them. Of the measured suggestions the tool gave, pick the ones that fit this post and use only those. If the person agrees to the three common practices, the opening also states the conclusion next to the reader line, subheadings are phrased as the reader's questions, and a short FAQ closes the post.
7. **Filter.** Before showing the draft, remove the five things to avoid: copied or stitched-together content and unedited AI text, heavy ads and promotional outbound links, keywords that do not fit the context, images and videos unrelated to the text, and unverified or inaccurate information.
8. **Check.** Run the 15 official items, the 3 practices and Uplika's measured rules (when a tool returned them) against the draft and show one table: layer, item, result (pass, gap or n/a), and the quoted line or what is missing. Below the table, list the measured suggestions you chose, labeled "measured by Uplika, weaker", with no result column. Below that, list every material you filled in with where it came from: Uplika's value, a link, your own measurement, a rewritten sentence, an AI-generated image or one you made. Self-check by quoting: a pass you cannot back with a quote from the draft is a gap.
9. **Hand off.** Give the draft, the checklist and the photos to the `naver-post` skill, which picks the form and category with the person, previews, checks the extension and publishes after approval. A comparison-led post suits a form meant for comparisons (such as `table-explain`) and a step-by-step one a walkthrough form (such as `divider-tutorial`), but the person decides. A form changes the layout, never the text, so the structure above survives either way.
10. **After publishing.** Uplika keeps an eye on a post it published: while the person's Chrome with the extension is open, it checks the post's main keyword again by itself on a schedule. Tell the person that, and read the results with `get_naver_visibility` and the post's link or Uplika id: the check history, `nextCheckAt`, and events when the post starts or stops being cited or shown. For a post published elsewhere, check its keyword again with `check_naver_visibility` when the person asks. For the whole blog, `scan_naver_blog_visibility` starts a report card and `get_naver_visibility` with the blog reads it. Never promise a citation: Naver decides what AI Briefing quotes, and a post that passes every item can still go uncited.

## Refresh an old post

Principle 5 (최신성 유지) asks that posts be updated when their information changes. Uplika rewrites a published Naver post in place, at the same URL.

1. Find candidates with `list_channel_posts` on the Naver account: posts whose prices, dates, versions or availability have likely changed. The blog's report card (`get_naver_visibility` with the blog) also shows posts that stopped being cited. Read one with `open_post` and its permalink.
2. Ask the person what changed. Their update is the only source for new facts about their own situation; general facts follow step 2 of the procedure.
3. Call `bridge_status`: the extension in their Chrome reads the post from Naver and does the rewrite. If `state` is not `online`, relay `userMessage` word for word and wait until the person says Chrome is open before calling `update_post`.
4. Draft the new version and run the checklist on it. Show the person what will change (old lines and new lines) and send it only after they approve.
5. Call `update_post` with the post's link or id, the new `content` and `wait: true` (editing a live post is asynchronous; if the wait runs out, read the result with `get_post`).
   - A post written in Naver's editor: the first call answers `naver_source_required` with the post's current `source` and its `sourceVersion`. Make the edit on that source. Blocks already in the post (photos, videos, cards, tables, styled text) are `@keep(...)` lines, kept exactly as they are: keep a line to keep that block, delete it to remove the block. You cannot edit inside one; to change an existing table's cells, delete its `@keep` line and write the table again in GFM at the same place. New blocks, a new table included, go anywhere in the usual grammar. Send the edited source as `content` together with `sourceVersion`.
   - If it answers `naver_source_required` again, the post changed on Naver after you read it: start over from the new `source`, never send the older copy.
   - A post published through Uplika: send the whole new body. Its `media:` references are the post's photo list, so keep every photo line that should stay; a photo the new body no longer places is removed from the post.
6. Check the result later the same way as step 10 of the procedure.

## When something fails

- `research_tool_disabled` (from `diagnose_naver_blog`, `list_naver_keyword_reports` or the visibility tools): only a research tool still in beta answers this. Ask the person once to open the link in the error and turn it on, and do not retry until they say it is on. Meanwhile go on without it: mark principle 2 as a gap with the reason "blog not diagnosed", or skip step 4 and say AI Briefing was not checked.
- `bridge_offline`: the extension is not connected, so nothing was searched. Relay the message and call again after the person says Chrome with the extension is open.
- `naver_search_busy`: a check is already running for this person, or today's allowance of search pages is used up. Do not call again before `retryAfterSeconds`; what was already read comes back from `get_naver_visibility`.
- `naver_search_blocked`: Naver kept refusing search pages from the person's browser, so Uplika is resting it. Wait `retryAfterSeconds` and do not try to get around it.
- `naver_search_permission`: the extension lacks permission to reach Naver search. Relay the message.
- `naver_keep_unknown`: a `@keep` id that is not in the post's current source. Use the ids from the source.
- `naver_rate_limited`: do not call again before `retryAfterSeconds`.
- `extension_outdated`: the extension in that Chrome is too old for source edits or for reading Naver search; relay the message with `faq:extension-not-updating`. When the message says the needed version is not on the Chrome Web Store yet, do not ask the person to update.
- `post_not_editable`: Uplika could not turn this post into a source it can rewrite without losing parts of it. The person edits it in Naver's editor.
- `workspace_required`: show the workspaces it lists, ask which one, and pass `workspaceId`.
- `account_disconnected`: hand over to the `troubleshoot` skill.
- Anything else: call `get_help` with the error code and pass its answer and link on.

## Tools

- `diagnose_naver_blog`: the blog's categories and posts per month, for topic consistency
- `list_naver_keyword_reports`: a saved keyword set and its `draftPrompt`
- `check_naver_visibility`: today's AI Briefing and search results for keywords, with Uplika's measured rules and weaker suggestions
- `get_naver_visibility`: a check's results, a post's check history or the blog's report card
- `scan_naver_blog_visibility`: start a report card for the whole blog
- `list_channel_posts`: the blog's existing posts, to find ones worth refreshing
- `open_post`: read an old post before refreshing it
- `bridge_status`: whether the extension that rewrites the post is online
- `update_post`: rewrite a published post at the same URL (after approval)
- `get_post`: the result of an edit when the wait runs out
- `get_help`: the answer for an error code
