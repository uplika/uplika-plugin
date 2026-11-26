---
name: naver-drafts
description: List, read and publish Naver Blog drafts as they are in Naver, or rewrite a published post at the same URL. 임시저장 글.
---

# Naver drafts

Naver Blog drafts (임시저장 글) and edits to published posts. There are several different jobs here; find out which one the person means before calling anything:

| The person wants | Tool | What happens |
|---|---|---|
| The current text and formatting of a draft, edits made by hand in Naver included | `read_naver_draft` | The extension reads the draft as it is in Naver now. Nothing changes and nothing goes public |
| A draft in Naver's draft box published exactly as it is there | `publish_naver_draft` | The extension opens that draft in Naver's editor and presses publish, so edits made by hand in Naver are kept |
| A draft published exactly as it is, but at a set time | `publish_naver_draft` with `scheduledAt` | At that time the extension publishes the text and photos the draft has in Naver then, with the title and category from when you schedule. If the draft has no title or no category, pass `title` or `category`; an empty one is refused. The tags the draft had when you schedule go out and tags added in Naver later stay, unless you pass `tags`, which replace them |
| The text of a draft Uplika saved changed, and still a draft | `update_post` with `options.naver_blog.draftOnly: true` | The draft in Naver is replaced with the new text; nothing goes public |
| Uplika's own copy of a draft it saved with `options.naver_blog.draftOnly` published instead | `update_post` | Uplika's text goes out as a new post with its own URL, and the old draft leaves the box |
| A post that is already published changed | `update_post` | The post is rewritten in place, at the same URL |

## Before anything

1. Call `bridge_status`. The Uplika extension in the person's Chrome reads the draft box, reads posts written in Naver's editor and writes the posts. If `state` is not `online`, relay `userMessage` word for word. With a terminal on the same computer, show the `wake` command for their system and run it only if they say yes; without one, ask them to open Chrome. Listing drafts and reading a post need it online, so wait until the person says Chrome is open.
2. If any call answers `workspace_required`, show the workspaces it lists, ask which one, and pass `workspaceId` from then on.

## Publish a draft as it is

1. Call `list_naver_drafts` (pass `accountId` to limit it to one blog). Each draft has its `logNo`, its title and when it was last saved, newest first. Drafts saved through Uplika and drafts the person saved by hand in Naver both appear.
2. Show the drafts (title and when each was last saved) and let the person pick one. The list does not show a draft's category, tags or visibility; read them with `read_naver_draft` before you say what they are:
   - A draft saved through Uplika with `options.naver_blog.draftOnly` keeps the category and visibility that post asked for if the person's Uplika extension was 0.7.54 or newer when it was saved, and its tags from 0.7.52. With an older extension, or when the post asked for none, it has the blog's default category and visibility and that post's result warning said what was left off; ask for them and pass them, reading the categories from `list_accounts` (`naverBlog.categories`). Anything you do not pass stays as the draft has it. Pass `tags` only to change them: a list you pass replaces the draft's tags.
   - A draft saved by hand keeps whatever Naver stored with it, which Uplika cannot see. Ask whether to leave those as they are or to set the category, tags or visibility explicitly.
   - A draft left behind by a failed publish is not the finished post. If an earlier failure said "A half-finished Naver draft may have been left", do not publish that draft: send the original post again with `retry_post` and ask the person to delete the draft in Naver.
3. Publish only after the person approves. Call `publish_naver_draft` with the `logNo`, plus `title`, `categoryId` (or `category` by name), `tags` or `openType` only for what they want changed, and `wait: true`. Do not send content: the text is whatever is in Naver.
4. If the response carries `bridge`, the post is queued: relay `bridge.userMessage` and do not say it was published. If it carries `note`, pass it on to the person: it warns when the draft has no body text, which is what a failed publish leaves. Otherwise call `get_post` for the status and the permalink. A draft that Uplika made turns into the same post record instead of a second one.

## Read a draft

