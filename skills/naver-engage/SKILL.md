---
name: naver-engage
description: Comment on neighbors' new posts, find neighbor candidates, like and follow on Naver Blog without guessing limits. 이웃 댓글, 서로이웃 후보, 공감.
---

# Naver engage

Engage with other Naver blogs from the person's connected blog: an automation that comments on neighbors' new posts (이웃 새 글 댓글), and one-off likes (공감) and follows (이웃추가). Everything here shows up on someone else's blog under the person's name, so every action is confirmed with them first.

All of it runs in the Uplika extension in the person's Chrome. Call `bridge_status` before a like, a follow or turning the automation on. If `state` is not `online`, relay `userMessage` word for word and wait until the person says Chrome is open.

## Actor and target are two different blogs

- **Actor:** the person's connected Naver Blog, the account the action is done as. In the extension's jobs this is `blogId`, and the server fills it in from the connected account. A workspace holds one Naver Blog, so choosing the workspace chooses the actor (`follow` still has an `accountId` argument for several blogs in one workspace; you will not need it). If a call answers `workspace_required`, show the workspaces it lists, ask which blog should act, and pass `workspaceId`.
- **Target:** the other blog, the owner of the post being liked or commented on, or the blog being followed. In the jobs this is `targetBlogId`, taken from the link.
- They are different values. Never derive one from the other: a link to someone else's post does not change who acts, and the actor never comes from a link.
- The person's Chrome has to be logged in to Naver as the actor blog. If it is logged in as a different blog, the job stops with `naver_wrong_login` and touches nothing. Relay the message, ask the person to log in as the actor blog, then try once more.

## Limits are not ours to guess

Never state, estimate or promise how many comments, likes or follows are safe per day or per hour, and never invent a pace. Naver closed its writing API over mechanical mass activity, and when Naver restricts an account it is the person's blog that gets suspended, not Uplika. Uplika's server and Naver decide the limits:

- The neighbor comment automation applies its own skip rules on the server (one comment per post, a gap between comments, nothing older than 48 hours). Uplika sets no daily count of its own since 2026-10-14; its description in `list_automation_templates` says what it skips; repeat that, not numbers of your own.
- If a call answers `naver_rate_limited`, `naver_engagement_limited` or `rate_limited`, stop. Do not call again before `retryAfterSeconds`, and do not work around it through another account or workspace. `naver_engagement_limited` means Naver itself stopped showing the add-neighbor page for that blog today (the page came back blank more than once); the answer carries `until`, and nothing goes out from that blog before midnight Korea time. Tell the person it is Naver's limit, not Uplika's, and pass on the `help` link.
- Like only the posts the person names.
- Follow only the blogs the person picked: a blog they named, or one they chose from a candidate list you showed them (`find_naver_neighbor_candidates`). Send one follow at a time and wait for its answer. When an answer is a stop code, stop the whole list there. Never send a refused blog again, and never resend it with `mutual: false` unless the person asks for that blog.

## Comment on neighbors' new posts (automation)

`template:neighbor_post_comment`: when a neighbor publishes a new post, Uplika reads it and leaves one comment written by AI in the channel's persona.

1. Call `list_accounts` to find the Naver Blog and its `accountId`. Call `list_automations` with that `accountId` and `templateId` `neighbor_post_comment` to see whether one already exists; reuse it rather than creating a second one.
2. Read the template in `list_automation_templates`: its params and what it skips.
3. Ask the person:
   - Whose posts: mutual neighbors only (`mutual`, the default) or every neighbor in the feed (`all`).
   - The instruction: what the blog is about and how the comments should sound (예: 「여행 블로그예요. 글에서 구체적인 장면 하나를 짚어 짧게 공감하는 댓글, 홍보 문구는 넣지 않기」).
   - A name for the automation.
4. Call `create_automation` with `accountId`, `templateId` `neighbor_post_comment` and `params` (`neighbors`, `instruction`, `name`). It is saved as a draft; nothing is posted yet.
5. Before turning it on, tell the person plainly:
   - Once it is live, each comment goes out on the neighbor's post without passing by them first.
   - It reacts only to posts published after it is turned on, and it skips posts and holds back comments by the rules in the template's description.
   - It runs only while Chrome with the Uplika extension is open on their computer.

   Show the instruction and the neighbor setting, and turn it on with `enable_automation` only after they approve.
