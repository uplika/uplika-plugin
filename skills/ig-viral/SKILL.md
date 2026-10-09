---
name: ig-viral
description: Find Instagram reels that beat their own account's median views, name each hook formula, and build a swipe file from examples you paste.
---

Adapted from Jakeschincariol/instagram-agent-skill (MIT). Not affiliated with the original author.

# ig-viral

Use when the person says "find viral videos", "what's working right now", "what are people posting in my niche", "reverse engineer this account", "build me a swipe file", "why is this reel doing numbers", or asks what to make next and has no evidence to answer with.

The research skill. Everything else in this pack writes; this one studies what is already working. Run it monthly, not daily. Formulas last a season.

One script lives in this skill's `scripts/` folder and it runs. From this skill's folder:

```bash
python3 scripts/swipe.py captured.tsv --out swipe.md
```

It reads the hook formulas and the hook scorer from the `ig-reel` skill's `scripts/` folder, so keep both skills installed side by side. Without a terminal it cannot run: rank the rows by hand with the same arithmetic and say the script was not run.

## The one idea that makes this worth doing

**Raw views are not evidence.** An account with two million followers doing 400,000 views had a quiet Tuesday. An account with four thousand followers doing 400,000 views found something, and that something is copyable.

So everything here ranks on the **outlier multiple**: views divided by that account's own recent median. Anything above 3x is a signal. Anything below 1.5x is that account's normal day and it teaches you nothing, no matter how big the number looks.

Collect accounts **within about 10x of the person's own size**. A formula that works at 2M followers often works because it is at 2M followers.

## Step 1: pick the accounts

Ask the person for 6 to 12 accounts, or propose them and get approval:

- **4 direct**: same niche, same offer, slightly ahead.
- **4 adjacent**: different niche, same audience. This is where formats get borrowed from before anybody in the niche has them.
- **2 to 4 outsized**: much bigger accounts, for format only, never for cadence or tone.

Also ask them to open their own **Saved collection**. It is the fastest and most relevant corpus that exists and it is already filtered by their taste.

## Step 2: the person collects, you read

Uplika has no Instagram search, and its tools read only the person's own connected accounts. So the rows come from the person: they open each account in their own Instagram app or browser, look at the last dozen reels, and paste what they see. Small volume is the point. Ten accounts, a dozen reels each, is enough to read.

**Rules that are not negotiable:**

- **Never log into Instagram on the person's behalf and never ask for a password.**
- **Do not drive a browser through Instagram and do not scrape.** Automated collection violates Instagram's Terms of Use and gets accounts action-blocked. Do not build a crawler, do not use a scraping service, and do not loop this in the background. If the person cannot collect the rows, work with fewer and say so.
- **Copy the formula, never the video.** The hook shape, the structure, the length, the pattern of cuts. Not their script, not their voice, not their edit. Attribute every row in the swipe file to the account it came from.

**What to capture per reel**, in the creator's own words:

| field | notes |
| --- | --- |
| account | handle |
| followers | from the profile |
| median | eyeball the last 12 reels and take the middle view count |
| views | this reel |
| hook | the first line, spoken or on screen, verbatim including bad grammar |
| on-screen | the first text card, if different |
| length | seconds |
| cta | what they asked for at the end |

Median is the important one. Without it you are back to ranking by follower count, which is the thing this skill exists to stop.

**When Instagram will not show enough:** the same hook grammar runs on YouTube Shorts, where view counts and transcripts are public and no login is involved. With a terminal it is a legitimate second corpus, and the spoken hook is easier to get:

```bash
# view counts for a channel's shorts
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@HANDLE/shorts" > channel.json

# the spoken first line of one short, from its auto-captions
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "en.*" \
  --sub-format json3 -o hook "https://www.youtube.com/watch?v=VIDEO_ID"
```

Take every caption word with a timestamp under 3.0 seconds. That is the hook, as said, not as written. Without a terminal, the person pastes these too.

## Step 3: rank it

Fill a tab-separated file with a header row and run the script:

```
account	followers	median	views	hook
@someone	48000	11000	412000	nobody tells you your first 30 reels are supposed to flop
```

```bash
python3 scripts/swipe.py captured.tsv --out swipe.md
```

It computes the outlier multiple, names the hook formula using the same 26 formulas `ig-reel` writes from, scores each hook with the `ig-reel` hook scorer, and prints what separates the top third from the bottom third. The classifier and the scorer read English: on Korean hooks they abstain or score on digits alone, so rank Korean rows by the multiple and name their formulas by reading.

## Step 4: say what it means, carefully

Report three things and no more:

1. **Which formulas over-index** in the top third, with counts. Two formulas appearing four times each across six accounts is a finding. One appearing twice is not.
2. **What the top third have in common structurally** that the bottom third do not: hook length, whether the payoff is visual, whether the first frame moves, where the ask is.
3. **The unclassified rows.** Every hook the classifier could not name is either noise or a formula that is not in `ig-reel`'s `scripts/hooks.json` yet. Read them by hand. This is the most valuable column in the output and it is the reason the script prints the count.

Then state the sample size and the confidence in plain words. Forty reels across six accounts supports a claim. Twelve does not, and saying so is the difference between research and horoscopes.

## Step 5: turn it into something to shoot

For the top three formulas, write **the person's version**: their own story, their own number, in the shape that is working. Hand each one to `ig-reel` with the formula id already chosen.

Never hand back "make a reel like this one". Hand back a hook line they could say tomorrow.

## Output

```
SWIPE  ·  38 reels  ·  7 accounts  ·  baseline: account median

OUTLIERS (above 3x)
  38.4x  hook 86  #3  Nobody Tells You   @acct_a    412,000  (median 10,700)
  11.2x  hook 79  #9  The Steal          @acct_c    180,000  (median 16,100)
  ...

WHAT IS OVER-INDEXING
  #3 Nobody Tells You   x5 in the top third, 0 in the bottom
  #2 Negative Command   x4
  median hook length    8 words up top, 19 at the bottom

UNCLASSIFIED (6)
  Two of these are the same shape and it is not in hooks.json: a hook that
  opens on someone else's comment read out loud. Worth adding.

YOUR VERSION
  #3  "Nobody tells you the first 20 proposals are supposed to lose."
  ...
```

Write the swipe file where the person wants it (`--out`; a bare file name lands in the current folder) and tell them the path. `ig-reel` reads it when they point to it, which is the point: after this runs once, the reels are written from the person's own evidence instead of from defaults.

Nothing is posted, followed, liked or messaged by this skill. It reads what the person gives it.

## With Uplika connected

Nothing in the collection changes: Uplika has no Instagram search, so the person still pastes the examples. Their own numbers are a different job: the `ig-audit` skill reads the person's posts and insights through Uplika, and comparing its multiples with this swipe file shows which formulas work for their account, not just for the niche.

## Without Uplika

This skill runs exactly as above with nothing connected.

## Tools

None. Uplika has no Instagram search, so the person pastes the examples and the script runs locally.
