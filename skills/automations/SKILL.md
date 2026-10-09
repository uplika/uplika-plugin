---
name: automations
description: Set up comment-to-DM, keyword DM, follow gate and public-reply automations from templates; validate, confirm, then enable.
---

# Automations

Comment-to-DM, keyword DMs, follow gates, file or link delivery, public comment replies, story replies, Naver neighbor comments. Automations act on real people without anyone watching, so the person approves before one goes live.

## How the platforms work (say this when it matters)

A business account cannot start a DM. On Instagram and Facebook the only automatic door is a private reply to a comment, one per comment (`faq:private-reply-once`); once the person answers, the messaging window opens (`faq:dm-24h-window`). Threads has no DMs at all (`faq:threads-no-dm`), so Threads automations reply in public. Ask `get_help` for the details instead of explaining from memory.

## Procedure

1. Find the account with `list_accounts` (only accounts that hold the messaging permission can run DM automations).
2. Call `list_automation_templates` and pick with the person. Common ones: `template:comment_to_dm` (comment, then a private reply with a button, then the link or file), `template:keyword_dm`, `template:comment_public_reply` (public replies, fixed or AI-written), `template:default_reply`, `template:story_reply_dm`, `template:neighbor_post_comment` (Naver Blog; see the `naver-engage` skill).
3. Which post: an existing post (id or link), `any`, or `next` (the next post on that account). A post that is only scheduled is not live yet: create the automation after it goes out, with the published post id. Attaching through the publish call's automation argument only works for posts that go out now.
4. Create a draft: `create_comment_to_dm` for the common case, `create_automation` with the template's params for the rest. Both create drafts; nothing goes out yet. Write the messages in the person's voice (`~/.uplika/<workspace-slug>/voice.md` if it exists). A file to deliver needs a direct https link to the file itself, or a media id from an upload.
5. For a flow document you edited yourself, run `validate_automation` and fix every problem it lists.
6. Show the person the trigger, every message, buttons, links and the follow rule. Turn it on with `enable_automation` only after they approve: **this is the moment messages start going to real people**.
7. Later: `list_automations` to see what is live, `update_automation` to change messages (read the version first), `list_automation_runs` to see what happened to each comment.

## When it refuses or does not fire

- `reconsent_required`, `feature_in_review`: hand over to the `troubleshoot` skill.
- `next_post_taken`, `automation_catch_all_taken`: only one automation per account may wait for the next post, and only one catch-all; the error names the live one. Ask which to keep.
- Nothing happened after a comment: read `list_automation_runs` (statuses like `blocked_window`, `blocked_opt_out`, `failed_channel`) and `faq:automation-not-firing`.

## Tools

- `list_accounts`: the account to run on
- `list_automation_templates`: templates and their params
- `create_comment_to_dm`: draft the common comment-to-DM flow
- `create_automation`: draft any other template
- `validate_automation`: check a flow document before saving
- `enable_automation`: go live, only after approval
- `update_automation`: edit messages or turn on and off
- `list_automations`: what exists and what is live
- `list_automation_runs`: what happened on each run
- `get_help`: platform rules and error answers