Use this when the person edited a draft by hand in Naver and wants you to see it, for example to write the next draft the same way.

1. Take the `logNo` from `list_naver_drafts`, or from a post's Naver `externalId` after `draft:`. Call `read_naver_draft` with it, plus `accountId` when the workspace has more than one blog. It reads the draft as it is in Naver now and changes nothing, so it needs no approval.
2. You get the title, `text`, the category, the tags, the visibility, the photo count and `blockTypes`. `text` holds only the body paragraphs and quotes; `blockTypes` counts every kind of block, so a heading or a table shows there even when its words are not in `text`.
3. When `blocks` is a list, it is the draft in document order: headings, paragraphs and quotes with their `markdown` in Uplika's grammar (bold, links, text color, highlight), and photos with their `caption` and count. Reuse that markdown as it is when you write the next draft. When `blocks` is null, pass `note` on to the person: the formatting, the photo captions and where the photos sit come with the next Uplika extension version, which installs by itself.
4. Photo files are not returned. To put the same photos in a new draft, ask the person for them.
5. `get_post` shows Uplika's own copy of a post, not what is in Naver now. For a draft's current text, use `read_naver_draft`.

## Publish a draft at a set time

1. Do steps 1 to 3 above, and also ask when it should go out and in which timezone. The time has to be 10 minutes to 365 days from now. The draft is read when you schedule it, so Chrome has to be on now as well as at that time.
2. After the person approves, call `publish_naver_draft` with the `logNo`, `scheduledAt` (ISO 8601 with a timezone offset) and only the overrides they want. If the draft has no title or no category, pass `title` or `category`; an empty one is refused. The answer is a scheduled post. Pass its `note` on: the text and photos that go out are whatever the draft has in Naver at that time, the title and category are the ones from now, and the tags it has now go out along with any added in Naver later, unless you pass `tags`. If they change those in Naver, call it again with the same `scheduledAt` and everything you passed before.
3. To move it, call `update_post` with a new `scheduledAt`, or `publish_naver_draft` again with the new time. To send it early, call `publish_now`. To cancel it, call `delete_post`: the draft stays in Naver.
4. Do not put `options.naver_blog.tempLogNo` on a new post to schedule a draft. Uplika writes that mark itself and refuses it.

## Change a draft Uplika saved and keep it a draft

When a post's Naver target has an `externalId` that starts with `draft:`, call `update_post` on that post with the new `content` and the Naver options in full, including `options.naver_blog.draftOnly: true`, after the person approves. Nothing goes public. A draft written by hand in Naver can only be edited in Naver.

## Publish Uplika's copy instead

A post Uplika saved with `options.naver_blog.draftOnly` has a Naver target whose `externalId` starts with `draft:`. If the person wants Uplika's version of the text rather than what is in Naver now, call `update_post` on that post with its `content` (changed or not) after they approve. Pass the Naver options again in full (`options.naver_blog.title`, `options.naver_blog.categoryId` or `options.naver_blog.category`, `options.naver_blog.tags`, `options.naver_blog.openType`, and `options.naver_blog.form` or `options.naver_blog.layout`), without `draftOnly`: options you pass replace the stored ones, and a draft has no category. It goes out as a new post and, with a current extension, the old draft is removed from the box. This is not an edit of a published post, so it gets a new URL.

## Rewrite a published post

`update_post` rewrites a published Naver post in place: same URL, same post number.

