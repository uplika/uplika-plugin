---
name: yt-script
description: "Write a YouTube script from an idea: five hooks off 21 formulas, scored, then the spoken script with retention beats. For scripts, hooks, openings."
---

Adapted from Jakeschincariol/youtube-agent-skill (MIT). Not affiliated with the original author.

# yt-script

One idea into a script somebody finishes. Use it whenever the person wants a video script, a hook, an opening line, "what should I say", "write my next video", or is about to record and does not have the first fifteen seconds yet.

Two tools live in this skill's `scripts/` folder and both actually run. Use them. Do not eyeball the hook. From this skill's folder:

```bash
python3 scripts/hookscore.py hooks.txt              # rank your hook options
python3 scripts/hookscore.py --hook "one line"      # score a single one
```

`scripts/hooks.json` holds the 21 formulas the score classifies against. Without a shell (claude.ai, ChatGPT) the script cannot run: check the hooks against the formulas by hand and say they were not scored.

## Before you write

1. Read `~/.uplika/<workspace-slug>/voice.md` if it exists. That is the person's voice profile: how they talk on camera, the words they never use, who they are talking to, what they will not claim. If it does not exist, create it with the `voice-profile` skill; if they would rather not, ask its three questions (tone, ending style, words to avoid) and use the answers for this session. A script in the wrong voice is worse than no script, because they have to read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have one, ask for it or write the line without it.

## With Uplika connected

If a call answers `workspace_required`, the account has more than one workspace: show the names it lists, ask which one, and pass that `workspaceId` on every later call in this session.

Optional, before the hooks: call `search_youtube_videos` with the idea as a viewer would type it (`q`), `order` viewCount, a recent `period`, and the idea as `topic`. The top titles, and the ones with a high `viewSubRatio` (views over subscribers), are openings this niche already answered, and the answer's `prompt` is a brief for titles and hooks you may follow. Treat them as examples. Still write your own five against the formulas and score them.

- `research_tool_disabled`: only a research tool still in beta answers this. Ask the person once to turn it on at the `enableUrl` in the error, and do not retry until they say it is on. Write the script without it meanwhile.
- `research_quota_exceeded` (their own daily searches) or `youtube_quota_exhausted` (the shared quota, back at `resetsAt`): skip the search and write without it.
- Any other error: call `get_help` with its code and pass the answer on.

## Without Uplika

Work from the idea alone: the person describes it and you write. If they want real examples first, use the `yt-viral` skill or ask them to paste a few titles from the niche.

## The shape

**The first 15 seconds is the whole job.** It does three things or the video leaks: confirm the click the title promised, open a question the viewer cannot close, and prove the payoff exists.

1. **Hook.** Write FIVE against [the 21 formulas](scripts/hooks.json), run them through `scripts/hookscore.py`, keep the top two, and show the person both with their scores. Never hand over one hook.
2. **The turn** (0:15-0:45). Say what the video is going to do, in one sentence, and start doing it. No channel intro, no "before we get started", no subscribe pitch. Those are the single most common cause of the 0:30 cliff.
3. **The body.** One idea per beat. Mark each beat with what is ON SCREEN, not just what is said: a talking head with nothing to look at is a podcast.
4. **The payoff.** Deliver the thing the hook promised, explicitly, and say that you are delivering it: "that is the prompt, it is in the description".
5. **The close.** One ask. Not three.

## Korean hooks

`hookscore.py` reads Korean (any Hangul in the line): Korean word lists, length counted in syllables, and Korean patterns for the formulas. It prints `Korean: heuristic, not calibrated` and gives no STRONG, WORKABLE or WEAK band, because nothing like the 74 English hooks behind the English panel exists for Korean yet. Use the numbers to rank Korean hooks against each other, never to call one strong or weak, and say so when you show them.

## What to hand back

- the two best hooks with their scored panels
- the script, beat by beat, with `[ON SCREEN: ...]` on every beat
- the runtime estimate: English at 150 words per minute; Korean at 306 syllables per minute (5.1 a second, measured on Uplika's own reels), counting Hangul syllables rather than words
- one line naming which formula the winning hook used and why it fits this idea

When the video is recorded, `yt-package` writes the title and thumbnail and `yt-upload` puts it up.

## The gate

Nothing here publishes. This skill writes and the person publishes. Every output ends in a block they copy, and the last line of every run is the question: **ship it, or change it?**

## Tools

- `search_youtube_videos`: optional, real titles and openings from the niche before writing hooks
- `get_help`: the answer for any other error code
