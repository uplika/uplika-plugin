---
name: naver-keywords
description: "Research Naver Blog keywords: diagnose the blog, expand seeds, measure and judge, pick one set per post. 네이버 키워드 조사, 검색량."
---

# Naver keywords

Find keywords a Naver Blog post can actually win, measured and judged by Uplika, and leave with one keyword set per post. The set's `draftPrompt` is the brief the writing skills work from.

Use it when the person asks what to write about on Naver, which keywords to target, how often a keyword is searched (검색량), or wants a keyword set before writing. Writing and publishing belong to the `naver-post` skill, or `naver-ai-cite` when the goal is to be cited in Naver's AI Briefing.

## Procedure

1. **Blog.** Ask which blog this is for (its id or any link to it). If the person has a connected Naver Blog, `list_accounts` shows it and its handle is the blog id. Any public blog works, connected or not.
2. **Diagnose.** Call `diagnose_naver_blog` with the blog. Read what it returns: the share of titles that carry a search intent word (price, how to, review), how many titles start with a date or episode label, posts per month, the categories, and `flags` with `thresholds` (for example `lowIntent`). `summary.oldest` and `summary.newest` say which dates it read and `summary.capped` says whether it stopped early, so do not describe a long-running blog's whole history from it. `seedCandidates` are words the blog repeats in its titles: candidates to research, not proven keywords. It reads titles only; whether the posts are actually cited by the AI Briefing or shown in search is `scan_naver_blog_visibility`, read with `get_naver_visibility`.
3. **Seeds.** Agree on seed keywords with the person: their topic, plus any `seedCandidates` they want. Write each seed the way people type it into Naver search (예: `제주 한달살기`, `아이패드 필기 앱`).
4. **Expand.** Call `expand_naver_keywords` with the seeds (no more per call than its description allows; too many answers `invalid_params`). `found[]` lists every autocomplete word with where it came from (`from` is the seed or `L1:<seed>`), and `via` says whether the person's Chrome extension or Uplika's server answered. These are candidates, not keywords yet. Drop the ones that are off topic for this post, together with the person when the list is long.
5. **Topic.** Ask for one line on what the post is about (예: `3월 제주 한달살기 숙소 고른 후기`). It goes into the brief; without it the brief tells the writer to pick a subject that fits the main keyword.
6. **Measure and judge.** Call `research_naver_keywords` with the candidates as `keywords`, the person's request as `seedText`, and the line as `topic`. Its description says how many keywords one call takes, and keywords past that are dropped without an error, so send the candidates that fit the post best, strongest first. Sets only group keywords measured in the same call. The response has:
   - `rows`: each keyword's monthly searches (`volume`), blog document count (`docs`), posts per month (`monthly`), `ratio` (searches over documents: higher means fewer writers per searcher), search `intent`, `verdict` and `why`.
   - `sets`: keywords grouped by search intent into one post each, a `main` keyword plus `subs`, each set with `prompt` (a Korean brief for the skeleton) and `draftPrompt` (a Korean brief for the whole post, with photo spots marked).
   - `reportId`: the saved report.
   - `partial: true` with `unmeasured[]`: the time budget ran out before every keyword was measured. Call again with the same keywords; the measured ones come from cache and the rest finish. This is not an error.
7. **Show.** One table per set: role (main or sub), keyword, volume, docs, ratio, verdict, and the gist of `why`. Read the verdict and its reason from the response. Do not recompute ratios or re-judge with thresholds of your own.
8. **Pick.** One set is one post. Ask which set to write first. The set's main keyword is already the one that can be won, not the biggest one: do not swap it for a bigger sub, and do not add keywords the response did not measure.
9. **Hand off.** Pass the chosen set's `draftPrompt` unchanged to `naver-post` (or `naver-ai-cite`), with its main keyword, subs and the `reportId`. Do not rewrite the brief or restate its rules; it carries its own placement rules and lengths. When the person wants to know whether Naver's AI Briefing answers the main keyword and whom it cites, hand over to `naver-ai-cite`: it checks that before writing.

## Verdicts

Every row's `verdict` comes with `why`, which carries the numbers behind it. Use these meanings when you explain them; the thresholds belong to the server.

| verdict | meaning |
|---|---|
| `best` | Few documents for the searches. The strongest main keyword |
| `possible` | Workable, with more competition than `best` |
| `hard` | Many documents. Grow the blog first |
| `wall` | So many documents that a new blog cannot break in |
| `hot` | Many new posts every month. New posts get pushed down fast |
| `saturated` | Too many documents for the searches |
| `phantom` | Searches at the floor. Ranking first brings nobody |

When document counts are missing (`axes` is 2) the server judges on searches and ad competition only and answers `candidate`, `hold` or `saturated_suspect`. `unmeasured` means Search Ad had no data for that spelling, so conclude nothing from it. The Korean briefs label verdicts 최적, 가능, 어려움, 벽, 과열, 포화, 허수.

## Past research

- `list_naver_keyword_reports` lists saved research, newest first, with every set and its prompts. Reports belong to the person, not to a workspace. Reuse one instead of measuring again.
- An older report may carry only `prompt`. If the chosen set has no `draftPrompt`, call `research_naver_keywords` again with that set's keywords and a `topic`; measurements still in the cache are reused.
- `get_naver_keyword_history` gives one keyword's measurements, one point per day it was measured, newest first. Use it to say whether a keyword is rising or cooling. An empty list means nobody has measured it here yet.

## When something fails

- `research_tool_disabled`: only a research tool still in beta answers this (the person has not turned it on for MCP connectors). Ask them once to open the link in the error (`enableUrl`) and turn it on, and do not retry until they say it is on. Carry on without it meanwhile, for example with keywords the person gives you.
- `naver_autocomplete_unavailable`: neither the extension nor Uplika's server could run autocomplete. Skip expansion and pass the seeds plus your own candidates straight to `research_naver_keywords`.
- `naver_autocomplete_busy` or `naver_autocomplete_paused`: wait `retryAfterSeconds`, then call once more.
- `quota_exceeded`: today's allowance for that kind of call is used up; the error says which (`what`) and the limit. Tell the person and work from saved reports and history.
- `naver_seo_busy` (Uplika's shared allowance with Naver is used up for now) or `rate_limited` (Naver is slowing us down): tell the person, and wait `retryAfterSeconds` when the error gives it. Do not loop.
- `workspace_required`: show the workspaces it lists, ask which one, and pass `workspaceId`.
- Anything else: call `get_help` with the error code and pass its answer and link on.

## Tools

- `list_accounts`: the connected Naver Blog and its handle (the blog id)
- `diagnose_naver_blog`: title habits, categories, posts per month, seed candidates
- `expand_naver_keywords`: autocomplete candidates from seed keywords
- `research_naver_keywords`: measure, judge and group keywords into sets with `draftPrompt`
- `list_naver_keyword_reports`: saved research to reuse
- `get_naver_keyword_history`: one keyword's measurements over time
- `scan_naver_blog_visibility`: whether the blog's latest posts are cited by the AI Briefing or shown in search, searched through the person's extension (titles alone do not say)
- `get_naver_visibility`: the report card and per-post results of that search check
- `get_help`: the answer for an error code
