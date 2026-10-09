---
name: ig-audit
description: Instagram post-mortem from real insights. Rank posts by multiple over your median views, find what separates hits from misses, say what to stop.
---

Adapted from Jakeschincariol/instagram-agent-skill (MIT). Not affiliated with the original author.

# ig-audit

Use when the person asks "what's working", "why did this flop", "read my analytics", "audit my content", or wants to know what to do more of.

The only honest source of what works for an account is that account. Every rule in every Instagram guide, including the ones in this pack, is a prior. The person's own last 30 posts are the evidence.

## Input

With Uplika connected, the posts and the numbers Uplika reports come from the tools (see "With Uplika connected"). Everything else comes from the person, and the same list is the whole input when nothing is connected. Ask for whichever they have:

- Insights per post from the Instagram app: views, reach, interactions, watch time, saves, shares, follows, and the non-follower share of reach. Screenshots are fine.
- Or the retention graph for their best and worst recent reels. This one screenshot is worth more than the rest combined.
- Or just the posts and their view counts, which is enough for a first pass.

## What to actually measure

Raw views is the least useful number on the page, because it is mostly a function of how many people already follow the account. Compute these instead and show the working:

| metric | how | what it tells you | where it comes from |
| --- | --- | --- | --- |
| **Outlier multiple** | views / the account's own median views | whether this was a real hit or a normal day | Uplika (views per post) or the app |
| **Non-follower reach** | % of reach from people who do not follow | whether it travelled at all | the app only |
| **Hold at 3s** | viewers still there at 3s / viewers who started | whether the hook worked. This is the hook's grade. | the app only (retention graph) |
| **Average watch time** | straight from insights | whether the middle worked | the app only |
| **Sends per reach** | shares / reach | the strongest single signal you can earn. A send is a person putting their name on it. | the app; Uplika has shares and views but no reach |
| **Follows per reach** | follows / reach | whether the profile converted the attention | the app only |

Rank by outlier multiple and sends per reach, not views. A reel with 4,000 views and 90 sends beat the one with 60,000 views and 11. When only Uplika's numbers are available, shares per view is the closest stand-in: say that it is a different measure from sends per reach.

## Then find the pattern

With the top five and bottom five side by side, look for what separates them, and be willing to conclude something the person will not like:

- **Hold at 3 seconds.** If the top and bottom differ here, it is the hook and nothing else, and everything downstream is a distraction.
- **Hook formula.** Which formulas from the `ig-reel` skill's `scripts/hooks.json` are in the top five? Read the first line of each caption, and ask the person what each reel said first, since the spoken hook is not in the caption.
- **Format.** Reel, carousel, single image.
- **Length.** Group into under 15s, 15 to 30s, 30 to 60s, over 60s. Uplika's answer does not include video length, so ask the person or skip it.
- **Theme.**
- **Whether the person replied to comments in the first hour.**
- **Day and time.** Check this **last** and only if the others show nothing. It is almost never the cause and it is where people want it to be.

State the finding as a claim with the evidence attached, and say how confident it is. With 30 posts you can see a pattern. With 6 you cannot, and saying so is better than inventing one.

## The distinction that saves people months

**A reel that gets views and no follows is not a failed reel, it is a profile problem.** A reel that gets no views is a hook problem. Separate the two before recommending anything. If non-follower reach is high and follows per reach is low, stop rewriting hooks and go to `ig-profile`.

## Output

```
AUDIT  ·  31 posts  ·  Jun 12 - Sep 5  ·  median views 4,100

TOP 5 BY OUTLIER MULTIPLE
  18.2x  #3  Nobody Tells You   74,600 views  62% non-follower  hold@3s 71%  128 sends
   6.4x  #1  Cost Confession    26,300 views  48% non-follower  hold@3s 64%   71 sends
  ...

BOTTOM 5
   0.3x  #11 Numbered            1,200 views  9% non-follower   hold@3s 31%    2 sends
  ...

WHAT THE DATA SAYS
1. Hold at 3 seconds is the whole story. Top five average 66%, bottom five 33%.
   Everything else you are worried about is downstream of the first two seconds.
2. The posts where you were the one who looked bad: mean 8.1x vs 0.9x for
   everything else. n=5. Strongest signal here and it is not close.
3. Tool listicles get views and nothing else. High reach, no sends, no follows.
   Three of your bottom five.
4. Day of week shows nothing. Your Tuesday and Friday means are inside the
   noise. Stop optimising it.

STOP: listicles.
DO MORE: the ones with a cost you paid and a number attached.
```

Mark every column that came from the person rather than from Uplika, and every post where a number was missing.

Then hand the conclusions to the `schedule-week` skill, so next week is built on the person's own evidence rather than on defaults, and to `ig-viral`, so the swipe file gets filtered to the formulas that work for this account specifically.

## With Uplika connected

1. **Account.** Call `list_accounts` and find the Instagram account. Never assume it is connected; if it is not, send the person to https://uplika.com/dashboard/connections. If the answer is `workspace_required`, show the workspaces it lists, ask which one, and pass that `workspaceId` on the next calls.
2. **Posts.** Call `list_channel_posts` with that account's id and a limit that covers the period you are auditing. Each post comes with its caption, time, type, permalink and thumbnail, including posts made in the Instagram app. The type tells a reel from a feed post; it does not tell a carousel from a single image, so look at the post or ask.
3. **Numbers.** For each post, call `get_insights` with its permalink. Instagram reports views, likes, replies (comments) and shares there. A null means Instagram did not report that number: it is not zero, so leave it out of the median and say how many posts were missing it.
4. **Compute** the median views, each post's multiple over it, and shares per view.
5. **Ask for the rest.** Reach, the non-follower share, saves, follows, average watch time and the retention graph (hold at 3 seconds) are not in Uplika's answer. Ask for screenshots of the best and worst reels at minimum.

## Without Uplika

Use whatever the person pastes, as in Input above. A first pass on views alone is still worth doing; say what it cannot show.

## Tools

- `list_accounts`: find the connected Instagram account
- `list_channel_posts`: the posts on the account (caption, time, type, permalink, thumbnail)
- `get_insights`: views, likes, replies and shares for one post (null is not zero)