6. Afterwards, `list_automation_runs` shows what it commented on and what it skipped. When the person wants it stopped, call `disable_automation`.

## Like (공감)

1. Take the link to the post from the person. On Naver Blog the post can belong to another blog; the connected blog does the liking.
2. Confirm with the person which post it is and which blog acts. Uplika has no unlike.
3. Call `like` with the link as `id`. To like a comment on the person's own post instead, pass `replyTo` with the comment's id from `list_replies`.
4. `already: true` means it was already liked and nothing changed. `naver_not_allowed` means Naver offers no like there: the person's own post, a secret or hidden comment, or a blog that turned comment likes off. Retrying does not help.

## Find neighbor candidates (서로이웃 후보)

When the person wants new neighbors on a topic, find candidates with Uplika instead of collecting blog ids from a web search.

1. Call `list_accounts` for the connected Naver Blog, and `bridge_status`. If the extension is offline the list still comes, but Uplika cannot read the blog's neighbor list; say so when you show it.
2. Ask for the topic (a few words, as they would search it on Naver) and the kind of request: mutual neighbor (서로이웃) or neighbor (이웃).
3. Call `find_naver_neighbor_candidates` once per topic with `query` and `mutual` (the same value you will give `follow`). Each call uses one of the person's daily keyword measurements; `quota` in the answer says what is left.
4. Show the list: each blog's address, name, latest post date on the topic, how many of its posts were in the sample, and the post titles. Say how many blogs were left out and why (`excluded`); where the extension can read the requests the account has sent, `pending` is a request still waiting and `declined_or_withdrawn` is one that was declined or taken back. When `relationKnown` is false, say the neighbor list could not be read (`relationNote`), so some blogs may already be connected.
5. Let the person pick. Confirm the picked blogs, and the message for mutual requests.
6. Call `follow` for one picked blog at a time, and wait for each answer before the next.
7. Tell the person each answer as one of the five in Follow below.
8. When an answer is a stop code, stop the whole list there and tell the person why.

Never add blogs the person did not pick, never send a refused blog again, never resend it with `mutual: false` unless the person asks for that blog.

## Follow (이웃추가)

1. Take the blog from the person: its id or any link to it.
2. Ask which kind: a neighbor (이웃), added right away, or a mutual neighbor (서로이웃), a request the other blog has to accept, optionally with a message Naver shows them.
3. Confirm, then call `follow` with `blog`, `mutual` and `message`. Uplika has no unfollow.
4. Read the answer as one of five:
   - Sent: `pending` (the mutual request waits for them; `requestSent: false` means a request was already waiting and nothing new went out) or `following` (added as a neighbor).
   - Already: `already`, already a neighbor, nothing sent.
   - Refused: `naver_follow_blocked`, that blog does not take this request. Do not send it again. If the message ends in `[matched=group_full]`, it is this account's neighbor group that is full, not that blog: stop.
   - Unknown: `naver_tab_lost`, nothing is known to have changed; sending it once more is safe.
   - Stop: `naver_engagement_limited`, `naver_not_logged_in`, `naver_wrong_login`, `bridge_offline`, `extension_outdated`. Stop the whole list there and tell the person.

## When something fails

- `bridge_offline`: the extension in the person's Chrome is not connected, so the like or follow did not happen. Relay the message (`faq:naver-extension-offline`), and try again once the person says Chrome is open.
- `extension_outdated`: the extension in that Chrome is too old for this job; the response says the installed and required versions. Relay it with `faq:extension-not-updating`.
- Anything else: call `get_help` with the error code and pass its answer and link on.

## Tools

- `list_accounts`: the connected Naver Blog that acts
- `bridge_status`: whether the extension in the person's Chrome is online
- `list_automations`: an existing neighbor comment automation on that account
- `list_automation_templates`: the template's params and what it skips
- `create_automation`: save the neighbor comment automation as a draft
- `enable_automation`: turn it on (after approval)
- `list_automation_runs`: what it commented on and what it skipped
- `disable_automation`: turn it off
- `list_replies`: comment ids on the person's own post
- `like`: like a post or comment as the connected blog (after approval)
- `find_naver_neighbor_candidates`: blogs that recently posted on a topic, with already connected ones left out
- `follow`: add a blog as a neighbor (after approval)
- `get_help`: the answer for an error code
