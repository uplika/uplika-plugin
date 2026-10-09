---
name: ig-carousel
description: Build an Instagram carousel (a cover that earns the swipe, slide copy, rendered slides) and publish it as one feed post after approval.
---

Adapted from Jakeschincariol/instagram-agent-skill (MIT). Not affiliated with the original author.

# ig-carousel

Use when the person says "carousel", "slides", "swipe post", "turn this into a carousel", or has a list-shaped or step-shaped idea that would die as a single image.

Carousels are the highest-dwell format on the grid, because a swipe is an interaction and a scroll is not. They also get a second chance: Instagram can show a carousel again starting from a later slide to someone who did not engage the first time, so slide two has to stand on its own as well.

The format rewards one idea broken into steps. It punishes a caption cut into pieces.

Read the voice file `~/.uplika/<workspace-slug>/voice.md` first if it exists. If it does not, ask three questions (tone, how they end a line, words they avoid) and offer to save the answers with the `voice-profile` skill.

## When to use it instead of a Reel

Use a carousel when the idea has **sequence and needs to be re-read**: steps, a framework with parts, a before and after, a list worth screenshotting. Use a Reel when the idea has motion, a face, or a payoff that has to be seen happening.

If the idea is one claim, it is neither. Hand it to `ig-reel` and say so.

## Structure

6 to 10 slides. The most one post can carry is in `list_platforms`, and a deck anywhere near it is a book nobody finishes. Under 5 and the swipe never starts.

```
1         COVER     the hook. 6 words or fewer, at a size that is legible in
                    the grid at thumbnail. One line of promise under it.
2         THE STAKE why this matters, in one sentence. This slide is also a
                    second cover, so it cannot be setup.
3 to N    ONE IDEA PER SLIDE. A headline of 3 to 7 words, at most 25 words
                    under it. If a slide needs a paragraph, it is two slides.
N+1       RECAP     the whole thing as a list. This is the screenshot slide.
LAST      CTA       one action. Save, comment a keyword, or follow. One.
```

## Slide copy rules

- **The cover is 80% of the result.** Six words. Big. Nothing on the deck saves a cover nobody swipes.
- **Design for the grid crop.** The profile grid crops to a portrait rectangle that is taller than it is wide, and the exact ratio has moved more than once. Build every slide at one portrait size and keep the cover text well inside the middle, clear of the edges, and the crop stops mattering.
- **Number the slides** (3/8). Completion goes up when people can see the end.
- **No slide is a paragraph.** If it cannot be said in 25 words, split it.
- **The recap slide is the one people screenshot and send.** Sends are the strongest signal you can earn. Make it standalone and readable with no context.
- **The handle on every slide**, small, bottom corner. Screenshots travel without you.
- **Alt text on the cover at minimum.** It is read by screen readers and by Instagram.

## Building the files

One image per slide, every slide the same portrait size. The aspect range the feed accepts is stated in the `publish` tool's description. A slide outside it is not refused: Uplika's server center-crops a copy to the nearest edge of the range and the post's warning says so, which cuts off whatever sat near the edges. Build inside the range and nothing is cut. Image types and how many items one post takes are in `list_platforms`.

Build it as HTML and render each slide to an image:

```bash
# one <section> per slide at the chosen fixed size, page-break-after: always
# then a headless Chrome screenshot per slide, or any HTML-to-image you already use
```

Write the HTML at that fixed size, with a single accent colour, and type no smaller than 32px, because this is read on a phone at a third of its real size. If the project has a brand skill or a design system, use it and do not invent a palette. Rendering needs a terminal. Without one, give the person the approved copy and they build the slides in their own design tool.

## Output

The slide-by-slide copy first, as a numbered list the person can read in ten seconds and edit before anything is rendered. Then the **caption**, which for a carousel is Job B in `ig-caption`: the caption is doing work here, because the cover has already used its six words.

Run both through `ig-human`. Build the files only after the person approves the copy.

```
CAROUSEL  ·  8 slides

1  COVER   THE $18,000 CLAUSE
           One line I now put in every contract.
2  STAKE   I approved the work. They asked for the money back nine days later.
3          WHAT IT SAYS
           Payment on delivery, not on approval.
...
7  RECAP   All four lines, in order.
8  CTA     Comment CONTRACT and I will send the full clause.

Caption: Job B, hook in line 1, one ask, 3 tags.
```

## With Uplika connected

1. **Account.** Call `select_channels` with the Instagram account, or with no scope and let the person choose. Never assume Instagram is connected; if it is not, send the person to https://uplika.com/dashboard/connections. If the answer is `workspace_required`, show the workspaces it lists, ask which one, and pass that `workspaceId` on every later call.
2. **Rules.** Read Instagram in `list_platforms`: how many items one post takes, image types, the caption rules and the features table. Instagram posts cannot be edited after they go out (the features table says so), so the slides, their order and the caption are approved first.
3. **Upload each slide, in order.** With a terminal: `media_presign` with the file name, type and size, PUT the bytes to the returned `uploadUrl` with curl, then `media_complete`. Without one: `media_from_url` for files at a public https address, or `media_upload_link` for files on the person's device (give them the link, then poll `media_upload_status` until it is ready). Write `altText` for each slide, the cover at minimum. Pass `aiGenerated` for images made with AI. Keep the media ids in slide order: that order is the swipe order.
4. **Show and confirm.** Show the slides in order, the caption, any first comment, collaborators and tags, the account and the time. Publish only after the person approves.
5. **Publish.** Call `publish` with the `accountIds` from `select_channels`, `content` (the caption), `mediaIds` in slide order, and `wait: true`. Several media ids on one feed post is the carousel: set `options.instagram.contentType` to `feed`, or leave it out. Optional: `options.instagram.collaborators` (they appear only after they accept), `options.instagram.firstComment`, and `options.instagram.userTags` (`mediaIndex` picks the slide; a photo tag also needs a position, see the option schema). For a later time pass `scheduledAt` with a time zone offset, and ask which time zone the person means.
6. **Report.** Call `get_post`: status, permalink and warnings. Read every warning to the person, such as a slide that was cropped, or items left out because the post took fewer than were sent (the first ones go out). If it failed, call `get_help` with its code and pass on the answer and its url. `reconsent_required`, `feature_in_review` and `account_disconnected` go to the `troubleshoot` skill.

## Without Uplika

The person renders or exports the slides and posts them from the Instagram app, with the caption pasted in.

## Tools

- `select_channels`: pick the Instagram account; returns the accountIds and limits
- `list_platforms`: item count, image rules, caption rules, the features table
- `media_presign`: upload slot when you can PUT each slide yourself
- `media_complete`: confirm each upload
- `media_from_url`: attach slides from public https addresses
- `media_upload_link`: let the person upload the slides from their own device
- `media_upload_status`: wait until that upload is ready
- `publish`: publish or schedule the carousel, only after the person approves
- `get_post`: status, permalink and warnings (crops, items left out)
- `get_help`: the answer for an error code
