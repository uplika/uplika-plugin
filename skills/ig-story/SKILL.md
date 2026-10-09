---
name: ig-story
description: Plan the day's Instagram Stories (frame sequence, which sticker does which job, the DM funnel) and publish the frames as stories after approval.
---

Adapted from Jakeschincariol/instagram-agent-skill (MIT). Not affiliated with the original author.

# ig-story

Use when the person says "stories", "what do I post on my story", "story sequence", "poll idea", "I have nothing to story about", or wants to sell something without making a post about it.

Stories are not a smaller feed. The feed is how strangers find you. Stories are how the people who already follow you decide whether you are a person worth buying from, and they are the only surface on Instagram where a tap turns into a conversation in one move.

Nobody outside your followers sees these, so the job is completely different: depth, not reach.

Read the voice file `~/.uplika/<workspace-slug>/voice.md` first if it exists. If it does not, ask three questions (tone, how they end a line, words they avoid) and offer to save the answers with the `voice-profile` skill.

## The daily shape

Three to seven frames a day. Beyond about seven, the tap-forward rate climbs and the last frames play to nobody, which is exactly where people put the ask.

```
1       THE OPEN     something happening today, with a face or a hand in it.
2-3     THE MIDDLE   the actual content: the process, the result, the mistake.
4       THE ASK      one sticker. Poll, question box, quiz or link.
5       THE CLOSE    the answer, the outcome, or tomorrow's setup.
```

Put the ask at frame 4, not frame 7. Completion drops with every tap and the ask should be seen by the people who are still there.

## The stickers, and what each is actually for

| sticker | job | use when |
| --- | --- | --- |
| **Poll** | the cheapest tap there is | you want volume of response, not information |
| **Question box** | harvesting the exact words people use | you need content ideas or objections, verbatim |
| **Quiz** | teaching by letting them be wrong | there is a common misconception in the niche |
| **Slider** | vibe check | nothing important. Fun, low value |
| **Link** | the only clickable surface besides the bio | there is somewhere real to go |
| **Countdown** | a deadline people can subscribe to | a launch, a live, a close date |
| **Add yours** | reach beyond your followers, occasionally | the prompt is one anyone in the niche can answer |

The question box is the most undervalued one in the list. Every answer is a caption, a Reel hook or a DM opener written in the audience's own words. Feed them to `ig-reel` as formula #16.

## Rules

- **A face or a hand in the first frame.** Text on a coloured background gets tapped through, and the first frame decides whether the rest get watched.
- **One idea per frame.** Reading a paragraph on a story is not a thing anyone does.
- **Keep text inside the middle.** The profile row sits on top of the frame and the reply bar sits underneath; anything in those bands is covered.
- **Talk to one person.** "You" singular. Stories are the closest thing to a DM that is not one.
- **Do not repost your own feed post to stories with no comment.** It is the single most ignored frame on the platform. If you are pointing at a post, say what happened in the comments and why it is worth going back for.
- **Sell on stories, not in posts.** Three frames of context, one frame of offer, one frame of proof. That sequence sells more than a feed post about the same thing and costs you no reach.

## The DM funnel, done honestly

The sequence that works: a story that names a problem, a question box or a poll that lets people say "that's me", and then a reply to each person who answered. The conversation starts because they spoke first.

Automated replies are a real, supported feature for professional accounts, through Instagram's own tools and approved partners. Bulk DMing people who did not interact is not, and it is what gets accounts restricted. The rule is simple: **they act first, then you reply.**

## Output

The frames in order, each with what is on screen, what is said, and which sticker, plus what to do with the answers:

```
STORIES  ·  Tuesday  ·  5 frames

1  [selfie, walking]      "Third refund request this year. Same reason."
2  [screen recording]     the clause, highlighted
3  [talking]              "Approval is a feeling. Delivery is a date."
4  [poll]                 "Have you been burned by a late approval?"  Yes / Not yet
5  [text on photo]        "Reply and I will send you the clause."

After: everyone who votes Yes gets a reply. That is the whole funnel.
```

Run the words through `ig-human` before showing them.

## With Uplika connected

Uplika publishes each story frame as one image or one video. Read the option schema before promising more: it has no sticker fields (poll, question box, quiz, link, countdown, add yours), so a frame that needs a sticker is posted from the Instagram app.

1. **Account.** Call `select_channels` with the Instagram account, or with no scope and let the person choose. Never assume Instagram is connected; if it is not, send the person to https://uplika.com/dashboard/connections. If the answer is `workspace_required`, show the workspaces it lists, ask which one, and pass that `workspaceId` on every later call.
2. **Rules.** Read Instagram in `list_platforms`: image and video rules, the option schema under `options`, and the features table. Instagram posts cannot be edited after they go out (the features table says so), so the frames are approved first.
3. **Build each frame** as a full-screen vertical image or video with every word on it. Stories show no caption.
4. **Upload each frame.** With a terminal: `media_presign` with the file name, type and size, PUT the bytes to the returned `uploadUrl` with curl, then `media_complete`. Without one: `media_from_url` for a file at a public https address, or `media_upload_link` for files on the person's device (give them the link, then poll `media_upload_status` until it is ready). Pass `aiGenerated` for media made with AI.
5. **Show and confirm.** Show the frames in order, which ones Uplika will publish and which ones the person posts from the app, the account and the time. Publish only after they approve.
6. **Publish one frame per call.** `publish` with the `accountIds` from `select_channels`, one media id, `options.instagram.contentType` set to `story`, and `wait: true`; then the next frame. Stories appear in the order they are posted, so wait for each before sending the next. When the sequence has a sticker frame, either post the whole sequence from the app, or publish the frames before it, let the person add the sticker frame in the app, then publish the rest. For a later time give each frame its own `scheduledAt` with a time zone offset, spaced out in the order the frames should appear, and ask which time zone the person means. `options.instagram.firstComment` and `options.instagram.collaborators` do not apply to stories.
7. **Report.** `get_post` for each frame gives its status. If one failed, call `get_help` with its code and pass on the answer and its url. `reconsent_required`, `feature_in_review` and `account_disconnected` go to the `troubleshoot` skill.

The reply side of the funnel:

- A reply someone types in a story's message bar arrives as a DM and opens the messaging window. An automation can answer it with a coupon, a link or an answer: `template:story_reply_dm`, set up with the `automations` skill. Someone who mentions the account in their own story can get a thank-you: `template:story_mention_thanks`.
- Poll votes and other sticker answers do not arrive as messages, so no automation sees them. Those people are answered by hand in the app.
- Answering by hand inside an open conversation is the `inbox` skill. The window rules are `faq:dm-24h-window`.
- A DM to someone who does not follow the account lands in their message requests and carries text only (`faq:dm-non-follower-media`). Write the reply so the text alone works.

## Without Uplika

Print the frames as above. The person builds and posts them from the Instagram app, stickers included, and replies by hand.

## Tools

- `select_channels`: pick the Instagram account; returns the accountIds
- `list_platforms`: image and video rules and the option schema (no sticker fields)
- `media_presign`: upload slot when you can PUT the file yourself
- `media_complete`: confirm that upload
- `media_from_url`: attach an image or video from a public https address
- `media_upload_link`: let the person upload from their own device
- `media_upload_status`: wait until that upload is ready
- `publish`: one call per frame, only after the person approves
- `get_post`: status of each frame
- `get_help`: the answer for an error code