1. Take the post's link (or its Uplika id) from the person.
2. Write the new version, show the person what will change (old lines and new lines), and send only after they approve.
3. Call `update_post` with the link or id, the new `content` and `wait: true`. Editing a live post is asynchronous: if the wait runs out, read the result with `get_post`.
   - **Written in Naver's editor:** the first call answers `naver_source_required` with the post's current `source` and its `sourceVersion`. Make the edit on that source. Blocks already in the post (photos, videos, cards, tables, styled text) are `@keep(...)` lines, kept exactly as they are: keep a line to keep that block, delete it to remove the block. You cannot edit inside one; to change an existing table's cells, delete its `@keep` line and write the table again in GFM at the same place. New blocks, a new table included, go anywhere in the usual grammar. Send the edited source as `content` together with `sourceVersion`. If it answers `naver_source_required` again, the post changed on Naver after you read it: start over from the new `source`.
   - **Published through Uplika:** fields you leave out keep their current value. Options you pass replace the post's whole options, so either leave them out or pass every Naver setting again.
   - **Photos:** the `media:` references in the new body are the post's photo list. A photo the new body no longer places is removed from the post. Pass `mediaIds` only for photos to add at the end without placing them.
4. If the Naver editor shows a missing-image error on a post Uplika published, rewriting it with `update_post` fixes it at the same URL.

## When something fails

- `bridge_offline`: the extension is not connected, so nothing was listed or read. Relay the message (`faq:naver-extension-offline`) and try again once Chrome is open.
- `extension_outdated`: the extension in that Chrome is too old for this job. The response says the installed and required versions, and Uplika asks that Chrome to update at the same moment. Relay it with `faq:extension-not-updating` and try again after the person says it updated.
- `naver_form_required`: the response lists `forms` (id, name, when). Show them and let the person pick (`options.naver_blog.form`), or set `options.naver_blog.layout` to `as-is` to keep the body exactly as written.
- `naver_draft_not_found`: that `logNo` is not in the blog's draft box. Call `list_naver_drafts` again and use a number from it.
- `naver_category_required` or `naver_category_unknown`: show the categories from `list_accounts` and let the person pick.
- A draft publish that failed with "Naver closed the publish window without opening a new post": sending the same draft again from here is unlikely to help. The person opens that draft in Naver and publishes it there, or you send the original post again (after they approve) and they delete the half-finished draft.
- `naver_temp_log_no_reserved`: a call carried `options.naver_blog.tempLogNo`. Nothing was sent. Publish the draft with `publish_naver_draft` (add `scheduledAt` to schedule it), or leave `tempLogNo` out to publish a new post.
- `naver_draft_field_not_editable`: the post is a scheduled draft publish, and the call changed its text, photos or channels (`error.field` says which). Nothing changed. Ask the person to edit the draft in Naver, or delete the post (the draft stays in Naver) and publish a new one.
- `naver_rate_limited`: Naver capped how much this ID publishes. Do not call again before `retryAfterSeconds`; the draft is already in Naver.
- `naver_keep_unknown`: a `@keep` id that is not in the post's current source. Use the ids from the source.
- `naver_media_over_limit`: the body places more photos or videos than Naver takes (the limit is in `list_platforms`). Nothing changed; `droppedIds` says what to take out.
- `post_not_editable`: Uplika cannot rewrite this post. The message says why and what to do: relay it. When Naver would not open the post for editing, the person changes it on Naver Blog directly.
- `account_disconnected`: hand over to the `troubleshoot` skill.
- Anything else: call `get_help` with the error code and pass its answer and link on.

## Tools

- `bridge_status`: whether the extension in the person's Chrome is online
- `list_naver_drafts`: the drafts in the blog's draft box
- `read_naver_draft`: one draft's text, formatting, category, tags and visibility as they are in Naver now (read-only)
- `list_accounts`: the blog's categories, for drafts saved without one or with an older extension
- `publish_naver_draft`: publish a draft exactly as it is in Naver, now or at `scheduledAt` (after approval)
- `update_post`: rewrite a published post at the same URL, replace a draft Uplika saved, move a scheduled draft, or publish Uplika's copy of a draft (after approval)
- `publish_now`: send a scheduled draft right away (after approval)
- `delete_post`: cancel a scheduled draft; the draft stays in Naver (after approval)
- `retry_post`: send the original post again when a failed publish left a half-finished draft (after approval)
- `get_post`: status and permalink after publishing or editing
- `list_platforms`: Naver's media limits
- `get_help`: the answer for an error code
