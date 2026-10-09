---
name: ig-profile
description: Score an Instagram profile out of 100 on a 12-part rubric, then rewrite what lost points (name field, bio, pinned posts, highlights, link, grid).
---

Adapted from Jakeschincariol/instagram-agent-skill (MIT). Not affiliated with the original author.

# ig-profile

Use when the person says "optimize my profile", "fix my bio", "score my Instagram", "why don't people follow me", or pastes their profile and asks how it reads.

Almost everybody optimises the wrong thing here. The profile is not a storefront people browse. It is a **decision screen**, arrived at from one reel, and it gets about three seconds to answer one question: is there more of that here, and is it for me.

Read the voice file `~/.uplika/<workspace-slug>/voice.md` first if it exists, so the rewrites sound like the person. If it does not, ask three questions (tone, how they end a line, words they avoid) and offer to save the answers with the `voice-profile` skill.

## Input

Ask the person to paste or screenshot: the name field, the handle, the bio, what the link points to, the highlight names, what is pinned, and the first nine grid covers. A screenshot of the top of the profile plus the first two grid rows is enough for a first pass. With Uplika connected, part of this comes from the tools (see below); the profile fields themselves still come from the person.

Do not log into Instagram on their behalf.

## Score it

Read `references/rubric.json` in this skill's folder. Twelve items, 100 points, each with what full marks looks like and how it usually fails. Score every item, show the table, give the total. Be honest. Most profiles land in the 30s and 40s on the first pass and a generous score is useless.

```
PROFILE SCORE  38/100

  name field       2/12   name only, no words anyone searches
  bio first line   3/12   three nouns and a coffee emoji
  pinned three     0/10   nothing pinned
  highlights       2/8    "Random", "Life", "2023"
  grid legibility  4/8    six of nine covers are a face mid-sentence
  ...
```

## Then rewrite, in this order

Fix in descending order of points lost. Do not rewrite everything at once: the person has to actually go and change each of these.

**1. The name field.** The bold line under the photo, not the handle. This is the field Instagram search matches against, and most accounts put a name in it and nothing else. Format that works: `{Name} | {what you do, in searched words}`. Give three options, each short enough to fit the field (Instagram shows the count while they type).

**2. Bio line one.** Who this is for and what changes. Not a job title, not adjectives, not a pipe-separated list of identities. The rest of the bio carries one piece of proof or one plain offer.

**3. The pinned three.** Three slots, three different jobs: the best proof, the clearest explanation of the offer, the best introduction to the person. This is the highest-leverage fix on the whole profile and it takes four taps. An unpinned grid shows whatever was posted last, which is a coin flip.

**4. Highlights.** Four to six, named for the questions a buyer asks: Pricing, Results, How it works, About. Not "Random". Delete the rest.

**5. The link.** One destination that matches what the bio just promised. Two is already a menu, and a menu converts worse than a door.

**6. Grid covers.** The first nine at thumbnail size. Reel covers get chosen, not left as whatever frame one was. Four words of text on a cover makes a grid readable in one glance.

## Output

Score table, then the rewrites as copy-ready blocks in fix-first order, each run through `ig-human`. Re-score at the end and show the delta honestly. If the rewrite reaches 84 and not 98, say 84, and say what the rest needs, which is usually a grid, a story habit and a pinned post that does not exist yet. None of that is a rewrite.

Nothing is saved to Instagram by this skill. The person edits each field.

## With Uplika connected

1. **Account.** Call `list_accounts` and find the Instagram account. Never assume it is connected; if it is not, send the person to https://uplika.com/dashboard/connections. If the answer is `workspace_required`, show the workspaces it lists, ask which one, and pass that `workspaceId` on the next calls. The entry gives the handle, and the display name and profile photo as Uplika last stored them, so ask the person for the current name field and bio.
2. **Grid and recent activity.** Call `list_channel_posts` with that account's id. Each post comes with its caption, time, type, permalink and thumbnail. The newest posts are the top of the grid: look at their thumbnails for the grid-legibility item and use the dates for the recent-activity item. The response does not mark pinned posts, so ask which three are pinned.
3. **What stays manual.** Uplika has no tool that reads or changes the name field, bio, link, highlights or pins. The person makes every edit in the Instagram app.
4. **Two follow-ups this skill can hand off.** New reels get a chosen cover with `options.instagram.coverMediaId` when they are published through `ig-reel`. If the person wants the link to open a conversation instead of a web page, an ig.me link plus `template:referral_welcome` greets whoever arrives; the `automations` skill sets that up.

## Without Uplika

Work from what the person pastes or screenshots, as in Input above.

## Tools

- `list_accounts`: the connected Instagram account, its handle, and the name and photo Uplika last stored
- `list_channel_posts`: the newest posts with thumbnails, captions and dates, for the grid and recent activity
